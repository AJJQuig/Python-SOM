'''
Created on Oct 25, 2016

@author: Alan Quigley
'''
from node import node
from random import randint
import math
from math import log

class Map:
    '''
    The Map class contains a list of all the nodes and handles training
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.constStartLearningRate = 0.1
        #Height and width of the cells when represented in 2d
        self.m_CellWidth = 0
        self.m_CellHeight = 0
        
        #holds the address of the winning node in the current iteration
        self.m_WinningNode = 0 
        
        #keeps track of what iteration the Train method is on
        self.m_IterationCount = 1
        self.m_NumIterations = 0
        
        #used to calculate the neighbourhood influence
        self.m_TimeConstant = 0
        
        #topological radius of the map
        self.m_MapRadius = 0 
        
        #current width of the winning nodes neighbourhood influence
        self.m_NeighbourhoodRadius = 0
        
        #area of influence and how much the learning rate of nodes within 
        #the influence radius are adjusted
        self.m_LearningRate = 0
        self.m_Influence = 0
        
        #set to true when training is finished
        self.m_Done = False
     
     
        
    def Create(self,xClient,yClient,nodesUp,nodesAcross,numIterations):
        '''
        Creates all the nodes for the map
        '''
        self.m_NumIterations = numIterations
        #Calc the cell width and height
        self.m_CellHeight = yClient / nodesUp
        self.m_CellWidth = xClient / nodesAcross
        
        #Contains all the nodes
        self.m_NodesList = []
        for y in xrange(nodesUp):
            for x in xrange(nodesAcross):
                #Create a node and append it to the list of nodes
                Node = node(x*self.m_CellWidth,(x+1)*self.m_CellWidth,y*self.m_CellHeight,(y+1)*self.m_CellHeight,self.m_CellWidth,self.m_CellHeight,3)
                self.m_NodesList.append(Node)
                
            
        self.m_MapRadius = max(xClient,yClient)
        self.m_TimeConstant = self.m_NumIterations/log(self.m_MapRadius)        
        return;
    
    
    
    def findBestMatchingNode(self, trainingNode):
        '''
        Finds the euclidean distance of nodes and trainingNode choosing the closest one as the winner
        '''
        
        #Set the lowest distance to a high value at the start
        self.m_LowestDistance = 999999
        #calculate the euclidean distance of each node in the map with the chosen training data   
        for x in xrange(len(self.m_NodesList)):
            self.m_Distance = self.m_NodesList[x].calculateDistance(trainingNode)
            
            if self.m_Distance < self.m_LowestDistance:
                self.m_LowestDistance = self.m_Distance
                self.m_Winner = self.m_NodesList[x]
        return self.m_Winner;
    
    
    
    def Render(self, screen): 
        #Render each node
        for x in xrange(len(self.m_NodesList)):
            self.m_NodesList[x].render(screen)
        return;
    
    
    
    def Organise(self, data):
        print "Organising"
        
        #check the weight of the training node matches the amount of weights a node has
        if len(data[0]) != 3:
            print "Training node weight size is incorrect"
            return False
        
        #Check if training has already been complete
        if self.m_Done == True:
            return True
        
        #Enter the training loop
        for x in xrange(self.m_NumIterations):
            print "Training: ",x+1,"/",self.m_NumIterations
            
            #Introduce the trainingNodes form the list at random
            self.trainingNodeNum = randint(0,len(data)-1)
            
            #present the randomly chosen trainingNode to each node and get the BMN
            self.m_WinningNode = self.findBestMatchingNode(data[self.trainingNodeNum])
            
            #Calculate the width of the neighourhood
            self.m_NeighbourhoodRadius = self.m_MapRadius * math.exp(- float(self.m_IterationCount)/self.m_TimeConstant)
            
            #Calculate the euclidean distance of the winning node and every node in the map
            for y in xrange(len(self.m_NodesList)):
                self.m_distToNodeSq = ((self.m_WinningNode.X() - self.m_NodesList[y].X()) *
                                       (self.m_WinningNode.X() - self.m_NodesList[y].X()) +
                                       (self.m_WinningNode.Y() - self.m_NodesList[y].Y()) *
                                       (self.m_WinningNode.Y() - self.m_NodesList[y].Y()))
                
                self.m_WidthSq = self.m_NeighbourhoodRadius * self.m_NeighbourhoodRadius
                
                #Check if the node is within the radius
                if self.m_distToNodeSq < self.m_WidthSq:
                    #Calculate how much the weights are adjusted
                    try:
                        self.m_Influence = math.exp(-float(self.m_distToNodeSq)/(2*self.m_WidthSq))
                    except OverflowError:
                        self.m_Influence = 0.0001
                    self.m_NodesList[y].adjustWeights(data[self.trainingNodeNum],self.m_LearningRate,self.m_Influence)
                
            
            #reduce the learning rate
            self.m_LearningRate = self.constStartLearningRate * math.exp(- float(self.m_IterationCount)/self.m_NumIterations) 
            self.m_IterationCount = self.m_IterationCount + 1   
        self.m_Done = True
        print "Finished Organizing"                     
        return True;
    
    
    def finishedTraining(self):
        return self.m_Done
    
    def getNodes(self):
        return self.m_NodesList
        
            
     
