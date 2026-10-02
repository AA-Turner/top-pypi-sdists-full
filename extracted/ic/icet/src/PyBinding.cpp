#include <iostream>
#include <sstream>
/* Ignore warnings we can't do much about */
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmaybe-uninitialized"
#include <pybind11/eigen.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <Eigen/Dense>
#pragma GCC diagnostic pop

#include "Cluster.hpp"
#include "ClusterExpansionCalculator.hpp"
#include "ClusterSpace.hpp"
#include "LatticeSite.hpp"
#include "LocalOrbitListGenerator.hpp"
#include "Orbit.hpp"
#include "OrbitList.hpp"
#include "Structure.hpp"
#include "Symmetry.hpp"

namespace py = pybind11;

namespace
{
/**
@brief Converts a Python object holding atomic numbers, either an array-like
    object or a plain sequence such as a list, into a contiguous
    std::vector<int>.
@details
    Rejects a non-integer dtype, whether the caller passed a numpy array
    directly or a plain sequence that numpy would infer one from (a list of
    floats, for instance), so that every entry point accepting atomic
    numbers applies the same rule on what counts as a valid input.
    py::array::ensure builds a numpy array from an arbitrary sequence with
    its natural dtype, which is what makes the same dtype check apply
    uniformly to both an array and a sequence input; it clears the Python
    error and returns a null array on failure instead of throwing, which is
    turned into a clear TypeError below rather than left to fault on the
    null array's methods.
    Requests a C-contiguous array explicitly (py::array::c_style) rather than
    relying on py::array_t<int>'s default forcecast alone, which accepts a
    non-contiguous array unchanged; reading such an array through a raw
    pointer, as the conversion below does, would then silently walk the
    wrong elements.
*/
std::vector<int> atomicNumbersFromPyArray(const py::object &occupations)
{
    py::array array = py::array::ensure(occupations);
    if (!array)
    {
        throw py::type_error("atomic numbers must be convertible to an array of integers");
    }
    const char kind = array.dtype().kind();
    if (kind != 'i' && kind != 'u')
    {
        throw py::type_error("atomic numbers must have an integer dtype");
    }
    py::array_t<int, py::array::c_style | py::array::forcecast> contiguous(array);
    return std::vector<int>(contiguous.data(), contiguous.data() + contiguous.size());
}

/**
@brief Builds the internal C++ Structure from the plain arrays that describe
    a structure on the Python side.
@details
    The C++ Structure class is not bound; structures cross the language
    boundary as positions, atomic numbers, cell metric, and periodic
    boundary conditions, and every binding that needs a structure builds one
    through this function.
*/
Structure structureFromPyArrays(const Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &positions,
                                const py::object &atomicNumbers,
                                const Eigen::Matrix3d &cell,
                                const std::vector<bool> &pbc)
{
    return Structure(positions, atomicNumbersFromPyArray(atomicNumbers), cell, pbc);
}
} // namespace

