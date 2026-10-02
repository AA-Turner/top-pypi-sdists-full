#include "OrbitList.hpp"

#include <algorithm>
#include <numeric>

/**
@details This constructor generates an orbit list for the given (supercell) structure from a set of neighbor lists and a matrix of (symmetry) equivalent sites.
@param structure Structure that the orbits will be based on
@param matrixOfEquivalentSites matrix of symmetry equivalent sites
@param neighborLists neighbor lists for each (cluster) order (0=pairs, 1=triplets etc)
@param positionTolerance tolerance applied when comparing positions in Cartesian coordinates
**/
OrbitList::OrbitList(const Structure &structure,
                     const std::vector<std::vector<LatticeSite>> &matrixOfEquivalentSites,
                     const std::vector<std::vector<std::vector<LatticeSite>>> &neighborLists,
                     const double positionTolerance)
    : _matrixOfEquivalentSites(matrixOfEquivalentSites), _structure(structure)
{
    if (!structure.hasAllowedAtomicNumbers())
    {
        std::ostringstream msg;
        msg << "OrbitList must be initialized with a structure with the species allowed on each site specified.";
        throw std::runtime_error(msg.str());
    }
    _referenceLatticeSites = getReferenceLatticeSites();

    // Checked here rather than only in checkInvariants at the end, since the
    // construction below reads the reference lattice sites throughout and
    // duplicates among them would make it produce nonsense before the final
    // check could report the actual cause.
    checkReferenceLatticeSitesAreUnique();

    /**
    The following list is used to compile "raw data" for the orbit list.
    The first index (vector) runs over the orbits, the second index (vector) over the
    equivalent cluster in a given orbit, and the final vector runs over the lattice sites
    that represent a particular cluster. **/
    std::vector<std::vector<std::vector<LatticeSite>>> listOfEquivalentClusters;

    // rows that have already been accounted for
    std::unordered_set<std::vector<int>, VectorHash> rowsTaken;

    ManyBodyNeighborList mbnl = ManyBodyNeighborList();

    for (size_t index = 0; index < neighborLists[0].size(); index++)
    {
        std::vector<std::pair<std::vector<LatticeSite>, std::vector<LatticeSite>>> mbnlLatticeSites = mbnl.build(neighborLists, index, false);
        for (const auto &mbnlPair : mbnlLatticeSites)
        {
            for (const auto &latticeSite : mbnlPair.second)
            {
                // complete cluster by combining the first and the second part of the MBNL pair
                std::vector<LatticeSite> cluster = mbnlPair.first;
                cluster.push_back(latticeSite);

                // check that original sites are sorted
                auto copyOfCluster = cluster;
                std::sort(copyOfCluster.begin(), copyOfCluster.end());
                if (copyOfCluster != cluster)
                {
                    throw std::runtime_error("Original sites are not sorted (OrbitList::OrbitList)");
                }

                // Get all translational variants of cluster, in order to be able to extract
                // the "lowest" one according to how lattice sites are sorted
                std::vector<std::vector<LatticeSite>> clusterWithTranslations = getSitesTranslatedToUnitcell(cluster);

                // get all sites from the matrix of equivalent sites
                auto pairOfSitesAndRowIndices = getMatchesInMatrixOfEquivalentSites(clusterWithTranslations)[0];

                if (rowsTaken.find(pairOfSitesAndRowIndices.second) == rowsTaken.end())
                {
                    // Found new stuff
                    appendOrbitFromRows(listOfEquivalentClusters, rowsTaken, pairOfSitesAndRowIndices.second);
                }
            }

            // special singlet case
            if (mbnlPair.second.size() == 0)
            {
                std::vector<LatticeSite> cluster = mbnlPair.first;
                auto indices = getReferenceLatticeSiteIndices(cluster);
                auto find = rowsTaken.find(indices);
                if (find == rowsTaken.end())
                {
                    // Found new stuff
                    appendOrbitFromRows(listOfEquivalentClusters, rowsTaken, indices);
                }
            }
        }
    }

    // Sort list of equivalent clusters
    for (size_t i = 0; i < listOfEquivalentClusters.size(); i++)
    {
        std::sort(listOfEquivalentClusters[i].begin(), listOfEquivalentClusters[i].end());
    }

    // Add orbits from list of equivalent clusters to this orbit list
    _orbits.reserve(listOfEquivalentClusters.size());
    for (const auto &equivalentClusters : listOfEquivalentClusters)
    {
        _orbits.push_back(createOrbit(equivalentClusters));
    }

    // Sort the orbit list by order and radius.
    sort(positionTolerance);

    checkInvariants();
}

/**
@details
    Constructs an orbit list from orbits that have already been assembled
    elsewhere, which is how LocalOrbitListGenerator builds the orbit lists of a
    supercell from the primitive one. Such an orbit list carries neither a
    structure nor a matrix of equivalent sites, since its clusters refer to the
    sites of the supercell rather than to those of the primitive structure.
@param orbits the orbits of the new orbit list, in the order they are to appear
**/
OrbitList::OrbitList(std::vector<Orbit> orbits)
    : _orbits(std::move(orbits))
{
    checkInvariants();
}

