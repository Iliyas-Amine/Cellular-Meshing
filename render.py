import vtk, os, glob

def read_vtk_file(file_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update() 
    return reader.GetOutput()

def view_vtk_mesh(polydata):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    renderer = vtk.vtkRenderer()
    
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)
    
    render_window.Render()
    render_window_interactor.Start()

pattern = os.path.join("meshes", '*.vtk')
vtk_files = glob.glob(pattern)
for file in vtk_files[:3]:
    vtk_mesh = read_vtk_file(file)
    view_vtk_mesh(vtk_mesh)
