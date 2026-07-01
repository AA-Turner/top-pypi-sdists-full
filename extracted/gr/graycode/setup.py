import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='graycode',
    version='1.0.5',
    author='Heikki Orsila',
    author_email='heikki.orsila@iki.fi',
    description=('Convert two\'s complement integer to gray code and '
                 'vice versa'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/heikkiorsila/gray-code',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
