
import socket
import time
from pynput import keyboard
import sqlite3


# 🔹 IP del Raspberry Pi (quello dove gira il server)
HOST = "192.168.1.124"   # IP
PORT = 5000

#Connessine con DB SQLite
# Connessione al database SQLite
db = sqlite3.connect("AlphaBotDB.db")
cursor = db.cursor()

def invia(comando):
    """Invia un comando al server e lo salva nel DB"""
    try:
        conn.sendall(comando.encode("utf-8"))
        print(f"Inviato comando: {comando}")

        # 🔹 Salva nel database
        cursor.execute("INSERT INTO comandi (comando) VALUES (?)", (comando,))
        db.commit()

    except:
        print("Connessione persa.")
        return False



# Crea una connessione TCP
try:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    print(f"Connesso al server {HOST}:{PORT}")
except Exception as e:
    print(f"Errore di connessione: {e}")
    exit()

def invia(comando):
    """Invia un comando al server"""
    try:
        conn.sendall(comando.encode("utf-8"))
        print(f"Inviato comando: {comando}")
    except:
        print("Connessione persa.")
        return False
    
def premi(key):
    """Funzione chiamata quando un tasto viene premuto"""
    try:
        if key.char == 'w':
            invia("w")
            time.sleep(0.01);  # avanti
        elif key.char == 's':
            invia("s") 
            time.sleep(0.01);  # indietro
        elif key.char == 'a':
            invia("a") 
            time.sleep(0.01);  # sinistra
        elif key.char == 'd':
            invia("d")
            time.sleep(0.01);   # destra
    except AttributeError:
        # gestisce tasti speciali
        if key == keyboard.Key.space:
            invia("esc")  # stop

def rilascia(key):
    """Funzione chiamata quando un tasto viene rilasciato"""
    try:
        if key.char in ['w', 'a', 's', 'd']:
            invia("esc")  # stop automatico al rilascio
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        print("Chiusura connessione...")
        conn.close()
        db.close()#Chiusura DB
        return False  # ferma il listener

# Avvia l’ascoltatore dei tasti
with keyboard.Listener(on_press=premi, on_release=rilascia) as listener:
    listener.join()
