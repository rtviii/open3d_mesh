import open3d as o3d
import numpy as np

if __name__ == "__main__":

    sample_pcd_data = o3d.data.PCDPointCloud()
    pcd             = o3d.io.read_point_cloud('./7ssw.pcd')

    # Estimate normals
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=3, max_nn=20))

    # Visualize point cloud with normals
    octree = o3d.geometry.Octree(max_depth=8)
    octree.convert_from_point_cloud(pcd)

    # Invert the Octree to capture the cavity
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd.points)


    negative_pcd        = o3d.geometry.PointCloud()
    negative_pcd.points = o3d.utility.Vector3dVector(np.asarray(bounding_box.get_box_points()) - np.asarray(pcd.points))
    octree_negative     = o3d.geometry.Octree(max_depth=8)

    octree_negative.convert_from_point_cloud(negative_pcd)

    # Visualize the original point cloud, normals, and the inverted octree
    o3d.visualization.draw_geometries([pcd, octree, octree_negative],
                                      point_show_normal=True,
                                      mesh_show_wireframe=True)

    # o3d.visualization.draw_geometries([pcd])
    exit()
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(np.asarray(pcd.points))

    # Create a new point cloud representing the "negative space"
    negative_pcd = o3d.geometry.PointCloud()

    negative_pcd.points = o3d.utility.Vector3dVector(np.asarray(bounding_box.get_box_points()) - np.asarray(pcd.points))
    octree_negative = o3d.geometry.Octree(max_depth=8)
    octree_negative.convert_from_point_cloud(negative_pcd)

    o3d.visualization.draw_geometries([octree_negative])

    # octree = o3d.geometry.Octree(max_depth=4)
    # octree.convert_from_point_cloud(pcd, size_expand=0.01)
    # print("Displaying input octree ...")
    # o3d.visualization.draw([octree])
    # print("Finding leaf node containing the first point of pointcloud ...")
    # print(octree.locate_leaf_node(pcd.points[0]))



    # exit()
    # Fit to unit cube.