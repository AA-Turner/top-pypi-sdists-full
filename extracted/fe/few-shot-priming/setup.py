import os
import setuptools
from setuptools import find_packages



new_version = "0.3.950"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "few_shot_priming",
    version = new_version,
    author = "Yamen Ajjour",
    packages = ["few_shot_priming", "few_shot_priming.argument_sampling"],
    author_email = "yajjour@hotmail.com",
    description = "Analyzing priming effects in a few shot setting environment",
    package_data={'': ['experiment/*.*' , 'logs/tmp', 'data/*.*', "conf.yaml", "conf-google.yaml"]},
    package_dir={ 'few_shot_priming': '.'},
    long_description = long_description,
    include_package_data=True,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.uni-hannover.de/y.ajjour/few-shot-priming",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
print (new_version)
