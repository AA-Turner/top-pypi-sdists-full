from datetime import datetime

import aiohttp
from pytz import timezone
from rich.console import Console

from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dao.rpa_historico import RpaHistorico
from worker_automate_hub.models.dao.rpa_processo import RpaProcesso
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoRequestDTO,
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger

console = Console()


async def create_store_historico(
    task: RpaProcessoEntradaDTO,
    processo: RpaProcesso,
    status: RpaHistoricoStatusEnum,
    retorno_processo: RpaRetornoProcessoDTO = None,
) -> RpaHistorico:
    """
    Salva o histórico de um processo com status Processando.

    Recebe um RpaProcessoEntradaDTO e um RpaProcesso como parâmetro e salva o
    histórico com status Processando. Retorna um dicionário com o uuid do
    histórico salvo.

    Args:
        task (RpaProcessoEntradaDTO): O processo a ser salvo.
        processo (RpaProcesso): O processo que está sendo executado.

    Returns:
        RpaHistorico: Dicionário com o uuid do histórico salvo.
    """
    try:
        from worker_automate_hub.config.settings import load_worker_config

        worker_config = load_worker_config()
        tz = timezone("America/Sao_Paulo")
        start_time = datetime.now(tz).isoformat()
        prioridade = task.prioridade or processo.prioridade or 1

        identificador_processo = (
            task.configEntrada.get("nfe")
            or task.configEntrada.get("chaveCte")
            or task.configEntrada.get("empresa")
            or task.configEntrada.get("uuidSimplifica")
            or ""
        )

        # Armazenar início da operação no histórico
        start_data = RpaHistoricoRequestDTO(
            uuidProcesso=task.uuidProcesso,
            uuidRobo=worker_config["UUID_ROBO"],
            prioridade=prioridade,
            desStatus=status,
            configEntrada=task.configEntrada,
            datInicioExecucao=start_time,
            datEntradaFila=task.datEntradaFila,
            identificador=identificador_processo,
            retorno=retorno_processo,
        )

        store_response: RpaHistorico = await store(start_data)
        console.print(
            f"\nHistorico salvo com o uuid: {store_response.uuidHistorico}\n",
            style="green",
        )
        return store_response
    except Exception as e:
        err_msg = f"Erro ao salvar o registro no histórico: {e}"
        console.print(f"\n{err_msg}\n", style="red")
        logger.error(f"{err_msg}")


async def create_update_historico(
    historico_uuid: str,
    task: RpaProcessoEntradaDTO,
    retorno_processo: RpaRetornoProcessoDTO,
    processo: RpaProcesso,
):
    """
    Atualiza o histórico de um processo com o status de sucesso ou falha.

    Recebe o uuid do histórico, o RpaProcessoEntradaDTO do processo, um booleano
    indicando se o processo foi um sucesso ou não, o RpaRetornoProcessoDTO do
    processo e o RpaProcesso do processo como parâmetro e atualiza o histórico
    com o status de sucesso ou falha. Retorna um dicionário com o uuid do
    histórico atualizado.

    Args:
        historico_uuid (str): O uuid do histórico.
        task (RpaProcessoEntradaDTO): O RpaProcessoEntradaDTO do processo.
        sucesso (bool): Um booleano indicando se o processo foi um sucesso ou não.
        retorno_processo (RpaRetornoProcessoDTO): O RpaRetornoProcessoDTO do processo.
        processo (RpaProcesso): O RpaProcesso do processo.

    Returns:
        RpaHistorico: Dicionário com o uuid do histórico atualizado.
    """

    try:
        from worker_automate_hub.config.settings import load_worker_config

        worker_config = load_worker_config()
        tz = timezone("America/Sao_Paulo")
        des_status: RpaHistoricoStatusEnum = retorno_processo.status
        end_time = datetime.now(tz).isoformat()
        prioridade = task.prioridade or processo.prioridade or 1

        identificador_processo = (
            task.configEntrada.get("nfe") 
            or task.configEntrada.get("chaveCte")
            or task.configEntrada.get("empresa")
            or task.configEntrada.get("uuidSimplifica")
            or ""
        )
        if not retorno_processo.tags:
            retorno_processo.tags = []

        # Armazenar fim da operação no histórico
        end_data = RpaHistoricoRequestDTO(
            uuidHistorico=historico_uuid,
            uuidProcesso=task.uuidProcesso,
            uuidRobo=worker_config["UUID_ROBO"],
            prioridade=prioridade,
            desStatus=des_status,
            configEntrada=task.configEntrada,
            retorno=retorno_processo,
            datFimExecucao=end_time,
            identificador=identificador_processo,
            tags=retorno_processo.tags,
        )

        update_response: RpaHistorico = await update(end_data)
        console.print(
            f"\nHistorico atualizado com o uuid: {update_response.uuidHistorico}\n",
            style="green",
        )
        return update_response

    except Exception as e:
        err_msg = f"Erro ao atualizar o histórico do processo: {e}"
        console.print(f"\n{err_msg}\n", style="red")
        logger.error(err_msg)


