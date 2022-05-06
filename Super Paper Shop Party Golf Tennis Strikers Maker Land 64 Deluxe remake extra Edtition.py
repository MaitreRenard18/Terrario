#Imports
import pygame
import os

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Shop Ultimate HD Deluxe Definitive Edition')

#Textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Textures\{}".format(os.getcwd(), file)
        image = pygame.image.load(path)

        textures[file_name] = image

        print(textures)

#Display & Variables
def affichage():
    screen.blit(textures["background"], (0,0))
    screen.blit(textures["shop"], (348,50))
pygame.display.flip()

gold = 80
fuel_capacity = 10
speed = 0.30

#Interactions
class Bouton:
    def __init__(self, image, pos, price):
        self.image = image
        self.pos = pos
        self.price = price

    def click(self):
        global running
        global speed
        global fuel_capacity
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if self.image == textures["exit"]:
                    running = False
                elif self.pos[0] == 393:
                    speed += 0.05
                    self.price += 20
                elif self.pos[0] == 777:
                    fuel_capacity += 2
                    self.price += 20
                elif self.pos[0] == 1161:
                    print("owo")
                    
    def animation(self):
        screen.blit(self.image, (self.pos[0], self.pos[1]))

boutons = [Bouton(textures["buy"], [393, 825], 20), Bouton(textures["buy"], [777, 825], 20), Bouton(textures["buy"], [1161, 825], 20), Bouton(textures["exit"], [823, 906], 0)]

#Game loop
running = True
while running:
    pygame.display.flip()

    mouse = pygame.mouse.get_pos()
    if 393<mouse[0]<393 + 365 and 825<mouse[1]<825 + 76:
        boutons[0].animation()
        boutons[0].click()
    elif 777<mouse[0]<777 + 365 and 820<mouse[1]<820 + 76:
        boutons[1].animation()
        boutons[1].click()
    elif 1161<mouse[0]<1161 + 365 and 825<mouse[1]<825 + 76:
        boutons[2].animation()
        boutons[2].click()
    elif 823<mouse[0]<823 + 273 and 906<mouse[1]<906 + 68:
        boutons[3].animation()
        boutons[3].click()
    else:
        affichage()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
