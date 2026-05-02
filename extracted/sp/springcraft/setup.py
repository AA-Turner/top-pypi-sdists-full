# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['springcraft']

package_data = \
{'': ['*'], 'springcraft': ['data/*']}

install_requires = \
['biotite>=0.32', 'numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'springcraft',
    'version': '0.3.0',
    'description': 'Investigate molecular dynamics with elastic network models',
    'long_description': 'Springcraft\n===========\n\n*Springcraft* is a *Biotite* extension package, that allows the analysis\nof `AtomArray` objects via *Elastic Network Models* (ENMs).\nAn ENM can be thought of as a system that connects residues via springs:\nInteraction of nearby residues is governed by a harmonic potential, with the\nnative (input) conformation representing the energy minimum.\nNormal mode analysis allows the researcher to investigate global\nfunctional movements of a protein in a fast coarse-grained manner.\n\n.. note::\n\n  *Springcraft* is still in alpha stage.\n  Although most implemented functionalities should already work as\n  expected, some features are not well tested, yet.\n\nInstallation\n------------\n\n*Springcraft* can be installed via\n\n.. code-block:: console\n\n   $ pip install springcraft\n\nor \n\n.. code-block:: console\n\n   $ conda install -c conda-forge springcraft\n\nYou can also install *Springcraft* from source.\nThe package uses `Poetry <https://python-poetry.org/>`_ for building\ndistributions.\nVia :pep:`517` it is possible to install the package from local source code\nvia *pip*:\n\n.. code-block:: console\n\n   $ git clone https://github.com/biotite-dev/springcraft.git\n   $ pip install ./springcraft\n\nExample\n=======\n\n.. code-block:: python\n\n   import numpy as np\n   import biotite.structure.io.pdbx as pdbx\n   import springcraft\n\n\n   pdbx_file = pdbx.PDBxFile.read("path/to/1l2y.cif")\n   atoms = pdbx.get_structure(pdbx_file, model=1)\n   ca = atoms[(atoms.atom_name == "CA") & (atoms.element == "C")]\n   ff = springcraft.InvariantForceField(cutoff_distance=7.0)\n   gnm = springcraft.GNM(ca, ff)\n   kirchhoff = gnm.kirchhoff\n\n   np.set_printoptions(linewidth=100)\n   print(kirchhoff)\n\nOutput:\n\n.. code-block:: none\n\n   [[ 4. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n    [-1.  6. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1.  0.]\n    [-1. -1.  7. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1.  0.]\n    [-1. -1. -1.  7. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n    [-1. -1. -1. -1.  8. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n    [ 0. -1. -1. -1. -1.  9. -1. -1. -1.  0. -1.  0.  0.  0.  0.  0.  0. -1.  0.  0.]\n    [ 0.  0. -1. -1. -1. -1.  8. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0. -1. -1. -1. -1.  7. -1. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0. -1. -1. -1. -1.  7. -1. -1.  0.  0. -1.  0.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0. -1. -1. -1.  7. -1. -1. -1. -1.  0.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0. -1. -1. -1. -1. -1.  8. -1. -1. -1.  0.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1.  7. -1. -1. -1. -1. -1.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1. -1.  5. -1. -1.  0.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0. -1. -1. -1. -1. -1.  7. -1. -1.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1. -1.  4. -1.  0.  0.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1.  0. -1. -1.  5. -1. -1.  0.  0.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1.  0.  0.  0. -1.  4. -1. -1.  0.]\n    [ 0.  0.  0.  0.  0. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1.  5. -1. -1.]\n    [ 0. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1.  5. -1.]\n    [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1. -1.  2.]]',
    'author': 'Patrick Kunzmann',
    'author_email': 'padix.key@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://springcraft.biotite-python.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
