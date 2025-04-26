from mimetypes import guess_type

import aiohttp
from rich.console import Console

from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.utils.logger import logger

console = Console()


async def send_file_to_datalake(
    directory: str, file: bytes, filename: str, file_extension: str = None
) -> None:
    """
    Envia um arquivo para a datalake.

    Args:
        file (bytes): O conteúdo binário do arquivo.
        filename (str): O nome do arquivo.
        file_extension (str, optional): A extensão do arquivo. Caso não seja
            passada, tenta determinar com base no nome do arquivo.

    Raises:
        aiohttp.ClientResponseError: Caso a API retorne um status de erro.
        Exception: Caso ocorra um erro genérico durante o processo.

    Returns:
        None
    """
    try:
        env_config, _ = load_env_config()

        if not file_extension:
            file_extension = filename.split(".")[-1]

        mime_type, _ = guess_type(filename)
        if not mime_type:
            mime_type = "application/octet-stream"

        body = aiohttp.FormData()
        body.add_field("file", file, filename=filename, content_type=mime_type)
        body.add_field("directoryBucket", directory)

        headers_basic = {"Authorization": f"Basic {env_config['API_AUTHORIZATION']}"}

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.post(
                f"{env_config['API_BASE_URL']}/arquivo/send-file-to-datalake",
                data=body,
                headers=headers_basic,
            ) as response:
                response.raise_for_status()

                response_text = await response.text()

                log_msg = f"\nSucesso ao enviar arquivo: {filename}\nResposta da API: {response_text}"
                console.print(log_msg, style="bold green")
                logger.info(log_msg)

    except aiohttp.ClientResponseError as e:
        err_msg = f"Erro na resposta da API: {e.status} - {e.message}\nDetalhes: {await e.response.text()}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

    except Exception as e:
        err_msg = f"Erro ao enviar arquivo: {str(e)}"
        console.print(f"\n{err_msg}\n", style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
