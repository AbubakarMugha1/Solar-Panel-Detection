from qgis.core import QgsProject, QgsLayoutExporter, QgsRectangle
import os

# Access current open project
project = QgsProject.instance()

# Get project folder (where your .qgz file is saved)
project_path = project.fileName()
project_folder = os.path.dirname(project_path)

# Create 'images' directory in the project folder if it doesn't exist
images_folder = os.path.join(project_folder, 'images')
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Your layout name
layout = project.layoutManager().layoutByName('DL_Project_Layout')  # change name if needed

# Access map item using the correct ID (Map 1)
map_item = layout.itemById('Map 1')  # 'Map 1' instead of 'map'

if map_item is None:
    print("Map item not found in layout!")
else:
    canvas = iface.mapCanvas()
    map_item.setExtent(canvas.extent())

    # Get initial extent (start location)
    start_extent = map_item.extent()

    # Export settings
    dpi = 150
    export_settings = QgsLayoutExporter.ImageExportSettings()
    export_settings.dpi = dpi

    # Make extent square
    width = start_extent.xMaximum() - start_extent.xMinimum()
    height = start_extent.yMaximum() - start_extent.yMinimum()
    size = min(width, height)

    center_x = (start_extent.xMaximum() + start_extent.xMinimum()) / 2
    center_y = (start_extent.yMaximum() + start_extent.yMinimum()) / 2

    # Define the new square starting extent
    square_extent = QgsRectangle(
        center_x - size/2,
        center_y - size/2,
        center_x + size/2,
        center_y + size/2
    )
    map_item.setExtent(square_extent)

    # Save start (top-left) corner
    x0 = square_extent.xMinimum()
    y0 = square_extent.yMaximum()

    step_size = size

    rows = 1
    cols = 1
    image_count = 1

    exporter = QgsLayoutExporter(layout)

    for row in range(rows):
        for col in range(cols):
            # Calculate extent based on start point
            new_extent = QgsRectangle(
                x0 + col * step_size,
                y0 - (row + 1) * step_size,
                x0 + (col + 1) * step_size,
                y0 - row * step_size
            )

            map_item.setExtent(new_extent)

            output_filename = os.path.join(images_folder, f'exported_grid_test_{image_count}.bmp')
            exporter.exportToImage(output_filename, export_settings)
            print(f'Exported {output_filename}')
            image_count += 1
