from __future__ import annotations

import setuptools
from setuptools.command.sdist import sdist as _sdist

class CustomSdistCommand(_sdist):
    def make_distribution(self):
        # CRAB-45784: PEP 625 no longer allows distributions (the .tar.gz file) to include non-normalized chars
        # ('-' in this case) in the file name. Replace the name with an underscore only for the distribution without
        # altering SPy's package name.
        # TODO CRAB-35238: This can be removed when setuptools is upgraded to v69.3.0 or later.
        self.distribution.metadata.name = self.distribution.metadata.name.replace("-", "_")
        super().make_distribution()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeq-spy",
    version="197.15",
    author="Seeq Corporation",
    author_email="support@seeq.com",
    description="Easy-to-use Python interface for Seeq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.seeq.com",
    project_urls={
        'Documentation': 'https://python-docs.seeq.com/',
        'Changelog': 'https://python-docs.seeq.com/changelog.html'
    },
    packages=setuptools.find_namespace_packages(exclude=['seeq.sdk', 'seeq.sdk.*']),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'Deprecated >= 1.2.6',
        'numpy >= 1.21.6',
        'pandas >= 1.2.5',
        'python-dateutil >= 2.7.3',
        'pytz >= 2020.1',
        'requests >= 2.22.0',
        'urllib3 >= 1.21.1',
    ],
    extras_require={
        # This should remain updated with the dependency_mapping in _dependencies.py
        'widgets': [
            'ipython >= 7.6.1',
            'ipywidgets >= 7.6.0',
            'matplotlib >= 3.5.0',
            'seeq-data-lab-env-mgr >= 0.1.0',
        ],
        'templates': [
            'beautifulsoup4 >= 4.8.0',
            'chevron >= 0.14.0',
            'Mako >= 1.1.0',
            'Markdown >= 3.3.4',
            'matplotlib >= 3.5.0',
        ],
        'jobs': [
            'cron-descriptor >= 1.2.24',
            'nbconvert >= 6.4.4',
            'nbformat >= 5.2.0',
            'recurrent >= 0.4.0',
        ],
        'jupyter': [
            'ipylab >= 0.5.2',
            'ipython >= 7.6.1',
            'ipywidgets >= 7.6.0',
            'jupyterlab >= 3.0.0',
            'nbconvert >= 6.4.4',
            'nbformat >= 5.2.0',
            'notebook >= 6.0.0',
            'psutil >= 5.9.0',
            'setuptools >= 65.0.0',
        ],
        'all': [
            'beautifulsoup4 >= 4.8.0',
            'chevron >= 0.14.0',
            'cron-descriptor >= 1.2.24',
            'ipylab >= 0.5.2',
            'ipywidgets >= 7.6.0',
            'jupyterlab >= 3.0.0',
            'Markdown >= 3.3.4',
            'matplotlib >= 3.5.0',
            'nbconvert >= 6.4.4',
            'nbformat >= 5.2.0',
            'notebook >= 6.0.0',
            'psutil >= 5.9.0',
            'recurrent >= 0.4.0',
            'setuptools >= 65.0.0',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    cmdclass={"sdist": CustomSdistCommand},
)
