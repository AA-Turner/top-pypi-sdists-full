
# -*- coding: utf-8 -*-

u'''A pure Python implementation of geodesy tools for various ellipsoidal and spherical earth models
using precision exact, elliptic, trigonometric, vector-based, iterative and approximate methods for
geodetic (lat-/longitude), geocentric (U{ECEF<https://WikiPedia.org/wiki/ECEF>} cartesian), local (U{LTP
<https://WikiPedia.org/wiki/Local_tangent_plane_coordinates>}) and certain U{triaxial ellipsoidal
<https://GeographicLib.SourceForge.io/1.44/triaxial.html>} coordinates.

Transcoded in part from U{JavaScript originals<https://GitHub.com/ChrisVeness/geodesy>} by I{Chris Veness (C)
2005-2024} and from several U{C++ classes<https://GeographicLib.SourceForge.io/C++/doc/annotated.html>} by I{Charles
F. F. Karney (C) 2008-2024} and published under the same U{MIT License<https://OpenSource.org/licenses/MIT>}**.

There are four modules for ellipsoidal earth models, C{ellipsoidalExact}, C{-Karney}, C{-Vincenty} and C{-Nvector}
and two for spherical ones, C{sphericalTrigonometry} and C{-Nvector}.  Each module provides a geodetic B{C{LatLon}}
and a geocentric B{C{Cartesian}} class with methods and functions to compute distance, surface area, perimeter,
forward and reverse azimuth, initial and final bearing, intermediate and nearest points, intersections of geodesic,
great circle and rhumb lines, circle intersections and secants, U{3-point resections
<https://WikiPedia.org/wiki/Position_resection_and_intersection>}, triangulation, trilateration (by intersection,
by overlap and in 3-D), conversions and unrolling, among other things.

Also included are modules for conversions to and from U{Cassini-Soldner
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1CassiniSoldner.html>},
U{ECEF<https://WikiPedia.org/wiki/ECEF>} (Earth-Centered, Earth-Fixed cartesian), U{UTM
<https://www.Movable-Type.co.UK/scripts/latlong-utm-mgrs.html>} (Universal Transverse Mercator
and U{Exact<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1TransverseMercatorExact.html>}),
U{UPS<https://WikiPedia.org/wiki/Universal_polar_stereographic_coordinate_system>} (Universal Polar
Stereographic) and U{Web Mercator<https://WikiPedia.org/wiki/Web_Mercator>} (Pseudo-Mercator) coordinates,
U{MGRS<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1MGRS.html>} (Military Grid Reference
System, UTM I{and} UPS) and U{OSGR<https://www.Movable-Type.co.UK/scripts/latlong-os-gridref.html>} (British
Ordinance Survery Grid Reference) grid references, U{TRF<http://ITRF.ENSG.IGN.Fr>} (Terrestrial Reference
Frames) and modules to encode and decode U{EPSG<https://EPSG.org>}, U{Geohashes
<https://www.Movable-Type.co.UK/scripts/geohash.html>}, U{Georefs (WGRS)
<https://WikiPedia.org/wiki/World_Geographic_Reference_System>} and U{Garefs (GARS)
<https://WikiPedia.org/wiki/Global_Area_Reference_System>}.

Other modules provide U{Albers equal-area
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AlbersEqualArea.html>} projections, U{equidistant
<https://GeographicLib.SourceForge.io/C++/doc/classGeographicLib_1_1AzimuthalEquidistant.html>} and other I{azimuthal}
projections, Lambert I{conformal conic} projections and positions, functions to clip paths or polygons of C{LatLon}
points using the U{Cohen-Sutherland<https://WikiPedia.org/wiki/Cohen-Sutherland_algorithm>},
U{Forster-Hormann-Popa<https://www.ScienceDirect.com/science/article/pii/S259014861930007X>},
U{Greiner-Hormann<http://www.inf.USI.CH/hormann/papers/Greiner.1998.ECO.pdf>},
U{Liang-Barsky<https://www.CS.Helsinki.FI/group/goa/viewing/leikkaus/intro.html>} and
U{Sutherland-Hodgman<https://WikiPedia.org/wiki/Sutherland-Hodgman_algorithm>} methods,
functions to U{simplify<https://Bost.Ocks.org/mike/simplify>} or linearize a path of C{LatLon}
points (or a U{NumPy array<https://docs.SciPy.org/doc/numpy/reference/generated/numpy.array.html>}),
including implementations of the U{Ramer-Douglas-Peucker<https://WikiPedia.org/wiki/
Ramer-Douglas-Peucker_algorithm>}, the U{Visvalingam-Whyatt<https://hydra.Hull.ac.UK/
resources/hull:8338>} and the U{Reumann-Witkam<https://psimpl.SourceForge.net/reumann-witkam.html>}
algorithms and modified versions of the former.

Plus modules and classes to U{interpolate<https://docs.SciPy.org/doc/scipy/reference/interpolate.html>} the
L{height<pygeodesy.heights>} of C{LatLon} points and L{Geoid<pygeodesy.geoids>} models, compute various U{Fréchet
<https://WikiPedia.org/wiki/Frechet_distance>} or U{Hausdorff<https://WikiPedia.org/wiki/Hausdorff_distance>}
distances or perform I{boolean} operations between (composite) polygons.

For further details see the U{documentation<https://mrJean1.GitHub.io/PyGeodesy>}, the descriptions of
U{Latitude/Longitude<https://www.Movable-Type.co.UK/scripts/latlong.html>}, U{Vincenty
<https://www.Movable-Type.co.UK/scripts/latlong-vincenty.html>} and U{Vector-based
<https://www.Movable-Type.co.UK/scripts/latlong-vectors.html>} geodesy, the original U{JavaScript source
<https://GitHub.com/ChrisVeness/geodesy>} or U{docs<https://www.Movable-Type.co.UK/scripts/geodesy/docs>}
and I{Karney}'s Python U{geographiclib<https://PyPI.org/project/geographiclib>} and C++ U{GeographicLib
<https://GeographicLib.SourceForge.io/C++/doc/index.html>}.

Installation
============

To install C{pygeodesy}, type C{python[3] -m pip install pygeodesy} or C{python[3] -m easy_install
pygeodesy} in a terminal or command window.

If the wheel C{pygeodesy-yy.m.d-py2.py3-none-any.whl} is missing in U{PyPI Download files<https://
PyPI.org/project/pygeodesy/#files>}, download the file from U{GitHub/dist<https://GitHub.com/mrJean1/
PyGeodesy/tree/master/dist>}.  Install that with C{python[3] -m pip install <path-to-downloaded-wheel>}
and verify with C{python[3] -m pygeodesy}.

Alternatively, download C{pygeodesy-yy.m.d.tar.gz} from U{PyPI<https://PyPI.org/project/pygeodesy>}
or U{GitHub<https://GitHub.com/mrJean1/PyGeodesy>}, C{unzip} the downloaded file, C{cd} to
directory C{pygeodesy-yy.m.d} and type C{python[3] setup.py install}.

To run all C{pygeodesy} tests, type C{python[3] test/run.py} or type C{python[3] test/unitTestSuite.py}
before or after installation.

Dependencies
============

Installation of I{Karney}'s Python package U{geographiclib<https://PyPI.org/project/geographiclib>}
is optional, but required for module L{ellipsoidalKarney}, L{azimuthal} classes L{EquidistantKarney}
and L{GnomonicKarney} and the L{HeightIDWkarney} interpolator.

Both U{numpy<https://PyPI.org/project/numpy>} and U{scipy<https://PyPI.org/project/scipy>} must be
installed for most L{Geoid...<pygeodesy.geoids>} and L{Height...<pygeodesy.heights>} interpolators,
except L{GeoidKarney} and the L{HeightIDW...<pygeodesy.heights>} ones.

Functions and C{LatLon} methods L{circin6}, L{circum3}, L{circum4_} and L{soddy4} and functions
L{triaxum5} and L{trilaterate3d2} require U{numpy<https://PyPI.org/project/numpy>} to be installed,
modules L{auxilats} and L{rhumb} may need U{numpy<https://PyPI.org/project/numpy>}.

Modules L{ellipsoidalGeodSolve} and L{geodsolve} and L{azimuthal} classes L{EquidistantGeodSolve}
and L{GnomonicGeodSolve} depend on I{Karney}'s C++ utility U{GeodSolve
<https://GeographicLib.SourceForge.io/C++/doc/GeodSolve.1.html>} to be executable and set with
env variable C{PYGEODESY_GEODSOLVE} or with property L{Ellipsoid.geodsolve}.

Class L{Intersectool} in module L{geodesici} needs I{Karney}'s C++ utility U{IntersectTool
<https://GeographicLib.SourceForge.io/C++/doc/IntersectTool.1.html>} to be executable and set with
env variable C{PYGEODESY_INTERSECTTOOL}.

To compare C{MGRS} results from modules L{mgrs} and C{testMgrs} with I{Karney}'s C++ utility
U{GeoConvert<https://GeographicLib.SourceForge.io/C++/doc/GeoConvert.1.html>}, the latter must
be executable and set with env variable C{PYGEODESY_GEOCONVERT}.

Module L{rhumb.solve} needs I{Karney}'s C++ utility U{RhumbSolve
<https://GeographicLib.SourceForge.io/C++/doc/RhumbSolve.1.html>} to be executable and set with
env variable C{PYGEODESY_RHUMBSOLVE} or with property L{Ellipsoid.rhumbsolve}.

Documentation
=============

In addition to the C{pygeodesy} package, the U{pygeodesy<https://PyPI.org/project/pygeodesy>}
U{distribution files<https://GitHub.com/mrJean1/PyGeodesy/tree/master/dist>} contain the tests,
the test results (on macOS only) and the complete U{documentation<https://mrJean1.GitHub.io/PyGeodesy>}
(generated by U{Epydoc<https://PyPI.org/project/epydoc>} using command line:
C{epydoc --html --no-private --no-source --name=pygeodesy --url=... -v pygeodesy}).

Tests
=====

The tests ran with Python 3.13.3 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0),
Python 3.12.7 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0,
U{numpy<https://PyPI.org/project/numpy>} 2.1.0, U{scipy<https://PyPI.org/project/scipy>} 1.14.1,
U{GeodSolve<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3,
U{IntersectTool<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3 and
U{RhumbSolve<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3),
Python 3.11.5 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0,
U{numpy<https://PyPI.org/project/numpy>} 1.24.2 and U{scipy<https://PyPI.org/project/scipy>} 1.10.1),
Python 3.10.8 (with U{geographiclib <https://PyPI.org/project/geographiclib>} 2.0,
U{numpy<https://PyPI.org/project/numpy>} 1.23.3, U{scipy<https://PyPI.org/project/scipy>} 1.9.1,
U{GeoConvert<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3,
U{GeodSolve<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3) and
Python 2.7.18 (with U{geographiclib<https://PyPI.org/project/geographiclib>} 1.50,
U{numpy<https://PyPI.org/project/numpy>} 1.16.6, U{scipy<https://PyPI.org/project/scipy>} 1.2.2,
U{GeoConvert<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3,
U{GeodSolve<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3,
U{IntersectTool<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3 and
U{RhumbSolve<https://GeographicLib.SourceForge.io/C++/doc/utilities.html>} 2.3), all in 64-bit on
macOS 15.4.1 Sequoia.

All tests ran with and without C{lazy import} for Python 3 and with command line option C{-W default} and
env variable C{PYGEODESY_WARNINGS=on} for all Python versions.  The results of those tests are included in
the distribution files.

Test coverage has been measured with U{coverage<https://PyPI.org/project/coverage>} 7.6.1 using Python
3.13.3, 3.12.7, 3.11.5 and 3.10.8.  The complete coverage report in HTML and a PDF summary are included in
the distribution files.

Python 3.13.3, 3.12.7, 3.11.5 and 3.10.8 run on Apple M4 Si (C{arm64}), I{natively}.  Python 2.7.18 runs
on Intel (C{x86_64}) or Intel I{emulation} ("C{arm64_x86_64}", see function L{machine<pygeodesy.machine>}).

The tests also ran with Python 3.13.3 (and U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0) on
U{Debian 12<https://Cirrus-CI.com/github/mrJean1/PyGeodesy/master>} in 64-bit only, with Python 3.12.5 (and
U{geographiclib<https://PyPI.org/project/geographiclib>} 2.0) on U{Windows 2019Server
<https://CI.AppVeyor.com/project/mrJean1/pygeodesy>} in 64-bit only and with Python 2.7.18 (and U{geographiclib
<https://PyPI.org/project/geographiclib>} 1.52) on U{Windows 10<https://CI.AppVeyor.com/project/mrJean1/pygeodesy>}
in 64- and 32-bit.

A single-File and single-Directory application with C{pygeodesy} has been bundled using U{PyInstaller
<https://PyPI.org/project/pyinstaller>} 3.4 and 64-bit Python 3.7.3 on macOS 10.13.6 High Sierra.

Previously, the tests were run with Python 3.13.0-2, 3.12.0-6, 3.11.2-4, 3.10.1-7, 3.9.6, 3.9.1, 3.8.7, 3.7.1, 2.7.15,
U{PyPy<https://PyPy.org>} 7.3.12 (Python 3.10.12), 7.3.1 (Python 3.6.9) and U{PyPy<https://PyPy.org>} 7.1.1 (Python
2.7.13) (and U{geographiclib <https://PyPI.org/project/geographiclib>} 1.52, U{numpy<https://PyPI.org/project/numpy>}
1.16.3, 1.16.4, 1.16.6, 1.19.0, 1.19.4, 1.19.5 or 1.22.4 and U{scipy<https://PyPI.org/project/scipy>} 1.2.1, 1.4.1,
1.5.2 or 1.8.1) on U{Ubuntu 16.04<https://Travis-CI.com/mrJean1/PyGeodesy>}, with Python 3.10.0-1, 3.9.0-5, 3.8.0-6,
3.7.2-6, 3.7.0, 3.6.2-5, 3.5.3, 2.7.13-17, 2.7.10 and 2.6.9 (and U{numpy<https://PyPI.org/project/numpy>} 1.19.0,
1.16.5, 1.16.2, 1.15.2, 1.14.0, 1.13.1, 1.8.0rc1 or 1.6.2 and U{scipy<https://PyPI.org/project/scipy>} 1.5.0), U{PyPy
<https://PyPy.org>} 7.3.0 (Python 2.7.13 and 3.6.9), U{PyPy<https://PyPy.org>} 6.0.0 (Python 2.7.13 and 3.5.3)
and U{Intel-Python<https://software.Intel.com/en-us/distribution-for-python>} 3.5.3 (and U{numpy
<https://PyPI.org/project/numpy>} 1.11.3) on macOS 14.0-6.1 Sonoma, 13.0-5.2 Ventura, 12.1-6 Monterey, 11.0-5.2-6.1
Big Sur (aka 10.16), 10.15.3, 10.15.5-7 Catalina, 10.14 Mojave, 10.13.6 High Sierra and 10.12 Sierra, MacOS X
10.11 El Capitan and/or MacOS X 10.10 Yosemite, with U{Pythonista<https://OMZ-Software.com/pythonista>}3.2 (with
geographiclib 1.50 or 1.49 and numpy 1.8.0) on iOS 14.4.2, 11.4.1, 12.0-3 on iPad4, iPhone6, iPhone10 and/or
iPhone12, with U{Pythonista<https://OMZ-Software.com/pythonista>} 3.1 on iOS 10.3.3, 11.0.3, 11.1.2 and 11.3
on iPad4, all in 64-bit only and with 32-bit Python 2.7.14 on Windows Server 2012R2, Windows 10 Pro and with
32-bit Python 2.6.6 on Windows XP SP3.

Notes
=====

All Python source code has been statically U{checked<https://GitHub.com/ActiveState/code/tree/master/recipes/
Python/546532_PyChecker_postprocessor>} with U{PyChecker<https://PyPI.org/project/pychecker>}, U{PyFlakes
<https://PyPI.org/project/pyflakes>}, U{PyCodeStyle<https://PyPI.org/project/pycodestyle>} (formerly Pep8) and
U{McCabe<https://PyPI.org/project/mccabe>} using Python 2.7.18 and with U{Flake8<https://PyPI.org/project/flake8>}
using Python 3.11.5, both in 64-bit on macOS 15.4.1 Sequoia.

For a summary of all I{Karney}-based functionality in C{pygeodesy}, see module U{karney
<https://mrJean1.GitHub.io/PyGeodesy/docs/pygeodesy.karney-module.html>}.

In Python 2, symbols L{S_DEG}, L{S_MIN}, L{S_SEC}, L{S_RAD} and L{S_SEP} may be multi-byte, non-ascii
characters and if so, I{not} C{unicode}.

Env variables
=============

The following environment variables are observed by C{pygeodesy}:

 - C{PYGEODESY_EXCEPTION_CHAINING} - see module L{errors<pygeodesy.errors>}.
 - C{PYGEODESY_FMT_FORM} - see module L{dms<pygeodesy.dms>}.
 - C{PYGEODESY_FSUM_F2PRODUCT} - see module L{fsums<pygeodesy.fsums>} and method L{f2product<pygeodesy.Fsum.f2product>}.
 - C{PYGEODESY_FSUM_NONFINITES} - see module L{fsums<pygeodesy.fsums>} and method L{nonfinites<pygeodesy.Fsum.nonfinites>}.
 - C{PYGEODESY_FSUM_RESIDUAL} - see module L{fsums<pygeodesy.fsums>} and method L{RESIDUAL<pygeodesy.Fsum.RESIDUAL>}.
 - C{PYGEODESY_GEOCONVERT} - see module L{mgrs<pygeodesy.mgrs>}.
 - C{PYGEODESY_GEODSOLVE} - see module L{geodsolve<pygeodesy.geodsolve>}.
 - C{PYGEODESY_INTERSECTTOOL} - see module L{geodesici<pygeodesy.geodesici>}.
 - C{PYGEODESY_LAZY_IMPORT} - see module L{lazily<pygeodesy.lazily>} and variable L{isLazy<pygeodesy.isLazy>}.
 - C{PYGEODESY_NOTIMPLEMENTED} - C{__special__} methods return C{NotImplemented} if set to "std".
 - C{PYGEODESY_RHUMBSOLVE} - see module L{rhumb.solve<pygeodesy.rhumb.solve>}.
 - C{PYGEODESY_UPS_POLES} - see modules L{ups<pygeodesy.ups>} and L{mgrs<pygeodesy.mgrs>}.

and these to specify standard or I{named} C{repr}esentations:

 - C{PYGEODESY_AZIMUTH_STD_REPR} - see method L{Azimuth<pygeodesy.Azimuth>}C{.__repr__}.
 - C{PYGEODESY_BEARING_STD_REPR} - see method L{Bearing<pygeodesy.Bearing>}C{.__repr__}.
 - C{PYGEODESY_BOOL_STD_REPR} - see method L{Bool<pygeodesy.Bool>}C{.__repr__}.
 - C{PYGEODESY_DEGREES_STD_REPR} - see method L{Degrees<pygeodesy.Degrees>}C{.__repr__}.
 - C{PYGEODESY_EPOCH_STD_REPR} - see method L{Float<pygeodesy.Epoch>}C{.__repr__}.
 - C{PYGEODESY_FLOAT_STD_REPR} - see method L{Float<pygeodesy.Float>}C{.__repr__}.
 - C{PYGEODESY_INT_STD_REPR} - see method L{Int<pygeodesy.Int>}C{.__repr__}.
 - C{PYGEODESY_METER_STD_REPR} - see method L{Meter<pygeodesy.Meter>}C{.__repr__}.
 - C{PYGEODESY_RADIANS_STD_REPR} - see method L{Radians<pygeodesy.Radians>}C{.__repr__}.
 - C{PYGEODESY_STR_STD_REPR} - see method L{Str<pygeodesy.Str>}C{.__repr__}.

plus during development:

 - C{PYGEODESY_FOR_DOCS} - for extended documentation by C{epydoc}.
 - C{PYGEODESY_GEOGRAPHICLIB} - see module L{karney<pygeodesy.karney>}.
 - C{PYGEODESY_WARNINGS} - see module L{props<pygeodesy.props>} and function L{DeprecationWarnings<pygeodesy.DeprecationWarnings>}.
 - C{PYGEODESY_XPACKAGES} - see module L{basics<pygeodesy.basics>}.
 - C{PYTHONDEVMODE} - see modules L{errors<pygeodesy.errors>} and L{props<pygeodesy.props>}.

and:

 - C{PYGEODESY_INIT__ALL__} - Set env variable C{PYGEODESY_INIT__ALL__} to anything other than C{"__all__"} to avoid
   importing all C{pygeodesy} modules unnecessarily (in Python 2 or with C{PYGEODESY_LAZY_IMPORT} turned off in Python
   3).  However, to import a C{pygeodesy} item, the item name must be qualified with the C{module} name, for example
   C{ from pygeodesy.ellipsoidalExact import LatLon } or C{ from pygeodesy.deprecated import collins }

License
=======

**) U{Copyright (C) 2016-2025 -- mrJean1 at Gmail -- All Rights Reserved.<https://OpenSource.org/licenses/MIT>}

C{Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:}

C{The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.}

C{THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.}

@newfield example: Example, Examples

@var EPS:    System's M{epsilon} ≈ 2.22044604925e-16 (C{float}).
@var EPS0:   M{EPS**2}  ≈ 4.9e-32 for near-zero comparison
@var EPS02:  M{EPS**4}  ≈ 2.4e-63 for near-zero squared comparison
@var EPS1:   M{1 - EPS} ≈ 0.9999999999999998 (C{float}).
@var EPS2:   M{EPS * 2} ≈ 4.440892098501e-16 (C{float}).
@var EPS_2:  M{EPS / 2} ≈ 1.110223024625e-16 (C{float}).
@var EPS4:   M{EPS * 4} ≈ 8.881784197001e-16 (C{float}).

@var F_D:   Format degrees as unsigned "deg°" with symbol, plus compass point suffix C{N, S, E} or C{W} (C{str}).
@var F_DM:  Format degrees as unsigned "deg°min′" with symbols, plus suffix (C{str}).
@var F_DMS: Format degrees as unsigned "deg°min′sec″" with symbols, plus suffix (C{str}).
@var F_DEG: Format degrees as unsigned "[D]DD" I{without} symbol, plus suffix (C{str}).
@var F_MIN: Format degrees as unsigned "[D]DDMM" I{without} symbols, plus suffix (C{str}).
@var F_SEC: Format degrees as unsigned "[D]DDMMSS" I{without} symbols, plus suffix (C{str}).
@var F_D60: Format degrees as unsigned "[D]DD.MMSS" C{sexagecimal} I{without} symbols, plus suffix (C{str}).
@var F__E:  Format degrees as unsigned "%E" I{without} symbols, plus suffix (C{str}).
@var F__F:  Format degrees as unsigned "%F" I{without} symbols, plus suffix (C{str}).
@var F__G:  Format degrees as unsigned "%G" I{without} symbols, plus suffix (C{str}).
@var F_RAD: Convert degrees to radians and format as unsigned "RR" with symbol, plus suffix (C{str}).

@var F_D_:   Format degrees as signed "-/deg°" with symbol, I{without} suffix (C{str}).
@var F_DM_:  Format degrees as signed "-/deg°min′" with symbols, I{without} suffix (C{str}).
@var F_DMS_: Format degrees as signed "-/deg°min′sec″" with symbols, I{without} suffix (C{str}).
@var F_DEG_: Format degrees as signed "-/[D]DD" I{without} symbol, I{without} suffix (C{str}).
@var F_MIN_: Format degrees as signed "-/[D]DDMM" I{without} symbols, I{without} suffix (C{str}).
@var F_SEC_: Format degrees as signed "-/[D]DDMMSS" I{without} symbols, I{without} suffix (C{str}).
@var F_D60_: Format degrees as signed "-/[D]DD.MMSS" C{sexagecimal} I{without} symbols, I{without} suffix (C{str}).
@var F__E_:  Format degrees as signed "-/%E" I{without} symbols, I{without} suffix (C{str}).
@var F__F_:  Format degrees as signed "-/%F" I{without} symbols, I{without} suffix (C{str}).
@var F__G_:  Format degrees as signed "-/%G" I{without} symbols, I{without} suffix (C{str}).
@var F_RAD_: Convert degrees to radians and format as signed "-/RR" I{without} symbol, I{without} suffix (C{str}).

@var F_D__:   Format degrees as signed "-/+deg°" with symbol, I{without} suffix (C{str}).
@var F_DM__:  Format degrees as signed "-/+deg°min′" with symbols, I{without} suffix (C{str}).
@var F_DMS__: Format degrees as signed "-/+deg°min′sec″" with symbols, I{without} suffix (C{str}).
@var F_DEG__: Format degrees as signed "-/+[D]DD" I{without} symbol, I{without} suffix (C{str}).
@var F_MIN__: Format degrees as signed "-/+[D]DDMM" I{without} symbols, without suffix (C{str}).
@var F_SEC__: Format degrees as signed "-/+[D]DDMMSS" I{without} symbols, I{without} suffix (C{str}).
@var F_D60__: Format degrees as signed "-/+[D]DD.MMSS" C{sexagecimal} I{without} symbols, I{without} suffix (C{str}).
@var F__E__:  Format degrees as signed "-/+%E" I{without} symbols, I{without} suffix (C{str}).
@var F__F__:  Format degrees as signed "-/+%F" I{without} symbols, I{without} suffix (C{str}).
@var F__G__:  Format degrees as signed "-/+%G" I{without} symbols, I{without} suffix (C{str}).
@var F_RAD__: Convert degrees to radians and format as signed "-/+RR" I{without} symbol, I{without} suffix (C{str}).

@var DIG:      System's M{float decimal digits} = 15 (C{int}).
@var INF:      Infinity (C{float}), see functions L{isinf<pygeodesy.isinf>} and L{isfinite<pygeodesy.isfinite>} and C{NINF}.
@var INT0:     C{int(0)}, missing Z-components, C{if B{z}=B{INT0}}, see functions L{isint0<pygeodesy.isint0>}, L{meeus2<pygeodesy.meeus2>}
@var MANT_DIG: System's M{float mantissa bits} = 53 (C{int}).
@var MAX:      System's M{float max} ≈ 1.798e+308 (C{float}).
@var MIN:      System's M{float min} ≈ 2.225e-308 (C{float}).
@var NAN:      Not-A-Number (C{float}), see function L{isnan<pygeodesy.isnan>}.
@var NEG0:     Negative 0.0 (C{float}), see function L{isneg0<pygeodesy.isneg0>}.
@var NINF:     Negative infinity (C{float}), see function L{isninf<pygeodesy.isninf>} and C{INF}.
@var NN:       Empty (C{str}), U{I{Nomen Nescio}<https://Wiktionary.org/wiki/N.N.>}.

@var PI:    Constant M{math.pi} (C{float}).
@var PI2:   Two PI, M{PI * 2}, aka I{Tau} (C{float}).
@var PI_2:  Half PI, M{PI / 2} (C{float}).
@var PI3:   Three PI, M{PI * 3} (C{float}).
@var PI3_2: One and a half PI, M{PI * 3 / 2} (C{float}).
@var PI_3:  One third PI, M{PI / 3} (C{float}).
@var PI4:   Four PI, M{PI * 4} (C{float}).
@var PI_4:  Quarter PI, M{PI / 4} (C{float}).

@var R_MA: Equatorial earth radius (C{meter}), WGS84, EPSG:3785.
@var R_MB: Polar earth radius (C{meter}), WGS84, EPSG:3785.
@var R_M:  Mean (spherical) earth radius (C{meter}).
@var R_KM: Mean (spherical) earth radius (C{Km}, kilometer).
@var R_NM: Mean (spherical) earth radius (C{NM}, nautical miles).
@var R_SM: Mean (spherical) earth radius (C{SM}, statute miles).
@var R_FM: Former FAI-Sphere earth radius (C{meter}).
@var R_GM: Average earth radius, distance to geoid surface (C{meter})
@var R_QM: Earth' (triaxial) quadratic mean radius (C{meter})
@var R_VM: Aviation/Navigation earth radius (C{meter}).

@var S_DEG: Degrees symbol, default C{"°"}
@var S_MIN: Minutes symbol, default C{"′"} aka I{PRIME}
@var S_SEC: Seconds symbol, default C{"″"} aka I{DOUBLE_PRIME}
@var S_RAD: Radians symbol, default C{""} aka L{NN<pygeodesy.NN>}
@var S_DMS: If C{True}, include, otherwise cancel all DMS symbols, default C{True}.
@var S_SEP: Separator between C{deg°|min′|sec″|suffix}, default C{""} aka L{NN<pygeodesy.NN>}

@var Conics:     Registered, predefined conics (C{enum-like}).
@var Datums:     Registered, predefined datums (C{enum-like}).
@var Ellipsoids: Registered, predefined ellipsoids (C{enum-like}).
@var RefFrames:  Registered, predefined reference frames (C{enum-like}).
@var Transforms: Registered, predefined transforms (C{enum-like}).
@var Triaxials:  Registered, predefined triaxial ellipsoids (C{enum-like}).

@var isLazy: Lazy import setting (C{int} 0, 1, 2 or 3+) from C{env} variable C{PYGEODESY_LAZY_IMPORT}, or C{None} if C{lazy import} is not supported or not enabled, or C{False} if initializing C{lazy import} failed.

@var pygeodesy_abspath: Fully qualified C{pygeodesy} directory name (C{str}).

@var version: Normalized C{pygeodesy} version (C{str}).
'''

