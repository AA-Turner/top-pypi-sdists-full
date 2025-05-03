import numpy
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    worker_sleep,
)
from rich.console import Console
import pyautogui
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PIL import ImageFilter, ImageEnhance
from pytesseract import image_to_string
from pywinauto import Application
import subprocess
import os
from worker_automate_hub.api.client import (
    get_config_by_name,
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys
import psutil
from time import sleep

pyautogui.PAUSE = 0.5
console = Console()
emsys = EMSys()


def get_text_from_window(window, relative_coords, value=None):
    try:
        screenshot = window.capture_as_image()
        imagem = screenshot.convert("L")
        imagem = imagem.filter(ImageFilter.SHARPEN)
        imagem = ImageEnhance.Contrast(imagem).enhance(2)
        cropped_screenshot = imagem.crop(relative_coords)
        texto = image_to_string(cropped_screenshot, lang="por")
        return (value.upper() in texto.upper()) if value != None else texto.lower()
    except Exception as error:
        console.print(f"Error: {error}")


async def open_contabil_processes():
    try:
        console.print("Abrindo EMSys Contabil...")
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil1.lnk")
        await worker_sleep(3)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil2.lnk")
        await worker_sleep(30)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil3.lnk")
        await worker_sleep(20)
        pyautogui.hotkey("win", "d")
        await worker_sleep(4)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil4.lnk")
        await worker_sleep(2)
    except Exception as error:
        console.print(f"Error: {error}")


async def integracao_contabil(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        await kill_all_emsys()
        await open_contabil_processes()
        config = await get_config_by_name("login_emsys_contabil")

        app = None
        max_attempts = 30
        console.print("Tentando encontrar janela de login...")
        for attempt in range(max_attempts):
            try:
                app = Application(backend="win32").connect(
                    title="Selecione o Usuário para autenticação"
                )
                console.print("Janela encontrada!")
                break
            except:
                console.print("Janela ainda nao encontrada...")
                await worker_sleep(1)
        if not app:
            console.print("Nao foi possivel encontrar a janela de login...")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro durante tentativa localizacao de janelas...",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        await emsys.verify_warning_and_error("Erro", "&Ok")
        await worker_sleep(4)
        pyautogui.click(x=1021, y=127)
        console.print("Logando...")
        await emsys.verify_warning_and_error("Erro", "&Ok")
        pyautogui.write(config.conConfiguracao.get("user"))
        pyautogui.press("enter")

        await worker_sleep(4)
        pyautogui.write(config.conConfiguracao.get("pass"))
        pyautogui.press("enter")
        await worker_sleep(10)

        main_window = None
        for attempt in range(max_attempts):
            main_window = Application().connect(title="EMSys [Contabil]")
            main_window = main_window.top_window()
            if main_window.exists():
                console.print("Janela encontrada!")
                break
            console.print("Janela ainda nao encontrada...")
            await worker_sleep(1)

        if not main_window:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro durante tentativa localizacao de janelas....",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Adicionando foco
        try:
            main_window.set_focus()
            console.print(f"Ativando janela: {main_window}")
        except Exception as error:
            console.print(f"Erro ao setar foco na janela: {main_window}")

        await worker_sleep(4)
        console.print("Iniciando interacao a janela de integracao contabil...")
        pyautogui.click(x=566, y=53)
        await worker_sleep(4)
        pyautogui.press("tab", presses=2, interval=1)
        await worker_sleep(4)
        pyautogui.press("enter")
        await worker_sleep(12)
        pyautogui.press("tab")
        pyautogui.click(x=654, y=342)
        await worker_sleep(5)
        console.print("Preenchendo campo periodo...")
        pyautogui.press("tab", presses=2)
        await worker_sleep(4)
        periodoInicial = task.configEntrada.get("periodoInicial")
        periodoInicial = periodoInicial.replace("/", "")
        pyautogui.write(periodoInicial)
        await worker_sleep(5)
        pyautogui.press("tab")
        await worker_sleep(4)
        periodoFinal = task.configEntrada.get("periodoFinal")
        periodoFinal = periodoFinal.replace("/", "")
        pyautogui.write(periodoFinal)
        await worker_sleep(3)
        console.print("Selecionando item do campo origem...")
        checkbox_origem = main_window.child_window(
            class_name="TRzComboBox", found_index=1
        )
        checkbox_origem.select(task.configEntrada.get("origem"))
        await worker_sleep(3)
        console.print("Clicando no botao pesquisar...")
        pyautogui.click(x=1250, y=380)
        await worker_sleep(60)
        console.print("Aguardando carregamento...")
        max_attempts = 240
        found = False
        console.print("Iniciando verificacoes...")

        for attempt in range(1, max_attempts + 1):
            console.print(
                f"Verificacao {attempt} ( maximo {max_attempts} ) - aguardando 1 minuto..."
            )
            field = get_text_from_window(main_window, (1033, 770, 1301, 785))
            poupop = get_text_from_window(main_window, (830, 500, 1100, 550))
            if "finalizado" in field:
                found = True
                break
            if "[Pesquisa] - Não é possível realizar a operação em mídias" in field:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro: '[Pesquisa] - Não é possível realizar a operação em mídias', por favor, reenfileirar processo",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            print("field:", field)
            print("poupop:", poupop)
            try:
                if "nenhum lote" in poupop or "menhum lote" in poupop:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"A integração não foi realizada: nenhum lote para integrar.",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            except:
                pass
            await worker_sleep(30)
        if not found:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro durante a pesquisa de lancamentos ( max_attempts excedido )",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        await worker_sleep(4)

        dados_consistentes = False
        dados_consistentes_is_checked = False
        max_attempts_dados_consistentes = 20
        console.print("Verificando ocorrencia de inconsistencias...")
        for attempt in range(1, max_attempts_dados_consistentes + 1):
            console.print(f"Verificacao {attempt}...")
            try:
                total_debito = main_window.Edit3.window_text()
                total_credito = main_window.Edit2.window_text()
                diferenca = main_window.Edit.window_text()
                if total_debito != total_credito:
                    if not dados_consistentes_is_checked:
                        pyautogui.click(x=702, y=758)  # lotes consistentes
                        await worker_sleep(3)
                        dados_consistentes_is_checked = True
                        total_debito = main_window.Edit3.window_text()
                        total_credito = main_window.Edit2.window_text()
                        diferenca = main_window.Edit.window_text()
                        if total_debito == total_credito:
                            if total_debito == "0,00":
                                await worker_sleep(2)
                                console.print("Clicando em integrar lançamentos...")
                                pyautogui.click(x=947, y=790)  # integrar lancamentos
                                await worker_sleep(2)
                                return RpaRetornoProcessoDTO(
                                    sucesso=False,
                                    retorno="Integração não realizada: nenhum lote para integrar após selecionar lotes consistentes",
                                    status=RpaHistoricoStatusEnum.Falha,
                                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                                )
                            else:
                                await worker_sleep(2)
                                console.print("Clicando em integrar lançamentos...")
                                pyautogui.click(x=947, y=790)  # integrar lancamentos
                        else:

                            return RpaRetornoProcessoDTO(
                                sucesso=False,
                                retorno="Integração não realizada, pois os valores de crédito e débito divergem mesmo após clicar em lotes consistentes.",
                                status=RpaHistoricoStatusEnum.Falha,
                                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                            )

                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                        )

                    await worker_sleep(50)

                else:
                    await worker_sleep(2)
                    console.print("Clicando em integrar lançamentos...")
                    pyautogui.click(x=947, y=790)  # integrar lancamentos

                if total_credito == total_debito and diferenca == "0,00":
                    dados_consistentes = True
                    break
            except:
                console.print(
                    "Nao foi possivel encontrar os campos diretamente, tentando via ocr..."
                )
                total_debito = get_text_from_window(
                    main_window, (854, 722, 956, 747)
                ).replace("\n", "")
                await worker_sleep(1)
                total_credito = get_text_from_window(
                    main_window, (1055, 722, 1162, 747)
                ).replace("\n", "")
                await worker_sleep(1)
                diferenca = get_text_from_window(
                    main_window, (1233, 722, 1336, 747)
                ).replace("\n", "")
                await worker_sleep(1)
                if total_debito != total_credito or diferenca != "0,00":
                    if not dados_consistentes_is_checked:
                        pyautogui.click(x=702, y=758)  # lotes consistentes
                        dados_consistentes_is_checked = True
                    await worker_sleep(2)
                    console.print("Clicando em integrar lançamentos...")
                    pyautogui.click(x=947, y=790)  # integrar lancamentos
                    await worker_sleep(60)
        if not dados_consistentes:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro: lotes inconsistentes (maximo de tentativas excedido em dados consistentes)",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )
        tela_processo_finalizado = None
        main_window_capture = main_window.capture_as_image()
        console.print("Aguardando a finalizacao do processo...")
        for attempt in range(1, max_attempts + 1):
            console.print("Aguardando 1 minuto...")
            await worker_sleep(60)
            new_window_capture = main_window.capture_as_image()
            array_image1 = numpy.array(main_window_capture)
            array_image2 = numpy.array(new_window_capture)
            if not numpy.array_equal(array_image1, array_image2):
                tela_processo_finalizado = new_window_capture
                break

        mensagem_mapeada = get_text_from_window(main_window, (830, 513, 998, 546))
        console.print(f"Mensagem de erro extraída da tela: {mensagem_mapeada}")
        if "conta indefinida" in mensagem_mapeada:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Integração não realizada, existe um erro de conta indefinida",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        if tela_processo_finalizado and dados_consistentes_is_checked:
            await worker_sleep(3)
            pyautogui.click(x=951, y=573)  # clicando em ok
            await worker_sleep(3)
            pyautogui.click(x=702, y=758)
            await worker_sleep(10)

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Integração realizada, porém, existem LOTES INCONSISTENTES",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )
        elif tela_processo_finalizado and not dados_consistentes_is_checked:
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso ao executar processo de integracao contabil",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        if not tela_processo_finalizado:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro de 'timeout' durante o processo integração contabil...",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as erro:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro durante o processo integração contabil, erro : {erro}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
