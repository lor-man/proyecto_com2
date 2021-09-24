

import socket

import threading

#PORT=4455
PORT=12021
SERVER="0.tcp.ngrok.io"
#SERVER="3.141.142.211"
HEADER=8
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECT"
USERNAME="USERNAME"
MESSAGE="MSG"
ERROR="EMPTY_MSG"
ADDR=(SERVER,PORT)

def lenMsg(msg): # Longitud de texto  
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length



client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
username=input("Username <---: ")
lenUsername=lenMsg(username)
client.send(lenMsg(USERNAME))
client.send(USERNAME.encode(FORMAT))
client.send(lenUsername)
client.send(username.encode(FORMAT))



def recvClient():# funcion para recibir los mensajes entrantes del servidor de parte de los usuarios
    msg=client.recv(HEADER)
    msg=msg.decode(FORMAT)
    if(msg):
        msg_len=int(msg)
        msg=client.recv(msg_len).decode(FORMAT)
        return msg
    else:
        return ERROR


def recvMessage():# funcion que se mantiene en espera de cualquier mensaje del servidor
  while(True):
    msg=client.recv(HEADER)
    msg=msg.decode(FORMAT)
    if msg:
        msg_len=int(msg)
        msg=client.recv(msg_len).decode(FORMAT)
        if(msg==MESSAGE): #Si la etiqueta del mensaje es un mensaje de un usuario entonces llama a la funcion especial para recibir el contenido del mensaje
            inMsg=recvClient()
            if(inMsg==ERROR):
                print(f"[ERROR] {client}")
            else:
                print("")
                print(inMsg)
                print("--->",end='',flush=True)

def sendMessage(): #Funcion de envio de mensajes, esta se mantiene en paralelo con la de escucha para no esperar si no se envia nada o si no se escucha nada del servidor
    estado=True
    while(estado):
        outMsg=input("--->")
        client.send(lenMsg(MESSAGE))
        client.send(MESSAGE.encode(FORMAT))
        client.send(lenMsg(outMsg))
        client.send(outMsg.encode(FORMAT))
        if(outMsg=="exit()"):
            estado=False
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    


threadRecv=threading.Thread(target=recvMessage)
threadRecv.daemon=True
threadRecv.start()


sendMessage()
exit()





"""

while(True):
    socket_list=[sys.stdin,client]
    read_sockets,write_socket,error_socket=select.select(socket_list,[],[])
    for socks in read_sockets:
        if (socks==client):
            cli=socks
            msg=socks.recv(HEADER)
            msg=msg.decode(FORMAT)
            if msg:
                msg_len=int(msg)
                msg=client.recv(msg_len).decode(FORMAT)
                if(msg==MESSAGE):
                    inMsg=recvClient(cli)
                    if(inMsg==ERROR):
                        print(f"[ERROR] {client}")
                    else:
                        print(inMsg)
        else:
            outMsg=input("--->")
            if(outMsg=="exit_"):
                client.send(lenMsg(DISCONNECT_MESSAGE))
                client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            client.send(lenMsg(MESSAGE))
            client.send(MESSAGE.encode(FORMAT))
            client.send(lenMsg(outMsg))
            client.send(outMsg.encode(FORMAT))


"""
    

            
            
                    
                    