/**
@details
    Returns an orbit list that holds the given orbits and shares the geometry
    of this one, meaning its structure and its matrix of equivalent sites. This
    is how the functions that produce a pruned or merged orbit list build their
    result, so that the result is a primitive orbit list in the same sense as
    the one it is derived from.
@param orbits the orbits of the new orbit list, in the order they are to appear
**/
OrbitList OrbitList::derive(std::vector<Orbit> orbits) const
{
    OrbitList derived;
    derived._orbits = std::move(orbits);
    derived._referenceLatticeSites = _referenceLatticeSites;
    derived._matrixOfEquivalentSites = _matrixOfEquivalentSites;
    derived._structure = _structure;
    derived.checkInvariants();
    return derived;
}

/**
@details
    Checks the invariants listed in the description of this class and throws a
    std::runtime_error naming the first violation found. Every constructor and
    every function that returns a new orbit list calls this on its result.
**/
void OrbitList::checkInvariants() const
{
    // An orbit list that carries a structure and a matrix of equivalent sites
    // is a primitive orbit list, for which two further invariants apply.
    const bool isPrimitive = _structure.size() > 0 && !_matrixOfEquivalentSites.empty();
    if (isPrimitive)
    {
        checkReferenceLatticeSitesAreUnique();
    }

    unsigned int previousOrder = 0;
    for (size_t orbitIndex = 0; orbitIndex < _orbits.size(); orbitIndex++)
    {
        const Orbit &orbit = _orbits[orbitIndex];

        if (orbit.size() == 0)
        {
            std::ostringstream msg;
            msg << "Orbit " << orbitIndex << " holds no clusters, so it has no representative cluster";
            msg << " (OrbitList::checkInvariants).";
            throw std::runtime_error(msg.str());
        }

        const unsigned int order = orbit.order();
        if (order < previousOrder)
        {
            std::ostringstream msg;
            msg << "Orbit " << orbitIndex << " has order " << order << ", which is lower than the order ";
            msg << previousOrder << " of the preceding orbit; the orbits must appear in non-decreasing order of cluster order";
            msg << " (OrbitList::checkInvariants).";
            throw std::runtime_error(msg.str());
        }
        previousOrder = order;

        for (const Cluster &cluster : orbit.clusters())
        {
            if (cluster.order() != order)
            {
                std::ostringstream msg;
                msg << "Orbit " << orbitIndex << " contains a cluster of order " << cluster.order();
                msg << ", which differs from the order " << order << " of its representative cluster";
                msg << " (OrbitList::checkInvariants).";
                throw std::runtime_error(msg.str());
            }
            if (isPrimitive)
            {
                for (const LatticeSite &latticeSite : cluster.latticeSites())
                {
                    if (latticeSite.index() >= _structure.size())
                    {
                        std::ostringstream msg;
                        msg << "Orbit " << orbitIndex << " contains a cluster with site index " << latticeSite.index();
                        msg << ", which is not in the range [0, " << _structure.size() << ") of the structure this orbit list is based on";
                        msg << " (OrbitList::checkInvariants).";
                        throw std::runtime_error(msg.str());
                    }
                }
            }
        }

        for (const ClusterVectorElement &element : orbit.clusterVectorElements())
        {
            if (element.multiComponentVector.size() != order)
            {
                std::ostringstream msg;
                msg << "Orbit " << orbitIndex << " has a cluster vector element whose multi-component vector has ";
                msg << element.multiComponentVector.size() << " entries rather than the " << order << " expected for its order";
                msg << " (OrbitList::checkInvariants).";
                throw std::runtime_error(msg.str());
            }
            if (element.sitePermutations.empty())
            {
                std::ostringstream msg;
                msg << "Orbit " << orbitIndex << " has a cluster vector element without site permutations";
                msg << " (OrbitList::checkInvariants).";
                throw std::runtime_error(msg.str());
            }
            if (element.multiplicity == 0)
            {
                std::ostringstream msg;
                msg << "Orbit " << orbitIndex << " has a cluster vector element with zero multiplicity";
                msg << " (OrbitList::checkInvariants).";
                throw std::runtime_error(msg.str());
            }
        }
    }
}

/**
@details Checks that the reference lattice sites, the first column of the
matrix of equivalent sites, contain no duplicates.
**/
void OrbitList::checkReferenceLatticeSitesAreUnique() const
{
    std::set<LatticeSite> uniqueReferenceLatticeSites(_referenceLatticeSites.begin(), _referenceLatticeSites.end());
    if (_referenceLatticeSites.size() != uniqueReferenceLatticeSites.size())
    {
        std::ostringstream msg;
        msg << "Found duplicates in the list of reference lattice sites (= first column of matrix of equivalent sites): ";
        msg << std::to_string(_referenceLatticeSites.size()) << " != " << std::to_string(uniqueReferenceLatticeSites.size());
        msg << " (OrbitList::checkReferenceLatticeSitesAreUnique)";
        throw std::runtime_error(msg.str());
    }
}

