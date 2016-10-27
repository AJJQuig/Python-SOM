'''
Created on Oct 25, 2016

@author: Alan Quigley
'''
from random import randint
import pygame
class node:
    '''
    node class for the SOM
    '''
    
    #topological 'radius' of the map
    n_MapRadius = 0;
   
    def __init__(self, lft, rgt,top,botm,nodeWidth,nodeHeight,numWeights):
        '''
        Constructor
        '''
        self.numWeights = numWeights
        #The edges of this nodes cell when rendering
        self.n_Left = lft
        self.n_Right = rgt
        self.n_Top = top
        self.n_Bottom = botm
        
        self.n_width = nodeWidth
        self.n_height = nodeHeight
        #The nodes coordinates within the map 
        self.n_X = self.n_Left + (self.n_Right - self.n_Left)/2 
        self.n_Y = self.n_Top + (self.n_Bottom - self.n_Top)/2
        
        #A list of the nodes values, randomly generated 
        self.n_Weights = []
        for x in xrange(numWeights):
            self.n_Weights.append(randint(0,255))
        
        #Check if the nodes weights equal what is expected
        if len(self.n_Weights) != numWeights:
            print "Error with nodes weights length"
         
    #get the euclidean distance between this nodes weights and the targetList
    def calculateDistance(self,targetList):
        self.distance = 0.0
        
        for x in xrange(len(self.n_Weights)):
            self.distance += (targetList[x] - self.n_Weights[x]) * (targetList[x] - self.n_Weights[x]) 
            
        return self.distance
    
        
    
    #adjust the nodes weights based on the target list and learning rate
    def adjustWeights(self, target, learningRate, influence):
        
        for x in xrange(self.numWeights):
            self.adjustedVal = self.n_Weights[x]
            self.adjustedVal += learningRate * influence * (target[x] - self.n_Weights[x])
            if self.adjustedVal < 0:
                self.adjustedVal = 0
            elif self.adjustedVal > 255:
                self.adjustedVal = 255
            self.n_Weights[x] = self.adjustedVal
        
        
    def render(self, screen):
        # Draw a solid rectangle
        self.colour = (int(self.n_Weights[0]),int(self.n_Weights[1]),int(self.n_Weights[2])) 
        pygame.draw.rect(screen, self.colour, [self.n_X, self.n_Y, self.n_width, self.n_height])
        pygame.display.update()
        return;
    
    
    def X(self):
        return self.n_X
    
    def Y(self):
        return self.n_Y
            