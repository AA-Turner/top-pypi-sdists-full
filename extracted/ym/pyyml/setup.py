import os
from setuptools import setup

here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.md')
readme = open(readme_path).read()
setup(
    name='pyyml',
    version='0.0.2',
    url='https://github.com/q1394168335/pyyml',
    author='haogege',
    author_email='1394168335@qq.com',
    description='Use python in yaml',
    long_description=readme,
    packages=[],
    install_requires=[
        'pyyaml >= 3.13',
    ],
    license='MIT',
)
