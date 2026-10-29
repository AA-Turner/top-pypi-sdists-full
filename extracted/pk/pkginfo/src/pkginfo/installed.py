import glob
import io
import os
import sys
import warnings

from .distribution import Distribution

class Installed(Distribution):

    def __init__(self, package, metadata_version=None):
        if isinstance(package, str):
            self.package_name = package
            try:
                __import__(package)
            except ImportError:
                package = None
            else:
                package = sys.modules[package]
        else:
            self.package_name = package.__name__
        self.package = package
        self.metadata_version = metadata_version
        self.extractMetadata()

    def read(self):
        opj = os.path.join
        if self.package is not None:
            bases = []
            for base in (self.package.__package__, self.package_name):
                if base not in ('', None) and base not in bases:
                    bases.append(base)
            # Bound at the '<name>-<version>' boundary:  don't let a
            # package whose name is a prefix of another package's name
            # match that other package's metadata (LP #1974172 / GH #9).
            egg_patterns, dist_patterns = [], []
            for base in bases:
                egg_patterns.append('%s-[0-9]*.egg-info' % base)
                dist_patterns.append('%s-[0-9]*.dist-info' % base)
            for base in bases:
                # version-less egg-info file / directory, e.g. from a
                # development or legacy install ('funny.egg-info')
                egg_patterns.append('%s.egg-info' % base)
            candidates = []
            def _add_candidate(where):
                candidates.extend(glob.glob(where))
            pkg_file = getattr(self.package, '__file__', None)
            if pkg_file is not None:
                for entry in sys.path:
                    if pkg_file.startswith(entry):
                        _add_candidate(opj(entry, 'EGG-INFO'))  # egg?
                        for pattern in egg_patterns:
                            _add_candidate(opj(entry, pattern))
                        for pattern in dist_patterns:
                            _add_candidate(opj(entry, pattern))
                dir, name = os.path.split(self.package.__file__)
                for egg_pattern in egg_patterns:
                    _add_candidate(opj(dir, egg_pattern))
                    _add_candidate(opj(dir, '..', egg_pattern))
                for dist_pattern in dist_patterns:
                    _add_candidate(opj(dir, dist_pattern))
                    _add_candidate(opj(dir, '..', dist_pattern))
                for candidate in candidates:
                    if os.path.isdir(candidate):
                        if candidate.lower().endswith("egg-info"):
                            path = opj(candidate, 'PKG-INFO')
                        elif candidate.endswith("dist-info"):
                            path = opj(candidate, 'METADATA')
                        else:  # pragma: NO COVER
                            continue
                    else:
                        path = candidate
                    if os.path.exists(path):
                        with io.open(path, errors='ignore') as f:
                            return f.read()
        warnings.warn('No PKG-INFO found for package: %s' % self.package_name)
