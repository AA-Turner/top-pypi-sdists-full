#pragma once

#include <cstddef>
#include <map>
#include <unordered_set>
#include <vector>

#include "Cluster.hpp"
#include "LatticeSite.hpp"
#include "ManyBodyNeighborList.hpp"
#include "Orbit.hpp"
#include "Structure.hpp"
#include "Symmetry.hpp"
#include "VectorOperations.hpp"

/**
@brief Groups radii that lie within a tolerance of one another.
@details
    Returns, for each radius, the index of the group it belongs to, where
    groups are numbered in ascending order of radius.
    A new group starts wherever the gap to the next smaller radius exceeds the
    tolerance, so radii that differ only by numerical noise share a group while
    radii belonging to different shells do not.

    Grouping once is what makes the ordering of orbits well defined.
    Testing "within tolerance" pairwise instead is not transitive, since a
    radius can lie within the tolerance of two others that do not lie within
    the tolerance of each other, and a comparison built on a relation that is
    not transitive is not a strict weak ordering, which std::sort requires.
    Where no such chain occurs, and the radii of a cluster space are normally
    either equal up to numerical noise or far apart, this yields exactly the
    grouping a pairwise test implies.
@param radii radii to group
@param tolerance largest gap between neighboring radii of one group
*/
std::vector<size_t> groupRadiiWithinTolerance(const std::vector<double> &radii,
                                              const double tolerance);

/**
@brief This class serves as a container for a sorted list of orbits and provides associated functionality.

@details
    An orbit list is immutable once constructed. The Python-facing editing
    operations, pruning and merging, are provided as the const member functions
    withoutOrbits, withoutInactiveOrbits, and withMergedOrbits, each of which
    returns a new orbit list and leaves this one untouched. Anything that holds
    an orbit list, in particular a ClusterExpansionCalculator, therefore keeps
    the model it was constructed with, and an alias can never turn into a
    mutation at a distance.

    Invariants
    ----------

    The following properties hold for every orbit list this class produces.
    They are checked by checkInvariants, which every constructor and every
    member function that returns a new orbit list calls on its result, since
    the cost is paid once per orbit list rather than per evaluation.

    1. Every orbit holds at least one cluster. The representative cluster of an
       orbit is its first cluster, so this is what makes a representative exist.
    2. Every cluster of an orbit has the same order as the representative
       cluster of that orbit.
    3. The orbits appear in non-decreasing order of cluster order. The cluster
       vector is laid out orbit by orbit in this order.
    4. Every cluster vector element has a multi-component vector as long as the
       cluster order, at least one site permutation, and a positive
       multiplicity.
    5. Every site index of every cluster lies within the structure the orbit
       list is based on.
    6. The reference lattice sites, that is the first column of the matrix of
       equivalent sites, are unique.

    Properties 5 and 6 are checked only for an orbit list that carries a
    structure and a matrix of equivalent sites, which is the case for the
    primitive orbit list produced by the geometry constructor below. The
    supercell orbit lists that LocalOrbitListGenerator derives from it carry
    neither, and their clusters refer to sites of the supercell rather than of
    the primitive structure.

    Three properties that one might expect here are deliberately absent.

    - **Clusters are not all anchored in the unit cell at the origin.** What
      appendOrbitFromRows adds is the lowest translation of a cluster, which
      serves as a canonical label, whereas the translation that demonstrates
      membership of the orbit is a different one whenever the lowest
      translation happens to sort below it. Both of the case-matrix systems
      with more than one site in the primitive cell contain such clusters, so
      this is ordinary rather than exceptional.
    - **The ordering of the sites within a cluster relative to the
      representative cluster is not checked.** Establishing it is what
      permuteClustersToMatchRepresentative does, and verifying it independently
      costs the same factorial search that produced it.
    - **Only the first of the four sort keys of OrbitList::sort is checked.**
      The second key compares radii through a tolerance window and is not
      transitive, so a chain of orbits with near-tied radii can leave output
      that violates it, and checking it would reject a cluster space that works
      (see planning/ordering-specification.md). Merging also changes the third
      and fourth keys of the merged orbit legitimately. The order key is exact,
      transitive, and preserved by both pruning and merging.
*/

class OrbitList
{
public:
    /// Empty constructor.
    OrbitList(){};

    /// Constructs orbit list from a set of neighbor lists, a matrix of equivalent sites, and a structure.
    OrbitList(const Structure &,
              const std::vector<std::vector<LatticeSite>> &,
              const std::vector<std::vector<std::vector<LatticeSite>>> &,
              const double);

    /// Constructs an orbit list from orbits that have already been assembled.
    explicit OrbitList(std::vector<Orbit>);

    /// Checks the invariants listed in the class description and throws if one of them is violated.
    void checkInvariants() const;

