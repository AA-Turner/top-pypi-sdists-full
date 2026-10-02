#include "ClusterExpansionCalculator.hpp"
#include <algorithm>
#include <set>
#include <sstream>

/**
@details Sets up a cluster expansion calculator for a specific supercell.
@param clusterSpace cluster space for which to set up the calculator
@param structure supercell for which to set up the calculator
@param fractionalPositionTolerance tolerance applied when comparing positions in fractional coordinates
*/
ClusterExpansionCalculator::ClusterExpansionCalculator(const ClusterSpace &clusterSpace,
                                                       const Structure &structure,
                                                       const double fractionalPositionTolerance)
    : _clusterSpace(clusterSpace),
      _occupations(structure.getAtomicNumbers()),
      _latticeMap(clusterSpace.primitiveStructure(), structure, fractionalPositionTolerance)
{
    // The occupations taken from the structure are held from here on, so they
    // are checked by the same criterion as an absolute update rather than left
    // to the first evaluation. An evaluation only meets a species on a site
    // that some active orbit reads, so pruning can leave an invalid species in
    // the held occupations that no evaluation ever reports.
    checkEverySpeciesAllowed(_occupations,
                             "ClusterExpansionCalculator::ClusterExpansionCalculator");

    // The per-orbit evaluation tables, which the entry points below resolve
    // through _latticeMap at call time.
    _evaluationTables = buildEvaluationTables(clusterSpace.getPrimitiveOrbitList(), _latticeMap);

    // How many distinct occupation patterns an orbit can produce is bounded
    // both by how many the species allow and by how many clusters the
    // evaluation counts, and the smaller of the two is what sizes the
    // counting buffer of a call. The three entry points count different
    // sets of clusters, so each gets its own bound.
    const std::vector<OrbitEvaluationPlan> &plans = _clusterSpace.orbitEvaluationPlans();
    for (size_t orbitIndex = 0; orbitIndex < _evaluationTables.orbitTables.size(); orbitIndex++)
    {
        const OrbitEvaluationTable &table = _evaluationTables.orbitTables[orbitIndex];
        const size_t allowedByTheSpecies = plans[orbitIndex].maximumDistinctPatterns;

        const size_t clustersInTheSupercell =
            table.numberOfBaseClusters * _latticeMap.numberOfCells();
        _maximumFullPatterns = std::max(_maximumFullPatterns,
                                        std::min(allowedByTheSpecies, clustersInTheSupercell));

        size_t clustersAtOneSite = 0;
        for (const auto &entries : table.localEntriesPerBasis)
        {
            clustersAtOneSite = std::max(clustersAtOneSite, entries.size());
        }
        _maximumLocalPatterns = std::max(_maximumLocalPatterns,
                                         std::min(allowedByTheSpecies, clustersAtOneSite));
        // A change evaluation counts each of those clusters twice, once as
        // it was and once as it becomes.
        _maximumChangePatterns = std::max(_maximumChangePatterns,
                                          std::min(allowedByTheSpecies, 2 * clustersAtOneSite));
    }
}

/**
@details
    Checks that the given occupations match the supercell of this calculator
    in size and that every site carries a species allowed on it, and if so
    returns them, moved into a vector owned by the caller of this function.
    Both are checked before anything is stored or evaluated, so occupations
    the model does not define cannot enter the held state.
    The occupation-taking full evaluation works on that call-owned copy,
    which is what makes it const and safe to call concurrently under the
    thread contract in the class description; setOccupations moves the copy
    into the held occupations, which is a mutation and requires exclusive
    access, as the contract states.
@param occupations occupation vector for the supercell
@param caller name of the calling function, used in the error message
*/
std::vector<int> ClusterExpansionCalculator::validateOccupations(std::vector<int> occupations,
                                                              const std::string &caller) const
{
    if (occupations.size() != _occupations.size())
    {
        std::ostringstream msg;
        msg << "Input occupations and internal supercell structure mismatch in size";
        msg << " (" << caller << ")";
        throw std::runtime_error(msg.str());
    }
    checkEverySpeciesAllowed(occupations, caller);
    return occupations;
}

