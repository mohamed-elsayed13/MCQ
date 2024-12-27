import socket
import json
import threading
import time
import tkinter as tk
from tkinter import messagebox

#Client setup
HOST = '127.0.0.1'
PORT = 12345

clientAnswers = [] 
timeUp = False  # Flag to indicate if the time is up
Question_index = 0

# Main application window
root = tk.Tk()
root.title("Computer Networking quiz")

# Create a label for time out
timer_label = tk.Label(root, text="Time remaining: 20 seconds", font=("Arial", 12), fg="red")
timer_label.pack(pady=10)

# Timer function for the quiz
def timer():
    global timeUp
    for i in range(120, 0, -1):
        timer_label.config(text=f"Time remaining: {i} seconds")
        time.sleep(1)
    timeUp=True
    Send_Answers()
    
# Update UI function
def update_ui(question_index):
    question_label.config(text=questions[question_index]['Question'])
    options[0].config(text=questions[question_index]['OptionA'])
    options[1].config(text=questions[question_index]['OptionB'])
    options[2].config(text=questions[question_index]['OptionC'])
    options[3].config(text=questions[question_index]['OptionD'])
    selected.set(-1)  # Reset selected option

# Function to send answers to the server
def Send_Answers():
    if timeUp:
        messagebox.showinfo("Time's up!", "The quiz ended because the timer ran out.")
    for _ in range(len(questions)-len(clientAnswers)):
        clientAnswers.append("N/A")
    # Send answers to the server    
    CLIENT_SOCKET.send(json.dumps(clientAnswers).encode())
    # Receive and display the result    
    result=json.loads(CLIENT_SOCKET.recv(2048).decode())
    messagebox.showinfo("Quiz result" , f"Your Score is {result['score']} out of {result['total']}")
    CLIENT_SOCKET.close() 
    root.destroy()

# Function to handle next question
def next_question():
    selected_option = selected.get()
    clientAnswers.append(chr(selected_option + 65) if selected_option in [0, 1, 2, 3] else "N/A")
    global Question_index
    Question_index+=1
    if Question_index<len(questions):
        update_ui(Question_index)
    else:
        Send_Answers()
            

newThread=threading.Thread(target=timer, daemon=True)
newThread.start()


try:
    CLIENT_SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((HOST,PORT))
    questions=json.loads(CLIENT_SOCKET.recv(2048).decode())
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit()



question= questions[Question_index]['Question']
texts = [questions[Question_index]['OptionA'], questions[Question_index]['OptionB'],questions[Question_index]['OptionC'],questions[Question_index]['OptionD']]


# Create a label for the question
question_label = tk.Label(root, text=question, font=("Arial", 14))
question_label.pack(pady=10)

# Variable to hold the selected option
selected = tk.IntVar()
selected.set(-1)  # Default value, no option selected

options=[]
# Create radio buttons for options
for index, option in enumerate(texts):
    rb = tk.Radiobutton(
        root, text=option, variable=selected, value=index, font=("Arial", 12)
    )
    rb.pack(anchor="w", padx=20)
    options.append(rb)

# Submit button
submit_button = tk.Button(root, text="Submit", command=next_question, font=("Arial", 12))
submit_button.pack(pady=10)

root.mainloop()  