import os.path as _os_path
import sys as _sys

_init__all__      =  True
# <https://PyInstaller.ReadTheDocs.io/en/stable/runtime-information.html>
_isfrozen         =  getattr(_sys, 'frozen', False)
pygeodesy_abspath = _os_path.dirname(_os_path.abspath(__file__))  # _sys._MEIPASS + '/pygeodesy'
_pygeodesy_       = __package__ or   _os_path.basename(pygeodesy_abspath)

if _isfrozen:  # avoid lazy import
    _lazy_import2 = None
else:
    # setting __path__ should ...
    __path__ = [pygeodesy_abspath]
    try:  # ... make this import work, ...
        import pygeodesy.lazily as _
    except ImportError:  # ... if it doesn't, extend _sys.path to include
        # this very directory such that all public and private sub-modules
        # can be imported (by epydoc, checked by PyChecker, etc.)
        _sys.path.insert(0, pygeodesy_abspath)  # XXX __path__[0]

    try:  # lazily requires Python 3.7+, see lazily.__doc__
        from pygeodesy.lazily import _init__all__, _lazy_import2  # PYCHOK expected
        _, __getattr__ = _lazy_import2(_pygeodesy_)  # PYCHOK expected

    except (ImportError, NotImplementedError):  # LazyImportError
        _lazy_import2 = None

