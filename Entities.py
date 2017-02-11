# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:40:37 2017

@author: Student
"""
import pygame
import math
import pdb
from Utilities import Direction
from Utilities import Color
from Utilities import Vec

#Different Vehicle types, includes Logs
class Vehicle:
    def __init__(self, lvlMgr, tileY, width, height, speed, direction, color):
        self.levelManager = lvlMgr
        self.position = Vec(0,0)
        
        if direction == Direction['Left']:
            self.position.x = lvlMgr.getMapSize().x * lvlMgr.getTileSize().x - 1
        else:
            self.position.x = 0 - width + 1
        self.position.y = lvlMgr.getTileSize().y * tileY
        self.tileY = tileY
        self.size = Vec(width, height)
        self.speed = speed
        self.direction = direction
        self.color = color
        
    def playerCollided(self, player):
        self.levelManager.playerKilled()
        
    def update(self, dT):
        self.position.x += (self.speed * (self.direction - 1)) * dT
        if self.levelManager.isOutsideWindow(self):
            self.levelManager.removeEntity(self)
        
    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.position.x, self.position.y + (self.levelManager.getTileSize().y - self.size.y) / 2, self.size.x, self.size.y - (self.levelManager.getTileSize().y - self.size.y) /2))
        
class DumpTruck(Vehicle):
    def __init__(self, lvlMgr, tileY, direction = 2):
        Vehicle.__init__(self, lvlMgr,tileY, 100, 36, 50, direction, Color['Yellow'])
        
class Convertable(Vehicle):
    def __init__(self, lvlMgr,tileY, direction = 2):
        Vehicle.__init__(self, lvlMgr,tileY, 50, 30, 120, direction, Color['Red'])
        
class Bus(Vehicle):
    def __init__(self, lvlMgr,tileY, direction = 2):
        Vehicle.__init__(self, lvlMgr,tileY, 120, 36, 70, direction, Color['Yellow'])
        
class Suv(Vehicle):
    def __init__(self, lvlMgr,tileY, direction = 2):
        Vehicle.__init__(self, lvlMgr,tileY, 80, 34, 80, direction, Color['Red'])
        
class Coupe(Vehicle):
    def __init__(self, lvlMgr,tileY, direction = 2):
        Vehicle.__init__(self, lvlMgr,tileY, 65, 32, 90, direction, Color['Green'])
        
class Log(Vehicle):
    def __init__(self, lvlMgr, tileY, width, speed, direction):
        self.levelManager = lvlMgr
        self.position = Vec(0,0)
        if direction == Direction['Left']:
            self.position.x = lvlMgr.getMapSize().x * lvlMgr.getTileSize().x
        else:
            self.position.x = 0 - width
        self.position.y = lvlMgr.getTileSize().y * tileY
        self.tileY = tileY
        self.size = Vec(width, lvlMgr.getTileSize().y - 2)
        self.speed = speed
        self.direction = direction
        self.color = Color['Brown']

    def playerCollided(self, player):
        player.hitLog(self)
        
    def getSpeed(self):
        return self.speed * (self.direction - 1)

    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.position.x, self.position.y + (self.levelManager.getTileSize().y - self.size.y) / 2, self.size.x, self.size.y - (self.levelManager.getTileSize().y - self.size.y) /2))


#Animal Entities
class Snake(Vehicle):
    def __init__(self, lvlMgr, tileY, speed, direction):
        Vehicle.__init__(self,lvlMgr, tileY, 60, 6, speed, direction, Color['Green'])
        self.segments = []
        self.segmentAmount = math.floor(self.size.x / 15)
        self.offset = 0
        self.frameChangeTime = 0.5
        self.frameTime = 0
        self.position.y += lvlMgr.getTileSize().y / 2
        for i in range(0, self.segmentAmount):
            self.segments.append(pygame.Rect(self.position.x, self.position.y, 15, 6))
        
    def update(self, dT):
        Vehicle.update(self, dT)
        self.frameTime += dT
        for i in range(0, self.segmentAmount):
            self.segments[i].left = self.position.x + (i * 15)
        if self.frameTime >= self.frameChangeTime:
            self.frameTime = 0
            for i in range(0, self.segmentAmount):
                if (i + self.offset) % 2 == 0:
                    self.segments[i].top = self.position.y - 2
                else:
                    self.segments[i].top = self.position.y + 2
            if self.offset == 1:
                self.offset = 0
            else:
                self.offset = 1
        
            
    def draw(self, renderTarget):
        for seg in self.segments:
            pygame.draw.rect(renderTarget, self.color, seg)
            
class Turtle(Vehicle):
    State = {'Floating' : 0, 'Submerging' : 1, 'Submerged' : 2,
             'Surfacing' : 3}
    def __init__(self, lvlMgr, tileY, tileWidth, speed, direction, timings = None):
        Vehicle.__init__(self, lvlMgr, tileY, tileWidth * lvlMgr.getTileSize().x, lvlMgr.getTileSize().y, speed, direction, Color['LightGreen'])
        self.tileWidth = tileWidth
        self.playerOn = False
        self.timer = 0
        self.state = Turtle.State['Floating']
        if timings == None:
            timings = (3,2,1,1)
        self.floatLength = timings[0]
        self.submergingLength = timings[1]
        self.submergedLength = timings[2]
        self.surfacingLength = timings[3]
        self.player = None
        
    def getSpeed(self):
        return self.speed * (self.direction - 1)
        
    def update(self, dT):
        Vehicle.update(self, dT)
        self.timer += dT
        if self.state == Turtle.State['Floating']:
            if self.timer >= self.floatLength:
                self.state = Turtle.State['Submerging']
                self.timer = 0
        if self.state == Turtle.State['Submerging']:
            if self.timer >= self.submergingLength:
                self.state = Turtle.State['Submerged']
                self.timer = 0
        if self.state == Turtle.State['Submerged']:
            if self.timer >= self.submergedLength:
                self.state = Turtle.State['Surfacing']
                self.timer = 0
        if self.state == Turtle.State['Surfacing']:
            if self.timer >= self.surfacingLength:
                self.state = Turtle.State['Floating']
                self.timer = 0
                
        if self.player != None:
            if self.player.onLog != self:
                self.playerOn = False
            else:
                if self.state == Turtle.State['Submerged']:
                    self.player = None
                    self.levelManager.playerKilled()
                
    def playerCollided(self, player):
        player.hitLog(self)
        self.player = player
        
    def draw(self, renderTarget):
        for i in range(0, self.tileWidth):
            if self.state == Turtle.State['Floating']:
                pygame.draw.ellipse(renderTarget, self.color, pygame.Rect(self.position.x + i * self.levelManager.getTileSize().x, self.position.y, self.levelManager.getTileSize().x, self.levelManager.getTileSize().y))
            elif self.state == Turtle.State['Submerging'] or self.state == Turtle.State['Surfacing']:
                pygame.draw.ellipse(renderTarget, self.color, pygame.Rect(self.position.x + i * self.levelManager.getTileSize().x + self.levelManager.getTileSize().x / 4, self.position.y + self.levelManager.getTileSize().y/4, self.levelManager.getTileSize().x/2, self.levelManager.getTileSize().y/2))
                