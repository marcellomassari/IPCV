import speech_recognition as sr
import object_detection
import object_insertion_2D
import cv2

termina = 0

r = sr.Recognizer()
mic = sr.Microphone(device_index=0)

print("Benvenuto, sono l'assistente vocale Mebel.")
print("Posso cercare oggetti nella tua stanza o aggiungerne di nuovi!")

while termina == 0:

    with mic as source:
        print("Aspetta solo un momento. Sto calibrando il microfono...")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Ora parla!!")
        audio = r.listen(source)

    audio_stringa = r.recognize_google(audio, language="it-IT")
    audio_vettore = audio_stringa.split()
    print(audio_vettore)

    if audio_vettore[0].lower() == "cerca":
        object = audio_vettore[len(audio_vettore)-1]
        if object == "tavolo":
            OBJ_ID = 60
        elif object == "sedia":
            OBJ_ID = 56
        elif object == "libro":
            OBJ_ID = 73
        elif object == "divano":
            OBJ_ID = 57
        elif object == "letto":
            OBJ_ID = 59
        else:
            print("Richiesta non valida!")
            OBJ_ID = -1

        print("Per inserire un nuovo comando premere ESC, grazie!")
        object_detection.start_video("videos/video_prova.mp4", OBJ_ID)

    elif audio_vettore[0].lower() == "posiziona":
        object_pos = audio_vettore[2]
        object_ref = audio_vettore[len(audio_vettore)-1]

        if len(audio_vettore) == 5:
            direction = audio_vettore[3]
        elif len(audio_vettore) == 6:
            direction = audio_vettore[3]
        elif len(audio_vettore) == 7:
            direction = audio_vettore[4]

        if object_ref == "tavolo":
            OBJ_REF_ID = 60
        elif object_ref == "sedia":
            OBJ_REF_ID = 56
        elif object_ref == "divano":
            OBJ_REF_ID = 57
        elif object_ref == "letto":
            OBJ_REF_ID = 59
        else:
            print("Richiesta non valida!")

        if object_pos == "vaso":
            IMG_OBJ = cv2.imread("objects/vaso.png")
        elif object_pos == "lampada":
            IMG_OBJ = cv2.imread("objects/lampada.png")
        elif object_pos == "piatto":
            IMG_OBJ = cv2.imread("objects/piatto.png")
        elif object_pos == "televisore":
            IMG_OBJ = cv2.imread("objects/televisore.png")

        print("Per inserire un nuovo comando premere ESC, grazie!")
        #object_insertion_2D.start_video("videos/video_prova.mp4", IMG_OBJ, direction, OBJ_REF_ID)
        object_insertion_2D.start_video(0, IMG_OBJ, direction, OBJ_REF_ID)

    elif audio_vettore[0].lower() == "termina":
        print("Grazie per aver utilizzato la nostra applicazione. Alla prossima!!")
        termina = 1

    else:
        print("Comando non valido. Ripetere per favore")

