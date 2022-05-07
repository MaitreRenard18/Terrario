#Imports
from math import floor
import pygame
import random
import os

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1056, 832))
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
        for x in range(self.width):
            self.tiles.append([])

            for y in range(self.height):
                if y == 0:
                    self.tiles[x].append("grass")
                elif y == 1:
                    self.tiles[x].append("dirt")
                elif y < 4:
                    self.tiles[x].append(random.choice(["dirt", "stone"]))
                elif y < 8:
                    self.tiles[x].append("stone")
                else:
                    choices = ["stone" for _ in range(12)]
                    choices.append("coal")

                    self.tiles[x].append(random.choice(choices))
        
        for _ in range(512):
            max_size = random.randint(32, 64)
            self.dig((random.randint(0, self.width), random.randint(4, self.height)), max_size)

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
                x_index = None if x < 0 or x > self.width - 1 else x
                y_index = None if y < 0 or y > self.height - 1 else y
                
                if x_index != None and y_index != None:
                    texture = textures[self.tiles[x_index][y_index]]
                    screen.blit(texture, (x * 32 + -offset[0] * 32, y * 32 + -offset[1] * 32))
                    
#Joueur
class player:
    def __init__(self, map):
        self.position = (map.width // 2, -1)
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
        screen.blit(textures[self.texture] , (screensize[0] // 2 - 16, screensize[1] // 2))

        self.map.tiles[floor(self.position[0])][floor(self.position[1])] = "cave"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.position = (self.position[0] + self.speed * .1, self.position[1])
            self.texture = "drill_base_right"
            return

        if keys[pygame.K_LEFT]:
            self.position = (self.position[0] - self.speed * .1, self.position[1])
            self.texture = "drill_base_left"
            return

        if keys[pygame.K_UP] and self.position[1] > -1:
            self.position = (self.position[0], self.position[1] - self.speed * .1)
            self.texture = "drill_base_up"
            return

        if keys[pygame.K_DOWN]:
            self.position = (self.position[0], self.position[1] + self.speed * .1)
            self.texture = "drill_base_down"
            return

#Variables
gold = 0
fuel_capacity = 10
speed = 0.30

#Shop
def affichage():
        screen.blit(textures["background"], (0,0)) #J'affiche le fond beige
        screen.blit(textures["shop"], (70,50)) #J'affiche l'interface
        
class Shop:
    def __init__(self, pic, pos, price): #J'ai besoin de l'image à afficher, des positions x/y, et du prix de chaque bouton/amélioration
        self.pic = pic
        self.pos = pos
        self.price = price

    def click(self):
        global shop #Le bool shop me permet d'intervertir entre le shop, et le monde normal
        global speed #Et j'ai besoin des variables globales speed/fuel_capacity/ pour les augmenter à chaque achat
        global fuel_capacity
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONUP: #Je vérifie si le joueur clique
                if self.pic == textures["exit"]: #Je change le bool shop, pour retourner dans le monde, si le joueur appui sur le bouton "Exit"
                    shop = False
                elif self.pos[0] == 103: #Sinon, je vérifie si il clique sur le bouton pour améliorer le speed, si oui j'augmente le speed, et son prix
                    speed += 0.05
                    self.price += 20
                elif self.pos[0] == 391: #Pareil, mais pour le fuel_capacity
                    fuel_capacity += 2
                    self.price += 20
                elif self.pos[0] == 679: #Pareil, mais pour le
                    print("owo")
                    
    def animation(self): #ça sert à afficher les boutons animé, par dessus l'interface
        screen.blit(self.pic, (self.pos[0], self.pos[1])) #du coup j'affiche l'image animé aux positions du bouton sur lequel je suis

#Game loop
clock = pygame.time.Clock()

print("Génération du monde")
level = map(256, 256)

print("Génération des grottes")
for _ in range(32):
    dig((random.randint(0, len(level.tiles)), random.randint(4, len(level.tiles[0]))), level.tiles, 32)

print("Génération terminée")

drill = player(level)

boutons = [Shop(textures["buy"], [103, 632], 20), Shop(textures["buy"], [391, 632], 20), Shop(textures["buy"], [679, 632], 20), Shop(textures["exit"], [426, 692], 0)]

shop = #ptdrr t'as vu ça a pas marché, met cque tu veux pour le bool <--- du coup
running = True
while running:
    
    pygame.display.flip()

    if shop: #Si le joueur est sur le shop
        mouse = pygame.mouse.get_pos() #Je prend la position de la souris
        if 103<mouse[0]<103 + 274 and 632<mouse[1]<632 + 57: #Si je suis sur les positions du bouton 1, j'appel l'animation + je vérifie si il y a un clique
            boutons[0].animation()
            boutons[0].click()
        elif 391<mouse[0]<391 + 274 and 632<mouse[1]<632 + 57: #Si je suis sur les positions du bouton 2, j'appel l'animation + je vérifie si il y a un clique
            boutons[1].animation()
            boutons[1].click()
        elif 679<mouse[0]<679 + 274 and 632<mouse[1]<632 + 57: #Si je suis sur les positions du bouton 3, j'appel l'animation + je vérifie si il y a un clique
            boutons[2].animation()
            boutons[2].click()
        elif 426<mouse[0]<426 + 273 and 692<mouse[1]<692 + 51: #Si je suis sur les positions du bouton exit, j'appel l'animation + je vérifie si il y a un clique
            boutons[3].animation()
            boutons[3].click()
        else:
            affichage() #Sinon je fais rien, donc je réaffiche le shop, par dessus les animations si il y en a eu
    else:
        clock.tick(60) 

        level.render(drill.get_camera_offset())
        drill.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False#Imports
