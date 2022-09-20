import socket
import threading
import os

HOST, PORT = "localhost", 8989
FORMAT = "UTF-8"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen()
os.system("cls")
print("> Server ON <")

global clients
server_on = True
stop_thread = False
clients = []

def handling(user_name, s_client, h_client):

    for i in clients:
        if i[1] != s_client:
            i[1].send(f"{user_name} has joined!".encode(FORMAT))

    running = True
    while running:

        try:
            c_data = s_client.recv(500).decode(FORMAT)
        except ConnectionResetError:
            running = False
            break
        except ConnectionAbortedError:
            running = False
            break

        print(f"{user_name}: {c_data}")

        for i in clients:
            if i[1] == s_client:
                if i[-1] == True:
                    running = False
            else:
                i[1].send(f"{user_name}: {c_data}".encode(FORMAT))

    for i in clients:
        if i[1] != s_client:
            i[1].send(f"Server: {user_name} has left...".encode(FORMAT))

    s_client.close()
    for i in clients:
        if i[1] == s_client:
            i[1].close()
            clients.remove(i)
            

def admin():
    global clients
    running = True
    while running:
        user_input = input("")

        os.system("cls")
        print("""
            0: shutdown the server
            1: Number of clients connected
            2 <username>: remove a client
            3: list of usernames client
        """)

        if user_input == '0':
            user_input = input("> Are you sure? (Y/n): ").lower()
            if user_input == '' or user_input == 'y' or user_input == 'yes': 
                for i in clients:
                    i[-1] = True
                running = False
            else:
                print("> Shutdowning is canceled. <")

        elif user_input == '1':
            print(f"> {len(clients)} of clients in server <")
        
        elif user_input == f"2 {user_input[2:]}":
            for i in clients:
                if i[0] == user_input[2:]:
                    i[1].send("Server: Disconnected by admin!".encode(FORMAT))
                    i[1].close()
                    print(f"> {i[0]} is ban! <")
        
        elif user_input == '3':
            for i in clients:
                print(i[0])

    socket.close()


threading.Thread(target=admin).start()

print("""
    0: shutdown the server
    1: Number of clients connected
    2 <username>: remove a client
    3: Instructions
""")

while server_on:

    try:
        s_client, h_client = socket.accept()
    except OSError:
        for i in clients:
            i[1].close()
        print("> Server shutdowning <")
        server_on = False
        break
    user_name = s_client.recv(24).decode(FORMAT)
    clients.append([user_name, s_client, h_client, stop_thread])
    threading.Thread(target=handling, args=(user_name, s_client, h_client)).start()

print("> Server is OFF <")