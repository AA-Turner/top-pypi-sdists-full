import asyncio
import getpass
from datetime import datetime
from pyautogui import ImageNotFoundException
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from rich.console import Console
import re
import time
import os
import numpy
from pywinauto.keyboard import send_keys
from pywinauto.findwindows import ElementNotFoundError
from worker_automate_hub.utils.util import login_emsys
import warnings
from PIL import ImageFilter, ImageEnhance
from pytesseract import image_to_string
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name, get_status_cte_emsys
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    delete_xml,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

pyautogui.PAUSE = 0.5
console = Console()
emsys = EMSys()

ASSETS_PATH_BASE = "assets"


async def localizar_e_clicar(caminho_imagem, tentativas=50, scroll_pixels=300):
    for tentativa in range(tentativas):
        try:
            pos = pyautogui.locateCenterOnScreen(caminho_imagem, confidence=0.9)
        except:
            print(f"Erro")
            pos = None
        if pos:
            pyautogui.click(pos)
            print(f"Imagem encontrada e clicada na tentativa {tentativa + 1}")
            return True
        else:
            pyautogui.scroll(-scroll_pixels)
            await worker_sleep(0.5)
    print("Não encontrou a imagem após as tentativas.")
    return False


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
        await worker_sleep(60)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil3.lnk")
        await worker_sleep(60)
        pyautogui.hotkey("win", "d")
        await worker_sleep(20)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil4.lnk")
        await worker_sleep(20)
    except Exception as error:
        console.print(f"Error: {error}")


async def metodo_selecao_origem_especial():

    try:
        app = Application(backend="win32").connect(
            class_name="TFrmIntegrador", found_index=0
        )
        main_window = app["TFrmIntegrador"]

        # clique no combobox
        combobox = main_window.child_window(
            class_name="TcxCheckComboBox", found_index=1
        ).wrapper_object()
        combobox.click_input()

        await worker_sleep(2)
    except:
        # Clica no campo para selecionar a origem
        pyautogui.click(x=653, y=379)