/**
@brief Sort the orbit list
@details
    This function sorts the orbit list by (1) order, (2) radius,
    (3) number of clusters in the orbit, and (4) coordinates of
    the sites in the clusters. This produces a reproducible
    (stable) order of the orbit list (and thereby the cluster vector).
@param positionTolerance tolerance applied when comparing positions in Cartesian coordinates
*/
std::vector<size_t> groupRadiiWithinTolerance(const std::vector<double> &radii,
                                              const double tolerance)
{
    std::vector<size_t> ascending(radii.size());
    std::iota(ascending.begin(), ascending.end(), 0);
    std::sort(ascending.begin(), ascending.end(),
              [&radii](const size_t lhs, const size_t rhs)
              { return radii[lhs] < radii[rhs]; });

    std::vector<size_t> groups(radii.size(), 0);
    for (size_t i = 1; i < ascending.size(); i++)
    {
        const double gap = radii[ascending[i]] - radii[ascending[i - 1]];
        groups[ascending[i]] = groups[ascending[i - 1]] + (gap > tolerance ? 1 : 0);
    }
    return groups;
}

void OrbitList::sort(const double positionTolerance)
{
    std::vector<double> radii;
    radii.reserve(_orbits.size());
    for (const Orbit &orbit : _orbits)
    {
        radii.push_back(orbit.radius());
    }
    const std::vector<size_t> radiusGroups = groupRadiiWithinTolerance(radii, positionTolerance);

    std::vector<size_t> order(_orbits.size());
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(),
              [this, &radiusGroups](const size_t lhs, const size_t rhs)
              {
                  const Orbit &left = _orbits[lhs];
                  const Orbit &right = _orbits[rhs];
                  // (1) Test against number of bodies in cluster.
                  if (left.representativeCluster().order() != right.representativeCluster().order())
                  {
                      return left.representativeCluster().order() < right.representativeCluster().order();
                  }
                  // (2) Compare by the group of radii this orbit belongs to, so
                  // that radii equal up to numerical noise are treated as ties
                  // and the keys below decide between them.
                  if (radiusGroups[lhs] != radiusGroups[rhs])
                  {
                      return radiusGroups[lhs] < radiusGroups[rhs];
                  }
                  // (3) Compare by the number of clusters in the orbit.
                  if (left.size() != right.size())
                  {
                      return left.size() < right.size();
                  }
                  // (4) Check the individual sites.
                  return left.clusters() < right.clusters();
              });

    std::vector<Orbit> sorted;
    sorted.reserve(_orbits.size());
    for (const size_t index : order)
    {
        sorted.push_back(std::move(_orbits[index]));
    }
    _orbits = std::move(sorted);
}

/**
@details Returns reference to the orbit at the given index.
@param index index of orbit
@returns reference to orbit
**/
const Orbit &OrbitList::getOrbit(unsigned int index) const
{
    if (index >= size())
    {
        throw std::out_of_range("Tried accessing orbit at out of bound index (Orbit OrbitList::getOrbit)");
    }
    return _orbits[index];
}

/**
@details
    Creates an orbit from a set of clusters that are equivalent by the
    symmetries of the underlying crystal.

    The clusters are handed over as groups of lattice sites in an arbitrary
    order of the sites within each group. Before the orbit can be created the
    sites have to be reordered such that the ordering of every cluster is
    consistent with that of the representative cluster, which is taken to be
    the first one. This matters for systems with more than two components,
    where the position of a site within a cluster selects which point function
    is applied to it.

    The work is carried out in three stages, each of which is delegated to a
    helper function:

    1. Collect the clusters that are related to the representative cluster by
       symmetry, in every ordering in which they occur (collectSymmetryRelatedClusters).
    2. Deduce the permutations of the representative cluster that leave the
       orbit unchanged (getAllowedPermutations).
    3. Reorder the sites of every cluster to match the representative cluster
       (permuteClustersToMatchRepresentative).

@param equivalentClusters groups of lattice sites that are equivalent by symmetry
@returns the resulting orbit
**/
Orbit OrbitList::createOrbit(const std::vector<std::vector<LatticeSite>> &equivalentClusters)
{
    // All translations of the representative cluster for which at least one
    // site lies in the unit cell at the origin. The sites within each
    // translation are deliberately left in their original order.
    const std::vector<std::vector<LatticeSite>> representativeClusterWithTranslations =
        getSitesTranslatedToUnitcell(equivalentClusters[0], false);

    const std::vector<std::vector<LatticeSite>> symmetryRelatedClusters =
        collectSymmetryRelatedClusters(representativeClusterWithTranslations);

    const std::set<std::vector<int>> allowedPermutations =
        getAllowedPermutations(representativeClusterWithTranslations, symmetryRelatedClusters);

    const std::vector<std::vector<LatticeSite>> permutedEquivalentClusters =
        permuteClustersToMatchRepresentative(equivalentClusters, symmetryRelatedClusters);

    // Turn the permuted equivalent clusters into actual Cluster objects
    std::vector<Cluster> clusters;
    clusters.reserve(permutedEquivalentClusters.size());
    std::shared_ptr<Structure> structurePtr = std::make_shared<Structure>(_structure);
    for (const auto &cluster : permutedEquivalentClusters)
    {
        clusters.push_back(Cluster(cluster, structurePtr));
    }
    return Orbit(clusters, allowedPermutations);
}

