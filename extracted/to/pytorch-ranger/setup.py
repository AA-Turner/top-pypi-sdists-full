from setuptools import setup
from setuptools import find_packages

setup(
    name='pytorch_ranger',
    version='0.1.1',
    description='Ranger - a synergistic optimizer using RAdam '
                '(Rectified Adam) and LookAhead in one codebase ',
    license='Apache',
    url="https://github.com/mpariente/Ranger-Deep-Learning-Optimizer",
    long_description='',
    python_requires='>=3.5',
    install_requires=['torch'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)