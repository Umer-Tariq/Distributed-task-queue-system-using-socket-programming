import socket
import os
import nltk
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
#establishing connection via port 9996. the connection is established between the controller and the reciever
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9996))
server.listen()
client, addr = server.accept()

paragraph_length = 0
result = []

while True:
    #recieve the length of the incoming review. Problem: the length maybe of 4 digits or 3 digits.
    received_data = client.recv(3)  
    paragraph_length = received_data.decode('utf-8')
    #if empty, then no more data is to be recieved and hence break the loop
    if not paragraph_length:
        break 
    paragraph_length = int(paragraph_length)
    #recieve the review
    data = client.recv(paragraph_length).decode()
    #classify the review and append the class in the results array
    result.append(classify_review(data))

print(result)
server.close()
