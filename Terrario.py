#Imports
from math import floor
import pygame
import random
import os

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1056, 832))
pygame.display.set_caption('Terrario')

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
        for x in range(self.width - 1):
            self.tiles.append([])

            for y in range(self.height):
                if y == 0:
                    self.tiles[x].append("air")
                elif y == 1:
                    self.tiles[x].append("grass")
                elif y == 2:
                    self.tiles[x].append("dirt")
                elif y == 3:
                    self.tiles[x].append(random.choice(["dirt", "dirt", "stone"]))
                elif y == 4:
                    self.tiles[x].append(random.choice(["dirt", "stone"]))
                elif y < 8:
                    self.tiles[x].append("stone")
                elif y < 12:
                    choices = ["stone" for _ in range(16)]
                    choices.append("coal")

                    self.tiles[x].append(random.choice(choices))
                elif y < 64:
                    choices = ["stone" for _ in range(32)]
                    choices.append("coal")
                    choices.append("coal")
                    choices.append("iron")

                    self.tiles[x].append(random.choice(choices))
                elif y < 256:
                    choices = ["stone" for _ in range(64)]
                    choices.append("iron")
                    choices.append("iron")
                    choices.append("gold")

                    self.tiles[x].append(random.choice(choices))
                elif y < 512:
                    choices = ["stone" for _ in range(128)]
                    choices.append("gold")
                    choices.append("gold")
                    choices.append("diamond")

                    self.tiles[x].append(random.choice(choices))
                elif y < 750:
                    choices = ["stone" for _ in range(128)]
                    choices.append("diamond")
                    choices.append("diamond")
                    choices.append("ruby")

                    self.tiles[x].append(random.choice(choices))
        
        for _ in range(750):
            max_size = random.randint(32, 64)
            self.dig((random.randint(0, self.width), random.randint(4, self.height)), max_size)

        for x in range(self.width - 1):
            self.tiles[x][0] = "air"
            self.tiles[x][-3] = random.choice(["stone", "bedrock"])
            self.tiles[x][-2] = random.choice(["stone", "bedrock", "bedrock"])
            self.tiles[x][-1] = "bedrock"

    def dig(self, position, max_size, size = 0):
        x = position[0]
        y = position[1]

        if size == max_size or x > len(self.tiles) - 1 or y > len(self.tiles[x]) - 1:
            return

        size += 1
        self.tiles[x][y] = "cave"

        choises = []
        if x + 1 < len(self.tiles) and self.tiles[x + 1][y] != "cave":
            choises.append((x + 1, y))

        if x - 1 >= 0 and self.tiles[x - 1][y] != "cave":
            choises.append((x - 1, y))

        if y + 1 < len(self.tiles[x]) and self.tiles[x][y + 1] != "cave":
            choises.append((x, y + 1))

        if y - 1 >= 0 and self.tiles[x][y - 1] != "cave":
            choises.append((x, y - 1))
        
        if len(choises) == 0:
            return

        node = [1 for _ in range(9)]
        node.append(2)
        node = random.choice(node)

        for _ in range(node):
            self.dig(random.choice(choises), max_size, size)

    def render(self, offset):
        screen.fill((145, 226, 255))

        screensize = screen.get_size()
        x_tile_number = screensize[0] // 32 + (screensize[0] % 32 > 0)
        y_tile_number = screensize[1] // 32 + (screensize[1] % 32 > 0)

        for x in range(offset[0], offset[0] + x_tile_number):
            for y in range(offset[1], offset[1] + y_tile_number):
                x_index = None if x < 0 or x > len(self.tiles) - 1 else x
                y_index = None if y < 0 or y > len(self.tiles[0]) - 1 else y
                
                if x_index != None and y_index != None:
                    texture = textures[self.tiles[x_index][y_index]]
                    screen.blit(pygame.transform.scale(texture, (32, 32)), (x * 32 - offset[0] * 32, y * 32 - offset[1] * 32))

#Joueur
class player:
    def __init__(self, map):
        self.position = (map.width // 2, 0)
        self.speed = 1
        
        self.map = map
        self.texture = "drill_base_right"

    def get_camera_offset(self):
        screensize = screen.get_size()
        x = floor(self.position[0]) - (screensize[0] // 32) // 2
        y = floor(self.position[1]) - (screensize[1] // 32) // 2

        return (x, y)

    def tick(self):
        screensize = screen.get_size()
        screen.blit(pygame.transform.scale(textures[self.texture], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2))

        x, y = floor(self.position[0]), floor(self.position[1])

        if self.map.tiles[x][y] != "scaffolding" and self.map.tiles[x][y] != "cave" and y != 0:
            self.map.tiles[x][y] = "cave"

        if self.map.tiles[x][y + 1] == "cave":
            screen.blit(pygame.transform.scale(textures["parachute"], (32, 32)), (screensize[0] // 2 - 16, screensize[1] // 2 - 32))
            self.position = (x, self.position[1] + .15)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.map.tiles[x + 1][y] != "bedrock":
            self.position = (self.position[0] + self.speed * .1, y)
            self.texture = "drill_base_right"
            return

        if keys[pygame.K_LEFT] and self.map.tiles[x - 1][y] != "bedrock":
            self.position = (self.position[0] - self.speed * .1, y)
            self.texture = "drill_base_left"
            return

        if keys[pygame.K_UP] and self.map.tiles[x][y - 1] != "bedrock" and y > 0:
            self.position = (self.position[0], self.position[1] - self.speed * .1)
            self.texture = "drill_base_up"

            if floor(self.position[1]) == y - 1:
                self.map.tiles[x][y] = "scaffolding"
            
            return

        if keys[pygame.K_DOWN] and self.map.tiles[x][y + 1] != "bedrock":
            self.position = (x, self.position[1] + self.speed * .1)
            self.texture = "drill_base_down"
            return

#Game loop
clock = pygame.time.Clock()
level = map(1024, 1024)
drill = player(level)

running = True
while running:
    clock.tick(60) 

    level.render(drill.get_camera_offset())
    drill.tick()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False