/**
@details
    Collects the clusters that are related by symmetry to any of the given
    translations of the representative cluster.

    Each translation is looked up in the matrix of equivalent sites, which
    yields the clusters that are directly equivalent to it, in the site
    ordering imposed by that matrix. The results for all translations are
    merged and sorted, so that the outcome can be used with the set operations
    of the standard library.

@param representativeClusterWithTranslations translations of the representative cluster
@returns the symmetry related clusters, sorted
**/
std::vector<std::vector<LatticeSite>> OrbitList::collectSymmetryRelatedClusters(
    const std::vector<std::vector<LatticeSite>> &representativeClusterWithTranslations) const
{
    std::vector<std::vector<LatticeSite>> symmetryRelatedClusters;
    for (const auto &representativeCluster : representativeClusterWithTranslations)
    {
        const auto equivalentClusters = getSymmetryRelatedSiteGroups(representativeCluster);
        symmetryRelatedClusters.insert(symmetryRelatedClusters.end(),
                                       equivalentClusters.begin(), equivalentClusters.end());
    }
    std::sort(symmetryRelatedClusters.begin(), symmetryRelatedClusters.end());
    return symmetryRelatedClusters;
}

/**
@details
    Determines the site permutations that map the representative cluster onto
    itself, in the sense that the permuted cluster is still one of the clusters
    of this orbit.

    All permutations of all translations of the representative cluster are
    formed and intersected with the symmetry related clusters. What remains are
    the reorderings of the representative cluster that also arise as symmetry
    equivalent clusters, and each of them is then expressed as a permutation of
    site indices. This is relevant for systems with more than two components,
    for which one must deal with multi-component vectors; if, for example,
    [0, 2, 1] is among the permutations, then the multi-component vector
    [0, 1, 0] describes the same cluster vector element as [0, 0, 1].

@param representativeClusterWithTranslations translations of the representative cluster
@param symmetryRelatedClusters the symmetry related clusters, sorted
@returns the permutations allowed for this orbit
**/
std::set<std::vector<int>> OrbitList::getAllowedPermutations(
    const std::vector<std::vector<LatticeSite>> &representativeClusterWithTranslations,
    const std::vector<std::vector<LatticeSite>> &symmetryRelatedClusters) const
{
    // Construct all permutations of all translations of the representative cluster.
    std::vector<std::vector<LatticeSite>> representativeClusterPermutations;
    for (const auto &representativeCluster : representativeClusterWithTranslations)
    {
        const auto permutedClusters = icet::getAllPermutations<LatticeSite>(representativeCluster);
        representativeClusterPermutations.insert(representativeClusterPermutations.end(),
                                                 permutedClusters.begin(), permutedClusters.end());
    }
    std::sort(representativeClusterPermutations.begin(), representativeClusterPermutations.end());

    // Keep those permutations that also occur among the symmetry related clusters.
    std::vector<std::vector<LatticeSite>> consistentClusters;
    std::set_intersection(symmetryRelatedClusters.begin(), symmetryRelatedClusters.end(),
                          representativeClusterPermutations.begin(), representativeClusterPermutations.end(),
                          std::back_inserter(consistentClusters));

    // Express each of them as a permutation of site indices. A cluster is
    // compared against every translation of the representative cluster, since
    // it may be a reordering of any one of them.
    std::set<std::vector<int>> allowedPermutations;
    std::vector<int> permutation;
    for (const auto &consistentCluster : consistentClusters)
    {
        bool foundPermutation = false;
        for (const auto &representativeCluster : representativeClusterWithTranslations)
        {
            if (icet::tryGetPermutation<LatticeSite>(representativeCluster, consistentCluster, permutation))
            {
                allowedPermutations.insert(permutation);
                foundPermutation = true;
            }
        }
        if (!foundPermutation)
        {
            throw std::runtime_error("Did not find integer permutation from allowed permutation to any translated representative site (OrbitList::getAllowedPermutations)");
        }
    }
    return allowedPermutations;
}

