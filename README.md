# TTL Exfiltration Monitor

> A lightweight CLI tool that sniffs network packets, detects anomalously low TTL values, and automatically scans suspicious sources with Nmap.

---

## What is it?

Low TTL values in IP packets are a common indicator of **Traceroute activity** or **covert tunneling**. This tool passively monitors all inbound traffic, flags any packet with a suspiciously low TTL, and immediately launches an Nmap scan against the source IP to gather further intelligence — all in real time.

---

## Project Overview

This tool implements a raw-socket packet sniffer that inspects the TTL field of every captured IP packet. When a packet's TTL falls below the configured threshold, the tool alerts the operator and triggers an automated Nmap service scan against the suspicious source IP to help identify what is running on that host.

---

## How It Works

1. **Permission Check** — Verifies the tool is running as root (Linux) or Administrator (Windows)
2. **Packet Sniffing** — Captures raw IP packets from the network interface
3. **Header Parsing** — Extracts TTL, protocol, Source IP, and Destination IP
4. **TTL Check** — Flags any packet with TTL below the threshold (default: 10)
5. **Nmap Scan** — Automatically scans the suspicious source IP for open ports and services

---

## Technologies Used

| Library | Purpose |
|---|---|
| `socket` | Raw socket creation and packet capture |
| `struct` | Binary unpacking of IP header fields |
| `os` | OS detection for cross-platform support |
| `sys` | Clean exit on permission failure |
| `subprocess` | Launching Nmap as a child process |
| `datetime` | Timestamping alerts |

---

## Project Structure

```
Network-Automation-Project/
│
├── ttlsniffer.py                          
├── README.md                              
└── TTL-Exfiltration-Monitor-Report.pdf   
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/M3nsho/Network-Automation-Project.git
cd Network-Automation-Project
```

### 2. Install Nmap

**Linux:**
```bash
sudo apt install nmap
```

**Windows:**  
Download from [https://nmap.org/download.html](https://nmap.org/download.html)

> No additional Python libraries are required — all dependencies are part of the Python standard library.

---

## How to Run

**Linux (requires root):**
```bash
sudo python3 ttlsniffer.py
```

**Windows (run as Administrator):**
```bash
python ttlsniffer.py
```

---

## Sample Output

```
[+] Permission checked.
[*] Sniffing started. TTL threshold: 10

[!] [14:32:07] LOW TTL DETECTED
    SRC:192.168.1.45 -> DST:192.168.1.1
    TTL:5  | Protocol:1
 [>] Launching Nmap scan on 192.168.1.45 ...

Starting Nmap 7.93 ( https://nmap.org )
Nmap scan report for 192.168.1.45
PORT    STATE  SERVICE  VERSION
22/tcp  open   ssh      OpenSSH 8.9
80/tcp  open   http     Apache httpd 2.4.52
Nmap done: 1 IP address scanned in 8.43 seconds
```

---

## ⚠️ Ethical & Legal Notice

This tool is intended **strictly for use on networks you own or have explicit written permission to monitor**. Unauthorized packet sniffing and port scanning may violate laws such as the Computer Fraud and Abuse Act (CFAA) or equivalent legislation in your country. Use responsibly.

---

## License

This project is for educational purposes only.
