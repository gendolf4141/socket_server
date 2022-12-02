import socket
from threading import Thread
from datetime import datetime
from colorama import Fore, init

# Настройки подключения
HOST: str = "192.168.0.102"
PORT: int = 12321

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {HOST}:{PORT}...")
# connect to the server
s.connect((HOST, PORT))
print("[+] Connected.")
# Сохранение имя пользователя
name_user = input("Введите имя: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# поток, который прослушивает сообщения для этого клиента и выводит их
t = Thread(target=listen_for_messages)
# сделайте демон потока таким, чтобы он заканчивался всякий раз, когда заканчивается основной поток
t.daemon = True
# запустите поток
t.start()

while True:
    # сообщение, которое мы хотим отправить на сервер
    to_send =  input()
    # Сообщение q для выхода из программы
    if to_send.lower() == 'q':
        break
    # Формирование сообщения
    to_send = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S') }] {name_user}: {to_send}{Fore.RESET}"
    # Отправка сообщения
    s.send(to_send.encode())

# close the socket
s.close()