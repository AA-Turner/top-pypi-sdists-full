#define _USE_MATH_DEFINES
#include <cmath>

#include "ClusterSpace.hpp"

/**
@details This constructor initializes a ClusterSpace object.
@param orbitList
    List of orbits for the primitive structure.
*/
ClusterSpace::ClusterSpace(std::shared_ptr<const OrbitList> orbitList)
{
    setPrimitiveOrbitList(orbitList);
}

/**
@details
    Bases this cluster space on the given orbit list, which is how pruning and
    merging take effect: the caller builds the pruned or merged orbit list and
    hands it over here.

    This changes which orbit list this cluster space refers to. It cannot
    change any orbit list, since orbit lists are immutable, so no other cluster
    space and no calculator that shares the previous one is affected by it.

    The species maps and the evaluation plans are built before any member is
    assigned, so that a cluster space that rejects an orbit list, one derived
    for a supercell for example, which carries no structure to read the
    allowed species from, is left exactly as it was rather than half changed.
@param orbitList the orbit list this cluster space is to be based on
*/
void ClusterSpace::setPrimitiveOrbitList(std::shared_ptr<const OrbitList> orbitList)
{
    if (!orbitList)
    {
        throw std::invalid_argument("A cluster space must be based on an orbit list (ClusterSpace::setPrimitiveOrbitList).");
    }
    std::vector<std::unordered_map<int, int>> speciesMaps = buildSpeciesMaps(*orbitList);
    std::vector<OrbitEvaluationPlan> plans = buildOrbitEvaluationPlans(*orbitList, speciesMaps);

    size_t maximumDistinctPatterns = 0;
    for (const OrbitEvaluationPlan &plan : plans)
    {
        maximumDistinctPatterns = std::max(maximumDistinctPatterns, plan.maximumDistinctPatterns);
    }

    _primitiveOrbitList = std::move(orbitList);
    _speciesMaps = std::move(speciesMaps);
    _orbitEvaluationPlans = std::move(plans);
    _maximumDistinctPatterns = maximumDistinctPatterns;
}

/**
@details Returns the map between atomic numbers and the internal species
enumeration scheme, which numbers the species allowed on a site consecutively
from zero in order of increasing atomic number.
@param orbitList the orbit list whose structure defines the allowed species
*/
std::vector<std::unordered_map<int, int>> ClusterSpace::buildSpeciesMaps(const OrbitList &orbitList)
{
    std::vector<std::unordered_map<int, int>> speciesMaps;
    for (const auto &atomicNumbers : orbitList.structure().allowedAtomicNumbers())
    {
        std::unordered_map<int, int> speciesMap;
        std::vector<int> atomicNumbersCopy = atomicNumbers;
        sort(atomicNumbersCopy.begin(), atomicNumbersCopy.end());
        for (size_t i = 0; i < atomicNumbersCopy.size(); i++)
        {
            speciesMap[atomicNumbersCopy[i]] = i;
        }
        speciesMaps.push_back(speciesMap);
    }
    return speciesMaps;
}

/**
@details This function calculates and returns the cluster vector for the
input structure in the cluster space.

The first element in the cluster vector will always be one (1) corresponding to
the zerolet. The remaining elements of the cluster vector represent averages
over orbits (symmetry equivalent clusters) of increasing order and size.

The clusters are enumerated into a full supercell orbit list and then counted.
This is the reference oracle against which the evaluation tables of
ClusterExpansionCalculator are checked, and it is not used in production.
Cluster vectors are computed through those tables instead, which reach the
same values without materializing the clusters, both for a single evaluation
and for repeated ones.

@param structure
    Input configuration
@param fractionalPositionTolerance
    Tolerance applied when comparing positions in fractional coordinates
**/

std::vector<double> ClusterSpace::getClusterVectorFromSupercellOrbitList(
    const Structure &structure,
    const double fractionalPositionTolerance) const
{
    // Construct orbit list for this structure.
    std::shared_ptr<Structure> supercell = std::make_shared<Structure>(structure);
    LocalOrbitListGenerator localOrbitListGenerator = LocalOrbitListGenerator(
        *_primitiveOrbitList,
        supercell,
        fractionalPositionTolerance);
    OrbitList supercellOrbitList = localOrbitListGenerator.getFullOrbitList();
    const std::vector<int> &occupations = supercell->getAtomicNumbers();
    OccupationSpan occupationSpan(occupations.data(), occupations.size());
    return getClusterVectorFromOrbitList(supercellOrbitList, occupationSpan, supercell->size());
}

/**
@details
    Evaluates a point function, the quantity the papers write as
    Theta_n(sigma). This is the name that quantity is exposed under on the
    Python side; evaluatePointFunction, where it is defined and documented,
    is the name the rest of the core uses.

@param numberOfAllowedSpecies number of allowed species on the site in question
@param clusterFunction index of the point function, counting the first non-trivial function as zero
@param species index of the species that occupies the site

@returns the value of the point function
*/
double ClusterSpace::evaluateClusterFunction(const int numberOfAllowedSpecies,
                                             const int clusterFunction,
                                             const int species) const
{
    return evaluatePointFunction(numberOfAllowedSpecies, clusterFunction, species);
}

