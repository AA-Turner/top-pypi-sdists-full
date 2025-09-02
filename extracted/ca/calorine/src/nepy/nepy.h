#include "nep.h"
using namespace std;

// Local struct to hold an atomic configuration.
struct Atom {
  int N;
  std::vector<int> type;
  std::vector<double> cell, position, mass;
};

class NEPY {
private:
  NEP3 nep;
  struct Atom atom;
  std::string model_filename;

public:
  NEPY(const std::string &model_filename, int N_atoms,
       std::vector<double> box, std::vector<std::string> atom_symbols,
       std::vector<double> positions, std::vector<double> masses);
  std::vector<double> getDescriptors();
  std::vector<double> getDipole();
  std::vector<double> getDipoleGradient(double displacement, int method,
                                        double charge);
  std::vector<double> getPolarizability();
  std::vector<double> getPolarizabilityGradient(double displacement, std::vector<int> components);
  std::vector<double> getLatentSpace();
  std::tuple<std::vector<double>, std::vector<double>, std::vector<double>>
  getPotentialForcesAndVirials();
  std::vector<std::string> _getAtomSymbols(std::string model_filename);
  void _convertAtomTypeNEPIndex(int N, std::vector<std::string> atom_symbols,
                                std::vector<std::string> model_atom_symbols,
                                std::vector<int> &type);
  void _getCenterOfMass(std::vector<double> center_of_mass);
  void setPositions(std::vector<double> positions);
  void setCell(std::vector<double> cell);
  void setMasses(std::vector<double> masses);
  void setSymbols(std::vector<std::string> atom_symbols);
};
