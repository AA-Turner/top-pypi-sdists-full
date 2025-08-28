import asyncio
import os
from datetime import datetime
from pywinauto import Application, timings, findwindows
import sys
import io

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
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
        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_35.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(
            config.conConfiguracao, app, task, filial_origem=filial
        )

        if return_login.sucesso == True:
            type_text_into_field(
                "Rel. Saldo Estoque ", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")

        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(2)

        ##### Janela Relatório Saldos do Estoque #####
        # Marcar check box data
        app = Application().connect(class_name="TFrmRelSaldoEstoque", timeout=60)
        main_window = app["TFrmRelSaldoEstoque"]
        main_window.set_focus()

        # Captura o campo de data
        data_chk = main_window.child_window(
            class_name="TCheckBox", found_index=3
        ).click_input()

        await worker_sleep(2)
        # Insere a data
        data_input = main_window.child_window(class_name="TDBIEditDate", found_index=0)

        data_input.set_edit_text(periodo)

        # Clicar em gerar relatório
        btn_gerar = main_window.child_window(
            class_name="TBitBtn", found_index=0
        ).click_input()

        # Aguarda até 60 segundos para a janela aparecer
        timings.wait_until_passes(
            timeout=1800,
            retry_interval=1,
            func=lambda: Application().connect(class_name="TFrmPreviewRelatorio"),
        )

        await worker_sleep(10)

        # Conecta à janela Preview Relatorio
        app = Application().connect(class_name="TFrmPreviewRelatorio")
        main_window = app["TFrmPreviewRelatorio"]
        main_window.set_focus()

        # Clicar em salvar
        caminho = r"assets\\extracao_relatorios\\btn_salvar.png"
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

        await worker_sleep(2)

        # Conecta na janela Configuração para Salvar Arquivo
        app = Application().connect(class_name="TFrmRelatorioFormato")
        main_window = app["TFrmRelatorioFormato"]
        main_window.set_focus()
        # Acessa o ComboBox pelo identificador conhecido
        combo = main_window.ComboBox

        # Garante que existe "Excel" na lista
        itens = combo.texts()
        print("Itens do ComboBox:", itens)

        # Seleciona o Excel correto (o segundo da lista, índice 8)
        combo.select(8)

        await worker_sleep(2)

        # Clicar em Salvar
        main_window.child_window(class_name="TBitBtn", found_index=1).click_input()

        await worker_sleep(5)

        # Conecta na janela "Salvar para arquivo"
        app = Application().connect(title_re="Salvar para arquivo", timeout=30)
        main_window = app.window(title_re="Salvar para arquivo")

        # Campo Nome (Edit) - use set_edit_text para evitar problemas de escape
        campo_nome = main_window.child_window(
            class_name="Edit", control_id=1148
        ).wrapper_object()
        caminho_arquivo = f"C:\\Users\\automatehub\\Downloads\\saldo_estoque_{periodo_format}_{filial}.xlsx"
        campo_nome.set_focus()
        campo_nome.set_edit_text(caminho_arquivo)

        print("✅ Texto inserido no campo Nome")

        await worker_sleep(2)

        # Clicar em ok para salvar
        main_window.child_window(class_name="Button", found_index=0).click_input()

        await worker_sleep(20)

        # caminho_img = r"assets\\extracao_relatorios\\janela_printing.png"

        # Aguarda até a janela com título "Printing" (ou "Salvando...") fechar

        try:
            app = Application().connect(title_re="Printing")  # conecta se existir
            janela = app.window(title_re="Printing")

            print("⏳ Aguardando a janela 'Printing' sumir...")
            janela.wait_not("visible", timeout=60)  # espera até 60 segundos
            print("✅ Janela 'Printing' fechada.")

        except findwindows.ElementNotFoundError:
            print("⚠️ Janela 'Printing' não estava aberta.")

        nome_com_extensao = f"saldo_estoque_{periodo_format}_{filial}.xlsx"
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
        retorno = f"Erro Processo Fechamento Balancete: {str(ex)}"
        logger.error(retorno)
        console.print(retorno, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=retorno,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
