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
    
    parts = data.split('<END>')  # Split data using '<END>' as the delimiter
    for part in parts[:-1]:  # Iterate over all parts except the last one
        current_review += part  # Append the part to the current_review
        reviews.append(current_review)  # Add the complete review to reviews
        current_review = ''  # Reset current_review for the next review

    current_review += parts[-1]  # Append the last part to the current_review

if current_review:  # Check if there's any remaining data in current_review
    reviews.append(current_review)

print("Received reviews:")
print(len(reviews))

print('--------------------------')

client.close()
server.close()


client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(("localhost", port))
##Sending the reviews to the reciever one by one
for i in reviews:
    client2.sendall(i.encode())

    client2.sendall("<END>".encode())

client2.close()
