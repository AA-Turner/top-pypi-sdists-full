import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotifywebapi",
    version="1.2.8",
    author="Brian Cheng",
    author_email="briantc@mit.edu",
    description="A simple Spotify Web API in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Firius0408/spotifywebapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
)