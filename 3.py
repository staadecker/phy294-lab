import matplotlib.pyplot as plt
import numpy as np
from sympy import Eq, symbols, tanh
from sympy.plotting.plot_implicit import ImplicitSeries
from sympy.plotting.plot import _matplotlib_list
import math

# Set style
plt.rcParams["font.family"] = "sans-serif"

# Define constants
GRAVITY = 980.665
FREQUENCY = 10
FREQUENCY3 = 15
SURFACE_TENSION_RATIO = 74.3
X_LOWER = 0.15
X_UPPER = 1.05
Y_LOWER = 12
Y_UPPER = 32
RESOLUTION = 200


def get_xy_for_implicit(expr):
    """
    Returns x y arrays for an implicit sympy expression using the internals
    of the sympy library.
    """
    # Sympy doesn't normally let us work with matplotlib so we need to be clever
    # After inspecting sympy source code, the following internal functions seem to
    # do what we need.
    series = ImplicitSeries(expr, (xs, X_LOWER, X_UPPER), (ys, Y_LOWER, Y_UPPER), True, True, 0, 300, 'blue')
    x, y = _matplotlib_list(series.get_raster()[0])
    # Only return a subset of points to respect resolution
    x = x[::len(x) // RESOLUTION]
    y = y[::len(y) // RESOLUTION]
    return x, y


# Calculate complete equation and complete equation w/o surface tension
xs, ys = symbols("xs ys")
anglr_freq = 2 * math.pi * FREQUENCY

x_true_equation, y_true_equation = get_xy_for_implicit(
    Eq(ys ** 2, ((GRAVITY * ys / anglr_freq + anglr_freq * SURFACE_TENSION_RATIO / ys) * tanh(anglr_freq * xs / ys)))
)
anglr_freq = 2 * math.pi * FREQUENCY3
x_3, y_3 = get_xy_for_implicit(
    Eq(ys ** 2, ((GRAVITY * ys / anglr_freq + anglr_freq * SURFACE_TENSION_RATIO / ys) * tanh(anglr_freq * xs / ys)))
)

# Plot
plt.plot(x_true_equation, y_true_equation)
plt.plot(x_3, y_3)

plt.xlabel("Water Depth (cm)")
plt.ylabel("Wave Velocity (cm/s)")
plt.legend(["Expected values at 10 Hz", "Expected values at 15 Hz"])

plt.savefig("3.png")
plt.show()