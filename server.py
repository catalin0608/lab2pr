import socket

# Adresa și portul serverului
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

# Crearea socket-ului UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Legarea socket-ului la adresa și portul specificate
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"Serverul a pornit pe adresa IP {SERVER_IP} și portul {SERVER_PORT}")

# Dicționar pentru a păstra adresele IP ale clienților
client_addresses = {}

while True:
    # Așteptarea primirii unui mesaj
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    
    # Înregistrarea adresei IP a clientului și afișarea mesajului
    if addr not in client_addresses.values():
        client_addresses[message] = addr
        print(f"S-a conectat un nou client: {message}")
    else:
        # Verificarea dacă mesajul este pentru canalul general sau pentru o conversație privată
        if message.startswith('@'):
            recipient_username, message = message.split(' ', 1)
            recipient_address = None
            for name, address in client_addresses.items():
                if name == recipient_username[1:]:
                    recipient_address = address
                    break
            if recipient_address:
                server_socket.sendto(f"[Privat de la {message}]: {message}".encode('utf-8'), recipient_address)
                server_socket.sendto(f"[Privat pentru {recipient_username[1:]} de la {message}]: {message}".encode('utf-8'), addr)
            else:
                server_socket.sendto("Utilizatorul specificat nu este disponibil.".encode('utf-8'), addr)
        else:
            print(f"Mesaj primit de la {message}: {data.decode('utf-8')}")
            
            # Trimiterea mesajului către toți clienții, cu excepția celui care l-a trimis
            for name, address in client_addresses.items():
                if address != addr:
                    server_socket.sendto(data, address)
