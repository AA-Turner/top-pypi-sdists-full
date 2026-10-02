import asyncio

from pydantic import ValidationError
from rich.console import Console
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

console = Console()


async def playground(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        console.print(
            f"\nProcesso de teste iniciado: {task.nomProcesso}\n", style="green"
        )
        max_attempts = 15
        for numero in range(1, max_attempts):
            console.print(f"Etapa [{numero}] de {max_attempts}", style="green")
            await asyncio.sleep(1)
        console.print(f"Processo de teste finalizado.", style="green")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo de teste executado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except ValidationError as exc:
        console.print(
            f"Erro de validação ao executar o processo de teste: {repr(exc.errors()[0]['type'])}",
            style="bold red",
        )
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro de validação ao executar o processo de teste: {repr(exc.errors()[0]['type'])}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

    except Exception as e:
        console.print(f"Erro ao executar o processo de teste: {e}", style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao executar o processo de teste: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
