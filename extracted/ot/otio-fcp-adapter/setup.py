# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-fcp-adapter',
    version='1.0.0',
    description='OpenTimelineIO FCP XML Adapter',
    long_description='# OpenTimelineIO FCP XML Adapter\n\nThe `fcp_xml` adapter is part of OpenTimelineIO\'s core adapter plugins.  \nIt provides reading and writing of Final Cut Pro 7 formatted XML files. \nFor more information on the FCP XML format please check the links in the \n[reference](#fcp7-xml-references) section \n\n# Adapter Feature Matrix\n\nThe following features of OTIO are supported by the `fcp_xml` adapter:\n\n|Feature                  | Support |\n|-------------------------|:-------:|\n|Single Track of Clips    | ✔       |\n|Multiple Video Tracks    | ✔       |\n|Audio Tracks & Clips     | ✔       |\n|Gap/Filler               | ✔       |\n|Markers                  | ✔       |\n|Nesting                  | ✔       |\n|Transitions              | ✖       |\n|Audio/Video Effects      | ✖       |\n|Linear Speed Effects     | ✖       |\n|Fancy Speed Effects      | ✖       |\n|Color Decision List      | ✖       |\n|Image Sequence Reference | ✖       |\n\n\n# FCP7 XML References\n\n- [Reference](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/FinalCutPro_XML/AboutThisDoc/AboutThisDoc.html#//apple_ref/doc/uid/TP30001152-TPXREF101)\n\n\n# License\nOpenTimelineIO and the "fcp_xml" adapter are open source software. \nPlease see the [LICENSE](LICENSE) for details.\n\nNothing in the license file or this project grants any right to use Pixar or \nany other contributor’s trade names, trademarks, service marks, or product names.\n\n\n## Contributions\n\nIf you want to contribute to the project, \nplease see: https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html\n\n\n# Contact\n\nFor more information, please visit http://opentimeline.io/\nor https://github.com/AcademySoftwareFoundation/OpenTimelineIO\nor join our discussion forum: https://lists.aswf.io/g/otio-discussion\n',
    author_email='Contributors to the OpenTimelineIO project <otio-discussion@lists.aswf.io>',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'opentimelineio>=0.15.0',
    ],
    entry_points={
        'opentimelineio.plugins': [
            'otio_fcp_adapter = otio_fcp_adapter',
        ],
    },
    packages=[
        'otio_fcp_adapter',
    ],
    package_dir={'': 'src'},
)
