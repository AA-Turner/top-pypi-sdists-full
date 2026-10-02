import asyncio
import os
from datetime import datetime
from pywinauto import Application, timings, findwindows, Desktop
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
from pywinauto.keyboard import send_keys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name, send_file
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    login_emsys,
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


async def extracao_saldo_estoque(task: RpaProcessoEntradaDTO):
    try:
        config = await get_config_by_name("login_emsys")
        periodo = task.configEntrada["periodo"]
        periodo_format = periodo.replace("/", "")
        filial = task.configEntrada["filialEmpresaOrigem"]
        historico_id = task.historico_id

        console.print("Finalizando processos antigos do EMSys...", style="bold yellow")
        await kill_all_emsys()

        console.print("Iniciando EMSys...", style="bold green")
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_35.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        console.print("Fazendo login no EMSys...", style="bold cyan")
        return_login = await login_emsys(
            config.conConfiguracao, app, task, filial_origem=filial
        )

        if return_login.sucesso:
            console.print("Login realizado com sucesso", style="bold green")
            type_text_into_field(
                "Rel. Saldo Estoque ", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"Erro no login: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(2)

        console.print("Abrindo janela Relatório de Saldo de Estoque...", style="bold cyan")
        app = Application().connect(class_name="TFrmRelSaldoEstoque", timeout=60)
        main_window = app["TFrmRelSaldoEstoque"]
        main_window.set_focus()

        console.print("Marcando campo de data...", style="bold cyan")
        main_window.child_window(class_name="TCheckBox", found_index=3).click_input()

        await worker_sleep(2)

        console.print(f"Inserindo período: {periodo}", style="bold cyan")
        data_input = main_window.child_window(class_name="TDBIEditDate", found_index=0) 
        data_input.set_edit_text(periodo)

        console.print("Gerando relatório...", style="bold cyan")
        main_window.child_window(class_name="TBitBtn", found_index=0).click_input()  

        timings.wait_until_passes(
            timeout=1800,
            retry_interval=1,
            func=lambda: Application().connect(class_name="TFrmPreviewRelatorio"),
        )
        await worker_sleep(2)

        console.print("Abrindo Preview Relatório...", style="bold cyan")
        app = Application().connect(class_name="TFrmPreviewRelatorio")
        main_window = app["TFrmPreviewRelatorio"]
        main_window.set_focus()

        max_tentativas = 5
        tentativa = 1
        sucesso = False

        # defina caminho_arquivo ANTES para não ficar indefinido
        caminho_arquivo = rf"C:\Users\automatehub\Downloads\saldo_estoque_{periodo_format}_{filial}.xlsx"

        while tentativa <= max_tentativas and not sucesso:
            console.print(f"Tentativa {tentativa} de {max_tentativas}", style="bold cyan")

            # 1) Abrir o picker pelo botão (imagem)
            console.print("Procurando botão de salvar (imagem)...", style="bold cyan")
            caminho_img = r'assets\\extracao_relatorios\\btn_salvar.png'
            if os.path.isfile(caminho_img):
                pos = pyautogui.locateCenterOnScreen(caminho_img, confidence=0.9)
                if pos:
                    pyautogui.click(pos)
                    console.print("Clique realizado no botão salvar", style="bold green")
                else:
                    console.print("Imagem encontrada mas não está visível na tela", style="bold yellow")
            else:
                console.print("Imagem do botão salvar NÃO existe", style="bold red")

            await worker_sleep(8)

            # 2) Selecionar formato Excel (desambiguando múltiplas TFrmRelatorioFormato)
            console.print("Selecionando formato Excel...", style="bold cyan")
            try:
                desktop = Desktop(backend="win32")

                # Liste todas as visíveis
                wins_visiveis = desktop.windows(class_name="TFrmRelatorioFormato", visible_only=True)
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
                            if w.child_window(class_name="TComboBox").exists(timeout=0.8):
                                candidatos.append(w)
                        except Exception:
                            pass
                    if candidatos:
                        alvo = candidatos[-1]     # a mais recente
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
                        console.print("Não foi possível localizar a opção de Excel no ComboBox.", style="bold red")
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
                for w in desktop.windows(class_name="TFrmRelatorioFormato", visible_only=True):
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
                app_save = Application(backend="win32").connect(title_re="Salvar para arquivo|Salvar como|Save As", timeout=30)
                spec_save = app_save.window(title_re="Salvar para arquivo|Salvar como|Save As")
                spec_save.wait("visible", timeout=30)
                win_save = spec_save.wrapper_object()
            except Exception as e:
                console.print(f"Não achou a janela 'Salvar para arquivo': {e}", style="bold red")
                tentativa += 1
                await worker_sleep(3)
                continue

            # 3.1) Remover arquivo pré-existente
            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                    console.print("Arquivo existente removido para evitar prompt de sobrescrita.", style="bold yellow")
                except Exception as e:
                    console.print(f"Não foi possível remover o arquivo existente: {e}", style="bold red")

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
                console.print(f"Arquivo configurado para: {caminho_arquivo}", style="bold green")

                await worker_sleep(1)

                btn_salvar_spec = spec_save.child_window(class_name="Button", found_index=0)
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
                spec_conf = app_conf.window(title_re="Confirm(ar)?( )?Salvar( )?Como|Confirm Save As")
                spec_conf.wait("visible", timeout=3)
                spec_conf.child_window(class_name="Button", found_index=0).click_input()
                console.print("Confirmação de sobrescrita respondida.", style="bold yellow")
            except Exception:
                pass

            await worker_sleep(2)

            # 4) Aguardar 'Printing' (se existir)
            console.print("Aguardando finalização do processo de impressão/salvamento...", style="bold cyan")
            try:
                app_print = Application(backend="win32").connect(title_re="Printing", timeout=5)
                spec_print = app_print.window(title_re="Printing")
                try:
                    spec_print.wait_not("visible", timeout=60)
                    console.print("Janela 'Printing' fechada.", style="bold green")
                except Exception:
                    console.print("Janela 'Printing' não fechou no tempo esperado. Seguindo.", style="bold yellow")
            except findwindows.ElementNotFoundError:
                console.print("Janela 'Printing' não apareceu.", style="bold yellow")
            except Exception as e:
                console.print(f"Erro ao aguardar 'Printing': {e}", style="bold yellow")

            # 5) Validar arquivo salvo
            if os.path.exists(caminho_arquivo):
                console.print(f"Arquivo encontrado: {caminho_arquivo}", style="bold green")
                with open(caminho_arquivo, "rb") as f:
                    file_bytes = io.BytesIO(f.read())
                sucesso = True
            else:
                console.print("Arquivo não encontrado, tentando novamente...", style="bold red")
                tentativa += 1
                await worker_sleep(3)

        if not sucesso:
            console.print("Falha após 5 tentativas. Arquivo não foi gerado.", style="bold red")

        nome_com_extensao = f'saldo_estoque_{periodo_format}_{filial}.xlsx'
        console.print("Enviando arquivo XLS para o BOF...", style="bold cyan")
        try:
            await send_file(
                historico_id,
                nome_com_extensao,
                "xlsx",
                file_bytes,
                file_extension="xlsx",
            )
            console.print("Removendo arquivo da pasta downloads", style="bold yellow")
            os.remove(caminho_arquivo)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Relatório enviado com sucesso!",
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

        console.print("Processo concluído com sucesso!", style="bold green")

    except Exception as ex:
        retorno = f"Erro Processo Fechamento Balancete: {str(ex)}"
        logger.error(retorno)
        console.print(retorno, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=retorno,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
