from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from island import Island
from coin import Coin
from portal import Portal

class SceneManager:
    def __init__(self):
        self.current_scene = 0
        self.scenes = []
        self.setup_scenes()
        
    def setup_scenes(self):
       
        scene1 = {
            'islands': [
                Island([0, 0, 0], 4.0),  
                Island([4, 0, 4], 3.0),  
                Island([8, 0, 0], 3.0), 
            ],
            'coins': [
                Coin([4, 1, 4]),  
            ],
            'portals': [
                Portal([8, 8, 8], 1), 
            ]
        }
        

        scene2 = {
            'islands': [
                Island([0, 0, 0], 3.0), 
                Island([3, 0, 3], 2.0),  
                Island([6, 0, 0], 2.0),  
                Island([9, 0, 3], 2.0),  
                Island([12, 0, 0], 3.0),  
            ],
            'coins': [
                Coin([3, 1, 3]),
                Coin([6, 1, 0]),
                Coin([9, 1, 3]),
            ],
            'portals': [
                Portal([12, 1, 0], 2), 
            ]
        }
        
        scene3 = {
            'islands': [
                Island([0, 0, 0], 3.0),  
                Island([4, 0, 4], 2.0),  
                Island([8, 0, 0], 2.0),  
                Island([12, 0, 4], 2.0),  
                Island([16, 0, 0], 2.0),  
                Island([20, 0, 4], 3.0),  
            ],
            'coins': [
                Coin([4, 1, 4]),
                Coin([8, 1, 0]),
                Coin([12, 1, 4]),
                Coin([16, 1, 0]),
                Coin([20, 1, 4]),
            ],
            'portals': [
                Portal([20, 1, 4], 0),  
            ]
        }
        
        self.scenes = [scene1, scene2, scene3]
        
    def get_current_scene(self):
        return self.scenes[self.current_scene]
        
    def change_scene(self, scene_index):
        if 0 <= scene_index < len(self.scenes):
            self.current_scene = scene_index
            return True
        return False
        
    def update(self, delta_time):
        current_scene = self.get_current_scene()
        
        for island in current_scene['islands']:
            island.update(delta_time)
            
        for coin in current_scene['coins']:
            coin.update(delta_time)
            
        for portal in current_scene['portals']:
            portal.update(delta_time)
            
    def draw(self):
        current_scene = self.get_current_scene()
        
        for island in current_scene['islands']:
            island.draw()
            
        for coin in current_scene['coins']:
            coin.draw()
            
        for portal in current_scene['portals']:
            portal.draw()
            
    def check_collisions(self, player):
        current_scene = self.get_current_scene()
        score_change = 0
        scene_change = None

        for coin in current_scene['coins']:
            if coin.check_collision(player):
                coin.collect()
                score_change += coin.value

        for portal in current_scene['portals']:
            if portal.check_collision(player):
                scene_change = portal.activate()
                
        return score_change, scene_change 