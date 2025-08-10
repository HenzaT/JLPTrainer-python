from flask import Flask, render_template, request, session, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_caching import Cache
# password hashing
from flask_bcrypt import Bcrypt
# migrations
from flask_migrate import Migrate
# session management
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required
)
import requests
import os
load_dotenv()

# create instance of LoginManager so we can use elsewhere
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

bcrypt = Bcrypt(app)

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config.from_mapping(config)
cache = Cache(app)

# Root, welcome
@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

# Index
def level_cache_key():
    level = request.args.get('level', '').strip().lower()
    return f"level:{level}"

@app.route('/api/index', methods=['GET'])
@cache.cached(timeout=50, key_prefix=level_cache_key)
def index():
    if request.method == 'GET':
        level = request.args.get('level')
    elif request.method == 'POST':
        data = request.get_json()
        level = data.get('level') if data else None

    jlpt_url = f'https://kanjiapi.dev/v1/kanji/{level}'
    try:
        response = requests.get(jlpt_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
         return jsonify({'error': str(e)}), 500

    return jsonify({
        level: data
    })

# all-kanji
# def all_kanji_cache_key():
#     data = request.get_json(silent=True) or {}
#     return f"level:{data.get('level', '').strip().lower()}"

@app.route('/api/all-kanji', methods=['GET'])
# @cache.cached(timeout=50, key_prefix=all_kanji_cache_key)
def all_kanji():
    # if request.method == 'POST':
    #     data = request.get_json()
    #     kanji_number = data.get('number') if data else None

    all_kanji = []
    for number in range(1, 6):
        jlpt_url = f'https://kanjiapi.dev/v1/kanji/jlpt-{str(number)}'
        try:
            response = requests.get(jlpt_url)
            response.raise_for_status()
            data = response.json()
            jlpt_dictionary = {
                f'jlpt-{number}': data
            }
            all_kanji.append(jlpt_dictionary)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    return jsonify(all_kanji)

# Show
def kanji_cache_key():
    kanji = request.args.get('kanji', '').strip().lower()
    return f"kanji:{kanji}"

@app.route('/api/show', methods=['GET'])
@cache.cached(timeout=50, key_prefix=kanji_cache_key)
def show():
    if request.method == 'GET':
        kanji = request.args.get('kanji')

    kanji_url = f'https://kanjiapi.dev/v1/kanji/{kanji}'
    try:
        response = requests.get(kanji_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
         return jsonify({'error': str(e)}), 500

    return jsonify(data)

@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
