import socket
import struct
import os
import sys
import subprocess
from datetime import datetime

#Default Configurations
TTL_THRESHOLD = 10
NMAP_FLAGS = "-sV"

#Check for permissions
def check_permissions():
    if os.name == 'nt':
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("[!] Not running as Administrator.")
            sys.exit(1)
    else:
        if os.geteuid() != 0:
            print("[!] Not running as root. Please re-run with: sudo python3 ttlsniffer.py")
            sys.exit(1)
    print("[+] Permission checked.")

#Parse IP Header
def parse_ip_header(data):
	ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
	ttl = ip_header[5]
	protocol = ip_header[6]
	src_ip = socket.inet_ntoa(ip_header[8])
	dst_ip = socket.inet_ntoa(ip_header[9])
	return ttl, protocol, src_ip, dst_ip

#Nmap Scanning
def nmap_scan(ip):
    print(f" [>] Launching Nmap scan on {ip} ...")
    try:
        result = subprocess.run(
            ["nmap"] + NMAP_FLAGS.split() + [ip],
            capture_output=True, text=True, timeout=60
        )
        print(result.stdout)
    except FileNotFoundError:
        print("[!] Nmap not found. Install it with: sudo apt install nmap")
    except subprocess.TimeoutExpired:
        print("[!] Nmap scan timed out.")

#SNIFF
def sniff_packets():
	try:
		if os.name == 'nt':
			s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
			s.bind((socket.gethostbyname(socket.gethostname()), 0))
			s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
			s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
		else:
			s= socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
		print(f"[*] Sniffing started. TTL threshold: {TTL_THRESHOLD}\n")
		
		already_scanned = set()
		while True:
			raw_data, _ = s.recvfrom(65535)
			
			ip_data = raw_data[14:] if os.name != 'nt' else raw_data
			if len(ip_data) < 20:
				continue
			
			ttl, protocol, src_ip, dst_ip = parse_ip_header(ip_data)
			if ttl < TTL_THRESHOLD:
				timestamp = datetime.now().strftime("%H:%M:%S")
				print(f"[!] [{timestamp}] LOW TTL DETECTED")
				print(f"    SRC:{src_ip} -> DST:{dst_ip}")
				print(f"    TTL:{ttl}  | Protocol:{protocol}")
				
				if src_ip not in already_scanned:
					already_scanned.add(src_ip)
					nmap_scan(src_ip)
	
	except KeyboardInterrupt:
		print("\n[*] STOPPING!")
		if os.name == 'nt':
			s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
		s.close()

if __name__ == "__main__":
    check_permissions()
    sniff_packets()