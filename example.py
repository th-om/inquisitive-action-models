#!/usr/bin/env python
# -*- coding: utf-8 -*-
from iamlq import *

#Define agents
a = Agent('a')
b = Agent('b')
c = Agent('c')

#Define atoms
p = Atom('p')
q = Atom('q')

#Define worlds
w1 = World('w1')
w2 = World('w2')
w3 = World('w3')
w4 = World('w4')

#Define domain of epistemic model
W = Set([w1,w2,w3,w4])

#Define state map of epistemic model
Sigma = StateMap({
    a: {
        w1: W.powerset(),
        w2: W.powerset(),
        w3: W.powerset(),
        w4: W.powerset()
    },
    b: {
        w1: W.powerset(),
        w2: W.powerset(),
        w3: W.powerset(),
        w4: W.powerset()
    },
    c: {
        w1: W.powerset(),
        w2: W.powerset(),
        w3: W.powerset(),
        w4: W.powerset()
    }
})

#Define valuation of epistemic model
V = Valuation({
    p: Set([w1,w3]),
    q: Set([w1,w2])
})

#Define epistemic model
M = Model(W,Sigma,V)


#Define action points and their content
x = ActionPoint('x',Question(p))
y = ActionPoint('y',q)

#Define domain of action model
S = Set([x,y])

#Define state map of action model
Delta = StateMap({
    a: {
        x: Set([[x]]).downset(),
        y: Set([[y]]).downset()
    },
    b: {
        x: Set([[x],[y]]).downset(),
        y: Set([[x],[y]]).downset()
    },
    c: {
        x: S.powerset(),
        y: S.powerset()
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
