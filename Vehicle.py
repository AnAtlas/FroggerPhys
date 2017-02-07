# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:14:39 2017

@author: Derek
"""
import pygame
import pdb
from Utilities import Direction

#define Colors
Color = { 'Black' : (0,0,0), 'White' : (255,255,255), 
         'Red' : (255,0,0), 'DarkGray' : (61,60,46),
         'Blue' : (0,0,255), 'LightGray' : (132,131,111),
         'Brown' : (164,121,35), 'Yellow' : (255,255,40),
         'Green' : (0,255,0)}


class Vehicle:
    def __init__(self, lvlMgr, tileY, width, height, speed, direction, color):
        self.levelManager = lvlMgr
        self.x = 0
        self.y = 0
        
        if direction == Direction['Left']:
            self.x = lvlMgr.getMapSize().x * lvlMgr.getTileSize().x - 1
        else:
            self.x = 0 - width + 1
        self.y = lvlMgr.getTileSize().y * tileY
        self.tileY = tileY
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.color = color
        
    def playerCollided(self, player):
        self.levelManager.playerKilled()
        
    def update(self, dT):
        self.x += (self.speed * (self.direction - 1)) * dT
        if self.levelManager.isOutsideWindow(self):
            self.levelManager.removeEntity(self)
        
    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.x, self.y + (self.levelManager.getTileSize().y - self.height) / 2, self.width, self.height - (self.levelManager.getTileSize().y - self.height) /2))
        
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
        self.x = 0
        self.y = 0
        if direction == Direction['Left']:
            self.x = lvlMgr.getMapSize().x * lvlMgr.getTileSize().x
        else:
            self.x = 0 - width
        self.y = lvlMgr.getTileSize().y * tileY
        self.tileY = tileY
        self.width = width
        self.height = 38
        self.speed = speed
        self.direction = direction
        self.color = Color['Brown']

    def playerCollided(self, player):
        player.hitLog(self)
        
    def getSpeed(self):
        return self.speed * (self.direction - 1)

    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.x, self.y + (self.levelManager.getTileSize().y - self.height) / 2, self.width, self.height - (self.levelManager.getTileSize().y - self.height) /2))