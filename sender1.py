import socket
import pandas as pd
import threading

num_senders = 5
m = []
df = pd.read_excel('movies.xlsx')
for i in df['review']:
    i = i + '#END@'
    m.append(i)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

def sender_func(lowerbound, upperbound):
    for i in range(lowerbound, upperbound + 1):
        lock.acquire()
        client.sendall(m[i].encode())
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
