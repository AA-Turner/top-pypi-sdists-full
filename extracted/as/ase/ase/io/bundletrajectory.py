# fmt: off

"""bundletrajectory - a module for I/O from large MD simulations.

The BundleTrajectory class writes trajectory into a directory with the
following structure, except we now use JSON instead of pickle,
so this text needs updating::

    filename.bundle (dir)
        metadata.json          Data about the file format, and about which
                               data is present.
        frames                 The number of frames (ascii file)
        F0 (dir)               Frame number 0
            smalldata.ulm      Small data structures in a dictionary
                               (pbc, cell, ...)
            numbers.ulm        Atomic numbers
            positions.ulm      Positions
            momenta.ulm        Momenta
            ...
        F1 (dir)

There is a folder for each frame, and the data is in the ASE Ulm format.
"""

import os
import shutil
import sys
import time
from pathlib import Path

import numpy as np

from ase import Atoms
from ase.calculators.singlepoint import (
    PropertyNotImplementedError,
    SinglePointCalculator,
)

# The system json module causes memory leaks!  Use ase's own.
# import json
from ase.io import jsonio
from ase.io.ulm import open as ulmopen
from ase.parallel import barrier, paropen, world


class BundleTrajectory:
    """Reads and writes atoms into a .bundle directory.

    The BundleTrajectory is an alternative way of storing
    trajectories, intended for large-scale molecular dynamics
    simulations, where a single flat file becomes unwieldy.  Instead,
    the data is stored in directory, a 'bundle' (the name bundle is
    inspired from bundles in Mac OS, which are really just directories
    the user is supposed to think of as a single file-like unit).

    Parameters:

    filename:
        The name of the directory.  Preferably ending in .bundle.

    mode (optional):
        The file opening mode.  'r' means open for reading, 'w' for
        writing and 'a' for appending.  Default: 'r'.  If opening in
        write mode, and the filename already exists, the old file is
        renamed to .bak (any old .bak file is deleted), except if the
        existing file is empty.

    atoms (optional):
        The atoms that will be written.  Can only be specified in
        write or append mode.  If not specified, the atoms must be
        given as an argument to the .write() method instead.

    backup=True:
        Use backup=False to disable renaming of an existing file.

    backend='ulm':
        Request a backend.  Currently only 'ulm' is supported.
        Only honored when writing.

    singleprecision=False:
        Store floating point data in single precision (ulm backend only).
    """
    slavelog = True  # Log from all nodes

    def __init__(self, filename, mode='r', atoms=None, backup=True,
                 backend='ulm', singleprecision=False):
        self.state = 'constructing'
        self.filename = filename
        self.pre_observers = []  # callback functions before write is performed
        self.post_observers = []  # callback functions after write is performed
        self.master = world.rank == 0
        self.extra_data = []
        self.singleprecision = singleprecision
        self._set_defaults()
        if mode == 'r':
            if atoms is not None:
                raise ValueError('You cannot specify atoms in read mode.')
            self._open_read()
        elif mode == 'w':
            self._open_write(atoms, backup, backend)
        elif mode == 'a':
            self._open_append(atoms, backend)
        else:
            raise ValueError('Unknown mode: ' + str(mode))

    def _set_defaults(self):
        "Set default values for internal parameters."
        self.version = 1
        self.subtype = 'normal'
        self.datatypes = {'positions': True,
                          'numbers': 'once',
                          'tags': 'once',
                          'masses': 'once',
                          'momenta': True,
                          'forces': True,
                          'energy': True,
                          'energies': False,
                          'stress': False,
                          'magmoms': True}

    def _set_backend(self, backend):
        """Set the backed doing the actual I/O."""
        if backend is not None:
            self.backend_name = backend

        if self.backend_name == 'ulm':
            self.backend = UlmBundleBackend(self.master, self.singleprecision)
        else:
            raise NotImplementedError(
                'This version of ASE cannot use BundleTrajectory '
                'with backend "%s"' % self.backend_name)

    def write(self, atoms=None):
        """Write the atoms to the file.

        If the atoms argument is not given, the atoms object specified
        when creating the trajectory object is used.
        """
        # Check that we are in write mode
        if self.state == 'prewrite':
            self.state = 'write'
            assert self.nframes == 0
        elif self.state != 'write':
            raise RuntimeError('Cannot write in ' + self.state + ' mode.')

        if atoms is None:
            atoms = self.atoms

        # Handle NEB etc.  If atoms is just a normal Atoms object, it is used
        # as-is.
        for image in atoms.iterimages():
            self._write_atoms(image)

    def _write_atoms(self, atoms):
        "Write a single atoms object to file."
        self._call_observers(self.pre_observers)
        self.log('Beginning to write frame ' + str(self.nframes))
        framedir = self._make_framedir(self.nframes)

        # Check which data should be written the first time:
        # Modify datatypes so any element of type 'once' becomes true
        # for the first frame but false for subsequent frames.
        datatypes = {}
        for k, v in self.datatypes.items():
            if v == 'once':
                v = (self.nframes == 0)
            datatypes[k] = v

        # Write 'small' data structures.  They are written jointly.
        smalldata = {'pbc': atoms.get_pbc(),
                     'cell': atoms.get_cell(),
                     'natoms': atoms.get_global_number_of_atoms(),
                     'constraints': atoms.constraints}
        if datatypes.get('energy'):
            try:
                smalldata['energy'] = atoms.get_potential_energy()
            except (RuntimeError, PropertyNotImplementedError):
                self.datatypes['energy'] = False
        if datatypes.get('stress'):
            try:
                smalldata['stress'] = atoms.get_stress()
            except PropertyNotImplementedError:
                self.datatypes['stress'] = False
        self.backend.write_small(framedir, smalldata)

        # Write the large arrays.
        if datatypes.get('positions'):
            self.backend.write(framedir, 'positions', atoms.get_positions())
        if datatypes.get('numbers'):
            self.backend.write(framedir, 'numbers', atoms.get_atomic_numbers())
        if datatypes.get('tags'):
            if atoms.has('tags'):
                self.backend.write(framedir, 'tags', atoms.get_tags())
            else:
                self.datatypes['tags'] = False
        if datatypes.get('masses'):
            if atoms.has('masses'):
                self.backend.write(framedir, 'masses', atoms.get_masses())
            else:
                self.datatypes['masses'] = False
        if datatypes.get('momenta'):
            if atoms.has('momenta'):
                self.backend.write(framedir, 'momenta', atoms.get_momenta())
            else:
                self.datatypes['momenta'] = False
        if datatypes.get('magmoms'):
            if atoms.has('initial_magmoms'):
                self.backend.write(framedir, 'magmoms',
                                   atoms.get_initial_magnetic_moments())
            else:
                self.datatypes['magmoms'] = False
        if datatypes.get('forces'):
            try:
                x = atoms.get_forces()
            except (RuntimeError, PropertyNotImplementedError):
                self.datatypes['forces'] = False
            else:
                self.backend.write(framedir, 'forces', x)
                del x
        if datatypes.get('energies'):
            try:
                x = atoms.get_potential_energies()
            except (RuntimeError, PropertyNotImplementedError):
                self.datatypes['energies'] = False
            else:
                self.backend.write(framedir, 'energies', x)
                del x
        # Write any extra data
        for (label, source, once) in self.extra_data:
            if self.nframes == 0 or not once:
                if source is not None:
                    x = source()
                else:
                    x = atoms.get_array(label)
                self.backend.write(framedir, label, x)
                del x
                if once:
                    self.datatypes[label] = 'once'
                else:
                    self.datatypes[label] = True
        # Finally, write metadata if it is the first frame
        if self.nframes == 0:
            metadata = {'datatypes': self.datatypes}
            self._write_metadata(metadata)
        self._write_nframes(self.nframes + 1)
        self._call_observers(self.post_observers)
        self.log('Done writing frame ' + str(self.nframes))
        self.nframes += 1

    def select_data(self, data, value):
        """Selects if a given data type should be written.

        Data can be written in every frame (specify True), in the
        first frame only (specify 'only') or not at all (specify
        False).  Not all data types support the 'only' keyword, if not
        supported it is interpreted as True.

        The following data types are supported, the letter in parenthesis
        indicates the default:

        positions (T), numbers (O), tags (O), masses (O), momenta (T),
        forces (T), energy (T), energies (F), stress (F), magmoms (T)

        If a given property is not present during the first write, it
        will be not be saved at all.
        """
        if value not in (True, False, 'once'):
            raise ValueError('Unknown write mode')
        if data not in self.datatypes:
            raise ValueError('Unsupported data type: ' + data)
        self.datatypes[data] = value

    def set_extra_data(self, name, source=None, once=False):
        """Adds extra data to be written.

        Parameters:
        name:  The name of the data.

        source (optional): If specified, a callable object returning
        the data to be written.  If not specified it is instead
        assumed that the atoms contains the data as an array of the
        same name.

        once (optional): If specified and True, the data will only be
        written to the first frame.
        """
        self.extra_data.append((name, source, once))

    def close(self):
        "Closes the trajectory."
        self.state = 'closed'
        lf = getattr(self, 'logfile', None)
        self.backend.close(log=lf)
        if lf is not None:
            lf.close()
            del self.logfile

    def log(self, text):
        """Write to the log file in the bundle.

        Logging is only possible in write/append mode.

        This function is mainly for internal use, but can also be called by
        the user.
        """
        if not (self.master or self.slavelog):
            return
        text = time.asctime() + ': ' + text
        if hasattr(self, 'logfile'):
            # Logging enabled
            if self.logfile is None:
                # Logfile not yet open
                try:
                    self.logdata.append(text)
                except AttributeError:
                    self.logdata = [text]
            else:
                self.logfile.write(text + '\n')
                self.logfile.flush()
        else:
            raise RuntimeError('Cannot write to log file in mode ' +
                               self.state)

    # __getitem__ is the main reading method.
    def __getitem__(self, n):
        return self._read(n)

    def _read(self, n):
        """Read an atoms object from the BundleTrajectory."""
        if self.state != 'read':
            raise OSError(f'Cannot read in {self.state} mode')
        if n < 0:
            n += self.nframes
        if n < 0 or n >= self.nframes:
            raise IndexError('Trajectory index %d out of range [0, %d['
                             % (n, self.nframes))

        framedir = os.path.join(self.filename, 'F' + str(n))
        framezero = os.path.join(self.filename, 'F0')
        smalldata = self.backend.read_small(framedir)
        data = {}
        data['pbc'] = smalldata['pbc']
        data['cell'] = smalldata['cell']
        data['constraint'] = smalldata['constraints']
        if self.subtype == 'split':
            self.backend.set_fragments(smalldata['fragments'])
            self.atom_id, _dummy = self.backend.read_split(framedir, 'ID')
        else:
            self.atom_id = None
        atoms = Atoms(**data)
        natoms = smalldata['natoms']
        for name in ('positions', 'numbers', 'tags', 'masses',
                     'momenta'):
            if self.datatypes.get(name):
                atoms.arrays[name] = self._read_data(framezero, framedir,
                                                     name, self.atom_id)
                assert len(atoms.arrays[name]) == natoms

        # Create the atoms object
        if self.datatypes.get('energy'):
            if self.datatypes.get('forces'):
                forces = self.backend.read(framedir, 'forces')
            else:
                forces = None
            if self.datatypes.get('magmoms'):
                magmoms = self.backend.read(framedir, 'magmoms')
            else:
                magmoms = None
            calc = SinglePointCalculator(atoms,
                                         energy=smalldata.get('energy'),
                                         forces=forces,
                                         stress=smalldata.get('stress'),
                                         magmoms=magmoms)
            atoms.calc = calc
        return atoms

    def read_extra_data(self, name, n=0):
        """Read extra data stored alongside the atoms.

        Currently only used to read data stored by an NPT dynamics object.
        The data is not associated with individual atoms.
        """
        if self.state != 'read':
            raise OSError(f'Cannot read extra data in {self.state} mode')
        # Handle negative n.
        if n < 0:
            n += self.nframes
        if n < 0 or n >= self.nframes:
            raise IndexError('Trajectory index %d out of range [0, %d['
                             % (n, self.nframes))
        framedir = os.path.join(self.filename, 'F' + str(n))
        framezero = os.path.join(self.filename, 'F0')
        return self._read_data(framezero, framedir, name, self.atom_id)

    def _read_data(self, f0, f, name, atom_id):
        "Read single data item."

        if self.subtype == 'normal':
            if self.datatypes[name] == 'once':
                d = self.backend.read(f0, name)
            else:
                d = self.backend.read(f, name)
        elif self.subtype == 'split':
            if self.datatypes[name] == 'once':
                d, issplit = self.backend.read_split(f0, name)
                atom_id, _dummy = self.backend.read_split(f0, 'ID')
            else:
                d, issplit = self.backend.read_split(f, name)
            if issplit:
                assert atom_id is not None
                assert len(d) == len(atom_id)
                d[atom_id] = np.array(d)
        return d

    def __len__(self):
        return self.nframes

    def _open_log(self):
        "Open the log file."
        if not (self.master or self.slavelog):
            return
        if self.master:
            lfn = os.path.join(self.filename, 'log.txt')
        else:
            lfn = os.path.join(self.filename, ('log-node%d.txt' %
                                               (world.rank,)))
        self.logfile = open(lfn, 'a', 1)   # Append to log if it exists.
        if hasattr(self, 'logdata'):
            for text in self.logdata:
                self.logfile.write(text + '\n')
            self.logfile.flush()
            del self.logdata

    def _open_write(self, atoms, backup, backend):
        """Open a bundle trajectory for writing.

        Parameters:
        atoms: Object to be written.
        backup: (bool) Whether a backup is kept if file already exists.
        backend: Which type of backend to use.

        Note that the file name of the bundle is already stored as an attribute.
        """
        self._set_backend(backend)
        self.logfile = None  # enable delayed logging
        self.atoms = atoms
        if os.path.exists(self.filename):
            # The output directory already exists.
            barrier()  # all must have time to see it exists
            if not self.is_bundle(self.filename, allowempty=True):
                raise OSError(
                    'Filename "' + self.filename +
                    '" already exists, but is not a BundleTrajectory.' +
                    ' Cowardly refusing to remove it.')
            if self.is_empty_bundle(self.filename):
                barrier()
                self.log(f'Deleting old "{self.filename}" as it is empty')
                self.delete_bundle(self.filename)
            elif not backup:
                barrier()
                self.log(
                    f'Deleting old "{self.filename}" as backup is turned off.')
                self.delete_bundle(self.filename)
            else:
                barrier()
                # Make a backup file
                bakname = self.filename + '.bak'
                if os.path.exists(bakname):
                    barrier()  # All must see it exists
                    self.log(f'Deleting old backup file "{bakname}"')
                    self.delete_bundle(bakname)
                self.log(f'Renaming "{self.filename}" to "{bakname}"')
                self._rename_bundle(self.filename, bakname)
        # Ready to create a new bundle.
        barrier()
        self.log(f'Creating new "{self.filename}"')
        self._make_bundledir(self.filename)
        self.state = 'prewrite'
        self._write_metadata({})
        self._write_nframes(0)    # Mark new bundle as empty
        self._open_log()
        self.nframes = 0

    def _open_read(self):
        "Open a bundle trajectory for reading."
        if not os.path.exists(self.filename):
            raise OSError('File not found: ' + self.filename)
        if not self.is_bundle(self.filename):
            raise OSError('Not a BundleTrajectory: ' + self.filename)
        self.state = 'read'
        # Read the metadata
        metadata = self._read_metadata()
        self.metadata = metadata
        if metadata['version'] > self.version:
            raise NotImplementedError(
                'This version of ASE cannot read a BundleTrajectory version ' +
                str(metadata['version']))
        if metadata['subtype'] not in ('normal', 'split'):
            raise NotImplementedError(
                'This version of ASE cannot read BundleTrajectory subtype ' +
                metadata['subtype'])
        self.subtype = metadata['subtype']
        if metadata['backend'] == 'ulm':
            self.singleprecision = metadata['ulm.singleprecision']
        self._set_backend(metadata['backend'])
        self.nframes = self._read_nframes()
        if self.nframes == 0:
            raise OSError('Empty BundleTrajectory')
        self.datatypes = metadata['datatypes']
        try:
            self.pythonmajor = metadata['python_ver'][0]
        except KeyError:
            self.pythonmajor = 2  # Assume written with Python 2.
        # We need to know if we are running Python 3.X and try to read
        # a bundle written with Python 2.X
        self.backend.readpy2 = (self.pythonmajor == 2)
        self.state = 'read'

    def _open_append(self, atoms, backend):
        """Open a trajectory for writing in append mode.

        If there is no pre-existing bundle, it is just opened in write mode
        instead.

        Parameters:
        atoms:  Object to be written.
        backend:  The backend to be used if a new bundle is opened.  Ignored
                  if we append to existing bundle, as the backend cannot be
                  changed.

        The filename is already stored as an attribute.
        """
        if not os.path.exists(self.filename):
            # OK, no old bundle.  Open as for write instead.
            barrier()
            self._open_write(atoms, False, backend)
            return
        if not self.is_bundle(self.filename):
            raise OSError('Not a BundleTrajectory: ' + self.filename)
        self.state = 'read'
        metadata = self._read_metadata()
        self.metadata = metadata
        if metadata['version'] != self.version:
            raise NotImplementedError(
                'Cannot append to a BundleTrajectory version '
                '%s (supported version is %s)' % (str(metadata['version']),
                                                  str(self.version)))
        if metadata['subtype'] not in ('normal', 'split'):
            raise NotImplementedError(
                'This version of ASE cannot append to BundleTrajectory '
                'subtype ' + metadata['subtype'])
        self.subtype = metadata['subtype']
        if metadata['backend'] == 'ulm':
            self.singleprecision = metadata['ulm.singleprecision']
        self._set_backend(metadata['backend'])
        self.nframes = self._read_nframes()
        self._open_log()
        self.log('Opening "%s" in append mode (nframes=%i)' % (self.filename,
                                                               self.nframes))
        self.state = 'write'
        self.atoms = atoms

    @property
    def path(self):
        return Path(self.filename)

    @property
    def metadata_path(self):
        return self.path / 'metadata.json'

    def _write_nframes(self, n):
        "Write the number of frames in the bundle."
        assert self.state == 'write' or self.state == 'prewrite'
        with paropen(self.path / 'frames', 'w') as fd:
            fd.write(str(n) + '\n')

    def _read_nframes(self):
        "Read the number of frames."
        return int((self.path / 'frames').read_text())

    def _write_metadata(self, metadata):
        """Write the metadata file of the bundle.

        Modifies the medadata dictionary!
        """
        # Add standard fields that must always be present.
        assert self.state == 'write' or self.state == 'prewrite'
        metadata['format'] = 'BundleTrajectory'
        metadata['version'] = self.version
        metadata['subtype'] = self.subtype
        metadata['backend'] = self.backend_name
        if self.backend_name == 'ulm':
            metadata['ulm.singleprecision'] = self.singleprecision
        metadata['python_ver'] = tuple(sys.version_info)
        encode = jsonio.MyEncoder(indent=4).encode
        fido = encode(metadata)
        with paropen(self.metadata_path, 'w') as fd:
            fd.write(fido)

    def _read_metadata(self):
        """Read the metadata."""
        assert self.state == 'read'
        return jsonio.decode(self.metadata_path.read_text())

    @staticmethod
    def is_bundle(filename, allowempty=False):
        """Check if a filename exists and is a BundleTrajectory.

        If allowempty=True, an empty folder is regarded as an
        empty BundleTrajectory."""
        filename = Path(filename)
        if not filename.is_dir():
            return False
        if allowempty and not os.listdir(filename):
            return True   # An empty BundleTrajectory
        metaname = filename / 'metadata.json'
        if metaname.is_file():
            mdata = jsonio.decode(metaname.read_text())
        else:
            return False

        try:
            return mdata['format'] == 'BundleTrajectory'
        except KeyError:
            return False

    @staticmethod
    def is_empty_bundle(filename):
        """Check if a filename is an empty bundle.

        Assumes that it is a bundle."""
        if not os.listdir(filename):
            return True   # Empty folders are empty bundles.
        with open(os.path.join(filename, 'frames'), 'rb') as fd:
            nframes = int(fd.read())

        # File may be removed by the master immediately after this.
        barrier()
        return nframes == 0

    @classmethod
    def delete_bundle(cls, filename):
        "Deletes a bundle."
        if world.rank == 0:
            # Only the master deletes
            if not cls.is_bundle(filename, allowempty=True):
                raise OSError(
                    f'Cannot remove "{filename}" as it is not a bundle '
                    'trajectory.'
                )
            if os.path.islink(filename):
                # A symbolic link to a bundle.  Only remove the link.
                os.remove(filename)
            else:
                # A real bundle
                shutil.rmtree(filename)
        else:
            # All other tasks wait for the directory to go away.
            while os.path.exists(filename):
                time.sleep(1)
        # The master may not proceed before all tasks have seen the
        # directory go away, as it might otherwise create a new bundle
        # with the same name, fooling the wait loop in _make_bundledir.
        barrier()

    def _rename_bundle(self, oldname, newname):
        "Rename a bundle.  Used to create the .bak"
        if self.master:
            os.rename(oldname, newname)
        else:
            while os.path.exists(oldname):
                time.sleep(1)
        # The master may not proceed before all tasks have seen the
        # directory go away.
        barrier()

    def _make_bundledir(self, filename):
        """Make the main bundle directory.

        Since all MPI tasks might write to it, all tasks must wait for
        the directory to appear.
        """
        self.log('Making directory ' + filename)
        assert not os.path.isdir(filename)
        barrier()
        if self.master:
            os.mkdir(filename)
        else:
            i = 0
            while not os.path.isdir(filename):
                time.sleep(1)
                i += 1
            if i > 10:
                self.log('Waiting %d seconds for %s to appear!'
                         % (i, filename))

    def _make_framedir(self, frame):
        """Make subdirectory for the frame.

        As only the master writes to it, no synchronization between
        MPI tasks is necessary.
        """
        framedir = os.path.join(self.filename, 'F' + str(frame))
        if self.master:
            self.log('Making directory ' + framedir)
            os.mkdir(framedir)
        return framedir

    def pre_write_attach(self, function, interval=1, *args, **kwargs):
        """Attach a function to be called before writing begins.

        function: The function or callable object to be called.

        interval: How often the function is called.  Default: every time (1).

        All other arguments are stored, and passed to the function.
        """
        if not callable(function):
            raise ValueError('Callback object must be callable.')
        self.pre_observers.append((function, interval, args, kwargs))

    def post_write_attach(self, function, interval=1, *args, **kwargs):
        """Attach a function to be called after writing ends.

        function: The function or callable object to be called.

        interval: How often the function is called.  Default: every time (1).

        All other arguments are stored, and passed to the function.
        """
        if not callable(function):
            raise ValueError('Callback object must be callable.')
        self.post_observers.append((function, interval, args, kwargs))

    def _call_observers(self, obs):
        "Call pre/post write observers."
        for function, interval, args, kwargs in obs:
            if (self.nframes + 1) % interval == 0:
                function(*args, **kwargs)


