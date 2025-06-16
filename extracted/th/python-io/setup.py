from setuptools import setup, find_packages

descriptions = {
    'short': """A Python module for working with user I/O.""",
    'long': """
    Python-IO is a Python module for working with user I/O.
    It has features for accepting user input and showing output.
    View the full syntax at: https://github.com/BenjaminTGa/Python_IO
    Download it with the command 'pip install Python-IO'.
    """
}

setup(
    name='Python_IO',
    description=descriptions['short'],
    long_description=descriptions['long'],
    version='0.3',
    #license='GNU Public Lisence 3.0'
    author="Ben G",
    author_email='formal.software@outlook.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/BenjaminTGa/Python_IO',
    keywords=['python', 'GUI', 'I/O', 'Modern'],
    install_requires=['customtkinter', 'requests']
)