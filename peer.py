# peer.py
import socket
import threading
import os
import json

LB_IP = "127.0.0.1"  # Replace with Load Balancer IP if on another machine
LB_PORT = 5000
BUFFER_SIZE = 1024

SHARED_DIR = "shared"
DOWNLOAD_DIR = "downloads"
PORT = 5001  # Each peer's listening port

# Ensure directories exist
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --------------------------
# Functions for communication with Load Balancer
# --------------------------
def register_with_lb():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LB_IP, LB_PORT))
        command = {"type": "register"}
        s.send(json.dumps(command).encode())
        response = s.recv(BUFFER_SIZE).decode()
        print(f"[LB] {response}")
        s.close()
    except Exception as e:
        print(f"[ERROR] Could not connect to Load Balancer: {e}")

def get_best_peer():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LB_IP, LB_PORT))
        command = {"type": "get_peer"}
        s.send(json.dumps(command).encode())
        response = json.loads(s.recv(BUFFER_SIZE).decode())
        s.close()
        return response.get("peer_ip")
    except Exception as e:
        print(f"[ERROR] Could not get peer from LB: {e}")
        return None

# --------------------------
# Server: share files with other peers
# --------------------------
def handle_client(conn, addr):
    try:
        filename = conn.recv(BUFFER_SIZE).decode()
        filepath = os.path.join(SHARED_DIR, filename)
        if os.path.exists(filepath):
            conn.send("FOUND".encode())
            with open(filepath, "rb") as f:
                data = f.read(BUFFER_SIZE)
                while data:
                    conn.send(data)
                    data = f.read(BUFFER_SIZE)
            print(f"[SENT] {filename} -> {addr[0]}")
        else:
            conn.send("NOTFOUND".encode())
    except Exception as e:
        print(f"[ERROR] {addr[0]} -> {e}")
    finally:
        conn.close()

def start_peer_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    server.listen()
    print(f"[PEER] Listening for incoming requests on port {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# --------------------------
# Client: request files from peers
# --------------------------
def request_file(filename):
    peer_ip = get_best_peer()
    if not peer_ip:
        print("[INFO] No peers available to download file.")
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((peer_ip, PORT))
        s.send(filename.encode())

        status = s.recv(BUFFER_SIZE).decode()
        if status == "FOUND":
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, "wb") as f:
                data = s.recv(BUFFER_SIZE)
                while data:
                    f.write(data)
                    data = s.recv(BUFFER_SIZE)
            print(f"[DOWNLOADED] {filename} from {peer_ip}")
        else:
            print(f"[NOT FOUND] {filename} is not available on {peer_ip}")
        s.close()
    except Exception as e:
        print(f"[ERROR] Could not download from {peer_ip}: {e}")

# --------------------------
# Main Program
# --------------------------
if __name__ == "__main__":
    print("===== Peer-to-Peer File Sharing System =====")
    register_with_lb()

    threading.Thread(target=start_peer_server, daemon=True).start()

    while True:
        print("\nOptions:")
        print("1. View shared files")
        print("2. Request a file")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            files = os.listdir(SHARED_DIR)
            print("\n📁 Shared Files:")
            for f in files:
                print(" -", f)
            if not files:
                print("No files shared yet.")
        elif choice == "2":
            filename = input("Enter filename to download: ")
            request_file(filename)
        elif choice == "3":
            print("Exiting peer...")
            break
        else:
            print("Invalid choice.")
