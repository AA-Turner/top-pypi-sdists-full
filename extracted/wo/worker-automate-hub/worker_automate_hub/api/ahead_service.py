import asyncio
import os
from pathlib import Path
import getpass
import aiohttp
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger


async def get_xml(chave_acesso: str):
    env_config, _ = load_env_config()
    try:
        headers_bearer = {"Authorization": f"Basic {env_config['API_AUTHORIZATION']}"}
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(
                f"{env_config['API_BASE_URL']}/api-ahead/get-xml",
                params={"chaveAcesso": chave_acesso},
                headers=headers_bearer,
            ) as response:
                print("Response:", response)
                if response.status == 200:
                    return await response.text()
                else:
                    err_msg = (
                        f"Erro ao obter o XML: {response.status} - {response.reason}"
                    )
                    logger.error(err_msg)
                    return None
    except Exception as e:
        err_msg = f"Erro ao obter o XML: {e}"
        logger.error(err_msg)
        return None


async def save_xml_to_downloads(chave_acesso: str):
    MAX_RETRIES = 5

    for attempt in range(1, MAX_RETRIES + 1):
        xml_content = await get_xml(chave_acesso)
        if xml_content:
            try:
                downloads_path = Path.home() / "Downloads"
                downloads_path.mkdir(parents=True, exist_ok=True)

                file_name = f"{chave_acesso}.xml"
                file_path = downloads_path / file_name

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(xml_content)

                logger.info(f"XML salvo em {file_path}")
                return True
            except Exception as e:
                err_msg = f"Erro ao salvar o XML: {e}"
                logger.error(err_msg)
        else:
            err_msg = "Não foi possível obter o XML."
            logger.error(err_msg)

        if attempt < MAX_RETRIES:
            await asyncio.sleep(15)

    return False
