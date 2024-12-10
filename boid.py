import pygame
import random
import math
from pygame import Vector2 as Vector
WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NUM_BOIDS = 70
MAX_SPEED = 8
MIN_SPEED = 4
MAX_FORCE = 0.2
PERCEPTION_RADIUS = 50
PI = math.pi
class Boid:
    def __init__(self, x, y):
        self.position = Vector(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = Vector(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = Vector(0, 0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.length = random.uniform(MIN_SPEED, MAX_SPEED)
        self.velocity = pygame.math.Vector2(self.length * math.cos(self.angle), self.length * math.sin(self.angle))
        self.perception = PERCEPTION_RADIUS
    def edges(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def align(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total  # Step 1: Average the steering vector

            if steering.length() > 0:
                steering = steering.normalize() * MAX_SPEED  # Step 2: Set magnitude to max_speed

            steering -= self.velocity  # Step 3: Subtract the current velocity

            # Step 4: Limit the force to max_force
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering

    def cohesion(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position 
            if steering.length() > 0:
                steering = steering.normalize() * MAX_SPEED 
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering

    def separation(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            dist  = self.position.distance_to(boid.position)

            if boid != self and dist < 20:
                diff = self.position - boid.position
                if dist != 0:
                    diff /= (dist * dist)
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * MAX_SPEED
            steering = steering - self.position
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering

    def show(self, screen):
        pygame.draw.circle(screen, WHITE, self.position, 8)
        
def update(boids):
    for boid in boids:
        align = boid.align(boids)
        cohesion = boid.cohesion(boids)
        separation = boid.separation(boids)
        
        boid.acceleration = align + cohesion + separation
        boid.velocity = boid.velocity + boid.acceleration
        boid.position = boid.position + boid.velocity
        boid.acceleration = 0
        boid.edges()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    try:
        while running:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            update(boids)
            for boid in boids:
                boid.show(screen)

            pygame.display.flip()
            clock.tick(30)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()