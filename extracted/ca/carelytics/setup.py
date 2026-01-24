from setuptools import setup, find_packages

setup(
    name="carelytics",
    version="0.1.3",
    author="Rohan Desai & Vaishnavi Sanjay Gadve",
    author_email="rohan.acme@gmail.com",
    description="A Python library for Healthcare Data Analytics and Revenue Cycle Management.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohan-desai/carelytics",  # Replace with your GitHub repo URL once pushed
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
