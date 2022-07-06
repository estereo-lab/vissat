
# Experimental IR sub-rutine

print(" ")
print("Reading observed IR spectra...")
print(" ")

import numpy as np
import scipy.interpolate as interpolate
import global_var
import os
import conditions



# Data imput files

expIR = np.genfromtxt(os.path.join(global_var.parent_dir,'IRexp.txt'), dtype=float)

expfreq = np.array(expIR[:,0])
expinten = np.array(expIR[:,1])

# Translating observed IR Spectra into spline function

t, c, k = interpolate.splrep(expfreq, expinten, s=0, k=3)


xmin, xmax = conditions.r1, conditions.r2
N = xmax - xmin + 1
xx = np.linspace(xmin, xmax, N)

fexpir = interpolate.BSpline(t, c, k, extrapolate=False)

Yexpir = fexpir(xx)

print("done")
print(" ")