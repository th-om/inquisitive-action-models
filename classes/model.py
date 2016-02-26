#!/usr/bin/env python
# -*- coding: utf-8 -*-
from actionmodel import *
from set import *
from world import *
from valuation import *
from statemap import *
from formula import *

class Model(object):
    def __init__(self,domain,statemap,valuation):
        self.domain = domain
        self.statemap = statemap
        self.valuation = valuation

    def __str__(self):
        return 'Domain:\n'  + str(self.domain) + '\n\n' + 'Statemap:\n' + str(self.statemap) + '\n\n' + 'Valuation:\n' + str(self.valuation)

    def __mul__(self, other):
        """Defines the update procedure (*) of an epistemic model with an action model: the result is a restricted modal product"""
        if isinstance(other, ActionModel):
            #DOMAIN
            domain = Set([])
            for world in self.domain:
                for actionPoint in other.domain:
                    new_world = World((world,actionPoint))
                    if support(self,Set([new_world.world]),new_world.actionpoint.cont):
                        domain.add(new_world)

            #STATEMAP
            states = domain.powerset()
            statemap = {}
            for agent in self.statemap.agents():
                statemap[agent] = {}
                for world in domain:
                    statemap[agent][world] = Set([])
                    for state in states:
                        #CONDITION (i)
                        condition1 = state.projection(2) in other.statemap[agent][world.actionpoint]

                        #CONDITION (ii)
                        condition2 = state.projection(1) in self.statemap[agent][world.world]

                        #CONDITION (iii)
                        #TO DO: this condition makes the wrong predictions for 2 actions points with the same action content ?p
                        condition3 = False
                        for d in other.statemap[agent][world.actionpoint]:
                            if len(d.items) and state.projection(2) <= d:
                                disjunction = ClassicDisjunction(*[s.cont for s in d])
                                if support(self,state.projection(1),disjunction):
                                    condition3 = True
                                    break

                        if condition1 and condition2 and condition3:
                            statemap[agent][world].add(state)

            statemap = StateMap(statemap)

            #VALUATION
            valuation_data = {}
            for atom in self.valuation:
                valuation_data[atom] = Set([])
                for world in domain:
                    if world.name[0] in self.valuation[atom]:
                        valuation_data[atom].add(world)
            valuation = Valuation(valuation_data)

            return Model(domain,statemap,valuation)

def support(model,state,formula):
    """Returns True iff the state in the model supports the proposition expressed by the formula"""
    return state in formula.getProposition(model)