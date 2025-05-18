from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

class Island:
    def __init__(self, position, size, texture_type="grass"):
        self.position = np.array(position, dtype=np.float32)
        self.size = size
        self.texture_type = texture_type
        self.texture_id = None
        self.rotation = 0.0
        
    def load_texture(self):
        pass
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        
        glColor3f(0.2, 0.8, 0.2)  
        
        glBegin(GL_QUADS)
        glVertex3f(-self.size/2, 0, -self.size/2)
        glVertex3f(-self.size/2, 0, self.size/2)
        glVertex3f(self.size/2, 0, self.size/2)
        glVertex3f(self.size/2, 0, -self.size/2)
        glEnd()
        
   
        glBegin(GL_QUADS)

        glVertex3f(-self.size/2, -0.5, -self.size/2)
        glVertex3f(-self.size/2, 0, -self.size/2)
        glVertex3f(self.size/2, 0, -self.size/2)
        glVertex3f(self.size/2, -0.5, -self.size/2)
        
        glVertex3f(-self.size/2, -0.5, self.size/2)
        glVertex3f(-self.size/2, 0, self.size/2)
        glVertex3f(self.size/2, 0, self.size/2)
        glVertex3f(self.size/2, -0.5, self.size/2)
        
        glVertex3f(-self.size/2, -0.5, -self.size/2)
        glVertex3f(-self.size/2, 0, -self.size/2)
        glVertex3f(-self.size/2, 0, self.size/2)
        glVertex3f(-self.size/2, -0.5, self.size/2)
        
        glVertex3f(self.size/2, -0.5, -self.size/2)
        glVertex3f(self.size/2, 0, -self.size/2)
        glVertex3f(self.size/2, 0, self.size/2)
        glVertex3f(self.size/2, -0.5, self.size/2)
        glEnd()
        
        glPopMatrix()
        
    def get_bounding_box(self):
        return {
            'min': self.position - np.array([self.size/2, 0.5, self.size/2]),
            'max': self.position + np.array([self.size/2, 0.0, self.size/2])
        }
        
    def check_collision(self, player):
        island_box = self.get_bounding_box()
        player_box = player.get_bounding_box()
        
        return (
            player_box['min'][0] <= island_box['max'][0] and
            player_box['max'][0] >= island_box['min'][0] and
            player_box['min'][1] <= island_box['max'][1] and
            player_box['max'][1] >= island_box['min'][1] and
            player_box['min'][2] <= island_box['max'][2] and
            player_box['max'][2] >= island_box['min'][2]
        ) 