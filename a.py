#!/usr/bin/env python3
import time
import subprocess
import os

FILE = "/tmp/a.sh"
INTERVAL = 3  # 3 detik

current_process = None

def run_script():
    global current_process

    # Kalau masih jalan, jangan spawn ulang
    if current_process and current_process.poll() is None:
        return

    current_process = subprocess.Popen(
        [FILE],  # <-- eksekusi langsung ./a.sh
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    # Pastikan executable
    os.chmod(FILE, 0o755)

    while True:
        run_script()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
