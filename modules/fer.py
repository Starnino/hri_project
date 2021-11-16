import cv2
import requests
import os
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
from time import sleep
import threading

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class FER:
    
    def __init__(self):
        self._emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.emotions = self._emotions
        self.face_cascade = None
        self.model = None
        self.last = None
        self.detection = False
        self.detected = False
        self.frames = None
        self.end = False
        self.display_bubble = False

    def __stream(self):

        #opencv initialization
        haar = 'models/haarcascade_frontalface_default.xml'
        if not os.path.isfile(haar):
            url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
            r = requests.get(url, allow_redirects=True)
            open(haar, 'wb').write(r.content)

        self.face_cascade = cv2.CascadeClassifier(haar)

        #face expression recognizer initialization
        structure = "models/facial_expression_model_structure.json"
        if not os.path.isfile(structure):
            url = 'https://raw.githubusercontent.com/serengil/tensorflow-101/master/model/facial_expression_model_structure.json'
            r = requests.get(url, allow_redirects=True)
            open(structure, 'wb').write(r.content)
    
        self.model = model_from_json(open(structure, "r").read())

        weights = 'models/facial_expression_model_weights.h5'
        if not os.path.isfile(weights):
            url = 'https://github.com/serengil/tensorflow-101/raw/master/model/facial_expression_model_weights.h5'
            r = requests.get(url, allow_redirects=True)
            open(weights, 'wb').write(r.content)

        self.model.load_weights(weights)
        #-----------------------------
        
        cap = cv2.VideoCapture(0)
        
        iteration = 0
        em_count = {key:0 for key in self.emotions}
        
        while True:
            
            # Capture frame-by-frame
            ret, frame = cap.read()
            iteration += 1
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # apply face detection procedures
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            self.detected = False if len(faces) == 0 else True
            
            if self.detection:
        
		for (x,y,w,h) in faces:
                    
		    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,0), 2) #draw rectangle to main image
		              
		    detected_face = frame[int(y):int(y+h), int(x):int(x+w)] #crop detected face
		    detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
		    detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

		    img_pixels = image.img_to_array(detected_face)
		    img_pixels = np.expand_dims(img_pixels, axis=0)
		    img_pixels /= 255 # normalize all pixels in scale of [0,1]
		              
		    predictions = self.model.predict(img_pixels) #store probabilities of 7 expressions
		              
		    percentages = predictions[0]/np.sum(predictions[0])*100
		    indexes = (-percentages).argsort()

                    for i in range(len(self.emotions)):
                        if self._emotions[indexes[i]] in self.emotions:
                            emotion = self._emotions[indexes[i]]
                            break
		                  
		    em_count[emotion] += 1
		        
		    # write emotion text
                    if self.last is not None:
		        cv2.rectangle(frame, (x,y), (x+120,y+35), (0,0,0), -1)
		        cv2.putText(frame, self.last, (int(x), int(y)+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
		        
		    if iteration%self.frames == 0: 
		        self.last = max(em_count, key=em_count.get)
		        em_count = {key:0 for key in self.emotions}

            # write bubble text
            if self.display_bubble:
                w, h = cap.get(3), cap.get(4)
                offset = 4*len(self.bubble_text)
                cv2.rectangle(frame, (int(w/2)-offset-20, int(h/2)-125), (int(w/2)+offset+40, int(h/2)-85), (255,255,255), -1)
                cv2.putText(frame, self.bubble_text, (int(w/2)-offset, int(h/2)-100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
                self.bubble_frames -= 1
                if self.bubble_frames == 0:
                    self.display_bubble = False
                    
	    #-------------------------
            
            # show image frame
            cv2.imshow('robot camera', frame)

            if (cv2.waitKey(1) & 0xFF == ord('q')) or self.end:
                break
        
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def stream(self):
        self.thread = threading.Thread(target=self.__stream)
        self.thread.start()
        
    def start_detection(self, frames=10):
        self.frames = frames
        self.detection = True

    def wait_detection(self, fun):
        t = threading.Thread(target=self.__thread_fun, args=(fun,))
        t.start()
        while not self.detected: continue
        t.do_run = False
        return

    def __thread_fun(self, fun):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            fun()

    def stop_detection(self):
        self.detection = False

    def end_detection(self):
        self.end = True

    def set_emotions(self, emotions):
        self.emotions = emotions
        
    def get_emotion(self):
        return self.last

    def display_bubble_text(self, text):
        text_len = len(text)
        self.display_bubble = True
        self.bubble_text = text
        if text_len < 5:
            self.bubble_frames = 20
        else:
            self.bubble_frames = text_len*2
        
        
if __name__ == "__main__":
    fer = FER()
    fer.stream()
    fer.start_detection()
    if fer.wait_detection(): print('trovato')
