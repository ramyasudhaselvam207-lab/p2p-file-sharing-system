# load_balancer.py
import socket
import threading
import json

# Dictionary to hold peer info: {peer_address: load_count}
peers = {}

# Lock to prevent data conflicts in multi-threading
lock = threading.Lock()

HOST = "0.0.0.0"
PORT = 5000

# Handle incoming peer connections
def handle_peer(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            command = json.loads(data)

            if command["type"] == "register":
                with lock:
                    peers[addr[0]] = 0
                conn.send("Registered successfully".encode())

            elif command["type"] == "update_load":
                with lock:
                    peers[addr[0]] = command["load"]

            elif command["type"] == "get_peer":
                with lock:
                    if peers:
                        # Choose peer with minimum load
                        best_peer = min(peers, key=peers.get)
                        response = {"peer_ip": best_peer}
                    else:
                        response = {"peer_ip": None}
                conn.send(json.dumps(response).encode())

        except Exception as e:
            print(f"[ERROR] {addr} -> {e}")
            break

    with lock:
        if addr[0] in peers:
            del peers[addr[0]]
    conn.close()
    print(f"[INFO] Peer disconnected: {addr[0]}")

# Main server loop
def start_load_balancer():
    print(f"[STARTING] Load Balancer running on port {PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        print(f"[CONNECTED] Peer connected: {addr[0]}")
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_load_balancer()
