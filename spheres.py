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


#? -------------- Utils ^ --------------------

with open('./encodings/6Z6K.json', 'r') as infile:
    data = json.load(infile)

C = np.array(data['coordinates']) 

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



#! ---create gride
amplitude_X =  np.max(Cx) - np.min(Cx)
amplitude_Y =  np.max(Cy) - np.min(Cy)
amplitude_Z =  np.max(Cz) - np.min(Cz)

dim = int(np.ceil(np.max([amplitude_Z,amplitude_Y,amplitude_X])) + 10)
x,y,z = np.indices((dim, dim, dim)) 

def midpoints(x):
    sl = ()
    for _ in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x

xc = midpoints(x)
yc = midpoints(y)
zc = midpoints(z)
#! ---create gride

rescaled_coordinates = np.array(list(zip(Cx,Cy,Cz))) 

print(rescaled_coordinates.shape)

#! zero out the whole grid
filled = xc + yc + zc  < -1

#! fill the grid with the coordinates of the atoms
# for coord in rescaled_coordinates:
#     vox_x,vox_y,vox_z = int(np.floor(coord[0])), int(np.floor(coord[1])), int(np.floor(coord[2]))
#     filled[vox_x,vox_y,vox_z] = True

    
# given a coordinate of the voxel and a radius around it, get the voxels that are included in the sphere 
# sphere of radius 2 around the voxel at 45,45,45 
def get_sphere_indices(center, radius, grid_size):
    x0, y0, z0 = center
    indices = []

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            for z in range(grid_size[2]):
                if (x - x0)**2 + (y - y0)**2 + (z - z0)**2 <= radius**2:
                    indices.append((x, y, z))

    return indices


sphere_indices = get_sphere_indices((45,45,45), 5, (90,90,90))
print(sphere_indices)
for index in sphere_indices:
    filled[index] = True


# print(filled.shape)
# print(filled)

# exit()
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x,y,z,filled,
           linewidth=0.5) 
ax.set(xlabel='r', ylabel='g', zlabel='b')
ax.set_aspect('equal')

plt.show()

# print(amplitude_X)
# print(amplitude_Y)
# print(amplitude_Z)

exit()


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
ax.scatter(Cx, Cy, Cz)
plt.show()
# # np.min(Cx)
# np.min(Cy)
# np.min(Cz)
# r, g, b = np.indices((17, 17, 17)) / 16.0


sphere = []

# ax = plt.figure().add_subplot(projection='3d')

# ax.voxels(np.array(zip(Cx,Cy,Cz)),
        #   facecolors=colors,
        #   edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
        #   linewidth=0.5)
# ax.set(xlabel='r', ylabel='g', zlabel='b')
# ax.set_aspect('equal')

# plt.show()
