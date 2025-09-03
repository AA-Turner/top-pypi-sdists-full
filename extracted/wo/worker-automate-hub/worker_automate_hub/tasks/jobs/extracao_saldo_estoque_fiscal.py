import asyncio
import os
from datetime import datetime
from pywinauto import Application, timings, findwindows, keyboard, Desktop
import sys
import io
import win32gui

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

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
from pywinauto.keyboard import send_keys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name, send_file
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    login_emsys_fiscal,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


async def extracao_saldo_estoque_fiscal(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys_fiscal")
        periodo = task.configEntrada["periodo"]
        periodo_format = periodo.replace("/", "")
        filial = task.configEntrada["filialEmpresaOrigem"]
        historico_id = task.historico_id
        await kill_all_emsys()

        config = await get_config_by_name("login_emsys_fiscal")

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSysFiscal.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        await worker_sleep(5)

        try:
            app = Application(backend="win32").connect(
                class_name="TFrmLoginModulo", timeout=100
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

        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(7)

        ##### Janela Movimento Livros Fiscais #####
        # Conecta na janela principal
        app = Application().connect(class_name="TFrmMovtoLivroFiscal")
        main_window = app.window(class_name="TFrmMovtoLivroFiscal")
        main_window.wait("exists enabled visible ready", timeout=20)

        # Pegar o wrapper do campo
        campo_data = main_window.child_window(class_name="TDBIEditDate")
        campo_data.wait("exists enabled visible ready", timeout=10)
        campo_data = campo_data.wrapper_object()  # agora é o controle de fato

        # Foco e clique
        campo_data.set_focus()
        campo_data.click_input()

        # Limpa e digita
        keyboard.send_keys("^a{BACKSPACE}" + periodo)

        # Seleciona inventário
        chk_inventario = main_window.child_window(
            class_name="TcxCheckBox", found_index=6
        ).click_input()

        await worker_sleep(2)

        # Caminho da imagem do botão
        imagem_botao = r"assets\\extracao_relatorios\\btn_incluir_livro.png"

        if os.path.exists(imagem_botao):
            try:
                # Localiza a imagem na tela
                botao = pyautogui.locateCenterOnScreen(
                    imagem_botao, confidence=0.9
                )  # confidence precisa do opencv instalado
                if botao:
                    pyautogui.click(botao)
                    print("Botão clicado com sucesso!")
                else:
                    print("Não encontrou o botão na tela.")
            except Exception as e:
                print(f"Erro ao localizar/clicar na imagem: {e}")
        else:
            print("Caminho da imagem não existe.")

        ##### Janela Perguntas da Geração Livros Fiscais #####
        app = Application().connect(class_name="TPerguntasLivrosFiscaisForm")
        main_window = app.window(class_name="TPerguntasLivrosFiscaisForm")
        main_window.wait("exists enabled visible ready", timeout=20)

        respostas = ["Não", "Sim", "Não", "Não"]

        for i, resposta in enumerate(respostas):
            combo = main_window.child_window(
                class_name="TDBIComboBoxValues", found_index=i
            ).wrapper_object()
            combo.set_focus()
            combo.click_input()
            await worker_sleep(0.1)
            keyboard.send_keys(resposta + "{ENTER}")
            await worker_sleep(0.2)
        # Clicar em confirmar
        main_window.child_window(class_name="TButton", found_index=1).click_input()

        await worker_sleep(2)

        ##### Janela Gerar Registros #####
        app = Application(backend="win32").connect(title="Gerar Registros")
        main_window = app.window(title="Gerar Registros")

        # Clicar no botão "Sim"
        main_window.child_window(title="&Sim", class_name="Button").click_input()

        await worker_sleep(2)

        ##### Janela Informa Motivo do Inventario #####
        app = Application().connect(class_name="TFrmMotvoMotivoInventario")
        main_window = app.window(class_name="TFrmMotvoMotivoInventario")
        main_window.wait("exists enabled visible ready", timeout=20)
        slc_01 = main_window.child_window(
            class_name="TDBIComboBoxValues", found_index=0
        ).click_input()
        await worker_sleep(1)
        keyboard.send_keys("01" + "{ENTER}")
        await worker_sleep(2)

        # Clicar em confirmar
        main_window.child_window(class_name="TBitBtn", found_index=0).click_input()

        await worker_sleep(5)

        CLASS = "TFrmPreviewRelatorio"

        # 1) Espera a janela aparecer (até 180s)
        desk = Desktop(backend="win32")
        deadline = time.time() + 180
        win = None
        while time.time() < deadline:
            try:
                w = desk.window(class_name=CLASS)
                if w.exists(timeout=0.5):
                    w.wait("visible enabled ready", timeout=30)
                    win = w
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if win is None:
            raise TimeoutError(f"Janela '{CLASS}' não apareceu dentro do timeout.")

        # 2) Conecta ao app usando o handle da janela encontrada
        app = Application(backend="win32").connect(handle=win.handle)
        main_window = app.window(handle=win.handle)

        # Dá o foco na janela
        main_window.set_focus()

        await worker_sleep(2)

        main_window.close()

        await worker_sleep(2)

        ##### Janela Movimento Livro Fiscal #####
        # Selecionar primeira linha inventario
        pyautogui.click(928, 475)

        await worker_sleep(2)

        # Clicar em visualizar livro
        caminho = r"assets\\extracao_relatorios\\btn_visu_livros.png"
        # Verifica se o arquivo existe
        if os.path.isfile(caminho):
            print("A imagem existe:", caminho)

            # Procura a imagem na tela
            pos = pyautogui.locateCenterOnScreen(
                caminho, confidence=0.9
            )  # ajuste o confidence se necessário
            if pos:
                pyautogui.click(pos)  # clica no centro da imagem
                print("Clique realizado na imagem.")
            else:
                print("Imagem encontrada no disco, mas não está visível na tela.")
        else:
            print("A imagem NÃO existe:", caminho)

        await worker_sleep(5)

        ##### Janela Movimento Livro Fiscal - Livro - Inventario para Competencia #####
        app = Application().connect(class_name="TFrmMovtoLivroFiscal")
        main_window = app.window(class_name="TFrmMovtoLivroFiscal")
        main_window.wait("exists enabled visible ready", timeout=20)
        input_7 = main_window.child_window(
            class_name="TDBIEditCode", found_index=0
        ).click_input()
        await worker_sleep(0.1)
        keyboard.send_keys("7" + "{TAB}")
        await worker_sleep(0.2)
        # Clicar em imprimir
        btn_imprimir = main_window.child_window(
            class_name="TBitBtn", found_index=0
        ).click_input()

        await worker_sleep(2)

        ##### Janela Selecion o Template Desejado #####
        app = Application().connect(class_name="TFrmFRVisualizaTemplateMenuNew")
        main_window = app.window(class_name="TFrmFRVisualizaTemplateMenuNew")
        main_window.wait("exists enabled visible ready", timeout=20)
        btn_gerar_rel = main_window.child_window(
            class_name="TBitBtn", found_index=1
        ).click_input()

        await worker_sleep(2)

        ##### Janela Parametros #####
        app = Application().connect(class_name="TFrmFRParametroRelatorio")
        main_window = app.window(class_name="TFrmFRParametroRelatorio")
        main_window.wait("exists enabled visible ready", timeout=20)
        slc_nao = main_window.child_window(
            class_name="TComboBox", found_index=0
        ).click_input()
        await worker_sleep(0.1)
        keyboard.send_keys("NAO" + "{ENTER}")
        await worker_sleep(0.2)

        # Clicar BOTAO OK
        slc_nao = main_window.child_window(
            class_name="TBitBtn", found_index=1
        ).click_input()

        await worker_sleep(2)

        max_tentativas = 5
        tentativa = 1
        sucesso = False

        # defina caminho_arquivo ANTES para não ficar indefinido
        caminho_arquivo = rf"C:\Users\automatehub\Downloads\saldo_estoque_fiscal_{periodo_format}_{filial}.xlsx"

        while tentativa <= max_tentativas and not sucesso:
            console.print(
                f"Tentativa {tentativa} de {max_tentativas}", style="bold cyan"
            )

            # 1) Abrir o picker pelo botão (imagem)
            console.print("Procurando botão de salvar (imagem)...", style="bold cyan")
            caminho_img = r"assets\\extracao_relatorios\btn_salvar.png"
            if os.path.isfile(caminho_img):
                pos = pyautogui.locateCenterOnScreen(caminho_img, confidence=0.9)
                if pos:
                    pyautogui.click(pos)
                    console.print(
                        "Clique realizado no botão salvar", style="bold green"
                    )
                else:
                    console.print(
                        "Imagem encontrada mas não está visível na tela",
                        style="bold yellow",
                    )
            else:
                console.print("Imagem do botão salvar NÃO existe", style="bold red")

            await worker_sleep(8)

            # 2) Selecionar formato Excel (desambiguando múltiplas TFrmRelatorioFormato)
            console.print("Selecionando formato Excel...", style="bold cyan")
            try:
                desktop = Desktop(backend="win32")

                # Liste todas as visíveis
                wins_visiveis = desktop.windows(
                    class_name="TFrmRelatorioFormato", visible_only=True
                )
                if not wins_visiveis:
                    raise RuntimeError("Janela de formato não apareceu.")

                # 2.1) Tente a janela em foco (foreground)
                h_fore = win32gui.GetForegroundWindow()
                alvo = None
                for w in wins_visiveis:
                    if w.handle == h_fore:
                        alvo = w
                        break

                # 2.2) Se não estiver em foco, pegue a que contém um TComboBox (a 'Configuração para Salvar arq...')
                if alvo is None:
                    candidatos = []
                    for w in wins_visiveis:
                        try:
                            if w.child_window(class_name="TComboBox").exists(
                                timeout=0.8
                            ):
                                candidatos.append(w)
                        except Exception:
                            pass
                    if candidatos:
                        alvo = candidatos[-1]  # a mais recente
                    else:
                        alvo = wins_visiveis[-1]  # fallback

                # Trabalhe via WindowSpecification
                spec_fmt = desktop.window(handle=alvo.handle)
                spec_fmt.wait("visible", timeout=10)
                win_fmt = spec_fmt.wrapper_object()
                win_fmt.set_focus()

                # Acessar o ComboBox
                try:
                    combo_spec = spec_fmt.child_window(class_name="TComboBox")
                except Exception:
                    combo_spec = spec_fmt.child_window(control_type="ComboBox")
                combo_spec.wait("exists enabled", timeout=10)
                combo = combo_spec.wrapper_object()

                textos = combo.texts()
                console.print(f"Itens do ComboBox: {textos}", style="bold yellow")

                # Seleção por índice conhecido; fallback por texto
                try:
                    combo.select(8)
                except Exception:
                    alvo_idx = None
                    for i, t in enumerate(textos):
                        if "EXCEL" in str(t).upper() or "XLSX" in str(t).upper():
                            alvo_idx = i
                            break
                    if alvo_idx is None:
                        console.print(
                            "Não foi possível localizar a opção de Excel no ComboBox.",
                            style="bold red",
                        )
                        tentativa += 1
                        await worker_sleep(2)
                        continue
                    combo.select(alvo_idx)

                await worker_sleep(1)

                # Clique em OK
                btn_ok_spec = spec_fmt.child_window(class_name="TBitBtn", found_index=1)
                btn_ok_spec.wait("enabled", timeout=5)
                btn_ok_spec.click_input()

                # Aguarde a janela de formato desaparecer
                try:
                    spec_fmt.wait_not("visible", timeout=10)
                except Exception:
                    pass

                # Feche possíveis duplicatas remanescentes (defensivo)
                for w in desktop.windows(
                    class_name="TFrmRelatorioFormato", visible_only=True
                ):
                    if w.handle != alvo.handle:
                        try:
                            w.close()
                        except Exception:
                            pass

            except Exception as e:
                console.print(f"Falha ao selecionar formato: {e}", style="bold red")
                tentativa += 1
                await worker_sleep(3)
                continue

            await worker_sleep(5)

            # 3) Janela "Salvar para arquivo"
            console.print("Abrindo janela de salvar arquivo...", style="bold cyan")
            try:
                app_save = Application(backend="win32").connect(
                    title_re="Salvar para arquivo|Salvar como|Save As", timeout=30
                )
                spec_save = app_save.window(
                    title_re="Salvar para arquivo|Salvar como|Save As"
                )
                spec_save.wait("visible", timeout=30)
                win_save = spec_save.wrapper_object()
            except Exception as e:
                console.print(
                    f"Não achou a janela 'Salvar para arquivo': {e}", style="bold red"
                )
                tentativa += 1
                await worker_sleep(3)
                continue

            # 3.1) Remover arquivo pré-existente
            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                    console.print(
                        "Arquivo existente removido para evitar prompt de sobrescrita.",
                        style="bold yellow",
                    )
                except Exception as e:
                    console.print(
                        f"Não foi possível remover o arquivo existente: {e}",
                        style="bold red",
                    )

            # 3.2) Preencher nome e salvar
            try:
                campo_spec = spec_save.child_window(class_name="Edit", control_id=1148)
                campo_spec.wait("exists enabled visible", timeout=10)
                campo_nome = campo_spec.wrapper_object()
                campo_nome.set_focus()
                try:
                    campo_nome.set_edit_text("")
                except Exception:
                    campo_nome.type_keys("^a{DELETE}", pause=0.02)

                campo_nome.type_keys(caminho_arquivo, with_spaces=True, pause=0.01)
                console.print(
                    f"Arquivo configurado para: {caminho_arquivo}", style="bold green"
                )

                await worker_sleep(1)

                btn_salvar_spec = spec_save.child_window(
                    class_name="Button", found_index=0
                )
                btn_salvar_spec.wait("enabled", timeout=10)
                btn_salvar_spec.click_input()

                # Esperar a janela sumir
                try:
                    spec_save.wait_not("visible", timeout=15)
                except Exception:
                    pass

            except Exception as e:
                console.print(f"Erro ao confirmar salvar: {e}", style="bold red")
                tentativa += 1
                await worker_sleep(3)
                continue

            await worker_sleep(2)

            # 3.3) Confirmar sobrescrita (se houver)
            try:
                app_conf = Application(backend="win32").connect(
                    title_re="Confirm(ar)?( )?Salvar( )?Como|Confirm Save As", timeout=3
                )
                spec_conf = app_conf.window(
                    title_re="Confirm(ar)?( )?Salvar( )?Como|Confirm Save As"
                )
                spec_conf.wait("visible", timeout=3)
                spec_conf.child_window(class_name="Button", found_index=0).click_input()
                console.print(
                    "Confirmação de sobrescrita respondida.", style="bold yellow"
                )
            except Exception:
                pass

            await worker_sleep(2)

            # 4) Aguardar 'Printing' (se existir)
            console.print(
                "Aguardando finalização do processo de impressão/salvamento...",
                style="bold cyan",
            )
            try:
                app_print = Application(backend="win32").connect(
                    title_re="Printing", timeout=5
                )
                spec_print = app_print.window(title_re="Printing")
                try:
                    spec_print.wait_not("visible", timeout=60)
                    console.print("Janela 'Printing' fechada.", style="bold green")
                except Exception:
                    console.print(
                        "Janela 'Printing' não fechou no tempo esperado. Seguindo.",
                        style="bold yellow",
                    )
            except findwindows.ElementNotFoundError:
                console.print("Janela 'Printing' não apareceu.", style="bold yellow")
            except Exception as e:
                console.print(f"Erro ao aguardar 'Printing': {e}", style="bold yellow")

            # 5) Validar arquivo salvo
            if os.path.exists(caminho_arquivo):
                console.print(
                    f"Arquivo encontrado: {caminho_arquivo}", style="bold green"
                )
                with open(caminho_arquivo, "rb") as f:
                    file_bytes = io.BytesIO(f.read())
                sucesso = True
            else:
                console.print(
                    "Arquivo não encontrado, tentando novamente...", style="bold red"
                )
                tentativa += 1
                await worker_sleep(3)

        if not sucesso:
            console.print(
                "Falha após 5 tentativas. Arquivo não foi gerado.", style="bold red"
            )

        nome_com_extensao = f"saldo_estoque_fiscal_{periodo_format}_{filial}.xlsx"
        # lê o arquivo
        print(caminho_arquivo)
        with open(f"{caminho_arquivo}", "rb") as file:
            file_bytes = io.BytesIO(file.read())

        console.print("Enviar Excel para o BOF")
        try:
            await send_file(
                historico_id,
                nome_com_extensao,
                "xlsx",
                file_bytes,
                file_extension="xlsx",
            )
            console.print("Removendo arquivo XLS da pasta downloads")
            os.remove(f"{caminho_arquivo}")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Relatório gerado com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        except Exception as e:
            console.print(f"Erro ao enviar o arquivo: {e}", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao enviar o arquivo: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as ex:
        retorno = f"Erro Processo Saldo Estoque Fiscal: {str(ex)}"
        logger.error(retorno)
        console.print(retorno, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=retorno,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
