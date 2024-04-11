import os
import socket
import time
import pandas as pd
df = pd.read_excel('movies.xlsx')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

#file_size = os.path.getsize("sample2.txt")
#print(file_size)
#client.send("receiver_1".encode())
#client.send("received_sample2.txt".encode())
##client.send(str(file_size).encode())
#while True:
#    data = file.read(1024)
#    if not data:
#        break

#    client.sendall(data)
#client.send(b"<END>")
#file.close()
im = 0
for i in df['review']:
    print(im)
    print(i)
    print('--------')
    client.sendall(i.encode())

    client.sendall("<END>".encode())
    im += 1

client.close()