#Imports
from math import floor
import pygame
import random
from time import sleep
import os
import sys

#Initialisation
pygame.init()
screen = pygame.display.set_mode((1056, 832)) #Créer la fenêtre
pygame.display.set_caption('Terrario') #Renomme la fenêtre

#Chargement des textures
textures = {}
for file in os.listdir("{}\Textures".format(os.getcwd())): #Récupère toute les fichiers se trouvant dans le dossier textures
    if file.endswith(".png"): #Vérifie qu'il sagit d'un png
        file_name = file.replace(".png", "").lower() #Créer un nom en minuscule sans le png
        
        path = "{}\Textures\{}".format(os.getcwd(), file) #Récupère l'emplacement du ficher
        image = pygame.image.load(path) #Charge l'image

        textures[file_name] = image #Ajoute une l'image dans le dictionnaire texture

#Class carte
layers = {
    0: ["air"],
    1: ["grass"],
    2: ["dirt"],
    3: ["dirt", "dirt", "stone"],
    4: ["dirt", "stone"],
    5: ["stone"],
    8: ["stone" for _ in range(16)] + ["coal"], #Ici par exemple le charbon à une chance sur 17 de se générer de la coucge 8 à 11
    12: ["stone" for _ in range(32)] + ["coal", "coal", "iron"],
    64: ["stone" for _ in range(64)] + ["iron", "iron", "gold"],
    256: ["stone" for _ in range(128)] + ["gold", "gold", "diamond"],
    512: ["stone" for _ in range(128)] + ["diamond", "diamond", "ruby"]
} #Dictionaire ou les minerais et leur chance d'apparition sont stockés

