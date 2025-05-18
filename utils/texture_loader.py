from OpenGL.GL import *
from PIL import Image
import os

def load_texture(filename):
    """Load a texture from file and return the texture ID."""
    try:
        image = Image.open(filename)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        
        width, height = image.size
        
        # Generate texture ID
        texture_id = glGenTextures(1)
        
        # Bind texture
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # Upload texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        return texture_id
        
    except Exception as e:
        print(f"Error loading texture {filename}: {e}")
        return None

def load_textures(texture_dir):
    """Load all textures from a directory and return a dictionary of texture IDs."""
    textures = {}
    
    # Create textures directory if it doesn't exist
    if not os.path.exists(texture_dir):
        os.makedirs(texture_dir)
        
    # Load each texture file in the directory
    for filename in os.listdir(texture_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            texture_path = os.path.join(texture_dir, filename)
            texture_name = os.path.splitext(filename)[0]
            textures[texture_name] = load_texture(texture_path)
            
    return textures

def bind_texture(texture_id):
    """Bind a texture for rendering."""
    if texture_id is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    else:
        glDisable(GL_TEXTURE_2D) 