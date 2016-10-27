'''
Created on Oct 25, 2016

@author: Alan Quigley
'''
from Map import Map
from random import randint
class SOM_Controller:
    '''
    Controller for the SOM
    '''
    def __init__(self,xClient, yClient, nodesUp, nodesAcross, numIterations):
        '''
        Constructor
        '''
        #Create the map and training data
        self.c_map = Map()
        self.c_map.Create(xClient, yClient, nodesUp, nodesAcross, numIterations)
        self.createDataSet()
    
    
    #begins the training of the system
    def train(self):
        if self.c_map.finishedTraining() == False:
            if self.c_map.Organise(self.c_trainingList) == False:
                return False
           
        return True
    
    
    #Creates the training data for the map          
    def createDataSet(self):
        #Create the training data, MUST HAVE SAME AMOUNT OF VALUES AS THE NODES WEIGHTS
        self.c_redTraining = [255,0,0]
        self.c_greenTraining = [0,255,0]
        self.c_blueTraining = [0,0,255]
        self.c_blackTraining = [0,0,0]
        self.c_yellowTraining = [255,255,0]
        self.c_purpleTraining = [255,0,255]
        self.c_cyanTraining = [0,255,255]
        self.c_whiteTraining = [255,255,255]
        
        #Add training data lists to c_trainingList
        self.c_trainingList = [self.c_redTraining,self.c_greenTraining,self.c_blueTraining,self.c_blackTraining,self.c_whiteTraining,self.c_yellowTraining,self.c_purpleTraining,self.c_cyanTraining]
        
        #Generate some random training data 
        for x in xrange(100):
            a_List = (randint(0,255),randint(0,255),randint(0,255))
            self.c_trainingList.append(a_List)
    
            
    def Render(self, screen):
        self.c_map.Render(screen)
    
        
    def Finished(self):
        return self.c_map.finishedTraining()