from flask import Flask, render_template, request
#import data
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



#SQLALCHEMY
Base = declarative_base() #establishes an sql database mapping so that database classes can be used.

class Poem_data(Base):
    __tablename__ = 'poem_data'

    id = Column(Integer, primary_key=True)
    poem_title = Column(String)
    poem_content = Column(String)
    poem_author = Column(String)

    def __repr__(self):
        return "<Poem_data(poem_title='%s', poem_content='%s', poem_author='%s')>" % (self.poem_title, self.poem_content, self.poem_author)

engine = create_engine('sqlite:///data.db', echo=True) #sqlite:///data.db

Base.metadata.create_all(bind=engine) #creates the data.db
Session = sessionmaker(bind=engine)

'''
example1 = Poem_data()
#example1.id = 1 adding this line causes an error.
example1.poem_title = 'Example1'
example1.poem_content = 'Things about kings'
example1.poem_author = 'Johnathon Steed'
session.add(example1)
session.commit()
'''

def updatedb():
    session = Session()
    poems_list = []
    poems = session.query(Poem_data).all()
    for poem in poems:
        dictionary = {"id":poem.id, "title":poem.poem_title, "body":poem.poem_content, "author":poem.poem_author}
        poems_list.append(dictionary)
    session.close()
    return poems_list

poems_list = updatedb()

#FLASK
app = Flask(__name__) #gives file a unique name. Name is randomised
#Poems = data.Poems() OLD WAY
@app.route('/') #/ means homepage of the site
def home():
    return render_template('home.html')

@app.route('/poems')
def poems():
    return render_template('poems.html', poems = poems_list)

@app.route('/poems', methods=['POST'])
def input_poem():
    session = Session() #from sqlalchemy
    new_poem = Poem_data()
    new_poem.poem_content = request.form['text']
    new_poem.poem_title = "Filler"
    session.add(new_poem)
    session.commit()
    session.close()
    poems_list = updatedb()
    return render_template('poems.html', poems = poems_list)


if __name__ == '__main__':
    app.run() #port5000
