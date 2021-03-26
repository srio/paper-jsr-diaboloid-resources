from srxraylib.plot.gol import plot_image, plot, plot_show, set_qt
import numpy

# import h5py
# import matplotlib
import pylab as plt



set_qt()


def create_surface(p=20.0,M=1.0,theta=2e-3,shape='diaboloid'):

    # file available at: https://github.com/oasys-kit/OASYS-SYNED/blob/master/orangecontrib/syned/util/diaboloid_tools.py
    from orangecontrib.syned.util.diaboloid_tools import diaboloid_exact_segment_to_point
    from orangecontrib.syned.util.diaboloid_tools import toroid_segment_to_point
    from orangecontrib.syned.util.diaboloid_tools import parabolic_cone_linearized_segment_to_point
    from orangecontrib.syned.util.diaboloid_tools import parabolic_cone_segment_to_point


    Y = numpy.linspace(-0.4, 0.4, 1001)
    X = numpy.linspace(-0.01, 0.01, 101)

    q = p * M
    Zt = toroid_segment_to_point(
               p=p,
               q=q,
               theta=theta,
               x=X,
               y=Y)

    if shape == 'diaboloid':
        Zd, XX, YY = diaboloid_exact_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'parabolic-cone':
        Zd, XX, YY = parabolic_cone_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'linearized-parabolic-cone':
        Zd, XX, YY = parabolic_cone_linearized_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif shape == 'elliptical-cylinder':
        Zd, XX, YY = diaboloid_exact_segment_to_point(
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

def do_plot(Z, X, Y, filename_root="tmp", title="", do_show=False, legend_position=None):
    fontsize = 40
    # fontsize_legend = 22
    # matplotlib.rc('xtick', labelsize=fontsize)
    # matplotlib.rc('ytick', labelsize=fontsize)
    # params = {'legend.fontsize':     fontsize,
    #           'legend.handlelength': fontsize // 20}
    # plt.rcParams.update(params)


    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams.update({'figure.autolayout': True})

    plt.rc('font', size=fontsize)
    # plt.rc('axes', titlesize=fontsize)
    plt.rc('axes',  labelsize=fontsize * 8 // 10)
    plt.rc('xtick', labelsize=fontsize * 8 // 10)
    plt.rc('ytick', labelsize=fontsize * 8 // 10)
    # plt.tight_layout()

    # from matplotlib import rcParams

#
    ff = 1.5 # 3.5 # 1.5
    figsize  = [7 * ff, 7 * ff]
    figsize2 = [7 * ff, 6 * ff / 2 + 2]

    # plt.gcf().subplots_adjust(bottom=0.15)

    nx, ny = Z.shape


    xtitle="X [mm]"
    ytitle="Y [mm]"
    fig, ax = plot_image(1e6 * Z, 1e3 * X, 1e3 * Y, yrange=[-405,405],
                         cmap='jet', aspect='auto', figsize=figsize, add_colorbar=False, title="", show=False)


    ax.set_xlabel(xtitle,) #fontsize=fontsize)
    ax.set_ylabel(ytitle,) #fontsize=fontsize)
    ax.set_title(title,  ) #fontsize=fontsize)

    # ONLY 5 ticks in Y
    ymin, ymax = ax.get_ylim()
    ax.set_yticks(numpy.round(numpy.linspace(-400, 400, 5), 2))

    ax.plot([-100, 100], [-400, -400], linestyle="--")
    ax.plot([-100, 100], [-100,-100])
    ax.plot([-100, 100], [0,0], linestyle="-.")
    ax.plot([-100, 100], [100,100])
    ax.plot([-100, 100], [400,400], linestyle="--", color='cyan')

    filename_png = filename_root + "_image.png"

    plt.savefig(filename_png)  # ,dpi=600)
    print("File written to disk: %s" % filename_png)
    if do_show: plt.show()


    #
    #
    #

    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams.update({'figure.autolayout': True})
    #
    plt.rc('font', size=fontsize * 3 // 4)
    # plt.rc('axes', titlesize=fontsize)
    plt.rc('axes', labelsize=fontsize * 5 // 8)
    plt.rc('xtick', labelsize=fontsize * 5 // 8)

    plt.rc('legend', fontsize=fontsize * 4 // 8)
    if legend_position is not None:
        plt.rc('legend', loc=legend_position)


    # plt.legend(frameon=False)
    # ax2.legend(loc='upper left', frameon=None)
    # plt.rc('ytick', labelsize=fontsize * 8 // 10)
    # plt.tight_layout()


    x = X * 1e3
    z0 = Z[:,ny//2] * 1e6

    # zstart = Z[:, 0] * 1e6
    # zend   = Z[:, -1] * 1e6

    zstart = Z[:, ny * 3 // 8] * 1e6
    zend   = Z[:, ny * 5 // 8] * 1e6

    zstart0 = Z[:, 0] * 1e6
    zend0   = Z[:, -1] * 1e6

    ytitle="Z [$\mu$m]"
    xtitle="X [mm]"
    fig, ax = plot(x, zstart0,
                   x, zstart,
                   x, z0,
                   x, zend,
                   x, zend0,
                   show=0,
                   figsize=figsize2,
                   # title=title,
                   legend=["Y=-400", "Y=-100", "Y=0", "Y=100", "Y=400"],
                   linestyle=["--",None,"-.",None,"--"],
                   color=[None,None,None,None,'cyan'])

    plt.legend(frameon=False)
    # ax2.legend(loc='upper left', frameon=None)
    # fig.legend(loc=1, prop={'size': 6})
    # import matplotlib

    ax.set_xlabel(xtitle, fontsize=fontsize * 5 // 8)
    ax.set_ylabel(ytitle, fontsize=fontsize * 5 // 8)


    filename_png = filename_root + "_profile.png"

    plt.savefig(filename_png)  # ,dpi=600)
    print("File written to disk: %s" % filename_png)
    if do_show: plt.show()

if __name__ == "__main__":

    #
    # FIG 7
    #
    if True:
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
            title=r"$\theta$=%d mrad    M=q:p=1:%d" % (int(THETA[i]*1e3), int(1/M[i]))
            do_plot(Z, X, Y, filename_root=CASES[i], title=title, do_show=False, legend_position='lower center')

    #
    # FIG 8
    #


    if False:
        CASES = [
            "diaboloid_bl1222_detrended",
            # "paraboliccone_bl1222_detrended",
            "ellipticalcylinder_bl1222_detrended",
            "linearized-parabolic-cone_bl1222_detrended",
            ]

        SHAPES = ['diaboloid',
                  # 'parabolic-cone',
                  'elliptical-cylinder',
                  'linearized-parabolic-cone'
                  ]

        for i in range(len(CASES)):
            Z, X, Y = create_surface(p=18.8, M=8.0750/18.8000, theta=2.0e-3, shape=SHAPES[i],)
            do_plot(Z, X, Y, filename_root=CASES[i], do_show=False)



    # Z, X, Y = create_surface(p=18.8, M=8.0750 / 18.8000, theta=2.0e-3, shape='linearized-parabolic-cone' )
    # title = r"$\theta$=%d mrad    M=q:p=1:%d" % (int(2e-3 * 1e3), int(1 / (18.0/8.075)))
    # do_plot(Z, X, Y, filename_root="linearizedparaboliccone_bl1222_detrended", title=title, do_show=False)

    plot_show()