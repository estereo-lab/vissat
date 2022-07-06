# VISSAT
A similarity tool for the analysis of IR and VCD vibrational spectra

Introduction

VISSAT is a software designed to aid in the comparison between calculated and observed infrared (IR) and vibrational circular dichroism (VCD) spectra of multi-conformational molecules. It uses Gaussian output files as the source of the calculated spectral parameters for each considered conformation, and then produces weighted IR and VCD spectra that are compared to the corresponding observed spectra.
Its attributes include the use of different methods to scale calculated frequencies, such as global and individual scaling factors. Then, similarity between observed and computed traces are calculated using IR (SIR) and VCD (ESI) similarity functions.
Additionally, different tools to allow a deeper analysis of the conformational preferences of the studied molecule, from the spectral similarity standpoint of view, are also available.

System requirements and installation

At the moment, VISSAT is available as a Python source code. To run it, a Python environment with the following packages installed is needed (latest version tested):
-	Python version 3.10.4.
-	scipy 1.8.0.
-	matplotlib 3.5.1.
-	fpdf 1.7.2 (use “conda install -c conda-forge fpdf” to install)
-	tabulate 0.8.9.
The following procedure can be used to install a suitable Miniconda environment:
-	Download and install Miniconda for your system from: https://docs.conda.io/en/latest/miniconda.html
-	Create a Conda environment that includes the needed packages. For this, open the Anaconda prompt and use the following command lines: 
conda create -n vissat-env python scipy matplotlib tabulate
-	Activate the created environment:
conda activate vissat-env
-	Install the remaining packages:
conda install -c conda-forge fpdf 
To finally run the code, navigate to the folder containing the VISSAT source code files and execute the main code with python:
python vissat.py

Input files

For VISSAT to run, it requires at least one gaussian out file and two separate text files for IR and VCD observed spectra. These files need to be located in the ~/vissat/ installation folder.
-	Gaussian files: FREQ or OPT-FREQ output files (.OUT) obtained using Gaussian version 03, 09 or 16, in either Windows or Linux, are required to extract frequencies, dipole strengths, rotational strengths and free-energies.
-	Observed spectra: IR and VCD spectra need to be tabulated in text files named IRexp.txt and VCDexp.txt respectively.
Additionally, the file condition.py can be used to modify default parameters such as spectral range and band half-widths.

Use Modules

The software has three principal modules that group different sub-routines to be performed. Each of them starts by extracting relevant data from the input text files (Gaussian out files, observed spectra txt files, etc.) and then produces a folder that contains a report with the obtained results, along with ASCII data files for post processing.
1.- Spectra scaling: Weighted spectra is calculated using the selected scaling methodology, and similarity values for IR (SIR) and VCD (ESI) are computed.
2.- Conformational analysis: The conformational abundances of each conformer are optimized to produce the best VCD similarity between calculated and observed spectra. Optimization towards the different VCD similarity functions (SE, S-E and ESI) can be selected.
3.- Similarity toolbox: Similarity functions can be computed using previously produced scaled frequencies. Results can be obtained for the weighted spectra or for individual conformations separately.

Output files

Every time a VISSAT routine is completed, a folder containing details about the calculations is created. Inside, the following output files can be found: 
 
-	VISSAT report PDF: A single page with the more essential results such as IR/VCD spectra comparisons and similarity values found.
-	VISSAT report TXT: A text output file containing methodological details such as, routine performed, gaussian file names, level of theory, conditions used, etc.
-	MATRICES folder: A folder with different text files that contain data calculated during the chosen routine.  
