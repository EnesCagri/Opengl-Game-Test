import math
from utils import normalize_vector

def normalize_vector(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length > 0:
        return [v[0]/length, v[1]/length, v[2]/length]
    return v

class Camera:
    def __init__(self):
        self.distance = 5.0
        self.rotation = 0.0
        self.pitch = 30.0
        self.sensitivity = 0.2
        self.min_pitch = -89.0
        self.max_pitch = 89.0
        
    def update(self, mouse_dx, mouse_dy):
        self.rotation -= mouse_dx * self.sensitivity
        self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch - mouse_dy * self.sensitivity))
        
    def get_position(self, target_pos):
        rad_rotation = math.radians(self.rotation)
        rad_pitch = math.radians(self.pitch)
        
        x = target_pos[0] + self.distance * math.cos(rad_pitch) * math.sin(rad_rotation)
        y = target_pos[1] + self.distance * math.sin(rad_pitch)
        z = target_pos[2] + self.distance * math.cos(rad_pitch) * math.cos(rad_rotation)
        
        return [x, y, z]
        
    def get_forward(self):
        rad_rotation = math.radians(self.rotation)
        rad_pitch = math.radians(self.pitch)
        
        x = math.cos(rad_pitch) * math.sin(rad_rotation)
        y = math.sin(rad_pitch)
        z = math.cos(rad_pitch) * math.cos(rad_rotation)
        
        return normalize_vector([x, y, z]) 