import asyncio
import os
import threading
from pathlib import Path

import pyfiglet
from rich.console import Console

from worker_automate_hub.api.client import (
    get_new_task,
    get_processo,
    notify_is_alive,
    send_gchat_message,
)
from worker_automate_hub.api.rpa_fila_service import burn_queue
from worker_automate_hub.api.rpa_historico_service import (
    create_store_historico,
)
from worker_automate_hub.api.webhook_service import send_to_webhook
from worker_automate_hub.config.settings import (
    load_env_config,
    load_worker_config,
)
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
from worker_automate_hub.tasks.task_definitions import is_uuid_in_tasks
from worker_automate_hub.tasks.task_executor import perform_task
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import (
    close_other_cmd_windows,
    get_installed_version,
    update_version_in_toml,
)
from worker_automate_hub.utils.util import check_screen_resolution

console = Console()


async def check_and_execute_tasks(stop_event: threading.Event):

    while not stop_event.is_set():
        try:
            task: RpaProcessoEntradaDTO = await get_new_task(stop_event)
            worker_config = load_worker_config()
            if task is not None:
                processo_existe = await is_uuid_in_tasks(task.uuidProcesso)
                if processo_existe:
                    await burn_queue(task.uuidFila)
                    logger.info(f"Executando a task: {task.nomProcesso}")
                    await perform_task(task)
                else:
                    log_message = f"O processo [{task.nomProcesso}] não existe no Worker [{worker_config['NOME_ROBO']}] e foi removido da fila."
                    console.print(f"\n{log_message}\n", style="yellow")
                    logger.error(log_message)
                    try:
                        processo: RpaProcesso = await get_processo(task.uuidProcesso)
                        await create_store_historico(
                            task,
                            processo,
                            RpaHistoricoStatusEnum.Descartado,
                            retorno_processo=RpaRetornoProcessoDTO(
                                sucesso=False,
                                retorno=log_message,
                                status=RpaHistoricoStatusEnum.Descartado,
                                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                            ),
                        )
                        # Libera o registro da fila e informa o chat
                        await burn_queue(task.uuidFila)
                        await send_gchat_message(log_message)
                    except Exception as e:
                        console.print(
                            f"Erro ao salvar histórico de processo não implementado: {e}",
                            style="bold red",
                        )
                    url_retorno = task.configEntrada.get("urlRetorno", None)

                    if url_retorno is not None:
                        await send_to_webhook(
                            url_retorno, RpaHistoricoStatusEnum.Descartado, log_message
                        )
            else:
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Ocorreu um erro de execução: {e}")
            await asyncio.sleep(5)


async def notify_alive(stop_event: threading.Event):

    env_config, _ = load_env_config()

    while not stop_event.is_set():
        try:
            logger.info("Notificando last alive...")
            await notify_is_alive(stop_event)
            await asyncio.sleep(int(env_config["NOTIFY_ALIVE_INTERVAL"]))
        except Exception as e:
            logger.error(f"Erro ao notificar que está ativo: {e}")
            await asyncio.sleep(int(env_config["NOTIFY_ALIVE_INTERVAL"]))


def run_async_tasks(stop_event: threading.Event):
    asyncio.run(check_and_execute_tasks(stop_event))


def run_async_last_alive(stop_event: threading.Event):
    asyncio.run(notify_alive(stop_event))


def main_process(stop_event: threading.Event):
    close_other_cmd_windows()

    current_dir = Path.cwd()
    toml_file_path = os.path.join(current_dir, "settings.toml")
    atual_version = get_installed_version("worker-automate-hub")
    update_version_in_toml(toml_file_path, atual_version)
    worker_config = load_worker_config()

    custom_font = "slant"
    ascii_banner = pyfiglet.figlet_format(f"Worker", font=custom_font)
    # os.system("cls") Comentado temporariamente
    console.print(ascii_banner + f" versão: {atual_version}\n", style="bold blue")
    initial_msg = f"Worker em execução: {worker_config['NOME_ROBO']}"
    logger.info(initial_msg)
    console.print(f"{initial_msg}\n", style="green")

    # Verifica se a resolução da tela é compatível
    check_screen_resolution()

    # Cria duas threads para rodar as funções simultaneamente
    thread_automacao = threading.Thread(target=run_async_tasks, args=(stop_event,))
    thread_status = threading.Thread(target=run_async_last_alive, args=(stop_event,))

    # Inicia as duas threads
    thread_automacao.start()
    thread_status.start()

    # Garante que o programa principal aguarde ambas as threads com verificação periódica
    while thread_automacao.is_alive() and thread_status.is_alive():
        thread_automacao.join(timeout=1)
        thread_status.join(timeout=1)


def run_worker(stop_event: threading.Event):
    try:
        main_process(stop_event)
    except KeyboardInterrupt:
        console.print("\nEncerrando threads...\n", style="yellow")

        # Sinalizar para as threads que devem parar
        stop_event.set()

        # Garante que o programa principal aguarde ambas as threads
        console.print("\nThreads finalizadas.\n", style="green")
    except asyncio.CancelledError:
        logger.info("Aplicação encerrada pelo usuário.")
    except Exception as e:
        logger.error(f"Erro não tratado: {e}")
