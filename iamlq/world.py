#!/usr/bin/env python
# -*- coding: utf-8 -*-
from style import *
from formula import *

class World(object):
    def __init__(self,name):
        self.name = name
        if type(self.name) is tuple:
            self.world = self.name[0]
            self.actionpoint = self.name[1]

    def __str__(self):
        if type(self.name) is tuple:
            return Style.GREEN + '(' + str(self.world.name) + ',' + str(self.actionpoint.name) + ')' + Style.END
        else:
            return Style.GREEN + str(self.name) + Style.END