/**
@brief Calculates the size of the cluster space, defined as the length of a cluster vector.
*/
size_t ClusterSpace::size() const
{
    size_t size = 1; // 1 for the zerolet
    for (size_t orbitIndex = 0; orbitIndex < _primitiveOrbitList->size(); orbitIndex++)
    {
        const Orbit &orbit = _primitiveOrbitList->getOrbit(orbitIndex);
        size += orbit.clusterVectorElements().size();
    }
    return size;
}

/**
@details
    Occupy cluster vector based on a supercell and a corresponding orbit list.
    Cluster vectors are computed in production by ClusterExpansionCalculator
    through its evaluation tables; this function reaches a total cluster
    vector the other way, by counting the clusters stored in the given orbit
    list, and serves as the reference oracle for that representation.

@param orbitList
    The orbit list to be used for counting, typically a full orbit list
    generated for the supercell.
@param occupations
    The occupations of the supercell whose cluster vector should be computed.
@param supercellSize
    The number of sites in the supercell that occupations refers to.
*/
std::vector<double> ClusterSpace::getClusterVectorFromOrbitList(const OrbitList &orbitList,
                                                                OccupationSpan occupations,
                                                                const size_t supercellSize) const
{
    // Check that orbit lists match
    if (_primitiveOrbitList->size() != orbitList.size())
    {
        std::ostringstream msg;
        msg << "Orbit lists do not match (ClusterSpace::getClusterVectorFromOrbitList)."
            << std::endl
            << orbitList.size() << " != " << _primitiveOrbitList->size() << std::endl;
        throw std::runtime_error(msg.str());
    }

    // How many distinct patterns an orbit can produce is bounded both by
    // how many the species allow and by how many clusters there are to
    // count, and the smaller of the two sizes the counting buffer.
    size_t maximumDistinctPatterns = 0;
    for (size_t orbitIndex = 0; orbitIndex < orbitList.size(); orbitIndex++)
    {
        maximumDistinctPatterns = std::max(
            maximumDistinctPatterns,
            std::min(_orbitEvaluationPlans[orbitIndex].maximumDistinctPatterns,
                     orbitList.getOrbit(orbitIndex).size()));
    }

    return assembleFullClusterVector(
        [&](const size_t orbitIndex, ClusterCountBuffer &counts)
        {
            countClustersOfOrbit(orbitList.getOrbit(orbitIndex),
                                 _orbitEvaluationPlans[orbitIndex],
                                 occupations, counts);
        },
        supercellSize, maximumDistinctPatterns);
}

/**
@details
    Counts the occupations of the clusters of one orbit of a supercell orbit
    list, each with a weight of one.

    ClusterExpansionCalculator counts the same quantity through its
    evaluation tables, which describe where the clusters sit without storing
    them. This function is the other way of reaching it, by walking clusters
    that are stored, and it is what
    ClusterSpace::getClusterVectorFromSupercellOrbitList uses on an arbitrary
    structure.

@param orbit orbit of the supercell orbit list whose clusters are counted
@param plan evaluation plan of the corresponding primitive orbit
@param occupations occupations of the supercell
@param counts buffer the counted patterns are accumulated into
*/
void ClusterSpace::countClustersOfOrbit(const Orbit &orbit,
                                        const OrbitEvaluationPlan &plan,
                                        OccupationSpan occupations,
                                        ClusterCountBuffer &counts) const
{
    PatternEncoder encoder(plan);
    for (const Cluster &cluster : orbit.clusters())
    {
        const std::vector<LatticeSite> &sites = cluster.latticeSites();
        encoder.begin();
        for (int position = 0; position < plan.order; position++)
        {
            encoder.add(occupations[sites[position].index()]);
        }
        if (encoder.anyUnallowed())
        {
            throwUnallowedOccupation(plan, "ClusterSpace::countClustersOfOrbit");
        }
        counts.add(encoder.pattern(), 1.0);
    }
}

/**
@details
    Assembles a full cluster vector from cluster counts supplied per orbit.
    The zerolet of a full cluster vector is always 1.
@param countClustersOfOrbit counting side of the assembly, see assembleClusterVector
@param supercellSize the number of sites in the supercell the counts refer to
@param maximumDistinctPatterns upper bound on the number of distinct occupation patterns one orbit can contribute
*/
std::vector<double> ClusterSpace::assembleFullClusterVector(
    const CountClustersOfOrbitFunction &countClustersOfOrbit,
    const size_t supercellSize,
    const size_t maximumDistinctPatterns) const
{
    return assembleClusterVector(countClustersOfOrbit, supercellSize, maximumDistinctPatterns,
                                 1.0, false);
}

