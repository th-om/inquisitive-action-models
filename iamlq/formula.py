#!/usr/bin/env python
# -*- coding: utf-8 -*-
from set import *
from style import *
from model import *

class Formula(object):
    def __init__(self):
        self.supportSet = {}

    def getDeclarativeVariant(self):
        raise NotImplementedError

    def getSupportSet(self,model):
        if model not in self.supportSet: #To speed things up, only calculate a support set from a formula once
            self.supportSet[model] = self.calculateSupportSet(model)

        return self.supportSet[model]

    def getAlternatives(self,model):
        return self.getSupportSet(model).maxElements()

    def calculateSupportSet(self,model):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

class Top(Formula):

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        return model.domain.powerset()

    def __str__(self):
        return Style.BLUE + '⊤' + Style.END

class Bottom(Formula):

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        return Set([[]])

    def __str__(self):
        return Style.BLUE + '⊥' + Style.END

class Atom(Formula):
    def __init__(self,letter):
        self.letter = letter
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        return model.valuation[self].powerset()

    def __str__(self):
        return Style.BLUE + self.letter + Style.END

class Negation(Formula):
    def __init__(self,sub):
        self.sub = sub
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return Negation(self.sub.getDeclarativeVariant())

    def calculateSupportSet(self,model):
        # ¬p is defined as p → ⊥. However, calculating the support set this way makes the script very slow, so we do this in a simplified way
        return (model.domain - self.sub.getSupportSet(model).union()).powerset()

    def __str__(self):
        return '¬' + str(self.sub)

class Question(Formula):
    def __init__(self,sub):
        self.sub = sub
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return ClassicDisjunction(self.sub,Negation(self.sub))

    def calculateSupportSet(self,model):
        return InqDisjunction(self.sub,Negation(self.sub)).getSupportSet(model)

    def __str__(self):
        return '?' + str(self.sub)

class Conjunction(Formula):
    def __init__(self,*args):
        self.conjuncts = args
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return Conjunction(*[conjunct.getDeclarativeVariant() for conjunct in self.conjuncts])

    def calculateSupportSet(self,model):
        result = None
        for conjunct in self.conjuncts:
            if result is None:
                result = conjunct.getSupportSet(model)
            else:
                result = result.intersect(conjunct.getSupportSet(model))

        return result

    def __str__(self):
        return '(' + ' & '.join([str(conjunct) for conjunct in self.conjuncts]) + ')'

class ClassicDisjunction(Formula):
    def __init__(self,*args):
        self.disjuncts = args
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return ClassicDisjunction(*[disjunct.getDeclarativeVariant() for disjunct in self.disjuncts])

    def calculateSupportSet(self,model):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].getSupportSet(model)
        else:
            return Negation(Conjunction(*[Negation(disjunct) for disjunct in self.disjuncts])).getSupportSet(model)

    def __str__(self):
        string = ' v '.join([str(disjunct) for disjunct in self.disjuncts])
        if len(self.disjuncts) > 1:
            string = '(' + string + ')'
        return string

class InqDisjunction(Formula):
    def __init__(self,*args):
        self.disjuncts = args
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return ClassicDisjunction(*[disjunct.getDeclarativeVariant() for disjunct in self.disjuncts])

    def calculateSupportSet(self,model):
        prop = Set([])
        for disjunct in self.disjuncts:
            prop += disjunct.getSupportSet(model)
        return prop

    def __str__(self):
        string = (' ᗐ ').join([str(disjunct) for disjunct in self.disjuncts])
        if len(self.disjuncts) > 1:
            string = '(' + string + ')'
        return string

class Implication(Formula):
    def __init__(self,antecedent,consequent):
        self.antecedent = antecedent
        self.consequent = consequent
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return Implication(self.antecedent.getDeclarativeVariant(),self.consequent.getDeclarativeVariant())

    def calculateSupportSet(self,model):
        """ For every state s: it is in this proposition iff for every subset t of s, if t in antecedent then t in consequent"""
        prop = Set([])
        for s in model.domain.powerset():
            add_s = True
            for t in s.powerset():
                if t in self.antecedent.getSupportSet(model) and t not in self.consequent.getSupportSet(model):
                    add_s = False
                    break
            if add_s:
                prop.add(s)
        return prop

        
    def __str__(self):
        return '(' + str(self.antecedent) + ' → ' + str(self.consequent) + ')'

class Knows(Formula):
    def __init__(self,agent,sub):
        self.agent = agent
        self.sub = sub
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        prop = Set([])
        for s in model.domain.powerset():
            add_s = True
            for w in s:
                sigma_w = model.statemap[self.agent][w].union()
                if not support(model,sigma_w,self.sub):
                    add_s = False
                    break
            if add_s:
                prop.add(s)
        return prop

    def __str__(self):
        return 'K' + str(self.agent) + '(' + str(self.sub) + ')'

class Entertains(Formula):
    def __init__(self,agent,sub):
        self.agent = agent
        self.sub = sub
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        prop = Set([])
        for s in model.domain.powerset():
            add_s = True
            for w in s:
                sigma_w = model.statemap[self.agent][w]
                for t in sigma_w:
                    if not support(model,t,self.sub):
                        add_s = False
                        break
                if not add_s:
                    break
            if add_s:
                prop.add(s)
        return prop

    def __str__(self):
        return 'E' + str(self.agent) + '(' + str(self.sub) + ')'

class Wonders(Formula):
    def __init__(self,agent,sub):
        self.agent = agent
        self.sub = sub
        Formula.__init__(self)

    def getDeclarativeVariant(self):
        return self

    def calculateSupportSet(self,model):
        return Conjunction(Negation(Knows(self.sub)),Entertains(self.sub)).getSupportSet()

    def __str__(self):
        return 'W' + str(self.agent) + '(' + str(self.sub) + ')'