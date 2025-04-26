from setuptools import setup, find_packages

setup(
    name='taming-transformers',
    version='0.0.1',
    description='Taming Transformers for High-Resolution Image Synthesis',
    url='https://github.com/CompVis/taming-transformers',
    author='Patrick Esser, Robin Rombach, Bjorn Ommer',
    author_email='patrick.esser@iwr.uni-heidelberg.de',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'numpy',
        'tqdm',
        'omegaconf>=2.0.0',
        'pytorch-lightning>=1.0.8'
    ],
)
