#Server=>Client: F"{status}"

import socket
from Alphabot import AlphaBot
import time

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


    print(f'Ho ricevuto: {data.decode()} da {sender_address}')
    
    if data.decode() == "w":
        bot.forward()
        #time.sleep(2)
    elif data.decode() == "s":
        bot.backward()
        #time.sleep(2)
    elif data.decode() == "a":
        bot.left()
        #time.sleep(2)
    elif data.decode() == "d":
        bot.right()
        #time.sleep(2)
    elif data.decode() == " ":
        bot.stop()
    elif data.decode() == "p":
        bot.stop()
        #connection.close()
        #s.close() #chiudo il socket
        attivo = False

connection.close()
s.close() #chiudo il socket