import asyncio
import warnings

import pyautogui
from rich.console import Console

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    find_element_center,
    find_target_position,
    kill_all_emsys,
    take_screenshot,
    type_text_into_field,
    wait_element_ready_win,
)

console = Console()


async def login_emsys_versao_especifica(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    from pywinauto.application import Application

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    try:
        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        # Abre um novo emsys
        app = Application().start("C:\\Rezende\\EMSys3\\EMSys3_29.exe")
        console.print("\nEMSys iniciando...", style="bold green")

        await asyncio.sleep(10)
        # Testa se existe alguma mensagem no Emsys
        window_message_login_emsys = await find_element_center(
            "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 10
        )

        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()

        pyautogui.click(screen_width / 2, screen_height / 2)

        # Clica no "Não mostrar novamente" se existir
        if window_message_login_emsys:
            pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
            pyautogui.click(
                window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
            )
            console.print("Mensagem de login encontrada e fechada.", style="bold green")

        # Ve se o Emsys esta aberto no login
        image_emsys_login = await find_element_center(
            "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 600
        )
        # config_robot = await get_config_by_name("Login EmSys")
        if image_emsys_login:
            # await asyncio.sleep(10)
            # type_text_into_field(
            #     config_robot["EmSys DB"], app["Login"]["ComboBox"], True, "50"
            # )
            # pyautogui.press("enter")
            # await asyncio.sleep(2)

            if await wait_element_ready_win(app["Login"]["Edit2"], 30):
                disconect_database = await find_element_center(
                    "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 300
                )

                if disconect_database:
                    # Realiza login no Emsys
                    type_text_into_field(
                        task.configEntrada["user"], app["Login"]["Edit2"], True, "50"
                    )
                    pyautogui.press("tab")
                    type_text_into_field(
                        task.configEntrada["pass"],
                        app["Login"]["Edit1"],
                        True,
                        "50",
                    )
                    pyautogui.press("enter")

                    # Seleciona a filial do emsys
                    selecao_filial = await find_element_center(
                        "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 15
                    )

                    if selecao_filial == None:
                        screenshot_path = take_screenshot()
                        selecao_filial = find_target_position(
                            screenshot_path, "Grupo", 0, -50, 15
                        )

                        if selecao_filial == None:
                            selecao_filial = (804, 640)

                        pyautogui.write(task.configEntrada["filial"])
                        pyautogui.press("enter")

                    else:
                        type_text_into_field(
                            task.configEntrada["filial"],
                            app["Seleção de Empresas"]["Edit"],
                            True,
                            "50",
                        )
                        pyautogui.press("enter")

                    button_logout = await find_element_center(
                        "assets/emsys/button_logout.png", (0, 0, 130, 150), 75
                    )

                    if button_logout:
                        console.print(
                            "Login realizado com sucesso.", style="bold green"
                        )
                        return RpaRetornoProcessoDTO(
                            sucesso=True,
                            retorno="Processo de login no EMSys executado com sucesso.",
                            status=RpaHistoricoStatusEnum.Sucesso,
                        )

            else:
                logger.info("login_emsys_win -> wait_element_ready_win [1]")
                console.print("Elemento de login não está pronto.", style="bold red")

    except Exception as ex:
        logger.error("Erro em login_emsys: " + str(ex))
        console.print(f"Erro em login_emsys: {str(ex)}", style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro em login_emsys: {str(ex)}",
            status=RpaHistoricoStatusEnum.Falha,
        )
