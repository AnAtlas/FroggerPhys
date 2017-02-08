# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:47:17 2017

@author: Student
"""

import pygame
import pdb
import math
from Utilities import Vec
from Utilities import Color
from Player import Player
from Levels import *

class LevelManager:
    
    entities = []
    entityId = 0
    windowWidth = 440
    windowHeight = 600
    tileSize = Vec(40,40)
    mapSize = Vec(11,15)
    levelAmount = 5
    background = pygame.Surface((windowWidth, windowHeight))
    entitySurface = pygame.Surface((windowWidth, windowHeight), pygame.SRCALPHA)
    goalsMade = 0
    goToNextLevel = False
    player = None
    loadedLevel = None
    playerLives = 5
    playerMarkedForDeath = False
    
    def __init__(self):
        self.myfont = pygame.font.SysFont("",24)
        
    def playerKilled(self):
        self.playerMarkedForDeath = True
            
    def spawnPlayer(self, spawnPoint):
        self.player = Player(self, spawnPoint)
        self.entities.append(self.player)
        
    def loadLevel(self, level):
        self.entities = []
        self.level = level
        if level == 1:
            self.loadedLevel = Level1(self)
        elif level == 2:
            self.loadedLevel = Level2(self)
        elif level == 3:
            self.loadedLevel = Level3(self)
        elif level == 4:
            self.loadedLevel = Level4(self)
        elif level == 5:
            self.loadedLevel = Level5(self)
        self.setupBackground()
        self.spawnPlayer(self.loadedLevel.spawnPoint)
        self.mapSize = Vec(self.loadedLevel.mapSize.x, self.loadedLevel.mapSize.y)
            
    def addEntity(self, ent):
        self.entities.append(ent)
        
    def removeEntity(self, ent):
        self.entities.remove(ent)
                
    def goalMade(self):
        self.goalsMade += 1
        if self.goalsMade >= self.loadedLevel.goalAmount:
            self.goToNextLevel = True
        
    def update(self, dT):
        if self.loadedLevel == None:
            return
        self.loadedLevel.update(dT)
        for ent in self.entities:
            ent.update(dT)
        self.checkCollisions()
        
        if self.playerMarkedForDeath :
            self.entities.remove(self.player)
            self.player = None
            self.playerLives-=1
            self.playerMarkedForDeath = False
            if self.playerLives > 0:
                self.spawnPlayer(self.loadedLevel.spawnPoint)
                
        if self.goToNextLevel:
            self.goalsMade = 0
            self.goToNextLevel = 0
            self.level += 1
            if self.level > self.levelAmount:
                self.level = self.level #PUT GAME OVER CODE HERE
            else:
                self.loadLevel(self.level)
                
    def draw(self, renderTarget):
        renderTarget.blit(self.background, (0,0))
        self.entitySurface = pygame.transform.scale(self.entitySurface, (self.loadedLevel.mapSize.x * self.tileSize.x, self.loadedLevel.mapSize.y * self.tileSize.y))
        self.entitySurface.fill((0,0,0,0))
        if self.player != None:
            self.entities.remove(self.player)
            self.entities.append(self.player)
        for ent in self.entities:
            ent.draw(self.entitySurface)
        self.entitySurface = pygame.transform.scale(self.entitySurface, (self.windowWidth, self.windowHeight))
        renderTarget.blit(self.entitySurface, (0,0))
        ren = self.myfont.render(str(len(self.entities)), 0, Color['White'])
        renderTarget.blit(ren, (20,20))
        pygame.display.flip()
        
    def checkCollisions(self):
        for ent in self.entities:
            if ent == self.player:
                continue
            if self.checkCollision(self.player, ent):
                ent.playerCollided(self.player)
                
                
    def checkCollision(self, obj1, obj2):
        if obj1 == None or obj2 == None:
            return False
        if obj2.x + obj2.width - 4 < obj1.x:
            return False
        if obj2.x > obj1.x + obj1.width - 4:
            return False
        if obj2.y + obj2.height - 4 < obj1.y:
            return False
        if obj2.y + 4 > obj1.y + obj1.height:
            return False
        return True
        
    def isOutsideWindow(self, ent):
        if ent.x >= self.mapSize.x * self.tileSize.x:
            return True
        if ent.y >= self.mapSize.y * self.tileSize.y:
            return True
        if ent.x + ent.width <= 0:
            return True
        if ent.y + ent.height <= 0:
            return True
        return False
        
    def getMapSize(self):
        return self.mapSize
        
    def getTileSize(self):
        return self.tileSize
        
    def setWindowSize(self, width, height):
        self.windowWidth = width
        self.windowHeight = height
        self.background = pygame.transform.scale(self.background, (self.windowWidth, self.windowHeight))
        self.entitySurface = pygame.transform.scale(self.entitySurface, (self.windowWidth, self.windowHeight))
        
    def setupBackground(self):
        #Setup background
        self.background.fill(Color['Black'])
        pygame.draw.rect(self.background, Color['DarkGray'], pygame.Rect(0, 0, self.tileSize.x * self.mapSize.x, self.tileSize.y * 2))
        pygame.draw.rect(self.background, Color['DarkGray'], pygame.Rect(0, self.tileSize.y * 2 + self.tileSize.y * self.loadedLevel.waterSize, self.tileSize.x * self.mapSize.x, self.tileSize.y))
        pygame.draw.rect(self.background, Color['LightGray'], pygame.Rect(0, self.tileSize.y * 2 + self.tileSize.y * self.loadedLevel.waterSize + self.tileSize.y, self.tileSize.x * self.mapSize.x, self.tileSize.y * self.loadedLevel.roadSize))
        pygame.draw.rect(self.background, Color['Brown'], pygame.Rect(0, self.tileSize.y * 13, self.tileSize.x * self.mapSize.x, self.tileSize.y * 2))
        
        #setup paint on road
        roadStartY = (3 + self.loadedLevel.waterSize) * self.tileSize.y
        roadWidth = self.loadedLevel.roadSize * self.tileSize.y
        height = roadStartY
        for row in range(0, self.loadedLevel.roadSize - 1):
            height += roadWidth / self.loadedLevel.roadSize
            if row == math.floor(self.loadedLevel.roadSize / 2):
                pygame.draw.rect(self.background, Color['Yellow'], pygame.Rect(0, height - 6, self.windowWidth, 4))
                pygame.draw.rect(self.background, Color['Yellow'], pygame.Rect(0, height + 2, self.windowWidth, 4))
            else:
                for x in range(0, 11):
                    pygame.draw.rect(self.background, Color['Yellow'], pygame.Rect(20 + 65 * x, height - 2, 35, 4))