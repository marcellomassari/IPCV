import cv2
import numpy as np

def load_yolo():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0,255, size=(len(classes), 3))
    return net, classes, colors, output_layers

def detect_objects(img, net, outputLayers):
    blob = cv2.dnn.blobFromImage(img, scalefactor=(1/255), size=(320,320), mean=(0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    return blob, outputs

def get_box_dimensions(outputs, height, width):
    boxes=[]
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            # select bounding box with confidence > 30%
            if conf > 0.3:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids

def draw_labels(boxes, confs, colors, class_ids, classes, img, IMG_OBJ, DIR, OBJ_REF_ID):
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            # IDENTIFICA SOLO CLASSE PRESCELTA
            if class_ids[i] == OBJ_REF_ID:
                x, y, w, h = boxes[i]

                down_width = int(w/4)
                down_height = int(h/2)
                down_points = (down_width, down_height)
                oggetto_add = cv2.resize(IMG_OBJ, down_points, interpolation=cv2.INTER_LINEAR)

                recenter = int(w/2) - int(down_width/2)
                adjust = int(h/15)

                oggetto_add2 = cv2.cvtColor(oggetto_add, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(oggetto_add2, 1, 255, cv2.THRESH_BINARY)
                if DIR == "sopra" or DIR == "sul" or DIR == "sull'":
                    h=int(-h/2)
                    if y+h+adjust<0:
                        print("Oggetto momentaneamente fuori dall'inquadratura. Riposizionare la webcam.")
                    else:
                        roi = img[y + h + adjust:y + h + adjust + down_height, x + recenter:x + recenter + down_width]
                        roi[np.where(mask)] = 0
                        roi += oggetto_add
                        tmp = cv2.add(roi, oggetto_add)
                        img[y + h + adjust :y + h + adjust + down_height, x + recenter:x + recenter + down_width] = tmp
                elif DIR == "sotto":
                    if OBJ_REF_ID==57 or OBJ_REF_ID==59:
                        print("Impossibile posizionare oggetto")
                    else:
                        roi = img[y + h - down_height:y + h, x + recenter:x + recenter + down_width]
                        roi[np.where(mask)] = 0
                        roi += oggetto_add
                        tmp = cv2.add(roi, oggetto_add)
                        img[y + h - down_height:y + h, x + recenter:x + recenter + down_width] = tmp
                elif DIR == "sinistra":
                    if x-down_width<0:
                        print("Oggetto fuori dall'inquadratura. Riposizionare la webcam")
                    else:
                        roi = img[y:y + down_height, x-down_width :x]
                        roi[np.where(mask)] = 0
                        roi += oggetto_add
                        tmp = cv2.add(roi, oggetto_add)
                        img[y:y + down_height, x-down_width:x] = tmp
                elif DIR == "destra":
                    if x+w+down_width > img.shape[1]:
                        print("Oggetto fuori dall'inquadratura. Riposizionare la webcam")
                    else:
                        roi = img[y:y+ down_height, x+w:x + w + down_width]
                        roi[np.where(mask)] = 0
                        roi += oggetto_add
                        tmp = cv2.add(roi, oggetto_add)
                        img[y:y + down_height + h, x+w:x + w + down_width] = tmp

        cv2.imshow("Image", img)


def start_video(video_path, IMG_OBJ, DIR, OBJ_REF_ID):
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(video_path)

    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame, IMG_OBJ, DIR, OBJ_REF_ID)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()