if _init__all__ and not _lazy_import2:  # import and set __all__

    # import all public modules and export as such
    import pygeodesy.albers                as albers                 # PYCHOK exported
    import pygeodesy.auxilats              as auxilats               # PYCHOK exported
    import pygeodesy.azimuthal             as azimuthal              # PYCHOK exported
    import pygeodesy.basics                as basics                 # PYCHOK exported
    import pygeodesy.booleans              as booleans               # PYCHOK exported
    import pygeodesy.cartesianBase         as cartesianBase          # PYCHOK INTERNAL
    import pygeodesy.clipy                 as clipy                  # PYCHOK exported
    import pygeodesy.constants             as constants              # PYCHOK exported
    import pygeodesy.css                   as css                    # PYCHOK exported
    import pygeodesy.datums                as datums                 # PYCHOK exported
    import pygeodesy.deprecated            as deprecated             # PYCHOK exported
    import pygeodesy.dms                   as dms                    # PYCHOK exported
    import pygeodesy.ecef                  as ecef                   # PYCHOK exported
    import pygeodesy.ecefLocals            as ecefLocals             # PYCHOK exported
    import pygeodesy.elevations            as elevations             # PYCHOK exported
    import pygeodesy.ellipsoidalBase       as ellipsoidalBase        # PYCHOK INTERNAL
    import pygeodesy.ellipsoidalBaseDI     as ellipsoidalBaseDI      # PYCHOK INTERNAL
    import pygeodesy.ellipsoidalExact      as ellipsoidalExact       # PYCHOK exported
    import pygeodesy.ellipsoidalGeodSolve  as ellipsoidalGeodSolve   # PYCHOK exported
    import pygeodesy.ellipsoidalKarney     as ellipsoidalKarney      # PYCHOK exported
    import pygeodesy.ellipsoidalNvector    as ellipsoidalNvector     # PYCHOK exported
    import pygeodesy.ellipsoidalVincenty   as ellipsoidalVincenty    # PYCHOK exported
    import pygeodesy.ellipsoids            as ellipsoids             # PYCHOK exported
    import pygeodesy.elliptic              as elliptic               # PYCHOK exported
    import pygeodesy.epsg                  as epsg                   # PYCHOK exported
    import pygeodesy.etm                   as etm                    # PYCHOK exported
    import pygeodesy.errors                as errors                 # PYCHOK exported
    import pygeodesy.fmath                 as fmath                  # PYCHOK exported
    import pygeodesy.formy                 as formy                  # PYCHOK exported
    import pygeodesy.frechet               as frechet                # PYCHOK exported
    import pygeodesy.fstats                as fstats                 # PYCHOK exported
    import pygeodesy.fsums                 as fsums                  # PYCHOK exported
    import pygeodesy.gars                  as gars                   # PYCHOK exported
    import pygeodesy.geodesici             as geodesici              # PYCHOK exported
    import pygeodesy.geodesicw             as geodesicw              # PYCHOK exported
    import pygeodesy.geodesicx             as geodesicx              # PYCHOK exported
    import pygeodesy.geodsolve             as geodsolve              # PYCHOK exported
    import pygeodesy.geohash               as geohash                # PYCHOK exported
    import pygeodesy.geoids                as geoids                 # PYCHOK exported
    import pygeodesy.hausdorff             as hausdorff              # PYCHOK exported
    import pygeodesy.heights               as heights                # PYCHOK exported
    import pygeodesy.internals             as internals              # PYCHOK exported
    import pygeodesy.interns               as interns                # PYCHOK exported
    import pygeodesy.iters                 as iters                  # PYCHOK exported
    import pygeodesy.karney                as karney                 # PYCHOK exported
    import pygeodesy.ktm                   as ktm                    # PYCHOK exported
    import pygeodesy.latlonBase            as latlonBase             # PYCHOK INTERNAL
    import pygeodesy.lazily                as lazily                 # PYCHOK exported
    import pygeodesy.lcc                   as lcc                    # PYCHOK exported
    import pygeodesy.ltp                   as ltp                    # PYCHOK exported
    import pygeodesy.ltpTuples             as ltpTuples              # PYCHOK exported
    import pygeodesy.mgrs                  as mgrs                   # PYCHOK exported
    import pygeodesy.named                 as named                  # PYCHOK exported
    import pygeodesy.namedTuples           as namedTuples            # PYCHOK exported
    import pygeodesy.nvectorBase           as nvectorBase            # PYCHOK INTERNAL
    import pygeodesy.osgr                  as osgr                   # PYCHOK exported
    import pygeodesy.points                as points                 # PYCHOK exported
    import pygeodesy.props                 as props                  # PYCHOK exported
    import pygeodesy.resections            as resections             # PYCHOK exported
    import pygeodesy.rhumb                 as rhumb                  # PYCHOK exported
    import pygeodesy.simplify              as simplify               # PYCHOK exported
    import pygeodesy.sphericalBase         as sphericalBase          # PYCHOK INTERNAL
    import pygeodesy.sphericalNvector      as sphericalNvector       # PYCHOK exported
    import pygeodesy.sphericalTrigonometry as sphericalTrigonometry  # PYCHOK exported
    import pygeodesy.solveBase             as solveBase              # PYCHOK exported
    import pygeodesy.streprs               as streprs                # PYCHOK exported
    import pygeodesy.trf                   as trf                    # PYCHOK exported
    import pygeodesy.triaxials             as triaxials              # PYCHOK exported
    import pygeodesy.units                 as units                  # PYCHOK exported
    import pygeodesy.unitsBase             as unitsBase              # PYCHOK INTERNAL
    import pygeodesy.ups                   as ups                    # PYCHOK exported
    import pygeodesy.utily                 as utily                  # PYCHOK exported
    import pygeodesy.utm                   as utm                    # PYCHOK exported
    import pygeodesy.utmups                as utmups                 # PYCHOK exported
    import pygeodesy.utmupsBase            as utmupsBase             # PYCHOK INTERNAL
    import pygeodesy.vector2d              as vector2d               # PYCHOK exported
    import pygeodesy.vector3d              as vector3d               # PYCHOK exported
    import pygeodesy.vector3dBase          as vector3dBase           # PYCHOK INTERNAL
    import pygeodesy.webmercator           as webmercator            # PYCHOK exported
    import pygeodesy.wgrs                  as wgrs                   # PYCHOK exported

    # lift all public classes, constants, functions, etc. but ONLY
    # from the following modules ... (see also David Beazley's
    # talk <https://DaBeaz.com/modulepackage/index.html>) ... BUT
    # NOT modules ellipsoidal*, epsg, gars, geohash, spherical*,
    # vector and wgrs ... in order keep those as modules ONLY
    from pygeodesy.albers                import *  # PYCHOK __all__
    from pygeodesy.azimuthal             import *  # PYCHOK __all__
