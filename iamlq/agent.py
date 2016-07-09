#!/usr/bin/env python
# -*- coding: utf-8 -*-
from style import *
class Agent(object):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return Style.RED + self.name + Style.END