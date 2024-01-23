import numpy as np
import matplotlib.pyplot as plt

x, y, z = np.indices((8, 8, 8))

# cube1 = (x < 3) & (y < 3) & (z < 3)
# cube2 = (x >= 5) & (y >= 5) & (z >= 5)
# link = abs(x - y) + abs(y - z) + abs(z - x) <= 2
# print(x)
# print(y)
# print("-------")
# voxelarray = x | y | z
# voxelarray[2,2,2] = 1  
# print(np.shape(voxelarray))

# colors = np.empty(voxelarray.shape, dtype=object)

# colors[link] = 'red'
# colors[cube1] = 'blue'
# colors[cube2] = 'green'

ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x, edgecolor='k')
plt.show()