import os
import time
import numpy as np
import global_var

# Output folder

if global_var.module_choice==1:
    if global_var.rutine_choice==1:
        rc = '_UnscFreq'
    elif global_var.rutine_choice==2:
        rc = '_GlbScl'
    elif global_var.rutine_choice==3:
        rc = '_ISFs'
if global_var.module_choice==2:
    if global_var.rutine_choice==1:
        rc = '_ConfDopt-Se'
    elif global_var.rutine_choice==2:
        rc = '_ConfDopt-S-e'
    elif global_var.rutine_choice==3:
        rc = '_ConfDopt-ESI'
if global_var.module_choice==3:
    if global_var.rutine_choice==1:
        rc = '_Sim'
    elif global_var.rutine_choice==2:
        rc = '_SinxConf'
        
global_var.rc = rc

output_folder = ('VISSAT_' + time.strftime("%Y-%m-%d_%H-%M-%S") + rc)
current_dir = global_var.current_dir
parent_dir = global_var.parent_dir
output_path = os.path.join(parent_dir, output_folder)
output_path_m = os.path.join(output_path, 'matrices')
output_folder_m = os.path.join(output_folder,'matrices')
os.mkdir(output_path)
os.mkdir(output_path_m)

global_var.output_path = output_path
global_var.output_path_m = output_path_m

# Data extraction from Gaussian files

import extract_mod

np.savetxt(os.path.join(output_path_m,'freeEnergies.txt'),extract_mod.free_energy_list)
#np.savetxt(os.path.join(output_path_m,'freqlist.txt'),extract_mod.freq_list)
#np.savetxt(os.path.join(output_path_m,'Diplist_withoutConfD.txt'),extract_mod.dipstr_list)
#np.savetxt(os.path.join(output_path_m,'Rotlist_withoutConfD.txt'),extract_mod.rotstr_list)

global_var.lot_func_str_list = extract_mod.lot_func_str_list
global_var.freeEnergies = extract_mod.free_energy_list
global_var.freqlist = extract_mod.freq_list
global_var.diplist = extract_mod.dipstr_list
global_var.rotlist = extract_mod.rotstr_list
global_var.diplist_without_confd = extract_mod.dipstr_list
global_var.rotlist_without_confd = extract_mod.rotstr_list
global_var.nIR = extract_mod.nIR
global_var.nconf = extract_mod.nconf
global_var.nmodes = extract_mod.nmodes
global_var.filenames_list = extract_mod.filenames_list



if global_var.module_choice !=3:
    
    # Conformational distribution calculation
    
    import distconf_mod
    
    global_var.rel_freeEnergies = distconf_mod.rel_freeEnergies
    global_var.freeEnergies_kcal = distconf_mod.freeEnergies_kcal
    global_var.weights = distconf_mod.weights
    global_var.diplist = distconf_mod.diplist
    global_var.rotlist = distconf_mod.rotlist
    global_var.globalmin = distconf_mod.globalmin

if global_var.module_choice==3:
    if global_var.rutine_choice==1:
        import distconf_mod
        
        global_var.rel_freeEnergies = distconf_mod.rel_freeEnergies
        global_var.freeEnergies_kcal = distconf_mod.freeEnergies_kcal
        global_var.weights = distconf_mod.weights
        global_var.diplist = distconf_mod.diplist
        global_var.rotlist = distconf_mod.rotlist
        global_var.globalmin = distconf_mod.globalmin
    else:
        pass

# Observed IR spectrum extraction

import expIR_mod

global_var.Yexpir = expIR_mod.Yexpir
global_var.xx = expIR_mod.xx
global_var.N = expIR_mod.N

Exp_IR_Spectra=np.c_[global_var.xx, global_var.Yexpir]
np.savetxt(os.path.join(output_path_m,'Exp_IR_Spectra.txt'),Exp_IR_Spectra)

# Observed VCD spectrum extraction

import expVCD_mod

global_var.Yexpvcd = expVCD_mod.Yexpvcd
global_var.Yexppos = expVCD_mod.Yexppos
global_var.Yexpneg = expVCD_mod.Yexpneg

#np.savetxt(os.path.join(output_path_m,'Yexpvcd.txt'),global_var.Yexpvcd)
#np.savetxt(os.path.join(output_path_m,'Yexppos.txt'),global_var.Yexppos)
#np.savetxt(os.path.join(output_path_m,'Yexpneg.txt'),global_var.Yexpneg)

Exp_VCD_Spectra=np.c_[global_var.xx, global_var.Yexpvcd]
np.savetxt(os.path.join(output_path_m,'Exp_VCD_Spectra.txt'),Exp_VCD_Spectra)

# IR similarity and scaling 

import simscal_mod;

global_var.freqlist = simscal_mod.freqlist
global_var.freqlistxconfOpt = simscal_mod.freqlistxconfOpt
global_var.diplistxconfOpt = simscal_mod.diplistxconfOpt
global_var.rotlistxconfOpt = simscal_mod.rotlistxconfOpt
global_var.Factoranh = simscal_mod.Factoranh
global_var.SIR = simscal_mod.SIR
if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    global_var.SIR_list = simscal_mod.SIR_list
    np.savetxt(os.path.join(output_path_m,'SIR_list.txt'),global_var.SIR_list)
