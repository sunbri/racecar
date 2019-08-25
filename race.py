import pygame
from pygame.locals import *
import math
from net import *

# Game constants
SCREEN_SIZE = 800

# Car subclasses Sprite
class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.original_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(400, 350))
        self.speed = 0
        self.acceleration = 1
        self.theta = 0
        self.omega = 30 
        self.destroyed = False
        self.net = Net()
        self.parent = False

        self.n = 0
        self.e = 0
        self.w = 0

    def reset(self):
        self.speed = 0
        self.theta = 0
        self.destroyed = False
        self.parent = False
        self.rect.center = (400, 350)

    # Accelerate
    def accelerate(self, direction):
        if not self.destroyed:
            self.speed += direction * self.acceleration
            if self.speed > 10:
                self.speed = 10
            elif self.speed < -10:
                self.speed = -10

    # Turn
    def turn(self, direction):
        if not self.destroyed:
            self.theta += direction * self.omega
            self.theta %= 360

    # Destroy
    def destroy(self):
        self.destroyed = True

    # x_norm^2 + y_norm^2 = 1
    def x_norm(self):
        return math.sin(math.radians(self.theta))

    def y_norm(self):
        return -math.cos(math.radians(self.theta))

    # Moving
    def update(self):
        if not self.destroyed:
            x_shift = self.x_norm() * self.speed
            y_shift = self.y_norm() * self.speed
            self.rect.move_ip(x_shift, y_shift)
            self.image = pygame.transform.rotate(self.original_image, -self.theta)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=self.rect.center)

# Class to store the wall only
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(topleft=(0,0))
        self.mask = pygame.mask.from_surface(self.image)

def main():

    # Initialize the pygame module
    pygame.init()

    # Initialize fon
    pygame.font.init()
    font = pygame.font.SysFont('helvetica', 20)

    # Set title of screen
    pygame.display.set_caption('Genetic Cars')

    # Create a surface
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    # Load car image
    Car.image = pygame.image.load("car.png").convert_alpha()
    Wall.image = pygame.image.load("wall_2.png").convert_alpha()

    # Load track and wall and display it
    track = pygame.image.load("track_2.png")
    screen.blit(track, (0, 0))
    pygame.display.flip()

    # Game groups
    all = pygame.sprite.RenderUpdates()
    cars = pygame.sprite.Group()

    # Assign default groups to each sprite class
    Car.containers = all, cars
    Wall.containers = all

    # Keeps control of the game loop
    running = True
    
    # Starting variables
    car_list = [Car() for i in range(600)]
    wall = Wall()
    clock = pygame.time.Clock()
    gens = 1

    # Game loop
    while running:
        # Loop through all events happening
        for event in pygame.event.get():
            # Exit game loop when quit
            if event.type == pygame.QUIT:
                running = False
            # Print mouse coord for click for debug
            if event.type == pygame.MOUSEBUTTONUP:
                for car in car_list:
                    if car.rect.collidepoint(event.pos) and car.parent == False:
                        car.parent = True
                        print("Parent Selected")
                        break

        # Get which keys have been pressed
        keystate = pygame.key.get_pressed()

        # Get new kids
        parents = [car.net for car in car_list if car.parent == True]
        if keystate[K_n] and parents:
            gens += 1
            for i in range(len(car_list)):
                car_list[i].reset()
                car_list[i].net = mutate_networks(parents)

        # Reset state of some cars to clear stuff
        if keystate[K_r]:
            for car in car_list:
                if car.destroyed:
                    car.reset()
                    car.destroyed = True

        # Clear the last drawn cars
        all.clear(screen, track)

        alive = 0
        # Do car stuff if not destroyed
        for car in car_list:

            if not car.destroyed:
                alive += 1
                # Get data - how far from wall in each direction
                # These are the proper angles
                x = car.x_norm()
                y = car.y_norm()

                # Scan north
                i = 0
                while True:
                    i += 1
                    x_loc = round(car.rect.center[0] + i*x)
                    y_loc = round(car.rect.center[1] + i*y)
                    if (wall.mask.get_at((x_loc, y_loc))):
                        car.n = i
                        #pygame.draw.line(screen, (0, 0, 255), 
                        #                 car.rect.center, (x_loc, y_loc), 1)
                        break

                # Scan east
                i = 0
                while True:
                    i += 1
                    x_loc = round(car.rect.center[0] - i*y)
                    y_loc = round(car.rect.center[1] + i*x)
                    if (wall.mask.get_at((x_loc, y_loc))):
                        car.e = i
                        #pygame.draw.line(screen, (0, 0, 255), 
                        #                 car.rect.center, (x_loc, y_loc), 1)
                        break

                # Scan west
                i = 0
                while True:
                    i += 1
                    x_loc = round(car.rect.center[0] + i*y)
                    y_loc = round(car.rect.center[1] - i*x)
                    if (wall.mask.get_at((x_loc, y_loc))):
                        car.w = i
                        #pygame.draw.line(screen, (0, 0, 255), 
                        #                 car.rect.center, (x_loc, y_loc), 1)
                        break

                # Get neural net response
                input_vec = np.array([[(car.n - 200) / 40], [(car.e - 60) / 15], [(car.w - 60) / 15], [(car.speed - 7) / 2], [np.radians(car.theta) - 3.14]], dtype=np.float)
                output = car.net.feedforward(input_vec)
                car.accelerate((output[0] - .5))
                car.turn((output[1] - .5))

        # Handle collision between car and wall
        for car in pygame.sprite.spritecollide(wall, cars, False, pygame.sprite.collide_mask):
            car.destroy()

        # Display text
        screen.blit(font.render('next gen (n)', False, (0, 0, 0)), (450, 700))
        screen.blit(font.render('gen ' + str(gens), False, (0, 0, 0)), (450, 720))
        screen.blit(font.render('reset dead cars (r)', False, (0, 0, 0)), (450, 740))
        screen.blit(font.render('alive cars ' + str(alive), False, (0, 0, 0)), (450, 760))

        # Render things
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # Draw after render to make sense
        all.update()

        # Framerate
        clock.tick(20)

# Run only if this module is being directly run
if __name__ == "__main__":
    main()
