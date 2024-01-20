
from pprint import pprint
import numpy as np
import open3d as o3d
from open3d import core as o3c


def create_pcd_from_atoms(positions:np.ndarray, atom_types:np.ndarray):
    pcd = o3d.geometry.PointCloud( o3d.utility.Vector3dVector(positions) )
    pcd.colors = o3d.utility.Vector3dVector(atom_types)

def voxel_grid_vis(pcd):
    N = np.asarray(pcd).shape[0]
    pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()), center=pcd.get_center())
    pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))

    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.01)
    o3d.visualization.draw_geometries([voxel_grid])

    print(pcd, "\n")

def create_pcd(points:np.ndarray, colors:np.ndarray):
    pcd = o3d.geometry.PointCloud( o3d.utility.Vector3dVector(points) )
    pcd.colors = o3d.utility.Vector3dVector(colors)
    # pcd = o3d.geometry.PointCloud( o3d.utility.Vector3dVector(np.array([[0, 0, 0], [1, 1, 1], [-1,-1,-1]], dtype=np.float32)) )
    # pcd.colors = o3d.utility.Vector3dVector(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32))
    o3d.io.write_point_cloud("with_labels.pcd", pcd)
    return pcd