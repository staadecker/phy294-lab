import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.rcParams["font.family"] = "sans-serif"

# Data
x = np.array([5, 10, 15, 20, 25])
y = np.array([4.32, 2.17, 1.41, 1.03, 0.85])

x_error = np.ones(5) * 0.05
y_error = np.array([0.08, 0.04, 0.04, 0.07, 0.03])

# Plot
plt.errorbar(x, y, yerr=y_error, xerr=x_error, fmt="o")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Wavelength (cm)")
plt.ylim(0, None)

# Show
plt.savefig("2a.png")
plt.show()
