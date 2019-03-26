# USAGE
# python deep_learning_object_detection.py --image images/example_01.jpg \
# --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# python detection_5secs.py --prototxt prototxt.txt --model model
# above line is for videos

# ssh -X -i ~/.ssh/my-ssh-key -C akashkomarika_10@35.196.221.168

# import the necessary packages
import numpy as np
import argparse
import cv2
import math

val=0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


# initialize the list of class 	labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "vehicle", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])


# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)
#cap = cv2.VideoCapture(" pedestrian1.mp4")
cap = cv2.VideoCapture("video9.mp4")
#cap = cv2.VideoCapture("bus1.mp4")
#cap = cv2.VideoCapture("video3.mp4")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

fourcc =cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc , 20.0, (frame_width,frame_height))

while True:

    ret, image = cap.read()
    (h, w) = image.shape[:2]# height , width	
#    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions

#   print("[INFO] computing object detectionss...")
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]
        
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
#        if confidence > args["confidence"]:
        if confidence > args["confidence"]:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            
            if idx == 7 or idx == 15 or idx == 6:#only cars-7 , trucks - 6 and pedestrians-15
		    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		    (startX, startY, endX, endY) = box.astype("int")
		    area = (startX-endX)*(startY-endY)
                    tmp =  1500/math.sqrt(area)    		    
                    
                    if idx ==15 :#person
                        tmp = tmp / 3    

		    # display the prediction
		    #label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		    label = "{}, {}".format(CLASSES[idx],str(int(tmp)) +"m")
		    
                    if tmp < 8 and idx == 15:
                        cv2.rectangle(image, (startX, startY), (endX, endY),
		        [0,0,255], 15)
                    elif tmp < 15 and ( idx == 6 or idx == 7 ) :
                        cv2.rectangle(image, (startX, startY), (endX, endY),
		        [0,0,255], 15)
                    else:                    
		        cv2.rectangle(image, (startX, startY), (endX, endY),
		        COLORS[idx], 2)
                     
		    y = startY - 15 if startY - 15 > 15 else startY + 15
		    cv2.putText(image, label, (startX, y),
		        cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLORS[idx], 2)


    out.write(image)    
#    cv2.imshow("Output", image)
     
    if val==1:
        cv2.destroyAllWindows()
        print main_func('result.png')
        break
    if cv2.waitKey(33)==27:
	cap.release()
        out.release()
	break
    
cv2.waitKey(0)
