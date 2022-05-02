import time
class Tile:

    nbrs = [(0,1), (0,-1), (1,0), (-1,0)]
    def __init__(self, tileStr: str, row: int, col: int):
        self.tileStr = tileStr
        self.ROW = row
        self.COL = col
        #if not self.checkValid():
        #    print("invalid state")
        #    exit()
        self.dashIndex = self.findDashIndex()

    def getTileStr(self) -> str: return self.tileStr
    def getIndex(self) -> tuple: return self.dashIndex

    def print_state(self) -> None:
        for i in range(self.ROW):
            for j in range(self.COL):
                print(self.tileStr[(i*self.COL)+j],end='')
            print()
        print()
        return

    def checkValid(self) -> bool:
        if len(self.tileStr) != self.COL * self.ROW: return False
        if self.tileStr.count('-') != 1: return False
        if self.COL % 2 == 0:
            if self.countInversions() % 2 != self.dashFromBottom() % 2: return True
        else:
            if self.countInversions() % 2 == 0: return True
        return False

    def dashFromBottom(self) -> int:
        for i in range(self.ROW):
            if '-' in self.tileStr[i*self.COL:i*self.COL+self.COL]:
                return self.ROW - i
        return -1

    def countInversions(self) -> int:
        invs = 0
        for i in range(len(self.tileStr)-1):
            if self.tileStr[i] == '-': continue
            for j in range(i,len(self.tileStr)):
                if self.tileStr[j] == '-': continue
                if self.tileStr[i] > self.tileStr[j]:
                    invs+=1
        return invs

    def findDashIndex(self) -> tuple:
        for i in range(self.ROW):
            sbstr = self.tileStr[i*self.COL:i*self.COL+self.COL]
            if '-' in sbstr:
                return (i, sbstr.index('-'))

    def make_move(self, n: tuple) -> str:
        target = self.tileStr[(n[0]*self.COL)+n[1]]
        newStr = self.tileStr[:self.dashIndex[0]*self.COL + self.dashIndex[1]] + target + self.tileStr[self.dashIndex[0]*self.COL + self.dashIndex[1] + 1:]
        newStr = newStr[:(n[0]*self.COL)+n[1]] + '-' + newStr[(n[0]*self.COL)+n[1] + 1:]
        return newStr

    def get_neighbours(self) -> list:
        validNbrs = []
        for n in self.nbrs:
            nR = n[0] + self.dashIndex[0]
            nC = n[1] + self.dashIndex[1]
            if nR >= 0 and nR < self.ROW and nC >= 0 and nC < self.COL:
                validNbrs.append(self.make_move((nR, nC)))
        return validNbrs

class aStarNode:
    def __init__(self, parent, state, heuristic):
        self.parent = parent
        self.gScore = 0
        if self.parent is not None:
            self.gScore = self.parent.gScore + 1
        self.state = state
        self.hScore = heuristic

    def __hash__(self): return hash(self.state.getTileStr())
    def __eq__(self, other): return self.state.getTileStr() == other.state.getTileStr()
    def getGScore(self): return self.gScore
    def getHScore(self): return self.hScore
    def getFScore(self): return self.gScore + self.hScore
    def getParent(self): return self.parent
    def getState(self): return self.state

class PrioQ:
    def __init__(self): self.q = {}
    def __len__(self) -> int: return len(self.q)
    def get_items(self): return self.q.keys()

    def enqueue(self, item, val: int):
        if item not in self.q.keys():
            self.q[item] = val
        else: print('dupe'); exit()
        return

    def dequeue(self):
        if len(self.q) == 0:
            print("cant dequeue")
            exit()
        mn = 99999
        minKey = None
        for key in self.q.keys():
            if self.q[key] < mn:
                mn = self.q[key]
                minKey = key
        self.q.pop(minKey)
        return minKey

    def remove(self, item):
        if item not in self.q.keys():
            print("item not in queue")
        else:
            self.q.pop(item)

