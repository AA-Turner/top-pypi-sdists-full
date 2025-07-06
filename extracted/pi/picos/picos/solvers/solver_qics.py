# ------------------------------------------------------------------------------
# Copyright (C) 2024 Kerry He
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PICOS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Implementation of :class:`QICSSolver`."""

import cvxopt
import numpy
import math

from ..apidoc import api_end, api_start
from ..constraints import (AffineConstraint, DummyConstraint, RSOCConstraint,
                           SOCConstraint, LMIConstraint, ComplexLMIConstraint,
                           ExpConeConstraint, KullbackLeiblerConstraint,
                           QuantRelEntropyConstraint,
                           ComplexQuantRelEntropyConstraint,
                           QuantCondEntropyConstraint,
                           ComplexQuantCondEntropyConstraint,
                           QuantKeyDistributionConstraint,
                           ComplexQuantKeyDistributionConstraint,
                           OpRelEntropyConstraint,
                           ComplexOpRelEntropyConstraint,
                           TrOpRelEntropyConstraint,
                           ComplexTrOpRelEntropyConstraint,
                           MatrixGeoMeanEpiConstraint,
                           ComplexMatrixGeoMeanEpiConstraint,
                           TrMatrixGeoMeanEpiConstraint,
                           ComplexTrMatrixGeoMeanEpiConstraint,
                           MatrixGeoMeanHypoConstraint,
                           ComplexMatrixGeoMeanHypoConstraint,
                           TrMatrixGeoMeanHypoConstraint,
                           ComplexTrMatrixGeoMeanHypoConstraint,
                           QuasiEntrEpiConstraint,
                           ComplexQuasiEntrEpiConstraint,
                           QuasiEntrHypoConstraint,
                           ComplexQuasiEntrHypoConstraint,
                           RenyiEntrConstraint,
                           ComplexRenyiEntrConstraint,
                           SandQuasiEntrEpiConstraint,
                           ComplexSandQuasiEntrEpiConstraint,
                           SandQuasiEntrHypoConstraint,
                           ComplexSandQuasiEntrHypoConstraint,
                           SandRenyiEntrConstraint,
                           ComplexSandRenyiEntrConstraint,
                           )
from ..expressions import (CONTINUOUS_VARTYPES, AffineExpression,
                           ComplexAffineExpression)
from ..modeling.footprint import Specification
from ..modeling.solution import (PS_FEASIBLE, PS_INFEASIBLE, PS_UNBOUNDED,
                                 PS_UNKNOWN, PS_ILLPOSED, SS_OPTIMAL,
                                 SS_INFEASIBLE, SS_UNKNOWN, SS_PREMATURE,
                                 Solution)
from .solver import Solver

_API_START = api_start(globals())
# -------------------------------


class QICSSolver(Solver):
    """Interface to the QICS solver."""

    SUPPORTED = Specification(
        objectives=[
            AffineExpression],
        variables=CONTINUOUS_VARTYPES,
        constraints=[
            DummyConstraint, AffineConstraint, SOCConstraint, RSOCConstraint,
            LMIConstraint, ComplexLMIConstraint, ExpConeConstraint,
            KullbackLeiblerConstraint, QuantRelEntropyConstraint,
            ComplexQuantRelEntropyConstraint, QuantCondEntropyConstraint,
            ComplexQuantCondEntropyConstraint, QuantKeyDistributionConstraint,
            ComplexQuantKeyDistributionConstraint, OpRelEntropyConstraint,
            ComplexOpRelEntropyConstraint, TrOpRelEntropyConstraint,
            ComplexTrOpRelEntropyConstraint, MatrixGeoMeanEpiConstraint,
            ComplexMatrixGeoMeanEpiConstraint, TrMatrixGeoMeanEpiConstraint,
            ComplexTrMatrixGeoMeanEpiConstraint, MatrixGeoMeanHypoConstraint,
            ComplexMatrixGeoMeanHypoConstraint, TrMatrixGeoMeanHypoConstraint,
            ComplexTrMatrixGeoMeanHypoConstraint, QuasiEntrEpiConstraint,
            ComplexQuasiEntrEpiConstraint, QuasiEntrHypoConstraint,
            ComplexQuasiEntrHypoConstraint, RenyiEntrConstraint,
            ComplexRenyiEntrConstraint, SandQuasiEntrEpiConstraint,
            ComplexSandQuasiEntrEpiConstraint, SandQuasiEntrHypoConstraint,
            ComplexSandQuasiEntrHypoConstraint, SandRenyiEntrConstraint,
            ComplexSandRenyiEntrConstraint,])

    @classmethod
    def supports(cls, footprint, explain=False):
        """Implement :meth:`~.solver.Solver.supports`."""
        result = Solver.supports(footprint, explain)
        if not result or (explain and not result[0]):
            return result

        if footprint not in cls.SUPPORTED:
            if explain:
                return False, cls.SUPPORTED.mismatch_reason(footprint)
            else:
                return False

        return (True, None) if explain else True

    @classmethod
    def default_penalty(cls):
        """Implement :meth:`~.solver.Solver.default_penalty`."""
        return 1.0  # Stable free/open source solver.

    @classmethod
    def test_availability(cls):
        """Implement :meth:`~.solver.Solver.test_availability`."""
        cls.check_import("qics")

    @classmethod
    def names(cls):
        """Implement :meth:`~.solver.Solver.names`."""
        return "qics", "QICS", "Quantum Information Conic Solver", None

    @classmethod
    def is_free(cls):
        """Implement :meth:`~.solver.Solver.is_free`."""
        return True

    def __init__(self, problem):
        """Initialize a QICS solver interface.

        :param ~picos.Problem problem: The problem to be solved.
        """
        super(QICSSolver, self).__init__(problem)

        self._numVars = 0
        """Total number of scalar variables passed to QICS."""

        self._qicsVarOffset = {}
        """Maps a PICOS variable to its offset in the constraint matrix."""

        self._qicsConIndices = {}
        """Maps a PICOS constraint to its row in the constraint matrix."""

        self._qicsVarCone = {}
        """Times a PICOS variable is associated with a PICOS constraint."""

        self._qicsVarConePosition = {}
        """Associates PICOS variables to where they are in PICOS constraints."""

    @staticmethod
    def stack(*args):
        """Stack vectors or matrices."""
        import scipy.sparse

        if isinstance(args[0], scipy.sparse.spmatrix):
            for i in range(1, len(args)):
                assert isinstance(args[i], scipy.sparse.spmatrix)

            return scipy.sparse.vstack(args, format="csc")
        else:
            reshaped_args = []
            for i in range(len(args)):
                assert isinstance(args[i], numpy.ndarray)
                reshaped_args += [args[i].reshape(-1, 1)]

            return numpy.vstack(reshaped_args)

    @staticmethod
    def blkdiag(*args):
        """Stack vectors or matrices."""
        import scipy.sparse

        assert isinstance(args[0], scipy.sparse.spmatrix)
        for i in range(1, len(args)):
            assert isinstance(args[i], scipy.sparse.spmatrix)

        if args[0].shape == (0, 0):
            return scipy.sparse.block_diag(args[1:], format="csc")

        return scipy.sparse.block_diag(args, format="csc")

    @staticmethod
    def complex_to_real(A):
        """Splits complex matrix into real and imaginary parts."""
        import scipy.sparse

        if isinstance(A, scipy.sparse.spmatrix):
            A = A.tocoo()

            rows = numpy.concatenate((2 * A.row, 2 * A.row + 1))
            cols = numpy.concatenate((A.col, A.col))
            data = numpy.concatenate((A.data.real, A.data.imag))

            where_nonzero = data != 0.0
            rows = rows[where_nonzero]
            cols = cols[where_nonzero]
            data = data[where_nonzero]

            return scipy.sparse.csc_matrix(
                (data, (rows, cols)), shape=(2 * A.shape[0], A.shape[1])
            )
        else:
            assert isinstance(A, numpy.ndarray)

            new_A = numpy.zeros(2 * A.shape[0])

            new_A[::2] = A.real
            new_A[1::2] = A.imag

            return new_A

    def reset_problem(self):
        """Implement :meth:`~.solver.Solver.reset_problem`."""
        self.int = None

        self._numVars = 0
        self._qicsVarOffset.clear()
        self._qicsConIndices.clear()
        self._qicsVarCone.clear()
        self._qicsVarConePosition.clear()

    def _affine_expression_to_G_and_h(self, expression):
        assert isinstance(
            expression, (AffineExpression, ComplexAffineExpression))

        return expression.scipy_sparse_matrix_form(
            varOffsetMap=self._qicsVarOffset, dense_b=True)

    _Gh = _affine_expression_to_G_and_h

    def _import_variables(self):
        offset = 0

        if self._use_G:
            variable_list = self.ext.variables.values()
        else:
            variable_list = self._sortedQicsVarConePosition

        for variable in variable_list:
            dim = variable.dim

            # Register the variable.
            self._qicsVarOffset[variable] = offset
            offset += dim

        assert offset == self._numVars

        # Add variable bounds as affine constraints.
        for variable in variable_list:
            bounds = variable.bound_constraint
            if bounds:
                self._import_affine_constraint(bounds)

    def _get_expand_compact_op(self, n, iscomplex=False):
        import scipy

        dim_compact = n * n if iscomplex else n * (n + 1) // 2
        dim_full = 2 * n * n if iscomplex else n * n

        I = numpy.zeros(dim_full)
        J = numpy.zeros(dim_full)
        V = numpy.zeros(dim_full)

        irt2 = math.sqrt(0.5)

        row = 0
        k = 0
        for j in range(n):
            for i in range(j):
                I[k : k + 2] = row
                if iscomplex:
                    J[k : k + 2] = [2 * (i + j * n), 2 * (j + i * n)]
                else:
                    J[k : k + 2] = [i + j * n, j + i * n]
                V[k : k + 2] = irt2
                k += 2
                row += 1
            I[k] = row
            J[k] = 2 * j * (n + 1) if iscomplex else j * (n + 1)
            V[k] = 1.0
            k += 1
            row += 1

        if iscomplex:
            for j in range(n):
                for i in range(j):
                    I[k : k + 2] = row
                    J[k : k + 2] = [2 * (i + j * n) + 1, 2 * (j + i * n) + 1]
                    V[k : k + 2] = [-irt2, irt2]
                    k += 2
                    row += 1

        return scipy.sparse.csr_matrix(
            (V, (I, J)), shape=(dim_compact, dim_full)
        )

    def _get_expand_compact_all_op(self):
        import scipy
        from ..expressions import SymmetricVariable, HermitianVariable

        expand_compact_ops = []
        for variable in self._sortedQicsVarConePosition:
            if isinstance(variable, SymmetricVariable):
                expand_compact_ops += [
                    self._get_expand_compact_op(variable.shape[0])
                ]
            elif isinstance(variable, HermitianVariable):
                expand_compact_ops += [
                    self._get_expand_compact_op(variable.shape[0], True)
                ]
            else:
                expand_compact_ops += [scipy.sparse.eye(variable.dim)]

        return scipy.sparse.block_diag(expand_compact_ops, format="csc")

    def _import_affine_constraint(self, constraint):
        import qics

        assert isinstance(constraint, AffineConstraint)

        (G_smaller, h_smaller) = self._Gh(constraint.smaller)
        (G_greater, h_greater) = self._Gh(constraint.greater)

        G = G_smaller - G_greater
        h = h_greater - h_smaller

        if constraint.is_equality():
            self._qicsConIndices[constraint] = range(
                self.int["b"].size, self.int["b"].size + h.size
            )

            self.int["A"] = self.stack(self.int["A"], G)
            self.int["b"] = self.stack(self.int["b"], h)
        else:
            if self._use_G:
                self._qicsConIndices[constraint] = len(self.int["cones"])

                self.int["G"] = self.stack(self.int["G"], G)
                self.int["h"] = self.stack(self.int["h"], h)
            else:
                import scipy

                self.int["G"] = self.blkdiag(
                    self.int["G"], -scipy.sparse.eye(len(h)))

            self.int["cones"] += [qics.cones.NonNegOrthant(len(h))]

    def _import_soc_constraint(self, constraint):
        import qics

        assert isinstance(constraint, SOCConstraint)

        (A, b) = self._Gh(constraint.ne)
        (c, d) = self._Gh(constraint.ub)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -c, -A)
            self.int["h"] = self.stack(self.int["h"], d, b)
        else:
            import scipy

            self.int["G"] = self.blkdiag(
                self.int["G"], -scipy.sparse.eye(1 + len(b)))

        self.int["cones"] += [qics.cones.SecondOrder(len(b))]

    def _import_rsoc_constraint(self, constraint):
        import qics

        assert isinstance(constraint, RSOCConstraint)

        (A, b) = self._Gh(constraint.ne)
        (c1, d1) = self._Gh(constraint.ub1)
        (c2, d2) = self._Gh(constraint.ub2)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        self.int["G"] = self.stack(self.int["G"], -c1 - c2, -2 * A, c2 - c1)
        self.int["h"] = self.stack(self.int["h"], d1 + d2, 2 * b, d1 - d2)

        self.int["cones"] += [qics.cones.SecondOrder(1 + len(b))]

    def _import_lmi_constraint(self, constraint):
        import qics

        assert isinstance(constraint, LMIConstraint)
        iscomplex = isinstance(constraint, ComplexLMIConstraint)

        (G_smaller, h_smaller) = self._Gh(constraint.smaller)
        (G_greater, h_greater) = self._Gh(constraint.greater)

        G = G_smaller - G_greater
        h = h_greater - h_smaller

        n = math.isqrt(len(h))

        if iscomplex:
            G = self.complex_to_real(G)
            h = self.complex_to_real(h)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], G)
            self.int["h"] = self.stack(self.int["h"], h)
        else:
            import scipy

            dim = 2 * n * n if iscomplex else n * n
            self.int["G"] = self.blkdiag(self.int["G"], -scipy.sparse.eye(dim))

        self.int["cones"] += [qics.cones.PosSemidefinite(n, iscomplex)]

    def _import_expcone_constraint(self, constraint):
        import qics

        assert isinstance(constraint, ExpConeConstraint)

        (Gx, hx) = self._Gh(constraint.x)
        (Gy, hy) = self._Gh(constraint.y)
        (Gz, hz) = self._Gh(constraint.z)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        # QICS' classical entr. cone is cl{(x,y,z) | x >= z*log(z/y), z,y > 0},
        # PICOS' is cl{(x,y,z) | x >= y*exp(z/y), y > 0}. Note that given y > 0
        # it is x >= y*exp(z/y) if and only if -z >= y*log(y/x). Therefore we
        # can transform from our coordinates to theirs with the mapping
        # (x, y, z) ↦ (-z, x, y). Further, G and h with G = (Gx, Gy, Gz) and
        # h = (hx, hy, hz) are such that G*X + h = (x, y, z) where X is the
        # row-vectorization of all variables. QICS however expects G and h such
        # that h - G*X is constrained to be in the exponential cone.
        self.int["G"] = self.stack(self.int["G"], Gz, -Gx, -Gy)
        self.int["h"] = self.stack(self.int["h"], -hz, hx, hy)

        self.int["cones"] += [qics.cones.ClassEntr(1)]

    def _import_kldiv_constraint(self, constraint):
        import qics

        assert isinstance(constraint, KullbackLeiblerConstraint)

        (Gt, ht) = self._Gh(constraint.upperBound)
        (Gx, hx) = self._Gh(constraint.numerator)
        (Gy, hy) = self._Gh(constraint.denominator)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        # Check if we can reduce to entropy
        if (hy == hy[0]).all():
            Gy_dense = Gy.toarray()
            if (Gy_dense == Gy_dense[0]).all():
                if self._use_G:
                    self.int["G"] = self.stack(
                        self.int["G"], -Gt, -Gy[[0]], -Gx)
                    self.int["h"] = self.stack(self.int["h"], ht, hy[[0]], hx)
                else:
                    import scipy

                    dim = 2 + len(hx)
                    self.int["G"] = self.blkdiag(
                        self.int["G"], -scipy.sparse.eye(dim))

                self.int["cones"] += [qics.cones.ClassEntr(len(hx))]

                return

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -Gt, -Gx, -Gy)
            self.int["h"] = self.stack(self.int["h"], ht, hx, hy)
        else:
            import scipy

            dim = 1 + 2 * len(hx)
            self.int["G"] = self.blkdiag(self.int["G"], -scipy.sparse.eye(dim))

        self.int["cones"] += [qics.cones.ClassRelEntr(len(hx))]

    def _import_qre_constraint(self, constraint):
        import qics

        assert isinstance(constraint, QuantRelEntropyConstraint)
        iscomplex = isinstance(constraint, ComplexQuantRelEntropyConstraint)

        (Gt, ht) = self._Gh(constraint.upperBound)
        (Gx, hx) = self._Gh(constraint.X)
        (Gy, hy) = self._Gh(constraint.Y)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        n = math.isqrt(len(hx))

        # Check if we can reduce to entropy by checking if columns of
        # G and h are all multiples of the identity matrix
        diag_idxs = numpy.arange(0, n * n, n + 1)
        offdiag_idxs = numpy.delete(numpy.arange(n * n), diag_idxs)
        if (hy[offdiag_idxs] == 0).all() and (hy[diag_idxs] == hy[0]).all():
            if numpy.isin(Gy.indices, diag_idxs).all():
                Gy_diag_dense = Gy[diag_idxs].toarray()
                if (Gy_diag_dense == Gy_diag_dense[0]).all():
                    if iscomplex:
                        Gx = self.complex_to_real(Gx)
                        hx = self.complex_to_real(hx)

                    if self._use_G:
                        self.int["G"] = self.stack(
                            self.int["G"], -Gt, -Gy[[0]].real, -Gx
                        )
                        self.int["h"] = self.stack(
                            self.int["h"], ht, hy[[0]].real, hx
                        )
                    else:
                        import scipy

                        dim = 2 + 2 * n * n if iscomplex else 2 + n * n
                        self.int["G"] = self.blkdiag(
                            self.int["G"], -scipy.sparse.eye(dim))

                    self.int["cones"] += [qics.cones.QuantEntr(n, iscomplex)]
                    return

        if iscomplex:
            Gx = self.complex_to_real(Gx)
            Gy = self.complex_to_real(Gy)
            hx = self.complex_to_real(hx)
            hy = self.complex_to_real(hy)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -Gt, -Gx, -Gy)
            self.int["h"] = self.stack(self.int["h"], ht, hx, hy)
        else:
            import scipy

            dim = 1 + 4 * n * n if iscomplex else 1 + 2 * n * n
            self.int["G"] = self.blkdiag(self.int["G"], -scipy.sparse.eye(dim))

        self.int["cones"] += [qics.cones.QuantRelEntr(n, iscomplex)]

    def _import_qce_constraint(self, constraint):
        import qics

        assert isinstance(constraint, QuantCondEntropyConstraint)
        iscomplex = isinstance(constraint, ComplexQuantCondEntropyConstraint)

        (Gt, ht) = self._Gh(constraint.lowerBound)
        (Gx, hx) = self._Gh(constraint.X)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        sys = constraint.subsystems
        dims = [dim[0] for dim in constraint.dimensions]

        if iscomplex:
            Gx = self.complex_to_real(Gx)
            hx = self.complex_to_real(hx)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], Gt, -Gx)
            self.int["h"] = self.stack(self.int["h"], -ht, hx)
        else:
            import scipy

            n = numpy.prod(dims)
            dim = 2 * n * n if iscomplex else n * n
            self.int["G"] = self.blkdiag(
                self.int["G"], scipy.sparse.eye(1), -scipy.sparse.eye(dim)
            )

        self.int["cones"] += [qics.cones.QuantCondEntr(dims, sys, iscomplex)]

    def _import_qkd_constraint(self, constraint):
        import qics

        assert isinstance(constraint, QuantKeyDistributionConstraint)
        iscomplex = isinstance(
            constraint, ComplexQuantKeyDistributionConstraint
        )

        (Gt, ht) = self._Gh(constraint.upperBound)
        (Gx, hx) = self._Gh(constraint.X)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        n = math.isqrt(len(hx))
        K_list = constraint.K_list
        Z_list = constraint.Z_list

        if iscomplex:
            Gx = self.complex_to_real(Gx)
            hx = self.complex_to_real(hx)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -Gt, -Gx)
            self.int["h"] = self.stack(self.int["h"], ht, hx)
        else:
            import scipy

            dim = 1 + 2 * n * n if iscomplex else 1 + n * n
            self.int["G"] = self.blkdiag(self.int["G"], -scipy.sparse.eye(dim))

        if K_list is None:
            self.int["cones"] += [qics.cones.QuantKeyDist(n, Z_list, iscomplex)]
        else:
            self.int["cones"] += [
                qics.cones.QuantKeyDist(K_list, Z_list, iscomplex)]

    def _import_operator_constraint(self, constraint):
        import qics

        OperatorConstraints = (
            OpRelEntropyConstraint,
            MatrixGeoMeanEpiConstraint,
            MatrixGeoMeanHypoConstraint,
        )
        MatrixGeoMeanConstraints = (
            MatrixGeoMeanEpiConstraint,
            MatrixGeoMeanHypoConstraint,
        )
        ComplexConstraints = (
            ComplexOpRelEntropyConstraint,
            ComplexMatrixGeoMeanEpiConstraint,
            ComplexMatrixGeoMeanHypoConstraint,
        )
        EpigraphConstraints = (
            OpRelEntropyConstraint,
            MatrixGeoMeanEpiConstraint,
        )

        assert isinstance(constraint, OperatorConstraints)
        iscomplex = isinstance(constraint, ComplexConstraints)
        isepigraph = isinstance(constraint, EpigraphConstraints)

        if isepigraph:
            (Gt, ht) = self._Gh(constraint.upperBound)
        else:
            (Gt, ht) = self._Gh(constraint.lowerBound)
        (Gx, hx) = self._Gh(constraint.X)
        (Gy, hy) = self._Gh(constraint.Y)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        n = math.isqrt(len(hx))
        sgn = 1 if isepigraph else -1

        if iscomplex:
            Gt = self.complex_to_real(Gt)
            Gx = self.complex_to_real(Gx)
            Gy = self.complex_to_real(Gy)
            ht = self.complex_to_real(ht)
            hx = self.complex_to_real(hx)
            hy = self.complex_to_real(hy)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -sgn * Gt, -Gx, -Gy)
            self.int["h"] = self.stack(self.int["h"], sgn * ht, hx, hy)
        else:
            import scipy

            dim = 2 * n * n if iscomplex else n * n
            self.int["G"] = self.blkdiag(
                self.int["G"],
                -sgn * scipy.sparse.eye(dim),
                -scipy.sparse.eye(2 * dim),
            )

        if isinstance(constraint, MatrixGeoMeanConstraints):
            func = constraint.power
        elif isinstance(constraint, OpRelEntropyConstraint):
            func = "log"
        self.int["cones"] += [qics.cones.OpPerspecEpi(n, func, iscomplex)]

    def _import_trace_constraint(self, constraint):
        import qics

        QuasiEntrConstraints = (
            QuasiEntrEpiConstraint,
            QuasiEntrHypoConstraint,
        )
        SandQuasiEntrConstraints = (
            SandQuasiEntrEpiConstraint,
            SandQuasiEntrHypoConstraint,
        )
        TrMatrixGeoMeanConstraints = (
            TrMatrixGeoMeanEpiConstraint,
            TrMatrixGeoMeanHypoConstraint,
        )
        ComplexConstraints = (
            ComplexTrMatrixGeoMeanEpiConstraint,
            ComplexTrMatrixGeoMeanHypoConstraint,
            ComplexQuasiEntrEpiConstraint,
            ComplexQuasiEntrHypoConstraint,
            ComplexSandQuasiEntrEpiConstraint,
            ComplexSandQuasiEntrHypoConstraint,
            ComplexTrOpRelEntropyConstraint,
        )
        EpigraphConstraints = (
            TrMatrixGeoMeanEpiConstraint,
            QuasiEntrEpiConstraint,
            SandQuasiEntrEpiConstraint,
            TrOpRelEntropyConstraint,
        )

        assert isinstance(constraint, QuasiEntrConstraints) \
            or isinstance(constraint, SandQuasiEntrConstraints) \
            or isinstance(constraint, TrMatrixGeoMeanConstraints) \
            or isinstance(constraint, TrOpRelEntropyConstraint)
        iscomplex = isinstance(constraint, ComplexConstraints)
        isepigraph = isinstance(constraint, EpigraphConstraints)

        if isepigraph:
            (Gt, ht) = self._Gh(constraint.upperBound)
        else:
            (Gt, ht) = self._Gh(constraint.lowerBound)
        (Gx, hx) = self._Gh(constraint.X)
        (Gy, hy) = self._Gh(constraint.Y)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        n = math.isqrt(len(hx))
        sgn = 1 if isepigraph else -1

        if iscomplex:
            Gx = self.complex_to_real(Gx)
            Gy = self.complex_to_real(Gy)
            hx = self.complex_to_real(hx)
            hy = self.complex_to_real(hy)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -sgn * Gt, -Gx, -Gy)
            self.int["h"] = self.stack(self.int["h"], sgn * ht, hx, hy)
        else:
            import scipy

            dim = 2 * n * n if iscomplex else n * n
            self.int["G"] = self.blkdiag(
                self.int["G"],
                -sgn * scipy.sparse.eye(1),
                -scipy.sparse.eye(2 * dim),
            )

        if isinstance(constraint, TrOpRelEntropyConstraint):
            self.int["cones"] += [qics.cones.OpPerspecTr(n, "log", iscomplex)]
        elif isinstance(constraint, TrMatrixGeoMeanConstraints):
            p = constraint.power
            self.int["cones"] += [qics.cones.OpPerspecTr(n, p, iscomplex)]
        elif isinstance(constraint, QuasiEntrConstraints):
            p = constraint.alpha
            self.int["cones"] += [qics.cones.QuasiEntr(n, p, iscomplex)]
        elif isinstance(constraint, SandQuasiEntrConstraints):
            p = constraint.alpha
            self.int["cones"] += [qics.cones.SandQuasiEntr(n, p, iscomplex)]

    def _import_renyi_constraint(self, constraint):
        import qics

        RenyiConstraints = (RenyiEntrConstraint, SandRenyiEntrConstraint)
        ComplexConstraints = (
            ComplexRenyiEntrConstraint,
            ComplexSandRenyiEntrConstraint,
        )

        assert isinstance(constraint, (RenyiConstraints))
        iscomplex = isinstance(constraint, ComplexConstraints)

        (Gt, ht) = self._Gh(constraint.upperBound)
        (Gu, hu) = self._Gh(constraint.u)
        (Gx, hx) = self._Gh(constraint.X)
        (Gy, hy) = self._Gh(constraint.Y)

        self._qicsConIndices[constraint] = len(self.int["cones"])

        n = math.isqrt(len(hx))

        if iscomplex:
            Gx = self.complex_to_real(Gx)
            Gy = self.complex_to_real(Gy)
            hx = self.complex_to_real(hx)
            hy = self.complex_to_real(hy)

        if self._use_G:
            self.int["G"] = self.stack(self.int["G"], -Gt, -Gu, -Gx, -Gy)
            self.int["h"] = self.stack(self.int["h"], ht, hu, hx, hy)
        else:
            import scipy

            dim = 2 + 4 * n * n if iscomplex else 2 + 2 * n * n
            self.int["G"] = self.blkdiag(self.int["G"], -scipy.sparse.eye(dim))

        alpha = constraint.alpha
        if isinstance(constraint, RenyiEntrConstraint):
            self.int["cones"] += [qics.cones.RenyiEntr(n, alpha, iscomplex)]
        elif isinstance(constraint, SandRenyiEntrConstraint):
            self.int["cones"] += [qics.cones.SandRenyiEntr(n, alpha, iscomplex)]

    def _import_objective(self):
        direction, objective = self.ext.no

        # QICS only supports minimization; flip the sign for maximization.
        if direction == "max":
            objective = -objective

        # Import coefficients.
        c, offset = self._Gh(objective)
        self.int["c"][:] = c.toarray().T
        self.int["offset"] = offset[0]

    def _import_constraint(self, constraint):
        OperatorConstraints = (
            OpRelEntropyConstraint,
            MatrixGeoMeanEpiConstraint,
            MatrixGeoMeanHypoConstraint,
        )
        TraceConstraints = (
            TrMatrixGeoMeanEpiConstraint,
            TrMatrixGeoMeanHypoConstraint,
            TrOpRelEntropyConstraint,
            QuasiEntrEpiConstraint,
            QuasiEntrHypoConstraint,
            SandQuasiEntrEpiConstraint,
            SandQuasiEntrHypoConstraint,
        )
        RenyiConstraints = (RenyiEntrConstraint, SandRenyiEntrConstraint)

        if isinstance(constraint, AffineConstraint):
            self._import_affine_constraint(constraint)
        elif isinstance(constraint, SOCConstraint):
            self._import_soc_constraint(constraint)
        elif isinstance(constraint, RSOCConstraint):
            self._import_rsoc_constraint(constraint)
        elif isinstance(constraint, LMIConstraint):
            self._import_lmi_constraint(constraint)
        elif isinstance(constraint, ExpConeConstraint):
            self._import_expcone_constraint(constraint)
        elif isinstance(constraint, KullbackLeiblerConstraint):
            self._import_kldiv_constraint(constraint)
        elif isinstance(constraint, QuantRelEntropyConstraint):
            self._import_qre_constraint(constraint)
        elif isinstance(constraint, QuantCondEntropyConstraint):
            self._import_qce_constraint(constraint)
        elif isinstance(constraint, QuantKeyDistributionConstraint):
            self._import_qkd_constraint(constraint)
        elif isinstance(constraint, OperatorConstraints):
            self._import_operator_constraint(constraint)
        elif isinstance(constraint, TraceConstraints):
            self._import_trace_constraint(constraint)
        elif isinstance(constraint, RenyiConstraints):
            self._import_renyi_constraint(constraint)
        else:
            assert isinstance(constraint, DummyConstraint), \
                "Unexpected constraint type: {}".format(
                constraint.__class__.__name__)

    def _check_constraint_needs_G(self, constraint):
        ConvexDivergenceConstraints = (
            QuantRelEntropyConstraint,
            OpRelEntropyConstraint,
            TrOpRelEntropyConstraint,
            MatrixGeoMeanEpiConstraint,
            TrMatrixGeoMeanEpiConstraint,
            QuasiEntrEpiConstraint,
            SandQuasiEntrEpiConstraint,
        )
        ConcaveDivergenceConstraints = (
            MatrixGeoMeanHypoConstraint,
            TrMatrixGeoMeanHypoConstraint,
            QuasiEntrHypoConstraint,
            SandQuasiEntrHypoConstraint,
        )
        RenyiConstraints = (RenyiEntrConstraint, SandRenyiEntrConstraint)

        if isinstance(constraint, AffineConstraint):
            if constraint.is_equality():
                return False
            else:
                return self._check_is_basevar([constraint.nnVar])
        elif isinstance(constraint, SOCConstraint):
            return self._check_is_basevar([constraint.ub, constraint.ne])
        elif isinstance(constraint, RSOCConstraint):
            return True  # QICS doesn't directly support this cone
        elif isinstance(constraint, LMIConstraint):
            return self._check_is_basevar([constraint.semidefVar])
        elif isinstance(constraint, ExpConeConstraint):
            return True  # QICS doesn't directly support this cone
        elif isinstance(constraint, KullbackLeiblerConstraint):
            return self._check_is_basevar(
                [constraint.upperBound, constraint.numerator,
                 constraint.denominator])
        elif isinstance(constraint, ConvexDivergenceConstraints):
            return self._check_is_basevar(
                [constraint.upperBound, constraint.X, constraint.Y])
        elif isinstance(constraint, ConcaveDivergenceConstraints):
            return self._check_is_basevar(
                [constraint.lowerBound, constraint.X, constraint.Y])
        elif isinstance(constraint, QuantCondEntropyConstraint):
            return self._check_is_basevar([constraint.lowerBound, constraint.X])
        elif isinstance(constraint, QuantKeyDistributionConstraint):
            return self._check_is_basevar([constraint.upperBound, constraint.X])
        elif isinstance(constraint, RenyiConstraints):
            return self._check_is_basevar(
                [constraint.upperBound, constraint.X, constraint.Y,
                 constraint.u])
        else:
            assert isinstance(constraint, DummyConstraint), \
                "Unexpected constraint type: {}".format(
                constraint.__class__.__name__)
            return True

    def _check_is_basevar(self, vars):
        from ..expressions import BaseVariable

        for var in vars:
            if isinstance(var, BaseVariable):
                assert var in self._qicsVarCone
                self._qicsVarCone[var] += 1
                self._qicsVarConePosition[var] = (
                    max(self._qicsVarConePosition.values()) + 1
                )
            else:
                return True
        return False

    def _check_use_G(self):
        # Register the variable
        for variable in self.ext.variables.values():
            self._qicsVarCone[variable] = 0
            self._qicsVarConePosition[variable] = -1

        # Go through all constraints and associate with variables
        for variable in self.ext.variables.values():
            bounds = variable.bound_constraint
            if bounds and self._check_constraint_needs_G(bounds):
                return True

        for constraint in self.ext.constraints.values():
            if self._check_constraint_needs_G(constraint):
                return True

        # Make sure all variables are associated with a single conic constraint
        if any([count != 1 for count in self._qicsVarCone.values()]):
            return True

        # Make modifications to data to accomodate for not using G matrix
        import scipy

        self.int["G"] = scipy.sparse.csc_matrix((0, 0))
        self.int["h"] = None

        self._sortedQicsVarConePosition = sorted(
            self._qicsVarConePosition, key=self._qicsVarConePosition.get
        )
        self._expand_compact_op = self._get_expand_compact_all_op()

        return False

    def _import_problem(self):
        import scipy.sparse

        self._numVars = sum(var.dim for var in self.ext.variables.values())

        # QICS' internal problem representation is stateless; a number of
        # vectors and matrices is supplied each time a search is started.
        # These vectors and matrices are thus stored in self.int.
        self.int = {
            # Objective function coefficients.
            "c": numpy.zeros((self._numVars, 1)),

            # Linear equality left hand side.
            "A": scipy.sparse.csc_matrix((0, self._numVars)),

            # Linear equality right hand side.
            "b": numpy.zeros((0, 1)),

            # Conic inequality left hand side.
            "G": scipy.sparse.csc_matrix((0, self._numVars)),

            # Conic inequality right hand side.
            "h": numpy.zeros((0, 1)),

            # Cone definitions.
            "cones": [],

            # Objective offset.
            "offset": 0.0,
        }

        # Check if we can model problem without using G matrix
        self._use_G = self._check_use_G()

        # Import variables with their bounds as affine constraints.
        self._import_variables()

        # Set objective.
        self._import_objective()

        # Import constraints.
        for constraint in self.ext.constraints.values():
            self._import_constraint(constraint)

        if not self._use_G:
            self.int["A"] = self.int["A"] @ self._expand_compact_op
            self.int["c"] = self._expand_compact_op.T @ self.int["c"]

    def _update_problem(self):
        raise NotImplementedError

    def _solve(self):
        import qics
        import scipy

        options = {}

        # verbosity
        options["verbose"] = max(0, self.verbosity())

        # rel_ipm_opt_tol
        if self.ext.options.rel_ipm_opt_tol is not None:
            options["tol_gap"] = self.ext.options.rel_ipm_opt_tol

        # rel_prim_fsb_tol, rel_dual_fsb_tol
        feasibilityTols = [tol for tol in (self.ext.options.rel_prim_fsb_tol,
                self.ext.options.rel_dual_fsb_tol) if tol is not None]
        if feasibilityTols:
            options["tol_feas"] = min(feasibilityTols)

        # max_iterations
        if self.ext.options.max_iterations is not None:
            options["max_iter"] = self.ext.options.max_iterations
        else:
            options["max_iter"] = int(1e6)

        # timelimit
        if self.ext.options.timelimit is not None:
            options["max_time"] = self.ext.options.timelimit

        # Handle QICS-specific options.
        options.update(self.ext.options.qics_params)

        # Remove zero rows from A, and make sure corresponding b is consistent
        JP = list(set(self.int["A"].tocoo().row))
        IP = range(len(JP))
        VP = [1] * len(JP)
        shapeP = (len(IP), self.int["A"].shape[0])

        if any([not numpy.isclose(b, 0.) for (i, b) in enumerate(self.int["b"])
                if i not in JP]):
            return Solution(
                primals=None, duals=None, problem=self.ext, solver="PICOS",
                primalStatus=SS_INFEASIBLE, dualStatus=SS_UNKNOWN,
                problemStatus=PS_INFEASIBLE, vectorizedPrimals=True)

        P = scipy.sparse.csr_matrix((VP, (IP, JP)), shape=shapeP)
        self.int["A"] = P @ self.int["A"]
        self.int["b"] = P @ self.int["b"]

        # Attempt to solve the problem.
        with self._header(), self._stopwatch():
            model = qics.Model(**self.int)
            solver = qics.Solver(model, **options)
            result = solver.solve()

        # Retrieve primals.
        primals = {}
        if self.ext.options.primals is not False:
            x_opt = result["x_opt"]
            if not self._use_G:
                x_opt = self._expand_compact_op @ result["x_opt"]
            for variable in self.ext.variables.values():
                offset = self._qicsVarOffset[variable]
                primal = list(x_opt[offset : offset + variable.dim, 0])
                primals[variable] = primal

        # Retrieve duals.
        HypographConstraints = (
            QuantCondEntropyConstraint,
            MatrixGeoMeanHypoConstraint,
            TrMatrixGeoMeanHypoConstraint,
        )

        duals = {}
        if self.ext.options.duals is not False:
            for constraint in self.ext.constraints.values():
                if isinstance(constraint, DummyConstraint):
                    duals[constraint] = cvxopt.spmatrix(
                        [], [], [], constraint.size)
                    continue

                idx = self._qicsConIndices[constraint]

                if isinstance(constraint, AffineConstraint):
                    if constraint.is_equality():
                        dual = -cvxopt.matrix((P.T @ result["y_opt"])[idx, 0])
                        duals[constraint] = dual
                        continue

                qics_dual = result["z_opt"][idx]

                # Transform back duals which were cast using a QICS
                # compatible cone
                if isinstance(constraint, RSOCConstraint):
                    # RScone were cast as a SOcone on import, so transform the
                    # dual to a proper RScone dual.
                    qics_dual = [
                        qics_dual[0][0] + qics_dual[1][-1],
                        qics_dual[0][0] - qics_dual[1][-1],
                        2.0 * qics_dual[1][:-1, 0]
                    ]
                if isinstance(constraint, ExpConeConstraint):
                    # Exponential cone was cast as a CRE cone, so transform
                    # duals back to the proper exponential cone
                    qics_dual = [qics_dual[1], qics_dual[2], -qics_dual[0]]
                if isinstance(constraint, KullbackLeiblerConstraint):
                    if qics_dual[1].size == 1:
                        # CRE was cast as a CE cone, so transform duals back to
                        # the proper CRE cone
                        n = qics_dual[2].size
                        qics_dual = [
                            qics_dual[0],
                            qics_dual[2],
                            qics_dual[1] * numpy.ones((n, 1)) / n
                        ]
                if isinstance(constraint, QuantRelEntropyConstraint):
                    if qics_dual[1].size == 1:
                        # QRE was cast as a QE cone, so transform duals back to
                        # the proper QRE cone
                        n = qics_dual[2].shape[0]
                        qics_dual = [
                            qics_dual[0],
                            qics_dual[2],
                            qics_dual[1] * numpy.eye(n) / n
                        ]
                if isinstance(constraint, HypographConstraints):
                    qics_dual[0] = -qics_dual[0]

                # If SDP constraint, then dual is a matrix. All other
                # constraints are vectorized
                if isinstance(constraint, LMIConstraint):
                    dual = cvxopt.matrix(qics_dual[0])
                else:
                    dual_list = [dual_k.ravel() for dual_k in qics_dual]
                    dual = cvxopt.matrix(numpy.concatenate(dual_list))

                duals[constraint] = dual

        # Retrieve objective value.
        value = (result["p_obj"] + result["d_obj"]) / 2
        if self.ext.no.direction == "max":
            value = -value

        # Retrieve solution status.
        status = result["sol_status"]
        if status == "optimal" or status == "near_optimal":
            primalStatus = SS_OPTIMAL
            dualStatus = SS_OPTIMAL
            problemStatus = PS_FEASIBLE
        elif status == "pinfeas" or status == "near_pinfeas":
            primalStatus = SS_INFEASIBLE
            dualStatus = SS_UNKNOWN
            problemStatus = PS_INFEASIBLE
        elif status == "dinfeas" or status == "near_dinfeas":
            primalStatus = SS_UNKNOWN
            dualStatus = SS_INFEASIBLE
            problemStatus = PS_UNBOUNDED
        elif status == "illposed":
            primalStatus = SS_UNKNOWN
            dualStatus = SS_UNKNOWN
            problemStatus = PS_ILLPOSED
        elif status == "unknown":
            primalStatus = SS_PREMATURE
            dualStatus = SS_PREMATURE
            problemStatus = PS_UNKNOWN
        else:
            assert False, "Unknown solver status '{}'".format(status)

        return self._make_solution(
            value,
            primals,
            duals,
            primalStatus,
            dualStatus,
            problemStatus,
            {"qics_info": result if result else None},
        )


# --------------------------------------
__all__ = api_end(_API_START, globals())