/**
@details Checks that every occupation is allowed on the site it sits on.
@param occupations occupation vector for the supercell
@param caller name of the calling function, used in the error message
*/
void ClusterExpansionCalculator::checkEverySpeciesAllowed(const std::vector<int> &occupations,
                                                          const std::string &caller) const
{
    for (size_t siteIndex = 0; siteIndex < occupations.size(); siteIndex++)
    {
        checkOccupationAllowed((int)siteIndex, occupations[siteIndex], caller);
    }
}

/**
@details Checks that the given site index lies within the supercell.
@param index index of a site in the supercell
@param caller name of the calling function, used in the error message
*/
void ClusterExpansionCalculator::checkSiteIndex(const int index, const std::string &caller) const
{
    if (index < 0 || (size_t)index >= _occupations.size())
    {
        std::ostringstream msg;
        msg << "Site index " << index << " is not in the range [0, " << _occupations.size() << ")";
        msg << " (" << caller << ")";
        throw std::out_of_range(msg.str());
    }
}

/**
@details
    Checks that every flip of the given move names a site within the
    supercell, a non-negative atomic number, and a species allowed on that
    site.
    Both callers validate the whole batch before any of it is evaluated or
    applied, so a move naming a species the model does not define is refused
    rather than acted on.
    Leaving the species question to the counting loops would not answer it:
    a site that no active orbit reads, which pruning can produce, is never
    visited there, and the change would come back as zero rather than as an
    error.
@param move the move to validate
@param caller name of the calling function, used in the error message
*/
void ClusterExpansionCalculator::validateMove(const Move &move, const std::string &caller) const
{
    for (const auto &flip : move)
    {
        checkSiteIndex(flip.first, caller);
        if (flip.second < 0)
        {
            std::ostringstream msg;
            msg << "New occupation " << flip.second << " must be a non-negative atomic number";
            msg << " (" << caller << ")";
            throw std::invalid_argument(msg.str());
        }
        checkOccupationAllowed(flip.first, flip.second, caller);
    }
}

/**
@details
    Checks that the given atomic number is allowed on the given site.
    The criterion is membership in the species map of the basis site, which
    is the same source the counting loops enforce this from: the species
    index tables of the evaluation plans are built from these species maps
    (buildOrbitEvaluationPlans), and the plan construction requires permuted
    positions to allow the same species, so an occupation this check rejects
    is exactly one the counting loops would reject wherever they read it.
    The check is deliberately applied to every site, including a site that
    no active orbit reads: the held occupations describe a configuration of
    the model, and a species the model does not define has no place in them
    even where the evaluation would not notice it.
@param siteIndex index of a site in the supercell
@param occupation atomic number to check
@param caller name of the calling function, used in the error message
*/
void ClusterExpansionCalculator::checkOccupationAllowed(const int siteIndex,
                                                        const int occupation,
                                                        const std::string &caller) const
{
    const auto &speciesMap =
        _clusterSpace.getSpeciesMaps()[_latticeMap.basisIndexOfSite(siteIndex)];
    if (speciesMap.count(occupation) == 0)
    {
        std::vector<int> allowed;
        allowed.reserve(speciesMap.size());
        for (const auto &entry : speciesMap)
        {
            allowed.push_back(entry.first);
        }
        std::sort(allowed.begin(), allowed.end());

        std::ostringstream msg;
        msg << "Atomic number " << occupation << " is not allowed on site " << siteIndex;
        msg << ". The atomic numbers allowed there are";
        for (const int number : allowed)
        {
            msg << " " << number;
        }
        msg << " (" << caller << ")";
        throw std::invalid_argument(msg.str());
    }
}

