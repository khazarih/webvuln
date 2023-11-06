from flask import Flask

app = Flask(__name__)

app.jinja_env.auto_reload = True
app.config["TESTING"] = True
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "abc"
app.config["TEMPLATES_AUTO_RELOAD"] = True

from app import views
