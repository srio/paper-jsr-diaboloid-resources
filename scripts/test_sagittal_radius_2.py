import numpy
from srxraylib.plot.gol import plot
import matplotlib.pylab as plt

p=20
theta=2e-3

Y = numpy.linspace(-0.8, 0.8, 1001)

p=20
q=5
RRs5 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

p=20
q=10
RRs10 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

p=20
q=15
RRs15 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

f = plot(
     Y, RRs5,
     Y, RRs10,
     Y, RRs15,
     # Y, R0s + pendent * Y,
     # Y, RRRs,
     legend=["p=20, q=5 Type I","p=20, q=10 Type I","p=20, q=15 Type I"], #, "Rs linearized (Eq. 9)", "Rs naive (see text)", ],
     xtitle="Y [m]", ytitle="Rs [m]", title="theta=2mrad",show=0)

q=20
p=5
RRs5 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

q=20
p=10
RRs10 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

q=20
p=15
RRs15 = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

f = plot(
     numpy.flip(Y), RRs5,
     numpy.flip(Y), RRs10,
     numpy.flip(Y), RRs15,
     # Y, R0s + pendent * Y,
     # Y, RRRs,
     legend=["p=20, q=5 Type II","p=20, q=10 Type II","p=20, q=15 Type II"], #, "Rs linearized (Eq. 9)", "Rs naive (see text)", ],
     xtitle="Y [m]", ytitle="Rs [m]", title="theta=2mrad",show=1)