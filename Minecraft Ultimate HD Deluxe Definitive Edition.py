from operator import le
import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((1024, 832))
pygame.display.set_caption('Minecraft Ultimate HD Deluxe Definitive Edition')

#Textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Textures\{}".format(os.getcwd(), file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))

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

    def render(self, offset):
        #Affiche le ciel
        screen.fill((145, 226, 255))

        #Vérifie si le scrolling peux être effectué
        if -offset[0] < 0:
            offset = (0, offset[1])
        elif -offset[0] + 26 > self.width:
            offset = (-self.height + 1, offset[1])

        if offset[1] < 0:
            offset = (offset[0], 0)
        elif offset[1] + 32 > self.height:
            offset = (offset[0], self.width - 1)
            
        #Affiche chaques tuiles
        for y in range(-offset[0] , -offset[0] + 26):
            for tile in range(offset[1], offset[1] + 32):
                screen.blit(textures[self.tiles[y][tile]], (tile * 32 - offset[1] * 32, y * 32 + (offset[0] * 32)))

        pygame.display.flip()
        
        

#Joueur
class player:
    def __init__(self, level):
        self.position = (0, 0)
        self.speed = 1

        self.level = level

        self.ticker = 0

    def tick(self):
        if self.ticker > 0:
            self.ticker -= 1
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.position = (self.position[0], self.position[1] + 1)
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_LEFT]:
            self.position = (self.position[0], self.position[1] - 1)
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_UP] and self.position[0] + 1 <= 0:
            self.position = (self.position[0] + 1, self.position[1])
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_DOWN] and self.position[0] - 1 >= -level.height:
            self.position = (self.position[0] - 1, self.position[1])
            self.ticker = 16 * (1 / self.speed)
            return

#Lance le jeu
level = map(128, 128)
drill = player(level)

running = True
while running:
    drill.tick()
    level.render(drill.position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False