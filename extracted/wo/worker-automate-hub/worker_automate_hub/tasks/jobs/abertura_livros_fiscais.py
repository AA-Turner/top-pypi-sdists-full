import time
import pyautogui
from datetime import datetime
import sys
import os
import sys
import os
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.keyboard import send_keys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)
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
    kill_all_emsys,
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

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

console = Console()

emsys = EMSys()

# ASSETS_PATH = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros"
ASSETS_PATH = r"assets\abertura_livros"


@repeat(times=10, delay=5)
async def wait_aguarde_window_closed(app, timeout=60):
    console.print("Verificando existencia de aguarde...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        janela_topo = app.top_window()
        titulo = janela_topo.window_text()
        console.print(f"Titulo da janela top:  ${titulo}")
        await emsys.verify_warning_and_error("Aviso", "&Ok")
        await worker_sleep(2)

        if "Gerar Registros" in titulo or "Movimento de Livro Fiscal" in titulo:
            console.log("Fim de aguardando...")
            return
        else:
            console.log("Aguardando...")

    console.log("Timeout esperando a janela Aguarde...")


async def abertura_livros_fiscais(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys_fiscal")

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSysFiscal.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        await worker_sleep(8)

        try:
            app = Application(backend="win32").connect(
                class_name="TFrmLoginModulo", timeout=120
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
            try:
                ##### Janela Confirm #####
                app = Application().connect(class_name="TMessageForm", timeout=5)
                main_window = app["TMessageForm"]
                main_window.set_focus()

                # Clicar em Não
                console.print("Navegando nos elementos...\n")
                main_window.child_window(class_name="TButton", found_index=0).click()
                await worker_sleep(2)
            except:
                pass

            ##### Janela Principal ####
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            main_window = app["TFrmPrincipalFiscal"]
            main_window.set_focus()

            # Localiza o campo TEdit
            input_livros = main_window.child_window(class_name="TEdit", found_index=0)
            input_livros.click_input()
            await worker_sleep(1)
            input_livros.set_edit_text("")  # Limpa o campo
            input_livros.type_keys("Livros Fiscais", with_spaces=True)
            await worker_sleep(1)
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("down")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                "\nPesquisa: 'Livros Fiscais' realizada com sucesso.",
                style="bold green",
            )

            await worker_sleep(2)

            console.print("Aguardando janela 'Movimento de Livro Fiscal' aparecer...")

            # Tempo limite de espera (em segundos)
            timeout = 3600
            inicio = time.time()

            # Espera até a janela aparecer
            while True:
                try:
                    app = Application().connect(
                        class_name="TFrmMovtoLivroFiscal", timeout=5
                    )
                    break  # Se conectar, sai do loop
                except ElementNotFoundError:
                    if time() - inicio > timeout:
                        console.print(
                            "[bold red]Erro: Janela 'TFrmMovtoLivroFiscal' não apareceu dentro do tempo limite.[/bold red]"
                        )
                        raise
                    await worker_sleep(2)

            console.print("Janela encontrada. Inserindo competência...")

            # Acessa a janela e insere a competência
            main_window = app["TFrmMovtoLivroFiscal"]
            main_window.set_focus()

            data_input = main_window.child_window(
                class_name="TDBIEditDate", found_index=0
            )
            data_input.click_input()
            await worker_sleep(1)
            data_input.set_edit_text("")

            competencia = task.configEntrada.get("periodo")  # Ex: "07/2025"
            data_input.type_keys(competencia, with_spaces=True)

            console.print(f"Competência '{competencia}' inserida com sucesso.")

            await worker_sleep(2)

            # Marcando caixa Entrada
            console.print("Marcando caixa entrada")
            entrada = main_window.child_window(
                class_name="TcxCheckBox", found_index=9
            ).click_input()

            await worker_sleep(2)

            # Marcando caixa Saida
            console.print("Marcando caixa saida")
            saida_checkbox = main_window.child_window(
                class_name="TcxCheckBox", found_index=8
            )

            # Tenta clicar inicialmente
            saida_checkbox.click_input()

            console.print("Aguardar marcar caixa de saida")
            imagem = rf"{ASSETS_PATH}\saida_marcada.png"

            tempo_limite = 600  # 10 minutos
            intervalo = 2  # segundos entre verificações

            inicio = time.time()

            while True:
                try:
                    localizacao = pyautogui.locateOnScreen(imagem, confidence=0.9)
                except Exception as e:
                    print(f"Erro ao localizar imagem: {e}")
                    localizacao = None

                if localizacao:
                    print("Imagem encontrada.")
                    break

                if time.time() - inicio > tempo_limite:
                    print("Tempo esgotado. A imagem não apareceu.")
                    break

                print(
                    "Imagem não apareceu na tela. Tentando clicar novamente na caixa de saída..."
                )
                try:
                    saida_checkbox.click_input()
                except Exception as e:
                    print(f"Erro ao clicar na checkbox: {e}")

                time.sleep(intervalo)

            await worker_sleep(2)

            # Clicando em incluir livro
            try:
                console.print("Clicando em incluir livro")
                cords = (698, 728)
                pyautogui.click(x=cords[0], y=cords[1])
                await worker_sleep(5)
            except:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao clicar em botão de incluir livro.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            ##### Janela Pergunta das Geração dos Livros Fiscais #####
            await worker_sleep(5)
            app = Application().connect(
                class_name="TPerguntasLivrosFiscaisForm", timeout=20
            )
            main_window = app["TPerguntasLivrosFiscaisForm"]
            main_window.set_focus()

            try:
                console.print("Clicando sim em janela somar os valores de IPI Frete")
                main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=0
                ).click_input()

                await worker_sleep(1)
                send_keys("{ENTER}")
                await worker_sleep(2)
            except:
                pass
            console.print("Clicando sim em janela gerar Numero de Serie do SAT")

            try:
                main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=4
                ).click_input()

                await worker_sleep(1)
                send_keys("{ENTER}")
                await worker_sleep(2)
            except:
                pass

            try:
                console.print(
                    "Clicando sim em janela gerar Numero de Serie a partir da chave do documento"
                )
                main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=1
                ).click_input()

                await worker_sleep(1)
                send_keys("{ENTER}")
                await worker_sleep(2)
            except:
                pass

            try:
                console.print(
                    "Clicando sim em janela gerar livro com observação da nota fiscal"
                )
                main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=3
                ).click_input()

                await worker_sleep(1)
                send_keys("{ENTER}")
                await worker_sleep(2)
            except:
                pass

            try:
                console.print("Clicando sim em janela somar valores de ICMS...")
                main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=2
                ).click_input()

                await worker_sleep(1)
                send_keys("{ENTER}")
            except:
                pass
            await worker_sleep(3)

            # Clicar em confirmar
            main_window.child_window(class_name="TButton", found_index=1).click_input()

            await worker_sleep(5)
            ##### Janela Gerar Registro ####
            console.print("Confirmar Registro")
            app = Application().connect(title="Gerar Registros", timeout=60)
            main_window = app["Gerar Registros"]
            main_window.set_focus()

            # Clicar em Sim
            main_window.child_window(class_name="Button", found_index=0).click_input()

            await worker_sleep(5)

            console.print("Aguardar o término de carregar")
            imagem = rf"{ASSETS_PATH}\livros_incluidos.png"

            tempo_limite = 6600  # 1h
            intervalo = 2  # segundos entre as verificações

            inicio = time.time()

            while True:
                janela_aberta = False

                # 1. Verifica se a imagem apareceu e clica em 'Sim' na janela "Informação"
                try:
                    if pyautogui.locateOnScreen(imagem, confidence=0.9):
                        print("Imagem 'livros_incluidos' apareceu na tela.")
                        try:
                            app_info = Application().connect(
                                title="Informação", timeout=5
                            )
                            info_window = app_info["Informação"]
                            info_window.set_focus()
                            console.print("Clicando em 'Sim' na janela Informação...")
                            info_window.child_window(
                                class_name="Button", found_index=0
                            ).click_input()
                        except:
                            pass
                except:
                    pass

                # Verifica se a janela TMsgBox de aviso está aberta
                try:
                    app_msgbox = Application().connect(class_name="TMsgBox", timeout=10)
                    box = app_msgbox["TMsgBox"]
                    print("Janela 'TMsgBox' encontrada.")
                    box.set_focus()
                    box.child_window(class_name="TBitBtn", found_index=0).click_input()
                    print("Clicou no botão 'TBitBtn'.")
                except:
                    pass

                # 2. Verifica e trata janela de confirmação TMessageForm
                try:
                    img_dialog = rf"{ASSETS_PATH}\notas_rejeitadas.png"
                    if os.path.exists(img_dialog):
                        caixa = pyautogui.locateOnScreen(
                            img_dialog, confidence=0.9, grayscale=True
                        )
                        if caixa:
                            print("Janela 'notas rejeitadas' detectada por imagem.")
                            region = (caixa.left, caixa.top, caixa.width, caixa.height)

                            app_msg = Application().connect(
                                class_name="TMessageForm", timeout=2
                            )
                            form = app_msg["TMessageForm"]
                            console.print(
                                "Janela de confirmação 'TMessageForm' encontrada."
                            )
                            form.set_focus()
                            form.child_window(
                                class_name="TButton", found_index=1
                            ).click_input()
                            print("Clicou no botão de sim.")

                            await worker_sleep(5)

                            img_dialog = (
                                rf"{ASSETS_PATH}\gerar_rel_notas_rejeitadas.png"
                            )
                            if os.path.exists(img_dialog):
                                caixa = pyautogui.locateOnScreen(
                                    img_dialog, confidence=0.9, grayscale=True
                                )
                                if caixa:
                                    print(
                                        "Janela 'notas relatorios rejeitadas' detectada por imagem."
                                    )
                                    region = (
                                        caixa.left,
                                        caixa.top,
                                        caixa.width,
                                        caixa.height,
                                    )

                                    app_msg = Application().connect(
                                        class_name="TMessageForm", timeout=2
                                    )
                                    form = app_msg["TMessageForm"]
                                    console.print(
                                        "Janela de confirmação 'TMessageForm' encontrada."
                                    )
                                    form.set_focus()
                                    form.child_window(
                                        class_name="TButton", found_index=0
                                    ).click_input()
                                    print("Clicou no botão de não.")
                except:
                    pass

                # 3. Verifica se a janela do relatório está aberta
                try:
                    app_report = Application().connect(
                        class_name="TFrmPreviewRelatorio", timeout=2
                    )
                    janela = app_report["TFrmPreviewRelatorio"]
                    print("Janela 'TFrmPreviewRelatorio' encontrada.")
                    janela_aberta = True
                except:
                    pass

                # Se encontrou a janela de relatório, sai
                if janela_aberta:
                    print("Relatório carregado. Saindo do loop.")
                    break

                # Verifica tempo limite
                if time.time() - inicio > tempo_limite:
                    print("Tempo esgotado. Relatório não carregado.")
                    break

                print(
                    "Aguardando janela de relatório... (verificando novas confirmações se houver)"
                )
                time.sleep(intervalo)

            await worker_sleep(8)

            try:
                app_msg = Application().connect(class_name="TMessageForm", timeout=5)
                form = app_msg["TMessageForm"]
                console.print("Janela de confirmação 'TMessageForm' encontrada.")
                form.set_focus()
                form.child_window(class_name="TButton", found_index=0).click_input()
                print("Clicou no botão de confirmação.")
            except:
                pass

            await worker_sleep(5)

            ##### Janela Pré-visualizando Relatório #####
            console.print("Fechar Janela Pré-visualizando Relatório ")
            app = Application().connect(class_name="TFrmPreviewRelatorio", timeout=60)
            main_window = app["TFrmPreviewRelatorio"]
            main_window.set_focus()

            # Verificando se a foi confirmado os livres
            console.print("Verificando se os livros foram confirmados")

            imagem = rf"{ASSETS_PATH}\confirmado_livros.png"
            if os.path.exists(imagem):
                caixa = pyautogui.locateOnScreen(imagem, confidence=0.9, grayscale=True)
            else:
                console.print("Imagem confirmada não encontrada")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro na Abertura de Livro Fiscal: Imagem confirmada não encontrada",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            await worker_sleep(5)
            # Clicar em fechar
            main_window.close()

            console.print("Livros confirmados")

            await worker_sleep(5)

            # Conecta na janela principal
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            main_window = app["TFrmPrincipalFiscal"]

            # Captura todos os controles do tipo Edit (inclui TEdit do Delphi)
            edits = main_window.descendants(class_name="TEdit")

            print(f"Foram encontrados {len(edits)} campos TEdit.")

            campo = edits[0]  # ou outro índice correto
            campo.click_input()
            await worker_sleep(1)

            # Tenta limpar o campo e verifica se realmente foi limpo
            max_tentativas = 3
            for tentativa in range(max_tentativas):
                campo.set_edit_text("")
                await worker_sleep(0.5)

                texto_atual = campo.window_text().strip()
                if texto_atual == "":
                    break  # Campo foi limpo com sucesso
                print(
                    f"Tentativa {tentativa+1}: campo ainda contém texto: '{texto_atual}'"
                )

            # Continua se o campo estiver limpo
            campo.type_keys("Livro de Apuração ICMS", with_spaces=True)
            await worker_sleep(1)

            send_keys("{ENTER}")
            await worker_sleep(2)
            send_keys("{ENTER}")

            await worker_sleep(5)

            ##### Janela Movimentação de Apuração ICMS #####
            app = Application().connect(class_name="TFrmMovtoApuraIcmsNew", timeout=60)
            main_window = app["TFrmMovtoApuraIcmsNew"]
            main_window.set_focus()

            console.print("Clicando no último livro, primeira linha")
            pyautogui.click(599, 410)

            await worker_sleep(1)

            console.print("Clicando em Estornar Livro")
            pyautogui.click(667, 742)

            await worker_sleep(3)

            main_window.close()

            await worker_sleep(3)

            # Conecta na janela principal
            console.print("Janela Livro de Apuração ICMS 2ª Etapa")
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            main_window = app["TFrmPrincipalFiscal"]

            # Captura todos os controles do tipo Edit (inclui TEdit do Delphi)
            edits = main_window.descendants(class_name="TEdit")

            print(f"Foram encontrados {len(edits)} campos TEdit.")

            campo = edits[0]
            campo.click_input()
            await worker_sleep(1)

            # Tenta limpar o campo e verifica se realmente foi limpo
            max_tentativas = 3
            for tentativa in range(max_tentativas):
                campo.set_edit_text("")
                await worker_sleep(0.5)

                texto_atual = campo.window_text().strip()
                if texto_atual == "":
                    break  # Campo foi limpo com sucesso
                print(
                    f"Tentativa {tentativa+1}: campo ainda contém texto: '{texto_atual}'"
                )

            # Continua se o campo estiver limpo
            campo.type_keys("Livro de Apuração ICMS", with_spaces=True)
            await worker_sleep(1)

            send_keys("{ENTER}")
            await worker_sleep(2)
            send_keys("{ENTER}")

            # await worker_sleep(5)
            console.print("Inserindo competência...")

            # Conecta na janela
            app = Application().connect(class_name="TFrmMovtoApuraIcmsNew", timeout=60)
            main_window = app["TFrmMovtoApuraIcmsNew"]
            main_window.set_focus()

            # Captura o campo de data (TDBIEditDate)
            data_input = main_window.child_window(
                class_name="TDBIEditDate", found_index=0
            )
            data_input.click_input()

            await worker_sleep(5)

            data_input.set_edit_text("")  # Limpa o campo

            # Define a competência
            # Ex: "07/2025"
            data_input.type_keys(competencia, with_spaces=True)

            console.print("Clicando no botão incluir apuração")
            # Clicar em incluir apuração
            imagem = rf"{ASSETS_PATH}\btn_incluir_apuracao.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)

            if localizacao:
                console.print(f"Imagem incluir apuração encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
                console.print("Botão incluir clicado com sucesso")

                await worker_sleep(2)

                # === 5) Se não houve 'Aviso' com erro mapeado, considera sucesso ===
                console.print("Nenhum erro confirmado. Fluxo OK.")
                try:
                    main_window.close()
                    console.print("Janela principal fechada.")
                except Exception as e:
                    console.print(f"Falha ao fechar janela principal (ignorado): {e}")

                retorno = "Apuração incluída com sucesso"
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

    except Exception as erro:

        console.print(f"Erro ao executar abertura de livros fiscais, erro : {erro}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na Abertura de Livro Fiscal : {erro}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
