import vtk
import logging
import numpy as np
from vtk.util import numpy_support
from utils.config import (SAVE)
from os import urandom

def _create_vtk_mesh_vectorized(noise_map):
    rows, cols = noise_map.shape
    x = np.arange(0, rows, 1)
    y = np.arange(0, cols, 1)
    mx, my = np.meshgrid(x, y, indexing='ij') 
    
    flat_x = mx.ravel()
    flat_y = noise_map.ravel()
    flat_z = my.ravel()        
    
    coords = np.column_stack((flat_x, flat_y, flat_z)).ravel()
    
    vtk_float_array = numpy_support.numpy_to_vtk(num_array=coords, deep=True, array_type=vtk.VTK_FLOAT)
    vtk_float_array.SetNumberOfComponents(3)
    
    points = vtk.vtkPoints()
    points.SetData(vtk_float_array)
    
    sgrid = vtk.vtkStructuredGrid()
    sgrid.SetDimensions(cols, rows, 1) 
    sgrid.SetPoints(points)

    geom_filter = vtk.vtkGeometryFilter()
    geom_filter.SetInputData(sgrid)
    geom_filter.Update()
    
    return geom_filter.GetOutput()

def _save_vtk_mesh(polydata, filename):
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(polydata)
    writer.Write()

def _gen_mesh(noise_map):
    uid = urandom(4).hex()
    logging.debug(f"Mesh#{uid} - Noise loaded")
    
    logging.debug(f"Mesh#{uid} - Creating primary mesh (Vectorized)...")
    vtk_mesh = _create_vtk_mesh_vectorized(noise_map)
    logging.debug(f"Mesh#{uid} - Created primary mesh")
    if SAVE:
        logging.debug(f"Mesh#{uid} - Saving...")
        _save_vtk_mesh(vtk_mesh, f"meshes/mesh_{uid}.vtk")
        logging.debug(f"Mesh#{uid} - Saved")