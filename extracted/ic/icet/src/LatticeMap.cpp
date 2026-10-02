#include "LatticeMap.hpp"

#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <sstream>

namespace
{

/// Floor division, i.e. division that rounds toward negative infinity for
/// any sign combination, unlike the truncation of the built-in operator.
int64_t floorDivide(const int64_t numerator, const int64_t denominator)
{
    int64_t quotient = numerator / denominator;
    if (numerator % denominator != 0 && (numerator < 0) != (denominator < 0))
    {
        quotient--;
    }
    return quotient;
}

/// Adjugate of a 3x3 integer matrix, i.e. the transpose of its cofactor
/// matrix, which satisfies adj(M) M = M adj(M) = det(M) I exactly in
/// integer arithmetic.
Matrix<int64_t, 3, 3> adjugate(const Matrix3i &m)
{
    Matrix<int64_t, 3, 3> adj;
    adj(0, 0) = (int64_t)m(1, 1) * m(2, 2) - (int64_t)m(1, 2) * m(2, 1);
    adj(0, 1) = (int64_t)m(0, 2) * m(2, 1) - (int64_t)m(0, 1) * m(2, 2);
    adj(0, 2) = (int64_t)m(0, 1) * m(1, 2) - (int64_t)m(0, 2) * m(1, 1);
    adj(1, 0) = (int64_t)m(1, 2) * m(2, 0) - (int64_t)m(1, 0) * m(2, 2);
    adj(1, 1) = (int64_t)m(0, 0) * m(2, 2) - (int64_t)m(0, 2) * m(2, 0);
    adj(1, 2) = (int64_t)m(0, 2) * m(1, 0) - (int64_t)m(0, 0) * m(1, 2);
    adj(2, 0) = (int64_t)m(1, 0) * m(2, 1) - (int64_t)m(1, 1) * m(2, 0);
    adj(2, 1) = (int64_t)m(0, 1) * m(2, 0) - (int64_t)m(0, 0) * m(2, 1);
    adj(2, 2) = (int64_t)m(0, 0) * m(1, 1) - (int64_t)m(0, 1) * m(1, 0);
    return adj;
}

} // namespace

