# coding: utf-8 
  
import sys 
from setuptools import setup, find_packages 
  
with open("README.rst", "r", encoding="utf-8") as fh: 
    long_description = fh.read() 
  
NAME = "aspose_cells" 
VERSION = "26.2.0" 
# To install the library, run the following 
# 
# python setup.py install 
# 
# prerequisite: setuptools 
# http://pypi.python.org/pypi/setuptools 
  
REQUIRES = ["JPype1 >= 1.2.1"] 
  
setup( 
    name=NAME, 
    version=VERSION, 
    description="Aspose.Cells for Python via Java is a high-performance library that unleashes the full potential of Excel in your Python projects. It can be used to efficiently manipulate and convert Excel and spreadsheet formats including XLS, XLSX, XLSB, ODS, CSV, and HTML - all from your Python code. Amazingly, it also offers free support.", 
    author="Aspose", 
    author_email="cells@aspose.com", 
    url="https://products.aspose.com/cells/python-java", 
    keywords=["Excel", "XLS", "XLSX", "XLSB", "CSV", "to", "PDF", "JPG", "PNG", "HTML", "ODS", "Numbers", "XLSM", "OOXML", "Spreadsheet", "Markdown", "XPS", "DOCX", "PPTX", "MHTML", "SVG", "JSON", "XML", "SQL"], 
    install_requires=REQUIRES, 
    packages=['asposecells'], 
    package_data={
        NAME: ['*.pyi','*.typed'],  # Include type hint files
    },
    include_package_data=True, 
    long_description=long_description, 
    long_description_content_type='text/x-rst', 
    classifiers=[ 
        'Programming Language :: Python :: 3.8', 
        'License :: Other/Proprietary License' 
    ], 
    platforms=[ 
        'Operating System :: MacOS :: MacOS X', 
        'Operating System :: Microsoft :: Windows :: Windows 7', 
        'Operating System :: Microsoft :: Windows :: Windows Vista', 
        'Operating System :: POSIX :: Linux', 
    ], 
    python_requires='<=3.13, >=3.8', 
) 
