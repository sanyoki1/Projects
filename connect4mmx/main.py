from copy import copy
class Connect:

    p1 = 'R'
    p2 = 'Y'
    ROW = 4
    COL = 5
    CON = 3

    def __init__(self) -> None:
        self.board = []
        for i in range(self.ROW):
            l = ''
            for j in range(self.COL):
               l += '-'
            self.board.append(l)

    def show_board(self) -> None:
        for i in range(self.COL): print(i, end=' ')
        print()
        for i in range(self.ROW):
            for j in range(self.COL):
                print(self.board[i][j], end=' ')
            print()
        print()

    def print_state(self,state) -> None:
        for i in range(self.COL): print(i, end=' ')
        print()
        for i in range(self.ROW):
            for j in range(self.COL):
                print(state[i][j], end=' ')
            print()
        print()

    def check_win(self, state):
        # check verticals
        for col in range(self.COL):
            prev = ''
            count = 0
            for row in reversed(range(self.ROW)):
                max = 0
                curr = state[row][col]
                if curr == '-':
                    break
                if curr == prev:
                    count += 1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        # check horizontal
        for row in range(self.ROW):
            prev = ''
            count = 0
            for col in reversed(range(self.COL)):
                max = 0
                curr = state[row][col]
                if curr == '-':
                    count = 0
                    prev = ''
                if curr == prev:
                    count += 1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        # left col
        for row in range(self.ROW):
            prev = ''
            count = 0
            offset = 0
            max = 0
            while (row+offset < self.ROW and offset < self.COL):
                curr = state[row+offset][offset]
                if curr == '-':
                    count = 0
                    prev = ''
                if curr == prev:
                    count+=1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                offset += 1
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        # top row
        for col in range(self.COL):
            prev = ''
            count = 0
            offset = 0
            max = 0
            while (offset < self.ROW and col+offset < self.COL):
                curr = state[offset][col+offset]
                if curr == '-':
                    count = 0
                    prev = ''
                if curr == prev:
                    count+=1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                offset += 1
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        # left col
        for row in reversed(range(self.ROW)):
            prev = ''
            count = 0
            offset = 0
            max = 0
            while (row-offset >= 0 and offset < self.COL):
                curr = state[row-offset][offset]
                if curr == '-':
                    count = 0
                    prev = ''
                if curr == prev:
                    count+=1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                offset += 1
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        # bot row
        for col in range(self.COL):
            prev = ''
            count = 0
            offset = 0
            max = 0
            while (self.ROW-offset-1 >= 0 and col+offset < self.COL):
                curr = state[self.ROW-offset-1][col+offset]
                if curr == '-':
                    count = 0
                    prev = ''
                if curr == prev:
                    count+=1
                else:
                    prev = curr
                    count = 1
                if max < count:
                    max = count
                offset += 1
                if max == self.CON:
                    if prev == self.p1:
                        return 1
                    else: return -1

        if self.check_full(state): return 0

        return None

    def legal_moves(self, state):
        l = []
        for i in range(self.COL):
            if state[0][i] == '-':
                l.append(i)
        return l

    def place_move(self, col, turn, state) -> bool:
        for i in reversed(range(self.ROW)):
            if state[i][col] == '-':
                state[i] = state[i][:col] + turn + state[i][col+1:]
                return True
        return False

    def check_full(self, state):
        for i in state:
            if i.count('-') > 0: return False
        return True

    def enemy_turn(self):
        bestScore = -9999
        bestMove = ()
        legal = self.legal_moves(self.board)
        for i in legal:
            new = copy(self.board)
            self.place_move(i, self.p1, new)
            score = self.minimax(0, False, new, -9999, 9999)
            if (score > bestScore):
                bestScore = score
                bestMove = i
        self.place_move(bestMove, self.p1, self.board)

    # TODO: score_position of board

    def minimax(self, depth, is_max, orig, a, b):
        result = self.check_win(orig)
        if result is not None:
            return result
        if is_max:
            bestScore = -9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.place_move(i, self.p1, new)
                bestScore = max(self.minimax(depth + 1, False, new, a, b), bestScore)
                if bestScore >= b: break
                a = max(a, bestScore)
            return bestScore
        else:
            bestScore = 9999
            for i in self.legal_moves(orig):
                new = copy(orig)
                self.place_move(i, self.p2, new)
                bestScore = min(self.minimax(depth + 1, True, new, a, b), bestScore)
                if bestScore <= a: break
                b = min(b, bestScore)
            return bestScore

    def play_game(self):
        curr = self.p1
        running = True
        while running:
            if curr == self.p2:
                # get input and repeat until valid
                move = int(input("Player %s - Enter col (0-%x): " % (curr, self.COL-1)))
                valid = self.place_move(move, curr, self.board)
                while not valid:
                    print("Invalid move")
                    move = int(input("Player %s - Enter col (0-%x): " % (curr, self.COL-1)))
                    valid = self.place_move(move, curr, self.board)
            else:
                self.enemy_turn()

            self.show_board()

            # check if someone has won
            if self.check_win(self.board) in (-1,1):
                print("Player %s has won" % curr)
                running = False
                break

            # if full draw
            if self.check_full(self.board):
                print("Draw")
                running = False
                break

            # switch current
            if curr == self.p1:
                curr = self.p2
            else:
                curr = self.p1



def main():
    print()
    test = Connect()
    test.show_board()
    test.play_game()



main()