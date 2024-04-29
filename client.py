import socket
import random

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.100.11"
ADDR = (SERVER, PORT)

q = 13
xa = random.randint(1, q - 1)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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
    
    ya = (a**xa) % q
    return ya

def calculate_k(yb):
    k = (yb**xa) % q
    return k

def encrypt(msg, k):
    encrypted_msg = ""
    for char in msg:
        encrypted_char = chr(ord(char) + k)
        encrypted_msg += encrypted_char
    return encrypted_msg

def send_ya(ya):
    ya_str = str(ya)
    ya_msg = ya_str.encode(FORMAT)
    ya_length = len(ya_msg)
    send_length = str(ya_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(ya_msg)

def receive_yb():
    # Receive the length of yb message
    yb_length = client.recv(HEADER).decode(FORMAT)
    if yb_length:
        yb_length = int(yb_length)
        # Receive yb from the server
        yb = client.recv(yb_length).decode(FORMAT)
        return int(yb)


def send(msg, yb):
    msg = encrypt(msg, calculate_k(yb))
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    

send_ya(calculate_y())
yb = receive_yb()
print(f"Received yb: {yb}")
print(calculate_k(yb))

while True:
    msg = input("Enter a message: ")  
    send(msg, yb)
    if msg == "":
        send(DISCONNECT_MESSAGE, yb)
        break
    