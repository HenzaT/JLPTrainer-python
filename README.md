## Python JLPT (Japanese language) app
This is a self-directed project and is my second app built using Flask. 

## Goals
For this project, I wanted to consolidate my learning of Python and Flask, and again connect it to a React frontend. Although I started the React frontend a while ago, I am a lot more confident in using Flask and React and so wanted to separate the concerns better by creating separate apps.

## Tech Stack
- Flask (Python)
- kanjiapi.dev (free, no key required)
- Postman (to test requests)

## Process
I first set up my Flask project following the documentation: 
```
mkdir JLPTrainer-python
cd JLPTrainer-python
python3 -m venv .venv
```
Activate the virtual environment:
```
. .venv/bin/activate
```
Install Flask
```
pip install Flask
```
Create a new file in the project
```
touch app.py
```

I installed everything I would need to make requests to an API:
```
pip install flask_cors
pip install requests
pip install flask_caching
```

This time, I used more conventional route names like 'index' and 'show'. In the root route, I wrote a clearer message for the user and instructions on how to access the index and show urls.

```
@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to the JLPTrainer backend." \
    "To find the kanji characters for each JLPT level, use the url /api/index?level=jlpt-NUMBER" \
    "To see a specific kanji, use the url /api/show?kanji=CHARACTER"
```

Before making calls to the API and writing the code for my routes, I had a think about what format I wanted my data to return in. The kanjiapi returns all characters for a specific JLPT level as a list (array), and information on specific kanji as a dictionary (hash). Although I played around with returning all kanji as a indexed dictionary, I ultimately decided to keep everything as it is - for example, being able to quickly iterate over the list would be much more useful on the client side. As I build up the React frontend, I may return to the flask backend and change how the data structures depending on how I use them on the client side. 

```
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
```

Having learnt about the importance of error handling and especially about giving clear feedback to the user when an error does occur in my last Flask app, I implemented this once again.

## Reflections
As an API, the kanjiapi is quite barebones and so I found myself thinking hard about the data structrues and ways to clearly signpost the returned data.

## Future Additions
