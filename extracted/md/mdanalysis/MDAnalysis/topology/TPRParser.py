# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- https://www.mdanalysis.org
# Copyright (c) 2006-2017 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the Lesser GNU Public Licence, v2.1 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,
# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.
# MDAnalysis: A Python package for the rapid analysis of molecular dynamics
# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th
# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.
# doi: 10.25080/majora-629e541a-00e
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#

# TPR parser and tpr support module
# Copyright (c) 2011 Zhuyi Xue
# Released under the  GNU Public Licence, v2


"""Gromacs portable run input TPR format parser
============================================

The :mod:`~MDAnalysis.topology.TPRParser` module allows reading of a
Gromacs_ portable run input file (a `TPR file`_). Because
the file format of the TPR file is changing rapidly, not all versions
are currently supported. The known working versions and the
approximate Gromacs release numbers are listed in the table
:ref:`TPR format versions <TPR-format-table>`.

.. _`TPR-format-table`:

.. table:: TPR format versions and generations read by :func:`MDAnalysis.topology.TPRParser.parse`.

   ========== ============== ==================== =====
   TPX format TPX generation Gromacs release      read
   ========== ============== ==================== =====
   ??         ??             3.3, 3.3.1           no

   58         17             4.0, 4.0.2, 4.0.3,   yes
                             4.0.4, 4.0.5, 4.0.6,
                             4.0.7

   73         23             4.5.0, 4.5.1, 4.5.2, yes
                             4.5.3, 4.5.4, 4.5.5

   83         24             4.6, 4.6.1           yes

   100        26             5.0, 5.0.1, 5.0.2,   yes
                             5.0.3,5.0.4, 5.0.5

   103        26             5.1                  yes

   110        26             2016                 yes
   112        26             2018                 yes
   116        26             2019                 yes
   119        27             2020[*]_             yes
   122        28             2021                 yes
   127        28             2022                 yes
   129        28             2023                 yes
   133        28             2024.1               yes
   134        28             2024.4               yes
   137        28             2025.0               yes
   ========== ============== ==================== =====

.. [*] Files generated by the beta versions of Gromacs 2020 are NOT supported.
   See `Issue 2428`_ for more details.

For further discussion and notes see `Issue 2`_. Please *open a new issue* in
the `Issue Tracker`_ when a new or different TPR file format version should be
supported.

Bonded interactions available in Gromacs are described in table 5.5 of the
`Gromacs manual`_. The following ones are used to build the topology (see
`Issue 463`_):

* bonds: regular bonds (type 1), G96 bonds (type 2), Morse (type 3),
  cubic bonds (type 4), connections (type 5), harmonic potentials (type 6),
  FENE bonds (type 7), restraint potentials (type 10),
  tabulated potential with exclusion/connection (type 8),
  tabulated potential without exclusion/connection (type 9), constraints with
  exclusion/connection (type 1), constraints without exclusion/connection (type
  2), SETTLE constraints
* angles: regular angles (type 1), G96 angles (type 2), cross bond-bond
  (type3), cross-bond-angle (type 4), Urey-Bradley (type 5), quartic angles
  (type 6), restricted bending potential (type 10), tabulated angles (type 8)
* dihedrals: proper dihedrals (type 1 and type 9), Ryckaert-Bellemans dihedrals
  (type 3), Fourier dihedrals (type 5), restricted dihedrals (type 10),
  combined bending-torsion potentials (type 11), tabulated dihedral (type 8)
* impropers: improper dihedrals (type 2), periodic improper dihedrals (type 4)


Classes
-------

.. autoclass:: TPRParser
   :members:
   :inherited-members:

See Also
--------
:mod:`MDAnalysis.topology.tpr`


Development notes
-----------------

The TPR reader is a pure-python implementation of a basic TPR
parser. Currently the following sections of the topology are parsed:

* Atoms: number, name, type, resname, resid, segid, chainID, mass, charge, element
  [residue, segment, radius, bfactor, resnum, moltype]
* Bonds
* Angles
* Dihedrals
* Impropers

This tpr parser is written according to the following files

- :file:`{gromacs_dir}/src/kernel/gmxdump.c`
- :file:`{gromacs_dir}/src/gmxlib/tpxio.c` (the most important one)
- :file:`{gromacs_dir}/src/gmxlib/gmxfio_rw.c`
- :file:`{gromacs_dir}/src/gmxlib/gmxfio_xdr.c`
- :file:`{gromacs_dir}/include/gmxfiofio.h`

or their equivalent in more recent versions of Gromacs.

The function :func:`read_tpxheader` is based on the
`TPRReaderDevelopment`_ notes.  Functions with names starting with
``read_`` or ``do_`` are trying to be similar to those in
:file:`gmxdump.c` or :file:`tpxio.c`, those with ``extract_`` are new.

Versions prior to Gromacs 4.0.x are not supported.

.. Links
.. _Gromacs: http://www.gromacs.org
.. _`Gromacs manual`: http://manual.gromacs.org/documentation/5.1/manual-5.1.pdf
.. _TPR file: http://manual.gromacs.org/current/online/tpr.html
.. _`Issue Tracker`: https://github.com/MDAnalysis/mdanalysis/issues
.. _`Issue 2`: https://github.com/MDAnalysis/mdanalysis/issues/2
.. _`Issue 463`: https://github.com/MDAnalysis/mdanalysis/pull/463
.. _TPRReaderDevelopment: https://github.com/MDAnalysis/mdanalysis/wiki/TPRReaderDevelopment
.. _`Issue 2428`: https://github.com/MDAnalysis/mdanalysis/issues/2428


.. versionchanged:: 2.0.0
   The `elements` topology attribute is now exposed if at least one atom has
   a valid element symbol. In that case, atoms for which the element is not
   recognized have their element attribute set to an empty string. If none of
   the elements are recognized, then the `elements` attribute is not set in the
   topology.

.. versionchanged:: 2.7.0
   If the TPR molblock is named "Protein_chain_XXX" then we assume that XXX is 
   describing the chain of a protein (in the sense of the PDB chainID) and set
   the topology attribute `chainID` to "XXX". In all other cases, the chainID
   remains the full molblock name. The `segID` is never changed.
"""
__author__ = "Zhuyi Xue"
__copyright__ = "GNU Public Licence, v2"


