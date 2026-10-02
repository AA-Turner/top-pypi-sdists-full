#define _USE_MATH_DEFINES
#include <cmath>

#include <algorithm>
#include <sstream>
#include <stdexcept>

#include "OrbitEvaluationPlan.hpp"

double evaluatePointFunction(const int numberOfAllowedSpecies,
                             const int pointFunction,
                             const int speciesIndex)
{
    const double argument = 2.0 * M_PI * (double)((pointFunction + 2) / 2) *
                            (double)speciesIndex / (double)numberOfAllowedSpecies;
    if (pointFunction % 2 == 0)
    {
        return -cos(argument);
    }
    return -sin(argument);
}

namespace
{

/// Largest pattern code width, in bits, that fits in a non-negative int64_t.
constexpr int MAXIMUM_PATTERN_BITS = 62;

/// Ceiling above which the count of distinct patterns is left to be bounded
/// by the number of clusters counted instead. The product of the allowed
/// species over the positions of a cluster is an upper bound on how many
/// patterns it can take, but it grows as a power of the order and is a
/// useless bound long before it overflows.
constexpr size_t MAXIMUM_PATTERN_BOUND = 1 << 16;

/// Returns the site indices of the representative cluster of the given orbit.
std::vector<int> representativeSiteIndices(const Orbit &orbit)
{
    std::vector<int> indices;
    for (const LatticeSite &site : orbit.representativeCluster().latticeSites())
    {
        indices.push_back(site.index());
    }
    return indices;
}

/**
@details
    Checks the precondition that the tabulation of the point functions
    rests on.

    A cluster contributes to a cluster vector element once per site
    permutation of its multi-component vector. Under a permutation p, the
    species that occupies position i of the cluster is combined with the
    point function and the allowed-species count belonging to position
    p[i]. That only means anything if the two positions allow the same
    species, and it is what lets the species that occupies a position be
    reduced to a species index before the permutations are applied.

    The permutations are symmetry operations that map a cluster onto itself
    within its orbit, so they relate positions that are symmetry equivalent
    and hence carry the same allowed species. That argument is not a
    guarantee, and a cluster space that violated it would produce silently
    wrong cluster vectors rather than fail, so it is checked here instead of
    assumed. It costs one comparison per position per permutation, once per
    cluster space.

@param orbit the orbit being planned
@param orbitIndex index of that orbit, used in the error message
@param siteIndices site indices of the representative cluster
@param speciesMaps species maps of the primitive structure
*/
void checkPermutedPositionsAllowTheSameSpecies(
    const Orbit &orbit,
    const size_t orbitIndex,
    const std::vector<int> &siteIndices,
    const std::vector<std::unordered_map<int, int>> &speciesMaps)
{
    for (const ClusterVectorElement &element : orbit.clusterVectorElements())
    {
        for (const std::vector<int> &permutation : element.sitePermutations)
        {
            for (size_t position = 0; position < permutation.size(); position++)
            {
                const size_t permuted = (size_t)permutation[position];
                if (speciesMaps[siteIndices[position]] != speciesMaps[siteIndices[permuted]])
                {
                    std::ostringstream msg;
                    msg << "Positions " << position << " and " << permuted
                        << " of the clusters of orbit " << orbitIndex
                        << " are related by a site permutation but do not allow"
                        << " the same species, so the cluster function of that orbit"
                        << " is not well defined"
                        << " (buildOrbitEvaluationPlans).";
                    throw std::runtime_error(msg.str());
                }
            }
        }
    }
}

/**
@details
    Tabulates the point function values of one cluster vector element.

    The table answers, for a site permutation, a position of the cluster and
    a species index at that position, what evaluatePointFunction returns for
    the point function that the multi-component vector selects. The species
    index is the one used when the pattern was encoded, meaning the index in
    the enumeration of the species allowed at that position, while the point
    function and the allowed-species count come from the permuted position,
    which is the combination ClusterSpace applies. The two positions allow
    the same species, as checked above, so the species index carries over
    unchanged.

@param element the cluster vector element of the orbit
@param numberOfAllowedSpecies number of allowed species per position of the representative cluster
@param speciesStride number of species-index values a position of this orbit can take
*/
std::vector<double> tabulatePointFunctionValues(const ClusterVectorElement &element,
                                                const std::vector<int> &numberOfAllowedSpecies,
                                                const size_t speciesStride)
{
    const size_t order = numberOfAllowedSpecies.size();
    std::vector<double> values(element.sitePermutations.size() * order * speciesStride, 0.0);
    for (size_t permutation = 0; permutation < element.sitePermutations.size(); permutation++)
    {
        for (size_t position = 0; position < order; position++)
        {
            const size_t permuted = (size_t)element.sitePermutations[permutation][position];
            const size_t base = (permutation * order + position) * speciesStride;
            // Species indices beyond what this position allows cannot occur
            // in a pattern; their entries stay at the zero the table was
            // filled with and are never read.
            for (int speciesIndex = 0; speciesIndex < numberOfAllowedSpecies[position]; speciesIndex++)
            {
                values[base + (size_t)speciesIndex] =
                    evaluatePointFunction(numberOfAllowedSpecies[permuted],
                                          element.multiComponentVector[permuted],
                                          speciesIndex);
            }
        }
    }
    return values;
}

} // namespace

