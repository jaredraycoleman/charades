import json
import os
from random import choice

import requests
from dotenv import load_dotenv
from flask import (Flask, make_response, redirect, render_template, request,
                   url_for)
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "set_topic",
            "description": "Set the name of the playlist",
            "parameters": {
                "type": "object",
                "properties": {
                    "english": {
                        "type": "string",
                        "description": "topic in English",
                    },
                    "portuguese": {
                        "type": "string",
                        "description": "topic in Portuguese",
                    },
                },
                "required": ["english", "portuguese"]
            }
        }
    }
]

DIFFICULTY = "difficult (but not toooo difficult)"

def get_random_topic(prev_topics):
    seed_words = requests.get('https://random-word-api.herokuapp.com/word?number=10')
    
    res = client.chat.completions.create(
        messages=[
            {
                "role": "user", 
                "content": "".join([
                    f"Come up with a {DIFFICULTY} charades topic in English and Portuguese. ",
                    "The topic should be a noun or verb and it should be a single word. ",
                    "You can use the following words to help you come up with a topic, ",
                    "but it doesn't have to be any of these words:"
                    ", ".join(seed_words.json()),
                    ". Don't use any of the following words (which have already been used): ",
                    prev_topics
                ])
            }
        ],
        model="gpt-3.5-turbo",
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "set_topic"}}
    )

    args = json.loads(res.choices[0].message.tool_calls[0].function.arguments)
    return args['english'], args['portuguese']

@app.route('/')
def index():
    prev_topics = request.cookies.get('prev_topics', '')
    print(prev_topics)
    topic_en, topic_pt = get_random_topic(prev_topics)
    team1_score = request.cookies.get('team1', 0)
    team2_score = request.cookies.get('team2', 0)
    prev_topics += f"{topic_en} ({topic_pt}), "
    resp = make_response(render_template('index.html', topic_en=topic_en, topic_pt=topic_pt, team1_score=team1_score, team2_score=team2_score))
    resp.set_cookie('prev_topics', prev_topics)
    return resp

@app.route('/update-score/<team>')
def update_score(team):
    if team not in ['team1', 'team2']:
        return redirect(url_for('index'))
    score = request.cookies.get(team, 0)
    new_score = int(score) + 1
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(team, str(new_score))
    return resp

@app.route('/reset-score')
def reset_score():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('team1', '0')
    resp.set_cookie('team2', '0')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
