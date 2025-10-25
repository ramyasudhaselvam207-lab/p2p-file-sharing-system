# 🌐 Peer-to-Peer File Sharing System with Load Balancing

## 🧭 Overview
The **Peer-to-Peer File Sharing System with Load Balancing** is a decentralized networking project developed in **Python** that enables peers to share and download files directly without using a central server.  
Each peer acts as both a **client** and a **server**, creating a balanced and scalable data-sharing network.

This project supports the **United Nations Sustainable Development Goal 9 (SDG 9 – Industry, Innovation & Infrastructure)** by promoting innovative, efficient, and resilient digital infrastructure for modern communication systems.

---

## 🚀 Features
- 🔄 **Decentralized architecture** – peers act as both clients and servers  
- ⚖️ **Load balancing** – distributes file requests evenly among peers  
- 🧵 **Multi-threaded connections** – supports multiple transfers simultaneously  
- 📁 **File sharing system** – easy upload/download between peers  
- 🔐 **Reliable transfer** – ensures data integrity  
- 🧩 **Extensible design** – future-ready for encryption or peer discovery  

---

## 🧠 System Architecture
Each peer maintains its own shared folder and communicates directly with others using socket connections.  
The **load balancer module** ensures that requests are distributed evenly among active peers to prevent congestion.

---

## ⚙️ Technologies Used
| Component | Technology |
|------------|-------------|
| Programming Language | Python |
| Libraries | socket, threading, os |
| Architecture | Peer-to-Peer (P2P) |
| Load Balancing | Least Connection / Round Robin |

---

## 📂 Folder Structure
p2p-file-sharing-system/
├── peer.py
├── load_balancer.py
├── README.md
├── requirements.txt
├── shared/
│ └── (files to share)
└── downloads/
└── (received files)


---

## 🧩 How It Works
1. Each peer runs `peer.py` and registers itself in the load balancer.  
2. Files placed inside the `shared/` folder are available for sharing.  
3. When a peer requests a file, the load balancer selects the least-loaded peer.  
4. The selected peer transfers the file directly to the requester.  
5. Downloaded files are saved in the `downloads/` folder.

---

## 🛠️ Installation & Usage

### 1️⃣ Clone the Repository
bash
git clone https://github.com/<your-username>/p2p-file-sharing-system.git
cd p2p-file-sharing-system

### 2️⃣ Run Peers

Open multiple terminals or systems on the same network and run:

python peer.py

### 3️⃣ Share Files

Place any files you want to share in the shared/ folder.

### 4️⃣ Request Files

From the peer menu, choose option 2 and enter:

The IP address of another peer

The filename you wish to download

### 5️⃣ Check Load Balancer Info

Option 3 shows connected peers and their load status.
