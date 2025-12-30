# Blender Proximity Shader

A Blender project demonstrating proximity-based shading using the Vector Transform node.

## Objective

Create a reusable system in Blender that changes the shading of a "Target" object based on its distance to an "Influencer" object. The core of this system is a shading network that leverages the **Vector Transform** node to correctly calculate the distance between objects by converting their position vectors into a common coordinate space.

## Features

- Python script (`create_proximity_shader.py`) that automatically creates two mesh objects: a "Target" (sphere) and an "Influencer" (cube).
- Generates a material for the "Target" object with a shading network using Vector Transform node.
- Calculates distance between objects and drives a color change (red when far, green when close).
- Includes demonstration `.blend` file (`proximity_demo.blend`) showing the final setup.

## How to Use

1. Open Blender and go to the Scripting workspace.
2. Open `create_proximity_shader.py` and run the script.
3. The script will create the objects and material automatically.
4. Move the Influencer object to see the Target's color change based on distance.

## Implementation Details

The distance calculation is performed in World Space to ensure consistency regardless of object transformations. The Vector Transform node converts the Influencer's object-space location to world space, then a Vector Math node (Distance) computes the distance to the Target's world position.

## License

MIT