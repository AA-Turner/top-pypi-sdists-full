from localstack.packages import Package,PackageInstaller
from localstack.packages.core import PythonPackageInstaller
_PYARROW_DEFAULT_VERSION='21.0.0'
class PyArrowPackage(Package):
	def __init__(A,default_version:str=_PYARROW_DEFAULT_VERSION):super().__init__(name='PyArrow',default_version=default_version)
	def _get_installer(A,version:str)->PackageInstaller:return PyArrowPackageInstaller(version)
	def get_versions(A)->list[str]:return[_PYARROW_DEFAULT_VERSION]
class PyArrowPackageInstaller(PythonPackageInstaller):
	def __init__(A,version:str):super().__init__('pyarrow',version)
pyarrow_package=PyArrowPackage()