#   from pygeodesy.auxilats              import *  # PYCHOK __(_)__
    from pygeodesy.basics                import *  # PYCHOK __all__
    from pygeodesy.booleans              import *  # PYCHOK __all__
    from pygeodesy.cartesianBase         import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.clipy                 import *  # PYCHOK __all__
    from pygeodesy.constants             import *  # PYCHOK __all__
    from pygeodesy.css                   import *  # PYCHOK __all__
    from pygeodesy.datums                import *  # PYCHOK __all__
    from pygeodesy.deprecated            import *  # PYCHOK __all__ DEPRECATED
    from pygeodesy.dms                   import *  # PYCHOK __all__
    from pygeodesy.ecef                  import *  # PYCHOK __all__
#   from pygeodesy.ecefLocals            import *  # PYCHOK __all__
    from pygeodesy.elevations            import *  # PYCHOK __all__
#   from pygeodesy.ellipsoidalBase       import *  # PYCHOK __(_)__ INTERNAL
#   from pygeodesy.ellipsoidalBaseDI     import *  # PYCHOK __(_)__ INTERNAL
#   from pygeodesy.ellipsoidalExact      import *  # PYCHOK __(_)__
#   from pygeodesy.ellipsoidalGeodSolve  import *  # PYCHOK __(_)__
#   from pygeodesy.ellipsoidalKarney     import *  # PYCHOK __(_)__
#   from pygeodesy.ellipsoidalNvector    import *  # PYCHOK __(_)__
    from pygeodesy.ellipsoidalVincenty   import *  # PYCHOK __(_)__
    from pygeodesy.ellipsoids            import *  # PYCHOK __all__
    from pygeodesy.elliptic              import *  # PYCHOK __all__
    from pygeodesy.epsg                  import *  # PYCHOK __all__
    from pygeodesy.etm                   import *  # PYCHOK __all__
    from pygeodesy.errors                import *  # PYCHOK __all__
    from pygeodesy.fmath                 import *  # PYCHOK __all__
    from pygeodesy.formy                 import *  # PYCHOK __all__
    from pygeodesy.frechet               import *  # PYCHOK __all__
    from pygeodesy.fstats                import *  # PYCHOK __all__
    from pygeodesy.fsums                 import *  # PYCHOK __all__
    from pygeodesy.gars                  import *  # PYCHOK __all__
    from pygeodesy.geodesici             import *  # PYCHOK __all__
    from pygeodesy.geodesicw             import *  # PYCHOK __all__
    from pygeodesy.geodesicx             import *  # PYCHOK __all__
    from pygeodesy.geodsolve             import *  # PYCHOK __all__
    from pygeodesy.geohash               import *  # PYCHOK __all__
    from pygeodesy.geoids                import *  # PYCHOK __all__
    from pygeodesy.hausdorff             import *  # PYCHOK __all__
    from pygeodesy.heights               import *  # PYCHOK __all__
    from pygeodesy.internals             import *  # PYCHOK __all__
    from pygeodesy.interns               import *  # PYCHOK __all__
    from pygeodesy.iters                 import *  # PYCHOK __all__
    from pygeodesy.karney                import *  # PYCHOK __all__
    from pygeodesy.ktm                   import *  # PYCHOK __all__
    from pygeodesy.latlonBase            import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.lazily                import *  # PYCHOK __all__
    from pygeodesy.lcc                   import *  # PYCHOK __all__
    from pygeodesy.ltp                   import *  # PYCHOK __all__
    from pygeodesy.ltpTuples             import *  # PYCHOK __all__
    from pygeodesy.mgrs                  import *  # PYCHOK __all__
    from pygeodesy.named                 import *  # PYCHOK __all__
    from pygeodesy.namedTuples           import *  # PYCHOK __all__
    from pygeodesy.nvectorBase           import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.osgr                  import *  # PYCHOK __all__
    from pygeodesy.points                import *  # PYCHOK __all__
    from pygeodesy.props                 import *  # PYCHOK __all__
    from pygeodesy.resections            import *  # PYCHOK __all__
    from pygeodesy.rhumb                 import *  # PYCHOK __all__
    from pygeodesy.simplify              import *  # PYCHOK __all__
