from modules.pepper import Pepper

emotions = ['angry', 'happy', 'sad']

def get_name_from_answer(ans):
    for s in ans.replace('. ','.').split('.'):
        up = [w for w in s[1:].split() if w[0].isupper()]
        for w in up:
            w = w.replace('.','').replace(',','')
            if w not in ['Pepper', 'I']: return w
    return None

def get_emotion_from_answer(ans):
    ans = ans.replace('.', ' ').replace(',',' ').lower().split()
    for w in ans:
        if w in emotions: return w
    return None


if __name__ == '__main__': 
    # init
    pepper = Pepper()

    # start camera streaming
    pepper.fer.set_emotions(emotions)
    pepper.fer.stream()
    
    # waiting face detection
    pepper.fer.wait_detection(fun=pepper.head_scan)

    # -----starting interaction

    # robot starts
    pepper.say('Hello human. I am Pepper the social robot. What is your name?')
    ans = pepper.wait_answer(timeout=10)
    name = get_name_from_answer(ans)

    pepper.say('It is very nice to meet you {}!'.format(name))
    pepper.human_name = name
    # starting emotion detection
    pepper.fer.start_detection()

    # asking for feeling
    pepper.say('How are you today {}?'.format(name), delay=2)
    ans = pepper.wait_answer(timeout=10)
    emotion = get_emotion_from_answer(ans)

    # stopping emotion detection
    pepper.fer.stop_detection()
    detected_emotion = pepper.fer.get_emotion()

    print(emotion, detected_emotion)

    while True:
        
        # human says thruth
        if emotion == detected_emotion:

            if emotion == 'happy':
                pepper.say('{}, it seems you are feeling really good today, dance with me!'.format(name))
                pepper.dance()
                pepper.say('It was funny {}. Have a nice day! :)'.format(name), delay=1)

            elif emotion == 'sad':
                pepper.say('oh, I see you are {} {} :('.format(emotion, name))
                pepper.say("I'll tell you something funny! ;)", delay=1)
                pepper.random_say('funny', delay=1)
                pepper.say('I hope you enjoyed it {}. Have a nice day! :)'.format(name), delay=1)

            elif emotion == 'angry':
                pepper.say('I think you need a break {}'.format(name))
                pepper.say('Do you want to play a game?', delay=1)
                pepper.say('Please {} say YES or NO'.format(name), delay=1)
                ans = pepper.wait_answer(timeout=10, text='Please {} say YES or NO'.format(name))
                if ans.lower() == 'yes':
                    pepper.say('ok {}, let\'s play a game together'.format(name), delay=1)
                    pepper.game()
                    pepper.say('Thank you for playing {}. Have a nice day! :)'.format(name), delay=2)
                else:
                    pepper.say('No problem {}, have a nice day! :)'.format(name))

            break

        # human says falseness
        else:

            if detected_emotion in ['angry', 'sad']:
                pepper.say('{}, are you sure you are not {}?'.format(name, detected_emotion))
                ans = pepper.wait_answer(timeout=10)
                emotion = get_emotion_from_answer(ans)
                
                if emotion != detected_emotion:
                    pepper.say('sorry {} I did not want to be invasive'.format(name))
                    pepper.say('Have a nice day! :)', delay=1)

                else: continue

            elif detected_emotion == 'happy':
                pepper.laugh()
                pepper.random_say('laughing', param=name, delay=1)
                pepper.say('Have a nice day! :)', delay=1)

            break

    # -----ending interaction
    pepper.stop()
