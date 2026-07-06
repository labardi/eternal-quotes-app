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

image_path = os.path.join(basedir, 'static', 'images', 'background')
bg_list = os.listdir(image_path)

app.permanent_session_lifetime = timedelta(days=30)

@app.route("/")
def print_quote():
    # 1. Инициализация
    if 'history' not in session:
        session['history'] = []
        session.permanent = True

    # 2. Высчитываем лимит один раз и используем безопасное сравнение
    max_history_length = int(len(quotes_list) * 0.5)

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
    session.modified = True

    random_bg_path = 'images/background/' + choice(bg_list)
    return render_template('index.html', quote=random_quote, bg_path=random_bg_path)
