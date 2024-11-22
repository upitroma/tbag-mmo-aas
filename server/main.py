from flask import Flask, jsonify, request

from characterCreation import characterCreation
from newCharacter import newCharacter

app = Flask(__name__)

# home page
@app.route('/', methods=['GET'])
def home():
    return "<h1>hello world!</h1><h3>go to /character-creation to get started!</h3>"

# character creation
@app.route('/character-creation', methods=['GET'])
def character_creation():
    return jsonify(characterCreation())

# new character
@app.route('/new-character', methods=['GET'])
def new_character():
    return jsonify(newCharacter(request.args.get('name')))


@app.route('/api', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({'received': data}), 201

if __name__ == '__main__':
    app.run(debug=True)
