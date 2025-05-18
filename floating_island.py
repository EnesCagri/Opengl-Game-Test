import math
import random
import os
import time
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
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

class FloatingIsland:
   
    block_textures = {}
    
    def __init__(self, center_pos, size=1.0, movement_type=None, block_type="grass"):
        self.center_pos = center_pos
        self.size = size
        self.base_y = center_pos[1]
        self.hover_offset = 0
        self.hover_speed = 0.5
        self.hover_amplitude = 0.1
        self.block_type = block_type
        

        self.movement_type = movement_type
        self.movement_time = random.random() * math.pi * 2 
        self.movement_speed = 0.5
        self.movement_amplitude = 2.0
        self.original_pos = center_pos.copy()
        

        self.blocks = []
        for x in range(-1, 2):
            for z in range(-1, 2):
                if x == 0 and z == 0:
                    self.blocks.append([x, 0, z])
                elif random.random() < 0.8:
                    y_offset = random.uniform(-0.2, 0.2)
                    self.blocks.append([x, y_offset, z])

        if not FloatingIsland.block_textures:
  
            texture_files = {
                'grass': 'grass.png',
                'netherrack': 'nether.png',
                'soul_sand': 'nether.png', 
                'end_stone': 'end.png',
                'obsidian': 'end.png',  
                'diamond': 'lapis.png',  
                'emerald': 'emerald.png',
                'gold': 'gold.png',
                'purple': 'purple.png'  
            }
            
            for block_name, filename in texture_files.items():
                try:
                    texture = load_texture(os.path.join("textures", filename))
                    FloatingIsland.block_textures[block_name] = texture
                except:
                    print(f"Warning: Could not load texture {filename}")
                 
                    size = 64
                    surface = pygame.Surface((size, size))
                    if block_name == 'grass':
                        surface.fill((34, 139, 34)) 
                    elif block_name == 'netherrack' or block_name == 'soul_sand':
                        surface.fill((20, 20, 20)) 
                    elif block_name == 'end_stone' or block_name == 'obsidian':
                        surface.fill((238, 232, 205))  
                    elif block_name == 'diamond':
                        surface.fill((0, 191, 255)) 
                    
                    texture_id = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    texture_data = pygame.image.tostring(surface, "RGBA", 1)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    FloatingIsland.block_textures[block_name] = texture_id
        

        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        self.create_island_geometry()
        glEndList()
    
    def create_island_geometry(self):
        glEnable(GL_TEXTURE_2D)
        
        for block in self.blocks:
            x, y, z = block
   
            scale = self.size * 0.9
            
            glPushMatrix()
            glTranslatef(x * scale, y * scale, z * scale)
            glScalef(scale, scale * 0.8, scale)  
            
   
            self.draw_textured_cube()
  
            if random.random() < 0.5: 
                glPushMatrix()
                glTranslatef(0, -0.5, 0)
                glScalef(0.3, random.uniform(0.3, 0.8), 0.3)
                self.draw_textured_cube(is_stalactite=True)
                glPopMatrix()
            
            glPopMatrix()
            
        glDisable(GL_TEXTURE_2D)
    
    def draw_textured_cube(self, is_stalactite=False):
        if is_stalactite:
       
            texture = FloatingIsland.block_textures[self.block_type]
        else:
            glEnable(GL_TEXTURE_2D)
            
            # Define vertices
            vertices = [
                [-0.5, -0.5, -0.5],  
                [0.5, -0.5, -0.5],   
                [0.5, 0.5, -0.5],  
                [-0.5, 0.5, -0.5],  
                [-0.5, -0.5, 0.5],  
                [0.5, -0.5, 0.5],   
                [0.5, 0.5, 0.5],    
                [-0.5, 0.5, 0.5]   
            ]
            
   
            uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
            
       
            faces = [
                ([0, 1, 2, 3], 'front'),  
                ([5, 4, 7, 6], 'front'),   
                ([1, 5, 6, 2], 'front'),    
                ([4, 0, 3, 7], 'front'),   
                ([3, 2, 6, 7], 'top'),     
                ([1, 0, 4, 5], 'bottom')   
            ]
            
            texture = FloatingIsland.block_textures[self.block_type]
            glBindTexture(GL_TEXTURE_2D, texture)
            
            for face, _ in faces:
                glBegin(GL_QUADS)
              
                v1 = vertices[face[1]]
                v2 = vertices[face[2]]
                v3 = vertices[face[0]]
                normal = [
                    (v2[1] - v1[1]) * (v3[2] - v1[2]) - (v2[2] - v1[2]) * (v3[1] - v1[1]),
                    (v2[2] - v1[2]) * (v3[0] - v1[0]) - (v2[0] - v1[0]) * (v3[2] - v1[2]),
                    (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
                ]
                glNormal3f(normal[0], normal[1], normal[2])
                
                for i, vertex_index in enumerate(face):
                    glTexCoord2f(uvs[i][0], uvs[i][1])
                    v = vertices[vertex_index]
                    glVertex3f(v[0], v[1], v[2])
                glEnd()
            
            glDisable(GL_TEXTURE_2D)
    
    def update(self, dt):
      
        self.hover_offset = self.hover_amplitude * math.sin(time.time() * self.hover_speed)
        
        if self.movement_type:
            self.movement_time += dt
            
            if self.movement_type == "circular":
  
                angle = self.movement_time * self.movement_speed
                self.center_pos[0] = self.original_pos[0] + math.cos(angle) * self.movement_amplitude
                self.center_pos[2] = self.original_pos[2] + math.sin(angle) * self.movement_amplitude
                
            elif self.movement_type == "horizontal":
        
                self.center_pos[0] = self.original_pos[0] + math.sin(self.movement_time * self.movement_speed) * self.movement_amplitude
                
            elif self.movement_type == "vertical":
      
                self.center_pos[1] = self.original_pos[1] + math.sin(self.movement_time * self.movement_speed) * self.movement_amplitude
                
            elif self.movement_type == "figure8":
            
                angle = self.movement_time * self.movement_speed
                self.center_pos[0] = self.original_pos[0] + math.sin(angle * 2) * self.movement_amplitude
                self.center_pos[2] = self.original_pos[2] + math.sin(angle) * self.movement_amplitude
    
    def draw(self):
        glPushMatrix()
       
        glTranslatef(
            self.center_pos[0],
            self.base_y + self.hover_offset,
            self.center_pos[2]
        )
        glCallList(self.display_list)
        glPopMatrix()
    
    def get_collision_boxes(self):
        boxes = []
        for block in self.blocks:
            x = self.center_pos[0] + block[0] * self.size * 0.9
            y = self.base_y + self.hover_offset + block[1] * self.size * 0.9
            z = self.center_pos[2] + block[2] * self.size * 0.9
            boxes.append([x, y, z])
        return boxes 