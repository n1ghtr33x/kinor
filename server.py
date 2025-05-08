import socket, threading

clients = []

def handle(client, address):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            for c in clients:
                if c != client:
                    c.send(data)
        except Exception as e:
            print(f"Ошибка с клиентом {address}: {e}")
            break
    clients.remove(client)
    client.close()

s = socket.socket()
s.bind(('0.0.0.0', 9999))
s.listen()

print("Сервер запущен")

while True:
    conn, address = s.accept()
    clients.append(conn)
    print(f"Клиент {address} подключился")
    threading.Thread(target=handle, args=(conn, address)).start()
