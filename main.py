import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time
import random
import os

from player import Player, CUBE_SIZE, PLAYER_RADIUS
from camera import Camera
from portal import Portal
from coin import Coin
from floating_island import FloatingIsland

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FOV = 45.0
NEAR_CLIP = 0.1
FAR_CLIP = 100.0
GRID_SIZE = 10  

class Game:
    def __init__(self):
        self.player = Player([0, 2, 0])
        self.camera = Camera()
        self.mouse_sensitivity = 0.2
        self.level_index = 1
        
        self.level_start_positions = {
            1: [0, 2, 0], 
            2: [0, 4, 0],   
            3: [0, 2, 0],  
            4: [0, 2, 0]    
        }
        
        self.levels = {
            1: self.generate_earth_level(),   
            2: self.generate_nether_level(),  
            3: self.generate_end_level(),     
            4: self.generate_diamond_level()   
        }
        self.islands = self.levels[self.level_index]['islands']
        self.portal = self.levels[self.level_index]['portal']
        self.coins = self.levels[self.level_index]['coins']
        
        self.sky_colors = {
            1: (0.5, 0.7, 1.0, 1.0),  
            2: (0.3, 0.1, 0.1, 1.0), 
            3: (0.1, 0.1, 0.2, 1.0), 
            4: (0.2, 0.5, 0.8, 1.0)  
        }
        
        self.screen = pygame.display.get_surface()
        
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 48)
        
        self.level_start_time = time.time()
        self.best_times = {1: float('inf'), 2: float('inf'), 3: float('inf'), 4: float('inf')}
        self.current_time = 0.0
        
        self.coins_collected = 0  
        self.total_coins = sum(1 for coin in self.coins if not coin.collected)
        self.total_score = 0  

    def init_gl(self):
        glClearColor(*self.sky_colors[self.level_index])
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 15, 5, 1))  
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1)) 
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))  
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))  
        
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.3, 0.3, 0.3, 1.0))

    def generate_earth_level(self):
        islands = []
        
        start_island = FloatingIsland([0, 0, 0], size=1.5)
        islands.append(start_island)
        
        current_x = 0
        current_z = 0
        
        for i in range(4):
            current_x += 4
            current_z += random.uniform(0.5, 1.5)
            movement = "horizontal" if i == 2 else None
            islands.append(FloatingIsland([current_x, 0, current_z], movement_type=movement))
        
        for i in range(3):
            current_x += 4
            current_z += random.uniform(-1, 1)
            height = i * 2
            movement = "vertical" if i == 1 else None
            islands.append(FloatingIsland([current_x, height, current_z], movement_type=movement))
        
        portal = Portal(
            [current_x + 4, 6, current_z],
            2, 
            [0, 5, 0],
            90  
        )
        
        coins = self.generate_coins(islands[1:-1])
        
        coins.append(Coin([0, 4, 0])) 
        
        mid_x = current_x / 2
        mid_z = current_z / 2
        coins.append(Coin([mid_x, 3, mid_z])) 
        
        return {'islands': islands, 'portal': portal, 'coins': coins}

    def generate_nether_level(self):
        islands = []
        
        spawn_platform = FloatingIsland([0, 0, 0], size=2.0, block_type="netherrack")
        islands.append(spawn_platform)
        
        for x in range(-2, 3):
            for z in range(-2, 3):
                if abs(x) <= 0 and abs(z) <= 0:
                    continue
                    
                if random.random() < 0.7:  
                    movement = "circular" if random.random() < 0.3 else None
                    islands.append(FloatingIsland([x * 4, random.uniform(-1, 1), z * 4], 
                                                movement_type=movement, 
                                                block_type="netherrack"))
  
        for _ in range(5):
            x = random.uniform(-10, 10)
            z = random.uniform(-10, 10)
            y = random.uniform(2, 4)
      
            if abs(x) < 3 and abs(z) < 3:
                continue
            movement = "horizontal" if random.random() < 0.5 else "vertical"
            islands.append(FloatingIsland([x, y, z], 
                                        movement_type=movement, 
                                        block_type="netherrack"))
        
     
        portal = Portal(
            [8, 3, 8], 
            3,  
            [0, 2, 0],
            90 
        )
        

        coins = []
        for island in islands[1:]:  
            if random.random() < 0.7: 
                coin_pos = [
                    island.center_pos[0],
                    island.base_y + 2, 
                    island.center_pos[2]
                ]
                coins.append(Coin(coin_pos, texture_type="lapis"))
        
        return {'islands': islands, 'portal': portal, 'coins': coins}

    def generate_end_level(self):
        islands = []
        
        center_x = 0
        center_z = 0
        radius = 3
        
        for i in range(20):
            angle = i * 0.5
            x = center_x + math.cos(angle) * radius * i * 0.3
            z = center_z + math.sin(angle) * radius * i * 0.3
            y = i * 0.5 
            
            movement = "figure8" if i % 5 == 0 else None
            islands.append(FloatingIsland([x, y, z], movement_type=movement, block_type="emerald"))
        
        for _ in range(5):
            x = random.uniform(-15, 15)
            z = random.uniform(-15, 15)
            y = random.uniform(5, 10)
            islands.append(FloatingIsland([x, y, z], block_type="emerald"))
        
        portal = Portal(
            [x, y + 2, z], 
            4, 
            [0, 2, 0],
            270 
        )
        
        coins = []
        for island in islands:
            if random.random() < 0.7: 
                coin_pos = [
                    island.center_pos[0],
                    island.base_y + 2, 
                    island.center_pos[2]
                ]
                coins.append(Coin(coin_pos, texture_type="emerald"))
        
        return {'islands': islands, 'portal': portal, 'coins': coins}

    def generate_diamond_level(self):
        islands = []
        coins = []
        
        grid_size = 10
        spacing = 3.0
        start_offset = -(grid_size * spacing) / 2
        
        for x in range(grid_size):
            for z in range(grid_size):
                pos_x = start_offset + (x * spacing)
                pos_z = start_offset + (z * spacing)
                
                height = math.sin(x * 0.5) * math.cos(z * 0.5) * 2
                
                movement = None
                if (x + z) % 4 == 0:
                    movement = random.choice(["circular", "figure8", "vertical"])
                
                islands.append(FloatingIsland([pos_x, height, pos_z], size=1.0, movement_type=movement, block_type="purple"))
        
      
        portal = Portal(
            [5, 5, 5],  
            0,  
            [0, 0, 0],
            270 
        )
        
        pattern_positions = [
            (3,3), (3,4), (3,5), (3,6),  
            (5,3), (5,4), (5,5), (5,6),  
            (7,3), (7,4), (7,5), (7,6),  
            (8,4), (8,5),
            (9,3), (9,6)
        ]
        
        for x, z in pattern_positions:
            pos_x = start_offset + (x * spacing)
            pos_z = start_offset + (z * spacing)
            height = math.sin(x * 0.5) * math.cos(z * 0.5) * 2
            coins.append(Coin([pos_x, height + 3, pos_z]))
        
        return {'islands': islands, 'portal': portal, 'coins': coins}

    def generate_coins(self, islands):
        coins = []
        for island in islands:
            if random.random() < 0.7:  
                coin_pos = [
                    island.center_pos[0],
                    island.base_y + 2,  
                    island.center_pos[2]
                ]
                coins.append(Coin(coin_pos))
        return coins

    def check_portal_collision(self):
        if self.portal:
            current_time = time.time()
            
            dx = self.player.position[0] - self.portal.position[0]
            dy = self.player.position[1] - self.portal.position[1]
            dz = self.player.position[2] - self.portal.position[2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
          
            self.debug_info = {
                'distance': distance,
                'portal_radius': self.portal.radius,
                'player_pos': self.player.position,
                'portal_pos': self.portal.position,
            }
            
         
            collision_threshold = self.portal.radius + self.player.radius
            

            if distance < collision_threshold:
                if self.coins_collected < 5:
         
                    return False
                    
                if self.level_index == 4 and self.portal.target_level == 0:
                    print("Congratulations! Game completed!")
                    pygame.quit()
                    sys.exit()
                    return True
                
                print(f"Portal triggered! Moving to level {self.portal.target_level}")
                
            
                level_time = current_time - self.level_start_time
                if level_time < self.best_times[self.level_index]:
                    self.best_times[self.level_index] = level_time
                
                self.total_score += self.coins_collected
                
                target_level = self.portal.target_level
                
                self.level_index = target_level
                level_data = self.levels[self.level_index]
                self.islands = level_data['islands']
                self.portal = level_data['portal']
                self.coins = level_data['coins']
                
                self.player = Player(self.level_start_positions[target_level])
                self.camera = Camera()
                
                glClearColor(*self.sky_colors[self.level_index])
                
                self.level_start_time = current_time
                self.coins_collected = 0
                self.total_coins = sum(1 for coin in self.coins if not coin.collected)
                
                # Reset player's coin collection state
                self.player.coins_collected = 0
                self.player.current_color = self.player.color_states[0].copy()
                self.player.target_color = self.player.color_states[0].copy()
                self.player.glow_intensity = 0.0
                
                return True
        return False
        
    def draw_ui_panel(self, surface, x, y, width, height):
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180)) 
        surface.blit(panel, (x, y))
        
    def draw_debug_info(self):
        if not hasattr(self, 'debug_info'):
            return
            
        texts = [
            f"Distance to portal: {self.debug_info['distance']:.2f}",
            f"Player pos: ({self.debug_info['player_pos'][0]:.1f}, {self.debug_info['player_pos'][1]:.1f}, {self.debug_info['player_pos'][2]:.1f})",
            f"Portal pos: ({self.debug_info['portal_pos'][0]:.1f}, {self.debug_info['portal_pos'][1]:.1f}, {self.debug_info['portal_pos'][2]:.1f})"
        ]
        
        text_height = 25
        panel_padding = 10
        panel_width = 400
        panel_height = (len(texts) * text_height) + (panel_padding * 2)
        
        panel_x = 10
        panel_y = WINDOW_HEIGHT - panel_height - 10
        
        self.draw_ui_panel(self.screen, panel_x, panel_y, panel_width, panel_height)
        
        y = panel_y + panel_padding
        for text in texts:
            text_surface = self.font.render(text, True, (200, 200, 200)) 
            self.screen.blit(text_surface, (panel_x + panel_padding, y))
            y += text_height
        
    def draw_scoreboard(self):
        self.current_time = time.time() - self.level_start_time
        
        if self.level_index == 4 and self.portal.target_level == 0:
            texts = [
                "Final Level",
                f"Coins: {self.coins_collected}/{self.total_coins}",
                "Collect 5 coins and",
                "enter the portal",
                "to complete the game!"
            ]
        else:
            texts = [
                f"Level {self.level_index}",
                f"Time: {self.current_time:.2f}s",
                f"Best: {self.best_times[self.level_index]:.2f}s" if self.best_times[self.level_index] != float('inf') else "Best: --:--",
                f"Coins: {self.coins_collected}/{self.total_coins}",
                f"Need 5 coins for portal!"
            ]

        text_height = 35
        panel_padding = 15
        panel_width = 250
        panel_height = (len(texts) * text_height) + (panel_padding * 2)
        
        panel_x = WINDOW_WIDTH - panel_width - 10
        panel_y = 10

        self.draw_ui_panel(self.screen, panel_x, panel_y, panel_width, panel_height)
        
        y = panel_y + panel_padding
        for i, text in enumerate(texts):
            if "Need 5 coins" in text:
                color = (0, 255, 0) if self.coins_collected >= 5 else (255, 50, 50)
            else:
                color = (255, 255, 0) 
            
            text_surface = self.large_font.render(text, True, color)
            x = panel_x + (panel_width - text_surface.get_width()) // 2
            self.screen.blit(text_surface, (x, y))
            y += text_height
            
    def draw_winning_message(self):
        if self.level_index == 5:  
            messages = [
                "Congratulations!",
                "You've completed all levels!",
                f"Total coins collected: {self.coins_collected}",
                "Enter the final portal",
                "to complete your journey!"
            ]
            
            text_height = 40
            panel_padding = 20
            panel_width = 500
            panel_height = (len(messages) * text_height) + (panel_padding * 2)
            
            panel_x = (WINDOW_WIDTH - panel_width) // 2
            panel_y = (WINDOW_HEIGHT - panel_height) // 2
            
            self.draw_ui_panel(self.screen, panel_x, panel_y, panel_width, panel_height)
            
            y = panel_y + panel_padding
            for message in messages:
                text_surface = self.large_font.render(message, True, (255, 255, 0))
                x = panel_x + (panel_width - text_surface.get_width()) // 2
                self.screen.blit(text_surface, (x, y))
                y += text_height

    def draw_total_score(self):
        panel_padding = 15
        panel_width = 200
        panel_height = 50
        
        panel_x = 10
        panel_y = 10
        
        self.draw_ui_panel(self.screen, panel_x, panel_y, panel_width, panel_height)
        
        score_text = f"Score: {self.total_score}"
        text_surface = self.large_font.render(score_text, True, (255, 255, 0)) 
        
        x = panel_x + panel_padding
        y = panel_y + (panel_height - text_surface.get_height()) // 2
        
        self.screen.blit(text_surface, (x, y))

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        camera_pos = self.camera.get_position(self.player.position)
        
        gluLookAt(
            camera_pos[0], camera_pos[1], camera_pos[2],
            self.player.position[0], self.player.position[1], self.player.position[2],
            0, 1, 0
        )

        self.player.draw()

        for island in self.islands:
            island.draw()

        for coin in self.coins:
            coin.draw()

        if self.portal:
            self.portal.draw(self.coins_collected)
        

        glPushMatrix()
        if self.level_index == 1:
            glColor3f(0.2, 0.2, 0.3) 
        elif self.level_index == 2:
            glColor3f(0.3, 0.1, 0.1) 
        elif self.level_index == 3:
            glColor3f(0.1, 0.3, 0.1) 
        elif self.level_index == 4:
            glColor3f(0.4, 0.6, 0.8) 
        
        glBegin(GL_QUADS)
        glVertex3f(-50, -20, -50)
        glVertex3f(-50, -20, 50)
        glVertex3f(50, -20, 50)
        glVertex3f(50, -20, -50)
        glEnd()
        glPopMatrix()
        
    
        pygame.display.flip()  
        self.draw_debug_info()
        self.draw_scoreboard()
        self.draw_total_score()  
        pygame.display.flip() 
        
    def handle_input(self):
        keys = pygame.key.get_pressed()

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        self.camera.update(mouse_dx * self.mouse_sensitivity, mouse_dy * self.mouse_sensitivity)

        self.player.update_movement(keys, self.camera.get_forward(), 0.016)
        
        if keys[K_SPACE]:
            self.player.jump()

    def update(self):
        collision_boxes = []
        for island in self.islands:
            island.update(0.016)
            collision_boxes.extend(island.get_collision_boxes())
        
        self.player.update(0.016, collision_boxes)
        
        for coin in self.coins:
            coin.update(0.016)
            if coin.check_collection(self.player.position):
                self.coins_collected += 1
                self.player.collect_coin()
        
        self.check_portal_collision()

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sky Island Hopper")
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    game = Game()
    game.init_gl()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, (display[0]/display[1]), NEAR_CLIP, FAR_CLIP)
    glMatrixMode(GL_MODELVIEW)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
        
        game.handle_input()
        
        game.update()
        
        game.draw_scene()

        pygame.display.flip()
        pygame.time.wait(10)
        
    pygame.quit()

if __name__ == "__main__":
    main() 