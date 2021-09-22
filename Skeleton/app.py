import json
from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''

# app routing maps the specified URL with the below function
@app.route('/', methods=['GET'])
def player1_connect():
    return render_template("player1_connect.html", status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    color = request.args.get('color')
    game.setPlayer1Color(color)
    return render_template("player1_connect.html", status=color)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    player1Color = game.getPlayer1Color()
    if player1Color == "":
        return render_template("p2Join.html", status="Error, pick player 1 color")
    elif player1Color == "red":
        game.setPlayer2Color("yellow")
    elif player1Color == "yellow":
        game.setPlayer2Color("red")
    return render_template("p2Join.html", status = game.getPlayer2Color())
       

'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    move = request.get_json()["column"].split("col")[1]
    move = int(move) - 1
    # Draw condition
    if game.getRemainMoves() < 0:
        return jsonify(move=game.getBoard(),invalid=True,reason="Draw!",winner=game.getWinner())
    # Checks for valid move and if there's a win condition
    if game.isValidMove(move) and game.getCurrentTurn() == "p1":
        game.setMove(move,game.getPlayer1Color())
        # Win conditions
        game.vertical4(move,game.getPlayer1Color())
        game.horizontal4(game.getPlayer1Color())
        game.diagonal4(move,game.getPlayer1Color())
        game.setRemainMoves(-1)
        game.setCurrentTurn("p2") 
        return jsonify(move=game.getBoard(),invalid=False,winner=game.getWinner())
    # If invalid move, return either wrong turn or current column is full
    else:
        if game.getCurrentTurn() != "p1": 
            return jsonify(move=game.getBoard(),invalid=True,reason="Not your turn",winner=game.getWinner())
        else:
            return jsonify(move=game.getBoard(),invalid=True,reason="Invalid Move",winner=game.getWinner())


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    move = request.get_json()["column"].split("col")[1]
    move = int(move) - 1
    if game.getRemainMoves() < 0:
        return jsonify(move=game.getBoard(),invalid=True,reason="Draw!",winner=game.getWinner())
    if game.isValidMove(move) and game.getCurrentTurn() == "p2":
        game.setMove(move,game.getPlayer2Color())
        game.vertical4(move,game.getPlayer2Color())
        game.horizontal4(game.getPlayer2Color())
        game.diagonal4(move,game.getPlayer2Color())
        game.setRemainMoves(-1)
        game.setCurrentTurn("p1") 
        return jsonify(move=game.getBoard(),invalid=False,winner=game.getWinner())
    else:
        if game.getCurrentTurn() != "p2":
            return jsonify(move=game.getBoard(),invalid=True,reason="Not your turn",winner=game.getWinner())
        else:
            return jsonify(move=game.getBoard(),invalid=True,reason="Invalid Move",winner=game.getWinner())



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
