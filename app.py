from flask import *
from random import choice
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, 'quotes.json')
quotes_list = json.loads(open(json_path, encoding='utf-8').read())['quotes']

image_path = os.path.join(BASE_DIR, 'static', 'images', 'background')
bg_list = os.listdir(image_path)


@app.route("/")
def print_quote():
    random_quote = choice(quotes_list)
    random_bg_path = 'images/background/' + choice(bg_list)
    return render_template('index.html', quote=random_quote, bg_path=random_bg_path)
