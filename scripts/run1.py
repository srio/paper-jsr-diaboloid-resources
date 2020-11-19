#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#
import Shadow
import numpy

import matplotlib.pylab as plt
from srxraylib.plot.gol import set_qt

set_qt()

def get_fwhm(histogram, bins):
    quote = numpy.max(histogram)*0.5
    cursor = numpy.where(histogram >= quote)


    bin_size = bins[1] - bins[0]
    if histogram[cursor].size > 1:
        fwhm        = bin_size*(cursor[0][-1]-cursor[0][0])
        coordinates = (bins[cursor[0][0]], bins[cursor[0][-1]])
    elif histogram[cursor].size == 1:
        fwhm        = bin_size
        coordinates = (bins[cursor[0][0]], bins[cursor[0][0]])
    else:
        fwhm = 0.0
        coordinates = None

    return fwhm, quote, coordinates

def get_tkt_fwhm(tkt):
    from srxraylib.plot.gol import plot
    # from oasys.util.oasys_util import get_fwhm

    x = tkt["bin_h_center"]
    y = tkt["bin_v_center"]
    hx = tkt["histogram_h"]
    hy = tkt["histogram_v"]
    plot(x, hx)
    plot(y, hy)

    fwhm_x, _, _ = get_fwhm(hx, x)
    fwhm_y, _, _ = get_fwhm(hy, y)
    return fwhm_x, fwhm_y

def run_shadow():
    #
    # Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
    #
    import Shadow
    import numpy

    # write (1) or not (0) SHADOW files start.xx end.xx star.xx
    iwrite = 0

    #
    # initialize shadow3 source (oe0) and beam
    #
    beam = Shadow.Beam()
    oe0 = Shadow.Source()
    oe1 = Shadow.OE()
    oe2 = Shadow.OE()

    #
    # Define variables. See meaning of variables in:
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/source.nml
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/oe.nml
    #

    oe0.FDISTR = 1
    oe0.FSOUR = 0
    oe0.F_PHOT = 0
    oe0.HDIV1 = 0.0025
    oe0.HDIV2 = 0.0025
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.ISTAR1 = 5676561
    oe0.NPOINT = 50000
    oe0.PH1 = 30000.0
    oe0.VDIV1 = 0.00025
    oe0.VDIV2 = 0.00025

    oe1.DUMMY = 100.0
    oe1.FCYL = 1
    oe1.FMIRR = 4
    oe1.FWRITE = 1
    oe1.F_DEFAULT = 0
    oe1.SIMAG = 10000000.0
    oe1.SSOUR = 6.5
    oe1.THETA = 89.885408441
    oe1.T_IMAGE = 0.0
    oe1.T_INCIDENCE = 89.885408441
    oe1.T_REFLECTION = 89.885408441
    oe1.T_SOURCE = 6.5

    oe2.DUMMY = 100.0
    oe2.FHIT_C = 1
    oe2.FILE_RIP = b'/home/srio/Oasys/diaboloid_bl1222_shadow.dat'
    oe2.FWRITE = 1
    oe2.F_G_S = 2
    oe2.F_RIPPLE = 1
    oe2.RLEN1 = 0.4
    oe2.RLEN2 = 0.4
    oe2.RWIDX1 = 0.01
    oe2.RWIDX2 = 0.01
    oe2.T_IMAGE = 8.075
    oe2.T_INCIDENCE = 89.885408441
    oe2.T_REFLECTION = 89.885408441
    oe2.T_SOURCE = 12.3

    # Run SHADOW to create the source

    if iwrite:
        oe0.write("start.00")

    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    #
    # run optical element 1
    #
    print("    Running optical element: %d" % (1))
    if iwrite:
        oe1.write("start.01")

    beam.traceOE(oe1, 1)

    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    #
    # run optical element 2
    #
    print("    Running optical element: %d" % (2))
    if iwrite:
        oe2.write("start.02")

    beam.traceOE(oe2, 2)

    if iwrite:
        oe2.write("end.02")
        beam.write("star.02")

    # Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space")
    # Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
    # Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")

    return beam


def plot_ticket_plotxy(tkt, col_h=1, col_v=3, title="", xtitle="", ytitle="", filename="", hfactor=1e4, vfactor=1e4):
    cmap = plt.cm.jet  # Greys #cm.coolwarm

    fx = 11
    fy = 11
    figure = plt.figure(figsize=(fx, fy))

    left, width = 0.13, 0.61
    bottom, height = 0.09, 0.61
    bottom_h = left_h = left + width + 0.02
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    #
    # main plot
    #
    axScatter = figure.add_axes(rect_scatter)

    axScatter.set_xlabel(xtitle, fontsize=20)
    axScatter.set_ylabel(ytitle, fontsize=20)

    axScatter.axis(xmin=hfactor * tkt["xrange"][0], xmax=hfactor * tkt["xrange"][1])
    axScatter.axis(ymin=vfactor * tkt["yrange"][0], ymax=vfactor * tkt["yrange"][1])

    axScatter.set_aspect(1.0)

    axScatter.pcolormesh(hfactor * tkt["bin_h_edges"], vfactor * tkt["bin_v_edges"], tkt["histogram"].T, cmap=cmap)

    axScatter.tick_params(labelsize=24)

    #
    # histograms
    #
    axHistx = figure.add_axes(rect_histx, sharex=axScatter)
    axHisty = figure.add_axes(rect_histy, sharey=axScatter)

    tmp_h_b = []
    tmp_h_h = []
    for s, t, v in zip(hfactor * tkt["bin_h_left"], hfactor * tkt["bin_h_right"], tkt["histogram_h"]):
        tmp_h_b.append(s)
        tmp_h_h.append(v)
        tmp_h_b.append(t)
        tmp_h_h.append(v)
        tmp_v_b = []
        tmp_v_h = []
    for s, t, v in zip(vfactor * tkt["bin_v_left"], vfactor * tkt["bin_v_right"], tkt["histogram_v"]):
        tmp_v_b.append(s)
        tmp_v_h.append(v)
        tmp_v_b.append(t)
        tmp_v_h.append(v)

    axHistx.plot(tmp_h_b, tmp_h_h)
    axHisty.plot(tmp_v_h, tmp_v_b)

    # supress ordinates labels ans ticks
    axHistx.get_yaxis().set_visible(False)
    axHisty.get_xaxis().set_visible(False)

    # supress abscissas labels (keep ticks)
    for tl in axHistx.get_xticklabels(): tl.set_visible(False)
    for tl in axHisty.get_yticklabels(): tl.set_visible(False)

    if title != None:
        axHistx.set_title(title, fontsize=20)

    if filename != "":
        plt.savefig(filename)
        print("File written to disk: %s" % filename)

    plt.show()
    return tkt




if True:
    beam = run_shadow()
    # Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space")
# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")

    # beam = in_object_1._beam
    tkt = beam.histo2(1, 3, ref=23, nolost=1, nbins=301, xrange=[-750e-6, 750e-6], yrange=[-0.0005, 0.001])

    plot_ticket_plotxy(tkt, hfactor=1e6, vfactor=1e6, xtitle="H [$\mu$m]", ytitle="V [$\mu$m]", filename="tmp.png",
                       ) # title="%3.1f x %3.1f nm$^2$" % (tkt["fwhm_h"] * 1e7, tkt["fwhm_v"] * 1e7))

    print("%g, %g " % get_tkt_fwhm(tkt))
    # print("Transmission: %6.3f percent"%(100*beam.intensity(nolost=1)/beam.nrays()))
