import cifradoHill
import hamming

while(True):
    #-------------------Hill---------------------------------------------------
    textoEntrada=cifradoHill.textEntrada("Texto de prueba")
    clave=cifradoHill.clave
    claveInv=cifradoHill.claveInv
    diccionarioLongitud=cifradoHill.numeroCaracteres
    textoCifrado=cifradoHill.cifDesHill(clave,textoEntrada,diccionarioLongitud)
    print('Texto ingresado codificado es: Texto de prueba',textoCifrado)#Texto cifrado de hill
    print('')

    #------------------------------------------------------------------------------

    #----------------------------Codificación hamming------------------------------
    textoCodificadoDeHamming,textoCadena=hamming.codificacion(textoCifrado)
    print('Bits de información y paridad: \n',textoCodificadoDeHamming)
    print('')

    #print(textoCadena)
    #----------------------------------------------------------------------------------------

    #---------------------------Ingreso de ruido (opcional)------------------------------
    #textoCodificadoDeHammingRuido=hamming.errorTransmision(textoCodificadoDeHamming,textoCadena)
    #print('Ingresar ruido: \n',textoCodificadoDeHammingRuido)
    #print('')
    #----------------------------------------------------------------------------------------


    #----------------------------Decodificacion con ruido(opcional)------------------------------
    #textoDecodificadoDeHamming=hamming.decod(textoCodificadoDeHammingRuido)
    #print('Texto recibido con errores corregidos:',textoDecodificadoDeHamming)
    #print('')
    #---------------------------------------------------------------------------------------------


    #---------------------------Decodificado sin ruido-------------------------------------------
    textoDecodificadoDeHamming=hamming.decodificacionHamming(textoCodificadoDeHamming)
    print('Texto recibido con errores corregidos:',textoDecodificadoDeHamming)
    print('')
    #--------------------------------------------------------------------------------------------


    #-----------------------------Descifrado de hill--------------------------------------------
    textoDescifradoHill=cifradoHill.cifDesHill(claveInv,textoDecodificadoDeHamming,diccionarioLongitud)
    print('Texto recibido decodificado es:',textoDescifradoHill)
    print('')
    print('')
    #-----------------------------------------------------------------------------------------
    print('-----------------------------------------------')
    print('')
    print('')
    input("")