#pragma once
#include <iostream>
#include <vector>
#include <Eigen/Dense>
#include "LatticeSite.hpp"
using namespace Eigen;

/**
@brief This class constructs clusters of arbitrary order from pair neighbor lists.

@details
    Given the neighbor lists for each order, this class builds all clusters up
    to that order that involve a given site. Higher-order clusters are obtained
    by repeated set intersection: a site can be added to a cluster only if it is
    a neighbor of every site already in it, which is precisely the intersection
    of the neighbor lists of those sites.
*/

class ManyBodyNeighborList
{
  public:
    ManyBodyNeighborList() {}

    /// Constructs all clusters up to the given order that involve a given site.
    std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> build(const std::vector<std::vector<std::vector<LatticeSite>>> &,
                                                                                     int index,
                                                                                     bool) const;

    /**
    @details Return the lattice sites that appear in two lists of lattice sites.
    @param firstNeighbors list of lattice sites
    @param secondNeighbors another list of lattice sites
    **/
    std::vector<LatticeSite> getIntersection(const std::vector<LatticeSite> &firstNeighbors,
                                             const std::vector<LatticeSite> &secondNeighbors) const
    {
        std::vector<LatticeSite> intersection;
        intersection.reserve(firstNeighbors.size());
        std::set_intersection(firstNeighbors.begin(), firstNeighbors.end(),
                              secondNeighbors.begin(), secondNeighbors.end(),
                              std::back_inserter(intersection));
        return intersection;
    }

  private:
    /// Extends the clusters built so far by one more site, recursively.
    void combineToHigherOrder(const std::vector<std::vector<LatticeSite>> &neighborList,
                              std::vector<std::pair<std::vector<LatticeSite>,
                                                    std::vector<LatticeSite>>> &manyBodyNeighborIndices,
                              const std::vector<LatticeSite> &neighbors,
                              std::vector<LatticeSite> &currentOriginalNeighbors,
                              bool saveBothWays,
                              const size_t maxOrder) const;

    /// Adds the given offset to all lattice sites in the list.
    void translateAllNeighbors(std::vector<LatticeSite> &neighbors, const Vector3i &unitCellOffset) const;

    /// Adds the singlet formed by the given site.
    void addSinglet(const int, std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> &) const;

    /// Adds all pairs that involve the given site.
    void addPairs(const int, const std::vector<std::vector<LatticeSite>> &, std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> &, bool) const;

    /// Returns the lattice sites that are larger than the given site.
    std::vector<LatticeSite> getFilteredNeighbors(const std::vector<LatticeSite> &, const LatticeSite &) const;
};
