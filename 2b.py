import matplotlib.pyplot as plt
import numpy as np
from sympy import Eq, symbols, tanh
from sympy.plotting.plot_implicit import ImplicitSeries
from sympy.plotting.plot import _matplotlib_list
import math

# Define constants
GRAVITY = 980.665
FREQUENCY = 10
SURFACE_TENSION_RATIO = 74.3
X_LOWER = 0.15
X_UPPER = 1.05
Y_LOWER = 12
Y_UPPER = 32
RESOLUTION = 200

# Measured data
x_data = np.array([0.2, 0.4, 0.6, 0.8, 1])
y_data = np.array([15, 17.9, 20.2, 21.4, 21.4])
err_x = np.ones(5) * 0.025
err_y = np.array([0.6, 0.3, 0.3, 0.4, 0.3])

# Shallow water equation
x_shallow = np.linspace(X_LOWER, X_UPPER, RESOLUTION)
y_shallow = (x_shallow * GRAVITY) ** 0.5


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
x_no_surface_tension, y_no_surface_tension = get_xy_for_implicit(
    Eq(ys ** 2, (GRAVITY * ys / anglr_freq * tanh(anglr_freq * xs / ys)))
)

# Plot
plt.errorbar(x_data, y_data, yerr=err_y, xerr=err_x, fmt="o")
plt.plot(x_true_equation, y_true_equation, "y")
plt.plot(x_no_surface_tension, y_no_surface_tension, "y:")
plt.plot(x_shallow, y_shallow, "orange")

plt.xlabel("Water Depth (cm)")
plt.ylabel("Wave Velocity (cm/s)")
plt.legend(["Complete equation (Eq. 3)", "Complete equation w/o surface tension", "Shallow water equation (Eq. 4)",
            "Measured velocity"])

# Show and save
plt.savefig("2b.png")
plt.show()

# Analysis

# Construct from the true equation the values we should have gotten
y_expected = []
source_index = 0
for i, val in enumerate(x_true_equation):
    # If we've passed in x the x_data value we're looking to match
    if val > x_data[source_index]:
        # Means the average between previous point and this point gives us our value
        y_expected.append(0.5 * (y_true_equation[i] + y_true_equation[i - 1]))
        # Increment source_index to indicate we want to match the next value now
        source_index += 1
        if source_index == len(x_data):
            break

# Find error
error = (y_expected - y_data) / y_data
print(sum(error) / len(error))