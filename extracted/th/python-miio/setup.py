# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miio',
 'miio.gateway',
 'miio.gateway.devices',
 'miio.integrations',
 'miio.integrations.airpurifier',
 'miio.integrations.airpurifier.airdog',
 'miio.integrations.airpurifier.airdog.tests',
 'miio.integrations.airpurifier.dmaker',
 'miio.integrations.airpurifier.dmaker.tests',
 'miio.integrations.airpurifier.zhimi',
 'miio.integrations.airpurifier.zhimi.tests',
 'miio.integrations.fan',
 'miio.integrations.fan.dmaker',
 'miio.integrations.fan.leshow',
 'miio.integrations.fan.leshow.tests',
 'miio.integrations.fan.zhimi',
 'miio.integrations.humidifier',
 'miio.integrations.humidifier.deerma',
 'miio.integrations.humidifier.deerma.tests',
 'miio.integrations.humidifier.shuii',
 'miio.integrations.humidifier.shuii.tests',
 'miio.integrations.humidifier.zhimi',
 'miio.integrations.humidifier.zhimi.tests',
 'miio.integrations.light',
 'miio.integrations.light.philips',
 'miio.integrations.light.philips.tests',
 'miio.integrations.light.yeelight',
 'miio.integrations.light.yeelight.tests',
 'miio.integrations.petwaterdispenser',
 'miio.integrations.petwaterdispenser.tests',
 'miio.integrations.vacuum',
 'miio.integrations.vacuum.dreame',
 'miio.integrations.vacuum.dreame.tests',
 'miio.integrations.vacuum.mijia',
 'miio.integrations.vacuum.mijia.tests',
 'miio.integrations.vacuum.roborock',
 'miio.integrations.vacuum.roborock.tests',
 'miio.integrations.vacuum.roidmi',
 'miio.integrations.vacuum.roidmi.tests',
 'miio.integrations.vacuum.viomi',
 'miio.interfaces',
 'miio.push_server',
 'miio.tests']

package_data = \
{'': ['*'], 'miio': ['data/*']}

install_requires = \
['PyYAML>=5,<7',
 'appdirs>=1,<2',
 'attrs',
 'click>=8',
 'construct>=2.10.56,<3.0.0',
 'croniter>=1',
 'cryptography>=35',
 'defusedxml>=0,<1',
 'pytz',
 'tqdm>=4,<5',
 'zeroconf>=0,<1']

extras_require = \
{':python_version <= "3.7"': ['importlib_metadata>=1,<2'],
 'docs': ['sphinx>=4.2',
          'sphinx_click',
          'sphinxcontrib-apidoc>=0,<1',
          'sphinx_rtd_theme>=0,<1']}

entry_points = \
{'console_scripts': ['miio-extract-tokens = miio.extract_tokens:main',
                     'miiocli = miio.cli:create_cli',
                     'mirobo = '
                     'miio.integrations.vacuum.roborock.vacuum_cli:cli']}

