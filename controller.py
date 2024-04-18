import socket
import threading
import pandas as pd

def compare_results(reviews):
    df = pd.read_excel('movies.xlsx')
    cont = 0
    for i in df['review']:
        if i not in reviews:
            print("*******************************************************")
            print(i[0:20])
            print(i[len(i)-20:len(i)])
            cont += 1
    print(cont)

def handle_send(client_socket, addr, name):
    current_review = ''
    #print('came = ', name)
    while True:
        try:
            data = client_socket.recv(1024).decode()
            ind = 9999
            for jj in range(0,len(data)):
                if data[jj] == '#':
                    ind = jj
            
            if ind >= len(data)-5 and ind < len(data):
                diff = len(data)-ind
                charr = client_socket.recv(5-diff).decode()
                data += charr
                
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError:", e)
            print("Skipping this data.")
            continue  # Skip processing this data

        if not data:  # Check if no data is received
            break  # Exit the loop
        #print(data[len(data)-10:len(data)])
        #print('################################################')
        parts = data.split('#END@')  # Split data using '<END>' as the delimiter
        for part in parts[:-1]:  # Iterate over all parts except the last one
            current_review += part  # Append the part to the current_review
            lock.acquire()
            reviews.append(current_review)  # Add the complete review to reviews
            lock.release()
            current_review = ''  # Reset current_review for the next review

        current_review += parts[-1]  # Append the last part to the current_review

    if current_review:  # Check if there's any remaining data in current_review
        reviews.append(current_review)

    #print('leaving = ', name)
    client_socket.close()  # Close the client socket after processing is done

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(5)

reviews = []
client_threads = []
i = 1
lock = threading.Lock()
while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_send, args=(client_socket, addr, i))
    client_thread.start()
    client_thread.join()
    i += 1
    c = 0
    r_num = 0
    for r in reviews:
        #print(r_num)
        if( len(r) == 0):
            c += 1
        """print(r[0:20])
        print( r[len(r)-20:len(r)])
        print('------------------------------')"""
        r_num += 1
    client_threads.append(client_thread)
    #compare_results(reviews)
    #print(c)
    server.close()
    break


port = 9997 
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(("localhost", port))
##Sending the reviews to the reciever one by one
for i in reviews:
    client2.sendall(i.encode())

    client2.sendall("<END>".encode())

client2.close()
