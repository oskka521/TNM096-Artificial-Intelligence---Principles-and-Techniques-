from copy import deepcopy
import random

####################Checking####################
def getInvCount(arr):
    inv_count = 0;
    temp = []
    for k in arr:
        for m in k:
            temp.append(m)

    for i in range(len(temp)):
       for j in range(i+1,len(temp)):
            if temp[j]>temp[i]:
                inv_count += 1
    return inv_count

def CheckIfSloveAble(array):
    invCount = getInvCount(array.board)
    if invCount%2 == 1:
        return False
    else:
        return True

####################Checking####################

####################The Game####################
class puzzle:
    def __init__(self, starting, parent):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h1 = 0
        self.h2 = 0

    def manhattan(self):
        h2 = 0
        for i in range(3):
            for j in range(3):
                x, y = divmod(self.board[i][j], 3)
                h2 += abs(x - i) + abs(y - j)
        return h2

    def NrOfMisplaced(self):
        h1 = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != h1:
                    h1 += 1
        return h1

    def goal(self):
        inc = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != inc:
                    return False
                inc += 1
        return True
####################The Game####################

################Playing The Game################
def move_function(curr):
    curr = curr.board
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    if x - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x - 1][y]
        b[x - 1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if x + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x + 1][y]
        b[x + 1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x][y - 1]
        b[x][y - 1] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x][y + 1]
        b[x][y + 1] = 0
        succ = puzzle(b, curr)
        q.append(succ)

    return q


def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if (item.f < f):
            f = item.f
            index = i

    return openList[index], index

def AStar(start,arg):
    loops = 0
    openList = []
    closedList = []
    openList.append(start)
    while openList:
        current, index = best_fvalue(openList)
        if current.goal():
            return current,loops
        openList.pop(index)
        closedList.append(current)
        loops += 1
        X = move_function(current)
        for move in X:
            ok = False  # checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:  # not in closed list
                newG = current.g + 1
                present = False

                # openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            if arg == 1:
                                openList[j].f = openList[j].g + openList[j].h2
                            elif arg == 2:
                                openList[j].f = openList[j].g + openList[j].h1 + openList[j].h2
                            elif arg == 3:
                                h5 = max([openList[j].h1, openList[j].h2])
                                openList[j].f = openList[j].g + h5
                            else:
                                openList[j].f = openList[j].g + openList[j].h1
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    if arg == 1:
                        move.h2 = move.manhattan()
                        move.f = move.g + move.h2
                    elif arg == 2:
                        move.h1 = move.NrOfMisplaced()
                        move.h2 = move.manhattan()
                        move.f = move.g + move.h2 + move.h1
                    elif arg == 3:
                        move.h1 = move.NrOfMisplaced()
                        move.h2 = move.manhattan()
                        h5 = max([move.h1,move.h2])
                        move.f = move.g + move.h2 + h5
                    else:
                        move.h1 = move.NrOfMisplaced()
                        move.f = move.g + move.h1
                    move.parent = current
                    openList.append(move)

################Playing The Game################


def Display(array,text):
    print("\n",text)
    for i in array:
        print(i)

def make2DArray(array):
    return [[array[0], array[1], array[2]],
            [array[3], array[4], array[5]],
            [array[6], array[7], array[8]]]


def main():


    array = [0,1,2,3,4,5,6,7,8]
    random.shuffle(array)
    array = make2DArray(array)
    print(array)

    # Slow Length: 20  Score, F =  28  Nrchecking =  20092 MAX
    array =  [[2, 4, 0], [3, 7, 5], [8, 1, 6]]

    start = puzzle(array, None)



    #Not solveable
    #start = puzzle([[3, 8, 0], [6, 7, 4], [2, 1, 5]], None)
    #start = puzzle([[5, 2, 8], [4, 1, 7], [0, 3, 6]], None)
    #start = puzzle([[0,1,2],[3,4,5],[6,7,8]], None)
    #start = puzzle([[2, 1, 0], [3, 4, 5], [6, 7, 8]], None)
    #start = puzzle([[2, 1, 0], [3, 4, 5], [6, 7, 8]], None)
    #solveable
    start = puzzle([[1,2,0],[3,4,5],[6,7,8]], None)
    #start = puzzle([[5, 2, 8], [4, 1, 7], [0, 3, 6]], None)



    NrOfMisplaced = 0
    ManhattanMethod = 1
    Both = 2
    max  = 3
    #Method = NrOfMisplaced
    #Method = ManhattanMethod
    #Method = Bothp
    Method = max

    if CheckIfSloveAble(start):
        print("This can be solved: ")
        result,loops = AStar(start,Method)
        noofMoves = 0
        Display(result.board, "Final")
        t = result.parent
        counter = 1
        while t:
            noofMoves += 1
            Display(t.board, "Nr %d" % (counter))
            # print(t.board)
            counter += 1
            t = t.parent

        print("\nLength: " + str(noofMoves), " Score, F = ",result.f, " Nrchecking = ",loops)

    else:
        print("cant be solved")
        for i in start.board:
            print(i)


if __name__ =="__main__":
    main()



