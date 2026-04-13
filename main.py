import json
import os
import sys
from typing import List

import pygame

class Item():
    def __init__(self, name: str, info: str, path: str):
        if not pygame.get_init():
            raise Exception("pygame.get_init() is False, please use pygame.init() before initialize items")
        self.name = name
        self.info = info
        self.asset = pygame.image.load(path).convert_alpha()

    @classmethod
    def from_json(cls, path: str):
        try:
            with open(path, "r") as file:
                data = json.load(file)
            return cls(data["name"], data["info"], data["path"])
        except FileNotFoundError:
            print(f"Error: The file at {sys.path} was not found.")
            raise
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON. {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

# Khởi tạo
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# carrot_item: Item = Item("carrot", "using to eat and plan carrots. [continue]", "carrot.png")
carrot_item: Item = Item.from_json('assets/carrot_item.json')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

try:
    font = pygame.font.Font(None, 48)
except Exception as e:
    print(f"Font loading error: {e}")
    pygame.quit()
    sys.exit()

player_pos = pygame.Vector2(0, 0)
selected_item = 0

running = True


map_size = (200, 300)
tile_map = [0]*map_size[0]*map_size[1]

chestnut_image = pygame.image.load(os.path.join('assets', 'chestnut.png')).convert_alpha()
assets = pygame.image.load(os.path.join('assets', 'keyboard-&-mouse_sheet_double.png')).convert_alpha()

#tile imgs
error_tile = pygame.image.load(os.path.join('assets', 'error-tile.png')).convert_alpha()
dirt_tile = pygame.image.load(os.path.join('assets', 'dirt.png')).convert_alpha()
tile_size = 32

items_player: List[Item] = [None]*10

items_player[0] = carrot_item

def load_map(filename: str):
    global tile_map
    try:
        with open(filename, 'r') as file:
            tile_map = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {filename}. {e}")

load_map('map.json')
print(type(tile_map))

def save_map(filename: str):
    try:
        with open(filename, 'w') as file:
            json.dump(tile_map, file)
    except Exception as e:
        print(f"Error saving map: {e}")

while running:
    delta = clock.tick() / 1000.0
    speed = 300

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_map('map.json')
    
    keys = pygame.key.get_pressed()

    direction = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        direction.y -= 1
    if keys[pygame.K_s]:
        direction.y += 1
    if keys[pygame.K_a]:
        direction.x -= 1
    if keys[pygame.K_d]:
        direction.x += 1

    if keys[pygame.K_1]:
        selected_item=0
    if keys[pygame.K_2]:
        selected_item=1
    if keys[pygame.K_3]:
        selected_item=2
    if keys[pygame.K_4]:
        selected_item=3
    if keys[pygame.K_5]:
        selected_item=4
    if keys[pygame.K_6]:
        selected_item=5
    if keys[pygame.K_7]:
        selected_item=6
    if keys[pygame.K_8]:
        selected_item=7
    if keys[pygame.K_9]:
        selected_item=8
    if keys[pygame.K_0]:
        selected_item=9

    
    if direction.length() > 0:
        direction = direction.normalize()

    player_pos += direction * speed * delta
    
    # 3. VẼ

    screen.fill(BLACK)

    for y in range(map_size[1]):
        for x in range(map_size[0]):     
            if tile_map[x+y*map_size[0]] == 0:
                screen.blit(error_tile, (x*tile_size,y*tile_size, tile_size, tile_size))
            elif tile_map[x+y*map_size[0]] == 1:
                screen.blit(dirt_tile, (x*tile_size,y*tile_size, tile_size, tile_size))
    
    ## Player
    pygame.draw.circle(screen, (0, 255, 0), (int(player_pos.x), int(player_pos.y)), 30)

    ## Player tile
    

    size_screen = screen.get_size()

    if items_player[selected_item] != None:
        text_surface = font.render(f"{items_player[selected_item].name}", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH//2, 300))
        screen.blit(text_surface, text_rect)

    ## Fast tool player
    for i in range(10):
        if items_player[i] != None:
            screen.blit(items_player[i].asset, (40*i+(size_screen[0]-40*10)//2, 400))
        pygame.draw.rect(screen, (0, 255, 0) if selected_item !=i else WHITE, (40*i+(size_screen[0]-40*10)//2, 400, 40, 40), 1)
        
        text_surface = pygame.font.Font(None, 32).render(f"{(i+1)%10}", True, WHITE)
        text_size = text_surface.get_size()
        screen.blit(text_surface, (40*i+(size_screen[0]-40*10)//2, 400, text_size[0], text_size[1]))

    
    actual_fps = clock.get_fps()
    pygame.display.set_caption(f"FPS hiện tại: {actual_fps:.2f}")

    text_surface = font.render(f"FPS: {actual_fps:.2f}", True, WHITE)
    text_rect = text_surface.get_rect()
    screen.blit(text_surface, text_rect)

    

    pygame.draw.rect(
        screen, (255, 100, 0),
        (player_pos.x//tile_size*tile_size, (player_pos.y+20)//tile_size*tile_size, tile_size, tile_size),
        2)
    
    if keys[pygame.K_q]:
        x, y = int(player_pos.x//tile_size), int((player_pos.y+20)//tile_size)
        tile_map[x+y*map_size[0]] = 1

    pygame.display.flip()

    

pygame.quit()