async def integracao_contabil_generica(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    try:
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)
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
                await worker_sleep(2)
        if not app:
            console.print("Nao foi possivel encontrar a janela de login...")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro durante tentativa localizacao de janelas...",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        await emsys.verify_warning_and_error("Erro", "&Ok")
        await worker_sleep(10)
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
        # pyautogui.press("tab")
        await worker_sleep(3)

        # console.print("Selecionando item do campo origem...")
        uuid_processo = task.uuidProcesso
        caminho_imagem = f"assets\\integracao_contabil\\{uuid_processo}.png"

        await metodo_selecao_origem_especial()
        await localizar_e_clicar(caminho_imagem)  # main_window.set_focus()
        await worker_sleep(5)

        console.print("Preenchendo campo periodo...")
        app = Application(backend="win32").connect(
            class_name="TFrmIntegrador", found_index=0
        )
        main_window = app["TFrmIntegrador"]
        await worker_sleep(4)
        periodo_inicial = task.configEntrada.get("periodoInicial")
        periodo_inicial = periodo_inicial.replace("/", "")
        # clique no combobox
        combobox = main_window.child_window(
            class_name="TRzEditDate", found_index=1
        ).wrapper_object()

        combobox.click_input()  # Clica no campo para focar
        combobox.type_keys("{BACKSPACE 5}")  # Apaga os 5 últimos caracteres

        await worker_sleep(2)

        combobox.type_keys(periodo_inicial)

        # Preencher Período final
        periodo_final = task.configEntrada.get("periodoFinal")
        periodo_final = periodo_final.replace("/", "")
        pyautogui.write(periodo_final)

        # clique no combobox
        combobox = main_window.child_window(
            class_name="TRzEditDate", found_index=0
        ).wrapper_object()

        combobox.click_input()  # Clica no campo para focar
        combobox.type_keys("{BACKSPACE 5}")  # Apaga os 5 últimos caracteres

        await worker_sleep(2)

        combobox.type_keys(periodo_final)  # Digita a nova data

        await worker_sleep(2)

        console.print("Clicando no botao pesquisar...")
        combobox = main_window.child_window(
            class_name="TBitBtn", found_index=3
        ).wrapper_object()
        combobox.click_input()

        await worker_sleep(10)

        console.print("Verificar se existem lotes")
        try:
            # Verifica mensagem sem lote pra integrar
            imagem_alvo = "assets\\integracao_contabil\\sem_lote.png"

            localizacao = pyautogui.locateOnScreen(imagem_alvo, confidence=0.9)

            if localizacao:
                console.print("Imagem sem lote para integrar encontrada!")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Sem lotes para integrar.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            else:
                console.print("Imagem não encontrada.")

        except ImageNotFoundException:
            console.print(
                "Imagem não encontrada (exceção capturada). Tentando clicar no OK."
            )
            try:
                app = Application(backend="win32").connect(
                    class_name="TMsgBox", found_index=0
                )
                main_window = app["TMsgBox"]
                main_window.child_window(
                    class_name="TBitBtn", found_index=0
                ).click_input()
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Sem lotes para integrar.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            except Exception as e:
                console.print(f"Não foi possível clicar no botão OK: {e}")

        await worker_sleep(5)

        try:
            imagem_finalizada = "assets\\integracao_contabil\\pesquisa_finalizada.png"

            if not os.path.exists(imagem_finalizada):
                raise FileNotFoundError(
                    f"Imagem não encontrada no caminho: {imagem_finalizada}"
                )

            print("Aguardando a imagem aparecer...")

            localizacao = None
            max_tentativas = 300

            for tentativa in range(1, max_tentativas + 1):
                print(f"Tentativa {tentativa} de {max_tentativas}...")
                try:
                    localizacao = pyautogui.locateOnScreen(
                        imagem_finalizada, confidence=0.85
                    )
                    if localizacao:
                        console.print("Imagem encontrada!")
                        break
                    else:
                        print("Imagem não encontrada ainda.")
                except Exception as e:
                    print(f"Erro ao verificar a imagem: {e}")

                await worker_sleep(20)

            if not localizacao:
                console.print("Imagem não foi encontrada após 300 tentativas")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Imagem de pesquisa finalizada não encontrada, favor verificar.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
        except Exception as e:
            console.print(f"Erro ao procurar imagem: {e}")

        # Conecta ao aplicativo
        app = Application(backend="win32").connect(title_re=".*Integrador Contábil.*")

        # Janela principal
        dlg = app.window(title_re=".*Integrador Contábil.*")

        # Captura todos os campos do tipo TRzEditNumber
        numeros = [
            e
            for e in dlg.descendants()
            if e.friendly_class_name() == "Edit" and e.class_name() == "TRzEditNumber"
        ]

        # Verifica os textos capturados
        for i, campo in enumerate(numeros):
            print(f"[{i}] -> {campo.window_text()}")

        # Atribui valores individuais
        diferenca = numeros[0].window_text()
        total_debito = numeros[1].window_text()
        total_credito = numeros[2].window_text()
        lotesMarcados = False
        print("Diferença:", diferenca)
        print("Total Débito:", total_debito)
        print("Total Crédito:", total_credito)

        await worker_sleep(10)
        clicou = False

        if total_credito != total_debito or diferenca != "0,00":
            try:
                lotesMarcados = True
                # Tenta encontrar exatamente o checkbox com o texto "Lotes Consistentes"
                checkbox = dlg.child_window(
                    title="Lotes Consistentes", class_name="TCheckBox"
                )

                if (
                    checkbox.exists()
                    and checkbox.is_enabled()
                    and checkbox.is_visible()
                ):
                    checkbox.click_input()
                    print("Checkbox 'Lotes Consistentes' clicado com sucesso.")

                await worker_sleep(10)
                # Captura todos os campos do tipo TRzEditNumber apos atualizacao de tela..
                numeros = [
                    e
                    for e in dlg.descendants()
                    if e.friendly_class_name() == "Edit"
                    and e.class_name() == "TRzEditNumber"
                ]

                # Verifica os textos capturados
                for i, campo in enumerate(numeros):
                    print(f"[{i}] -> {campo.window_text()}")

                # Atribui valores individuais
                diferenca = numeros[0].window_text()
                total_debito = numeros[1].window_text()
                total_credito = numeros[2].window_text()

                print("Diferença:", diferenca)
                print("Total Débito:", total_debito)
                print("Total Crédito:", total_credito)

                if diferenca > "0,00":
                    clicou = True
                    main_window_capture = main_window.capture_as_image()
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Integração não realizada, pois os valores de crédito e débito divergem mesmo após clicar em lotes consistentes.",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )
            except Exception as e:
                print("Erro inesperado:", e)
        if not clicou:
            print("Clicar no botão integrar")
        # Clicar em integrar
        try:
            # Conecta ao app pela classe principal
            app = Application(backend="win32").connect(
                class_name="TFrmIntegrador", found_index=0
            )
            main_window = app["TFrmIntegrador"]

            # Buscar botão pelo texto (mesmo com acento)
            botao_integrar = main_window.child_window(
                title="Integrar Lançamentos", class_name="TBitBtn"
            ).wrapper_object()

            botao_integrar.click_input()

            await worker_sleep(5)

            assets_int_cont = "assets\\integracao_contabil\\"
            err_dict = {
                assets_int_cont
                + "erro_duplicidade.png": "Integração não realizada. Erro de Duplicidade localizado enquanto finalizava a integração, contate o suporte do Emsys.",
                assets_int_cont
                + "conta_indefinida_error.png": "Integração não realizada. Conta contábil indefinida no sistema.",
                assets_int_cont
                + "lote_sem_complemento_error.png": "Integração não realizada. Lote encontrado sem complemento obrigatório.",
                assets_int_cont
                + "diferenca_cred_deb.png": "Integração não realizada. Existem diferença em lotes consistentes, por favor verificar.",
                assets_int_cont
                + "integracao_sucesso.png": "Integração Finalizada com Sucesso.",
            }
            # Aguardar finalizar
            while True:
                try:
                    app = Application(backend="win32").connect(
                        class_name="TMsgBox", found_index=0
                    )
                    msg_box = app["TMsgBox"]

                    # Antes de qualquer coisa, verifica por imagem de erro
                    for img_path, mensagem in err_dict.items():
                        try:
                            err = pyautogui.locateOnScreen(img_path, confidence=0.90)
                        except:
                            continue

                        if err:
                            if "integracao_sucesso.png" in img_path:
                                console.print(f"[green]{mensagem}[/green]")
                                msg_box.child_window(
                                    class_name="TBitBtn", found_index=0
                                ).click_input()
                                break

                            console.print(f"[red]Erro encontrado:[/red] {mensagem}")

                            return RpaRetornoProcessoDTO(
                                sucesso=False,
                                retorno=mensagem,
                                status=RpaHistoricoStatusEnum.Falha,
                                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                            )

                    await worker_sleep(1)

                    try:
                        app = Application(backend="win32").connect(
                            class_name="TMsgBox", found_index=0
                        )
                        main_window = app["TMsgBox"]
                        main_window.child_window(
                            class_name="TBitBtn", found_index=0
                        ).click_input()
                        break
                    except ElementNotFoundError:
                        console.print(
                            "[yellow]Janela TMsgBox ainda não visível.[/yellow]"
                        )
                        break

                except ElementNotFoundError:
                    console.print("[yellow]Janela TMsgBox ainda não visível.[/yellow]")
                except Exception as e:
                    print(f"Erro inesperado ao verificar janela de confirmação: {e}")
                    break

                await worker_sleep(1)

                try:
                    app = Application(backend="win32").connect(
                        class_name="TMsgBox", found_index=0
                    )
                    main_window = app["TMsgBox"]
                    main_window.child_window(
                        class_name="TBitBtn", found_index=0
                    ).click_input()
                    time.sleep(5)
                    break
                except ElementNotFoundError:
                    console.print("[yellow]Janela TMsgBox ainda não visível.[/yellow]")

            if lotesMarcados:
                if (
                    checkbox.exists()
                    and checkbox.is_enabled()
                    and checkbox.is_visible()
                ):
                    checkbox.click_input()
                    print("Checkbox 'Lotes Consistentes' desmarcado com sucesso.")
                time.sleep(5)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Integração realizada, porém, existem LOTES INCONSISTENTES.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso ao executar processo de integracao contabil",
                    status=RpaHistoricoStatusEnum.Sucesso,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        except Exception as erro:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro durante o processo integração contabil, erro : {erro}",
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
