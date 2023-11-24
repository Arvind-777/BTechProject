from pysat.solvers import Solver
import cnf_encoding
from pysat.card import *


def checkDrawOrXWin(boardState, vacant_squares):
    cnfTemp = cnf_encoding.cnf_XWinning.copy()
    cnfTemp.extend(CardEnc.equals(lits=[ele+9 for ele in vacant_squares], encoding=0, bound=0).clauses)
    cnfTemp.extend(CardEnc.equals(lits=vacant_squares, encoding=0, bound=0).clauses)
    with Solver(bootstrap_with=cnfTemp) as solver:
        if(solver.solve(assumptions=boardState)):
            return 1

    return -1 if len(vacant_squares)==0 else 0


def checkOWin(boardState, vacant_squares):
    cnfTemp = cnf_encoding.cnf_OWinning.copy()
    cnfTemp.extend(CardEnc.equals(lits=[ele+9 for ele in vacant_squares], encoding=0, bound=0).clauses)
    cnfTemp.extend(CardEnc.equals(lits=vacant_squares, encoding=0, bound=0).clauses)
    with Solver(bootstrap_with=cnfTemp) as solver:
        return (solver.solve(assumptions=boardState))


marked_squares = []
vacant_squares = [1,2,3,4,5,6,7,8,9]
X_squares = []
O_squares = []
boardState = []

while(True):
    cnf = cnf_encoding.cnf_XWinning.copy()

    while(True):
        try:
            square = int(input("\nChoose square number(1 to 9) to mark with an X: \n"))
            if(square not in vacant_squares):
                print(f"\nThe square you have chosen has already been marked or is out of bounds. Choose one of the vacant squares. The vacant squares are :- {vacant_squares}\n")
            if(square in vacant_squares):
                break
        except:
            print("\nPlease choose a valid integer in the range 1 to 9")
    
    marked_squares.append(square)
    vacant_squares.remove(square)
    X_squares.append(square)
    boardState.append(square+9)
    boardState.append(-square)

    gameState = checkDrawOrXWin(boardState,vacant_squares)
    if(gameState==-1):
        print(f"\nGAME OVER\nGame has ended in a draw. \nX Squares:{X_squares}\nO Squares:{O_squares}\n")
        break
    if(gameState==1):
        print(f"\nGAME OVER\nX has won. \nX Squares:{X_squares}\nO Squares:{O_squares}\n")
        break

    while(True):
        try:
            square = int(input("\nChoose square number(1 to 9) to mark with an O: \n"))
            if(square not in vacant_squares):
                print(f"\nThe square you have chosen has already been marked or is out of bounds. Choose one of the vacant squares. The vacant squares are :- {vacant_squares}\n")
            if(square in vacant_squares):
                break
        except:
            print("\nPlease choose a valid integer in the range 1 to 9")

    marked_squares.append(square)
    vacant_squares.remove(square)
    O_squares.append(square)
    boardState.append(square)
    boardState.append(-square-9)

    oWin = checkOWin(boardState,vacant_squares)
    if(oWin):
        print(f"\nGAME OVER\nO has won. \nX Squares:{X_squares}\nO Squares:{O_squares}\n")
        break

    cnf.extend(CardEnc.equals(lits=[ele+9 for ele in vacant_squares], encoding=0, bound=1).clauses)
    cnf.extend(CardEnc.equals(lits=vacant_squares, encoding=0, bound=0).clauses)

    print("\nSo far, the squares marked with an X are:",X_squares,"\nSo far, the squares marked with an O are:",O_squares)
    
    with Solver(bootstrap_with=cnf) as solver:
        if(solver.solve(assumptions=boardState)):
            newState = solver.get_model()
            for ele in newState:
                if (18>=ele>=10 and (ele-9) in vacant_squares):
                    print(f"X can win if it plays on Square {ele-9} in the next move")
                    
        else:
            print("X can't yet win in the next move")