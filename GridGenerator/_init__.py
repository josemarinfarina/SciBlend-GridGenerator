import bpy
bl_info = {
    "name": "Grid Generator",
    "author": "José Marín",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Tools",
    "description": "Generates a grid of numbers with advanced functionalities",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


class OBJECT_PT_GridGeneratorPanel(bpy.types.Panel):
    bl_label = "Grid Generator"
    bl_idname = "OBJECT_PT_grid_generator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GridGenerator'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        grid_settings = scene.grid_settings

        # Grid Settings
        box = layout.box()
        box.label(text="Grid Settings", icon='GRID')
        box.prop(grid_settings, "unit_measure", text="Unit of Measure")
        box.prop(grid_settings, "distance_x", text="Distance X")
        box.prop(grid_settings, "distance_y", text="Distance Y")
        box.prop(grid_settings, "distance_z", text="Distance Z")
        box.prop(grid_settings, "subdivisions", text="Subdivisions")

        layout.separator()

        # Number Settings
        box = layout.box()
        box.label(text="Number Settings", icon='FONT_DATA')
        box.prop(grid_settings, "show_numbers", text="Show Numbers")
        box.prop(grid_settings, "text_size", text="Text Size")
        box.prop(grid_settings, "use_custom_font", text="Custom Font")
        if grid_settings.use_custom_font:
            box.prop(grid_settings, "custom_font", text="Font File")

        layout.separator()

        # Edge Settings
        box = layout.box()
        box.label(text="Edge Settings", icon='MOD_WIREFRAME')
        box.prop(grid_settings, "edge_size", text="Edge Thickness")

        layout.separator()

        # Emissive Material Settings
        box = layout.box()
        box.label(text="Emissive Material", icon='MATERIAL')
        box.prop(grid_settings, "emission_color", text="Emission Color")
        box.prop(grid_settings, "emission_strength", text="Emission Strength")

        layout.separator()

        # Scene Resizing
        box = layout.box()
        box.label(text="Scene Resizing", icon='FULLSCREEN_ENTER')
        box.prop(grid_settings, "unit_scale", text="Unit Scale")
        box.prop(grid_settings, "target_unit_measure", text="New Unit Measure")

        layout.separator()

        # Operations
        box = layout.box()
        box.label(text="Operations", icon='TOOL_SETTINGS')
        row = box.row(align=True)
        row.operator("object.generate_nodes",
                     text="Generate Nodes", icon='NODETREE')
        row.operator("object.create_edges", text="Create Edges",
                     icon='OUTLINER_OB_CURVE')

        row = box.row(align=True)
        row.operator("object.apply_emissive_material",
                     text="Apply Emissive Material", icon='MATERIAL')
        row.operator("object.resize_scene", text="Resize Scene",
                     icon='ARROW_LEFTRIGHT')

        row = box.row(align=True)
        row.operator("object.update_text_size",
                     text="Update Text Size", icon='FONT_DATA')
        row.operator("object.update_edge_size",
                     text="Update Edge Size", icon='MOD_WIREFRAME')


class GenerateNodesOperator(bpy.types.Operator):
    bl_idname = "object.generate_nodes"
    bl_label = "Generate Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings

        scale_factor = {
            'mm': 0.001,
            'cm': 0.01,
            'dm': 0.1,
            'm': 1
        }.get(grid_settings.unit_measure, 1)

        dist_x = grid_settings.distance_x * scale_factor
        dist_y = grid_settings.distance_y * scale_factor
        dist_z = grid_settings.distance_z * scale_factor

        # Use existing camera or create a new one
        camera = next(
            (obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA'), None)
        if not camera:
            bpy.ops.object.camera_add(
                align='VIEW', location=(0, -10, 5), rotation=(0, 0, 0))
            camera = bpy.context.object

        # Remove only objects related to the previous grid
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("GridNode_") or obj.name.startswith("EdgeObj_"):
                obj.select_set(True)
        bpy.ops.object.delete()

        subdivs = grid_settings.subdivisions
        text_objects = []

        # Calculate offsets to center the grid
        offset_x = -dist_x / 2
        offset_y = -dist_y / 2
        offset_z = -dist_z / 2

        # Get the default font
        default_font = None
        for font in bpy.data.fonts:
            if font.users > 0:
                default_font = font
                break

        for z in range(subdivs + 1):
            for y in range(subdivs + 1):
                for x in range(subdivs + 1):
                    # Calculate centered position
                    location = (
                        x * dist_x / subdivs + offset_x,
                        y * dist_y / subdivs + offset_y,
                        z * dist_z / subdivs + offset_z
                    )

                    if grid_settings.show_numbers:
                        bpy.ops.object.text_add(location=location)
                        text_obj = bpy.context.object
                        text_obj.name = f"GridNode_{x}_{y}_{z}"

                        # Adjust text to show centered coordinates
                        coord_x = x * grid_settings.distance_x / subdivs - grid_settings.distance_x / 2
                        coord_y = y * grid_settings.distance_y / subdivs - grid_settings.distance_y / 2
                        coord_z = z * grid_settings.distance_z / subdivs - grid_settings.distance_z / 2
                        text_obj.data.body = f"{coord_x:.2f}, {
                            coord_y:.2f}, {coord_z:.2f}"

                        text_obj.scale = (grid_settings.text_size,) * 3

                        # Set font
                        if grid_settings.use_custom_font and grid_settings.custom_font != "":
                            try:
                                text_obj.data.font = bpy.data.fonts.load(
                                    grid_settings.custom_font)
                            except:
                                self.report(
                                    {'WARNING'}, f"Could not load custom font. Using default font.")
                                text_obj.data.font = default_font
                        else:
                            text_obj.data.font = default_font

                        constraint = text_obj.constraints.new(type='TRACK_TO')
                        constraint.target = camera
                        constraint.track_axis = 'TRACK_Z'
                        constraint.up_axis = 'UP_Y'

                        text_objects.append(text_obj)
                    else:
                        # Create an empty object to mark the position
                        bpy.ops.object.empty_add(
                            type='PLAIN_AXES', location=location)
                        empty_obj = bpy.context.object
                        empty_obj.name = f"GridNode_{x}_{y}_{z}"
                        text_objects.append(empty_obj)

        return {'FINISHED'}


class CreateEdgesOperator(bpy.types.Operator):
    bl_idname = "object.create_edges"
    bl_label = "Create Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings
        text_objects = [
            obj for obj in bpy.context.scene.objects if obj.name.startswith("GridNode_")]

        def create_edge(v1, v2):
            curve_data = bpy.data.curves.new(
                name=f"Curve_{v1}_{v2}", type='CURVE')
            curve_data.dimensions = '3D'
            curve_obj = bpy.data.objects.new(f"EdgeObj_{v1}_{v2}", curve_data)
            bpy.context.collection.objects.link(curve_obj)

            spline = curve_data.splines.new(type='POLY')
            spline.points.add(1)
            spline.points[0].co = (*text_objects[v1].location, 1)
            spline.points[1].co = (*text_objects[v2].location, 1)

            curve_data.bevel_depth = grid_settings.edge_size
            curve_data.bevel_resolution = 12

        subdivs = grid_settings.subdivisions
        for z in range(subdivs + 1):
            for y in range(subdivs + 1):
                for x in range(subdivs + 1):
                    index = z * (subdivs + 1)**2 + y * (subdivs + 1) + x

                    # X connections
                    if x < subdivs:
                        create_edge(index, index + 1)

                    # Y connections
                    if y < subdivs:
                        create_edge(index, index + (subdivs + 1))

                    # Z connections
                    if z < subdivs:
                        create_edge(index, index + (subdivs + 1)**2)

        return {'FINISHED'}


class UpdateTextSizeOperator(bpy.types.Operator):
    bl_idname = "object.update_text_size"
    bl_label = "Update Text Size"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings
        text_size = grid_settings.text_size

        for obj in bpy.context.scene.objects:
            if obj.type == 'FONT':
                obj.scale = (text_size,) * 3

        return {'FINISHED'}


class UpdateEdgeSizeOperator(bpy.types.Operator):
    bl_idname = "object.update_edge_size"
    bl_label = "Update Edge Size"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings
        edge_size = grid_settings.edge_size

        for obj in bpy.context.scene.objects:
            if obj.type == 'CURVE' and obj.name.startswith("EdgeObj_"):
                obj.data.bevel_depth = edge_size

        return {'FINISHED'}


class ApplyEmissiveMaterialOperator(bpy.types.Operator):
    bl_idname = "object.apply_emissive_material"
    bl_label = "Apply Emissive Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings

        # Create a new emissive material
        mat = bpy.data.materials.new(name="Emissive Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear existing nodes
        nodes.clear()

        # Create necessary nodes
        node_emission = nodes.new(type='ShaderNodeEmission')
        node_output = nodes.new(type='ShaderNodeOutputMaterial')

        # Configure emission node
        node_emission.inputs['Color'].default_value = grid_settings.emission_color
        node_emission.inputs['Strength'].default_value = grid_settings.emission_strength

        # Connect nodes
        links.new(node_emission.outputs['Emission'],
                  node_output.inputs['Surface'])

        # Apply material to edges and numbers
        for obj in bpy.context.scene.objects:
            if obj.type in ['CURVE', 'FONT']:
                if obj.data.materials:
                    obj.data.materials[0] = mat
                else:
                    obj.data.materials.append(mat)

        return {'FINISHED'}


class ResizeSceneOperator(bpy.types.Operator):
    bl_idname = "object.resize_scene"
    bl_label = "Resize Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        grid_settings = scene.grid_settings

        # Change the unit scale
        scene.unit_settings.scale_length = grid_settings.unit_scale

        # Change the length unit
        unit_map = {
            'mm': 'MILLIMETERS',
            'cm': 'CENTIMETERS',
            'dm': 'DECIMETERS',
            'm': 'METERS'
        }
        scene.unit_settings.length_unit = unit_map[grid_settings.target_unit_measure]

        self.report({'INFO'}, f"Scene resized to {
                    grid_settings.target_unit_measure}")
        return {'FINISHED'}


class GridSettings(bpy.types.PropertyGroup):
    unit_measure: bpy.props.EnumProperty(
        name="Unit of Measure",
        description="Select the unit of measure for the distance",
        items=[
            ('mm', "Millimeters", ""),
            ('cm', "Centimeters", ""),
            ('dm', "Decimeters", ""),
            ('m', "Meters", "")
        ],
        default='m'
    )
    distance_x: bpy.props.FloatProperty(
        name="Distance X",
        description="Distance between numbers on X axis",
        default=1.0,
        min=0.1,
        max=1000.0
    )
    distance_y: bpy.props.FloatProperty(
        name="Distance Y",
        description="Distance between numbers on Y axis",
        default=1.0,
        min=0.1,
        max=1000.0
    )
    distance_z: bpy.props.FloatProperty(
        name="Distance Z",
        description="Distance between numbers on Z axis",
        default=1.0,
        min=0.1,
        max=1000.0
    )
    subdivisions: bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of subdivisions in each dimension",
        default=2,
        min=1,
        max=20
    )
    show_numbers: bpy.props.BoolProperty(
        name="Show Numbers",
        description="Show numbers on nodes",
        default=True
    )
    text_size: bpy.props.FloatProperty(
        name="Text Size",
        description="Size of the text on nodes",
        default=0.5,
        min=0.1,
        max=5.0
    )
    edge_size: bpy.props.FloatProperty(
        name="Edge Size",
        description="Thickness of the grid edges",
        default=0.05,
        min=0.01,
        max=0.5
    )
    emission_color: bpy.props.FloatVectorProperty(
        name="Emission Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        min=0.0,
        max=1.0
    )
    emission_strength: bpy.props.FloatProperty(
        name="Emission Strength",
        default=1.0,
        min=0.0,
        max=10.0
    )
    unit_scale: bpy.props.FloatProperty(
        name="Unit Scale",
        description="Scale factor for the scene units",
        default=1.0,
        min=0.00001,
        max=1000.0
    )
    target_unit_measure: bpy.props.EnumProperty(
        name="Target Unit of Measure",
        description="Unit of measure to change the scene to",
        items=[
            ('mm', "Millimeters", ""),
            ('cm', "Centimeters", ""),
            ('dm', "Decimeters", ""),
            ('m', "Meters", "")
        ],
        default='m'
    )
    use_custom_font: bpy.props.BoolProperty(
        name="Use Custom Font",
        description="Use a custom font for the grid numbers",
        default=False
    )
    custom_font: bpy.props.StringProperty(
        name="Custom Font",
        description="Path to custom font file",
        default="",
        subtype='FILE_PATH'
    )


def register():
    bpy.utils.register_class(OBJECT_PT_GridGeneratorPanel)
    bpy.utils.register_class(GenerateNodesOperator)
    bpy.utils.register_class(CreateEdgesOperator)
    bpy.utils.register_class(UpdateTextSizeOperator)
    bpy.utils.register_class(UpdateEdgeSizeOperator)
    bpy.utils.register_class(ApplyEmissiveMaterialOperator)
    bpy.utils.register_class(ResizeSceneOperator)
    bpy.utils.register_class(GridSettings)
    bpy.types.Scene.grid_settings = bpy.props.PointerProperty(
        type=GridSettings)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_GridGeneratorPanel)
    bpy.utils.unregister_class(GenerateNodesOperator)
    bpy.utils.unregister_class(CreateEdgesOperator)
    bpy.utils.unregister_class(UpdateTextSizeOperator)
    bpy.utils.unregister_class(UpdateEdgeSizeOperator)
    bpy.utils.unregister_class(ApplyEmissiveMaterialOperator)
    bpy.utils.unregister_class(ResizeSceneOperator)
    bpy.utils.unregister_class(GridSettings)
    del bpy.types.Scene.grid_settings


if __name__ == "__main__":
    register()
