import socket
import pandas as pd
import threading
import random
import json

#Server setup

HOST='127.0.0.1'
PORT= 12345
SERVER_SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER_SOCKET.bind((HOST,PORT))
SERVER_SOCKET.listen(5)

#Read the questions from excel file  
questions_df=pd.read_excel("ExamQuestions.xlsx")

#Convert questions_df to a list of Dict.
questions=questions_df.to_dict(orient="records")

print ("Server is ready to serve clients...")

def handle_client(Client_connection):
    """Handle client connection in a separate thread."""
    try:
        print(f"Recieved connection from client : {Client_addr}")
        
        # Randomly select 5 questions for the client
        selected_questions=random.sample(questions,5)
        Client_connection.send(json.dumps(selected_questions).encode())
        
        # Receive answers from the client
        clientAnswers=json.loads(Client_connection.recv(2048).decode())
        print(f"Recieved answers from {Client_addr} are : {clientAnswers}")
        
        # Grade the quiz
        score=0
        for i, question in enumerate(selected_questions):
            if (clientAnswers[i]==question["CorrectAnswer"]):
                score+=1
        
        # Send the grade back to the client        
        result={'score':score,'total':len(selected_questions)}
        Client_connection.send(json.dumps(result).encode())
        print(f"Sent result to {Client_addr}: {result}")    
    
    except Exception as e:
        print(f"Error handling client {Client_addr}: {e}")
    
    finally:
        Client_connection.close()
        print(f"Connection with {Client_addr} closed.\n")

while True:
    Client_connection,Client_addr = SERVER_SOCKET.accept()
    # Create a new thread for each client connection
    newThread = threading.Thread(target=handle_client, args=(Client_connection,))
    newThread.start()    
SERVER_SOCKET.close()    