setup_kwargs = {
    'name': 'python-miio',
    'version': '0.5.12',
    'description': 'Python library for interfacing with Xiaomi smart appliances',
    'long_description': 'python-miio\n===========\n\n|Chat| |PyPI version| |PyPI downloads| |Build Status| |Coverage Status| |Docs| |Black|\n\nThis library (and its accompanying cli tool) can be used to interface with devices using Xiaomi\'s `miIO <https://github.com/OpenMiHome/mihome-binary-protocol/blob/master/doc/PROTOCOL.md>`__ and MIoT protocols.\n\n\nGetting started\n---------------\n\nIf you already have a token for your device and the device type, you can directly start using `miiocli` tool.\nIf you don\'t have a token for your device, refer to `Getting started <https://python-miio.readthedocs.io/en/latest/discovery.html>`__ section of `the manual <https://python-miio.readthedocs.io>`__ for instructions how to obtain it.\n\nThe `miiocli` is the main way to execute commands from command line.\nYou can always use `--help` to get more information about the available commands.\nFor example, executing it without any extra arguments will print out options and available commands::\n\n    $ miiocli --help\n    Usage: miiocli [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      -d, --debug\n      -o, --output [default|json|json_pretty]\n      --help                          Show this message and exit.\n\n    Commands:\n      airconditioningcompanion\n      ..\n\nYou can get some information from any miIO/MIoT device, including its device model, using the `info` command::\n\n    miiocli device --ip <ip> --token <token> info\n\n    Model: some.device.model1\n    Hardware version: esp8285\n    Firmware version: 1.0.1_0012\n    Network: {\'localIp\': \'<ip>\', \'mask\': \'255.255.255.0\', \'gw\': \'<ip>\'}\n    AP: {\'rssi\': -73, \'ssid\': \'<nnetwork>\', \'primary\': 11, \'bssid\': \'<bssid>\'}\n\nDifferent devices are supported by their corresponding modules (e.g., `roborockvacuum` or `fan`).\nYou can get the list of available commands for any given module by passing `--help` argument to it::\n\n    $ miiocli roborockvacuum --help\n\n    Usage: miiocli roborockvacuum [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --ip TEXT       [required]\n      --token TEXT    [required]\n      --id-file FILE\n      --help          Show this message and exit.\n\n    Commands:\n      add_timer                Add a timer.\n      ..\n\nEach command invocation will automatically detect the device model necessary for some actions by querying the device.\nYou can avoid this by specifying the model manually::\n\n    miiocli roborockvacuum --model roborock.vacuum.s5 --ip <ip> --token <token> start\n\n\nAPI usage\n---------\nAll functionality is accessible through the `miio` module::\n\n    from miio import RoborockVacuum\n\n    vac = RoborockVacuum("<ip address>", "<token>")\n    vac.start()\n\nEach separate device type inherits from `miio.Device`\n(and in case of MIoT devices, `miio.MiotDevice`) which provides a common API.\n\nEach command invocation will automatically detect (and cache) the device model necessary for some actions\nby querying the device.\nYou can avoid this by specifying the model manually::\n\n    from miio import RoborockVacuum\n\n    vac = RoborockVacuum("<ip address>", "<token>", model="roborock.vacuum.s5")\n\nPlease refer to `API documentation <https://python-miio.readthedocs.io/en/latest/api/miio.html>`__ for more information.\n\n\nTroubleshooting\n---------------\nYou can find some solutions for the most common problems can be found in `Troubleshooting <https://python-miio.readthedocs.io/en/latest/troubleshooting.html>`__ section.\n\nIf you have any questions, or simply want to join up for a chat, check `our Matrix room <https://matrix.to/#/#python-miio-chat:matrix.org>`__.\n\nContributing\n------------\n\nWe welcome all sorts of contributions from patches to add improvements or fixing bugs to improving the documentation.\nTo ease the process of setting up a development environment we have prepared `a short guide <https://python-miio.readthedocs.io/en/latest/contributing.html>`__ for getting you started.\n\n\nSupported devices\n-----------------\n\n-  Xiaomi Mi Robot Vacuum V1, S4, S4 MAX, S5, S5 MAX, S6 Pure, M1S, S7\n-  Xiaomi Mi Home Air Conditioner Companion\n-  Xiaomi Mi Smart Air Conditioner A (xiaomi.aircondition.mc1, mc2, mc4, mc5)\n-  Xiaomi Mi Air Purifier 2, 3H, 3C, 4, Pro, Pro H, 4 Pro (zhimi.airpurifier.m2, mb3, mb4, mb5, v7, vb2, va2), 4 Lite\n-  Xiaomi Mi Air (Purifier) Dog X3, X5, X7SM (airdog.airpurifier.x3, airdog.airpurifier.x5, airdog.airpurifier.x7sm)\n-  Xiaomi Mi Air Humidifier\n-  Smartmi Air Purifier\n-  Xiaomi Aqara Camera\n-  Xiaomi Aqara Gateway (basic implementation, alarm, lights)\n-  Xiaomi Mijia 360 1080p\n-  Xiaomi Mijia STYJ02YM (Viomi)\n-  Xiaomi Mijia 1C STYTJ01ZHM (Dreame)\n-  Dreame F9, D9, Z10 Pro\n-  Xiaomi Mi Home (Mijia) G1 Robot Vacuum Mop MJSTG1\n-  Xiaomi Roidmi Eve\n-  Xiaomi Mi Smart WiFi Socket\n-  Xiaomi Chuangmi Plug V1 (1 Socket, 1 USB Port)\n-  Xiaomi Chuangmi Plug V3 (1 Socket, 2 USB Ports)\n-  Xiaomi Smart Power Strip V1 and V2 (WiFi, 6 Ports)\n-  Xiaomi Philips Eyecare Smart Lamp 2\n-  Xiaomi Philips RW Read (philips.light.rwread)\n-  Xiaomi Philips LED Ceiling Lamp\n-  Xiaomi Philips LED Ball Lamp (philips.light.bulb)\n-  Xiaomi Philips LED Ball Lamp White (philips.light.hbulb)\n-  Xiaomi Philips Zhirui Smart LED Bulb E14 Candle Lamp\n-  Xiaomi Philips Zhirui Bedroom Smart Lamp\n-  Huayi Huizuo Lamps\n-  Xiaomi Universal IR Remote Controller (Chuangmi IR)\n-  Xiaomi Mi Smart Pedestal Fan V2, V3, SA1, ZA1, ZA3, ZA4, ZA5 1C, P5, P9, P10, P11, P33\n-  Xiaomi Rosou SS4 Ventilator (leshow.fan.ss4)\n-  Xiaomi Mi Air Humidifier V1, CA1, CA4, CB1, MJJSQ, JSQ, JSQ1, JSQ001\n-  Xiaomi Mi Water Purifier (Basic support: Turn on & off)\n-  Xiaomi Mi Water Purifier D1, C1 (Triple Setting)\n-  Xiaomi PM2.5 Air Quality Monitor V1, B1, S1\n-  Xiaomi Smart WiFi Speaker\n-  Xiaomi Mi WiFi Repeater 2\n-  Xiaomi Mi Smart Rice Cooker\n-  Xiaomi Smartmi Fresh Air System VA2 (zhimi.airfresh.va2), VA4 (zhimi.airfresh.va4),\n   A1 (dmaker.airfresh.a1), T2017 (dmaker.airfresh.t2017)\n-  Yeelight lights (basic support, we recommend using `python-yeelight <https://gitlab.com/stavros/python-yeelight/>`__)\n-  Xiaomi Mi Air Dehumidifier\n-  Xiaomi Tinymu Smart Toilet Cover\n-  Xiaomi 16 Relays Module\n-  Xiaomi Xiao AI Smart Alarm Clock\n-  Smartmi Radiant Heater Smart Version (ZA1 version)\n-  Xiaomi Mi Smart Space Heater\n-  Xiaomiyoupin Curtain Controller (Wi-Fi) (lumi.curtain.hagl05)\n-  Xiaomi Xiaomi Mi Smart Space Heater S (zhimi.heater.mc2)\n-  Xiaomi Xiaomi Mi Smart Space Heater 1S (zhimi.heater.za2)\n-  Yeelight Dual Control Module (yeelink.switch.sw1)\n-  Scishare coffee maker (scishare.coffee.s1102)\n-  Qingping Air Monitor Lite (cgllc.airm.cgdn1)\n-  Xiaomi Walkingpad A1 (ksmb.walkingpad.v3)\n-  Xiaomi Smart Pet Water Dispenser (mmgg.pet_waterer.s1, s4)\n-  Xiaomi Mi Smart Humidifer S (jsqs, jsq5)\n-  Xiaomi Mi Robot Vacuum Mop 2 (Pro+, Ultra)\n\n\n*Feel free to create a pull request to add support for new devices as\nwell as additional features for supported devices.*\n\nProjects using this library\n---------------------------\n\nThis library is used by various projects to support MiIO/MiOT devices.\nIf you are using this library for your project, feel free to open a PR to get it listed here!\n\nHome Assistant (official)\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nHome Assistant uses this library to support several platforms out-of-the-box.\nThis list is incomplete as the platforms (in parentheses) may also support other devices listed above.\n\n-  `Xiaomi Mi Robot Vacuum <https://home-assistant.io/components/vacuum.xiaomi_miio/>`__ (vacuum)\n-  `Xiaomi Philips Light <https://home-assistant.io/components/light.xiaomi_miio/>`__ (light)\n-  `Xiaomi Mi Air Purifier and Air Humidifier <https://home-assistant.io/components/fan.xiaomi_miio/>`__ (fan)\n-  `Xiaomi Smart WiFi Socket and Smart Power Strip <https://home-assistant.io/components/switch.xiaomi_miio/>`__ (switch)\n-  `Xiaomi Universal IR Remote Controller <https://home-assistant.io/components/remote.xiaomi_miio/>`__ (remote)\n-  `Xiaomi Mi Air Quality Monitor (PM2.5) <https://home-assistant.io/components/sensor.xiaomi_miio/>`__ (sensor)\n-  `Xiaomi Aqara Gateway Alarm <https://home-assistant.io/components/alarm_control_panel.xiaomi_miio/>`__ (alarm_control_panel)\n-  `Xiaomi Mi WiFi Repeater 2 <https://www.home-assistant.io/components/device_tracker.xiaomi_miio/>`__ (device_tracker)\n\nHome Assistant (custom)\n^^^^^^^^^^^^^^^^^^^^^^^\n\n-  `Xiaomi Mi Home Air Conditioner Companion <https://github.com/syssi/xiaomi_airconditioningcompanion>`__\n-  `Xiaomi Mi Smart Pedestal Fan <https://github.com/syssi/xiaomi_fan>`__\n-  `Xiaomi Mi Smart Rice Cooker <https://github.com/syssi/xiaomi_cooker>`__\n-  `Xiaomi Raw Sensor <https://github.com/syssi/xiaomi_raw>`__\n-  `Xiaomi MIoT Devices <https://github.com/ha0y/xiaomi_miot_raw>`__\n-  `Xiaomi Miot Auto <https://github.com/al-one/hass-xiaomi-miot>`__\n\nOther related projects\n----------------------\n\nThis is a list of other projects around the Xiaomi ecosystem that you can find interesting.\nFeel free to submit more related projects.\n\n-  `dustcloud <https://github.com/dgiese/dustcloud>`__ (reverse engineering and rooting xiaomi devices)\n-  `Valetudo <https://github.com/Hypfer/Valetudo>`__ (cloud free vacuum firmware)\n-  `micloud <https://github.com/Squachen/micloud>`__ (library to access xiaomi cloud services, can be used to obtain device tokens)\n-  `micloudfaker <https://github.com/unrelentingtech/micloudfaker>`__ (dummy cloud server, can be used to fix powerstrip status requests when without internet access)\n-  `Your project here? Feel free to open a PR! <https://github.com/rytilahti/python-miio/pulls>`__\n\n.. |Chat| image:: https://img.shields.io/matrix/python-miio-chat:matrix.org\n   :target: https://matrix.to/#/#python-miio-chat:matrix.org\n.. |PyPI version| image:: https://badge.fury.io/py/python-miio.svg\n   :target: https://badge.fury.io/py/python-miio\n.. |PyPI downloads| image:: https://img.shields.io/pypi/dw/python-miio\n   :target: https://pypi.org/project/python-miio/\n.. |Build Status| image:: https://github.com/rytilahti/python-miio/actions/workflows/ci.yml/badge.svg\n   :target: https://github.com/rytilahti/python-miio/actions/workflows/ci.yml\n.. |Coverage Status| image:: https://codecov.io/gh/rytilahti/python-miio/branch/master/graph/badge.svg?token=lYKWubxkLU\n   :target: https://codecov.io/gh/rytilahti/python-miio\n.. |Docs| image:: https://readthedocs.org/projects/python-miio/badge/?version=latest\n   :alt: Documentation status\n   :target: https://python-miio.readthedocs.io/en/latest/?badge=latest\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n',
    'author': 'Teemu R',
    'author_email': 'tpr@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rytilahti/python-miio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
