from flask import *
from random import choice
import json
import os
from datetime import timedelta
from dotenv import load_dotenv # Добавляем импорт

# 1. Вычисляем абсолютный путь к папке, в которой лежит этот самый файл app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# 2. Жестко приказываем искать .env именно в этой папке
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_key_for_dev')

json_path = os.path.join(basedir, 'quotes.json')
quotes_list = json.loads(open(json_path, encoding='utf-8').read())['quotes']

app.permanent_session_lifetime = timedelta(days=30)

cloud_name = "hligceqf"

images = ['monet1', 'monet2', 'monet3', 'monet4', 'monet5', 'monet6', 'monet7', 'monet8', 'monet9', 'monet10', 'monet11', 'monet12', 'monet13']

@app.route("/")
def print_quote():
    session.permanent = True

    # 1. Инициализация
    if 'history' not in session:
        session['history'] = []

    # 2. Высчитываем лимит один раз и используем безопасное сравнение
    max_history_length = int(len(quotes_list) * 0.5)
    max_background_length = int(len(images) * 0.5)

    # Если базу урезали, и история стала больше базы, обрезаем ее с запасом
    while len(session['history']) >= max_history_length:
        session['history'].pop(0)

    # 3. Рулетка с проверкой коллизий
    random_quote = choice(quotes_list)
    quote_id = random_quote['id']

    while quote_id in session['history']:
        random_quote = choice(quotes_list)
        quote_id = random_quote['id']

    # 4. Сохранение результата
    session['history'].append(quote_id)

    if 'background' not in session:
        session['background'] = []
    if not session['background']:  # пустой список
        current_image = choice(images)
    else:
        current_image = session['background'][-1]

    if 'counter_list' not in session:
        session['counter_list'] = []

    session['counter_list'].append(quote_id)

    while len(session['background']) > max_background_length:
        session['background'].pop(0)

    if len(session['counter_list']) % 5 == 0:
        session['counter_list'] = []
        while current_image in session['background']:
            current_image = choice(images)

    if session['background']:
        if session['background'][-1] != current_image:
            session['background'].append(current_image)
    else:
        session['background'].append(current_image)

    def cloudinary_url(image, width):
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/w_{width},f_avif,q_auto:good/{image}"

    bg_urls = {
        "768": cloudinary_url(current_image, 768),
        "1280": cloudinary_url(current_image, 1280),
        "1920": cloudinary_url(current_image, 1920),
        "2560": cloudinary_url(current_image, 2560)
    }

    session.modified = True
    return render_template('index.html', quote=random_quote, bg_urls=bg_urls)
