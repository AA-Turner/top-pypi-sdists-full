import threading

from rich.console import Console

from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import check_for_update

console = Console()


async def handle_api_response(response, stop_event: threading.Event, last_alive=False):
    """
    Trata as respostas da API baseadas no status HTTP.

    Args:
        response: Objeto de resposta da API.
        stop_event: Evento para parar as threads, usado para o processo de atualização.
        last_alive: Booleano para diferenciar a notificação de "alive" de outros tipos de resposta.
    """
    status = response.status

    def log_and_print_message(message, style="red", log_level="error"):
        """Loga e imprime a mensagem com o estilo e nível de log fornecidos."""
        console.print(message, style=style)
        log_func = getattr(logger, log_level)
        log_func(message)

    if last_alive:
        handle_last_alive_response(status)
    else:
        return await handle_task_response(response, status, stop_event)


def handle_last_alive_response(status):
    """
    Trata respostas específicas para a última notificação "alive".

    Args:
        status: Código de status da resposta HTTP.
    """
    match status:
        case 200:
            log_and_print_message(
                "\n[Worker last alive] Informado salvo com sucesso.\n",
                style="bold green",
                log_level="info",
            )
        case 500:
            log_and_print_message("500 - Erro interno da API!")
        case 503:
            log_and_print_message("503 - Serviço indisponível ou worker inativo!")
        case _:
            log_and_print_message(f"Status não tratado: {status}")


async def handle_task_response(response, status, stop_event):
    """
    Trata as respostas da API para as tarefas.

    Args:
        response: Objeto de resposta da API.
        status: Código de status da resposta HTTP.
        stop_event: Evento para parar as threads, usado para o processo de atualização.

    Returns:
        Retorna um dicionário com dados ou None, dependendo da resposta.
    """
    match status:
        case 200:
            data = await response.json()
            return {"data": data, "update": False}
        case 204:
            log_and_print_message(
                "204 - Nenhum processo encontrado", style="yellow", log_level="info"
            )
        case 300:
            log_and_print_message(
                "300 - Necessário atualização!", style="blue", log_level="info"
            )
            check_for_update(stop_event)
        case 401:
            log_and_print_message("401 - Acesso não autorizado!")
        case 404:
            log_and_print_message(
                "404 - Nenhum processo disponível!", style="yellow", log_level="warning"
            )
        case 500:
            log_and_print_message("500 - Erro interno da API!")
        case 503:
            log_and_print_message("503 - Serviço indisponível ou worker inativo!")
        case _:
            log_and_print_message(f"Status não tratado: {status}")

    return None


def log_and_print_message(message, style="red", log_level="error"):
    """
    Função utilitária para logar e imprimir mensagens com estilos e níveis de log customizáveis.

    Args:
        message: Texto da mensagem.
        style: Estilo da mensagem no Rich Console.
        log_level: Nível de log (info, warning, error).
    """
    console.print(message, style=style)
    log_func = getattr(logger, log_level)
    log_func(message)
