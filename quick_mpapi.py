
#
# To do:
# Remove hardcoded path to pseudopotential library
# Expand print summary to whole api data
# Create a child class of ase.Atoms to handle mp_interface
#

#
# Standard Python libraries
#
import numpy as np
from scipy.constants import physical_constants as constants
import json

#
# Atomic Simulation Environment
#
from ase import Atoms
from ase.visualize import view

#
# Local libraries
#
from ase_interface import build_atoms, get_ibrav, export_pwi
from mp_interface import get_url, get_json, print_summary
from pseudopotentials import qe_pppath as ppath, qe_uspp_gipaw as pps
from simulationparameters import vasp_to_espresso, set_starting_magnetization, get_vasp_kgrid 

espresso_version=7.0

#
# Physical Constants
#
angtobohr = 1./(1e10*constants["Bohr radius"][0])
degtorad  = np.pi/180.

#
# The material identifyer and user key to download
# this needs to be figured out
#
material_id = 
api_key     = 
lview       = True 
lsummary    = True

if __name__ == "__main__":
   #
   # Grab the task data from materials project in JSON format
   #
   m_url = get_url(material_id, api_key)            # Structure
   m_data = get_json(m_url)
   
   s_url = get_url(material_id, api_key, "incar")   # Input parameters
   s_data = get_json(s_url)["incar"]
   
   k_url = get_url(material_id, api_key, "kpoints") # k-point grid
   k_data = get_json(k_url)["kpoints"]

   #   
   # Figure out which bravais lattice to use
   #
   ibrav, crystal, celldm, cell_param = get_ibrav(m_data["structure"]["lattice"], material_id, api_key, False)

   #   
   # Construct atoms object
   #
   a = build_atoms(m_data["structure"]["sites"], cell_param)

   #
   # Simulation paramaters from vasp
   #
   param = vasp_to_espresso(s_data, False, False, version=espresso_version)
   # If magnetic, get starting magnetic moments
   try:
       if param["nspin"] == 2:
           a = set_starting_magnetization(param, a)
           param.pop("starting_magnetization")
   except Exception as e:
       print(e)
       pass

   #
   # Set k-point grid
   #
   kpts = get_vasp_kgrid(k_data)

   #   
   # Espresso file for writing
   #
   export_pwi(material_id, a, param, pps, kpts)

   #
   # Other useful features from user input
   #
   if lview:
      view(a)
   if lsummary:
      print_summary(crystal, ibrav)   
