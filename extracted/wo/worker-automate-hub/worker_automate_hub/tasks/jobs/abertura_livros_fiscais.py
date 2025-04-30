import time
import pyautogui

from worker_automate_hub.utils.logger import logger
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

from worker_automate_hub.api.client import get_config_by_name
from pywinauto import Application
from rich.console import Console
from worker_automate_hub.utils.util import (
    is_window_open_by_class,
    kill_contabil_processes,
    kill_process,
    login_emsys_fiscal,
    type_text_into_field,
    worker_sleep,
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys
import pyperclip
import warnings
import asyncio
from worker_automate_hub.decorators.repeat import repeat
from pytesseract import image_to_string
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

console = Console()

emsys = EMSys()


@repeat(times=5, delay=2)
async def wait_aguarde_window_closed(timeout=300):
    console.print("Esperando janela 'Aguarde...' fechar")
    start_time = time.time()

    while time.time() - start_time < timeout:
        await worker_sleep(4)
        all_windows = Desktop(backend="uia").windows()
        aguarde_aberta = any("aguarde" in w.window_text().lower() for w in all_windows)

        if aguarde_aberta:
            console.print("Janela 'Aguarde...' ainda aberta", style="bold yellow")
            await worker_sleep(10)
        else:
            console.print("Janela 'Aguarde...' fechou", style="bold green")
            await worker_sleep(2)
            return

    console.log("Timeout esperando a janela 'Aguarde...' fechar.")


def click_desconfirmar():
    cords = (675, 748)
    pyautogui.click(x=cords[0], y=cords[1])


def ctrl_c():
    pyautogui.press("tab", presses=12)  # verificar
    pyautogui.hotkey("ctrl", "c")
    return pyperclip.paste()


async def abertura_livros_fiscais(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys_fiscal")

        await kill_process("EMSys")
        await kill_process("EMSysFiscal")
        await kill_contabil_processes()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSysFiscal.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        await worker_sleep(4)

        try:
            app = Application(backend="win32").connect(
                class_name="TFrmLoginModulo", timeout=50
            )
        except:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir o EMSys Fiscal, tela de login não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        return_login = await login_emsys_fiscal(config.conConfiguracao, app, task)
        if return_login.sucesso:
            await worker_sleep(2)
            type_text_into_field(
                "Livros Fiscais", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("down")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                "\nPesquisa: 'Livros Fiscais' realizada com sucesso.",
                style="bold green",
            )
            await worker_sleep(10)
            livros_fiscais_window = app.top_window()
            # Preenchendo campo competencia
            console.print("Preenchendo campo competencia...")
            pyautogui.press("tab")
            competencia = task.configEntrada.get("periodo")
            pyautogui.write(competencia)
            await worker_sleep(3)

            # Resetando tabs
            console.print("Levando cursor para campo competencia")
            pyautogui.click(729, 321)
            await worker_sleep(2)

            # Marcando caixa Entrada
            console.print("Marcando caixa entrada")
            pyautogui.press("tab")
            pyautogui.press("space")
            await worker_sleep(2)

            # Marcando caixa Saida
            console.print("Marcando caixa saida")
            pyautogui.press("tab")
            pyautogui.press("space")
            await worker_sleep(2)

            # Clicando em incluir livro
            try:
                console.print("Clicando em incluir livro")
                cords = (676, 716)
                pyautogui.click(x=cords[0], y=cords[1])
                await worker_sleep(5)
            except:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao clicar em botão de incluir livro.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            # Clicando em sim na janela de gerar registros após incluir
            console.print("Clicando em sim na janela de gerar registros após incluir")
            cords = (942, 603)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Clicando nao na tela de somar icms outros
            console.print("Clicando em nao na janela de calcular icms Outros.")
            cords = (1000, 570)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Clicando sim em janela de confirmar observacao
            console.print("Clicando sim em janela de confirmar observacao")
            cords = (920, 560)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Esperando janela aguarde
            console.print("Aguardando tela de aguarde ser finalizada")
            await wait_aguarde_window_closed()
            await worker_sleep(15)

            console.print("Fechando possivel janela de aviso...")
            await emsys.verify_warning_and_error("Aviso", "&Ok")
            await worker_sleep(5)

            # Esperando janela aguarde registro de entrada
            await wait_aguarde_window_closed()

            # Fechando possivel tela de aviso após sumir o aguarde
            console.print("Fechando possivel janela de aviso...")
            await emsys.verify_warning_and_error("Aviso", "&Ok")
            await worker_sleep(5)

            # Clicando sim em janela gerar Num Serie
            console.print("Clicando sim em janela gerar Numero de Serie")
            cords = (920, 560)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Clicando sim em janela somar os valores de IPI, Frete..
            console.print("Clicando sim em janela somar os valores de IPI Frete")
            cords = (920, 560)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Esperando janela aguarde
            console.print("Aguardando tela de aguarde ser finalizada")
            await wait_aguarde_window_closed()
            await worker_sleep(30)

            app.top_window().set_focus()
            await worker_sleep(5)

            # Clicando OK em janela de livro incluido
            console.print("Clicando em OK em janela de livro incluido")
            await emsys.verify_warning_and_error("Informação", "OK")
            await worker_sleep(5)

            console.print("Selecionando primeira linha da tabela")
            # Selecionando primeira linha da tabela
            pyautogui.click(604, 485)
            # Iterando apenas as 2 primeiras linhas da tabela para procurar entrada/saida
            for _ in range(2):
                conteudo = ctrl_c().lower()
                if (
                    "entrada" in conteudo
                    and "confirmado" in conteudo
                    and competencia in conteudo
                ):
                    console.print(f"Clicando em desconfirmar entrada na tabela...")
                    click_desconfirmar()
                    await worker_sleep(2)
                if (
                    "saida" in conteudo
                    and "confirmado" in conteudo
                    and competencia in conteudo
                ):
                    console.print(f"Clicando em desconfirmar saida na tabela...")
                    click_desconfirmar()
                    await worker_sleep(2)
                pyautogui.press("down")
            await worker_sleep(5)

            # Fechando janela de livro fiscal
            console.print("Fechando janela de livro fiscal")
            livros_fiscais_window.close()
            await worker_sleep(5)

            # Abrindo janela de apuracao de ICMS
            console.print("Abrindo janela de apuracao de ICMS")
            type_text_into_field(
                "Livro de Apuração ICMS", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )

            await worker_sleep(5)

            pyautogui.press("enter", presses=2)

            await worker_sleep(5)
            titulo_atual = app.top_window().window_text().lower()
            if "apuração icms" not in titulo_atual:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro, ocorreu um problema ao tentar interagir com a janela de apuração.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            pyautogui.click(x=601, y=406)
            primeira_entrada = ctrl_c().lower()
            if "encerrado" in primeira_entrada:
                # Clicando em estornar livro
                console.print("Clicando em estornar livro")
                cords = (662, 739)
                pyautogui.click(x=cords[0], y=cords[1])
                await worker_sleep(4)

            # Clicando no campo competencia antes de preencher
            cords = (670, 329)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(4)

            # Preenchendo campo competencia
            console.print("Preenchendo campo competencia")
            pyautogui.write(competencia)

            # Clicando em incluir apuracao
            console.print("Clicando em incluir apuracao")
            cords = (659, 688)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(4)

            console.print("Operacao finalizada com sucesso")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Abertura de livro fiscal concluida com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(
                "\nError Messsage: {return_login.retorno}", style="bold green"
            )
            return return_login

    except Exception as erro:
        console.print(f"Erro ao executar abertura de livros fiscais, erro : {erro}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na Abertura de Livro Fiscal : {erro}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
