# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:16:23 2017

@author: Student
"""
import pdb
from Vehicle import *
from Animals import *

EntityType = { 'Snake' : 0, 'Log' : 1, 'Suv': 2, 'DumpTruck' : 3,
             'Convertable' : 4, 'Coupe' : 5, 'Bus' : 6, 'Goal' : 7}


class EntityFactory:
    
    def __init__(self, entityType, params):
        self.entityType = entityType
        self.params = params
        
    def createEntity(self):
        if self.entityType == EntityType['Snake']:
            return Snake(self.params[0], self.params[1], self.params[2], self.params[3])
        elif self.entityType == EntityType['Log']:
            return Log(self.params[0], self.params[1], self.params[2], self.params[3], self.params[4])
        elif self.entityType == EntityType['Suv']:
            return Suv(self.params[0], self.params[1], self.params[2])
        elif self.entityType == EntityType['DumpTruck']:
            return DumpTruck(self.params[0], self.params[1], self.params[2])
        elif self.entityType == EntityType['Convertable']:
            return Convertable(self.params[0], self.params[1], self.params[2])
        elif self.entityType == EntityType['Coupe']:
            return Coupe(self.params[0], self.params[1], self.params[2])
        elif self.entityType == EntityType['Bus']:
            return Bus(self.params[0], self.params[1], self.params[2])
        elif self.entityType == EntityType['Goal']:
            return Goal(self.params[0], self.params[1], self.params[2])
        pdb.set_trace()