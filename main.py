import pygame
from Ball import *
from Line import *
from Engine import *
from Polygon import *

background_color = (0, 162, 232)
(width, height) = (640, 480)

running = True

FPS = 60

def main():
    global running, screen
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Basket")

    e = GameEngine((0.0, 0.1))

    clock = pygame.time.Clock()

    while running:
        t = clock.tick(60)

        screen.fill(background_color)
        x, y = pygame.mouse.get_pos()
        e.draw(screen)
        e.tick(np.array((x, y)))
        pygame.display.update()

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                e.key_released(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                e.grabBall(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                e.releaseBall()


    pygame.quit()

if __name__ == '__main__':
    main()
