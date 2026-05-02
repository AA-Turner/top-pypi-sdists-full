import setuptools
from springlabs_cc_alexis import __version__ as version
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='springlabs_cc_alexis',
    version=version,
    packages=setuptools.find_packages(),
    include_package_data=True,
    author="Alexis Hinojosa",
    author_email="alexishinojosa008@gmail.com",
    description="Springlabs Prints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://springlabs.ai/",
    project_urls={
        "Source Code": "https://gitlab.com/AlejandroBarcenas/springlabs-django-cli",
    },
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        springlabs_cc_alexis=springlabs_cc_alexis.scripts.springlabs_cc_alexis:cli
    ''',
)
