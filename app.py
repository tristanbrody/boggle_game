from flask import Flask, request, redirect, session, render_template, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

from boggle import Boggle

boggle_game = Boggle()

@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    Get requests to home page will create a new game board and set session variables. 
    Post requests will call a helper function to validate input and return JSON output. 
    """
    if request.method == 'GET':
        reset_session()
        return render_template('home.html')
    elif request.method == 'POST':
        if request.json.get('score', None) is not None:
            update_game_results()
            return jsonify({"high_score": session['high_score']})
        else:
            word_result = handle_input(request.json["word"])
            already_on_board = True if word_result == "already guessed" else False
            return jsonify({"message": f"Your word was {word_result}", "duplicate": already_on_board}, 200)

@app.route('/reset', methods=['POST'])
def restart_game():
    return redirect(url_for('home_page'))

def update_game_results():
    high_score = session.get('high_score', 0)
    print(request.method)
    print(request.json)
    session['high_score'] = request.json['score'] if request.json['score'] > high_score else high_score 

def handle_input(word):
    """Validate word entered on form, and update list of guesses in session accordingly"""
    word_result = boggle_game.check_valid_word(session['board'], word)

    if word_result == 'ok':
        update_score(word)

    word_list = session['guesses']

    if word not in word_list:
        word_list.append(word)
        session['guesses'] = word_list
    else:
        word_result = "already guessed"
    return word_result

def reset_session():
    session['board'] = boggle_game.make_board()
    session['guesses'] = []
    session['total_points'] = 0

def update_score(word):
    print('should be updating session')
    session['total_points'] = session['total_points'] + len(word) 
    print(session['total_points'])