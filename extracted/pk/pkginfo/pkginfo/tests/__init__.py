# requirements

import os

_DODGY_PKGINFO = os.path.join(
    os.path.dirname(__file__),
    'dodgy', 'namespaced.dodgy-0.1.egg-info', 'PKG-INFO')


def _fixture_pkginfo():
    from email.parser import Parser

    with open(_DODGY_PKGINFO) as fp:
        return Parser().parse(fp)


def _checkSample(_, installed):
    # 'dodgy' fixture carries a static snapshot of this project's own
    # metadata (LP #2098742):  cross-check the parsed values against
    # the checked-in file itself, rather than against the live package.
    expected = _fixture_pkginfo()

    assert(installed.version == expected['Version'])
    assert(installed.name == expected['Name'])
    assert(installed.keywords == expected['Keywords'])
    assert(list(installed.supported_platforms) == [])


def _checkDevelop(_, installed):
    # 'Develop' points at this project's own (live) egg-info, regenerated
    # with the current version by any build;  cross-check against the
    # installed distribution's recorded version.
    from importlib import metadata as importlib_metadata

    version = importlib_metadata.version('pkginfo')
    assert(installed.version == version)
    assert(installed.name == 'pkginfo')
    assert(installed.keywords == 'distribution sdist installed metadata')
    assert(list(installed.supported_platforms) == [])

def _checkClassifiers(_, installed):
    assert(list(installed.classifiers) == [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
    ])


def _defaultMetadataVersion():
    # Cross-check against the sample's own metadata, rather than a
    # hardcoded literal (LP #2103804).  See GH #10.
    return _fixture_pkginfo()['Metadata-Version']
