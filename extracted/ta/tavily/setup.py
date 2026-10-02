from setuptools import setup, find_packages

DESCRIPTION = "Simple API TAVILY"

# Setup configuration
setup(
    name="tavily",
    version="1.1.0",
    author="Archi Vensent",
    author_email="archivensent1990drill@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    install_requires=[
    "requests",
    "aiohttp",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords=[
        "python",
        "api",
        "console",
        "terminal",
    ],
    python_requires=">=3.7",
)
