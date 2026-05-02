from setuptools import setup,find_packages
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="fytly",
    version="3.6.3",  # Update version as needed
    author="Aegletek",
    author_email="coe@aegletek.com",
    url="https://www.aegletek.com/",
    description="A grading component for keyword-based scoring for resumes",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    #packages=["scorer"],  # Explicitly list your package
    packages=find_packages(),
    #package_dir={"": "."},  # Important for proper package discovery
    include_package_data=True,
    package_data={
        "scorer.configs": ["*.properties", "*.txt"],  # <-- Important!
    },

    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyPDF2",
        "python-docx",
        "pyspellchecker",
        "spacy",
        "nltk",
        "rapidfuzz",
    ],
)