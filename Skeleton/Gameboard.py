import db


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [["" for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
        self.current_row = len(self.board) - 1

    def setPlayer1Color(self, color):
        if color == "red":
            self.player1 = "red"
        elif color == "yellow":
            self.player1 = "yellow"

    def getPlayer1Color(self):
        return self.player1

    def setPlayer2Color(self, color):
        if color == "red":
            self.player2 = "red"
        elif color == "yellow":
            self.player2 = "yellow"

    def getPlayer2Color(self):
        return self.player2

    def getWinner(self):
        return self.game_result

    def setWinner(self, player):
        self.game_result = player
        db.clear()

    def getCurrentTurn(self):
        return self.current_turn

    def setCurrentTurn(self, player):
        self.current_turn = player

    def getRemainMoves(self):
        return self.remaining_moves

    def setRemainMoves(self, count):
        self.remaining_moves -= count

    def drawCondition(self):
        if self.remaining_moves < 0:
            return True
        return False

    def getBoard(self):
        return self.board

    def setBoard(self, newBoard):
        self.board = newBoard

    def convertToMatrix(self, newBoard, rows, columns):
        result = []
        start = 0
        end = columns
        for i in range(rows):
            result.append(newBoard[start:end])
            start += columns
            end += columns
        return result

    def convertToBoard(self, newBoard):
        board = [newBoard.split(' ')]
        board = self.convertToMatrix(board, 6, 7)
        print(board)
        self.board = board

    def initSavedBoard(self):
        # Database (current_turn, board, winner, player1, player2,
        # remaining_moves)
        saved_state = db.getMove()
        # print(saved_state)
        if(len(saved_state) != 0):
            self.setCurrentTurn(saved_state[0])
            self.convertToBoard(saved_state[1])
            self.setWinner(saved_state[2])
            self.setPlayer1Color(saved_state[3])
            self.setPlayer2Color(saved_state[4])
            self.setRemainMoves(saved_state[5])

    def stringBoard(self):
        board = self.getBoard()
        flat_board = [y for x in board for y in x]
        print(flat_board)
        string_board = ' '.join(map(str, flat_board))
        return string_board

    def setMove(self, col, player):
        openIndex = len(self.board) - 1
        for row in range(len(self.board)-1, -1, -1):
            if self.board[row][col] == "":
                openIndex = row
                break
        self.board[openIndex][col] = player
        self.current_row = openIndex
        sql_tuple = (self.getCurrentTurn(), self.stringBoard(),
                     self.getWinner(), self.getPlayer1Color(),
                     self.getPlayer2Color(), self.getRemainMoves())
        db.add_move(sql_tuple)

    def isValidMove(self, col, player):
        # checks if top most slot is filled, or there's a winner, or it's not
        # the curr player's turn
        if (self.board[0][col] != "" or self.getWinner() != "" or
           self.current_turn != player or self.remaining_moves < 0):
            return False
        return True

    def vertical4(self, col, player):
        count = 0
        for row in range(len(self.board)-1, -1, -1):
            if self.board[row][col] == player:
                count += 1
            else:
                count = 0
            if(count == 4):
                self.setWinner(player)

    def horizontal4(self, player):
        count = 0
        for col in range(len(self.board[0])-1, -1, -1):
            if self.board[self.current_row][col] == player:
                count += 1
            else:
                count = 0
            if(count == 4):
                self.setWinner(player)

    def diagonal4(self, move, player):
        # Win condition for positive slope
        count = 0
        row = self.current_row
        col = move
        while col != 0 and row != len(self.board)-1:
            col -= 1
            row += 1
        while row > 0 and col < len(self.board[0]):
            if self.board[row][col] == player:
                count += 1
            else:
                count = 0
            col += 1
            row -= 1
            if count >= 4:
                self.setWinner(player)

        # win condition for negative slope
        count = 0
        row = self.current_row
        col = move
        while col != 0 and row != 0:
            col -= 1
            row -= 1
        while row < len(self.board) and col < len(self.board[0]):
            if self.board[row][col] == player:
                count += 1
            else:
                count = 0
            col += 1
            row += 1
            if count >= 4:
                self.setWinner(player)
