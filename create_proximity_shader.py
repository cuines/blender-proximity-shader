"""
Create a proximity-based shader in Blender using Vector Transform node.
This script creates a Target sphere and an Influencer cube, and sets up a material
that changes color based on distance between them.
Run this script in Blender's Scripting workspace.
"""

import bpy
import bmesh

def clear_scene():
    """Remove default objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_target():
    """Create a sphere as the Target object."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
    target = bpy.context.active_object
    target.name = "Target"
    return target

def create_influencer():
    """Create a cube as the Influencer object."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(3, 0, 0))
    influencer = bpy.context.active_object
    influencer.name = "Influencer"
    return influencer

def create_proximity_material(target, influencer):
    """Create a material for the Target that changes color based on distance to Influencer."""
    # Create a new material
    mat = bpy.data.materials.new(name="ProximityMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create necessary nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (600, 0)
    
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (400, 0)
    
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    color_ramp_node.location = (200, 0)
    color_ramp_node.color_ramp.interpolation = 'LINEAR'
    # Set colors: red at position 0, green at position 1
    color_ramp_node.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp_node.color_ramp.elements[0].position = 0.0
    color_ramp_node.color_ramp.elements[1].color = (0.0, 1.0, 0.0, 1.0)  # Green
    color_ramp_node.color_ramp.elements[1].position = 1.0
    
    # Vector Math node to compute distance
    vector_math_node = nodes.new(type='ShaderNodeVectorMath')
    vector_math_node.location = (0, 0)
    vector_math_node.operation = 'DISTANCE'
    
    # Geometry node to get Target's world position
    geometry_node = nodes.new(type='ShaderNodeNewGeometry')
    geometry_node.location = (-200, 100)
    
    # Object Info node to get Influencer's location
    object_info_node = nodes.new(type='ShaderNodeObjectInfo')
    object_info_node.location = (-200, -100)
    object_info_node.object = influencer  # Link to Influencer object
    
    # Vector Transform node to convert Influencer's location to world space
    vector_transform_node = nodes.new(type='ShaderNodeVectorTransform')
    vector_transform_node.location = (-400, -100)
    vector_transform_node.vector_type = 'POINT'
    vector_transform_node.convert_from = 'OBJECT'
    vector_transform_node.convert_to = 'WORLD'
    
    # Connect nodes
    # Vector Transform takes Object Info's location (object space) and outputs world space
    links.new(object_info_node.outputs['Location'], vector_transform_node.inputs['Vector'])
    # Distance between Target's world position (Geometry) and Influencer's world position (Vector Transform)
    links.new(geometry_node.outputs['Position'], vector_math_node.inputs[0])
    links.new(vector_transform_node.outputs['Vector'], vector_math_node.inputs[1])
    # Distance drives ColorRamp factor (normalized by a mapping node)
    # We'll use a Map Range node to map distance to 0-1 range
    map_range_node = nodes.new(type='ShaderNodeMapRange')
    map_range_node.location = (0, -200)
    map_range_node.inputs['From Min'].default_value = 0.0
    map_range_node.inputs['From Max'].default_value = 10.0  # Distance range up to 10 units
    map_range_node.inputs['To Min'].default_value = 0.0
    map_range_node.inputs['To Max'].default_value = 1.0
    map_range_node.clamp = True
    links.new(vector_math_node.outputs['Value'], map_range_node.inputs['Value'])
    links.new(map_range_node.outputs['Result'], color_ramp_node.inputs['Fac'])
    # ColorRamp output to BSDF base color
    links.new(color_ramp_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    # BSDF to output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Assign material to target
    if target.data.materials:
        target.data.materials[0] = mat
    else:
        target.data.materials.append(mat)
    
    return mat

def main():
    """Main function to set up the scene."""
    # Clear default scene (optional)
    # clear_scene()  # Uncomment if you want a clean scene
    
    # Create objects
    target = create_target()
    influencer = create_influencer()
    
    # Create proximity material
    create_proximity_material(target, influencer)
    
    # Print instructions
    print("Proximity shader setup complete!")
    print("Move the 'Influencer' cube to see the 'Target' sphere change color.")
    print("Distance range is mapped from 0-10 units to red (far) to green (near).")
    
    # Optionally save the blend file
    # bpy.ops.wm.save_as_mainfile(filepath="proximity_demo.blend")

if __name__ == "__main__":
    main()