from setuptools import setup, find_packages
 
setup(
    name = "databricks_pypi_extras",
    version = "0.1",
    decription = 'databricks whl library',
    extras_require = {
      'db1': ["databricks_pypi1"],
      'db2': ["databricks_pypi2"],
    },
    packages = find_packages())
