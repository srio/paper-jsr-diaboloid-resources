import numpy
from srxraylib.plot.gol import plot
import matplotlib.pylab as plt



mirror_names = ["toroid", "diaboloid", "parabolic-cone"]
ylimit = [500, 50, 200]

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

    plot(
        1 / a[0, :], a[1, :] * a[0, :],
        1 / a[0, :], a[7, :] * a[0, :],
        1 / a[0, :], a[2, :] * a[0, :],
        1 / a[0, :], a[8, :] * a[0, :],
        legend=["FWHM/Magnification H um",
                "sigma/Magnification H um",
                "FWHM/Magnification V um",
                "sigma/Magnification V um"],
        yrange=[0,ylimit[i]],
        color=['red','red','blue','blue'],
        linestyle=['--',None,'--',None],
        xtitle="Magnification",
        ytitle="Width of the intensity distribution [$\mu$m]",
        show=False)

    file_png = "scan_%s.png" % mirror_name
    plt.savefig(file_png)
    print("File written to disk: %s" % file_png)

    plt.show()


# out[0, i] = m
# out[1, i] = tkt["fwhm_h"] * 1e6
# out[2, i] = tkt["fwhm_v"] * 1e6
# out[3, i] = q
# out[4, i] = beam.intensity(nolost=0)
# out[5, i] = beam.intensity(nolost=1)
# out[6, i] = Rs

plot()