from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF

def addRowConditions(cnf,n): #condition for each row on every level to have One Queen
    for level in range(0,n):
        for row in range(0,n):
            litsList = [level*n*n+row*n+col+1 for col in range(0,n)]
            cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def addColConditions(cnf,n): #condition for each column on every level to have at max One Queen
    for level in range(0,n):
        for col in range(0,n):
            litsList = [level*n*n+row*n+col+1 for row in range(0,n)]
            cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

def addDiagConditions(cnf,n): #condition for each diagonal on every level to have at max One Queen
    for level in range(0,n):
        for num in range(1,n+1):
            litsList = []
            diagLength = n-num+1
            i = num
            for j in range(0,diagLength):
                litsList.append(level*n*n+i)
                i += n+1
            cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

        for num in range(1,n):
            litsList = []
            diagLength = n-num
            i = num*n+1
            for j in range(0,diagLength):
                litsList.append(level*n*n+i)
                i += n+1
            cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

        for num in range(0,n):
            litsList = []
            diagLength = num+1
            i = num*n+1
            for j in range(0,diagLength):
                litsList.append(level*n*n+i)
                i -= n-1
            cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)

        for num in range(1,n):
            litsList = []
            diagLength = n-num
            i = n*n-n+1+num
            for j in range(0,diagLength):
                litsList.append(level*n*n+i)
                i -= n-1
            cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses)        

def addVerticalConditions(cnf,n): #condition for each vertical column to have at max one Queen
    for i in range(1,n*n+1):
        litsList = []
        for level in range(0,n):
            litsList.append(level*n*n+i)
        cnf.extend(CardEnc.atmost(lits = litsList, encoding=0, bound=1).clauses) 

def createBoard(n): 
    cnf = CNF()
    addRowConditions(cnf,n)
    addColConditions(cnf,n)
    addDiagConditions(cnf,n)
    addVerticalConditions(cnf,n)
    return cnf

def getInput():
    nVal = int(input("\nEnter the value of N : "))
    return nVal

def displayOutput(model,n):
    cube = []
    for level in range(0,n):
        board = []
        for i in range(0,n):
            board.append(['.' for j in range(0,n)])
        cube.append(board)

    for litVal in model:
        if(litVal<1 or litVal>n*n*n):
            continue
        squareNum = litVal
        row = (((squareNum-1)%(n*n))//n)+1
        col = (((squareNum-1)%(n*n))%n)+1
        level = ((squareNum-1)//(n*n))+1
        cube[level-1][row-1][col-1] = 'Q'

    for level in range(0,n):
        board = cube[level]
        print(f"\nLevel-{level+1} Layout:\n")
        for row in board:
            print(*row)


nVal = getInput()
n2QueenCNF = createBoard(nVal)
with Solver(bootstrap_with=n2QueenCNF) as solver:
        if(solver.solve()):
            solution = solver.get_model()
            print("\nThe N^2 Queens layout is as shown below, level by level: \n")
            displayOutput(solution,nVal)
        else:
            print("There is no N^2 Queens layout in the NxNxN cube as required for N = ",nVal)
