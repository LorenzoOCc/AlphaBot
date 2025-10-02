#Client=>Server: F"{comando}|{tempo}"

import socket 

#TCP
BUFFER= 4096
SERVER_ADDRESS= ('192.168.1.122',10490) #metto l'IP del pc con il server
#creo un socket ipv4 UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(SERVER_ADDRESS)

attivo = True
print("Connessione stabilita")
while attivo:

    message= input('scrivi un messaggi(comando|tempo): ')

    s.send(message.encode())
    if message == "p":
        attivo = False    
    

s.close()