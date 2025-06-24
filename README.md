# polyacrylates
Polarizable MD simulations using AMOEBA Force Field and Monte Carlo Simulations in Python for the study: "Polyacrylates with protein recognition and functional modulation".

Input files for the polarizable MD simulations:
f1seq1.xyz, f1seq2.xyz, f8seq1.xyz, pegseq1.xyz - in Tinker XYZ format

Parameter files for AMOEBA:
parameters.prm, tinker.key

Python scripts for analysis:
interactionenergy.py - calculates interaction energy between two groups of atoms.

VMD scripts for analysis:
vmd1.tcl - backbone RMSD and radius of gyration (Rg) for GFP; Rg, end-to-end distance, SASA for oligomer;
vmd2.tcl - trans-cis angle for chromophore (CRO)
vmd3.tcl - distance of center of mass (COM) of oligomer from COM of protein and CRO atom 734; coordinates of benzene ring C in CRO
vmd4.tcl - coordinates of imidazole ring atoms in CRO
vmd5.tcl - coordinates of COM of oligomer
vmd6.tcl - RDFs
vmd7.tcl - RMSD of CRO

Monte Carlo simulations in Python:
montecarlo.py - to run the Monte Carlo Simulations
euclideandistance.py - for calculation of Euclidean Distances

If you use this repository or scripts in your work, please cite the associated publication:

```Polyacrylates with protein recognition and functional modulation, Darwin C. Gomez, Swarnadeep Seth, Ronnie Mondal, Stephen J. Koehler, Jared G. Baker, Charles Plate, Ian C. Anderson, Mikayla R. Smith, Joey Gloriod, Morgan Gunter, Valerie Vaissier Welborn, Sanket A. Deshmukh, C. Adrian Figg, Journal Name, Year. [DOI/link to be added when available]```
