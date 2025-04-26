import asyncio
import random

import pandas as pd
import pyautogui
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger

# Variável global para armazenar o status atual da tarefa
current_task_status = {
    "step": 0,
    "total_steps": 0,
    "description": "Sem tarefa",
}


async def update_task_status(step, total_steps, description):
    global current_task_status
    current_task_status = {
        "step": step,
        "total_steps": total_steps,
        "description": description,
    }


async def exemplo_processo(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        num_actions = 10
        actions = []

        await update_task_status(0, num_actions, "Iniciando")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Iniciando...", total=num_actions)

            for i in range(num_actions):
                screen_width, screen_height = pyautogui.size()
                x = random.randint(0, screen_width - 1)
                y = random.randint(0, screen_height - 1)

                action_type = random.choice(["move", "click", "write"])
                if action_type == "move":
                    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.0))
                elif action_type == "click":
                    pyautogui.click(x, y)
                elif action_type == "write":
                    pyautogui.click(x, y)
                    pyautogui.write("Hello", interval=0.1)

                # Atualizando a variável global de status da tarefa
                await update_task_status(
                    i + 1,
                    num_actions,
                    f"Executando ação {i + 1}/{num_actions}: {action_type}",
                )

                # Atualizando a barra de progresso
                progress.update(
                    task,
                    advance=1,
                    description=f"Executando ação {i + 1}/{num_actions}: {action_type}",
                )

                await asyncio.sleep(12)

            filename = "random_actions.xlsx"
            df = pd.DataFrame(actions)
            df.to_excel(filename, index=False)

        logger.info("Processo executado com sucesso")
        print("Processo executado com sucesso")
        await update_task_status(0, 0, "Sem tarefa")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Task executed successfully and data saved to Excel.",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        logger.error(f"Erro ao executar o processo: {e}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"An error occurred: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
