import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9996))
server.listen()
client, addr = server.accept()

file_name = client.recv(20).decode()
print(file_name)
print('----------\n')
#file_size = client.recv(4).decode()
#print (file_size)
file = open(file_name, "wb")
file_bytes = b""
done = False

while done == False:
    data = client.recv(1024)

    if file_bytes [-5:] == b"<END>":
        done = True
    else:
        file_bytes += data

file.write(file_bytes)
file_size = os.path.getsize("sample2.txt")
print('received size = ', file_size)
file.close()
server.close()
