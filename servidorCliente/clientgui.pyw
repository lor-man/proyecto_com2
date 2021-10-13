import socket
import threading
import random

import codificadores.hamming as hamming
import codificadores.cesar as cesar
import codificadores.cifradoHill as hill
import codificadores.codificacioPropia as codPropio
import codificadores.texto_a_voz as txt2v

from tkinter import *
from tkinter import ttk



#---------------------------------------------------------
PORT=45853
#PORT=16914
#SERVER="8.tcp.ngrok.io"
SERVER="192.168.1.79"
HEADER=8
FORMAT='utf-8'
DISCONNECT_MESSAGE="exit()"
USERNAME="USERNAME"
MESSAGE="MSG"
ERROR="EMPTY_MSG"
ADDR=(SERVER,PORT)

#---------------------------------------------------------


#---------------------------------------------------------

class clientGui():

    def __init__(self):

        self.chatGui=Tk()
        
        self.chatGui.withdraw()
        

        #ventana de ingreso de nombre de usuario-----------------------------------------------------------------------

        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        self.login.configure(bg="gray14")
        self.login.iconbitmap('icono3.ico')
     
        self.pls=Label(self.login,text="Ingresa el nombre de usuario",justify=CENTER)
        self.pls.configure(bg="gray14",fg="white")
        self.pls.grid(row=1,column=1,columnspan=2,padx=20,pady=20)

        self.labelNombre=Label(self.login,text="Nombre: ")
        self.labelNombre.configure(bg="gray14",fg="white")
        self.labelNombre.grid(row=2,column=1,padx=20,pady=20)

        self.entryNombre=Entry(self.login)
        self.entryNombre.grid(row=2,column=2,padx=20,pady=20)
        self.entryNombre.configure(bg="gray20",fg="white")
        self.entryNombre.focus()

        self.siguienteVentana=Button(self.login,text="Continuar",command= lambda:self.siguiente(self.entryNombre.get()))
        self.siguienteVentana.configure(bg="gray20",fg="white")
        self.siguienteVentana.grid(row=3,column=1,columnspan=2,sticky="nswe")
        

        #------------------------------------------------------------------------------------------------------------------
        self.login.bind('<Return>',self.funcLogin)
        self.chatGui.protocol("WM_DELETE_WINDOW",self.cerrarVentana)
        #txt2v.textoAVoz("Bienvenido, despues de esuchar el siguiente mensaje ingrese el nombre de usuario y luego presione la tecla Enter")
        self.chatGui.mainloop()

    
    
    def siguiente(self,nombre):
        self.login.destroy()
        self.chat(nombre)
        
        
        self.threadRecv=threading.Thread(target=self.recvMessage)
        self.threadRecv.daemon=True
        self.threadRecv.start()
        #self.threadRecv.join()

   


    def chat(self,nombre):
        self.nombre=nombre
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.chatGui.bind('<Return>',self.funcChat)
        self.chatGui.resizable(False,False)

        self.client.send(self.lenMsg(USERNAME))
        self.client.send(USERNAME.encode(FORMAT))
        self.client.send(self.lenMsg(self.nombre))
        self.client.send(self.nombre.encode(FORMAT))

        self.chatGui.deiconify()
        self.chatGui.title(f"Usuario: {self.nombre}")
        self.chatGui.iconbitmap('icono3.ico')
        
        self.chatGui.configure(bg="black")
        
        self.textEntrada=StringVar()


        self.entradaTexto=Entry(self.chatGui,textvariable=self.textEntrada,width=50,bg="gray13",fg="white")
        self.entradaTexto.grid(row=2,column=1)
        self.entradaTexto.focus()
  
        self.botonEnviar=Button(self.chatGui,text="Enviar",width=15,bg="gray14",fg="black",command=lambda: self.sendBoton(self.textEntrada.get()))
        self.botonEnviar.grid(row=2,column=2,columnspan=2)
      
        self.text=Text(self.chatGui,height=15,width=52,bg="gray14",fg="white")
        self.text.grid(row=1,column=1,columnspan=2)
       
        self.scrollV=Scrollbar(self.chatGui,command=self.text.yview)
        self.scrollV.grid(row=1,column=3,sticky="nsew")       
        self.text.config(yscrollcommand=self.scrollV.set)
        self.text.config(state='disabled')

    def funcChat(self,event):#Cuando se presiona enter procesa el nombre de usuario en la pantalla de login
        self.sendBoton(self.textEntrada.get())
        return

    def funcLogin(self,event):#Envia el mensaje cada vez que se presiona enter     
        self.siguiente(self.entryNombre.get())
        return

    def lenMsg(self,msg):
        msg_length = len(msg.encode(FORMAT))
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        return send_length

    def cifradoRandom(self,mensaje):
        cifrador=random.randint(1,3)    
        if(cifrador==1):#hill
            mensaje="HIL"+hill.cifradoDescifrado(mensaje,0) 
            
        elif(cifrador==2):#cesar   
            mensaje="CES"+cesar.cifradoCesar(mensaje)
        elif(cifrador==3):#propio
            mensaje="PRO"+codPropio.codificador(mensaje)
        return mensaje
   
    def descifradoRandom(self,mensaje):
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
        
    def recvClient(self):
        msg=self.client.recv(HEADER)
        msg=msg.decode(FORMAT)
        if(msg):
            msg_len=int(msg)
            msg=self.client.recv(msg_len).decode(FORMAT)
            #---------------Hamming------------------------
            mensajeRecv=hamming.hammingDecodificacion(msg)
            #--------------descifrado----------------------
            mensajeRecv=self.descifradoRandom(mensajeRecv)
            #----------------------------------------------
            return mensajeRecv
        else:
            return ERROR

    def recvMessage(self):
    
        while(True):
            try:
                msg=self.client.recv(HEADER)
                msg=msg.decode(FORMAT)
                if msg:
                    msg_len=int(msg)
                    msg=self.client.recv(msg_len).decode(FORMAT)
                    if(msg==MESSAGE): #Si la etiqueta del mensaje es un mensaje de un usuario entonces llama a la funcion especial para recibir el contenido del mensaje
                        inMsg=self.recvClient()
                        if(inMsg==ERROR):
                            print(f"[ERROR] {self.client}")
                        else:
                            #------Impresion en gui---------------
                            self.text.config(state='normal')
                            self.text.insert(END,inMsg+"\n\n")
                            self.text.config(state='disabled')
                            self.text.see(END)
                            #--------------------------------------
                            txt2v.textoAVoz(inMsg)
                            print("\r"+inMsg)
                            print("--->",end='',flush=True)
            except Exception as exc:
                print(str(exc))
                print("Error al recibir mensaje")
                #self.cerrarVentana()
                break   

    def sendBoton(self,mensaje):
        self.text.config(state='disabled')
        self.msg=mensaje
        self.textEntrada.set("")
        self.sendThread=threading.Thread(target=self.sendMessage)
        #sendThread.daemon=True
        self.sendThread.start()
        #self.sendThread.join()
    
    def sendMessage(self):
        self.text.config(state='disabled')
        outMsg=self.msg
        try:
            while(True):
                if(outMsg=="exit()"):
                    print("Desconectando......")
                    self.client.send(self.lenMsg(MESSAGE))
                    self.client.send(MESSAGE.encode(FORMAT))
                    self.client.send(self.lenMsg(DISCONNECT_MESSAGE))
                    self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))

                    self.cerrarVentana()

                elif(outMsg!="exit()"):
                    #-------------Impresion en gui--------------------
                    self.text.config(state='normal')
                    self.text.insert(END,f"----> {outMsg}"+"\n\n")
                    self.text.config(state='disabled')
                    self.text.see(END)

                    #--------------Cifrador random--------------------
                    outMsg=self.cifradoRandom(outMsg)
                    #--------------hamming------------------
                    mensaje=hamming.hammingCodificacion(outMsg)
                    #---------------------------------------
                    self.client.send(self.lenMsg(MESSAGE))
                    self.client.send(MESSAGE.encode(FORMAT))
                    self.client.send(self.lenMsg(mensaje))
                    self.client.send(mensaje.encode(FORMAT))
                break
        except:
            self.cerrarVentana()

    def cerrarVentana(self):
        try:
            
            print(type(self.client))
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            print("Saliendo")
            self.chatGui.destroy()
            
        except:
            print("error")
            self.chatGui.destroy()
       
        



ventana=clientGui()





