
**File  Detail**

* simulation.py  - Main simulation file  
* options.py - simulation options parameter
* adjustment.py  - adjustment step from the algorithm
* jump.py - Jump operation 
* projection.py - projection operation
* utility_foam.py - utility functions to use in diffent files
* convergence.py - check convergence with the reference run 
* analysis.py - analysing with plot 


**Folder Detail**

* __OpenFoam_coarse/__ - Project structure with coarse mesh and coarse time with initial variables 
* __OpenFoam_fine/__ - Project structure with fine mesh and fine time with initial variables 

**Before running simulation**

* OpenFoam must be installed we used __openfoam8__ version 
* Install python modules from __requirements.txt__
* Have to run __blockMesh__ command in both  __OpenFoam_fine/__, __OpenFoam_coarse/__
* Setup simulation parameter in options.py 


**Command to run simulation**

* python simulation.py 

* python simulation.py > simlog.log  -> to save log