if global_var.module_choice == 2:
    global_var.cfnabn_norm = simscal_mod.cnfabn_norm
    np.savetxt(os.path.join(output_path_m,'confabn.txt'),global_var.cfnabn_norm)
np.savetxt(os.path.join(output_path_m,'freqlistxconfOpt.txt'),global_var.freqlistxconfOpt)
np.savetxt(os.path.join(output_path_m,'diplistxconfOpt.txt'),global_var.diplistxconfOpt)
np.savetxt(os.path.join(output_path_m,'rotlistxconfOpt.txt'),global_var.rotlistxconfOpt)
np.savetxt(os.path.join(output_path_m,'ISFvis.txt'),simscal_mod.ISFvis,fmt='%0.3f')

# VCD similarity

import esi_mod

global_var.esie1 = esi_mod.esie1
global_var.esie2 = esi_mod.esie2
global_var.ESI = esi_mod.ESI
if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    global_var.ESI_list = esi_mod.ESI_list
    global_var.esie1_list = esi_mod.esie1_list
    global_var.esie2_list = esi_mod.esie2_list

print(" ")
print("Plotting results and producing reports...")
print(" ")

if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    pass
else:

    # Spectra plotting
    import matplotlib.pyplot as plt
    import conditions
    import functions
    
    for i in range(len(global_var.freqlistxconfOpt[:,0])):
        for j in range(len(global_var.freqlistxconfOpt[0,:])):
            if i== 0 and j==0:
                fn = functions.lor(1, global_var.xx, global_var.freqlistxconfOpt[i,j], global_var.diplistxconfOpt[i,j], conditions.h)/(91.84*np.pi)
            else: 
                f1 = functions.lor(1, global_var.xx, global_var.freqlistxconfOpt[i,j], global_var.diplistxconfOpt[i,j], conditions.h)/(91.84*np.pi)
                fn = fn + f1
    
    ircalcmax = np.amax(fn)
    #print ("calcmax: ", ircalcmax)
    irexpmax = np.amax(global_var.Yexpir)
    #print ("expmax: ", irexpmax)
    ir_plot_scale_factor=ircalcmax/irexpmax
    #print ("IR_plot_scale_factor: ",  ir_plot_scale_factor)
    scaled_Yexpir = global_var.Yexpir*ir_plot_scale_factor

    plt.figure(figsize=(12, 6))
    plt.title('IR spectra', fontsize=17)
    plt.plot(global_var.xx, fn, 'r', label='Calculated')
    plt.plot(global_var.xx, (scaled_Yexpir), 'b', label='Observed')
    plt.ylabel('Intensity', fontsize=13)
    plt.yticks(fontsize=9)
    plt.xlabel('Wavenumbers (cm-1)', fontsize=13)
    plt.xticks(fontsize=9)
    plt.grid(color='#F2F2F2', alpha=1, zorder=0)
    plt.legend(loc='best')
    plt.savefig(os.path.join(output_path,'IRspectra'), dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()
    Calc_IR_Spectra=np.c_[global_var.xx, fn]
    np.savetxt(os.path.join(output_path_m,'Calc_IR_Spectra.txt'),Calc_IR_Spectra)
    
    for i in range(len(global_var.freqlistxconfOpt[:,0])):
        for j in range(len(global_var.freqlistxconfOpt[0,:])):
            if i== 0 and j==0:
                fn = functions.lor(1, global_var.xx, global_var.freqlistxconfOpt[i,j], global_var.rotlistxconfOpt[i,j], conditions.h)/(229600*np.pi)
            else: 
                f1 = functions.lor(1, global_var.xx, global_var.freqlistxconfOpt[i,j], global_var.rotlistxconfOpt[i,j], conditions.h)/(229600*np.pi)
                fn = fn + f1
    
    vcdcalcmax = np.amax(fn)
    #print ("vcdcalcmax: ", vcdcalcmax)
    vcdexpmax = np.amax(global_var.Yexpvcd)
    #print ("vcdexpmax: ", vcdexpmax)
    vcd_plot_scale_factor=vcdcalcmax/vcdexpmax
    #print ("VCD_plot_scale_factor: ",  vcd_plot_scale_factor)
    scaled_Yexpvcd = global_var.Yexpvcd*vcd_plot_scale_factor

    plt.figure(figsize=(12, 6))
    plt.title('VCD spectra', fontsize=17)
    plt.plot(global_var.xx, fn, 'r', label='Calculated')
    plt.plot(global_var.xx, (scaled_Yexpvcd), 'b', label='Observed')
    plt.ylabel('Intensity', fontsize=13)
    plt.yticks(fontsize=9)
    plt.xlabel('Wavenumbers (cm-1)', fontsize=13)
    plt.xticks(fontsize=9)
    plt.grid(color='#F2F2F2', alpha=1, zorder=0)
    plt.legend(loc='best')
    plt.savefig(os.path.join(output_path,'VCDspectra'), dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()
    Calc_VCD_Spectra=np.c_[global_var.xx, fn]
    np.savetxt(os.path.join(output_path_m,'Calc_VCD_Spectra.txt'),Calc_VCD_Spectra)

import report

print("done")
print(" ")
