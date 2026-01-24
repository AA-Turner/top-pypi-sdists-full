from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ..._jsii import *


@jsii.enum(jsii_type="projen.python.uvConfig.AddBoundsKind")
class AddBoundsKind(enum.Enum):
    '''(experimental) The default version specifier when adding a dependency.

    :stability: experimental
    :schema: AddBoundsKind
    '''

    LOWER = "LOWER"
    '''(experimental) Only a lower bound, e.g., ``>=1.2.3``. (lower).

    :stability: experimental
    '''
    MAJOR = "MAJOR"
    '''(experimental) Allow the same major version, similar to the semver caret, e.g., ``>=1.2.3, <2.0.0``.

    Leading zeroes are skipped, e.g. ``>=0.1.2, <0.2.0``. (major)

    :stability: experimental
    '''
    MINOR = "MINOR"
    '''(experimental) Allow the same minor version, similar to the semver tilde, e.g., ``>=1.2.3, <1.3.0``.

    Leading zeroes are skipped, e.g. ``>=0.1.2, <0.1.3``. (minor)

    :stability: experimental
    '''
    EXACT = "EXACT"
    '''(experimental) Pin the exact version, e.g., ``==1.2.3``.

    This option is not recommended, as versions are already pinned in the uv lockfile. (exact)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.AnnotationStyle")
class AnnotationStyle(enum.Enum):
    '''(experimental) Indicate the style of annotation comments, used to indicate the dependencies that requested each package.

    :stability: experimental
    :schema: AnnotationStyle
    '''

    LINE = "LINE"
    '''(experimental) Render the annotations on a single, comma-separated line.

    (line)

    :stability: experimental
    '''
    SPLIT = "SPLIT"
    '''(experimental) Render each annotation on its own line.

    (split)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.AuthPolicy")
