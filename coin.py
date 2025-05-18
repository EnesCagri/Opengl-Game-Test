import math
import random
import time
import os
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from utils import load_texture

def load_texture(filename):
    textureSurface = pygame.image.load(filename)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    return texture

class Coin:
    def __init__(self, position, texture_type="gold"):
        self.position = position
        self.rotation = 0
        self.collected = False
        self.radius = 0.3
        self.hover_offset = 0
        self.hover_speed = 3.0
        self.rotation_speed = 180.0
        self.hover_time_offset = random.random() * math.pi * 2
        
        # Load texture based on type
        texture_file = texture_type + ".png"
        self.texture = load_texture(os.path.join("textures", texture_file))
        
        # Create coin display list
        self.coin_list = glGenLists(1)
        glNewList(self.coin_list, GL_COMPILE)
        self.create_coin_geometry()
        glEndList()
        
    def create_coin_geometry(self):
        glPushMatrix()
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)  # Use texture color directly
        
        glDisable(GL_LIGHTING)

        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)

        glRotatef(90, 1, 0, 0)  
        glColor3f(1.0, 0.84, 0.0)  
        gluCylinder(quad, self.radius, self.radius, 0.05, 32, 1)
        

        glPushMatrix()
        glTranslatef(0, 0, 0.05)
        
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.84, 0.0)  
        glTexCoord2f(0.5, 0.5) 
        glVertex3f(0, 0, 0) 
        
        segments = 32
        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * self.radius
            y = math.sin(angle) * self.radius
            glTexCoord2f(0.5 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle))
            glVertex3f(x, y, 0)
        glEnd()
        
        glPopMatrix()
        
 
        glPushMatrix()
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.84, 0.0)  
        glTexCoord2f(0.5, 0.5)  
        glVertex3f(0, 0, 0)  
        
        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * self.radius
            y = math.sin(angle) * self.radius
            glTexCoord2f(0.5 + 0.5 * math.cos(-angle), 0.5 + 0.5 * math.sin(-angle))
            glVertex3f(x, y, 0)
        glEnd()
        glPopMatrix()
        

        glEnable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE) 
        glPopMatrix()
        
    def draw(self):
        if not self.collected:
            glPushMatrix()

            glTranslatef(
                self.position[0],
                self.position[1] + self.hover_offset,
                self.position[2]
            )
            
     
            glRotatef(self.rotation, 0, 1, 0)
            
       
            glRotatef(15, 1, 0, 0)
            
     
            glCallList(self.coin_list)
            
            glPopMatrix()
            
    def update(self, dt):
        if not self.collected:

            self.rotation += self.rotation_speed * dt
            
            time_val = time.time() + self.hover_time_offset
            primary_wave = math.sin(time_val * self.hover_speed) * 0.2
            secondary_wave = math.sin(time_val * self.hover_speed * 2) * 0.05
            self.hover_offset = primary_wave + secondary_wave

    def check_collection(self, player_pos):
        if not self.collected:
            dx = self.position[0] - player_pos[0]
            dy = (self.position[1] + self.hover_offset) - player_pos[1]
            dz = self.position[2] - player_pos[2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if distance < (self.radius + 0.5):  
                self.collected = True
                return True
        return False 