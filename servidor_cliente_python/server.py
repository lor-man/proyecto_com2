import socket 
import threading


PORT=45853
#SERVER=socket.gethostbyname(socket.gethostname())
SERVER="127.0.0.1"
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECT"
USERNAME="USERNAME"
MESSAGE="MSG"
HEADER=8

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

clients=[]

def lenMsg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length

def clientsMessage(msg,connection,username):
    for client in clients:
        if(client!=connection):
            try:               
                msgSend="["+str(username)+"]:"+str(msg)
                client.send(lenMsg(MESSAGE))    
                client.send(MESSAGE.encode(FORMAT))
                client.send(lenMsg(msgSend))
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
    
        msg_length=conn.recv(HEADER)    
        
        msg_length=msg_length.decode(FORMAT)
        
        

        if msg_length:
            msg_length=int(msg_length)
            
            msg=conn.recv(msg_length).decode(FORMAT)
            
            #print(f"[RECIBIDO] {msg}")

            if(userRegister): #Registra al usuario con un nombre de usuario
                username=msg
                userRegister=False 
                
            if (messageIn):#Muestra el mensaje
                messageCont=msg               
                clientsMessage(messageCont,conn,username)
                

                if(msg=="exit()"):# Desconecta al cliente 
                    connected=False
                    disconnectUser=f"Disconnected"
                    clientsMessage(disconnectUser,conn,username)
                    
                    

                messageIn=False

            if (msg==USERNAME): #El siguiente mensaje indica que sera el apodo escogido por el cliente
                userRegister=True
                #print(userRegister)

            if (msg==MESSAGE):                
                messageIn=True
                #print("message"+str(messageIn))

            print(f"[{addr}]{msg}")
            #conn.send("msg received".encode(FORMAT))
        
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