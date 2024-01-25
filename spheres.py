import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np


#TODO: convert to 1/10 Angstrom before scaling & shiftin to get a finer representation
def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    return rmin, rmax, cmin, cmax


def midpoints(x):
    sl = ()
    for _ in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x

def get_sphere_indices(center, radius, grid_size):
    x0, y0, z0 = center
    indices = []

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            for z in range(grid_size[2]):
                if (x - x0)**2 + (y - y0)**2 + (z - z0)**2 <= radius**2:
                    indices.append((x, y, z))

    return indices



# ! The data
# ! - atom coordinates (within 15 angstrom of the centerlin)
# ! - vdw radius and atom type for each coordinate

with open('./encodings/6Z6K.json', 'r') as infile:
    data = json.load(infile)

C     = np.array(data['coordinates'])
R_T_0 = np.array(data['radius_types_0'])

def normalize_atom_coordinates(coordinates:np.ndarray):
    """@param coordinates: numpy array of shape (N,3) for atoms lining the tunnel in radius R (usually 15Angstrom) from MOLE centerline"""
    #! normalize to origin
    C = coordinates
    Cx = C[:,0] - np.mean(C[:,0])
    Cy = C[:,1] - np.mean(C[:,1])
    Cz = C[:,2] - np.mean(C[:,2])

    #! negative deviation from zero"
    dev =  np.min(
            [   
            np.min(Cx),
            np.min(Cy),
            np.min(Cz)
            ])

    #! shift to positive quadrant
    Cx = Cx + abs(dev)
    Cy = Cy + abs(dev)
    Cz = Cz + abs(dev)
    rescaled_coords = np.array(list(zip(Cx,Cy,Cz))) 

    # ! Create a 3D grid 10 voxels larger than the max amplitude of the point cloud in any direction
    amplitude_X =  np.max(Cx) - np.min(Cx)
    amplitude_Y =  np.max(Cy) - np.min(Cy)
    amplitude_Z =  np.max(Cz) - np.min(Cz)

    biggest_dimension = int(np.ceil(np.max([amplitude_Z,amplitude_Y,amplitude_X])) + 10)
    return rescaled_coords, biggest_dimension



def get_sphere_indices_voxelized(center, radius):
    """Make sure radius reflects the size of the underlying voxel grid"""
    radius = int(np.ceil(radius)) # TODO : make sure the radius is not ceil'ed when the gridsize is increased
    x0, y0, z0 = center
    
    #!------ Generate indices of a voxel cube of side 2r+2  around the centerpoint
    x_range = slice(x0-( radius+1 ), x0+( radius+1 ))
    y_range = slice(y0-( radius+1 ), y0+( radius+1 ))
    z_range = slice(z0-( radius+1 ), z0+( radius+1 ))

    indices = np.indices((x_range.stop - x_range.start, y_range.stop - y_range.start, z_range.stop - z_range.start))
    indices += np.array([x_range.start, y_range.start, z_range.start])[:, np.newaxis, np.newaxis, np.newaxis]
    indices = indices.transpose(1, 2, 3, 0)
    indices_list = list(map(tuple, indices.reshape(-1, 3)))
    #!------ Generate indices of a voxel cube of side 2r+2  around the centerpoint

    sphere_active_ix = []
    for ind in indices_list:
        x_ = ind[0]
        y_ = ind[1]
        z_ = ind[2]
        if (x_ - x0)**2 + (y_ - y0)**2 + (z_ - z0)**2 <= radius**2:
            sphere_active_ix.append((x_, y_, z_))

    return sphere_active_ix


# Visualize just center coordinates
def visualize_source_coordinates(nulled_grid:np.ndarray, coordinates:np.ndarray, ):
    for coordinate  in coordinates:
        # coordinates of the side of the given voxel
        vox_x,vox_y,vox_z = int(np.floor(coordinate[0])), int(np.floor(coordinate[1])), int(np.floor(coordinate[2]))
        nulled_grid[vox_x,vox_y,vox_z] = True
    return nulled_grid


# visualize_source_coordinates(filled,rescaled_coordinates)

def visualize_as_spheres(nulled_grid, source_coordinates:np.ndarray, radii_types:np.ndarray):
    for coordinate, radius_type in zip(source_coordinates, radii_types):
        vox_x,vox_y,vox_z = int(np.floor(coordinate[0])), int(np.floor(coordinate[1])), int(np.floor(coordinate[2]))
        indices = get_sphere_indices_voxelized((int(vox_x),int(vox_y),int(vox_z)), radius_type[0])
        for index in indices:
            nulled_grid[index] = True
    return nulled_grid

# visualize_as_spheres(filled,rescaled_coordinates, R_T_0)




def plt_plot(x_ix,y_ix,z_ix,filled_grid):
    # facecolors =  np.zeros(filled.shape + (3,))
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(x_ix,y_ix,z_ix,filled_grid,
    facecolors=[0, 1, 1, 0.3] , linewidth=0.5) 
    ax.set(xlabel='r', ylabel='g', zlabel='b')
    ax.set_aspect('equal')

    plt.show()
    exit()


rescaled_coordinates, dim = normalize_atom_coordinates(C)
x,y,z = np.indices((dim, dim, dim)) 
xc = midpoints(x)
yc = midpoints(y)
zc = midpoints(z)
filled = xc + yc + zc  < -1

filled = visualize_source_coordinates(filled,rescaled_coordinates)
plt_plot(x,y,z,filled)