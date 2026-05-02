from setuptools import setup, find_packages

setup(
    name="springtownai-rag",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "boto3",
    ],
    author="Your Name",
    author_email="dhruv.307@gmail.com",
    description="A simple S3 file downloader",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvgm/springtownai-rag",  # If you have a repo for this package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

