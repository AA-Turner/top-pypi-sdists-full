import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frontend",  # Replace with your own username
    python_requires=">=3.8",
    version="0.0.3",
    license="GNU GENERAL PUBLIC LICENSE",
    author="Pragy Agarwal",
    author_email="agar.pragy@gmail.com",
    description="Develop complex & beautiful UI frontends using Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AgarwalPragy/frontend",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'starlette>=0.12.0', 'uvicorn>=0.7.1', 'itsdangerous>=1.1.0', 'aiofiles'
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
    ],
)
