
from __future__ import division 
from pyomo.environ import *

model = AbstractModel()

model.m = Param(within=NonNegativeIntegers)
model.n = Param(within=NonNegativeIntegers)

model.Ia = RangeSet(1, model.m+model.n)
model.Ja = RangeSet(1, model.m*model.n)

model.a = Param(model.Ia, model.Ja)
model.b = Param(model.Ia)
model.r = Param(model.Ja)

# the next line declares a variable indexed by the set J
model.y = Var(model.Ia, domain=Reals)

#maximize
def obj_expression(model):
    return summation(model.b, model.y)

model.OBJ = Objective(rule=obj_expression)

#we need to do At*y, but changing the indexes to 
#access the matrix does the trick
def ax_constraint_rule(model, j):
    # return the expression for the constraint for i
    return sum(model.a[i,j] * model.y[i] for i in model.Ia) >= model.r[j]

# the next line creates one constraint for each member of the set model.I
model.AxbConstraint = Constraint(model.Ja, rule=ax_constraint_rule)