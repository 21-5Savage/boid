import pygame
import random
import math
from boid1 import *
from pygame import Vector2 as Vector
from gen_sim import *
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bofs = [Bof(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_f)]
    bops = [Bop(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_p)]
    boids = bofs + bops
    running = True
    sim = Simulation()
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sim.update(bops, bofs, boids)
        for boid in boids:
            boid.show(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()