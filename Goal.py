# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 11:40:12 2017

@author: Student
"""
import pygame
from Utilities import Color

class Goal:
    
    def __init__(self, lvlMgr, width, x):
        self.levelManager = lvlMgr
        self.width = width
        self.height = lvlMgr.getTileSize().y
        self.x = x
        self.y = lvlMgr.getTileSize().y
        self.empty = True
        self.color = Color['Black']

    def update(self, dT):
        self.x = self.x
        
    def playerCollided(self, player):
        if self.empty:
            self.levelManager.goalMade()
            self.empty = False
        else:
            self.levelManager.playerKilled()
            
    def draw(self, renderTarget):
        pygame.draw.rect(renderTarget, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        if not self.empty:
            pygame.draw.rect(renderTarget, Color['Green'], pygame.Rect(self.x + self.width / 4, self.y + self.height / 4, self.width / 2, self.height / 2))