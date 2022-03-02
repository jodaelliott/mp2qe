
from scipy.constants import physical_constants as constants

from pseudopotentials import qe_pppath as ppath

RytoeV = 1./constants["Rydberg constant times hc in eV"][0]

def set_espresso_param(parameters, kw, kwarg):
   # 
   # Update espresso parameter dictionary with keyword and keyword argument
   #
   parameters[kw] = kwarg
   return()

def vasp_to_espresso(vasp_params, basic=False, debug=True):
   #
   # Go through the vasp parameters and create dictionary of espresso parameters
   #

   # Initial (minimal set of params) to run simulation
   espresso_params = {
          # CONTROL
          "calculation" : "scf",
          "prefix"      : "espresso",
          "outdir"      : "tmp",
          "pseudo_dir"  : ppath,
          "verbosity"   : "high",
          "title"       : "name",
          "tprnfor"     : True,
          "disk_io"     : "low",
          # SYSTEM
          "ecutwfc"     :  40,
          # ELECTRONS
      }

   if not basic:
   # Basic option ignores all following vasp parameters, can be used to check symmetry etc.
      for param in vasp_params:
   
   
         if param == 'SYSTEM':
            set_espresso_param(espresso_params, "title", vasp_params[param])
   
         elif param == 'ALGO':
            # Algorithm for solution of the SCF cycle
            if (vasp_params[param] == "Normal"):
               set_espresso_param(espresso_params, "diagonalization", "david")
   
            elif (vasp_params[param] == "Fast") or (vasp_params[param] == "VeryFast"):
               set_espresso_param(espresso_params, "diagonalization", "rmm-davidson")
   
            elif (vasp_params[param] == "All") or (vasp_params[param] == "Conjugate"):
               set_espresso_param(espresso_params, "diagonalization", "cg")
   
         elif param == "ISPIN":
            # Spin polarization
            # XSpectra not compatible with nspin = 4
            if (vasp_params[param] == 1):
               set_espresso_param(espresso_params, "nspin", 1)
   
            elif (vasp_params[param] == 2):
               set_espresso_param(espresso_params, "nspin", 2)
   
         elif param == "NELM":
            # Max number of SCF steps
            set_espresso_param(espresso_params, "electron_maxstep", vasp_params[param])
   
         elif param == "EDIFF":
            # Threshold for convergence of SCF
            set_espresso_param(espresso_params, "conv_thr", vasp_params[param]/RytoeV)
   
         elif param == "NSW":
            # Number of ionic steps (calculation = scf should override this no matter what)
            if vasp_params[param] == 0:
               set_espresso_param(espresso_params, "nstep", 1)
            else:
               set_espresso_param(espresso_params, "nstep", vasp_params[param])
   
         elif param == "ISIF":
            # Calculate and print stress to outputfile
            if vasp_params[param] > 0: set_espresso_param(espresso_params, "tstress", True)
   
         elif param == "ISYM":
            # Turn on/off symmetry
            if vasp_params[param] < 0: set_espresso_param(espresso_params, "nosym", True)
   
         elif param == "ENCUT":
            # Cutoff for plane waves
            set_espresso_param(espresso_params, "ecutwfc", round(vasp_params[param]*RytoeV, -1))
            if (debug): print("Caution: cutoff on planewaves not transferable between codes, for production ecutwfc should be converged.")
   
         elif param == "NBANDS":
            # Number of bands to compute
            set_espresso_param(espresso_params, "nbnd", vasp_params[param])
   
         elif param == "ISMEAR":
            # Type of smearing to apply
            if (vasp_params[param] >= -1):
               #espresso_params["occupations"] = "smearing"
               set_espresso_param(espresso_params, "occupations", "smearing")
               if vasp_params[param] > 0:
                  set_espresso_param(espresso_params, "smearing", "methfessel-paxton")
                  if (debug): print("Caution: Espresso only allows for first-order MP smearning, we have order %d" % (vasp_params[param]))
               elif vasp_params[param] == 0:
                  set_espresso_param(espresso_params, "smearing", "gaussian")
               elif vasp_params[param] == -1:
                  set_espresso_param(espresso_params,"smearing", "fermi-dirac")
            elif (vasp_params[param] == -4):
               set_espresso_param(espresso_params, "occupations", "tetrahedra_opt")
            elif (vasp_params[param] == -5):
               #espresso_params["occupations"] = "tetrahedra"
               set_espresso_param(espresso_params,"occupations", "tetrahedra")
            else:
               print("Bizzare vasp smearning used, contact joshua.elliott@diamond.ac.uk")
   
         elif param == "SIGMA":
            # Value of sigma used for smearing
            set_espresso_param(espresso_params, "degauss", vasp_params[param]*RytoeV)
   
         elif param == "MAGMOM":
            # Initial magnetic moments
            mgmom = []
            for atom in enumerate(vasp_params[param]):
               mgmom.append(atom[1])
   
            set_espresso_param(espresso_params, "starting_magnetization", mgmom)
   
         # We ignore IBRION, ICHARG because we set calculation='scf' and use espresso default
         # (atomic+random) for intial wfc and density 
         elif (param == "IBRION") or (param == "ICHARG"):
            if debug: print("%s knowingly overidden" % (param))
         
         elif (param == "NELMIN") or (param == "PREC") or (param == "LREAL") or (param == "KPOINT_BSE") or (param == "LPEAD") or (param == "LEFG") or (param == "LCALCPOL") or (param == "LCALCEPS") or (param == "EFIELD_PEAD"):
            if debug: print("%s knowingly ignored" % (param))
   
         elif (param == "LWAVE") or (param == "LCHARG") or (param == "LORBIT") or (param == "LAECHG"):
            if debug: print("For %s, disk input/output handled by qe disk_io" % (param))
   
         else:
            print("I have ignored VASP parameter: %s" % (str(param)))
   
   
   if debug: print(espresso_params)
   return(espresso_params)

def set_starting_magnetization(params, atoms):
   # set initial magnetization in atoms object and expunge magmom from espresso parameters dictionary
   mgmom = params["starting_magnetization"]
   atoms.set_initial_magnetic_moments(magmoms=mgmom)

   return(atoms)

def get_vasp_kgrid(grid_data, debug=False):

   # Figure out the grid definition
   if grid_data["generation_style"] == "Monkhorst":
      grid = grid_data["kpoints"][0]
      offset = grid_data["shift"]

   if debug: print(offset)
   for sk in enumerate(offset):
      if sk[1] == 0.5:
         offset[sk[0]] = 1

   if debug: print(grid, offset)
   return(grid, offset)
