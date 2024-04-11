import socket
import os
import time
import pandas as pd

def compare_results(reviews):
    df = pd.read_excel('movies.xlsx')
    for i in df['review']:
        if i not in reviews:
            print("*******************************************************")
            print(i)

#hashmap = { "receiver_1" : 9996 }
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()
#rec = client.recv().decode()
port = 9996


client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(("localhost", port))

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

print("Received reviews:")
print(len(reviews))

print('--------------------------')

##Sending the reviews to the reciever one by one
for i in reviews:
    client2.sendall(i.encode())

    client2.sendall("<END>".encode())



client.close()
server.close()
client2.close()
