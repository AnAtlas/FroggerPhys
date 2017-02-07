# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 18:09:14 2017

@author: Student
"""

import pygame

from LevelManager import LevelManager

windowWidth = 440
windowHeight = 600

pygame.init()
screen = pygame.display.set_mode((windowWidth,windowHeight), pygame.RESIZABLE)
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

done = False

levelManager = LevelManager()
levelManager.loadLevel(1)
elapsedTime = 0

while not done:
    elapsedTime = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            windowWidth = event.dict['size'][0]
            windowHeight = event.dict['size'][1]
            levelManager.setWindowSize(windowWidth, windowHeight)
    levelManager.update(elapsedTime)
    levelManager.draw(screen) 
pygame.quit()


