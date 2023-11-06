from app import app
from flask import render_template, request, flash, redirect
from base64 import b64encode
import requests


@app.get("/ssrf")
def ssrf_get():
    return render_template("vulnerable_templates/ssrf.html")


@app.post("/ssrf")
def ssrf_post():
    url = request.form.get("url")
    if url:
        http_response = requests.get(url)
        content = http_response.content
        encoded = b64encode(content).decode()

    context = {"content": encoded}
    return render_template("vulnerable_templates/ssrf.html", **context)