/**
@details
    Replaces the held occupations of the supercell.
@param occupations occupation vector for the supercell
*/
void ClusterExpansionCalculator::setOccupations(std::vector<int> occupations)
{
    _occupations = validateOccupations(std::move(occupations),
                                       "ClusterExpansionCalculator::setOccupations");
}

/**
@details
    Advances the held occupations through the given moves, which is how an
    accepted move takes effect.
    Every flip of every move is validated before the first one is applied,
    including that the new atomic number is allowed on its site, so a
    rejected list of moves leaves the held occupations exactly as they
    were.
    The species check makes the accept seam at least as strict as the
    evaluating one: an unallowed species that entered the held occupations
    here would not fail until the next evaluation, far from its cause.
@param moves the moves to apply, in order
*/
void ClusterExpansionCalculator::applyMoves(const std::vector<Move> &moves)
{
    for (const Move &move : moves)
    {
        validateMove(move, "ClusterExpansionCalculator::applyMoves");
    }
    for (const Move &move : moves)
    {
        for (const auto &flip : move)
        {
            _occupations[flip.first] = flip.second;
        }
    }
}

namespace
{
/**
@brief Restores flipped occupations when it goes out of scope.
@details
    getClusterVectorChanges applies the flips of a move to the held
    occupations while it works through the move, and must leave them as it
    found them on every exit path, including an exception thrown by the
    evaluation of a later flip.
    This guard records the previous value of every site it flips and
    restores the recorded values in reverse order when it is destroyed,
    so a site flipped more than once within a move ends up at its original
    value.
*/
class OccupationRevertGuard
{
public:
    explicit OccupationRevertGuard(std::vector<int> &occupations)
        : _occupations(occupations)
    {
    }

    /// Sets the occupation of a site, recording what it replaces.
    void apply(const int siteIndex, const int newOccupation)
    {
        _appliedFlips.emplace_back(siteIndex, _occupations[siteIndex]);
        _occupations[siteIndex] = newOccupation;
    }

    ~OccupationRevertGuard()
    {
        for (auto flip = _appliedFlips.rbegin(); flip != _appliedFlips.rend(); flip++)
        {
            _occupations[flip->first] = flip->second;
        }
    }

private:
    /// The occupations the guard restores.
    std::vector<int> &_occupations;

    /// The applied flips, each holding the site index and the value it replaced.
    std::vector<std::pair<int, int>> _appliedFlips;
};
} // namespace

/**
@details
    Returns one cluster vector change per move.
    Each move is evaluated independently from the held occupations, and
    within a move the flips are applied sequentially, so the change of a
    two-site move is the change of the first flip plus the change of the
    second flip evaluated with the first one applied.
    The flips are applied to the held occupations while the move is
    evaluated and reverted afterwards, on every exit path, so this function
    is state-neutral; that transient mutation is why it is not const, and
    it is what the thread contract in the class description means by
    requiring exclusive access.
@param moves the moves to evaluate, each an ordered sequence of (site index, new atomic number) pairs
*/
std::vector<std::vector<double>> ClusterExpansionCalculator::getClusterVectorChanges(const std::vector<Move> &moves)
{
    for (const Move &move : moves)
    {
        validateMove(move, "ClusterExpansionCalculator::getClusterVectorChanges");
    }

    std::vector<std::vector<double>> changes;
    changes.reserve(moves.size());
    for (const Move &move : moves)
    {
        OccupationRevertGuard guard(_occupations);
        std::vector<double> change;
        for (size_t indexInMove = 0; indexInMove < move.size(); indexInMove++)
        {
            const auto &flip = move[indexInMove];
            std::vector<double> changeOfFlip =
                getClusterVectorChangeFromHeldOccupations(flip.first, flip.second);
            if (indexInMove == 0)
            {
                change = std::move(changeOfFlip);
            }
            else
            {
                for (size_t element = 0; element < change.size(); element++)
                {
                    change[element] += changeOfFlip[element];
                }
            }
            // Only a flip that another flip is evaluated after needs to be
            // applied; in particular a single-flip move, the shape a Monte
            // Carlo trial step produces, touches no state at all.
            if (indexInMove + 1 < move.size())
            {
                guard.apply(flip.first, flip.second);
            }
        }
        if (move.empty())
        {
            change.assign(_clusterSpace.size(), 0.0);
        }
        changes.push_back(std::move(change));
    }
    return changes;
}

