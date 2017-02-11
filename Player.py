# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 02:18:15 2017

@author: Student
"""
import pygame
import pdb
from Utilities import Vec
from Utilities import Color

class Player:

    def __init__(self, lvlMgr,tileXY):
        self.levelManager = lvlMgr
        self.position = Vec(tileXY.x * lvlMgr.getTileSize().x, tileXY.y * lvlMgr.getTileSize().y)
        self.jumpPosition = Vec(self.position.x, self.position.y)
        self.tilePosition = Vec(tileXY.x, tileXY.y)
        self.direction = 0
        self.prevPressed = [0,0,0,0]
        self.onLog = None
        self.size = Vec(40,40)
        self.jumpToTile = Vec(0,0)
        self.jumpFromTile = Vec(0,0)
        self.jumpDistance = lvlMgr.getTileSize().y
        self.jumpSpeed = 180
        self.jumping = False
        self.color = Color['Green']
        self.logRelativePosition = Vec(0,0)
        
    def update(self, dT):
        pressed = pygame.key.get_pressed()
        if self.levelManager.isOutsideWindow(self):
            self.levelManager.playerKilled()
        if pressed[pygame.K_f]:
            a = 3
            pdb.set_trace()
        if self.jumping:
            if self.direction == 0 or self.direction == 2:
                self.position.x = self.position.x + ((self.direction - 1) * self.jumpSpeed) * dT
                if not self.levelManager.checkCollision(self, self.onLog):
                    self.onLog = None
                if self.onLog == None:
                    if abs(self.position.x - self.jumpPosition.x) >= self.jumpDistance:
                        self.position.x = round(self.position.x)
                        self.jumping = False
                else:
                    self.position.x += self.onLog.getSpeed() * dT
                    if abs((self.position.x - self.onLog.position.x) - (self.logRelativePosition.x)) >= self.jumpDistance:
                        self.position.x = round(self.position.x)
                        self.jumping = False
                        
            if self.direction == 1 or self.direction == 3:
                self.position = self.position + ((self.jumpToTile - self.jumpFromTile) * self.jumpSpeed * dT)
                self.onLog = None
                if abs(self.position.y - self.jumpFromTile.y * 40) >= self.jumpDistance:
                    self.position.y = self.jumpToTile.y * 40
                    self.tilePosition = Vec(self.jumpToTile.x, self.jumpToTile.y)
                    self.jumping = False
            
        else:
            if self.onLog != None:
                self.position.x += self.onLog.getSpeed() * dT
                    
            if not pressed[pygame.K_a] and not pressed[pygame.K_w] and not pressed[pygame.K_d] and not pressed[pygame.K_s]:
                self.prevPressed = [0,0,0,0]
                return
            if pressed[pygame.K_a] and not self.prevPressed[0]:
                self.direction = 0
                self.jumpPosition = Vec(self.position.x, self.position.y)
                self.prevPressed[0] = 1
                self.jumping = True
                if self.onLog != None:
                    self.logRelativePosition = self.position - self.onLog.position

            if pressed[pygame.K_w] and not self.prevPressed[1]:
                self.direction = 1
                self.jumpToTile = self.tilePosition + Vec(0,-1)
                self.jumpFromTile = Vec(self.tilePosition.x, self.tilePosition.y)
                self.prevPressed[1] = 1
                self.jumping = True
            if pressed[pygame.K_d] and not self.prevPressed[2]:
                self.direction = 2
                self.jumpPosition = Vec(self.position.x, self.position.y)
                self.prevPressed[2] = 1
                self.jumping = True
                if self.onLog != None:
                    self.logRelativePosition = self.position - self.onLog.position
                    
            if pressed[pygame.K_s] and not self.prevPressed[3]:
                self.direction = 3
                self.jumpToTile = self.tilePosition + Vec(0,1)
                self.jumpFromTile = Vec(self.tilePosition.x, self.tilePosition.y)
                self.prevPressed[3] = 1
                self.jumping = True
            
            
                
                    
    def hitLog(self, log):
        self.onLog = log
        
    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.position.x + 4, self.position.y + 4, self.size.x - 8, self.size.y - 8))