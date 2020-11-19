import numpy
from srxraylib.plot.gol import plot
import matplotlib.pylab as plt
import matplotlib
# matplotlib.rc('xtick', labelsize=12)
# matplotlib.rc('ytick', labelsize=12)
plt.rcParams.update({'font.size':18})

p=18.8
q=8.075
theta=2e-3


Y = numpy.linspace(-0.8, 0.8, 1001)

# coddington Eq
Rs = 2.0 * numpy.sin(theta) / (1 / p + 1 / q) + Y * 0
# corrected value
print("Correction factor: ", (numpy.cos(theta))**2  )
R0s = 2.0 * numpy.sin(theta) * (numpy.cos(theta))**2 / (1 / p + 1 / q) + Y * 0  # NEW

# exact variation of Rs
YY = Y * numpy.cos(theta)  # added to pass y -> Y
RRs = 2 * p * numpy.sin(theta) * numpy.cos(theta) * (q - YY)  * numpy.sqrt(YY / p + (numpy.cos(theta))**2) / (p + q)

#naive solution
pY = -p * numpy.cos(theta)
pZ = p * numpy.sin(theta)

qY = q * numpy.cos(theta)
qZ = q * numpy.sin(theta)

P = numpy.sqrt( (pY - Y)**2 + pZ)
Q = numpy.sqrt( (qY - Y)**2 + qZ)
THETA = numpy.arcsin( p * numpy.sin(theta) / P)
RRRs = 2.0 * numpy.sin(THETA) / (1 / P + 1 / Q)

# linearized
# pendent = 1 / (p + q) * (numpy.tan(theta) * q - 2 * p * numpy.sin(theta) * numpy.cos(theta))
# print("pendent1", pendent)
pendent = - numpy.sin(theta) * numpy.cos(theta) / (p+q) * (2 * p * (numpy.cos(theta))**2 - q)
# print("pendent2", pendent)

fig, ax = plot(
     Y, RRs,
     Y, R0s + pendent * Y,
     Y, RRRs,
     legend=["Rs (non-linear, Eq. 9)", "Rs (linearized, Eq. 10)", "Rs naive (see text)", ],
     xtitle="Y [m]", ytitle="Rs [m]", show=0, figsize=(10,6))

plt.savefig("sagittalradius.png")
print("File writte to disk: sagittalradius.png")

plt.show()

