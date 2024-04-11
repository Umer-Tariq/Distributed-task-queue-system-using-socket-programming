import socket
import os
import time

#hashmap = { "receiver_1" : 9996 }
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9998))
server.listen()
client, addr = server.accept()
#rec = client.recv(1.decode()
#port = hashmap[rec]
#file_name = client.recv(20).decode()
#file_size = client.recv(4).decode()

#client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client2.connect(("localhost", port))

#client2.send(file_name.encode())
#print(file_name)
#client2.send(str(file_size).encode())
reviews = []
current_review = ''

while True:
    try:
        data = client.recv(1024).decode()
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError:", e)
        print("Skipping this data.")
        continue  # Skip processing this data

    if not data:  # Check if no data is received
        break  # Exit the loop
    if '<END>' in data:
        parts = data.split('<END>')  # Split data using '<END>' as the delimiter
        current_review += parts[0]  # Append the first part to the current_review
        reviews.append(current_review)  # Add the complete review to reviews
        current_review = parts[1]  # Start a new review with the second part
    else:
        current_review += data  # Append data to the current_review


#print("Received reviews:")
for i in range(0, len(reviews)):
    print(i)
    print(reviews[i])
    time.sleep(1)

#print(reviews[1])

client.close()
server.close()
#client2.close()