import os, qi, time, random, threading
from modules.fer import FER
from modules.server import GameServer

misund = ['I am sorry, I did not understand. Could you repeat it please?',
           'Maybe my robotic ears did not work well, say it again please',
           'I am sorry, byt I did not hear you, please say it loudly!']

funny = ['Why are robots shy?\nBecause they have hardware and software but no unerware.',
         'A robot walks into a bar, orders a drink, and lays down some cash.\nThe bartender says, \"we don\'t serve robots.\" The robot replies, \"oh, but some day you will.\"',
         'Did you hear about the robot who tried to escape imprisonment?\nDon\'t worry, he got reCAPTCHA!']

laugh = ['ahahaha you are so funny {} :\')', 'Nice one {}! :\')']

true_ans = ['Wow!', 'Great job', 'Well done!', 'It is correct!']
false_ans = ['Nope :(', 'Wrong answer!', 'That was close!', 'Come on, you can do better!'] 

questions = ['Robots can move in different ways', 'Robots can build cars', 'Robots can sleep', 'Robots are stronger than people','The word "robot" comes from the czech "robota", which means "slavery"/"hard work"', 'Pepper robot was built for playing football', 'Robots can (digitally) see the environment']
answers = ['true', 'true', 'false', 'true', 'true', 'false', 'true']

