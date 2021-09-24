from sympy import *
import random as rnd


def textEntrada():
    try:
        text = input("Ingrese el texto: ").upper()
        return text
    except:
        print("Texto no valido")
        return 0


def textCambio(origiText, dic1):#Cambiando valores a numeros
    numText = Matrix()
    parText = []
    cont0 = 0
    cont1 = 0
    if(len(origiText) % 2 != 0):
        origiText = origiText+" "
    for caracter in origiText:
        try:
            parText.append(dic1[caracter])
            cont0 += 1
            if(cont0 == 2):
                numText = numText.col_insert(cont1, Matrix(parText))
                parText = []
                cont1 += 1
                cont0 = 0
        except:#deteccion de errores caracter no encontrado
            parText.append(dic1[" "])
            cont0 += 1
            if(cont0 == 2):
                numText = numText.col_insert(cont1, Matrix(parText))
                parText = []
                cont1 += 1
                cont0 = 0
            print("Caracter no encontrado: " +
                  caracter+" reemplazado por espacio")
    return numText

def cifDesHill(clave, texto,detN):
    # Cambio de texto a su equivalente numerico
    textCodificado = textCambio(texto, dic1)
    textCifradoMat = Matrix()
    textaux0 = []
    textCif = ""
    try:
        for parColumna in range(0, textCodificado.shape[1]):
            #colTexCod = (clave*textCodificado.col(parColumna)) % detN  # cifrado en modulo 28
            textCifradoMat = textCifradoMat.col_insert(parColumna, (clave*textCodificado.col(parColumna)) % detN)#Ingresa el par de valores cifrados en una matriz distinta

        for colCifrada in range(0, textCifradoMat.shape[1]):
            #colx = textCifradoMat.col(colCifrada)
            textaux0.append(reLlave(textCifradoMat.col(colCifrada)[0], dic1))
            textaux0.append(reLlave(textCifradoMat.col(colCifrada)[1], dic1))
        for caracter in textaux0:
            textCif = textCif+caracter
        return textCif
    except Exception as exc:
        print("No se pudo cifrar el texto")
        print(str(exc))
        return("Err")


def reLlave(valor_i, dic):  # recupera la llave del diccionario segun su valor numerico
    try:
        for llave, valor in dic.items():
            if(valor_i == valor):
                return llave
    except:
        print("No se encuentra la llave del valor")
        return " "


def invModN(matClave,detN):
    res = 0
    x = 0
    mod = 0
    det = matClave.det()
    while(mod != 1 % detN):#matriz inversa.
        res = det*x
        mod = res % detN
        x += 1
    matClave = ((matClave.inv()*det)*(x-1)) % detN
    return matClave


def claveMatrizGen(detN):  # Generador de matriz clave aleatoria
    clave = Matrix()
    filax = []
    for fila in range(0, 2):
        for a in range(0, 2):
            filax.append((rnd.randint(0, 100)) % detN)
        clave = clave.row_insert(fila, Matrix([filax]))
        filax = []
    return clave % detN

dic1 = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
        "K": 10,"L": 11, "M": 12, "N": 13, "Ñ": 14,"O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
        "T": 20,"U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, " ": 27, "?": 28,"1":29,
        "2":30,"3":31,"4":32,"5":33,"6":34,"7":35,"8":36,"9":37,"0":38}
numeroCaracteres=len(dic1)

#det = 0
"""
while(det == 0):  # Obtencion de clave aleatoria para cifrar si el determinante no es 0 es aceptable
    clave = claveMatrizGen(ndet)
    det = clave.det()

"""
# Se obtiene la matriz inversa de la clave en modulo 39


#clave=Matrix([[4,8],[2,3]]) #Clave para cifrar
clave=Matrix([[3,4],[2,1]]) #Clave para cifrar
claveInv = invModN(clave,numeroCaracteres)

estado = True
"""
while(estado):
    print("---------------Cifrado/descifrado de hill----------------")
    print(                ****Opciones****
                 *1)Cifrar      *
                 *2)Descifrar   *
                 *3)Salir       *
                 ****************)
    try:
        opc = input("-> ")
        if(opc == "1"):
            texto = textEntrada()
            textCifrado = cifDesHill(clave, texto,numeroCaracteres)
            print("-----------------Cifrado-------------------")
            print("Entrada=> "+texto)
            print("Salida => "+textCifrado)
            print("-------------------------------------------")
        elif(opc == "2"):
            texto = textEntrada()
            textDescifrado = cifDesHill(claveInv, texto,numeroCaracteres)
            print("-----------------Descifrado----------------")
            print("Entrada=>"+texto)
            print("Salida =>"+textDescifrado)
            print("-------------------------------------------")

        elif(opc == "3"):
            estado = False

        else:
            print("Opción incorrecta")
    except Exception as exc:
        print("Algo a ido mal intentalo nuevamente")
        print(str(exc))

Necesitas usar 
    textEntrada
    cifDesHill
    invMod28
"""