#pragma once

#include <cstddef>
#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>

#include "ClusterCountBuffer.hpp"
#include "OrbitList.hpp"

/**
@brief Evaluates a point function, also called an orthogonal point function.
@details
    The point functions are defined as

        Theta_n(sigma) = 1                            if n = 0
                       = -cos(pi (n + 1) sigma / M)   if n is odd
                       = -sin(pi n sigma / M)         if n is even

    where M is the number of allowed species on the site and sigma is the
    index of the species that occupies it.

    Note that the index n used in this definition counts the constant
    function as n = 0, whereas the pointFunction argument of this function
    counts the first non-trivial function as 0. The two indices therefore
    differ by one, which is why the expressions below appear to interchange
    the cases: an even pointFunction corresponds to an odd n and hence to
    the cosine branch.

    ClusterSpace::evaluateClusterFunction is the name this is exposed under
    on the Python side.

@param numberOfAllowedSpecies number of allowed species on the site in question, M above
@param pointFunction index of the point function, equal to n - 1 above; must be non-negative
@param speciesIndex index of the species that occupies the site, sigma above
@returns the value of the point function
*/
double evaluatePointFunction(const int numberOfAllowedSpecies,
                             const int pointFunction,
                             const int speciesIndex);

/**
@brief What one element of the cluster vector needs in order to be evaluated.
@details
    An element is identified by an orbit and a multi-component vector alpha.
    Everything that depends on alpha but not on the occupations is worked
    out once, when the cluster space is set up.

    The point functions are tabulated rather than evaluated per call.
    A cluster contributes to this element once per site permutation of
    alpha, and under a given permutation the value contributed by position i
    of the cluster depends only on the species that occupies that position.
    That species enters the counting loops as a species index, so the whole
    dependence fits in a lookup table indexed by (permutation, position,
    species index), holding exactly the numbers evaluatePointFunction would
    have returned.
*/
struct ClusterVectorElementPlan
{
    /**
    @brief Multiplicity of this element.
    @details
        Site permutations times the number of clusters in the primitive
        orbit, which is what turns the sum over counted clusters into an
        average; see averageClusterFunctionOverOrbit.
    */
    size_t multiplicity;

    /// Number of site permutations this element is counted under.
    size_t numberOfSitePermutations;

    /**
    @brief Tabulated point function values.
    @details
        Indexed as ((permutation * order) + position) * speciesStride +
        species index, where speciesStride comes from the orbit plan.
        Entries for species indices that cannot occur at a position are
        present as padding and are never read.
    */
    std::vector<double> pointFunctionValues;
};

/**
@brief What one orbit needs in order to be evaluated.
@details
    Where OrbitEvaluationTable describes where the clusters of an orbit sit,
    this describes what their occupations mean: how the species on their
    sites become a pattern code, and how the patterns become cluster vector
    elements.

    Encoding
    --------

    The occupation pattern of a cluster is encoded into one integer. Each
    position of the cluster contributes one digit, the index of the species
    that occupies it in the enumeration of the species allowed at that
    position, and the digits are packed at a fixed width of
    speciesIndexBits, position 0 first. Two properties follow, and the
    counting loops rely on both.

    Distinct patterns have distinct codes, because every digit fits in its
    field. And codes compare in the same order as the patterns they encode
    compare position by position, because the fields are equally wide and
    position 0 is the most significant. Since the species allowed at a
    position are numbered by increasing atomic number, that is also the
    order in which the patterns compare by atomic number.

    Species indices are read from a flat table indexed by atomic number
    rather than looked up in a hash map. The table covers one range of
    atomic numbers shared by all orbits, with one further entry at the end
    that stands for every atomic number outside that range, so that an
    atomic number that is not allowed at a position and one that is out of
    range alike yield -1 and are caught by the same test.
*/
struct OrbitEvaluationPlan
{
    /// Whether this orbit contributes to the cluster vector at all.
    bool active = false;

    /// Number of sites per cluster.
    int order = 0;

    /// Width in bits of the field one position occupies in a pattern code.
    int speciesIndexBits = 0;

    /// Number of species-index values a position of this orbit can take.
    size_t speciesStride = 0;

    /// Upper bound on the number of distinct patterns the clusters of this orbit can take.
    size_t maximumDistinctPatterns = 0;

    /// Lowest atomic number the species index table covers.
    int lowestAtomicNumber = 0;

    /// Number of atomic numbers the species index table covers, and the index of its out-of-range entry.
    int atomicNumberCount = 0;

