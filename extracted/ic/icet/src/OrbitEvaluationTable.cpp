#include "OrbitEvaluationTable.hpp"

#include <algorithm>
#include <unordered_map>

namespace
{

/// Returns true if the given cluster, as an ordered list of sites, is
/// already present in the list of clusters.
/// Site order matters, exactly as in Orbit::contains, because for a
/// multi-component cluster space the position of a site within the cluster
/// determines which cluster vector element an occupation pattern maps to.
bool containsCluster(const std::vector<std::vector<LatticeSite>> &clusters,
                     const std::vector<LatticeSite> &cluster)
{
    return std::find(clusters.begin(), clusters.end(), cluster) != clusters.end();
}

} // namespace

/**
@details
    Builds the evaluation tables for all orbits of the primitive orbit list.

    The extended clusters of each orbit are generated exactly the way
    LocalOrbitListGenerator::getLocalOrbitList generates the additional
    clusters of a self-contained local orbit list: for each base cluster,
    every translation with one site in the anchor cell
    (OrbitList::getSitesTranslatedToUnitcell) is appended unless an equal
    cluster, in the same site order, is already present.
    That construction does not depend on the anchor cell, which is what
    makes one table valid for every cell of the supercell.
    Keeping the same generation order also keeps the enumeration order of
    clusters in the per-basis local views identical to the order in which
    the corresponding clusters appear in a self-contained local orbit list,
    so the floating point accumulation order of cluster counts is preserved.

    The weight of a per-basis entry is 1 / n with n the number of slots of
    the cluster whose relative offset is an integer combination of the rows
    of the supercell matrix (checked through LatticeMap::wrap) and whose
    basis index matches; those are exactly the slots that resolve to the
    anchor site itself, matching what
    Cluster::getCountOfOccurencesOfSiteIndex counts on a transformed
    cluster.

@param primitiveOrbitList orbit list of the primitive structure
@param latticeMap map for the supercell the tables are built for
*/
EvaluationTables buildEvaluationTables(const OrbitList &primitiveOrbitList,
                                       const LatticeMap &latticeMap)
{
    EvaluationTables tables;
    std::unordered_map<Vector3i, int32_t, Vector3iHash> relativeOffsetIds;

    for (size_t orbitIndex = 0; orbitIndex < primitiveOrbitList.size(); orbitIndex++)
    {
        const Orbit &orbit = primitiveOrbitList.getOrbit(orbitIndex);
        OrbitEvaluationTable table;
        table.order = (int)orbit.order();

        // Collect the base clusters, in orbit order.
        std::vector<std::vector<LatticeSite>> clusters;
        clusters.reserve(orbit.size());
        for (const Cluster &cluster : orbit.clusters())
        {
            clusters.push_back(cluster.latticeSites());
        }
        table.numberOfBaseClusters = clusters.size();

        // Append the extended clusters, replicating the self-contained
        // construction of LocalOrbitListGenerator::getLocalOrbitList.
        for (size_t c = 0; c < table.numberOfBaseClusters; c++)
        {
            std::vector<std::vector<LatticeSite>> translatedSiteGroups =
                primitiveOrbitList.getSitesTranslatedToUnitcell(clusters[c], false);
            for (const auto &translatedSites : translatedSiteGroups)
            {
                if (!containsCluster(clusters, translatedSites))
                {
                    clusters.push_back(translatedSites);
                }
            }
        }

        // Turn the clusters into slots.
        table.slotBasisIndices.reserve(clusters.size() * table.order);
        table.slotRelativeOffsetIds.reserve(clusters.size() * table.order);
        for (const auto &cluster : clusters)
        {
            for (const LatticeSite &site : cluster)
            {
                table.slotBasisIndices.push_back((int32_t)site.index());
                const Vector3i &offset = site.unitcellOffset();
                auto inserted = relativeOffsetIds.emplace(offset, (int32_t)tables.relativeOffsets.size());
                if (inserted.second)
                {
                    tables.relativeOffsets.push_back(offset);
                }
                table.slotRelativeOffsetIds.push_back(inserted.first->second);
            }
        }

        // Build the per-basis local views.
        table.localEntriesPerBasis.resize(latticeMap.numberOfBasisSites());
        for (size_t c = 0; c < clusters.size(); c++)
        {
            for (const LatticeSite &site : clusters[c])
            {
                if (!site.unitcellOffset().isZero())
                {
                    continue;
                }
                // The cluster contains this basis site in the anchor cell,
                // so it enters that site's local view, weighted by 1 / n
                // with n counting every slot that resolves to the same
                // supercell site, including periodic images in small
                // supercells.
                int occurrences = 0;
                for (const LatticeSite &other : clusters[c])
                {
                    if (other.index() == site.index() &&
                        latticeMap.wrap(other.unitcellOffset()).isZero())
                    {
                        occurrences++;
                    }
                }
                table.localEntriesPerBasis[site.index()].push_back(
                    {(int32_t)c, 1.0 / (double)occurrences});
            }
        }

        tables.orbitTables.push_back(std::move(table));
    }

    // Precompute the cell reached from each cell by each relative offset.
    size_t numberOfOffsets = tables.relativeOffsets.size();
    tables.neighborCellIndices.resize(latticeMap.numberOfCells() * numberOfOffsets);
    for (size_t cellIndex = 0; cellIndex < latticeMap.numberOfCells(); cellIndex++)
    {
        for (size_t offsetId = 0; offsetId < numberOfOffsets; offsetId++)
        {
            tables.neighborCellIndices[cellIndex * numberOfOffsets + offsetId] =
                latticeMap.cellIndex(latticeMap.cellOffset(cellIndex) + tables.relativeOffsets[offsetId]);
        }
    }
    return tables;
}
