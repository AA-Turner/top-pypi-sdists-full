from setuptools import setup, find_namespace_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.in'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='aspose-cad',
      version='26.11.0',
      python_requires='>=3.5,<3.14',
      description='Aspose.CAD for Python is a CAD and BIM drawings Processing library that allows developers to modify, convert and publish various drawing and image formats without need to have any other CAD software.',
      url='https://products.aspose.com/cad/python',
      project_urls={},
      author='Aspose',
      license='https://company.aspose.com/legal/eula',
      classifiers=['Intended Audience :: Developers','Intended Audience :: Education','License :: Other/Proprietary License','License :: Free To Use But Restricted','Operating System :: Microsoft :: Windows','Operating System :: Unix','Operating System :: MacOS','Operating System :: MacOS :: MacOS X','Operating System :: POSIX','Programming Language :: Python :: 3','Programming Language :: Python :: 3 :: Only','Programming Language :: Python :: 3.5','Programming Language :: Python :: 3.6','Programming Language :: Python :: 3.7','Programming Language :: Python :: 3.8','Programming Language :: Python :: 3.9','Programming Language :: Python :: 3.10','Programming Language :: Python :: 3.11','Programming Language :: Python :: 3.12','Programming Language :: Python :: 3.13','Topic :: Software Development','Topic :: Software Development :: Libraries','Topic :: Office/Business'],
      keywords=['dwg,dwg to pdf,convert,publish,export,create,write,metadata,edit,modify,cad,bim,dxf,dgn,dwf,dwfx,ifc,stl,dxb,cf2,hpgl,plt,ply,ifc,iges,pcl,pdf-3d,dwt,dxb,3ds,u3d,stp,collada,obj,stp,jpg,png,j2k,psd,svg,pdf,wmf,dicom,webp,html5,gif'],
      platforms=['linux_x86_64'],
      packages=find_namespace_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'pyinstaller40': ['hook-dirs=aspose.cad:get_pyinstaller_hook_dirs']
      },
      long_description=long_description,
      long_description_content_type='text/markdown')