#   from pygeodesy.sphericalBase         import *  # PYCHOK __(_)__ INTERNAL
#   from pygeodesy.sphericalNvector      import *  # PYCHOK __(_)__
#   from pygeodesy.sphericalTrigonometry import *  # PYCHOK __(_)__
#   from pygeodesy.solveBase             import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.streprs               import *  # PYCHOK __all__
    from pygeodesy.trf                   import *  # PYCHOK __all__
    from pygeodesy.triaxials             import *  # PYCHOK __all__
    from pygeodesy.units                 import *  # PYCHOK __all__
    from pygeodesy.unitsBase             import *  # PYCHOK __all__ Float, ...
    from pygeodesy.ups                   import *  # PYCHOK __all__
    from pygeodesy.utily                 import *  # PYCHOK __all__
    from pygeodesy.utm                   import *  # PYCHOK __all__
    from pygeodesy.utmups                import *  # PYCHOK __all__
#   from pygeodesy.utmupsBase            import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.vector2d              import *  # PYCHOK __all__
    from pygeodesy.vector3d              import *  # PYCHOK __all__
    from pygeodesy.vector3dBase          import *  # PYCHOK __(_)__ INTERNAL
    from pygeodesy.webmercator           import *  # PYCHOK __all__
    from pygeodesy.wgrs                  import *  # PYCHOK __all__

    def _all(globalocals):
        from pygeodesy.internals import _headof,  _DOT_  # PYCHOK expected
        from pygeodesy.interns import NN as _NN, _attribute_, _COMMASPACE_, \
                                     _module_, _s_, _UNDER_  # PYCHOK expected
        from pygeodesy.streprs import Fmt as _Fmt  # PYCHOK expected
        # collect all public module and attribute names and check
        # that modules are imported from this package, 'pygeodesy'
        # (but the latter only when not bundled with PyInstaller or
        # Py2Exe, since the file-layout is different.  Courtesy of
        # GilderGeek<https://GitHub.com/mrJean1/PyGeodesy/issues/31>)
        ns = list(lazily._ALL_INIT)
