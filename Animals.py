# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 17:23:53 2017

@author: Student
"""
import pygame
import math
import pdb
from copy import deepcopy
from Vehicle import Vehicle
from Utilities import Color

class Snake(Vehicle):
    def __init__(self, lvlMgr, tileY, speed, direction):
        Vehicle.__init__(self,lvlMgr, tileY, 60, 6, speed, direction, Color['Green'])
        self.segments = []
        self.segmentAmount = math.floor(self.width / 15)
        self.offset = 0
        self.frameChangeTime = 0.5
        self.frameTime = 0
        self.y += lvlMgr.getTileSize().y / 2
        for i in range(0, self.segmentAmount):
            self.segments.append(pygame.Rect(self.x, self.y, 15, 6))
        
    def update(self, dT):
        Vehicle.update(self, dT)
        self.frameTime += dT
        for i in range(0, self.segmentAmount):
            self.segments[i].left = self.x + (i * 15)
        if self.frameTime >= self.frameChangeTime:
            self.frameTime = 0
            for i in range(0, self.segmentAmount):
                if (i + self.offset) % 2 == 0:
                    self.segments[i].top = self.y - 2
                else:
                    self.segments[i].top = self.y + 2
            if self.offset == 1:
                self.offset = 0
            else:
                self.offset = 1
        
            
    def draw(self, renderTarget):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_g]:
            pdb.set_trace()
        for seg in self.segments:
            pygame.draw.rect(renderTarget, self.color, seg)