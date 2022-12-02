import socket
from threading import Thread


HOST: str = "192.168.0.102"
PORT: int = 12321
users = list()


def handle_connection(sock, addr):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except Exception as e:
            print(f"Client suddenly closed while receiving")
            break

        try:
            for client_socket in users:
                if client_socket != sock:
                    client_socket.sendall(msg.encode())
        except ConnectionError:
            print(f"Client suddenly closed, cannot send")
            break
        print("Disconnected by", addr)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
    serv_sock.bind((HOST, PORT))
    serv_sock.listen(1)

    while True:
        print(f"Подключение: {HOST}:{PORT}")
        # мы постоянно прислушиваемся к новым подключениям
        client_socket, client_address = serv_sock.accept()
        print(f"{client_address} connected.")

        # добавьте нового подключенного клиента в подключенные сокеты
        if client_socket not in users:
            users.append(client_socket)

        # запустите новый поток, который прослушивает сообщения каждого клиента
        t = Thread(target=handle_connection, args=(client_socket,client_address,))
        t.start()
