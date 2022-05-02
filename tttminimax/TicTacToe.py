import sys
from copy import copy
class TicTacToe:

    inRow = 3
    player = 'O'
    enemy = 'X'
    def __init__(self, rc: tuple) -> None:
        self.currPlayer = self.player
        self.rc = rc
        self.state = []
        for i in range(self.rc[0]):
            c = '-' * self.rc[1]
            self.state.append(c)

    def print_state(self, board) -> None:
        print('  ' + ''.join([str(i) for i in range(self.rc[1])]))
        for i in range(len(board)):
            print(str(i) + ' ' + board[i])
        print()

    def make_move(self, ul: tuple, turn: str, board) -> None:
        newStr = board[ul[0]][:ul[1]] + turn + board[ul[0]][ul[1]+1:]
        board[ul[0]] = newStr

    def check_full(self,board) -> bool:
        c = 0
        for i in board:
            if '-' in i:
                c+=1
        if c == 0: return True
        return False

    def check_valid(self, urc: list) -> bool:
        if len(urc) < 2: return False
        if urc[0].isdigit() and urc[1].isdigit():
            r, c = int(urc[0]), int(urc[1])
            if self.state[r][c] != '-': return False
            if 0 <= r < self.rc[0] and 0 <= c < self.rc[1]: return True
        return False

    def legal_moves(self, board):
        l = []
        for i in range(self.rc[0]):
            for j in range(self.rc[1]):
                if board[i][j] == '-':
                    l.append((i,j))
        return l

    def check_win(self, board):
        # row by row
        for r in board:
            x,o = 0,0
            for c in range(self.rc[1]):
                if r[c] == 'X':
                    x+=1
                    o=0
                elif r[c] == 'O':
                    x=0
                    o+=1
                else: x,o = 0,0
                if x == self.inRow: return 1
                if o == self.inRow: return -1

        # col by col
        for c in range(self.rc[1]):
            x,o = 0,0
            for r in range(self.rc[0]):
                if board[r][c] == 'X':
                    x+=1
                    o=0
                elif board[r][c] == 'O':
                    x=0
                    o+=1
                else: x,o = 0,0
                if x == self.inRow: return 1
                if o == self.inRow: return -1

        for r in range(self.rc[0]+1-self.inRow):
            for c in range(self.rc[1]+1-self.inRow):
                x,o = 0,0
                for i in range(self.inRow):
                    if board[r+i][c+i] == 'X':
                        x+=1
                        o=0
                    elif board[r+i][c+i] == 'O':
                        x=0
                        o+=1
                    else: x,o = 0,0
                    if x == self.inRow: return 1
                    if o == self.inRow: return -1

        for r in range(self.rc[0]+1-self.inRow):
            for c in range(self.inRow-1,self.rc[1]):
                x,o = 0,0
                for i in range(self.inRow):
                    if board[r+i][c-i] == 'X':
                        x+=1
                        o=0
                    elif board[r+i][c-i] == 'O':
                        x=0
                        o+=1
                    else: x,o = 0,0
                    if x == self.inRow: return 1
                    if o == self.inRow: return -1

        if self.check_full(board): return 0

        return None

    def enemy_turn(self):
        bestScore = -9999
        bestMove = ()
        legal = self.legal_moves(self.state)
        for i in legal:
            new = copy(self.state)
            self.make_move(i, self.enemy, new)
            score = self.minimax(0, False, new, -9999, 9999)
            if (score > bestScore):
                bestScore = score
                bestMove = (i[0],i[1])
        self.make_move(bestMove, self.enemy, self.state)

    def minimax(self, depth, is_max, orig, a, b):
        result = self.check_win(orig)
        if result is not None:
            return result
        if is_max:
            bestScore = -9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.make_move(i, self.enemy, new)
                bestScore = max(self.minimax(depth + 1, False, new, a, b), bestScore)
                if bestScore >= b: break
                a = max(a, bestScore)
            return bestScore
        else:
            bestScore = 9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.make_move(i, self.player, new)
                bestScore = min(self.minimax(depth + 1, True, new, a, b), bestScore)
                if bestScore <= a: break
                b = min(b, bestScore)
            return bestScore

    '''
    def minimax(self, depth, is_max, orig):
        result = self.check_win(orig)
        if result is not None:
            return result
        if is_max:
            bestScore = -9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.make_move(i, self.enemy, new)
                score = self.minimax(depth + 1, False, new)
                bestScore = max(score,bestScore)
            return bestScore
        else:
            bestScore = 9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.make_move(i, self.player, new)
                score = self.minimax(depth + 1, True, new)
                bestScore = min(score,bestScore)
            return bestScore
    '''

    def play(self):
        self.print_state(self.state)
        while not self.check_full(self.state):
            self.enemy_turn()
            if self.check_win(self.state) != None: self.print_state(self.state);exit()
            self.print_state(self.state)

            userIn = input('Player %s enter row and col (eg. 1 0): ' % self.player)
            sdrc = userIn[:3].split(' ')
            while not self.check_valid(sdrc):
                print('Invalid move')
                userIn = input('Player %s Enter row and col (eg. 1 0): ' % self.player)
                sdrc = userIn[:3].split(' ')

            self.make_move((int(sdrc[0]),int(sdrc[1])), self.player, self.state)
            if self.check_win(self.state) != None: self.print_state(self.state);exit()

            self.print_state(self.state)

def main():
    ttt = TicTacToe((4,3))
    ttt.play()

main()

