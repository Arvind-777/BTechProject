from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF


def queenVar(row, col):
    return 8*row+col+1

def givenVar(row, col):
    return 64+8*row+col+1

def isInsideBoard(row, col):
    return (0<=row<8)and(0<=col<8)

def addOnePieceCondition(cnf): #condition to have one queen on whole board and no queen where a given piece already exists
    queenList=  []
    for row in range(0,8):
        for col in range(0,8):
            queenList.append(queenVar(row,col))
            cnf.extend(CardEnc.atmost(lits = [queenVar(row,col),givenVar(row,col)], encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits = queenList, encoding=0, bound=1).clauses)

def addQueenConditions(cnf,givenPiecesSquares): #conditions to make sure the queen attacks all pieces placed on the board
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
    for row,col in givenPiecesSquares:
        queenList = []
        for dr,dc in offsets:
            r = row+dr
            c = col+dc
            if(isInsideBoard(r,c)):
                queenList.append(queenVar(r,c))
        cnf.extend(CardEnc.equals(lits = queenList, encoding=0, bound=1).clauses)

def addNoObstructionsCondition(cnf): #conditions to make sure that no piece is obstructed from the queen by another piece and is in direct line of sight of queen
    for row in range(0,8):
        for c1 in range(0,6):
            for c2 in range(c1+1,7):
                for c3 in range(c2+1,8):
                    cnf.append([-queenVar(row,c1),-givenVar(row,c2),-givenVar(row,c3)])
                    cnf.append([-queenVar(row,c3),-givenVar(row,c2),-givenVar(row,c1)])
    for col in range(0,8):
        for r1 in range(0,6):
            for r2 in range(r1+1,7):
                for r3 in range(r2+1,8):
                    cnf.append([-queenVar(r1,col),-givenVar(r2,col),-givenVar(r3,col)])
                    cnf.append([-queenVar(r3,col),-givenVar(r2,col),-givenVar(r1,col)])
    for col in range(0,8):
        diag = [(i,col+i) for i in range(0,8) if isInsideBoard(i,col+i)]
        for i in range(0,len(diag)-2):
            for j in range(i+1,len(diag)-1):
                for k in range(j+1,len(diag)):
                    cnf.append([-queenVar(diag[i][0],diag[i][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[k][0],diag[k][1])])
                    cnf.append([-queenVar(diag[k][0],diag[k][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[i][0],diag[i][1])])
    for row in range(1,8):
        diag = [(row+i,i) for i in range(0,8) if isInsideBoard(row+i,i)]
        for i in range(0,len(diag)-2):
            for j in range(i+1,len(diag)-1):
                for k in range(j+1,len(diag)):
                    cnf.append([-queenVar(diag[i][0],diag[i][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[k][0],diag[k][1])])
                    cnf.append([-queenVar(diag[k][0],diag[k][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[i][0],diag[i][1])])
    for col in range(0,8):
        diag = [(i,col-i) for i in range(0,8) if isInsideBoard(i,col-i)]
        for i in range(0,len(diag)-2):
            for j in range(i+1,len(diag)-1):
                for k in range(j+1,len(diag)):
                    cnf.append([-queenVar(diag[i][0],diag[i][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[k][0],diag[k][1])])
                    cnf.append([-queenVar(diag[k][0],diag[k][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[i][0],diag[i][1])])
    for row in range(1,8):
        diag = [(row+i,7-i) for i in range(0,8) if isInsideBoard(row+i,7-i)]
        for i in range(0,len(diag)-2):
            for j in range(i+1,len(diag)-1):
                for k in range(j+1,len(diag)):
                    cnf.append([-queenVar(diag[i][0],diag[i][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[k][0],diag[k][1])])
                    cnf.append([-queenVar(diag[k][0],diag[k][1]),-givenVar(diag[j][0],diag[j][1]),-givenVar(diag[i][0],diag[i][1])])    



def getPiecesInput():
    assumptions = []
    givenPiecesSquares = []

    while True:
        position = list(map(int, input(f"\nEnter the row and column of the piece or simply press enter if all pieces have been given : ").strip().split()))
        if len(position)<2:
            break
        position = position[:2]
        row = position[0]
        col = position[1]
        if(isInsideBoard(row,col)):
            assumptions.append(givenVar(row,col))
            givenPiecesSquares.append((row,col))

    return assumptions, givenPiecesSquares

def createBoard(givenPiecesSquares): 
    cnf = CNF()
    addOnePieceCondition(cnf)
    addQueenConditions(cnf,givenPiecesSquares)
    addNoObstructionsCondition(cnf)
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


givenPieces, givenPiecesSquares = getPiecesInput()
allPiecesAttackedCNF = createBoard(givenPiecesSquares)
with Solver(bootstrap_with=allPiecesAttackedCNF) as solver:
        if(solver.solve(assumptions=givenPieces)):
            solution = solver.get_model()
            print("\nA possible placement of the Queen is as shown below : \n")
            displayOutput(solution)
        else:
            print("\nThere is no way to place the Queen such that all of the given arrangement of pieces are attacked by it\n")
