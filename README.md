# SciBlend: Grid Generator for Blender v.2.0.0

This script is an add-on for Blender 4.2 that allows users to create customizable 3D and 2D grids with numbered nodes and adjustable edges. It's a powerful tool for scientific visualization, data representation, and spatial analysis in three-dimensional and two-dimensional space.

![Advanced 3D Grid Example](media/1.png)


## Table of Contents

1. [Requirements](#requirements)
2. [Features](#features)
3. [Install the Add-on](#install-the-add-on)
4. [Usage](#usage)
   - [Accessing the Add-on Panel](#1-accessing-the-add-on-panel)
   - [Configuring Your Grid](#2-configuring-your-grid)
   - [Generating the Grid](#3-generating-the-grid)
   - [Customizing Appearance](#4-customizing-appearance)
   - [Working with the Result](#5-working-with-the-result)
5. [Tips for Best Results](#tips-for-best-results)
6. [Contributing](#contributing)

## Requirements

Before installing Blender and the add-on, ensure that you meet the following requirements:

1. **Operating System**: 
    - Any OS that supports Blender 4.2 (Windows, macOS, Linux)
  
2. **Blender**:
    - Blender 4.2 or higher

3. **Python**:
    - Python 3.11 (bundled with Blender 4.2)

## Features

- **Multiple Grid Types**: Choose between five different modes: Cubic with Internal Edges, Cubic with Exterior Edges Only, Cubic with Exterior Edges and Subdivisions, 2D Grid, and 2D Grid with Subdivisions.

- **Flexible Units**: Support for a wide range of units from nanometers to kilometers.
- **2D Grid Orientation**: Ability to orient 2D grids on different planes (XY, XZ, YZ, and their negatives).
- **Numbered Nodes**: Option to display coordinate numbers at each grid point, with customizable display axes for 2D grids.
- **Adjustable Edges**: Create visible edges with customizable thickness that scales with the chosen unit.
- **Text Customization**: Control text size, offset, and direction for each axis independently. Option to use custom fonts for grid labels.
- **Emissive Materials**: Apply emissive materials to make the grid stand out in renders.
- **Real-time Updates**: Dynamically update text and edge sizes without regenerating the entire structure.
- **Scene Resizing**: Easily resize the entire scene and adjust units while maintaining proportions.

## Install the Add-on

1. **Package the Script**:
    - Place the provided script files into a folder named `GridGenerator`.

2. **Install the Add-on in Blender**:
    - Open Blender and go to `Edit > Preferences > Add-ons`.
    - Click on `Install...` and select the `GridGenerator` folder.
    - Enable the add-on by checking the box next to `Grid Generator`.

3. **Using the Add-on**:
    - Access the add-on from the `View3D` panel under the `Grid Generator` tab.
    - Configure your grid and add it to your composition.


![Usage](https://github.com/user-attachments/assets/312c28a1-d8d9-49d6-924c-a52f80a5b35d)


## Usage

Once the add-on is installed and enabled, you can use it to generate and customize grids in Blender:

1. **Accessing the Add-on Panel**:
   - Open Blender and switch to the `3D Viewport`.
   - In the right sidebar, locate the `Grid Generator` tab.

2. **Configuring Your Grid**:
   - Choose the `Grid Type` (Cubic with Internal Edges, Cubic with Exterior Edges Only, Cubic with Exterior Edges and Subdivisions, 2D Grid, or 2D Grid with Subdivisions).
   - Set the `Unit of Measure` (from nanometers to kilometers).
   - Adjust the `Length` of the grid in X, Y, and Z directions.
   - Set the number of `Subdivisions` of the grid edges.
   - For 2D grids, select the `2D Grid Orientation` and `2D Toggle Axis` options.
   - Toggle `Show Numbers` to display coordinate values at each point.
   - Adjust `Text Size` and `Edge Size` as needed.
   - Configure `Text Offset` and `Text Direction` for each axis.
   - Optionally, select a custom font for grid labels.

3. **Generating the Grid**:
   - Click `Generate Nodes` to create the basic structure.
   - Use `Create Edges` to add visible edges to the grid.

4. **Customizing Appearance**:
   - Adjust `Text Size` and `Edge Size` at any time using the respective update buttons.
   - Set the `Emission Color` and `Emission Strength` for the emissive material.
   - Click `Apply Emissive Material` to make the grid glow.
   - Use `Resize Scene` to change the overall scale and units of the scene.

5. **Working with the Result**:
   - The generated grid will be placed in your scene.
   - You can move, rotate, or scale the entire structure as needed.
   - Use Blender's built-in tools to further customize or animate the grid.

## Tips for Best Results

- For precise measurements, ensure your Blender units are set correctly in the scene properties.
- Experiment with different subdivision levels to find the right balance between detail and performance.
- Use the emissive material option to make your grid stand out in dark or complex scenes.
- When working with very large or very small scales, use the appropriate unit of measure for better precision.
- For 2D grids, experiment with different orientations and length axis settings to find the best representation for your data.
- Combine this add-on with Blender's animation tools to create dynamic coordinate system visualizations.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.




