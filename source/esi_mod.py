
# ESI calculation sub-rutine
print(" ")
print("Performing VCD similarity analysis...")
print(" ")
print(" ")

import global_var
import functions
import conditions
import numpy as np

# Data imput files
freqlistxconfOpt = global_var.freqlistxconfOpt
rotlistxconfOpt = global_var.rotlistxconfOpt
Yexppos = global_var.Yexppos
Yexpneg = global_var.Yexpneg
N = global_var.N
xx = global_var.xx

if global_var.module_choice == 3 and global_var.rutine_choice == 2:
    ESI_list =np.empty(0)
    esie1_list =np.empty(0)
    esie2_list =np.empty(0)
    for i in range(len(freqlistxconfOpt[0,:])):
        print(" ")
        print("Calculating similarities using pre-optimized ISF´s......")
        print(" ")
        print(i)            
        for j in range(len(freqlistxconfOpt[:,0])):
                if j== 0:
                    Ycal = functions.lor(1, global_var.xx, freqlistxconfOpt[j,i], rotlistxconfOpt[j,i], conditions.h)
                else: 
                    f1 = functions.lor(1, global_var.xx, freqlistxconfOpt[j,i], rotlistxconfOpt[j,i], conditions.h)
                    Ycal = Ycal + f1
        # Positive space
        
        Ycalpos = np.array(Ycal)
        Ycalpos[Ycalpos<0] = 0
        
        # Negative space
        
        Ycalneg = np.array(Ycal)
        Ycalneg[Ycalneg>0] = 0
        Ycalneg = np.abs(Ycalneg)
        
        (ESI,esie1,esie2) = functions.esisim(Yexppos,Yexpneg,Ycalpos,Ycalneg)
        ESI_list = np.append(ESI_list, ESI)
        esie1_list = np.append(esie1_list, esie1)
        esie2_list = np.append(esie2_list, esie2)
        
        print('A VCD similarity value of',round(esie1, 3),' was found for the calculated enantiomer')
        print(" ")
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
        
        print("done")
        print(" ")
else:        
    for i in range(len(freqlistxconfOpt[:,0])):
        for j in range(len(freqlistxconfOpt[0,:])):
            if i== 0 and j==0:
                Ycal = functions.lor(1, xx, freqlistxconfOpt[i,j], rotlistxconfOpt[i,j], conditions.h)
            else: 
                f1 = functions.lor(1, xx, freqlistxconfOpt[i,j], rotlistxconfOpt[i,j], conditions.h)
                Ycal = Ycal + f1
    
    # Positive space
    
    Ycalpos = np.array(Ycal)
    Ycalpos[Ycalpos<0] = 0
    
    # Negative space
    
    Ycalneg = np.array(Ycal)
    Ycalneg[Ycalneg>0] = 0
    Ycalneg = np.abs(Ycalneg)
    
    (ESI,esie1,esie2) = functions.esisim(Yexppos,Yexpneg,Ycalpos,Ycalneg)
    
    print('A VCD similarity value of',round(esie1, 3),' was found for the calculated enantiomer')
    print(" ")
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
    
    print("done")
    print(" ")