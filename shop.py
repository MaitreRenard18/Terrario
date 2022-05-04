import pygame
from pygame.locals import *
pygame.init()

size = width, height = 1920, 1080

screen = pygame.display.set_mode(size)

images = {"bc": pygame.image.load("background.png"), "shop": pygame.image.load("shopUIredi.png"), "BUY": pygame.image.load("BUYanimredi.png"), "EXIT": pygame.image.load("EXITanimredi.png")}
screen.blit(images["bc"], (0,0))
screen.blit(images["shop"], (348,50))
pygame.display.flip()

gold = 0

class Bouton:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos

    def click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()

    def animation(self):
        screen.blit(self.image, (self.pos[0], self.pos[1])) #si pos souris = pos bouton, j'affiche l'animation par dessus l'image de base

anim = [Bouton(images["BUY"], [393, 825]), Bouton(images["BUY"], [777, 825]), Bouton(images["BUY"], [1161, 825]), Bouton(images["EXIT"], [823, 906])]
#^ ça c'est mon tableau qui content les positions des boutons, pour les animations

running = True
while running:

    mouse = pygame.mouse.get_pos()
    if 393<mouse[0]<393 + 365 and 825<mouse[1]<825 + 76:
        anim[0].animation()
    elif 777<mouse[0]<777 + 365 and 825<mouse[1]<825 + 76:
        anim[1].animation()
    elif 1161<mouse[0]<1161 + 365 and 825<mouse[1]<825 + 76:
        anim[2].animation()
    elif 823<mouse[0]<823 + 273 and 825<mouse[1]<906 + 68:
        anim[3].animation() and anim[3].click()
    else:
        screen.blit(images["shop"], (348,50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
