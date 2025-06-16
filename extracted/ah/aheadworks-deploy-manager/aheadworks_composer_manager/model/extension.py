import os, shutil
import re
import json
import zipfile

from tempfile import mkdtemp


class VerfiedDescriptior:
    def __init__(self):
        self.val = {}

    def __get__(self, obj, objtype):
        return self.val[obj]

    def __set__(self, obj, val):
        self.val[obj] = val


class NameDescriptor(VerfiedDescriptior):

    def __set__(self, obj, val):
        if not re.match( r"^([a-z0-9_-])+/([a-z0-9_-])+$", val, re.IGNORECASE):
            raise ValueError("Name must be in <vendor>/<package name> format, \"%s\" given" % val)
        self.val[obj] = val


class VersionDescriptor(VerfiedDescriptior):

    def __set__(self, obj, val):
        # Check `version` field
        if not re.match(r"^(|v)([0-9])+\.([0-9])+\.([0-9])+(-(patch|p|dev|a|alpha|b|beta|rc)([0-9])*)?$", val):
            raise ValueError("Version must follow https://getcomposer.org/doc/04-schema.md#version"
                             "format, \"%s\" given" % val)
        self.val[obj] = val


class TypeDescriptor(VerfiedDescriptior):

    allowed = ("magento2-theme", "magento2-language", "magento2-module")

    def __set__(self, obj, val):
        if val not in self.allowed:
            raise ValueError("Type can only be one of the following:"
                             "%s; %s given." % (", ".join(self.allowed), val))
        self.val[obj] = val


class Metadata:
    """
    Composer.json wrapper with m2-extension specific options and checks
    """

    name = NameDescriptor()
    version = VersionDescriptor()
    type = TypeDescriptor()

    def __init__(self):
        pass

    def init_from_file(self, fp):

        s = fp.read()
        try:
            js = json.loads(s)
        except TypeError:
            js = json.loads(s.decode())
        self.update(js)

    def update(self, values):
        for k, v in values.items():
            setattr(self, k, v)

    def __iter__(self):
        return iter({k: getattr(self, k) for k in dir(self) if not k.startswith('__') and not callable(getattr(self, k))}.items())


class Extension:

    def __init__(self, path=None):
        self.meta = Metadata()
        self.path = path

    def __enter__(self):
        self.tempdir = mkdtemp()
        if os.path.isdir(self.path):
            self.init_from_path(self.path)
            return self

        with zipfile.ZipFile(self.path, "r") as zip_ref:
            zip_ref.extractall(self.tempdir)
            self.init_from_path(self.tempdir)
            return self

    def __exit__(self, etype, value, traceback):
        shutil.rmtree(self.tempdir)

    def init_from_path(self, path):
        self.path = path
        if not os.path.exists(os.path.join(self.path, 'registration.php')):
            raise IOError("registration.php file doesn't exist")

        with open(os.path.join(self.path, 'composer.json')) as jsfp:
            self.meta.init_from_file(jsfp)

    def init_from_zip(self, path):
        z = zipfile.ZipFile(path)
        for fn in z.namelist():
            if os.path.basename(fn) == 'composer.json':
                with z.open(fn) as fp:
                    self.meta.init_from_file(fp)
                    return
        raise IOError("No composer.json file found in {}". format(path))
