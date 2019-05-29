from homeapp import app
from db import db

db.init_app(app)

@app.before_first_request #first thing the server does
def create_tables():
    db.create_all() #creates data.db unless it exists already
