from pysat.formula import CNF
from pysat.card import *

# Literals for O are going to be from 1 to 9 and for X are from 10 to 18
condForXNotWinning =  [[-10,1,-14,5,-18,9],[-12,3,-14,5,-16,7],[-10,1,-13,4,-16,7],[-11,2,-14,5,-17,8],[-12,3,-15,6,-18,9],[-10,1,-11,2,-12,3],[-13,4,-14,5,-15,6],[-16,7,-17,8,-18,9]]
condForONotWinning =  [[10,-1,14,-5,18,-9],[12,-3,14,-5,16,-7],[10,-1,13,-4,16,-7],[11,-2,14,-5,17,-8],[12,-3,15,-6,18,-9],[10,-1,11,-2,12,-3],[13,-4,14,-5,15,-6],[16,-7,17,-8,18,-9]]
# create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
# cnf = CardEnc.equals(lits=[1, 2, 3], encoding=EncType.pairwise, bound=2)
# cnf.extend([[-1],[2],[3]])

cnf_XNotWinning = CNF(from_clauses=condForXNotWinning)
cnf_ONotWinning = CNF(from_clauses=condForONotWinning)
cnf_XWinning = cnf_XNotWinning.negate()
cnf_OWinning = cnf_ONotWinning.negate()