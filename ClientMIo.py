
import socket
from pynput import keyboard

# 🔹 IP del Raspberry Pi (quello dove gira il server)
HOST = "192.168.1.124"   # <--- CAMBIA QUESTO con l'IP del tuo Raspberry
PORT = 5000

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
            invia("f")   # avanti
        elif key.char == 's':
            invia("b")   # indietro
        elif key.char == 'a':
            invia("l")   # sinistra
        elif key.char == 'd':
            invia("r")   # destra
    except AttributeError:
        # gestisce tasti speciali
        if key == keyboard.Key.space:
            invia("s")  # stop

def rilascia(key):
    """Funzione chiamata quando un tasto viene rilasciato"""
    try:
        if key.char in ['w', 'a', 's', 'd']:
            invia("s")  # stop automatico al rilascio
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        print("Chiusura connessione...")
        conn.close()
        return False  # ferma il listener

# Avvia l’ascoltatore dei tasti
with keyboard.Listener(on_press=premi, on_release=rilascia) as listener:
    listener.join()