/**
@details
    Reorders the sites of each of the given clusters such that the ordering is
    consistent with the representative cluster.

    A cluster whose sites are already ordered consistently occurs verbatim
    among the symmetry related clusters and is taken over unchanged. Otherwise
    every permutation of every translation of the cluster is tried until one is
    found that does occur there, and that reordering is used instead.

@param equivalentClusters the clusters of the orbit, with sites in arbitrary order
@param symmetryRelatedClusters the symmetry related clusters, which define the consistent ordering
@returns the clusters with their sites reordered, in the order of the input
**/
std::vector<std::vector<LatticeSite>> OrbitList::permuteClustersToMatchRepresentative(
    const std::vector<std::vector<LatticeSite>> &equivalentClusters,
    const std::vector<std::vector<LatticeSite>> &symmetryRelatedClusters) const
{
    const std::unordered_set<std::vector<LatticeSite>> consistentlyOrderedClusters(
        symmetryRelatedClusters.begin(), symmetryRelatedClusters.end());

    std::vector<std::vector<LatticeSite>> permutedEquivalentClusters;
    permutedEquivalentClusters.reserve(equivalentClusters.size());

    for (const auto &cluster : equivalentClusters)
    {
        if (consistentlyOrderedClusters.count(cluster) > 0)
        {
            permutedEquivalentClusters.push_back(cluster);
            continue;
        }

        // The sites of this cluster are not ordered as they should be. Search
        // the permutations of its translations for an ordering that is.
        bool foundOrdering = false;
        for (const auto &translatedCluster : getSitesTranslatedToUnitcell(cluster, false))
        {
            for (const auto &permutedCluster : icet::getAllPermutations<LatticeSite>(translatedCluster))
            {
                if (consistentlyOrderedClusters.count(permutedCluster) > 0)
                {
                    permutedEquivalentClusters.push_back(permutedCluster);
                    foundOrdering = true;
                    break;
                }
            }
            if (foundOrdering)
            {
                break;
            }
        }

        if (!foundOrdering)
        {
            throw std::runtime_error("Did not find a permutation of the orbit sites to the permutations of the representative sites (OrbitList::permuteClustersToMatchRepresentative)");
        }
    }
    return permutedEquivalentClusters;
}

/**
@details
    Given a group of sites ("cluster"), this function returns the clusters
    that are equivalent to this cluster by symmetries of the underlying
    crystal. These clusters are obtained by

    (1) identifying the rows in matrixOfEquivalentSites that correspond to
        the input cluster (i.e., where in the first column are the sites of
        the input cluster?),
    (2) looping over the remaining columns of matrixOfEquivalentSites and
        forming new clusters by combining the sites corresponding to the
        rows identified in (1),
    (3) forming translational equivalents of the thus obtained clusters
        by translating them such that one of its sites at a time lies in
        the unit cell.

@param sites The sites of a cluster
@returns Groups of sites ("clusters") that are equivalent to the input cluster
**/
std::vector<std::vector<LatticeSite>> OrbitList::getSymmetryRelatedSiteGroups(const std::vector<LatticeSite> &sites) const
{
    std::vector<int> rowIndicesFromReferenceLatticeSites = getReferenceLatticeSiteIndices(sites, false);

    std::vector<std::vector<LatticeSite>> allColumns;
    for (size_t columnIndex = 0; columnIndex < _matrixOfEquivalentSites[0].size(); columnIndex++)
    {
        std::vector<LatticeSite> nondistinctLatticeSites;

        for (const int &rowIndex : rowIndicesFromReferenceLatticeSites)
        {
            nondistinctLatticeSites.push_back(_matrixOfEquivalentSites[rowIndex][columnIndex]);
        }

        // Include translated sites as well
        auto translatedEquivalentSites = getSitesTranslatedToUnitcell(nondistinctLatticeSites, false);
        allColumns.insert(allColumns.end(), translatedEquivalentSites.begin(), translatedEquivalentSites.end());
    }
    return allColumns;
}

/**
@details
This function creates all possible translations of the input list of lattice sites, for which at
least one of the lattice sites is inside the (original) unit cell.
For example, given a pair with unit cell offsets
  [0, 0, 1], [-3, 0, 3]
one gets
  [0, 0, 0], [-3, 0, 2]
  [3, 0, -2], [0, 0, 0]

This translation gives rise to equivalent clusters that sometimes
are not found by using the set of crystal symmetries given by spglib.

@param latticeSites list of lattice sites
@param sort if true sort the translated sites
*/
std::vector<std::vector<LatticeSite>> OrbitList::getSitesTranslatedToUnitcell(const std::vector<LatticeSite> &latticeSites,
                                                                              bool sort) const
{

    std::vector<std::vector<LatticeSite>> listOfTranslatedLatticeSites;
    listOfTranslatedLatticeSites.push_back(latticeSites);
    for (size_t i = 0; i < latticeSites.size(); i++)
    {
        if (!latticeSites[i].unitcellOffset().isZero()) // only translate sites outside the primitive unitcell
        {
            auto translatedSites = getTranslatedSites(latticeSites, i);
            if (sort)
            {
                std::sort(translatedSites.begin(), translatedSites.end());
            }
            listOfTranslatedLatticeSites.push_back(translatedSites);
        }
    }

    // Sort this so that the lowest vec<latticeSite> will be chosen and therefore the sorting of orbits should be consistent.
    std::sort(listOfTranslatedLatticeSites.begin(), listOfTranslatedLatticeSites.end());

    return listOfTranslatedLatticeSites;
}

