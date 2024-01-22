from pprint import pprint
import numpy as np
import open3d as o3d


#TODO : 1. Remove ions and non-standard residues when refining the tunnel
#TOOD : 2. make the centerline scan in refinement dynamic (on radius of probe)
RCSB_ID = '6Z6K'
# pcd = o3d.io.read_point_cloud("./refined_{}.pcd".format(RCSB_ID))
# So if we have a voxel grid of the size 


"""Quantize each voxel to be 1/10 of angstrom"""



def create_sphere(radius:float, center: np.ndarray):
    

    ...



def quantize_on_vdw(coordinates, atom_types)->list:

    return []

pcd = o3d.geometry.PointCloud( o3d.utility.Vector3dVector([ [0,0,0], [1,0,0,] ]) )
N = np.asarray(pcd.points).shape[0]
pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()), center=pcd.get_center())
pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))
# labels = pcd.points
# pprint(dir(pcd))
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.05)

voxel_grid.add_voxel(o3d.geometry.Voxel([0,0,2/0.05]))
print("Dimensiosn ", voxel_grid.dimension())
# print("bb ", voxel_grid.get_axis_aligned_bounding_box())
# print("bb ", voxel_grid.get_box_points())

for i in range(len(voxel_grid.get_voxels())):
    voxel = voxel_grid.get_voxels()[i]
    pprint(dir(voxel))
    print(voxel)
    # print(f"Voxel {i + 1}: Coordinates {voxel.grid_index}, Active: {voxel.grid_active}")
    
grid_size = voxel_grid.get_max_bound() / voxel_grid.voxel_size
grid_size = np.ceil(grid_size).astype(int)
pprint(dir(voxel_grid))

for z in range(grid_size[2]):
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            voxel_index = [x, y, z]
            

            voxel_grid.add_voxel(o3d.geometry.Voxel(voxel))

            # # Print or process the voxel information
            # print(f"Voxel at index {voxel_index}: Active - {voxel.grid_active}")


    # Check conditions based on voxel positions and set some to active
    # if voxel.grid_index[2] > 0:
    #     voxel_grid.get_voxels()[i].grid_active = True
# # pprint(dir(voxel_grid))
# pprint(voxel_grid.get_voxels())
# o3d.geometry.AxisAlignedBoundingBox()
# o3d.visualization.draw_geometries([voxel_grid])