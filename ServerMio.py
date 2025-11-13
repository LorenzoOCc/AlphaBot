import socket
from AlphaBot import AlphaBot

# Inizializza il robot
bot = AlphaBot()

HOST = "0.0.0.0"
PORT = 5000

# Crea socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server in ascolto su {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Connessione da {addr}")
    
    while True:
        data = conn.recv(1024).decode("utf-8").strip()
        if not data:
            break

        print(f"Comando ricevuto: {data}")

        try:
            comando, durata = data.split(",")
            durata = float(durata)   # tempo in secondi
        except ValueError:
            comando = data
            durata = 0

        if comando == "w":
            bot.forward()
            
        elif comando == "s":
            bot.backward()

        elif comando == "a":
            bot.left()

        elif comando == "d":
            bot.right()

        elif comando == "esc":
            bot.stop()

        else:
            print("Comando non riconosciuto")
    
    conn.close()