def heuristic(s, COL):
    '''
    # inversions heuristic
    invs = 0
    for i in range(len(s) - 1):
        if s[i] == '-': continue
        for j in range(i, len(s)):
            if s[j] == '-': continue
            if s[i] > s[j]:
                invs += 1
    if s[len(s) - 1] != '-': invs += 1
    return invs

    # misplaced tiles heuristic
    tC = 0
    mt = 0
    for i in range(len(s)):
        if s[i] == '-' and i != len(s)-1: mt += 1
        elif s[i] != '-':
            if ord(s[i]) - ord('a') != tC:
                mt += 1
            tC += 1
    return mt
    '''

    # manhattan heuristic
    solved = getEndState(len(s))
    o = {}
    n = {}
    for i in range(len(s)):
        o[s[i]] = (i//COL,i%COL)
        n[solved[i]] = (i//COL,i%COL)

    manhattan = 0
    for i in solved:
        manhattan += abs(o[i][0] - n[i][0]) + abs(o[i][1] - n[i][1])
    return manhattan

def reconstruct_path(curr, start):
    print()
    path = []
    while curr != start:
        path.append(curr.getState())
        curr = curr.getParent()
    start.getState().print_state()
    print_path(path)

def print_path(path):
    for i in reversed(path):
        i.print_state()
    print("Solvable in " + str(len(path)) + " moves.")

def astar(tile):
    solved = getEndState(len(tile.getTileStr()))
    pq = PrioQ()
    seen = set()
    newNode = aStarNode(None, tile, heuristic(tile.getTileStr(), tile.COL))
    start = newNode
    pq.enqueue(newNode, newNode.getFScore())

    totalNodes = 1
    fac = tile.ROW * tile.COL
    for i in range(1,fac+1):
        totalNodes *= i
    totalNodes //= 2

    print('0/%d nodes' % totalNodes)
    nodes = 1
    while len(pq) > 0:
        curr = pq.dequeue()
        currS = curr.getState()
        if curr.getState().getTileStr() == solved:
            reconstruct_path(curr, start)
            return nodes

        seen.add(currS.getTileStr())
        for nbr in currS.get_neighbours():
            if nbr in seen:
                continue

            gScore = curr.getGScore() + 1

            match = None
            for i in pq.get_items():
                if nbr == i.getState().getTileStr():
                    match = i

            if match is None:
                nodes+=1
                nbrState = Tile(nbr, currS.ROW, currS.COL)
                newNode = aStarNode(curr, nbrState, heuristic(nbrState.tileStr, nbrState.COL))
                pq.enqueue(newNode, newNode.getFScore())
            elif gScore < match.getGScore():
                nodes+=1
                pq.remove(match)
                nbrState = Tile(nbr, currS.ROW, currS.COL)
                newNode = aStarNode(curr, nbrState, heuristic(nbrState.tileStr, nbrState.COL))
                pq.enqueue(newNode, newNode.getFScore())
        # if nodes % 1000 == 0: print('%d/%d nodes' % (nodes, totalNodes))
        if nodes % 1500 in (0,1): print('%.8f%c of nodes searched' % (float(nodes) / float(totalNodes), '%'))

def checkValid(str, ROW, COL) -> bool:
    if len(str) != ROW * COL: return False
    if str.count('-') != 1: return False
    if COL % 2 == 0:
        if countInversions(str) % 2 != dashFromBottom(str, ROW, COL) % 2: return True
    else:
        if countInversions(str) % 2 == 0: return True
    return False

def dashFromBottom(str, ROW, COL):
    for i in range(ROW):
        if '-' in str[i * COL:i * COL + COL]:
            return ROW - i
    return -1

def countInversions(str) -> int:
    invs = 0
    for i in range(len(str)-1):
        if str[i] == '-': continue
        for j in range(i,len(str)):
            if str[j] == '-': continue
            if str[i] > str[j]:
                invs+=1
    return invs

def getEndState(size):
    s = ''
    start = ord('a')
    for i in range(size - 1):
        s += chr(start+i)
    s += '-'
    return s

def main():
    start = time.time()
    tile = Tile('cafbghed-', 3, 3)
    if not checkValid(tile.getTileStr(), tile.ROW, tile.COL):
        print('tile not valid')
        exit()
    print("nodes opened: %d" % astar(tile))
    print('took: %.8f seconds' % (time.time() - start))
    print(getEndState(len(tile.getTileStr())))

main()