class UlmBundleBackend:
    """Backend for BundleTrajectories stored as ASE Ulm files."""

    def __init__(self, master, singleprecision):
        # Store if this backend will actually write anything
        self.writesmall = master
        self.writelarge = master
        self.singleprecision = singleprecision

        # Integer data may be downconverted to the following types
        self.integral_dtypes = ['uint8', 'int8', 'uint16', 'int16',
                                'uint32', 'int32', 'uint64', 'int64']
        # Dict comprehensions not supported in Python 2.6 :-(
        self.int_dtype = {k: getattr(np, k)
                          for k in self.integral_dtypes}
        self.int_minval = {k: np.iinfo(self.int_dtype[k]).min
                           for k in self.integral_dtypes}
        self.int_maxval = {k: np.iinfo(self.int_dtype[k]).max
                           for k in self.integral_dtypes}
        self.int_itemsize = {k: np.dtype(self.int_dtype[k]).itemsize
                             for k in self.integral_dtypes}

    def write_small(self, framedir, smalldata):
        "Write small data to be written jointly."
        if self.writesmall:
            with ulmopen(os.path.join(framedir, 'smalldata.ulm'), 'w') as fd:
                fd.write(**smalldata)

    def write(self, framedir, name, data):
        "Write data to separate file."
        if self.writelarge:
            shape = data.shape
            dtype = str(data.dtype)
            stored_as = dtype
            all_identical = False
            # Check if it a type that can be stored with less space
            if np.issubdtype(data.dtype, np.integer):
                # An integer type, we may want to convert
                minval = data.min()
                maxval = data.max()

                # ulm cannot write np.bool_:
                all_identical = bool(minval == maxval)
                if all_identical:
                    data = int(data.flat[0])  # Convert to standard integer
                else:
                    for typ in self.integral_dtypes:
                        if (minval >= self.int_minval[typ] and
                            maxval <= self.int_maxval[typ] and
                                data.itemsize > self.int_itemsize[typ]):

                            # Convert to smaller type
                            stored_as = typ
                            data = data.astype(self.int_dtype[typ])
            elif data.dtype == np.float32 or data.dtype == np.float64:
                all_identical = bool(data.min() == data.max())
                if all_identical:
                    data = float(data.flat[0])  # Convert to standard float
                elif data.dtype == np.float64 and self.singleprecision:
                    # Downconvert double to single precision
                    stored_as = 'float32'
                    data = data.astype(np.float32)
            fn = os.path.join(framedir, name + '.ulm')
            with ulmopen(fn, 'w') as fd:
                fd.write(shape=shape,
                         dtype=dtype,
                         stored_as=stored_as,
                         all_identical=all_identical,
                         data=data)

    def read_small(self, framedir):
        "Read small data."
        with ulmopen(os.path.join(framedir, 'smalldata.ulm'), 'r') as fd:
            return fd.asdict()

    def read(self, framedir, name):
        "Read data from separate file."
        fn = os.path.join(framedir, name + '.ulm')
        with ulmopen(fn, 'r') as fd:
            if fd.all_identical:
                # Only a single data value
                data = np.zeros(fd.shape,
                                dtype=getattr(np, fd.dtype)) + fd.data
            elif fd.dtype == fd.stored_as:
                # Easy, the array can be returned as-is.
                data = fd.data
            else:
                # Cast the data back
                data = fd.data.astype(getattr(np, fd.dtype))
        return data

    def read_info(self, framedir, name, split=None):
        """Read information about file contents without reading the data.

        Information is a dictionary containing as aminimum the shape and
        type.
        """
        fn = os.path.join(framedir, name + '.ulm')
        if split is None or os.path.exists(fn):
            with ulmopen(fn, 'r') as fd:
                info = {}
                info['shape'] = fd.shape
                info['type'] = fd.dtype
                info['stored_as'] = fd.stored_as
                info['identical'] = fd.all_identical
            return info
        else:
            info = {}
            for i in range(split):
                fn = os.path.join(framedir, name + '_' + str(i) + '.ulm')
                with ulmopen(fn, 'r') as fd:
                    if i == 0:
                        info['shape'] = list(fd.shape)
                        info['type'] = fd.dtype
                        info['stored_as'] = fd.stored_as
                        info['identical'] = fd.all_identical
                    else:
                        info['shape'][0] += fd.shape[0]
                        assert info['type'] == fd.dtype
                        info['identical'] = (info['identical']
                                             and fd.all_identical)
            info['shape'] = tuple(info['shape'])
            return info

    def set_fragments(self, nfrag):
        self.nfrag = nfrag

    def read_split(self, framedir, name):
        """Read data from multiple files.

        Falls back to reading from single file if that is how data is stored.

        Returns the data and an object indicating if the data was really
        read from split files.  The latter object is False if not
        read from split files, but is an array of the segment length if
        split files were used.
        """
        data = []
        if os.path.exists(os.path.join(framedir, name + '.ulm')):
            # Not stored in split form!
            return (self.read(framedir, name), False)
        for i in range(self.nfrag):
            suf = '_%d' % (i,)
            data.append(self.read(framedir, name + suf))
        seglengths = [len(d) for d in data]
        return (np.concatenate(data), seglengths)

    def close(self, log=None):
        """Close anything that needs to be closed by the backend.

        The default backend does nothing here.
        """


