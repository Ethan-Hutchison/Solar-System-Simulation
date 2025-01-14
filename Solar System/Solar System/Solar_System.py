import pygame
import math

#set window size for display
pygame.init()
Width = 1800
Height = 1000
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Solar System Sim")

#colors so they rgb codes dont have to be wriiten a ton
Yellow = (255,255,0)
Gray = (100, 100, 100)
White = (255,255,255)
Blue = (0,0,255)
Red = (255,0,0)
Brown = (150, 75, 0)
Orange = (255, 100, 0)

#class for creating planets
class Planet:
    AU = 149.6e6 * 1000 #distance from sun in astronimic units
    Scale = 80 / AU
    G = 6.67428e-11 #Gravitational constant
    timestep = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.sun = False
        self.distance = 0
        self.orbit = []
        self.vel_x = 0
        self.vel_y = 0
        
    def draw(self, win):
        x = self.x * self.Scale + Width / 2
        y = self.y * self.Scale + Height / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.Scale + Width / 2
                y = y * self.Scale + Height / 2
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        
    #creating the gravitational forces on planets by the sun for their orbit    
    def gravity(self, other):
        other_x = other.x
        other_y = other.y
        dist_x = other.x - self.x
        dist_y = other.y - self.y
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        
        if other.sun:
            self.diststance = dist
        #calculates the forces and angles of the forces
        force = self.G * self.mass * other.mass / dist ** 2
        angle = math.atan2(dist_y, dist_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        
        return force_x, force_y
    #updates the position of each planet as the simulation runs
    def positions(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.gravity(planet)
            total_force_x += fx
            total_force_y += fy
         #calculates the velocities of the planets so they orbit at the right speed   
        self.vel_x += total_force_x / self.mass * self.timestep
        self.vel_y += total_force_y / self.mass * self.timestep
        self.x += self.vel_x * self.timestep
        self.y += self.vel_y * self.timestep
        self.orbit.append((self.x, self.y))


def main():
    running = True
    clock = pygame.time.Clock()
    sun = Planet(0, 0, 15, Yellow, 1.98892 * 10**30)
    sun.sun = True
    mercury = Planet(0.39 * Planet.AU, 0, 4, Gray, 0.330 * 10**23)
    mercury.vel_y = -47.4 * 1000
    
    venus = Planet(0.723 * Planet.AU, 0, 7, White, 4.8685 * 10**24)
    venus.vel_y = -35.02 * 1000
    
    earth = Planet(1 * Planet.AU, 0, 8, Blue, 5.9742 * 10**24)
    earth.vel_y = -29.783 * 1000
    
    mars = Planet(1.524 * Planet.AU, 0, 6, Red, 6.39 * 10**23)
    mars.vel_y = -24.077 * 1000
    
    jupiter = Planet(5.20 * Planet.AU, 0, 10, Brown, 1.898 * 10**27)
    jupiter.vel_y = -13.1 * 1000



    planets = [sun, mercury,venus, earth, mars, jupiter]

    
    while running: 
        Win.fill((0 ,0, 0))
        clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for planet in planets:
            planet.positions(planets)
            planet.draw(Win)
        pygame.display.update()
    
    pygame.quit()
main()