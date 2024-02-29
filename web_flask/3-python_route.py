#!/usr/bin/python3
"""
This module starts a Flask web application with four routes.
"""

from flask import Flask
from flask import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" on the root route.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display "HBNB" on the /hbnb route.
    """
    return "HBNB"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """
    Display "Python " followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    Default text is "is cool".
    """
    return "Python {}".format(escape(text.replace("_", " ")))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