async def store(data: RpaHistoricoRequestDTO) -> dict:
    """
    Armazena o histórico de um processo com status Processando.

    Recebe um RpaHistoricoRequestDTO como parâmetro e salva o
    histórico com status Processando. Retorna um dicionário com o uuid do
    histórico salvo.

    Args:
        data (RpaHistoricoRequestDTO): O histórico a ser salvo.

    Returns:
        RpaHistorico: Dicionário com o uuid do histórico salvo.
    """
    env_config, _ = load_env_config()

    if not data:
        raise ValueError("Parâmetro data deve ser informado")

    if not isinstance(data, RpaHistoricoRequestDTO):
        raise TypeError("Parâmetro data deve ser do tipo RpaHistoricoRequestDTO")

    headers_basic = {
        "Authorization": f"Basic {env_config['API_AUTHORIZATION']}",
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=True)
        ) as session:
            payload = data.model_dump_json()

            async with session.post(
                f"{env_config['API_BASE_URL']}/historico",
                data=payload,
                headers=headers_basic,
            ) as response:
                response_text = await response.text()
                logger.info(f"Resposta store: {response_text}")

                if response.status == 200:
                    try:
                        response_data = await response.json()
                        return RpaHistorico(**response_data)
                    except aiohttp.ContentTypeError:
                        return {
                            "error": "Resposta não é JSON",
                            "status_code": response.status,
                        }
                else:
                    return {"error": response_text, "status_code": response.status}
    except aiohttp.ClientError as e:
        logger.error(f"Erro de cliente aiohttp: {str(e)}")
        return {"error": str(e), "status_code": 500}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"error": str(e), "status_code": 500}


async def update(data: RpaHistoricoRequestDTO) -> dict:
    """
    Atualiza um registro de histórico com base no uuidHistorico informado.

    Args:
        data (RpaHistoricoRequestDTO): Os dados do histórico a ser atualizado.

    Returns:
        RpaHistorico: O histórico atualizado.
    """
    env_config, _ = load_env_config()
    headers_basic = {
        "Authorization": f"Basic {env_config['API_AUTHORIZATION']}",
        "Content-Type": "application/json",
    }
    if not data or not isinstance(data, RpaHistoricoRequestDTO):
        raise TypeError("Parâmetro data deve ser do tipo RpaHistoricoRequestDTO")
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=True)
        ) as session:
            if not data.uuidHistorico:
                raise ValueError("Parâmetro uuidHistorico deve ser informado")

            payload = data.model_dump_json()

            async with session.put(
                f"{env_config['API_BASE_URL']}/historico",
                data=payload,
                headers=headers_basic,
            ) as response:
                response_text = await response.text()
                logger.info(f"Resposta update: {response_text}")

                if response.status == 200:
                    try:
                        response_data = await response.json()
                        return RpaHistorico(**response_data)
                    except aiohttp.ContentTypeError:
                        return {
                            "error": "Resposta não é JSON",
                            "status_code": response.status,
                        }
                else:
                    return {"error": response_text, "status_code": response.status}
    except aiohttp.ClientError as e:
        logger.error(f"Erro de cliente aiohttp: {str(e)}")
        return {"error": str(e), "status_code": 500}
    except ValueError as e:
        logger.error(f"Erro de valor: {str(e)}")
        return {"error": str(e), "status_code": 400}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"error": str(e), "status_code": 500}
