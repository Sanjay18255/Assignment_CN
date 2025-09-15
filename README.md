# DNS Resolver Assignment

##  Overview
This project implements a DNS Resolver using a client–server model.

- The **client** reads DNS queries from a PCAP file (`9.pcap`), adds a custom header, and sends them to the server.  
- The **server** extracts the header, applies predefined rules, and returns a resolved IP address from a pool of 15 IPs.  
- The **report** is generated in the required format (`dns_report.txt`).

##  Custom Header Format
Each DNS query has an **8-byte custom header**:
- Format: `HHMMSSID`
  - `HH` → Hour (24h format)  
  - `MM` → Minute  
  - `SS` → Second  
  - `ID` → Query sequence number (00, 01, …)  

Example: `18041600` → Hour=18, Minute=04, Second=16, ID=00.

## ⚙️ Server Rules
- **IP Pool (15 addresses):**
  192.168.1.1 → 192.168.1.15
- **Routing logic:**
  - Morning (04:00–11:59) → use IPs [1–5]  
  - Afternoon (12:00–19:59) → use IPs [6–10]  
  - Night (20:00–03:59) → use IPs [11–15]  
- Final index is chosen by:
  pool_start + (ID % 5)

---

##  Quick Run

# 1. Create venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Start server (Terminal A)
python3 server.py --host 0.0.0.0 --port 55556

# 3. Run client (Terminal B) with 9.pcap
python3 client.py --pcap 9.pcap --host 127.0.0.1 --port 55556 --out results.csv

# 4. Generate final report
python3 generate_report.py results.csv dns_report.txt

---

##  Output Example
[CLIENT] facebook.com -> 192.168.1.6 (Header=18041600)  
[CLIENT] stackoverflow.com -> 192.168.1.7 (Header=18041601)  
[CLIENT] example.com -> 192.168.1.8 (Header=18041602)  
[CLIENT] linkedin.com -> 192.168.1.9 (Header=18041603)  
[CLIENT] apple.com -> 192.168.1.10 (Header=18041604)  
[CLIENT] google.com -> 192.168.1.6 (Header=18041605)  

---

##  dns_report.txt (final report)
CustomHeader   Domain            ResolvedIP  
18041600       facebook.com      192.168.1.6  
18041601       stackoverflow.com 192.168.1.7  
18041602       example.com       192.168.1.8  
18041603       linkedin.com      192.168.1.9  
18041604       apple.com         192.168.1.10  
18041605
