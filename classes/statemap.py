#!/usr/bin/env python
# -*- coding: utf-8 -*-
from set import *

class StateMap(object):
    def __init__(self,data):
        self.data = data

    def __iter__(self):
        for elem in self.data:
            yield elem

    def __getitem__(self,agent):
        return self.data[agent]

    def agents(self):
        return self.data.keys()

    def __str__(self):
        string = ''

        agents = Set(self.data.keys())
        agents.sort()

        worlds = Set(self.data[agents[0]].keys())
        worlds.sort()

        for agent in agents:
            if string:
                string += '\n'
            string += str(agent) + ': '
            for world in worlds:
                string += '\n' + str(world) + ': ' + str(self.data[agent][world])

        return string