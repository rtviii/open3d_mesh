import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

with open('./encodings/6Z6K.json', 'r') as infile:
    data = json.load(infile)


C = np.array(data['coordinates'])

print("Normalize to origin")
Cx = C[:,0] - np.mean(C[:,0])
Cy = C[:,1] - np.mean(C[:,1])
Cz = C[:,2] - np.mean(C[:,2])

print("Calculating max deviation from zero")
dev =  np.min(
        [   
        np.min(Cx),
        np.min(Cy),
        np.min(Cz)
        ])

Cx = Cx + abs(dev)
Cy = Cy + abs(dev)
Cz = Cz + abs(dev)




# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# n = 100
# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# # ax.scatter(Cx, Cy, Cz)
# plt.show()
# # np.min(Cx)
# np.min(Cy)
# np.min(Cz)
# r, g, b = np.indices((17, 17, 17)) / 16.0


sphere = []

ax = plt.figure().add_subplot(projection='3d')

ax.voxels(np.array(zip(Cx,Cy,Cz)),
        #   facecolors=colors,
        #   edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
          linewidth=0.5)
ax.set(xlabel='r', ylabel='g', zlabel='b')
ax.set_aspect('equal')

plt.show()
