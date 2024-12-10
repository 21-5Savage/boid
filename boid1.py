import pygame
import random
import math
from pygame import Vector2 as Vector

WIDTH, HEIGHT = int(1300), int(800)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NUM_f = 200
NUM_p = 300
MAX_SPEED_f = 10
MAX_SPEED_p = 8
MIN_SPEED = 4
MAX_FORCE = 0.5
PERCEPTION_RADIUS_f = 50
PERCEPTION_RADIUS_p = 100

class Boid:
    def __init__(self, x, y):
        self.position = Vector(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.position = Vector(x, y)
        self.velocity = Vector(random.uniform(-2, 2), random.uniform(-2, 2)).normalize() * random.uniform(MIN_SPEED, 8)
        self.acceleration = Vector(0, 0)
        self.coef_align = random.uniform(0,3)
        self.coef_cohesion = random.uniform(0,3)
        self.coef_separation = 2
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
            if boid != self and self.position.distance_to(boid.position) < self.perception and self.spec == boid.spec:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering * self.coef_align
    def cohesion(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception and self.spec == boid.spec:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering * self.coef_cohesion
    def separation(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            if boid != self and boid.spec == self.spec:
                dist = self.position.distance_to(boid.position)
                if dist < self.perception:  
                    diff = self.position - boid.position  
                    if dist != 0:
                        diff = diff / (dist * dist)
                    steering += diff
                    total += 1

        if total > 0:
            steering /= total  
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed 
            steering -= self.velocity 
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE 
        return steering * self.coef_separation
    def show(self, screen):
        if self.spec == "F":
            pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), 4)
        if self.spec == "P":
            pygame.draw.circle(screen, (255,0,0), (int(self.position.x), int(self.position.y)), 4)
        
class Bof(Boid):
    def __init__(self, x, y):
        Boid.__init__(self, x, y)
        self.spec = "F"
        self.perception = PERCEPTION_RADIUS_f
        self.max_speed = MAX_SPEED_f
        self.coef_r = 2
    def run(self, boids):
        steering = Vector(0, 0)
        closest_bop = None
        closest_dist = self.perception + 1

        for boid in boids:
            if boid.spec == "P":  
                dist = self.position.distance_to(boid.position)
                if dist < closest_dist:
                    closest_bop = boid
                    closest_dist = dist
        if closest_bop:
            desired_velocity = (self.position - closest_bop.position).normalize() * self.max_speed
            steering = desired_velocity - self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
        return steering  * self.coef_r
    
class Bop(Boid):
    def __init__(self, x, y, coef_chase=-1, coef_choose=-1, coef_align=-1, coef_cohesion=-1):
        Boid.__init__(self, x, y)
        self.spec = "P"
        self.perception = PERCEPTION_RADIUS_p
        self.max_speed = MAX_SPEED_p
        self.kill_count = 0
        self.coef_chase = random.uniform(0,3)
        self.coef_choose = random.uniform(0,3)
        if coef_chase != -1:
            self.coef_chase = coef_chase
        if coef_choose != -1:
            self.coef_choose = coef_choose
        if coef_align != -1:
            self.coef_align = coef_align
        if coef_cohesion != -1:
            self.coef_cohesion = coef_cohesion
    def chase(self, boids):
        target = None
        min_dist = float('inf')
        for boid in boids:
            if boid.spec == "F":  
                dist = self.position.distance_to(boid.position)
                if dist < self.perception and dist < min_dist:
                    min_dist = dist
                    target = boid
        if target:
            desired_velocity = (target.position - self.position)
            if desired_velocity != Vector(0, 0):
                desired_velocity = desired_velocity.normalize() * self.max_speed
            steering = desired_velocity - self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
            return steering *self.coef_chase
        return Vector(0, 0)
    def choose(self, boids):
        target = None
        min_dot_product = float('inf')

        for boid in boids:
            if boid.spec == "F":  
                dot_product = self.velocity.normalize().dot(boid.velocity.normalize())
                if self.position.distance_to(boid.position) < self.perception and dot_product < min_dot_product:
                    min_dot_product = dot_product
                    target = boid

        if target:
            desired_velocity = (target.position - self.position).normalize() * self.max_speed
            steering = desired_velocity - self.velocity
            if steering.length() > MAX_FORCE:
                steering = steering.normalize() * MAX_FORCE
            return steering * self.coef_choose

        return Vector(0, 0)

def evolve_bops(bops, num_new_bops, mutation_rate=0.1):
    bops.sort(key=lambda bop: bop.kill_count, reverse=True)
    top_bops = bops[:50] 
    
    new_bops = []
    
    for elite in top_bops:
        elite_child = Bop(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        elite_child.coef_chase = elite.coef_chase
        elite_child.coef_choose = elite.coef_choose
        elite_child.coef_align = elite.coef_align
        elite_child.coef_cohesion = elite.coef_cohesion
        
        elite_child.coef_chase = max(0, elite_child.coef_chase) 
        elite_child.coef_choose = max(0, elite_child.coef_choose)
        elite_child.coef_align = max(0, elite_child.coef_align)
        elite_child.coef_cohesion = max(0, elite_child.coef_cohesion)
        
        elite_child.coef_chase = min(MAX_SPEED_p, elite_child.coef_chase) 
        elite_child.coef_choose = min(MAX_SPEED_p, elite_child.coef_choose)
        elite_child.coef_align = min(MAX_SPEED_p, elite_child.coef_align)
        elite_child.coef_cohesion = min(MAX_SPEED_p, elite_child.coef_cohesion)
        new_bops.append(elite_child)
    
    remaining_slots = num_new_bops - len(new_bops)
    for _ in range(remaining_slots):
        parent1, parent2 = random.sample(top_bops, 2)
        
        child_coef_chase = (parent1.coef_chase + parent2.coef_chase) / 2
        child_coef_choose = (parent1.coef_choose + parent2.coef_choose) / 2
        child_coef_align = (parent1.coef_align + parent2.coef_align) / 2
        child_coef_cohesion = (parent1.coef_cohesion + parent2.coef_cohesion) / 2
        
        if random.random() < mutation_rate:
            child_coef_chase += random.uniform(-0.5, 0.5)
        if random.random() < mutation_rate:
            child_coef_choose += random.uniform(-0.5, 0.5)
        if random.random() < mutation_rate:
            child_coef_align += random.uniform(-0.5, 0.5)
        if random.random() < mutation_rate:
            child_coef_cohesion += random.uniform(-0.5, 0.5)
        
        child = Bop(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        
        child.coef_chase = max(0, child_coef_chase) 
        child.coef_choose = max(0, child_coef_choose)
        child.coef_align = max(0, child_coef_align)
        child.coef_cohesion = max(0, child_coef_cohesion)
        
        child.coef_chase = min(MAX_SPEED_p, child_coef_chase) 
        child.coef_choose = min(MAX_SPEED_p, child_coef_choose)
        child.coef_align = min(MAX_SPEED_p, child_coef_align)
        child.coef_cohesion = min(MAX_SPEED_p, child_coef_cohesion)
        
        new_bops.append(child)
    
    return new_bops