/**
@details
    Counts the occupations of all clusters of one orbit over the whole
    supercell, by iterating the base clusters of the evaluation table over
    every anchor cell.
    This enumerates the same clusters as a full orbit list assembled from
    the per-offset local orbit lists, and since every cluster enters with a
    weight of exactly one, the counts are integers and independent of the
    enumeration order.
@param table evaluation table of the orbit
@param plan evaluation plan of the orbit
@param occupations occupations of the supercell
@param counts buffer the counted patterns are accumulated into
*/
void ClusterExpansionCalculator::countClusters(const OrbitEvaluationTable &table,
                                               const OrbitEvaluationPlan &plan,
                                               OccupationSpan occupations,
                                               ClusterCountBuffer &counts) const
{
    PatternEncoder encoder(plan);
    const size_t numberOfOffsets = _evaluationTables.relativeOffsets.size();
    for (size_t anchorCell = 0; anchorCell < _latticeMap.numberOfCells(); anchorCell++)
    {
        const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data() + anchorCell * numberOfOffsets;
        for (size_t c = 0; c < table.numberOfBaseClusters; c++)
        {
            const size_t base = c * table.order;
            encoder.begin();
            for (int i = 0; i < table.order; i++)
            {
                int32_t siteIndex = _latticeMap.siteIndexFromCellIndex(
                    table.slotBasisIndices[base + i],
                    neighborCells[table.slotRelativeOffsetIds[base + i]]);
                encoder.add(occupations[siteIndex]);
            }
            if (encoder.anyUnallowed())
            {
                throwUnallowedOccupation(plan, "ClusterExpansionCalculator::countClusters");
            }
            counts.add(encoder.pattern(), 1.0);
        }
    }
}

/**
@details
    Counts the occupations of the clusters of one orbit that contain the
    given site in its own cell, each weighted by 1 / n with n the number of
    occurrences of the site in the cluster.
    This reproduces, cluster by cluster and in the same order,
    Orbit::getClusterCounts with a double-counting correction site on the
    self-contained local orbit list of the cell of the site.
@param table evaluation table of the orbit
@param plan evaluation plan of the orbit
@param occupations occupations of the supercell
@param siteIndex index of the site whose local contribution is counted
@param counts buffer the counted patterns are accumulated into
*/
void ClusterExpansionCalculator::countClustersLocal(const OrbitEvaluationTable &table,
                                                    const OrbitEvaluationPlan &plan,
                                                    OccupationSpan occupations,
                                                    const int siteIndex,
                                                    ClusterCountBuffer &counts) const
{
    PatternEncoder encoder(plan);
    const size_t numberOfOffsets = _evaluationTables.relativeOffsets.size();
    const int32_t anchorCell = _latticeMap.cellIndexOfSite(siteIndex);
    const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data() + (size_t)anchorCell * numberOfOffsets;
    for (const auto &entry : table.localEntriesPerBasis[_latticeMap.basisIndexOfSite(siteIndex)])
    {
        const size_t base = (size_t)entry.clusterIndex * table.order;
        encoder.begin();
        for (int i = 0; i < table.order; i++)
        {
            int32_t clusterSiteIndex = _latticeMap.siteIndexFromCellIndex(
                table.slotBasisIndices[base + i],
                neighborCells[table.slotRelativeOffsetIds[base + i]]);
            encoder.add(occupations[clusterSiteIndex]);
        }
        if (encoder.anyUnallowed())
        {
            throwUnallowedOccupation(plan, "ClusterExpansionCalculator::countClustersLocal");
        }
        counts.add(encoder.pattern(), entry.unit);
    }
}

