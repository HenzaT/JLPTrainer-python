from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
import requests

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)

CORS(app)
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to the JLPTrainer backend." \
    "To find the kanji characters for each JLPT level, use the url /api/index?level=jlpt-NUMBER" \
    "To see a specific kanji, use the url /api/show?kanji=CHARACTER"

def level_cache_key():
    data = request.get_json(silent=True) or {}
    return f"level:{data.get('level', '').strip().lower()}"

@app.route('/api/index', methods=['GET', 'POST'])
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

    return jsonify(data)

def kanji_cache_key():
    data = request.get_json(silent=True) or {}
    return f"kanji:{data.get('kanji', '').strip().lower()}"

@app.route('/api/show', methods=['GET', 'POST'])
@cache.cached(timeout=50, key_prefix=kanji_cache_key)
def show():
    if request.method == 'GET':
        kanji = request.args.get('kanji')
    elif request.method == 'POST':
        data = request.get_json()
        kanji = data.get('kanji') if data else None

    kanji_url = f'https://kanjiapi.dev/v1/kanji/{kanji}'
    try:
        response = requests.get(kanji_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
         return jsonify({'error': str(e)}), 500

    return jsonify({
        kanji: data
    })
