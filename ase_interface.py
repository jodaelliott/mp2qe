
#
# Interface to the Atomic Simulation Environment Routines
#

import numpy as np
from scipy.constants import physical_constants as constants

from ase import Atoms
from ase.io.espresso import write_espresso_in

from mp_interface import get_url, get_json
from space_group import space_group_to_ibrav

#
# Physical Constants
#
angtobohr = 1./(1e10*constants["Bohr radius"][0])
degtorad  = np.pi/180.

def build_atoms(system_json, cell):
   #
   # Build an ase.Atoms object from the mp json files
   #
   positions = np.zeros([len(system_json), 3])
   symbols = np.chararray(len(system_json), itemsize=2, unicode=True)

   for i in enumerate(positions):
      i[1][:] = system_json[i[0]]['abc']
      symbols[i[0]] = system_json[i[0]]['label']

   system = Atoms(symbols=symbols, scaled_positions=positions, cell=cell)

   return(system)

def get_ibrav(lat, material_id, api_key, debug=False):
   #
   # Determine all of the structural properties of the crystal
   #
   a = float("%.4f" % lat["a"])
   b = float("%.4f" % lat["b"])
   c = float("%.4f" % lat["c"])

   alpha = float("%.4f" % lat["alpha"])
   beta  = float("%.4f" % lat["beta"])
   gamma = float("%.4f" % lat["gamma"])

   if (debug): print(" a: %.4f\n b: %.4f\n c: %.4f\n alpha: %.4f\n beta: %.4f\n gamma: %.4f" % 
                     (a, b, c, alpha, beta, gamma))

   sg_url = get_url(material_id, api_key, feature='spacegroup')
   sg_data = get_json(sg_url)["spacegroup"]

   crystal = sg_data["crystal_system"]
   space_group = sg_data["number"]
   ibrav = int(space_group_to_ibrav(space_group))

   celldm = np.zeros(6)
   celldm[0] = a*angtobohr

   if (ibrav == 1) or (ibrav == 2) or (ibrav == 3) or (ibrav == -3):
      pass
   elif (ibrav == 4) or (ibrav == 6) or (ibrav == 7):
      celldm[2] = c/a
   elif (ibrav == 5) or (ibrav == -5):
      if debug: print(np.cos(gamma*degtorad))
      celldm[3] = np.cos(gamma*degtorad)
   elif (ibrav == 8) or (ibrav == 9) or (ibrav == -9) or (ibrav == 91) or (ibrav == 10) or (ibrav == 11):
      celldm[1] = b/a
      celldm[2] = c/a
   elif (ibrav == 12):
      celldm[1] = b/a
      celldm[2] = c/a
      celldm[3] = np.cos(a*b)
   elif (ibrav == -12):
      celldm[1] = b/a
      celldm[2] = c/a
      celldm[4] = np.cos(a*c)
   elif (ibrav == 13):
      celldm[1] = b/a
      celldm[2] = c/a
      celldm[3] = np.cos(gamma)
   elif (ibrav == -13):
      celldm[1] = b/a
      celldm[2] = c/a
      celldm[4] = np.cos(beta)
   elif (ibrav == 14):
      celldm[1] = b/a
      celldm[2] = c/a
      celldm[3] = np.cos(b*c)
      celldm[4] = np.cos(a*c)
      celldm[5] = np.cos(a*b)

   return(ibrav, crystal, celldm, [a, b, c, alpha, beta, gamma])

def export_pwi(material_id, atoms, input_data, pseudopotentials, kpts):
   #
   # Open and write a quantum espresso, pw.x input file
   #
   f = open(material_id+"_scf.pwi", "w")
   # Write and close espresso input file
   write_espresso_in(f, atoms, input_data=input_data, pseudopotentials=pseudopotentials, kpts=kpts[0], koffset=kpts[1])
   f.close()

   return()