/**
@details
    Counts the changes in the occupations of the clusters of one orbit
    caused by changing the occupation of one site, over the same clusters
    and with the same weights as countClustersLocal.
    The new occupation is substituted at every slot that resolves to the
    flipped site, which includes its periodic images in supercells small
    enough for a cluster to contain both.
@param table evaluation table of the orbit
@param plan evaluation plan of the orbit
@param occupations occupations of the supercell before the change
@param flipIndex index of the site whose occupation changes
@param newOccupation new atomic number on that site
@param counts buffer the counted patterns are accumulated into
*/
void ClusterExpansionCalculator::countClusterChanges(const OrbitEvaluationTable &table,
                                                     const OrbitEvaluationPlan &plan,
                                                     OccupationSpan occupations,
                                                     const int flipIndex,
                                                     const int newOccupation,
                                                     ClusterCountBuffer &counts) const
{
    PatternEncoder encoderBefore(plan);
    PatternEncoder encoderAfter(plan);
    const size_t numberOfOffsets = _evaluationTables.relativeOffsets.size();
    const int32_t anchorCell = _latticeMap.cellIndexOfSite(flipIndex);
    const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data() + (size_t)anchorCell * numberOfOffsets;
    for (const auto &entry : table.localEntriesPerBasis[_latticeMap.basisIndexOfSite(flipIndex)])
    {
        const size_t base = (size_t)entry.clusterIndex * table.order;
        encoderBefore.begin();
        encoderAfter.begin();
        for (int i = 0; i < table.order; i++)
        {
            int32_t clusterSiteIndex = _latticeMap.siteIndexFromCellIndex(
                table.slotBasisIndices[base + i],
                neighborCells[table.slotRelativeOffsetIds[base + i]]);
            int occupation = occupations[clusterSiteIndex];
            encoderBefore.add(occupation);

            // If the present site is the one that was changed,
            // we need to use a different atomic number
            encoderAfter.add(clusterSiteIndex == flipIndex ? newOccupation : occupation);
        }
        if (encoderBefore.anyUnallowed() || encoderAfter.anyUnallowed())
        {
            throwUnallowedOccupation(plan, "ClusterExpansionCalculator::countClusterChanges");
        }
        // The old cluster has disappeared and we got the new one instead
        counts.add(encoderBefore.pattern(), -entry.unit);
        counts.add(encoderAfter.pattern(), entry.unit);
    }
}

/**
@details
    Returns the change in the cluster vector caused by changing the held
    occupation of one site, without changing the held occupations.
    The flip is expected to have been validated by the caller.
@param flipIndex index in the supercell where the occupation changes
@param newOccupation new atomic number on that site
*/
std::vector<double> ClusterExpansionCalculator::getClusterVectorChangeFromHeldOccupations(const int flipIndex,
                                                                                          const int newOccupation) const
{
    OccupationSpan occupationSpan(_occupations.data(), _occupations.size());
    const std::vector<OrbitEvaluationPlan> &plans = _clusterSpace.orbitEvaluationPlans();
    return _clusterSpace.assembleClusterVectorChange(
        [&](const size_t orbitIndex, ClusterCountBuffer &counts)
        {
            countClusterChanges(_evaluationTables.orbitTables[orbitIndex], plans[orbitIndex],
                                occupationSpan, flipIndex, newOccupation, counts);
        },
        _occupations.size(), _maximumChangePatterns);
}

