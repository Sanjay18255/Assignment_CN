import argparse
import socket

# Predefined IP pool (15 addresses)
IP_POOL = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
]

def resolve_ip(header: str) -> str:
    """Resolve IP from header using time-based routing rules"""
    hour = int(header[0:2])
    seq_id = int(header[-2:])   # last 2 digits represent query sequence

    # Determine pool segment based on hour
    if 4 <= hour <= 11:         # Morning
        pool_start = 0
    elif 12 <= hour <= 19:      # Afternoon
        pool_start = 5
    else:                       # Night (20–23 or 00–03)
        pool_start = 10

    index = pool_start + (seq_id % 5)  # pick IP within segment
    return IP_POOL[index]

def main():
    """Main server function: accept client queries and respond with resolved IP"""
    parser = argparse.ArgumentParser(description="DNS Resolver Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=55555)
    args = parser.parse_args()

    # Create and bind TCP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((args.host, args.port))
    server_sock.listen(5)
    print(f"Server listening on {args.host}:{args.port} ...")

    try:
        while True:
            conn, addr = server_sock.accept()
            data = conn.recv(1024)
            if not data:
                conn.close()
                continue

            header = data[:8].decode()       # extract custom header
            domain = data[8:].decode().strip()  # extract domain

            ip = resolve_ip(header)          # get resolved IP

            print(f"Got query {domain} with header {header} -> {ip}")
            conn.sendall(ip.encode())
            conn.close()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
