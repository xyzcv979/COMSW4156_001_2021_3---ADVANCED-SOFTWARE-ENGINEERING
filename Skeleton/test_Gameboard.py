#
# Testing file for Gameboard.py
#

import unittest
from Gameboard import Gameboard

game = Gameboard()
player = "p1"
playerColor = "red"


class Test_TestGameboard(unittest.TestCase):
    # Minimum testing cases as outlined in assignments.txt are below

    def test_valid_move(self):
        # Checks if the move is valid
        openMove = 1
        # Resetting gameboard to default settings
        game.current_turn = player
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""]]
        game.game_result = ""
        game.remaining_moves = 42
        validMove = game.isValidMove(openMove, player)
        self.assertEqual(validMove, True)

    def test_set_move(self):
        # Tests if gameboard successfully sets in a move
        openMove = 1
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""]]
        game.setMove(openMove, playerColor)
        list = [["", "", "", "", "", "", ""],
                ["", "", "", "", "", "", ""],
                ["", "", "", "", "", "", ""],
                ["", "", "", "", "", "", ""],
                ["", "", "", "", "", "", ""],
                ["", "red", "", "", "", "", ""]]
        self.assertListEqual(game.getBoard(), list)

    def test_invalid_turn(self):
        # Checks Invalid move - not player's turn
        # Current turn is player 1's
        game.setCurrentTurn(player)
        checkTurn = game.isValidMove(1, "p2")
        self.assertEqual(checkTurn, False)

    def test_winner_declared(self):
        # Checks Invalid move - winner already declared
        # Sets the winner to player1 and asserts if a move is valid
        game.setCurrentTurn(player)
        game.setWinner(player)
        checkTurn = game.isValidMove(1, player)
        self.assertEqual(checkTurn, False)

    def test_draw(self):
        # Checks Invalid move - draw (tie)
        # If there's a draw, IsValidMove function returns false
        game.setCurrentTurn(player)
        game.remaining_moves = -1
        if game.drawCondition() is True:
            self.assertEqual(game.isValidMove(1, player), False)

    def test_column_filled(self):
        # Checks Invalid move - current column is filled\
        # Sets board to a populated list with column 1 filled
        # Asserts to see if valid move is possible on column 1
        game.setCurrentTurn(player)
        game.board = [["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""]]
        checkTurn = game.isValidMove(1, player)
        self.assertEqual(checkTurn, False)

    def test_vertical4(self):
        # Checks Winning move - vertical direction
        game.setCurrentTurn(player)
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["", "red", "", "", "", "", ""]]
        game.vertical4(1, playerColor)
        winner = game.getWinner()
        self.assertEqual(winner, playerColor)

    def test_horizontal4(self):
        # Checks Winning move - horizontal direction
        game.setCurrentTurn(player)
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["red", "red", "red", "red", "", "", ""]]
        game.current_row = 5
        game.horizontal4(playerColor)
        winner = game.getWinner()
        self.assertEqual(winner, playerColor)

    def test_diagonal4_positive(self):
        # Checks Winning move - negative slope diagonal direction
        game.setCurrentTurn(player)
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "red", "", "", ""],
                      ["", "", "", "", "red", "", ""],
                      ["", "", "", "", "", "red", ""],
                      ["", "", "", "", "", "", "red"]]
        game.current_row = 2
        game.diagonal4(3, playerColor)
        winner = game.getWinner()
        self.assertEqual(winner, playerColor)

    def test_diagonal4_negative(self):
        # Checks Winning move - positive slope diagonal direction
        game.setCurrentTurn(player)
        game.board = [["", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", ""],
                      ["", "", "", "red", "", "", ""],
                      ["", "", "red", "", "", "", ""],
                      ["", "red", "", "", "", "", ""],
                      ["red", "", "", "", "", "", ""]]
        game.current_row = 2
        game.diagonal4(3, playerColor)
        winner = game.getWinner()
        self.assertEqual(winner, playerColor)

    # Additional testing cases in order to get near 100% coverage
    def test_player1_color(self):
        # Checks player1 color
        game.setPlayer1Color("red")
        self.assertEqual(game.getPlayer1Color(), "red")
        game.setPlayer1Color("yellow")
        self.assertEqual(game.getPlayer1Color(), "yellow")

    def test_player2_color(self):
        # Checks player2 color
        game.setPlayer2Color("yellow")
        self.assertEqual(game.getPlayer2Color(), "yellow")
        game.setPlayer2Color("red")
        self.assertEqual(game.getPlayer2Color(), "red")

    def test_get_current_turn(self):
        # Checks current turn
        game.setCurrentTurn("p1")
        self.assertEqual(game.getCurrentTurn(), "p1")

    def test_get_remain_moves(self):
        # checks remaining moves before draw
        game.remaining_moves = 42
        game.setRemainMoves(1)
        self.assertEqual(game.getRemainMoves(), 41)

    def test_draw_condition(self):
        game.remaining_moves = 42
        self.assertEqual(game.drawCondition(), False)
