import platform
import urllib.request
import os
import subprocess
import sys
import os.path as path
import tarfile
import shutil

__version__ = '0.19.9'

BIN = path.join(path.dirname(__file__), 'dep-tree')
BIN_TAR = BIN + '.tar.gz'
BIN_EXTRACTED = BIN + '-extracted'

OS_MAP = {
    'Darwin': 'darwin',
    'Linux': 'linux',
    'Windows': 'windows'
}

ARCH_MAP = {
    'x86_64': 'amd64',
    'AMD64': 'amd64',
    'arm64': 'arm64',
    'aarch64': 'arm64'
}


def url(arch, system):
    return f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_{system}_{arch}.tar.gz"


def find_executable(files):
    for file in files:
        if file == 'dep-tree' or file == 'dep-tree.exe':
            return file
    print('Could not find executable file in uncompressed folder')
    exit(1)


def main():
    arch = platform.machine()
    system = platform.system()
    if system not in OS_MAP:
        print(f'System "{system}" is not supported, supported operating systems are ${", ".join(OS_MAP.keys())}')
        exit(1)

    if arch not in ARCH_MAP:
        print(f'Architecture "{arch}" is not supported, supported architectures are ${", ".join(ARCH_MAP.keys())}')
        exit(1)

    if not path.isfile(BIN):
        if path.isdir(BIN_EXTRACTED):
            shutil.rmtree(BIN_EXTRACTED)
        if path.isfile(BIN_TAR):
            os.remove(BIN_TAR)
        urllib.request.urlretrieve(url(ARCH_MAP[arch], OS_MAP[system]), BIN_TAR)
        file = tarfile.open(BIN_TAR)
        file.extractall(BIN_EXTRACTED)
        shutil.move(
            path.join(BIN_EXTRACTED, find_executable(os.listdir(BIN_EXTRACTED))),
            BIN
        )
        shutil.rmtree(BIN_EXTRACTED)
        file.close()
        os.remove(BIN_TAR)

    exit(subprocess.call(
        [BIN, *sys.argv[1:]],
        executable=BIN,
        stdout=sys.stdout.buffer,
        stderr=sys.stderr.buffer,
    ))


if __name__ == '__main__':
    main()