/**
@details
    Builds the map for one supercell.
    The integer matrix M with S = M P is obtained from the two cell metrics,
    and every supercell site is located in the primitive frame with
    findLatticeSiteByPosition, the same float machinery the rest of the core
    uses for this purpose.
    The construction verifies that every (basis index, wrapped offset) pair
    maps to exactly one supercell site and vice versa, so an inconsistent
    input fails here, loudly, rather than during evaluation.
@param primitiveStructure primitive structure underlying the supercell
@param supercell supercell structure to build the map for
@param fractionalPositionTolerance tolerance applied when comparing positions in fractional coordinates
*/
LatticeMap::LatticeMap(const Structure &primitiveStructure,
                       const Structure &supercell,
                       const double fractionalPositionTolerance)
    : _numberOfBasisSites(primitiveStructure.size())
{
    // Extract the integer matrix M from S = M P.
    Matrix3d supercellMatrixAsDoubles = supercell.getCell() * primitiveStructure.getCell().inverse();
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            double rounded = std::round(supercellMatrixAsDoubles(i, j));
            if (std::abs(supercellMatrixAsDoubles(i, j) - rounded) > fractionalPositionTolerance)
            {
                std::ostringstream msg;
                msg << "The cell metric of the supercell is not an integer combination"
                    << " of the primitive lattice vectors (LatticeMap)." << std::endl
                    << "supercell matrix: " << std::endl
                    << supercellMatrixAsDoubles;
                throw std::runtime_error(msg.str());
            }
            _supercellMatrix(i, j) = (int)rounded;
        }
    }
    _adjugate = adjugate(_supercellMatrix);
    _determinant = (int64_t)_supercellMatrix.cast<int64_t>().determinant();
    if (_determinant == 0)
    {
        throw std::runtime_error("The supercell matrix is singular (LatticeMap)");
    }

    size_t expectedNumberOfCells = (size_t)std::abs(_determinant);
    if (expectedNumberOfCells * _numberOfBasisSites != supercell.size())
    {
        std::ostringstream msg;
        msg << "The number of sites in the supercell does not match the cell metrics"
            << " (LatticeMap)." << std::endl
            << "sites in supercell: " << supercell.size() << std::endl
            << "sites expected from the cell metrics: "
            << expectedNumberOfCells * _numberOfBasisSites;
        throw std::runtime_error(msg.str());
    }

    // Locate every supercell site in the primitive frame.
    _basisIndexOfSite.resize(supercell.size());
    _cellIndexOfSite.resize(supercell.size());
    std::vector<Vector3i> wrappedOffsetOfSite(supercell.size());
    for (size_t i = 0; i < supercell.size(); i++)
    {
        LatticeSite primitiveSite = primitiveStructure.findLatticeSiteByPosition(
            supercell.positionByIndex(i), fractionalPositionTolerance);
        _basisIndexOfSite[i] = (int32_t)primitiveSite.index();
        wrappedOffsetOfSite[i] = wrap(primitiveSite.unitcellOffset());
    }

    // Assign cell indices to the wrapped offsets in a deterministic order.
    _cellOffsets.assign(wrappedOffsetOfSite.begin(), wrappedOffsetOfSite.end());
    std::sort(_cellOffsets.begin(), _cellOffsets.end(), Vector3iCompare());
    _cellOffsets.erase(std::unique(_cellOffsets.begin(), _cellOffsets.end()), _cellOffsets.end());
    if (_cellOffsets.size() != expectedNumberOfCells)
    {
        std::ostringstream msg;
        msg << "The number of distinct wrapped cell offsets does not match the"
            << " determinant of the supercell matrix (LatticeMap)." << std::endl
            << "distinct offsets: " << _cellOffsets.size() << std::endl
            << "determinant: " << expectedNumberOfCells;
        throw std::runtime_error(msg.str());
    }
    for (size_t cellIndex = 0; cellIndex < _cellOffsets.size(); cellIndex++)
    {
        _cellIndexOfWrappedOffset[_cellOffsets[cellIndex]] = (int32_t)cellIndex;
    }

    // Fill the dense site table.
    // No entry can remain at -1 afterwards: the number of sites equals the
    // size of the table (checked above) and a duplicate throws below, so by
    // the pigeonhole principle every entry is written exactly once.
    _siteIndices.assign(_cellOffsets.size() * _numberOfBasisSites, -1);
    for (size_t i = 0; i < supercell.size(); i++)
    {
        int32_t cellIndex = _cellIndexOfWrappedOffset.at(wrappedOffsetOfSite[i]);
        _cellIndexOfSite[i] = cellIndex;
        int32_t &entry = _siteIndices[(size_t)cellIndex * _numberOfBasisSites + _basisIndexOfSite[i]];
        if (entry != -1)
        {
            std::ostringstream msg;
            msg << "Two supercell sites map to the same primitive-frame site (LatticeMap)."
                << std::endl
                << "site indices: " << entry << " and " << i;
            throw std::runtime_error(msg.str());
        }
        entry = (int32_t)i;
    }
}

/**
@details
    Returns the representative of the given cell offset, wrapped modulo the
    rows of the supercell matrix M.
    The fractional coordinates of the offset with respect to M are computed
    exactly, as the offset times the adjugate of M over the determinant, and
    their componentwise floor gives the integer combination of rows of M
    that is subtracted.
@param cellOffset cell offset in units of the primitive lattice vectors
*/
Vector3i LatticeMap::wrap(const Vector3i &cellOffset) const
{
    Vector3i multiple;
    for (int j = 0; j < 3; j++)
    {
        int64_t numerator = 0;
        for (int i = 0; i < 3; i++)
        {
            numerator += (int64_t)cellOffset[i] * _adjugate(i, j);
        }
        multiple[j] = (int)floorDivide(numerator, _determinant);
    }
    Vector3i wrapped;
    for (int j = 0; j < 3; j++)
    {
        int64_t component = cellOffset[j];
        for (int i = 0; i < 3; i++)
        {
            component -= (int64_t)multiple[i] * _supercellMatrix(i, j);
        }
        wrapped[j] = (int)component;
    }
    return wrapped;
}

/**
@details
    Returns the cell index of the given cell offset, which may lie outside
    the supercell and is wrapped first.
    An offset whose wrapped representative is unknown to the map indicates an
    inconsistent internal state rather than invalid input, since the wrapped
    representatives cover the supercell completely by construction.
@param cellOffset cell offset in units of the primitive lattice vectors
*/
int32_t LatticeMap::cellIndex(const Vector3i &cellOffset) const
{
    try
    {
        return _cellIndexOfWrappedOffset.at(wrap(cellOffset));
    }
    catch (const std::out_of_range &)
    {
        std::ostringstream msg;
        msg << "Failed to retrieve the cell index for cell offset "
            << cellOffset[0] << " " << cellOffset[1] << " " << cellOffset[2]
            << " (LatticeMap::cellIndex)";
        throw std::out_of_range(msg.str());
    }
}
