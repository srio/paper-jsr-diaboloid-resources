import numpy
from srxraylib.plot.gol import plot
a = numpy.loadtxt("diaboloid_sagittal.txt")
x = a[:,0].copy()
y = a[:,1].copy()
print(a.shape,y.shape)

# x = numpy.linspace(0, 0.015, 500)
p = 20.0 # 18.8
q = 10.0 # 8.075
theta = 5e-3 # 2e-3

sin2t = numpy.sin(2 * theta)

#
# sphere
#
ysph = (p + q) / (2 * p * q * sin2t) * x**2
Rs = 2 * numpy.sin(theta) / (1/p + 1/q)
ysphExact = Rs - numpy.sqrt(Rs ** 2 - x ** 2)

# plot(x, ysph,
#      x, ysphExact,
#      legend=["Sphere (quadratic)","Sphere (exact)"])

#
# exact
#
y0 = q * sin2t
ykenExact = y0 - numpy.sqrt( y0**2 + 2 * p**2 + 2 * p * q - 2 * (p + q) * p * numpy.sqrt(1 + (x/p)**2))

f = p * numpy.sin(2 * theta)
yhowardEq1 = f**2 + 2 * q**2 + 2 * p * q - \
     2 * (p + q) * numpy.sqrt(x**2 + q**2)
yhowardEq1 = f - numpy.sqrt(yhowardEq1)
yhowardEq2 = f - numpy.sqrt(f**2 - (p+q) / q * x**2)
yhowardEq4 = 9/4 / (p * numpy.sin(2 * theta))**3 * x**4

plot(
     x, y,
     x, ykenExact,
     x, yhowardEq1,
     x, yhowardEq2,
     legend=["numeric", "ken Eq 27 swapped", "howard Eq 1", "howard Eq 2"],
     xtitle="X [m]", ytitle="Heigh [m]",title="Full shape")

plot(
     x, ykenExact - ysph,
     x, yhowardEq1 - ysph,
     x, yhowardEq2 - ysph,
     x, yhowardEq4,
     legend=["ken Eq 27 swapped - circ", "howard Eq 1 - circ", "howard Eq 2 - circ", "howard Eq 4"],
     xtitle="X [m]", ytitle="Height [m]",title="Differences with circle (quadratic)")

plot(
     x, ykenExact - ysphExact,
     x, yhowardEq1 - ysphExact,
     x, yhowardEq2 - ysphExact,
     x, yhowardEq4,
     legend=["ken Eq 27 swapped - circ", "howard Eq 1 - circ", "howard Eq 2 - circ", "howard Eq 4"],
     xtitle="X [m]", ytitle="Height [m]",title="Differences with circle (exact)")

plot(
     x, ysphExact - yhowardEq2,
     x, yhowardEq4,
     legend=["howard Eq 3 - Eq 2 ", "howard Eq 4"],
     xtitle="X [m]", ytitle="Height [m]",title="Differences (howard paper)")

# yhoward0 =   9 / (4 * p * numpy.sin(theta))
# yhoward1 = 1/8 * (p + q)**2 / (p**2 * q**3  * (numpy.sin(2*theta))**3 )


# print(yhoward0, yhoward1, yhoward2)
# yhoward = yhowardEq4 * x**4


#
# y00 = p * sin2t
# ykenExact00 = y00 - numpy.sqrt( y00**2 - (p + q) /q * x**2)
#
#
#
# ykenApprox = (1/8) * x**4 * (p + q) / (p**2 * y0) * (1/ p + (p + q) / y0**2)
#
# # yken *= numpy.sqrt(y0)
# # yken += 1.0
#

# plot(
#      x, y, #(y - ysphExact) - (y - ysphExact).min(),
#      x, ykenExact,
#      # x, ykenExact00,
#      # x, ykenApprox + ysph,
#      # x, yhoward + ysphExact,
#      legend=["numeric", "kenExact"])

# plot(
#      # x, y - ysph, #(y - ysphExact) - (y - ysphExact).min(),
#      x, ykenExact - ysph,
#      x, ykenApprox,
#      x, yhoward,
#      legend=["kenExact-quadratic","kenApprox","howard"],
#      title="Differences")
#
# plot(
#      # x, y - ysph, #(y - ysphExact) - (y - ysphExact).min(),
#      x, -ykenExact00 + ysphExact,
#      x, yhoward,
#      x, -yhowardEq2 + ysphExact,
#      x, -ykenExact + ysphExact,
#      legend=["-Eq 2 + Eq 3", "Eq 4", "-Eq 1 + Eq 3","KEN"],
#      title="Differences")

# t0 = 1 / p
# t1 = - (p+q) / (q**2 * (numpy.sin(2*theta))**2 )
# print(t0-t1,t0,t1)
#
# print( "(9 * (0.015)**4) / (4 * 20 * numpy.sin(5e-3)) = ", (9 * (0.015)**4) / (4 * 20 * numpy.sin(5e-3)))