class Pepper:

        def __init__(self, test=False):
                pip = os.getenv('PEPPER_IP') #Pepper IP
                pport = 9559 #Pepper port

                try:
                        url = "tcp://" + pip + ":" + str(pport)
	                self.app = qi.Application(["App", "--qi-url=" + url])
                except RuntimeError:
                        print("Can't connect to Naoqi ...")
	
                self.app.start()
                
                #starting services
                self.memory_service  = self.app.session.service("ALMemory")
                self.motion_service  = self.app.session.service("ALMotion")
                self.ans_service = self.app.session.service("ALAnimatedSpeech")
                self.touch_service = self.app.session.service("ALTouch")

                #face emotion recognition system
                self.fer = FER() if not test else None

                # game flags
                self.human_name = 'human'
                self.server = None

                #keys
                self.fakeasr_key = 'Robot/ASR'

                # joints
                self.joints = ["HeadYaw", "HeadPitch",
                               "LShoulderPitch", "LShoulderRoll",
                               "RShoulderPitch", "RShoulderRoll",
                               "LElbowYaw", "LElbowRoll",
                               "RElbowYaw", "RElbowRoll",
                               "LWristYaw", "RWristYaw"]

                # events
                t = threading.Thread(target=self.__event_handler)
                t.start()

        def stop(self):
                self.app.stop()
                if self.fer is not None:
                        self.fer.end_detection()
                        
        # ----- speech
        
        def say(self, text, delay=0):
                time.sleep(delay)
                configuration = {'bodyLanguageMode':'contextual'}
                self.ans_service.say(text, configuration)

        def random_say(self, context, param=None, delay=0):
                if context == 'misunderstanding':
                        self.say(random.choice(misund), delay=delay)
                elif context == 'funny':
                        self.say(random.choice(funny), delay=delay)
                elif context == 'laughing':
                        self.say(random.choice(laugh).format(param), delay=delay)
                elif context == 'true':
                        self.say(random.choice(true_ans), delay=delay)       
                elif context == 'false':
                        self.say(random.choice(false_ans), delay=delay)

        def _fakeasr(self):
                return self.memory_service.getData(self.fakeasr_key)

        def wait_answer(self, timeout=5, text=None):
                self.memory_service.insertData(self.fakeasr_key, None)
                while True:
                        time.sleep(timeout)
                        ans = self._fakeasr()
                        if ans is not None: return ans
                        if text is not None:
                                self.say(text)
                        else:
                                self.random_say('misunderstanding')

        # ----- motion
                
        
        def laugh(self, time=0.1, moves=5):
                joint = "HeadPitch"
                for _ in range(moves):
                        # look up
                        self.motion_service.angleInterpolation(joint, -0.1, time, True)
                        # look down
                        self.motion_service.angleInterpolation(joint, -0.3, time*2, True)
                # look center
                self.motion_service.angleInterpolation(joint, -0.2, time, True)

        def dance(self, moves=4):
                joints = ['HeadPitch', 'HeadYaw', 'RElbowYaw', 'RElbowRoll', 'RShoulderPitch', 'LElbowYaw', 'LElbowRoll', 'LShoulderPitch']
                times = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
                
                for i in range(moves):
                        angles = [0.5, 0, 1.48, 2, -0.4, -1.43, -2, 0.5]
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [-0.2, 0, 1.48, 1, -0.25, -1.43, -1, 0.25] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                for i in range(moves):
                        angles = [0.5, 0, 1.48, 2, 0, -1.43, -2, -0.5]
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [-0.2, 0, 1.48, 1, 0.25, -1.43, -1, -0.25] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                for i in range(int(moves/2)):
                        angles = [0, 0.5, 1, 2, 0.1, -1.9, -2, 0.2]
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [0, 0, 1.48, 2, 0.1, -1.43, -2, 0.2] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [0, 0.5, 1, 2, 0.1, -1.9, -2, 0.2] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                for i in range(int(moves/2)):
                        angles = [0, -0.5, 1.9, 2, 0.1, -1, -2, 0.2]
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [0, 0, 1.48, 2, 0.1, -1.43, -2, 0.2] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                        angles = [0, -0.5, 1.9, 2, 0.1, -1, -2, 0.2] 
                        self.motion_service.angleInterpolation(joints, angles, times, True)
                times = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                angles = [-0.5, 0, 1.48, 0, 2, -1.43, 0, -1.2]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                time.sleep(1)
                
                # return to posture
                angles = [0, 0, 1.48, 0, 1.6, -1.43, 0, 1.6]
                self.motion_service.angleInterpolation(joints, angles, times, True)


        def head_scan(self):
                joints = ["HeadYaw", "HeadPitch"]
                times = [1, 0.5]
                # look left
                angles = [1, -0.2]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                # look right
                angles = [-1, -0.2]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                # look center
                angles = [0, 0]
                self.motion_service.angleInterpolation(joints, angles, times, True)

        def _touch_head(self):
                joints = ["HeadPitch", 'RElbowRoll', 'RElbowYaw', 'RShoulderPitch']
                times = [1, 1, 1, 1]
                # touch head
                angles = [0.5, 4, 0.9, -0.5]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                # say
                self.say('oh, you touched my head!')
                # return to posture
                angles = [0, 0, 1.47, 1.6]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                

        def _look_hand(self, hand):
                elbowRoll = 'RElbowRoll' if hand == 'right' else 'LElbowRoll'
                joints = ["HeadYaw", "HeadPitch", elbowRoll]
                times = [0.8, 0.8, 0.8]
                # look left/right hand
                angles = [-0.2, 1, 1.2] if hand == 'right' else [0.2, 1, -1.2]
                self.motion_service.angleInterpolation(joints, angles, times, True)
                # say
                if self.server is None:
                        self.say('oh, you touched my {} hand!'.format(hand))
                # return to posture
                angles = [0, 0, 0]
                self.motion_service.angleInterpolation(joints, angles, times, True)

        # ----- events and callbacks
        
        def __event_handler(self):
                # subscribe to events
                fakeasr_event = 'Robot/ASR_event'
                asr = self.memory_service.subscriber(fakeasr_event)
                asr.signal.connect(self.on_ASR)
                
                touch_event = 'TouchChanged'
                ht = self.memory_service.subscriber(touch_event)
                ht.signal.connect(self.on_touch)

                # listen
                self.app.run()

        def on_ASR(self, value):
                self.fer.display_bubble_text(value)

        def on_touch(self, value):
                status = self.touch_service.getStatus()
                for s in status:
                        if s[1]:
                                sensor = s[0].split('/')[0]
                                if sensor == 'Head':
                                        self.fer.display_bubble_text('Simulating head touch')
                                        self._touch_head()
                                        break
                                
                                elif sensor[1:] == 'Hand':
                                        s = 'right' if sensor[0] == 'R' else 'left'
                                        if self.fer is not None:
                                                self.fer.display_bubble_text('Simulating {} hand touch'.format(s))
                                        self._look_hand(s)
                                        
                                        if self.server is not None:
                                                ans = 'true' if s == 'right' else 'false'
                                                self.server.answer(ans)
                                        break
                                        
        # ----- game

        def game(self):
                # rules
                self.say('The game is True or False. In order to answer you can either touch the tablet or touch my hands.', delay=1)
                self.say('If you touch my RIGHT hand, than the answer is TRUE', delay=1)
                self.say('If you touch my LEFT hand instead, the answer is FALSE', delay=0.5)
                self.say('Are you ready {}? let\'s start!'.format(self.human_name), delay=1)
                self.say('Look at the tablet')
                # start game
                callback = lambda value: self.random_say(value)          
                self.server = GameServer(player=self.human_name,
                                    questions=questions,
                                    answers=answers,
                                    callback=callback)
                                
                self.server.start()
                self.server = None
                # end game

        
                