/**
@details
    Assembles a local cluster vector, the contribution of one site, from
    cluster counts supplied per orbit.
    Local cluster vectors are an additive decomposition of the full cluster
    vector: summed over all sites of the supercell they reproduce it, as
    long as no cluster contains the same site more than once through
    periodic images.
    Two ingredients make that so.
    The zerolet, which is 1 in the full cluster vector, is considered as
    made up of equal contributions from all sites, so the zerolet of a
    local cluster vector is 1 / N with N the supercell size.
    Every other element is divided by the order of its orbit, because a
    cluster of order k is counted once for each of its k sites and would
    otherwise be counted k times in the sum over sites; see
    ClusterExpansionCalculator::getLocalClusterVector.
@param countClustersOfOrbit counting side of the assembly, see assembleClusterVector
@param supercellSize the number of sites in the supercell the counts refer to
@param maximumDistinctPatterns upper bound on the number of distinct occupation patterns one orbit can contribute
*/
std::vector<double> ClusterSpace::assembleLocalClusterVector(
    const CountClustersOfOrbitFunction &countClustersOfOrbit,
    const size_t supercellSize,
    const size_t maximumDistinctPatterns) const
{
    return assembleClusterVector(countClustersOfOrbit, supercellSize, maximumDistinctPatterns,
                                 1.0 / supercellSize, true);
}

/**
@details
    Assembles the change in the cluster vector caused by a change in
    occupation from cluster counts supplied per orbit, which for this
    assembly are expected to be count differences.
    The zerolet does not depend on the occupations, so its change is 0.
@param countClustersOfOrbit counting side of the assembly, see assembleClusterVector
@param supercellSize the number of sites in the supercell the counts refer to
@param maximumDistinctPatterns upper bound on the number of distinct occupation patterns one orbit can contribute
*/
std::vector<double> ClusterSpace::assembleClusterVectorChange(
    const CountClustersOfOrbitFunction &countClustersOfOrbit,
    const size_t supercellSize,
    const size_t maximumDistinctPatterns) const
{
    return assembleClusterVector(countClustersOfOrbit, supercellSize, maximumDistinctPatterns,
                                 0.0, false);
}

/**
@details
    Assembles a cluster vector from cluster counts supplied per orbit.

    This is the one place where cluster counts are turned into cluster
    vector elements; the callers differ only in how they count and in the
    zerolet.
    ClusterSpace::getClusterVectorFromOrbitList counts by walking the
    clusters stored in a supercell orbit list, and
    ClusterExpansionCalculator counts through its per-orbit evaluation
    tables.

@param countClustersOfOrbit
    Counts the clusters of the orbit with the given index in the primitive
    orbit list into the given buffer. Called once per active orbit, with a
    buffer that has been prepared and that is finished afterwards, so an
    implementation only has to add what it counts.
@param supercellSize
    The number of sites in the supercell the counts refer to.
@param maximumDistinctPatterns
    Upper bound on the number of distinct occupation patterns one orbit can
    contribute, used to size the counting buffer once for the whole call.
@param zerolet
    The leading element of the cluster vector, which does not depend on the
    counts and is fixed by which kind of cluster vector is being assembled.
@param divideElementsByOrder
    Whether to divide each element after the zerolet by the order of its
    orbit, which is what makes local cluster vectors an additive
    decomposition of the full cluster vector; see
    assembleLocalClusterVector.
*/
std::vector<double> ClusterSpace::assembleClusterVector(
    const CountClustersOfOrbitFunction &countClustersOfOrbit,
    const size_t supercellSize,
    const size_t maximumDistinctPatterns,
    const double zerolet,
    const bool divideElementsByOrder) const
{
    std::vector<double> clusterVector;
    clusterVector.push_back(zerolet);

    // One buffer for the whole call, reused from orbit to orbit, so that the
    // counting loops below it allocate nothing.
    ClusterCountBuffer counts;
    const size_t primitiveStructureSize = _primitiveOrbitList->structure().size();

    // The cluster vector holds one element per multi-component vector of
    // each active orbit, in orbit order, after the zerolet.
    clusterVector.reserve(size());

    for (size_t orbitIndex = 0; orbitIndex < _primitiveOrbitList->size(); orbitIndex++)
    {
        const OrbitEvaluationPlan &plan = _orbitEvaluationPlans[orbitIndex];
        if (!plan.active)
        {
            continue;
        }

        counts.prepare(maximumDistinctPatterns);
        countClustersOfOrbit(orbitIndex, counts);
        counts.finish();

        // One element per multi-component vector alpha of this orbit. These
        // are vectors of point function indices.
        //
        // Example 1: For a binary alloy we obtain [0, 0] and [0, 0, 0] for
        // pair and triplet terms, respectively.
        //
        // Example 2: For a ternary alloy we obtain [0, 0], [0, 1], [1, 0],
        // and [1, 1] for pairs (and similarly for triplets). However, if the
        // two sites of the pair are equivalent (which, for example, is
        // always the case in systems with one atom in the primitive cell,
        // such as FCC) [0, 1] and [1, 0] are considered equivalent and we
        // will only get one of them.
        for (const ClusterVectorElementPlan &element : plan.elements)
        {
            double value = averageClusterFunctionOverOrbit(
                element, plan, counts, primitiveStructureSize, supercellSize);
            if (divideElementsByOrder)
            {
                value /= (double)plan.order;
            }
            clusterVector.push_back(value);
        }
    }
    return clusterVector;
}
