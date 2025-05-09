# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- https://www.mdanalysis.org
# Copyright (c) 2006-2020 The MDAnalysis Development Team and contributors
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

"""HOLE Analysis --- :mod:`MDAnalysis.analysis.hole2`
=====================================================================================

:Author: Lily Wang
:Year: 2020
:Copyright: Lesser GNU Public License v2.1+

.. versionadded:: 1.0.0

This module contains the tools to interface with HOLE_
:footcite:p:`Smart1993,Smart1996` to analyse an ion channel pore or transporter
pathway :footcite:p:`Stelzl2014`.

"""
import warnings

try:
    from mdahole2.analysis.hole import hole, HoleAnalysis
    from mdahole2.analysis import utils, templates
    from mdahole2.analysis.utils import create_vmd_surface
except ImportError:
    wmsg = (
        "Please install the mdahole2 mdakit to use it in MDAnalysis.\n"
        "More details can be found here: "
        "https://www.mdanalysis.org/mdahole2/getting_started.html"
    )
    warnings.warn(wmsg, category=UserWarning)
else:
    wmsg = (
        "Deprecated in version 2.8.0\n"
        "MDAnalysis.analysis.hole2 is deprecated in favour of the "
        "MDAKit madahole2 (https://www.mdanalysis.org/mdahole2/) "
        "and will be removed in MDAnalysis version 3.0.0"
    )
    warnings.warn(wmsg, category=DeprecationWarning)
