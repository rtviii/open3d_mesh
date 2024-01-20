

from pprint import pprint
import numpy as np
import open3d as o3d
from open3d import core as o3c





pcd = o3d.io.read_point_cloud("with_labels.pcd")
print(np.asarray(pcd.colors))
N = np.asarray(pcd.points).shape[0]
pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()), center=pcd.get_center())

voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.01)
o3d.visualization.draw_geometries([voxel_grid])
print(pcd, "\n")