# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 02:39:15 2017

@author: Student
"""

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