#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes import *

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
s = ActionPoint('s',Question(p))
t = ActionPoint('t',Question(q))

#Define domain of action model
S = Set([s,t])

#Define state map of action model
Delta = StateMap({
    a: {
        s: S.powerset(),
        t: S.powerset()
    },
    b: {
        s: Set([[s],[t]]).downset(),
        t: Set([[s],[t]]).downset()
    },
    c: {
        s: Set([[s]]).downset(),
        t: Set([[t]]).downset()
    }
})

#Define action model
N = ActionModel(S,Delta)

#Define the epistemic model afther update
O = M * N

#Print results
print Style.BOLD + '==== Epistemic Model ====' + Style.END + '\n' + str(M) + '\n\n'

print Style.BOLD + '==== Action Model ====' + Style.END + '\n' + str(N) + '\n\n'

print Style.BOLD + '==== Updated Model ====' + Style.END + '\n' + str(O)
