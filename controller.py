import socket
import os

hashmap = { "receiver_1" : 9996 }
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()
rec = client.recv(10).decode()
port = hashmap[rec]
file_name = client.recv(20).decode()
#file_size = client.recv(4).decode()

done = "False"

client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(("localhost", port))

client2.send(file_name.encode())
print(file_name)
#client2.send(str(file_size).encode())

while done == 'False':
    data = client.recv(1024)

    if data[-5:] == b"<END>":
        done = True

    client2.sendall(data)

server.close()
client2.close()