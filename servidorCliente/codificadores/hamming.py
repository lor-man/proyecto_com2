import numpy as np

def xorCal(arrayData): #Calcula el XOR entre todos los elementos de un array
    xorRes=0
    for data in range(len(arrayData)):
        xorRes=xorRes^arrayData[data]
    return xorRes

def matrizStringCodificado(textoMatrizCod):# convierte una matriz de nx16 a un equivalente de caracteres para ser enviado en formatop string
    
    charList=[chr(arrayBin) for arrayBin in np.packbits(textoMatrizCod)] 
    stringCodificado="".join(charList)
    return stringCodificado

def stringMatrizCodificado(stringCodificado):#Devuelve la matriz de bits de una cadana de caracteres codificada de nx16
    
    intStringCodificado=[ord(charElemento) for charElemento in stringCodificado]
    #print(intStringCodificado)
    intStringCodificadoMatriz=np.array([[intStringCodificado[posE]for posE in range(pos,pos+2)] for pos in range(0,len(intStringCodificado),2)],dtype=np.uint8)
    stringBinario=np.unpackbits(intStringCodificadoMatriz,axis=1)
    return stringBinario

def codificacion(textoEntradaHamming):# codificacion hamming de un texto
    hammingArray=None   #Matriz de nx16 en la cual n es el numero total de letras que se ingresan por teclado
    cadenaHamming=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype=np.uint8)#array auxiliar donde se almacena la letra a codificar
    try:
        #textoEntradaHamming=textoEntradaHamming.encode('utf-8') 
        #print(textoEntradaHamming)      
        if(len(textoEntradaHamming)==0):#Si no se ingresa texto retorna un error

            return 1

        arrayBytes=np.unpackbits(np.array([[ord(asciiC)]for asciiC in textoEntradaHamming],dtype=np.uint8),axis=1)#Obtencion de los bits de cada letra
      
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
        #print(cadenaHamming)
        return cadenaHamming #Retorna la matriz de nx16 donde se encuentran todos los caracteres con codigo hamming y la cadena introducida
    
    except Exception as exc:
          # si ocurre un error se devuelve en tanto para la matriz y la cadena el mismo valor 1->Error
        print("Algo a ido mal intentalo de nuevo") 
        #print(str(exc))
        return 1

def errorTransmision(mensaje): #mensaje es matriz de nx16 donde n es el array de cada letra con codigo hamming
    
    cadenaHammingError=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]) #Inicializacion de matriz auxiliar donde se guardaran los array de cada caracter con el error aleatorio

    for letraCodHam in mensaje: #ingreso de Error en cada letra del mensaje contenido en la matriz de nx16
        #letrCodHam es el array de la letra n de la matriz nx16
        randPos=np.random.randint(0,30,dtype=np.uint8)#obtiene la posicion aleatoria del error
        if(randPos<=15):
            #print(f"Posicion con error: {randPos}")
            letraCodHam[randPos]=np.uint8(not(letraCodHam[randPos])) #Se cambia el valor actual del bit en la posicion obtenida
        cadenaHammingError=np.append(cadenaHammingError,[letraCodHam],axis=0)# Se agrega el array del caracter al cual se le agrego el error a la matriz auxiliar 
       
    cadenaHammingError=np.delete(cadenaHammingError,0,axis=0) #Se eliminina la fila 0 de la matriz auxiliar debido a que solo era para inicializar el elemento
    #print(cadenaHammingError)

    return cadenaHammingError #Retorno de la matriz con errores introducidos

def detectorCorrector(mensaje): #deteccion y correccion de error

    for letraIndex in range(0,mensaje.shape[0]):#Recorre cada fila del mensaje de una matriz de nx16
        
        letraRecv=mensaje[letraIndex]       
        
        errorPos=xorCal([bitPos for bitPos in range(1,letraRecv.size) if letraRecv[bitPos]==1])#Calculo de la posicion de error por medio de la operacion xor
       
        if(errorPos==0):    #Si la posicion del error es 0 existen 2 opciones: que no exista error y el bit de paridad sea correcto
                           #o que no halla error y que el bit de paridad sea erroneo

            parityHamming=xorCal(letraRecv[1:])#Calculo de la paridad de los datos del codigo hamming sin contar el primer bit
                   
            if(parityHamming!=letraRecv[0]):# Si el bit de paridad calculado en parityHamming no es identico al del array recibido el bit de paridad es incorrecto
                
                letraRecv[0]=np.uint8(not(letraRecv[0]))# Se cambia el error en el bit de paridad
        
            else: # de lo contrario no existe ningun error
                
                mensaje[letraIndex]=letraRecv
                
        else:# si la posicion no es 0
            #print(f"posicion de error {errorPos} en {letraIndex}")        
            letraRecv[errorPos]=np.uint8(not(letraRecv[errorPos]))
            parityHamming=xorCal(letraRecv[1:])#Calculo de la paridad de los datos del codigo hamming sin contar el primer bit

            if(parityHamming!=letraRecv[0]):
            #   print(f"2 o mas errores en letraRecv[{letraIndex}]")
                mensaje[letraIndex]=letraRecv
            else:
                mensaje[letraIndex]=letraRecv

    return(mensaje)

def decodificacionHamming(mensaje):#Retorna el texto de una matriz de de hamming de nx16
    texto=""

    for letra in mensaje:
           
        texto=texto+chr(np.packbits(np.array([letra[pos] for pos in range(0,13) if (pos!=0 and pos!=1 and pos!=2 and pos!=4 and pos!=8) ]))[0])

    return(texto)

"""
cadena=codificacion("Prueba")
cadenaError=errorTransmision(cadena)
stringCadenaError=matrizStringCodificado(cadenaError)
print("-------------------------Envio------------------------------")

print(f"Enviado posible error {stringCadenaError}")
print("-------------------------------------------------------------")

print("..........................Decodificacion.....................")
matrizCadenaError=stringMatrizCodificado(stringCadenaError)
cadenaDetector=detectorCorrector(matrizCadenaError)
stringRecuperado=decodificacionHamming(cadenaDetector)

print(f"Recuperado {stringRecuperado}")
print("............................................................")



cadena=codificacion("Prueba")
cadenaError=errorTransmision(cadena)
stringCadenaError=matrizStringCodificado(cadenaError)
print("-------------------------Envio------------------------------")

print(f"Enviado posible error {stringCadenaError}")
print("-------------------------------------------------------------")

print("..........................Decodificacion.....................")
matrizCadenaError=stringMatrizCodificado(stringCadenaError)
cadenaDetector=detectorCorrector(matrizCadenaError)
stringRecuperado=decodificacionHamming(cadenaDetector)

print(f"Recuperado {stringRecuperado}")
print("............................................................")

"""

