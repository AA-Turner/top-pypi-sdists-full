#pragma once

#include <cstdint>
#include <vector>

#include <Eigen/Dense>

#include "LatticeMap.hpp"
#include "OrbitList.hpp"

using namespace Eigen;

/**
@brief Describes the clusters of one orbit in one representative cell.
@details
    The clusters of an orbit repeat identically in every primitive cell of a
    supercell, so one table of them, expressed relative to an unspecified
    anchor cell, stands in for the copies that would otherwise be stored per
    cell.
    Each cluster site is a slot holding a basis index and the id of a
    relative cell offset; a LatticeMap turns (basis index, anchor cell +
    relative offset) into a supercell site index at evaluation time.

    The base clusters are those of the primitive orbit, anchored per the
    convention in planning/ordering-specification.md; iterating them over
    all anchor cells enumerates every cluster of the supercell exactly once,
    which is what the full cluster vector needs.
    The extended clusters append the translations that put each remaining
    site of a base cluster in the anchor cell, so that base plus extended
    clusters together cover every cluster that touches the anchor cell,
    which is what local and change evaluations need.
    Per basis index, the local entries list the clusters (base and extended)
    that contain that basis site in the anchor cell itself, each with the
    weight 1 / n, where n is the number of slots of the cluster that resolve
    to that same supercell site; n exceeds one only when the supercell is
    small enough that a cluster contains a site together with one of its
    periodic images.
*/
struct OrbitEvaluationTable
{
    /// One cluster of the per-basis local view: a cluster id and its weight.
    struct LocalEntry
    {
        int32_t clusterIndex;
        double unit;
    };

    /// Number of sites per cluster.
    int order;

    /// Number of base clusters; these occupy the cluster indices [0, numberOfBaseClusters).
    size_t numberOfBaseClusters;

    /// Basis index per slot, cluster-major; cluster c occupies slots [c order, (c + 1) order).
    std::vector<int32_t> slotBasisIndices;

    /// Relative-offset id per slot, indexing EvaluationTables::relativeOffsets.
    std::vector<int32_t> slotRelativeOffsetIds;

    /// Clusters containing the given basis site in the anchor cell, per basis index.
    std::vector<std::vector<LocalEntry>> localEntriesPerBasis;

    /// Returns the total number of clusters (base and extended).
    size_t numberOfClusters() const { return order == 0 ? 0 : slotBasisIndices.size() / order; }
};

/**
@brief The evaluation tables of all orbits, with their shared offset registry.
@details
    The relative offsets that occur in any slot of any orbit are collected
    into one list, so that the cell a slot lands in, relative to an anchor
    cell, can be precomputed once per (anchor cell, relative offset) pair.
    That precomputation is neighborCellIndices, a dense array of shape
    (number of cells, number of relative offsets), which reduces the
    per-slot work at evaluation time to two array reads.
*/
struct EvaluationTables
{
    /// One table per orbit, aligned with the orbits of the primitive orbit list.
    std::vector<OrbitEvaluationTable> orbitTables;

    /// The distinct relative cell offsets referenced by the slots of any orbit.
    std::vector<Vector3i> relativeOffsets;

    /// Cell index reached from each cell by each relative offset, cell-major.
    std::vector<int32_t> neighborCellIndices;
};

/// Builds the evaluation tables for the given primitive orbit list and supercell map.
EvaluationTables buildEvaluationTables(const OrbitList &primitiveOrbitList,
                                       const LatticeMap &latticeMap);
