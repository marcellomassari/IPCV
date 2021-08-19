import speech_recognition as sr

r = sr.Recognizer()
#print(sr.Microphone.list_microphone_names())

#microfono Lorenzo
mic = sr.Microphone(device_index=1)

#microfono Marcello
#mic = sr.Microphone(device_index=0)

with mic as source:
    print("Please wait. Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=5)
    print("Say something!")
    audio = r.listen(source)

print("I thinks you said '" + r.recognize_google(audio, language="it-IT") + "'")


