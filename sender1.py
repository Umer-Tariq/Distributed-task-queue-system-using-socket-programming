import socket
import pandas as pd
import threading
import time

encryption_mapping = {
    'A': 'C', 'B': 'D', 'C': 'E', 'D': 'F', 'E': 'G', 'F': 'H', 'G': 'I', 'H': 'J',
    'I': 'K', 'J': 'L', 'K': 'M', 'L': 'N', 'M': 'O', 'N': 'P', 'O': 'Q', 'P': 'R',
    'Q': 'S', 'R': 'T', 'S': 'U', 'T': 'V', 'U': 'W', 'V': 'X', 'W': 'Y', 'X': 'Z',
    'Y': 'A', 'Z': 'B',
    'a': 'c', 'b': 'd', 'c': 'e', 'd': 'f', 'e': 'g', 'f': 'h', 'g': 'i', 'h': 'j',
    'i': 'k', 'j': 'l', 'k': 'm', 'l': 'n', 'm': 'o', 'n': 'p', 'o': 'q', 'p': 'r',
    'q': 's', 'r': 't', 's': 'u', 't': 'v', 'u': 'w', 'v': 'x', 'w': 'y', 'x': 'z',
    'y': 'a', 'z': 'b',
    '0': '2', '1': '3', '2': '4', '3': '5', '4': '6',
    '5': '7', '6': '8', '7': '9', '8': '0', '9': '1', "!" : ',', ',' : ".", "." : '!', ' ' : ' '
    
}

decryption_mapping = {v: k for k, v in encryption_mapping.items()}

def enrypt_string(string):
    result = ''
    for c in string:
        if c in encryption_mapping:
            result += encryption_mapping[c]
        
    return result

def decrypt_string(string):
    result = ''
    for c in string:
        if c in decryption_mapping:
            result += decryption_mapping[c]
        
    return result



num_senders = 5
m = []
df = pd.read_excel('movies.xlsx')

df['review'] = df['review'].apply(enrypt_string)


for i in df['review']:
    i = i + '#END@'
    m.append(i)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

start_time = time.time()
print(start_time)

count = 0  # Initialize count variable to count bytes sent

def sender_func(lowerbound, upperbound):
    global count  # Access count variable defined outside the function
    for i in range(lowerbound, upperbound + 1):
        lock.acquire()
        sent_data = m[i].encode()
        client.sendall(sent_data)
        count += len(sent_data)  # Increment count by the length of the data sent
        lock.release()

total_rows = len(m) - 1  # Subtract 1 for the heading row
rows_per_sender = total_rows // num_senders  # Calculate rows per sender

sender_threads = []
lock = threading.Lock()
lb = 0  # Start from row 1 (excluding heading row)
ub = lb + rows_per_sender
print('len of df is ', len(df))
for i in range(0, num_senders):
    sender_thread = threading.Thread(target=sender_func, args=(lb, ub))
    sender_threads.append(sender_thread)
    lb = ub + 1  # Move to the next set of rows for the next sender
    ub = lb + rows_per_sender
    if ub >= len(df):
        ub = len(df) - 1  # Handle the last sender

for thread in sender_threads:
    thread.start()

for thread in sender_threads:
    thread.join()
client.close()

s = socket.socket()
s.bind(("localhost", 9988))
s.listen()

client2, addr = s.accept()

msg = client2.recv(1024).decode('utf-8')

delay = time.time() - start_time
print(f"Delay: {delay} seconds.")
pkt_rcv = client2.recv(1024).decode('utf-8')
    
print(f"Total bytes sent: {count}")
print(f"ThroughPut: {count/delay}")
print("Packets Rcv: ", pkt_rcv)
client2.close()
