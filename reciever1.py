import socket
import os
import nltk

def classify_review(review):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    paragraph = "I loved the new movie. The acting was great, and the plot was engaging. " \
                "However, the ending was a bit disappointing."

    sentiment_scores = sid.polarity_scores(paragraph)

    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment

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
