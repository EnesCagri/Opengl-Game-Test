from OpenGL.GL import *
from OpenGL.GLUT import *
import time

class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.start_time = time.time()
        self.game_time = 0
        
    def add_points(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            
    def update(self):
        self.game_time = time.time() - self.start_time
        
    def draw(self):

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 600, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        

        glColor3f(1.0, 1.0, 1.0) 
        self.render_text(10, 30, f"Score: {self.score}")
        self.render_text(10, 60, f"High Score: {self.high_score}")
        
        minutes = int(self.game_time // 60)
        seconds = int(self.game_time % 60)
        self.render_text(10, 90, f"Time: {minutes:02d}:{seconds:02d}")
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
    def render_text(self, x, y, text):
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            
    def reset(self):
        self.score = 0
        self.start_time = time.time()
        self.game_time = 0 