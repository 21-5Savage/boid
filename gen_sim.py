from boid1 import *
import main as sim

class Simulation:
    def __init__(self):
        self.simulation_number = 1

    def update(self, bops, bofs, boids):
        for bop in bops:
            for bof in bofs[:]: 
                if bop.position.distance_to(bof.position) < 2:
                    bofs.remove(bof) 
                    bop.kill_count += 1
        remaining_boids = bofs + bops

        for boid in remaining_boids:
            if isinstance(boid, Bop):
                chase = boid.chase(remaining_boids)
                choose = boid.choose(remaining_boids)
                align = boid.align(remaining_boids)
                cohesion = boid.cohesion(remaining_boids)
                separation = boid.separation(remaining_boids)
                boid.acceleration = align + cohesion + separation + chase + choose
            else:
                run = boid.run(remaining_boids)
                if run.length() > 0: 
                    separation = boid.separation(remaining_boids)
                    boid.acceleration = run + separation
                else:
                    align = boid.align(remaining_boids)
                    cohesion = boid.cohesion(remaining_boids)
                    separation = boid.separation(remaining_boids)
                    boid.acceleration = align + cohesion + separation

            boid.velocity += boid.acceleration
            if boid.velocity.length() > boid.max_speed:
                boid.velocity = boid.velocity.normalize() * boid.max_speed
            boid.position += boid.velocity
            boid.edges()
            boid.acceleration *= 0 

        bops.sort(key=lambda x: x.kill_count, reverse=True)
        if len(bofs) == 0:
            with open("kills.txt", "w") as file:
                file.write(f'Simulation {self.simulation_number}\n')
                for boid in bops:
                    file.write(f'k = {boid.kill_count} chase = {boid.coef_chase:.5f} choose = {boid.coef_choose:.5f} align = {boid.coef_align:.5f} cohesion = {boid.coef_cohesion:.5f}\n')

            new_bops = evolve_bops(bops, len(bops))
            bops[:] = new_bops
            bofs[:] = [Bof(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_f)]
            self.simulation_number += 1 

        boids[:] = bofs + bops