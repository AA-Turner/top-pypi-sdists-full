import aiohttp
from rich.console import Console

from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger

console = Console()


async def burn_queue(id_fila: str):
    env_config, _ = load_env_config()
    try:

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=True)
        ) as session:
            async with session.delete(
                f"{env_config["API_BASE_URL"]}/fila/burn-queue/{id_fila}",
                headers=headers_basic,
            ) as response:
                if response.status == 200:
                    logger.info("Fila excluida com sucesso.")
                    console.print("\nFila excluida com sucesso.\n", style="bold green")
                else:
                    logger.error(f"Erro ao excluir a fila: {response.content}")
                    console.print(
                        f"Erro ao excluir a fila: {response.content}", style="bold red"
                    )

    except Exception as e:
        err_msg = f"Erro remover registro da fila: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None


async def unlock_queue(id: str):
    env_config, _ = load_env_config()
    try:
        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=True)
        ) as session:
            async with session.get(
                f"{env_config["API_BASE_URL"]}/fila/unlock-queue/{id}",
                headers=headers_basic,
            ) as response:
                return await response.text()

    except Exception as e:
        err_msg = f"Erro ao desbloquear a fila: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None
