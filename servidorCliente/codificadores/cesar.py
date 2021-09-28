import string 
from datetime import date

dia=date.today()
dia=int(dia.strftime("%d"))%25

alfabeto= list(string.ascii_lowercase)
#print(alfabeto)

def cifradoCesar(texto):
	texto=texto.lower()
	texto_cifrado= ""
	for letra in texto:
		if letra in alfabeto:
			indice_actual = alfabeto.index(letra)
			indice_cesar = indice_actual + dia
			if indice_cesar > 25:
				indice_cesar -= 25 
			texto_cifrado += alfabeto[indice_cesar]
		else:
			texto_cifrado += letra
	return texto_cifrado

#frase = "abcdefghijklmnopqrstuvwxyz"
#frase_cifrada = cifradoCesar(frase)
#print(frase_cifrada)

def decifradoCesar (texto):
	texto=texto.lower()
	texto_decodificado= ""
	for letra in texto:
		if letra in alfabeto:
			indice_cesar = alfabeto.index(letra)
			indice_original = indice_cesar - dia
			if indice_original < 0:
				indice_original += 25 
			texto_decodificado += alfabeto[indice_original]
		else:
			texto_decodificado += letra
	return texto_decodificado
#frase_decodificada = decifradoCesar(frase_cifrada)
#print(frase_decodificada)