/**
@details Takes all lattice sites in vector latticeSites and subtracts the unitcell offset of site latticeSites[index].
@param latticeSites List of lattice sites, typically a cluster
@param index Index of site relative to which to shift
*/
std::vector<LatticeSite> OrbitList::getTranslatedSites(const std::vector<LatticeSite> &latticeSites,
                                                       const unsigned int index) const
{
    Vector3i offset = latticeSites[index].unitcellOffset();
    auto translatedSites = latticeSites;
    for (auto &latticeSite : translatedSites)
    {
        latticeSite.addUnitcellOffset(-offset);
    }
    return translatedSites;
}

/**
@details
    Assembles a new orbit from the given rows of the matrix of equivalent
    sites, and appends it to the list of equivalent clusters.

    Each row of the matrix lists the sites that are equivalent to the site in
    its first column. Reading a fixed set of rows across one column therefore
    yields one cluster, and reading them across every column yields the whole
    orbit. Every such cluster is looked up again in the matrix, together with
    its translations, which serves two purposes: it identifies the rows that
    the cluster occupies, so that the same orbit is not assembled a second time
    from a different starting point, and it selects the representation of the
    cluster that is used here.

    A cluster is only included if it is anchored in the unit cell at the
    origin. Clusters that lie entirely outside it are translational copies of
    clusters that are counted elsewhere, and including them would amount to
    counting "ghost clusters".

@param listOfEquivalentClusters
    List of orbits to which the new orbit is appended. The first index runs
    over the orbits, the second over the equivalent clusters of a given orbit,
    and the third over the lattice sites of a particular cluster.
@param rowsTaken
    Sets of rows that have already been accounted for, updated by this function
@param rowIndices indices of rows in the matrix of symmetry equivalent sites
**/
void OrbitList::appendOrbitFromRows(std::vector<std::vector<std::vector<LatticeSite>>> &listOfEquivalentClusters,
                                    std::unordered_set<std::vector<int>, VectorHash> &rowsTaken,
                                    const std::vector<int> &rowIndices) const
{
    std::vector<std::vector<LatticeSite>> clustersOfNewOrbit;
    clustersOfNewOrbit.reserve(_matrixOfEquivalentSites[0].size());

    for (size_t column = 0; column < _matrixOfEquivalentSites[0].size(); column++)
    {
        // Read one cluster off this column of the matrix of equivalent sites.
        std::vector<LatticeSite> cluster;
        cluster.reserve(rowIndices.size());
        for (const int row : rowIndices)
        {
            cluster.push_back(_matrixOfEquivalentSites[row][column]);
        }

        // Of all translations of this cluster, keep those that can be located
        // among the reference lattice sites, paired with the rows they occupy.
        const auto matches = getMatchesInMatrixOfEquivalentSites(getSitesTranslatedToUnitcell(cluster));

        // If the lowest translation has already been accounted for, then so
        // has this cluster, and there is nothing left to do for this column.
        if (rowsTaken.count(matches[0].second) > 0)
        {
            continue;
        }

        bool clusterAdded = false;
        for (const auto &match : matches)
        {
            if (rowsTaken.count(match.second) > 0)
            {
                continue;
            }
            rowsTaken.insert(match.second);

            // At most one cluster is added per column, and only once a
            // translation has been seen that is anchored in the unit cell at
            // the origin. The condition is therefore evaluated on the
            // translation currently under consideration, whereas what gets
            // added is always the lowest translation, so that the choice of
            // representation does not depend on the order in which the
            // translations happen to be visited. The two need not be the same
            // translation, and in practice often are not: the lowest
            // translation is a canonical label for the cluster rather than the
            // one that demonstrates that it belongs to this orbit. The sites
            // are translated again wherever it matters, in createOrbit and in
            // LocalOrbitListGenerator.
            if (!clusterAdded && validCluster(match.first))
            {
                clustersOfNewOrbit.push_back(matches[0].first);
                clusterAdded = true;
            }
        }
    }

    if (!clustersOfNewOrbit.empty())
    {
        listOfEquivalentClusters.push_back(clustersOfNewOrbit);
    }
}

/**
@details
    Returns those of the given groups of sites that can be located among the
    reference lattice sites, each paired with the row indices at which its
    sites were found. Groups that cannot be located are left out, which is an
    ordinary outcome rather than an error. If none of them can be located an
    error is thrown, since the caller always supplies the translations of a
    cluster that was itself read off the matrix of equivalent sites.
@param translatedSites groups of sites, typically the translations of one cluster
*/
std::vector<std::pair<std::vector<LatticeSite>, std::vector<int>>> OrbitList::getMatchesInMatrixOfEquivalentSites(
    const std::vector<std::vector<LatticeSite>> &translatedSites) const
{
    std::vector<int> rowIndices;
    std::vector<std::pair<std::vector<LatticeSite>, std::vector<int>>> matchedSites;
    for (const auto &sites : translatedSites)
    {
        if (tryGetReferenceLatticeSiteIndices(sites, rowIndices))
        {
            matchedSites.push_back(std::make_pair(sites, rowIndices));
        }
    }
    if (matchedSites.empty())
    {
        throw std::runtime_error("Did not find any of the translated sites in reference lattice sites in the matrix of equivalent sites (OrbitList::getMatchesInMatrixOfEquivalentSites)");
    }
    return matchedSites;
}

