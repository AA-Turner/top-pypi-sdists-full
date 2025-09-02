# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'packages'}

packages = \
['aioserial']

package_data = \
{'': ['*']}

install_requires = \
['pyserial']

setup_kwargs = {
    'name': 'aioserial',
    'version': '1.3.1',
    'description': 'An asynchronous serial port library of Python',
    'long_description': "# aioserial\n\n* [Quick start](#quick-start)\n    + [A simple serial port reader](#a-simple-serial-port-reader)\n    + [pyserial-asyncio example replacement](#pyserial-asyncio-example-replacement)\n* [API](#api)\n    + [AioSerial](#aioserial)\n        - [Constructor](#constructor)\n        - [Methods](#methods)\n            * [read_async](#read-async)\n            * [read_until_async](#read-until-async)\n            * [readinto_async](#readinto-async)\n            * [readline_async](#readline-async)\n            * [readlines_async](#readlines-async)\n            * [write_async](#write-async)\n            * [writelines_async](#writelines-async)\n    + [Other APIs](#other-apis)\n* [Why aioserial?](#why-aioserial-)\n\nA Python package that combines [asyncio](https://docs.python.org/3/library/asyncio.html) and [pySerial](https://pypi.org/project/pyserial/).\n\n## Quick start\n\n### A simple serial port reader\n\n```py\nimport asyncio\n\nimport aioserial\n\n\nasync def read_and_print(aioserial_instance: aioserial.AioSerial):\n    while True:\n        print((await aioserial_instance.read_async()).decode(errors='ignore'), end='', flush=True)\n\nasyncio.run(read_and_print(aioserial.AioSerial(port='COM1')))\n```\n\n### pyserial-asyncio example replacement\n\n**The example usage from pyserial-asyncio**\n\nhttps://pyserial-asyncio.readthedocs.io/en/latest/shortintro.html\n\n```py\nimport asyncio\nimport serial_asyncio\n\nclass Output(asyncio.Protocol):\n    def connection_made(self, transport):\n        self.transport = transport\n        print('port opened', transport)\n        transport.serial.rts = False  # You can manipulate Serial object via transport\n        transport.write(b'Hello, World!\\n')  # Write serial data via transport\n\n    def data_received(self, data):\n        print('data received', repr(data))\n        if b'\\n' in data:\n            self.transport.close()\n\n    def connection_lost(self, exc):\n        print('port closed')\n        self.transport.loop.stop()\n\n    def pause_writing(self):\n        print('pause writing')\n        print(self.transport.get_write_buffer_size())\n\n    def resume_writing(self):\n        print(self.transport.get_write_buffer_size())\n        print('resume writing')\n\nloop = asyncio.get_event_loop()\ncoro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200)\nloop.run_until_complete(coro)\nloop.run_forever()\nloop.close()\n```\n\n**aioserial equivalence**\n\n```py\nimport asyncio\n\nimport aioserial\n\n\nasync def read_and_print(aioserial_instance: aioserial.AioSerial):\n    while True:\n        data: bytes = await aioserial_instance.read_async()\n        print(data.decode(errors='ignore'), end='', flush=True)\n        if b'\\n' in data:\n            aioserial_instance.close()\n            break\n\naioserial_instance: aioserial.AioSerial = aioserial.AioSerial(port='/dev/ttyUSB0', baudrate=115200)\nasyncio.run(asyncio.gather(read_and_print(aioserial_instance), aioserial_instance.write_async(b'Hello, World!\\n')))\n```\n\n## API\n\n### AioSerial\n\n```py\n>>> import aioserial\n>>> import serial\n\n>>> isinstance(aioserial.AioSerial(), serial.Serial)\nTrue\n\n>>> issubclass(aioserial.AioSerial, serial.Serial)\nTrue\n\n>>> aioserial.Serial is serial.Serial\nTrue\n```\n\n#### Constructor\n\n```py\naioserial_instance: aioserial.AioSerial = aioserial.AioSerial(\n    # ... same with what can be passed to serial.Serial ...,\n    loop: Optional[asyncio.AbstractEventLoop] = None,\n    cancel_read_timeout: int = 1,\n    cancel_write_timeout: int = 1)\n```\n\n#### Methods\n\n\n##### read_async\n\n```py\nbytes_read: bytes = \\\n    await aioserial_instance.read_async(size: int = 1)\n```\n\n##### read_until_async\n\n```py\nat_most_certain_size_of_bytes_read: bytes = \\\n    await aioserial_instance.read_until_async(\n        expected: bytes = aioserial.LF, size: Optional[int] = None)\n```\n\n##### readinto_async\n\n```py\nnumber_of_byte_read: int = \\\n    await aioserial_instance.readinto_async(b: Union[array.array, bytearray])\n```\n\n##### readline_async\n\n```py\na_line_of_at_most_certain_size_of_bytes_read: bytes = \\\n    await aioserial_instance.readline_async(size: int = -1)\n```\n\n##### readlines_async\n\n```py\nlines_of_at_most_certain_size_of_bytes_read: bytes = \\\n    await aioserial_instance.readlines_async(hint: int = -1)\n```\n\n##### write_async\n\n```py\nnumber_of_byte_like_data_written: int = \\\n    await aioserial_instance.write_async(bytes_like_data)\n```\n\n##### writelines_async\n\n```py\nnumber_of_byte_like_data_in_the_given_list_written: int = \\\n    await aioserial_instance.writelines_async(list_of_bytes_like_data)\n```\n\n### Other APIs\n\nAll the other APIs in the mother package [pySerial](https://pypi.org/project/pyserial/) are supported in aioserial as-is.\n\n## Why aioserial?\n\n* Want to use an asyncio-based but not a (self-built) thread-based serial library.\n* [pySerial-asyncio](https://pypi.org/project/pyserial-asyncio/) does [not support Windows](https://github.com/pyserial/pyserial-asyncio/issues/3).\n* APIs in all the other packages ([pySerial-asyncio](https://pypi.org/project/pyserial-asyncio/),\n    [asyncserial](https://pypi.org/project/asyncserial/)) that target the same goal are not designed in high level.\n",
    'author': 'Johann Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/changyuheng/aioserial.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
