import pygame
import threading
from pygame.locals import *
pygame.init()

size = width, height = 1920, 1080

screen = pygame.display.set_mode(size)

images = {"bc": pygame.image.load("background.png"), "shop": pygame.image.load("shopUIredi.png"), "BUY": pygame.image.load("BUYanimredi.png"), "EXIT": pygame.image.load("EXITanimredi.png")}
screen.blit(images["bc"], (0,0))
screen.blit(images["shop"], (348,50))
pygame.display.flip()

class Bouton:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos

    def click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.pos[0]<event.pos[0]<self.pos[0] + self.image.get_width() and self.pos[1]<event.pos[1]<self.pos[1] + self.image.get_height():        
                    screen.blit(self.image, (self.pos[0], self.pos[1]))

    def animation(self):
        """for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:""" #ici c'était un test, mais c'est inutile car le "MOUSEMOTION" prend en compte uniquement le mouvement de souris et pas la position
        mouse = pygame.mouse.get_pos() #je prend la pos de la souris
        if self.pos[0]<mouse[0]<self.pos[0] + self.image.get_width() and self.pos[1]<mouse[1]<self.pos[1] + self.image.get_height():
            screen.blit(self.image, (self.pos[0], self.pos[1])) #si pos souris = pos bouton, j'affiche l'animation par dessus l'image de base
        else:
            screen.blit(images["shop"], (348,50)) #sinon j'affiche l'image de base, pour enlever d'autre animations qui ont potentiellement été chargé auparavant

anim = [Bouton(images["BUY"], [393, 825]), Bouton(images["BUY"], [777, 825]), Bouton(images["BUY"], [1161, 825]), Bouton(images["EXIT"], [823, 906])]
#^ ça c'est mon tableau qui content les positions des boutons, pour les animations

running = True
while running:
    for i in range(len(anim)): #du coup c'est ici que ça marche pas
        anim[i].animation() #ici j'appelle chaque animation de chaque bouton, en boucle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()