"""
Contains the Orbit class which hold onformation about equivalent clusters.
"""
import numpy as np
import tarfile
import pickle

from .utilities import BiMap
from .atoms import Atom
from ..input_output.logging_tools import logger
from ..input_output.read_write_files import add_items_to_tarfile_pickle, read_items_pickle


logger = logger.getChild('orbits')


# This is the interface accessible for cluster_space
def get_orbits(cluster_list, atom_list, rotation_matrices, translation_vectors,
               permutations, prim, symprec):
    """Generate a list of the orbits for the clusters in a supercell
    configuration.

    This method requires as input a list of the clusters in a supercell
    configuration as well as a set of symmetry operations (rotations and
    translations). From this information it will generate a list of the orbits,
    i.e. the set of symmetry inequivalent clusters each associated with its
    respective set of equivalent clusters.

    Parameters
    ----------
    cluster_list : BiMap object
        a list of clusters
    atom_list : BiMap object
        a list of atoms in a supercell
    rotation_matrices : list of NumPy (3,3) arrays
        rotational symmetries to be imposed (e.g., from spglib)
    translation_vectors : list of NumPy (3) arrays
        translational symmetries to be imposed (e.g., from spglib)
    permutations : list of permutations
        lookup table for permutations
    prim : hiPhive Atoms object
        primitive structure

    Returns
    -------
    list of Orbits objs
        orbits associated with the list of input clusters

    """

    logger.debug('Preparing input...')
    atoms = prepare_atoms(atom_list)
    clusters = prepare_clusters(cluster_list)
    rotations = prepare_rotations(rotation_matrices)
    translations = prepare_translations(translation_vectors)
    permutations = prepare_permutations(permutations)
    cell = prim.cell
    basis = prim.basis

    logger.debug('Creating permutation map...')
    permutation_map, extended_atoms = \
        get_permutation_map(atoms, rotations, translations, basis, symprec)

    logger.debug('Creating orbits...')
    orbits = _get_orbits(permutation_map, extended_atoms, clusters, basis,
                         cell, rotations, permutations)

    return orbits


# All prepares are in case we changes some interface stuff
def prepare_permutations(permutations):
    perms = BiMap()
    for p in permutations:
        perms.append(tuple(p))
    return perms


def prepare_atoms(atom_list):
    atoms = BiMap()
    for atom in atom_list:
        atoms.append(atom)
    return atoms


def prepare_clusters(cluster_list):
    clusters = BiMap()
    for cluster in cluster_list:
        clusters.append(tuple(cluster))
    return clusters


def prepare_rotations(rotation_matrices):
    return rotation_matrices


def prepare_translations(translation_vectors):
    return translation_vectors


def get_permutation_map(atoms, rotations, translations, basis, symprec):

    extended_atoms = atoms.copy()

    permutation_map = np.zeros((len(atoms), len(rotations)), dtype=int)

    scaled_positions = [atom.spos(basis) for atom in extended_atoms]

    for sym_index, (R, T) in enumerate(zip(rotations, translations)):
        for atom_index, spos in enumerate(scaled_positions):

            new_spos = np.dot(R, spos) + T
            new_atom = Atom.spos_to_atom(new_spos, basis, symprec)

            if new_atom not in extended_atoms:
                extended_atoms.append(new_atom)

            mapped_atom_index = extended_atoms.index(new_atom)
            permutation_map[atom_index, sym_index] = mapped_atom_index

    return permutation_map, extended_atoms


# The internal function doing the outer loop over orbits
def _get_orbits(permutation_map, extended_atoms, clusters,
                basis, cell,
                rotations, permutations):
    cluster_is_found = [False] * len(clusters)
    orbits = []
    for cluster_index, cluster in enumerate(clusters):
        if cluster_is_found[cluster_index]:
            continue

        orbit = Orbit()

        cluster_atoms = [extended_atoms[i] for i in cluster]

        positions = [atom.pos(basis, cell) for atom in cluster_atoms]
        orbit.radius = get_geometrical_radius(positions)
        orbit.maximum_distance = get_maximum_distance(positions)
        orbit.order = len(cluster)

        populate_orbit(orbit, permutations, clusters,
                       cluster,
                       permutation_map, extended_atoms,
                       cluster_is_found)
        orbits.append(orbit)

#            bar.tick()
    return orbits


# Takes a cluster and generates all equivalent, translated clusters
def generate_translated_clusters(cluster, extended_atoms):
    transformed_cluster_atoms = [extended_atoms[i] for i in cluster]
    tested_offsets = set()
    for atom in transformed_cluster_atoms:
        offset = atom.offset
        if offset in tested_offsets:
            continue
        else:
            tested_offsets.add(offset)
        translated_cluster = []
        for atom in transformed_cluster_atoms:
            new_offset = np.subtract(atom.offset, offset)
            new_atom = Atom(atom.site, new_offset)
            translated_cluster.append(extended_atoms.index(new_atom))
        yield tuple(translated_cluster)