class Map:
    def __init__(self, width, height): #Prend en paramètre une largeur et une hauter
        self.width = width
        self.height = height

        self.tiles = [] #Liste ou les "tuiles" sont stockées sous le format [x][y]
        self.generate() #Appelle la fonction generate qui genère la carte
    
    def generate(self):
        print("Génération des tuiles.")

        for x in range(self.width - 1):
            sys.stdout.write('\r') #Affiche la progression dans la console
            sys.stdout.write("{}%".format(floor((x / (self.width - 1)) * 100) + 1))
            sys.stdout.flush()

            self.tiles.append([]) #Ajoute un tableau dans "tiles" qui represente une colone

            for y in range(self.height): #Pour chaques lignes dans la colone, des tuiles sont générées en fonction du numéro de ligne
                keys = list(layers.keys())

                for layer_key in range(len(keys) - 1, -1, -1):
                    if y >= keys[layer_key]:
                        layer = layers[keys[layer_key]]
                        self.tiles[x].append(random.choice(layer))
                        break

        print("\nGénération des grottes.")
        for i in range(750): #Génère 750 grottes
            sys.stdout.write('\r') #Affiche la progression dans la console
            sys.stdout.write("{}%".format(floor((i / 750) * 100) + 1))
            sys.stdout.flush()

            max_size = random.randint(32, 64) #Prend une taille aléatoire en 32 et 64 tuiles
            self.dig((random.randint(0, self.width), random.randint(4, self.height)), max_size) #Appelle la fonction dig qui génère une grotte

        for x in range(self.width - 1):
            self.tiles[x][0] = "air" #Ajoute une couche d'air à la surface
            self.tiles[x][-3] = random.choice(["stone", "bedrock"]) #Génère de la "bedrock" au fond de la carte
            self.tiles[x][-2] = random.choice(["stone", "bedrock", "bedrock"])
            self.tiles[x][-1] = "bedrock"

        print("\nGénération terminée.")

    def dig(self, position, max_size, size = 0): #Prend en paramètre une position (tuple), une taille max, et une taille actuelle (Qui augmente de 1 à chaque appelle)
        x, y = position

        if size == max_size or x > len(self.tiles) - 1 or y > len(self.tiles[x]) - 1: #Si la grotte à attend sa taille max. ou que les bordure de la map ont été atteinte, arrêter la génération
            return

        size += 1 #Augmente la taille
        self.tiles[x][y] = "cave" #Met une tuille de "grotte" a l'emplacement x, y

        choises = [] #Initialise un tableau ou les possiblités d'extension de la grotte seront stocker
        if x + 1 < len(self.tiles) and self.tiles[x + 1][y] != "cave": #Verifie si la grotte peut s'éttendre à droite
            choises.append((x + 1, y))

        if x - 1 >= 0 and self.tiles[x - 1][y] != "cave": #A droite
            choises.append((x - 1, y))

        if y + 1 < len(self.tiles[x]) and self.tiles[x][y + 1] != "cave": #En bas
            choises.append((x, y + 1))

        if y - 1 >= 0 and self.tiles[x][y - 1] != "cave": #En haut
            choises.append((x, y - 1))
        
        if len(choises) == 0: #Vérifie que la grotte peut s'éttendre
            return

        branch = [1 for _ in range(9)]
        branch.append(2)
        branch = random.choice(branch) #Choisie en combien de "branches" la grotte va s'éttendre (1 chance sur 10 qu'il y ait 2 embranchements)

        for _ in range(branch): #Appelle plusieurs fois la fonction dig en fonction du nombre d'embranchements
            self.dig(random.choice(choises), max_size, size)

    def render(self, offset): #Fonction qui affiche la carte, en prennant en paramètre la position de la camera
        screen.fill((145, 226, 255)) #Met le fond en bleu pour simuler du ciel 

        screensize = screen.get_size() #Récupère la taille de l'écran pour regarder combien de tuiles peuvent être afficher en même temps
        x_tile_number = screensize[0] // 32 + (screensize[0] % 32 > 0) 
        y_tile_number = screensize[1] // 32 + (screensize[1] % 32 > 0)

        for x in range(offset[0], offset[0] + x_tile_number): #Pour chaques colones visibles sur l'écran
            for y in range(offset[1], offset[1] + y_tile_number): #Pour chaques lignes visibles sur l'écran
                x_index = None if x < 0 or x > len(self.tiles) - 1 else x #Vérifie que la colone existe
                y_index = None if y < 0 or y > len(self.tiles[0]) - 1 else y #Vérifie que la ligne existe
                
                if x_index != None and y_index != None: #Si la colone et la ligne existent
                    texture = textures[self.tiles[x_index][y_index]] #Récupère la texture dans "tiles"
                    screen.blit(pygame.transform.scale(texture, (32, 32)), (x * 32 - offset[0] * 32, y * 32 - offset[1] * 32)) #Et l'affiche sur l'écran

#Class joueur
ores_values = {
    "coal": 1,
    "iron": 2,
    "gold": 4,
    "diamond": 8,
    "ruby": 15
}

