from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF


def knightVar(row, col):
    return 8*row+col+1

def bishopVar(row, col):
    return 64+8*row+col+1

def rookVar(row,col):
    return 128+8*row+col+1

def queenVar(row,col):
    return 192+8*row+col+1

def isInsideBoard(row,col):
    return (0<=row<8)and(0<=col<8)

def addOnePieceConditions(cnf): #condition to have one piece of each type on whole board and at max one piece on each square
    knightList = []
    bishopList = []
    rookList = []
    queenList = []
    for row in range(0,8):
        for col in range(0,8):
            knightList.append(knightVar(row,col))
            bishopList.append(bishopVar(row,col))
            rookList.append(rookVar(row,col))
            queenList.append(queenVar(row,col))
            cnf.extend(CardEnc.atmost(lits = [knightVar(row,col),bishopVar(row,col),rookVar(row,col),queenVar(row,col)], encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits = knightList, encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits = bishopList, encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits = rookList, encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits = queenList, encoding=0, bound=1).clauses)

def addKnightConditions(cnf): #conditions to make sure the knight attacks no pieces
    offsets = [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]
    for row in range(0,8):
        for col in range(0,8):
            for dr,dc in offsets:
                r = row+dr
                c = col+dc
                if(isInsideBoard(r,c)):
                    cnf.append([-knightVar(row,col),-bishopVar(r,c)])
                    cnf.append([-knightVar(row,col),-rookVar(r,c)])
                    cnf.append([-knightVar(row,col),-queenVar(r,c)])

def addBishopConditions(cnf): #conditions to make sure the bishop attacks no pieces
    offsets = []
    for i in range(1,8):
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
                    cnf.append([-bishopVar(row,col),-knightVar(r,c)])
                    cnf.append([-bishopVar(row,col),-rookVar(r,c)])
                    cnf.append([-bishopVar(row,col),-queenVar(r,c)])

def addRookConditions(cnf): #conditions to make sure the rook attacks no pieces
    offsets = []
    for i in range(1,8):
        offsets.append((0,-i))
        offsets.append((0,i))
        offsets.append((-i,0))
        offsets.append((i,0))
    for row in range(0,8):
        for col in range(0,8):
            for dr,dc in offsets:
                r = row+dr
                c = col+dc
                if(isInsideBoard(r,c)):
                    cnf.append([-rookVar(row,col),-knightVar(r,c)])
                    cnf.append([-rookVar(row,col),-bishopVar(r,c)])
                    cnf.append([-rookVar(row,col),-queenVar(r,c)])

def addQueenConditions(cnf): #conditions to make sure the queen attacks no pieces
    offsets = []
    for i in range(1,8):
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
                    cnf.append([-queenVar(row,col),-knightVar(r,c)])
                    cnf.append([-queenVar(row,col),-bishopVar(r,c)])
                    cnf.append([-queenVar(row,col),-rookVar(r,c)])      

def createBoard(): 
    cnf = CNF()
    addOnePieceConditions(cnf)
    addKnightConditions(cnf)
    addBishopConditions(cnf)
    addRookConditions(cnf)
    addQueenConditions(cnf)
    return cnf

def displayOutput(model):
    board = []
    for i in range(0,8):
        board.append(['.' for j in range(0,8)])

    for litVal in model:
        if(litVal<1 or litVal>256):
            continue
        squareNum = (litVal-1)%64
        pieceType = (litVal-1)//64
        val = ''
        if(pieceType==0):
            val='K'
        if(pieceType==1):
            val='B'
        if(pieceType==2):
            val='R'
        if(pieceType==3):
            val='Q'
        row = (squareNum//8)
        col = (squareNum%8)
        board[row][col] = val

    for row in board:
        print(*row)


fourPiecesCNF = createBoard()
with Solver(bootstrap_with=fourPiecesCNF) as solver:
        if(solver.solve()):
            solution = solver.get_model()
            print("\nA possible layout of the 4 pieces is as shown below : \n")
            displayOutput(solution)
        else:
            print("There is no way to place the 4 pieces such that none of them attack each other")
