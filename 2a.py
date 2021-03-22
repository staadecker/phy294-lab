import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Set style
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.figsize"] = (10, 4)

# Data
x = np.array([5, 10, 15, 20, 25])
y = np.array([4.32, 2.17, 1.41, 1.03, 0.85])

x_error = np.ones(5) * 0.05
y_error = np.array([0.08, 0.04, 0.04, 0.07, 0.03])

fig, axs = plt.subplots(1, 3)

# Plot
axs[0].errorbar(x, y, yerr=y_error, xerr=x_error, fmt="o")

axs[0].set_xlabel("Frequency (Hz)")
axs[0].set_ylabel("Wavelength (cm)")
axs[0].set_ylim(0, None)

period = 1 / x
period_error = x_error / x ** 2
axs[1].errorbar(period, y, yerr=y_error, xerr=period_error, fmt=".")
axs[1].set_xlabel("Period (s)")
# axs[1].set_ylabel("Wavelength (cm)")
axs[1].set_ylim(0, None)

# Linear regression
result = linregress(period, y)
x_conti = np.linspace(0.03, 0.22)
y_conti = result.intercept + result.slope * x_conti
axs[1].plot(x_conti, y_conti)

# Residuals
axs[2].scatter(period, y - result.intercept - period * result.slope)
axs[2].set_xlabel("Period (s)")
# axs[2].set_ylabel("Residuals")

# Show
plt.savefig("2a.png")
plt.show()
