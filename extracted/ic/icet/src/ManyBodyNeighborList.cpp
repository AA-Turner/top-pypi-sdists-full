#include "ManyBodyNeighborList.hpp"

/**
@details
    This function uses @a neighborLists to construct all possible
    neighbors up to the given order. The output will be:
    @code{.cpp}
    std::vector<std::pair<originalNeighbors, manyNeighbors>>
    @endcode

    The many body neighbors can be retrieved by doing:
    @code{.cpp}
    for (const auto nbr : manyBodyNeighborIndices)
    {
        std::vector<std::pair<int,Vector3d>> neighbors = nbr.first; // this are the first original neighbors
        for(const auto manynbr : nbr.second)
        {
            manyBodyNeighbor = neighbors;
            manyBodyNeighbor.append(manynbr);
        }
    }
    @endcode

    This means that if @a originalNeighbors.size()==2 then for each lattice site in @a manyNeighbors
    you can combine it with @a originalNeighbors to get all triplets that have these first two original neighbors (lattice indices).

    @param neighborLists list of neighbor lists
    @param index index of the site for which to construct the clusters
    @param saveBothWays if true then both @a i,j,k and @a j,i,k etc.. will be saved; otherwise only @a i,j,k will be saved if @a i<j<k.
*/

std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> ManyBodyNeighborList::build(const std::vector<std::vector<std::vector<LatticeSite>>> &neighborLists,
                                                                                                      int index,
                                                                                                      bool saveBothWays) const
{

    if (neighborLists.empty())
    {
        throw std::runtime_error("Error: neighbor list vector is empty in ManyBodyNeighborList::build");
    }
    std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> manyBodyNeighborIndices;

    addSinglet(index, manyBodyNeighborIndices);
    addPairs(index, neighborLists[0], manyBodyNeighborIndices, saveBothWays);

    for (size_t order = 2; order < neighborLists.size() + 2; order++)
    {
        const std::vector<LatticeSite> &neighbors = neighborLists[order - 2][index];
        Vector3i zeroVector = {0, 0, 0};
        std::vector<LatticeSite> currentOriginalNeighbors;
        currentOriginalNeighbors.push_back(LatticeSite(index, zeroVector)); // index is always first index

        combineToHigherOrder(neighborLists[order - 2], manyBodyNeighborIndices, neighbors, currentOriginalNeighbors, saveBothWays, order);
    }
    return manyBodyNeighborIndices;
}

/// Adds singlet from the index to manyBodyNeighborIndices
void ManyBodyNeighborList::addSinglet(const int index,
                                      std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> &manyBodyNeighborIndices) const
{
    Vector3i zeroVector = {0, 0, 0};
    LatticeSite latticeNeighborSinglet = LatticeSite(index, zeroVector);
    std::vector<LatticeSite> singletLatticeSites;
    singletLatticeSites.push_back(latticeNeighborSinglet);

    std::vector<LatticeSite> latticeSitesEmpty;
    manyBodyNeighborIndices.push_back(std::make_pair(singletLatticeSites, latticeSitesEmpty));
}

/// Add all pairs originating from index using neighborList
void ManyBodyNeighborList::addPairs(const int index,
                                    const std::vector<std::vector<LatticeSite>> &neighborList,
                                    std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> &manyBodyNeighborIndices,
                                    bool saveBothWays) const

{
    Vector3i zeroVector = {0, 0, 0};
    LatticeSite latticeNeighborIndex = LatticeSite(index, zeroVector);

    std::vector<LatticeSite> firstSite = {latticeNeighborIndex};
    std::vector<LatticeSite> neighbors = neighborList[index];
    // exclude smaller neighbors
    if (!saveBothWays)
    {
        neighbors = getFilteredNeighbors(neighbors, latticeNeighborIndex);
    }

    if (neighbors.size() == 0)
    {
        return;
    }
    manyBodyNeighborIndices.push_back(std::make_pair(firstSite, neighbors));
}

