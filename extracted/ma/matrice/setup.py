from setuptools import setup, find_packages
import pathlib
import os

#print(os.getcwd(), os.listdir(os.getcwd()))

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
#print(here, here / "config/requirements.txt")
#requirements = (here / "config/requirements.txt").read_text(encoding="utf-8").split()
#print(find_packages('src'))
#print(requirements)

setup(
    name="matrice",




    version = "1.0.98862",



    description="SDK for connecting to matrice.ai services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matrice-ai/python-sdk",
    author= "Matrice.ai",
    author_email = "dipendra@matrice.ai",
    install_requires = ['requests'],
    classifiers=[
        "Development Status :: 4 - Beta",       
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="matrice setuptools sdk development",
    packages=find_packages(where="src", include=["matrice", "matrice.*"]),  # Only include matrice and its subpackages
    package_dir={'': 'src'},  # Tells setuptools to look for packages in the 'src' directory
    python_requires=">=3.7, <4",
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/matrice-ai/python-sdk/issues",
        "Source": "https://github.com/matrice-ai/python-sdk/",
    },
)
