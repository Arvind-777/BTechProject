from pysat.solvers import Solver
from pysat.card import *
from pysat.formula import CNF


def addSingleValueConditions(cnf): #condition for each square to have only one number from 1 to 9
    for i in range(1,82):
        litsList = [i+j*81 for j in range(0,9)]
        cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def addRowConditions(cnf): #condition for each row to have every number from 1 to 9 exactly once
    for row in range(1,10):
        for num in range(1,10):
            litsList = [(num-1)*81+(row-1)*9+col for col in range(1,10)]
            cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def addColConditions(cnf): #condition for each column to have every number from 1 to 9 exactly once
    for col in range(1,10):
        for num in range(1,10):
            litsList = [(num-1)*81+(row-1)*9+col for row in range(1,10)]
            cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def addBoxConditions(cnf): #condition for each 3x3 box to have every number from 1 to 9 exactly once
    for box in range(1,10):
        for num in range(1,10):
            litsList = [(num-1)*81+(box//3)*27+((box-1)%3)*3+i for i in [1,2,3,10,11,12,19,20,21]]
            cnf.extend(CardEnc.equals(lits = litsList, encoding=0, bound=1).clauses)

def createBoard(): 
    cnf = CNF()
    addSingleValueConditions(cnf)
    addRowConditions(cnf)
    addColConditions(cnf)
    addBoxConditions(cnf)
    return cnf

def getSudokuInput():
    assumptions = []

    for row in range(1,10):
        rowVals = list(map(int, input(f"\nEnter the numbers in row-{row} : ").strip().split()))[:9]
        for i in range(0,9):
            num = rowVals[i]
            if(num==0):
                continue
            squareNum = (row-1)*9+i+1
            litVal = (num-1)*81+squareNum
            if(1<=litVal and litVal<=729):
                assumptions.append(litVal)

    return assumptions

def displayOutput(model):
    board = []
    for i in range(0,9):
        board.append([0,0,0,0,0,0,0,0,0])

    for litVal in model:
        if(litVal<0 or litVal>729):
            continue
        num = ((litVal-1)//81)+1
        squareNum = litVal-(num-1)*81
        row = ((squareNum-1)//9)+1
        col = ((squareNum-1)%9)+1
        board[row-1][col-1] = num

    for row in board:
        print(*row)



sudokuCNF = createBoard()
presentNumbers = getSudokuInput()
with Solver(bootstrap_with=sudokuCNF) as solver:
        if(solver.solve(assumptions=presentNumbers)):
            sudokuSolution = solver.get_model()
            print("\nThe Solved Sudoku is as shown below : \n")
            displayOutput(sudokuSolution)
        else:
            print("This Sudoku cannot be solved")
