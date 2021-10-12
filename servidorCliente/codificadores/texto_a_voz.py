from gtts import gTTS
#from playsound import playsound
import pygame
import pathlib
#from datetime import datetime
from mutagen.mp3 import MP3

def mp3Path():
    path=str(pathlib.Path(__file__).parent.resolve())
    path=path.replace("\\","/")

    #fechaHora=datetime.now()
    #dt_string=fechaHora.strftime("%d-%m-%Y")

    #path=path+"/"+dt_string+".mp3"
    
    path=path+"/audio.mp3"
    #print(path)
    return path
def duracion(path):
    audio=MP3(path)
    time=int(audio.info.length*1000)
    return time

def textoAVoz(texto):
    path=mp3Path()
    pygame.init()
    pygame.mixer.init()
    try:
        if(texto):
            texto=texto.replace("[","")
            texto=texto.replace("]"," dice:")
            #print(texto)
            tts = gTTS(text=texto, lang='es-us')
            tts.save(path)
            
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            
            pygame.mixer.music.play()
            pygame.time.delay(duracion(path))
            pygame.mixer.music.unload()
            
        else:
            tts = gTTS("Mensaje vacio",lang='es-us')
            tts.save(path)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            pygame.time.delay(duracion(path))
            pygame.mixer.music.unload()
           
    except:
        tts=gTTS('error al reproducir mensaje',lang='es-us')
        tts.save(path)
        #pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.time.delay(duracion(path))
        pygame.mixer.music.unload()
        #playsound(path)

#textoAVoz("hola a todos")