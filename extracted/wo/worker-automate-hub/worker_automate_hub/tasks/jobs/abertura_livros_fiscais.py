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


async def wait_until_window_close(app):
    await worker_sleep(3)
    max_attempts = 500
    for _ in range(max_attempts):
        if "Aguarde" not in app.top_window().window_text():
            await worker_sleep(3)
            if "Aguarde" not in app.top_window().window_text():
                break
        await worker_sleep(3)


@repeat(times=10, delay=5)
async def wait_aguarde_window_closed():
    sucesso = False
    while not sucesso:
        desktop = Desktop(backend="uia")
        # Tenta localizar a janela com o título que contém "Aguarde"
        window = desktop.window(title_re="Aguarde...")
        # Se a janela existe, continua monitorando
        if window.exists():
            console.print(f"Janela 'Aguarde...' ainda aberta", style="bold yellow")
            logger.info(f"Janela 'Aguarde...' ainda aberta")
            await worker_sleep(10)
            continue
        else:
            try:
                desktop_second = Desktop(backend="uia")
                window_aguarde = desktop_second.window(title_re="Aguarde...")
                if not window_aguarde.exists():
                    sucesso = True
                    break
                else:
                    console.print(
                        f"Janela 'Aguarde...' ainda aberta. Seguindo para próxima tentativa",
                        style="bold yellow",
                    )
                    continue
            except:
                console.print(
                    f"Janela 'Aguarde...' não existe mais.", style="bold green"
                )
                await worker_sleep(10)
                break


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
            console.print("Clicando em incluir livro")
            cords = (676, 716)
            pyautogui.click(x=cords[0], y=cords[1])
            await worker_sleep(5)

            # Clicando em sim na janela de confirmacao
            console.print("Clicando sim em janela de confirmacao")
            await emsys.verify_warning_and_error("Gerar Registros", "Sim")
            await worker_sleep(5)

            # Clicando sim em segunda janela de confirmacao
            console.print("Confirmando segunda janela de confirmacao")
            await emsys.verify_warning_and_error("Gerar Registros", "&Sim")
            await worker_sleep(5)

            # Clicando sim em janela de confirmar observacao
            console.print("Clicando sim em janela de confirmar observacao")
            await emsys.verify_warning_and_error("Gerar Registros", "&Sim")
            await worker_sleep(5)

            # Clicando sim em janela de confirmar observacao
            console.print("Clicando sim em janela de confirmar observacao")
            await emsys.verify_warning_and_error("Gerar Registros", "&Sim")
            await worker_sleep(5)

            # Esperando janela aguarde
            console.print("Aguardando tela de aguarde ser finalizada")
            await wait_until_window_close(app)
            await worker_sleep(15)

            console.print("Fechando possivel janela de aviso...")
            await emsys.verify_warning_and_error("Aviso", "&Ok")
            await worker_sleep(5)

            # Esperando janela aguarde registro de entrada
            console.print("Aguardando tela de gerando registro de entrada")
            await wait_aguarde_window_closed()
            await worker_sleep(2)

            # Esperando janela aguarde registro de saida
            console.print("Aguardando tela de gerando registro de saida")
            await wait_aguarde_window_closed()
            await worker_sleep(8)

            # Fechando possivel tela de aviso após sumir o aguarde
            console.print("Fechando possivel janela de aviso...")
            await emsys.verify_warning_and_error("Aviso", "&Ok")
            await worker_sleep(5)

            # Clicando sim em janela gerar Num Serie
            console.print("Clicando sim em janela gerar Numero de Serie")
            await emsys.verify_warning_and_error("Gerar Registros", "&Sim")
            await worker_sleep(5)

            # Clicando sim em janela somar valores
            console.print("Clicando sim em janela somar valores")
            await emsys.verify_warning_and_error("Gerar Registros", "&Sim")

            # Esperando janela aguarde
            console.print("Aguardando tela de aguarde ser finalizada")
            await wait_until_window_close(app)
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
