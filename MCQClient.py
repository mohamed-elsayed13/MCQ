import socket
import json
import threading
import time
import queue
#Client setup
HOST='127.0.0.1'
PORT=12345

clientAnswers = [] 
timeUp = False  # Flag to indicate if the time is up
input_queue = queue.Queue()  # Queue for non-blocking input

# Input function
def get_input():
    while not timeUp:
        user_input = input()  # Blocking input
        input_queue.put(user_input)

def timer():
    global timeUp
    time.sleep(20)
    timeUp=True
    print("Time is up! Submitting your answers..")    

newThread=threading.Thread(target=timer, daemon=True)
newThread.start()

input_thread = threading.Thread(target=get_input, daemon=True)
input_thread.start()

try:
    CLIENT_SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((HOST,PORT))
    questions=json.loads(CLIENT_SOCKET.recv(2048).decode())
    # print(questions)
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit()

  
for i,question in enumerate(questions):
    if timeUp==True:
        break
    print(f"Q{i+1}: {question['Question']}")
    print(f"A) {question['OptionA']} ")
    print(f"B) {question['OptionB']} ")
    print(f"C) {question['OptionC']} ")
    print(f"D) {question['OptionD']} ")
    print("Your answer (A/B/C/D): ", end="", flush=True)
    
    Answer=None
    while not timeUp and Answer is None:
        try:
            # Get the answer from the input queue
            Answer = input_queue.get_nowait().strip().upper()
        except queue.Empty:
            time.sleep(0.1)  # Wait briefly and check again

    # If time's up or no answer was provided, default to "N/A"
    clientAnswers.append(Answer if Answer in ["A", "B", "C", "D"] else "N/A")

for _ in range(len(questions)-len(clientAnswers)):
    clientAnswers.append("N/A")

# Send answers to the server    
CLIENT_SOCKET.send(json.dumps(clientAnswers).encode())
# Receive and display the result    
result=json.loads(CLIENT_SOCKET.recv(2048).decode())
print(f"Your Score is {result['score']} out of {result['total']}")

CLIENT_SOCKET.close()     