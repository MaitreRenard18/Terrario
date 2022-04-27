import pygame
import random
import os
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Minecraft Ultimate HD Deluxe Definitive Edition')

#Textures
textures = {}

for file in os.listdir(str(os.getcwd()) + "\Textures"):
    textures[file.replace(".png", "").lower()] = pygame.transform.scale(pygame.image.load(str(os.getcwd()) + "\Textures\\" + file).convert(), (32, 32))

#Map
def generate_map(width, height):
    map = [["grass" for _ in range(width)]]

    for i in range(height - 1):
        if i < 2:
            map.append(["dirt" for _ in range(width)])
        elif i < 4:
            map.append([random.choice(["dirt", "stone"]) for _ in range(width)])
        elif i < 8:
            map.append(["stone" for _ in range(width)])
        else:
            map.append([random.choice(["coal", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone"]) for _ in range(width)])

    return map

def render_map(map, sky_offset):
    screen.fill((145, 226, 255))
    
    for lvl in range(0, len(map)):
        for tile in range(0, len(map[lvl])):
            screen.blit(textures[map[lvl][tile]] , (tile * 32, lvl * 32 + sky_offset * 32))

#Run the game
map = generate_map(32, 32)
render_map(map, 8)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False