from ..lib.util import openany
from .tpr import utils as tpr_utils
from .tpr import setting as S
from .base import TopologyReaderBase
from ..core.topologyattrs import Resnums

import logging

logger = logging.getLogger("MDAnalysis.topology.TPRparser")


class TPRParser(TopologyReaderBase):
    """Read topology information from a Gromacs_ `TPR file`_.

    .. _Gromacs: http://www.gromacs.org
    .. _TPR file: http://manual.gromacs.org/current/online/tpr.html
    """

    format = "TPR"

    def parse(self, tpr_resid_from_one=True, **kwargs):
        """Parse a Gromacs TPR file into a MDAnalysis internal topology structure.

        Parameters
        ----------
        tpr_resid_from_one: bool (optional)
            Toggle whether to index resids from 1 or 0 from TPR files.
            TPR files index resids from 0 by default, even though GRO and ITP
            files index from 1.

        Returns
        -------
        structure : dict


        .. versionchanged:: 1.1.0
            Added the ``tpr_resid_from_one`` keyword to control if
            resids are indexed from 0 or 1. Default ``False``.
        .. versionchanged:: 2.0.0
            Changed to ``tpr_resid_from_one=True`` by default.
        """
        with openany(self.filename, mode="rb") as infile:
            tprf = infile.read()
        data = tpr_utils.TPXUnpacker(tprf)
        try:
            th = tpr_utils.read_tpxheader(data)  # tpxheader
        except (EOFError, ValueError):
            msg = f"{self.filename}: Invalid tpr file or cannot be recognized"
            logger.critical(msg)
            raise IOError(msg)

        self._log_header(th)

        # Starting with gromacs 2020 (tpx version 119), the body of the file
        # is encoded differently. We change the unpacker accordingly.
        if th.fver >= S.tpxv_AddSizeField and th.fgen >= 27:
            actual_body_size = len(data.get_buffer()) - data.get_position()
            if actual_body_size == 4 * th.sizeOfTprBody:
                # See issue #2428.
                msg = (
                    "TPR files produced with beta versions of gromacs 2020 "
                    "are not supported."
                )
                logger.critical(msg)
                raise IOError(msg)
            data = tpr_utils.TPXUnpacker2020.from_unpacker(data)

        state_ngtc = th.ngtc  # done init_state() in src/gmxlib/tpxio.c
        if th.bBox:
            tpr_utils.extract_box_info(data, th.fver)

        if state_ngtc > 0:
            if th.fver < 69:  # redundancy due to  different versions
                tpr_utils.ndo_real(data, state_ngtc)
            tpr_utils.ndo_real(
                data, state_ngtc
            )  # relevant to Berendsen tcoupl_lambda

        if th.bTop:
            tpr_top = tpr_utils.do_mtop(
                data, th.fver, tpr_resid_from_one=tpr_resid_from_one
            )
        else:
            msg = f"{self.filename}: No topology found in tpr file"
            logger.critical(msg)
            raise IOError(msg)

        tpr_top.add_TopologyAttr(Resnums(tpr_top.resids.values.copy()))

        return tpr_top

    def _log_header(self, th):
        logger.info(f"Gromacs version   : {th.ver_str}")
        logger.info(f"tpx version       : {th.fver}")
        logger.info(f"tpx generation    : {th.fgen}")
        logger.info(f"tpx precision     : {th.precision}")
        logger.info(f"tpx file_tag      : {th.file_tag}")
        logger.info(f"tpx natoms        : {th.natoms}")
        logger.info(f"tpx ngtc          : {th.ngtc}")
        logger.info(f"tpx fep_state     : {th.fep_state}")
        logger.info(f"tpx lambda        : {th.lamb}")
        logger.debug(f"tpx bIr (input record): {th.bIr}")
        logger.debug(f"tpx bTop         : {th.bTop}")
        logger.debug(f"tpx bX           : {th.bX}")
        logger.debug(f"tpx bV           : {th.bV}")
        logger.debug(f"tpx bF           : {th.bF}")
        logger.debug(f"tpx bBox         : {th.bBox}")
