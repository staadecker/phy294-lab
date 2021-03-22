import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Set style
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.figsize"] = (10, 4)

# Data
x = np.array([0.25, 0.286, 0.333, 0.4, 0.5])
y = np.array([0.15, 0.3, 0.39, 0.54, 0.69])

x_error = np.array([0.006, 0.008, 0.011, 0.016, 0.025])
y_error = np.array([0.03, 0.01, 0.04, 0.02, 0.02])

# Linear regression
result = linregress(x, y)
x_conti = np.linspace(0.23, 0.57)
y_conti = result.intercept + result.slope * x_conti

# Plot
figure, axs = plt.subplots(1, 2)
axs[0].errorbar(x, y, yerr=y_error, xerr=x_error, fmt="o")
axs[0].plot(x_conti, y_conti)

axs[0].set_xlabel("1/a (cm^-1)")
axs[0].set_ylabel("sin(theta)")
axs[0].set_ylim(0, None)

axs[1].scatter(x, y - result.intercept - x * result.slope)
axs[1].set_xlabel("1/a (cm^-1)")
axs[1].set_ylabel("Residuals")

# Show
plt.savefig("4a.png")
plt.show()
