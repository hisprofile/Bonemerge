bl_info = {
    "name" : "Bonemerge for Blender",
    "description" : "Attaches cosmetics to a TF2 Character",
    "author" : "hisanimations",
    "version" : (1, 2),
    "blender" : (3, 0, 0),
    "location" : "View3d > Bonemerge",
    "support" : "COMMUNITY",
    "category" : "Rigging",
}

import bpy

loc = "BONEMERGE-ATTACH-LOC"
rot = "BONEMERGE-ATTACH-ROT"
    
classes = []

bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Armature)

class NULLSNAP(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "Bonemerge"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bonemerge"
    bl_icon = "BONE_DATA"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        
        row.label(text='Attach TF2 cosmetics.', icon='MOD_CLOTH')
        ob = context.object
        row = layout.row()
        self.layout.prop_search(context.scene, "target", bpy.data, "armatures", text="Link to")
        
        row = layout.row()
        row.operator('hisanim.attachto', icon="LINKED")
        row=layout.row()
        row.operator('hisanim.detachfrom', icon="UNLINKED")
        


class ATTACH(bpy.types.Operator):
    bl_idname = "hisanim.attachto"
    bl_label = "Attach"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        if context.scene.target == None:
            raise TypeError("\n\nNo armature selected!")
        obj = context.scene.target.name
    
        
        for i in bpy.context.selected_objects:
            if i.name == obj:
                continue
            if i.type == 'MESH':
                i = i.parent
            for ii in i.pose.bones:
                try:
                    bpy.data.objects[obj].pose.bones[ii.name]
                except:
                    continue
                
                try:
                    ii.constraints[loc]
                    pass
                except:
                    ii.constraints.new('COPY_LOCATION').name = loc
                    ii.constraints.new('COPY_ROTATION').name = rot
                
                
                ii.constraints[loc].target = bpy.data.objects[obj]
                ii.constraints[loc].subtarget = ii.name
                ii.constraints[rot].target = bpy.data.objects[obj]
                ii.constraints[rot].subtarget = ii.name
        
        return {'FINISHED'}
    
class DETACH(bpy.types.Operator):
    bl_idname = "hisanim.detachfrom"
    bl_label = "Detach"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                i = i.parent
            for ii in i.pose.bones:
                try:
                    ii.constraints.remove(ii.constraints[loc])
                    ii.constraints.remove(ii.constraints[rot])
                except:
                    continue
        
        return {'FINISHED'}
    
classes.append(ATTACH)
classes.append(DETACH)

classes.append(NULLSNAP)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()