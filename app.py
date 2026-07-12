from flask import *
from random import choice
import json
import os
from datetime import timedelta
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))


load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_key_for_dev')

json_path = os.path.join(basedir, 'quotes.json')
quotes_list = json.loads(open(json_path, encoding='utf-8').read())['quotes']

app.permanent_session_lifetime = timedelta(days=30)

cloud_name = "hligceqf"

images = ['monet1', 'monet2', 'monet3', 'monet4', 'monet5', 'monet6', 'monet7', 'monet8', 'monet9', 'monet10', 'monet11', 'monet12', 'monet13']

# Создаем необходимые функции

def cloudinary_url(image, width):
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/w_{width},f_avif,q_auto:good/{image}"

def get_next_quote(quotes_list):
    if 'history' not in session:
        session['history'] = []

    max_history_length = int(len(quotes_list) * 0.5)

    while len(session['history']) >= max_history_length:
        session['history'].pop(0)

    next_quote = choice(quotes_list)
    quote_id = next_quote['id']

    while quote_id in session['history']:
        next_quote = choice(quotes_list)
        quote_id = next_quote['id']

    session['history'].append(quote_id)
    session.modified = True

    return next_quote

def get_next_background(images_list, quote_id):
    max_background_length = int(len(images_list) * 0.5)
    time_to_swap = False

    if 'background' not in session:
        session['background'] = []

    if 'current_image' not in session:
        session['current_image'] = choice(images_list)

    if 'next_image' not in session:
        session['next_image'] = session['current_image']

    if 'counter_list' not in session:
        session['counter_list'] = []

    session['counter_list'].append(quote_id)


    while len(session['background']) > max_background_length:
        session['background'].pop(0)

    if len(session['counter_list']) % 5 == 0:
        session['counter_list'] = []
        session['current_image'] = session['next_image']
        time_to_swap = True

    if len(session['counter_list']) % 5 == 4:
        while session['next_image'] in session['background']:
            session['next_image'] = choice(images_list)


    if session['background']:
        if session['background'][-1] != session['next_image']:
            session['background'].append(session['next_image'])
    else:
        session['background'].append(session['next_image'])

    current_bg_urls = {
        "768": cloudinary_url(session['current_image'], 768),
        "1280": cloudinary_url(session['current_image'], 1280),
        "1920": cloudinary_url(session['current_image'], 1920),
        "2560": cloudinary_url(session['current_image'], 2560)
    }

    next_bg_urls = {
        "768": cloudinary_url(session['next_image'], 768),
        "1280": cloudinary_url(session['next_image'], 1280),
        "1920": cloudinary_url(session['next_image'], 1920),
        "2560": cloudinary_url(session['next_image'], 2560)
    }

    session.modified = True

    return current_bg_urls, next_bg_urls, session['current_image'], session['next_image'], time_to_swap

# Код роутов

@app.route("/")
def build_page():
    session.permanent = True

    next_quote = get_next_quote(quotes_list)
    quote_id = next_quote['id']

    current_bg_urls, next_bg_urls, current_image, next_image, time_to_swap = get_next_background(images, quote_id)

    return render_template('index.html', quote=next_quote, current_bg_urls=current_bg_urls, next_bg_urls=next_bg_urls)

@app.route("/api/next_quote")
def send_data():
    next_quote = get_next_quote(quotes_list)
    quote_id = next_quote['id']

    current_bg_urls, next_bg_urls, current_image, next_image, time_to_swap = get_next_background(images, quote_id)

    str_next_urls = f"{next_bg_urls['768']} 768w, {next_bg_urls['1280']} 1280w, {next_bg_urls['1920']} 1920w, {next_bg_urls["2560"]} 2560w"

    return jsonify(quote=next_quote, current_image=current_image, next_image=next_image, str_next_urls=str_next_urls, time_to_swap=time_to_swap)