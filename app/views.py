from app import app
from flask import render_template, request
from jinja2 import TemplateNotFound


@app.route("/")
def index():
    return render_template("index.html")


from app.vulnerable_views import race_condition, missing_csrf