class AuthPolicy(enum.Enum):
    '''(experimental) When to use authentication.

    :stability: experimental
    :schema: AuthPolicy
    '''

    AUTO = "AUTO"
    '''(experimental) Authenticate when necessary.

    If credentials are provided, they will be used. Otherwise, an unauthenticated request will
    be attempted first. If the request fails, uv will search for credentials. If credentials are
    found, an authenticated request will be attempted. (auto)

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) Always authenticate.

    If credentials are not provided, uv will eagerly search for credentials. If credentials
    cannot be found, uv will error instead of attempting an unauthenticated request. (always)

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Never authenticate.

    If credentials are provided, uv will error. uv will not search for credentials. (never)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.BuildBackendSettings",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "default_excludes": "defaultExcludes",
        "module_name": "moduleName",
        "module_root": "moduleRoot",
        "namespace": "namespace",
        "source_exclude": "sourceExclude",
        "source_include": "sourceInclude",
        "wheel_exclude": "wheelExclude",
    },
)
class BuildBackendSettings:
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Union["WheelDataIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
        default_excludes: typing.Optional[builtins.bool] = None,
        module_name: typing.Any = None,
        module_root: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.bool] = None,
        source_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        wheel_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Settings for the uv build backend (``uv_build``).

        Note that those settings only apply when using the ``uv_build`` backend, other build backends
        (such as hatchling) have their own configuration.

        All options that accept globs use the portable glob patterns from
        `PEP 639 <https://packaging.python.org/en/latest/specifications/glob-patterns/>`_.

        :param data: (experimental) Data includes for wheels. Each entry is a directory, whose contents are copied to the matching directory in the wheel in ``<name>-<version>.data/(purelib|platlib|headers|scripts|data)``. Upon installation, this data is moved to its target location, as defined by `https://docs.python.org/3.12/library/sysconfig.html#installation-paths <https://docs.python.org/3.12/library/sysconfig.html#installation-paths>`_. Usually, small data files are included by placing them in the Python module instead of using data includes. - ``scripts``: Installed to the directory for executables, ``<venv>/bin`` on Unix or ``<venv>\\Scripts`` on Windows. This directory is added to ``PATH`` when the virtual environment is activated or when using ``uv run``, so this data type can be used to install additional binaries. Consider using ``project.scripts`` instead for Python entrypoints. - ``data``: Installed over the virtualenv environment root. Warning: This may override existing files! - ``headers``: Installed to the include directory. Compilers building Python packages with this package as build requirement use the include directory to find additional header files. - ``purelib`` and ``platlib``: Installed to the ``site-packages`` directory. It is not recommended to use these two options.
        :param default_excludes: (experimental) If set to ``false``, the default excludes aren't applied. Default excludes: ``__pycache__``, ``*.pyc``, and ``*.pyo``.
        :param module_name: (experimental) The name of the module directory inside ``module-root``. The default module name is the package name with dots and dashes replaced by underscores. Package names need to be valid Python identifiers, and the directory needs to contain a ``__init__.py``. An exception are stubs packages, whose name ends with ``-stubs``, with the stem being the module name, and which contain a ``__init__.pyi`` file. For namespace packages with a single module, the path can be dotted, e.g., ``foo.bar`` or ``foo-stubs.bar``. For namespace packages with multiple modules, the path can be a list, e.g., ``["foo", "bar"]``. We recommend using a single module per package, splitting multiple packages into a workspace. Note that using this option runs the risk of creating two packages with different names but the same module names. Installing such packages together leads to unspecified behavior, often with corrupted files or directory trees.
        :param module_root: (experimental) The directory that contains the module directory. Common values are ``src`` (src layout, the default) or an empty path (flat layout).
        :param namespace: (experimental) Build a namespace package. Build a PEP 420 implicit namespace package, allowing more than one root ``__init__.py``. Use this option when the namespace package contains multiple root ``__init__.py``, for namespace packages with a single root ``__init__.py`` use a dotted ``module-name`` instead. To compare dotted ``module-name`` and ``namespace = true``, the first example below can be expressed with ``module-name = "cloud.database"``: There is one root ``__init__.py`` ``database``. In the second example, we have three roots (``cloud.database``, ``cloud.database_pro``, ``billing.modules.database_pro``), so ``namespace = true`` is required:: src └── cloud └── database ├── __init__.py ├── query_builder │ └── __init__.py └── sql ├── parser.py └── __init__.py Example:: src ├── cloud │ ├── database │ │ ├── __init__.py │ │ ├── query_builder │ │ │ └── __init__.py │ │ └── sql │ │ ├── __init__.py │ │ └── parser.py │ └── database_pro │ ├── __init__.py │ └── query_builder.py └── billing └── modules └── database_pro ├── __init__.py └── sql.py
        :param source_exclude: (experimental) Glob expressions which files and directories to exclude from the source distribution.
        :param source_include: (experimental) Glob expressions which files and directories to additionally include in the source distribution. ``pyproject.toml`` and the contents of the module directory are always included.
        :param wheel_exclude: (experimental) Glob expressions which files and directories to exclude from the wheel.

        :stability: experimental
        :schema: BuildBackendSettings
        '''
        if isinstance(data, dict):
            data = WheelDataIncludes(**data)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8edb4b678376787a735855010994c917f5562ec1c18ac7700c5f21373aa27eb)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument default_excludes", value=default_excludes, expected_type=type_hints["default_excludes"])
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument module_root", value=module_root, expected_type=type_hints["module_root"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument source_exclude", value=source_exclude, expected_type=type_hints["source_exclude"])
            check_type(argname="argument source_include", value=source_include, expected_type=type_hints["source_include"])
            check_type(argname="argument wheel_exclude", value=wheel_exclude, expected_type=type_hints["wheel_exclude"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data
        if default_excludes is not None:
            self._values["default_excludes"] = default_excludes
        if module_name is not None:
            self._values["module_name"] = module_name
        if module_root is not None:
            self._values["module_root"] = module_root
        if namespace is not None:
            self._values["namespace"] = namespace
        if source_exclude is not None:
            self._values["source_exclude"] = source_exclude
        if source_include is not None:
            self._values["source_include"] = source_include
        if wheel_exclude is not None:
            self._values["wheel_exclude"] = wheel_exclude

    @builtins.property
    def data(self) -> typing.Optional["WheelDataIncludes"]:
        '''(experimental) Data includes for wheels.

        Each entry is a directory, whose contents are copied to the matching directory in the wheel
        in ``<name>-<version>.data/(purelib|platlib|headers|scripts|data)``. Upon installation, this
        data is moved to its target location, as defined by
        `https://docs.python.org/3.12/library/sysconfig.html#installation-paths <https://docs.python.org/3.12/library/sysconfig.html#installation-paths>`_. Usually, small
        data files are included by placing them in the Python module instead of using data includes.

        - ``scripts``: Installed to the directory for executables, ``<venv>/bin`` on Unix or
          ``<venv>\\Scripts`` on Windows. This directory is added to ``PATH`` when the virtual
          environment  is activated or when using ``uv run``, so this data type can be used to install
          additional binaries. Consider using ``project.scripts`` instead for Python entrypoints.
        - ``data``: Installed over the virtualenv environment root.

        Warning: This may override existing files!

        - ``headers``: Installed to the include directory. Compilers building Python packages
          with this package as build requirement use the include directory to find additional header
          files.
        - ``purelib`` and ``platlib``: Installed to the ``site-packages`` directory. It is not recommended
          to use these two options.

        :stability: experimental
        :schema: BuildBackendSettings#data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional["WheelDataIncludes"], result)

    @builtins.property
    def default_excludes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to ``false``, the default excludes aren't applied.

        Default excludes: ``__pycache__``, ``*.pyc``, and ``*.pyo``.

        :stability: experimental
        :schema: BuildBackendSettings#default-excludes
        '''
        result = self._values.get("default_excludes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def module_name(self) -> typing.Any:
        '''(experimental) The name of the module directory inside ``module-root``.

        The default module name is the package name with dots and dashes replaced by underscores.

        Package names need to be valid Python identifiers, and the directory needs to contain a
        ``__init__.py``. An exception are stubs packages, whose name ends with ``-stubs``, with the stem
        being the module name, and which contain a ``__init__.pyi`` file.

        For namespace packages with a single module, the path can be dotted, e.g., ``foo.bar`` or
        ``foo-stubs.bar``.

        For namespace packages with multiple modules, the path can be a list, e.g.,
        ``["foo", "bar"]``. We recommend using a single module per package, splitting multiple
        packages into a workspace.

        Note that using this option runs the risk of creating two packages with different names but
        the same module names. Installing such packages together leads to unspecified behavior,
        often with corrupted files or directory trees.

        :stability: experimental
        :schema: BuildBackendSettings#module-name
        '''
        result = self._values.get("module_name")
        return typing.cast(typing.Any, result)

    @builtins.property
    def module_root(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory that contains the module directory.

        Common values are ``src`` (src layout, the default) or an empty path (flat layout).

        :stability: experimental
        :schema: BuildBackendSettings#module-root
        '''
        result = self._values.get("module_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Build a namespace package.

        Build a PEP 420 implicit namespace package, allowing more than one root ``__init__.py``.

        Use this option when the namespace package contains multiple root ``__init__.py``, for
        namespace packages with a single root ``__init__.py`` use a dotted ``module-name`` instead.

        To compare dotted ``module-name`` and ``namespace = true``, the first example below can be
        expressed with ``module-name = "cloud.database"``: There is one root ``__init__.py`` ``database``.
        In the second example, we have three roots (``cloud.database``, ``cloud.database_pro``,
        ``billing.modules.database_pro``), so ``namespace = true`` is required::

           src
           └── cloud
           └── database
           ├── __init__.py
           ├── query_builder
           │   └── __init__.py
           └── sql
           ├── parser.py
           └── __init__.py

        Example::

           src
           ├── cloud
           │   ├── database
           │   │   ├── __init__.py
           │   │   ├── query_builder
           │   │   │   └── __init__.py
           │   │   └── sql
           │   │       ├── __init__.py
           │   │       └── parser.py
           │   └── database_pro
           │       ├── __init__.py
           │       └── query_builder.py
           └── billing
           └── modules
           └── database_pro
           ├── __init__.py
           └── sql.py

        :stability: experimental
        :schema: BuildBackendSettings#namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob expressions which files and directories to exclude from the source distribution.

        :stability: experimental
        :schema: BuildBackendSettings#source-exclude
        '''
        result = self._values.get("source_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob expressions which files and directories to additionally include in the source distribution.

        ``pyproject.toml`` and the contents of the module directory are always included.

        :stability: experimental
        :schema: BuildBackendSettings#source-include
        '''
        result = self._values.get("source_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wheel_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob expressions which files and directories to exclude from the wheel.

        :stability: experimental
        :schema: BuildBackendSettings#wheel-exclude
        '''
        result = self._values.get("wheel_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildBackendSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.python.uvConfig.DependencyGroupSettings",
    jsii_struct_bases=[],
    name_mapping={"requires_python": "requiresPython"},
)
class DependencyGroupSettings:
    def __init__(
        self,
        *,
        requires_python: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param requires_python: (experimental) Version of python to require when installing this group.

        :stability: experimental
        :schema: DependencyGroupSettings
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd491f584ee7212fb2c3697548f60d044362ecd866f97a41a269a2f581e15d60)
            check_type(argname="argument requires_python", value=requires_python, expected_type=type_hints["requires_python"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if requires_python is not None:
            self._values["requires_python"] = requires_python

    @builtins.property
    def requires_python(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of python to require when installing this group.

        :stability: experimental
        :schema: DependencyGroupSettings#requires-python
        '''
        result = self._values.get("requires_python")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DependencyGroupSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.python.uvConfig.ForkStrategy")
class ForkStrategy(enum.Enum):
    '''
    :stability: experimental
    :schema: ForkStrategy
    '''

    FEWEST = "FEWEST"
    '''(experimental) Optimize for selecting the fewest number of versions for each package.

    Older versions may
    be preferred if they are compatible with a wider range of supported Python versions or
    platforms. (fewest)

    :stability: experimental
    '''
    REQUIRES_HYPHEN_PYTHON = "REQUIRES_HYPHEN_PYTHON"
    '''(experimental) Optimize for selecting latest supported version of each package, for each supported Python version.

    (requires-python)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.Index",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "authenticate": "authenticate",
        "cache_control": "cacheControl",
        "default": "default",
        "explicit": "explicit",
        "format": "format",
        "ignore_error_codes": "ignoreErrorCodes",
        "name": "name",
        "publish_url": "publishUrl",
    },
)
class Index:
    def __init__(
        self,
        *,
        url: builtins.str,
        authenticate: typing.Optional["AuthPolicy"] = None,
        cache_control: typing.Optional[typing.Union["IndexCacheControl", typing.Dict[builtins.str, typing.Any]]] = None,
        default: typing.Optional[builtins.bool] = None,
        explicit: typing.Optional[builtins.bool] = None,
        format: typing.Optional["IndexFormat"] = None,
        ignore_error_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        name: typing.Optional[builtins.str] = None,
        publish_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: (experimental) The URL of the index. Expects to receive a URL (e.g., ``https://pypi.org/simple``) or a local path.
        :param authenticate: (experimental) When uv should use authentication for requests to the index. Example:: [[tool.uv.index]] name = "my-index" url = "https://<omitted>/simple" authenticate = "always"
        :param cache_control: (experimental) Cache control configuration for this index. When set, these headers will override the server's cache control headers for both package metadata requests and artifact downloads:: [[tool.uv.index]] name = "my-index" url = "https://<omitted>/simple" cache-control = { api = "max-age=600", files = "max-age=3600" }
        :param default: (experimental) Mark the index as the default index. By default, uv uses PyPI as the default index, such that even if additional indexes are defined via ``[[tool.uv.index]]``, PyPI will still be used as a fallback for packages that aren't found elsewhere. To disable the PyPI default, set ``default = true`` on at least one other index. Marking an index as default will move it to the front of the list of indexes, such that it is given the highest priority when resolving packages.
        :param explicit: (experimental) Mark the index as explicit. Explicit indexes will *only* be used when explicitly requested via a ``[tool.uv.sources]`` definition, as in:: [[tool.uv.index]] name = "pytorch" url = "https://download.pytorch.org/whl/cu121" explicit = true [tool.uv.sources] torch = { index = "pytorch" }
        :param format: (experimental) The format used by the index. Indexes can either be PEP 503-compliant (i.e., a PyPI-style registry implementing the Simple API) or structured as a flat list of distributions (e.g., ``--find-links``). In both cases, indexes can point to either local or remote resources.
        :param ignore_error_codes: (experimental) Status codes that uv should ignore when deciding whether to continue searching in the next index after a failure. Example:: [[tool.uv.index]] name = "my-index" url = "https://<omitted>/simple" ignore-error-codes = [401, 403]
        :param name: (experimental) The name of the index. Index names can be used to reference indexes elsewhere in the configuration. For example, you can pin a package to a specific index by name:: [[tool.uv.index]] name = "pytorch" url = "https://download.pytorch.org/whl/cu121" [tool.uv.sources] torch = { index = "pytorch" }
        :param publish_url: (experimental) The URL of the upload endpoint. When using ``uv publish --index <name>``, this URL is used for publishing. A configuration for the default index PyPI would look as follows:: [[tool.uv.index]] name = "pypi" url = "https://pypi.org/simple" publish-url = "https://upload.pypi.org/legacy/"

        :stability: experimental
        :schema: Index
        '''
        if isinstance(cache_control, dict):
            cache_control = IndexCacheControl(**cache_control)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075e56d66f36a514ad1fafdc5b03260161a84fb1d2c5ce8069204ee4b239111d)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument authenticate", value=authenticate, expected_type=type_hints["authenticate"])
            check_type(argname="argument cache_control", value=cache_control, expected_type=type_hints["cache_control"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument explicit", value=explicit, expected_type=type_hints["explicit"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument ignore_error_codes", value=ignore_error_codes, expected_type=type_hints["ignore_error_codes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publish_url", value=publish_url, expected_type=type_hints["publish_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if authenticate is not None:
            self._values["authenticate"] = authenticate
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if default is not None:
            self._values["default"] = default
        if explicit is not None:
            self._values["explicit"] = explicit
        if format is not None:
            self._values["format"] = format
        if ignore_error_codes is not None:
            self._values["ignore_error_codes"] = ignore_error_codes
        if name is not None:
            self._values["name"] = name
        if publish_url is not None:
            self._values["publish_url"] = publish_url

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The URL of the index.

        Expects to receive a URL (e.g., ``https://pypi.org/simple``) or a local path.

        :stability: experimental
        :schema: Index#url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authenticate(self) -> typing.Optional["AuthPolicy"]:
        '''(experimental) When uv should use authentication for requests to the index.

        Example::

           [[tool.uv.index]]
           name = "my-index"
           url = "https://<omitted>/simple"
           authenticate = "always"

        :stability: experimental
        :schema: Index#authenticate
        '''
        result = self._values.get("authenticate")
        return typing.cast(typing.Optional["AuthPolicy"], result)

    @builtins.property
    def cache_control(self) -> typing.Optional["IndexCacheControl"]:
        '''(experimental) Cache control configuration for this index.

        When set, these headers will override the server's cache control headers
        for both package metadata requests and artifact downloads::

           [[tool.uv.index]]
           name = "my-index"
           url = "https://<omitted>/simple"
           cache-control = { api = "max-age=600", files = "max-age=3600" }

        :stability: experimental
        :schema: Index#cache-control
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional["IndexCacheControl"], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Mark the index as the default index.

        By default, uv uses PyPI as the default index, such that even if additional indexes are
        defined via ``[[tool.uv.index]]``, PyPI will still be used as a fallback for packages that
        aren't found elsewhere. To disable the PyPI default, set ``default = true`` on at least one
        other index.

        Marking an index as default will move it to the front of the list of indexes, such that it
        is given the highest priority when resolving packages.

        :stability: experimental
        :schema: Index#default
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def explicit(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Mark the index as explicit.

        Explicit indexes will *only* be used when explicitly requested via a ``[tool.uv.sources]``
        definition, as in::

           [[tool.uv.index]]
           name = "pytorch"
           url = "https://download.pytorch.org/whl/cu121"
           explicit = true

           [tool.uv.sources]
           torch = { index = "pytorch" }

        :stability: experimental
        :schema: Index#explicit
        '''
        result = self._values.get("explicit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format(self) -> typing.Optional["IndexFormat"]:
        '''(experimental) The format used by the index.

        Indexes can either be PEP 503-compliant (i.e., a PyPI-style registry implementing the Simple
        API) or structured as a flat list of distributions (e.g., ``--find-links``). In both cases,
        indexes can point to either local or remote resources.

        :stability: experimental
        :schema: Index#format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["IndexFormat"], result)

    @builtins.property
    def ignore_error_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) Status codes that uv should ignore when deciding whether to continue searching in the next index after a failure.

        Example::

           [[tool.uv.index]]
           name = "my-index"
           url = "https://<omitted>/simple"
           ignore-error-codes = [401, 403]

        :stability: experimental
        :schema: Index#ignore-error-codes
        '''
        result = self._values.get("ignore_error_codes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the index.

        Index names can be used to reference indexes elsewhere in the configuration. For example,
        you can pin a package to a specific index by name::

           [[tool.uv.index]]
           name = "pytorch"
           url = "https://download.pytorch.org/whl/cu121"

           [tool.uv.sources]
           torch = { index = "pytorch" }

        :stability: experimental
        :schema: Index#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL of the upload endpoint.

        When using ``uv publish --index <name>``, this URL is used for publishing.

        A configuration for the default index PyPI would look as follows::

           [[tool.uv.index]]
           name = "pypi"
           url = "https://pypi.org/simple"
           publish-url = "https://upload.pypi.org/legacy/"

        :stability: experimental
        :schema: Index#publish-url
        '''
        result = self._values.get("publish_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Index(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.python.uvConfig.IndexCacheControl",
    jsii_struct_bases=[],
    name_mapping={"api": "api", "files": "files"},
)
class IndexCacheControl:
    def __init__(
        self,
        *,
        api: typing.Optional[builtins.str] = None,
        files: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Cache control configuration for an index.

        :param api: (experimental) Cache control header for Simple API requests.
        :param files: (experimental) Cache control header for file downloads.

        :stability: experimental
        :schema: IndexCacheControl
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadc80a7c1e7527e1cc3946322c9b1d4206a4fd507f1046ab1298219615cd172)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api is not None:
            self._values["api"] = api
        if files is not None:
            self._values["files"] = files

    @builtins.property
    def api(self) -> typing.Optional[builtins.str]:
        '''(experimental) Cache control header for Simple API requests.

        :stability: experimental
        :schema: IndexCacheControl#api
        '''
        result = self._values.get("api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def files(self) -> typing.Optional[builtins.str]:
        '''(experimental) Cache control header for file downloads.

        :stability: experimental
        :schema: IndexCacheControl#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IndexCacheControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.python.uvConfig.IndexFormat")
class IndexFormat(enum.Enum):
    '''
    :stability: experimental
    :schema: IndexFormat
    '''

    SIMPLE = "SIMPLE"
    '''(experimental) A PyPI-style index implementing the Simple Repository API.

    (simple)

    :stability: experimental
    '''
    FLAT = "FLAT"
    '''(experimental) A ``--find-links``-style index containing a flat list of wheels and source distributions.

    (flat)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.IndexStrategy")
class IndexStrategy(enum.Enum):
    '''
    :stability: experimental
    :schema: IndexStrategy
    '''

    FIRST_HYPHEN_INDEX = "FIRST_HYPHEN_INDEX"
    '''(experimental) Only use results from the first index that returns a match for a given package name.

    While this differs from pip's behavior, it's the default index strategy as it's the most
    secure. (first-index)

    :stability: experimental
    '''
    UNSAFE_HYPHEN_FIRST_HYPHEN_MATCH = "UNSAFE_HYPHEN_FIRST_HYPHEN_MATCH"
    '''(experimental) Search for every package name across all indexes, exhausting the versions from the first index before moving on to the next.

    In this strategy, we look for every package across all indexes. When resolving, we attempt
    to use versions from the indexes in order, such that we exhaust all available versions from
    the first index before moving on to the next. Further, if a version is found to be
    incompatible in the first index, we do not reconsider that version in subsequent indexes,
    even if the secondary index might contain compatible versions (e.g., variants of the same
    versions with different ABI tags or Python version constraints).

    See: `https://peps.python.org/pep-0708/ <https://peps.python.org/pep-0708/>`_ (unsafe-first-match)

    :stability: experimental
    '''
    UNSAFE_HYPHEN_BEST_HYPHEN_MATCH = "UNSAFE_HYPHEN_BEST_HYPHEN_MATCH"
    '''(experimental) Search for every package name across all indexes, preferring the "best" version found.

    If a
    package version is in multiple indexes, only look at the entry for the first index.

    In this strategy, we look for every package across all indexes. When resolving, we consider
    all versions from all indexes, choosing the "best" version found (typically, the highest
    compatible version).

    This most closely matches pip's behavior, but exposes the resolver to "dependency confusion"
    attacks whereby malicious actors can publish packages to public indexes with the same name
    as internal packages, causing the resolver to install the malicious package in lieu of
    the intended internal package.

    See: `https://peps.python.org/pep-0708/ <https://peps.python.org/pep-0708/>`_ (unsafe-best-match)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.KeyringProviderType")
class KeyringProviderType(enum.Enum):
    '''(experimental) Keyring provider type to use for credential lookup.

    :stability: experimental
    :schema: KeyringProviderType
    '''

    DISABLED = "DISABLED"
    '''(experimental) Do not use keyring for credential lookup.

    (disabled)

    :stability: experimental
    '''
    SUBPROCESS = "SUBPROCESS"
    '''(experimental) Use the ``keyring`` command for credential lookup.

    (subprocess)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.LinkMode")
class LinkMode(enum.Enum):
    '''
    :stability: experimental
    :schema: LinkMode
    '''

    CLONE = "CLONE"
    '''(experimental) Clone (i.e., copy-on-write) packages from the wheel into the ``site-packages`` directory. (clone).

    :stability: experimental
    '''
    COPY = "COPY"
    '''(experimental) Copy packages from the wheel into the ``site-packages`` directory.

    (copy)

    :stability: experimental
    '''
    HARDLINK = "HARDLINK"
    '''(experimental) Hard link packages from the wheel into the ``site-packages`` directory.

    (hardlink)

    :stability: experimental
    '''
    SYMLINK = "SYMLINK"
    '''(experimental) Symbolically link packages from the wheel into the ``site-packages`` directory.

    (symlink)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.PipGroupName",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path"},
)
class PipGroupName:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The pip-compatible variant of a [``GroupName``].

        Either  or :.
        If  is omitted it defaults to "pyproject.toml".

        :param name: 
        :param path: 

        :stability: experimental
        :schema: PipGroupName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61408a230f83617e8924d0c29339bd155df27bf401eeae828f9b19222e91953d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        :schema: PipGroupName#name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: PipGroupName#path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipGroupName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.python.uvConfig.PipOptions",
    jsii_struct_bases=[],
    name_mapping={
        "all_extras": "allExtras",
        "allow_empty_requirements": "allowEmptyRequirements",
        "annotation_style": "annotationStyle",
        "break_system_packages": "breakSystemPackages",
        "compile_bytecode": "compileBytecode",
        "config_settings": "configSettings",
        "config_settings_package": "configSettingsPackage",
        "custom_compile_command": "customCompileCommand",
        "dependency_metadata": "dependencyMetadata",
        "emit_build_options": "emitBuildOptions",
        "emit_find_links": "emitFindLinks",
        "emit_index_annotation": "emitIndexAnnotation",
        "emit_index_url": "emitIndexUrl",
        "emit_marker_expression": "emitMarkerExpression",
        "exclude_newer": "excludeNewer",
        "exclude_newer_package": "excludeNewerPackage",
        "extra": "extra",
        "extra_build_dependencies": "extraBuildDependencies",
        "extra_build_variables": "extraBuildVariables",
        "extra_index_url": "extraIndexUrl",
        "find_links": "findLinks",
        "fork_strategy": "forkStrategy",
        "generate_hashes": "generateHashes",
        "group": "group",
        "index_strategy": "indexStrategy",
        "index_url": "indexUrl",
        "keyring_provider": "keyringProvider",
        "link_mode": "linkMode",
        "no_annotate": "noAnnotate",
        "no_binary": "noBinary",
        "no_build": "noBuild",
        "no_build_isolation": "noBuildIsolation",
        "no_build_isolation_package": "noBuildIsolationPackage",
        "no_deps": "noDeps",
        "no_emit_package": "noEmitPackage",
        "no_extra": "noExtra",
        "no_header": "noHeader",
        "no_index": "noIndex",
        "no_sources": "noSources",
        "no_strip_extras": "noStripExtras",
        "no_strip_markers": "noStripMarkers",
        "only_binary": "onlyBinary",
        "output_file": "outputFile",
        "prefix": "prefix",
        "prerelease": "prerelease",
        "python": "python",
        "python_platform": "pythonPlatform",
        "python_version": "pythonVersion",
        "reinstall": "reinstall",
        "reinstall_package": "reinstallPackage",
        "require_hashes": "requireHashes",
        "resolution": "resolution",
        "strict": "strict",
        "system": "system",
        "target": "target",
        "torch_backend": "torchBackend",
        "universal": "universal",
        "upgrade": "upgrade",
        "upgrade_package": "upgradePackage",
        "verify_hashes": "verifyHashes",
    },
)
class PipOptions:
    def __init__(
        self,
        *,
        all_extras: typing.Optional[builtins.bool] = None,
        allow_empty_requirements: typing.Optional[builtins.bool] = None,
        annotation_style: typing.Optional["AnnotationStyle"] = None,
        break_system_packages: typing.Optional[builtins.bool] = None,
        compile_bytecode: typing.Optional[builtins.bool] = None,
        config_settings: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        config_settings_package: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]] = None,
        custom_compile_command: typing.Optional[builtins.str] = None,
        dependency_metadata: typing.Optional[typing.Sequence[typing.Union["StaticMetadata", typing.Dict[builtins.str, typing.Any]]]] = None,
        emit_build_options: typing.Optional[builtins.bool] = None,
        emit_find_links: typing.Optional[builtins.bool] = None,
        emit_index_annotation: typing.Optional[builtins.bool] = None,
        emit_index_url: typing.Optional[builtins.bool] = None,
        emit_marker_expression: typing.Optional[builtins.bool] = None,
        exclude_newer: typing.Optional[builtins.str] = None,
        exclude_newer_package: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        extra_build_dependencies: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
        extra_build_variables: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
        extra_index_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        find_links: typing.Optional[typing.Sequence[builtins.str]] = None,
        fork_strategy: typing.Optional["ForkStrategy"] = None,
        generate_hashes: typing.Optional[builtins.bool] = None,
        group: typing.Optional[typing.Sequence[typing.Union["PipGroupName", typing.Dict[builtins.str, typing.Any]]]] = None,
        index_strategy: typing.Optional["IndexStrategy"] = None,
        index_url: typing.Optional[builtins.str] = None,
        keyring_provider: typing.Optional["KeyringProviderType"] = None,
        link_mode: typing.Optional["LinkMode"] = None,
        no_annotate: typing.Optional[builtins.bool] = None,
        no_binary: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_build: typing.Optional[builtins.bool] = None,
        no_build_isolation: typing.Optional[builtins.bool] = None,
        no_build_isolation_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_deps: typing.Optional[builtins.bool] = None,
        no_emit_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_header: typing.Optional[builtins.bool] = None,
        no_index: typing.Optional[builtins.bool] = None,
        no_sources: typing.Optional[builtins.bool] = None,
        no_strip_extras: typing.Optional[builtins.bool] = None,
        no_strip_markers: typing.Optional[builtins.bool] = None,
        only_binary: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_file: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        prerelease: typing.Optional["PrereleaseMode"] = None,
        python: typing.Optional[builtins.str] = None,
        python_platform: typing.Optional["TargetTriple"] = None,
        python_version: typing.Optional[builtins.str] = None,
        reinstall: typing.Optional[builtins.bool] = None,
        reinstall_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        require_hashes: typing.Optional[builtins.bool] = None,
        resolution: typing.Optional["ResolutionMode"] = None,
        strict: typing.Optional[builtins.bool] = None,
        system: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        torch_backend: typing.Optional["TorchMode"] = None,
        universal: typing.Optional[builtins.bool] = None,
        upgrade: typing.Optional[builtins.bool] = None,
        upgrade_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify_hashes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Settings that are specific to the ``uv pip`` command-line interface.

        These values will be ignored when running commands outside the ``uv pip`` namespace (e.g.,
        ``uv lock``, ``uvx``).

        :param all_extras: (experimental) Include all optional dependencies. Only applies to ``pyproject.toml``, ``setup.py``, and ``setup.cfg`` sources.
        :param allow_empty_requirements: (experimental) Allow ``uv pip sync`` with empty requirements, which will clear the environment of all packages.
        :param annotation_style: (experimental) The style of the annotation comments included in the output file, used to indicate the source of each package.
        :param break_system_packages: (experimental) Allow uv to modify an ``EXTERNALLY-MANAGED`` Python installation. WARNING: ``--break-system-packages`` is intended for use in continuous integration (CI) environments, when installing into Python installations that are managed by an external package manager, like ``apt``. It should be used with caution, as such Python installations explicitly recommend against modifications by other package managers (like uv or pip).
        :param compile_bytecode: (experimental) Compile Python files to bytecode after installation. By default, uv does not compile Python (``.py``) files to bytecode (``__pycache__/*.pyc``); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times. When enabled, uv will process the entire site-packages directory (including packages that are not being modified by the current operation) for consistency. Like pip, it will also ignore errors.
        :param config_settings: (experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend, specified as ``KEY=VALUE`` pairs.
        :param config_settings_package: (experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend for specific packages, specified as ``KEY=VALUE`` pairs.
        :param custom_compile_command: (experimental) The header comment to include at the top of the output file generated by ``uv pip compile``. Used to reflect custom build scripts and commands that wrap ``uv pip compile``.
        :param dependency_metadata: (experimental) Pre-defined static metadata for dependencies of the project (direct or transitive). When provided, enables the resolver to use the specified metadata instead of querying the registry or building the relevant package from source. Metadata should be provided in adherence with the `Metadata 2.3 <https://packaging.python.org/en/latest/specifications/core-metadata/>`_ standard, though only the following fields are respected: - ``name``: The name of the package. - (Optional) ``version``: The version of the package. If omitted, the metadata will be applied to all versions of the package. - (Optional) ``requires-dist``: The dependencies of the package (e.g., ``werkzeug>=0.14``). - (Optional) ``requires-python``: The Python version required by the package (e.g., ``>=3.10``). - (Optional) ``provides-extra``: The extras provided by the package.
        :param emit_build_options: (experimental) Include ``--no-binary`` and ``--only-binary`` entries in the output file generated by ``uv pip compile``.
        :param emit_find_links: (experimental) Include ``--find-links`` entries in the output file generated by ``uv pip compile``.
        :param emit_index_annotation: (experimental) Include comment annotations indicating the index used to resolve each package (e.g., ``# from https://pypi.org/simple``).
        :param emit_index_url: (experimental) Include ``--index-url`` and ``--extra-index-url`` entries in the output file generated by ``uv pip compile``.
        :param emit_marker_expression: (experimental) Whether to emit a marker string indicating the conditions under which the set of pinned dependencies is valid. The pinned dependencies may be valid even when the marker expression is false, but when the expression is true, the requirements are known to be correct.
        :param exclude_newer: (experimental) Limit candidate packages to those that were uploaded prior to a given point in time. Accepts a superset of `RFC 3339 <https://www.rfc-editor.org/rfc/rfc3339.html>`_ (e.g., ``2006-12-02T02:07:43Z``). A full timestamp is required to ensure that the resolver will behave consistently across timezones.
        :param exclude_newer_package: (experimental) Limit candidate packages for specific packages to those that were uploaded prior to the given date. Accepts package-date pairs in a dictionary format.
        :param extra: (experimental) Include optional dependencies from the specified extra; may be provided more than once. Only applies to ``pyproject.toml``, ``setup.py``, and ``setup.cfg`` sources.
        :param extra_build_dependencies: (experimental) Additional build dependencies for packages. This allows extending the PEP 517 build environment for the project's dependencies with additional packages. This is useful for packages that assume the presence of packages like ``pip``, and do not declare them as build dependencies.
        :param extra_build_variables: (experimental) Extra environment variables to set when building certain packages. Environment variables will be added to the environment when building the specified packages.
        :param extra_index_url: (experimental) Extra URLs of package indexes to use, in addition to ``--index-url``. Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_ (the simple repository API), or a local directory laid out in the same format. All indexes provided via this flag take priority over the index specified by ```index_url`` <#index-url>`_. When multiple indexes are provided, earlier values take priority. To control uv's resolution strategy when multiple indexes are present, see ```index_strategy`` <#index-strategy>`_.
        :param find_links: (experimental) Locations to search for candidate distributions, in addition to those found in the registry indexes. If a path, the target must be a directory that contains packages as wheel files (``.whl``) or source distributions (e.g., ``.tar.gz`` or ``.zip``) at the top level. If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
        :param fork_strategy: (experimental) The strategy to use when selecting multiple versions of a given package across Python versions and platforms. By default, uv will optimize for selecting the latest version of each package for each supported Python version (``requires-python``), while minimizing the number of selected versions across platforms. Under ``fewest``, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
        :param generate_hashes: (experimental) Include distribution hashes in the output file.
        :param group: (experimental) Include the following dependency groups.
        :param index_strategy: (experimental) The strategy to use when resolving against multiple index URLs. By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (``first-index``). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
        :param index_url: (experimental) The URL of the Python package index (by default: `https://pypi.org/simple <https://pypi.org/simple>`_). Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_ (the simple repository API), or a local directory laid out in the same format. The index provided by this setting is given lower priority than any indexes specified via ```extra_index_url`` <#extra-index-url>`_.
        :param keyring_provider: (experimental) Attempt to use ``keyring`` for authentication for index URLs. At present, only ``--keyring-provider subprocess`` is supported, which configures uv to use the ``keyring`` CLI to handle authentication.
        :param link_mode: (experimental) The method to use when installing packages from the global cache. Defaults to ``clone`` (also known as Copy-on-Write) on macOS, and ``hardlink`` on Linux and Windows. WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (``uv cache clean``) will break all installed packages by way of removing the underlying source files. Use symlinks with caution. Default: clone``(also known as Copy-on-Write) on macOS, and``hardlink` on Linux and
        :param no_annotate: (experimental) Exclude comment annotations indicating the source of each package from the output file generated by ``uv pip compile``.
        :param no_binary: (experimental) Don't install pre-built wheels. The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available. Multiple packages may be provided. Disable binaries for all packages with ``:all:``. Clear previously specified packages with ``:none:``.
        :param no_build: (experimental) Don't build source distributions. When enabled, resolving will not run arbitrary Python code. The cached wheels of already-built source distributions will be reused, but operations that require building distributions will exit with an error. Alias for ``--only-binary :all:``.
        :param no_build_isolation: (experimental) Disable isolation when building source distributions. Assumes that build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_ are already installed.
        :param no_build_isolation_package: (experimental) Disable isolation when building source distributions for a specific package. Assumes that the packages' build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_ are already installed.
        :param no_deps: (experimental) Ignore package dependencies, instead only add those packages explicitly listed on the command line to the resulting requirements file.
        :param no_emit_package: (experimental) Specify a package to omit from the output resolution. Its dependencies will still be included in the resolution. Equivalent to pip-compile's ``--unsafe-package`` option.
        :param no_extra: (experimental) Exclude the specified optional dependencies if ``all-extras`` is supplied.
        :param no_header: (experimental) Exclude the comment header at the top of output file generated by ``uv pip compile``.
        :param no_index: (experimental) Ignore all registry indexes (e.g., PyPI), instead relying on direct URL dependencies and those provided via ``--find-links``.
        :param no_sources: (experimental) Ignore the ``tool.uv.sources`` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any local or Git sources.
        :param no_strip_extras: (experimental) Include extras in the output file. By default, uv strips extras, as any packages pulled in by the extras are already included as dependencies in the output file directly. Further, output files generated with ``--no-strip-extras`` cannot be used as constraints files in ``install`` and ``sync`` invocations.
        :param no_strip_markers: (experimental) Include environment markers in the output file generated by ``uv pip compile``. By default, uv strips environment markers, as the resolution generated by ``compile`` is only guaranteed to be correct for the target environment.
        :param only_binary: (experimental) Only use pre-built wheels; don't build source distributions. When enabled, resolving will not run code from the given packages. The cached wheels of already-built source distributions will be reused, but operations that require building distributions will exit with an error. Multiple packages may be provided. Disable binaries for all packages with ``:all:``. Clear previously specified packages with ``:none:``.
        :param output_file: (experimental) Write the requirements generated by ``uv pip compile`` to the given ``requirements.txt`` file. If the file already exists, the existing versions will be preferred when resolving dependencies, unless ``--upgrade`` is also specified.
        :param prefix: (experimental) Install packages into ``lib``, ``bin``, and other top-level folders under the specified directory, as if a virtual environment were present at that location. In general, prefer the use of ``--python`` to install into an alternate environment, as scripts and other artifacts installed via ``--prefix`` will reference the installing interpreter, rather than any interpreter added to the ``--prefix`` directory, rendering them non-portable.
        :param prerelease: (experimental) The strategy to use when considering pre-release versions. By default, uv will accept pre-releases for packages that *only* publish pre-releases, along with first-party requirements that contain an explicit pre-release marker in the declared specifiers (``if-necessary-or-explicit``).
        :param python: (experimental) The Python interpreter into which packages should be installed. By default, uv installs into the virtual environment in the current working directory or any parent directory. The ``--python`` option allows you to specify a different interpreter, which is intended for use in continuous integration (CI) environments or other automated workflows. Supported formats: - ``3.10`` looks for an installed Python 3.10 in the registry on Windows (see ``py --list-paths``), or ``python3.10`` on Linux and macOS. - ``python3.10`` or ``python.exe`` looks for a binary with the given name in ``PATH``. - ``/home/ferris/.local/bin/python3.10`` uses the exact Python at the given path.
        :param python_platform: (experimental) The platform for which requirements should be resolved. Represented as a "target triple", a string that describes the target platform in terms of its CPU, vendor, and operating system name, like ``x86_64-unknown-linux-gnu`` or ``aarch64-apple-darwin``.
        :param python_version: (experimental) The minimum Python version that should be supported by the resolved requirements (e.g., ``3.8`` or ``3.8.17``). If a patch version is omitted, the minimum patch version is assumed. For example, ``3.8`` is mapped to ``3.8.0``.
        :param reinstall: (experimental) Reinstall all packages, regardless of whether they're already installed. Implies ``refresh``.
        :param reinstall_package: (experimental) Reinstall a specific package, regardless of whether it's already installed. Implies ``refresh-package``.
        :param require_hashes: (experimental) Require a matching hash for each requirement. Hash-checking mode is all or nothing. If enabled, *all* requirements must be provided with a corresponding hash or set of hashes. Additionally, if enabled, *all* requirements must either be pinned to exact versions (e.g., ``==1.0.0``), or be specified via direct URL. Hash-checking mode introduces a number of additional constraints: - Git dependencies are not supported. - Editable installations are not supported. - Local dependencies are not supported, unless they point to a specific wheel (``.whl``) or source archive (``.zip``, ``.tar.gz``), as opposed to a directory.
        :param resolution: (experimental) The strategy to use when selecting between the different compatible versions for a given package requirement. By default, uv will use the latest compatible version of each package (``highest``).
        :param strict: (experimental) Validate the Python environment, to detect packages with missing dependencies and other issues.
        :param system: (experimental) Install packages into the system Python environment. By default, uv installs into the virtual environment in the current working directory or any parent directory. The ``--system`` option instructs uv to instead use the first Python found in the system ``PATH``. WARNING: ``--system`` is intended for use in continuous integration (CI) environments and should be used with caution, as it can modify the system Python installation.
        :param target: (experimental) Install packages into the specified directory, rather than into the virtual or system Python environment. The packages will be installed at the top-level of the directory.
        :param torch_backend: (experimental) The backend to use when fetching packages in the PyTorch ecosystem. When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem, and will instead use the defined backend. For example, when set to ``cpu``, uv will use the CPU-only PyTorch index; when set to ``cu126``, uv will use the PyTorch index for CUDA 12.6. The ``auto`` mode will attempt to detect the appropriate PyTorch index based on the currently installed CUDA drivers. This option is in preview and may change in any future release.
        :param universal: (experimental) Perform a universal resolution, attempting to generate a single ``requirements.txt`` output file that is compatible with all operating systems, architectures, and Python implementations. In universal mode, the current Python version (or user-provided ``--python-version``) will be treated as a lower bound. For example, ``--universal --python-version 3.7`` would produce a universal resolution for Python 3.7 and later.
        :param upgrade: (experimental) Allow package upgrades, ignoring pinned versions in any existing output file.
        :param upgrade_package: (experimental) Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Accepts both standalone package names (``ruff``) and version specifiers (``ruff<0.5.0``).
        :param verify_hashes: (experimental) Validate any hashes provided in the requirements file. Unlike ``--require-hashes``, ``--verify-hashes`` does not require that all requirements have hashes; instead, it will limit itself to verifying the hashes of those requirements that do include them.

        :stability: experimental
        :schema: PipOptions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945d6160c5542e9b39ed19c707a1b0e7ee5ea909cc55041a32f162098f3853e7)
            check_type(argname="argument all_extras", value=all_extras, expected_type=type_hints["all_extras"])
            check_type(argname="argument allow_empty_requirements", value=allow_empty_requirements, expected_type=type_hints["allow_empty_requirements"])
            check_type(argname="argument annotation_style", value=annotation_style, expected_type=type_hints["annotation_style"])
            check_type(argname="argument break_system_packages", value=break_system_packages, expected_type=type_hints["break_system_packages"])
            check_type(argname="argument compile_bytecode", value=compile_bytecode, expected_type=type_hints["compile_bytecode"])
            check_type(argname="argument config_settings", value=config_settings, expected_type=type_hints["config_settings"])
            check_type(argname="argument config_settings_package", value=config_settings_package, expected_type=type_hints["config_settings_package"])
            check_type(argname="argument custom_compile_command", value=custom_compile_command, expected_type=type_hints["custom_compile_command"])
            check_type(argname="argument dependency_metadata", value=dependency_metadata, expected_type=type_hints["dependency_metadata"])
            check_type(argname="argument emit_build_options", value=emit_build_options, expected_type=type_hints["emit_build_options"])
            check_type(argname="argument emit_find_links", value=emit_find_links, expected_type=type_hints["emit_find_links"])
            check_type(argname="argument emit_index_annotation", value=emit_index_annotation, expected_type=type_hints["emit_index_annotation"])
            check_type(argname="argument emit_index_url", value=emit_index_url, expected_type=type_hints["emit_index_url"])
            check_type(argname="argument emit_marker_expression", value=emit_marker_expression, expected_type=type_hints["emit_marker_expression"])
            check_type(argname="argument exclude_newer", value=exclude_newer, expected_type=type_hints["exclude_newer"])
            check_type(argname="argument exclude_newer_package", value=exclude_newer_package, expected_type=type_hints["exclude_newer_package"])
            check_type(argname="argument extra", value=extra, expected_type=type_hints["extra"])
            check_type(argname="argument extra_build_dependencies", value=extra_build_dependencies, expected_type=type_hints["extra_build_dependencies"])
            check_type(argname="argument extra_build_variables", value=extra_build_variables, expected_type=type_hints["extra_build_variables"])
            check_type(argname="argument extra_index_url", value=extra_index_url, expected_type=type_hints["extra_index_url"])
            check_type(argname="argument find_links", value=find_links, expected_type=type_hints["find_links"])
            check_type(argname="argument fork_strategy", value=fork_strategy, expected_type=type_hints["fork_strategy"])
            check_type(argname="argument generate_hashes", value=generate_hashes, expected_type=type_hints["generate_hashes"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument index_strategy", value=index_strategy, expected_type=type_hints["index_strategy"])
            check_type(argname="argument index_url", value=index_url, expected_type=type_hints["index_url"])
            check_type(argname="argument keyring_provider", value=keyring_provider, expected_type=type_hints["keyring_provider"])
            check_type(argname="argument link_mode", value=link_mode, expected_type=type_hints["link_mode"])
            check_type(argname="argument no_annotate", value=no_annotate, expected_type=type_hints["no_annotate"])
            check_type(argname="argument no_binary", value=no_binary, expected_type=type_hints["no_binary"])
            check_type(argname="argument no_build", value=no_build, expected_type=type_hints["no_build"])
            check_type(argname="argument no_build_isolation", value=no_build_isolation, expected_type=type_hints["no_build_isolation"])
            check_type(argname="argument no_build_isolation_package", value=no_build_isolation_package, expected_type=type_hints["no_build_isolation_package"])
            check_type(argname="argument no_deps", value=no_deps, expected_type=type_hints["no_deps"])
            check_type(argname="argument no_emit_package", value=no_emit_package, expected_type=type_hints["no_emit_package"])
            check_type(argname="argument no_extra", value=no_extra, expected_type=type_hints["no_extra"])
            check_type(argname="argument no_header", value=no_header, expected_type=type_hints["no_header"])
            check_type(argname="argument no_index", value=no_index, expected_type=type_hints["no_index"])
            check_type(argname="argument no_sources", value=no_sources, expected_type=type_hints["no_sources"])
            check_type(argname="argument no_strip_extras", value=no_strip_extras, expected_type=type_hints["no_strip_extras"])
            check_type(argname="argument no_strip_markers", value=no_strip_markers, expected_type=type_hints["no_strip_markers"])
            check_type(argname="argument only_binary", value=only_binary, expected_type=type_hints["only_binary"])
            check_type(argname="argument output_file", value=output_file, expected_type=type_hints["output_file"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument python", value=python, expected_type=type_hints["python"])
            check_type(argname="argument python_platform", value=python_platform, expected_type=type_hints["python_platform"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument reinstall", value=reinstall, expected_type=type_hints["reinstall"])
            check_type(argname="argument reinstall_package", value=reinstall_package, expected_type=type_hints["reinstall_package"])
            check_type(argname="argument require_hashes", value=require_hashes, expected_type=type_hints["require_hashes"])
            check_type(argname="argument resolution", value=resolution, expected_type=type_hints["resolution"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument system", value=system, expected_type=type_hints["system"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument torch_backend", value=torch_backend, expected_type=type_hints["torch_backend"])
            check_type(argname="argument universal", value=universal, expected_type=type_hints["universal"])
            check_type(argname="argument upgrade", value=upgrade, expected_type=type_hints["upgrade"])
            check_type(argname="argument upgrade_package", value=upgrade_package, expected_type=type_hints["upgrade_package"])
            check_type(argname="argument verify_hashes", value=verify_hashes, expected_type=type_hints["verify_hashes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_extras is not None:
            self._values["all_extras"] = all_extras
        if allow_empty_requirements is not None:
            self._values["allow_empty_requirements"] = allow_empty_requirements
        if annotation_style is not None:
            self._values["annotation_style"] = annotation_style
        if break_system_packages is not None:
            self._values["break_system_packages"] = break_system_packages
        if compile_bytecode is not None:
            self._values["compile_bytecode"] = compile_bytecode
        if config_settings is not None:
            self._values["config_settings"] = config_settings
        if config_settings_package is not None:
            self._values["config_settings_package"] = config_settings_package
        if custom_compile_command is not None:
            self._values["custom_compile_command"] = custom_compile_command
        if dependency_metadata is not None:
            self._values["dependency_metadata"] = dependency_metadata
        if emit_build_options is not None:
            self._values["emit_build_options"] = emit_build_options
        if emit_find_links is not None:
            self._values["emit_find_links"] = emit_find_links
        if emit_index_annotation is not None:
            self._values["emit_index_annotation"] = emit_index_annotation
        if emit_index_url is not None:
            self._values["emit_index_url"] = emit_index_url
        if emit_marker_expression is not None:
            self._values["emit_marker_expression"] = emit_marker_expression
        if exclude_newer is not None:
            self._values["exclude_newer"] = exclude_newer
        if exclude_newer_package is not None:
            self._values["exclude_newer_package"] = exclude_newer_package
        if extra is not None:
            self._values["extra"] = extra
        if extra_build_dependencies is not None:
            self._values["extra_build_dependencies"] = extra_build_dependencies
        if extra_build_variables is not None:
            self._values["extra_build_variables"] = extra_build_variables
        if extra_index_url is not None:
            self._values["extra_index_url"] = extra_index_url
        if find_links is not None:
            self._values["find_links"] = find_links
        if fork_strategy is not None:
            self._values["fork_strategy"] = fork_strategy
        if generate_hashes is not None:
            self._values["generate_hashes"] = generate_hashes
        if group is not None:
            self._values["group"] = group
        if index_strategy is not None:
            self._values["index_strategy"] = index_strategy
        if index_url is not None:
            self._values["index_url"] = index_url
        if keyring_provider is not None:
            self._values["keyring_provider"] = keyring_provider
        if link_mode is not None:
            self._values["link_mode"] = link_mode
        if no_annotate is not None:
            self._values["no_annotate"] = no_annotate
        if no_binary is not None:
            self._values["no_binary"] = no_binary
        if no_build is not None:
            self._values["no_build"] = no_build
        if no_build_isolation is not None:
            self._values["no_build_isolation"] = no_build_isolation
        if no_build_isolation_package is not None:
            self._values["no_build_isolation_package"] = no_build_isolation_package
        if no_deps is not None:
            self._values["no_deps"] = no_deps
        if no_emit_package is not None:
            self._values["no_emit_package"] = no_emit_package
        if no_extra is not None:
            self._values["no_extra"] = no_extra
        if no_header is not None:
            self._values["no_header"] = no_header
        if no_index is not None:
            self._values["no_index"] = no_index
        if no_sources is not None:
            self._values["no_sources"] = no_sources
        if no_strip_extras is not None:
            self._values["no_strip_extras"] = no_strip_extras
        if no_strip_markers is not None:
            self._values["no_strip_markers"] = no_strip_markers
        if only_binary is not None:
            self._values["only_binary"] = only_binary
        if output_file is not None:
            self._values["output_file"] = output_file
        if prefix is not None:
            self._values["prefix"] = prefix
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if python is not None:
            self._values["python"] = python
        if python_platform is not None:
            self._values["python_platform"] = python_platform
        if python_version is not None:
            self._values["python_version"] = python_version
        if reinstall is not None:
            self._values["reinstall"] = reinstall
        if reinstall_package is not None:
            self._values["reinstall_package"] = reinstall_package
        if require_hashes is not None:
            self._values["require_hashes"] = require_hashes
        if resolution is not None:
            self._values["resolution"] = resolution
        if strict is not None:
            self._values["strict"] = strict
        if system is not None:
            self._values["system"] = system
        if target is not None:
            self._values["target"] = target
        if torch_backend is not None:
            self._values["torch_backend"] = torch_backend
        if universal is not None:
            self._values["universal"] = universal
        if upgrade is not None:
            self._values["upgrade"] = upgrade
        if upgrade_package is not None:
            self._values["upgrade_package"] = upgrade_package
        if verify_hashes is not None:
            self._values["verify_hashes"] = verify_hashes

    @builtins.property
    def all_extras(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include all optional dependencies.

        Only applies to ``pyproject.toml``, ``setup.py``, and ``setup.cfg`` sources.

        :stability: experimental
        :schema: PipOptions#all-extras
        '''
        result = self._values.get("all_extras")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_empty_requirements(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow ``uv pip sync`` with empty requirements, which will clear the environment of all packages.

        :stability: experimental
        :schema: PipOptions#allow-empty-requirements
        '''
        result = self._values.get("allow_empty_requirements")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def annotation_style(self) -> typing.Optional["AnnotationStyle"]:
        '''(experimental) The style of the annotation comments included in the output file, used to indicate the source of each package.

        :stability: experimental
        :schema: PipOptions#annotation-style
        '''
        result = self._values.get("annotation_style")
        return typing.cast(typing.Optional["AnnotationStyle"], result)

    @builtins.property
    def break_system_packages(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow uv to modify an ``EXTERNALLY-MANAGED`` Python installation.

        WARNING: ``--break-system-packages`` is intended for use in continuous integration (CI)
        environments, when installing into Python installations that are managed by an external
        package manager, like ``apt``. It should be used with caution, as such Python installations
        explicitly recommend against modifications by other package managers (like uv or pip).

        :stability: experimental
        :schema: PipOptions#break-system-packages
        '''
        result = self._values.get("break_system_packages")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compile_bytecode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Compile Python files to bytecode after installation.

        By default, uv does not compile Python (``.py``) files to bytecode (``__pycache__/*.pyc``);
        instead, compilation is performed lazily the first time a module is imported. For use-cases
        in which start time is critical, such as CLI applications and Docker containers, this option
        can be enabled to trade longer installation times for faster start times.

        When enabled, uv will process the entire site-packages directory (including packages that
        are not being modified by the current operation) for consistency. Like pip, it will also
        ignore errors.

        :stability: experimental
        :schema: PipOptions#compile-bytecode
        '''
        result = self._values.get("compile_bytecode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def config_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend, specified as ``KEY=VALUE`` pairs.

        :stability: experimental
        :schema: PipOptions#config-settings
        '''
        result = self._values.get("config_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def config_settings_package(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]]:
        '''(experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend for specific packages, specified as ``KEY=VALUE`` pairs.

        :stability: experimental
        :schema: PipOptions#config-settings-package
        '''
        result = self._values.get("config_settings_package")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]], result)

    @builtins.property
    def custom_compile_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The header comment to include at the top of the output file generated by ``uv pip compile``.

        Used to reflect custom build scripts and commands that wrap ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#custom-compile-command
        '''
        result = self._values.get("custom_compile_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependency_metadata(self) -> typing.Optional[typing.List["StaticMetadata"]]:
        '''(experimental) Pre-defined static metadata for dependencies of the project (direct or transitive).

        When
        provided, enables the resolver to use the specified metadata instead of querying the
        registry or building the relevant package from source.

        Metadata should be provided in adherence with the `Metadata 2.3 <https://packaging.python.org/en/latest/specifications/core-metadata/>`_
        standard, though only the following fields are respected:

        - ``name``: The name of the package.
        - (Optional) ``version``: The version of the package. If omitted, the metadata will be applied
          to all versions of the package.
        - (Optional) ``requires-dist``: The dependencies of the package (e.g., ``werkzeug>=0.14``).
        - (Optional) ``requires-python``: The Python version required by the package (e.g., ``>=3.10``).
        - (Optional) ``provides-extra``: The extras provided by the package.

        :stability: experimental
        :schema: PipOptions#dependency-metadata
        '''
        result = self._values.get("dependency_metadata")
        return typing.cast(typing.Optional[typing.List["StaticMetadata"]], result)

    @builtins.property
    def emit_build_options(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include ``--no-binary`` and ``--only-binary`` entries in the output file generated by ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#emit-build-options
        '''
        result = self._values.get("emit_build_options")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def emit_find_links(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include ``--find-links`` entries in the output file generated by ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#emit-find-links
        '''
        result = self._values.get("emit_find_links")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def emit_index_annotation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include comment annotations indicating the index used to resolve each package (e.g., ``# from https://pypi.org/simple``).

        :stability: experimental
        :schema: PipOptions#emit-index-annotation
        '''
        result = self._values.get("emit_index_annotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def emit_index_url(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include ``--index-url`` and ``--extra-index-url`` entries in the output file generated by ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#emit-index-url
        '''
        result = self._values.get("emit_index_url")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def emit_marker_expression(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to emit a marker string indicating the conditions under which the set of pinned dependencies is valid.

        The pinned dependencies may be valid even when the marker expression is
        false, but when the expression is true, the requirements are known to
        be correct.

        :stability: experimental
        :schema: PipOptions#emit-marker-expression
        '''
        result = self._values.get("emit_marker_expression")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclude_newer(self) -> typing.Optional[builtins.str]:
        '''(experimental) Limit candidate packages to those that were uploaded prior to a given point in time.

        Accepts a superset of `RFC 3339 <https://www.rfc-editor.org/rfc/rfc3339.html>`_ (e.g.,
        ``2006-12-02T02:07:43Z``). A full timestamp is required to ensure that the resolver will
        behave consistently across timezones.

        :stability: experimental
        :schema: PipOptions#exclude-newer
        '''
        result = self._values.get("exclude_newer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_newer_package(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Limit candidate packages for specific packages to those that were uploaded prior to the given date.

        Accepts package-date pairs in a dictionary format.

        :stability: experimental
        :schema: PipOptions#exclude-newer-package
        '''
        result = self._values.get("exclude_newer_package")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def extra(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Include optional dependencies from the specified extra; may be provided more than once.

        Only applies to ``pyproject.toml``, ``setup.py``, and ``setup.cfg`` sources.

        :stability: experimental
        :schema: PipOptions#extra
        '''
        result = self._values.get("extra")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extra_build_dependencies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]]:
        '''(experimental) Additional build dependencies for packages.

        This allows extending the PEP 517 build environment for the project's dependencies with
        additional packages. This is useful for packages that assume the presence of packages like
        ``pip``, and do not declare them as build dependencies.

        :stability: experimental
        :schema: PipOptions#extra-build-dependencies
        '''
        result = self._values.get("extra_build_dependencies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]], result)

    @builtins.property
    def extra_build_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) Extra environment variables to set when building certain packages.

        Environment variables will be added to the environment when building the
        specified packages.

        :stability: experimental
        :schema: PipOptions#extra-build-variables
        '''
        result = self._values.get("extra_build_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def extra_index_url(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Extra URLs of package indexes to use, in addition to ``--index-url``.

        Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_
        (the simple repository API), or a local directory laid out in the same format.

        All indexes provided via this flag take priority over the index specified by
        ```index_url`` <#index-url>`_. When multiple indexes are provided, earlier values take priority.

        To control uv's resolution strategy when multiple indexes are present, see
        ```index_strategy`` <#index-strategy>`_.

        :stability: experimental
        :schema: PipOptions#extra-index-url
        '''
        result = self._values.get("extra_index_url")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def find_links(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Locations to search for candidate distributions, in addition to those found in the registry indexes.

        If a path, the target must be a directory that contains packages as wheel files (``.whl``) or
        source distributions (e.g., ``.tar.gz`` or ``.zip``) at the top level.

        If a URL, the page must contain a flat list of links to package files adhering to the
        formats described above.

        :stability: experimental
        :schema: PipOptions#find-links
        '''
        result = self._values.get("find_links")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fork_strategy(self) -> typing.Optional["ForkStrategy"]:
        '''(experimental) The strategy to use when selecting multiple versions of a given package across Python versions and platforms.

        By default, uv will optimize for selecting the latest version of each package for each
        supported Python version (``requires-python``), while minimizing the number of selected
        versions across platforms.

        Under ``fewest``, uv will minimize the number of selected versions for each package,
        preferring older versions that are compatible with a wider range of supported Python
        versions or platforms.

        :stability: experimental
        :schema: PipOptions#fork-strategy
        '''
        result = self._values.get("fork_strategy")
        return typing.cast(typing.Optional["ForkStrategy"], result)

    @builtins.property
    def generate_hashes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include distribution hashes in the output file.

        :stability: experimental
        :schema: PipOptions#generate-hashes
        '''
        result = self._values.get("generate_hashes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[typing.List["PipGroupName"]]:
        '''(experimental) Include the following dependency groups.

        :stability: experimental
        :schema: PipOptions#group
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[typing.List["PipGroupName"]], result)

    @builtins.property
    def index_strategy(self) -> typing.Optional["IndexStrategy"]:
        '''(experimental) The strategy to use when resolving against multiple index URLs.

        By default, uv will stop at the first index on which a given package is available, and
        limit resolutions to those present on that first index (``first-index``). This prevents
        "dependency confusion" attacks, whereby an attacker can upload a malicious package under the
        same name to an alternate index.

        :stability: experimental
        :schema: PipOptions#index-strategy
        '''
        result = self._values.get("index_strategy")
        return typing.cast(typing.Optional["IndexStrategy"], result)

    @builtins.property
    def index_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL of the Python package index (by default: `https://pypi.org/simple <https://pypi.org/simple>`_).

        Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_
        (the simple repository API), or a local directory laid out in the same format.

        The index provided by this setting is given lower priority than any indexes specified via
        ```extra_index_url`` <#extra-index-url>`_.

        :stability: experimental
        :schema: PipOptions#index-url
        '''
        result = self._values.get("index_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyring_provider(self) -> typing.Optional["KeyringProviderType"]:
        '''(experimental) Attempt to use ``keyring`` for authentication for index URLs.

        At present, only ``--keyring-provider subprocess`` is supported, which configures uv to
        use the ``keyring`` CLI to handle authentication.

        :stability: experimental
        :schema: PipOptions#keyring-provider
        '''
        result = self._values.get("keyring_provider")
        return typing.cast(typing.Optional["KeyringProviderType"], result)

    @builtins.property
    def link_mode(self) -> typing.Optional["LinkMode"]:
        '''(experimental) The method to use when installing packages from the global cache.

        Defaults to ``clone`` (also known as Copy-on-Write) on macOS, and ``hardlink`` on Linux and
        Windows.

        WARNING: The use of symlink link mode is discouraged, as they create tight coupling between
        the cache and the target environment. For example, clearing the cache (``uv cache clean``)
        will break all installed packages by way of removing the underlying source files. Use
        symlinks with caution.

        :default: clone``(also known as Copy-on-Write) on macOS, and``hardlink` on Linux and

        :stability: experimental
        :schema: PipOptions#link-mode
        '''
        result = self._values.get("link_mode")
        return typing.cast(typing.Optional["LinkMode"], result)

    @builtins.property
    def no_annotate(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Exclude comment annotations indicating the source of each package from the output file generated by ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#no-annotate
        '''
        result = self._values.get("no_annotate")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_binary(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Don't install pre-built wheels.

        The given packages will be built and installed from source. The resolver will still use
        pre-built wheels to extract package metadata, if available.

        Multiple packages may be provided. Disable binaries for all packages with ``:all:``.
        Clear previously specified packages with ``:none:``.

        :stability: experimental
        :schema: PipOptions#no-binary
        '''
        result = self._values.get("no_binary")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Don't build source distributions.

        When enabled, resolving will not run arbitrary Python code. The cached wheels of
        already-built source distributions will be reused, but operations that require building
        distributions will exit with an error.

        Alias for ``--only-binary :all:``.

        :stability: experimental
        :schema: PipOptions#no-build
        '''
        result = self._values.get("no_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_build_isolation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Disable isolation when building source distributions.

        Assumes that build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_
        are already installed.

        :stability: experimental
        :schema: PipOptions#no-build-isolation
        '''
        result = self._values.get("no_build_isolation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_build_isolation_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Disable isolation when building source distributions for a specific package.

        Assumes that the packages' build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_
        are already installed.

        :stability: experimental
        :schema: PipOptions#no-build-isolation-package
        '''
        result = self._values.get("no_build_isolation_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_deps(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignore package dependencies, instead only add those packages explicitly listed on the command line to the resulting requirements file.

        :stability: experimental
        :schema: PipOptions#no-deps
        '''
        result = self._values.get("no_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_emit_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specify a package to omit from the output resolution.

        Its dependencies will still be
        included in the resolution. Equivalent to pip-compile's ``--unsafe-package`` option.

        :stability: experimental
        :schema: PipOptions#no-emit-package
        '''
        result = self._values.get("no_emit_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_extra(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Exclude the specified optional dependencies if ``all-extras`` is supplied.

        :stability: experimental
        :schema: PipOptions#no-extra
        '''
        result = self._values.get("no_extra")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_header(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Exclude the comment header at the top of output file generated by ``uv pip compile``.

        :stability: experimental
        :schema: PipOptions#no-header
        '''
        result = self._values.get("no_header")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_index(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignore all registry indexes (e.g., PyPI), instead relying on direct URL dependencies and those provided via ``--find-links``.

        :stability: experimental
        :schema: PipOptions#no-index
        '''
        result = self._values.get("no_index")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_sources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignore the ``tool.uv.sources`` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any local or Git sources.

        :stability: experimental
        :schema: PipOptions#no-sources
        '''
        result = self._values.get("no_sources")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_strip_extras(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include extras in the output file.

        By default, uv strips extras, as any packages pulled in by the extras are already included
        as dependencies in the output file directly. Further, output files generated with
        ``--no-strip-extras`` cannot be used as constraints files in ``install`` and ``sync`` invocations.

        :stability: experimental
        :schema: PipOptions#no-strip-extras
        '''
        result = self._values.get("no_strip_extras")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_strip_markers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include environment markers in the output file generated by ``uv pip compile``.

        By default, uv strips environment markers, as the resolution generated by ``compile`` is
        only guaranteed to be correct for the target environment.

        :stability: experimental
        :schema: PipOptions#no-strip-markers
        '''
        result = self._values.get("no_strip_markers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def only_binary(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Only use pre-built wheels; don't build source distributions.

        When enabled, resolving will not run code from the given packages. The cached wheels of already-built
        source distributions will be reused, but operations that require building distributions will
        exit with an error.

        Multiple packages may be provided. Disable binaries for all packages with ``:all:``.
        Clear previously specified packages with ``:none:``.

        :stability: experimental
        :schema: PipOptions#only-binary
        '''
        result = self._values.get("only_binary")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def output_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Write the requirements generated by ``uv pip compile`` to the given ``requirements.txt`` file.

        If the file already exists, the existing versions will be preferred when resolving
        dependencies, unless ``--upgrade`` is also specified.

        :stability: experimental
        :schema: PipOptions#output-file
        '''
        result = self._values.get("output_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Install packages into ``lib``, ``bin``, and other top-level folders under the specified directory, as if a virtual environment were present at that location.

        In general, prefer the use of ``--python`` to install into an alternate environment, as
        scripts and other artifacts installed via ``--prefix`` will reference the installing
        interpreter, rather than any interpreter added to the ``--prefix`` directory, rendering them
        non-portable.

        :stability: experimental
        :schema: PipOptions#prefix
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prerelease(self) -> typing.Optional["PrereleaseMode"]:
        '''(experimental) The strategy to use when considering pre-release versions.

        By default, uv will accept pre-releases for packages that *only* publish pre-releases,
        along with first-party requirements that contain an explicit pre-release marker in the
        declared specifiers (``if-necessary-or-explicit``).

        :stability: experimental
        :schema: PipOptions#prerelease
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional["PrereleaseMode"], result)

    @builtins.property
    def python(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Python interpreter into which packages should be installed.

        By default, uv installs into the virtual environment in the current working directory or
        any parent directory. The ``--python`` option allows you to specify a different interpreter,
        which is intended for use in continuous integration (CI) environments or other automated
        workflows.

        Supported formats:

        - ``3.10`` looks for an installed Python 3.10 in the registry on Windows (see
          ``py --list-paths``), or ``python3.10`` on Linux and macOS.
        - ``python3.10`` or ``python.exe`` looks for a binary with the given name in ``PATH``.
        - ``/home/ferris/.local/bin/python3.10`` uses the exact Python at the given path.

        :stability: experimental
        :schema: PipOptions#python
        '''
        result = self._values.get("python")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_platform(self) -> typing.Optional["TargetTriple"]:
        '''(experimental) The platform for which requirements should be resolved.

        Represented as a "target triple", a string that describes the target platform in terms of
        its CPU, vendor, and operating system name, like ``x86_64-unknown-linux-gnu`` or
        ``aarch64-apple-darwin``.

        :stability: experimental
        :schema: PipOptions#python-platform
        '''
        result = self._values.get("python_platform")
        return typing.cast(typing.Optional["TargetTriple"], result)

    @builtins.property
    def python_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minimum Python version that should be supported by the resolved requirements (e.g., ``3.8`` or ``3.8.17``).

        If a patch version is omitted, the minimum patch version is assumed. For example, ``3.8`` is
        mapped to ``3.8.0``.

        :stability: experimental
        :schema: PipOptions#python-version
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reinstall(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Reinstall all packages, regardless of whether they're already installed.

        Implies ``refresh``.

        :stability: experimental
        :schema: PipOptions#reinstall
        '''
        result = self._values.get("reinstall")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reinstall_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Reinstall a specific package, regardless of whether it's already installed.

        Implies
        ``refresh-package``.

        :stability: experimental
        :schema: PipOptions#reinstall-package
        '''
        result = self._values.get("reinstall_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def require_hashes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Require a matching hash for each requirement.

        Hash-checking mode is all or nothing. If enabled, *all* requirements must be provided
        with a corresponding hash or set of hashes. Additionally, if enabled, *all* requirements
        must either be pinned to exact versions (e.g., ``==1.0.0``), or be specified via direct URL.

        Hash-checking mode introduces a number of additional constraints:

        - Git dependencies are not supported.
        - Editable installations are not supported.
        - Local dependencies are not supported, unless they point to a specific wheel (``.whl``) or
          source archive (``.zip``, ``.tar.gz``), as opposed to a directory.

        :stability: experimental
        :schema: PipOptions#require-hashes
        '''
        result = self._values.get("require_hashes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resolution(self) -> typing.Optional["ResolutionMode"]:
        '''(experimental) The strategy to use when selecting between the different compatible versions for a given package requirement.

        By default, uv will use the latest compatible version of each package (``highest``).

        :stability: experimental
        :schema: PipOptions#resolution
        '''
        result = self._values.get("resolution")
        return typing.cast(typing.Optional["ResolutionMode"], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Validate the Python environment, to detect packages with missing dependencies and other issues.

        :stability: experimental
        :schema: PipOptions#strict
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def system(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install packages into the system Python environment.

        By default, uv installs into the virtual environment in the current working directory or
        any parent directory. The ``--system`` option instructs uv to instead use the first Python
        found in the system ``PATH``.

        WARNING: ``--system`` is intended for use in continuous integration (CI) environments and
        should be used with caution, as it can modify the system Python installation.

        :stability: experimental
        :schema: PipOptions#system
        '''
        result = self._values.get("system")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Install packages into the specified directory, rather than into the virtual or system Python environment.

        The packages will be installed at the top-level of the directory.

        :stability: experimental
        :schema: PipOptions#target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def torch_backend(self) -> typing.Optional["TorchMode"]:
        '''(experimental) The backend to use when fetching packages in the PyTorch ecosystem.

        When set, uv will ignore the configured index URLs for packages in the PyTorch ecosystem,
        and will instead use the defined backend.

        For example, when set to ``cpu``, uv will use the CPU-only PyTorch index; when set to ``cu126``,
        uv will use the PyTorch index for CUDA 12.6.

        The ``auto`` mode will attempt to detect the appropriate PyTorch index based on the currently
        installed CUDA drivers.

        This option is in preview and may change in any future release.

        :stability: experimental
        :schema: PipOptions#torch-backend
        '''
        result = self._values.get("torch_backend")
        return typing.cast(typing.Optional["TorchMode"], result)

    @builtins.property
    def universal(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Perform a universal resolution, attempting to generate a single ``requirements.txt`` output file that is compatible with all operating systems, architectures, and Python implementations.

        In universal mode, the current Python version (or user-provided ``--python-version``) will be
        treated as a lower bound. For example, ``--universal --python-version 3.7`` would produce a
        universal resolution for Python 3.7 and later.

        :stability: experimental
        :schema: PipOptions#universal
        '''
        result = self._values.get("universal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow package upgrades, ignoring pinned versions in any existing output file.

        :stability: experimental
        :schema: PipOptions#upgrade
        '''
        result = self._values.get("upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upgrade_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Allow upgrades for a specific package, ignoring pinned versions in any existing output file.

        Accepts both standalone package names (``ruff``) and version specifiers (``ruff<0.5.0``).

        :stability: experimental
        :schema: PipOptions#upgrade-package
        '''
        result = self._values.get("upgrade_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify_hashes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Validate any hashes provided in the requirements file.

        Unlike ``--require-hashes``, ``--verify-hashes`` does not require that all requirements have
        hashes; instead, it will limit itself to verifying the hashes of those requirements that do
        include them.

        :stability: experimental
        :schema: PipOptions#verify-hashes
        '''
        result = self._values.get("verify_hashes")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.python.uvConfig.PrereleaseMode")
class PrereleaseMode(enum.Enum):
    '''
    :stability: experimental
    :schema: PrereleaseMode
    '''

    DISALLOW = "DISALLOW"
    '''(experimental) Disallow all pre-release versions.

    (disallow)

    :stability: experimental
    '''
    ALLOW = "ALLOW"
    '''(experimental) Allow all pre-release versions.

    (allow)

    :stability: experimental
    '''
    IF_HYPHEN_NECESSARY = "IF_HYPHEN_NECESSARY"
    '''(experimental) Allow pre-release versions if all versions of a package are pre-release.

    (if-necessary)

    :stability: experimental
    '''
    EXPLICIT = "EXPLICIT"
    '''(experimental) Allow pre-release versions for first-party packages with explicit pre-release markers in their version requirements.

    (explicit)

    :stability: experimental
    '''
    IF_HYPHEN_NECESSARY_HYPHEN_OR_HYPHEN_EXPLICIT = "IF_HYPHEN_NECESSARY_HYPHEN_OR_HYPHEN_EXPLICIT"
    '''(experimental) Allow pre-release versions if all versions of a package are pre-release, or if the package has an explicit pre-release marker in its version requirements.

    (if-necessary-or-explicit)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.PythonDownloads")
class PythonDownloads(enum.Enum):
    '''
    :stability: experimental
    :schema: PythonDownloads
    '''

    AUTOMATIC = "AUTOMATIC"
    '''(experimental) Automatically download managed Python installations when needed.

    (automatic)

    :stability: experimental
    '''
    MANUAL = "MANUAL"
    '''(experimental) Do not automatically download managed Python installations;

    require explicit installation. (manual)

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Do not ever allow Python downloads.

    (never)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.PythonPreference")
class PythonPreference(enum.Enum):
    '''
    :stability: experimental
    :schema: PythonPreference
    '''

    ONLY_HYPHEN_MANAGED = "ONLY_HYPHEN_MANAGED"
    '''(experimental) Only use managed Python installations;

    never use system Python installations. (only-managed)

    :stability: experimental
    '''
    MANAGED = "MANAGED"
    '''(experimental) Prefer managed Python installations over system Python installations.

    System Python installations are still preferred over downloading managed Python versions.
    Use ``only-managed`` to always fetch a managed Python version. (managed)

    :stability: experimental
    '''
    SYSTEM = "SYSTEM"
    '''(experimental) Prefer system Python installations over managed Python installations.

    If a system Python installation cannot be found, a managed Python installation can be used. (system)

    :stability: experimental
    '''
    ONLY_HYPHEN_SYSTEM = "ONLY_HYPHEN_SYSTEM"
    '''(experimental) Only use system Python installations;

    never use managed Python installations. (only-system)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.ResolutionMode")
class ResolutionMode(enum.Enum):
    '''
    :stability: experimental
    :schema: ResolutionMode
    '''

    HIGHEST = "HIGHEST"
    '''(experimental) Resolve the highest compatible version of each package.

    (highest)

    :stability: experimental
    '''
    LOWEST = "LOWEST"
    '''(experimental) Resolve the lowest compatible version of each package.

    (lowest)

    :stability: experimental
    '''
    LOWEST_HYPHEN_DIRECT = "LOWEST_HYPHEN_DIRECT"
    '''(experimental) Resolve the lowest compatible version of any direct dependencies, and the highest compatible version of any transitive dependencies.

    (lowest-direct)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.SchemaConflictItem",
    jsii_struct_bases=[],
    name_mapping={"extra": "extra", "group": "group", "package": "package"},
)
class SchemaConflictItem:
    def __init__(
        self,
        *,
        extra: typing.Optional[builtins.str] = None,
        group: typing.Optional[builtins.str] = None,
        package: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A single item in a conflicting set.

        Each item is a pair of an (optional) package and a corresponding extra or group name for that
        package.

        :param extra: 
        :param group: 
        :param package: 

        :stability: experimental
        :schema: SchemaConflictItem
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b46b2b7c2469ab6410378ad3f31dbc8765e96c46f61c3c1491291cc61b80c51)
            check_type(argname="argument extra", value=extra, expected_type=type_hints["extra"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if extra is not None:
            self._values["extra"] = extra
        if group is not None:
            self._values["group"] = group
        if package is not None:
            self._values["package"] = package

    @builtins.property
    def extra(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: SchemaConflictItem#extra
        '''
        result = self._values.get("extra")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: SchemaConflictItem#group
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: SchemaConflictItem#package
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaConflictItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.python.uvConfig.StaticMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "provides_extra": "providesExtra",
        "requires_dist": "requiresDist",
        "requires_python": "requiresPython",
        "version": "version",
    },
)
class StaticMetadata:
    def __init__(
        self,
        *,
        name: builtins.str,
        provides_extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        requires_dist: typing.Optional[typing.Sequence[builtins.str]] = None,
        requires_python: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A subset of the Python Package Metadata 2.3 standard as specified in `https://packaging.python.org/specifications/core-metadata/ <https://packaging.python.org/specifications/core-metadata/>`_.

        :param name: 
        :param provides_extra: 
        :param requires_dist: 
        :param requires_python: (experimental) PEP 508-style Python requirement, e.g., ``>=3.10``.
        :param version: (experimental) PEP 440-style package version, e.g., ``1.2.3``.

        :stability: experimental
        :schema: StaticMetadata
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95950a1bc1c16c14e86122ea689404f253b5e734ee94d174a1c7d2cb8d2e1b13)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provides_extra", value=provides_extra, expected_type=type_hints["provides_extra"])
            check_type(argname="argument requires_dist", value=requires_dist, expected_type=type_hints["requires_dist"])
            check_type(argname="argument requires_python", value=requires_python, expected_type=type_hints["requires_python"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if provides_extra is not None:
            self._values["provides_extra"] = provides_extra
        if requires_dist is not None:
            self._values["requires_dist"] = requires_dist
        if requires_python is not None:
            self._values["requires_python"] = requires_python
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        :schema: StaticMetadata#name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provides_extra(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        :schema: StaticMetadata#provides-extra
        '''
        result = self._values.get("provides_extra")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def requires_dist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        :schema: StaticMetadata#requires-dist
        '''
        result = self._values.get("requires_dist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def requires_python(self) -> typing.Optional[builtins.str]:
        '''(experimental) PEP 508-style Python requirement, e.g., ``>=3.10``.

        :stability: experimental
        :schema: StaticMetadata#requires-python
        '''
        result = self._values.get("requires_python")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) PEP 440-style package version, e.g., ``1.2.3``.

        :stability: experimental
        :schema: StaticMetadata#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.python.uvConfig.TargetTriple")
class TargetTriple(enum.Enum):
    '''(experimental) The supported target triples. Each triple consists of an architecture, vendor, and operating system.

    See: `https://doc.rust-lang.org/nightly/rustc/platform-support.html <https://doc.rust-lang.org/nightly/rustc/platform-support.html>`_

    :stability: experimental
    :schema: TargetTriple
    '''

    WINDOWS = "WINDOWS"
    '''(experimental) An alias for ``x86_64-pc-windows-msvc``, the default target for Windows.

    (windows)

    :stability: experimental
    '''
    LINUX = "LINUX"
    '''(experimental) An alias for ``x86_64-unknown-linux-gnu``, the default target for Linux.

    (linux)

    :stability: experimental
    '''
    MACOS = "MACOS"
    '''(experimental) An alias for ``aarch64-apple-darwin``, the default target for macOS.

    (macos)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC = "X86_UNDERSCORE_64_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC"
    '''(experimental) A 64-bit x86 Windows target.

    (x86_64-pc-windows-msvc)

    :stability: experimental
    '''
    AARCH64_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC = "AARCH64_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC"
    '''(experimental) An ARM64 Windows target.

    (aarch64-pc-windows-msvc)

    :stability: experimental
    '''
    I686_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC = "I686_HYPHEN_PC_HYPHEN_WINDOWS_HYPHEN_MSVC"
    '''(experimental) A 32-bit x86 Windows target.

    (i686-pc-windows-msvc)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_GNU = "X86_UNDERSCORE_64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_GNU"
    '''(experimental) An x86 Linux target.

    Equivalent to ``x86_64-manylinux_2_28``. (x86_64-unknown-linux-gnu)

    :stability: experimental
    '''
    AARCH64_HYPHEN_APPLE_HYPHEN_DARWIN = "AARCH64_HYPHEN_APPLE_HYPHEN_DARWIN"
    '''(experimental) An ARM-based macOS target, as seen on Apple Silicon devices.

    By default, assumes the least-recent, non-EOL macOS version (13.0), but respects
    the ``MACOSX_DEPLOYMENT_TARGET`` environment variable if set. (aarch64-apple-darwin)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_APPLE_HYPHEN_DARWIN = "X86_UNDERSCORE_64_HYPHEN_APPLE_HYPHEN_DARWIN"
    '''(experimental) An x86 macOS target.

    By default, assumes the least-recent, non-EOL macOS version (13.0), but respects
    the ``MACOSX_DEPLOYMENT_TARGET`` environment variable if set. (x86_64-apple-darwin)

    :stability: experimental
    '''
    AARCH64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_GNU = "AARCH64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_GNU"
    '''(experimental) An ARM64 Linux target.

    Equivalent to ``aarch64-manylinux_2_28``. (aarch64-unknown-linux-gnu)

    :stability: experimental
    '''
    AARCH64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_MUSL = "AARCH64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_MUSL"
    '''(experimental) An ARM64 Linux target.

    (aarch64-unknown-linux-musl)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_MUSL = "X86_UNDERSCORE_64_HYPHEN_UNKNOWN_HYPHEN_LINUX_HYPHEN_MUSL"
    '''(experimental) An ``x86_64`` Linux target.

    (x86_64-unknown-linux-musl)

    :stability: experimental
    '''
    RISCV64_HYPHEN_UNKNOWN_HYPHEN_LINUX = "RISCV64_HYPHEN_UNKNOWN_HYPHEN_LINUX"
    '''(experimental) A RISCV64 Linux target.

    (riscv64-unknown-linux)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX2014 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX2014"
    '''(experimental) An ``x86_64`` target for the ``manylinux2014`` platform.

    Equivalent to ``x86_64-manylinux_2_17``. (x86_64-manylinux2014)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_17 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_17"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_17`` platform.

    (x86_64-manylinux_2_17)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_28 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_28"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_28`` platform.

    (x86_64-manylinux_2_28)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_31 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_31"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_31`` platform.

    (x86_64-manylinux_2_31)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_32 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_32"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_32`` platform.

    (x86_64-manylinux_2_32)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_33 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_33"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_33`` platform.

    (x86_64-manylinux_2_33)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_34 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_34"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_34`` platform.

    (x86_64-manylinux_2_34)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_35 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_35"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_35`` platform.

    (x86_64-manylinux_2_35)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_36 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_36"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_36`` platform.

    (x86_64-manylinux_2_36)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_37 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_37"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_37`` platform.

    (x86_64-manylinux_2_37)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_38 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_38"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_38`` platform.

    (x86_64-manylinux_2_38)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_39 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_39"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_39`` platform.

    (x86_64-manylinux_2_39)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_40 = "X86_UNDERSCORE_64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_40"
    '''(experimental) An ``x86_64`` target for the ``manylinux_2_40`` platform.

    (x86_64-manylinux_2_40)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX2014 = "AARCH64_HYPHEN_MANYLINUX2014"
    '''(experimental) An ARM64 target for the ``manylinux2014`` platform.

    Equivalent to ``aarch64-manylinux_2_17``. (aarch64-manylinux2014)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_17 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_17"
    '''(experimental) An ARM64 target for the ``manylinux_2_17`` platform.

    (aarch64-manylinux_2_17)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_28 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_28"
    '''(experimental) An ARM64 target for the ``manylinux_2_28`` platform.

    (aarch64-manylinux_2_28)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_31 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_31"
    '''(experimental) An ARM64 target for the ``manylinux_2_31`` platform.

    (aarch64-manylinux_2_31)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_32 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_32"
    '''(experimental) An ARM64 target for the ``manylinux_2_32`` platform.

    (aarch64-manylinux_2_32)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_33 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_33"
    '''(experimental) An ARM64 target for the ``manylinux_2_33`` platform.

    (aarch64-manylinux_2_33)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_34 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_34"
    '''(experimental) An ARM64 target for the ``manylinux_2_34`` platform.

    (aarch64-manylinux_2_34)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_35 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_35"
    '''(experimental) An ARM64 target for the ``manylinux_2_35`` platform.

    (aarch64-manylinux_2_35)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_36 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_36"
    '''(experimental) An ARM64 target for the ``manylinux_2_36`` platform.

    (aarch64-manylinux_2_36)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_37 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_37"
    '''(experimental) An ARM64 target for the ``manylinux_2_37`` platform.

    (aarch64-manylinux_2_37)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_38 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_38"
    '''(experimental) An ARM64 target for the ``manylinux_2_38`` platform.

    (aarch64-manylinux_2_38)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_39 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_39"
    '''(experimental) An ARM64 target for the ``manylinux_2_39`` platform.

    (aarch64-manylinux_2_39)

    :stability: experimental
    '''
    AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_40 = "AARCH64_HYPHEN_MANYLINUX_UNDERSCORE_2_UNDERSCORE_40"
    '''(experimental) An ARM64 target for the ``manylinux_2_40`` platform.

    (aarch64-manylinux_2_40)

    :stability: experimental
    '''
    AARCH64_HYPHEN_LINUX_HYPHEN_ANDROID = "AARCH64_HYPHEN_LINUX_HYPHEN_ANDROID"
    '''(experimental) An ARM64 Android target.

    By default uses Android API level 24, but respects
    the ``ANDROID_API_LEVEL`` environment variable if set. (aarch64-linux-android)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_LINUX_HYPHEN_ANDROID = "X86_UNDERSCORE_64_HYPHEN_LINUX_HYPHEN_ANDROID"
    '''(experimental) An ``x86_64`` Android target.

    By default uses Android API level 24, but respects
    the ``ANDROID_API_LEVEL`` environment variable if set. (x86_64-linux-android)

    :stability: experimental
    '''
    WASM32_HYPHEN_PYODIDE2024 = "WASM32_HYPHEN_PYODIDE2024"
    '''(experimental) A wasm32 target using the Pyodide 2024 platform.

    Meant for use with Python 3.12. (wasm32-pyodide2024)

    :stability: experimental
    '''
    ARM64_HYPHEN_APPLE_HYPHEN_IOS = "ARM64_HYPHEN_APPLE_HYPHEN_IOS"
    '''(experimental) An ARM64 target for iOS device.

    By default, iOS 13.0 is used, but respects the ``IPHONEOS_DEPLOYMENT_TARGET``
    environment variable if set. (arm64-apple-ios)

    :stability: experimental
    '''
    ARM64_HYPHEN_APPLE_HYPHEN_IOS_HYPHEN_SIMULATOR = "ARM64_HYPHEN_APPLE_HYPHEN_IOS_HYPHEN_SIMULATOR"
    '''(experimental) An ARM64 target for iOS simulator.

    By default, iOS 13.0 is used, but respects the ``IPHONEOS_DEPLOYMENT_TARGET``
    environment variable if set. (arm64-apple-ios-simulator)

    :stability: experimental
    '''
    X86_UNDERSCORE_64_HYPHEN_APPLE_HYPHEN_IOS_HYPHEN_SIMULATOR = "X86_UNDERSCORE_64_HYPHEN_APPLE_HYPHEN_IOS_HYPHEN_SIMULATOR"
    '''(experimental) An ``x86_64`` target for iOS simulator.

    By default, iOS 13.0 is used, but respects the ``IPHONEOS_DEPLOYMENT_TARGET``
    environment variable if set. (x86_64-apple-ios-simulator)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.ToolUvWorkspace",
    jsii_struct_bases=[],
    name_mapping={"exclude": "exclude", "members": "members"},
)
class ToolUvWorkspace:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude: (experimental) Packages to exclude as workspace members. If a package matches both ``members`` and ``exclude``, it will be excluded. Supports both globs and explicit paths. For more information on the glob syntax, refer to the ```glob`` documentation <https://docs.rs/glob/latest/glob/struct.Pattern.html>`_.
        :param members: (experimental) Packages to include as workspace members. Supports both globs and explicit paths. For more information on the glob syntax, refer to the ```glob`` documentation <https://docs.rs/glob/latest/glob/struct.Pattern.html>`_.

        :stability: experimental
        :schema: ToolUvWorkspace
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104c3e675eb0f61a5c9f7a762fb9754ae023eb9e0db4e9434a1631ad9e3119bb)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if members is not None:
            self._values["members"] = members

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Packages to exclude as workspace members. If a package matches both ``members`` and ``exclude``, it will be excluded.

        Supports both globs and explicit paths.

        For more information on the glob syntax, refer to the ```glob`` documentation <https://docs.rs/glob/latest/glob/struct.Pattern.html>`_.

        :stability: experimental
        :schema: ToolUvWorkspace#exclude
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Packages to include as workspace members.

        Supports both globs and explicit paths.

        For more information on the glob syntax, refer to the ```glob`` documentation <https://docs.rs/glob/latest/glob/struct.Pattern.html>`_.

        :stability: experimental
        :schema: ToolUvWorkspace#members
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ToolUvWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.python.uvConfig.TorchMode")
class TorchMode(enum.Enum):
    '''(experimental) The strategy to use when determining the appropriate PyTorch index.

    :stability: experimental
    :schema: TorchMode
    '''

    AUTO = "AUTO"
    '''(experimental) Select the appropriate PyTorch index based on the operating system and CUDA driver version.

    (auto)

    :stability: experimental
    '''
    CPU = "CPU"
    '''(experimental) Use the CPU-only PyTorch index.

    (cpu)

    :stability: experimental
    '''
    CU130 = "CU130"
    '''(experimental) Use the PyTorch index for CUDA 13.0. (cu130).

    :stability: experimental
    '''
    CU129 = "CU129"
    '''(experimental) Use the PyTorch index for CUDA 12.9. (cu129).

    :stability: experimental
    '''
    CU128 = "CU128"
    '''(experimental) Use the PyTorch index for CUDA 12.8. (cu128).

    :stability: experimental
    '''
    CU126 = "CU126"
    '''(experimental) Use the PyTorch index for CUDA 12.6. (cu126).

    :stability: experimental
    '''
    CU125 = "CU125"
    '''(experimental) Use the PyTorch index for CUDA 12.5. (cu125).

    :stability: experimental
    '''
    CU124 = "CU124"
    '''(experimental) Use the PyTorch index for CUDA 12.4. (cu124).

    :stability: experimental
    '''
    CU123 = "CU123"
    '''(experimental) Use the PyTorch index for CUDA 12.3. (cu123).

    :stability: experimental
    '''
    CU122 = "CU122"
    '''(experimental) Use the PyTorch index for CUDA 12.2. (cu122).

    :stability: experimental
    '''
    CU121 = "CU121"
    '''(experimental) Use the PyTorch index for CUDA 12.1. (cu121).

    :stability: experimental
    '''
    CU120 = "CU120"
    '''(experimental) Use the PyTorch index for CUDA 12.0. (cu120).

    :stability: experimental
    '''
    CU118 = "CU118"
    '''(experimental) Use the PyTorch index for CUDA 11.8. (cu118).

    :stability: experimental
    '''
    CU117 = "CU117"
    '''(experimental) Use the PyTorch index for CUDA 11.7. (cu117).

    :stability: experimental
    '''
    CU116 = "CU116"
    '''(experimental) Use the PyTorch index for CUDA 11.6. (cu116).

    :stability: experimental
    '''
    CU115 = "CU115"
    '''(experimental) Use the PyTorch index for CUDA 11.5. (cu115).

    :stability: experimental
    '''
    CU114 = "CU114"
    '''(experimental) Use the PyTorch index for CUDA 11.4. (cu114).

    :stability: experimental
    '''
    CU113 = "CU113"
    '''(experimental) Use the PyTorch index for CUDA 11.3. (cu113).

    :stability: experimental
    '''
    CU112 = "CU112"
    '''(experimental) Use the PyTorch index for CUDA 11.2. (cu112).

    :stability: experimental
    '''
    CU111 = "CU111"
    '''(experimental) Use the PyTorch index for CUDA 11.1. (cu111).

    :stability: experimental
    '''
    CU110 = "CU110"
    '''(experimental) Use the PyTorch index for CUDA 11.0. (cu110).

    :stability: experimental
    '''
    CU102 = "CU102"
    '''(experimental) Use the PyTorch index for CUDA 10.2. (cu102).

    :stability: experimental
    '''
    CU101 = "CU101"
    '''(experimental) Use the PyTorch index for CUDA 10.1. (cu101).

    :stability: experimental
    '''
    CU100 = "CU100"
    '''(experimental) Use the PyTorch index for CUDA 10.0. (cu100).

    :stability: experimental
    '''
    CU92 = "CU92"
    '''(experimental) Use the PyTorch index for CUDA 9.2. (cu92).

    :stability: experimental
    '''
    CU91 = "CU91"
    '''(experimental) Use the PyTorch index for CUDA 9.1. (cu91).

    :stability: experimental
    '''
    CU90 = "CU90"
    '''(experimental) Use the PyTorch index for CUDA 9.0. (cu90).

    :stability: experimental
    '''
    CU80 = "CU80"
    '''(experimental) Use the PyTorch index for CUDA 8.0. (cu80).

    :stability: experimental
    '''
    ROCM6_3 = "ROCM6_3"
    '''(experimental) Use the PyTorch index for ROCm 6.3. (rocm6.3).

    :stability: experimental
    '''
    ROCM6_2_4 = "ROCM6_2_4"
    '''(experimental) Use the PyTorch index for ROCm 6.2.4. (rocm6.2.4).

    :stability: experimental
    '''
    ROCM6_2 = "ROCM6_2"
    '''(experimental) Use the PyTorch index for ROCm 6.2. (rocm6.2).

    :stability: experimental
    '''
    ROCM6_1 = "ROCM6_1"
    '''(experimental) Use the PyTorch index for ROCm 6.1. (rocm6.1).

    :stability: experimental
    '''
    ROCM6_0 = "ROCM6_0"
    '''(experimental) Use the PyTorch index for ROCm 6.0. (rocm6.0).

    :stability: experimental
    '''
    ROCM5_7 = "ROCM5_7"
    '''(experimental) Use the PyTorch index for ROCm 5.7. (rocm5.7).

    :stability: experimental
    '''
    ROCM5_6 = "ROCM5_6"
    '''(experimental) Use the PyTorch index for ROCm 5.6. (rocm5.6).

    :stability: experimental
    '''
    ROCM5_5 = "ROCM5_5"
    '''(experimental) Use the PyTorch index for ROCm 5.5. (rocm5.5).

    :stability: experimental
    '''
    ROCM5_4_2 = "ROCM5_4_2"
    '''(experimental) Use the PyTorch index for ROCm 5.4.2. (rocm5.4.2).

    :stability: experimental
    '''
    ROCM5_4 = "ROCM5_4"
    '''(experimental) Use the PyTorch index for ROCm 5.4. (rocm5.4).

    :stability: experimental
    '''
    ROCM5_3 = "ROCM5_3"
    '''(experimental) Use the PyTorch index for ROCm 5.3. (rocm5.3).

    :stability: experimental
    '''
    ROCM5_2 = "ROCM5_2"
    '''(experimental) Use the PyTorch index for ROCm 5.2. (rocm5.2).

    :stability: experimental
    '''
    ROCM5_1_1 = "ROCM5_1_1"
    '''(experimental) Use the PyTorch index for ROCm 5.1.1. (rocm5.1.1).

    :stability: experimental
    '''
    ROCM4_2 = "ROCM4_2"
    '''(experimental) Use the PyTorch index for ROCm 4.2. (rocm4.2).

    :stability: experimental
    '''
    ROCM4_1 = "ROCM4_1"
    '''(experimental) Use the PyTorch index for ROCm 4.1. (rocm4.1).

    :stability: experimental
    '''
    ROCM4_0_1 = "ROCM4_0_1"
    '''(experimental) Use the PyTorch index for ROCm 4.0.1. (rocm4.0.1).

    :stability: experimental
    '''
    XPU = "XPU"
    '''(experimental) Use the PyTorch index for Intel XPU.

    (xpu)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.python.uvConfig.TrustedPublishing")
class TrustedPublishing(enum.Enum):
    '''
    :stability: experimental
    :schema: TrustedPublishing
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) always.

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) never.

    :stability: experimental
    '''
    AUTOMATIC = "AUTOMATIC"
    '''(experimental) Attempt trusted publishing when we're in a supported environment, continue if that fails.

    Supported environments include GitHub Actions and GitLab CI/CD. (automatic)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.python.uvConfig.UvConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "add_bounds": "addBounds",
        "allow_insecure_host": "allowInsecureHost",
        "build_backend": "buildBackend",
        "build_constraint_dependencies": "buildConstraintDependencies",
        "cache_dir": "cacheDir",
        "cache_keys": "cacheKeys",
        "check_url": "checkUrl",
        "compile_bytecode": "compileBytecode",
        "concurrent_builds": "concurrentBuilds",
        "concurrent_downloads": "concurrentDownloads",
        "concurrent_installs": "concurrentInstalls",
        "config_settings": "configSettings",
        "config_settings_package": "configSettingsPackage",
        "conflicts": "conflicts",
        "constraint_dependencies": "constraintDependencies",
        "default_groups": "defaultGroups",
        "dependency_groups": "dependencyGroups",
        "dependency_metadata": "dependencyMetadata",
        "dev_dependencies": "devDependencies",
        "environments": "environments",
        "exclude_dependencies": "excludeDependencies",
        "exclude_newer": "excludeNewer",
        "exclude_newer_package": "excludeNewerPackage",
        "extra_build_dependencies": "extraBuildDependencies",
        "extra_build_variables": "extraBuildVariables",
        "extra_index_url": "extraIndexUrl",
        "find_links": "findLinks",
        "fork_strategy": "forkStrategy",
        "index": "index",
        "index_strategy": "indexStrategy",
        "index_url": "indexUrl",
        "keyring_provider": "keyringProvider",
        "link_mode": "linkMode",
        "managed": "managed",
        "native_tls": "nativeTls",
        "no_binary": "noBinary",
        "no_binary_package": "noBinaryPackage",
        "no_build": "noBuild",
        "no_build_isolation": "noBuildIsolation",
        "no_build_isolation_package": "noBuildIsolationPackage",
        "no_build_package": "noBuildPackage",
        "no_cache": "noCache",
        "no_index": "noIndex",
        "no_sources": "noSources",
        "offline": "offline",
        "override_dependencies": "overrideDependencies",
        "package": "package",
        "pip": "pip",
        "prerelease": "prerelease",
        "preview": "preview",
        "publish_url": "publishUrl",
        "pypy_install_mirror": "pypyInstallMirror",
        "python_downloads": "pythonDownloads",
        "python_downloads_json_url": "pythonDownloadsJsonUrl",
        "python_install_mirror": "pythonInstallMirror",
        "python_preference": "pythonPreference",
        "reinstall": "reinstall",
        "reinstall_package": "reinstallPackage",
        "required_environments": "requiredEnvironments",
        "required_version": "requiredVersion",
        "resolution": "resolution",
        "sources": "sources",
        "trusted_publishing": "trustedPublishing",
        "upgrade": "upgrade",
        "upgrade_package": "upgradePackage",
        "workspace": "workspace",
    },
)
class UvConfiguration:
    def __init__(
        self,
        *,
        add_bounds: typing.Optional["AddBoundsKind"] = None,
        allow_insecure_host: typing.Optional[typing.Sequence[builtins.str]] = None,
        build_backend: typing.Optional[typing.Union["BuildBackendSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        build_constraint_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_dir: typing.Optional[builtins.str] = None,
        cache_keys: typing.Optional[typing.Sequence[typing.Any]] = None,
        check_url: typing.Optional[builtins.str] = None,
        compile_bytecode: typing.Optional[builtins.bool] = None,
        concurrent_builds: typing.Optional[jsii.Number] = None,
        concurrent_downloads: typing.Optional[jsii.Number] = None,
        concurrent_installs: typing.Optional[jsii.Number] = None,
        config_settings: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        config_settings_package: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]] = None,
        conflicts: typing.Optional[typing.Sequence[typing.Sequence[typing.Union["SchemaConflictItem", typing.Dict[builtins.str, typing.Any]]]]] = None,
        constraint_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_groups: typing.Any = None,
        dependency_groups: typing.Optional[typing.Mapping[builtins.str, typing.Union["DependencyGroupSettings", typing.Dict[builtins.str, typing.Any]]]] = None,
        dependency_metadata: typing.Optional[typing.Sequence[typing.Union["StaticMetadata", typing.Dict[builtins.str, typing.Any]]]] = None,
        dev_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_newer: typing.Optional[builtins.str] = None,
        exclude_newer_package: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra_build_dependencies: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
        extra_build_variables: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
        extra_index_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        find_links: typing.Optional[typing.Sequence[builtins.str]] = None,
        fork_strategy: typing.Optional["ForkStrategy"] = None,
        index: typing.Optional[typing.Sequence[typing.Union["Index", typing.Dict[builtins.str, typing.Any]]]] = None,
        index_strategy: typing.Optional["IndexStrategy"] = None,
        index_url: typing.Optional[builtins.str] = None,
        keyring_provider: typing.Optional["KeyringProviderType"] = None,
        link_mode: typing.Optional["LinkMode"] = None,
        managed: typing.Optional[builtins.bool] = None,
        native_tls: typing.Optional[builtins.bool] = None,
        no_binary: typing.Optional[builtins.bool] = None,
        no_binary_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_build: typing.Optional[builtins.bool] = None,
        no_build_isolation: typing.Optional[builtins.bool] = None,
        no_build_isolation_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_build_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        no_cache: typing.Optional[builtins.bool] = None,
        no_index: typing.Optional[builtins.bool] = None,
        no_sources: typing.Optional[builtins.bool] = None,
        offline: typing.Optional[builtins.bool] = None,
        override_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        package: typing.Optional[builtins.bool] = None,
        pip: typing.Optional[typing.Union["PipOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        prerelease: typing.Optional["PrereleaseMode"] = None,
        preview: typing.Optional[builtins.bool] = None,
        publish_url: typing.Optional[builtins.str] = None,
        pypy_install_mirror: typing.Optional[builtins.str] = None,
        python_downloads: typing.Optional["PythonDownloads"] = None,
        python_downloads_json_url: typing.Optional[builtins.str] = None,
        python_install_mirror: typing.Optional[builtins.str] = None,
        python_preference: typing.Optional["PythonPreference"] = None,
        reinstall: typing.Optional[builtins.bool] = None,
        reinstall_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_version: typing.Optional[builtins.str] = None,
        resolution: typing.Optional["ResolutionMode"] = None,
        sources: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
        trusted_publishing: typing.Optional["TrustedPublishing"] = None,
        upgrade: typing.Optional[builtins.bool] = None,
        upgrade_package: typing.Optional[typing.Sequence[builtins.str]] = None,
        workspace: typing.Optional[typing.Union["ToolUvWorkspace", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Metadata and configuration for uv.

        :param add_bounds: (experimental) The default version specifier when adding a dependency. When adding a dependency to the project, if no constraint or URL is provided, a constraint is added based on the latest compatible version of the package. By default, a lower bound constraint is used, e.g., ``>=1.2.3``. When ``--frozen`` is provided, no resolution is performed, and dependencies are always added without constraints. This option is in preview and may change in any future release.
        :param allow_insecure_host: (experimental) Allow insecure connections to host. Expects to receive either a hostname (e.g., ``localhost``), a host-port pair (e.g., ``localhost:8080``), or a URL (e.g., ``https://localhost``). WARNING: Hosts included in this list will not be verified against the system's certificate store. Only use ``--allow-insecure-host`` in a secure network with verified sources, as it bypasses SSL verification and could expose you to MITM attacks.
        :param build_backend: (experimental) Configuration for the uv build backend. Note that those settings only apply when using the ``uv_build`` backend, other build backends (such as hatchling) have their own configuration.
        :param build_constraint_dependencies: (experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.
        :param cache_dir: (experimental) Path to the cache directory.
        :param cache_keys: (experimental) The keys to consider when caching builds for the project. Cache keys enable you to specify the files or directories that should trigger a rebuild when modified. By default, uv will rebuild a project whenever the ``pyproject.toml``, ``setup.py``, or ``setup.cfg`` files in the project directory are modified, or if a ``src`` directory is added or removed, i.e.:: cache-keys = [{ file = "pyproject.toml" }, { file = "setup.py" }, { file = "setup.cfg" }, { dir = "src" }] As an example: if a project uses dynamic metadata to read its dependencies from a ``requirements.txt`` file, you can specify ``cache-keys = [{ file = "requirements.txt" }, { file = "pyproject.toml" }]`` to ensure that the project is rebuilt whenever the ``requirements.txt`` file is modified (in addition to watching the ``pyproject.toml``). Globs are supported, following the syntax of the ```glob`` <https://docs.rs/glob/0.3.1/glob/struct.Pattern.html>`_ crate. For example, to invalidate the cache whenever a ``.toml`` file in the project directory or any of its subdirectories is modified, you can specify ``cache-keys = [{ file = "*_/*.toml" }]``. Note that the use of globs can be expensive, as uv may need to walk the filesystem to determine whether any files have changed. Cache keys can also include version control information. For example, if a project uses ``setuptools_scm`` to read its version from a Git commit, you can specify ``cache-keys = [{ git = { commit = true }, { file = "pyproject.toml" }]`` to include the current Git commit hash in the cache key (in addition to the ``pyproject.toml``). Git tags are also supported via ``cache-keys = [{ git = { commit = true, tags = true } }]``. Cache keys can also include environment variables. For example, if a project relies on ``MACOSX_DEPLOYMENT_TARGET`` or other environment variables to determine its behavior, you can specify ``cache-keys = [{ env = "MACOSX_DEPLOYMENT_TARGET" }]`` to invalidate the cache whenever the environment variable changes. Cache keys only affect the project defined by the ``pyproject.toml`` in which they're specified (as opposed to, e.g., affecting all members in a workspace), and all paths and globs are interpreted as relative to the project directory.
        :param check_url: (experimental) Check an index URL for existing files to skip duplicate uploads. This option allows retrying publishing that failed after only some, but not all files have been uploaded, and handles error due to parallel uploads of the same file. Before uploading, the index is checked. If the exact same file already exists in the index, the file will not be uploaded. If an error occurred during the upload, the index is checked again, to handle cases where the identical file was uploaded twice in parallel. The exact behavior will vary based on the index. When uploading to PyPI, uploading the same file succeeds even without ``--check-url``, while most other indexes error. The index must provide one of the supported hashes (SHA-256, SHA-384, or SHA-512).
        :param compile_bytecode: (experimental) Compile Python files to bytecode after installation. By default, uv does not compile Python (``.py``) files to bytecode (``__pycache__/*.pyc``); instead, compilation is performed lazily the first time a module is imported. For use-cases in which start time is critical, such as CLI applications and Docker containers, this option can be enabled to trade longer installation times for faster start times. When enabled, uv will process the entire site-packages directory (including packages that are not being modified by the current operation) for consistency. Like pip, it will also ignore errors.
        :param concurrent_builds: (experimental) The maximum number of source distributions that uv will build concurrently at any given time. Defaults to the number of available CPU cores. Default: the number of available CPU cores.
        :param concurrent_downloads: (experimental) The maximum number of in-flight concurrent downloads that uv will perform at any given time.
        :param concurrent_installs: (experimental) The number of threads used when installing and unzipping packages. Defaults to the number of available CPU cores. Default: the number of available CPU cores.
        :param config_settings: (experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend, specified as ``KEY=VALUE`` pairs.
        :param config_settings_package: (experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend for specific packages, specified as ``KEY=VALUE`` pairs. Accepts a map from package names to string key-value pairs.
        :param conflicts: (experimental) A list of sets of conflicting groups or extras.
        :param constraint_dependencies: (experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.
        :param default_groups: (experimental) The list of ``dependency-groups`` to install by default. Can also be the literal ``"all"`` to default enable all groups.
        :param dependency_groups: (experimental) Additional settings for ``dependency-groups``. Currently this can only be used to add ``requires-python`` constraints to dependency groups (typically to inform uv that your dev tooling has a higher python requirement than your actual project). This cannot be used to define dependency groups, use the top-level ``[dependency-groups]`` table for that.
        :param dependency_metadata: (experimental) Pre-defined static metadata for dependencies of the project (direct or transitive). When provided, enables the resolver to use the specified metadata instead of querying the registry or building the relevant package from source. Metadata should be provided in adherence with the `Metadata 2.3 <https://packaging.python.org/en/latest/specifications/core-metadata/>`_ standard, though only the following fields are respected: - ``name``: The name of the package. - (Optional) ``version``: The version of the package. If omitted, the metadata will be applied to all versions of the package. - (Optional) ``requires-dist``: The dependencies of the package (e.g., ``werkzeug>=0.14``). - (Optional) ``requires-python``: The Python version required by the package (e.g., ``>=3.10``). - (Optional) ``provides-extra``: The extras provided by the package.
        :param dev_dependencies: (experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.
        :param environments: (experimental) A list of environment markers, e.g., ``python_version >= '3.6'``.
        :param exclude_dependencies: (experimental) Package names to exclude, e.g., ``werkzeug``, ``numpy``.
        :param exclude_newer: (experimental) Limit candidate packages to those that were uploaded prior to a given point in time. Accepts a superset of `RFC 3339 <https://www.rfc-editor.org/rfc/rfc3339.html>`_ (e.g., ``2006-12-02T02:07:43Z``). A full timestamp is required to ensure that the resolver will behave consistently across timezones.
        :param exclude_newer_package: (experimental) Limit candidate packages for specific packages to those that were uploaded prior to the given date. Accepts package-date pairs in a dictionary format.
        :param extra_build_dependencies: (experimental) Additional build dependencies for packages. This allows extending the PEP 517 build environment for the project's dependencies with additional packages. This is useful for packages that assume the presence of packages like ``pip``, and do not declare them as build dependencies.
        :param extra_build_variables: (experimental) Extra environment variables to set when building certain packages. Environment variables will be added to the environment when building the specified packages.
        :param extra_index_url: (experimental) Extra URLs of package indexes to use, in addition to ``--index-url``. Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_ (the simple repository API), or a local directory laid out in the same format. All indexes provided via this flag take priority over the index specified by ```index_url`` <#index-url>`_ or ```index`` <#index>`_ with ``default = true``. When multiple indexes are provided, earlier values take priority. To control uv's resolution strategy when multiple indexes are present, see ```index_strategy`` <#index-strategy>`_. (Deprecated: use ``index`` instead.)
        :param find_links: (experimental) Locations to search for candidate distributions, in addition to those found in the registry indexes. If a path, the target must be a directory that contains packages as wheel files (``.whl``) or source distributions (e.g., ``.tar.gz`` or ``.zip``) at the top level. If a URL, the page must contain a flat list of links to package files adhering to the formats described above.
        :param fork_strategy: (experimental) The strategy to use when selecting multiple versions of a given package across Python versions and platforms. By default, uv will optimize for selecting the latest version of each package for each supported Python version (``requires-python``), while minimizing the number of selected versions across platforms. Under ``fewest``, uv will minimize the number of selected versions for each package, preferring older versions that are compatible with a wider range of supported Python versions or platforms.
        :param index: (experimental) The indexes to use when resolving dependencies. Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_ (the simple repository API), or a local directory laid out in the same format. Indexes are considered in the order in which they're defined, such that the first-defined index has the highest priority. Further, the indexes provided by this setting are given higher priority than any indexes specified via ```index_url`` <#index-url>`_ or ```extra_index_url`` <#extra-index-url>`_. uv will only consider the first index that contains a given package, unless an alternative `index strategy <#index-strategy>`_ is specified. If an index is marked as ``explicit = true``, it will be used exclusively for the dependencies that select it explicitly via ``[tool.uv.sources]``, as in:: [[tool.uv.index]] name = "pytorch" url = "https://download.pytorch.org/whl/cu121" explicit = true [tool.uv.sources] torch = { index = "pytorch" } If an index is marked as ``default = true``, it will be moved to the end of the prioritized list, such that it is given the lowest priority when resolving packages. Additionally, marking an index as default will disable the PyPI default index.
        :param index_strategy: (experimental) The strategy to use when resolving against multiple index URLs. By default, uv will stop at the first index on which a given package is available, and limit resolutions to those present on that first index (``first-index``). This prevents "dependency confusion" attacks, whereby an attacker can upload a malicious package under the same name to an alternate index.
        :param index_url: (experimental) The URL of the Python package index (by default: `https://pypi.org/simple <https://pypi.org/simple>`_). Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_ (the simple repository API), or a local directory laid out in the same format. The index provided by this setting is given lower priority than any indexes specified via ```extra_index_url`` <#extra-index-url>`_ or ```index`` <#index>`_. (Deprecated: use ``index`` instead.)
        :param keyring_provider: (experimental) Attempt to use ``keyring`` for authentication for index URLs. At present, only ``--keyring-provider subprocess`` is supported, which configures uv to use the ``keyring`` CLI to handle authentication.
        :param link_mode: (experimental) The method to use when installing packages from the global cache. Defaults to ``clone`` (also known as Copy-on-Write) on macOS, and ``hardlink`` on Linux and Windows. WARNING: The use of symlink link mode is discouraged, as they create tight coupling between the cache and the target environment. For example, clearing the cache (``uv cache clean``) will break all installed packages by way of removing the underlying source files. Use symlinks with caution. Default: clone``(also known as Copy-on-Write) on macOS, and``hardlink` on Linux and
        :param managed: (experimental) Whether the project is managed by uv. If ``false``, uv will ignore the project when ``uv run`` is invoked.
        :param native_tls: (experimental) Whether to load TLS certificates from the platform's native certificate store. By default, uv loads certificates from the bundled ``webpki-roots`` crate. The ``webpki-roots`` are a reliable set of trust roots from Mozilla, and including them in uv improves portability and performance (especially on macOS). However, in some cases, you may want to use the platform's native certificate store, especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's included in your system's certificate store.
        :param no_binary: (experimental) Don't install pre-built wheels. The given packages will be built and installed from source. The resolver will still use pre-built wheels to extract package metadata, if available.
        :param no_binary_package: (experimental) Don't install pre-built wheels for a specific package.
        :param no_build: (experimental) Don't build source distributions. When enabled, resolving will not run arbitrary Python code. The cached wheels of already-built source distributions will be reused, but operations that require building distributions will exit with an error.
        :param no_build_isolation: (experimental) Disable isolation when building source distributions. Assumes that build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_ are already installed.
        :param no_build_isolation_package: (experimental) Disable isolation when building source distributions for a specific package. Assumes that the packages' build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_ are already installed.
        :param no_build_package: (experimental) Don't build source distributions for a specific package.
        :param no_cache: (experimental) Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation.
        :param no_index: (experimental) Ignore all registry indexes (e.g., PyPI), instead relying on direct URL dependencies and those provided via ``--find-links``.
        :param no_sources: (experimental) Ignore the ``tool.uv.sources`` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any local or Git sources.
        :param offline: (experimental) Disable network access, relying only on locally cached data and locally available files.
        :param override_dependencies: (experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.
        :param package: (experimental) Whether the project should be considered a Python package, or a non-package ("virtual") project. Packages are built and installed into the virtual environment in editable mode and thus require a build backend, while virtual projects are *not* built or installed; instead, only their dependencies are included in the virtual environment. Creating a package requires that a ``build-system`` is present in the ``pyproject.toml``, and that the project adheres to a structure that adheres to the build backend's expectations (e.g., a ``src`` layout).
        :param pip: 
        :param prerelease: (experimental) The strategy to use when considering pre-release versions. By default, uv will accept pre-releases for packages that *only* publish pre-releases, along with first-party requirements that contain an explicit pre-release marker in the declared specifiers (``if-necessary-or-explicit``).
        :param preview: (experimental) Whether to enable experimental, preview features.
        :param publish_url: (experimental) The URL for publishing packages to the Python package index (by default: `https://upload.pypi.org/legacy/ <https://upload.pypi.org/legacy/>`_).
        :param pypy_install_mirror: (experimental) Mirror URL to use for downloading managed PyPy installations. By default, managed PyPy installations are downloaded from `downloads.python.org <https://downloads.python.org/>`_. This variable can be set to a mirror URL to use a different source for PyPy installations. The provided URL will replace ``https://downloads.python.org/pypy`` in, e.g., ``https://downloads.python.org/pypy/pypy3.8-v7.3.7-osx64.tar.bz2``. Distributions can be read from a local directory by using the ``file://`` URL scheme.
        :param python_downloads: (experimental) Whether to allow Python downloads.
        :param python_downloads_json_url: (experimental) URL pointing to JSON of custom Python installations. Note that currently, only local paths are supported.
        :param python_install_mirror: (experimental) Mirror URL for downloading managed Python installations. By default, managed Python installations are downloaded from ```python-build-standalone`` <https://github.com/astral-sh/python-build-standalone>`_. This variable can be set to a mirror URL to use a different source for Python installations. The provided URL will replace ``https://github.com/astral-sh/python-build-standalone/releases/download`` in, e.g., ``https://github.com/astral-sh/python-build-standalone/releases/download/20240713/cpython-3.12.4%2B20240713-aarch64-apple-darwin-install_only.tar.gz``. Distributions can be read from a local directory by using the ``file://`` URL scheme.
        :param python_preference: (experimental) Whether to prefer using Python installations that are already present on the system, or those that are downloaded and installed by uv.
        :param reinstall: (experimental) Reinstall all packages, regardless of whether they're already installed. Implies ``refresh``.
        :param reinstall_package: (experimental) Reinstall a specific package, regardless of whether it's already installed. Implies ``refresh-package``.
        :param required_environments: (experimental) A list of environment markers, e.g., `sys_platform == 'darwin'.
        :param required_version: (experimental) Enforce a requirement on the version of uv. If the version of uv does not meet the requirement at runtime, uv will exit with an error. Accepts a `PEP 440 <https://peps.python.org/pep-0440/>`_ specifier, like ``==0.5.0`` or ``>=0.5.0``.
        :param resolution: (experimental) The strategy to use when selecting between the different compatible versions for a given package requirement. By default, uv will use the latest compatible version of each package (``highest``).
        :param sources: (experimental) The sources to use when resolving dependencies. ``tool.uv.sources`` enriches the dependency metadata with additional sources, incorporated during development. A dependency source can be a Git repository, a URL, a local path, or an alternative registry. See `Dependencies <https://docs.astral.sh/uv/concepts/projects/dependencies/>`_ for more.
        :param trusted_publishing: (experimental) Configure trusted publishing. By default, uv checks for trusted publishing when running in a supported environment, but ignores it if it isn't configured. uv's supported environments for trusted publishing include GitHub Actions and GitLab CI/CD.
        :param upgrade: (experimental) Allow package upgrades, ignoring pinned versions in any existing output file.
        :param upgrade_package: (experimental) Allow upgrades for a specific package, ignoring pinned versions in any existing output file. Accepts both standalone package names (``ruff``) and version specifiers (``ruff<0.5.0``).
        :param workspace: (experimental) The workspace definition for the project, if any.

        :stability: experimental
        :schema: UvConfiguration
        '''
        if isinstance(build_backend, dict):
            build_backend = BuildBackendSettings(**build_backend)
        if isinstance(pip, dict):
            pip = PipOptions(**pip)
        if isinstance(workspace, dict):
            workspace = ToolUvWorkspace(**workspace)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc04a41ac6b3f4657c0dca1f873f83584612a895d87f8c6a6b420bd4d56e6612)
            check_type(argname="argument add_bounds", value=add_bounds, expected_type=type_hints["add_bounds"])
            check_type(argname="argument allow_insecure_host", value=allow_insecure_host, expected_type=type_hints["allow_insecure_host"])
            check_type(argname="argument build_backend", value=build_backend, expected_type=type_hints["build_backend"])
            check_type(argname="argument build_constraint_dependencies", value=build_constraint_dependencies, expected_type=type_hints["build_constraint_dependencies"])
            check_type(argname="argument cache_dir", value=cache_dir, expected_type=type_hints["cache_dir"])
            check_type(argname="argument cache_keys", value=cache_keys, expected_type=type_hints["cache_keys"])
            check_type(argname="argument check_url", value=check_url, expected_type=type_hints["check_url"])
            check_type(argname="argument compile_bytecode", value=compile_bytecode, expected_type=type_hints["compile_bytecode"])
            check_type(argname="argument concurrent_builds", value=concurrent_builds, expected_type=type_hints["concurrent_builds"])
            check_type(argname="argument concurrent_downloads", value=concurrent_downloads, expected_type=type_hints["concurrent_downloads"])
            check_type(argname="argument concurrent_installs", value=concurrent_installs, expected_type=type_hints["concurrent_installs"])
            check_type(argname="argument config_settings", value=config_settings, expected_type=type_hints["config_settings"])
            check_type(argname="argument config_settings_package", value=config_settings_package, expected_type=type_hints["config_settings_package"])
            check_type(argname="argument conflicts", value=conflicts, expected_type=type_hints["conflicts"])
            check_type(argname="argument constraint_dependencies", value=constraint_dependencies, expected_type=type_hints["constraint_dependencies"])
            check_type(argname="argument default_groups", value=default_groups, expected_type=type_hints["default_groups"])
            check_type(argname="argument dependency_groups", value=dependency_groups, expected_type=type_hints["dependency_groups"])
            check_type(argname="argument dependency_metadata", value=dependency_metadata, expected_type=type_hints["dependency_metadata"])
            check_type(argname="argument dev_dependencies", value=dev_dependencies, expected_type=type_hints["dev_dependencies"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument exclude_dependencies", value=exclude_dependencies, expected_type=type_hints["exclude_dependencies"])
            check_type(argname="argument exclude_newer", value=exclude_newer, expected_type=type_hints["exclude_newer"])
            check_type(argname="argument exclude_newer_package", value=exclude_newer_package, expected_type=type_hints["exclude_newer_package"])
            check_type(argname="argument extra_build_dependencies", value=extra_build_dependencies, expected_type=type_hints["extra_build_dependencies"])
            check_type(argname="argument extra_build_variables", value=extra_build_variables, expected_type=type_hints["extra_build_variables"])
            check_type(argname="argument extra_index_url", value=extra_index_url, expected_type=type_hints["extra_index_url"])
            check_type(argname="argument find_links", value=find_links, expected_type=type_hints["find_links"])
            check_type(argname="argument fork_strategy", value=fork_strategy, expected_type=type_hints["fork_strategy"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument index_strategy", value=index_strategy, expected_type=type_hints["index_strategy"])
            check_type(argname="argument index_url", value=index_url, expected_type=type_hints["index_url"])
            check_type(argname="argument keyring_provider", value=keyring_provider, expected_type=type_hints["keyring_provider"])
            check_type(argname="argument link_mode", value=link_mode, expected_type=type_hints["link_mode"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument native_tls", value=native_tls, expected_type=type_hints["native_tls"])
            check_type(argname="argument no_binary", value=no_binary, expected_type=type_hints["no_binary"])
            check_type(argname="argument no_binary_package", value=no_binary_package, expected_type=type_hints["no_binary_package"])
            check_type(argname="argument no_build", value=no_build, expected_type=type_hints["no_build"])
            check_type(argname="argument no_build_isolation", value=no_build_isolation, expected_type=type_hints["no_build_isolation"])
            check_type(argname="argument no_build_isolation_package", value=no_build_isolation_package, expected_type=type_hints["no_build_isolation_package"])
            check_type(argname="argument no_build_package", value=no_build_package, expected_type=type_hints["no_build_package"])
            check_type(argname="argument no_cache", value=no_cache, expected_type=type_hints["no_cache"])
            check_type(argname="argument no_index", value=no_index, expected_type=type_hints["no_index"])
            check_type(argname="argument no_sources", value=no_sources, expected_type=type_hints["no_sources"])
            check_type(argname="argument offline", value=offline, expected_type=type_hints["offline"])
            check_type(argname="argument override_dependencies", value=override_dependencies, expected_type=type_hints["override_dependencies"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument pip", value=pip, expected_type=type_hints["pip"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument publish_url", value=publish_url, expected_type=type_hints["publish_url"])
            check_type(argname="argument pypy_install_mirror", value=pypy_install_mirror, expected_type=type_hints["pypy_install_mirror"])
            check_type(argname="argument python_downloads", value=python_downloads, expected_type=type_hints["python_downloads"])
            check_type(argname="argument python_downloads_json_url", value=python_downloads_json_url, expected_type=type_hints["python_downloads_json_url"])
            check_type(argname="argument python_install_mirror", value=python_install_mirror, expected_type=type_hints["python_install_mirror"])
            check_type(argname="argument python_preference", value=python_preference, expected_type=type_hints["python_preference"])
            check_type(argname="argument reinstall", value=reinstall, expected_type=type_hints["reinstall"])
            check_type(argname="argument reinstall_package", value=reinstall_package, expected_type=type_hints["reinstall_package"])
            check_type(argname="argument required_environments", value=required_environments, expected_type=type_hints["required_environments"])
            check_type(argname="argument required_version", value=required_version, expected_type=type_hints["required_version"])
            check_type(argname="argument resolution", value=resolution, expected_type=type_hints["resolution"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument trusted_publishing", value=trusted_publishing, expected_type=type_hints["trusted_publishing"])
            check_type(argname="argument upgrade", value=upgrade, expected_type=type_hints["upgrade"])
            check_type(argname="argument upgrade_package", value=upgrade_package, expected_type=type_hints["upgrade_package"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_bounds is not None:
            self._values["add_bounds"] = add_bounds
        if allow_insecure_host is not None:
            self._values["allow_insecure_host"] = allow_insecure_host
        if build_backend is not None:
            self._values["build_backend"] = build_backend
        if build_constraint_dependencies is not None:
            self._values["build_constraint_dependencies"] = build_constraint_dependencies
        if cache_dir is not None:
            self._values["cache_dir"] = cache_dir
        if cache_keys is not None:
            self._values["cache_keys"] = cache_keys
        if check_url is not None:
            self._values["check_url"] = check_url
        if compile_bytecode is not None:
            self._values["compile_bytecode"] = compile_bytecode
        if concurrent_builds is not None:
            self._values["concurrent_builds"] = concurrent_builds
        if concurrent_downloads is not None:
            self._values["concurrent_downloads"] = concurrent_downloads
        if concurrent_installs is not None:
            self._values["concurrent_installs"] = concurrent_installs
        if config_settings is not None:
            self._values["config_settings"] = config_settings
        if config_settings_package is not None:
            self._values["config_settings_package"] = config_settings_package
        if conflicts is not None:
            self._values["conflicts"] = conflicts
        if constraint_dependencies is not None:
            self._values["constraint_dependencies"] = constraint_dependencies
        if default_groups is not None:
            self._values["default_groups"] = default_groups
        if dependency_groups is not None:
            self._values["dependency_groups"] = dependency_groups
        if dependency_metadata is not None:
            self._values["dependency_metadata"] = dependency_metadata
        if dev_dependencies is not None:
            self._values["dev_dependencies"] = dev_dependencies
        if environments is not None:
            self._values["environments"] = environments
        if exclude_dependencies is not None:
            self._values["exclude_dependencies"] = exclude_dependencies
        if exclude_newer is not None:
            self._values["exclude_newer"] = exclude_newer
        if exclude_newer_package is not None:
            self._values["exclude_newer_package"] = exclude_newer_package
        if extra_build_dependencies is not None:
            self._values["extra_build_dependencies"] = extra_build_dependencies
        if extra_build_variables is not None:
            self._values["extra_build_variables"] = extra_build_variables
        if extra_index_url is not None:
            self._values["extra_index_url"] = extra_index_url
        if find_links is not None:
            self._values["find_links"] = find_links
        if fork_strategy is not None:
            self._values["fork_strategy"] = fork_strategy
        if index is not None:
            self._values["index"] = index
        if index_strategy is not None:
            self._values["index_strategy"] = index_strategy
        if index_url is not None:
            self._values["index_url"] = index_url
        if keyring_provider is not None:
            self._values["keyring_provider"] = keyring_provider
        if link_mode is not None:
            self._values["link_mode"] = link_mode
        if managed is not None:
            self._values["managed"] = managed
        if native_tls is not None:
            self._values["native_tls"] = native_tls
        if no_binary is not None:
            self._values["no_binary"] = no_binary
        if no_binary_package is not None:
            self._values["no_binary_package"] = no_binary_package
        if no_build is not None:
            self._values["no_build"] = no_build
        if no_build_isolation is not None:
            self._values["no_build_isolation"] = no_build_isolation
        if no_build_isolation_package is not None:
            self._values["no_build_isolation_package"] = no_build_isolation_package
        if no_build_package is not None:
            self._values["no_build_package"] = no_build_package
        if no_cache is not None:
            self._values["no_cache"] = no_cache
        if no_index is not None:
            self._values["no_index"] = no_index
        if no_sources is not None:
            self._values["no_sources"] = no_sources
        if offline is not None:
            self._values["offline"] = offline
        if override_dependencies is not None:
            self._values["override_dependencies"] = override_dependencies
        if package is not None:
            self._values["package"] = package
        if pip is not None:
            self._values["pip"] = pip
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if preview is not None:
            self._values["preview"] = preview
        if publish_url is not None:
            self._values["publish_url"] = publish_url
        if pypy_install_mirror is not None:
            self._values["pypy_install_mirror"] = pypy_install_mirror
        if python_downloads is not None:
            self._values["python_downloads"] = python_downloads
        if python_downloads_json_url is not None:
            self._values["python_downloads_json_url"] = python_downloads_json_url
        if python_install_mirror is not None:
            self._values["python_install_mirror"] = python_install_mirror
        if python_preference is not None:
            self._values["python_preference"] = python_preference
        if reinstall is not None:
            self._values["reinstall"] = reinstall
        if reinstall_package is not None:
            self._values["reinstall_package"] = reinstall_package
        if required_environments is not None:
            self._values["required_environments"] = required_environments
        if required_version is not None:
            self._values["required_version"] = required_version
        if resolution is not None:
            self._values["resolution"] = resolution
        if sources is not None:
            self._values["sources"] = sources
        if trusted_publishing is not None:
            self._values["trusted_publishing"] = trusted_publishing
        if upgrade is not None:
            self._values["upgrade"] = upgrade
        if upgrade_package is not None:
            self._values["upgrade_package"] = upgrade_package
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def add_bounds(self) -> typing.Optional["AddBoundsKind"]:
        '''(experimental) The default version specifier when adding a dependency.

        When adding a dependency to the project, if no constraint or URL is provided, a constraint
        is added based on the latest compatible version of the package. By default, a lower bound
        constraint is used, e.g., ``>=1.2.3``.

        When ``--frozen`` is provided, no resolution is performed, and dependencies are always added
        without constraints.

        This option is in preview and may change in any future release.

        :stability: experimental
        :schema: UvConfiguration#add-bounds
        '''
        result = self._values.get("add_bounds")
        return typing.cast(typing.Optional["AddBoundsKind"], result)

    @builtins.property
    def allow_insecure_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Allow insecure connections to host.

        Expects to receive either a hostname (e.g., ``localhost``), a host-port pair (e.g.,
        ``localhost:8080``), or a URL (e.g., ``https://localhost``).

        WARNING: Hosts included in this list will not be verified against the system's certificate
        store. Only use ``--allow-insecure-host`` in a secure network with verified sources, as it
        bypasses SSL verification and could expose you to MITM attacks.

        :stability: experimental
        :schema: UvConfiguration#allow-insecure-host
        '''
        result = self._values.get("allow_insecure_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def build_backend(self) -> typing.Optional["BuildBackendSettings"]:
        '''(experimental) Configuration for the uv build backend.

        Note that those settings only apply when using the ``uv_build`` backend, other build backends
        (such as hatchling) have their own configuration.

        :stability: experimental
        :schema: UvConfiguration#build-backend
        '''
        result = self._values.get("build_backend")
        return typing.cast(typing.Optional["BuildBackendSettings"], result)

    @builtins.property
    def build_constraint_dependencies(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.

        :stability: experimental
        :schema: UvConfiguration#build-constraint-dependencies
        '''
        result = self._values.get("build_constraint_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the cache directory.

        :stability: experimental
        :schema: UvConfiguration#cache-dir
        '''
        result = self._values.get("cache_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_keys(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) The keys to consider when caching builds for the project.

        Cache keys enable you to specify the files or directories that should trigger a rebuild when
        modified. By default, uv will rebuild a project whenever the ``pyproject.toml``, ``setup.py``,
        or ``setup.cfg`` files in the project directory are modified, or if a ``src`` directory is
        added or removed, i.e.::

           cache-keys = [{ file = "pyproject.toml" }, { file = "setup.py" }, { file = "setup.cfg" }, { dir = "src" }]

        As an example: if a project uses dynamic metadata to read its dependencies from a
        ``requirements.txt`` file, you can specify ``cache-keys = [{ file = "requirements.txt" }, { file = "pyproject.toml" }]``
        to ensure that the project is rebuilt whenever the ``requirements.txt`` file is modified (in
        addition to watching the ``pyproject.toml``).

        Globs are supported, following the syntax of the ```glob`` <https://docs.rs/glob/0.3.1/glob/struct.Pattern.html>`_
        crate. For example, to invalidate the cache whenever a ``.toml`` file in the project directory
        or any of its subdirectories is modified, you can specify ``cache-keys = [{ file = "*_/*.toml" }]``.
        Note that the use of globs can be expensive, as uv may need to walk the filesystem to
        determine whether any files have changed.

        Cache keys can also include version control information. For example, if a project uses
        ``setuptools_scm`` to read its version from a Git commit, you can specify ``cache-keys = [{ git = { commit = true }, { file = "pyproject.toml" }]``
        to include the current Git commit hash in the cache key (in addition to the
        ``pyproject.toml``). Git tags are also supported via ``cache-keys = [{ git = { commit = true, tags = true } }]``.

        Cache keys can also include environment variables. For example, if a project relies on
        ``MACOSX_DEPLOYMENT_TARGET`` or other environment variables to determine its behavior, you can
        specify ``cache-keys = [{ env = "MACOSX_DEPLOYMENT_TARGET" }]`` to invalidate the cache
        whenever the environment variable changes.

        Cache keys only affect the project defined by the ``pyproject.toml`` in which they're
        specified (as opposed to, e.g., affecting all members in a workspace), and all paths and
        globs are interpreted as relative to the project directory.

        :stability: experimental
        :schema: UvConfiguration#cache-keys
        '''
        result = self._values.get("cache_keys")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def check_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Check an index URL for existing files to skip duplicate uploads.

        This option allows retrying publishing that failed after only some, but not all files have
        been uploaded, and handles error due to parallel uploads of the same file.

        Before uploading, the index is checked. If the exact same file already exists in the index,
        the file will not be uploaded. If an error occurred during the upload, the index is checked
        again, to handle cases where the identical file was uploaded twice in parallel.

        The exact behavior will vary based on the index. When uploading to PyPI, uploading the same
        file succeeds even without ``--check-url``, while most other indexes error.

        The index must provide one of the supported hashes (SHA-256, SHA-384, or SHA-512).

        :stability: experimental
        :schema: UvConfiguration#check-url
        '''
        result = self._values.get("check_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compile_bytecode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Compile Python files to bytecode after installation.

        By default, uv does not compile Python (``.py``) files to bytecode (``__pycache__/*.pyc``);
        instead, compilation is performed lazily the first time a module is imported. For use-cases
        in which start time is critical, such as CLI applications and Docker containers, this option
        can be enabled to trade longer installation times for faster start times.

        When enabled, uv will process the entire site-packages directory (including packages that
        are not being modified by the current operation) for consistency. Like pip, it will also
        ignore errors.

        :stability: experimental
        :schema: UvConfiguration#compile-bytecode
        '''
        result = self._values.get("compile_bytecode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def concurrent_builds(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of source distributions that uv will build concurrently at any given time.

        Defaults to the number of available CPU cores.

        :default: the number of available CPU cores.

        :stability: experimental
        :schema: UvConfiguration#concurrent-builds
        '''
        result = self._values.get("concurrent_builds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def concurrent_downloads(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of in-flight concurrent downloads that uv will perform at any given time.

        :stability: experimental
        :schema: UvConfiguration#concurrent-downloads
        '''
        result = self._values.get("concurrent_downloads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def concurrent_installs(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of threads used when installing and unzipping packages.

        Defaults to the number of available CPU cores.

        :default: the number of available CPU cores.

        :stability: experimental
        :schema: UvConfiguration#concurrent-installs
        '''
        result = self._values.get("concurrent_installs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def config_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend, specified as ``KEY=VALUE`` pairs.

        :stability: experimental
        :schema: UvConfiguration#config-settings
        '''
        result = self._values.get("config_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def config_settings_package(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]]:
        '''(experimental) Settings to pass to the `PEP 517 <https://peps.python.org/pep-0517/>`_ build backend for specific packages, specified as ``KEY=VALUE`` pairs.

        Accepts a map from package names to string key-value pairs.

        :stability: experimental
        :schema: UvConfiguration#config-settings-package
        '''
        result = self._values.get("config_settings_package")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]], result)

    @builtins.property
    def conflicts(
        self,
    ) -> typing.Optional[typing.List[typing.List["SchemaConflictItem"]]]:
        '''(experimental) A list of sets of conflicting groups or extras.

        :stability: experimental
        :schema: UvConfiguration#conflicts
        '''
        result = self._values.get("conflicts")
        return typing.cast(typing.Optional[typing.List[typing.List["SchemaConflictItem"]]], result)

    @builtins.property
    def constraint_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.

        :stability: experimental
        :schema: UvConfiguration#constraint-dependencies
        '''
        result = self._values.get("constraint_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_groups(self) -> typing.Any:
        '''(experimental) The list of ``dependency-groups`` to install by default.

        Can also be the literal ``"all"`` to default enable all groups.

        :stability: experimental
        :schema: UvConfiguration#default-groups
        '''
        result = self._values.get("default_groups")
        return typing.cast(typing.Any, result)

    @builtins.property
    def dependency_groups(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "DependencyGroupSettings"]]:
        '''(experimental) Additional settings for ``dependency-groups``.

        Currently this can only be used to add ``requires-python`` constraints
        to dependency groups (typically to inform uv that your dev tooling
        has a higher python requirement than your actual project).

        This cannot be used to define dependency groups, use the top-level
        ``[dependency-groups]`` table for that.

        :stability: experimental
        :schema: UvConfiguration#dependency-groups
        '''
        result = self._values.get("dependency_groups")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "DependencyGroupSettings"]], result)

    @builtins.property
    def dependency_metadata(self) -> typing.Optional[typing.List["StaticMetadata"]]:
        '''(experimental) Pre-defined static metadata for dependencies of the project (direct or transitive).

        When
        provided, enables the resolver to use the specified metadata instead of querying the
        registry or building the relevant package from source.

        Metadata should be provided in adherence with the `Metadata 2.3 <https://packaging.python.org/en/latest/specifications/core-metadata/>`_
        standard, though only the following fields are respected:

        - ``name``: The name of the package.
        - (Optional) ``version``: The version of the package. If omitted, the metadata will be applied
          to all versions of the package.
        - (Optional) ``requires-dist``: The dependencies of the package (e.g., ``werkzeug>=0.14``).
        - (Optional) ``requires-python``: The Python version required by the package (e.g., ``>=3.10``).
        - (Optional) ``provides-extra``: The extras provided by the package.

        :stability: experimental
        :schema: UvConfiguration#dependency-metadata
        '''
        result = self._values.get("dependency_metadata")
        return typing.cast(typing.Optional[typing.List["StaticMetadata"]], result)

    @builtins.property
    def dev_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.

        :stability: experimental
        :schema: UvConfiguration#dev-dependencies
        '''
        result = self._values.get("dev_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of environment markers, e.g., ``python_version >= '3.6'``.

        :stability: experimental
        :schema: UvConfiguration#environments
        '''
        result = self._values.get("environments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Package names to exclude, e.g., ``werkzeug``, ``numpy``.

        :stability: experimental
        :schema: UvConfiguration#exclude-dependencies
        '''
        result = self._values.get("exclude_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_newer(self) -> typing.Optional[builtins.str]:
        '''(experimental) Limit candidate packages to those that were uploaded prior to a given point in time.

        Accepts a superset of `RFC 3339 <https://www.rfc-editor.org/rfc/rfc3339.html>`_ (e.g.,
        ``2006-12-02T02:07:43Z``). A full timestamp is required to ensure that the resolver will
        behave consistently across timezones.

        :stability: experimental
        :schema: UvConfiguration#exclude-newer
        '''
        result = self._values.get("exclude_newer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_newer_package(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Limit candidate packages for specific packages to those that were uploaded prior to the given date.

        Accepts package-date pairs in a dictionary format.

        :stability: experimental
        :schema: UvConfiguration#exclude-newer-package
        '''
        result = self._values.get("exclude_newer_package")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def extra_build_dependencies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]]:
        '''(experimental) Additional build dependencies for packages.

        This allows extending the PEP 517 build environment for the project's dependencies with
        additional packages. This is useful for packages that assume the presence of packages like
        ``pip``, and do not declare them as build dependencies.

        :stability: experimental
        :schema: UvConfiguration#extra-build-dependencies
        '''
        result = self._values.get("extra_build_dependencies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]], result)

    @builtins.property
    def extra_build_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) Extra environment variables to set when building certain packages.

        Environment variables will be added to the environment when building the
        specified packages.

        :stability: experimental
        :schema: UvConfiguration#extra-build-variables
        '''
        result = self._values.get("extra_build_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def extra_index_url(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Extra URLs of package indexes to use, in addition to ``--index-url``.

        Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_
        (the simple repository API), or a local directory laid out in the same format.

        All indexes provided via this flag take priority over the index specified by
        ```index_url`` <#index-url>`_ or ```index`` <#index>`_ with ``default = true``. When multiple indexes
        are provided, earlier values take priority.

        To control uv's resolution strategy when multiple indexes are present, see
        ```index_strategy`` <#index-strategy>`_.

        (Deprecated: use ``index`` instead.)

        :stability: experimental
        :schema: UvConfiguration#extra-index-url
        '''
        result = self._values.get("extra_index_url")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def find_links(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Locations to search for candidate distributions, in addition to those found in the registry indexes.

        If a path, the target must be a directory that contains packages as wheel files (``.whl``) or
        source distributions (e.g., ``.tar.gz`` or ``.zip``) at the top level.

        If a URL, the page must contain a flat list of links to package files adhering to the
        formats described above.

        :stability: experimental
        :schema: UvConfiguration#find-links
        '''
        result = self._values.get("find_links")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fork_strategy(self) -> typing.Optional["ForkStrategy"]:
        '''(experimental) The strategy to use when selecting multiple versions of a given package across Python versions and platforms.

        By default, uv will optimize for selecting the latest version of each package for each
        supported Python version (``requires-python``), while minimizing the number of selected
        versions across platforms.

        Under ``fewest``, uv will minimize the number of selected versions for each package,
        preferring older versions that are compatible with a wider range of supported Python
        versions or platforms.

        :stability: experimental
        :schema: UvConfiguration#fork-strategy
        '''
        result = self._values.get("fork_strategy")
        return typing.cast(typing.Optional["ForkStrategy"], result)

    @builtins.property
    def index(self) -> typing.Optional[typing.List["Index"]]:
        '''(experimental) The indexes to use when resolving dependencies.

        Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_
        (the simple repository API), or a local directory laid out in the same format.

        Indexes are considered in the order in which they're defined, such that the first-defined
        index has the highest priority. Further, the indexes provided by this setting are given
        higher priority than any indexes specified via ```index_url`` <#index-url>`_ or
        ```extra_index_url`` <#extra-index-url>`_. uv will only consider the first index that contains
        a given package, unless an alternative `index strategy <#index-strategy>`_ is specified.

        If an index is marked as ``explicit = true``, it will be used exclusively for the
        dependencies that select it explicitly via ``[tool.uv.sources]``, as in::

           [[tool.uv.index]]
           name = "pytorch"
           url = "https://download.pytorch.org/whl/cu121"
           explicit = true

           [tool.uv.sources]
           torch = { index = "pytorch" }

        If an index is marked as ``default = true``, it will be moved to the end of the prioritized list, such that it is
        given the lowest priority when resolving packages. Additionally, marking an index as default will disable the
        PyPI default index.

        :stability: experimental
        :schema: UvConfiguration#index
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[typing.List["Index"]], result)

    @builtins.property
    def index_strategy(self) -> typing.Optional["IndexStrategy"]:
        '''(experimental) The strategy to use when resolving against multiple index URLs.

        By default, uv will stop at the first index on which a given package is available, and
        limit resolutions to those present on that first index (``first-index``). This prevents
        "dependency confusion" attacks, whereby an attacker can upload a malicious package under the
        same name to an alternate index.

        :stability: experimental
        :schema: UvConfiguration#index-strategy
        '''
        result = self._values.get("index_strategy")
        return typing.cast(typing.Optional["IndexStrategy"], result)

    @builtins.property
    def index_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL of the Python package index (by default: `https://pypi.org/simple <https://pypi.org/simple>`_).

        Accepts either a repository compliant with `PEP 503 <https://peps.python.org/pep-0503/>`_
        (the simple repository API), or a local directory laid out in the same format.

        The index provided by this setting is given lower priority than any indexes specified via
        ```extra_index_url`` <#extra-index-url>`_ or ```index`` <#index>`_.

        (Deprecated: use ``index`` instead.)

        :stability: experimental
        :schema: UvConfiguration#index-url
        '''
        result = self._values.get("index_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyring_provider(self) -> typing.Optional["KeyringProviderType"]:
        '''(experimental) Attempt to use ``keyring`` for authentication for index URLs.

        At present, only ``--keyring-provider subprocess`` is supported, which configures uv to
        use the ``keyring`` CLI to handle authentication.

        :stability: experimental
        :schema: UvConfiguration#keyring-provider
        '''
        result = self._values.get("keyring_provider")
        return typing.cast(typing.Optional["KeyringProviderType"], result)

    @builtins.property
    def link_mode(self) -> typing.Optional["LinkMode"]:
        '''(experimental) The method to use when installing packages from the global cache.

        Defaults to ``clone`` (also known as Copy-on-Write) on macOS, and ``hardlink`` on Linux and
        Windows.

        WARNING: The use of symlink link mode is discouraged, as they create tight coupling between
        the cache and the target environment. For example, clearing the cache (``uv cache clean``)
        will break all installed packages by way of removing the underlying source files. Use
        symlinks with caution.

        :default: clone``(also known as Copy-on-Write) on macOS, and``hardlink` on Linux and

        :stability: experimental
        :schema: UvConfiguration#link-mode
        '''
        result = self._values.get("link_mode")
        return typing.cast(typing.Optional["LinkMode"], result)

    @builtins.property
    def managed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the project is managed by uv.

        If ``false``, uv will ignore the project when
        ``uv run`` is invoked.

        :stability: experimental
        :schema: UvConfiguration#managed
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def native_tls(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to load TLS certificates from the platform's native certificate store.

        By default, uv loads certificates from the bundled ``webpki-roots`` crate. The
        ``webpki-roots`` are a reliable set of trust roots from Mozilla, and including them in uv
        improves portability and performance (especially on macOS).

        However, in some cases, you may want to use the platform's native certificate store,
        especially if you're relying on a corporate trust root (e.g., for a mandatory proxy) that's
        included in your system's certificate store.

        :stability: experimental
        :schema: UvConfiguration#native-tls
        '''
        result = self._values.get("native_tls")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_binary(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Don't install pre-built wheels.

        The given packages will be built and installed from source. The resolver will still use
        pre-built wheels to extract package metadata, if available.

        :stability: experimental
        :schema: UvConfiguration#no-binary
        '''
        result = self._values.get("no_binary")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_binary_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Don't install pre-built wheels for a specific package.

        :stability: experimental
        :schema: UvConfiguration#no-binary-package
        '''
        result = self._values.get("no_binary_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Don't build source distributions.

        When enabled, resolving will not run arbitrary Python code. The cached wheels of
        already-built source distributions will be reused, but operations that require building
        distributions will exit with an error.

        :stability: experimental
        :schema: UvConfiguration#no-build
        '''
        result = self._values.get("no_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_build_isolation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Disable isolation when building source distributions.

        Assumes that build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_
        are already installed.

        :stability: experimental
        :schema: UvConfiguration#no-build-isolation
        '''
        result = self._values.get("no_build_isolation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_build_isolation_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Disable isolation when building source distributions for a specific package.

        Assumes that the packages' build dependencies specified by `PEP 518 <https://peps.python.org/pep-0518/>`_
        are already installed.

        :stability: experimental
        :schema: UvConfiguration#no-build-isolation-package
        '''
        result = self._values.get("no_build_isolation_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_build_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Don't build source distributions for a specific package.

        :stability: experimental
        :schema: UvConfiguration#no-build-package
        '''
        result = self._values.get("no_build_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def no_cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation.

        :stability: experimental
        :schema: UvConfiguration#no-cache
        '''
        result = self._values.get("no_cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_index(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignore all registry indexes (e.g., PyPI), instead relying on direct URL dependencies and those provided via ``--find-links``.

        :stability: experimental
        :schema: UvConfiguration#no-index
        '''
        result = self._values.get("no_index")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_sources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignore the ``tool.uv.sources`` table when resolving dependencies. Used to lock against the standards-compliant, publishable package metadata, as opposed to using any local or Git sources.

        :stability: experimental
        :schema: UvConfiguration#no-sources
        '''
        result = self._values.get("no_sources")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def offline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Disable network access, relying only on locally cached data and locally available files.

        :stability: experimental
        :schema: UvConfiguration#offline
        '''
        result = self._values.get("offline")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def override_dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) PEP 508-style requirements, e.g., ``ruff==0.5.0``, or ``ruff @ https://...``.

        :stability: experimental
        :schema: UvConfiguration#override-dependencies
        '''
        result = self._values.get("override_dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def package(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the project should be considered a Python package, or a non-package ("virtual") project.

        Packages are built and installed into the virtual environment in editable mode and thus
        require a build backend, while virtual projects are *not* built or installed; instead, only
        their dependencies are included in the virtual environment.

        Creating a package requires that a ``build-system`` is present in the ``pyproject.toml``, and
        that the project adheres to a structure that adheres to the build backend's expectations
        (e.g., a ``src`` layout).

        :stability: experimental
        :schema: UvConfiguration#package
        '''
        result = self._values.get("package")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pip(self) -> typing.Optional["PipOptions"]:
        '''
        :stability: experimental
        :schema: UvConfiguration#pip
        '''
        result = self._values.get("pip")
        return typing.cast(typing.Optional["PipOptions"], result)

    @builtins.property
    def prerelease(self) -> typing.Optional["PrereleaseMode"]:
        '''(experimental) The strategy to use when considering pre-release versions.

        By default, uv will accept pre-releases for packages that *only* publish pre-releases,
        along with first-party requirements that contain an explicit pre-release marker in the
        declared specifiers (``if-necessary-or-explicit``).

        :stability: experimental
        :schema: UvConfiguration#prerelease
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional["PrereleaseMode"], result)

    @builtins.property
    def preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable experimental, preview features.

        :stability: experimental
        :schema: UvConfiguration#preview
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL for publishing packages to the Python package index (by default: `https://upload.pypi.org/legacy/ <https://upload.pypi.org/legacy/>`_).

        :stability: experimental
        :schema: UvConfiguration#publish-url
        '''
        result = self._values.get("publish_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pypy_install_mirror(self) -> typing.Optional[builtins.str]:
        '''(experimental) Mirror URL to use for downloading managed PyPy installations.

        By default, managed PyPy installations are downloaded from `downloads.python.org <https://downloads.python.org/>`_.
        This variable can be set to a mirror URL to use a different source for PyPy installations.
        The provided URL will replace ``https://downloads.python.org/pypy`` in, e.g., ``https://downloads.python.org/pypy/pypy3.8-v7.3.7-osx64.tar.bz2``.

        Distributions can be read from a
        local directory by using the ``file://`` URL scheme.

        :stability: experimental
        :schema: UvConfiguration#pypy-install-mirror
        '''
        result = self._values.get("pypy_install_mirror")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_downloads(self) -> typing.Optional["PythonDownloads"]:
        '''(experimental) Whether to allow Python downloads.

        :stability: experimental
        :schema: UvConfiguration#python-downloads
        '''
        result = self._values.get("python_downloads")
        return typing.cast(typing.Optional["PythonDownloads"], result)

    @builtins.property
    def python_downloads_json_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL pointing to JSON of custom Python installations.

        Note that currently, only local paths are supported.

        :stability: experimental
        :schema: UvConfiguration#python-downloads-json-url
        '''
        result = self._values.get("python_downloads_json_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_install_mirror(self) -> typing.Optional[builtins.str]:
        '''(experimental) Mirror URL for downloading managed Python installations.

        By default, managed Python installations are downloaded from ```python-build-standalone`` <https://github.com/astral-sh/python-build-standalone>`_.
        This variable can be set to a mirror URL to use a different source for Python installations.
        The provided URL will replace ``https://github.com/astral-sh/python-build-standalone/releases/download`` in, e.g., ``https://github.com/astral-sh/python-build-standalone/releases/download/20240713/cpython-3.12.4%2B20240713-aarch64-apple-darwin-install_only.tar.gz``.

        Distributions can be read from a local directory by using the ``file://`` URL scheme.

        :stability: experimental
        :schema: UvConfiguration#python-install-mirror
        '''
        result = self._values.get("python_install_mirror")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_preference(self) -> typing.Optional["PythonPreference"]:
        '''(experimental) Whether to prefer using Python installations that are already present on the system, or those that are downloaded and installed by uv.

        :stability: experimental
        :schema: UvConfiguration#python-preference
        '''
        result = self._values.get("python_preference")
        return typing.cast(typing.Optional["PythonPreference"], result)

    @builtins.property
    def reinstall(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Reinstall all packages, regardless of whether they're already installed.

        Implies ``refresh``.

        :stability: experimental
        :schema: UvConfiguration#reinstall
        '''
        result = self._values.get("reinstall")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reinstall_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Reinstall a specific package, regardless of whether it's already installed.

        Implies
        ``refresh-package``.

        :stability: experimental
        :schema: UvConfiguration#reinstall-package
        '''
        result = self._values.get("reinstall_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required_environments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of environment markers, e.g., `sys_platform == 'darwin'.

        :stability: experimental
        :schema: UvConfiguration#required-environments
        '''
        result = self._values.get("required_environments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforce a requirement on the version of uv.

        If the version of uv does not meet the requirement at runtime, uv will exit
        with an error.

        Accepts a `PEP 440 <https://peps.python.org/pep-0440/>`_ specifier, like ``==0.5.0`` or ``>=0.5.0``.

        :stability: experimental
        :schema: UvConfiguration#required-version
        '''
        result = self._values.get("required_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolution(self) -> typing.Optional["ResolutionMode"]:
        '''(experimental) The strategy to use when selecting between the different compatible versions for a given package requirement.

        By default, uv will use the latest compatible version of each package (``highest``).

        :stability: experimental
        :schema: UvConfiguration#resolution
        '''
        result = self._values.get("resolution")
        return typing.cast(typing.Optional["ResolutionMode"], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]]:
        '''(experimental) The sources to use when resolving dependencies.

        ``tool.uv.sources`` enriches the dependency metadata with additional sources, incorporated
        during development. A dependency source can be a Git repository, a URL, a local path, or an
        alternative registry.

        See `Dependencies <https://docs.astral.sh/uv/concepts/projects/dependencies/>`_ for more.

        :stability: experimental
        :schema: UvConfiguration#sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]], result)

    @builtins.property
    def trusted_publishing(self) -> typing.Optional["TrustedPublishing"]:
        '''(experimental) Configure trusted publishing.

        By default, uv checks for trusted publishing when running in a supported environment, but
        ignores it if it isn't configured.

        uv's supported environments for trusted publishing include GitHub Actions and GitLab CI/CD.

        :stability: experimental
        :schema: UvConfiguration#trusted-publishing
        '''
        result = self._values.get("trusted_publishing")
        return typing.cast(typing.Optional["TrustedPublishing"], result)

    @builtins.property
    def upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow package upgrades, ignoring pinned versions in any existing output file.

        :stability: experimental
        :schema: UvConfiguration#upgrade
        '''
        result = self._values.get("upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upgrade_package(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Allow upgrades for a specific package, ignoring pinned versions in any existing output file.

        Accepts both standalone package names (``ruff``) and version specifiers (``ruff<0.5.0``).

        :stability: experimental
        :schema: UvConfiguration#upgrade-package
        '''
        result = self._values.get("upgrade_package")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workspace(self) -> typing.Optional["ToolUvWorkspace"]:
        '''(experimental) The workspace definition for the project, if any.

        :stability: experimental
        :schema: UvConfiguration#workspace
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional["ToolUvWorkspace"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UvConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.python.uvConfig.WheelDataIncludes",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "headers": "headers",
        "platlib": "platlib",
        "purelib": "purelib",
        "scripts": "scripts",
    },
)
class WheelDataIncludes:
    def __init__(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        headers: typing.Optional[builtins.str] = None,
        platlib: typing.Optional[builtins.str] = None,
        purelib: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Data includes for wheels.

        See ``BuildBackendSettings::data``.

        :param data: 
        :param headers: 
        :param platlib: 
        :param purelib: 
        :param scripts: 

        :stability: experimental
        :schema: WheelDataIncludes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be987521727f135b7dbd7d35da55b57aed2eaf5c64a6c79a5c0e3283d6277aa)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument platlib", value=platlib, expected_type=type_hints["platlib"])
            check_type(argname="argument purelib", value=purelib, expected_type=type_hints["purelib"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data
        if headers is not None:
            self._values["headers"] = headers
        if platlib is not None:
            self._values["platlib"] = platlib
        if purelib is not None:
            self._values["purelib"] = purelib
        if scripts is not None:
            self._values["scripts"] = scripts

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: WheelDataIncludes#data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: WheelDataIncludes#headers
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platlib(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: WheelDataIncludes#platlib
        '''
        result = self._values.get("platlib")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purelib(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: WheelDataIncludes#purelib
        '''
        result = self._values.get("purelib")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scripts(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        :schema: WheelDataIncludes#scripts
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WheelDataIncludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddBoundsKind",
    "AnnotationStyle",
    "AuthPolicy",
    "BuildBackendSettings",
    "DependencyGroupSettings",
    "ForkStrategy",
    "Index",
    "IndexCacheControl",
    "IndexFormat",
    "IndexStrategy",
    "KeyringProviderType",
    "LinkMode",
    "PipGroupName",
    "PipOptions",
    "PrereleaseMode",
    "PythonDownloads",
    "PythonPreference",
    "ResolutionMode",
    "SchemaConflictItem",
    "StaticMetadata",
    "TargetTriple",
    "ToolUvWorkspace",
    "TorchMode",
    "TrustedPublishing",
    "UvConfiguration",
    "WheelDataIncludes",
]

publication.publish()

def _typecheckingstub__e8edb4b678376787a735855010994c917f5562ec1c18ac7700c5f21373aa27eb(
    *,
    data: typing.Optional[typing.Union[WheelDataIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
    default_excludes: typing.Optional[builtins.bool] = None,
    module_name: typing.Any = None,
    module_root: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.bool] = None,
    source_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    wheel_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd491f584ee7212fb2c3697548f60d044362ecd866f97a41a269a2f581e15d60(
    *,
    requires_python: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075e56d66f36a514ad1fafdc5b03260161a84fb1d2c5ce8069204ee4b239111d(
    *,
    url: builtins.str,
    authenticate: typing.Optional[AuthPolicy] = None,
    cache_control: typing.Optional[typing.Union[IndexCacheControl, typing.Dict[builtins.str, typing.Any]]] = None,
    default: typing.Optional[builtins.bool] = None,
    explicit: typing.Optional[builtins.bool] = None,
    format: typing.Optional[IndexFormat] = None,
    ignore_error_codes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    name: typing.Optional[builtins.str] = None,
    publish_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadc80a7c1e7527e1cc3946322c9b1d4206a4fd507f1046ab1298219615cd172(
    *,
    api: typing.Optional[builtins.str] = None,
    files: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61408a230f83617e8924d0c29339bd155df27bf401eeae828f9b19222e91953d(
    *,
    name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945d6160c5542e9b39ed19c707a1b0e7ee5ea909cc55041a32f162098f3853e7(
    *,
    all_extras: typing.Optional[builtins.bool] = None,
    allow_empty_requirements: typing.Optional[builtins.bool] = None,
    annotation_style: typing.Optional[AnnotationStyle] = None,
    break_system_packages: typing.Optional[builtins.bool] = None,
    compile_bytecode: typing.Optional[builtins.bool] = None,
    config_settings: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    config_settings_package: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]] = None,
    custom_compile_command: typing.Optional[builtins.str] = None,
    dependency_metadata: typing.Optional[typing.Sequence[typing.Union[StaticMetadata, typing.Dict[builtins.str, typing.Any]]]] = None,
    emit_build_options: typing.Optional[builtins.bool] = None,
    emit_find_links: typing.Optional[builtins.bool] = None,
    emit_index_annotation: typing.Optional[builtins.bool] = None,
    emit_index_url: typing.Optional[builtins.bool] = None,
    emit_marker_expression: typing.Optional[builtins.bool] = None,
    exclude_newer: typing.Optional[builtins.str] = None,
    exclude_newer_package: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    extra_build_dependencies: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
    extra_build_variables: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    extra_index_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    find_links: typing.Optional[typing.Sequence[builtins.str]] = None,
    fork_strategy: typing.Optional[ForkStrategy] = None,
    generate_hashes: typing.Optional[builtins.bool] = None,
    group: typing.Optional[typing.Sequence[typing.Union[PipGroupName, typing.Dict[builtins.str, typing.Any]]]] = None,
    index_strategy: typing.Optional[IndexStrategy] = None,
    index_url: typing.Optional[builtins.str] = None,
    keyring_provider: typing.Optional[KeyringProviderType] = None,
    link_mode: typing.Optional[LinkMode] = None,
    no_annotate: typing.Optional[builtins.bool] = None,
    no_binary: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_build: typing.Optional[builtins.bool] = None,
    no_build_isolation: typing.Optional[builtins.bool] = None,
    no_build_isolation_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_deps: typing.Optional[builtins.bool] = None,
    no_emit_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_header: typing.Optional[builtins.bool] = None,
    no_index: typing.Optional[builtins.bool] = None,
    no_sources: typing.Optional[builtins.bool] = None,
    no_strip_extras: typing.Optional[builtins.bool] = None,
    no_strip_markers: typing.Optional[builtins.bool] = None,
    only_binary: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_file: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    prerelease: typing.Optional[PrereleaseMode] = None,
    python: typing.Optional[builtins.str] = None,
    python_platform: typing.Optional[TargetTriple] = None,
    python_version: typing.Optional[builtins.str] = None,
    reinstall: typing.Optional[builtins.bool] = None,
    reinstall_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_hashes: typing.Optional[builtins.bool] = None,
    resolution: typing.Optional[ResolutionMode] = None,
    strict: typing.Optional[builtins.bool] = None,
    system: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.str] = None,
    torch_backend: typing.Optional[TorchMode] = None,
    universal: typing.Optional[builtins.bool] = None,
    upgrade: typing.Optional[builtins.bool] = None,
    upgrade_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify_hashes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b46b2b7c2469ab6410378ad3f31dbc8765e96c46f61c3c1491291cc61b80c51(
    *,
    extra: typing.Optional[builtins.str] = None,
    group: typing.Optional[builtins.str] = None,
    package: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95950a1bc1c16c14e86122ea689404f253b5e734ee94d174a1c7d2cb8d2e1b13(
    *,
    name: builtins.str,
    provides_extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    requires_dist: typing.Optional[typing.Sequence[builtins.str]] = None,
    requires_python: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104c3e675eb0f61a5c9f7a762fb9754ae023eb9e0db4e9434a1631ad9e3119bb(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc04a41ac6b3f4657c0dca1f873f83584612a895d87f8c6a6b420bd4d56e6612(
    *,
    add_bounds: typing.Optional[AddBoundsKind] = None,
    allow_insecure_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    build_backend: typing.Optional[typing.Union[BuildBackendSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    build_constraint_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_dir: typing.Optional[builtins.str] = None,
    cache_keys: typing.Optional[typing.Sequence[typing.Any]] = None,
    check_url: typing.Optional[builtins.str] = None,
    compile_bytecode: typing.Optional[builtins.bool] = None,
    concurrent_builds: typing.Optional[jsii.Number] = None,
    concurrent_downloads: typing.Optional[jsii.Number] = None,
    concurrent_installs: typing.Optional[jsii.Number] = None,
    config_settings: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    config_settings_package: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]] = None,
    conflicts: typing.Optional[typing.Sequence[typing.Sequence[typing.Union[SchemaConflictItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
    constraint_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_groups: typing.Any = None,
    dependency_groups: typing.Optional[typing.Mapping[builtins.str, typing.Union[DependencyGroupSettings, typing.Dict[builtins.str, typing.Any]]]] = None,
    dependency_metadata: typing.Optional[typing.Sequence[typing.Union[StaticMetadata, typing.Dict[builtins.str, typing.Any]]]] = None,
    dev_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_newer: typing.Optional[builtins.str] = None,
    exclude_newer_package: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra_build_dependencies: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
    extra_build_variables: typing.Optional[typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    extra_index_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    find_links: typing.Optional[typing.Sequence[builtins.str]] = None,
    fork_strategy: typing.Optional[ForkStrategy] = None,
    index: typing.Optional[typing.Sequence[typing.Union[Index, typing.Dict[builtins.str, typing.Any]]]] = None,
    index_strategy: typing.Optional[IndexStrategy] = None,
    index_url: typing.Optional[builtins.str] = None,
    keyring_provider: typing.Optional[KeyringProviderType] = None,
    link_mode: typing.Optional[LinkMode] = None,
    managed: typing.Optional[builtins.bool] = None,
    native_tls: typing.Optional[builtins.bool] = None,
    no_binary: typing.Optional[builtins.bool] = None,
    no_binary_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_build: typing.Optional[builtins.bool] = None,
    no_build_isolation: typing.Optional[builtins.bool] = None,
    no_build_isolation_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_build_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    no_cache: typing.Optional[builtins.bool] = None,
    no_index: typing.Optional[builtins.bool] = None,
    no_sources: typing.Optional[builtins.bool] = None,
    offline: typing.Optional[builtins.bool] = None,
    override_dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    package: typing.Optional[builtins.bool] = None,
    pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    prerelease: typing.Optional[PrereleaseMode] = None,
    preview: typing.Optional[builtins.bool] = None,
    publish_url: typing.Optional[builtins.str] = None,
    pypy_install_mirror: typing.Optional[builtins.str] = None,
    python_downloads: typing.Optional[PythonDownloads] = None,
    python_downloads_json_url: typing.Optional[builtins.str] = None,
    python_install_mirror: typing.Optional[builtins.str] = None,
    python_preference: typing.Optional[PythonPreference] = None,
    reinstall: typing.Optional[builtins.bool] = None,
    reinstall_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_version: typing.Optional[builtins.str] = None,
    resolution: typing.Optional[ResolutionMode] = None,
    sources: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Any]]] = None,
    trusted_publishing: typing.Optional[TrustedPublishing] = None,
    upgrade: typing.Optional[builtins.bool] = None,
    upgrade_package: typing.Optional[typing.Sequence[builtins.str]] = None,
    workspace: typing.Optional[typing.Union[ToolUvWorkspace, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be987521727f135b7dbd7d35da55b57aed2eaf5c64a6c79a5c0e3283d6277aa(
    *,
    data: typing.Optional[builtins.str] = None,
    headers: typing.Optional[builtins.str] = None,
    platlib: typing.Optional[builtins.str] = None,
    purelib: typing.Optional[builtins.str] = None,
    scripts: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
