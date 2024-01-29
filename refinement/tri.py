import numpy as np
import matplotlib.pyplot as plt

x, y, z = np.indices((8, 8, 8))
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x, edgecolor='k')
plt.show()