from srxraylib.plot.gol import plot_image, plot
import h5py

import pylab as plt
from matplotlib.colors import Normalize


filename = "/home/srio/Oasys/diaboloid_detrended.h5"

f = h5py.File(filename, 'r')
X = f["surface_file/X"][:]
Y = f["surface_file/Y"][:]
Z = f["surface_file/Z"][:].T
f.close()
figsize=[7,6]
fig, ax = plot_image(1e6 * Z, 1e3 * X, 1e3 * Y, cmap='jet', aspect='auto', figsize=figsize, add_colorbar=True,
           xtitle="X [mm]", ytitle="Y [mm]", title="diaboloid minus toroid [$\mu$m]", show=False)

# if is_propagated:
#     fig, ax = plot_image(arr1, 1e3 * x, 1e3 * y, cmap='jet', figsize=[9, 5], add_colorbar=False, show=0,
#                          xtitle="X [$\mu$m]", ytitle="Y [$\mu$m]", title="", aspect="equal",
#                          xrange=[-600, 600], yrange=[-300, 300]
#                          )
# else:
#     fig, ax = plot_image(arr1, 1e3 * x, 1e3 * y, cmap='jet', figsize=[12, 4], add_colorbar=False, show=0,
#                          xtitle="X [$\mu$m]", ytitle="Y [$\mu$m]", title="", aspect="equal",
#                          xrange=[-75, 75], yrange=[-20, 20])
#
# ax.xaxis.label.set_size(15)
# ax.yaxis.label.set_size(20)
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)


filename = "/tmp/detrended_image.png"
plt.savefig(filename)  # ,dpi=600)
print("File written to disk: %s" % filename)
plt.show()


#
#
#

nx, ny = Z.shape
x = X * 1e3
z0 = Z[:,ny//2] * 1e6
zstart = Z[:,0] * 1e6
zend = Z[:,-1] * 1e6
plot(x, zstart, x, z0, x, zend, show=0, figsize=[figsize[0], figsize[1]//2],
    xtitle="X [mm]", ytitle="Z [$\mu$m]", legend=["Y=-100", "Y=0", "Y=100"])


filename = "/tmp/detrended_profiles.png"
plt.savefig(filename)  # ,dpi=600)
print("File written to disk: %s" % filename)
plt.show()