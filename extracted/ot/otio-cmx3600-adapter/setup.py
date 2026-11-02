# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-cmx3600-adapter',
    version='1.0.0',
    description='OpenTimelineIO CMX 3600 EDL Adapter',
    long_description='# OpenTimelineIO CMX3600 EDL Adapter\n\nThe `cmx_3600` adapter is part of OpenTimelineIO\'s core adapter plugins.  \nIt provides reading and writing of CMX3600 formatted Edit Decision Lists (EDL). \nFor more information on the CMX3600 format please check the links in the \n[reference](edl-references) section \n\n# Adapter Feature Matrix\n\nThe following features of OTIO are supported by the `cmx_3600` adapter:\n\n|Feature                  | Support |\n|-------------------------|:-------:|\n|Single Track of Clips    | ✔       |\n|Multiple Video Tracks    | ✖       |\n|Audio Tracks & Clips     | ✔       |\n|Gap/Filler               | ✔       |\n|Markers                  | ✔       |\n|Nesting                  | ✖       |\n|Transitions              | ✔       |\n|Audio/Video Effects      | ✖       |\n|Linear Speed Effects     | ✔       |\n|Fancy Speed Effects      | ✖       |\n|Color Decision List      | ✔       |\n|Image Sequence Reference | ✔       |\n\n\n# Style Variations\nThe `cmx_3600` adapter supports writing EDL\'s with slight variations required by \ncertain applications. At the moment the supported styles are:\n* `avid` = [Avid Media Composer](https://www.avid.com/media-composer) (default)\n* `nucoda` = [Nucoda](https://digitalvision.world/products/nucoda/)\n* `premiere` = [Adobe Premiere Pro](https://www.adobe.com/products/premiere.html)\n\n\n## Main Functions\nThe two main functions below are usually called indirectly through \n`otio.adapters.read_from_[file|string]` and `otio.adapters.write_to_[file|string]`.\nHowever, since the `cmx_3600` adapter provides some additional arguments we \nshould mention them here.\n\n### read_from_string(input_str, rate=24, ignore_timecode_mismatch=False)\n\nReads a CMX Edit Decision List (EDL) from a string.  \nSince EDLs don\'t contain metadata specifying the rate they are meant\nfor, you may need to specify the `rate` parameter (default is 24).  \nBy default, read_from_string will throw an exception if it discovers\ninvalid timecode in the EDL. For example, if a clip\'s record timecode\noverlaps with the previous cut.  \nSince this is a common mistake in many EDLs, you can specify \n`ignore_timecode_mismatch=True`, which will\nsupress these errors and attempt to guess at the correct record\ntimecode based on the source timecode and adjacent cuts.  \nFor best results, you may wish to do something like this:\n\n``` python\ntry:\n    timeline = otio.adapters.read_from_string("mymovie.edl", rate=30)\nexcept EDLParseError:\n   print(\'Log a warning here\')\n   try:\n       timeline = otio.adapters.read_from_string(\n           "mymovie.edl",\n           rate=30,\n           ignore_timecode_mismatch=True)\n   except EDLParseError:\n       print(\'Log an error here\')\n```\n\n### write_to_string(input_otio, rate=None, style=\'avid\', reelname_len=8)\n\nWrites a CMX Edit Decision List (EDL) to a string.  \nThis function introduces `style` and `reelname_len` parameters.  \nThe `style` parameter let\'s you produce slight variations of EDL\'s \n(`avid` by default). Other supported styles are "nucoda" and "premiere".  \nThe `reelname_len` parameter lets you determine how many characters are in the \nreel name of the EDL (default is 8). Setting it to `None` will not set a limit \nof characters.\n\n\n# EDL References\n\n- Full specification: [SMPTE 258M-2004 "For Television −− Transfer of Edit Decision Lists"](https://ieeexplore.ieee.org/document/7291839) (See also [this older document](http://xmil.biz/EDL-X/CMX3600.pdf))\n- [Reference](https://prohelp.apple.com/finalcutpro_help-r01/English/en/finalcutpro/usermanual/chapter_96_section_0.html)\n\n\n# License\nOpenTimelineIO and the "cmx_3600" adapter are open source software. Please see the [LICENSE](LICENSE) \nfor details.\n\nNothing in the license file or this project grants any right to use Pixar or any other contributor’s trade names, trademarks, service marks, or product names.\n\n\n## Contributions\n\nIf you want to contribute to the project, \nplease see: https://opentimelineio.readthedocs.io/en/latest/tutorials/contributing.html\n\n\n# Contact\n\nFor more information, please visit http://opentimeline.io/\nor https://github.com/AcademySoftwareFoundation/OpenTimelineIO\nor join our discussion forum: https://lists.aswf.io/g/otio-discussion\n\n',
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
            'otio_cmx3600_adapter = otio_cmx3600_adapter',
        ],
    },
    packages=[
        'otio_cmx3600_adapter',
    ],
    package_dir={'': 'src'},
)
