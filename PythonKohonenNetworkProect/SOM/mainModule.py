'''
Created on Oct 25, 2016

@author: Alan Quigley
'''
import pygame
from SOM_Controller import SOM_Controller
#Initialize pygame and create the display screen
pygame.init()
screenX = 500
screenY = 500
screen = pygame.display.set_mode((screenX,screenY))
#set the caption for the screen
pygame.display.set_caption("Self Organizing Map")

#set how many nodes are on the X and Y axis aswell as the iterations to be done
nodesOnY = 50
nodesOnX = 50
totalIters = 500

#Create the controller and subsequently the whole map then render it
controller = SOM_Controller(screenX,screenY,nodesOnY,nodesOnX,totalIters)
controller.Render(screen)

#loop until the user clicks the close button
done = False
clock = pygame.time.Clock()
        
while not done:
    clock.tick(10)
    
    #Check if the user clicked close and set the program to be done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    
    #IF the training hasnt been done already then train the map 
    if controller.Finished() == False:
        if controller.train() == False:
            done = True #There's an error
    
    
    #render the completed map and update the display
    controller.Render(screen)    
    pygame.display.update()
