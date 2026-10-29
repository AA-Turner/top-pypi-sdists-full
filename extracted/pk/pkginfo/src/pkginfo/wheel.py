import io
import os
import zipfile


from .distribution import Distribution
from .distribution import parse


class Wheel(Distribution):

    def __init__(self, filename, metadata_version=None):
        self.filename = filename
        self.metadata_version = metadata_version
        self._parseFilenameTags()
        self.purelib = None
        self.extractMetadata()

    def _parseFilenameTags(self):
        # PEP 427:  {distribution}-{version}(-{build})?-{python}-{abi}-{platform}.whl
        stem = os.path.basename(self.filename)
        if stem.endswith('.whl'):
            stem = stem[:-len('.whl')]
        parts = stem.split('-')
        if len(parts) == 5:
            self.build_tag = None
            self.python_tag, self.abi_tag, self.platform_tag = parts[2:]
        elif len(parts) == 6:
            self.build_tag, self.python_tag, self.abi_tag, self.platform_tag = (
                parts[2:])
        else:
            self.build_tag = None
            self.python_tag = None
            self.abi_tag = None
            self.platform_tag = None

    def _extractPurelib(self, metadata_path, names, read_file):
        # PEP 427:  'Root-Is-Purelib' lives in the sibling 'WHEEL' file,
        # and is True iff the archive contents install into 'purelib'
        # (vs. 'platlib');  pure wheels built without extensions are
        # tagged 'any' for the platform.
        wheel_name = metadata_path[:-len('METADATA')] + 'WHEEL'
        if wheel_name not in names:
            return
        wheel_data = read_file(wheel_name).decode('ascii', 'ignore')
        root_is_purelib = parse(io.StringIO(wheel_data)).get(
            'Root-Is-Purelib')
        if root_is_purelib is not None:
            root_is_purelib = root_is_purelib.strip().lower()
            if root_is_purelib == 'true':
                self.purelib = True
            elif root_is_purelib == 'false':
                self.purelib = False

    def read(self):
        fqn = os.path.abspath(os.path.normpath(self.filename))
        if not os.path.exists(fqn):
            raise ValueError('No such file: %s' % fqn)

        if fqn.endswith('.whl'):
            archive = zipfile.ZipFile(fqn)
            names = archive.namelist()

            def read_file(name):
                return archive.read(name)

            close = archive.close

        elif fqn.endswith('.dist-info'):
            names = [os.path.join(fqn, p) for p in os.listdir(fqn)]

            def read_file(name):
                with io.open(name, mode='rb') as inf:
                    return inf.read()

            close = lambda : None

        else:
            raise ValueError('Not a known wheel archive format or '
                             'installed .dist-info: %s' % fqn)

        try:
            tuples = [x.split('/') for x in names if 'METADATA' in x]
            schwarz = sorted([(len(x), x) for x in tuples])
            for path in [x[1] for x in schwarz]:
                candidate = '/'.join(path)
                data = read_file(candidate)
                if b'Metadata-Version' in data:
                    self._extractPurelib(candidate, names, read_file)
                    return data
        finally:
            close()

        raise ValueError('No METADATA in archive: %s' % fqn)
