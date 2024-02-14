import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vert_arr_obj_name, texture_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        self.app = app
        self.pos = pos
        self.scale = scale
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.matrix_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vert_arr_obj = app.mesh.vert_arr_obj.vert_arr_objs[vert_arr_obj_name]
        self.program = self.vert_arr_obj.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        matrix_model = glm.mat4()
        # translate
        matrix_model = glm.translate(matrix_model, self.pos) 
        
        # rotate
        matrix_model = glm.rotate(matrix_model, self.rot.x, glm.vec3(1,0,0))
        matrix_model = glm.rotate(matrix_model, self.rot.y, glm.vec3(0,1,0))
        matrix_model = glm.rotate(matrix_model, self.rot.z, glm.vec3(0,0,1))
        
        # scale
        matrix_model = glm.scale(matrix_model, self.scale)
        return matrix_model

    def render(self):
        self.update()
        self.vert_arr_obj.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vert_arr_obj_name, texture_id, pos, rot, scale):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['matrix_view'].write(self.camera.matrix_view)
        self.program['matrix_model'].write(self.matrix_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        # mvp
        self.program['matrix_projection'].write(self.camera.matrix_projection)
        self.program['matrix_view'].write(self.camera.matrix_view)
        self.program['matrix_model'].write(self.matrix_model)
        
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        
class Cube(ExtendedBaseModel):
    def __init__(self, app, vert_arr_obj_name='cube', 
                 texture_id=0, pos=(0,0,0), 
                 rot=(0, 0, 0), scale=(1,1,1)):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
    
        
class Cat(ExtendedBaseModel):
    def __init__(self, app, vert_arr_obj_name='cat', 
                 texture_id='cat', pos=(0,0,0), 
                 rot=(0,0,0), scale=(1,1,1)):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
        self.on_init()
        
        
class Sphere(ExtendedBaseModel):
    def __init__(self, app, vert_arr_obj_name='sphere', 
                 texture_id='sphere', pos=(0,0,0), 
                 rot=(0,0,0), scale=(1,1,1)):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
        self.on_init()

class Skybox(ExtendedBaseModel):
    def __init__(self, app, vert_arr_obj_name='skybox', 
                 texture_id='skybox', pos=(0,0,0), 
                 rot=(0,0,0), scale=(1,1,1)):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
        self.on_init()
        
    def update(self):
        self.program['matrix_view'].write(glm.mat4(glm.mat3(self.camera.matrix_view)))
        
    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        
        # mvp
        self.program['matrix_projection'].write(self.camera.matrix_projection)
        self.program['matrix_view'].write(glm.mat4(glm.mat3(self.camera.matrix_view)))
        
class AdvancedSkybox(ExtendedBaseModel):
    def __init__(self, app, vert_arr_obj_name='advanced_skybox', 
                 texture_id='advanced_skybox', pos=(0,0,0), 
                 rot=(0,0,0), scale=(1,1,1)):
        super().__init__(app, vert_arr_obj_name, texture_id, pos, rot, scale)
        self.on_init()
        
    def update(self):
        matrix_view = glm.mat4(glm.mat3(self.camera.matrix_view))
        self.program['matrix_invProjView'].write(glm.inverse(self.camera.matrix_projection * matrix_view))
        
    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        