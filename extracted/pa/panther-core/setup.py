from distutils.core import setup

VERSION = "0.16.2"

install_requires = [
    'jsonpath-ng',
]

with open('requirements.txt') as f:
    dependencies_with_versions = []
    for dependency in f.readlines():
        dependency_with_version = dependency.strip()
        package_name = dependency_with_version.split('==')[0]
        if package_name in install_requires:
            dependencies_with_versions.append(dependency_with_version)

setup(
    name='panther_core',
    packages=['panther_core', 'panther_core/exec', 'panther_core/snapshots'],
    package_dir={
        'exec': 'panther_core/exec',
        'snapshots': 'panther_core/snapshots',
    },
    version=VERSION,
    license='AGPL-3.0',
    description='Panther core library',
    author='Panther Labs Inc',
    author_email='pypi@runpanther.io',
    url='https://github.com/panther-labs/panther_core',
    download_url=f'https://github.com/panther-labs/panther_core/archive/refs/tags/v{VERSION}.tar.gz',
    keywords=['Security', 'CLI'],
    install_requires=install_requires,
    classifiers=[
        'Topic :: Security',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
)
