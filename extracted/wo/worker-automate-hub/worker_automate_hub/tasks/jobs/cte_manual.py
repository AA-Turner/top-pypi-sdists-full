from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO


async def cte_manual(task: RpaProcessoEntradaDTO):
    chaveCte = task.configEntrada.get("chaveCte")
    return RpaRetornoProcessoDTO(
        sucesso=False,
        retorno=f"CTE Não automatizado. Realize a importação manualmente. CHAVE: {chaveCte}",
        status=RpaHistoricoStatusEnum.Falha,
        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
    )