[[noreturn]] void throwUnallowedOccupation(const OrbitEvaluationPlan &plan, const char *caller)
{
    std::ostringstream msg;
    msg << "A site of a cluster of order " << plan.order
        << " is occupied by a species that is not allowed on it"
        << " (" << caller << ").";
    throw std::runtime_error(msg.str());
}

std::vector<OrbitEvaluationPlan> buildOrbitEvaluationPlans(
    const OrbitList &primitiveOrbitList,
    const std::vector<std::unordered_map<int, int>> &speciesMaps)
{
    // One range of atomic numbers shared by every orbit, so that a species
    // index table row is indexed the same way whichever orbit it belongs to.
    int lowestAtomicNumber = 0;
    int highestAtomicNumber = 0;
    bool anySpeciesSeen = false;
    for (const std::unordered_map<int, int> &speciesMap : speciesMaps)
    {
        for (const auto &speciesPair : speciesMap)
        {
            if (!anySpeciesSeen)
            {
                lowestAtomicNumber = speciesPair.first;
                highestAtomicNumber = speciesPair.first;
                anySpeciesSeen = true;
            }
            lowestAtomicNumber = std::min(lowestAtomicNumber, speciesPair.first);
            highestAtomicNumber = std::max(highestAtomicNumber, speciesPair.first);
        }
    }
    // With no allowed species anywhere every orbit is inactive, so the table
    // holds nothing but the out-of-range entry.
    const int atomicNumberCount = anySpeciesSeen ? highestAtomicNumber - lowestAtomicNumber + 1 : 0;

    std::vector<OrbitEvaluationPlan> plans;
    for (size_t orbitIndex = 0; orbitIndex < primitiveOrbitList.size(); orbitIndex++)
    {
        const Orbit &orbit = primitiveOrbitList.getOrbit(orbitIndex);
        OrbitEvaluationPlan plan;
        plan.lowestAtomicNumber = lowestAtomicNumber;
        plan.atomicNumberCount = atomicNumberCount;

        // An inactive orbit has a site on which fewer than two species are
        // allowed, contributes no cluster vector element, and is never
        // counted, so it needs no plan beyond being marked inactive.
        if (!orbit.active())
        {
            plans.push_back(std::move(plan));
            continue;
        }

        plan.active = true;
        plan.order = (int)orbit.order();
        const std::vector<int> numberOfAllowedSpecies =
            orbit.representativeCluster().getNumberOfAllowedSpeciesPerSite();
        const std::vector<int> siteIndices = representativeSiteIndices(orbit);

        checkPermutedPositionsAllowTheSameSpecies(orbit, orbitIndex, siteIndices, speciesMaps);

        plan.speciesStride = (size_t)*std::max_element(numberOfAllowedSpecies.begin(),
                                                       numberOfAllowedSpecies.end());
        plan.speciesIndexBits = 1;
        while (((size_t)1 << plan.speciesIndexBits) < plan.speciesStride)
        {
            plan.speciesIndexBits++;
        }
        if (plan.speciesIndexBits * plan.order > MAXIMUM_PATTERN_BITS)
        {
            std::ostringstream msg;
            msg << "The occupation pattern of a cluster of order " << plan.order
                << " with up to " << plan.speciesStride
                << " allowed species per site does not fit in one integer"
                << " (buildOrbitEvaluationPlans).";
            throw std::runtime_error(msg.str());
        }

        // How many distinct patterns the clusters of this orbit can take,
        // which is what sizes the counting buffer.
        plan.maximumDistinctPatterns = 1;
        for (const int allowed : numberOfAllowedSpecies)
        {
            plan.maximumDistinctPatterns *= (size_t)allowed;
            if (plan.maximumDistinctPatterns >= MAXIMUM_PATTERN_BOUND)
            {
                plan.maximumDistinctPatterns = MAXIMUM_PATTERN_BOUND;
                break;
            }
        }

        // The species index table, one row per position of the cluster, with
        // the row entry beyond the atomic numbers covered standing for every
        // atomic number outside the range.
        plan.speciesIndices.assign((size_t)plan.order * (size_t)(atomicNumberCount + 1), -1);
        for (int position = 0; position < plan.order; position++)
        {
            const size_t base = (size_t)position * (size_t)(atomicNumberCount + 1);
            for (const auto &speciesPair : speciesMaps[siteIndices[position]])
            {
                plan.speciesIndices[base + (size_t)(speciesPair.first - lowestAtomicNumber)] =
                    (int32_t)speciesPair.second;
            }
        }

        for (const ClusterVectorElement &element : orbit.clusterVectorElements())
        {
            ClusterVectorElementPlan elementPlan;
            elementPlan.multiplicity = element.multiplicity;
            elementPlan.numberOfSitePermutations = element.sitePermutations.size();
            elementPlan.pointFunctionValues =
                tabulatePointFunctionValues(element, numberOfAllowedSpecies, plan.speciesStride);
            plan.elements.push_back(std::move(elementPlan));
        }

        plans.push_back(std::move(plan));
    }
    return plans;
}
