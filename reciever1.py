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

current_result = ''

while True:
    #try:
    data = client.recv(1024).decode()
    #except UnicodeDecodeError as e:
    #    print("UnicodeDecodeError:", e)
    #    print("Skipping this data.")
    #    continue  # Skip processing this data

    if not data:  # Check if no data is received
        break  # Exit the loop
    if '<END>' in data:
        parts = data.split('<END>')  # Split data using '<END>' as the delimiter
        current_result += parts[0]  # Append the first part to the current_review
        result.append(current_result)  # Add the complete review to reviews
        current_result = parts[1]  # Start a new review with the second part
    else:
        current_result += data  # Append data to the current_review

print(len(result))
client.close()
server.close()
