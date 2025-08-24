from __future__ import annotations

import asyncio
import contextlib
from pathlib import Path

from loguru import logger

from flexget import plugin
from flexget.event import event
from flexget.plugin import PluginError
from flexget.utils.simple_persistence import SimplePersistence

with contextlib.suppress(ImportError):
    from nio import AsyncClient, JoinError, LoginResponse, RoomSendError, UploadError

with contextlib.suppress(ImportError):
    import aiofiles
    import magic
    from aiofiles import os
    from PIL import Image

plugin_name = 'matrix'

logger = logger.bind(name=plugin_name)
persist = SimplePersistence('matrix')


class PotentialCacheError(PluginError):
    """Exception to be thrown when the failure is suspected to result from cache inconsistency or invalidation."""


class MatrixNotifier:
    """Send messages via Matrix.

    The ``matrix`` extra is required to be installed.
    Install it with: ``pip install flexget[matrix]``

    Configuration:

    - ``server``
    - one of:

      - ``token``
      - ``user``, ``password`` and optional ``device_name``

    - one of:

      - ``room_id``
      - ``room_address``

    - ``images`` (optional)

    ``server``
        Matrix server hostname to integrate to, e.g. ``https://matrix.org``.

    ``token``
        View in Element Desktop -> settings ->  Help & About -> Advanced -> Access Token.

    ``user``
        ``@user_id:user_server``, e.g., ``@gazpachoking:matrix.org``.

    ``password``
        Your password.

    ``device_name``
        The session name used by FlexGet, defaults to ``FlexGet Notifier``.

    ``room_id``
        View in Element Desktop -> room settings -> Advanced -> Access Token. It should start with ``!``.

    ``room_address``
        View in Element Desktop -> room settings -> General -> Internal room ID. It should start with ``#``. You will be joined automatically if you haven't entered the room.

    ``images``
        An array of file paths to images. You need to install the two Python packages ``pillow`` and ``python-magic``.
        Additionally, ``python-magic`` requires the ``libmagic`` C library:

        * For Linux and macOS, see https://github.com/ahupp/python-magic.
        * On Windows, add the ``file.exe`` provided by https://github.com/nscaife/file-windows to your ``PATH`` environment variable.

    Example 1:

    .. code:: yaml

      notify:
        entries:
          via:
            - matrix:
                server: https://matrix.org
                token: mat_K0a8IbdhQL5EsSghilk0axaTeOiUKq_dsBde4
                room_id: '!yVNsbqQZjUqpxOyEgk:matrix.org'

    Example 2:

    .. code:: yaml

      notify:
        entries:
          via:
            - matrix:
                server: https://matrix.org
                user: '@gazpachoking:matrix.org'
                password: ZrJ32Der0ret
                device_name: FlexGet
                room_address: '#flexget:matrix.org'

    Example 3:

    .. code:: yaml

      notify:
        entries:
          via:
            - matrix:
                server: https://matrix.org
                user: '@gazpachoking:matrix.org'
                password: ZrJ32Der0ret
                room_id: '!yVNsbqQZjUqpxOyEgk:matrix.org'
                images:
                  - photo.png
                  - C:/Users/vivodi/Desktop/image.jpg
    """

    schema = {
        'type': 'object',
        'properties': {
            'server': {'type': 'string'},
            'token': {'type': 'string'},
            'user': {'type': 'string'},
            'password': {'type': 'string'},
            'device_name': {'type': 'string'},
            'room_id': {'type': 'string'},
            'room_address': {'type': 'string'},
            'images': {'type': 'array', 'items': {'type': 'string'}},
        },
        'required': ['server'],
        'additionalProperties': False,
        'allOf': [
            {
                'oneOf': [
                    {'required': ['token'], 'not': {'required': ['device_name']}},
                    {'required': ['user', 'password']},
                ]
            },
            {'oneOf': [{'required': ['room_id']}, {'required': ['room_address']}]},
        ],
    }

    def notify(self, title, message, config):
        """Send notification to Matrix room."""
        asyncio.run(self.main(message, config))

    async def login(self, config, client) -> None:
        client.access_token = config.get(
            'token',
            persist.get(config.get('user'))
            if config.get('device_name') is None
            or persist.get('device_name') == config.get('device_name')
            else None,
        )
        if not client.access_token:
            client.user = config['user']
            response = await client.login(
                config['password'],
                device_name=config.get('device_name', 'FlexGet Notifier'),
            )
            if isinstance(response, LoginResponse):
                persist[config['user']] = response.access_token
                persist['device_name'] = config.get('device_name')
                logger.success(
                    'Logged in successfully using password, credentials have been persisted.'
                )
            else:
                logger.error(
                    'Login failed: {}, homeserver = "{}"; user = "{}"',
                    response,
                    config['server'],
                    config['user'],
                )
                raise PotentialCacheError('Login failed')

    async def get_room_id(self, config, client) -> str:
        room_id = config.get('room_id', persist.get(config.get('room_address')))
        if not room_id:
            response = await client.join(config['room_address'])
            if isinstance(response, JoinError):
                raise PluginError(f'Failed to join room: {response.message}')
            logger.success('Successfully joined via room address, room_id has been persisted.')
            room_id = response.room_id
            persist[config['room_address']] = room_id
        return room_id

    async def send_message(self, message, client, room_id) -> None:
        response = await client.room_send(
            room_id=room_id,
            message_type='m.room.message',
            content={'msgtype': 'm.text', 'body': message},
        )
        if isinstance(response, RoomSendError):
            raise PotentialCacheError(f'Failed to send message: {response}')
        logger.success('Message sent successfully, event ID: {}', response.event_id)

    async def send_image(self, client: AsyncClient, room_id: str, image: Path) -> None:
        """Send image to room.

        This is a working example for a JPG image:

        .. code:: json

            "content": {
                "body": "someimage.jpg",
                "info": {
                    "size": 5420,
                    "mimetype": "image/jpeg",
                    "thumbnail_info": {
                        "w": 100,
                        "h": 100,
                        "mimetype": "image/jpeg",
                        "size": 2106
                    },
                    "w": 100,
                    "h": 100,
                    "thumbnail_url": "mxc://example.com/SomeStrangeThumbnailUriKey"
                },
                "msgtype": "m.image",
                "url": "mxc://example.com/SomeStrangeUriKey"
            }
        """
        mime_type = magic.from_file(image, mime=True)
        if not mime_type.startswith('image/'):
            raise PluginError('File does not have an image mime type.')
        (width, height) = Image.open(image).size
        file_stat = await os.stat(image)
        async with aiofiles.open(image, 'r+b') as f:
            resp, _maybe_keys = await client.upload(
                f,
                content_type=mime_type,
                filename=image.name,
                filesize=file_stat.st_size,
            )
        if isinstance(resp, UploadError):
            raise PluginError(f'Failed to upload image. Failure response: {resp}')
        logger.success('Image was uploaded successfully to server.')
        content = {
            'body': image.name,
            'info': {
                'size': file_stat.st_size,
                'mimetype': mime_type,
                'thumbnail_info': None,  # TODO: Add `thumbnail_info`, with its format already specified in the docstring.
                'w': width,
                'h': height,
                'thumbnail_url': None,  # TODO: Add `thumbnail_url`, with its format already specified in the docstring.
            },
            'msgtype': 'm.image',
            'url': resp.content_uri,
        }
        response = await client.room_send(room_id, message_type='m.room.message', content=content)
        if isinstance(response, RoomSendError):
            raise PluginError(f'Failed to send image: {response}')
        logger.success('Image sent successfully, event ID: {}', response.event_id)

    async def main(self, message, config):
        client = AsyncClient(config['server'])
        try:
            for attempt in range(2):
                try:
                    await self.login(config, client)
                    room_id = await self.get_room_id(config, client)
                    await self.send_message(message, client, room_id)
                    for image in config.get('images', []):
                        await self.send_image(client, room_id, Path(image))
                    break
                except PotentialCacheError as e:
                    logger.warning('Attempt #{}/2 failed: {}', attempt + 1, e)
                    if attempt == 0:
                        logger.info(
                            'Clearing potentially expired persisted token {} and room_id {}, preparing to retry...',
                            persist.get(config.get('user')),
                            persist.get(config.get('room_id')),
                        )
                        if config.get('user') in persist:
                            del persist[config['user']]
                        if config.get('room_address') in persist:
                            del persist[config['room_address']]
                        continue
                    raise
        finally:
            await client.close()


@event('plugin.register')
def register_plugin():
    plugin.register(MatrixNotifier, plugin_name, api_ver=2, interfaces=['notifiers'])
