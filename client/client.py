import time
import json
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

with open('config.json') as json_file:
    settings = json.load(json_file)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.connect(('127.0.0.1', 8000))
connection_msg = '< ' + settings['name'] + ' connected > '
client_sock.sendall(str.encode(connection_msg))

chat = []
options = []
my_messages = [connection_msg]
template_reset = ''

with open ('template.txt') as file:
    template_reset = file.read()

with open('chat.txt', 'w') as file:
    file.write('< You logged in as ' + settings['name'] + ' >\n')
    file.write(template_reset)

class MyHandler(FileSystemEventHandler):
    event = FileModifiedEvent('1.txt')
    def on_modified(self, event):
        with open('chat.txt') as file:
            lines = file.readlines()
            # name_str = lines[1][12:].rstrip()
            name_str = settings['name']
            try:
                text_str = lines[5].strip()
                options = lines[1].strip()
            except IndexError:
                text_str = ''
                options = ''

            if 'disconnect' in options and my_messages[-1] != '< ' + settings['name'] + ' disconected >' :
                disconnection_msg = '< ' + settings['name'] + ' disconected >'
                client_sock.sendall(str.encode(disconnection_msg))
                my_messages.append(disconnection_msg)

            if 'clear' in options:
                for msg in chat:
                    chat.pop()
                with open('chat.txt', 'w') as file:
                    file.write('< You logged in as ' + settings['name'] + ' >\n')
                    file.write(template_reset)

            elif text_str != my_messages[-1] and name_str != '' and text_str != '' and my_messages[-1] != '< ' + settings['name'] + ' disconected >' :

                client_sock.sendall(str.encode(name_str + ' > ' + text_str))
                my_messages.append(text_str)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)

            if my_messages[-1] == '< ' + settings['name'] + ' disconected >':
                raise KeyboardInterrupt

            data = client_sock.recv(1024)

            if not data:
                raise KeyboardInterrupt

            print('Ok: ', data.decode("utf-8"))
            chat.append(data.decode("utf-8"))
            print("\a")

            with open('chat.txt', 'w') as file:
                file.write('< You logged in as ' + settings['name'] + ' >\n')
                file.write(template_reset)
                for msg in chat:
                    file.write(msg.replace(settings['name'], 'You', 1) + '\n')


    except KeyboardInterrupt:
        client_sock.close()
        with open('chat.txt', 'w') as file:
            file.write('')
        observer.stop()
    observer.join()
