from setuptools import setup, find_packages

setup(
    name="canonmap",
    version="0.2.43",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "google-cloud-storage",
        "pandas",
        "chardet",
        "numpy",
        "scikit-learn",
        "rapidfuzz",
        "metaphone",
        "tqdm",
        "requests",
        "codename",
    ],
    extras_require={
        "embedding": [
            "sentence-transformers",
            "transformers",
            "torch",
            "tokenizers",
        ],
    },
    author="Vince Berry",
    author_email="vince.berry@gmail.com",
    description="CanonMap - A Python library for entity canonicalization and mapping with enhanced configuration and response models",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinceberry/canonmap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cm=canonmap.cli:main",
        ],
    },
)