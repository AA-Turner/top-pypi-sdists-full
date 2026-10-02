import numpy
import asyncio
import sys
import os
import io
from pywinauto.keyboard import send_keys

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
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    worker_sleep,
)
from rich.console import Console
import pyautogui
from datetime import datetime

# from dateutil.relativedelta import relativedelta
from PIL import ImageFilter, ImageEnhance
from pytesseract import image_to_string
from pywinauto import Application, Desktop
import subprocess
import os
from worker_automate_hub.api.client import get_config_by_name, send_file
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


async def geracao_balancetes_filial(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    try:
        await kill_all_emsys()
        await open_contabil_processes()
        config = await get_config_by_name("login_emsys_contabil")
        filial = task.configEntrada.get("filialEmpresaOrigem")
        periodo_inicial = task.configEntrada.get("periodoInicial")
        periodo_final = task.configEntrada.get("periodoFinal")
        historico_id = task.historico_id
        if historico_id:
            console.print("Historico ID recuperado com sucesso...\n")
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
        console.print("Cicar em BAL")
        pyautogui.click(x=453, y=96)
        await worker_sleep(4)

        console.print("Preenchendo campo periodo...")

        app = Application(backend="win32").connect(class_name="TFrmBalancete")
        win = app.window(class_name="TFrmBalancete")

        # Seus índices: inicial = found_index=1, final = found_index=0
        ctrl_inicial = win.child_window(
            class_name="TRzEditDate", found_index=1
        ).wrapper_object()
        ctrl_final = win.child_window(
            class_name="TRzEditDate", found_index=0
        ).wrapper_object()

        # ---- Inicial ----
        try:
            ctrl_inicial.set_edit_text(periodo_inicial)  # tenta via WM_SETTEXT
        except Exception:
            ctrl_inicial.set_focus()
            ctrl_inicial.click_input()
            send_keys("^a{DELETE}")
            send_keys(
                periodo_inicial.replace("/", "")
            )  # fallback: digita só dígitos (máscara)

        # ---- Final ----
        try:
            ctrl_final.set_edit_text(periodo_final)
        except Exception:
            ctrl_final.set_focus()
            ctrl_final.click_input()
            send_keys("^a{DELETE}")
            send_keys(periodo_final.replace("/", ""))

        await worker_sleep(4)

        console.print("Selecionar detalhada por centro de custo..")
        detalhada = win.child_window(class_name="TRzComboBox", found_index=0)
        detalhada.select("Centro de Custo")

        await worker_sleep(6)

        console.print("Selecionar considerar contas analíticas zerada")
        contas_analit_zeradas = win.child_window(
            class_name="TRzCheckBox", found_index=2
        ).click()

        await worker_sleep(4)

        console.print("Selecionar considerar contas sintéticas zerada")
        contas_sint_zeradas = win.child_window(
            class_name="TRzCheckBox", found_index=0
        ).click()

        await worker_sleep(4)

        console.print("Selecionar por filiais")
        selec_filiais = win.child_window(
            class_name="TRzCheckBox", found_index=3
        ).click()

        await worker_sleep(4)

        console.print("Selecionar CSV")
        selec_csv = win.child_window(class_name="TRzComboBox", found_index=1)
        selec_csv.select("Arquivo CSV")

        await worker_sleep(4)

        console.print("Clicar em gerar relatório")
        btn_gerar_relatorio = win.child_window(
            class_name="TBitBtn", found_index=0
        ).click()

        # Selecionar filial
        app = Application(backend="win32").connect(
            title="Seleção de Empresas", timeout=10
        )
        dlg = app.window(title="Seleção de Empresas")
        edit = dlg.child_window(class_name="TEdit", found_index=0).wrapper_object()

        # Tenta via WM_SETTEXT
        try:
            edit.set_focus()
            edit.set_edit_text("")  # limpa
            edit.set_edit_text(filial)  # escreve
        except Exception:
            # Fallback: digita como teclado
            edit.set_focus()
            edit.click_input()
            send_keys("^a{DELETE}")
            send_keys("3", with_spaces=True)

        await worker_sleep(3)

        # Marcar filial
        imagem_alvo = "assets\\geracao_bal_filial\\btn_selec_uma_filial.png"

        btn_sect_uma = pyautogui.locateCenterOnScreen(
            imagem_alvo, confidence=0.9
        )  # requer opencv-python
        if btn_sect_uma:  # se achou, clica
            pyautogui.click(btn_sect_uma)

        btn_ok = dlg.child_window(class_name="TBitBtn", title="&OK").click()

        # aguarda até a janela "Gera Arquivo CSV (Excel)" existir (ou ficar visível)
        csv_win = Desktop(backend="win32").window(title="Gera Arquivo CSV (Excel)")
        csv_win.wait("exists", timeout=3600)

        app_csv = Application(backend="win32").connect(title="Gera Arquivo CSV (Excel)")
        dlg_csv = app_csv.window(title="Gera Arquivo CSV (Excel)")
        edit = dlg_csv.child_window(class_name="Edit", found_index=0)
        # Tenta via WM_SETTEXT (mais estável)
        try:
            periodo_inicial = periodo_inicial.replace("/", "")
            periodo_final = periodo_final.replace("/", "")
            edit.set_focus()
            edit.set_edit_text("")  # limpa
            edit.set_edit_text(
                rf"C:\Users\automatehub\Downloads\balancete_{periodo_inicial}_{periodo_final}_{filial}"
            )
        except Exception:
            # Fallback: digita como teclado
            edit.set_focus()
            edit.click_input()
            send_keys("^a{DELETE}")
            send_keys(
                rf"C:\Users\automatehub\Downloads\balancete_{periodo_inicial}_{periodo_final}_{filial}",
                with_spaces=True,
            )

        # Clicar em salvar
        app = Application(backend="win32").connect(
            title="Gera Arquivo CSV (Excel)", timeout=10
        )
        dlg = app.window(title="Gera Arquivo CSV (Excel)")
        btn_salvar = dlg.child_window(class_name="Button", found_index=0).click()

        await worker_sleep(6)

        # Janela confirmação clicar em OK
        app = Application(backend="win32").connect(title="Informação", timeout=10)
        dlg = app.window(title="Informação")
        btn_ok = dlg.child_window(class_name="Button", found_index=0).click()

        console.print("Arquivo salvo com sucesso...\n")
        await worker_sleep(3)
        path_to_txt = rf"C:\Users\automatehub\Downloads\balancete_{periodo_inicial}_{periodo_final}_{filial}"

        with open(f"{path_to_txt}.csv", "rb") as file:
            file_bytes = io.BytesIO(file.read())

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desArquivo = f"balancete_{periodo_inicial}_{periodo_final}_{filial}.csv"
        try:
            await send_file(
                historico_id, desArquivo, "csv", file_bytes, file_extension="csv"
            )
            os.remove(path_to_txt + ".csv")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Balancete gerado com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        except Exception as e:
            result = f"Arquivo balancete gerado com sucesso, porém gerou erro ao realizar o envio para o backoffice {e} - Arquivo ainda salvo na dispositivo utilizado no diretório {path_to_txt}!"
            console.print(result, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=result,
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
