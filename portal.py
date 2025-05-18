import math
from OpenGL.GL import *
import time

class Portal:
    def __init__(self, position, target_level, target_position, orientation=0):
        self.position = position
        self.target_level = target_level
        self.target_position = target_position
        self.radius = 2.0  
        self.rotation = 0  
        self.rotation_speed = 180.0  
        self.orientation = orientation  

    def draw(self, coins_collected=0):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        glRotatef(self.orientation, 0, 1, 0)
        
        self.rotation += self.rotation_speed * 0.016 
        if self.rotation >= 360:
            self.rotation -= 360
            
  
        for i in range(5):
            depth = i * 0.05 
            scale = 1.0 - (i * 0.15)  
            
            glPushMatrix()
            glTranslatef(0, 0, -depth)
            glRotatef(self.rotation + (i * 30), 0, 0, 1) 

            if coins_collected < 5:  
                glMaterialfv(GL_FRONT, GL_EMISSION, [0.5, 0.0, 0.0, 1.0]) 
                glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.0, 0.0, 1.0])
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
            else:  
                glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.0, 0.5, 1.0])  
                glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.0, 0.4, 1.0])
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.0, 1.0, 1.0])
            
            glBegin(GL_TRIANGLE_FAN)
            if coins_collected < 5:
                glColor4f(1.0, 0.0, 0.0, 0.9) 
            else:
                glColor4f(0.5, 0.0, 1.0, 0.9) 
            glVertex3f(0, 0, 0)  
            
            segments = 32
            for j in range(segments + 1):
                angle = (j / segments) * 2 * math.pi
                r = self.radius * scale

                r += 0.2 * math.sin(angle * 3 + self.rotation * math.pi / 180)
                x = r * math.cos(angle)
                y = r * math.sin(angle)

                if coins_collected < 5:
                    glColor4f(0.5, 0.0, 0.0, 0.7)  
                else:
                    glColor4f(0.0, 0.5, 1.0, 0.7)  
                glVertex3f(x, y, 0)
            glEnd()
            
            glPopMatrix()
        

        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        
        glPopMatrix()
        
    def get_bounding_box(self):
        return {
            'min': self.position - np.array([self.radius, self.radius, 0.1]),
            'max': self.position + np.array([self.radius, self.radius, 0.1])
        }
        
    def check_collision(self, player):
        portal_box = self.get_bounding_box()
        player_box = player.get_bounding_box()
        
        return (
            player_box['min'][0] <= portal_box['max'][0] and
            player_box['max'][0] >= portal_box['min'][0] and
            player_box['min'][1] <= portal_box['max'][1] and
            player_box['max'][1] >= portal_box['min'][1] and
            player_box['min'][2] <= portal_box['max'][2] and
            player_box['max'][2] >= portal_box['min'][2]
        )
        
    def activate(self):
        return self.target_level, self.target_position 