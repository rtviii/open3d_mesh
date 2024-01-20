// #include "gemmi/include/gemmi/read_cif.hpp"  // for cif::read, cif::write
#include "gemmi/include/gemmi/cif.hpp"
#include "gemmi/include/gemmi/gz.hpp"
#include "gemmi/include/gemmi/mmcif.hpp"
#include <fstream>  // for std::ofstream
#include <iostream>
#include <string>


using namespace gemmi;
int main() {

    const std::string& cif_path = "/home/rtviii/dev/open3d_mesh/3JAH/3JAH.cif";


    gemmi::cif::Document doc   = gemmi::cif::read_file(cif_path);
    gemmi::Structure structure = gemmi::make_structure(doc);
}