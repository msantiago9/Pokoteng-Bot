import os
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import url_for
from werkzeug.utils import redirect

# loads environment variables, such as database_url.
load_dotenv(find_dotenv())

# initializes the flask application.
app = Flask(__name__)

# fetches the database uri from heroku.
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"  # don't defraud my app ok?


@app.route("/")
def puinyui():
    return render_template('index.html', foo="bar")


if __name__ == "__main__":
    app.run(
        #port=int(os.getenv("PORT", "8080")),
        #host=os.getenv("IP", "0.0.0.0"),
        debug=True
    )
