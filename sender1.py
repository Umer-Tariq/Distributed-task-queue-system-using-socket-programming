import os
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

file = open("sample2.txt", "rb")
file_size = os.path.getsize("sample2.txt")
print(file_size)
client.send("receiver_1".encode())
client.send("received_sample2.txt".encode())
#client.send(str(file_size).encode())
while True:
    data = file.read(1024)
    if not data:
        break

    client.sendall(data)
client.send(b"<END>")
file.close()
client.close()