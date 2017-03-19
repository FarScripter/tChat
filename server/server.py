import socket

chat = []

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_sock.bind(('127.0.0.1', 8000))
# serv_sock.setblocking(0)
clients = []

while True:
    data, addr = serv_sock.recvfrom(1024)
    if addr not in clients:
        clients.append(addr)
    print(data.decode("utf-8"))
    chat.append(data.decode("utf-8"))
    for client in clients:
        serv_sock.sendto(data, client)

    with open('log.txt', 'a') as logs:
        pass

serv_sock.close()
