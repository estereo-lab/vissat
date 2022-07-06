
# File Extraction

print(" ")
print("Extracting data from .out files...")

import re
import sys
import numpy as np
import pathlib
import global_var
import glob

parent_dir = global_var.parent_dir
free_energy_list = np.empty(0)
freq_list = np.empty(0)
dipstr_list = np.empty(0)
rotstr_list = np.empty(0)
filenames_list = []
lot_func_str_list =[]
NConf = 0
ext = ('*.out')
for files in pathlib.Path(parent_dir).glob(ext):
    NConf += 1
    element1 = (str('CONF'+ str('{:0>3}'.format(NConf))))
    element2 = pathlib.Path(files).name
    f = open (files,'r')
    content = (f.read())
    re_freeE = re.compile('(?<= Sum of electronic and thermal Free Energies=) *\-\d+\.\d+',re.MULTILINE)
    fe = re.search(re_freeE, content)
    free_energy = np.array(fe.group(0), dtype=np.float64)
    free_energy_list = np.append(free_energy_list, free_energy)
    re_freq = re.compile('(?<= Frequencies --) *(\-?\d+\.\d+) *(\d+\.\d+) *(\d+\.\d+)',re.MULTILINE)
    fr = re.findall(re_freq, content)
    freq = np.array(fr, dtype=np.float64)
    freq_list = np.append(freq_list, freq)
    re_dipstr = re.compile('(?<= Dip. str.   --) *(\d+\.\d+) *(\d+\.\d+) *(\d+\.\d+)',re.MULTILINE)
    ds = re.findall(re_dipstr, content)
    dipstr = np.array(ds, dtype=np.float64)
    dipstr_list = np.append(dipstr_list, dipstr)
    re_rotstr = re.compile('(?<= Rot. str.   --) *(\-?\d+\.\d+) *(\-?\d+\.\d+) *(\-?\d+\.\d+)',re.MULTILINE)
    rs = re.findall(re_rotstr, content)
    rotstr = np.array(rs, dtype=np.float64)
    rotstr_list = np.append(rotstr_list, rotstr)
    re_lot_func = re.compile(r'(?<= SCF Done:  E\()(\S+)(\))')
    lot_func = re.search(re_lot_func, content)
    lot_func_str = str(lot_func.group(1))
    re_lot_basis = re.compile(r'(?<= Standard basis: ) *\S+')
    lot_basis = re.search(re_lot_basis, content)
    lot_basis_str = str(lot_basis.group(0))
    element = [(element1,element2,lot_func_str,lot_basis_str)]
    filenames_list += element

if sum(n < 0 for n in freq_list)!=0:
    print ("NEGATIVE FREQUENCIES DETECTED")
    print ("EXITING PROGRAM")
    sys.exit('NEGATIVE FREQUENCIES') 
    

nIR = len(freq_list)
print(nIR)
nconf = len(glob.glob1(parent_dir,ext))
print(nconf)
nmodes = int(nIR/nconf)
print(nconf)

print(" ")
print("done")
print(" ")