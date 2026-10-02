# This module contains the various variables used as tolerances and similar
# throughout the code in the core functionality.


class config:
    class eigensymmetries:
        rotation_integer_tolerance = 1e-12
        method = 'iterative'
        crystal_symmetries = True

        class iterative:
            zero_tolerance = 1e-12
            simplify = True
            simplify_tolerance = None
            method = 'symbolic'


"""This is the tolerance used when the rotation matrices and similar are tested
if they are integers.
"""
integer_tolerance = 1e-12

""" For each symmetry, the constraint matrix can be reduced to square
again. This can be done either by 'symbolic', 'numeric' or not at all
(None). Default is None since the matrix is often small enough to fit
in memory.
'symbolic', 'numeric', None
"""
eigentensor_compress_mode = None

"""If this is True, before every symbolic compression the values will be
simplified by sympy, potentially turning them into exact rational or
irrational numbers. This can be useful for systems with non-integer
rotation matrices in cartesian coordinates e.g. hcp. The main purpose is
to make the rref more stable against repeating rounding errors.
True, False
"""
eigentensor_simplify_before_compress = False

""" If non compress was used during construction but used before solving
True, False
"""
eigentensor_simplify_before_last_compress = False

"""If the compress_mode is None the constraint matrix might be compressed
right before the nullspace() solver
'numeric', 'symbolic', None
"""
eigentensor_compress_before_solve = None

"""This might make the nullspace() more stable
True, False
"""
eigentensor_simplify_before_solve = True

"""
'symbolic', 'numeric'
"""
eigentensor_solve_mode = 'symbolic'


"""
'symbolic', 'numeric'
"""
sum_rule_constraint_mode = 'symbolic'

"""
True, False
"""
sum_rule_constraint_simplify = True


"""
True, False
"""
constraint_vectors_simplify_before_compress = True

"""
'symbolic', 'numeric', None
"""
constraint_vectors_compress_mode = 'symbolic'

"""
True, False
"""
constraint_vectors_simplify_before_solve = True

"""
'symbolic', 'numeric'
"""
constraint_vectors_solve_mode = 'symbolic'
