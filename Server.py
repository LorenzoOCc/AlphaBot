#Server=>Client: F"{status}"

import socket
from Alphabot import AlphaBot
import time
import keyboard

#TCP
ADDRESS= ('0.0.0.0' , 10490) #0.0.0.0 è un indirizzo IP speciale anche detto 'this host', si possono anche usare ""
BUFFER= 4096
numeroConnessioni=20
risposta=0

#creo un socket ipv4 UDP
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#questo è un server quindi facciamo la .bind
s.bind(ADDRESS)

s.listen(numeroConnessioni)#numero massimo connessioni

connection,sender_address=s.accept()#una volta accettato crea connessione

bot = AlphaBot()
# setta entrambi i motori al 30% di velocità
bot.setPWMA(50)
bot.setPWMB(50)

attivo = True

while attivo:
#metto il server il ricezione
    data=connection.recv(BUFFER)#come parametro vuole la dimensione del buffer
#connection.send(risposta.encode())#manda il messaggio dentro la risposta alla connection(client)

    if data.decode() == 'w' and keyboard.is_pressed('w'):
        data.d
        bot.forward()
    elif data.decode() == 's' and keyboard.is_pressed('s'):
        bot.backward()
    elif data.decode() == 'a' and keyboard.is_pressed('a'):
        bot.left()
    elif data.decode() == 'd' and keyboard.is_pressed('d'):
        bot.right()
    elif data.decode() == 'space' and keyboard.is_pressed('space'):
        bot.stop()
    elif data.decode() == 'esc' and keyboard.is_pressed('esc'):
        bot.stop()
        attivo = False
        break
        #connection.close()
        #s.close() #chiudo il socket

connection.close()
s.close() #chiudo il socket