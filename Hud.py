# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:46:25 2017

@author: Student
"""
import pygame
from Utilities import Color

class Hud:
    def __init__(self, lvlMgr):
        self.levelManager = lvlMgr
        self.myfont = pygame.font.SysFont("",24)
        self.mode = 'Game'
        
    def update(self, dT):
        a = 3
        
    def draw(self, renderTarget):
        if self.mode == 'Game':
            ren = self.myfont.render("Score: " + str(self.levelManager.score), 0, Color['White'])
            ren2 = self.myfont.render("Lives:", 0, Color['White'])
            renderTarget.blit(ren, (10,(self.levelManager.getMapSize().y - 1) * (self.levelManager.getTileSize().y)))
            renderTarget.blit(ren2, (100, (self.levelManager.getMapSize().y - 1) * (self.levelManager.getTileSize().y)))
            for i in range(0, self.levelManager.playerLives):
                pygame.draw.circle(renderTarget, Color['Green'], (154 + 12 * i,(self.levelManager.getMapSize().y - 1) * (self.levelManager.getTileSize().y) + 9) , 5)
        elif self.mode == 'GameWon':
            ren = self.myfont.render("Game Won!!!!", 0, Color['White'])
            renderTarget.blit(ren, (10,(self.levelManager.getMapSize().y - 1) * (self.levelManager.getTileSize().y)))
        elif self.mode == 'GameOver':
            ren = self.myfont.render("Game Over!!!", 0, Color['White'])
            renderTarget.blit(ren, (10,(self.levelManager.getMapSize().y - 1) * (self.levelManager.getTileSize().y)))
    def setMode(self, m):
        self.mode = m