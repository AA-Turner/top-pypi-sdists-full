import asyncio
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def update(domain, password, host, ttl=60, session=None):
    data = {
        'domain': domain,
        'password': password,
        'command': "REPLACE {} {} A DYNAMIC_IP".format(host, ttl)
    }

    async with session or aiohttp.ClientSession() as session:
        try:
            resp = await asyncio.gather(session.post('https://dnsapi4.mythic-beasts.com/',data=data))
            body = await resp[0].text()

            if body.startswith("REPLACE"):
                _LOGGER.debug("Updating Mythic Beasts successful: %s", body)
                return True

            if body.startswith("ERR"):
                _LOGGER.error("Updating Mythic Beasts failed: %s",
                              body.partition(' ')[2])

            if body.startswith("NREPLACE"):
                _LOGGER.warning("Updating Mythic Beasts failed: %s",
                                body.partition(';')[2])

        except Exception as e:
            _LOGGER.error("Updating Mythic Beasts failed: %s", e)

        return False
