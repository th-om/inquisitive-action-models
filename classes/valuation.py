#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Valuation(object):
    def __init__(self,data):
        self.data = data

    def __getitem__(self,atom):
        return self.data[atom]

    def __iter__(self):
        for elem in self.data:
            yield elem

    def __str__(self):
        string = ''
        for i in self.data:
            if string:
                string += '\n'
            string += str(i) + ': ' + str(self.data[i])
        return string