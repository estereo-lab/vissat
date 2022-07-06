import os
import sys
import global_var
import conditions
import getopt
from pathlib import Path

current_dir = Path.cwd()
parent_dir = current_dir.parent.absolute()
global_var.current_dir = current_dir
global_var.parent_dir = parent_dir

def module_options():
    module_choice = None
    rutine_choice = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "m:r:")
    except getopt.GetoptError as err:
        print(" ")
        print('Command line instructions incomplete. Moving to interactive mode...')
        opts =[]
        interactive_mode()
    else:
        for opt, arg in opts:
            if opt in ['-m']:
                module_choice = arg
            elif opt in ['-r']:
                rutine_choice = arg
        global_var.module_choice = module_choice
        global_var.rutine_choice = rutine_choice
        if module_choice == None or rutine_choice == None:
            print(" ")
            print('Command line instructions incomplete. Moving to interactive mode...')
            opts =[]
            interactive_mode()
        else:
            commandline_mode()


def commandline_mode():
    print(" ")
    print("******************************************************************")
    print("Welcome to VSSAT: Vibrational Spectra Similarity and Analysis Tool")
    print("                           Version 1.0                            ")
    print("******************************************************************")
    print(" ")
    if global_var.module_choice == 'scaling':
        print("Spectra scaling module SELECTED")
        print(" ")
        if global_var.rutine_choice == 'unscaled':
            print("Unscaled frequencies rutine SELECTED")
            print(" ")
        elif global_var.rutine_choice =='saf':
            print("Single anharmonicity factor rutine SELECTED")
            print(" ")
        elif global_var.rutine_choice=='isfs':
            print("Individual scaling factors ISF´s from user starting points rutine SELECTED")
            print(" ")
        else:
            print("NOT A VALID RUTINE IMPUT. EXITING")
            sys.exit('IMPUT ERROR')
    elif global_var.module_choice == 'conf':
        print("Conformational analysis module SELECTED")
        print(" ")
        print("ATTENTION: all of these rutines require a valid list of ISF´s (ISFvis.txt) on the main directory to run.")
        print("These are produced by any of the rutines in the Spectra scaling module and stored in the corresponding VISSAT output folder")
        print(" ")
        if global_var.rutine_choice=='esie1':
            print("Conformational distribution from esie1 SELECTED")
            print(" ")
        elif global_var.rutine_choice=='esie2':
            print("Conformational distribution from esie2 SELECTED")
            print(" ")
        elif global_var.rutine_choice=='esi':
            print("Conformational distribution from ESI SELECTED")
            print(" ")
        else:
            print("NOT A VALID RUTINE IMPUT. EXITING")
            sys.exit('IMPUT ERROR')
    elif global_var.module_choice == 'similarity':
        print("Similarity toolbox module SELECTED")
        print(" ")
        print("ATTENTION: all of these rutines requeire a valid list of ISF´s (ISFvis.txt) on the main directory to run.")
        print("These are produced by any of the rutines in module 1 and stored in the corresponding VISSAT output folder")
        print(" ")
        if global_var.rutine_choice=='isfs':
            print("Similarity values from ISF´s SELECTED")
            print(" ")
        elif global_var.rutine_choice=='xconf':
            print("Similarity values per conformation SELECTED")
            print(" ")
        else:
            print("NOT A VALID RUTINE IMPUT. EXITING")
            sys.exit('IMPUT ERROR')
    else:
        print("NOT A VALID MODULE IMPUT. EXITING")
        sys.exit('IMPUT ERROR')
        



