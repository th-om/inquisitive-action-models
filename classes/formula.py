#!/usr/bin/env python
# -*- coding: utf-8 -*-
from set import *
from style import *

#TODO: cache result of getProposition to make things a little faster

class Formula(object):
    def getProposition(self,model):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

class Top(Formula):

    def getProposition(self,model):
        return model.domain.powerset()

    def __str__(self):
        return Style.BLUE + '⊤' + Style.END

class Bottom(Formula):

    def getProposition(self,model):
        return Set([[]])

    def __str__(self):
        return Style.BLUE + '⊥' + Style.END

class Atom(Formula):
    def __init__(self,letter):
        self.letter = letter

    def getProposition(self,model):
        return model.valuation[self].powerset()

    def __str__(self):
        return Style.BLUE + self.letter + Style.END

class Negation(Formula):
    def __init__(self,sub):
        self.sub = sub

    def getProposition(self,model):
        #return Implication(self.sub,Bottom()).getProposition(model) # ¬p is defined as p → ⊥. This however makes the script very slow
        return (model.domain - self.sub.getProposition(model).union()).powerset()

    def __str__(self):
        return '¬' + str(self.sub)

class Question(Formula):
    def __init__(self,sub):
        self.sub = sub

    def getProposition(self,model):
        return InqDisjunction(self.sub,Negation(self.sub)).getProposition(model)

    def __str__(self):
        return '?' + str(self.sub)

class Conjunction(Formula):
    def __init__(self,*args):
        self.conjuncts = args

    def getProposition(self,model):
        result = None
        for conjunct in self.conjuncts:
            if result is None:
                result = conjunct.getProposition(model)
            else:
                result = result.intersect(conjunct.getProposition(model))

        return result

    def __str__(self):
        return '(' + ' & '.join([str(conjunct) for conjunct in self.conjuncts]) + ')'

class ClassicDisjunction(Formula):
    def __init__(self,*args):
        self.disjuncts = args

    def getProposition(self,model):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].getProposition(model)
        else:
            return Negation(Conjunction(*[Negation(disjunct) for disjunct in self.disjuncts])).getProposition(model)

    def __str__(self):
        string = ' v '.join([str(disjunct) for disjunct in self.disjuncts])
        if len(self.disjuncts) > 1:
            string = '(' + string + ')'
        return string

class InqDisjunction(Formula):
    def __init__(self,disjunct1,disjunct2):
        self.disjunct1 = disjunct1
        self.disjunct2 = disjunct2

    def getProposition(self,model):
        return self.disjunct1.getProposition(model) + self.disjunct2.getProposition(model)

    def __str__(self):
        return '(' + str(self.disjunct1) + ' ' + Style.UNDERLINE + 'v' + Style.END + ' ' + str(self.disjunct2) + ')'

class Implication(Formula):
    def __init__(self,antecedent,consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def getProposition(self,model):
        """ For every state s: it is in this proposition iff for every subset t of s, if t in antecedent then t in consequent"""
        prop = Set([])
        for s in model.domain.powerset():
            add_s = True
            for t in s.powerset():
                if t in self.antecedent.getProposition(model) and t not in self.consequent.getProposition(model):
                    add_s = False
                    break
            if add_s:
                prop.add(s)
        return prop

        
    def __str__(self):
        return '(' + str(self.antecedent) + ' → ' + str(self.consequent) + ')'
