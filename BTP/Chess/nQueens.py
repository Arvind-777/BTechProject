from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF

def addRowConditions(cnf,n): #condition for each row to have One Queen
    for row in range(0,n):
        litsList = [row*n+col+1 for col in range(0,n)]
        cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def addColConditions(cnf,n): #condition for each column to have at max One Queen
    for col in range(0,n):
        litsList = [row*n+col+1 for row in range(0,n)]
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

def addDiagConditions(cnf,n): #condition for each diagonal to have at max One Queen
    for num in range(1,n+1):
        litsList = []
        diagLength = n-num+1
        i = num
        for j in range(0,diagLength):
            litsList.append(i)
            i += n+1
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

    for num in range(1,n):
        litsList = []
        diagLength = n-num
        i = num*n+1
        for j in range(0,diagLength):
            litsList.append(i)
            i += n+1
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

    for num in range(0,n):
        litsList = []
        diagLength = num+1
        i = num*n+1
        for j in range(0,diagLength):
            litsList.append(i)
            i -= n-1
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

    for num in range(1,n):
        litsList = []
        diagLength = n-num
        i = n*n-n+1+num
        for j in range(0,diagLength):
            litsList.append(i)
            i -= n-1
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)        


def createBoard(n): 
    cnf = CNF()
    addRowConditions(cnf,n)
    addColConditions(cnf,n)
    addDiagConditions(cnf,n)
    return cnf

def getInput():
    nVal = int(input("\nEnter the value of N : "))
    return nVal

def displayOutput(model,n):
    board = []
    for i in range(0,n):
        board.append(['.' for j in range(0,n)])

    for litVal in model:
        if(litVal<1 or litVal>n*n):
            continue
        squareNum = litVal
        row = ((squareNum-1)//n)+1
        col = ((squareNum-1)%n)+1
        board[row-1][col-1] = 'Q'

    for row in board:
        print(*row)



nVal = getInput()
nQueenCNF = createBoard(nVal)
with Solver(bootstrap_with=nQueenCNF) as solver:
        if(solver.solve()):
            solution = solver.get_model()
            print("\nThe N Queens layout is as shown below : \n")
            displayOutput(solution,nVal)
        else:
            print("There cannot be N Queens on the NxN board for N = ",nVal)
