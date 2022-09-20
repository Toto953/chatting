import socket
import threading

HOST, PORT = "localhost", 8989
FORMAT = "UTF-8"

user_name = input("> Your name: ")

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
socket.send(user_name.encode(FORMAT))


def sending():
    running = True
    while running:

        try:
            message_input = input("").encode(FORMAT)
        except EOFError:
            print("Error: leaving")
            running = False
            break

        try:
            socket.send(message_input)
        except OSError:
            print("Error: SERVER OFF, message not sent...")
            running = False
            break

    socket.close()


def recving():
    running = True
    s_data = ""
    while running:

        try:
            s_data = socket.recv(500).decode(FORMAT)
        except ConnectionAbortedError:
            running = False
            print("Error: leaving")
            break
        except ConnectionResetError:
            print("Error: SERVER OFF, battery is low...")
            break

        if s_data == "quit":
            running = False
            print("Error: SERVER OFF, is shutdowned")
            break

        print(s_data)

    socket.close()

threading.Thread(target=sending).start()
threading.Thread(target=recving).start()