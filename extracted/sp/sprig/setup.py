import os

import setuptools

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path, "r") as fp:
    long_description = fp.read()

here = os.path.abspath(os.path.dirname(__file__))

setuptools.setup(
    name="sprig",
    author="AP Ljungquist",
    author_email="ap@ljungquist.eu",
    description="A home to code that would otherwise be homeless",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apljungquist/sprig",
    license="MIT",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "sprig": ["py.typed"],
    },
    zip_safe=False,
    install_requires=[
        "more_itertools",
        "typing_extensions",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
