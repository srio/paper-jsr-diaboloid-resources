import numpy
from srxraylib.plot.gol import plot
import matplotlib.pylab as plt

p=18.8
q=8.075
theta=2e-3


Y = numpy.linspace(-0.8, 0.8, 1001)

Rs = 2.0 * numpy.sin(theta) / (1 / p + 1 / q) + Y * 0
R0s = numpy.sin(2 * theta) / (1 / p + 1 / q) + Y * 0

RRs = 2 * p * (q - Y) * numpy.sin(theta) * numpy.sqrt(Y / p + (numpy.cos(theta))**2) / (p + q)

pY = -p * numpy.cos(theta)
pZ = p * numpy.sin(theta)

qY = q * numpy.cos(theta)
qZ = q * numpy.sin(theta)

P = numpy.sqrt( (pY - Y)**2 + pZ)
Q = numpy.sqrt( (qY - Y)**2 + qZ)
THETA = numpy.arcsin( p * numpy.sin(theta) / P)
RRRs = 2.0 * numpy.sin(THETA) / (1 / P + 1 / Q)

pendent = 1 / (p + q) * (numpy.tan(theta) * q - 2 * p * numpy.sin(theta) * numpy.cos(theta))

f = plot(
     Y, RRs,
     Y, R0s + pendent * Y,
     Y, RRRs,
     legend=["Rs (Eq. 8)", "Rs linearized (Eq. 9)", "Rs naive (see text)", ],
     xtitle="Y [m]", ytitle="Rs [m]", show=0)

plt.savefig("sagittalradius.png")
print("File writte to disk: sagittalradius.png")

plt.show()

