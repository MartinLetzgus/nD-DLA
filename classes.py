# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 08:28:28 2020

@author: marti
"""
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d
from itertools import product, combinations

class Grid():
    def __init__(self,dim,size,array=0):
        self.dim = dim #can only be 2 in the V1
        self.size = size
        self.array = np.zeros([size]*dim)
        
    class iterCells():
        #This iterator returns the coordinates of each cell of the grid
        def __init__(self, dim, size, start=0):
            self.num = start
            self.dim = dim
            self.size = size
            coord = ()
            n = self.num
            for d in range (dim):
                coord = coord + (int(n%size),)
                n = n - n%size
                n = n/size
            self.coord = coord
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self.num<self.size**self.dim:
                c = self.coord
                self.num += 1
                coord = ()
                n = self.num
                for d in range (self.dim):
                    coord = coord + (int(n%self.size),)
                    n = n - n%self.size
                    n = n/self.size
                self.coord = coord
                return c
            else:
                raise StopIteration
                      
    class iterNeighbours():
    #This iterator allows us to look for each neighboor of a cell
        def __init__(self, dim, size, tuple_coord, start =0):
            self.center = tuple_coord
            self.dim = dim
            self.size = size
            self.num = start
            self.coord = tuple([i-1 if (i-1>=0) else i for i in tuple_coord])
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self.num<3**self.dim:
                coord = ()
                c = self.coord
                while(len(coord)!=len(self.coord)or(coord==self.center)):
                    self.num += 1
                    coord = ()
                    n = self.num
                    for d in range (self.dim):
                        if ((self.center[d] + (n%3)-1>=0) and (self.center[d] + (n%3)-1 < self.size)):
                            coord = coord + (int(self.center[d] + (n%3)-1),)
                        else:
                            break
                        n = n - n%3
                        n = n/3
                self.coord = coord
                return c
            else:
                raise StopIteration
        
    def createCircle(self):
        rayon = self.size/2-1
        for coord in iter(self.iterCells(self.dim,self.size)):
            distance_from_centre = 0
            for c in (coord):
                distance_from_centre += (c+0.5-(self.size/2))**2
            if distance_from_centre >= rayon**2:
                self.array[coord] = -2
    
    def initRandom(self,x):
        for coord in iter(self.iterCells(self.dim,self.size)):
            if(random.random()<=x and self.array[coord]==0):
                self.array[coord]=1
                
    def customStart(self,list_of_points):
        for coord in list_of_points:
            assert(len(coord)==self.dim)
            self.array[coord]=-1
        
                
    def addRandomPoints(self,n):
        for i in range (n):
            ok = False
            while(ok==False):
                coord = ()
                for i in range (self.dim):
                    coord = coord + (random.randint(0,self.size),)
                if self.array[coord]>=0:
                    self.array[coord] += 1
                    ok=True
                    
    def countPoints(self):
        total = 0
        for coord in iter(self.iterCells(self.dim,self.size)):
            if self.array[coord]>0:
                total+=self.array[coord]
        return total
    
    def check_neighbours(self,coord):
        assert(len(coord)==self.dim)
        for coord_neigh in iter(self.iterNeighbours(self.dim,self.size,coord)):
            if(self.array[coord_neigh]<0):
                return True
        return False 

    def nextStep(self):        
        new_array = np.copy(self.array)
        for coord in iter(self.iterCells(self.dim,self.size)):
            if self.array[coord]>=1:
                if(self.check_neighbours(coord)):
                    new_array[coord]=-1
                else:
                    for i in range (int(self.array[coord])):
                        new_coord = ()
                        for d in range(self.dim):
                            new_coord = new_coord + (np.clip(coord[d] + random.randint(-1,2),0,self.size-1),)
                        new_array[coord] -= 1
                        new_array[new_coord] += 1
        self.array = new_array
                    
    def clean(self):
        self.array = np.zeros([self.size]*self.dim)
        
    def save2D(self, colorz, name_of_file):
        assert(self.dim==2)
        cmap = mpl.colors.ListedColormap(colorz)
        plt.imsave(name_of_file,self.array, cmap=cmap,vmax=1,vmin=-2)
        plt.clf()
        
    def save3D(self,colorz,name_of_file,angle):
        assert(self.dim==3)
        fig = plt.figure()
        ax = plt.axes(projection='3d')    
        ax.set_xlim(0,self.size+1)
        ax.set_ylim(0,self.size+1)
        ax.set_zlim(0,self.size+1)
        ax.set_axis_off()
        for x in range (self.size):
            for y in range (self.size):
                for z in range (self.size):
                    if (self.array[x,y,z]!=0 and self.array[x,y,z]!=-2): 
                        color = colorz(self.array[x,y,z])
                        r = [-0.5,0.5]
                        X, Y = np.meshgrid(r, r)
                        ax.plot_surface(X+x+0.5,Y+y+0.5,np.atleast_2d(0.5)+z+0.5, alpha=0.5, color=color)
                        ax.plot_surface(X+x+0.5,Y+y+0.5,np.atleast_2d(-0.5)+z+0.5, alpha=0.5, color=color)
                        ax.plot_surface(X+x+0.5,np.atleast_2d(-0.5)+y+0.5,Y+z+0.5, alpha=0.5, color=color)
                        ax.plot_surface(X+x+0.5,np.atleast_2d(0.5)+y+0.5,Y+z+0.5, alpha=0.5, color=color)
                        ax.plot_surface(np.atleast_2d(0.5)+x+0.5,X+y+0.5,Y+z+0.5, alpha=0.5, color=color)
                        ax.plot_surface(np.atleast_2d(-0.5)+x+0.5,X+y+0.5,Y+z+0.5, alpha=0.5, color=color)
        ax.view_init(elev=10., azim=angle)
        plt.savefig(str(name_of_file))
        plt.clf()               