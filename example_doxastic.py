#!/usr/bin/env python
# -*- coding: utf-8 -*-
from iamlq import *

#Define agents
a = Agent('a')
b = Agent('b')

#Define atoms
p = Atom('p')

#Define worlds
w1 = World('w1')
w2 = World('w2')

#Define domain of epistemic model
W = Set([w1,w2])

#Define state map of epistemic model
Sigma = StateMap({
    a: {
        w1: W.powerset(),
        w2: W.powerset()
    },
    b: {
        w1: W.powerset(),
        w2: W.powerset()
    }
})

#Define valuation of epistemic model
V = Valuation({
    p: Set([w1])
})

#Define epistemic model
M = Model(W,Sigma,V)


#Define action points and their content
x = ActionPoint('x',Question(p))
y = ActionPoint('y',Top())

#Define domain of action model
S = Set([x,y])

#Define state map of action model
Delta = StateMap({
    a: {
        x: Set([[x]]).downset(),
        y: Set([[y]]).downset()
    },
    b: {
        x: Set([[y]]).downset(),
        y: Set([[y]]).downset()
    }
})

#Define action model
N = ActionModel(S,Delta)

#Define the epistemic model after update
O = M * N

#Print results
print Style.BOLD + '==== Epistemic Model ====' + Style.END + '\n' + str(M) + '\n\n'

print Style.BOLD + '==== Action Model ====' + Style.END + '\n' + str(N) + '\n\n'

print Style.BOLD + '==== Updated Model ====' + Style.END + '\n' + str(O)
