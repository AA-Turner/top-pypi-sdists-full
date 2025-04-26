from rich.console import Console

from worker_automate_hub.api.client import get_processo, send_gchat_message
from worker_automate_hub.api.rpa_fila_service import unlock_queue
from worker_automate_hub.api.rpa_historico_service import (
    create_store_historico,
    create_update_historico,
)
from worker_automate_hub.api.webhook_service import send_to_webhook
from worker_automate_hub.config.settings import load_worker_config
from worker_automate_hub.models.dao.rpa_historico import RpaHistorico
from worker_automate_hub.models.dao.rpa_processo import RpaProcesso
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.tasks.task_definitions import task_definitions
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.toast import show_toast
from worker_automate_hub.utils.util import capture_and_send_screenshot

console = Console()


async def perform_task(task: RpaProcessoEntradaDTO):
    log_msg = f"Processo a ser executado: {task.nomProcesso}"
    show_toast("Info", f"Processo a ser executado: {task.nomProcesso}")

    console.print(f"\n{log_msg}\n", style="green")
    logger.info(log_msg)
    task_uuid = task.uuidProcesso
    url_retorno = task.configEntrada.get("urlRetorno", None)
    identificador_webhook = task.configEntrada.get("identificador", None)
    processo: RpaProcesso = await get_processo(task_uuid)
    if processo is None:
        worker_config = load_worker_config()
        err_msg = f"[WORKER] [{worker_config['NOME_ROBO']}] Falha ao obter o processo [{task.nomProcesso}] uuid [{task_uuid}] da API, não foi possivel registrar o historico, mas o processo será executado."
        console.print(err_msg, style="yellow")
        logger.error(err_msg)
        show_toast("Erro", err_msg)
        await send_gchat_message(err_msg)
        registrar_historico = False
    else:
        registrar_historico = True

    if registrar_historico:
        historico: RpaHistorico = await create_store_historico(
            task, processo, RpaHistoricoStatusEnum.Processando
        )
    try:
        if task_uuid in task_definitions:
            # Executar a task
            # if task_uuid == "276d0c41-0b7c-4446-ae0b-dd5d782917cc" or task_uuid == "5d8a529e-b323-453f-82a3-980184a16b52":
            task.historico_id = historico.uuidHistorico

            result: RpaRetornoProcessoDTO = await task_definitions[task_uuid](task)
            if registrar_historico:
                await create_update_historico(
                    historico_uuid=historico.uuidHistorico,
                    task=task,
                    retorno_processo=result,
                    processo=processo,
                )

            if result.sucesso == False:
                show_toast("Erro", f"Processo executado com falha: {result}")

                await capture_and_send_screenshot(
                    uuidRelacao=historico.uuidHistorico, desArquivo=result.retorno
                )
            else:
                show_toast("Sucesso", f"Processo executado com sucesso: {result}")

            if url_retorno is not None and result.sucesso == False:
                if identificador_webhook:
                    await send_to_webhook(
                        url_retorno,
                        result.status,
                        result.retorno,
                        identificador_webhook,
                    )
                else:
                    await send_to_webhook(url_retorno, result.status, result.retorno)
            return result
        else:
            err_msg = f"Falha ao buscar o processo {task.nomProcesso} na API."
            console.print(err_msg, style="yellow")
            logger.error(err_msg)
            show_toast("Erro", err_msg)
            await send_gchat_message(err_msg)

            if registrar_historico:
                await create_update_historico(
                    historico_uuid=historico.uuidHistorico,
                    task=task,
                    retorno_processo=RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=err_msg,
                        status=RpaHistoricoStatusEnum.Descartado,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    ),
                    processo=processo,
                )
            await unlock_queue(task.uuidFila)
            if url_retorno is not None:
                await send_to_webhook(
                    url_retorno, RpaHistoricoStatusEnum.Descartado, err_msg
                )
            return None
    except Exception as e:
        err_msg = f"Erro ao performar o processo: {e}"
        console.print(f"\n{err_msg}\n", style="red")
        logger.error(err_msg)
        show_toast("Erro", err_msg)

        if registrar_historico:
            await create_update_historico(
                historico_uuid=historico.uuidHistorico,
                task=task,
                retorno_processo=RpaRetornoProcessoDTO(
                    sucesso=False, retorno=err_msg, status=RpaHistoricoStatusEnum.Falha
                ),
                processo=processo,
            )
        await capture_and_send_screenshot(
            uuidRelacao=historico.uuidHistorico, desArquivo=err_msg
        )
        if url_retorno is not None:
            await send_to_webhook(url_retorno, RpaHistoricoStatusEnum.Falha, err_msg)
