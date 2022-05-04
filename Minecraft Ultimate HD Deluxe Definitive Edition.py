from matplotlib.pyplot import text
import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((1024, 800))
pygame.display.set_caption('Minecraft Ultimate HD Deluxe Definitive Edition')

#Textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Textures\{}".format(os.getcwd(), file)
        image = pygame.image.load(path)

        textures[file_name] = image

#Carte
class map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = []

        self.generate()

    def generate(self):
        #Génère les deux premières couches
        self.tiles = [["grass" for _ in range(self.width)], ["dirt" for _ in range(self.width)]]
        
        #Génère le reste
        for y in range(2, self.height):
            if y < 4:
                self.tiles.append([random.choice(["dirt", "stone"]) for _ in range(self.width)])
            elif y < 8:
                self.tiles.append(["stone" for _ in range(self.width)])
            else:
                self.tiles.append([random.choice(["coal", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone"]) for _ in range(self.width)])

    def render(self):
        #Affiche le ciel
        screen.fill((145, 226, 255))

        #Affiche chaques tuiles
        for y in range(0, len(self.tiles)):
            for tile in range(0, len(self.tiles[y])):
                screen.blit(textures[self.tiles[y][tile]], (tile * 32, y * 32 + 8 * 32))

        pygame.display.flip()

#Joueur
class player:
    def __init__(self):
        self.position = (0, 0)


    
#Lance le jeu
level = map(32, 32)
level.render()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False