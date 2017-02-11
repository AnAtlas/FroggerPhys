# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:29:36 2017

@author: Student
"""

#Helper Vector class
class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other):
        return Vec(self.x * other, self.y * other)
        
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
        
#define Directions
Direction = {'Left' : 0, 'Up' : 1, 'Right' : 2, 'Down' : 3 }

#define Colors
Color = { 'Black' : (0,0,0), 'White' : (255,255,255), 
         'Red' : (255,0,0), 'DarkGray' : (61,60,46),
         'Blue' : (0,0,255), 'LightGray' : (132,131,111),
         'Brown' : (164,121,35), 'Yellow' : (255,255,40),
         'Green' : (0,255,0), 'LightGreen' : (137,255,0)}

Debugging = True