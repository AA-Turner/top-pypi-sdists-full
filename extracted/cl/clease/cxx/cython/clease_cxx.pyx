# distutils: language = c++
# cython: c_string_type=str, c_string_encoding=ascii
from libcpp cimport bool

include "pyce_updater.pyx"
include "py_cluster.pyx"
include "py_atoms.pyx"

cdef extern from "additional_tools.hpp":
    cpdef bool has_parallel()
