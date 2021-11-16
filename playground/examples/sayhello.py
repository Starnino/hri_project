import os, qi, time

pip = os.getenv('PEPPER_IP') #Pepper IP
pport = 9559 #Pepper port

try:
	url = "tcp://" + pip + ":" + str(pport)
	app = qi.Application(["App", "--qi-url=" + url ])
except RuntimeError:
	print("Can't connect to Naoqi ...")
	
app.start()
session = app.session

time.sleep(2)
tts_service = session.service("ALTextToSpeech")
tts_service.setLanguage("English")
tts_service.setParameter("speed", 90)
tts_service.say("Hello. How are you?")
