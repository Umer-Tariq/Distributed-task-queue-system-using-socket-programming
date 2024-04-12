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
        current_result += part  # Append the part to the current_result
        result.append(current_result)  # Add the complete result to result
        current_result = ''  # Reset current_result for the next result

    current_result += parts[-1]  # Append the last part to the current_result

if current_result:  # Check if there's any remaining data in current_result
    result.append(current_result)  # Add the last result to result

print(len(result))
client.close()
server.close()
