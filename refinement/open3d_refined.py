from pprint import pprint
import numpy as np
import open3d as o3d

RCSB_ID = '6Z6K'
pcd = o3d.io.read_point_cloud("./refined_{}.pcd".format(RCSB_ID))


N = np.asarray(pcd.points).shape[0]
pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()), center=pcd.get_center())
pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))
# labels = pcd.points
pprint(dir(pcd))
# voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.01)
# o3d.visualization.draw_geometries([voxel_grid])