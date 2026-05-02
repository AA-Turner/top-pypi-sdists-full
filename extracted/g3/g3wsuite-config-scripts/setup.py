from setuptools import setup, find_packages

setup(
    name="g3wsuite_config_scripts",
    version="0.6.3",
    description="Configuration scripts for the g3w suite setup",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "g3w_dev_setup=g3w_config_scripts.g3w_dev_setup:main",  
            "g3w_prod_setup=g3w_config_scripts.g3w_prod_setup:main",  
            "g3w_config_gen=g3w_config_scripts.g3w_config_gen:main",
            "g3w_branding=g3w_config_scripts.g3w_branding:main",
        ],
    },
    install_requires=[
        "pillow>=11.1.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrea Antonello",
    author_email="andrea.antonello@gmail.com",
    url="https://github.com/moovida/g3wsuite_config_scripts",
)
