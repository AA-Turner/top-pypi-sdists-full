# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-aaf-adapter',
    version='2.0.0',
    description='OpenTimelineIO AAF Adapter',
    long_description='# OpenTimelineIO Advanced Authoring Format (AAF) Adapter\n\n[![Supported VFX Platform Versions](https://img.shields.io/badge/vfx%20platform-2020--2023-lightgrey.svg)](http://www.vfxplatform.com/)\n![Dynamic YAML Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FOpenTimelineIO%2Fotio-aaf-adapter%2Fmain%2F.github%2Fworkflows%2Fci.yaml&query=%24.jobs%5B%22test-plugin%22%5D.strategy.matrix%5B%22otio-version%22%5D&label=OpenTimelineIO)\n![Dynamic YAML Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FOpenTimelineIO%2Fotio-aaf-adapter%2Fmain%2F.github%2Fworkflows%2Fci.yaml&query=%24.jobs%5B%22test-plugin%22%5D.strategy.matrix%5B%22python-version%22%5D&label=Python)\n\n## Overview\n\nThis project is a [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) adapter for reading and writing Advanced Authoring Format (AAF) files.\nThis adapter was originally included with OpenTimelineIO as a contrib adapter. It is in the process of being separated into this project to improve maintainability and reduced the dependencies of both projects.\n\n## Feature Matrix\n\n| Feature                  | Read  | Write |\n| -------                  | ----  | ----- |\n| Single Track of Clips    |  ✔   |   ✔   |\n| Multiple Video Tracks    |  ✔   |   ✔   |\n| Audio Tracks & Clips     |  ✔   |   ✔   |\n| Gap/Filler               |  ✔   |   ✔   |\n| Markers                  |  ✔   |   ✔   |\n| Nesting                  |  ✔   |   ✔   |\n| Transitions              |  ✔   |   ✔   |\n| Audio/Video Effects      |  ✖   |   ✖   |\n| Linear Speed Effects     |  ✔   |   ✖   |\n| Fancy Speed Effects      |  ✖   |   ✖   |\n| Color Decision List      |  ✖   |   ✖   |\n| Image Sequence Reference |  ✖   |   ✖   |\n\n## Requirements\n\n* [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)\n* [pyaaf2](https://github.com/markreidvfx/pyaaf2)\n\n\n## Licensing\n\nThis repository is licensed under the [Apache License, Version 2.0](LICENSE.md).\n\n## Testing for Development\n\n```bash\n# In the root folder of the repo\npip install -e .\n\n# Test adapter\notioconvert -i some_timeline.aaf -o some_timeline.ext\n```\n\nIf you are using a version of OpentimelineIO that still has the AAF contrib adapter you may need to add the path of [plugin_manifest.json](./src/otio_aaf_adapter/plugin_manifest.json) to your `OTIO_PLUGIN_MANIFEST_PATH` [environment variable.](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-env-variables.html) This should override the contrib version.\n\n## Contributions\n\nIf you have any suggested changes to the otio-aaf-adapter,\nplease provide them via [pull request](../../pulls) or [create an issue](../../issues) as appropriate.\n\nAll contributions to this repository must align with the contribution\n[guidelines](https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html)\nof the OpenTimelineIO project.\n',
    author_email='Contributors to the OpenTimelineIO project <otio-discussion@lists.aswf.io>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'opentimelineio>=0.17.0',
        'pyaaf2>=1.7.0',
    ],
    entry_points={
        'opentimelineio.plugins': [
            'otio_aaf_adapter = otio_aaf_adapter',
        ],
    },
    packages=[
        'otio_aaf_adapter',
        'otio_aaf_adapter.adapters',
        'otio_aaf_adapter.adapters.aaf_adapter',
    ],
    package_dir={'': 'src'},
)
