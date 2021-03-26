#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#
import Shadow
import numpy


def run_shadow(T_IMAGE=8.075, RWIDX=0.02):
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

    oe0.BENER = 2.0
    oe0.EPSI_X = 1.5000000000000003e-11
    oe0.EPSI_Z = 7.49e-11
    oe0.FDISTR = 4
    oe0.FSOURCE_DEPTH = 4
    oe0.F_COLOR = 3
    oe0.F_PHOT = 0
    oe0.HDIV1 = 0.0005
    oe0.HDIV2 = 0.0005
    oe0.ISTAR1 = 5676561
    oe0.NCOL = 0
    oe0.NPOINT = 50000
    oe0.N_COLOR = 0
    oe0.PH1 = 30000.0
    oe0.PH2 = 30005.0
    oe0.POL_DEG = 0.0
    oe0.R_ALADDIN = 1.419421681694264
    oe0.R_MAGNET = 1.419421681694264
    oe0.SIGDIX = 0.0
    oe0.SIGDIZ = 0.0
    oe0.SIGMAX = 1e-05
    oe0.SIGMAY = 0.0
    oe0.SIGMAZ = 7e-06
    oe0.VDIV1 = 1.0
    oe0.VDIV2 = 1.0
    oe0.WXSOU = 0.0
    oe0.WYSOU = 0.0
    oe0.WZSOU = 0.0

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
    oe2.FILE_RIP = b'diaboloid_shadow.dat'
    oe2.FWRITE = 1
    oe2.F_G_S = 2
    oe2.F_RIPPLE = 1
    oe2.RLEN1 = 0.4
    oe2.RLEN2 = 0.4
    oe2.RWIDX1 = RWIDX # 0.02
    oe2.RWIDX2 = RWIDX # 0.02
    oe2.T_IMAGE = T_IMAGE # T_IMAGE=8.075
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

    return beam

def create_surface_file(ftype="toroid",p=18.8,q=8.075,theta=2e-3,ratio=1.0):
    from Shadow import ShadowTools as ST
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import ken_diaboloid_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import valeriy_diaboloid_exact_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import valeriy_parabolic_cone_segment_to_point
    from orangecontrib.syned.als.widgets.tools.ow_als_diaboloid import toroid_segment_to_point

    Rs = 2.0 * numpy.sin(theta) / (1 / p + 1 / q) * ratio
    Y = numpy.linspace(-0.8, 0.8, 1001)
    X = numpy.linspace(-Rs, Rs, 101)

    if ftype == "toroid":
        Z = toroid_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif ftype == "diaboloid":
        Z, XX, YY = valeriy_diaboloid_exact_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)
    elif ftype == "parabolic-cone":
        Z, XX, YY = valeriy_parabolic_cone_segment_to_point(
                   p=p,
                   q=q,
                   theta=theta,
                   x=X,
                   y=Y)

    # print(Z.shape, X.shape, Y.shape)
    ST.write_shadow_surface(Z.T,
                            X,
                            Y,
                            "diaboloid_shadow.dat")

    return Rs



def plot_ticket_plotxy(tkt, col_h=1, col_v=3, title="", xtitle="", ytitle="", filename="", hfactor=1e4, vfactor=1e4):
    import matplotlib.pylab as plt
    from srxraylib.plot.gol import set_qt

    set_qt()
    cmap = plt.cm.PuBu  # plt.cm.jet # Greys #cm.coolwarm

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

    # axScatter.set_aspect(1.0)

    axScatter.pcolormesh(hfactor * tkt["bin_h_edges"], vfactor * tkt["bin_v_edges"], tkt["histogram"].T, cmap=cmap)

    axScatter.tick_params(labelsize=24)

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
    p = 18.8

    # M = numpy.array([10])
    M = numpy.linspace(1, 10, 400)
    nruns = M.size
    out = numpy.zeros((10,nruns))
    theta = 2e-3

    for i,m in enumerate(M):

        q = p / m # 8.075

        # Rs = create_surface_file(ftype="diaboloid", q=q, ratio=0.81)
        Rs = create_surface_file(ftype="parabolic-cone", q=q, ratio=0.81)
        # Rs = create_surface_file(ftype="toroid", q=q, ratio=0.99)
        beam = run_shadow(T_IMAGE=q, RWIDX=Rs)

        tkt = beam.histo2(1, 3, ref=23, nolost=1, nbins=301) #, xrange=[-200e-6, 200e-6], yrange=[-350e-6, 50e-6])

        if M.size == 1:
            plot_ticket_plotxy(tkt, hfactor=1e6, vfactor=1e6, xtitle="H [nm]", ytitle="V [nm]", filename="",
                               title="%3.1f x %3.1f nm$^2$  M=%4.2f" % (tkt["fwhm_h"] * 1e6, tkt["fwhm_v"] * 1e6, m))

        out[0, i] = m
        try:
            out[1, i] = tkt["fwhm_h"] * 1e6
        except:
            out[1, i] = 0

        try:
            out[2, i] = tkt["fwhm_v"] * 1e6
        except:
            out[2, i] = 0
        out[3, i] = q
        out[4, i] = beam.intensity(nolost=0)
        out[5, i] = beam.intensity(nolost=1)
        out[6, i] = Rs
        out[7, i] = beam.get_standard_deviation(1, nolost=1) * 1e6
        out[8, i] = beam.get_standard_deviation(3, nolost=1) * 1e6

    f = open("tmp.dat",'w')
    for i in range(nruns):
        f.write("%g %g %g %g %g %g %g %g %g\n" %
                (out[0,i], out[1,i], out[2,i], out[3,i], out[4,i], out[5,i], out[6,i], out[7,i], out[8,i]))
    f.close()
    print("File written to disk: tmp.dat")

    from srxraylib.plot.gol import plot
    plot(out[0, :], out[1, :],
         out[0, :], out[2, :],
         out[0, :], out[7, :],
         out[0, :], out[8, :],
         legend=["FWHM H um","FWHM V um", "sigma H um","sigma V um"],
         yrange=[0,100],
         xtitle="DeMagnification",ytitle="")

# Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space M=%f"%M)
# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")
