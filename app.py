import random
import re
import string
import dotenv
import os

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

URL = "https://api.api-ninjas.com/v1/quotes"
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
CORS(app)

def get_random_quote():
    response = requests.get(URL, headers={'X-Api-Key': API_KEY})
    data = response.json()
    return data[0]


def alphabet_dict():
    letters = string.ascii_letters
    numbers = list(range(1, len(letters) + 1))
    random.shuffle(numbers)
    dicti = dict(zip(letters, numbers))
    print(dicti)
    return dicti


@app.route('/start', methods=['GET'])
def start_game():
    data = get_random_quote()
    quote = data["quote"].lower()
    answered_quote = re.sub('[a-z]', "_", quote)
    letter_to_number = alphabet_dict()
    numerical_hints = [letter_to_number.get(char, ' ') for char in quote]

    return jsonify({
        "quote": quote,
        "answered_quote": answered_quote,
        "numerical_hints": numerical_hints,
        "author": data["author"],
        "category": data["category"]
    })


@app.route('/guess', methods=['POST'])
def guess_letter():
    data = request.json
    quote = data['quote']
    answered_quote = data['answered_quote']
    numerical_hints = data['numerical_hints']
    guess_index = int(data['guess_index'])
    guess_letter = data['guess_letter'].lower()

    if answered_quote[guess_index] == '_':
        if quote[guess_index] == guess_letter:
            answered_quote = answered_quote[:guess_index] + guess_letter + answered_quote[guess_index + 1:]
            correct = True
        else:
            correct = False
    else:
        correct = False

    return jsonify({
        "quote": quote,
        "answered_quote": answered_quote,
        "numerical_hints": numerical_hints,
        "author": data["author"],
        "category": data["category"],
        "correct": correct
    })


if __name__ == '__main__':
    app.run(debug=True)
