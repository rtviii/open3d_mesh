#include <iostream>

namespace cif = gemmi::cif;

int main() {
  cif::Document doc = cif::read_file("./tunnels_for_Artem/euk/3JAH/3JAH.cif");

  for (cif::Block& block : doc.blocks)
    for (auto cc : block.find("_chem_comp.", {"id", "formula_weight"}))
      std::cout << c<c[0] << " weights " << cc[1] << std::endl;
}




