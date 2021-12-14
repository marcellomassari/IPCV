import speech_recognition as sr
import object_detection

UTENTE_ID = -1

r = sr.Recognizer()

mic = sr.Microphone(device_index=0)

with mic as source:
    print("Aspetta. Sto calibrando il microfono...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Ora parla!!")
    audio = r.listen(source)

audio_stringa = r.recognize_google(audio, language="it-IT")
audio_vettore = audio_stringa.split()
print(audio_vettore)

if audio_vettore[0].lower() == "cerca":
    object = audio_vettore[len(audio_vettore)-1]
    if object == "tavolo":
        UTENTE_ID = 60
    elif object == "sedia":
        UTENTE_ID = 56
    elif object == "libro":
        UTENTE_ID = 73
    elif object == "divano":
        UTENTE_ID = 57
    elif object == "letto":
        UTENTE_ID = 59
    else:
        print("Richiesta non valida!")

    object_detection.start_video("videos/video_prova.mp4", utente_id=UTENTE_ID)
    #object_detection.webcam_detect(utente_id=UTENTE_ID)

elif audio_vettore[0].lower() == "posiziona":
   print("POSIZIONAMENTO OGGETTI")

print(UTENTE_ID)