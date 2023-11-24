from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF


def queenVar(row, col):
    return 8*row+col+1

def givenVar(row, col):
    return 64+8*row+col+1

def isInsideBoard(row,col):
    return (0<=row<8)and(0<=col<8)

def addOnePieceCondition(cnf): #condition to have one queen on whole board
    queenList=  []
    for row in range(0,8):
        for col in range(0,8):
            queenList.append(queenVar(row,col))
    cnf.extend(CardEnc.equals(lits = queenList, encoding=0, bound=1).clauses)

def addQueenConditions(cnf): #conditions to make sure the queen attacks no pieces placed on the board
    offsets = []
    for i in range(1,8):
        offsets.append((0,0))
        offsets.append((0,-i))
        offsets.append((0,i))
        offsets.append((-i,0))
        offsets.append((i,0))
        offsets.append((-i,-i))
        offsets.append((-i,i))
        offsets.append((i,i))
        offsets.append((i,-i))
    for row in range(0,8):
        for col in range(0,8):
            for dr,dc in offsets:
                r = row+dr
                c = col+dc
                if(isInsideBoard(r,c)):
                    cnf.append([-queenVar(row,col),-givenVar(r,c)])

def getPiecesInput():
    assumptions = []

    while True:
        position = list(map(int, input(f"\nEnter the row and column of the piece or simply press enter if all pieces have been given : ").strip().split()))
        if len(position)<2:
            break
        position = position[:2]
        row = position[0]
        col = position[1]
        if(isInsideBoard(row,col)):
            assumptions.append(givenVar(row,col))

    return assumptions   

def createBoard(): 
    cnf = CNF()
    addOnePieceCondition(cnf)
    addQueenConditions(cnf)
    return cnf

def displayOutput(model):
    board = []
    for i in range(0,8):
        board.append(['.' for j in range(0,8)])

    for litVal in model:
        if(litVal<1 or litVal>128):
            continue
        squareNum = (litVal-1)%64
        pieceType = (litVal-1)//64
        val = ''
        if(pieceType==0):
            val='Q'
        if(pieceType==1):
            val='X'
        row = (squareNum//8)
        col = (squareNum%8)
        board[row][col] = val

    for row in board:
        print(*row)


noPiecesAttackedCNF = createBoard()
givenPieces = getPiecesInput()
with Solver(bootstrap_with=noPiecesAttackedCNF) as solver:
        if(solver.solve(assumptions=givenPieces)):
            solution = solver.get_model()
            print("\nA possible placement of the Queen is as shown below : \n")
            displayOutput(solution)
        else:
            print("\nThere is no way to place the Queen such that none of the given arrangement of pieces are attacked by it\n")
