import cadquery as cq
import sys
import os
# import vedo
# from vedo import Plotter

STL_FOLDER = '/app/app/static/stls'
# STL_IMGS_FOLDER = '/app/app/static/stl_imgs'
def scale_dxf_to_size(dxf_path, output_stl, extrusion_height):
    # Importar el DXF
    dxf_shapes = cq.importers.importDXF(dxf_path)

    if not dxf_shapes:
        print("Error: No se pudo cargar el DXF")
        sys.exit(1)


    # Extruir la geometría 2D a 3D
    extruded = dxf_shapes.extrude(extrusion_height)

    # Exportar a STL
    stl_path = os.path.join(STL_FOLDER, output_stl)

    cq.exporters.export(extruded, stl_path)
    print(f"Archivo STL generado: {stl_path}")

