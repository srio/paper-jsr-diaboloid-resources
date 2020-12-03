from srxraylib.plot.gol import plot_image, plot
import h5py

import matplotlib
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
import pylab as plt
import numpy

params = {'legend.fontsize': 20,
          'legend.handlelength': 2}
plt.rcParams.update(params)

def create_surface(p=20.0,M=1.0,theta=2e-3,shape='exact'):
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import valeriy_diaboloid_exact_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import toroid_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import valeriy_parabolic_cone_linearized_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import valeriy_parabolic_cone_segment_to_point

    Y = numpy.linspace(-0.1, 0.1, 1001)
    X = numpy.linspace(-0.01, 0.01, 101)

    q = p * M
    Zt = toroid_segment_to_point(
               p=p,
               q=q,
               theta=theta,
               x=X,
               y=Y)

    if shape == 'diaboloid':
        Zd, XX, YY = valeriy_diaboloid_exact_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'parabolic-cone':
        Zd, XX, YY = valeriy_parabolic_cone_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'linearized-parabolic-cone':
        Zd, XX, YY = valeriy_parabolic_cone_linearized_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'elliptical-cylinder':
        Zd, XX, YY = valeriy_diaboloid_exact_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)

        nx, ny = Zd.shape
        sagittal_central_profile = Zd[:,ny//2] - Zd[nx//2,ny//2]
        for i in range(ny):
            Zd[:,i] = Zd[nx//2,i] + sagittal_central_profile



    else:
        raise ("Shape not implemented.")

    return Zd-Zt, X, Y


# def get_surface():
#
#     filename = "/home/srio/Oasys/diaboloid_detrended.h5"
#
#     print("Filename is: ", filename[0:-3])
#
#     f = h5py.File(filename, 'r')
#     X = f["surface_file/X"][:]
#     Y = f["surface_file/Y"][:]
#     Z = f["surface_file/Z"][:].T
#     f.close()
#     return Z, X, Y

def do_plot(Z, X, Y, filename_root="tmp", do_show=False):
    ff = 1.5
    figsize=[7*ff,7*ff]
    figsize2 = [7*ff,6*ff / 2 + 2]

    xtitle="X [mm]"
    ytitle="Y [mm]"
    fig, ax = plot_image(1e6 * Z, 1e3 * X, 1e3 * Y, cmap='jet', aspect='auto', figsize=figsize, add_colorbar=False,title="", show=False)


    ax.set_xlabel(xtitle,fontsize=20)
    ax.set_ylabel(ytitle,fontsize=20)

    # filename_png = filename[0:-3] + "_image.png"
    filename_png = filename_root + "_image.png"

    plt.savefig(filename_png)  # ,dpi=600)
    print("File written to disk: %s" % filename_png)
    if do_show: plt.show()


    #
    #
    #

    nx, ny = Z.shape
    x = X * 1e3
    z0 = Z[:,ny//2] * 1e6
    zstart = Z[:,0] * 1e6
    zend = Z[:,-1] * 1e6
    ytitle="Y [$\mu$m]"
    xtitle="X [mm]"
    fig, ax = plot(x, zstart, x, z0, x, zend, show=0, figsize=figsize2,
        legend=["Y=-100", "Y=0", "Y=100"])

    #fig.legend(loc=1, prop={'size': 6})
    ax.set_xlabel(xtitle,fontsize=22)
    ax.set_ylabel(ytitle,fontsize=22)

    #filename = "/tmp/detrended_profiles.png"
    # filename_png = filename[0:-3] + "_profile.png"
    filename_png = filename_root + "_profile.png"

    plt.savefig(filename_png)  # ,dpi=600)
    print("File written to disk: %s" % filename_png)
    if do_show: plt.show()

if __name__ == "__main__":
    # Z, X, Y = get_surface()

    #
    # FIG 7
    #
    if False:
        CASES = [
            "diaboloid_detrended_1:1",
            "diaboloid_detrended_1:2",
            "diaboloid_detrended_1:5",
            "diaboloid_detrended_5mrad_1:1",
            "diaboloid_detrended_5mrad_1:2",
            "diaboloid_detrended_5mrad_1:5" ]

        THETA = [2e-3, 2e-3, 2e-3, 5e-3, 5e-3, 5e-3]
        M = [1.0, 1.0/2, 1.0/5, 1.0, 1.0/2, 1.0/5,]

        for i in range(len(CASES)):
            Z, X, Y = create_surface(M=M[i], theta=THETA[i])
            do_plot(Z, X, Y, filename_root=CASES[i], do_show=False)

    #
    # FIG 8
    #

    # diaboloid_bl1222_detrended_image.png
    # paraboliccone_bl1222_detrended_image.png
    # ellipticalcylinder_bl1222_detrended_image.png

    if False:
        CASES = [
            "diaboloid_bl1222_detrended",
            "paraboliccone_bl1222_detrended",
            "ellipticalcylinder_bl1222_detrended",
            ]

        SHAPES = ['diaboloid', 'parabolic-cone', 'elliptical-cylinder']

        for i in range(len(CASES)):
            Z, X, Y = create_surface(p=18.8, M=8.0750/18.8000, theta=2.0e-3, shape=SHAPES[i],)
            do_plot(Z, X, Y, filename_root=CASES[i], do_show=False)

    Z, X, Y = create_surface(p=18.8, M=8.0750 / 18.8000, theta=2.0e-3, shape='linearized-parabolic-cone' )
    do_plot(Z, X, Y, filename_root="linearizedparaboliccone_bl1222_detrended", do_show=True)