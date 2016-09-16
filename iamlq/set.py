#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain, combinations

class Set(object):
    def __init__(self,items):

        for i, value in enumerate(items):
            if type(items[i]) is list:
                items[i] = Set(value)
        self.items = list(set(items))
        self.sorted = False

    def __iter__(self):
        for elem in self.items:
            yield elem

    def __getitem__(self,item):
        return self.items[item]

    def __str__(self):
        self.sort()
        if not len(self.items):
            return '∅'
        elif len(self.items) == 1 and self.items[0] == Set([]):
            return '{∅}'
        elif self.isDownset():
            string = str(self.maxElements()) + '↓'
            return string
        else:
            string = ''
            for item in self.items:
                if string:
                    string += ', '
                string += str(item)
            return '{' + string + '}'

    def __eq__(self, other):
        """A Set is equal to another set iff they contain the same elements"""
        if isinstance(other, self.__class__):
            for i in self.items:
                if i not in other.items:
                    return False
            for i in other.items:
                if i not in self.items:
                    return False
            return True
        else:

            return False

    def __add__(self, other):
        """Defines addition (+) on Sets"""
        result = Set([])
        if isinstance(other, self.__class__):
            for i in self.items:
                result.add(i)
            for i in other.items:
                result.add(i)
            return result
        else:
            return False

    def __sub__(self, other):
        """Defines subtraction (-) on Sets"""
        result = Set([])
        if isinstance(other, self.__class__):
            for i in self.items:
                if i not in other.items:
                    result.add(i)
            return result
        else:
            return False

    def __le__(self, other):
        """Defines subset relation (<=) on Sets"""
        for i in self.items:
            if i not in other.items:
                return False
        return True

    def intersect(self, other):
        """Returns the intersection of the Set with another Set"""
        result = Set([])
        for i in self.items:
            if i in other.items:
                result.add(i)
        return result

    def union(self,*args):
        """Returns the union of a Set of Sets"""

        if not len(args):
            result = Set([])
            for i in self.items:
                for j in i.items:
                    result.add(j)
            return result

    def sort(self):
        """
        Sort Sets of Sets by amount of elements, Sets of other elements alphabetically

        Sorting is only done to make the output look nice
        """
        if not self.sorted:
            self.items.sort(key=lambda x: str(x) if type(x) != Set else len(x.items))
            self.sorted = True #Do not try to sort the same Set again

    def add(self,new_item):
        for item in self.items:
            if item == new_item:
                return False
        self.items.append(new_item)
        self.sorted = False
        return True

    def downset(self):
        """Returns the downward closure of a Set"""
        downset = Set([])
        for s in self.items:
            if type(s) != Set:
                return False
            for subset in s.powerset().items:
                downset.add(subset)
        return downset

    def isDownset(self):
        """Returns True iff Set is downward closed"""
        return self == self.downset()

    def maxElements(self):
        """Returns the maximal elements of a Set of Sets (the Sets such that no other Set is a proper superset of it)"""
        maxElements = Set([])
        for s in self.items:
            isSubset = False
            if type(s) != Set:
                return False
            for t in self.items:
                if s <= t and s != t:
                    isSubset = True
                    break
            if not isSubset:
                maxElements.add(s)

        return maxElements

    def powerset(self):
        """Returns the powerset (set of all subsets) of a Set"""
        powerset = Set([])
        i = set(self.items)
        for z in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
            powerset.add(Set(z))
        return powerset

    def projection(self,index):
        """Returns the projection of a Set of n-tuples (projection(Set([(a,b),(c,d)]),1) = Set([a,c]))"""
        new_set = Set([])
        for elem in self:
            new_set.add(elem.name[index-1])
        return new_set

    def restriction(self,element,index):
        """Returns the restriction of a Set of n-tuples to the ones that contain a certain element at a certain index"""
        new_set = Set([])
        for elem in self:
            if elem.name[index-1] == element:
                new_set.add(elem)
        return new_set