/**
@details
    This constructs a cluster vector that only includes clusters that contain
    the input index.

    Normalization
    -------------

    Local cluster vectors are an additive decomposition of the cluster
    vector over the sites of the supercell,

        sum over i of getLocalClusterVector(i) = getClusterVector(),

    both sides evaluated from the held occupations.

    A cluster of order k is counted once for each of its k sites, so it
    contributes to the local cluster vector of every site it contains, and
    the assembly divides each element by the order of its orbit to
    compensate; the zerolet is 1 / N per site. See
    ClusterSpace::assembleLocalClusterVector, where both are applied.

    The additivity holds as long as no cluster contains the same site more
    than once through periodic images. When it does, that cluster enters
    the local cluster vector of the repeated site with a weight of 1 / n
    rather than n times, where n is the number of occurrences, and the sum
    falls short by the difference. See countClustersLocal, where the
    counting is done, and ClusterSpace.are_local_cluster_vectors_additive
    on the Python side, which tests whether a given supercell satisfies the
    condition.

@param index the local index of the supercell
*/
std::vector<double> ClusterExpansionCalculator::getLocalClusterVector(const int index) const
{
    checkSiteIndex(index, "ClusterExpansionCalculator::getLocalClusterVector");

    OccupationSpan occupationSpan(_occupations.data(), _occupations.size());
    const std::vector<OrbitEvaluationPlan> &plans = _clusterSpace.orbitEvaluationPlans();
    return _clusterSpace.assembleLocalClusterVector(
        [&](const size_t orbitIndex, ClusterCountBuffer &counts)
        {
            countClustersLocal(_evaluationTables.orbitTables[orbitIndex], plans[orbitIndex],
                               occupationSpan, index, counts);
        },
        _occupations.size(), _maximumLocalPatterns);
}

/**
@details Calculate the cluster vector for the given occupations of the supercell.
@param occupations the occupation vector of the supercell
*/
std::vector<double> ClusterExpansionCalculator::getClusterVector(std::vector<int> occupationsIn) const
{
    std::vector<int> occupations = validateOccupations(std::move(occupationsIn), "ClusterExpansionCalculator::getClusterVector");

    OccupationSpan occupationSpan(occupations.data(), occupations.size());
    const std::vector<OrbitEvaluationPlan> &plans = _clusterSpace.orbitEvaluationPlans();
    return _clusterSpace.assembleFullClusterVector(
        [&](const size_t orbitIndex, ClusterCountBuffer &counts)
        {
            countClusters(_evaluationTables.orbitTables[orbitIndex], plans[orbitIndex],
                          occupationSpan, counts);
        },
        _occupations.size(), _maximumFullPatterns);
}

/**
@details Calculate the cluster vector for the held occupations of the supercell.
*/
std::vector<double> ClusterExpansionCalculator::getClusterVector() const
{
    OccupationSpan occupationSpan(_occupations.data(), _occupations.size());
    const std::vector<OrbitEvaluationPlan> &plans = _clusterSpace.orbitEvaluationPlans();
    return _clusterSpace.assembleFullClusterVector(
        [&](const size_t orbitIndex, ClusterCountBuffer &counts)
        {
            countClusters(_evaluationTables.orbitTables[orbitIndex], plans[orbitIndex],
                          occupationSpan, counts);
        },
        _occupations.size(), _maximumFullPatterns);
}

/**
@details
    Returns whether the local cluster vectors of this supercell sum to its
    cluster vector, which is the precondition for using them as an additive
    decomposition; the setup-time check that
    ClusterSpace.are_local_cluster_vectors_additive exposes on the Python
    side.

    The answer is read off the evaluation tables, where it is a byproduct
    of their construction, as follows.
    The decomposition fails exactly when some cluster contains the same
    supercell site more than once through periodic images, because such a
    cluster enters the local counting with a weight of 1 / n, with n its
    number of occurrences of the repeated site, instead of once per site.
    That weight is precomputed: it is the unit of the local entry
    (OrbitEvaluationTable::LocalEntry), so a cluster with a repeated site
    is a local entry whose unit is below one.
    The scan below covers every cluster of the supercell, not merely every
    cluster near one cell, because every cluster contains a site, that site
    is some basis index in some cell, and viewed from that cell as the
    anchor the cluster appears among the local entries of that basis index;
    the entries of one anchor cell stand for their translations to every
    other cell, which resolve to the same multiset of sites up to
    translation and therefore repeat a site if and only if the entry does.
*/
bool ClusterExpansionCalculator::areLocalClusterVectorsAdditive() const
{
    for (const OrbitEvaluationTable &table : _evaluationTables.orbitTables)
    {
        for (const auto &entries : table.localEntriesPerBasis)
        {
            for (const auto &entry : entries)
            {
                if (entry.unit < 1.0)
                {
                    return false;
                }
            }
        }
    }
    return true;
}

