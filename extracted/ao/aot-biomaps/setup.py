from setuptools import setup, find_packages

setup(
    name='AOT_biomaps',
    version='2.8.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'k-wave-python',
        'setuptools',
        'pyyaml',
        'numba',
        'tqdm',
        'nvidia-ml-py3',
        'scikit-image',
        'scikit-learn',
        'pandas',
    ],
    extras_require={
        'cpu': [
        ],
        'gpu': [
            'cupy',
            'torch',
        ],
    },
    author='Lucas Duclos',
    author_email='lucas.duclos@universite-paris-saclay.fr',
    description='Acousto-Optic Tomography',
    url='https://github.com/LucasDuclos/AcoustoOpticTomography',
)