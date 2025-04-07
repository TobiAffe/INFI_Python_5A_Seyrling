import pygame
import sys
from npc_chatbot import NPCBot

pygame.init()

# Fenster
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magier trifft Spieler")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Spieler
player_size = 50
player_pos = pygame.Vector2(100, 100)
player_speed = 5

# NPC
npc_size = 50
npc = NPCBot(pygame.Vector2(400, 300))

# Font
font = pygame.font.SysFont("arial", 18)

# Game Loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielerbewegung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += player_speed

    # NPC-Update und Anzeige
    npc.update(player_pos)

    pygame.draw.rect(WIN, BLACK, (*player_pos, player_size, player_size))  # Spieler
    pygame.draw.rect(WIN, BLUE, (*npc.pos, npc_size, npc_size))            # NPC
    npc.draw_text(WIN, font)

    pygame.display.update()

pygame.quit()
sys.exit()