# Here is the actual categorization
def populate_orbit(orbit, permutations, clusters,
                   cluster,
                   permutation_map, extended_atoms,
                   cluster_is_found):
    for sym_index in range(permutation_map.shape[1]):

        of = OrientationFamily(sym_index)

        transformed_cluster = permutation_map[cluster, sym_index]

        for translated_cluster in generate_translated_clusters(
                transformed_cluster, extended_atoms):

            argsort = tuple(np.argsort(translated_cluster))
            perm_index = permutations.index(argsort)

            translated_cluster = tuple(sorted(translated_cluster))
            translated_cluster_index = clusters.index(translated_cluster)

            if cluster == translated_cluster:
                if (sym_index, perm_index) not in orbit.eigensymmetries:
                    orbit.eigensymmetries.append((sym_index, perm_index))

            if not cluster_is_found[translated_cluster_index]:
                cluster_is_found[translated_cluster_index] = True
                of.cluster_indices.append(translated_cluster_index)
                of.permutation_indices.append(perm_index)

        if len(of.cluster_indices) > 0:
            orbit.orientation_families.append(of)

    return orbit


class Orbit:
    """
    This class serves as a container for storing data pertaining to an orbit.

    Attributes
    ----------
    orientation_families : list of OrientationFamily objs
        orientation families of the orbit
    eigensymmetries : list of tuples
        each eigensymmetry corresponds to a pair where the first index
        is the symmetry and the second is the permutation
    eigentensors : list(numpy.ndarray)
        decomposition of the force constant into symmetry elements
    """

    # TODO: Make properties of the parameters
    def __init__(self):
        self.orientation_families = []
        self.eigensymmetries = []
        self.eigentensors = []
        self.radius = None
        self.order = None
        self.maximum_distance = None

    @property
    def prototype_index(self):
        """int : index of cluster that serves as prototype for this orbit

        In the code the first symmetry is always the identity so the first
        orientation family should always correspond to the prototype"""
        return self.orientation_families[0].cluster_indices[0]

    def write(self, f):
        """Write a Orbit instance to a file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """
        tar_file = tarfile.open(mode='w', fileobj=f)

        # add all available attributes
        add_items_to_tarfile_pickle(tar_file, self.__dict__, 'attributes')

    @staticmethod
    def read(f):
        """Load a ClusterSpace from file

        Parameters
        ----------
        f : string or file object
            name of input file (string) or stream to load from (file object)
        """

        orb = Orbit()
        tar_file = tarfile.open(mode='r', fileobj=f)

        # read attributes pickle
        attributes = read_items_pickle(tar_file, 'attributes')
        for name, value in attributes.items():
            orb.__setattr__(name, value)
        return orb


class OrientationFamily:
    """A container for storing information for a "family of orientations".

    An orbit contains many clusters. Some of the clusters can be tranlsated
    onto each other and other must first be rotated. A set of clusters in the
    orbit which can all be translated onto each other are oriented in the same
    way and belongs to the same orientation family. The family is haracterized
    by the symmetry (rotation) which relates it to the prototype structure of
    the orbit.

    Since the clusters are generally stored sorted the permutation information
    must also be stored.

    Parameters
    ----------
    symmetry_index : int
        The index of the symmetry corresponding to spglibs symmetry

    Attributes
    ----------
    symmetry_index : int
        The index of the symmetry corresponding to spglibs symmetry
    cluster_indices : list of ints
        The indices of the clusters belonging to this family
    permutation_indices : list of ints
        The indices of the permutation vector
    """

    def __init__(self, symmetry_index=None):
        self.symmetry_index = symmetry_index
        self.cluster_indices = []
        self.permutation_indices = []

    def write(self, f):
        """ Write the object to file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """
        pickle.dump(self, f)

    @staticmethod
    def read(f):
        """Load a OrientationFamily object from a pickle file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)

        Returns
        -------
        OrientationFamily object
        """
        return pickle.load(f)


def get_geometrical_radius(positions):
    """Compute the geometrical size of a 3-dimensional point cloud. The
    geometrical size is defined as the average distance to the geometric
    center.

    Parameters
    ----------
    positions : list of 3-dimensional vectors
        positions of points in cloud

    Returns
    -------
    float
        geometric size of point cloud
    """
    geometric_center = np.mean(positions, axis=0)
    return np.mean(np.sqrt(np.sum((positions - geometric_center)**2, axis=1)))


def get_maximum_distance(positions):
    """Compute the maximum distance between any two points in a 3-dimensional
    point cloud. This is equivalent to the "size" criterion used when imposing
    a certain (pair) cutoff criterion during construction of a set of clusters.

    Parameters
    ----------
    positions : list of 3-dimensional vectors
        positions of points in cloud

    Returns
    -------
    float
        maximum distance betwee any two points
    """
    if len(positions) == 0:
        return 0.0
    max_distance = 0.0
    for pt1 in positions[:-1]:
        for pt2 in positions[1:]:
            max_distance = max(max_distance, np.linalg.norm(pt1 - pt2))
    return max_distance
