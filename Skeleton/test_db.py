#
# Testing file for Gameboard.py
#

import unittest
import db
from Gameboard import Gameboard

game = Gameboard()


class Test_TestGameboard(unittest.TestCase):
    # Minimum testing cases as outlined in assignments.txt are below

    def test_add_move(self):
        db.clear()
        db.init_db()
        move = ("p1", game.stringBoard(), "", "red", "yellow", 20)
        db.add_move(move)
        self.assertEquals(db.getMove()[0][5], 20)
        db.clear()

    def test_get_move(self):
        db.clear()
        db.init_db()
        move = ("p2", game.stringBoard(), "", "red", "yellow", 42)
        db.add_move(move)
        self.assertEquals(db.getMove()[0][0], "p2")
        db.clear()
