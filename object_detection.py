import cv2
import numpy as np
import argparse
import time
import matplotlib.pyplot as plt

def load_yolo():
    # load YoloV3 weights and configuration file
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # store names of coco.names in a list
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # pass in the names of the layers for which the output is to be computed
    # net.getUnconnectedOutLayers() returns the indices of the output layers of the network
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0,255, size=(len(classes), 3))
    return net, classes, colors, output_layers

def load_image(img_path):
    # image loading
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    return img, height, width, channels

def detect_objects(img, net, outputLayers):
    # blobFromImage preprocesses our image to predict the objects. Performs scaling, mean, subtraction and channel swap
    # scalefactor = 1/255 to scale image pixels in the range of [0..1]
    blob = cv2.dnn.blobFromImage(img, scalefactor=(1/255), size=(320,320), mean=(0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    # forward() returns a nested list containing information about all the detected objects:
    # x and y of the center of the object; heigth and width of the bounding box; confidence and scores for all the classes of objects listed in coco.names
    outputs = net.forward(outputLayers)
    return blob, outputs

def get_box_dimensions(outputs, height, width):
    boxes=[]
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            #print(scores)
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

def draw_labels(boxes, confs, colors, class_ids, classes, img):
    # draw the bounding box and add an object label to it
    # NMSBoxes --> Non-Maximum Suppression --> we pass in confidence threshold value and NMS threshold value as parameters to select one bounding box.
    # From the range 0 to 1 we should select an intermediate value like 0.4 or 0.5
    # to make sure that we detect thew overlapping objects but do not end up getting multiple bounding boxes for the same object.
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x, y-5), font, 1, color, 1)
        cv2.imshow("Image", img)


def image_detect(img_path):
    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs, = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    draw_labels(boxes, confs, colors, class_ids, classes, image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break


def webcam_detect():
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors,class_ids, classes, frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()

def start_video(video_path):
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(video_path)
    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()

if __name__ == "__main__":
    img_path = "images/strada_prova.jpeg"
    video_path = "videos/video_prova.mp4"
    #image_detect(img_path)
    #webcam_detect()
    start_video(video_path)

    cv2.destroyAllWindows()