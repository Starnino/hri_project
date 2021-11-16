import os, qi, _qi, time

pip = os.getenv('PEPPER_IP') #Pepper IP
pport = 9559 #Pepper port

try:
	url = "tcp://" + pip + ":" + str(pport)
	app = qi.Application(["App", "--qi-url=" + url ])
except RuntimeError:
	print("Can't connect to Naoqi ...")
	
app.start()
session = app.session

animation_player_service = session.service("ALAnimationPlayer")
f = animation_player_service.run("animations/Stand/Gestures/Hey_1", _async=True)
f.value()
foo = animation_player_service._getAnimations
#animation_player_service.run("animations/Bella")
print(animation_player_service._getPathsForTags())