/**
@details
    Extends the partial cluster in @a currentOriginalNeighbors by one site at a
    time, recursing until clusters of order @a maxOrder have been reached.

    Each candidate site is taken from @a neighbors, which holds the sites that
    are neighbors of every site already in the partial cluster. For a candidate
    site j the neighbors of j are looked up in @a neighborList, translated by
    the unit cell offset of j, and intersected with @a neighbors. The result is
    the set of sites that are neighbors of the extended partial cluster, and it
    serves as the candidate set for the next level of recursion.

    Once the partial cluster holds maxOrder - 1 sites, the pair consisting of
    the partial cluster and its non-empty intersection is appended to
    @a manyBodyNeighborIndices. Combining the partial cluster with any one site
    from the intersection then yields a cluster of order maxOrder.

    Unless @a saveBothWays is set, candidate sites that are smaller than the
    site added last are skipped, so that each cluster is generated only once.

@param neighborList neighbor list for the order under construction
@param manyBodyNeighborIndices list of clusters to which the results are appended
@param neighbors sites that are neighbors of all sites in the partial cluster
@param currentOriginalNeighbors the partial cluster built up so far
@param saveBothWays if true, clusters are generated in every site ordering rather than only one
@param maxOrder the order of the clusters to be constructed
*/
void ManyBodyNeighborList::combineToHigherOrder(const std::vector<std::vector<LatticeSite>> &neighborList,
                                                std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> &manyBodyNeighborIndices,
                                                const std::vector<LatticeSite> &neighbors,
                                                std::vector<LatticeSite> &currentOriginalNeighbors,
                                                bool saveBothWays,
                                                const size_t maxOrder) const
{

    for (const auto &neighbor : neighbors)
    {
        // Skip neighbors that are smaller than the last added site, so that
        // each cluster is only generated once. When saving both ways the
        // first site is excluded from this comparison.
        if ((!saveBothWays || currentOriginalNeighbors.size() > 1) &&
            neighbor < currentOriginalNeighbors.back())
        {
            continue;
        }

        auto originalNeighborCopy = currentOriginalNeighbors;
        originalNeighborCopy.push_back(neighbor); // put neighbor in originalNeighbors

        auto neighborsOfNeighbor = neighborList[neighbor.index()];

        // translate the neighbors
        translateAllNeighbors(neighborsOfNeighbor, neighbor.unitcellOffset());

        // exclude smaller neighbors
        if (!saveBothWays)
        {
            neighborsOfNeighbor = getFilteredNeighbors(neighborsOfNeighbor, neighbor);
        }

        // construct the intersection
        const auto intersection = getIntersection(neighbors, neighborsOfNeighbor);

        if (originalNeighborCopy.size() + 1 < maxOrder)
        {
            combineToHigherOrder(neighborList, manyBodyNeighborIndices, intersection, originalNeighborCopy, saveBothWays, maxOrder);
        }

        if (intersection.size() > 0 && originalNeighborCopy.size() == (maxOrder - 1))
        {
            manyBodyNeighborIndices.push_back(std::make_pair(originalNeighborCopy, intersection));
        }
    }
}

/**
@details
    Returns the lattice sites in the input list that are larger than the given
    site. Since the list is always sorted, it is enough to find the first site
    that is larger than the given one and return everything from there on.
@param neighbors sorted list of lattice sites
@param site site relative to which to filter
*/
std::vector<LatticeSite> ManyBodyNeighborList::getFilteredNeighbors(const std::vector<LatticeSite> &neighbors,
                                                                    const LatticeSite &site) const
{
    auto first = std::upper_bound(neighbors.begin(), neighbors.end(), site);
    return std::vector<LatticeSite>(first, neighbors.end());
}

/**
@details Adds the given offset to the unit cell offset of all lattice sites in the list.
@param neighbors list of lattice sites to translate
@param unitCellOffset offset to add, in units of the lattice vectors
*/
void ManyBodyNeighborList::translateAllNeighbors(std::vector<LatticeSite> &neighbors, const Vector3i &unitCellOffset) const
{
    for (auto &latticeSite : neighbors)
    {
        latticeSite.addUnitcellOffset(unitCellOffset);
    }
}
