import random

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compute")
def compute():

    x = random.randint(0, 10)
    y = random.randint(0, 10)
    z = x * y

    return render_template("compute.html", x=x, y=y, z=z)

if __name__ == '__main__':
    app.run(debug=True)