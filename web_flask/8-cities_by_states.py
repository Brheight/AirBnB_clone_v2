#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Remove the current SQLAlchemy Session after each request
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Display a HTML page with a list of all State objects and their cities
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
