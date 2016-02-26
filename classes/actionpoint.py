#!/usr/bin/env python
# -*- coding: utf-8 -*-
from style import *

class ActionPoint(object):
    def __init__(self,name,cont):
        self.name = name
        self.cont = cont

    def __str__(self):
        return Style.PURPLE + self.name + Style.END