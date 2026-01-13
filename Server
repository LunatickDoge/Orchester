import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

clients = []

print("Server started on", HOST, PORT)

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
