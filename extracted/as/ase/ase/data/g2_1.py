# fmt: off

# flake8: noqa
"""
The following contains a database of small molecules

Data for the G2/97 database are from
Raghavachari, Redfern, and Pople, J. Chem. Phys. Vol. 106, 1063 (1997).
See http://www.cse.anl.gov/Catalysis_and_Energy_Conversion/Computational_Thermochemistry.shtml for the original files.

All numbers are experimental values, except for coordinates, which are
MP2(full)/6-31G(d) optimized geometries (from http://www.cse.anl.gov/OldCHMwebsiteContent/compmat/G2-97.htm)

Atomic species:
ref: Curtiss et al. JCP 106, 1063 (1997).
'Enthalpy' is the experimental enthalpies of formation at 0K
'thermal correction' is the thermal corrections H(298)-H(0)

Molecular species:
ref: Staroverov et al. JCP 119, 12129 (2003)
'Enthalpy' is the experimental enthalpies of formation at 298K
'ZPE' is the zero-point energies
'thermal correction' is the thermal enthalpy corrections H(298K) - H_exp(0K)
ZPE and thermal corrections are estimated from B3LYP geometries and vibrations.

For details about G2-1 and G2-2 sets see doi:10.1063/1.477422.

Experimental ionization potentials are from http://srdata.nist.gov/cccbdb/
Information presented on these pages is considered public information
and may be distributed or copied http://www.nist.gov/public_affairs/disclaimer.cfm

"""

from ase.symbols import string2symbols

atom_names = ['H', 'Li', 'Be', 'C', 'N', 'O', 'F', 'Na', 'Si', 'P', 'S', 'Cl']

molecule_names = ['LiH', 'BeH', 'CH', 'CH2_s3B1d', 'CH2_s1A1d', 'CH3', 'CH4', 'NH', 'NH2', 'NH3', 'OH', 'H2O', 'HF', 'SiH2_s1A1d', 'SiH2_s3B1d', 'SiH3', 'SiH4', 'PH2', 'PH3', 'SH2', 'HCl', 'Li2', 'LiF', 'C2H2', 'C2H4',
                  'C2H6', 'CN', 'HCN', 'CO', 'HCO', 'H2CO', 'CH3OH', 'N2', 'N2H4', 'NO', 'O2', 'H2O2', 'F2', 'CO2', 'Na2', 'Si2', 'P2', 'S2', 'Cl2', 'NaCl', 'SiO', 'CS', 'SO', 'ClO', 'ClF', 'Si2H6', 'CH3Cl', 'CH3SH', 'HOCl', 'SO2']

