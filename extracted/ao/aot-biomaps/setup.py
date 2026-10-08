from setuptools import setup, find_packages
import os

REQUIRED_DEPENDENCIES = [
    'numpy>=1.22.2,<2.3.0',
    'scipy>=1.15.0',
    'tqdm>=4.60.0',
    'matplotlib>=3.10.0',
    'numba>=0.61.2',
    'scikit-image>=0.24.0'
]

OPTIONAL_DEPENDENCIES = {
    'acoustic': ['k-wave-python>=0.6.2'],
    # CuPy N'EST PLUS dans les dépendances obligatoires :
    # l'utilisateur choisit le wheel correspondant à SON CUDA.
    'gpu-cuda11': ['cupy-cuda11x>=11.0.0'],
    'gpu-cuda12': ['cupy-cuda12x>=12.0.0'],
    'gpu-cuda13': ['cupy-cuda13x>=13.0.0'],
}

setup(
    name='aot-biomaps',
    version='2.9.1021',
    packages=find_packages(),
    package_dir={'': '.'},
    include_package_data=True,
    package_data={
        'AOT_biomaps': ['AOT_Recon/AOT_biomaps_kernels.cu'],
    },
    install_requires=REQUIRED_DEPENDENCIES,          # ← plus de CuPy ici
    extras_require=OPTIONAL_DEPENDENCIES,
    author='Lucas Duclos',
    author_email='lucas.duclos@universite-paris-saclay.fr',
    description='Acousto-Optic Tomography Reconstruction Library',
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/LucasDuclos/AcoustoOpticTomography',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['aot-biomaps = AOT_biomaps.__main__:main'],
    },
)








