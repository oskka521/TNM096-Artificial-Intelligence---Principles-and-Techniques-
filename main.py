from copy import deepcopy
import random
import time
import heapq


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


class state:
    def __init__(self,board,parent):
        self.board = board
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h1 = 0
        self.h2 = 0
        self.GoalBoard = [1,2,3,4,5,6,7,8,0]

    def NrOfMisplaced(self):
        h1 = 0
        counter = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != self.GoalBoard[counter]:
                    h1 += 1
                counter += 1
        return h1


    def manhattan(self):
        h2 = 0
        for y in range(3):  
            for x in range(3):
                value = self.board[y][x]
                Vx, Vy = self.GetXY(value, make2DArray(self.GoalBoard))
                #print("looking at", value, " Vx  = ", Vx, " Vy  = ", Vy, " x  = ", x, " y  = ", y)
                h2 += abs(Vx - x) + abs(Vy - y)
        return h2

    def GetXY(self,value,arr):
        for y in range(3):
            for x in range(3):
                if arr[y][x] == value:
                    return x, y


    def goal(self):
        counter = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != self.GoalBoard[counter]:
                    return False
                counter += 1
        return True

    def __lt__(self, other):
        return self.f < other.f




def make2DArray(array):
    return [[array[0], array[1], array[2]],
            [array[3], array[4], array[5]],
            [array[6], array[7], array[8]]]

def BoardToclosedDict(board):
    string = "["
    for i in range(3):
        for j in range(3):
            string += str(board[i][j]) + ","
    string = string[0:len(string)-1] + "]"
    return string

def move_function(ThisState):
    ThisState = ThisState.board
    for i in range(3):
        for j in range(3):
            if ThisState[i][j] == 0:
                y = i
                x = j
                break
    ListOfChildern = []
    #print("X = ",x, ", Y = ",y)
    if x - 1 >= 0: #left
        #print("can left")
        b = deepcopy(ThisState)
        b[y][x] = b[y][x - 1]
        b[y][x - 1] = 0
        succ = state(b, ThisState)
        ListOfChildern.append(succ)
    if x + 1 < 3: #right
        #print("can right")
        b = deepcopy(ThisState)
        b[y][x] = b[y][x + 1]
        b[y][x + 1] = 0
        succ = state(b, ThisState)
        ListOfChildern.append(succ)
    if y - 1 >= 0: #down
        #print("can up")
        b = deepcopy(ThisState)
        b[y][x] = b[y - 1][x]
        b[y - 1][x] = 0
        succ = state(b, ThisState)
        ListOfChildern.append(succ)
    if y + 1 < 3: #up
        #print("can down")
        b = deepcopy(ThisState)
        b[y][x] = b[y + 1][x]
        b[y + 1][x] = 0
        succ = state(b, ThisState)
        ListOfChildern.append(succ)

    return ListOfChildern

def RunAstarSeach(StartPos,arg):

    openList = []
    closedDict = {}
    heapq.heappush(openList,StartPos)

    while openList:
        CurrentPos = heapq.heappop(openList)

        Priority = 0
        ToStr = BoardToclosedDict(CurrentPos.board)


        if CurrentPos.goal():
            print("ENDING")
            return CurrentPos,closedDict

        closedDict[ToStr] = CurrentPos
        ListOfChildern = move_function(CurrentPos)


        for child in ListOfChildern:
            if BoardToclosedDict(child.board) in closedDict:
                continue

            else:
                child.g = CurrentPos.g + 1
                child.h1 = child.NrOfMisplaced()
                child.h2 = child.manhattan()

                if arg == 1:
                    child.f = child.h1 + child.g
                else:
                    child.f = child.h2 + child.g
                #print("here is the Children : ", child.board, " f: ", child.f, " h: ", child.h1)
                child.parent = CurrentPos
                heapq.heappush(openList, child)


        #openList.sort(key=lambda x:x.f,reverse=False)





def main():
    array = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    array = [2, 3, 1, 4, 5, 6, 7, 8, 0]
    array = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    array = [1, 2, 3, 4, 5, 6, 0, 7, 8]
    array = [1, 2, 3, 0, 5, 6, 4, 7, 8]
    array = [0, 1, 3, 5, 2, 6, 4, 7, 8]
    array = [5, 1, 3, 0, 2, 6, 4, 7, 8]
    array = [5, 1, 3, 2, 7, 6, 0, 4, 8] #Easy
    array = [1, 0, 5, 6, 4, 7, 2, 3, 8] #almost the Hardest 27 moves
    array = [6, 4, 7, 8, 5, 0, 3, 2, 1] #hardest 31 moves
    array = make2DArray(array)
    print(array)
    firstState = state(array,None)
    t1 = time.time()

    # CheckIfSloveAble(firstState)
    if True:
        print("This can be solved: ")
        arg = 2
        result,closedDict = RunAstarSeach(firstState,arg)

        trace = result.parent
        counter = result.g
        t2 = time.time()
        if arg == 2:
            typeString = "Manhattan"
        else:
            typeString = "NrOfMissPlaced"
        print("\n\nXXXXXXXXXXXSolutionXXXXXXXXXXX")
        print("Number of visited states: %d "%(len(closedDict)))
        print("Number of Levels: %d\nTime: %f\nType: %s"%(result.g,t2 - t1,typeString))
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")

        print("THE WAY (NR = %d) " % (counter), result.board,"The F-value: %d" %(result.f))
        counter -= 1
        while trace:
            print("THE WAY (NR = %d) "% (counter),trace.board, "The F-value: %d" %(trace.f))
            counter  -= 1
            trace = trace.parent


if __name__ == "__main__":
    main()