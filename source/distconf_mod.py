
import conditions
import numpy as np
import os
import sys

# Conformational Distribution sub-rutine

print(" ")
print("Calculating conformational distribution...")
print(" ")

import global_var

diplist = global_var.diplist
rotlist = global_var.rotlist
nIR = global_var.nIR
nconf = global_var.nconf
nmodes = np.int(global_var.nmodes)

# Data imput files
if conditions.extEnergies == True and conditions.extAbundances == True:
    print("CAN'T USE EXTERNAL ENERGIES AND ABUNDANCES AT THE SAME TIME. EXITING")
    sys.exit('IMPUT ERROR')
elif global_var.module_choice==2 and conditions.extAbundances == True:
    print("CAN'T USE EXTERNAL ABUNDANCES WITH THE CONFORMATIONAL ANALYSIS MODULE. EXITING")
    sys.exit('IMPUT ERROR')
elif conditions.extEnergies == True:
    print("WARNING: Using external energies from freeEnergies.txt to calculate the conformational distribution")
    print(" ")
    print("Gaussian free energies will be ignored")
    freeEnergies = np.genfromtxt(os.path.join(global_var.parent_dir,'freeEnergies.txt'), dtype=float)
elif conditions.extAbundances == True:
    print("WARNING: Using external abundances from confabn.txt to calculate the conformational distribution")
    print(" ")
    print("Gaussian free energies will be ignored")
    confabn = np.genfromtxt(os.path.join(global_var.parent_dir,'confabn.txt'), dtype=float)
    freeEnergies = global_var.freeEnergies
else:
    print("Free energies from .out files will be used to calculate the conformational distribution")
    freeEnergies = global_var.freeEnergies


# Relative free energies in kcal/mol calculation

freeEnergies_kcal = freeEnergies * conditions.H
rel_freeEnergies = freeEnergies_kcal - freeEnergies_kcal.min()

if global_var.module_choice==2:
    rel_freeEnergies = np.repeat(0, nconf)

# Conformational distribution calculation

weights = np.exp(np.negative(rel_freeEnergies)/(conditions.kb*conditions.T))/np.sum(np.exp(np.negative(rel_freeEnergies)/(conditions.kb*conditions.T)));

globalmin = np.argmax(weights)

if conditions.extAbundances == True:
    weights = confabn/100
    rel_freeEnergies = np.repeat(0, nconf)

rweights = np.repeat(weights, nmodes)

diplist = diplist * rweights
rotlist = rotlist * rweights

#np.savetxt(os.path.join(global_var.output_path_m,'Diplist_withConfD.txt'),diplist)
#np.savetxt(os.path.join(global_var.output_path_m,'Rotlist_withConfD.txt'),rotlist)

rweights = np.reshape(rweights, (nmodes,nconf))*100

#np.savetxt(os.path.join(global_var.output_path_m,'rweights.txt'),rweights)
np.savetxt(os.path.join(global_var.output_path_m,'Abundances.txt'),weights)

print("done")
print(" ")