PYBIND11_MODULE(_icet, m)
{

    m.doc() = R"pbdoc(
        This is the compiled core of icet, generated via pybind11 from the C++
        classes and methods that carry out the heavy lifting.

        The classes exposed here are an implementation detail and are not
        intended to be used directly. The public interface of the package
        lives in the icet and mchammer modules, which wrap these classes.
    )pbdoc";

    m.def(
        "find_lattice_sites_by_positions",
        [](const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
           const Eigen::Matrix3d &cell,
           const std::vector<bool> &pbc,
           const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &queryPositions,
           const double fractionalPositionTolerance)
        {
            // The lookup depends only on the geometry, so the structure is
            // built with placeholder atomic numbers.
            Structure structure(positions, std::vector<int>(positions.rows(), 0), cell, pbc);
            std::vector<LatticeSite> latticeSites;
            latticeSites.reserve(queryPositions.rows());
            for (int row = 0; row < queryPositions.rows(); row++)
            {
                latticeSites.push_back(structure.findLatticeSiteByPosition(
                    queryPositions.row(row), fractionalPositionTolerance));
            }
            return latticeSites;
        },
        R"pbdoc(
        Returns the lattice sites of a structure that match the given
        positions. Each lattice site pairs the index of a site of the
        structure with the offset of the unit cell in which the matched
        position sits.

        Parameters
        ----------
        positions : np.ndarray
            positions of the sites of the structure in Cartesian coordinates
        cell : np.ndarray
            cell metric of the structure
        pbc : list[bool]
            periodic boundary conditions of the structure
        query_positions : np.ndarray
            positions to match, in Cartesian coordinates
        fractional_position_tolerance : float
            tolerance applied when comparing positions in fractional coordinates

        Returns
        -------
        list[LatticeSite]
            one lattice site per query position
        )pbdoc",
        py::arg("positions"),
        py::arg("cell"),
        py::arg("pbc"),
        py::arg("query_positions"),
        py::arg("fractional_position_tolerance"));

    py::class_<Cluster>(m, "Cluster",
                        R"pbdoc(
        This class handles a cluster, i.e., a group of lattice sites.

        Parameters
        ----------
        lattice_sites : list[LatticeSite]
            the lattice sites that form the cluster
        positions : np.ndarray
            positions of the sites of the structure that the lattice sites
            refer to, in Cartesian coordinates
        cell : np.ndarray
            cell metric of that structure
        pbc : list[bool]
            periodic boundary conditions of that structure
        allowed_atomic_numbers : list[list[int]]
            atomic numbers allowed on each site of that structure; needed
            only when an Orbit is to be constructed from the cluster, which
            reads them to set up its multi-component vectors
        )pbdoc")
        .def(py::init(
                 [](const std::vector<LatticeSite> &latticeSites,
                    const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
                    const Eigen::Matrix3d &cell,
                    const std::vector<bool> &pbc,
                    const std::vector<std::vector<int>> &allowedAtomicNumbers)
                 {
                     // The cluster itself reads only the geometry of its
                     // structure, so it is built with placeholder atomic
                     // numbers; the allowed atomic numbers are carried for
                     // the Orbit constructor.
                     Structure structure(positions, std::vector<int>(positions.rows(), 0), cell, pbc);
                     if (!allowedAtomicNumbers.empty())
                     {
                         structure.setAllowedAtomicNumbers(allowedAtomicNumbers);
                     }
                     return Cluster(latticeSites, std::make_shared<const Structure>(std::move(structure)));
                 }),
             "Initializes a cluster instance.",
             py::arg("lattice_sites"),
             py::arg("positions"),
             py::arg("cell"),
             py::arg("pbc"),
             py::arg("allowed_atomic_numbers") = std::vector<std::vector<int>>{})
        .def_property_readonly(
            "lattice_sites",
            &Cluster::latticeSites,
            "list[LatticeSite] : the lattice sites that constitute the cluster")
        .def_property_readonly(
            "radius",
            &Cluster::radius,
            "float : the radius of the cluster")
        .def_property_readonly(
            "distances",
            &Cluster::distances,
            "list[float] : the distances between the points in the cluster")
        .def_property_readonly(
            "order",
            &Cluster::order,
            "int : order of the cluster (= number of sites)")
        .def_property_readonly(
            "positions",
            &Cluster::getPositions,
            "list[np.ndarray] : positions of sites in the cluster in Cartesian coordinates")
        .def("__len__",
             &Cluster::order);

    py::class_<LatticeSite>(m, "LatticeSite",
                            R"pbdoc(
        This class handles a lattice site, which is identified by the index of
        a site in a structure together with the offset of the unit cell in
        which it sits.

        Parameters
        ----------
        site_index : int
            index of the site in the structure
        unitcell_offset : list[int]
            offset of the site relative to the unit cell at the origin, in
            units of the cell vectors
        )pbdoc")
        .def(py::init<const int,
                      const Vector3i &>(),
             "Initializes a LatticeSite object.",
             py::arg("site_index"),
             py::arg("unitcell_offset"))
        .def_property_readonly(
            "index",
            &LatticeSite::index,
            "int : site index")
        .def_property_readonly(
            "unitcell_offset",
            &LatticeSite::unitcellOffset,
            "np.ndarray : unit cell offset (in units of the cell vectors)")
        .def(py::self < py::self)
        .def(py::self == py::self)
        .def(py::self + Eigen::Vector3i())
        .def("__hash__", [](const LatticeSite &latticeNeighbor)
             { return std::hash<LatticeSite>{}(latticeNeighbor); });

    py::class_<Orbit>(m, "Orbit",
                      R"pbdoc(
        This class handles an orbit. An orbit consists of one or
        more clusters that are equivalent by the symmetries of the
        underlying structure. One of these clusters (the first in
        the list of clusters handed to the constructor) will be
        treated as the "representative cluster". All clusters
        need to have sites that are permuted in a manner consistent
        with the representative cluster. This is the responsibility
        of the user when constructing an orbit. Normally, however,
        orbits are constructed internally, in which case
        the user does not need to think about this permutation.

        Parameters
        ----------
        clusters : list[Cluster]
            The clusters that make up this orbit.
        allowed_permutations : list[list[int]]
            A list of the permutations allowed for this orbit.
            For example, if ``[0, 2, 1]`` is in this list, the
            multi-component vector ``[0, 1, 0]`` is the same as
            ``[0, 0, 1]``.
        )pbdoc")
        .def(py::init<const std::vector<Cluster> &,
                      const std::set<std::vector<int>> &>())
        .def_property_readonly(
            "representative_cluster",
            &Orbit::representativeCluster,
            "Cluster to which all other symmetry equivalent clusters can be related.")
        .def_property_readonly(
            "order",
            &Orbit::order,
            "Number of sites in the representative cluster.")
        .def_property_readonly(
            "radius",
            &Orbit::radius,
            "Radius of the representative cluster.")
        .def_property_readonly(
            "allowed_permutations",
            [](const Orbit &orbit)
            {
                // Convert from set to vector before return
                std::set<std::vector<int>> allowedPermutations = orbit.getAllowedClusterPermutations();
                std::vector<std::vector<int>> retPermutations(allowedPermutations.begin(), allowedPermutations.end());
                return retPermutations;
            },
            R"pbdoc(
             List of equivalent permutations for this orbit. If this
             orbit is a triplet and the permutation ``[0, 2, 1]`` exists this means
             that the lattice sites ``[s1, s2, s3]`` are equivalent to ``[s1, s3,
             s2]``. This will have the effect that for a ternary cluster expansion the
             multi-component vector ``(0, 1, 0)`` will not be considered separately
             since it is equivalent to ``(0, 0, 1)``.
             )pbdoc")
        .def_property_readonly(
            "clusters",
            &Orbit::clusters,
            "List of the clusters in this orbit.")
        .def_property_readonly(
            "cluster_vector_elements",
            [](const Orbit &orbit)
            {
                std::vector<py::dict> clusterVectorElements;
                for (const auto &cvElement : orbit.clusterVectorElements())
                {
                    py::dict cvElementPy;
                    cvElementPy["multicomponent_vector"] = cvElement.multiComponentVector;
                    cvElementPy["site_permutations"] = cvElement.sitePermutations;
                    cvElementPy["multiplicity"] = cvElement.multiplicity;
                    clusterVectorElements.push_back(cvElementPy);
                }
                return clusterVectorElements;
            },
            R"pbdoc(
             list[dict] : the cluster vector elements to which this orbit
             contributes.

             Each element is a dictionary with the keys
             ``multicomponent_vector``, ``site_permutations``, and
             ``multiplicity``. In a binary system there is exactly one such
             element per orbit, whereas in ternary and higher-order systems
             there are generally several, one per distinct multi-component
             vector.
             )pbdoc")
        .def(
            "get_cluster_counts",
            [](const Orbit &orbit,
               const py::object &occupations,
               const int siteIndexForDoubleCountingCorrection)
            {
                std::vector<int> atomicNumbers = atomicNumbersFromPyArray(occupations);
                // OccupationSpan does not bounds-check, unlike the
                // std::vector<int>::at it replaced here, so an occupation
                // vector smaller than what this orbit's clusters were built
                // against needs to be rejected explicitly, before it can be
                // read out of bounds.
                for (const auto &cluster : orbit.clusters())
                {
                    for (const auto &site : cluster.latticeSites())
                    {
                        if (site.index() >= atomicNumbers.size())
                        {
                            std::ostringstream msg;
                            msg << "Lattice site index " << site.index() << " is out of bounds";
                            msg << " for an occupation vector with " << atomicNumbers.size() << " entries";
                            msg << " (Orbit.get_cluster_counts)";
                            throw std::out_of_range(msg.str());
                        }
                    }
                }
                OccupationSpan occupationSpan(atomicNumbers.data(), atomicNumbers.size());
                py::dict clusterCountDict;
                for (const auto &mapPair : orbit.getClusterCounts(occupationSpan,
                                                                  siteIndexForDoubleCountingCorrection))
                {
                    py::list clusterSpecies;
                    for (const auto &el : mapPair.first)
                    {
                        clusterSpecies.append(el);
                    }
                    // Counts are accumulated as doubles, because a cluster
                    // that contains a site more than once contributes a
                    // fraction of one per occurrence. Those fractions always
                    // add up again over the clusters of an orbit, so the
                    // total is expected to be an integer up to rounding.
                    const double integerTolerance = 1e-6;
                    if (std::abs(std::round(mapPair.second) - mapPair.second) > integerTolerance)
                    {
                        throw std::runtime_error("Cluster count is a non-integer.");
                    }
                    int count = (int)std::round(mapPair.second);
                    clusterCountDict[py::tuple(clusterSpecies)] = count;
                }
                return clusterCountDict;
            },
            R"pbdoc(
             Count clusters in this orbit for an occupation vector.

             Parameters
             ----------
             occupations : list[int] | np.ndarray
                Atomic numbers of the structure whose clusters are counted,
                one per site of the structure that the lattice sites of this
                orbit refer to.
             site_index_for_double_counting_correction : int
                Avoid double counting clusters containing this index.
                Default: -1, i.e., no such correction.
             )pbdoc",
            py::arg("occupations"),
            py::arg("site_index_for_double_counting_correction") = -1)
        .def(
            "translated",
            [](const Orbit &orbit, const Eigen::Vector3i &offset)
            {
                Orbit translated = orbit;
                translated.translate(offset);
                return translated;
            },
            py::arg("offset"),
            R"pbdoc(
             Returns a copy of this orbit whose clusters have been translated
             by a constant offset. This orbit is left as it is.

             Parameters
             ----------
             offset : list[int]
                Offset in multiples of the cell vectors of
                the structure used to define the clusters in this orbit
                (typically the primitive structure).
             )pbdoc")
        .def("__len__", &Orbit::size);

    py::class_<OrbitList, std::shared_ptr<OrbitList>>(m, "_OrbitList",
                                                      R"pbdoc(
        This class manages an orbit list. The orbit list is constructed for
        the structure described by the given arrays using the matrix of
        equivalent sites and a list of neighbor lists.

        Parameters
        ----------
        positions : np.ndarray
            positions of the sites of the (primitive) structure in Cartesian
            coordinates
        atomic_numbers : list[int] | np.ndarray
            atomic numbers of the species on each site
        allowed_atomic_numbers : list[list[int]]
            atomic numbers allowed on each site
        cell : np.ndarray
            cell metric
        pbc : list[bool]
            periodic boundary conditions
        matrix_of_equivalent_sites : list[list[LatticeSite]]
            matrix of symmetry equivalent sites
        neighbor_lists : list[list[list[LatticeSite]]]
            neighbor lists for each (cluster) order
        position_tolerance
            tolerance applied when comparing positions in Cartesian coordinates
        )pbdoc")
        .def(py::init(
                 [](const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
                    const py::object &atomicNumbers,
                    const std::vector<std::vector<int>> &allowedAtomicNumbers,
                    const Eigen::Matrix3d &cell,
                    const std::vector<bool> &pbc,
                    const std::vector<std::vector<LatticeSite>> &matrixOfEquivalentSites,
                    const std::vector<std::vector<std::vector<LatticeSite>>> &neighborLists,
                    const double positionTolerance)
                 {
                     Structure structure = structureFromPyArrays(positions, atomicNumbers, cell, pbc);
                     structure.setAllowedAtomicNumbers(allowedAtomicNumbers);
                     return OrbitList(structure, matrixOfEquivalentSites, neighborLists, positionTolerance);
                 }),
             "Constructs an orbit list from a matrix of equivalent sites.",
             py::arg("positions"),
             py::arg("atomic_numbers"),
             py::arg("allowed_atomic_numbers"),
             py::arg("cell"),
             py::arg("pbc"),
             py::arg("matrix_of_equivalent_sites"),
             py::arg("neighbor_lists"),
             py::arg("position_tolerance"))
        .def_property_readonly(
            "orbits",
            &OrbitList::orbits,
            "list[Orbit] : the orbits of this orbit list")
        .def("get_orbit",
             &OrbitList::getOrbit,
             R"pbdoc(
             Returns the orbit at the given position in the orbit list.

             Parameters
             ----------
             index : int
                 index of the orbit

             Returns
             -------
             Orbit
                 the orbit at the given index
             )pbdoc",
             py::arg("index"))
        .def("without_inactive_orbits",
             &OrbitList::withoutInactiveOrbits,
             R"pbdoc(
             Returns a new orbit list from which the orbits with inactive
             sites, i.e., sites on which only one species is allowed, have
             been left out. This orbit list is not modified.

             Returns
             -------
             _OrbitList
                 the new orbit list
             )pbdoc")
        .def("without_orbits",
             &OrbitList::withoutOrbits,
             R"pbdoc(
             Returns a new orbit list from which the orbits with the given
             indices have been left out. This orbit list is not modified.

             Parameters
             ---------
             indices : list[int]
                 indices of the orbits to leave out, in any order

             Returns
             -------
             _OrbitList
                 the new orbit list
             )pbdoc",
             py::arg("indices"))
        .def("with_merged_orbits",
             &OrbitList::withMergedOrbits,
             R"pbdoc(
             Returns a new orbit list in which each group of orbits has been
             merged into its first member, and in which the merged-away orbits
             have been left out. This orbit list is not modified.

             The removal of the merged-away orbits is part of this operation.
             An orbit list in which orbits had been merged but not removed
             would still match the length of any orbit list derived from this
             one while no longer corresponding to it orbit by orbit, which is
             an inconsistency that no length check could detect.

             Parameters
             ---------
             groups : dict[int, list[int]]
                 maps the index of an orbit to the indices of the orbits that
                 are to be merged into it; all indices refer to this orbit list

             Returns
             -------
             _OrbitList
                 the new orbit list
             )pbdoc",
             py::arg("groups"))
        .def("_get_sites_translated_to_unitcell",
             &OrbitList::getSitesTranslatedToUnitcell,
             R"pbdoc(
             Returns a set of sites where at least one site is translated inside the unit cell.

             Parameters
             ----------
             lattice_neighbors : list[LatticeSite]
                set of lattice sites that might be representative for a cluster
             sort : bool
                If true sort translated sites.
             )pbdoc",
             py::arg("lattice_neighbors"),
             py::arg("sort"))
        .def("_get_symmetry_related_site_groups",
             &OrbitList::getSymmetryRelatedSiteGroups,
             R"pbdoc(
             Extracts groups of sites that are symmetrically equivalent to the input
             sites.

             Parameters
             ----------
             sites : list[LatticeSite]
                 sites that correspond to the columns that will be returned
             )pbdoc",
             py::arg("sites"))
        .def(
            "_get_structure_data",
            [](const OrbitList &orbitList)
            {
                const Structure &structure = orbitList.structure();
                const std::vector<int> &atomicNumbers = structure.getAtomicNumbers();
                py::dict data;
                data["positions"] = structure.getPositions();
                data["atomic_numbers"] = py::array(atomicNumbers.size(), atomicNumbers.data());
                data["cell"] = structure.getCell();
                data["pbc"] = structure.getPBC();
                return data;
            },
            R"pbdoc(
             Returns the positions, atomic numbers, cell metric, and periodic
             boundary conditions of the structure used to construct the orbit
             list, as a dictionary of plain arrays.
             )pbdoc")
        .def("__len__",
             &OrbitList::size,
             "Returns the total number of orbits in the orbit list.")
        .def_property_readonly("matrix_of_equivalent_positions",
                               &OrbitList::getMatrixOfEquivalentSites,
                               py::return_value_policy::copy,
                               "list[list[LatticeSite]] : matrix of symmetry equivalent sites,"
                               " as a copy; writing to it does not change the orbit list");

    py::class_<LocalOrbitListGenerator>(m, "LocalOrbitListGenerator",
                                        R"pbdoc(
        This class handles the generation of local orbit lists, which are used in
        the computation of cluster vectors of supercells of the primitive structure.
        Upon initialization a LocalOrbitListGenerator object is constructed from an
        orbit list and a supercell structure.

        Parameters
        ----------
        orbit_list : _OrbitList
            an orbit list set up from a primitive structure
        positions : np.ndarray
            positions of the sites of the supercell in Cartesian coordinates;
            the supercell must be built up from the same primitive structure
            used to set up the input orbit list
        atomic_numbers : list[int] | np.ndarray
            atomic numbers of the species on each site of the supercell
        cell : np.ndarray
            cell metric of the supercell
        pbc : list[bool]
            periodic boundary conditions of the supercell
        fractional_position_tolerance : float
            tolerance for positions in fractional coordinates
        )pbdoc")
        .def(py::init(
                 [](const OrbitList &orbitList,
                    const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
                    const py::object &atomicNumbers,
                    const Eigen::Matrix3d &cell,
                    const std::vector<bool> &pbc,
                    const double fractionalPositionTolerance)
                 {
                     auto supercell = std::make_shared<Structure>(
                         structureFromPyArrays(positions, atomicNumbers, cell, pbc));
                     return LocalOrbitListGenerator(orbitList, supercell, fractionalPositionTolerance);
                 }),
             "Constructs a LocalOrbitListGenerator object from an orbit list and a supercell.",
             py::arg("orbit_list"),
             py::arg("positions"),
             py::arg("atomic_numbers"),
             py::arg("cell"),
             py::arg("pbc"),
             py::arg("fractional_position_tolerance"))
        .def("generate_local_orbit_list",
             &LocalOrbitListGenerator::getLocalOrbitList,
             R"pbdoc(
             Generates and returns the local orbit list for an offset of
             the primitive structure.

             Parameters
             ----------
             offset : list[int]
                 Offset in terms of primitive cell vectors.
             self_contained : bool
                 If this orbit list will be used on its own to calculate local cluster vectors or
                 differences in cluster vector, this parameter needs to be true (if false, not all
                 clusters involving this offset will be included).
             )pbdoc",
             py::arg("offset"),
             py::arg("self_contained") = false)
        .def("generate_full_orbit_list",
             &LocalOrbitListGenerator::getFullOrbitList,
             R"pbdoc(
             Generates and returns a local orbit list, which orbits included the equivalent sites
             of all local orbit list in the supercell.
             )pbdoc")
        .def("get_number_of_unique_offsets",
             &LocalOrbitListGenerator::getNumberOfUniqueOffsets,
             "Returns the number of unique offsets")
        .def("_get_unique_primcell_offsets",
             &LocalOrbitListGenerator::getUniquePrimitiveCellOffsets,
             "Returns a list with offsets of primitive structure that span to position of atoms in the supercell.");

    // Every member exposed here is reached from icet/core/cluster_space.py.
    py::class_<ClusterSpace>(m, "ClusterSpace",
                             R"pbdoc(
        This class handles a cluster space, i.e., the set of orbits that
        defines the cluster vector of a structure. It provides functionality
        for calculating cluster vectors and for retrieving associated
        information.

        This is the compiled counterpart of :class:`icet.ClusterSpace`, which
        is what should be used instead.

        Parameters
        ----------
        orbit_list : _OrbitList
            orbit list of the primitive structure
        )pbdoc")
        .def(py::init<std::shared_ptr<const OrbitList>>(),
             "Initializes a ClusterSpace instance.",
             py::arg("orbit_list"))
        .def(
            "get_cluster_vector_from_supercell_orbit_list",
            [](const ClusterSpace &clusterSpace,
               const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
               const py::object &atomicNumbers,
               const Eigen::Matrix3d &cell,
               const std::vector<bool> &pbc,
               const double fractionalPositionTolerance)
            {
                Structure structure = structureFromPyArrays(positions, atomicNumbers, cell, pbc);
                auto cv = clusterSpace.getClusterVectorFromSupercellOrbitList(
                    structure, fractionalPositionTolerance);
                return py::array(cv.size(), cv.data());
            },
            R"pbdoc(
             Returns the cluster vector corresponding to the structure
             described by the input arrays, computed by building a full
             supercell orbit list and counting the clusters it stores.
             The first element in the cluster vector will always be one (1) corresponding to
             the zerolet. The remaining elements of the cluster vector represent averages
             over orbits (symmetry equivalent clusters) of increasing order and size.

             This is the reference oracle for the evaluation tables of
             :class:`_ClusterExpansionCalculator`, kept reachable for
             equivalence testing. Cluster vectors are computed through those
             tables in production, by
             :func:`icet.ClusterSpace.get_cluster_vector`.

             Parameters
             ----------
             positions : np.ndarray
                 Positions of the sites of the structure in Cartesian coordinates.
             atomic_numbers : list[int] | np.ndarray
                 Atomic numbers of the species on each site.
             cell : np.ndarray
                 Cell metric.
             pbc : list[bool]
                 Periodic boundary conditions.
             fractional_position_tolerance : float
                 Tolerance applied when comparing positions in fractional coordinates.

             Returns
             -------
             np.ndarray
                 the cluster vector
             )pbdoc",
            py::arg("positions"),
            py::arg("atomic_numbers"),
            py::arg("cell"),
            py::arg("pbc"),
            py::arg("fractional_position_tolerance"))
        .def(
            "_set_orbit_list",
            &ClusterSpace::setPrimitiveOrbitList,
            R"pbdoc(
             Bases this cluster space on the given orbit list, which is how
             pruning and merging take effect: the caller builds the pruned or
             merged orbit list and hands it over here.

             This changes which orbit list this cluster space refers to. It
             cannot change any orbit list, since orbit lists are immutable, so
             no other cluster space and no calculator that shares the previous
             one is affected by it.

             Parameters
             ----------
             orbit_list : _OrbitList
                 the orbit list this cluster space is to be based on
             )pbdoc",
            py::arg("orbit_list"))

        .def_property_readonly(
            "species_maps",
            &ClusterSpace::getSpeciesMaps,
            R"pbdoc(
             list[dict[int, int]] : for each site in the primitive structure,
             the map from atomic number to the internal species enumeration,
             which numbers the species allowed on that site consecutively from
             zero in order of increasing atomic number.
             )pbdoc")
        .def("evaluate_cluster_function",
             &ClusterSpace::evaluateClusterFunction,
             R"pbdoc(
             Evaluates a cluster function (also "orthogonal point function")
             for one site.

             Parameters
             ----------
             number_of_allowed_species : int
                 number of species allowed on the site in question
             cluster_function : int
                 index of the cluster function, counting the first non-trivial
                 function as zero
             species : int
                 index of the species that occupies the site, in the internal
                 enumeration given by :attr:`species_maps`

             Returns
             -------
             float
                 the value of the cluster function
             )pbdoc",
             py::arg("number_of_allowed_species"),
             py::arg("cluster_function"),
             py::arg("species"))
        .def("__len__", &ClusterSpace::size);

    py::class_<ClusterExpansionCalculator>(m, "_ClusterExpansionCalculator",
                                           R"pbdoc(
        This class provides a cluster expansion calculator for a specific
        supercell. Upon initialization various quantities specific to that
        supercell are precomputed, which speeds up subsequent calculations and
        makes Monte Carlo simulations feasible.

        This is the compiled counterpart of
        :class:`mchammer.calculators.ClusterExpansionCalculator`, which is what
        should be used instead.

        The calculator holds the occupations of its supercell, initialized
        from the ``atomic_numbers`` it is constructed with.
        :func:`set_occupations` replaces them, :func:`apply_moves` advances
        them through a list of moves, and the local and change evaluations
        read them.
        A move is an ordered sequence of ``(site index, new atomic number)``
        pairs, so a swap of two sites is a move of length two and a single
        flip is a move of length one.

        The thread contract follows the standard C++ container idiom.
        Const operations, meaning :func:`get_cluster_vector`,
        :func:`get_local_cluster_vector`, and reading :attr:`occupations`,
        may run concurrently on one calculator, as long as no thread
        concurrently calls anything else on it.
        :func:`set_occupations`, :func:`apply_moves`, and
        :func:`get_cluster_vector_changes` require exclusive access to the
        calculator; the last of these applies and reverts the flips of each
        move on the held occupations, restoring them on every exit path, so
        it is state-neutral but not safe to run concurrently with anything.
        Distinct calculators are fully independent even when they share a
        cluster space.

        Parameters
        ----------
        cluster_space : ClusterSpace
            cluster space for which to set up the calculator
        positions : np.ndarray
            positions of the sites of the supercell in Cartesian coordinates
        atomic_numbers : list[int] | np.ndarray
            atomic numbers of the species on each site of the supercell
        cell : np.ndarray
            cell metric of the supercell
        pbc : list[bool]
            periodic boundary conditions of the supercell
        fractional_position_tolerance : float
            tolerance applied when comparing positions in fractional coordinates
        )pbdoc")
        .def(py::init(
                 [](const ClusterSpace &clusterSpace,
                    const Eigen::Matrix<double, Dynamic, 3, Eigen::RowMajor> &positions,
                    const py::object &atomicNumbers,
                    const Eigen::Matrix3d &cell,
                    const std::vector<bool> &pbc,
                    const double fractionalPositionTolerance)
                 {
                     Structure supercell = structureFromPyArrays(positions, atomicNumbers, cell, pbc);
                     return ClusterExpansionCalculator(clusterSpace, supercell, fractionalPositionTolerance);
                 }),
             "Initializes a _ClusterExpansionCalculator instance.",
             py::arg("cluster_space"),
             py::arg("positions"),
             py::arg("atomic_numbers"),
             py::arg("cell"),
             py::arg("pbc"),
             py::arg("fractional_position_tolerance"))
        .def(
            "set_occupations",
            [](ClusterExpansionCalculator &calc, const py::object &occupations)
            {
                calc.setOccupations(atomicNumbersFromPyArray(occupations));
            },
            R"pbdoc(
              Replaces the held occupations of the supercell.

              The occupations are copied at this boundary, so later changes
              to the array passed in do not reach the calculator.

              Parameters
              ----------
              occupations : list[int] | np.ndarray
                  the occupation vector for the supercell
              )pbdoc",
            py::arg("occupations"))
        .def_property_readonly(
            "occupations",
            [](const ClusterExpansionCalculator &calc)
            {
                const std::vector<int> &occupations = calc.getOccupations();
                return py::array(occupations.size(), occupations.data());
            },
            "np.ndarray : the held occupations of the supercell (copy)")
        .def(
            "apply_moves",
            &ClusterExpansionCalculator::applyMoves,
            R"pbdoc(
              Advances the held occupations through the given moves, which is
              how an accepted move takes effect.
              Every flip of every move is validated before the first one is
              applied, including that the new atomic number is allowed on
              its site, so a rejected list of moves leaves the held
              occupations exactly as they were.

              Parameters
              ----------
              moves : list[list[tuple[int, int]]]
                  the moves to apply, in order; each move is an ordered
                  sequence of (site index, new atomic number) pairs
              )pbdoc",
            py::arg("moves"))
        .def(
            "get_cluster_vector_changes",
            [](ClusterExpansionCalculator &calc,
               const std::vector<ClusterExpansionCalculator::Move> &moves)
            {
                std::vector<std::vector<double>> changes = calc.getClusterVectorChanges(moves);
                const size_t rows = changes.size();
                // An empty batch keeps the full number of columns, so the
                // result flows through the same array arithmetic as a
                // non-empty one; a shape of (0, 0) would break a matrix
                // product against the parameter vector.
                const size_t columns = rows == 0 ? calc.clusterVectorLength() : changes[0].size();
                py::array_t<double> result({rows, columns});
                auto access = result.mutable_unchecked<2>();
                for (size_t row = 0; row < rows; row++)
                {
                    for (size_t column = 0; column < columns; column++)
                    {
                        access(row, column) = changes[row][column];
                    }
                }
                return result;
            },
            R"pbdoc(
              Returns one cluster vector change per move, evaluated from the
              held occupations, which are unchanged when this method returns.

              Each move is evaluated independently from the held occupations,
              and within a move the flips are applied sequentially, so the
              change of a two-site move is the change of the first flip plus
              the change of the second flip evaluated with the first one
              applied.

              Parameters
              ----------
              moves : list[list[tuple[int, int]]]
                  the moves to evaluate; each move is an ordered sequence of
                  (site index, new atomic number) pairs

              Returns
              -------
              np.ndarray
                  the changes in the cluster vector, one row per move
              )pbdoc",
            py::arg("moves"))
        .def(
            "get_local_cluster_vector",
            [](const ClusterExpansionCalculator &calc, const int index)
            {
                auto localCv = calc.getLocalClusterVector(index);
                return py::array(localCv.size(), localCv.data());
            },
            R"pbdoc(
              Returns a cluster vector that only considers clusters that
              contain the input index, evaluated from the held occupations.

              Local cluster vectors are an additive decomposition of the
              cluster vector over the sites of the supercell::

                  sum(get_local_cluster_vector(i)
                      for i in range(len(structure)))
                      == get_cluster_vector()

              A cluster of order k is counted once for each of its k sites,
              so it contributes to the local cluster vector of every site it
              contains, and each element is divided by the order of its orbit
              to compensate; the zerolet is 1 / N per site. The additive
              decomposition is what makes local cluster vectors usable as
              site contributions::

                  sum(np.dot(get_local_cluster_vector(i), parameters)
                      for i in range(len(structure))) * len(structure)
                      == calculate_total(occupations)

              Both identities require that no cluster contains the same site
              more than once through periodic images. In a supercell small
              enough for a cluster to reach a periodic image of one of its own
              sites, that cluster enters the local cluster vector of the
              repeated site with a weight of 1 / n rather than n times, where n
              is the number of occurrences, and the sums fall short by the
              difference. Use
              :func:`ClusterSpace.are_local_cluster_vectors_additive` to test
              whether a given supercell satisfies this condition.

              Parameters
              ----------
              index : int
                  index of site whose local cluster vector should be calculated

              Returns
              -------
              np.ndarray
                  the local cluster vector
              )pbdoc",
            py::arg("index"))
        .def(
            "get_cluster_vector",
            [](const ClusterExpansionCalculator &calc,
               const py::object &occupations)
            {
                std::vector<double> cv;
                if (occupations.is_none())
                {
                    cv = calc.getClusterVector();
                }
                else
                {
                    cv = calc.getClusterVector(atomicNumbersFromPyArray(occupations));
                }
                return py::array(cv.size(), cv.data());
            },
            R"pbdoc(
              Returns full cluster vector used in total property calculations.

              Parameters
              ----------
              occupations : list[int] | np.ndarray | None
                  the occupation vector for the supercell; the held
                  occupations are used if ``None`` (default)

              Returns
              -------
              np.ndarray
                  the cluster vector
              )pbdoc",
            py::arg("occupations") = py::none())
        .def_property_readonly(
            "are_local_cluster_vectors_additive",
            &ClusterExpansionCalculator::areLocalClusterVectorsAdditive,
            R"pbdoc(
              bool : whether the local cluster vectors of this supercell sum
              to its cluster vector, which is the precondition for using
              them as an additive decomposition. This is false exactly when
              some cluster contains the same site more than once through
              periodic images. Read off the evaluation tables, where it is
              a byproduct of their construction, so it is essentially free.
              )pbdoc")
        .def_property_readonly(
            "is_self_interacting",
            &ClusterExpansionCalculator::isSelfInteracting,
            R"pbdoc(
              bool : whether any two clusters of this supercell consist of
              the same sites through periodic boundary conditions, in which
              case distinct interaction terms of the model are evaluated on
              the same group of sites and results can be misleading.
              Answered by comparing the local entries of the evaluation
              tables at one anchor cell, which is exact by translation
              covariance, so the amount of work does not depend on the size
              of the supercell.
              )pbdoc");
}
