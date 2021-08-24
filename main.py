import speech_recognition as sr

r = sr.Recognizer()

#microfono Lorenzo
mic = sr.Microphone(device_index=1)

#microfono Marcello e Massimiliano
#mic = sr.Microphone(device_index=0)

with mic as source:
    print("Aspetta. Sto calibrando il microfono...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Ora parla!!")
    audio = r.listen(source)

print("Hai detto '" + r.recognize_google(audio, language="it-IT") + "'")

