import bpy
import json

# Create a new armature object
bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
armature = bpy.context.object

# Switch to Edit mode to add bones
bpy.ops.object.mode_set(mode='EDIT')

# Load JSON file
with open(r"D:\Projects\MV-Pose-Detection\generated_data\static_pose_data.json") as f:
    bones_data = json.load(f)

bones_data = bones_data["bones"]

print(bones_data)
print(bones_data.items())

# Example bones with specific head and tail locations
#bones_data = {
#    "bone_1": {"head": (0, 0, 0), "tail": (0, 0, 1)},
#    "bone_2": {"head": (0, 0, 1), "tail": (0, 1, 2)},
#    "bone_3": {"head": (0, 1, 2), "tail": (0, 2, 3)},
#}

for bone_name, bone_info in bones_data.items():
    bone = armature.data.edit_bones.new(bone_name)
    bone.head = bone_info["head"]
    bone.tail = bone_info["tail"]

# Return to Object mode
bpy.ops.object.mode_set(mode='OBJECT')