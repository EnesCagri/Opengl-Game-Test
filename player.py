import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import normalize_vector, cross_product

CUBE_SIZE = 1.0
PLAYER_RADIUS = 0.5

def normalize_vector(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length > 0:
        return [v[0]/length, v[1]/length, v[2]/length]
    return v

def cross_product(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

class Player:
    def __init__(self, position=[0, 0, 0]):
        self.start_position = position.copy() 
        self.position = position
        self.velocity = [0, 0, 0]
        self.acceleration = [0, 0, 0]
        self.radius = 0.5
        self.mass = 1.0
        self.jump_force = 10.0
        
   
        self.base_move_speed = 12.0
        self.max_move_speed = 35.0
        self.acceleration_rate = 25.0
        self.deceleration_rate = 15.0
        self.current_speed = 0.0
        
        self.friction = 0.9
        self.grounded = False
        self.gravity = [0, -20.0, 0]
        self.current_platform = None
        self.platform_velocity = [0, 0, 0] 

        self.sphere_list = glGenLists(1)
        glNewList(self.sphere_list, GL_COMPILE)
        quad = gluNewQuadric()
        gluSphere(quad, self.radius, 32, 32)
        glEndList()

    def reset_position(self):
        self.position = self.start_position.copy()
        self.velocity = [0, 0, 0]
        self.acceleration = [0, 0, 0]
        self.grounded = False
        self.current_platform = None

    def jump(self):
        if self.grounded:
            self.velocity[1] = self.jump_force
            self.grounded = False
            self.current_platform = None

    def update_movement(self, keys, camera_forward, dt):
        move_dir = [camera_forward[0], 0, camera_forward[2]]
        move_dir = normalize_vector(move_dir)

        right_dir = normalize_vector(cross_product(move_dir, [0, 1, 0]))

        movement = [0, 0, 0]
        is_moving = False
        
        if keys[K_w]:
            movement[0] -= move_dir[0]
            movement[2] -= move_dir[2]
            is_moving = True
        if keys[K_s]:
            movement[0] += move_dir[0]
            movement[2] += move_dir[2]
            is_moving = True
        if keys[K_d]:
            movement[0] -= right_dir[0]
            movement[2] -= right_dir[2]
            is_moving = True
        if keys[K_a]:
            movement[0] += right_dir[0]
            movement[2] += right_dir[2]
            is_moving = True

        if is_moving:
            self.current_speed = min(
                self.max_move_speed,
                self.current_speed + self.acceleration_rate * dt
            )
        else:
            self.current_speed = max(
                0,
                self.current_speed - self.deceleration_rate * dt
            )

        if math.sqrt(movement[0]**2 + movement[2]**2) > 0:
            movement = normalize_vector(movement)
            movement[0] *= self.current_speed
            movement[2] *= self.current_speed
            
            if not self.grounded:
                movement[0] *= 0.3
                movement[2] *= 0.3
                
            self.acceleration[0] = movement[0]
            self.acceleration[2] = movement[2]
        else:
            self.acceleration[0] = 0
            self.acceleration[2] = 0

    def handle_collision(self, platforms):
        self.grounded = False
        old_platform = self.current_platform
        self.current_platform = None
        self.platform_velocity = [0, 0, 0]
        
        next_pos = [
            self.position[0] + self.velocity[0] * 0.016,
            self.position[1] + self.velocity[1] * 0.016,
            self.position[2] + self.velocity[2] * 0.016
        ]

        for platform in platforms:
            if (abs(self.position[0] - platform[0]) < CUBE_SIZE + self.radius and
                abs(self.position[2] - platform[2]) < CUBE_SIZE + self.radius):

                platform_top = platform[1] + CUBE_SIZE
                platform_bottom = platform[1]

                if (self.velocity[1] <= 0 and 
                    self.position[1] >= platform_top and  
                    next_pos[1] - self.radius <= platform_top): 
                    
                    self.position[1] = platform_top + self.radius
                    self.velocity[1] = 0
                    self.grounded = True
                    self.current_platform = platform
                    
                    if isinstance(platform, list) and len(platform) > 3:
                        self.platform_velocity = platform[3:]
                    
                    return True

                elif (self.velocity[1] > 0 and  
                      self.position[1] <= platform_bottom and  
                      next_pos[1] + self.radius >= platform_bottom):
                    
                    self.position[1] = platform_bottom - self.radius
                    self.velocity[1] = 0
                    return True
                
                if self.position[1] > platform_bottom and self.position[1] < platform_top:
                    depth_x = (CUBE_SIZE + self.radius) - abs(self.position[0] - platform[0])
                    depth_z = (CUBE_SIZE + self.radius) - abs(self.position[2] - platform[2])

                    if depth_x < depth_z:
                        self.velocity[0] = 0
                        if self.position[0] > platform[0]:
                            self.position[0] = platform[0] + CUBE_SIZE + self.radius
                        else:
                            self.position[0] = platform[0] - CUBE_SIZE - self.radius
                    else:
                        self.velocity[2] = 0
                        if self.position[2] > platform[2]:
                            self.position[2] = platform[2] + CUBE_SIZE + self.radius
                        else:
                            self.position[2] = platform[2] - CUBE_SIZE - self.radius
                    return True
        
        return False

    def update(self, dt, platforms):
        if self.position[1] < -5:
            self.reset_position()
            return

        self.acceleration[1] += self.gravity[1]

        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        self.velocity[2] += self.acceleration[2] * dt

        if self.grounded:
            self.velocity[0] *= self.friction
            self.velocity[2] *= self.friction
            
            self.velocity[0] += self.platform_velocity[0]
            self.velocity[1] += self.platform_velocity[1]
            self.velocity[2] += self.platform_velocity[2]

        old_pos = self.position.copy()
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.position[2] += self.velocity[2] * dt
        

        self.handle_collision(platforms)

        self.acceleration = [0, 0, 0]

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        

        glColor3f(0.2, 0.5, 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.5, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        glCallList(self.sphere_list)
        glPopMatrix() 