/**
@details
    Returns whether any two clusters of this supercell consist of the same
    sites through periodic boundary conditions, which is the condition
    ClusterSpace.is_supercell_self_interacting exposes on the Python side;
    a supercell that self-interacts can produce misleading results, because
    distinct interaction terms of the model are evaluated on the same group
    of sites.

    The scan below compares only the local entries of one anchor cell, per
    basis index and across all orbits, which is a size-independent amount
    of work, and it is exact for the following reasons.
    Take any two distinct clusters of the supercell with the same site
    multiset, and let s = (basis b, cell c) be their first site, which they
    share since their sites are identical.
    Both clusters contain the site of basis b in cell c, so both appear
    among the local entries of basis b resolved at anchor cell c, as
    distinct entries, since the map from (entry, anchor) to a cluster of
    the supercell is injective for a fixed anchor.
    Resolving an entry at anchor c translates the sites it resolves to at
    anchor 0 by the offset of c, and that translation is a bijection on
    site indices, so two entries resolve to equal site multisets at anchor
    c exactly when they do at anchor 0.
    The collision therefore already exists among the entries of basis b at
    anchor 0, which is where the scan looks; conversely, two distinct
    entries of one basis resolving to the same sites are two distinct
    clusters of the supercell on the same sites.

    The sets span all orbits within each basis, so two clusters of
    different orbits landing on the same sites, the subtler form of
    self-interaction, are detected as well as two clusters of one orbit.
    A cluster containing the same site twice does not by itself make the
    supercell self-interacting; it takes a second cluster on the same
    sites. That is why this condition is independent of the additivity of
    the local cluster vectors, and a supercell can self-interact while the
    additive decomposition still holds exactly.
    The equivalence of this criterion with the definition on a full
    supercell orbit list is asserted for every case-matrix system in
    tests/golden/test_setup_time_checks.py.
*/
bool ClusterExpansionCalculator::isSelfInteracting() const
{
    // The row of neighbor cell indices of anchor cell 0.
    const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data();
    for (size_t basisIndex = 0; basisIndex < _latticeMap.numberOfBasisSites(); basisIndex++)
    {
        std::set<std::vector<int>> sortedClusterSites;
        for (const OrbitEvaluationTable &table : _evaluationTables.orbitTables)
        {
            for (const auto &entry : table.localEntriesPerBasis[basisIndex])
            {
                const size_t base = (size_t)entry.clusterIndex * table.order;
                std::vector<int> clusterSiteIndices(table.order);
                for (int i = 0; i < table.order; i++)
                {
                    clusterSiteIndices[i] = _latticeMap.siteIndexFromCellIndex(
                        table.slotBasisIndices[base + i],
                        neighborCells[table.slotRelativeOffsetIds[base + i]]);
                }
                std::sort(clusterSiteIndices.begin(), clusterSiteIndices.end());
                if (!sortedClusterSites.insert(std::move(clusterSiteIndices)).second)
                {
                    return true;
                }
            }
        }
    }
    return false;
}

