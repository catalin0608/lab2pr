import socket
import threading

# Adresa și portul serverului
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

# Crearea socket-ului UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Funcție pentru a primi mesaje de la server și a le afișa
def receive_messages():
    while True:
        data, server_address = client_socket.recvfrom(1024)
        print(data.decode('utf-8'))

# Introducerea numelui de utilizator
username = input("Introduceți username-ul: ")

# Trimiterea numelui de utilizator la server pentru înregistrare
client_socket.sendto(username.encode('utf-8'), (SERVER_IP, SERVER_PORT))

# Crearea unui fir de execuție separat pentru a primi mesajele de la server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # Introducerea mesajului
    message = input("Introduceți mesajul: ")
    
    # Verificarea dacă mesajul este pentru canalul general sau pentru o conversație privată
    if message.startswith('@'):
        recipient_username, message = message.split(' ', 1)
        recipient_address = None
        client_socket.sendto(b'get_clients', (SERVER_IP, SERVER_PORT))
        data, server_address = client_socket.recvfrom(1024)
        client_addresses = eval(data.decode('utf-8'))
        for name, address in client_addresses.items():
            if name == recipient_username[1:]:
                recipient_address = address
                break
        if recipient_address:
            client_socket.sendto(f"[Privat de la {username}]: {message}".encode('utf-8'), recipient_address)
        else:
            print("Utilizatorul specificat nu este disponibil.")
    else:
        # Trimiterea mesajului în canalul general
        client_socket.sendto(f"[Canal general de la {username}]: {message}".encode('utf-8'), (SERVER_IP, SERVER_PORT))
