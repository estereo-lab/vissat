# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:44:30 2022

@author: mamun
"""
import numpy as np
import scipy.interpolate as interpolate
import conditions
import global_var


# Lorentzian function

# x: frequency scaling factor
# y: frequency
# a: mode frequency
# b: mode intensity
# c: bandwidth
    
def lor(x, y, a, b, c):

    return a*x*b*(c/((y-(a*x))**2+c**2))


# Similarity function

# a: experimental Y
# b: calculated Y 
# xmin: inferior range
# xmax: superior range

def sim(Yexp, Ycal):
    r1 = conditions.r1
    r2 = conditions.r2
    xx = global_var.xx
    t_a, c_a, k_a = interpolate.splrep(xx, (Yexp*Ycal), s=0, k=3)
    t_b, c_b, k_b = interpolate.splrep(xx, (Yexp*Yexp), s=0, k=3)
    t_c, c_c, k_c = interpolate.splrep(xx, (Ycal*Ycal), s=0, k=3)

    YexpxYcal = interpolate.BSpline(t_a, c_a, k_a, extrapolate=False)
    YexpxYexp = interpolate.BSpline(t_b, c_b, k_b, extrapolate=False)
    YcalxYcal = interpolate.BSpline(t_c, c_c, k_c, extrapolate=False)

    return YexpxYcal.integrate(r1,r2)/(np.sqrt(YexpxYexp.integrate(r1,r2)*YcalxYcal.integrate(r1,r2)))


# SAF function

# a: freqlist por conf
# b: diplist por conf
# c: halfwidth
# d: inferior range
# e: superior range
# f: single scaling factor
# g: experimental function

def safmin(freqlistxconf, diplistxconf, h, saf, Yexp):
    xx = global_var.xx

    for i in range(len(freqlistxconf[:,0])):
        for j in range(len(freqlistxconf[0,:])):
            if i== 0 and j==0:
                Ycal = lor(saf, xx, freqlistxconf[i,j], diplistxconf[i,j], h)
            else: 
                f1 = lor(saf, xx, freqlistxconf[i,j], diplistxconf[i,j], h)
                Ycal = Ycal + f1
    return sim(Yexp,Ycal)


# VCD similarity function

# a: freqlist por conf
# b: diplist por conf
# c: halfwidth
# d: inferior range
# e: superior range
# f: single scaling factor
# g: experimental function

def esisim(Yexppos,Yexpneg,Ycalpos,Ycalneg):
    r1 = conditions.r1
    r2 = conditions.r2
    xx = global_var.xx
    
    t_a, c_a, k_a = interpolate.splrep(xx, (Yexppos), s=0, k=3)
    t_b, c_b, k_b = interpolate.splrep(xx, (Yexpneg), s=0, k=3)
    t_c, c_c, k_c = interpolate.splrep(xx, (Ycalpos), s=0, k=3)
    t_d, c_d, k_d = interpolate.splrep(xx, (Ycalneg), s=0, k=3)
    
    Yexppos_fun = interpolate.BSpline(t_a, c_a, k_a, extrapolate=False)
    Yexpneg_fun = interpolate.BSpline(t_b, c_b, k_b, extrapolate=False)
    Ycalpos_fun = interpolate.BSpline(t_c, c_c, k_c, extrapolate=False)
    Ycalneg_fun = interpolate.BSpline(t_d, c_d, k_d, extrapolate=False)
    
    # Enantiomer 1 ESI caculation
    # Positive parameters
    spos = sim(Yexppos,Ycalpos);
    wpos = Yexppos_fun.integrate(r1,r2)+Ycalpos_fun.integrate(r1,r2)
    # Negative parameters
    sneg = sim(Yexpneg,Ycalneg);
    wneg = Yexpneg_fun.integrate(r1,r2)+Ycalneg_fun.integrate(r1,r2)
    
    esie1 = ((spos*wpos)+(sneg*wneg))/(wpos+wneg)
    
    # Enantiomer 2 ESI caculation
    # Positive parameters
    spose = sim(Yexppos,Ycalneg);
    wpose = Yexppos_fun.integrate(r1,r2)+Ycalneg_fun.integrate(r1,r2)
    # Negative parameters
    snege = sim(Yexpneg,Ycalpos);
    wnege = Yexpneg_fun.integrate(r1,r2)+Ycalpos_fun.integrate(r1,r2)
    
    esie2 = ((spose*wpose)+(snege*wnege))/(wpose+wnege)
    
    ESI = esie1-esie2
    
    return ESI, esie1, esie2


def isfmin(freqlistxconf, diplistxconf, h, isfs, Yexp):
    freqlistxconf = freqlistxconf * isfs[:, np.newaxis]
    xx = global_var.xx
    i=0    
    while i in range(len(freqlistxconf[:,global_var.globalmin])-1):
      if freqlistxconf[i+1,global_var.globalmin]-freqlistxconf[i,global_var.globalmin]< 0:
          check = False
          break
      else:
        i = i+1
        check = True
    
    if check==True:
        for i in range(len(freqlistxconf[:,0])):
            for j in range(len(freqlistxconf[0,:])):
                if i== 0 and j==0:
                    Ycal = lor(1, xx, freqlistxconf[i,j], diplistxconf[i,j], h)
                else: 
                    f1 = lor(1, xx, freqlistxconf[i,j], diplistxconf[i,j], h)
                    Ycal = Ycal + f1    
                result = sim(Yexp,Ycal)
    else:
        result = -1
            
    return result

def Se_min(freqlistxconf, rotlistxconf, h, cnfabn, Yexppos, Yexpneg, rutine_choice):
    cnfabn = np.abs(cnfabn)
    rotlistxconf = rotlistxconf * cnfabn[np.newaxis,:]
    xx = global_var.xx
    i=0    

    for i in range(len(freqlistxconf[:,0])):
        for j in range(len(freqlistxconf[0,:])):
            if i== 0 and j==0:
                Ycal = lor(1, xx, freqlistxconf[i,j], rotlistxconf[i,j], h)
            else: 
                f1 = lor(1, xx, freqlistxconf[i,j], rotlistxconf[i,j], h)
                Ycal = Ycal + f1
    
    # Positive space   
    Ycalpos = np.array(Ycal)
    Ycalpos[Ycalpos<0] = 0
   
    # Negative space    
    Ycalneg = np.array(Ycal)
    Ycalneg[Ycalneg>0] = 0
    Ycalneg = np.abs(Ycalneg)
    
    (ESI,esie1,esie2) = esisim(Yexppos,Yexpneg,Ycalpos,Ycalneg)
    
    if rutine_choice==1:        
        result = esie1
    elif rutine_choice==2:
        result = esie2
    elif rutine_choice==3:
        result = ESI
           
    return result
























