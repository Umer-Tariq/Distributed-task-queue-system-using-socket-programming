import socket
import os
import nltk
import threading
import csv

nltk.download('vader_lexicon')

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


#function to classify a review as positiv or negative. Expects one singal review as input. Returns it's class.
def classify_review(paragraph):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    sentiment_scores = sid.polarity_scores(paragraph)

    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment

def write_csv_headers(file_name, headers):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def calc_Sentiment(result, lb, ub, Sentiments, file_name):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(lb, ub + 1):
            Sentiments[i] = classify_review(result[i])
            lock.acquire()
            writer.writerow([result[i], Sentiments[i]])
            lock.release()
        
    print(f'Successfully wrote data to {file_name}')



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9997))
server.listen()
client, addr = server.accept()

paragraph_length = 0
result = []

current_result = ''

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
        current_result += part
        current_result = decrypt_string(current_result)
        result.append(current_result)  # Add the complete result to result
        current_result = ''  # Reset current_result for the next result

    current_result += parts[-1]  # Append the last part to the current_result
##
s = socket.socket()

s.connect(("localhost",9988))
msg = "ACK"
s.send(msg.encode('utf-8'))


##
if current_result:
    current_result = decrypt_string(current_result)  # Check if there's any remaining data in current_result
    result.append(current_result)  # Add the last result to result


client.close()
server.close()

lock = threading.Lock()
Sentiments = ['0'] * len(result)
#
pkt_rcv = str(len(Sentiments))
print(pkt_rcv)
s.send(pkt_rcv.encode('utf-8'))
s.close()
#
sender_threads = []
#calculaTing senTimenT analsis on resulTs
num_threads = 5
total_rows = len(result)
rows_per_sender = total_rows // num_threads 
lb = 0
ub = lb + rows_per_sender
file_name = 'movies_results.csv'
headers = ['Review', 'Sentiment']
write_csv_headers(file_name, headers)
for i in range(0, num_threads):
    sender_thread = threading.Thread(target=calc_Sentiment, args=(result, lb, ub, Sentiments, file_name))
    sender_threads.append(sender_thread)
    lb = ub + 1  # Move to the next set of rows for the next sender
    ub = lb + rows_per_sender 
    if ub >= len(result):
        ub = len(result) - 1

for thread in sender_threads:
    thread.start()

for thread in sender_threads:
    thread.join()

server.close()