    /// Returns a copy of this orbit list with the orbits at the given indices removed.
    OrbitList withoutOrbits(const std::vector<size_t> &) const;

    /// Returns a copy of this orbit list with the orbits that have inactive sites removed.
    OrbitList withoutInactiveOrbits() const;

    /// Returns a copy of this orbit list with each group of orbits merged into its first member.
    OrbitList withMergedOrbits(const std::map<size_t, std::vector<size_t>> &) const;

    /// Returns the orbit of the given index.
    const Orbit &getOrbit(unsigned int) const;

    /// Returns the number of orbits.
    size_t size() const { return _orbits.size(); }

    /// Returns all translations of the given sites for which at least one site
    /// lies in the unit cell at the origin.
    std::vector<std::vector<LatticeSite>> getSitesTranslatedToUnitcell(const std::vector<LatticeSite> &,
                                                                       bool sort = true) const;

    /// Returns symmetry related site groups via _matrixOfEquivalentSites and translations
    std::vector<std::vector<LatticeSite>> getSymmetryRelatedSiteGroups(const std::vector<LatticeSite> &) const;

    /// Returns the matrix of equivalent sites used to construct the orbit list.
    const std::vector<std::vector<LatticeSite>> &getMatrixOfEquivalentSites() const { return _matrixOfEquivalentSites; }

    /// Returns the orbits in this orbit list.
    const std::vector<Orbit> &orbits() const { return _orbits; }

    /// Returns the structure.
    const Structure &structure() const;

private:
    /// Sorts the orbits by order, radius, orbit size, and the sites of their clusters.
    void sort(const double);

    /// Returns a copy of this orbit list carrying the given orbits and the geometry of this one.
    OrbitList derive(std::vector<Orbit>) const;

    /// Create an orbit by deducing the proper permutations
    Orbit createOrbit(const std::vector<std::vector<LatticeSite>> &);

    /// Collects the clusters that are related by symmetry to the given translations
    /// of the representative cluster.
    std::vector<std::vector<LatticeSite>> collectSymmetryRelatedClusters(const std::vector<std::vector<LatticeSite>> &) const;

    /// Deduces the site permutations that leave the orbit of the representative cluster unchanged.
    std::set<std::vector<int>> getAllowedPermutations(const std::vector<std::vector<LatticeSite>> &,
                                                      const std::vector<std::vector<LatticeSite>> &) const;

    /// Reorders the sites of each cluster to be consistent with the representative cluster.
    std::vector<std::vector<LatticeSite>> permuteClustersToMatchRepresentative(const std::vector<std::vector<LatticeSite>> &,
                                                                               const std::vector<std::vector<LatticeSite>> &) const;

    /// Assembles the orbit formed by the given rows of the matrix of equivalent sites,
    /// and appends it to the list of equivalent clusters.
    void appendOrbitFromRows(std::vector<std::vector<std::vector<LatticeSite>>> &,
                             std::unordered_set<std::vector<int>, VectorHash> &,
                             const std::vector<int> &) const;

    /// Returns the first column of the matrix of equivalent sites.
    std::vector<LatticeSite> getReferenceLatticeSites() const;

    /// Checks that the reference lattice sites contain no duplicates.
    void checkReferenceLatticeSitesAreUnique() const;

    /// Looks up the rows of the matrix of equivalent sites that match the lattice
    /// sites, and returns true if all of them could be found.
    bool tryGetReferenceLatticeSiteIndices(const std::vector<LatticeSite> &,
                                           std::vector<int> &,
                                           bool = true) const;

    /// Returns rows of the matrix of equivalent sites that match the lattice sites.
    std::vector<int> getReferenceLatticeSiteIndices(const std::vector<LatticeSite> &,
                                                    bool = true) const;

    /// Returns true if the cluster includes at least one site from the unit cell at the origin.
    bool validCluster(const std::vector<LatticeSite> &) const;

    /// Returns the sites translated such that the site with the given index
    /// lies in the unit cell at the origin.
    std::vector<LatticeSite> getTranslatedSites(const std::vector<LatticeSite> &,
                                                const unsigned int) const;

    /// Returns those of the given groups of sites that can be found among the
    /// reference lattice sites, each paired with the matching row indices.
    std::vector<std::pair<std::vector<LatticeSite>, std::vector<int>>> getMatchesInMatrixOfEquivalentSites(const std::vector<std::vector<LatticeSite>> &) const;

    /// Contains all the orbits in the orbit list.
    std::vector<Orbit> _orbits;

    /// Lattice sites used as references, equivalent to the first column of the _matrixOfEquivalentSites
    std::vector<LatticeSite> _referenceLatticeSites;

    /// Matrix of equivalent sites.
    std::vector<std::vector<LatticeSite>> _matrixOfEquivalentSites;

    /// Structure for which orbit list was constructed.
    Structure _structure;
};
