#pragma once

#include <cstdint>
#include <unordered_map>
#include <vector>

#include <Eigen/Dense>

#include "Structure.hpp"
#include "VectorOperations.hpp"

using namespace Eigen;

/**
@brief Maps between supercell site indices and primitive-frame lattice sites.
@details
    A supercell of a primitive structure is described by an integer matrix M
    such that S = M P, where the rows of P and S are the lattice vectors of
    the primitive cell and the supercell.
    Every site of the supercell then corresponds to a pair of a basis index
    (a site index of the primitive structure) and a cell offset in units of
    the primitive lattice vectors, and two offsets that differ by an integer
    combination of the rows of M describe the same supercell site.

    This class holds that correspondence for one supercell.
    It is built once, from positions, using the same float machinery that
    locates sites elsewhere in the core (findLatticeSiteByPosition), and
    afterwards answers lookups with integer arithmetic only: offsets are
    wrapped modulo the rows of M, and the wrapped offsets are mapped to a
    contiguous range of cell indices so that lookups on the evaluation path
    are plain array reads.

    The wrapped representative of an offset o is o - m M, where the integer
    row vector m is obtained componentwise as the floor of the fractional
    coordinates of o with respect to M, computed exactly from the adjugate
    and the determinant of M.
*/
class LatticeMap
{
public:
    /// Constructor.
    LatticeMap(const Structure &primitiveStructure,
               const Structure &supercell,
               const double fractionalPositionTolerance);

    /// Returns the number of primitive cells in the supercell.
    size_t numberOfCells() const { return _cellOffsets.size(); }

    /// Returns the number of sites in the primitive structure.
    size_t numberOfBasisSites() const { return _numberOfBasisSites; }

    /// Returns the number of sites in the supercell.
    size_t numberOfSites() const { return _basisIndexOfSite.size(); }

    /// Returns the supercell site index of the site with the given basis
    /// index and cell offset; the offset may lie outside the supercell and
    /// is wrapped.
    int32_t siteIndex(const size_t basisIndex, const Vector3i &cellOffset) const
    {
        return siteIndexFromCellIndex(basisIndex, cellIndex(cellOffset));
    }

    /// Returns the cell index of the given cell offset; the offset may lie
    /// outside the supercell and is wrapped.
    int32_t cellIndex(const Vector3i &cellOffset) const;

    /// Returns the supercell site index for a basis index and a cell index,
    /// with no wrapping; this is the lookup used on the evaluation path.
    int32_t siteIndexFromCellIndex(const size_t basisIndex, const int32_t cellIndex) const
    {
        return _siteIndices[(size_t)cellIndex * _numberOfBasisSites + basisIndex];
    }

    /// Returns the cell index of the primitive cell that contains the given supercell site.
    int32_t cellIndexOfSite(const size_t siteIndex) const { return _cellIndexOfSite[siteIndex]; }

    /// Returns the basis index of the given supercell site.
    int32_t basisIndexOfSite(const size_t siteIndex) const { return _basisIndexOfSite[siteIndex]; }

    /// Returns the stored representative offset of the cell with the given cell index.
    const Vector3i &cellOffset(const size_t cellIndex) const { return _cellOffsets[cellIndex]; }

    /// Returns the representative of the given cell offset, wrapped modulo the supercell.
    Vector3i wrap(const Vector3i &cellOffset) const;

private:
    /// Number of sites in the primitive structure.
    size_t _numberOfBasisSites;

    /// Integer matrix M relating the two cell metrics through S = M P.
    Matrix3i _supercellMatrix;

    /// Adjugate of M, satisfying adj(M) M = M adj(M) = det(M) I.
    Matrix<int64_t, 3, 3> _adjugate;

    /// Determinant of M.
    int64_t _determinant;

    /// Supercell site index per (cell index, basis index), cell-major.
    std::vector<int32_t> _siteIndices;

    /// Representative wrapped offset per cell index, in cell index order.
    std::vector<Vector3i> _cellOffsets;

    /// Cell index per wrapped offset; used when wrapping cannot be avoided.
    std::unordered_map<Vector3i, int32_t, Vector3iHash> _cellIndexOfWrappedOffset;

    /// Cell index of the primitive cell that contains each supercell site.
    std::vector<int32_t> _cellIndexOfSite;

    /// Basis index of each supercell site.
    std::vector<int32_t> _basisIndexOfSite;
};
