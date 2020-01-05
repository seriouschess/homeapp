import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from poem_model import Poem_data
from highscore_model import Highscore_data
#from fortyk.KnightKiller import KnightKiller **works on windows but not linux**
from KnightKiller import KnightKiller
from SCBC import TerranSimulation

app = Flask(__name__)
#'sqlite:///data.db' for local testing
#'sqlite:////var/www/html/homeapp/data.db' for server deployment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/html/homeapp/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turned off to save resources. SQLAlchemy has its own tracker to match object variables to database values
app.config['SQALCHEMY_RECORD_QUERIES'] = True #for debugging queries only

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/') #Homepage
def home():
    return render_template('home.html')

@app.route('/about')
def portfolio_display():
    return render_template('portfolio.html')

@app.route('/jquery')
def jquery():
    path = r"/var/www/html/homeapp/jquery"
    #"C:\Users\Admin\PycharmProjects\jquery_test\code\jquery" #NOT FOR USE WITH UNIX!! DEBUG ONLY!
    #"/var/www/html/homeapp/jquery"
    return send_from_directory(path, 'jquery.js')

@app.route('/poems')
def poems():
    poems_list = Poem_data.update_list()
    return render_template('poems.html', poems = poems_list)

@app.route('/poems', methods=['POST'])
def input_poem():
    try: #delete method. It's here because HTML forms don't trust delete methods.
        Poem_data.delete_by_id(int(request.form['poemid']))
    except:
        pass
    try:
        new_poem = Poem_data()
        new_poem.poem_content = request.form['text'] #request from HTML form
        new_poem.insertpoem()
    except:
        pass
    poems_list = Poem_data.update_list()
    return render_template('poems.html', poems = poems_list)

@app.route('/40k')
def Test_roller():
    return render_template('test_roller.html')

@app.route('/40k', methods=['POST'])
def calculate_attack():
    new_attack = KnightKiller(request.form['attacker'], request.form['target'], int(request.form['hiton']))
    (average_attacks, dmg_list) = new_attack.calculate_attack()
    return render_template('test_roller_results.html', Average = average_attacks, damage_list=dmg_list)

@app.route('/asteroids')
def Asteroids():
    return render_template('Asteroids.html')

@app.route('/highscores')
def highscores():
    Highscores = Highscore_data.update_list()
    return render_template('highscores.html', score_list = Highscores)

@app.route('/get_tenth', methods = ['GET'])
def get_tenth():
        Highscores = Highscore_data.update_list()
        return jsonify(tenth_place = Highscores[9]["value"]) #tenth_place

@app.route('/initialize_scores') #used by developer to initialize table
def initialize_highscores():
    if (len(Highscore_data.update_list()) < 10): #only execute if table does not have 10 values
        for x in range(0,10): #create 10 scores (top 10)
            score_object = Highscore_data()
            score_object.highscore_value = 50
            score_object.highscore_initials = "AAA"
            score_object.insert_score()
    return render_template('highscores.html')

@app.route('/post_score', methods = ["POST"])
def postscore():
    new_highscore = Highscore_data()
    new_highscore.highscore_value = int(request.json["value"])
    new_highscore.highscore_initials = request.json["initials"]
    print(new_highscore.highscore_value)
    new_highscore.insert_score()
    Highscores = Highscore_data.update_list()
    Highscore_data.clean(Highscores[10]["value"]) #delete all scores below 11th place to save storage
    return jsonify(score_added = True)

@app.route('/starcraft')
def SC_Build_Calculator():
    return render_template('StarcraftCalculator.html')

@app.route('/starcraft', methods=['POST'])
def Calculate_Build():
    Minutes = TerranSimulation.run()
    return render_template('StarcraftCalculatorP.html', Minutes = Minutes)

if __name__ == '__main__': #allows localhost testing
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)
