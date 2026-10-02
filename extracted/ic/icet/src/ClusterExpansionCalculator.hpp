#pragma once
#include <Eigen/Dense>
#include <string>
#include <vector>
#include "ClusterSpace.hpp"
#include "LatticeMap.hpp"
#include "OrbitEvaluationTable.hpp"
#include "Structure.hpp"
using namespace Eigen;

/**
@brief This class provides a cluster expansion calculator.

@details
    A cluster expansion calculator is specific for a certain supercell. Upon
    initialization various quantities specific to the given supercell are
    precomputed. This greatly speeds up subsequent calculations and enables one
    to carry out e.g., Monte Carlo simulations in a computationally efficient
    manner.

    Evaluation works on one representative description of the clusters of
    each orbit (see OrbitEvaluationTable), resolved to supercell site
    indices through a LatticeMap at call time, rather than on stored copies
    of the clusters per primitive cell of the supercell.

    Occupation state
    ----------------

    The calculator holds the occupations of its supercell, initialized from
    the structure it is constructed with.
    setOccupations replaces them, applyMoves advances them through a list
    of moves, and the local and change evaluations read them, so those
    evaluations no longer carry an occupation vector whose transfer would
    cost O(N) per call.
    A move is an ordered sequence of (site index, new atomic number) pairs,
    so a swap of two sites is a move of length two and a single flip is a
    move of length one.

    Thread contract
    ---------------

    This class follows the standard C++ container contract.
    Const member functions may be called concurrently on one calculator, as
    long as no thread concurrently calls a non-const member function on it;
    they share only immutable data and per-call buffers.
    The non-const member functions, setOccupations, applyMoves, and
    getClusterVectorChanges, require exclusive access to the calculator.
    getClusterVectorChanges is non-const because it applies and reverts the
    flips of each move on the held occupations; it restores them on every
    exit path, including an exception thrown mid-move, so it is
    state-neutral.
    Distinct calculators are fully independent even when they share a
    cluster space, since everything shared is immutable.
**/
class ClusterExpansionCalculator
{
public:
    /// A move: an ordered sequence of (site index, new atomic number) pairs.
    using Move = std::vector<std::pair<int, int>>;

    /// Constructor.
    ClusterExpansionCalculator(const ClusterSpace &, const Structure &, const double);

    /// Replaces the held occupations of the supercell.
    void setOccupations(std::vector<int>);

    /// Returns the held occupations of the supercell.
    const std::vector<int> &getOccupations() const { return _occupations; }

    /// Advances the held occupations through the given moves.
    void applyMoves(const std::vector<Move> &);

    /// Returns one cluster vector change per move, each evaluated from the
    /// held occupations, which are unchanged when this function returns.
    std::vector<std::vector<double>> getClusterVectorChanges(const std::vector<Move> &);

    /// Returns the length of the cluster vectors this calculator produces.
    size_t clusterVectorLength() const { return _clusterSpace.size(); }

    /// Returns the full cluster vector of the given occupations.
    std::vector<double> getClusterVector(std::vector<int>) const;

    /// Returns the full cluster vector of the held occupations.
    std::vector<double> getClusterVector() const;

    /// Returns a local cluster vector, the contribution of one site to the
    /// cluster vector of the held occupations.
    std::vector<double> getLocalClusterVector(const int) const;

    /// Returns whether the local cluster vectors of this supercell sum to
    /// its cluster vector.
    bool areLocalClusterVectorsAdditive() const;

    /// Returns whether any two clusters of this supercell consist of the
    /// same sites through periodic boundary conditions.
    bool isSelfInteracting() const;

    /// Returns the resolved cluster site indices per orbit for the local
    /// view of one site; read by the equivalence gate in
    /// tests/cpp/test_main.cpp.
    std::vector<std::vector<std::vector<int>>> getLocalClusterSiteIndices(const int) const;

    /// Returns the double-counting weights per orbit for the local view of
    /// one site; read by the equivalence gate.
    std::vector<std::vector<double>> getLocalClusterWeights(const int) const;

    /// Returns the resolved cluster site indices per orbit for the base
    /// clusters anchored at the given cell offset; read by the equivalence
    /// gate.
    std::vector<std::vector<std::vector<int>>> getFullClusterSiteIndices(const Vector3i &) const;

private:
    /// Checks the size of the given occupations against the supercell and,
    /// if they match, hands them back, owned by the caller of this
    /// function; see the thread contract in the class description for
    /// which callers may run concurrently.
    std::vector<int> validateOccupations(std::vector<int>, const std::string &) const;

    /// Checks that every occupation is allowed on the site it sits on.
    void checkEverySpeciesAllowed(const std::vector<int> &, const std::string &) const;

    /// Checks that a site index lies within the supercell.
    void checkSiteIndex(const int, const std::string &) const;

    /// Checks that every flip of the given move names a site within the
    /// supercell and a non-negative atomic number.
    void validateMove(const Move &, const std::string &) const;

    /// Checks that the given atomic number is allowed on the given site.
    void checkOccupationAllowed(const int, const int, const std::string &) const;

    /// Returns the change in the cluster vector caused by changing the held
    /// occupation of one site, without changing the held occupations.
    std::vector<double> getClusterVectorChangeFromHeldOccupations(const int, const int) const;

    /// Counts the occupations of all clusters of one orbit over the whole supercell.
    void countClusters(const OrbitEvaluationTable &, const OrbitEvaluationPlan &, OccupationSpan, ClusterCountBuffer &) const;

    /// Counts the occupations of the clusters of one orbit that contain one site.
    void countClustersLocal(const OrbitEvaluationTable &, const OrbitEvaluationPlan &, OccupationSpan, const int, ClusterCountBuffer &) const;

    /// Counts the changes in the occupations of the clusters of one orbit
    /// caused by changing the occupation of one site.
    void countClusterChanges(const OrbitEvaluationTable &, const OrbitEvaluationPlan &, OccupationSpan, const int, const int, ClusterCountBuffer &) const;

    /**
    @brief Internal cluster space.
    @details
        This is a copy of the cluster space handed to the constructor, taken
        when this calculator is constructed. It shares the primitive orbit list
        with the original through a pointer to const, and orbit lists are
        immutable, so the model this calculator evaluates is fixed at
        construction. Pruning or merging orbits on the originating cluster
        space afterwards gives that cluster space a different orbit list and
        leaves this copy, and therefore this calculator, as it was.
    */
    ClusterSpace _clusterSpace;

    /**
    @brief The held occupations of the supercell.
    @details
        This is the one copy of the configuration the calculator holds, and
        its length is the size of the supercell.
        Mutated only by setOccupations and applyMoves, and, transiently, by
        getClusterVectorChanges, which restores them on every exit path.
        The const evaluation entry points read them, which is what the
        thread contract in the class description is about.
    */
    std::vector<int> _occupations;

    /// Maps between supercell site indices and primitive-frame lattice sites.
    LatticeMap _latticeMap;

    /// Per-orbit cluster descriptions, resolved through _latticeMap at call time.
    EvaluationTables _evaluationTables;

    /// Upper bound on the distinct occupation patterns one orbit contributes to a full cluster vector.
    size_t _maximumFullPatterns = 0;

    /// Upper bound on the distinct occupation patterns one orbit contributes to a local cluster vector.
    size_t _maximumLocalPatterns = 0;

    /// Upper bound on the distinct occupation patterns one orbit contributes to a change in the cluster vector.
    size_t _maximumChangePatterns = 0;
};
