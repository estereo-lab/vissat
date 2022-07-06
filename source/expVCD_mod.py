

# Experimental VCD sub-rutine

print(" ")
print("Reading observed VCD spectra...")
print(" ")


import numpy as np
import scipy.interpolate as interpolate
import global_var
import os

xx = global_var.xx


# Data imput files

expVCD = np.genfromtxt(os.path.join(global_var.parent_dir,'DCVexp.txt'), dtype=float)

expfreq = np.array(expVCD[:,0])
expinten = np.array(expVCD[:,1])

# Translating observed IR Spectra into spline functions

# Full space

t, c, k = interpolate.splrep(expfreq, expinten, s=0, k=3)
fexpvcd = interpolate.BSpline(t, c, k, extrapolate=False)
Yexpvcd = fexpvcd(xx)

# Positive space

expintenpos = np.array(expinten)
expintenpos[expintenpos<0] = 0

t, c, k = interpolate.splrep(expfreq, expintenpos, s=0, k=3)
fexppos = interpolate.BSpline(t, c, k, extrapolate=False)
Yexppos = fexppos(xx)

# Negative space

expintenneg = np.array(expinten)
expintenneg[expintenneg>0] = 0
expintenneg = np.abs(expintenneg)

t, c, k = interpolate.splrep(expfreq, expintenneg, s=0, k=3)
fexpneg = interpolate.BSpline(t, c, k, extrapolate=False)
Yexpneg = fexpneg(xx)

print("done")
print(" ")