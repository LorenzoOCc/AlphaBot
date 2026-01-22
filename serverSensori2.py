import RPi.GPIO as GPIO
import socket
import threading
import time
from AlphaBot import AlphaBot

# Impostazioni GPIO
DR = 16  # sensore destro
DL = 19  # sensore sinistro

# Inizializzazione GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Inizializza il robot
bot = AlphaBot()

# Variabile di stato globale per indicare se c'è un ostacolo
ostacolo_rilevato = False
ostacolo_lock = threading.Lock()

# Server TCP
HOST = "0.0.0.0"
PORT = 5000

# Funzione per la lettura continua dei sensori
def funzione_sensori():
    global ostacolo_rilevato
    print("Monitoraggio sensori avviato...")
    while True:
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)

        with ostacolo_lock:
            if DR_status == 0 or DL_status == 0:
                if not ostacolo_rilevato:
                    print("⚠️ Ostacolo rilevato! Solo retromarcia consentita.")
                    ostacolo_rilevato = True
                    bot.stop()
            else:
                if ostacolo_rilevato:
                    print("✅ Ostacolo rimosso, comandi normali ripristinati.")
                    ostacolo_rilevato = False

        time.sleep(0.05)  # piccolo delay per non sovraccaricare la CPU

# Avvia il thread per la lettura sensori
t_sensori = threading.Thread(target=funzione_sensori, daemon=True)
t_sensori.start()

# Creazione socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server in ascolto su {HOST}:{PORT}")

try:
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
                durata = float(durata)
            except ValueError:
                comando = data
                durata = 0

            # Controllo stato ostacolo
            with ostacolo_lock:
                ostacolo_attivo = ostacolo_rilevato

            # Se c'è un ostacolo, accetta solo il comando 's'
            if ostacolo_attivo and comando != "s":
                print("⛔ Movimento bloccato: ostacolo presente. Solo 's' consentito.")
                bot.stop()
                continue

            # Esecuzione dei comandi
            if comando == "w":
                bot.forward()
                if durata > 0:
                    time.sleep(durata)
                    bot.stop()

            elif comando == "s":
                bot.backward()
                if durata > 0:
                    time.sleep(durata)
                    bot.stop()

            elif comando == "a":
                bot.left()
                if durata > 0:
                    time.sleep(durata)
                    bot.stop()

            elif comando == "d":
                bot.right()
                if durata > 0:
                    time.sleep(durata)
                    bot.stop()

            elif comando == "esc":
                bot.stop()

            else:
                print("Comando non riconosciuto")

        conn.close()
        print("Connessione chiusa.")

except KeyboardInterrupt:
    print("Interruzione manuale, chiusura server...")

finally:
    bot.stop()
    GPIO.cleanup()
    server_socket.close()