def interactive_mode():
    print(" ")
    print("******************************************************************")
    print("Welcome to VSSAT: Vibrational Spectra Similarity and Analysis Tool")
    print("                           Version 1.0                            ")
    print("******************************************************************")
    print(" ")
    print("Please choose one of the following modules to run:")
    print(" ")
    print("Spectra scaling (1)")
    print("Conformational analysis (2)")
    print("Similarity toolbox (3)")
    print(" ")
    module_choice = int(input("Please choose: "))
    global_var.module_choice = module_choice

    if module_choice==1 :
        print(" ")
        print("Spectra scaling module SELECTED")
        print(" ")
        print("Now please choose one of the following rutines to run:")
        print(" ")
        print("Obtain vibrational spectra without scaling (1)")
        print("Obtain vibrational spectra using a single anharmonicity factor (2)")
        print("Obtain optimized Individual scaling factors ISF´s from user starting points (3)")
        print(" ")
        rutine_choice = int(input("Please choose: "))
        global_var.rutine_choice = rutine_choice
        if rutine_choice==1:  
            print("Unscaled frequencies rutine SELECTED")
        elif rutine_choice==2:
            print("Single anharmonicity factor rutine SELECTED")
        elif rutine_choice==3:
            print("Individual scaling factors ISF´s from user starting points rutine SELECTED")
            print(" ")
        else:
            print("NOT A VALID IMPUT. EXITING")
            sys.exit('IMPUT ERROR')


    elif module_choice==2:
        print("Conformational analysis module SELECTED")
        print(" ")
        print("ATTENTION: all of these rutines require a valid list of ISF´s (ISFvis.txt) on the main directory to run.")
        print("These are produced by any of the rutines in the Spectra scaling module and stored in the corresponding VISSAT output folder")
        print(" ")
        print("Now please choose one of the following rutines to run:")
        print(" ")
        print("Obtain an optimal conformational distribution using esie1 (1)")
        print("Obtain an optimal conformational distribution using esie1 (2)")
        print("Obtain an optimal conformational distribution using ESI (3)")
        rutine_choice = int(input("Please choose: "))
        global_var.rutine_choice = rutine_choice
        if rutine_choice==1:
            print("Conformational distribution from esie1 SELECTED")
        elif rutine_choice==2:
            print("Conformational distribution from esie2 SELECTED")
        elif rutine_choice==3:
            print("Conformational distribution from ESI SELECTED")
        else:
            print("NOT A VALID IMPUT. EXITING")
            sys.exit('IMPUT ERROR')
        
    elif module_choice==3:
        print("Similarity toolbox module SELECTED")
        print(" ")
        print("ATTENTION: all of these rutines requeire a valid list of ISF´s (ISFvis.txt) on the main directory to run.")
        print("These are produced by any of the rutines in module 1 and stored in the corresponding VISSAT output folder")
        print(" ")
        print("Now please choose one of the following rutines to run:")
        print(" ")
        print("Obtain similarity values (SIR and ESI) using ISF´s already optimized (1)")
        print("Obtain similarity values (SIR and ESI) for each conformation individually (2)")
        rutine_choice = int(input("Please choose: "))
        global_var.rutine_choice = rutine_choice
        if rutine_choice==1:
            print("Similarity values from ISF´s SELECTED")
        elif rutine_choice==2:
            print("Similarity values per conformation SELECTED")
        else:
            print("NOT A VALID IMPUT. EXITING")
            sys.exit('IMPUT ERROR')
    else:
        print("NOT A VALID IMPUT. EXITING")
        sys.exit('IMPUT ERROR')

module_options()

print(" ")
print("*************************************")
print(" ")
print("The following conditions will be used:")
print(" ")
print("Conditions:")
print(" ")
print("General spectral details:")
print(" ")
print('Band halfwidth: ',conditions.h,'cm-1')
print('Spectral range: ',conditions.r1, '-',conditions.r2, 'cm-1')
print('Baseline correction of observed VCD: ',conditions.blc, 'cm-1')
print(" ")
print("*************************************")
print(" ")

ext = ('.out')

nconf = (len([files for files in os.listdir(parent_dir) if files.endswith(ext)]))

print(nconf, 'conformations have been detected')
print(" ")
print("*************************************")
print(" ")

if global_var.module_choice == 'scaling':
    global_var.module_choice = 1
    if global_var.rutine_choice == 'unscaled':
        global_var.rutine_choice = 1
    elif global_var.rutine_choice =='saf':
        global_var.rutine_choice = 2
    elif global_var.rutine_choice=='isfs':
        global_var.rutine_choice = 3
elif global_var.module_choice == 'conf':
    if global_var.rutine_choice=='esie1':
        global_var.rutine_choice=1
    elif global_var.rutine_choice=='esie2':
        global_var.rutine_choice=2
    elif global_var.rutine_choice=='esi':
        global_var.rutine_choice=3
elif global_var.module_choice == 'similarity':
    if global_var.rutine_choice=='isfs':
        global_var.rutine_choice=1
    elif global_var.rutine_choice=='xconf':
        global_var.rutine_choice=2

import runscript_mod
print("DONE")
sys.exit(0)    