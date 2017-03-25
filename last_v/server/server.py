import socket
import json
from datetime import datetime


with open('config.json') as json_file:
    config = json.load(json_file)

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_sock.bind((config['ip'], config['port']))

chat = []
clients = []
users = []

while True:
    data, addr = serv_sock.recvfrom(1024)
    if addr not in clients:
        clients.append(addr)

    chat.append(data.decode("utf-8"))
    with open('log.txt', 'a') as logs:
        logs.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' <|> ' + chat[-1].strip() + "\n")

    if '!*{&c82-492832>' in chat[-1]:
        name = chat[-1][2:-27].strip()
        if name not in users:
            users.append(name)

    if '!*{&dc82-492832>' in chat[-1]:
        name = chat[-1][2:-29].strip()
        if name in users:
            users.remove(name)

    users_str = 'Users :'
    for user in users:
        users_str += ' ' + user + ','
    for client in clients:
        serv_sock.sendto(str.encode(users_str[0:-1] + '!*{&u82-492832>'),client)

    for client in clients:
        serv_sock.sendto(data, client)


serv_sock.close()
