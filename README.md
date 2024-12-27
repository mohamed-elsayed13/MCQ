# Computer Networking Quiz Application

An interactive client-server quiz application designed for computer networking enthusiasts. The application allows users to participate in a timed quiz, submit their answers, and receive results instantly.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
5. [How It Works](#how-it-works)

---

## Overview
This application demonstrates the client-server communication model using Python sockets. A server distributes quiz questions to connected clients, and clients interact through a graphical interface to answer these questions. The server evaluates the answers and sends the results back to the client.

---

## Features
- **Timed Quiz:** Each user has a limited time to complete the quiz.
- **Graphical User Interface (GUI):** Easy-to-use Tkinter-based client interface.
- **Randomized Questions:** Server selects random questions from a database.
- **Real-time Grading:** Instant feedback on quiz performance.

---

## Technologies Used
### Backend (Server):
- **Python Sockets** for client-server communication.
- **Pandas** for question management from Excel files.

### Frontend (Client):
- **Tkinter** for creating the graphical interface.

### Protocols:
- **TCP/IP** for reliable communication between server and client.

---

## Setup and Installation
### Prerequisites:
1. Python 3.x installed on both client and server machines.
2. Required Python libraries: `socket`, `pandas`, `threading`, `json`, `tkinter`, and `random`.

### Steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/computer-networking-quiz.git
    cd computer-networking-quiz
    ```
2. Install dependencies:
    ```bash
    pip install pandas
    ```
3. Prepare the question database:
   - Place an Excel file named `ExamQuestions.xlsx` in the server directory with the required question format.
4. Run the server:
    ```bash
    python server.py
    ```
5. Run the client:
    ```bash
    python client.py
    ```

---

## How It Works
1. **Server:** Waits for incoming connections and sends random questions from the database.
2. **Client:** Displays the quiz in a graphical interface with options to answer and submit.
3. **Grading:** The server evaluates the answers and sends the score to the client.




