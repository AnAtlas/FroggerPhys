# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:47:48 2017

@author: Student
"""
import pygame
from Utilities import Color
from Utilities import Debugging
from Utilities import Vec

class Zone:
    
    def __init__(self, lvlMgr, width, height, tileX, tileY):
        self.levelManager = lvlMgr
        self.position = Vec(tileX * self.levelManager.getTileSize().x, tileY * self.levelManager.getTileSize().y)
        self.size = Vec(width * self.levelManager.getTileSize().x, height * self.levelManager.getTileSize().y)
        self.color = Color['White']

    def update(self, dT):
        self.position.x = self.position.x
        
    def playerCollided(self, player):
        self.position.x = self.position.x
        
    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y))
        
class Goal(Zone):
    
    def __init__(self, lvlMgr, width, tileX):
        Zone.__init__(self,lvlMgr, width, 1, tileX, 1)
        self.empty = True
        self.color = Color['Black']
        
    def playerCollided(self, player):
        if self.empty:
            self.levelManager.goalMade()
            self.empty = False
        else:
            self.levelManager.playerKilled()
            
    def draw(self, renderTarget):
        Zone.draw(self,renderTarget)
        if not self.empty:
            pygame.draw.rect(renderTarget, Color['Green'], pygame.Rect(self.position.x + self.size.x / 4, self.position.y + self.size.y / 4, self.size.x / 2, self.size.y / 2))
            
class Water(Zone):
    def __init__(self, lvlMgr, width, height):
        Zone.__init__(self,lvlMgr, width, height, 0,2)
        self.color = Color['Blue']
        self.frameCount = 0
        
    def playerCollided(self, player):
        if player.onLog == None and player.jumping == False:
            self.frameCount += 1
            if self.frameCount >= 2:
                self.levelManager.playerKilled()
        else:
            self.frameCount = 0
            
class Wall(Zone):
    def __init__(self, lvlMgr, width, tileX):
        Zone.__init__(self, lvlMgr, width, 1, tileX, 1)
        
    def playerCollided(self, player):
        self.levelManager.playerKilled()
        
    def draw(self, renderTarget):
        if Debugging:
            Zone.draw(self,renderTarget)