from worker_automate_hub.utils.logger import logger
from rich.console import Console

import aiohttp

console = Console()

async def send_to_webhook(
    url_retorno: str,
    status: str,
    observacao: str,
    identificador_webhook: str = None
) -> None:    
    """
    Envia uma notificacao para o endpoint do webhook passado como parametro.

    Args:
        url_retorno (str): URL do endpoint do webhook.
        status (str): Status da notificacao.
        observacao (str): Observacao da notificacao.

    Raises:
        ValueError: Se a URL, status ou observacao forem vazias.
    """
    if not url_retorno:
        raise ValueError("URL do retorno esta vazia.")

    if not status:
        raise ValueError("Status da notificacao esta vazio.")

    if not observacao:
        raise ValueError("Observacao da notificacao esta vazia.")

    data = {
        "status": status,
        "observacao": observacao,
    }

    if identificador_webhook:
        data["identificador"] = identificador_webhook

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(f"{url_retorno}", data=data) as response:
                data = await response.text()
                if response.status != 200:
                    raise Exception(f"Erro ao enviar notificacao: {data}")

                log_msg = f"\nSucesso ao enviar {data}\n para o webhook: {url_retorno}.\n"
                console.print(
                    log_msg,
                    style="bold green",
                )
                logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do webhook: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.info(err_msg)