data = {
    'Be': {'CAS No.': 7440417,
           'charges': None,
           'database': 'G2-1',
           'description': 'Be atom',
           'enthalpy': 76.48,
           'ionization energy': 9.32,
           'magmoms': None,
           'name': 'Beryllium',
           'positions': [[0.0, 0.0, 0.0]],
           'symbols': 'Be',
           'thermal correction': 0.46},
    'BeH': {'CAS No.': 13597972,
            'ZPE': 2.9073,
            'charges': None,
            'database': 'G2-1',
            'description': 'Beryllium hydride (BeH), D*h symm.',
            'enthalpy': 81.7,
            'ionization energy': 8.21,
            'magmoms': [0.8, 0.2],
            'name': 'BeH (beryllium monohydride)',
            'positions': [[0.0, 0.0, 0.269654], [0.0, 0.0, -1.078616]],
            'symbols': 'BeH',
            'thermal correction': 2.0739},
    'C': {'CAS No.': 7440440,
          'charges': None,
          'database': 'G2-1',
          'description': 'C atom',
          'enthalpy': 169.98,
          'ionization energy': 11.26,
          'magmoms': [2.0],
          'name': 'Carbon',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'C',
          'thermal correction': 0.25},
    'C2H2': {'CAS No.': 74862,
             'ZPE': 16.6001,
             'charges': None,
             'database': 'G2-1',
             'description': 'Acetylene (C2H2), D*h symm.',
             'enthalpy': 54.2,
             'ionization energy': 11.4,
             'magmoms': None,
             'name': 'C_2H_2',
             'positions': [[0.0, 0.0, 0.60808],
                           [0.0, 0.0, -0.60808],
                           [0.0, 0.0, -1.67399],
                           [0.0, 0.0, 1.67399]],
             'symbols': 'CCHH',
             'thermal correction': 2.4228,
             'vertical ionization energy': 11.49},
    'C2H4': {'CAS No.': 74851,
             'ZPE': 31.5267,
             'charges': None,
             'database': 'G2-1',
             'description': 'Ethylene (H2C=CH2), D2h symm.',
             'enthalpy': 12.5,
             'ionization energy': 11.4,
             'magmoms': None,
             'name': 'C_2H_4',
             'positions': [[0.0, 0.0, 0.66748],
                           [0.0, 0.0, -0.66748],
                           [0.0, 0.922832, 1.237695],
                           [0.0, -0.922832, 1.237695],
                           [0.0, 0.922832, -1.237695],
                           [0.0, -0.922832, -1.237695]],
             'symbols': 'CCHHHH',
             'thermal correction': 2.51,
             'vertical ionization energy': 11.49},
    'C2H6': {'CAS No.': 74840,
             'ZPE': 46.095,
             'charges': None,
             'database': 'G2-1',
             'description': 'Ethane (H3C-CH3), D3d symm.',
             'enthalpy': -20.1,
             'magmoms': None,
             'name': 'C_2H_6',
             'positions': [[0.0, 0.0, 0.762209],
                           [0.0, 0.0, -0.762209],
                           [0.0, 1.018957, 1.157229],
                           [-0.882443, -0.509479, 1.157229],
                           [0.882443, -0.509479, 1.157229],
                           [0.0, -1.018957, -1.157229],
                           [-0.882443, 0.509479, -1.157229],
                           [0.882443, 0.509479, -1.157229]],
             'symbols': 'CCHHHHHH',
             'thermal correction': 2.7912},
    'CH': {'CAS No.': 3315375,
           'ZPE': 3.9659,
           'charges': None,
           'database': 'G2-1',
           'description': 'CH radical. Doublet, C*v symm.',
           'enthalpy': 142.5,
           'ionization energy': 10.64,
           'magmoms': [1.0, 0.0],
           'name': 'CH(Methylidyne)',
           'positions': [[0.0, 0.0, 0.160074], [0.0, 0.0, -0.960446]],
           'symbols': 'CH',
           'thermal correction': 2.0739},
    'CH2_s1A1d': {'CAS No.': 2465567,
                  'ZPE': 10.2422,
                  'charges': None,
                  'database': 'G2-1',
                  'description': 'Singlet methylene (CH2), C2v symm, 1-A1.',
                  'enthalpy': 102.8,
                  'magmoms': None,
                  'name': 'CH_2 (^1A_1)',
                  'positions': [[0.0, 0.0, 0.174343],
                                [0.0, 0.862232, -0.523029],
                                [0.0, -0.862232, -0.523029]],
                  'symbols': 'CHH',
                  'thermal correction': 2.3745},
    'CH2_s3B1d': {'CAS No.': 2465567,
                  'ZPE': 10.6953,
                  'charges': None,
                  'database': 'G2-1',
                  'description': 'Triplet methylene (CH2), C2v symm, 3-B1.',
                  'enthalpy': 93.7,
                  'ionization energy': 10.4,
                  'magmoms': [2.0, 0.0, 0.0],
                  'name': 'CH_2 (^3B_1)',
                  'positions': [[0.0, 0.0, 0.110381],
                                [0.0, 0.982622, -0.331142],
                                [0.0, -0.982622, -0.331142]],
                  'symbols': 'CHH',
                  'thermal correction': 2.3877},
    'CH3': {'CAS No.': 2229074,
            'ZPE': 18.3383,
            'charges': None,
            'database': 'G2-1',
            'description': 'Methyl radical (CH3), D3h symm.',
            'enthalpy': 35.0,
            'ionization energy': 9.84,
            'magmoms': [1.0, 0.0, 0.0, 0.0],
            'name': 'CH_3',
            'positions': [[0.0, 0.0, 0.0],
                          [0.0, 1.07841, 0.0],
                          [0.93393, -0.539205, 0.0],
                          [-0.93393, -0.539205, 0.0]],
            'symbols': 'CHHH',
            'thermal correction': 2.5383},
    'CH3Cl': {'CAS No.': 74873,
              'ZPE': 23.3013,
              'charges': None,
              'database': 'G2-1',
              'description': 'Methyl chloride (CH3Cl), C3v symm.',
              'enthalpy': -19.6,
              'ionization energy': 11.26,
              'magmoms': None,
              'name': 'CH_3Cl',
              'positions': [[0.0, 0.0, -1.121389],
                            [0.0, 0.0, 0.655951],
                            [0.0, 1.029318, -1.47428],
                            [0.891415, -0.514659, -1.47428],
                            [-0.891415, -0.514659, -1.47428]],
              'symbols': 'CClHHH',
              'thermal correction': 2.4956,
              'vertical ionization energy': 11.29},
    'CH3OH': {'CAS No.': 67561,
              'ZPE': 31.6635,
              'charges': None,
              'database': 'G2-1',
              'description': 'Methanol (CH3-OH), Cs symm.',
              'enthalpy': -48.0,
              'ionization energy': 10.84,
              'magmoms': None,
              'name': 'H_3COH',
              'positions': [[-0.047131, 0.664389, 0.0],
                            [-0.047131, -0.758551, 0.0],
                            [-1.092995, 0.969785, 0.0],
                            [0.878534, -1.048458, 0.0],
                            [0.437145, 1.080376, 0.891772],
                            [0.437145, 1.080376, -0.891772]],
              'symbols': 'COHHHH',
              'thermal correction': 2.6832,
              'vertical ionization energy': 10.96},
    'CH3SH': {'CAS No.': 74931,
              'ZPE': 28.3973,
              'charges': None,
              'database': 'G2-1',
              'description': 'Methanethiol (H3C-SH), Staggered, Cs symm.',
              'enthalpy': -5.5,
              'ionization energy': 9.44,
              'magmoms': None,
              'name': 'H_3CSH',
              'positions': [[-0.047953, 1.149519, 0.0],
                            [-0.047953, -0.664856, 0.0],
                            [1.283076, -0.823249, 0.0],
                            [-1.092601, 1.461428, 0.0],
                            [0.432249, 1.551207, 0.892259],
                            [0.432249, 1.551207, -0.892259]],
              'symbols': 'CSHHHH',
              'thermal correction': 2.869,
              'vertical ionization energy': 9.44},
    'CH4': {'CAS No.': 74828,
            'ZPE': 27.6744,
            'charges': None,
            'database': 'G2-1',
            'description': 'Methane (CH4), Td symm.',
            'enthalpy': -17.9,
            'ionization energy': 12.64,
            'magmoms': None,
            'name': 'CH_4',
            'positions': [[0.0, 0.0, 0.0],
                          [0.629118, 0.629118, 0.629118],
                          [-0.629118, -0.629118, 0.629118],
                          [0.629118, -0.629118, -0.629118],
                          [-0.629118, 0.629118, -0.629118]],
            'symbols': 'CHHHH',
            'thermal correction': 2.3939,
            'vertical ionization energy': 13.6},
    'CN': {'CAS No.': 2074875,
           'ZPE': 3.0183,
           'charges': None,
           'database': 'G2-1',
           'description': 'Cyano radical (CN), C*v symm, 2-Sigma+.',
           'enthalpy': 104.9,
           'ionization energy': 13.6,
           'magmoms': [1.0, 0.0],
           'name': 'CN (Cyano radical)',
           'positions': [[0.0, 0.0, -0.611046], [0.0, 0.0, 0.523753]],
           'symbols': 'CN',
           'thermal correction': 2.0739},
    'CO': {'CAS No.': 630080,
           'ZPE': 3.1062,
           'charges': None,
           'database': 'G2-1',
           'description': 'Carbon monoxide (CO), C*v symm.',
           'enthalpy': -26.4,
           'ionization energy': 14.01,
           'magmoms': None,
           'name': 'CO',
           'positions': [[0.0, 0.0, 0.493003], [0.0, 0.0, -0.657337]],
           'symbols': 'OC',
           'thermal correction': 2.0739,
           'vertical ionization energy': 14.01},
    'CO2': {'CAS No.': 124389,
            'ZPE': 7.313,
            'charges': None,
            'database': 'G2-1',
            'description': 'Carbon dioxide (CO2), D*h symm.',
            'enthalpy': -94.1,
            'ionization energy': 13.78,
            'magmoms': None,
            'name': 'CO_2',
            'positions': [[0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.178658],
                          [0.0, 0.0, -1.178658]],
            'symbols': 'COO',
            'thermal correction': 2.2321,
            'vertical ionization energy': 13.78},
    'CS': {'CAS No.': 2944050,
           'ZPE': 1.8242,
           'charges': None,
           'database': 'G2-1',
           'description': 'Carbon monosulfide (CS), C*v symm.',
           'enthalpy': 66.9,
           'ionization energy': 11.33,
           'magmoms': None,
           'name': 'SC',
           'positions': [[0.0, 0.0, -1.123382], [0.0, 0.0, 0.421268]],
           'symbols': 'CS',
           'thermal correction': 2.0814},
    'Cl': {'CAS No.': 22537151,
           'charges': None,
           'database': 'G2-1',
           'description': 'Cl atom',
           'enthalpy': 28.59,
           'ionization energy': 12.97,
           'magmoms': [1.0],
           'name': 'Chlorine',
           'positions': [[0.0, 0.0, 0.0]],
           'symbols': 'Cl',
           'thermal correction': 1.1},
    'Cl2': {'CAS No.': 7782505,
            'ZPE': 0.7737,
            'charges': None,
            'database': 'G2-1',
            'description': 'Cl2 molecule, D*h symm.',
            'enthalpy': 0.0,
            'ionization energy': 11.48,
            'magmoms': None,
            'name': 'Cl_2',
            'positions': [[0.0, 0.0, 1.007541], [0.0, 0.0, -1.007541]],
            'symbols': 'ClCl',
            'thermal correction': 2.1963,
            'vertical ionization energy': 11.49},
    'ClF': {'CAS No.': 7790898,
            'ZPE': 1.1113,
            'charges': None,
            'database': 'G2-1',
            'description': 'ClF molecule, C*v symm, 1-SG.',
            'enthalpy': -13.2,
            'ionization energy': 12.66,
            'magmoms': None,
            'name': 'FCl',
            'positions': [[0.0, 0.0, -1.084794], [0.0, 0.0, 0.574302]],
            'symbols': 'FCl',
            'thermal correction': 2.1273,
            'vertical ionization energy': 12.77},
    'ClO': {'CAS No.': 14989301,
            'ZPE': 1.1923,
            'charges': None,
            'database': 'G2-1',
            'description': 'ClO radical, C*v symm, 2-PI.',
            'enthalpy': 24.2,
            'ionization energy': 10.89,
            'magmoms': [1.0, 0.0],
            'name': 'ClO',
            'positions': [[0.0, 0.0, 0.514172], [0.0, 0.0, -1.092615]],
            'symbols': 'ClO',
            'thermal correction': 2.1172,
            'vertical ionization energy': 11.01},
    'F': {'CAS No.': 14762948,
          'charges': None,
          'database': 'G2-1',
          'description': 'F atom',
          'enthalpy': 18.47,
          'ionization energy': 17.42,
          'magmoms': [1.0],
          'name': 'Fluorine',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'F',
          'thermal correction': 1.05},
    'F2': {'CAS No.': 7782414,
           'ZPE': 1.5179,
           'charges': None,
           'database': 'G2-1',
           'description': 'F2 molecule, D*h symm.',
           'enthalpy': 0.0,
           'ionization energy': 15.7,
           'magmoms': None,
           'name': 'F_2',
           'positions': [[0.0, 0.0, 0.710304], [0.0, 0.0, -0.710304]],
           'symbols': 'FF',
           'thermal correction': 2.0915,
           'vertical ionization energy': 15.7},
    'H': {'CAS No.': 12385136,
          'charges': None,
          'database': 'G2-1',
          'description': 'H atom',
          'enthalpy': 51.63,
          'ionization energy': 13.6,
          'magmoms': [1.0],
          'name': 'Hydrogen',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'H',
          'thermal correction': 1.01},
    'H2CO': {'CAS No.': 50000,
             'ZPE': 16.4502,
             'charges': None,
             'database': 'G2-1',
             'description': 'Formaldehyde (H2C=O), C2v symm.',
             'enthalpy': -26.0,
             'ionization energy': 10.88,
             'magmoms': None,
             'name': 'H_2CO',
             'positions': [[0.0, 0.0, 0.683501],
                           [0.0, 0.0, -0.536614],
                           [0.0, 0.93439, -1.124164],
                           [0.0, -0.93439, -1.124164]],
             'symbols': 'OCHH',
             'thermal correction': 2.3927,
             'vertical ionization energy': 10.88},
    'H2O': {'CAS No.': 7732185,
            'ZPE': 13.2179,
            'charges': None,
            'database': 'G2-1',
            'description': 'Water (H2O), C2v symm.',
            'enthalpy': -57.8,
            'ionization energy': 12.62,
            'magmoms': None,
            'name': 'H_2O',
            'positions': [[0.0, 0.0, 0.119262],
                          [0.0, 0.763239, -0.477047],
                          [0.0, -0.763239, -0.477047]],
            'symbols': 'OHH',
            'thermal correction': 2.372},
    'H2O2': {'CAS No.': 7722841,
             'ZPE': 16.4081,
             'charges': None,
             'database': 'G2-1',
             'description': 'Hydrogen peroxide (HO-OH), C2 symm.',
             'enthalpy': -32.5,
             'ionization energy': 10.58,
             'magmoms': None,
             'name': 'HOOH',
             'positions': [[0.0, 0.734058, -0.05275],
                           [0.0, -0.734058, -0.05275],
                           [0.839547, 0.880752, 0.422001],
                           [-0.839547, -0.880752, 0.422001]],
             'symbols': 'OOHH',
             'thermal correction': 2.623,
             'vertical ionization energy': 11.7},
    'HCN': {'CAS No.': 74908,
            'ZPE': 10.2654,
            'charges': None,
            'database': 'G2-1',
            'description': 'Hydrogen cyanide (HCN), C*v symm.',
            'enthalpy': 31.5,
            'ionization energy': 13.6,
            'magmoms': None,
            'name': 'HCN',
            'positions': [[0.0, 0.0, -0.511747],
                          [0.0, 0.0, 0.664461],
                          [0.0, 0.0, -1.580746]],
            'symbols': 'CNH',
            'thermal correction': 2.1768,
            'vertical ionization energy': 13.61},
    'HCO': {'CAS No.': 2597446,
            'ZPE': 8.029,
            'charges': None,
            'database': 'G2-1',
            'description': 'HCO radical, Bent Cs symm.',
            'enthalpy': 10.0,
            'ionization energy': 8.12,
            'magmoms': [1.0, 0.0, 0.0],
            'name': 'HCO',
            'positions': [[0.06256, 0.593926, 0.0],
                          [0.06256, -0.596914, 0.0],
                          [-0.875835, 1.211755, 0.0]],
            'symbols': 'COH',
            'thermal correction': 2.3864,
            'vertical ionization energy': 9.31},
    'HCl': {'CAS No.': 7647010,
            'ZPE': 4.1673,
            'charges': None,
            'database': 'G2-1',
            'description': 'Hydrogen chloride (HCl), C*v symm.',
            'enthalpy': -22.1,
            'ionization energy': 12.74,
            'magmoms': None,
            'name': 'HCl',
            'positions': [[0.0, 0.0, 0.07111], [0.0, 0.0, -1.208868]],
            'symbols': 'ClH',
            'thermal correction': 2.0739},
    'HF': {'CAS No.': 7664393,
           'ZPE': 5.7994,
           'charges': None,
           'database': 'G2-1',
           'description': 'Hydrogen fluoride (HF), C*v symm.',
           'enthalpy': -65.1,
           'ionization energy': 16.03,
           'magmoms': None,
           'name': 'HF',
           'positions': [[0.0, 0.0, 0.093389], [0.0, 0.0, -0.840502]],
           'symbols': 'FH',
           'thermal correction': 2.0733,
           'vertical ionization energy': 16.12},
    'HOCl': {'CAS No.': 7790923,
             'ZPE': 8.1539,
             'charges': None,
             'database': 'G2-1',
             'description': 'HOCl molecule, Cs symm.',
             'enthalpy': -17.8,
             'ionization energy': 11.12,
             'magmoms': None,
             'name': 'HOCl (hypochlorous acid)',
             'positions': [[0.036702, 1.113517, 0.0],
                           [-0.917548, 1.328879, 0.0],
                           [0.036702, -0.602177, 0.0]],
             'symbols': 'OHCl',
             'thermal correction': 2.4416},
    'Li': {'CAS No.': 7439932,
           'charges': None,
           'database': 'G2-1',
           'description': 'Li atom',
           'enthalpy': 37.69,
           'ionization energy': 5.39,
           'magmoms': [1.0],
           'name': 'Lithium',
           'positions': [[0.0, 0.0, 0.0]],
           'symbols': 'Li',
           'thermal correction': 1.1},
    'Li2': {'CAS No.': 14452596,
            'ZPE': 0.4838,
            'charges': None,
            'database': 'G2-1',
            'description': 'Dilithium (Li2), D*h symm.',
            'enthalpy': 51.6,
            'ionization energy': 5.11,
            'magmoms': None,
            'name': 'Li_2',
            'positions': [[0.0, 0.0, 1.38653], [0.0, 0.0, -1.38653]],
            'symbols': 'LiLi',
            'thermal correction': 2.3086},
    'LiF': {'CAS No.': 7789244,
            'ZPE': 1.4019,
            'charges': None,
            'database': 'G2-1',
            'description': 'Lithium Fluoride (LiF), C*v symm.',
            'enthalpy': -80.1,
            'ionization energy': 11.3,
            'magmoms': None,
            'name': 'LiF',
            'positions': [[0.0, 0.0, -1.174965], [0.0, 0.0, 0.391655]],
            'symbols': 'LiF',
            'thermal correction': 2.099},
    'LiH': {'CAS No.': 7580678,
            'ZPE': 2.0149,
            'charges': None,
            'database': 'G2-1',
            'description': 'Lithium hydride (LiH), C*v symm.',
            'enthalpy': 33.3,
            'ionization energy': 7.9,
            'magmoms': None,
            'name': 'LiH',
            'positions': [[0.0, 0.0, 0.41], [0.0, 0.0, -1.23]],
            'symbols': 'LiH',
            'thermal correction': 2.0783},
    'N': {'CAS No.': 17778880,
          'charges': None,
          'database': 'G2-1',
          'description': 'N atom',
          'enthalpy': 112.53,
          'ionization energy': 14.53,
          'magmoms': [3.0],
          'name': 'Nitrogen',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'N',
          'thermal correction': 1.04},
    'N2': {'CAS No.': 7727379,
           'ZPE': 3.4243,
           'charges': None,
           'database': 'G2-1',
           'description': 'N2 molecule, D*h symm.',
           'enthalpy': 0.0,
           'ionization energy': 15.58,
           'magmoms': None,
           'name': 'N_2',
           'positions': [[0.0, 0.0, 0.56499], [0.0, 0.0, -0.56499]],
           'symbols': 'NN',
           'thermal correction': 2.0733,
           'vertical ionization energy': 15.58},
    'N2H4': {'CAS No.': 302012,
             'ZPE': 32.9706,
             'charges': None,
             'database': 'G2-1',
             'description': 'Hydrazine (H2N-NH2), C2 symm.',
             'enthalpy': 22.8,
             'ionization energy': 8.1,
             'magmoms': None,
             'name': 'H_2NNH_2',
             'positions': [[0.0, 0.718959, -0.077687],
                           [0.0, -0.718959, -0.077687],
                           [0.211082, 1.092752, 0.847887],
                           [-0.948214, 1.005026, -0.304078],
                           [-0.211082, -1.092752, 0.847887],
                           [0.948214, -1.005026, -0.304078]],
             'symbols': 'NNHHHH',
             'thermal correction': 2.6531,
             'vertical ionization energy': 8.98},
    'NH': {'CAS No.': 13774920,
           'ZPE': 4.5739,
           'charges': None,
           'database': 'G2-1',
           'description': 'NH, triplet, C*v symm.',
           'enthalpy': 85.2,
           'ionization energy': 13.1,
           'magmoms': [2.0, 0.0],
           'name': 'NH',
           'positions': [[0.0, 0.0, 0.129929], [0.0, 0.0, -0.909501]],
           'symbols': 'NH',
           'thermal correction': 2.0739,
           'vertical ionization energy': 13.49},
    'NH2': {'CAS No.': 13770406,
            'ZPE': 11.742,
            'charges': None,
            'database': 'G2-1',
            'description': 'NH2 radical, C2v symm, 2-B1.',
            'enthalpy': 45.1,
            'ionization energy': 10.78,
            'magmoms': [1.0, 0.0, 0.0],
            'name': 'NH_2',
            'positions': [[0.0, 0.0, 0.14169],
                          [0.0, 0.806442, -0.495913],
                          [0.0, -0.806442, -0.495913]],
            'symbols': 'NHH',
            'thermal correction': 2.3726,
            'vertical ionization energy': 12.0},
    'NH3': {'CAS No.': 7664417,
            'ZPE': 21.2462,
            'charges': None,
            'database': 'G2-1',
            'description': 'Ammonia (NH3), C3v symm.',
            'enthalpy': -11.0,
            'ionization energy': 10.07,
            'magmoms': None,
            'name': 'NH_3',
            'positions': [[0.0, 0.0, 0.116489],
                          [0.0, 0.939731, -0.271808],
                          [0.813831, -0.469865, -0.271808],
                          [-0.813831, -0.469865, -0.271808]],
            'symbols': 'NHHH',
            'thermal correction': 2.3896,
            'vertical ionization energy': 10.82},
    'NO': {'CAS No.': 10102439,
           'ZPE': 2.7974,
           'charges': None,
           'database': 'G2-1',
           'description': 'NO radical, C*v symm, 2-Pi.',
           'enthalpy': 21.6,
           'ionization energy': 9.26,
           'magmoms': [0.6, 0.4],
           'name': 'NO',
           'positions': [[0.0, 0.0, -0.609442], [0.0, 0.0, 0.533261]],
           'symbols': 'NO',
           'thermal correction': 2.0745,
           'vertical ionization energy': 9.26},
    'Na': {'CAS No.': 7440235,
           'charges': None,
           'database': 'G2-1',
           'description': 'Na atom',
           'enthalpy': 25.69,
           'ionization energy': 5.14,
           'magmoms': [1.0],
           'name': 'Sodium',
           'positions': [[0.0, 0.0, 0.0]],
           'symbols': 'Na',
           'thermal correction': 1.54},
    'Na2': {'CAS No.': 25681792,
            'ZPE': 0.2246,
            'charges': None,
            'database': 'G2-1',
            'description': 'Disodium (Na2), D*h symm.',
            'enthalpy': 34.0,
            'ionization energy': 4.89,
            'magmoms': None,
            'name': 'Na_2',
            'positions': [[0.0, 0.0, 1.576262], [0.0, 0.0, -1.576262]],
            'symbols': 'NaNa',
            'thermal correction': 2.4699},
    'NaCl': {'CAS No.': 7647145,
             'ZPE': 0.5152,
             'charges': None,
             'database': 'G2-1',
             'description': 'Sodium Chloride (NaCl), C*v symm.',
             'enthalpy': -43.6,
             'ionization energy': 9.2,
             'magmoms': None,
             'name': 'NaCl',
             'positions': [[0.0, 0.0, -1.45166], [0.0, 0.0, 0.93931]],
             'symbols': 'NaCl',
             'thermal correction': 2.2935,
             'vertical ionization energy': 9.8},
    'O': {'CAS No.': 17778802,
          'charges': None,
          'database': 'G2-1',
          'description': 'O atom',
          'enthalpy': 58.99,
          'ionization energy': 13.62,
          'magmoms': [2.0],
          'name': 'Oxygen',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'O',
          'thermal correction': 1.04},
    'O2': {'CAS No.': 7782447,
           'ZPE': 2.3444,
           'charges': None,
           'database': 'G2-1',
           'description': 'O2 molecule, D*h symm, Triplet.',
           'enthalpy': 0.0,
           'ionization energy': 12.07,
           'magmoms': [1.0, 1.0],
           'name': 'O_2',
           'positions': [[0.0, 0.0, 0.622978], [0.0, 0.0, -0.622978]],
           'symbols': 'OO',
           'thermal correction': 2.0752,
           'vertical ionization energy': 12.3},
    'OH': {'CAS No.': 3352576,
           'ZPE': 5.2039,
           'charges': None,
           'database': 'G2-1',
           'description': 'OH radical, C*v symm.',
           'enthalpy': 9.4,
           'ionization energy': 13.02,
           'magmoms': [0.5, 0.5],
           'name': 'OH',
           'positions': [[0.0, 0.0, 0.108786], [0.0, 0.0, -0.870284]],
           'symbols': 'OH',
           'thermal correction': 2.0739},
    'P': {'CAS No.': 7723140,
          'charges': None,
          'database': 'G2-1',
          'description': 'P atom',
          'enthalpy': 75.42,
          'ionization energy': 10.49,
          'magmoms': [3.0],
          'name': 'Phosphorus',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'P',
          'thermal correction': 1.28},
    'P2': {'CAS No.': 12185090,
           'ZPE': 1.1358,
           'charges': None,
           'database': 'G2-1',
           'description': 'P2 molecule, D*h symm.',
           'enthalpy': 34.3,
           'ionization energy': 10.53,
           'magmoms': None,
           'name': 'P_2',
           'positions': [[0.0, 0.0, 0.966144], [0.0, 0.0, -0.966144]],
           'symbols': 'PP',
           'thermal correction': 2.1235,
           'vertical ionization energy': 10.62},
    'PH2': {'CAS No.': 13765430,
            'ZPE': 8.2725,
            'charges': None,
            'database': 'G2-1',
            'description': 'PH2 radical, C2v symm.',
            'enthalpy': 33.1,
            'ionization energy': 9.82,
            'magmoms': [1.0, 0.0, 0.0],
            'name': 'PH_2 (Phosphino radical)',
            'positions': [[0.0, 0.0, 0.115396],
                          [0.0, 1.025642, -0.865468],
                          [0.0, -1.025642, -0.865468]],
            'symbols': 'PHH',
            'thermal correction': 2.3845},
    'PH3': {'CAS No.': 7803512,
            'ZPE': 14.7885,
            'charges': None,
            'database': 'G2-1',
            'description': 'Phosphine (PH3), C3v symm.',
            'enthalpy': 1.3,
            'ionization energy': 9.87,
            'magmoms': None,
            'name': 'PH_3',
            'positions': [[0.0, 0.0, 0.124619],
                          [0.0, 1.200647, -0.623095],
                          [1.039791, -0.600323, -0.623095],
                          [-1.039791, -0.600323, -0.623095]],
            'symbols': 'PHHH',
            'thermal correction': 2.4203,
            'vertical ionization energy': 10.95},
    'S': {'CAS No.': 7704349,
          'charges': None,
          'database': 'G2-1',
          'description': 'S atom',
          'enthalpy': 65.66,
          'ionization energy': 10.36,
          'magmoms': [2.0],
          'name': 'Sulfur',
          'positions': [[0.0, 0.0, 0.0]],
          'symbols': 'S',
          'thermal correction': 1.05},
    'S2': {'CAS No.': 23550450,
           'ZPE': 1.0078,
           'charges': None,
           'database': 'G2-1',
           'description': 'S2 molecule, D*h symm, triplet.',
           'enthalpy': 30.7,
           'ionization energy': 9.36,
           'magmoms': [1.0, 1.0],
           'name': 'S_2',
           'positions': [[0.0, 0.0, 0.960113], [0.0, 0.0, -0.960113]],
           'symbols': 'SS',
           'thermal correction': 2.1436,
           'vertical ionization energy': 9.55},
    'SH2': {'CAS No.': 7783064,
            'ZPE': 9.3129,
            'charges': None,
            'database': 'G2-1',
            'description': 'Hydrogen sulfide (H2S), C2v symm.',
            'enthalpy': -4.9,
            'ionization energy': 10.46,
            'magmoms': None,
            'name': 'SH_2',
            'positions': [[0.0, 0.0, 0.102135],
                          [0.0, 0.974269, -0.817083],
                          [0.0, -0.974269, -0.817083]],
            'symbols': 'SHH',
            'thermal correction': 2.3808,
            'vertical ionization energy': 10.5},
    'SO': {'CAS No.': 13827322,
           'ZPE': 1.6158,
           'charges': None,
           'database': 'G2-1',
           'description': 'Sulfur monoxide (SO), C*v symm, triplet.',
           'enthalpy': 1.2,
           'ionization energy': 11.29,
           'magmoms': [1.0, 1.0],
           'name': 'SO',
           'positions': [[0.0, 0.0, -1.015992], [0.0, 0.0, 0.507996]],
           'symbols': 'OS',
           'thermal correction': 2.0877},
    'SO2': {'CAS No.': 7446095,
            'ZPE': 4.3242,
            'charges': None,
            'database': 'G2-1',
            'description': 'Sulfur dioxide (SO2), C2v symm.',
            'enthalpy': -71.0,
            'ionization energy': 12.35,
            'magmoms': None,
            'name': 'SO_2',
            'positions': [[0.0, 0.0, 0.370268],
                          [0.0, 1.277617, -0.370268],
                          [0.0, -1.277617, -0.370268]],
            'symbols': 'SOO',
            'thermal correction': 2.5245,
            'vertical ionization energy': 12.5},
    'Si': {'CAS No.': 7440213,
           'charges': None,
           'database': 'G2-1',
           'description': 'Si atom',
           'enthalpy': 106.6,
           'ionization energy': 8.15,
           'magmoms': [2.0],
           'name': 'Silicon',
           'positions': [[0.0, 0.0, 0.0]],
           'symbols': 'Si',
           'thermal correction': 0.76},
    'Si2': {'CAS No.': 12597352,
            'ZPE': 0.7028,
            'charges': None,
            'database': 'G2-1',
            'description': 'Si2 molecule, D*h symm, Triplet (3-Sigma-G-).',
            'enthalpy': 139.9,
            'ionization energy': 7.9,
            'magmoms': [1.0, 1.0],
            'name': 'Si_2 (Silicon diatomic)',
            'positions': [[0.0, 0.0, 1.130054], [0.0, 0.0, -1.130054]],
            'symbols': 'SiSi',
            'thermal correction': 2.2182},
    'Si2H6': {'CAS No.': 1590870,
              'ZPE': 30.2265,
              'charges': None,
              'database': 'G2-1',
              'description': 'Disilane (H3Si-SiH3), D3d symm.',
              'enthalpy': 19.1,
              'ionization energy': 9.74,
              'magmoms': None,
              'name': 'Si_2H_6',
              'positions': [[0.0, 0.0, 1.167683],
                            [0.0, 0.0, -1.167683],
                            [0.0, 1.393286, 1.68602],
                            [-1.206621, -0.696643, 1.68602],
                            [1.206621, -0.696643, 1.68602],
                            [0.0, -1.393286, -1.68602],
                            [-1.206621, 0.696643, -1.68602],
                            [1.206621, 0.696643, -1.68602]],
              'symbols': 'SiSiHHHHHH',
              'thermal correction': 3.7927,
              'vertical ionization energy': 10.53},
    'SiH2_s1A1d': {'CAS No.': 13825906,
                   'ZPE': 7.1875,
                   'charges': None,
                   'database': 'G2-1',
                   'description': 'Singlet silylene (SiH2), C2v symm, 1-A1.',
                   'enthalpy': 65.2,
                   'ionization energy': 8.92,
                   'magmoms': None,
                   'name': 'SiH_2 (^1A_1)(silicon dihydride)',
                   'positions': [[0.0, 0.0, 0.131272],
                                 [0.0, 1.096938, -0.918905],
                                 [0.0, -1.096938, -0.918905]],
                   'symbols': 'SiHH',
                   'thermal correction': 2.3927},
    'SiH2_s3B1d': {'CAS No.': 13825906,
                   'ZPE': 7.4203,
                   'charges': None,
                   'database': 'G2-1',
                   'description': 'Triplet silylene (SiH2), C2v symm, 3-B1.',
                   'enthalpy': 86.2,
                   'magmoms': [2.0, 0.0, 0.0],
                   'name': 'SiH_2 (^3B_1)(silicon dihydride)',
                   'positions': [[0.0, 0.0, 0.094869],
                                 [0.0, 1.271862, -0.664083],
                                 [0.0, -1.271862, -0.664083]],
                   'symbols': 'SiHH',
                   'thermal correction': 2.4078},
    'SiH3': {'CAS No.': 13765441,
             'ZPE': 13.0898,
             'charges': None,
             'database': 'G2-1',
             'description': 'Silyl radical (SiH3), C3v symm.',
             'enthalpy': 47.9,
             'ionization energy': 8.14,
             'magmoms': [1.0, 0.0, 0.0, 0.0],
             'name': 'SiH_3',
             'positions': [[0.0, 0.0, 0.079299],
                           [0.0, 1.41328, -0.370061],
                           [1.223937, -0.70664, -0.370061],
                           [-1.223937, -0.70664, -0.370061]],
             'symbols': 'SiHHH',
             'thermal correction': 2.4912,
             'vertical ionization energy': 8.74},
    'SiH4': {'CAS No.': 7803625,
             'ZPE': 19.2664,
             'charges': None,
             'database': 'G2-1',
             'description': 'Silane (SiH4), Td symm.',
             'enthalpy': 8.2,
             'ionization energy': 11.0,
             'magmoms': None,
             'name': 'SiH_4',
             'positions': [[0.0, 0.0, 0.0],
                           [0.856135, 0.856135, 0.856135],
                           [-0.856135, -0.856135, 0.856135],
                           [-0.856135, 0.856135, -0.856135],
                           [0.856135, -0.856135, -0.856135]],
             'symbols': 'SiHHHH',
             'thermal correction': 2.5232,
             'vertical ionization energy': 12.3},
    'SiO': {'CAS No.': 10097286,
            'ZPE': 1.7859,
            'charges': None,
            'database': 'G2-1',
            'description': 'Silicon monoxide (SiO), C*v symm.',
            'enthalpy': -24.6,
            'ionization energy': 11.49,
            'magmoms': None,
            'name': 'SiO',
            'positions': [[0.0, 0.0, 0.560846], [0.0, 0.0, -0.98148]],
            'symbols': 'SiO',
            'thermal correction': 2.0821}}


def get_ionization_energy(name, vertical=True):
    """Return the experimental ionization energy from the database.

    If vertical is True, the vertical ionization energy is returned if
    available.
    """
    if name not in data:
        raise KeyError(f'System {name} not in database.')
    elif 'ionization energy' not in data[name]:
        raise KeyError(f'No data on ionization energy for system {name}.')
    else:
        if vertical and 'vertical ionization energy' in data[name]:
            return data[name]['vertical ionization energy']
        else:
            return data[name]['ionization energy']


def get_atomization_energy(name):
    """Determine extrapolated experimental atomization energy from the database.

    The atomization energy is extrapolated from experimental heats of
    formation at room temperature, using calculated zero-point energies
    and thermal corrections.

    The atomization energy is returned in kcal/mol = 43.36 meV:

    >>> from ase.units import *; print kcal / mol
    0.0433641146392

    """
    d = data[name]
    e = d['enthalpy']
    z = d['ZPE']
    dh = d['thermal correction']
    ae = -e + z + dh
    for a in string2symbols(d['symbols']):
        h = data[a]['enthalpy']
        dh = data[a]['thermal correction']
        ae += h - dh
    return ae
