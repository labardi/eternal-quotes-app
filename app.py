from flask import *
from random import choice
import json
import os

app = Flask(__name__)

quotes_list = json.loads(open('quotes.json', encoding='utf-8').read())['quotes']

image_path = 'static/images/background'
bg_list = os.listdir(image_path)


@app.route("/")
def print_quote():
    random_quote = choice(quotes_list)
    random_bg_path = 'images/background/' + choice(bg_list)
    return render_template('index.html', quote=random_quote, bg_path=random_bg_path)
