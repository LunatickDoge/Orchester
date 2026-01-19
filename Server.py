import socket

def get_local_ip():
    try:
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        ip = temp_sock.getsockname()[0]
        temp_sock.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())

HOST = "0.0.0.0"
PORT = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

clients = []

local_ip = get_local_ip()
print(f"Server started!")
print(f"Local IP for other players: {local_ip}")
print(f"Port: {PORT}")

while True:
    data, addr = s.recvfrom(1024)
    msg = data.decode()

    if msg == "JOIN":
        if addr not in clients:
            clients.append(addr)
            print("Player joined:", addr)

        if len(clients) == 2:
            print("Two players joined. Starting battle!")
            s.sendto(b"START:0", clients[0])
            s.sendto(b"START:1", clients[1])

    if msg.startswith("PICK:"):
        if len(clients) == 2:
            other_client = clients[1] if addr == clients[0] else clients[0]
            s.sendto(f"OPPONENT_PICK:{msg.split(':')[1]}".encode(), other_client)

    if msg.startswith("MOVE:"):
        if len(clients) == 2:
            other_client = clients[1] if addr == clients[0] else clients[0]
            s.sendto(f"OPPONENT_MOVE:{msg.split(':')[1]}".encode(), other_client)
