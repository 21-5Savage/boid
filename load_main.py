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
    
    bops = []
    with open("kills copy.txt", "r") as file:
        lines = file.readlines()
    
    part = lines[0].strip().split()
    sim_counter = int(part[1]) + 1
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) >= 15: 
            coef_chase = float(parts[5])
            coef_choose = float(parts[8])
            coef_align = float(parts[11])
            coef_cohesion = float(parts[14])
            bop = Bop(random.uniform(0, WIDTH), random.uniform(0, HEIGHT),
                        coef_chase=coef_chase, coef_choose=coef_choose, coef_align=coef_align, coef_cohesion=coef_cohesion)
            bops.append(bop)
    boids = bofs + bops
    running = True
    sim = Simulation()
    sim.simulation_number = sim_counter
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