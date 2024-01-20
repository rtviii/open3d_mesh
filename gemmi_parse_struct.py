import gemmi
import numpy as np

struct_path = "./tunnels_for_Artem/euk/3JAH/3JAH.cif"
# Load the structure
structure = gemmi.read_structure(struct_path)