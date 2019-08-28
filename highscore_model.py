from db import db

class Highscore_data(db.Model):
    __tablename__ = 'highscore_data'
    id = db.Column(db.Integer, primary_key = True)
    highscore_value = db.Column(db.Integer())
    highscore_initials = db.Column(db.String(3))

    def __init__(self, highscore_value='?', highscore_initials='?'):
        self.highscore_value = highscore_value
        self.highscore_initials = highscore_initials

    @classmethod
    def update_list(cls):
        highscores_list = []
        highscores = cls.query.all()
        for score in highscores:
            dictionary = {"id":score.id, "value":score.highscore_value, "initials":score.highscore_initials}
            highscores_list.append(dictionary)

        sorted_scores = []

        while len(highscores_list) > 0:
            largest = 0
            largest_x = 9,000 #default value irrelevent
            for x in range(0, len(highscores_list)):
                #print(highscores_list[x]["value"]) #for testing lol god help me
                if int(highscores_list[x]["value"]) >= largest:
                    largest = highscores_list[x]["value"]
                    largest_x = x
            sorted_scores.append(highscores_list[largest_x])
            highscores_list.pop(largest_x)

        return sorted_scores #returns sorted list dictionaries contining highscores

    @classmethod
    def clean(cls, lowest_highscore):
        highscores = cls.query.all()
        for score in highscores:
            if (score.highscore_value < lowest_highscore):
                db.session.delete(score)
        db.session.commit()

    def insert_score(self): #inserts a new score into the database
        db.session.add(self)
        db.session.commit()
