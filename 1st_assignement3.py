
#structure of the code from https://github.com/Pyomo/PyomoGettingStarted/blob/master/01_PyomoOverview.ipynb

from __future__ import division 
from pyomo.environ import *

model = AbstractModel()

model.m = Param(within=NonNegativeIntegers) # Number of queries
model.n = Param(within=NonNegativeIntegers) # Number of companies

model.Ia = RangeSet(1, model.m+model.n)
model.Ja = RangeSet(1, (model.m*model.n) + (model.m+model.n))
model.I = RangeSet(1,model.n)
model.J = RangeSet(1,model.m)

model.a = Param(model.Ia, model.Ja)
model.b = Param(model.Ia) #Budget
model.c = Param(model.Ja)

model.x = Var(model.Ja, domain=NonNegativeReals)

def obj_expression(model):
    return summation(model.c, model.x)

#std form - minimize
model.OBJ = Objective(rule=obj_expression)


def ax_constraint_rule(model, i):
    # return the expression for the constraint for i
    return sum(model.a[i,j] * model.x[j] for j in model.Ja) == model.b[i]

# the next line creates one constraint for each member of the set model.I
model.AxbConstraint = Constraint(model.Ia, rule=ax_constraint_rule)