    /**
    @brief Species index per position and atomic number, or -1 where the species is not allowed.
    @details
        Indexed as position * (atomicNumberCount + 1) + atomic number -
        lowestAtomicNumber, with the last entry of each row reserved for
        atomic numbers outside the range covered.

        Two pieces of code know that layout, and deliberately only two:
        buildOrbitEvaluationPlans, which fills the table, and PatternEncoder,
        which reads it. Anything else that needs a species index should go
        through the encoder rather than index the table itself, so that the
        layout and the convention for an atomic number that is out of range
        cannot drift apart between a reader and a writer.
    */
    std::vector<int32_t> speciesIndices;

    /// One entry per multi-component vector of this orbit.
    std::vector<ClusterVectorElementPlan> elements;
};

/**
@brief Builds the pattern code of one cluster, one site at a time.
@details
    Counting loops differ in how they find the sites of a cluster but not in
    what they do with the species they find there, which is this. Sites are
    added in the order of the positions of the cluster, so the encoder walks
    the rows of the species index table rather than indexing into them.

    An occupation that no species index is defined for, whether because the
    species is not allowed at that position or because the atomic number
    lies outside the range the table covers, yields -1. Rather than test for
    that per site, the encoder collects the sign bit of every species index
    it has seen, so that one test per cluster tells whether any of them was
    unallowed. The pattern code of such a cluster is meaningless, and its
    caller is expected to throw instead of counting it.
*/
class PatternEncoder
{
public:
    explicit PatternEncoder(const OrbitEvaluationPlan &plan)
        : _speciesIndices(plan.speciesIndices.data()),
          _row(plan.speciesIndices.data()),
          _rowLength((size_t)(plan.atomicNumberCount + 1)),
          _lowestAtomicNumber(plan.lowestAtomicNumber),
          _atomicNumberCount((uint32_t)plan.atomicNumberCount),
          _speciesIndexBits(plan.speciesIndexBits)
    {
    }

    /// Starts the cluster over at its first position.
    void begin()
    {
        _pattern = 0;
        _unallowedSpeciesIndices = 0;
        _row = _speciesIndices;
    }

    /// Adds the next position of the cluster, occupied by the given atomic number.
    void add(const int atomicNumber)
    {
        const uint32_t offset = (uint32_t)(atomicNumber - _lowestAtomicNumber);
        const int32_t speciesIndex = _row[offset < _atomicNumberCount ? offset : _atomicNumberCount];
        _row += _rowLength;
        _unallowedSpeciesIndices |= speciesIndex;
        _pattern = (_pattern << _speciesIndexBits) | (uint64_t)(uint32_t)speciesIndex;
    }

    /// Whether any position added since begin() carries a species that is not allowed on it.
    bool anyUnallowed() const { return _unallowedSpeciesIndices < 0; }

    /// The pattern code of the cluster.
    int64_t pattern() const { return (int64_t)_pattern; }

private:
    /// First row of the species index table of the orbit.
    const int32_t *_speciesIndices;

    /// Row of the position that add() will take next.
    const int32_t *_row;

    /// Number of entries per row of the species index table.
    size_t _rowLength;

    /// Lowest atomic number the species index table covers.
    int _lowestAtomicNumber;

    /// Number of atomic numbers the table covers, and the offset of its out-of-range entry.
    uint32_t _atomicNumberCount;

    /// Width in bits of the field one position occupies in the pattern code.
    int _speciesIndexBits;

    /// The pattern code built so far.
    uint64_t _pattern = 0;

    /// The species indices seen so far, combined so that the sign bit marks any unallowed one.
    int32_t _unallowedSpeciesIndices = 0;
};

/**
@brief Builds the evaluation plans of all orbits of the given orbit list.
@param primitiveOrbitList the primitive orbit list of the cluster space
@param speciesMaps for each site of the primitive structure, the map from atomic number to species index
*/
std::vector<OrbitEvaluationPlan> buildOrbitEvaluationPlans(
    const OrbitList &primitiveOrbitList,
    const std::vector<std::unordered_map<int, int>> &speciesMaps);

/**
@brief Reports an occupation that no species index is defined for.
@details
    Separate from the counting loops, and never inlined into them, so that
    the loops carry only the test and not the machinery of building the
    message.
@param plan evaluation plan of the orbit being counted
@param caller name of the calling function, used in the error message
*/
[[noreturn]] void throwUnallowedOccupation(const OrbitEvaluationPlan &plan,
                                           const char *caller);