# XXX   ps = () if _isfrozen else set([_pygeodesy_] + __name__.split(_DOT_))
        for mod, attrs in lazily._all_enums():
            mod = _headof(_headof(mod))
            if mod not in globalocals:
                t = _DOT_(_pygeodesy_, mod)
                raise ImportError('missing %s%s: %s' % (_module_, _NN, t))
            ns.append(mod)
            # check that all other public attrs do exist
            if attrs and isinstance(attrs, tuple):
                attrs = lazily._ALL_ATTRS(attrs)
                t = tuple(a for a in attrs if a not in globalocals)
                if t:
                    s = _Fmt.SQUARE(_s_, len(t)) if len(t) > 1 else _NN
                    t = _COMMASPACE_.join(_DOT_(_pygeodesy_, mod, a) for a in t)
                    raise ImportError('missing %s%s: %s' % (_attribute_, s, t))
                ns.extend(attrs)
# XXX       if ps:  # check that mod is a _pygeodesy_ module
# XXX           m = globalocals[mod]  # assert(typename(m) == mod)
# XXX           f = getattr(m, _dunder_file_, _NN)
# XXX           d = _os_path.dirname(_os_path.abspath(f)) if f else pygeodesy_abspath
# XXX           p = getattr(m, _dunder_package_, _NN) or _pygeodesy_
# XXX           if p not in ps or d != pygeodesy_abspath:
# XXX               t = '%s from %r' % (_DOT_(p, mod), f or p)
# XXX               raise ImportError('foreign %s: %s' % (_module_, t))
        return tuple(set(ns))  # remove duplicates

    __all__ = _all(globals())  # or locals()
else:
    __all__ = ()
    _init__all__ = False

from pygeodesy.internals import _version2,  _DOT_  # PYCHOK import
# from pygeodesy.interns import _DOT_  # from .internals
__version__ = '25.05.05'
# see setup.py for similar logic
version     = _DOT_(*_version2(__version__, n=3))

del _DOT_, _lazy_import2, _os_path, _sys, _version2

# **) MIT License
#
# Copyright (C) 2016-2025 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
