from utils.fileutils import _load_noise_map
from os import urandom
import vtk, logging

def _create_vtk_mesh(noise_map):
    points = vtk.vtkPoints()
    num_rows, num_cols = noise_map.shape
    
    # Insert points
    for i in range(num_rows):
        for j in range(num_cols):
            z_value = noise_map[i, j] # * 0.65 # NOTE In case you want to tone down the degree of the slope
            points.InsertNextPoint(i, z_value, j)

    polys = vtk.vtkCellArray()
    
    # Create polygons (triangles) by connecting adjacent points
    for i in range(num_rows - 1):  # Iterate up to num_rows-1 for valid polygons
        for j in range(num_cols - 1):  # Iterate up to num_cols-1 for valid polygons
            idx1 = i * num_cols + j
            idx2 = idx1 + 1
            idx3 = (i + 1) * num_cols + j
            idx4 = idx3 + 1

            polys.InsertNextCell(3, [idx1, idx2, idx3])
            polys.InsertNextCell(3, [idx2, idx4, idx3])
    
    # Create polydata
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(polys)
    
    return polydata

def _smooth_mesh(polydata, number_of_iterations=100):
    logging.info("Starting mesh smoothing...")
    smoother = vtk.vtkSmoothPolyDataFilter()
    logging.info("Smoother initialized")
    smoother.SetInputData(polydata)
    logging.info("Input data set")
    smoother.SetNumberOfIterations(number_of_iterations)
    logging.info(f"Number of iterations set to {number_of_iterations}")
    smoother.SetRelaxationFactor(0.1)
    logging.info("Relaxation factor set")
    smoother.Update() 
    logging.info("Smoother updated")
    return smoother.GetOutput()


def _save_vtk_mesh(polydata, filename):
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(polydata)
    writer.Write()

def _gen_mesh(noise_map):
    uid = urandom(4).hex()
    logging.info(f"Mesh#{uid} - Noise loaded")
    logging.info(f"Mesh#{uid} - Creating primary mesh...")
    vtk_mesh = _create_vtk_mesh(noise_map)
    logging.info(f"Mesh#{uid} - Created primary mesh")
    logging.info(f"Mesh#{uid} - Smoothing mesh...")
    smoothed_mesh = _smooth_mesh(vtk_mesh) 
    logging.info(f"Mesh#{uid} - Mesh smoothed")
    logging.info(f"Mesh#{uid} - Saving...")
    _save_vtk_mesh(vtk_mesh, f"meshes/mesh_{uid}.vtk")
    _save_vtk_mesh(smoothed_mesh, f"meshes/smesh_{uid}.vtk")
    logging.info(f"Mesh#{uid} - Saved")