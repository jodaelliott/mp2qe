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

All the best,
Josh

