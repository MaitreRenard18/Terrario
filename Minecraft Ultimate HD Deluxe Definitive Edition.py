#Imports
from cgitb import text
from turtle import screensize, width
import pygame
import random
import os

#Initialization
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
        for x in range(self.width):
            self.tiles.append([])

            for y in range(self.height):
                match y:
                    case 0:
                        self.tiles[x].append("grass")
                    case 1:
                        self.tiles[x].append("dirt")
                    case y if y < 4:
                       self.tiles[x].append(random.choice(["dirt", "stone"]))
                    case y if y < 8:
                        self.tiles[x].append("stone")
                    case _:
                        choices = ["stone" for _ in range(12)]
                        choices.append("coal")

                        self.tiles[x].append(random.choice(choices))

    def render(self, offset):
        screen.fill((145, 226, 255))

        screensize = screen.get_size()
        x_tile_number = screensize[0] // 32 + (screensize[0] % 32 > 0)
        y_tile_number = screensize[1] // 32 + (screensize[1] % 32 > 0)

        for x in range(offset[0], offset[0] + x_tile_number):
            for y in range(offset[1], offset[1] + y_tile_number):
                x_index = None if x < 0 or x > self.width - 1 else x
                y_index = None if y < 0 or y > self.height - 1 else y
                
                if x_index != None and y_index != None:
                    texture = textures[self.tiles[x_index][y_index]]
                    screen.blit(texture, (x * 32 + -offset[0] * 32, y * 32 + -offset[1] * 32))

        pygame.display.flip()

#Joueur
class player:
    def __init__(self):
        self.position = (0, 0)
        self.speed = 1

        self.ticker = 0

    def tick(self):
        if self.ticker > 0:
            self.ticker -= 1
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.position = (self.position[0] + 1, self.position[1])
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_LEFT]:
            self.position = (self.position[0] - 1, self.position[1])
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_UP]:
            self.position = (self.position[0], self.position[1] - 1)
            self.ticker = 16 * (1 / self.speed)
            return

        if keys[pygame.K_DOWN]:
            self.position = (self.position[0], self.position[1] + 1)
            self.ticker = 16 * (1 / self.speed)
            return

#Game loop
level = map(512, 512)
drill = player()

running = True
while running:
    drill.tick()
    level.render(drill.position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False