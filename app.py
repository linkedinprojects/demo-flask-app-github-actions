from flask import Flask
from flask import render_template
import socket
import random
import os
import argparse

app = Flask(__name__)

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#2980b9",
    "blue2": "#30336b",
    "pink": "#be2edd",
    "darkblue": "#130f40"
}

# Directly setting the background color to green
COLOR = "green"  
# Uncomment the following line to use random color generation
# COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink"])

@app.route("/")
def main():
    return render_template('hello.html', name=socket.gethostname(), color=color_codes[COLOR])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
