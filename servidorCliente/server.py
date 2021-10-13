import socket 
import threading
import codificadores.hamming as hamming

PORT=45853
#SERVER=socket.gethostbyname(socket.gethostname())
SERVER="127.0.0.1"
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="exit()"
USERNAME="USERNAME"
MESSAGE="MSG"
HEADER=8

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

clients=[]

def lenMsg(msg):
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length

def clientsMessage(msg,connection,username):
    for client in clients:
        if(client!=connection):
            try:      
                msgSend=username+msg #msgSend="["+str(username)+"]:"+msg
                client.send(lenMsg(MESSAGE.encode(FORMAT)))    
                client.send(MESSAGE.encode(FORMAT))
                client.send(lenMsg(msgSend.encode(FORMAT)))
                client.send(msgSend.encode(FORMAT))
            except:
                clients.remove(client)
                client.close()
                

def handle_client(conn,addr):
    print(f"[new connection] {addr} connected.")
    username=""
    userRegister=False
    messageIn=False
    messageCont=None
    connected= True
    while(connected):
        try:
            msg_length=conn.recv(HEADER)    
            
            msg_length=msg_length.decode(FORMAT)
        
            if msg_length:
                msg_length=int(msg_length)
                
                msg=conn.recv(msg_length).decode(FORMAT)
                
                if(userRegister): #Registra al usuario con un nombre de usuario
                    username="["+msg+"]"

                    username=hamming.hammingCodificacion(username)
                
                    userRegister=False 
                    
                if (messageIn):#Muestra el mensaje
                    messageCont=msg 
                    if(messageCont==DISCONNECT_MESSAGE):# Desconecta al cliente 
                        connected=False

                        disconnectUser=hamming.hammingCodificacion("Disconnected")
                        
                        clientsMessage(disconnectUser,conn,username)
                    else:
                        clientsMessage(messageCont,conn,username)
                    messageIn=False

                if (msg==USERNAME): #El siguiente mensaje indica que sera el apodo escogido por el cliente
                    userRegister=True

                if (msg==MESSAGE):                
                    messageIn=True

                print(f"[{addr}] Recibido")
        except:
            #clients.remove(conn)
            break
        
    clients.remove(conn)  
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon=True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()