/**
@details This function returns true if the cluster includes at least on site from the unit cell at the origin, i.e. its unitcell offset is zero.
@param latticeSites list of sites to check
*/
bool OrbitList::validCluster(const std::vector<LatticeSite> &latticeSites) const
{
    for (const auto &latticeSite : latticeSites)
    {
        if (latticeSite.unitcellOffset().isZero())
        {
            return true;
        }
    }
    return false;
}

/**
@details
    For each lattice site in the input vector, this function looks up the index
    of the entry in _referenceLatticeSites that holds an equivalent lattice
    site, and returns true if every site could be found.

    This is the non-throwing counterpart of getReferenceLatticeSiteIndices,
    intended for the call sites at which a site that is absent from the
    reference lattice sites is an ordinary outcome rather than an error.
@param latticeSites List of sites to search for
@param rowIndices Set to the indices of the matching entries in _referenceLatticeSites
@param sort If true, the returned list of indices will be sorted
@return True if all sites were found, in which case rowIndices has been filled in
**/
bool OrbitList::tryGetReferenceLatticeSiteIndices(const std::vector<LatticeSite> &latticeSites,
                                                  std::vector<int> &rowIndices,
                                                  bool sort) const
{
    rowIndices.clear();
    rowIndices.reserve(latticeSites.size());
    for (const auto &latticeSite : latticeSites)
    {
        const auto find = std::find(_referenceLatticeSites.begin(), _referenceLatticeSites.end(), latticeSite);
        if (find == _referenceLatticeSites.end())
        {
            return false;
        }
        rowIndices.push_back(std::distance(_referenceLatticeSites.begin(), find));
    }
    if (sort)
    {
        std::sort(rowIndices.begin(), rowIndices.end());
    }
    return true;
}

/**
@details
    For each lattice site in the input vector, this function returns the
    index of the entry in _referenceLatticeSites that holds an equivalent
    lattice site.
@param latticeSites List of sites to search for
@param sort If true, the returned list of indices will be sorted
@return Indices of entries in _referenceLatticeSites that are equivalent to the sites latticeSites
**/
std::vector<int> OrbitList::getReferenceLatticeSiteIndices(const std::vector<LatticeSite> &latticeSites,
                                                           bool sort) const
{
    std::vector<int> rowIndices;
    if (!tryGetReferenceLatticeSiteIndices(latticeSites, rowIndices, sort))
    {
        throw std::runtime_error("Did not find lattice site in the reference lattice sites in the matrix of equivalent sites (OrbitList::getReferenceLatticeSiteIndices)");
    }
    return rowIndices;
}

/**
@details
    Returns the reference lattice sites, i.e., the first column of the matrix of
    equivalent sites. Every other column of that matrix lists sites that are
    symmetry equivalent to the site in the first column of the same row, so the
    first column identifies the rows and thereby serves as the key by which
    symmetry related sites are looked up.
**/
std::vector<LatticeSite> OrbitList::getReferenceLatticeSites() const
{
    std::vector<LatticeSite> referenceLatticeSites;
    referenceLatticeSites.reserve(_matrixOfEquivalentSites[0].size());
    for (const auto &row : _matrixOfEquivalentSites)
    {
        referenceLatticeSites.push_back(row[0]);
    }
    return referenceLatticeSites;
}

/**
@details
    Returns a copy of this orbit list from which the orbits at the given
    indices have been left out. The remaining orbits keep their relative order,
    so the cluster vector of the result is the cluster vector of this orbit
    list with the corresponding elements deleted.
@param indices indices of the orbits to leave out, in any order
**/
OrbitList OrbitList::withoutOrbits(const std::vector<size_t> &indices) const
{
    std::set<size_t> indicesToRemove;
    for (const size_t index : indices)
    {
        if (index >= size())
        {
            std::ostringstream msg;
            msg << "Index " << index << " was out of bounds (OrbitList::withoutOrbits)." << std::endl;
            msg << "OrbitList size: " << size();
            throw std::out_of_range(msg.str());
        }
        if (!indicesToRemove.insert(index).second)
        {
            std::ostringstream msg;
            msg << "Index " << index << " was given more than once (OrbitList::withoutOrbits).";
            throw std::invalid_argument(msg.str());
        }
    }

    std::vector<Orbit> remainingOrbits;
    remainingOrbits.reserve(size() - indicesToRemove.size());
    for (size_t index = 0; index < size(); index++)
    {
        if (indicesToRemove.count(index) == 0)
        {
            remainingOrbits.push_back(_orbits[index]);
        }
    }
    return derive(std::move(remainingOrbits));
}

