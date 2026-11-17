import pyvista as pv
import tetgen
import numpy as np
pv.set_plot_theme('document')

sphere = pv.Sphere()
cyl = pv.Cylinder(center=(0, 0, 0), direction=(0, 0, 1), radius=0.2, height=1.0, resolution=100)

# Triangulate the mesh to get only triangles
cyl_tri = cyl.triangulate()
print("traingularized")
tet = tetgen.TetGen(cyl_tri)
tet.tetrahedralize(order=1, mindihedral=20, minratio=1.5)
grid = tet.grid
grid.plot(show_edges=True) 

# Save the volume mesh (tetrahedral mesh)
cyl.save("cyl_surface.obj") 

# Save the volume mesh (tetrahedral mesh)
pv.save_meshio("cyl_volume.mesh", tet.grid) 