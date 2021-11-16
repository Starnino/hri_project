from flask import Flask, request, render_template, Response
import threading, requests, os

class GameServer:

    def __init__(self, player, questions, answers, callback, host="127.0.0.1", port=5000):
        self.app = Flask(__name__, template_folder=os.getcwd()+'/templates')
        self.app.add_url_rule('/', 'index', self.index, methods=['GET', 'POST'])
        self.app.add_url_rule('/shutdown', 'shutdown', self.shutdown)
        self.host = host
        self.port = port
        self.player = player
        self.questions = questions
        self.answers = answers
        self.callback = callback
        self.score = 0
        self.total = len(questions)
        self.robot_answer = ''

    def shutdown(self):
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return "Shutting down..."

    def index(self):
        if request.method == 'GET':
            if not request.args:
                return render_template("index.html", name=self.player)
            else:
                response = Response(self.robot_answer)
                self.robot_answer = ''
                return response

        elif request.method == 'POST':
            if request.form['button'] == 'start':
                return render_template('game.html', question=self.questions.pop(0))
            else:
                answer = request.form['button']

                if 'robot' in request.form:
                    value = request.form['robot']
                    print(value)
                
                if self.answers.pop(0) == answer:
                    self.callback('true')
                    self.score += 1
                else:
                    self.callback('false')
                    
                if len(self.questions) == 0:
                    self.stop()
                    return render_template('end.html', score=self.score, l=self.total)
            
                return render_template("game.html", question=self.questions.pop(0))

    def answer(self, value):
        self.robot_answer = value

    def start(self):
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.run(host=self.host, threaded=True, port=self.port)
    
    def stop(self):
        resp = requests.get('http://'+self.host+':'+str(self.port)+'/shutdown')

if __name__ == "__main__":
    
    import time, sys
    s = GameServer()
    s.start()
    time.sleep(10)
    s.stop()
