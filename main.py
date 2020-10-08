# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 00:57:44 2020

@author: marti
"""
from classes import *
from functions import play

dim = 2
size = 101
max_steps = 1000
output_path = 'pngs/2Dfromline'
        
grid = Grid(dim,size)

#Start with a circle :
#t.createCircle()

#Start with a point :
#grid.customStart([(50,50)])

#Start with a horizontal line :
grid.customStart([(50,x) for x in range (grid.size)])

#Choose how much points will be on the greed (between 0 and 1)
grid.initRandom(0.3)

play(grid,max_steps,True,output_path)