/**
@brief Returns the cluster function of one counted pattern under one site permutation.
@details
    This is Pi_alpha of Sect. II of AngMunRah19 for a single cluster, the
    product over the positions of the cluster of the point function that
    alpha selects for each of them. Both factors of that product are
    already worked out: which point function applies is folded into the
    tabulation, and which species occupies the position is the digit the
    pattern code holds for it.
@param element plan of the cluster vector element being evaluated
@param plan evaluation plan of the orbit
@param sitePermutation index of the site permutation
@param pattern encoded occupation pattern of the cluster
*/
inline double clusterFunctionOfPattern(const ClusterVectorElementPlan &element,
                                       const OrbitEvaluationPlan &plan,
                                       const size_t sitePermutation,
                                       const int64_t pattern)
{
    const double *values = element.pointFunctionValues.data() +
                           sitePermutation * (size_t)plan.order * plan.speciesStride;
    const int64_t digitMask = ((int64_t)1 << plan.speciesIndexBits) - 1;
    double clusterFunction = 1.0;
    for (int position = 0; position < plan.order; position++)
    {
        const int shift = plan.speciesIndexBits * (plan.order - 1 - position);
        const int64_t speciesIndex = (pattern >> shift) & digitMask;
        clusterFunction *= values[(size_t)position * plan.speciesStride + (size_t)speciesIndex];
    }
    return clusterFunction;
}

/*
The normalization convention this code implements
-------------------------------------------------

A cluster vector element is an average, not a sum. For an orbit beta and a
multi-component vector alpha it is

    Xi_{alpha,beta}(sigma) = < Pi_alpha(sigma) >_beta,

which is Eq. (2) of the tutorial paper (EkbRosFra24), with the cluster
function Pi_alpha as defined in Sect. II of the icet paper (AngMunRah19) and
implemented by clusterFunctionOfPattern above.

The average runs over the clusters of the orbit that lie in one primitive
cell, and over the site permutations that alpha is counted under. The
function below forms it in three steps.

  * The sum over the counted clusters and their permutations. Counting has
    already coalesced clusters that carry the same occupation pattern, so
    the sum runs over patterns, each weighted by how many clusters carried
    it. Whole clusters count as one; a cluster that contains the same site
    more than once through a periodic image counts, in a local or change
    evaluation, as 1 / n per occurrence, which is where non-integer weights
    come from.

  * Division by the multiplicity, which is the number of site permutations
    of alpha times the number of clusters of the orbit in the primitive
    orbit list. This is what makes the result an average rather than a sum.
    It is a precomputed number rather than the number of clusters actually
    counted, because local and change evaluations count only the clusters
    that touch one site and must still be normalized against the whole
    orbit.

  * Multiplication by the ratio of the primitive cell size to the supercell
    size, which reduces the sum over the whole supercell to one primitive
    cell.

Two consequences are worth stating, because the two papers differ in where
they absorb the multiplicity m_beta.

  * Elements lie in [-1, 1]. Each point function does, so each cluster
    function does, and an average of numbers in [-1, 1] does. Nothing here
    scales an element by how many clusters an orbit has.

  * Multiplicities are therefore not carried in the cluster vector. They
    belong to the sensing matrix and to the effective cluster interactions
    that multiply these elements, and icet applies them there.

The zerolet, the leading element, is not produced here; it is fixed by which
kind of cluster vector is being assembled and is set in
ClusterSpace::assembleClusterVector.
That function also applies the one convention that distinguishes a local
cluster vector beyond its zerolet: each element of a local cluster vector is
further divided by the order of its orbit, so that the local cluster vectors
sum to the full cluster vector over the sites of the supercell.
*/

/**
@brief Returns one cluster vector element: the average of the cluster function over an orbit.
@details See the comment block above for the normalization convention.
@param element plan of the cluster vector element being evaluated
@param plan evaluation plan of the orbit
@param counts the counted occupation patterns of the orbit, after ClusterCountBuffer::finish
@param primitiveStructureSize number of sites in the primitive structure
@param supercellSize number of sites in the supercell the counts refer to
*/
inline double averageClusterFunctionOverOrbit(const ClusterVectorElementPlan &element,
                                              const OrbitEvaluationPlan &plan,
                                              const ClusterCountBuffer &counts,
                                              const size_t primitiveStructureSize,
                                              const size_t supercellSize)
{
    double sumOverOrbit = 0.0;
    for (size_t entry = 0; entry < counts.size(); entry++)
    {
        const int64_t pattern = counts.pattern(entry);
        const double weight = counts.weight(entry);
        for (size_t permutation = 0; permutation < element.numberOfSitePermutations; permutation++)
        {
            sumOverOrbit += weight * clusterFunctionOfPattern(element, plan, permutation, pattern);
        }
    }
    return sumOverOrbit / (double)element.multiplicity *
           (double)primitiveStructureSize / (double)supercellSize;
}
