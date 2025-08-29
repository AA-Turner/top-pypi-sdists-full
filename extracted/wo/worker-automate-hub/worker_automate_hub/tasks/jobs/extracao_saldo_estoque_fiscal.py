import asyncio
import os
from datetime import datetime
from pywinauto import Application, timings, findwindows, keyboard
import sys
import io

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

        app = Application(backend="win32").start(
            "C:\\Rezende\\EMSys3\\EMSysFiscal_39.exe"
        )
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
        keyboard.send_keys("^a{BACKSPACE}07/2025")

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
        # Clicar em Sim
        btn_sim = main_window.child_window(
            class_name="Button", found_index=1
        ).click_input()

        await worker_sleep(2)

        ##### Janela Informa Motivo do Inventario #####
        app = Application().connect(class_name="TFrmMotvoMotivoInventario")
        main_window = app.window(class_name="TFrmMotvoMotivoInventario")
        main_window.wait("exists enabled visible ready", timeout=20)
        slc_01 = main_window.child_window(
            class_name="TDBIComboBoxValues", found_index=0
        ).click_input()
        await worker_sleep(0.1)
        keyboard.send_keys("01" + "{ENTER}")
        await worker_sleep(0.2)

        # Clicar em confirmar
        main_window.child_window(class_name="TBitBtn", found_index=0).click_input()

        await worker_sleep(5)

        ##### Conecta à janela Preview Relatorio #####
        app = Application(backend="win32").connect(class_name="TFrmPreviewRelatorio")

        # Espera até a janela aparecer e estar pronta
        main_window = app.window(class_name="TFrmPreviewRelatorio")
        main_window.wait("exists enabled visible ready", timeout=180)

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
        app = Application().connect(class_name="TFrmRelatorioFormato", found_index=0)
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
        btn_salvar = main_window.child_window(
            class_name="TBitBtn", found_index=1
        ).click_input()

        await worker_sleep(5)

        # Conecta na janela "Salvar para arquivo"
        app = Application().connect(title_re="Salvar para arquivo", timeout=30)
        main_window = app.window(title_re="Salvar para arquivo")

        # Campo Nome (Edit) - use set_edit_text para evitar problemas de escape
        campo_nome = main_window.child_window(
            class_name="Edit", control_id=1148
        ).wrapper_object()
        caminho_arquivo = rf"C:\Users\automatehub\Downloads\saldo_estoque_fiscal_{periodo_format}_{filial}.xlsx"
        campo_nome.set_focus()
        campo_nome.set_edit_text(caminho_arquivo)

        print("✅ Texto inserido no campo Nome")

        await worker_sleep(3)
       
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
        caminho_arquivo = f"C:\\Users\\automatehub\\Downloads\\saldo_estoque_fiscal_{periodo_format}_{filial}.xlsx"
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