class Player:
    def __init__(self, position, map):
        self.position = position
        self.direction = ["right", (1, 0)]

        self.speed = 1
        self.moving_cooldown = 0
        self.falling_cooldown = 0

        self.gold = 0
        self.fuel = 100
        
        self.map = map

    def get_camera_offset(self):
        screensize = screen.get_size()
        x = floor(self.position[0]) - (screensize[0] // 32) // 2
        y = floor(self.position[1]) - (screensize[1] // 32) // 2

        return (x, y)

    def mine(self):
        x, y = self.position
        ore = self.map.tiles[x][y]

        if ore in ores_values:
            self.gold += ores_values[ore]

        self.map.tiles[x][y] = "cave"

    def tick(self):
        screensize = screen.get_size()

        drill_base_texture = pygame.transform.scale(textures["drill_base_{}".format(self.direction[0])], (32, 32))
        drill_base_position = (screensize[0] // 2 - 16, screensize[1] // 2)
        screen.blit(drill_base_texture, drill_base_position)

        drill_texture = pygame.transform.scale(textures["drill_{}".format(self.direction[0])], (32, 32))
        drill_position = (drill_base_position[0] + self.direction[1][0] * 32, drill_base_position[1] + self.direction[1][1] * 32)
        screen.blit(drill_texture, drill_position)

        x, y = self.position

        if not self.map.tiles[x][y] in ["scaffolding", "cave", "air"]:
            self.mine()
        
        if self.map.tiles[x][y + 1] == "cave":
            parachue_texture = pygame.transform.scale(textures["parachute"], (32, 32))
            screen.blit(parachue_texture, (screensize[0] // 2 - 16, screensize[1] // 2 - 32))

            if self.falling_cooldown > 0:
                self.falling_cooldown -= .25
                return
            
            self.position = (x, self.position[1] + 1)
            self.falling_cooldown = 1

            return

        if self.moving_cooldown > 0:
            self.moving_cooldown -= self.speed * .1
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.map.tiles[x + 1][y] != "bedrock":
            self.position = (x + 1, y)
            self.direction = ["right", (1, 0)]
            self.fuel -= 1

            self.moving_cooldown = 1
            return

        if keys[pygame.K_LEFT] and self.map.tiles[x - 1][y] != "bedrock":
            self.position = (x - 1, y)
            self.direction = ["left", (-1, 0)]
            self.fuel -= 1

            self.moving_cooldown = 1
            return

        if keys[pygame.K_UP] and self.map.tiles[x][y - 1] != "bedrock" and y > 0:
            self.position = (x, y - 1)
            self.direction = ["up", (0, -1)]
            self.fuel -= 1

            self.map.tiles[x][y] = "scaffolding"
            
            self.moving_cooldown = 1
            return

        if keys[pygame.K_DOWN] and self.map.tiles[x][y + 1] != "bedrock":
            self.position = (x, y + 1)
            self.direction = ["down", (0, 1)]
            self.fuel -= 1

            self.moving_cooldown = 1
            return

#Class batiment
class ShopBuilding:
    def __init__(self, position, map):
        self.position = position
        self.map = map

        self.falling_cooldown = 0


    def tick(self):
        x, y = self.position

        floor_underneath = False
        for i in range(5):
            if not self.map.tiles[x + i][y + 1] in ["cave", "scaffolding"]:
                floor_underneath = True
                self.falling_cooldown = 1

        if self.falling_cooldown > 0:
                self.falling_cooldown -= .25
        else:
            if not floor_underneath:
                self.position = (x, y + 1)
                self.falling_cooldown = 1

        offset = drill.get_camera_offset()
        screensize = screen.get_size()

        if offset[0] <= x + 4 and offset[0] + screensize[0] // 32 > x and offset[1] < y + 1:
            texture = textures["garage"]
            screen.blit(pygame.transform.scale(texture, (160, 80)), (x * 32 - offset[0] * 32, y * 32 - offset[1] * 32 - 48))

            if not floor_underneath:
                parachute_texture = textures["shop_parachute"]
                screen.blit(pygame.transform.scale(parachute_texture, (160, 160)), (x * 32 - offset[0] * 32, y * 32 - offset[1] * 32 - 208))

#Boucle principal
clock = pygame.time.Clock() #Créer une "clock" qui permet de limiter la vitesse d'excution maximal grace à la fonction tick()

level = Map(1024, 1024) #Créer une carte de 1024 * 1024
drill = Player((level.width // 2, 0), level) #Créer le joueur ayant comme paramètre la carte

shop = ShopBuilding((level.width // 2, 0), level)

running = True
while running: #Boucle principal qui execute toutes les fonctions à chaques frames
    clock.tick(60) 

    level.render(drill.get_camera_offset()) #Affiche la carte avec une position de camera obtenue grace à fonction get_camera_offset()
    shop.tick() #"Met a jour" la shop
    drill.tick() #"Met a jour" la foreuse

    pygame.display.flip() #Met à jour l'affichage

    for event in pygame.event.get(): #Permet d'arrêter la boucle (Et donc le jeu si la fenêtre est fermée)
        if event.type == pygame.QUIT:
            running = False
