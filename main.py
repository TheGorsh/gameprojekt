import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Das grosse HAW-Spiel")
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 30)

clock = pygame.time.Clock()
# Die Schleife, und damit unser Spiel, läuft solange running == True.
running = 1
while running:
    # Framerate auf 30 Frames pro Sekunde beschränken.
    # Pygame wartet, falls das Programm schneller läuft.
    clock.tick(30)

    # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        # Spiel beenden, wenn wir ein QUIT-Event finden.
        if event.type == pygame.QUIT:
             running = False
