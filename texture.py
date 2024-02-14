import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/wood.png')
        self.textures[1] = self.get_texture(path='textures/steel.png')
        self.textures[2] = self.get_texture(path='textures/gold.png')
        self.textures['model'] = self.get_texture(path='textures/cardiac.png')

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotrophy=32.0
        return texture

    def destroy(self):
        [texture.release() for texture in self.textures.values()]