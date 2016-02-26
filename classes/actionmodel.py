#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ActionModel(object):
    def __init__(self,domain,statemap):
        self.domain = domain
        self.statemap = statemap

    def __str__(self):
        cont = ''
        for actionpoint in self.domain:
            if cont:
                cont += '\n'
            cont += 'cont(' + str(actionpoint) + ') = ' + str(actionpoint.cont)
        return 'Domain:\n' + str(self.domain) + '\n\n' + 'Statemap:\n' + str(self.statemap) + '\n\n' + 'Cont:\n' + cont