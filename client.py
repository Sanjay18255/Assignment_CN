import argparse
import socket
import datetime
from scapy.all import rdpcap, DNS, DNSQR

# The required 6 domains to query
TARGET_DOMAINS = [
    "facebook.com",
    "stackoverflow.com",
    "example.com",
    "linkedin.com",
    "apple.com",
    "google.com",
]

def build_custom_header(seq_id: int) -> str:
    """Build 8-byte custom header: HHMMSSID"""
    now = datetime.datetime.now()
    return now.strftime("%H%M%S") + f"{seq_id:02d}"

def normalize(qname: bytes) -> str:
    """Convert query name from bytes to lowercase string without trailing dot"""
    try:
        return qname.decode().rstrip('.').lower()
    except Exception:
        return "unknown"

def main():
    """Main client function: parse PCAP, send DNS queries, receive IPs, save CSV"""
    parser = argparse.ArgumentParser(description="DNS Resolver Client")
    parser.add_argument("--pcap", required=True, help="Input pcap file")
    parser.add_argument("--host", required=True, help="Server host")
    parser.add_argument("--port", type=int, required=True, help="Server port")
    parser.add_argument("--out", default="results.csv", help="Output CSV file")
    args = parser.parse_args()

    # Read packets from pcap file
    pkts = rdpcap(args.pcap)
    found = {}
    for pkt in pkts:
        # Filter only DNS query packets
        if not pkt.haslayer(DNS) or pkt.qr != 0 or pkt.qd is None:
            continue
        qname = normalize(pkt[DNSQR].qname)
        if qname in TARGET_DOMAINS and qname not in found:
            found[qname] = qname
        if len(found) == len(TARGET_DOMAINS):
            break

    results = []
    for idx, domain in enumerate(TARGET_DOMAINS):
        # Build header and payload
        header = build_custom_header(idx)
        payload = header.encode("ascii") + domain.encode("ascii")

        # Send to server and receive resolved IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((args.host, args.port))
            s.sendall(payload)
            resp = s.recv(1024).decode().strip()
            s.close()
        except Exception:
            resp = "0.0.0.0"

        print(f"[CLIENT] {domain} -> {resp} (Header={header})")
        results.append((header, domain, resp))

    # Save results to CSV
    with open(args.out, "w") as f:
        f.write("CustomHeader,Domain,ResolvedIP\n")
        for r in results:
            f.write(",".join(r) + "\n")

if __name__ == "__main__":
    main()