/**
@details
    Returns a copy of this orbit list from which the orbits with inactive
    sites, meaning sites with only one allowed species, have been left out.
**/
OrbitList OrbitList::withoutInactiveOrbits() const
{
    std::vector<Orbit> activeOrbits;
    activeOrbits.reserve(size());
    for (const Orbit &orbit : _orbits)
    {
        if (orbit.active())
        {
            activeOrbits.push_back(orbit);
        }
    }
    return derive(std::move(activeOrbits));
}

/**
@details
    Returns a copy of this orbit list in which each group of orbits has been
    merged into its first member and the merged-away orbits have been left out.
    Merging an orbit into another means adding the clusters of the former to
    the latter, which is what makes the two contribute a single, shared element
    to the cluster vector.

    All indices refer to this orbit list, so a caller can name them by reading
    the orbit list once, without having to account for the renumbering that the
    removals cause.

    Removing the merged-away orbits is part of this operation rather than a
    separate step a caller could omit. Omitting it would leave an orbit list
    whose length still matches that of any orbit list derived from this one
    while the orbits no longer correspond, which no size check could catch.
@param groups maps the index of an orbit to the indices of the orbits merged into it
**/
OrbitList OrbitList::withMergedOrbits(const std::map<size_t, std::vector<size_t>> &groups) const
{
    std::vector<Orbit> mergedOrbits = _orbits;
    std::vector<size_t> indicesToRemove;
    std::set<size_t> indicesSeen;

    for (const auto &group : groups)
    {
        const size_t target = group.first;
        if (target >= size())
        {
            std::ostringstream msg;
            msg << "Index " << target << " was out of bounds (OrbitList::withMergedOrbits)." << std::endl;
            msg << "OrbitList size: " << size();
            throw std::out_of_range(msg.str());
        }
        if (!indicesSeen.insert(target).second)
        {
            std::ostringstream msg;
            msg << "Orbit " << target << " takes part in more than one merge (OrbitList::withMergedOrbits).";
            throw std::invalid_argument(msg.str());
        }

        for (const size_t source : group.second)
        {
            if (source >= size())
            {
                std::ostringstream msg;
                msg << "Index " << source << " was out of bounds (OrbitList::withMergedOrbits)." << std::endl;
                msg << "OrbitList size: " << size();
                throw std::out_of_range(msg.str());
            }
            if (!indicesSeen.insert(source).second)
            {
                std::ostringstream msg;
                msg << "Orbit " << source << " takes part in more than one merge (OrbitList::withMergedOrbits).";
                throw std::invalid_argument(msg.str());
            }
            // The merged orbit reads every cluster it holds, including the
            // ones taken over from the source, through the multi-component
            // vectors of the target, and those address the point functions of
            // the species allowed on the sites of the target. Orbits whose
            // sites allow different species therefore cannot be merged,
            // whatever else they have in common: two binary orbits on
            // different sublattices agree on the number of cluster vector
            // elements, on the multi-component vectors and on the site
            // permutations, and differ only here.
            //
            // The comparison is skipped when the two orbits describe
            // different numbers of sites, which is a mismatch of order.
            // Orbit::operator+= reports that below, and comparing the species
            // of a different number of sites would report it as a mismatch of
            // species instead.
            const auto targetSpecies =
                _orbits[target].representativeCluster().getAllowedSpeciesPerSite();
            const auto sourceSpecies =
                _orbits[source].representativeCluster().getAllowedSpeciesPerSite();

            // An orbit list whose structure carries no table of allowed
            // species cannot answer the question, which is the case for the
            // orbit lists of a supercell, since a cluster vector evaluated
            // through one takes its species from the cluster space instead.
            // Merging is refused there rather than performed unchecked, since
            // an unchecked merge produces a model that reads the clusters of
            // one orbit through the species of another and reports nothing.
            if (targetSpecies.empty() || sourceSpecies.empty())
            {
                std::ostringstream msg;
                msg << "Orbits can only be merged in an orbit list that states the species"
                    << " allowed on each site, which the orbit list of a supercell does not"
                    << " (OrbitList::withMergedOrbits).";
                throw std::invalid_argument(msg.str());
            }

            if (targetSpecies.size() == sourceSpecies.size() && targetSpecies != sourceSpecies)
            {
                std::ostringstream msg;
                msg << "The sites of orbit " << target << " and orbit " << source
                    << " allow different species, so they cannot be merged"
                    << " (OrbitList::withMergedOrbits).";
                throw std::invalid_argument(msg.str());
            }
            mergedOrbits[target] += _orbits[source];
            indicesToRemove.push_back(source);
        }
    }

    return derive(std::move(mergedOrbits)).withoutOrbits(indicesToRemove);
}

/**
@brief Getter for structure object
*/
const Structure &OrbitList::structure() const
{
    if (_structure.size() == 0)
    {
        std::ostringstream msg;
        msg << "No structure has been initialized in this OrbitList (OrbitList::structure)";
        throw std::runtime_error(msg.str());
    }
    return _structure;
}

