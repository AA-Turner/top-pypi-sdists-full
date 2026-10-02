#pragma once

#define _USE_MATH_DEFINES
#include <cmath>
#include <functional>

#include "ClusterCountBuffer.hpp"
#include "LocalOrbitListGenerator.hpp"
#include "OccupationSpan.hpp"
#include "OrbitEvaluationPlan.hpp"
#include "OrbitList.hpp"
#include "Structure.hpp"
#include "VectorOperations.hpp"

/**
@brief This class handles the cluster space.
@details It provides functionality for setting up a cluster space, calculating
cluster vectors as well as retrieving various types of associated information.
*/
class ClusterSpace
{
public:
  /// Constructor.
  ClusterSpace(){};
  ClusterSpace(std::shared_ptr<const OrbitList>);

  /// Returns the entire primitive orbit list.
  const OrbitList &getPrimitiveOrbitList() const { return *_primitiveOrbitList; }

  /// Returns the primitive orbit list as a shared pointer.
  std::shared_ptr<const OrbitList> getPrimitiveOrbitListPointer() const { return _primitiveOrbitList; }

  /// Bases this cluster space on the given orbit list.
  void setPrimitiveOrbitList(std::shared_ptr<const OrbitList>);

  /// Returns the primitive structure.
  const Structure &primitiveStructure() const { return _primitiveOrbitList->structure(); }

  /// Returns the cluster space size, i.e. the length of a cluster vector.
  size_t size() const;

  /// Returns the mapping between atomic numbers and the internal species enumeration scheme for each site.
  const std::vector<std::unordered_map<int, int>> &getSpeciesMaps() const { return _speciesMaps; }

  /// Returns the cluster vector of the input structure, computed by building
  /// a full supercell orbit list. This is the reference oracle for the
  /// evaluation tables of ClusterExpansionCalculator, not a production path.
  std::vector<double> getClusterVectorFromSupercellOrbitList(const Structure &, const double) const;

  /// Returns the total cluster vector given the orbit list and an occupation span.
  std::vector<double> getClusterVectorFromOrbitList(const OrbitList &, OccupationSpan, const size_t supercellSize) const;

  /// The counting side of a cluster vector assembly; fills the buffer with
  /// the counts of the orbit with the given index in the primitive orbit list.
  using CountClustersOfOrbitFunction = std::function<void(const size_t, ClusterCountBuffer &)>;

  /// Assembles a full cluster vector from per-orbit cluster counts.
  std::vector<double> assembleFullClusterVector(const CountClustersOfOrbitFunction &, const size_t supercellSize, const size_t maximumDistinctPatterns) const;

  /// Assembles a local cluster vector, the contribution of one site, from per-orbit cluster counts.
  std::vector<double> assembleLocalClusterVector(const CountClustersOfOrbitFunction &, const size_t supercellSize, const size_t maximumDistinctPatterns) const;

  /// Assembles the change in the cluster vector caused by a change in occupation from per-orbit cluster counts.
  std::vector<double> assembleClusterVectorChange(const CountClustersOfOrbitFunction &, const size_t supercellSize, const size_t maximumDistinctPatterns) const;

  /// Returns, per orbit, what its clusters need in order to be counted and evaluated.
  const std::vector<OrbitEvaluationPlan> &orbitEvaluationPlans() const { return _orbitEvaluationPlans; }

  /// Returns the largest number of distinct occupation patterns any orbit of this cluster space can take.
  size_t maximumDistinctPatterns() const { return _maximumDistinctPatterns; }

  /// Returns the default cluster function.
  double evaluateClusterFunction(const int, const int, const int) const;

private:
  /// Returns the map between atomic numbers and the internal species enumeration.
  static std::vector<std::unordered_map<int, int>> buildSpeciesMaps(const OrbitList &);

  /// Counts the occupations of all clusters of one orbit of a supercell orbit list.
  void countClustersOfOrbit(const Orbit &, const OrbitEvaluationPlan &, OccupationSpan, ClusterCountBuffer &) const;

  /// Assembles a cluster vector from per-orbit cluster counts, with the given
  /// zerolet, dividing each element by the order of its orbit when asked to.
  std::vector<double> assembleClusterVector(const CountClustersOfOrbitFunction &, const size_t supercellSize, const size_t maximumDistinctPatterns, const double zerolet, const bool divideElementsByOrder) const;

  /**
  @brief Primitive orbit list based on the structure and the cutoffs.
  @details
      The orbit list is immutable, and it is held through a pointer to const so
      that this remains true for every cluster space that shares it. Pruning
      and merging replace this pointer with one to a newly built orbit list
      rather than changing the one it currently refers to, so a copy of this
      cluster space, such as the one a ClusterExpansionCalculator holds, keeps
      the orbit list it was given.
  */
  std::shared_ptr<const OrbitList> _primitiveOrbitList;

  /// Map between atomic numbers and the internal species enumeration scheme for each site in the primitive structure.
  std::vector<std::unordered_map<int, int>> _speciesMaps;

  /// Per orbit, what its clusters need in order to be counted and evaluated; aligned with the orbit list.
  std::vector<OrbitEvaluationPlan> _orbitEvaluationPlans;

  /// The largest number of distinct occupation patterns any orbit of this cluster space can take.
  size_t _maximumDistinctPatterns = 0;
};
