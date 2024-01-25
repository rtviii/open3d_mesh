
import json
from pprint import pprint
import numpy as np
import time



t1= time.time()
def midpoints(x):
    sl = ()
    for _ in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x


with open('./encodings/6Z6K.json', 'r') as infile:
    data = json.load(infile)

C     = np.array(data['coordinates'])
R_T_0 = np.array(data['radius_types_0'])

#! normalize to origin
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

rescaled_coordinates = np.array(list(zip(Cx,Cy,Cz))) 

# ! Create a 3D grid 10 voxels larger than the max amplitude of the point cloud in any direction
amplitude_X =  np.max(Cx) - np.min(Cx)
amplitude_Y =  np.max(Cy) - np.min(Cy)
amplitude_Z =  np.max(Cz) - np.min(Cz)



dim = int(np.ceil(np.max([amplitude_Z,amplitude_Y,amplitude_X])) + 10)
x,y,z = np.indices((dim, dim, dim)) 

xc     = midpoints(x)
yc     = midpoints(y)
zc     = midpoints(z)

filled = xc + yc + zc  < -1





def get_sphere_indices(center, radius, grid_size):
    x0, y0, z0 = center
    indices = []

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            for z in range(grid_size[2]):
                if (x - x0)**2 + (y - y0)**2 + (z - z0)**2 <= radius**2:
                    indices.append((x, y, z))

    return indices

def get_sphere_indices_voxelized(center, radius):
    """Make sure radius reflects the size of the underlying voxel grid"""
    x0, y0, z0 = center
    
    x_range = slice(x0-( radius+1 ), x0+( radius+1 ))
    y_range = slice(y0-( radius+1 ), y0+( radius+1 ))
    z_range = slice(z0-( radius+1 ), z0+( radius+1 ))

    indices = np.indices((x_range.stop - x_range.start, y_range.stop - y_range.start, z_range.stop - z_range.start))
    indices += np.array([x_range.start, y_range.start, z_range.start])[:, np.newaxis, np.newaxis, np.newaxis]
    indices = indices.transpose(1, 2, 3, 0)
    indices_list = list(map(tuple, indices.reshape(-1, 3)))

    sphere_active_ix = []
    for ind in indices_list:
        x_ = ind[0]
        y_ = ind[1]
        z_ = ind[2]
        if (x_ - x0)**2 + (y_ - y0)**2 + (z_ - z0)**2 <= radius**2:
            sphere_active_ix.append((x_, y_, z_))

    return sphere_active_ix



test_pts = np.random.randint(10, 90, size=(50, 3))

dim = 100

t1= time.time()
for pt in test_pts:
    get_sphere_indices_voxelized(pt, 5)

t2= time.time()
print(t2-t1)



# generate 50 random points on a 100x100 grid and test the difference in time execution  between the voxelized and unvoxelized version




# print(np.shape(_))
# for coordinate, radius_type in zip(rescaled_coordinates, R_T_0):
#     vox_x,vox_y,vox_z = int(np.floor(coordinate[0])), int(np.floor(coordinate[1])), int(np.floor(coordinate[2]))
#     indices = get_sphere_indices((vox_x,vox_y,vox_z), radius_type[0], (dim, dim, dim))
#     for index in indices:
#         filled[index] = True

# print(filled.shape)
# print(filled[50:60, 70:80, 30:40].shape)
# print(filled[50:60, 70:80, 30:40].shape)

