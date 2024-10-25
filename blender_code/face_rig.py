import bpy
import json
from mathutils import Vector

class FacialAnimationRig:
    def __init__(self, json_path):
        self.json_path = json_path
        self.face_data = self.load_face_data()
        self.armature = None
        self.scale_factor = 5.0

    def load_face_data(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load face data: {e}")

    def create_armature(self):
        # Clean up existing armatures
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='ARMATURE')
        bpy.ops.object.delete()

        # Create new armature
        bpy.ops.object.armature_add(enter_editmode=True)
        armature = bpy.context.active_object
        armature.name = "FaceRig"

        # Create bones based on landmark structure
        bones = armature.data.edit_bones
        landmark_indices = self.face_data['metadata']['landmark_indices']

        for feature, positions in landmark_indices.items():
            for position in positions:
                bone_name = f"{feature}_{position}"
                bone = bones.new(bone_name)
                bone.head = Vector((0, 0, 0))
                bone.tail = Vector((0, 0, 0.1))

        bpy.ops.object.mode_set(mode='OBJECT')
        self.armature = armature
        return armature

    def animate_rig(self):
        if not self.armature:
            raise RuntimeError("Armature not created yet")

        bpy.context.view_layer.objects.active = self.armature
        bpy.ops.object.mode_set(mode='POSE')

        # Clear existing animation
        if self.armature.animation_data:
            self.armature.animation_data_clear()

        frames = self.face_data['frames']
        for frame_data in frames:
            frame_num = frame_data['frame']
            bpy.context.scene.frame_set(frame_num)

            for feature, positions in frame_data['landmarks'].items():
                for position, coords in positions.items():
                    bone_name = f"{feature}_{position}"
                    if bone_name in self.armature.pose.bones:
                        bone = self.armature.pose.bones[bone_name]
                        location = Vector((
                            coords['x'] * self.scale_factor,
                            coords['y'] * self.scale_factor,
                            coords['z'] * self.scale_factor
                        ))
                        bone.location = location
                        bone.keyframe_insert(data_path="location", frame=frame_num)

        bpy.ops.object.mode_set(mode='OBJECT')
        print("Animation completed successfully!")

# Run this in Blender's text editor
json_path = r"D:\Projects\MV-Pose-Detection\face_data.json"  # Update this path
animator = FacialAnimationRig(json_path)
animator.create_armature()
animator.animate_rig()