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
mkdir python-weather-app
cd python-weather-app
python3 -m venv .venv
```
Activate the virtual environment:

`. .venv/bin/activate`

Install Flask

`pip install Flask`

Create a new file in the project

`touch app.py`

I ensured any API keys would be stored safely by creating a .env file and installing 

`pip install python-dotenv`

This allowed me to safely fetch the API key from my .env file. 

When first connecting it to my react frontend, I came across an error regarding CORS. I discovered that CORS is a browser security feature, and without the CORS headers it would be impossible for the react frontend to make requests. 

## Reflections
I've really enjoyed using Python and Flask. It's very intuitive and the syntax is similar to Ruby. Having a foundation in Rails helped, as I was able to get to grips with the routing system quickly. As this was relatively simple to set up, I could really focus on things like the security of the app.

## Future Additions
