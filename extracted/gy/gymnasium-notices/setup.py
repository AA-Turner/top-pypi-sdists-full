import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gymnasium-notices",
    version="0.0.1",
    author="Jordan Terry",
    author_email="jkterry0@farama.org",
    description="Notices for gymnasium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Farama-Foundation/gym-notices",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
