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
from Utilities import Debugging
from Player import Player
from Levels import *
from Hud import Hud

class LevelManager:
    
    entities = []
    tileSize = Vec(40,40)
    mapSize = Vec(11,15)
    levelAmount = 5
    
    def __init__(self, window):
        self.myfont = pygame.font.SysFont("",24)
        self.hud = Hud(self)
        self.window = window
        self.windowWidth = 440
        self.windowHeight = 600
        self.background = pygame.Surface((self.windowWidth, self.windowHeight))
        self.entitySurface = pygame.Surface((self.windowWidth, self.windowHeight), pygame.SRCALPHA)
        self.hudSurface = pygame.Surface((self.windowWidth, self.windowHeight), pygame.SRCALPHA)
        self.gameOver = False
        self.gameWon = False
        self.playerLives = 5
        self.playerMarkedForDeath = False
        self.score = 0
        self.hasGirlfriend = 0
        self.loadedLevel = None
        self.player = None
        self.goToNextLevel = False
        self.goalsMade = 0
        
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
        self.setWindowSize(self.mapSize.x * self.tileSize.x, self.mapSize.y * self.tileSize.y)
        self.screen = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.RESIZABLE)
        self.hud.setMode('Game')
            
    def addEntity(self, ent):
        self.entities.append(ent)
        
    def removeEntity(self, ent):
        self.entities.remove(ent)
                
    def goalMade(self):
        self.score += 100
        self.goalsMade += 1
        if self.goalsMade >= self.loadedLevel.goalAmount:
            self.score += self.loadedLevel.goalAmount * 100
            self.goToNextLevel = True
        else:
            self.entities.remove(self.player)
            self.player = None
            self.spawnPlayer(self.loadedLevel.spawnPoint)
            
    def playerWon(self):
        self.gameWon = True
        self.hud.setMode('GameWon')
        
        
    def restartGame(self):
        self.gameOver = False
        self.gameWon = False
        self.playerLives = 5
        self.playerMarkedForDeath = False
        self.score = 0
        self.hasGirlfriend = 0
        self.loadedLevel = None
        self.player = None
        self.goToNextLevel = False
        self.goalsMade = 0
        self.loadLevel(1)
        
    def update(self, dT):
        if self.loadedLevel == None:
            return
        if self.gameWon:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                self.restartGame()
                
        if self.gameOver:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                self.restartGame()
                
        self.hud.update(dT)
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
            else:
                self.gameOver = True
                self.hud.setMode('GameOver')
                
        if self.goToNextLevel:
            self.goalsMade = 0
            self.goToNextLevel = 0
            self.level += 1
            if self.level > self.levelAmount:
                self.gameWon = True
                self.hud.setMode('GameWon')
            else:
                self.loadLevel(self.level)
                
    def draw(self, renderTarget):
        renderTarget.blit(self.background, (0,0))
        self.entitySurface = pygame.transform.scale(self.entitySurface, (self.loadedLevel.mapSize.x * self.tileSize.x, self.loadedLevel.mapSize.y * self.tileSize.y))
        self.entitySurface.fill((0,0,0,0))
        self.hudSurface = pygame.transform.scale(self.hudSurface, (self.loadedLevel.mapSize.x * self.tileSize.x, self.loadedLevel.mapSize.y * self.tileSize.y))
        self.hudSurface.fill((0,0,0,0))
        if self.player != None:
            self.entities.remove(self.player)
            self.entities.append(self.player)
        for ent in self.entities:
            ent.draw(self.entitySurface)
        self.entitySurface = pygame.transform.scale(self.entitySurface, (self.windowWidth, self.windowHeight))
        renderTarget.blit(self.entitySurface, (0,0))
        self.hud.draw(self.hudSurface)
        self.hudSurface = pygame.transform.scale(self.hudSurface, (self.windowWidth, self.windowHeight))
        renderTarget.blit(self.hudSurface, (0,0))
        if Debugging:
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
        if obj2.position.x + obj2.size.x - 4 < obj1.position.x:
            return False
        if obj2.position.x > obj1.position.x + obj1.size.x - 4:
            return False
        if obj2.position.y + obj2.size.y - 4 < obj1.position.y:
            return False
        if obj2.position.y + 4 > obj1.position.y + obj1.size.y:
            return False
        return True
        
    def isOutsideWindow(self, ent):
        if ent.position.x >= self.mapSize.x * self.tileSize.x:
            return True
        if ent.position.y >= self.mapSize.y * self.tileSize.y:
            return True
        if ent.position.x + ent.size.x <= 0:
            return True
        if ent.position.y + ent.size.y <= 0:
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
        self.hudSurface = pygame.transform.scale(self.hudSurface, (self.windowWidth, self.windowHeight))
        
    def setupBackground(self):
        #Setup background
        self.background.fill(Color['Black'])
        pygame.draw.rect(self.background, Color['DarkGray'], pygame.Rect(0, 0, self.tileSize.x * self.mapSize.x, self.tileSize.y * 2))
        pygame.draw.rect(self.background, Color['DarkGray'], pygame.Rect(0, self.tileSize.y * 2 + self.tileSize.y * self.loadedLevel.waterSize, self.tileSize.x * self.mapSize.x, self.tileSize.y))
        pygame.draw.rect(self.background, Color['LightGray'], pygame.Rect(0, self.tileSize.y * 2 + self.tileSize.y * self.loadedLevel.waterSize + self.tileSize.y, self.tileSize.x * self.mapSize.x, self.tileSize.y * self.loadedLevel.roadSize))
        pygame.draw.rect(self.background, Color['Brown'], pygame.Rect(0, self.tileSize.y * 13, self.tileSize.x * self.mapSize.x, self.tileSize.y * 2))
        
        if self.loadedLevel.roadSize <= 0:
            return
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