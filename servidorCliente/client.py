import socket
import threading
import random

import codificadores.hamming as hamming
import codificadores.cesar as cesar
import codificadores.cifradoHill as hill
import codificadores.codificacioPropia as codPropio
import codificadores.texto_a_voz as txt2v

PORT=45853
#PORT=12021
#SERVER="0.tcp.ngrok.io"
SERVER="25.76.141.131"
HEADER=8
FORMAT='utf-8'
DISCONNECT_MESSAGE="exit()"
USERNAME="USERNAME"
MESSAGE="MSG"
ERROR="EMPTY_MSG"
ADDR=(SERVER,PORT)

def lenMsg(msg): # Longitud de texto  
  
    msg_length = len(msg.encode(FORMAT))
    
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

def cifradoRandom(mensaje):
    cifrador=random.randint(1,3)
    
    if(cifrador==1):#hill
        mensaje="HIL"+hill.cifradoDescifrado(mensaje,0) 
           
    elif(cifrador==2):#cesar   
        mensaje="CES"+cesar.cifradoCesar(mensaje)
    elif(cifrador==3):#propio
        mensaje="PRO"+codPropio.codificador(mensaje)
    return mensaje

def descifradoRandom(mensaje):
    
    usuarioRango=[pos for pos in range(len(mensaje)) if (mensaje[pos]=="[" or mensaje[pos]=="]")]
    
    usuario=mensaje[usuarioRango[0]:usuarioRango[1]+1]

    cifrado=mensaje[usuarioRango[1]+1:usuarioRango[1]+4]
   
    mensajeCifrado=mensaje[usuarioRango[1]+4::]
    
    if(cifrado=="HIL"):
      
        mensaje=hill.cifradoDescifrado(mensajeCifrado,1)
    elif(cifrado=="CES"):
       
        mensaje=cesar.decifradoCesar(mensajeCifrado)
    elif(cifrado=="PRO"):
    
        mensaje=codPropio.decodificador(mensajeCifrado)
    mensaje=usuario+mensaje
    return mensaje


def recvClient():# funcion para recibir los mensajes entrantes del servidor de parte de los usuarios
    msg=client.recv(HEADER)
    msg=msg.decode(FORMAT)
    if(msg):
        msg_len=int(msg)
        msg=client.recv(msg_len).decode(FORMAT)
        #---------------Hamming------------------------
        mensajeRecv=hamming.hammingDecodificacion(msg)
        #--------------descifrado----------------------
        mensajeRecv=descifradoRandom(mensajeRecv)
        #----------------------------------------------
        return mensajeRecv
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
                txt2v.textoAVoz(inMsg)
                print("\r"+inMsg)
                print("--->",end='',flush=True)
                

def sendMessage(): #Funcion de envio de mensajes, esta se mantiene en paralelo con la de escucha para no esperar si no se envia nada o si no se escucha nada del servidor
    estado=True
    while(estado):
        outMsg=input("--->")        
        if(outMsg=="exit()"):
            print("Desconectando......")
            client.send(lenMsg(MESSAGE))
            client.send(MESSAGE.encode(FORMAT))
            client.send(lenMsg(DISCONNECT_MESSAGE))
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            estado=False
        elif(outMsg):
            #--------------Cifrador random--------------------
           
            outMsg=cifradoRandom(outMsg)
            
            #--------------hamming------------------
            mensaje=hamming.hammingCodificacion(outMsg)
            #---------------------------------------
            client.send(lenMsg(MESSAGE))
            client.send(MESSAGE.encode(FORMAT))
            client.send(lenMsg(mensaje))
            client.send(mensaje.encode(FORMAT))
        
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    


threadRecv=threading.Thread(target=recvMessage)
threadRecv.daemon=True
threadRecv.start()


sendMessage()