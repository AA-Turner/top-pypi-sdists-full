import os, sys, platform, subprocess, tempfile
import urllib.request

_PYROSETTA_EAST_MIRROR_ = 'https://graylab.jhu.edu/download/PyRosetta4/archive/release'
_PYROSETTA_WEST_MIRROR_ = 'https://west.rosettacommons.org/pyrosetta/release/release'
_PYROSETTA_RELEASES_URLS_ = [_PYROSETTA_WEST_MIRROR_, _PYROSETTA_EAST_MIRROR_]


def get_pyrosetta_os():
    if sys.platform.startswith("linux"):
        if platform.uname().machine == 'aarch64': r = 'aarch64'
        else:
            #r = 'ubuntu' if os.path.isfile('/etc/lsb-release') and 'Ubuntu' in open('/etc/lsb-release').read() else 'linux'  # can be linux1, linux2, etc
            r = 'ubuntu'

    elif sys.platform == "darwin" : r = 'mac'
    elif sys.platform == "cygwin" : r = 'cygwin'
    elif sys.platform == "win32" :  r = 'windows'
    else:                           r = 'unknown'

    if platform.machine() == 'arm64': r = 'm1'

    return r


def get_latest_file(dir_url):
    try:
        with urllib.request.urlopen(dir_url+'latest.html') as f:
            html = f.read().decode('utf-8')
            latest_file = html.partition('url=')[2].partition('"')[0]

    except urllib.error.HTTPError as e:
        print(f'Could not retrive latest.html from {dir_url!r} error-code: {e.code}, aborting...')
        sys.exit(1)

    return latest_file


def install_pyrosetta(mirror=0, type='Release', extras='', serialization=False, distributed=False, silent=False, skip_if_installed=True, use_setup_py_package=False):
    if skip_if_installed:
        try:
            import pyrosetta
            pyrosetta.init
            if not silent: print('PyRosetta install detected, doing nothing...')
            return

        except (ModuleNotFoundError, AttributeError) as _:
            pass


    if distributed: serialization = True

    if extras: extras = '.' + '.'.join( sorted( extras.split('.') ) )

    assert not ( (serialization or distributed) and extras), 'ERROR: both extras and serialization/distributed flags should not be specified at the same time!'

    if serialization: extras = '.cxx11thread.serialization'

    #packages = 'numpy attrs billiard cloudpickle dask dask-jobqueue distributed gitpython jupyter traitlets  blosc pandas scipy python-xz' if distributed else 'numpy'
    packages = 'numpy pyrosetta-distributed' if distributed else 'numpy'

    os_name = get_pyrosetta_os()

    if os_name not in ['ubuntu', 'mac', 'm1']:
        print(f'Could not find PyRosetta wheel for {os_name!r}, aborting...')
        sys.exit(1)

    if not silent: print(f'Installing PyRosetta:\n os: {os_name}\n type: {type}\n Rosetta C++ extras: {extras[1:]}\n mirror: {_PYROSETTA_RELEASES_URLS_[mirror]}\n extra packages: {packages}\n')

    login, password = '', ''
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, _PYROSETTA_RELEASES_URLS_[mirror], login, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    if not use_setup_py_package:
        url = f'{_PYROSETTA_RELEASES_URLS_[mirror]}/PyRosetta4.{type}.python{sys.version_info.major}{sys.version_info.minor}.{os_name}{extras}.wheel/'

        wheel = get_latest_file(url)

        url_parts = list( url.partition('https://') )
        url_parts.insert(-1, f'{login}:{password}@')
        url = ''.join(url_parts)

        url += wheel
        if not silent: print(f'PyRosetta wheel url: {url}')

        try: subprocess.check_call(f'pip install {url}', shell=True)
        except subprocess.CalledProcessError as e:

            try: subprocess.check_output(f'pip install --dry-run {url}', shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                output = e.output.decode('utf-8')
                if 'is not a supported wheel on this platform' in output:
                    print('Attempt to install wheel failed, falling back to use `setup.py` package...')
                    use_setup_py_package = True
                else:
                    sys.exit(e.returncode)


    if use_setup_py_package:
        url = f'{_PYROSETTA_RELEASES_URLS_[mirror]}/PyRosetta4.{type}.python{sys.version_info.major}{sys.version_info.minor}.{os_name}{extras}/'
        setup_tar_bz2 = get_latest_file(url)

        with tempfile.TemporaryDirectory(prefix=f'PyRosetta4.{type}.python{sys.version_info.major}{sys.version_info.minor}.{os_name}{extras}.') as temp_dir:
            print(f'Downloading {url}/{setup_tar_bz2} into {temp_dir}')
            subprocess.check_call(f'cd {temp_dir} && curl {url}/{setup_tar_bz2} | tar -jxom && cd {setup_tar_bz2[:-len(".tar.bz2")]}/setup && pip install .', shell=True)

    subprocess.check_call(f'pip install {packages}', shell=True)
