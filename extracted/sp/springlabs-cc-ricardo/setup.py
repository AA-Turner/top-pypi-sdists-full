import setuptools
from springlabs_cc_ricardo import __version__ as version
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='springlabs_cc_ricardo',
    version=version,
    packages=setuptools.find_packages(),
    include_package_data=True,
    author="Ricardo Romero",
    author_email="crrg1022@gmail.com",
    description="Springlabs Projects Django Standard(NO ES COPIA)",
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
        springlabs_cc_ricardo=springlabs_cc_ricardo.scripts.springlabs_cc_ricardo:cli
    ''',
)
