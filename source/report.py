# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:28:13 2022

@author: mamun
"""

from fpdf import FPDF
import time
import global_var
import os
import sys 
import numpy as np
import conditions
import pathlib
from tabulate import tabulate

module_choice = global_var.module_choice
rutine_choice = global_var.rutine_choice
output_path = global_var.output_path

if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    pass
else:

    fanh = 1
    
    if module_choice==1:
        if rutine_choice ==2:
           fanh = global_var.Factoranh[0]
    
    fanh_str = str(np.round(fanh,3))
    SIR = global_var.SIR
    SIR_str = str(np.round(SIR,3))
    esie1 = global_var.esie1
    esie1_str = str(round(esie1,3))
    esie2 = global_var.esie2
    esie2_str = str(round(esie2,3))
    ESI = global_var.ESI
    ESI_str = str(round(ESI,3))
    
    
    class PDF(FPDF):
        def header(self):
            # Arial bold 15
            self.set_font('Arial', 'B', 22)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 10, 'VISSAT report sheet', 0, 0, 'C')
            # Line break
            self.ln(210)
    
        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Date
            self.cell(0, 10, time.strftime("%b %d %Y %H:%M:%S"), 0, 0, 'C')
    
    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.image(os.path.join(output_path,'IRspectra.png'), x = 10, y = 25, w = 180, h = 0)
    pdf.image(os.path.join(output_path,'VCDspectra.png'), x = 10, y = 125, w = 180, h = 0)
    
    pdf.set_font('Times', '', 20) 
    if global_var.module_choice ==1:
        if global_var.rutine_choice ==1:
           pdf.cell(0, 14, 'Unscaled frequencies', 0, 1, 'C')
           pdf.cell(0, 8, 'Scaling factor = ' + fanh_str, 0, 0)
        elif global_var.rutine_choice==2:
           pdf.cell(0, 14, 'Frequencies scaled using a single scaling factor', 0, 1, 'C')
           pdf.cell(0, 8, 'Scaling factor = ' + fanh_str, 0, 0)        
        else:
            pdf.cell(0, 14, 'Frequencies scaled using Idividual Sacaling Factors', 0, 1, 'C')
            pdf.cell(0, 8, 'Scaling factor = ISF´s', 0, 0)
    pdf.cell(0, 8, 'Se = ' + esie1_str, 0, 1, 'R')
    pdf.cell(0, 8, 'Sir = ' + SIR_str, 0, 0)
    pdf.cell(0, 8, 'S-e = ' + esie2_str, 0, 1, 'R')
    pdf.cell(60)
    pdf.cell(80, 8, 'ESI = ' + ESI_str, 1, 1, 'C')
    pdf.output(os.path.join(output_path,(('VISSAT_report_' + time.strftime("%Y-%m-%d_%H-%M-%S") + global_var.rc + '.pdf'))), 'F')

stdoutOrigin=sys.stdout 
sys.stdout = open(os.path.join(output_path,(('VISSAT_report_' + time.strftime("%Y-%m-%d_%H-%M-%S") + global_var.rc + '.txt'))), "w")
print(" ")
print("********************************************************")
print("VISSAT: Vibrational Spectra Similarity and Analysis Tool")
print("                    Version 1.0                         ")
print("********************************************************")
print(" ")
print("The following rutine was chosen:")
print(" ")
if global_var.module_choice ==1:
    if global_var.rutine_choice ==1:
        print("Similarity analysis using unscaled frequencies")
    elif global_var.rutine_choice==2:
        print("Similarity analysis using frequencies scaled with a single scaling factor")    
    elif global_var.rutine_choice==3:
        print("Similarity analysis using frequencies scaled with idividual Sacaling Factors")
if global_var.module_choice ==2:
    if global_var.rutine_choice ==1:
        print("Conformational distribution from esie1")
    elif global_var.rutine_choice==2:
        print("Conformational distribution from esie1")    
    elif global_var.rutine_choice==3:
        print("Conformational distribution from ESI")
print(" ")
print("********************************************************")
print(" ")
print(" ")
print('The EXTRACT module detected ' + str(global_var.nconf) + ' conformations in the parent directory:')
print(" ")


print(tabulate(global_var.filenames_list, headers=["Conf" , "Filename" , "Functional" , "Basis Set"]))

if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    pass
else:

    global_var.freeEnergies

    print(" ")
    print(" ")
    print("********************************************************")
    print(" ")
    print("The DISTCONF module calculated the following conformational distribution using Gibbs free energies:")
    print(" ")
    if global_var.module_choice == 2:
        print('Also, the OPTCONF module calculated the following conformational distribution from similarity optimization:')
    print(" ")
    print(" ")

    conf_dist_tbl = []
    ext = ('*.out')
    NConf = 0
    Idx = -1
    for files in pathlib.Path(global_var.parent_dir).glob(ext):
        NConf += 1
        Idx += 1
        element1 = (str('CONF'+ str('{:0>3}'.format(NConf))))
        element2 = '{:.6f}'.format(global_var.freeEnergies[Idx])
        element3 = '{:.6f}'.format(global_var.freeEnergies_kcal[Idx])
        element4 = '{:.6f}'.format(global_var.rel_freeEnergies[Idx])
        element5 = str(global_var.weights[Idx]*100)
        if global_var.module_choice == 2:
            element6 = str(global_var.cfnabn_norm[Idx])
            element = [(element1,element2,element3, element4, element5,element6)]
        else:
            element = [(element1,element2,element3, element4, element5)]
        conf_dist_tbl += element

    if global_var.module_choice == 2:
                print(tabulate(conf_dist_tbl, headers=["Conf" , "FreeE (h)" , "FreeE (kcal/mol)" , "DeltaG (kcal/mol)" , "Abundance (%)" , "Opt Abund (%)"], floatfmt=".6f"))
    else:
        print(tabulate(conf_dist_tbl, headers=["Conf" , "FreeE (h)" , "FreeE (kcal/mol)" , "DeltaG (kcal/mol)" , "Abundance (%)"], floatfmt=".6f"))    

if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    
    print(" ")
    print(" ")
    print("********************************************************")
    print(" ")
    print("The following similarities were found for each conformation:")
    print(" ")
    print(" ")
    
    conf_dist_tbl = []
    ext = ('*.out')
    NConf = 0
    Idx = -1
    for files in pathlib.Path(global_var.parent_dir).glob(ext):
            NConf += 1
            Idx += 1
            element1 = (str('CONF'+ str('{:0>3}'.format(NConf))))
            element2 = global_var.SIR_list[Idx]
            element3 = global_var.esie1_list[Idx]
            element4 = global_var.esie2_list[Idx]
            element5 = global_var.ESI_list[Idx]
            element = [(element1,element2,element3, element4, element5)]
            conf_dist_tbl += element

    print(tabulate(conf_dist_tbl, headers=["Conf" , "SIR" , "S E" , "S -E" , "ESI"], floatfmt=".3f"))    

print(" ")
print(" ")
print("********************************************************")
print(" ")
print("Similarity calculations were made considering the following specfications in conditions.py:")
print(" ")
print(" ")
print('Band halfwidth: ',conditions.h,'cm-1')
print('Spectral range: ',conditions.r1, '-',conditions.r2, 'cm-1')
print('Baseline correction of observed VCD: ',conditions.blc, 'cm-1')
print(" ")
print(" ")
print("********************************************************")

if global_var.module_choice == 3 and global_var.rutine_choice ==2:
    pass
else:

    print(" ")
    print("                IR SIMILARITY       ")
    print(" ")
    if global_var.module_choice ==1:
        if global_var.rutine_choice ==1:
            print('An IR similarity value of',round(SIR, 3), 'was found')
        elif global_var.rutine_choice==2:
            print('An IR similarity value of',np.round(SIR,3), 'was found using an anH of',fanh_str)    
        elif global_var.rutine_choice==3:
            print('An IR similarity value of',round(SIR, 3), ' was found using optimized ISF´s')
    if global_var.module_choice ==3 and global_var.rutine_choice ==1:
        print('An IR similarity value of',np.round(SIR,3), 'was found using an anH of',fanh_str)    

    
    print(" ")
    print("********************************************************")
    print(" ")
    print("                VCD SIMILARITY       ")
    print(" ")
    print('A VCD similarity value of',round(esie1, 3),' was found for the calculated enantiomer')
    print(" ")
    print('A VCD similarity value of',round(esie2, 3),' was found for the calculated opposite enantiomer')
    print(" ")
    print(" ")
    print("********************************************************************************")
    print(" ")
    print('A VCD ESI value of',round(ESI, 3),' was found for the selected frequency scaling method')
    print(" ")
    print("********************************************************************************")
    print(" ")
    print(" ")

sys.stdout.close()
sys.stdout=stdoutOrigin