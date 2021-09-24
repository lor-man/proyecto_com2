import numpy as np

def xorCal(arrayData): #Calcula el XOR entre todos los elementos de un array
    xorRes=0
    for data in range(len(arrayData)):
        xorRes=xorRes^arrayData[data]
    return xorRes


def codificacion(textoEntradaHamming):
    hammingArray=None   #Matriz de nx16 en la cual n es el numero total de letras que se ingresan por teclado
    cadenaHamming=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype=np.uint8)#array auxiliar donde se almacena la letra a codificar
    try:            
       
        cadena=textoEntradaHamming
        if(len(cadena)==0):#Si no se ingresa texto retorna un error
            return 1,1

        bytesCadena=np.array(bytearray(cadena,'utf-8'),dtype=np.uint8)   #Transformacion de caracter de la cadena a bits
        arrayBytes=np.transpose(np.unpackbits([bytesCadena],axis=0))     #Ordenando bits correspondientes a cada caracter

      
       
        for letra in arrayBytes: #Calculo de los bits de paridad p0, p1,p2,p4,p8 parar los 8 bits de datos.
            p0=0
            p1=xorCal([letra[0],letra[1],letra[3],letra[4],letra[6]])#letra[0]^letra[1]^letra[3]^letra[4]^letra[6]
            p2=xorCal([letra[0],letra[2],letra[3],letra[5],letra[6]])
            p4=xorCal([letra[1],letra[2],letra[3],letra[7]])
            p8=xorCal([letra[4],letra[5],letra[6],letra[7]])
            hammingArray=np.array([[0,p1,p2,letra[0],p4,letra[1],letra[2],letra[3],p8,letra[4],letra[5],letra[6],letra[7],0,0,0]],dtype=np.uint8)#creacion de la codigo hamming para la letra correspondiente con un total de 16 bits
            
            p0=xorCal(hammingArray[0])#Calculo del bit de paridad de hamming extendido
            hammingArray[0][0]=p0#Se agrega el bit de paridad extendido

            cadenaHamming=np.append(cadenaHamming,hammingArray,axis=0)#Se agrega la letra n en la matriz de nx16 donde se guardan las letras con codigo hamming

        cadenaHamming=np.delete(cadenaHamming,0,axis=0)# Eliminacion del primer elemento de la matriz de nx16 ya que este elemento solo la inicia 
        
       
        
        return cadenaHamming,cadena #Retorna la matriz de nx16 donde se encuentran todos los caracteres con codigo hamming y la cadena introducida
    
    except Exception as exc:  # si ocurre un error se devuelve en tanto para la matriz y la cadena el mismo valor 1->Error
        print("Algo a ido mal intentalo de nuevo") 
        print(str(exc))
        return 1,1

def errorTransmision(mensaje,cadena): #mensaje es matriz de nx16 donde n es el array de cada letra con codigo hamming
    
    cadenaHammingError=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]) #Inicializacion de matriz auxiliar donde se guardaran los array de cada caracter con el error aleatorio

    for letraCodHam in mensaje: #ingreso de Error en cada letra del mensaje contenido en la matriz de nx16
        #letrCodHam es el array de la letra n de la matriz nx16
        randPos=np.random.randint(0,15,dtype=np.uint8)#obtiene la posicion aleatoria del error
        letraCodHam[randPos]=np.uint8(not(letraCodHam[randPos])) #Se cambia el valor actual del bit en la posicion obtenida
        cadenaHammingError=np.append(cadenaHammingError,[letraCodHam],axis=0)# Se agrega el array del caracter al cual se le agrego el error a la matriz auxiliar 
       
    cadenaHammingError=np.delete(cadenaHammingError,0,axis=0) #Se eliminina la fila 0 de la matriz auxiliar debido a que solo era para inicializar el elemento


    return cadenaHammingError #Retorno de la matriz con errores introducidos

def dectCorError(mensaje): #deteccion y correccion de error

    for letraIndex in range(0,mensaje.shape[0]):#Recorre cada fila del mensaje de una matriz de nx16
        letraRec=mensaje[letraIndex]
        letraRecAux=mensaje[letraIndex]
     
        onePos=[]#Posiciones de los datos con valor 1 del codigo hamming sin contar el primer bit
        errorPos=0#Posicion del error obtenida al realizar la operacion xor en los datos de onePos
        parityBlock=0#bit de paridad calculado de todo el conjunto de bits del codigo hamming sin contar el primer bit

        for element in range(1,letraRec.size):#obtiene la posicion del elemento de cada array si este es un 1
            if(letraRec[element]==1):
                onePos.append(element)
     
        errorPos=xorCal(onePos)#Calculo de la posicion de error por medio de la operacion xor

        if(errorPos==0):    #Si la posicion del error es 0 existen 2 opciones: que no halla error y el bit de paridad sea correcto
                            #o que no halla error y que el bit de paridad sea erroneo
                       
            for pos in range(1,letraRec.size):#Calculo de la paridad de los datos del codigo hamming sin contar el primer bit
                parityBlock=parityBlock^letraRec[pos]

            if(parityBlock!=letraRec[0]):# Si el bit de paridad calculado en parityBlock no es identico al del array recibido el bit de paridad es incorrecto
                
                letraRec[0]=np.uint8(not(letraRec[0]))# Se cambia el error en el bit de paridad
        
            else: # de lo contrario no existe ningun error
                
                mensaje[letraIndex]=letraRec
                
        else:# si la posicion 
          
            letraRec[errorPos]=np.uint8(not(letraRec[errorPos]))
            for pos in range(1,letraRec.size):
                parityBlock=parityBlock^letraRec[pos]
          
            if(parityBlock!=letraRec[0]):     
                         
                #print("\t\t\t-----------------------------\n\t\t\tDos o mas errores encontrados\n\t\t\t-----------------------------")
                mensaje[letraIndex]=letraRec
            else:
                               
             
                mensaje[letraIndex]=letraRec
    return(mensaje)

def decod(mensaje):
    listBits=[]
    listDec=[]
    texto=""

    for letra in mensaje:
        listBits=[]
        for pos in range(0,13):
            if(pos!=0 and pos!=1 and pos!=2 and pos!=4 and pos!=8):
                listBits.append(letra[pos])
  
        listBits0=np.array(listBits)
        listDec.append(np.packbits(listBits0)[0])
 
    for charT in listDec:
        texto=texto+chr(charT)
    aux=listDec
    bytesCadena=np.array(bytearray(aux),dtype=np.uint8)
    arrayBytes=np.transpose(np.unpackbits([bytesCadena],axis=0))

    return(texto)

