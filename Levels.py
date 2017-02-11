# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 01:15:48 2017

@author: Student
"""
import pdb
import pygame
from Utilities import Direction
from Utilities import Vec
from Zones import Goal
from Zones import Water
from Zones import Wall
from EntityFactory import EntityFactory
from EntityFactory import EntityType

class Level:
    def __init__(self, lvlMgr):
        self.levelManager = lvlMgr
        self.spawnPoint = Vec(6, 14)
        self.waterSize = 5
        self.roadSize = 5
        self.mapSize = Vec(11,15)
        self.rowManagers = []
        self.goalAmount = 3
        self.goalSize = 60
        self.level = 0
        
    def update(self, dT):
        for r in self.rowManagers:
            r.update(dT)
        
class Timing:    
    def __init__(self, time):
        self.time = time
        self.hit = False
        
class RowManager:    
    def __init__(self, lvlMgr, entityFactory, times):
        self.levelManager = lvlMgr
        self.entityFactory = entityFactory
        self.timings = []
        self.time = 0
        
        for t in times:
            self.timings.append(Timing(t))
        self.timings.pop()
        self.endTime = times[len(times) - 1]
        
    def update(self, dT):
        self.time += dT
        
        for t in self.timings:
            if not t.hit and self.time > t.time:
                t.hit = True
                self.levelManager.addEntity(self.entityFactory.createEntity())
                
        if self.time > self.endTime:
            self.time = 0
            for t in self.timings:
                t.hit = False
        
class Level1(Level):
    
    def __init__(self, lvlMgr):
        Level.__init__(self, lvlMgr)
        self.mapSize = Vec(11,15)
        self.waterSize = 5
        self.roadSize = 5
        self.goalAmount = 2
        self.goalSize = 1.2
        self.level = 1
        
        #NOTE Keep timing length the same to keep in sync
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 2, 100, 50, Direction['Left'])), [2,5,8,11]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 3, 200, 40, Direction['Right'])),  [1,8,15]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 4, 120, 120, Direction['Left'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 5, 100, 40, Direction['Right'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Turtle'], (lvlMgr, 6, 3, 40, Direction['Left'])), [1, 10]))
        
        #self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Snake'], (lvlMgr, 7, 20, Direction['Right'])), [1,8]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Bus'], (lvlMgr, 8,  Direction['Left'])), [1,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Coupe'], (lvlMgr, 9,  Direction['Right'])), [1.5,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 10,  Direction['Left'])), [3,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['DumpTruck'], (lvlMgr, 11,  Direction['Right'])), [2.5,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Suv'], (lvlMgr, 12,  Direction['Left'])), [1.25,8]))
        
        wallWidth = (((self.mapSize.x * lvlMgr.getTileSize().x) - (self.goalSize * lvlMgr.getTileSize().x * self.goalAmount)) / (self.goalAmount + 1)) / lvlMgr.getTileSize().x
       
        for i in range(1, self.goalAmount + 1):
            self.levelManager.addEntity(Goal(lvlMgr, self.goalSize, (wallWidth * i) + (self.goalSize * (i - 1))))

        for i in range(0, self.goalAmount + 1):
            self.levelManager.addEntity(Wall(lvlMgr, wallWidth, ((wallWidth * lvlMgr.getTileSize().x + self.goalSize * lvlMgr.getTileSize().x) / lvlMgr.getTileSize().x) * i))
        self.levelManager.addEntity(Water(lvlMgr, self.mapSize.x, self.waterSize))
        
        
class Level2(Level):
    
    def __init__(self, lvlMgr):
        Level.__init__(self, lvlMgr)
        self.mapSize = Vec(11,15)
        self.waterSize = 3
        self.roadSize = 7
        self.goalAmount = 4
        self.goalSize = 1.2
        self.level = 2
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 2, 100, 50, Direction['Left'])), [4,8,10]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 3, 200, 40, Direction['Right'])),  [0, 6, 12]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Turtle'], (lvlMgr, 4, 3, 40, Direction['Left'], (1,1,1,1))), [1, 10]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Snake'], (lvlMgr, 5, 20, Direction['Right'])), [1,8]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Bus'], (lvlMgr, 6,  Direction['Left'])), [4, 6, 9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Coupe'], (lvlMgr, 7,  Direction['Right'])), [1,2,5]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 8,  Direction['Left'])), [3,6]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['DumpTruck'], (lvlMgr, 9,  Direction['Right'])), [4, 8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Suv'], (lvlMgr, 10,  Direction['Left'])), [4,5,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Coupe'], (lvlMgr, 11,  Direction['Right'])), [2,3,5]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 12,  Direction['Left'])), [2,4,6]))
        
        wallWidth = (((self.mapSize.x * lvlMgr.getTileSize().x) - (self.goalSize * lvlMgr.getTileSize().x * self.goalAmount)) / (self.goalAmount + 1)) / lvlMgr.getTileSize().x
       
        for i in range(1, self.goalAmount + 1):
            self.levelManager.addEntity(Goal(lvlMgr, self.goalSize, (wallWidth * i) + (self.goalSize * (i - 1))))

        for i in range(0, self.goalAmount + 1):
            self.levelManager.addEntity(Wall(lvlMgr, wallWidth, ((wallWidth * lvlMgr.getTileSize().x + self.goalSize * lvlMgr.getTileSize().x) / lvlMgr.getTileSize().x) * i))
        self.levelManager.addEntity(Water(lvlMgr, self.mapSize.x, self.waterSize))
        
class Level3(Level):
    
    def __init__(self, lvlMgr):
        Level.__init__(self, lvlMgr)
        self.mapSize = Vec(15,15)
        self.waterSize = 5
        self.roadSize = 5
        self.goalAmount = 4
        self.goalSize = 1.2
        self.level = 3
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 2, 100, 50, Direction['Left'])), [2,5,8,11]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 3, 200, 40, Direction['Right'])),  [1,8,15]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 4, 120, 120, Direction['Left'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 5, 100, 40, Direction['Right'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 6, 100, 110, Direction['Left'])), [1.5, 4, 7]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Snake'], (lvlMgr, 7, 20, Direction['Right'])), [1,8]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Bus'], (lvlMgr, 8,  Direction['Left'])), [1,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Coupe'], (lvlMgr, 9,  Direction['Left'])), [1.5,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 10,  Direction['Right'])), [2,2.5,3,3.5,4]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 11,  Direction['Right'])), [1,1.5,2,2.5,4]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 12,  Direction['Right'])), [0,0.5,1,1.5,4]))
        
        wallWidth = (((self.mapSize.x * lvlMgr.getTileSize().x) - (self.goalSize * lvlMgr.getTileSize().x * self.goalAmount)) / (self.goalAmount + 1)) / lvlMgr.getTileSize().x
       
        for i in range(1, self.goalAmount + 1):
            self.levelManager.addEntity(Goal(lvlMgr, self.goalSize, (wallWidth * i) + (self.goalSize * (i - 1))))

        for i in range(0, self.goalAmount + 1):
            self.levelManager.addEntity(Wall(lvlMgr, wallWidth, ((wallWidth * lvlMgr.getTileSize().x + self.goalSize * lvlMgr.getTileSize().x) / lvlMgr.getTileSize().x) * i))
        self.levelManager.addEntity(Water(lvlMgr, self.mapSize.x, self.waterSize))
        
class Level4(Level):
    
    def __init__(self, lvlMgr):
        Level.__init__(self, lvlMgr)
        self.mapSize = Vec(11,15)
        self.waterSize = 8
        self.roadSize = 2
        self.goalAmount = 5
        self.goalSize = 1.1
        self.level = 4
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 2, 100, 50, Direction['Left'])), [2,5,10]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 3, 200, 40, Direction['Right'])),  [1,8,15]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 4, 120, 120, Direction['Left'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 5, 100, 40, Direction['Right'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 6, 100, 110, Direction['Left'])), [1.5, 4, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 7, 120, 120, Direction['Right'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 8, 100, 40, Direction['Left'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 9, 100, 110, Direction['Right'])), [1.5, 4, 7]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Snake'], (lvlMgr, 10, 20, Direction['Right'])), [1,8]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Bus'], (lvlMgr, 11,  Direction['Left'])), [1,3,5,8]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 12,  Direction['Left'])), [.5,3,3.5,5,6]))
        
        wallWidth = (((self.mapSize.x * lvlMgr.getTileSize().x) - (self.goalSize * lvlMgr.getTileSize().x * self.goalAmount)) / (self.goalAmount + 1)) / lvlMgr.getTileSize().x
       
        for i in range(1, self.goalAmount + 1):
            self.levelManager.addEntity(Goal(lvlMgr, self.goalSize, (wallWidth * i) + (self.goalSize * (i - 1))))

        for i in range(0, self.goalAmount + 1):
            self.levelManager.addEntity(Wall(lvlMgr, wallWidth, ((wallWidth * lvlMgr.getTileSize().x + self.goalSize * lvlMgr.getTileSize().x) / lvlMgr.getTileSize().x) * i))
        self.levelManager.addEntity(Water(lvlMgr, self.mapSize.x, self.waterSize))
        
class Level5(Level):
    
    def __init__(self, lvlMgr):
        Level.__init__(self, lvlMgr)
        self.mapSize = Vec(6,15)
        self.waterSize = 9
        self.roadSize = 1
        self.goalAmount = 5
        self.goalSize = 1.1
        self.level = 4
        self.spawnPoint = Vec(3,14)
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 2, 100, 50, Direction['Left'])), [2,5,10]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 3, 200, 40, Direction['Right'])),  [1,8,15]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 4, 120, 120, Direction['Left'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 5, 100, 40, Direction['Right'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 6, 100, 110, Direction['Left'])), [1.5, 4, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 7, 120, 120, Direction['Right'])), [1, 3, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 8, 100, 40, Direction['Left'])),  [1,4,9]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 9, 100, 110, Direction['Right'])), [1.5, 4, 7]))
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Log'], (lvlMgr, 10, 100, 40, Direction['Left'])),  [1,4,9]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Snake'], (lvlMgr, 11, 20, Direction['Right'])), [1,8]))
        
        self.rowManagers.append(RowManager(lvlMgr, EntityFactory(EntityType['Convertable'], (lvlMgr, 12,  Direction['Left'])), [.5,3,3.5,5,6]))
        
        wallWidth = (((self.mapSize.x * lvlMgr.getTileSize().x) - (self.goalSize * lvlMgr.getTileSize().x * self.goalAmount)) / (self.goalAmount + 1)) / lvlMgr.getTileSize().x
       
        for i in range(1, self.goalAmount + 1):
            self.levelManager.addEntity(Goal(lvlMgr, self.goalSize, (wallWidth * i) + (self.goalSize * (i - 1))))

        for i in range(0, self.goalAmount + 1):
            self.levelManager.addEntity(Wall(lvlMgr, wallWidth, ((wallWidth * lvlMgr.getTileSize().x + self.goalSize * lvlMgr.getTileSize().x) / lvlMgr.getTileSize().x) * i))
        self.levelManager.addEntity(Water(lvlMgr, self.mapSize.x, self.waterSize))
        
        