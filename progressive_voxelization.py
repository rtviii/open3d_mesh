# The goal is to create a method that places a sphere at a given coordinate

from pprint import pprint
import open3d as o3d
import numpy as np

#TODO : 1. Remove ions and non-standard residues when refining the tunnel
#TOOD : 2. make the centerline scan in refinement dynamic (on radius of probe)

def get_sphere_indices_voxelized(center: np.ndarray, radius: int):

    """Make sure radius reflects the size of the underlying voxel grid"""
    x0, y0, z0 = center

    #!------ Generate indices of a voxel cube of side 2r+2  around the centerpoint
    x_range = slice(int(np.floor(x0) - (radius )), int(np.ceil(x0) + (radius )))
    y_range = slice(int(np.floor(y0) - (radius )), int(np.ceil(y0) + (radius )))
    z_range = slice(int(np.floor(z0) - (radius )), int(np.ceil(z0) + (radius )))

    indices = np.indices( (
            x_range.stop - x_range.start,
            y_range.stop - y_range.start,
            z_range.stop - z_range.start) )

    indices += np.array([x_range.start, y_range.start, z_range.start])[ :, np.newaxis, np.newaxis, np.newaxis ]
    indices = indices.transpose(1, 2, 3, 0)
    indices_list = list(map(tuple, indices.reshape(-1, 3)))
    #!------ Generate indices of a voxel cube of side 2r+2  around the centerpoint

    sphere_active_ix = []
    for ind in indices_list:
        x_ = ind[0]
        y_ = ind[1]
        z_ = ind[2]
        if (x_ - x0) ** 2 + (y_ - y0) ** 2 + (z_ - z0) ** 2 <= radius**2:
            sphere_active_ix.append([x_, y_, z_])

    return np.array(sphere_active_ix)


coord0 = [0,0,0]
coord1 = [50, 50, 50]
coord2 = [150, 150, 150]

_ix = [coord0, coord1, coord2]

pcd        = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np.array(_ix))

voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.1)
origin = np.asarray(voxel_grid.origin)
indices1 = get_sphere_indices_voxelized(coord1, 50)
for i in indices1:
    voxel_grid.add_voxel(o3d.geometry.Voxel(i))

indices2 = get_sphere_indices_voxelized(coord2, 20)
for i in indices2:
    voxel_grid.add_voxel(o3d.geometry.Voxel(i))


voxels = np.asarray(voxel_grid.get_voxels())

o3d.visualization.draw_geometries([voxel_grid])
