import numpy
from srxraylib.plot.gol import plot, set_qt
import matplotlib.pylab as plt


set_qt()

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.autolayout': True})

params = {'legend.fontsize': 15,
          'legend.frameon': False,
          'legend.handlelength': 2,
          # 'axes.titlesize' : 24,
          'axes.labelsize' :   24,
          'lines.linewidth' :  3,
          'lines.markersize' : 10,
          'xtick.labelsize' :  25,
          'ytick.labelsize' :  25,
          # 'grid.color':       'r',
          # 'grid.linestyle':   '-',
          # 'grid.linewidth':     2,
          }
plt.rcParams.update(params)


mirror_names = ["diaboloid", "toroid"] #, "parabolic-cone"]
ylimit = [100, 500, 200]
# ylimit = [60, 200]
# a = numpy.loadtxt("parabolic-cone.dat").T
# a = numpy.loadtxt("diaboloid.dat").T

for i, mirror_name in enumerate(mirror_names):
    a = numpy.loadtxt("%s.dat" % mirror_name).T

    print(a.shape)

    # plot(
    #     1 / a[0, :], a[1, :] * a[0, :],
    #     1 / a[0, :], a[2, :] * a[0, :],
    #     1 / a[0, :], a[5, :] * 100 / (a[5, :]).max(),
    #     legend=["FWHM/Magnification H um","FWHM/Magnification V um", "Integrated Intensity"],
    #     yrange=[0,500],
    #     xtitle="Magnification",ytitle="")

    fig, ax = plot(
        1 / a[0, :], a[1, :] * a[0, :],
        1 / a[0, :], a[7, :] * a[0, :],
        1 / a[0, :], a[2, :] * a[0, :],
        1 / a[0, :], a[8, :] * a[0, :],
        1 / a[0, :], numpy.sqrt(a[2, :] ** 2 + a[1, :] ** 2) * a[0, :],
        1 / a[0, :], numpy.sqrt(a[8, :] ** 2 + a[7, :] ** 2) * a[0, :],
        legend=[
                "Horizontal FWHM/$M$",
                "Horizontal $\sigma/M$",
                "Vertical FWHM/$M$",
                "Vertical $\sigma/M$",
                "Radial FWHM/$M$",
                "Radial $\sigma/M$",
                ],
        yrange=[0,ylimit[i]],xrange=[0.15,1],
        color=['red','red','blue','blue','green','green',],
        linestyle=['--',None,'--',None,'--',None],
        xtitle="Magnification $M$",
        ytitle="Focal size over $M$ [$\mu$m]",
        show=False,
        figsize=(10,6))

    # plt.grid()
    ax.yaxis.grid()

    file_png = "scan_%s.pdf" % mirror_name
    plt.savefig(file_png)
    print("File written to disk: %s" % file_png)

    plt.show()

    tmp1 = numpy.sqrt(a[2, :] ** 2 + a[1, :] ** 2) * a[0, :]
    tmp2 = numpy.sqrt(a[8, :] ** 2 + a[7, :] ** 2) * a[0, :]
    tmp1_min = numpy.argmin(tmp1)
    tmp2_min = numpy.argmin(tmp2)
    print("Minumum found for RADIAL FWHM, sigma", 1 / a[0, tmp1_min], 1 / a[0, tmp2_min] )
    tmp1 = a[2, :]
    tmp2 = a[8, :]
    tmp1_min = numpy.argmin(tmp1)
    tmp2_min = numpy.argmin(tmp2)
    print("Minumum found for VERTICAL FWHM, sigma", 1 / a[0, tmp1_min], 1 / a[0, tmp2_min])

# out[0, i] = m
# out[1, i] = tkt["fwhm_h"] * 1e6
# out[2, i] = tkt["fwhm_v"] * 1e6
# out[3, i] = q
# out[4, i] = beam.intensity(nolost=0)
# out[5, i] = beam.intensity(nolost=1)
# out[6, i] = Rs

plot()