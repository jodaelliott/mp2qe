# Materials Project to Quantum Espresso

Attempt at general purpose translation between materials project (API) and Quantum Espresso (pw.x) input files.

Requires:
- Numpy
- SciPy
- Atomic Simulation Environment
- PSLibrary Pseudopotential Library

Setup:
This early version requires just three input parameters:
  - (i) Materials project api key (<code>api_key</code> set in <code>quick_mpapi.py</code>)
 - (ii) Materials project material id code (for best results use scf task id) (<code>material_id</code> set in <code>quick_mpapi.py</code>)
- (iii) Path to pseudopotential library (set in <code>pseudopotentials.py</code>)

NB this set of inputs will be edited/expanded in the future.

## Not implemented yet (but under development)
 - k-point grids not generated via Monkhorst pack. Will revert to Gamma point only.
 - nscf, relax, vc-relax, MD, will revert to <code>calculation=scf</code>
 - spin-orbit coupling, expect erratic behaviour
 - complex magenetic ordering (AFM arrangment of the same atomic type), will revert to FM ordering

## How to use

- Install/Load relevant packages
- Set API key:
  - Go to Materials Project Website and register for an account.
  - Log in to account and navigate to API (in the top menu bar)
  - Under the section API Keys, your personal API key should be reported
  - Copy your personal api key into the variable <code>api_key</code> on line 41 of <code>quick_mpapi.py</code>
- Set Pseudopotential Path
  - On the workstation/server where you will launch calculations, navigate to the directory containing the gipaw pseudopotentials
  - type <code>pwd</code>, copy and past the printed path to <code>qe_pppath</code> on line 4 of <code>psuedopotentials.py</code>
- Set the material identification number
  - From the materials project dashboard, select the elements in the material you wish to simulate, click search
  - Chose the option which matches the correct chemical formula and crystal phase of your material
  - Verify it is the correct material and navigate to calculation summary
  - Select a simulation option (for best results with this software, I recommend static if available)
  - Copy the unique material identification number <code>mp-xxxx</code> from the top of the page (highlighted in a blue box) into the variable <code>material_id</code> on line 40 of <code>quick_mpapi.py</code>
- Lauch mp2qe
  - type <code>python3 quick_mpapi.py</code> into the console
  - (Optional) Store list of ignored vasp parameters (if any), send them to me to check!
  - Check the output <code>mp-xxxx.pwi</code> input file for obvious errors
 - Launch Quantum Espresso
   - <code>mpirun -np 4 pw.x -inp mp-xxxx.pwi</code> 
All the best,
Josh

