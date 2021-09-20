import speech_recognition as sr

UTENTE_ID = -1

r = sr.Recognizer()

#microfono Lorenzo
#mic = sr.Microphone(device_index=1)

#microfono Marcello e Massimiliano
mic = sr.Microphone(device_index=0)

with mic as source:
    print("Aspetta. Sto calibrando il microfono...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Ora parla!!")
    audio = r.listen(source)

#print("Hai detto '" + r.recognize_google(audio, language="it-IT") + "'")
if r.recognize_google(audio, language="it-IT") == "Cerca oggetti":
    print("Cosa vuoi cercare?")


elif r.recognize_google(audio, language="it-IT") == "Posiziona oggetti":
    print("POSIZIONA OGGETTI")