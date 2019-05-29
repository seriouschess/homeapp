from db import db

class Poem_data(db.Model):
    __tablename__ = 'poem_data'
    id = db.Column(db.Integer, primary_key = True)
    poem_title = db.Column(db.String(80))
    poem_content = db.Column(db.String(120))
    poem_author = db.Column(db.String(80))

    def __init__(self, poem_title='?', poem_content='?', poem_author='?'):
        self.poem_title = poem_title
        self.poem_content = poem_content
        self.poem_author = poem_author

    @classmethod
    def update_list(cls):
        poems_list = []
        poems = cls.query.all()
        poem_count = 0
        for poem in poems:
            poem_count += 1
            dictionary = {"id":poem.id, "title":"Poem Number {}".format(poem_count), "body":poem.poem_content, "author":poem.poem_author}
            poems_list.append(dictionary)
        return poems_list

    def insertpoem(self): #inserts a new poem into the database with a title
        db.session.add(self)
        db.session.commit()
