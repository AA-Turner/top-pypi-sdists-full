from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_gui',
    version='0.1.63.231',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description="abstract_gui provides reusable components, factories, utilities for logging, threading, state management, and more, making it easier to build responsive, feature-rich interfaces without boilerplate code.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_gui',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.11',
      ],
    install_requires=[
        'aiohttp',
        'abstract_utilities',
        'PySimpleGUIWeb',
        'PySimpleGUI',
        'pydot',
        'clipboard',
        'PyQt6',
        'abstract_apis'
        ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)