/**
@details
    Returns, per orbit, the supercell site indices of the clusters of the
    local view of the given site, in the order countClustersLocal visits
    them.
    This function exists only for the equivalence gate in
    tests/golden/test_evaluation_table_equivalence.py, which compares this
    enumeration against the per-offset local orbit lists generated by
    LocalOrbitListGenerator.
@param siteIndex index of a site in the supercell
*/
std::vector<std::vector<std::vector<int>>> ClusterExpansionCalculator::getLocalClusterSiteIndices(const int siteIndex) const
{
    checkSiteIndex(siteIndex, "ClusterExpansionCalculator::getLocalClusterSiteIndices");
    std::vector<std::vector<std::vector<int>>> siteIndicesPerOrbit;
    const size_t numberOfOffsets = _evaluationTables.relativeOffsets.size();
    const int32_t anchorCell = _latticeMap.cellIndexOfSite(siteIndex);
    const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data() + (size_t)anchorCell * numberOfOffsets;
    for (const OrbitEvaluationTable &table : _evaluationTables.orbitTables)
    {
        std::vector<std::vector<int>> clusters;
        for (const auto &entry : table.localEntriesPerBasis[_latticeMap.basisIndexOfSite(siteIndex)])
        {
            const size_t base = (size_t)entry.clusterIndex * table.order;
            std::vector<int> clusterSiteIndices(table.order);
            for (int i = 0; i < table.order; i++)
            {
                clusterSiteIndices[i] = _latticeMap.siteIndexFromCellIndex(
                    table.slotBasisIndices[base + i],
                    neighborCells[table.slotRelativeOffsetIds[base + i]]);
            }
            clusters.push_back(std::move(clusterSiteIndices));
        }
        siteIndicesPerOrbit.push_back(std::move(clusters));
    }
    return siteIndicesPerOrbit;
}

/**
@details
    Returns, per orbit, the double-counting weights of the clusters of the
    local view of the given site, aligned with getLocalClusterSiteIndices.
    This function exists only for the equivalence gate.
@param siteIndex index of a site in the supercell
*/
std::vector<std::vector<double>> ClusterExpansionCalculator::getLocalClusterWeights(const int siteIndex) const
{
    checkSiteIndex(siteIndex, "ClusterExpansionCalculator::getLocalClusterWeights");
    std::vector<std::vector<double>> weightsPerOrbit;
    for (const OrbitEvaluationTable &table : _evaluationTables.orbitTables)
    {
        std::vector<double> weights;
        for (const auto &entry : table.localEntriesPerBasis[_latticeMap.basisIndexOfSite(siteIndex)])
        {
            weights.push_back(entry.unit);
        }
        weightsPerOrbit.push_back(std::move(weights));
    }
    return weightsPerOrbit;
}

/**
@details
    Returns, per orbit, the supercell site indices of the base clusters
    anchored at the given cell offset, in the order countClusters visits
    them for that anchor cell.
    This function exists only for the equivalence gate, which compares this
    enumeration against a local orbit list generated for the same offset.
@param cellOffset cell offset in units of the primitive lattice vectors
*/
std::vector<std::vector<std::vector<int>>> ClusterExpansionCalculator::getFullClusterSiteIndices(const Vector3i &cellOffset) const
{
    std::vector<std::vector<std::vector<int>>> siteIndicesPerOrbit;
    const size_t numberOfOffsets = _evaluationTables.relativeOffsets.size();
    const int32_t anchorCell = _latticeMap.cellIndex(cellOffset);
    const int32_t *neighborCells = _evaluationTables.neighborCellIndices.data() + (size_t)anchorCell * numberOfOffsets;
    for (const OrbitEvaluationTable &table : _evaluationTables.orbitTables)
    {
        std::vector<std::vector<int>> clusters;
        for (size_t c = 0; c < table.numberOfBaseClusters; c++)
        {
            const size_t base = c * table.order;
            std::vector<int> clusterSiteIndices(table.order);
            for (int i = 0; i < table.order; i++)
            {
                clusterSiteIndices[i] = _latticeMap.siteIndexFromCellIndex(
                    table.slotBasisIndices[base + i],
                    neighborCells[table.slotRelativeOffsetIds[base + i]]);
            }
            clusters.push_back(std::move(clusterSiteIndices));
        }
        siteIndicesPerOrbit.push_back(std::move(clusters));
    }
    return siteIndicesPerOrbit;
}
