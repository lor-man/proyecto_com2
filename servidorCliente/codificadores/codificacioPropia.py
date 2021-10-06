#Kevin Estuardo Estrada Villatoro  201801404
import numpy as np
def codificador(texto):
    #---------------------------Emisor----------------------------
    #print('\n---------------Forma segura de enviar mensajes----------------')
    #entrada=str(input('Ingrese un mensaje para enviar:'))
    #print('')

    #print(texto)
    mensaje=[]; codificado=[]

    for i in texto: 
        mensaje.append(ord(i))            #Lista de ascii 
        
    for i in mensaje:
        codificado.append(chr(i+20)) #Lista de strings
    #print(len(codificado))


    texto0="".join(codificado)
    #print('Mensaje codificado: ',texto)
    #print('')
    #print(texto0)
    return texto0

    #-----------------------------Receptor-------------------------------------
def decodificador(texto):
    recibido=[]; Mensaje=[]
    #print(len(texto))
    for caracter in texto:
        recibido.append(ord(caracter))      #Lista de ascii
        
    for i in recibido:
        Mensaje.append(chr(i-20))           #Lista de strings
        #print(chr(i-20))
    mensaje="".join(Mensaje)
    #print('El mensaje enviado fue: ',"".join(Mensaje))
    #print('')
    #print('')
    #print(mensaje)
    return mensaje