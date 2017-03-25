import time
import json
import socket

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

with open('config.json') as json_file:
    config = json.load(json_file)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.connect((config['ip'], config['port']))
connection_msg = '< ' + config['name'] + ' connected !*{&c82-492832> '
client_sock.sendall(str.encode(connection_msg))

chat = []
options = []
my_messages = [connection_msg]
template_reset = ''
users = []
user_str = ''

with open ('template.txt') as file:
    template_reset = file.read()

with open('chat.txt', 'w') as file:
    file.write('<! You logged in as ' + config['name'] + ' !>\n')
    file.write(template_reset)

class MyHandler(FileSystemEventHandler):
    event = FileModifiedEvent('chat.txt')

    def on_modified(self, event):
        with open('chat.txt') as file:
            lines = file.readlines()
            # name_str = lines[1][12:].rstrip()
            name_str = config['name']
            try:
                text_len = 1
                while True:
                    if lines[len(lines)-(4 + text_len)] != '--------------------------\n':
                        text_len += 1
                    else:
                        break
                text_str = ''
                for text in lines[len(lines)-(3 + text_len):len(lines)-3]:
                    text_str += '\t\t\t\t\t\t\t ' + text

                text_str = text_str.strip()
                options = lines[len(lines)-2].strip()
            except IndexError:
                text_str = ''
                options = ''

            if ('disconnect' in options or 'выход' in options ) and my_messages[-1] != '< ' + config['name'] + ' disconected !*{&dc82-492832>' :
                disconnection_msg = '< ' + config['name'] + ' disconected !*{&dc82-492832>'
                client_sock.sendall(str.encode(disconnection_msg))
                my_messages.append(disconnection_msg)


            elif text_str != my_messages[-1] and name_str != '' and text_str != '' and my_messages[-1] != '< ' + config['name'] + ' disconected !*{&dc82-492832>' :
                if len(name_str) <= 5:
                    client_sock.sendall(str.encode(name_str + '\t\t\t\t > ' + text_str))
                elif 5 < len(name_str) <= 8:
                    client_sock.sendall(str.encode(name_str + '\t\t\t > ' + text_str))
                elif len(name_str) > 8:
                    point = len(name_str) - 8
                    client_sock.sendall(str.encode(name_str[:-point] + '...\t > ' + text_str))
                my_messages.append(text_str)



if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)

            if my_messages[-1] == '< ' + config['name'] + ' disconected !*{&dc82-492832>':
                raise KeyboardInterrupt

            data = client_sock.recv(1024)

            if not data:
                raise KeyboardInterrupt

            # print('server.log > ', data.decode("utf-8"))
            if '!*{&u82-492832>' not in data.decode("utf-8"):
                chat.append(data.decode("utf-8"))
            else:
                user_str = data.decode("utf-8")[:-15]
                print("\a")

            with open('chat.txt', 'w') as file:
                file.write('<! You logged in as ' + config['name'] + ' !>\n\n')
                file.write('<          tChat         >\n')
                file.write('--------------------------\n')
                for msg in chat:
                    if '!*{&c82-492832>' not in msg and '!*{&dc82-492832>' not in msg and 'shared !*{&file82-492832>' not in msg and len(msg) <= 2048:
                        if msg != chat[-1]:
                            if len(config['name']) <= 4:
                                file.write(msg.replace(config['name']+'\t', 'You\t\t', 1) + '\n\n')
                            elif 4 < len(config['name']) <= 8:
                                file.write(msg.replace(config['name']+'\t', 'You\t\t\t', 1) + '\n\n')
                            elif len(config['name']) > 8:
                                point = len(config['name']) - 8
                                file.write(msg.replace(config['name'][:-point]+'...\t', 'You\t\t\t\t\t', 1) + '\n\n')
                        else:
                            if len(config['name']) <= 4:
                                file.write(msg.replace(config['name']+'\t', 'You\t\t', 1) + '\n')
                            elif 4 < len(config['name']) <= 8:
                                file.write(msg.replace(config['name']+'\t', 'You\t\t\t', 1) + '\n')
                            elif len(config['name']) > 8:
                                point = len(config['name']) - 8
                                file.write(msg.replace(config['name'][:-point]+'...\t', 'You\t\t\t\t\t', 1) + '\n')

                file.write(template_reset)
                if user_str:
                    file.write(user_str + '\n')

    except KeyboardInterrupt:
        disconnection_msg = '< ' + config['name'] + ' disconected !*{&dc82-492832>'
        client_sock.sendall(str.encode(disconnection_msg))
        my_messages.append(disconnection_msg)
        client_sock.close()
        with open('chat.txt', 'w') as file:
            file.write('')
        observer.stop()
    observer.join()
