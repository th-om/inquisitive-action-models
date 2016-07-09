#!/usr/bin/env python
# -*- coding: utf-8 -*-
from formula import *

class ActionModel(object):
    def __init__(self,domain,statemap):
        self.domain = domain
        self.statemap = statemap

    def __str__(self):
        cont = '\n'.join(['cont(' + str(actionpoint) + ') = ' + str(actionpoint.cont) for actionpoint in self.domain])
        pre = '\n'.join(['pre(' + str(actionpoint) + ') = ' + str(actionpoint.pre) for actionpoint in self.domain])
        return 'Domain:\n' + str(self.domain) + '\n\n' + 'Statemap:\n' + str(self.statemap) + '\n\n' + 'Contents and Preconditions:\n' + cont + '\n' + pre