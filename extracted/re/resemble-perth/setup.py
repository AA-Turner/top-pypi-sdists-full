import os
import setuptools
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as help_file:
    long_description = help_file.read()

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()

# Model and pretrained data files that should be included in the package
bundled_data = [
    "perth_net/pretrained/*/*.*",  # Perth models
]

setuptools.setup(
    name="resemble-perth",
    version="1.0.1",
    author="Resemble AI, Aditya",
    author_email="team@resemble.ai, aditya@resemble.ai",
    description="Audio Watermarking and Detection Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/resemble-ai/Perth",
    keywords=["Audio Watermarking", "Perceptual Watermarking", "Neural Networks", "Audio Processing"],
    project_urls={
        'Bug Reports': 'https://github.com/resemble-ai/Perth/issues',
        'Source': 'https://github.com/resemble-ai/Perth',
        'Documentation': 'https://github.com/resemble-ai/Perth/blob/main/README.md',
    },
    packages=find_packages(),
    package_data={"perth": bundled_data},
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        'console_scripts': [
            'perth=perth.cli.watermark_cli:main',
        ],
    },
)
