import zipfile

import pytest

def _make_archive(filename, root_is_purelib=None):
    metadata = (
        b'Metadata-Version: 2.0\n'
        b'Name: mypackage\n'
        b'Version: 0.1\n')

    with zipfile.ZipFile(filename, 'w') as zipf:
        zipf.writestr('mypackage-0.1.dist-info/METADATA', metadata)
        if root_is_purelib is not None:
            zipf.writestr(
                'mypackage-0.1.dist-info/WHEEL',
                'Wheel-Version: 1.0\n'
                'Root-Is-Purelib: %s\n' % ('true' if root_is_purelib
                                           else 'false'))

def _make_wheel(filename, metadata_version=None):
    from pkginfo.wheel import Wheel

    if metadata_version is not None:
        return Wheel(filename, metadata_version=metadata_version)
    else:
        return Wheel(filename)

def _checkSample(wheel, filename):
    assert(wheel.filename == filename)
    assert(wheel.name == 'mypackage')
    assert(wheel.version == '0.1')
    assert(wheel.keywords == None)

def _checkClassifiers(wheel):
    assert(
        list(wheel.classifiers) == [
            'Development Status :: 4 - Beta',
            'Environment :: Console (Text Based)',
        ]
    )
    assert(list(wheel.supported_platforms) == [])

def test_wheel_ctor_w_bogus_filename(examples_dir):
    filename = str(examples_dir / 'nonesuch-0.1-any.whl')

    with pytest.raises(ValueError):
        _make_wheel(filename)

def test_wheel_ctor_w_non_wheel(archive):
    filename = str(archive)

    with pytest.raises(ValueError):
        _make_wheel(filename)

def test_wheel_ctor_wo_dist_info(examples_dir):
    filename = str(examples_dir / 'nodistinfo-0.1-any.whl')

    with pytest.raises(ValueError):
        _make_wheel(filename)

def test_wheel_ctor_w_valid_wheel(test_wheel):
    filename = str(test_wheel)

    wheel = _make_wheel(filename)

    assert(wheel.metadata_version == '2.0')
    _checkSample(wheel, filename)
    _checkClassifiers(wheel)

def test_wheel_ctor_w_valid_wheel_and_metadata_version(test_wheel):
    filename = str(test_wheel)

    wheel = _make_wheel(filename, metadata_version='1.1')

    assert(wheel.metadata_version == '1.1')
    _checkSample(wheel, filename)
    _checkClassifiers(wheel)

def test_wheel_ctor_w_valid_wheel_w_description_header(examples_dir):
    filename = str(examples_dir / 'distlib-0.3.1-py2.py3-none-any.whl')

    wheel = _make_wheel(filename, metadata_version='1.1')

    assert(wheel.metadata_version == '1.1')
    assert(wheel.description)

def test_wheel_ctor_w_valid_wheel_w_description_body(examples_dir):
    filename = str(examples_dir / 'testlp1974172-0.0.0-py3-none-any.whl')

    wheel = _make_wheel(filename, metadata_version='2.1')

    assert(wheel.metadata_version == '2.1')
    assert(
        "https://bugs.launchpad.net/pkginfo/+bug/1885458" in
        wheel.description
    )

def test_wheel_ctor_w_installed_wheel(examples_dir):
    filename = str(examples_dir / 'mypackage-0.1.dist-info')

    wheel = _make_wheel(filename)

    assert(wheel.metadata_version == '2.0')
    _checkSample(wheel, filename)
    _checkClassifiers(wheel)

def test_wheel_filename_tags_w_valid_wheel(test_wheel):
    wheel = _make_wheel(str(test_wheel))

    # LP #2015657 / GH #11
    assert(wheel.python_tag == 'cp26')
    assert(wheel.abi_tag == 'none')
    assert(wheel.platform_tag == 'linux_x86_64')
    assert(wheel.build_tag == None)

def test_wheel_purelib_w_platlib_wheel(test_wheel):
    wheel = _make_wheel(str(test_wheel))

    assert(wheel.purelib is False)   # from the archive's 'WHEEL' file

def test_wheel_purelib_w_pure_wheel(examples_dir):
    filename = str(examples_dir / 'distlib-0.3.1-py2.py3-none-any.whl')

    wheel = _make_wheel(filename)

    assert(wheel.python_tag == 'py2.py3')
    assert(wheel.platform_tag == 'any')
    assert(wheel.purelib is True)

def test_wheel_filename_tags_w_build_tag(tmp_path):
    filename = str(tmp_path /
                   'mypackage-0.1-1-cp39-cp39-'
                   'manylinux1_x86_64.manylinux1_i686.whl')

    _make_archive(filename, root_is_purelib=False)

    wheel = _make_wheel(filename)

    assert(wheel.python_tag == 'cp39')
    assert(wheel.abi_tag == 'cp39')
    assert(wheel.platform_tag == 'manylinux1_x86_64.manylinux1_i686')
    assert(wheel.build_tag == '1')
    assert(wheel.purelib is False)

def test_wheel_filename_tags_w_unparseable(examples_dir):
    # Unpacked .dist-info directories don't carry filename tags, and the
    # fixture lacks a 'WHEEL' file.
    filename = str(examples_dir / 'mypackage-0.1.dist-info')

    wheel = _make_wheel(filename)

    assert(wheel.python_tag == None)
    assert(wheel.build_tag == None)
    assert(wheel.purelib == None)

def test_wheel_ctor_w_valid_installed_wheel(temp_dir, test_wheel):

    filename = str(test_wheel)

    with zipfile.ZipFile(filename) as zipf:
        zipf.extractall(temp_dir)

    installed_filename = temp_dir / 'mypackage-0.1.dist-info'
    wheel = _make_wheel(str(installed_filename))

    assert(wheel.metadata_version == '2.0')
    _checkSample(wheel, str(installed_filename))
    _checkClassifiers(wheel)
