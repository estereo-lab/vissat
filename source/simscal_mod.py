# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 09:42:28 2022

@author: mamun
"""


# IR similarity and scaling sub-rutine


import global_var
import numpy as np
import functions
import conditions
import os
from scipy.optimize import minimize, Bounds

if global_var.module_choice ==1:
    if global_var.rutine_choice ==1:
        print(" ")
        print("Performing similarity analysis using unscaled frequencies")
        print(" ")
    elif global_var.rutine_choice==2:
        print(" ")
        print("Performing similarity analysis using frequencies scaled with a single scaling factor")
        print(" ")
    elif global_var.rutine_choice==3:
        print(" ")
        print("Performing similarity analysis using frequencies scaled with idividual Scaling Factors")
        print(" ")



freqlist = global_var.freqlist

nconf = global_var.nconf
nmodes = global_var.nmodes
module_choice = global_var.module_choice
rutine_choice = global_var.rutine_choice
Yexpir = global_var.Yexpir
diplist = global_var.diplist
rotlist = global_var.rotlist

# Reshaping data to selected range and conformations

freqlistxconf = np.reshape(freqlist,(nmodes,nconf), order='F')
diplistxconf = np.reshape(diplist, (nmodes,nconf), order='F')
rotlistxconf = np.reshape(rotlist,(nmodes,nconf), order='F')


np.savetxt(os.path.join(global_var.output_path_m,'freqlistxconf.txt'),freqlistxconf)
np.savetxt(os.path.join(global_var.output_path_m,'diplistxconf.txt'),diplistxconf)
np.savetxt(os.path.join(global_var.output_path_m,'rotlistxconf.txt'),rotlistxconf)

def isfvis_imp(x):
    ISFvis = np.genfromtxt(os.path.join(global_var.parent_dir,'ISFvis.txt'), dtype=float)
    np.savetxt(os.path.join(global_var.output_path_m,'ISFvisSP.txt'),ISFvis,fmt='%0.3f')
    freqlistxconf = x * ISFvis[:, np.newaxis]
    return freqlistxconf

if module_choice==1:
    if  rutine_choice==3:
        freqlistxconf = isfvis_imp(freqlistxconf)
if module_choice==2:
    freqlistxconf = isfvis_imp(freqlistxconf)
if module_choice==3:
    freqlistxconf = isfvis_imp(freqlistxconf)

freqlistxconfR1 = np.empty(0)
diplistxconfR1 = np.empty(0)
rotlistxconfR1 = np.empty(0)
freqlistxconfLow = np.empty(0)



for n in range(len(freqlistxconf[:,0])):
    for k in range(len(freqlistxconf[0,:])):
        if freqlistxconf[n,0]>conditions.r1:
            freqlistxconfR1 = np.append(freqlistxconfR1,freqlistxconf[n,k])
            diplistxconfR1 = np.append(diplistxconfR1,diplistxconf[n,k])
            rotlistxconfR1 = np.append(rotlistxconfR1,rotlistxconf[n,k])
        else:
            freqlistxconfLow = np.append(freqlistxconfLow,freqlistxconf[n,k])

freqlistxconfR1 = np.reshape(freqlistxconfR1,(-1,global_var.nconf))
diplistxconfR1 = np.reshape(diplistxconfR1,(-1,global_var.nconf))
rotlistxconfR1 = np.reshape(rotlistxconfR1,(-1,global_var.nconf))
freqlistxconfLow = np.reshape(freqlistxconfLow,(-1,global_var.nconf))


freqlistxconfR2 = np.empty(0)
diplistxconfR2 = np.empty(0)
rotlistxconfR2 = np.empty(0)
freqlistxconfHigh = np.empty(0)

for n in range(len(freqlistxconfR1[:,0])):
    for k in range(len(freqlistxconfR1[0,:])):
        if freqlistxconfR1[n,0]<conditions.r2:
            freqlistxconfR2 = np.append(freqlistxconfR2,freqlistxconfR1[n,k])
            diplistxconfR2 = np.append(diplistxconfR2,diplistxconfR1[n,k])
            rotlistxconfR2 = np.append(rotlistxconfR2,rotlistxconfR1[n,k])
        else:
            freqlistxconfHigh = np.append(freqlistxconfHigh,freqlistxconfR1[n,k])

freqlistxconfR2 = np.reshape(freqlistxconfR2,(-1,global_var.nconf))
diplistxconfR2 = np.reshape(diplistxconfR2,(-1,global_var.nconf))
rotlistxconfR2 = np.reshape(rotlistxconfR2,(-1,global_var.nconf))
freqlistxconfHigh = np.reshape(freqlistxconfHigh,(-1,global_var.nconf))


if module_choice==1:
    
    if rutine_choice==1:
        SIR = functions.safmin(freqlistxconfR2,diplistxconfR2,conditions.h, 1, Yexpir)
        print('An IR similarity value of',round(SIR, 3), 'was found')
        print(" ")
        Factoranh = 1
        freqlistxconfOpt = freqlistxconfR2
        diplistxconfOpt = diplistxconfR2
        rotlistxconfOpt = rotlistxconfR2
    elif rutine_choice==2:
        print(" ")
        print("Finding the optimal anharmonicity factor...")
        print(" ")
        def SIR_fun(x):
            return (functions.safmin(freqlistxconfR2,diplistxconfR2,conditions.h, x, Yexpir))*-1
        Nfeval = 1
        def callbackF(xi):
            global Nfeval
            print ('{0:4d}   {1: 3.6f}   {2: 3.6f}'.format(Nfeval, xi[0], (SIR_fun(xi))*-1))
            Nfeval += 1
        print  ('{0:4s}   {1:9s}   {2:9s}'.format('Iter', ' fAnh', 'SIR'))   
        min = minimize(SIR_fun, 1, method='nelder-mead', callback=callbackF, options={'xatol': 1e-8, 'disp': False})
        SIR = np.array(min.fun) * -1
        Factoranh = np.array(min.x)
        print('An IR similarity value of',np.round(SIR,3), 'was found using an anH of',np.round(Factoranh[0],3))
        print(" ")
        freqlistxconfOpt = freqlistxconfR2*Factoranh
        diplistxconfOpt = diplistxconfR2;
        rotlistxconfOpt = rotlistxconfR2;
    elif rutine_choice==3:
        print(" ")
        print("Finding the optimal ISF´s using starting points......")
        print(" ")
        isfs = np.repeat(1,len(freqlistxconfR2[:,0]))
        isfs_lb = np.repeat(0.995,len(freqlistxconfR2[:,0]))
        isfs_ub = np.repeat(1.005,len(freqlistxconfR2[:,0]))  
        hess = lambda x: np.repeat(0,len(freqlistxconfR2[:,0]))  
        bounds = Bounds(isfs_lb, isfs_ub)
        def ISFmin(x):
            return (functions.isfmin(freqlistxconfR2,diplistxconfR2,conditions.h, x, Yexpir))*-1
        Nfeval = 1
        def callbackF(xi):
            global Nfeval
            print ('{0:4d}   {1: 3.6f}'.format(Nfeval, (ISFmin(xi))*-1))
            Nfeval += 1
        print  ('{0:4s}   {1:9s}'.format('Iter', 'SIR'))       
        min = minimize(ISFmin, isfs, method='COBYLA',callback=callbackF, options={'maxiter': 2000,'disp': True})
        SIR = min.fun * -1
        Isfs = min.x
        Factoranh = 1
        print(Isfs)
        print(" ")
        print('An IR similarity value of',round(SIR, 3), ' was found using optimized ISF´s')
        print(" ")
        freqlistxconfOpt = freqlistxconfR2 * Isfs[:, np.newaxis]
        diplistxconfOpt = diplistxconfR2;
        rotlistxconfOpt = rotlistxconfR2;
elif module_choice==2:
    if rutine_choice==1:
        print(" ")
        print("Finding conformational abundances that maximizes Se......")
        print(" ")
        cnfabn = np.repeat(1,len(freqlistxconfR2[0,:]))
        def SE_min(x):
            return (functions.Se_min(freqlistxconfR2, rotlistxconfR2, conditions.h, x, global_var.Yexppos, global_var.Yexpneg, rutine_choice))*-1
        Nfeval = 1
        def callbackF(xi):
            global Nfeval
            print ('{0:4d}   {1: 3.6f}'.format(Nfeval, (SE_min(xi))*-1))
            Nfeval += 1
        print  ('{0:4s}   {1:9s}'.format('Iter', 'Se'))       
        min = minimize(SE_min, cnfabn, method='COBYLA',callback=callbackF, options={'maxiter': 2000,'disp': True})
        Se = min.fun * -1
        cnfabn = np.abs(min.x)
        Factoranh = 1
        cnfabn_sum = np.sum(cnfabn)
        cnfabn_norm = (cnfabn/cnfabn_sum)*100
        print(" ")
        print('A similarity value of',round(Se, 3), ' for the calculated enantiomer was found using optimized conformational abundances')
        print(" ")
        freqlistxconfOpt = freqlistxconfR2
        diplistxconfOpt = diplistxconfR2 * cnfabn_norm[np.newaxis,:]
        rotlistxconfOpt = rotlistxconfR2 * cnfabn_norm[np.newaxis,:]
        SIR = functions.safmin(freqlistxconfOpt ,diplistxconfOpt,conditions.h, 1, Yexpir)
         
    if rutine_choice==2:
        print(" ")
        print("Finding conformational abundances that maximizes S-e......")
        print(" ")
        cnfabn = np.repeat(1,len(freqlistxconfR2[0,:]))
        def SE_min(x):
            return (functions.Se_min(freqlistxconfR2, rotlistxconfR2, conditions.h, x, global_var.Yexppos, global_var.Yexpneg, rutine_choice))*-1
        Nfeval = 1
        def callbackF(xi):
            global Nfeval
            print ('{0:4d}   {1: 3.6f}'.format(Nfeval, (SE_min(xi))*-1))
            Nfeval += 1
        print  ('{0:4s}   {1:9s}'.format('Iter', 'S-e'))       
        min = minimize(SE_min, cnfabn, method='COBYLA',callback=callbackF, options={'maxiter': 2000,'disp': True})
        Se = min.fun * -1
        cnfabn = np.abs(min.x)
        Factoranh = 1
        cnfabn_sum = np.sum(cnfabn)
        cnfabn_norm = (cnfabn/cnfabn_sum)*100
        print(" ")
        print('A similarity value of',round(Se, 3), ' for the opposite enantiomer was found using optimized conformational abundances')
        print(" ")
        freqlistxconfOpt = freqlistxconfR2

        diplistxconfOpt = diplistxconfR2 * cnfabn_norm[np.newaxis,:]
        rotlistxconfOpt = rotlistxconfR2 * cnfabn_norm[np.newaxis,:]
        SIR = functions.safmin(freqlistxconfOpt ,diplistxconfOpt,conditions.h, 1, Yexpir)
        
    if rutine_choice==3:
        print(" ")
        print("Finding conformational abundances that maximizes ESI......")
        print(" ")
        cnfabn = np.repeat(1,len(freqlistxconfR2[0,:]))
        def SE_min(x):
            return (functions.Se_min(freqlistxconfR2, rotlistxconfR2, conditions.h, x, global_var.Yexppos, global_var.Yexpneg, rutine_choice))*-1
        Nfeval = 1
        def callbackF(xi):
            global Nfeval
            print ('{0:4d}   {1: 3.6f}'.format(Nfeval, (SE_min(xi))*-1))
            Nfeval += 1
        print  ('{0:4s}   {1:9s}'.format('Iter', 'ESI'))       
        min = minimize(SE_min, cnfabn, method='COBYLA',callback=callbackF, options={'maxiter': 2000,'disp': True})
        ESI = min.fun * -1
        cnfabn = np.abs(min.x)
        Factoranh = 1
        cnfabn_sum = np.sum(cnfabn)
        cnfabn_norm = (cnfabn/cnfabn_sum)*100
        print(" ")
        print('An ESI similarity value of',round(ESI, 3), ' was found using optimized conformational abundances')
        print(" ")
        freqlistxconfOpt = freqlistxconfR2
        diplistxconfOpt = diplistxconfR2 * cnfabn_norm[np.newaxis,:]
        rotlistxconfOpt = rotlistxconfR2 * cnfabn_norm[np.newaxis,:]
        SIR = functions.safmin(freqlistxconfOpt ,diplistxconfOpt,conditions.h, 1, Yexpir)

elif module_choice==3:
    if rutine_choice==1:
        print(" ")
        print("Calculating similarities using pre-optimized ISF´s......")
        print(" ")
        SIR = functions.safmin(freqlistxconfR2,diplistxconfR2,conditions.h, 1, Yexpir)
        print('An IR similarity value of',round(SIR, 3), 'was found')
        print(" ")
        Factoranh = 1
        freqlistxconfOpt = freqlistxconfR2
        diplistxconfOpt = diplistxconfR2
        rotlistxconfOpt = rotlistxconfR2
    if rutine_choice==2:
        SIR_list =np.empty(0)
        for i in range(len(freqlistxconfR2[0,:])):
            print(" ")
            print("Calculating similarities using pre-optimized ISF´s......")
            print(" ")
            print(i)            
            for j in range(len(freqlistxconfR2[:,0])):
                    if j== 0:
                        Ycal = functions.lor(1, global_var.xx, freqlistxconfR2[j,i], diplistxconfR2[j,i], conditions.h)
                    else: 
                        f1 = functions.lor(1, global_var.xx, freqlistxconfR2[j,i], diplistxconfR2[j,i], conditions.h)
                        Ycal = Ycal + f1
            SIR = functions.sim(Yexpir,Ycal)
            SIR_list = np.append(SIR_list, SIR)
            print('An IR similarity value of',round(SIR, 3), 'was found')
            print(" ")
        Factoranh = 1
        freqlistxconfOpt = freqlistxconfR2
        diplistxconfOpt = diplistxconfR2
        rotlistxconfOpt = rotlistxconfR2


freqlistxconfOptComplete = np.r_[freqlistxconfLow,freqlistxconfOpt,freqlistxconfHigh]
ISFlist= freqlistxconfOptComplete/freqlistxconf
ISFvis = np.array(ISFlist[:,0])

if module_choice==1:
    if rutine_choice==3:
        ISFvis = np.genfromtxt(os.path.join(global_var.parent_dir,'ISFvis.txt'), dtype=float)
        ISFvis = np.array(ISFlist[:,0])*ISFvis

print("done")
print(" ")