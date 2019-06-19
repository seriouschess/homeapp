import os
from flask import Flask, render_template, request
from poem_model import Poem_data
#from fortyk.KnightKiller import KnightKiller
from KnightKiller import KnightKiller

app = Flask(__name__)
#'sqlite:///data.db' for local testing
#'sqlite:////var/www/html/homeapp/data.db' for server deployment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/html/homeapp/data.db' #required to have postgres on the server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turned off to save resources. SQLAlchemy has its own tracker to match object variables to database values
app.config['SQALCHEMY_RECORD_QUERIES'] = True #for debugging queries only

@app.route('/') #/ means homepage of the site
def home():
    return render_template('home.html')

@app.route('/poems')
def poems():
    poems_list = Poem_data.update_list()
    return render_template('poems.html', poems = poems_list)

@app.route('/poems', methods=['POST'])
def input_poem():
    try: #delete method. It's here because HTML forms aren't trusted.
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

if __name__ == '__main__': #allows localhost testing
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)
