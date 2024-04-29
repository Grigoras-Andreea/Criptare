import random
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

q = 13
xb = random.randint(1, q - 1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the server to the address
server.bind(ADDR)

def calculate_a(q):
    for a in range(1, q):
        results = []
        for j in range(1, q):
            a_to_j = a ** j
            a_to_j_mod_q = a_to_j % q
            if a_to_j_mod_q not in results:
                results.append(a_to_j_mod_q)
        if len(results) == q - 1:
            return a

def calculate_y():
    #generate random number from 1 to q
    a = calculate_a(q)
    
    yb = (a**xb) % q
    return yb

def calculate_k(ya):
    k = (ya**xb) % q
    return k

def decrypt(msg, k):
    decrypted_msg = ""
    for char in msg:
        decrypted_char = chr(ord(char) - k)
        decrypted_msg += decrypted_char
    return decrypted_msg

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    ya_length = conn.recv(HEADER).decode(FORMAT)
    if ya_length:
        ya_length = int(ya_length)
        ya = conn.recv(ya_length).decode(FORMAT)
        print(f"[{addr}] ya received: {ya}")
    
    # Calculate yb
    yb = calculate_y()
    
    # Send yb to the client
    yb_str = str(yb)
    yb_str = yb_str.encode(FORMAT)
    yb_length = len(yb_str)
    yb_send_length = str(yb_length).encode(FORMAT)
    yb_send_length += b' ' * (HEADER - len(yb_send_length))
    conn.send(yb_send_length)
    conn.send(yb_str)
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            msg = decrypt(msg, calculate_k(int(ya)))
            print(f"[{addr}] Decrypted message: {msg}")
            conn.send("Message received".encode(FORMAT))
    
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()