# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 08:48:45 2020

@author: marti
"""

from classes import *
from numpy import random
import matplotlib.pyplot as plt
import matplotlib as mpl

colors = ['white','red', 'black', 'yellow']

def colorz(x):
    if x==-1:
        return('red')
    else:
        return('yellow')

def play(grid,max_steps=1000,save_pictures=True,output_path='',angle_between_steps=6,frames_by_step=2):
    alive = grid.countPoints()
    print(alive)
    liste = [alive]
    i=0
    angle = 0
    while(alive>0 and i<(max_steps)):
        if(save_pictures and grid.dim==3):
            for ii in range (frames_by_step):
                output_name = output_path+str(i)+"_"+str(ii)+'.png'
                grid.save3D(colorz,output_name,angle)
        elif(save_pictures and grid.dim==2):
            grid.save2D(colors,output_path+str(i)+'.png')
        grid.nextStep()
        alive = grid.countPoints()
        liste.append(alive)
        i+=1
        print(alive)