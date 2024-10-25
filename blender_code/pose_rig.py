import bpy
import json
from mathutils import Vector

class PoseAnimationRig:
    def __init__(self, json_path):
        self.json_path = json_path
        self.pose_data = self.load_pose_data()
        self.armature = None
        self.scale_factor = 5.0  # Adjust based on the actual size needed

    def load_pose_data(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load pose data: {e}")

    def create_armature(self):
        # Clean up existing armatures
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='ARMATURE')
        bpy.ops.object.delete()

        # Create new armature
        bpy.ops.object.armature_add(enter_editmode=True)
        armature = bpy.context.active_object
        armature.name = "PoseRig"

        # Create bones based on landmark structure
        bones = armature.data.edit_bones
        for feature, idx in self.pose_data['frames'][0]['landmarks'].items():  # Use first frame data
            bone_name = feature
            bone = bones.new(bone_name)
            # Set bone positions initially to origin (or appropriate values)
            bone.head = Vector((0, 0, 0))
            bone.tail = Vector((0, 0, 0.1))  # Length of the bone

            print(f"Created bone: {bone_name} at head: {bone.head} tail: {bone.tail}")

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

        frames = self.pose_data['frames']
        for frame_data in frames:
            frame_num = frame_data['frame']
            bpy.context.scene.frame_set(frame_num)

            # Update the pose bones based on pose landmarks
            for feature, coords in frame_data['landmarks'].items():
                bone_name = feature
                if bone_name in self.armature.pose.bones:
                    bone = self.armature.pose.bones[bone_name]
                    location = Vector((
                        coords['x'] * self.scale_factor,
                        coords['y'] * self.scale_factor,
                        coords['z'] * self.scale_factor
                    ))
                    bone.location = location
                    bone.keyframe_insert(data_path="location", frame=frame_num)

                    print(f"Frame {frame_num}: Set {bone_name} to {location}")

        bpy.ops.object.mode_set(mode='OBJECT')
        print("Animation completed successfully!")

#Run this in Blender's text editor
json_path = r"D:\Projects\MV-Pose-Detection\pose_data.json"  # Update this path to where your json file is stored
animator = PoseAnimationRig(json_path)
animator.create_armature()
animator.animate_rig()