def read_bundletrajectory(filename, index=-1):
    """Reads one or more atoms objects from a BundleTrajectory.

    Arguments:

    filename: str
        The name of the bundle (really a directory!)
    index: int
        An integer specifying which frame to read, or an index object
        for reading multiple frames.  Default: -1 (reads the last
        frame).
    """
    traj = BundleTrajectory(filename, mode='r')
    if isinstance(index, int):
        yield traj[index]

    for i in range(*index.indices(len(traj))):
        yield traj[i]


def write_bundletrajectory(filename, images, append=False):
    """Write image(s) to a BundleTrajectory.

    Write also energy, forces, and stress if they are already
    calculated.
    """

    if append:
        mode = 'a'
    else:
        mode = 'w'
    traj = BundleTrajectory(filename, mode=mode)

    if hasattr(images, 'get_positions'):
        images = [images]

    for atoms in images:
        # Avoid potentially expensive calculations:
        calc = atoms.calc
        if hasattr(calc, 'calculation_required'):
            for quantity in ('energy', 'forces', 'stress', 'magmoms'):
                traj.select_data(quantity,
                                 not calc.calculation_required(atoms,
                                                               [quantity]))
        traj.write(atoms)
    traj.close()


def print_bundletrajectory_info(filename):
    """Prints information about a BundleTrajectory.

    Mainly intended to be called from a command line tool.
    """
    if not BundleTrajectory.is_bundle(filename):
        raise ValueError('Not a BundleTrajectory!')
    if BundleTrajectory.is_empty_bundle(filename):
        print(filename, 'is an empty BundleTrajectory.')
        return
    # Read the metadata
    fn = os.path.join(filename, 'metadata.json')
    with open(fn) as fd:
        metadata = jsonio.decode(fd.read())

    print(f'Metadata information of BundleTrajectory "{filename}":')
    for k, v in metadata.items():
        if k != 'datatypes':
            print(f"  {k}: {v}")
    with open(os.path.join(filename, 'frames'), 'rb') as fd:
        nframes = int(fd.read())
    print('Number of frames: %i' % (nframes,))
    print('Data types:')
    for k, v in metadata['datatypes'].items():
        if v == 'once':
            print(f'  {k}: First frame only.')
        elif v:
            print(f'  {k}: All frames.')
    # Look at first frame
    if metadata['backend'] == 'ulm':
        backend = UlmBundleBackend(True, False)
    else:
        raise NotImplementedError(
            f'Backend {metadata["backend"]} not supported.')
    frame = os.path.join(filename, 'F0')
    small = backend.read_small(frame)
    print('Contents of first frame:')
    for k, v in small.items():
        if k == 'constraints':
            if v:
                print(f'  {len(v)} constraints are present')
            else:
                print('  Constraints are absent.')
        elif k == 'pbc':
            print(f'  Periodic boundary conditions: {v!s}')
        elif k == 'natoms':
            print('  Number of atoms: %i' % (v,))
        elif hasattr(v, 'shape'):
            print(f'  {k}: shape = {v.shape!s}, type = {v.dtype!s}')
            if k == 'cell':
                print('        [[%12.6f, %12.6f, %12.6f],' % tuple(v[0]))
                print('         [%12.6f, %12.6f, %12.6f],' % tuple(v[1]))
                print('         [%12.6f, %12.6f, %12.6f]]' % tuple(v[2]))
        else:
            print(f'  {k}: {v!s}')
    # Read info from separate files.
    if metadata['subtype'] == 'split':
        nsplit = small['fragments']
    else:
        nsplit = False
    for k, v in metadata['datatypes'].items():
        if v and k not in small:
            info = backend.read_info(frame, k, nsplit)
            infoline = f'  {k}: '
            for k, v in info.items():
                infoline += f'{k} = {v!s}, '
            infoline = infoline[:-2] + '.'  # Fix punctuation.
            print(infoline)


def main():
    import optparse
    parser = optparse.OptionParser(
        usage='python -m ase.io.bundletrajectory '
        'a.bundle [b.bundle ...]',
        description='Print information about '
        'the contents of one or more bundletrajectories.')
    _opts, args = parser.parse_args()
    for name in args:
        print_bundletrajectory_info(name)


if __name__ == '__main__':
    main()
