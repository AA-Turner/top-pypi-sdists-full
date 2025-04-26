import asyncio
import calendar
import datetime
import getpass
import io
import math
import os
import re
import shutil
import subprocess
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, TypedDict

import aiohttp
import cv2
import psutil
import pyautogui
import pyperclip
from pywinauto import Desktop
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image, ImageEnhance
from prompt_toolkit.shortcuts import checkboxlist_dialog
from pytesseract import pytesseract
from pywinauto.application import Application, findwindows
from pywinauto.keyboard import send_keys
from pywinauto_recorder.player import set_combobox
from rich.console import Console
import win32clipboard

from worker_automate_hub.config.settings import load_worker_config
from worker_automate_hub.decorators.repeat import repeat
from worker_automate_hub.models.dao.rpa_configuracao import RpaConfiguracao
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import get_installed_version

console = Console()

ASSETS_PATH = "assets"

global_variables = {}


def set_variable(key, value):
    global_variables[key] = value


def get_variable(key):
    return global_variables.get(key, None)


async def worker_sleep(multiplier: int):
    """
    Função que espera o tempo configurado multiplicado por um fator.

    O tempo de espera é definido pela variável global "timeout_multiplicador".
    Caso essa variável não esteja definida, uma exceção ValueError será levantada.
    Se o valor da variável for menor ou igual a zero, uma exceção ValueError será
    levantada.

    :param int multiplier: Fator de multiplicação do tempo de espera.
    :raises ValueError: Se a variável "timeout_multiplicador" não estiver definida
        ou for menor ou igual a zero.
    :raises TypeError: Se o valor da variável "timeout_multiplicador" não for um
        número (int ou float).
    """
    timeout_multiplicador = get_variable("timeout_multiplicador")
    if timeout_multiplicador is None:
        timeout_multiplicador = 1
        console.log("O timeout multiplicador não foi definido")

    # Adicionando delay de 1/3 em todas as chamadas do método
    delay = (timeout_multiplicador * multiplier) * 1.3

    console.log(
        f"Aguardando {(delay)} segundos...",
        style="bold yellow",
    )
    await asyncio.sleep(delay)


async def get_system_info():
    """
    Retorna um objeto com informações do sistema.

    As informações retornadas são:

    - UUID do robo
    - Porcentagem de uso de CPU no momento
    - Porcentagem de uso de memória no momento
    - Espaço disponível no disco em GB

    :return: Um objeto `SystemInfoDTO` com as informações do sistema.
    :rtype: SystemInfoDTO
    """
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "espacoDisponivel": f"{disk_info.free / (1024 ** 3):.2f}",
    }


async def get_new_task_info():
    worker_config = load_worker_config()
    atual_version = get_installed_version("worker-automate-hub")
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": atual_version,
    }


def multiselect_prompt(options, title="Select options"):
    result = checkboxlist_dialog(
        values=[(option, option) for option in options],
        title=title,
        text="Use space to select multiple options.\nPress Enter to confirm your selection.",
    ).run()

    if result is None:
        console.print("[red]No options selected.[/red]")


async def kill_process(process_name: str):
    """
    Mata um processo com o nome especificado.

    :param process_name: O nome do processo a ser finalizado.
    :type process_name: str

    :return: None
    :rtype: None

    :raises Exception: Se houver um erro ao tentar finalizar o processo.
    """
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            err_msg = f"Erro ao listar processos: {stderr.decode().strip()}"
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        if stdout is None:
            err_msg = "Não foi possível obter a lista de processos."
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        lines = stdout.decode().strip().split("\n")
        for line in lines:
            # Verifique se o processo atual corresponde ao nome do processo
            if process_name in line:
                try:
                    # O PID(Process ID)   a segunda coluna na saída do tasklist
                    pid = int(line.split(",")[1].strip('"'))
                    await asyncio.create_subprocess_exec(
                        "taskkill", "/PID", str(pid), "/F"
                    )
                    log_msg = f"Processo {process_name} (PID {pid}) finalizado."
                    logger.info(log_msg)
                    console.print(
                        f"\n{log_msg}\n",
                        style="bold green",
                    )
                except Exception as ex:
                    err_msg = f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}"
                    logger.error(err_msg)
                    console.print(
                        err_msg,
                        style="bold red",
                    )
        else:
            log_msg = f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}."
            logger.info(
                log_msg,
                None,
            )
            console.print(
                log_msg,
                style="bold yellow",
            )

    except Exception as e:
        err_msg = f"Erro ao tentar matar o processo: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                console.print(
                    f"[{counter+1}] - Elemento não encontrado na posição: {region_to_look}"
                )

            if element_center:
                console.print(
                    f"[{counter+1}] - Elemento encontrado na posição: {region_to_look}\n",
                    style="green",
                )
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await worker_sleep(1)

        return None
    except Exception as ex:
        console.print(
            f"{counter} - Buscando elemento na tela: {region_to_look}",
            style="bold yellow",
        )
        return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        try:
            app = Application().connect(class_name="TFrmMenuPrincipal", timeout=60)
            main_window = app["TFrmMenuPrincipal"]

            main_window.set_focus()
        except:
            console.print(f"Erro ao conectar na janela, tentando seguir..")

        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)

    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await worker_sleep(1)
                if element.wait("exists", timeout=2):
                    await worker_sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await worker_sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False


async def login_emsys_fiscal(
    config: dict, app, task: RpaProcessoEntradaDTO
) -> RpaRetornoProcessoDTO:
    """
    Função que realiza o login no EMSys Fiscal.

    Args:
        config (dict): Dicionario com as configuracoes do login no EMSys Fiscal.
        app: Aplicacao do EMSys Fiscal.
        task (RpaProcessoEntradaDTO): Dicionario com as informacoes do processo.

    Returns:
        RpaRetornoProcessoDTO: Dicionario com o resultado do login.
    """

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    filial_cod = task.configEntrada.get("empresa")
    console.print(f"Empresa a ser processada: {filial_cod}")

    try:
        console.print("\nEMSys Fiscal inciado com sucesso...", style="bold green")
        app = Application().connect(class_name="TFrmLoginModulo")
        main_window = app["Login"]

        user = config.get("user")
        password = config.get("pass")

        if not user or not password:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: Não foi possivel obter as credencias para login",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        main_window.set_focus()
        await worker_sleep(2)
        edit_user = main_window.child_window(
            class_name="TcxCustomInnerTextEdit", found_index=1
        )
        edit_user.click()
        await worker_sleep(2)
        pyautogui.write(user)

        await worker_sleep(2)
        edit_password = main_window.child_window(
            class_name="TcxCustomInnerTextEdit", found_index=0
        )
        edit_password.click()
        await worker_sleep(2)
        pyautogui.write(password)

        await worker_sleep(2)
        edit_password.type_keys("{ENTER}")
        await worker_sleep(6)

        max_attempts = 15
        i = 0
        while i < max_attempts:
            selecionar_empresa = await is_window_open_by_class(
                "TFrmSelecaoEmpresa", "TFrmSelecaoEmpresa"
            )
            if selecionar_empresa["IsOpened"] == True:
                console.print(
                    "janela para gerar seleção da empresa foi aberta com sucesso...\n"
                )
                break
            else:
                warning_pop_up = await is_window_open("Warning")
                information_pop = await is_window_open("Information")
                if warning_pop_up["IsOpened"] == True or information_pop == True:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Pop-up Warning/Information ao tentar realizar login",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
                else:
                    edit_password.type_keys("{ENTER}")
                    await worker_sleep(1)
                    i = i + 1

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela para seleção da empresa, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Seleciona a filial do emsys
        console.print(f"Seleciona a filial {filial_cod} no emsys...")
        app = Application().connect(class_name="TFrmSelecaoEmpresa")
        main_window = app["TFrmSelecaoEmpresa"]
        main_window.set_focus()

        edit_filial = main_window.child_window(class_name="TEdit", found_index=0)
        edit_filial.click()
        await worker_sleep(1)
        pyautogui.write(filial_cod)
        await worker_sleep(2)
        edit_filial.type_keys("{ENTER}")

        await worker_sleep(10)
        console.print(f"Verificando a presença de Confirm...")
        confirm_pop_up = await is_window_open("Confirm")
        if confirm_pop_up["IsOpened"] == True:  
            app = Application().connect(class_name="TMessageForm")
            main_window = app["TMessageForm"]
            main_window.set_focus()
            main_window.child_window(title="&No").click()

        await worker_sleep(10)
        
        console.print(f"Verificando a presença de Warning...")
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: Não foi possível acessar a filial {filial_cod}, esta com o CNPJ bloqueado, por favor verificar",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        information_pop_up = await is_window_open_by_class(
            "TMessageForm", "TMessageForm"
        )
        if information_pop_up["IsOpened"] == True:
            app_information = Application().connect(class_name="TMessageForm")
            main_window_information = app_information["TMessageForm"]
            main_window.set_focus()
            await worker_sleep(2)
            btn_no = main_window_information["&No"]
            if btn_no.exists():
                try:
                    btn_no.click()
                    await worker_sleep(3)
                    console.print(
                        "O botão No após selecionar a filiam na seleção de empresa foi clicado com sucesso.",
                        style="green",
                    )
                except:
                    console.print(
                        "Falha ao clicar no botão No após selecionar a filiam na seleção de empresa",
                        style="red",
                    )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro: Botão No, nao existe no pop-up information após a seleção da filial da empresa",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

        max_attempts = 10
        i = 0
        while i < max_attempts:
            console.print("Aguardando o EMSys Fiscal...\n")
            emsys_opened = await is_window_open_by_class(
                "TFrmPrincipalFiscal", "TFrmPrincipalFiscal"
            )
            if emsys_opened["IsOpened"] == True:
                console.print("Login realizado com sucesso.", style="bold green")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Logou com sucesso no emsys!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            else:
                i = i + 1
                await worker_sleep(1)

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir o EMSys Fiscal, tela de login não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        log_msg = f"Erro ao realizar login no EMSys Fiscal, erro: {e}..."
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def login_emsys(
    config: dict, app, task: RpaProcessoEntradaDTO, **kwargs
) -> RpaRetornoProcessoDTO:
    """
    Função que realiza o login no EMSys.

    Args:
        config (dict): Dicionario com as configuracoes do login no EMSys.
        app: Aplicacao do EMSys.
        task (RpaProcessoEntradaDTO): Dicionario com as informacoes do processo.

    Returns:
        RpaRetornoProcessoDTO: Dicionario com o resultado do login.
    """

    # Para processos onde a config_entrada é enviada vazia, obtemos
    # o número da filial através do **kwargs
    filial_origem = kwargs.get("filial_origem", None)

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    await worker_sleep(15)
    # await asyncio.sleep(10)
    # Testa se existe alguma mensagem no Emsys
    console.print("Testando se existe alguma mensagem no Emsys...")
    window_message_login_emsys = await find_element_center(
        "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 15
    )

    # Clica no "Não mostrar novamente" se existir
    console.print("Clicando no 'Não mostrar novamente' se existir...")
    if window_message_login_emsys:
        pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
        pyautogui.click(
            window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
        )
        console.print("Mensagem de login encontrada e fechada.", style="bold green")

    # Ve se o Emsys esta aberto no login
    console.print("Verificando se o Emsys esta aberto no login...")
    image_emsys_login = await find_element_center(
        "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 60
    )

    # if image_emsys_login == None:
    #     image_emsys_login = await find_element_center(
    #     "assets/emsys/logo_emsys_linx_login.png", (800, 200, 1400, 700), 60
    # )

    if image_emsys_login:
        console.print("Aguardando a janela de login ficar pronta...")
        if await wait_element_ready_win(app["Login"]["Edit2"], 80):
            console.print("Procurando o icone disconect_database...")
            disconect_database = await find_element_center(
                "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 60
            )

            if disconect_database:
                # Realiza login no Emsys
                console.print("Realizando login no Emsys...")
                type_text_into_field(
                    config.get("user"), app["Login"]["Edit2"], True, "50"
                )
                pyautogui.press("tab")
                type_text_into_field(
                    config.get("pass"),
                    app["Login"]["Edit1"],
                    True,
                    "50",
                )
                pyautogui.press("enter")

                # Seleciona a filial do emsys
                console.print("Seleciona a filial do emsys...")
                selecao_filial = await find_element_center(
                    "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 15
                )

                console.print(f"Selecao filial via imagem: {selecao_filial}")
                if selecao_filial == None:
                    screenshot_path = take_screenshot()
                    selecao_filial = find_target_position(
                        screenshot_path, "Grupo", 0, -50, attempts=15
                    )
                    console.print(
                        f"Selecao filial localização de texto: {selecao_filial}"
                    )
                    if selecao_filial == None:
                        selecao_filial = (700, 639)
                        console.print(f"Selecao filial posição fixa: {selecao_filial}")

                    pyautogui.click(selecao_filial)
                    try:
                        if not filial_origem:
                            console.print(
                                f"Escrevendo [{task.configEntrada.get("filialEmpresaOrigem", "N/A")}] no campo filial..."
                            )
                            pyautogui.write(
                                task.configEntrada.get("filialEmpresaOrigem")
                                or task.configEntrada.get("codigoEmpresa")
                            )
                        else:
                            console.print(
                                f"Escrevendo [{filial_origem}] no campo filial..."
                            )
                            pyautogui.write(filial_origem)
                    except Exception as error:
                        console.print(f"Error: {error}")
                        console.print(
                            f"Escrevendo [{task.configEntrada.get("codigoEmpresa", "N/A")}] no campo filial..."
                        )
                        pyautogui.write(task.configEntrada.get("codigoEmpresa"))

                else:
                    if not filial_origem:
                        console.print(
                            f"Escrevendo [{task.configEntrada.get("filialEmpresaOrigem", "N/A")}] no campo filial..."
                        )
                        type_text_into_field(
                            task.configEntrada.get("filialEmpresaOrigem")
                            or task.configEntrada.get("codigoEmpresa"),
                            app["Seleção de Empresas"]["Edit"],
                            True,
                            "50",
                        )
                    else:
                        console.print(
                            f"Escrevendo [{filial_origem}] no campo filial..."
                        )
                        type_text_into_field(
                            filial_origem,
                            app["Seleção de Empresas"]["Edit"],
                            True,
                            "50",
                        )

                pyautogui.press("enter")

                button_logout = await find_element_center(
                    "assets/emsys/button_logout.png", (0, 0, 130, 150), 60
                )

                if button_logout:
                    console.print("Login realizado com sucesso.", style="bold green")
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno="Logou com sucesso no emsys!",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )

        else:
            log_msg = "Elemento de login não está pronto."
            logger.info(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Falha ao logar no EMSys!",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    else:
        screen_width, screen_height = pyautogui.size()
        log_msg = f"A tela de login não foi encontrada. Resolução atual: {screen_width}x{screen_height}."
        logger.info(log_msg)
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def api_simplifica(
    urlSimplifica: str,
    status: str,
    observacao: str,
    uuidsimplifica: str,
    numero_nota: str,
    valor_nota: str,
) -> None:
    """
    Envia notificacao para o simplifica com status e observacao.

    Args:
    urlSimplifica (str): URL do endpoint do simplifica.
    status (str): Status da notificacao.
    observacao (str): Observacao da notificacao.
    uuidsimplifica (str): UUID da notificacao.
    numero_nota (str): Numero da nota.
    valor_nota (str): Valor da nota.
    """
    if not urlSimplifica:
        raise ValueError("URL do endpoint do simplifica esta vazia.")

    if not status:
        raise ValueError("Status da notificacao esta vazio.")

    if not observacao:
        raise ValueError("Observacao da notificacao esta vazia.")

    if not uuidsimplifica:
        raise ValueError("UUID da notificacao esta vazio.")

    data = {
        "uuid_simplifica": uuidsimplifica,
        "status": status,
        "numero_nota": numero_nota,
        "observacao": observacao,
        "valor_nota": valor_nota,
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=True)
        ) as session:
            async with session.post(f"{urlSimplifica}", data=data) as response:
                if response.status != 200:
                    raise Exception(f"Erro ao enviar notificacao: {response.text()}")

                data = await response.text()
                log_msg = f"\nSucesso ao enviar {data}\n para o simplifica"
                console.print(
                    log_msg,
                    style="bold green",
                )
                logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do Simplifica: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.info(err_msg)


def add_start_on_boot_to_registry():
    import winreg as reg

    try:
        # Caminho para a chave Run
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Nome da chave
        key_name = "worker-startup"

        # Caminho para o executável no diretório atual
        directory_value = os.path.join(os.getcwd(), "worker-startup.bat")

        # Acessar a chave de registro
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE
        )

        # Adicionar ou modificar o valor
        reg.SetValueEx(registry_key, key_name, 0, reg.REG_SZ, directory_value)

        # Fechar a chave de registro
        reg.CloseKey(registry_key)

        log_msg = f"Chave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao adicionar ao registro: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def create_worker_bat():
    try:
        # Caminho do diretório atual
        current_dir = os.getcwd()
        nome_arquivo = "worker-startup.bat"

        # Conteúdo do arquivo
        # cd %USERPROFILE%
        bat_content = f"""@echo off
cd {current_dir}   
pipx install worker-automate-hub --force     
start /min "" "worker" "run" "--assets"
"""

        # Caminho completo para o arquivo
        bat_file_path = os.path.join(current_dir, nome_arquivo)

        # Escrevendo o conteúdo no arquivo
        with open(bat_file_path, "w") as file:
            file.write(bat_content.strip())

        log_msg = f"Arquivo {nome_arquivo} criado com sucesso em {bat_file_path}!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao criar o arquivo {nome_arquivo}: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def take_screenshot() -> Path:
    """
    Tira um screenshot da tela atual e salva em um arquivo com o nome
    especificado e a data/hora atual.

    :return: caminho do arquivo de screenshot gerado
    :rtype: str
    """
    if not Path.cwd().exists():
        raise FileNotFoundError("O caminho atual nao existe.")

    screenshot_path = Path.cwd() / "temp" / "screenshot.png"

    if not screenshot_path.parent.exists():
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
    except Exception as e:
        raise Exception("Erro ao tirar screenshot") from e

    if not screenshot_path.exists():
        raise FileNotFoundError("O arquivo de screenshot nao foi gerado")

    return screenshot_path


def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(str(image_path))

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold binário
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Remover ruído com medianBlur
    denoised_image = cv2.medianBlur(binary_image, 3)

    # Aumentar o contraste
    contrast_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)

    return contrast_image


def take_target_position(
    screenshot_path: Path, target_text: str, vertical=0, horizontal=0
) -> tuple | None:

    selected_image = Image.open(screenshot_path).convert("L")

    # Configurações do pytesseract
    # custom_config = r'--oem 3 --psm 6'

    # Extrair dados do texto usando pytesseract
    text_data = pytesseract.image_to_data(
        selected_image,
        output_type=pytesseract.Output.DICT,
        lang="por",  # , config=custom_config
    )

    # Identificar a posição do texto desejado
    field_center = None
    for i, text in enumerate(text_data["text"]):
        if len(text) > 0:
            if target_text.lower() in str(text).lower():
                x = text_data["left"][i]
                y = text_data["top"][i]
                w = text_data["width"][i]
                h = text_data["height"][i]
                # Centralizando nas coordenadas do campo
                field_center = (x + w // 2, y + h // 2)
                break

    # Aplicar as modificações de posição
    if field_center:
        field_center = (field_center[0] + horizontal, field_center[1] + vertical)

    return field_center


def find_target_position(
    screenshot_path: Path,
    target_text: str,
    vertical_pos: int = 0,
    horizontal_pos: int = 0,
    attempts: int = 5,
) -> tuple | None:
    """
    Encontra a posição de um campo na tela com base em uma imagem de screenshot.

    Args:
        screenshot_path (Path): Caminho para a imagem de screenshot.
        target_text (str): Texto do campo a ser encontrado.
        vertical_pos (int, optional): Posição vertical do campo. Defaults to 0.
        horizontal_pos (int, optional): Posição horizontal do campo. Defaults to 0.
        attempts (int, optional): Número de tentativas. Defaults to 5.

    Returns:
        tuple | None: Posição do campo encontrada ou None.
    """
    if screenshot_path is None:
        raise ValueError("screenshot_path não pode ser nulo")

    if not screenshot_path.exists():
        raise FileNotFoundError(f"O arquivo {screenshot_path} não existe")

    if target_text is None or len(target_text.strip()) == 0:
        raise ValueError("target_text não pode ser nulo ou vazio")

    attempt = 0
    target_pos = None

    while attempt < attempts:
        target_pos = take_target_position(
            screenshot_path,
            target_text,
            vertical=vertical_pos,
            horizontal=horizontal_pos,
        )
        console.print(f"Tentativa {attempt + 1} - Posição: {target_pos}")
        if target_pos is not None:
            log_msg = (
                f"Posição do campo [{target_text}] encontrada na tentativa [{attempt + 1}], "
                f"com valor de: {target_pos}"
            )
            console.print(log_msg, style="green")
            logger.info(log_msg)
            return target_pos

        attempt += 1

    # Caso não tenha encontrado após todas as tentativas
    log_msg = f"Não foi possível encontrar o campo [{target_text}] em [{attempts}] tentativas!"
    console.print(log_msg, style="red")

    return None


def select_model_capa() -> RpaRetornoProcessoDTO:
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Documento", 0, 140, 5)
    if field == None:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno="Não foi possivel encontrar o campo 'Documento'",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    pyautogui.click(field)
    pyautogui.write("Nfe")
    pyautogui.hotkey("enter")
    # Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
    while True:
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "Documento", 0, 140, 5)
        if field is None:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel encontrar o campo 'Documento'",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        pyautogui.click(field)
        worker_sleep(1)
        pyautogui.write("Nfe")
        pyautogui.hotkey("enter")
        # Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
        while True:
            screenshot_path = take_screenshot()
            field_doc = find_target_position(screenshot_path, "77", 0, 140, 5)
            if field_doc is not None:
                break
            else:
                pyautogui.click(field)
                pyautogui.hotkey("enter")
                pyautogui.hotkey("down")
                pyautogui.hotkey("enter")
                pyautogui.hotkey("tab")
                worker_sleep(2)

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Modelo Selecionado",
            status=RpaHistoricoStatusEnum.Sucesso,
        )


async def download_xml(
    google_drive_folder_id: str,
    get_gcp_token: RpaConfiguracao,
    get_gcp_credentials: RpaConfiguracao,
    chave_nota: str,
) -> RpaRetornoProcessoDTO:
    """
    Baixa um arquivo xml do Google Drive com base em um ID de pasta e um nome de arquivo.

    Args:
        google_drive_folder_id (str): ID da pasta do Google Drive.
        get_gcp_token (RpaConfiguracao): Configurações para obter o token do GCP.
        get_gcp_credentials (RpaConfiguracao): Configurações para obter as credenciais do GCP.
        chave_nota (str): Chave da nota para buscar o arquivo xml.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto RpaRetornoProcessoDTO com o resultado da execução do processo.
    """
    try:
        console.print("Verificando a existência do arquivo no Google Drive...\n")
        chave_nota = f"{chave_nota}.xml"
        gcp_credencial = GetCredsGworkspace(
            token_dict=get_gcp_token.conConfiguracao,
            credentials_dict=get_gcp_credentials.conConfiguracao,
        )
        creds = gcp_credencial.get_creds_gworkspace()

        if not creds:
            console.print(f"Erro ao obter autenticação para o GCP...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao obter autenticação para o GCP",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Inicializando o serviço do Google Drive
        drive_service = build("drive", "v3", credentials=creds)

        # Query para procurar o arquivo com o nome da chave da nota
        query = (
            f"'{google_drive_folder_id}' in parents and name contains '{chave_nota}'"
        )
        results = (
            drive_service.files()
            .list(
                q=query,
                pageSize=10,  # Reduzindo o número de resultados
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                fields="files(id, name)",
            )
            .execute()
        )

        # Verificando se o arquivo foi encontrado
        items = results.get("files", [])

        if not items:
            console.print(f"Nenhum arquivo com o nome {chave_nota} foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nenhum arquivo com o nome {chave_nota} foi encontrado no Google Drive",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Pegando o primeiro arquivo encontrado
        file_id = items[0]["id"]
        file_name = items[0]["name"]
        console.print(f"Arquivo {file_name} encontrado. Iniciando o download...\n")

        # Definindo o caminho local para salvar o arquivo
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

        # Iniciando o download
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            console.print(f"Download {int(status.progress() * 100)}% concluído.")

        console.print(
            f"Arquivo {file_name} baixado com sucesso e salvo em {file_path}.\n"
        )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Arquivo {file_name} baixado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        console.print(f"Erro ao baixar o arquivo do Google Drive, erro: {e}...\n")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao baixar o arquivo do Google Drive, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def get_xml_outras_empresas() -> RpaRetornoProcessoDTO:
    """
    Função para recuperar o XML da NF-e.

    Returns:
    - None
    """

    console.print("Verificando a existencia da tela de importação do XML... \n")
    app = Application().connect(title="Selecione a forma de obter o XML da NF-e")
    main_window = app["Selecione a forma de obter o XML da NF-e"]

    # Verificando se a janela principal existe
    if main_window.exists():
        console.print("Janela principal encontrada com sucesso... \n")
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Janela principal de importação do XML não foi encontrada.",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    console.print("Selecionando Notas de outras empresas... \n")
    arquivo_xml_button = main_window.child_window(title="Notas de Outras Empresas")
    if arquivo_xml_button.exists() and arquivo_xml_button.is_enabled():
        arquivo_xml_button.click()
        console.print("Notas de outras empresas XML selecionado com sucesso... \n")
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Botão Notas de outras empresas não foi encontrado.",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    await worker_sleep(3)

    console.print("Verificando se o botão OK existe ... \n")
    ok_button = main_window.child_window(title="OK", class_name="TBitBtn")
    if ok_button.exists() and ok_button.is_enabled():
        max_attempts = 3
        i = 0
        for i in range(max_attempts):
            console.print("Clicando em OK... \n")
            try:
                ok_button.click()
                console.print("Botão OK clicado com sucesso... \n")
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")
                continue

            await worker_sleep(3)

            console.print("Verificando a existência da tela para importar o XML...\n")
            try:
                app = Application().connect(class_name="TFrmImportarNotaOutraEmpresa")
                main_window = app["TFrmImportarNotaOutraEmpresa"]
                console.print(
                    "A tela de Importar Nota de Outra Empresa foi encontrada!"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"A tela de Importar Nota de Outra Empresa foi encontrada!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            except Exception as e:
                console.print(
                    f"Tela de importação não encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Número máximo de tentativas atingido. A tela para importar o Nota de Outra Empresa não foi encontrada.",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    else:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro - Botão OK não foi encontrado para acessar Notas de outras empresas.",
        )


async def get_xml(xml_file: str) -> None:
    """
    Função para recuperar o XML da NF-e.

    Args:
    - xml_file (str): Nome do arquivo do XML da NF-e sem a extensão .xml

    Returns:
    - None
    """

    try:
        console.print("Verificando a existencia da tela de importação do XML... \n")
        app = Application().connect(title="Selecione a forma de obter o XML da NF-e")
        main_window = app["Selecione a forma de obter o XML da NF-e"]

        # Verificando se a janela principal existe
        if main_window.exists():
            console.print("Janela principal encontrada com sucesso... \n")
        else:
            raise Exception("Janela principal de importação do XML não foi encontrada.")

        console.print("Selecionando Arquivo XML para seguir com a importação... \n")
        arquivo_xml_button = main_window.child_window(title="Arquivo XML")
        if arquivo_xml_button.exists() and arquivo_xml_button.is_enabled():
            arquivo_xml_button.click()
            console.print("Arquivo XML selecionado com sucesso... \n")
        else:
            raise Exception("Botão Arquivo XML não foi encontrado.")

        await worker_sleep(3)

        console.print("Verificando se o botão OK existe ... \n")
        ok_button = main_window.child_window(title="OK", class_name="TBitBtn")
        if ok_button.exists() and ok_button.is_enabled():
            max_attempts = 3
            i = 0
            while i < max_attempts:
                console.print("Clicando em OK... \n")
                try:
                    ok_button.click()
                    console.print("Botão OK clicado com sucesso... \n")
                except:
                    console.print("Não foi possivel clicar no Botão OK... \n")

                await worker_sleep(3)

                console.print(
                    "Verificando a existência da tela para importar o XML...\n"
                )
                try:
                    app = Application().connect(title="Abrir")
                    main_window = app["Abrir"]
                    console.print("A tela de importação foi encontrada!")
                    break
                except Exception as e:
                    console.print(
                        f"Tela de importação não encontrada. Tentativa {i + 1}/{max_attempts}."
                    )

                i += 1

            if i == max_attempts:
                raise Exception(
                    "Número máximo de tentativas atingido. A tela para importar o XML não foi encontrada."
                )

        else:
            raise Exception("Botão OK não foi encontrado.")

        await worker_sleep(10)

        console.print("Conectando na tela de importação do XML...\n")
        app = Application().connect(title="Abrir")
        main_window = app["Abrir"]

        # Verificando se a janela principal existe
        if main_window.exists():
            console.print("Janela para importar o xml encontrada com sucesso... \n")
        else:
            raise Exception("Janela para importar o xml não foi encontrada.")

        console.print("Carregando informações do XML a ser importado...\n")
        username = getpass.getuser()
        xml_name = f"{xml_file}.xml"
        path_to_xml = f"C:\\Users\\{username}\\Downloads\\{xml_name}"
        console.print("Inserindo caminho do XML...\n")
        main_window.type_keys("%n")
        await worker_sleep(2)
        pyautogui.write(path_to_xml)
        await worker_sleep(2)
        main_window.type_keys("%a")
        await worker_sleep(2)
    except Exception as error:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao obter XML: {error}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def delete_xml(nfe_key: str) -> None:
    """
    Deleta o arquivo xml referente a nota fiscal eletrônica informada.

    Args:
    nfe_key (str): Chave da nota fiscal eletrônica a ser deletada.

    Returns:
    None
    """
    try:
        if not nfe_key:
            raise ValueError("nfe_key não pode ser nulo ou vazio")

        xml_filename = f"{nfe_key}.xml"
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(download_folder, xml_filename)

        if not os.path.exists(file_path):
            console.print(
                f"Arquivo {xml_filename} não encontrado em {download_folder}.",
                style="bold yellow",
            )
            return

        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} não é um arquivo")

        os.remove(file_path)
        console.print(
            f"Arquivo {xml_filename} deletado com sucesso.", style="bold green"
        )
    except Exception as e:
        console.print(
            f"Erro ao deletar o arquivo {xml_filename}: {str(e)}", style="bold red"
        )
        raise Exception(f"Erro ao deletar o arquivo {xml_filename}: {str(e)}") from e


def config_natureza():
    """
    Configura a natureza da nota fiscal no EMSys.

    Clica no campo Natureza, escreve "16", pressiona a tecla down sete vezes e pressiona enter.
    """
    pyautogui.click(869, 370)
    worker_sleep(1)
    pyautogui.write("16")
    worker_sleep(1)
    pyautogui.press("down", presses=7)
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)


def config_almoxarifado(cod_almoxarifado: str) -> None:
    """
    Configura o almoxarifado da nota fiscal no EMSys.

    Clica no campo Almoxarifado, escreve o código do almoxarifado, pressiona a tecla tab e clica em OK.

    :param cod_almoxarifado: Código do almoxarifado.
    :type cod_almoxarifado: str
    :return: None
    :rtype: None
    """
    pyautogui.click(841, 390)
    worker_sleep(1)
    pyautogui.write(cod_almoxarifado)
    worker_sleep(1)
    pyautogui.press("tab")
    worker_sleep(1)
    pyautogui.click(1099, 727)


def check_itens_nota():
    """
    Verifica se os itens da nota fiscal foram cadastrados.

    Clica no botão "Itens" na tela de Nota Fiscal de Entrada e espera 1 segundo.
    Em seguida, clica no botão "OK" na tela de Itens da Nota Fiscal e espera 1 segundo.

    :return: None
    :rtype: None
    """
    pyautogui.click(631, 343)
    worker_sleep(1)
    pyautogui.click(626, 545)
    worker_sleep(1)


def check_pagamento():
    """
    Verifica se o pagamento foi realizado.

    Clica no botão "Pagamento" na tela de Nota Fiscal de Entrada, espera 1 segundo, clica no botão "OK" na tela de Pagamento, espera 1 segundo, escreve "ba" e pressiona a tecla Enter.

    :return: None
    :rtype: None
    """
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(878, 544)
    worker_sleep(1)
    pyautogui.write("ba")
    worker_sleep(1)
    pyautogui.hotkey("enter")
    worker_sleep(1)


def check_pagamento_transferencia_cd():
    pyautogui.click(623, 374)
    worker_sleep(1)
    pyautogui.click(916, 349)
    worker_sleep(1)
    pyautogui.press("down", presses=19)
    worker_sleep(1)
    pyautogui.hotkey("enter")


def preencher_valor_restante(restante):
    pyautogui.click(1284, 351)
    worker_sleep(1)
    pyautogui.write(restante)
    worker_sleep(1)


async def incluir_registro():
    pyautogui.click(594, 297)
    await worker_sleep(30)
    # pyautogui.click(1225, 635)
    # worker_sleep(30)
    # pyautogui.click(959, 564)


def finalizar_importacao():
    """
    Finaliza a importacao de notas no EMSys.

    Clica no botao "Finalizar" na tela de Importacao de Notas e pressiona a tecla enter.

    :return: None
    :rtype: None
    """
    pyautogui.click(597, 299)
    worker_sleep(1)
    pyautogui.hotkey("enter")


async def importar_notas_outras_empresas(data_emissao, numero_nota, empresa=None):
    try:
        # Digita empresa
        data_emissao = data_emissao.replace("/", "")
        if empresa is not None:
            pyautogui.write(empresa)
        else:
            pyautogui.write("171")
        await worker_sleep(1)
        # Digita datas
        pyautogui.click(768, 428)
        await worker_sleep(1)
        pyautogui.write(data_emissao)
        await worker_sleep(1)
        pyautogui.click(859, 430)
        await worker_sleep(1)
        pyautogui.write(data_emissao)
        await worker_sleep(1)
        # Clica Campo 'Num:'"
        pyautogui.click(1014, 428)
        pyautogui.write(numero_nota)
        await worker_sleep(1)
        # Click pesquisar
        pyautogui.click(1190, 428)
        await worker_sleep(20)
        # Click em importar
        pyautogui.click(1207, 684)
        await worker_sleep(20)
        return True
    except Exception as e:
        print(f"Erro ao importar nota: {e}")
        return False


def digitar_datas_emissao(data_emissao: str) -> None:
    """
    Digita as datas de emissão na tela de notas.

    Encontra as posições dos campos 'Data de emissão' e 'Data de emissão fim' na tela
    e digita a data informada.

    :param data_emissao: Data de emissão no formato 'DDMMYYYY'
    :type data_emissao: str
    :raises Exception: Caso não consiga encontrar os campos 'Data de emissão' ou 'Data de emissão fim'
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "emissão", 0, 40, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Data de emissão'")
    pyautogui.click(field)
    pyautogui.write(data_emissao)

    field = find_target_position(screenshot_path, "a", 0, 40, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Data de emissão fim'")
    pyautogui.click(field)
    pyautogui.write(data_emissao)


async def import_nfe() -> RpaRetornoProcessoDTO:
    """
    Função que clica no botão 'Importar NF-e' no sistema EMsys.

    Retorna um objeto RpaRetornoProcessoDTO com o status do processo.
    Se o botão for encontrado e clicado com sucesso, o status será 'Sucesso'.
    Caso contrário, o status será 'Falha'.

    :return: RpaRetornoProcessoDTO
    """
    await worker_sleep(2)
    console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")

    try:
        importar_nfe = pyautogui.locateOnScreen(
            ASSETS_PATH + "\\entrada_notas\\ImportarNF-e.png", confidence=0.7
        )
        if importar_nfe:
            pyautogui.click(importar_nfe)
            await worker_sleep(8)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Clicou Importar nfe",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel localizar o campo 'Importar NF-e' ",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
    except:
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]
        tpanel = main_window.child_window(class_name="TPanel")
        tpanel.set_focus()
        await worker_sleep(2)

        # Coordernadas relativa a Janela de Notas de entrada e ao filho TPainel
        x_start = 515
        y_start = 1
        x_end = 620
        y_end = 37

        absolute_x = x_start + tpanel.rectangle().left + (x_end - x_start) // 2
        absolute_y = y_start + tpanel.rectangle().top + (y_end - y_start) // 2
        pyautogui.click(absolute_x, absolute_y)
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Clicou Importar nfe",
            status=RpaHistoricoStatusEnum.Sucesso,
        )


def digitar_numero_nota(numero_nota: str) -> None:
    """
    Digita o numero da nota no campo 'Núm Nota' e clica em 'Pesquisar'

    :param numero_nota: Numero da nota a ser digitado
    :type numero_nota: str
    :raises Exception: Caso não consiga encontrar o campo 'Núm Nota' ou o botão 'Pesquisar'
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Núm", 0, 60, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o campo 'Núm Nota'")
    # pyautogui.click(field)
    pyautogui.write(numero_nota)
    console.log("Escreveu numero da nota", style="bold green")
    field = find_target_position(screenshot_path, "pesquisar", 0, 0, 15)
    if field == None:
        raise Exception("Não foi possivel encontrar o botão 'Pesquisar'")
    console.log("Clicando em pesquisar", style="bold green")
    pyautogui.click(field)


def select_nfe(nfe_type: str) -> bool:
    """
    Seleciona o tipo de nota fiscal no sistema.

    Args:
        nfe_type (str): Tipo de nota fiscal.

    Returns:
        bool: True se a seleção for feita com sucesso, False caso contrário.
    """
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, nfe_type, 0, 0, 15)
    if field is None:
        raise ValueError(f"Campo '{nfe_type}' não encontrado")

    pyautogui.click(field)

    return True


async def transmitir_nota(
    task: RpaProcessoEntradaDTO, nota_fiscal: str, valor_nota: str
) -> RpaRetornoProcessoDTO:
    """
    Função responsável por transmitir a nota fiscal.

    Args:
        task (RpaProcessoEntradaDTO): Objeto com as informações da nota.
        nota_fiscal (str): Número da nota fiscal.
        valor_nota (str): Valor da nota fiscal.

    Returns:
        RpaRetornoProcessoDTO: Um objeto com o resultado da transmissão da nota.
    """
    pyautogui.click(875, 596)
    logger.info("\nNota Transmitida")
    console.print("\nNota Transmitida", style="bold green")

    await worker_sleep(7)

    # Fechar transmitir nota
    console.print("Fechando a transmissão da nota...\n")

    pyautogui.click(957, 556)

    await worker_sleep(15)
    screenshot_path = take_screenshot()
    transmitir_fechar = find_target_position(screenshot_path, "fechar", attempts=15)
    if transmitir_fechar is not None:
        pyautogui.click(transmitir_fechar)
        log_msg = f"Nota Transmitida com sucesso"
        logger.info(log_msg)
        console.print(log_msg, style="bold green")
    else:
        log_msg = f"Nota não transmitida"
        logger.info(log_msg)
        console.print(log_msg, style="bold red")
        await api_simplifica(
            task.configEntrada.get("urlRetorno"),
            "ERRO",
            log_msg,
            task.configEntrada.get("uuidSimplifica"),
            nota_fiscal,
            valor_nota,
        )
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    return RpaRetornoProcessoDTO(
        sucesso=True,
        retorno="Nota transmitida com sucesso",
        status=RpaHistoricoStatusEnum.Sucesso,
    )


async def select_model_pre_venda(
    text_to_find: str, task: RpaProcessoEntradaDTO
) -> bool:
    """
    Procura se o campo de select ja possui a opção que você precisa selecionada,
    caso sim, retorna True, caso contrário, chama a função find_desired_model
    para selecionar o modelo desejado.

    Args:
        text_to_find (str): Texto a ser procurado no campo modelo
        task (RpaProcessoEntradaDTO): Processo em andamento

    Returns:
        bool: Se o modelo foi selecionado corretamente
    """
    if task is None:
        raise ValueError("task não pode ser nulo")
    if text_to_find is None or len(text_to_find.strip()) == 0:
        raise ValueError("text_to_find não pode ser nulo ou vazio")

    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field is None:
        return False
    else:
        return True


async def extract_value():
    # pyautogui.click(1304, 780)
    logger.info("Extrindo Valor da nota")
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.doubleClick(1304, 780, interval=0.3)
    pyautogui.hotkey("ctrl", "c")
    console.log(f"Valor nota copiado: {pyperclip.paste()}", style="bold green")
    valor_nota = pyperclip.paste()
    # valor_nota = re.findall(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', valor_nota)
    # print(valor_nota)
    logger.info(valor_nota)
    return valor_nota


async def extract_nf_number() -> str | None:
    """
    Extrai o numero da nota fiscal, baseado na posição do botão gerada na tela

    Returns:
        str: Numero da nota fiscal, None em caso de erro
    """
    logger.info("Extraindo Numero da nota")
    try:
        pyperclip.copy("")
        await asyncio.sleep(1)
        pyautogui.click(965, 515)
        await asyncio.sleep(5)
        pyautogui.hotkey("ctrl", "c")
        nota_fiscal = pyperclip.paste()
        nota_fiscal = re.findall(r"\d+-?\d*", nota_fiscal)
        if nota_fiscal is None or len(nota_fiscal) == 0:
            return ''
        logger.info(nota_fiscal)
        console.print(nota_fiscal)
        return nota_fiscal[0]
    except Exception as e:
        logger.error(f"Erro ao extrair o numero da nota fiscal: {e}")
        return None


async def find_desired_model(text_to_find: str, task: RpaProcessoEntradaDTO) -> bool:
    """
    Encontra o modelo da nota com base na query "get_index_modelo_emsys"

    Args:
        text_to_find (str): Texto a ser procurado no campo modelo
        task (RpaProcessoEntradaDTO): Processo em andamento

    Returns:
        bool: Se o modelo foi selecionado corretamente
    """
    try:
        from worker_automate_hub.api.client import get_index_modelo_emsys

        index = await get_index_modelo_emsys(
            task.configEntrada.get("filialEmpresaOrigem"), text_to_find
        )
        if index is None or index.get("indice") is None:
            raise Exception("Erro ao obter o índice do modelo")
        console.log(f"Indice do banco: {index.get('indice')}")
    except Exception as e:
        console.log(f"Erro ao obter o índice do modelo: {e}", style="bold red")
        return False

    # Se não achou clica no campo modelo e sobe ate a primeira opção
    modelo_select_position = (830, 268)
    pyautogui.click(modelo_select_position)
    # Sobe para o primeiro modelo disponivel
    pyautogui.hotkey("enter")
    pyautogui.press("up", presses=20, interval=0.1)
    try:
        indice: int = int(index.get("indice"))
    except Exception as e:
        console.log(
            f"Erro ao converter o índice do modelo para inteiro: {e}", style="bold red"
        )
        return False
    # Seleciona o modelo com base na query "get_index_modelo_emsys"
    pyautogui.press("down", presses=indice)
    pyautogui.hotkey("tab")

    await worker_sleep(3)
    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field:
        console.log("Selecionou Modelo da nota corretamente", style="bold green")
        return True
    else:
        console.log("Modelo não selecionado corretamente", style="bold red")
        return False


async def faturar_pre_venda(task: RpaProcessoEntradaDTO) -> dict:
    await worker_sleep(10)

    # Clica em Faturar
    app = Application().connect(class_name="TFrmPreVenda")
    main_window = app["TFrmPreVenda"]
    panel_window = main_window.child_window(class_name="TPage", found_index=0)
    btn_window = panel_window.child_window(class_name="TBitBtn", found_index=7)

    if btn_window.exists():
        try:
            btn_window.click()
            await worker_sleep(3)
            console.print("O botão Faturar foi clicado com sucesso.", style="green")
        except:
            console.print("Falha ao clicar no botão faturar.", style="red")
            return {"sucesso": False, "retorno": "Falha ao clicar no botão faturar."}
    else:
        console.print("O Botão Faturar não foi encontrado.", style="red")
        return {"sucesso": False, "retorno": "O Botão Faturar não foi encontrado."}

    await worker_sleep(20)

    # Alert
    try:
        app = Application().connect(class_name="TMessageForm")
        main_window = app["TMessageForm"]

        btn_yes = main_window["&Yes"]
        if btn_yes.exists():
            try:
                btn_yes.click()
                await worker_sleep(3)
                console.print(
                    "O botão Yes de Faturar foi clicado com sucesso.", style="green"
                )
            except:
                console.print("Falha ao clicar no botão Yes de faturar.", style="red")
                # return {"sucesso": False, "retorno": "Falha ao clicar no botão Yes de faturar."}
        else:
            console.print("O Botão Yes de Faturar não foi encontrado.", style="red")
            # return {"sucesso": False, "retorno": "O Botão Yes de Faturar não foi encontrado."}
    except:
        console.print("O Botão Yes de Faturar não foi encontrado.", style="red")

    await worker_sleep(2)
    console.print(f"Clicou em: 'Faturar'", style="bold green")

    await worker_sleep(10)

    # Aviso "Deseja faturar pré-venda?"
    button_yes = (918, 557)  # find_target_position(screenshot_path, "yes", attempts=15)
    pyautogui.click(button_yes)


    await worker_sleep(10)

    # Verifica se existe a mensagem de recalcular parcelas
    screenshot_path = take_screenshot()
    message_recalcular = find_target_position(screenshot_path, "Recalcular", attempts=5)
    # Se existir clica em nao
    if message_recalcular is not None:
        button_no = (
            999,
            560,
        )  # find_target_position(screenshot_path, "No", attempts=15)
        pyautogui.click(button_no)
        log_msg = "Clicou em 'No' na mensagem de recalcular parcelas"
        console.log(log_msg, style="bold green")
        logger.info(log_msg)
    else:
        log_msg = "A Mensagem de recalcular parcelas não existe"
        logger.info(log_msg)
        console.print(log_msg, style="bold yellow")

    await worker_sleep(8)

    # Seleciona Modelo
    console.log("Selecionando o modelo...\n", style="bold green")
    try:
        app = Application().connect(class_name="TFrmDadosFaturamentoPreVenda")
        main_window = app["TFrmDadosFaturamentoPreVenda"]

        combo_box_model = main_window.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        combo_box_model.click()

        await worker_sleep(3)
        set_combobox("||List", "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077")
        await worker_sleep(3)

    except Exception as e:

        err_msg = f"Falha ao selecionar o Modelo {e}"
        await api_simplifica(
            task.configEntrada.get("urlRetorno"),
            "ERRO",
            err_msg,
            task.configEntrada.get("uuidSimplifica"),
            None,
            None,
        )
        return {"sucesso": False, "retorno": err_msg}

    # Extrai total da Nota
    console.log("Obtendo o total da Nota...\n", style="bold green")
    valor_nota = await extract_value()
    console.print(f"\nValor NF: '{valor_nota}'", style="bold green")

    # Clicar no botao "OK" com um certo verde
    app = Application().connect(class_name="TFrmDadosFaturamentoPreVenda")
    main_window = app["TFrmDadosFaturamentoPreVenda"]
    btn_window = main_window.child_window(class_name="TBitBtn", found_index=1)

    if btn_window.exists():
        try:
            btn_window.click()
            await worker_sleep(3)
            console.print("O botão Ok verde foi clicado com sucesso.", style="green")
        except:
            console.print("Falha ao clicar no botão Ok verde.", style="red")
            return {"sucesso": False, "retorno": "Falha ao clicar no botão Ok verde."}
    else:
        console.print("O Botão Ok verde não foi encontrado.", style="red")
        return {"sucesso": False, "retorno": "O Botão Ok verde não foi encontrado."}

    await worker_sleep(15)

    # Alert de pré venda
    try:
        app = Application().connect(class_name="TMessageForm")
        main_window = app["TMessageForm"]

        btn_yes = main_window["&Yes"]
        if btn_yes.exists():
            try:
                btn_yes.click()
                await worker_sleep(3)
                console.print(
                    "O botão Yes de deseja faturar pré venda foi clicado com sucesso.",
                    style="green",
                )
            except:
                console.print(
                    "Falha ao clicar no botão Yes de deseja faturar pré venda.",
                    style="red",
                )
                return {
                    "sucesso": False,
                    "retorno": "Falha ao clicar no botão Yes de deseja faturar pré venda.",
                }
        else:
            console.print(
                "O Botão Yes de deseja faturar pré venda não foi encontrado.",
                style="red",
            )
            return {
                "sucesso": False,
                "retorno": "O Botão Yes de deseja faturar pré venda não foi encontrado.",
            }
    except:
        console.print(
            "O Botão Yes de deseja faturar pré venda não foi encontrado.", style="red"
        )
        return {
            "sucesso": False,
            "retorno": "O Botão Yes de deseja faturar pré venda não foi encontrado.",
        }

    return {
        "sucesso": True,
        "retorno": "Faturar pre venda concluído com sucesso!",
        "valor_nota": valor_nota,
    }


@repeat(times=10, delay=30)
async def wait_window_close(window_name):
    from pywinauto import Desktop

    desktop = Desktop(backend="uia")
    # Loop infinito para verificar continuamente a janela
    max_trys = 50
    current_try = 0
    while current_try <= max_trys:
        try:
            # Tenta localizar a janela com o título que contém "Aguarde"
            window = desktop.window(title_re=window_name)
            # Se a janela existe, continua monitorando
            if window.exists():
                console.print(f"Janela '{window_name}' ainda aberta", style="bold yellow")
                await worker_sleep(20)
                current_try += 1
            else:
                await worker_sleep(5)
                # console.print(
                #     f"Janela '{window_name}' foi fechada.", style="bold green"
                # )
                try:
                    window = desktop.window(title_re=window_name)
                    if window.exists():
                        console.print(
                            f"Janela '{window_name}' ainda aberta", style="bold yellow"
                        )
                        current_try += 1
                        continue
                except:
                    console.print(f"Janela '{window_name}' não existe mais.", style="bold green")
                    return  False
               
                return False  # Retorna falso pois a janela esta fechada
            await worker_sleep(30)  # Espera 2 (* o multiplicador) segundos antes de verificar novamente
            current_try += 1
        except Exception as e:
            console.print(f"Erro: {e}")
            return True




async def verify_nf_incuded() -> bool:
    """
    Verifica se a nota fiscal foi incluída com sucesso.

    Returns:
        bool: True se a nota foi incluída, False caso contrário
    """
    try:
        nota_incluida = pyautogui.locateOnScreen(
            ASSETS_PATH + "\\entrada_notas\\nota_fiscal_incluida.png", confidence=0.7
        )
        if nota_incluida:
            return True
        else:
            return False
            # pyautogui.click(959, 562)
    except Exception as e:
        console.print(f"Error: {e}")
        return False


async def rateio_window(nota: dict):
    """
    Abre a janela de rateio de nota e preenche todos os campos com base na nota informada.

    Args:
        nota (dict): Dicionario com as informacoes da nota.

    Raises:
        ValueError: Se a nota for nula.
        RuntimeError: Se nao for possivel encontrar o campo "todos" na tela.
        RuntimeError: Se nao for possivel converter o valor da nota para inteiro.
    """
    if nota is None:
        raise ValueError("Nota nao pode ser nula")

    screenshot_path = take_screenshot()

    # Clica em Selecionar todos
    field = find_target_position(screenshot_path, "todos", 0, 0, 15)
    if field is None:
        raise RuntimeError("Nao foi possivel encontrar o campo 'todos'")

    pyautogui.click(field)
    await worker_sleep(2)

    # Digita "Centro" 1000 + filialEmpresaOrigem
    pyautogui.click(788, 514)
    try:
        filial = 1000 + int(nota.get("filialEmpresaOrigem"))
    except TypeError:
        raise RuntimeError("Nao foi possivel converter o valor da nota para inteiro")
    pyautogui.write(str(filial))
    pyautogui.hotkey("tab")

    # Marca "Aplicar rateio aos itens selecionados"
    pyautogui.hotkey("space")
    pyautogui.hotkey("tab")

    # Digita % Rateio
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("del")
    pyautogui.write("100")

    # Clica Incluir registro
    pyautogui.click(1161, 548)
    await asyncio.sleep(20)

    # Clica OK
    pyautogui.click(1200, 683)
    await worker_sleep(5)


def check_screen_resolution():
    """
    Verifica se a resolução atual da tela é a recomendada.

    Imprime um aviso se a resolução atual for diferente da recomendada.
    """
    screen_width, screen_height = pyautogui.size()
    screen_width_recommended = 1280
    screen_height_recommended = 720

    if (
        screen_width != screen_width_recommended
        or screen_height != screen_height_recommended
    ):
        console.print(
            f"\nAviso: A resolução atual da tela é {screen_width}x{screen_height}. Recomendado: {screen_width_recommended}x{screen_height_recommended}. Podem ocorrer erros nos processos.\n",
            style="bold yellow",
        )
        logger.info(
            f"Aviso: A resolução atual da tela é {screen_width}x{screen_height}. Recomendado: {screen_width_recommended}x{screen_height_recommended}."
        )


async def capture_and_send_screenshot(uuidRelacao: str, desArquivo: str) -> None:
    """
    Função que captura uma screenshot da tela, salva em um buffer e a envia usando a função send_file.

    Args:
        uuidRelacao (str): UUID da relação associada ao arquivo.
        desArquivo (str): Descrição do arquivo.
        tipo (str): Tipo de arquivo (imagem, etc).
    """
    try:
        from worker_automate_hub.api.client import send_file

        # Tira a screenshot
        screenshot = pyautogui.screenshot()

        # Salva a screenshot em um buffer de memória em formato PNG
        screenshot_buffer = io.BytesIO()
        screenshot.save(screenshot_buffer, format="PNG")

        # Reseta o cursor do buffer para o início
        screenshot_buffer.seek(0)

        # Adiciona um timestamp ao nome do arquivo para evitar duplicatas
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desArquivo = f"{desArquivo}_{timestamp}.png"

        # Chama a função para enviar o arquivo
        await send_file(uuidRelacao, desArquivo, "img", screenshot_buffer.read())

    except Exception as e:
        err_msg = f"Erro ao capturar ou enviar a screenshot: {str(e)}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


async def read_xml_file(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespaces = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

        itens = []

        for item in root.findall(".//nfe:det", namespaces):
            prod = item.find("nfe:prod", namespaces)
            if prod is not None:
                codigo = (
                    prod.find("nfe:cProd", namespaces).text
                    if prod.find("nfe:cProd", namespaces) is not None
                    else None
                )
                descricao = (
                    prod.find("nfe:xProd", namespaces).text
                    if prod.find("nfe:xProd", namespaces) is not None
                    else None
                )
                quantidade = (
                    prod.find("nfe:qCom", namespaces).text
                    if prod.find("nfe:qCom", namespaces) is not None
                    else None
                )
                valor_unitario = (
                    prod.find("nfe:vUnCom", namespaces).text
                    if prod.find("nfe:vUnCom", namespaces) is not None
                    else None
                )
                n_item = item.attrib.get("nItem", None)

                itens.append(
                    {
                        "n_item": n_item,
                        "codigo": codigo,
                        "descricao": descricao,
                        "quantidade": quantidade,
                        "valor_unitario": valor_unitario,
                    }
                )

        return itens

    except FileNotFoundError:
        raise Exception(f"arquivo XML não encontrado")
    except ET.ParseError as e:
        raise Exception(f"Erro ao analisar o arquivo XML: {e}")
    except Exception as e:
        raise Exception(f"Ocorreu um erro: {e}")


async def extract_group_by_itens(itens):
    informacoes = []

    for item in itens:
        n_item = item["n_item"]
        descricao = item["descricao"]

        console.print(
            f"Tentando obter o formato no primeiro regex - item {descricao}.. \n"
        )
        try:
            match = re.search(r"\((\d+)X(\d+)(L|KG)?\)", descricao)
            formato = match.group(0) if match else None
        except Exception as e:
            console.print(
                f" Erro ao obter o regex no primeiro formato - item {descricao}, erro {e}.. \n"
            )
            formato = None

        if formato is None:
            try:
                match = re.search(r"(\d+X\d+(\w+))", descricao)
                formato = match.group(0) if match else None
            except Exception as e:
                console.print(
                    f" Erro ao obter o regex no segundo formato - item {descricao}, erro {e}.. \n"
                )
                formato = None

        if formato is not None:
            formato = formato.replace("(", "").replace(")", "")
        else:
            console.print(f"Formato não encontrado para o item {n_item}: {descricao}\n")

        informacoes.append(
            {"n_item": n_item, "formato": formato, "descricao": descricao}
        )

    return informacoes


async def select_documento_type(document_type: str) -> RpaRetornoProcessoDTO:
    """
    Função que seleciona o tipo de documento na janela de Nota Fiscal de Entrada.

    Args:
        document_type (str): Tipo de documento a ser selecionado.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto com informações sobre o status do processo.
    """
    try:
        app = Application().connect(class_name="TFrmNotaFiscalEntrada", timeout=60)
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        await worker_sleep(3)

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_tipo_documento = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        combo_box_tipo_documento.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )
        await worker_sleep(4)
        try:
            set_combobox("||List", document_type)
        except Exception as e:
            console.log(
                "Não foi possivel selecionar o tipo de documento via set combobox, realizando a alteração utilizando send keys"
            )
            combo_box_tipo_documento.click()
            await worker_sleep(2)
            pyautogui.write("N")
            await worker_sleep(1)
            pyautogui.hotkey("enter")
            await worker_sleep(2)

            max_try = 20
            i = 0
            while i <= max_try:
                combo_box_tipo_documento = panel_TTabSheet.child_window(
                    class_name="TDBIComboBox", found_index=1
                )
                document_type_selected = combo_box_tipo_documento.window_text()
                if document_type == document_type_selected:
                    break
                else:
                    pyautogui.press("down")
                    await worker_sleep(2)
                    i = i + 1

        combo_box_tipo_documento = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        document_type_selected = combo_box_tipo_documento.window_text()
        if document_type in document_type_selected:
            console.print(
                f"Tipo de documento '{document_type}', selecionado com sucesso...\n"
            )

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Documento {document_type} selecionado com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel selecionar o tipo do documento",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel selecionar o tipo do documento, erro: {e} ",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


class WindowStatus(TypedDict):
    IsOpened: bool
    Janela: str


async def is_window_open(window_title: str) -> WindowStatus:
    """
    Verifica se uma janela esta aberta atraves do titulo da janela.

    Args:
    - window_title (str): Titulo da janela

    Returns:
    - WindowStatus: Dicionario com a chave IsOpened e o valor bool e a chave Janela com o valor da janela
    """
    try:
        app = Application().connect(title=window_title)
        main_window = app[window_title]
        return WindowStatus(IsOpened=True, Janela=window_title)

    except findwindows.ElementNotFoundError:
        return WindowStatus(IsOpened=False, Janela=window_title)

    except Exception as e:
        raise ValueError(f"Erro ao verificar telas erros/warnings {e}")


async def is_window_open_by_class(window_class: str, app_class: str) -> WindowStatus:
    """
    Verifica se uma janela esta aberta atraves da classe da janela.

    Args:
    - window_class (str): Classe da janela
    - app_class (str): Classe do aplicativo

    Returns:
    - WindowStatus: Dicionario com a chave IsOpened e o valor bool e a chave Janela com o valor da janela
    """
    try:
        app = Application().connect(class_name=window_class)
        return WindowStatus(IsOpened=True, Janela=app_class)

    except findwindows.ElementNotFoundError:
        return WindowStatus(IsOpened=False, Janela=app_class)

    except Exception as e:
        raise ValueError(f"Erro ao verificar telas erros itens/warnings {e}")


async def warnings_after_xml_imported() -> RpaRetornoProcessoDTO:
    """
    Função responsável por verificar se existe um warning após a importação do xml,
    e clicar no botão NO para andamento do processo.

    :return: RpaRetornoProcessoDTO com o status e o retorno da operação.
    """
    console.print("Interagindo com a tela de warning após a importação do xml...\n")
    app = Application().connect(title="Warning")
    main_window = app["Warning"]

    console.print("Verificando se existe o botao NO, para andamento do processo...\n")
    # btn_no = main_window.child_window(title="&No")
    btn_no = main_window["&No"]

    if btn_no.exists():
        try:
            console.print("Clicando em NO, para andamento do processo...\n")
            btn_no.click()
            await worker_sleep(4)
            if main_window.exists():
                console.print(
                    "Verificando se existe um segundo botao NO, para andamento do processo...\n"
                )
                btn_no = main_window["&No"]
                # btn_no = main_window.child_window(title="&No")
                console.print("Clicando novamente em NO")
                btn_no.click()
                await worker_sleep(5)
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para clicar em NO",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

            else:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para clicar em NO",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

        except Exception as e:
            console.print(f"Erro ao clicar em NO: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Warning: Erro ao clicar em NO: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    else:
        console.print("Warning - Erro após a importação do arquivo...\n")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno="Warning - Erro após a importação do arquivo, não foi encontrado o botão No para andamento do processo... \n",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def error_after_xml_imported() -> RpaRetornoProcessoDTO:
    await worker_sleep(3)
    """
    Função responsável por verificar se existe um erro após a importação do xml,
    e capturar a mensagem de erro para posterior log.

    :return: RpaRetornoProcessoDTO com o status e o retorno da operação.
    """
    console.print("Interagindo com a tela de erro após a importação do xml...\n")
    app = Application().connect(title="Erro")
    main_window = app["Erro"]
    await worker_sleep(7)
    all_controls_from_error = main_window.children()
    capturar_proxima_mensagem = False
    console.print("Obtendo mensagem de erro mapeada...\n")

    for control in all_controls_from_error:
        control_text = control.window_text()
        console.print(f"control text: {control_text}")

        if "Mensagem do Banco de Dados" in control_text:
            capturar_proxima_mensagem = True

        elif capturar_proxima_mensagem:
            if "duplicate key" in control_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Não foi possivel seguir devido ao numero da chave ja existir no banco de dados, erro: {control_text}... \n",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            elif "ja lancada" in control_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop-up nota incluida encontrada, porém nota encontrada como 'já lançada' trazendo as seguintes informações: {control_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            elif "de despesa" in control_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Tipo de despesa não informada: {control_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            elif "deadlock" in control_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro de deadlock: {control_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro do banco de dados: {control_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

        elif "xml" in control_text.lower():
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota descartada: {control_text}... \n",
                status=RpaHistoricoStatusEnum.Descartado,
            )

        elif "XML já foi importado anteriormente" in control_text:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota descartada: {control_text}... \n",
                status=RpaHistoricoStatusEnum.Descartado,
            )


async def error_before_persist_record() -> RpaRetornoProcessoDTO:
    try:
        console.print(
            "Interagindo com a tela de erro após clicar em incluir registro...\n"
        )
        app = Application().connect(title="Information")
        main_window = app["Erro"]
        await worker_sleep(7)
        all_controls_from_error = main_window.children()
        capturar_proxima_mensagem = False
        console.print("Obtendo mensagem de erro mapeada...\n")

        for control in all_controls_from_error:
            control_text = control.window_text()

            if "que a data de entrada" in control_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao incluir registro, As datas das parcelas não podem ser menores que a data de entrada da nota: {control_text} \n",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            elif capturar_proxima_mensagem:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao incluir registro: {control_text} \n",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
    except:
        console.print("Erro ao capturar mensagem de erro")


async def itens_not_found_supplier(xml: str) -> RpaRetornoProcessoDTO:
    try:
        username = getpass.getuser()
        console.print("Verificando se existe tela de multiplas referencias.\n")
        await worker_sleep(10)

        itens_fornecedor = await is_window_open_by_class(
            "TFrmSelecionaItensFornecedor", "TFrmSelecionaItensFornecedor"
        )

        if itens_fornecedor["IsOpened"] == True:
            console.print("Tela de multiplas referencias existe.\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Tela de Itens fornecedor - Multiplas referencias",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        console.print("Iteragindo com a tela de itens não localizados // NCM ...\n")

        app = Application().connect(class_name="TFrmAguarde", timeout=60)

        max_attempts = 60
        i = 0

        while i < max_attempts:
            try:
                main_window = app["TMessageForm"]
                console.print("Janela 'TMessageForm' encontrada!")
                break
            except Exception as e:
                console.print(f"Erro ao tentar acessar TMessageForm: {e}")
                janela_aguarde = await is_window_open_by_class(
                    "TFrmAguarde", "TFrmAguarde"
                )
                if janela_aguarde["IsOpened"] == True:
                    console.print(
                        "Aguardando tela de aguarde desaparecer ou conectar...\n"
                    )
                else:
                    try:
                        main_window = app["TMessageForm"]
                        if main_window.exists():
                            console.print("Janela 'TMessageForm' encontrada!")
                            break
                    except:
                        return RpaRetornoProcessoDTO(
                            sucesso=True,
                            retorno="Tela de aguardar carregada - Seguindo com andamento do processo (NCM).",
                            status=RpaHistoricoStatusEnum.Sucesso,
                        )

            await worker_sleep(3)
            i += 1

        window_title = main_window.window_text()

        if "Confirm" in window_title or "Seleciona Itens Fornecedor" in window_title:
            console.print("Itens nao localizados para o fornecedor...\n")
            if main_window.exists():
                main_window.type_keys("%n")
                await worker_sleep(10)

                console.print(
                    "Verificando a existencia de tela de selecionar Itens...\n"
                )
                itens_fornecedor = await is_window_open_by_class(
                    "TFrmSelecionaItensFornecedor", "TFrmSelecionaItensFornecedor"
                )

                if itens_fornecedor["IsOpened"] == True:
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno="Tela de Itens fornecedor - Multiplas referencias",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
                else:
                    console.print(
                        "Não possui a existencia de tela de selecionar Itens Fornecedor...\n"
                    )

                await worker_sleep(10)
                console.print("Verificando a existe da tela dos itens com erro...\n")

                max_attempts = 60
                i = 0
                while i < max_attempts:
                    logs_erro = await is_window_open_by_class(
                        "TFrmExibeLogErroImportacaoNfe", "TFrmExibeLogErroImportacaoNfe"
                    )
                    if logs_erro["IsOpened"] == True:
                        break
                    else:
                        console.print(
                            "Aguardando confirmação de tela de erro importação NFe...\n"
                        )
                        try:
                            app = Application().connect(class_name="TFrmAguarde")
                            main_window = app["TMessageForm"]
                            console.print("Janela 'Information' encontrada!")
                            window_title = main_window.window_text()
                            if "Information" in window_title:
                                main_window.type_keys("%n")
                            else:
                                console.print(
                                    "Não possui a existencia de 'Information'...\n"
                                )
                        except:
                            console.print(
                                "Não possui a existencia de tela de Information...\n"
                            )
                        await worker_sleep(5)
                        i += 1

                await worker_sleep(5)
                logs_erro = await is_window_open_by_class(
                    "TFrmExibeLogErroImportacaoNfe", "TFrmExibeLogErroImportacaoNfe"
                )
                if logs_erro["IsOpened"] == True:
                    app = Application().connect(
                        class_name="TFrmExibeLogErroImportacaoNfe"
                    )
                    main_window = app["TFrmExibeLogErroImportacaoNfe"]
                    console.print(
                        "Tela com itens com erro existe, salvando os itens...\n"
                    )

                    btn_save = main_window.child_window(
                        title="Salvar", class_name="TBitBtn"
                    )

                    if btn_save.exists():
                        max_attempts = 3
                        i = 0
                        while i < max_attempts:
                            console.print("Clicando no botão de salvar...\n")
                            try:
                                btn_save.click()
                            except:
                                console.print(
                                    "Não foi possivel clicar no Botão OK... \n"
                                )
                            await worker_sleep(3)

                            console.print(
                                "Verificando a existencia da tela 'Salvar'...\n"
                            )
                            try:
                                app = Application().connect(title="Salvar")
                                main_window = app["Salvar"]
                                console.print("Tela 'Salvar' encontrada!")
                                break
                            except Exception as e:
                                console.print(
                                    f"Tela 'Salvar' não encontrada. Tentativa {i + 1}/{max_attempts}."
                                )
                            i += 1

                        if i == max_attempts:
                            return RpaRetornoProcessoDTO(
                                sucesso=False,
                                retorno="Número máximo de tentativas ao tentar conectar à tela 'Salvar'.",
                                status=RpaHistoricoStatusEnum.Falha,
                                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                            )

                        await worker_sleep(4)
                        console.print("Interagindo com a tela 'Salvar'...\n")
                        path_to_txt = (
                            f"C:\\Users\\{username}\\Downloads\\erro_itens{xml}.txt"
                        )

                        main_window.type_keys("%n")
                        pyautogui.write(path_to_txt)
                        await worker_sleep(1)
                        main_window.type_keys("%l")
                        console.print("Arquivo salvo com sucesso...\n")

                        await worker_sleep(3)
                        with open(
                            path_to_txt, "r", encoding="latin1", errors="replace"
                        ) as arquivo:
                            conteudo = arquivo.read()
                            console.print(
                                f"Arquivo salvo com sucesso, itens com erro {conteudo}...\n"
                            )

                        os.remove(path_to_txt)
                        console.print("Removendo o arquivo...\n")

                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Itens nao localizados p/ fornecedor. Mensagem: {conteudo}",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                        )
                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Botao Salvar - Não foi encontrado",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Tela 'TFrmExibeLogErroImportacaoNfe' não encontrada, tentar novamente...",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro não mapeado, pop-up Confirm não encontrado...",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

        elif "Information" in window_title:
            console.print("Tela de NCM para o fornecedor...\n")
            if main_window.exists():
                console.print("Tela de NCM, clicando em NO para prosseguir...\n")
                main_window.type_keys("%n")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Tela de NCM - clicado em NO para andamento do processo",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Tela TMessageForm sem Title match. Seguindo...",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de itens/ncm: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def tipo_despesa(tipo: str) -> RpaRetornoProcessoDTO:
    console.print(
        f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para seleção do tipo de despesas...\n"
    )
    try:
        new_app = Application(backend="uia").connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        console.print(
            f"Conectado com sucesso, acessando o atributo filho ' Tipo de Despesa'...\n"
        )
        tipo_despesa = window.child_window(
            title=" Tipo de Despesa", class_name="TGroupBox"
        )

        console.print(
            f"Conectado com sucesso, inserindo o valor do tipo de despesa...\n"
        )

        edit = tipo_despesa.child_window(
            class_name="TDBIEditCode", found_index=1, control_type="Edit"
        )

        if edit.exists():
            edit.set_edit_text(tipo)
            edit.type_keys("{TAB}")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o valor da despesa",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print(f"Campo tipo de despesas - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo tipo de despesas - Não foi encontrado... \n",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o tipo de despesa, erro: {e}... \n",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def zerar_icms() -> RpaRetornoProcessoDTO:
    console.print(
        f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para marcar a opção Zerar ICMS...\n"
    )
    try:
        new_app = Application(backend="uia").connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        checkbox = window.child_window(
            title="Zerar tributação ICMS",
            class_name="TCheckBox",
            control_type="CheckBox",
        )
        if checkbox.exists():
            if not checkbox.get_toggle_state() == 1:
                checkbox.click()
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Sucesso para interagir com o checkbox para zerar o valor do icms",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        else:
            console.print(f"Campo zerar icms - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o valor da despesa",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para marcar a opção de zerar ICMS, erro: {e}... \n",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def cod_icms(codigo: str) -> RpaRetornoProcessoDTO:
    console.print(
        f"Conectando a tela de Informações para importação da Nota Fiscal Eletrônica para informar o codigo do icms...\n"
    )
    try:
        new_app = Application(backend="uia").connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        window = new_app["Informações para importação da Nota Fiscal Eletrônica"]

        console.print(f"Conectado com sucesso, acessando o atributo filho 'ICMS'...\n")
        icms_codigo = window.child_window(title="ICMS", class_name="TGroupBox")

        console.print(
            f"Conectado com sucesso, inserindo o valor do codigo do icms...\n"
        )

        edit = icms_codigo.child_window(
            class_name="TDBIEditCode", found_index=0, control_type="Edit"
        )

        if edit.exists():
            edit.set_edit_text(codigo)
            edit.type_keys("{TAB}")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Sucesso para inserir o codigo do icms",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print(f"Campo codigo do icms - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo codigo do icms - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o codigo do icms, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def rateio_despesa(unidade_code: str) -> RpaRetornoProcessoDTO:
    console.print(
        f"Conectando a tela de Rateio da Despesa para encerramento do processo...\n"
    )
    console.print(f"Código filial {unidade_code}...\n")
    try:

        console.print(f"Tentando clicar em Selecionar todos...\n")
        try:
            selecionar_todos = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\SelecionarTodos.png", confidence=0.5
            )
            if selecionar_todos:
                console.print(f"Campo selecionar todos encontrado, interagindo...\n")
                pyautogui.click(selecionar_todos)

        except Exception as e:
            console.print(f"Error ao interagir com o campo de selecionar todos : {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Error ao interagir com o campo de selecionar todos : {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(5)

        try:
            app = Application().connect(class_name="TFrmDadosRateioDespesa")
            main_window = app["TFrmDadosRateioDespesa"]
            console.print(f"Conectado com pela classe do emsys...\n")
        except:
            app = Application().connect(title="Rateio da Despesa")
            main_window = app["Rateio da Despesa"]
            console.print(f"Conectado pelo title...\n")

        main_window.set_focus()

        console.print(
            f"Conectado com sucesso, acessando o atributo filho 'Centro'...\n"
        )
        panel_centro = main_window.child_window(class_name="TPanel", found_index=1)

        console.print(
            f"Conectado com sucesso, inserindo o valor do tipo de despesa...\n"
        )

        edit = panel_centro.child_window(class_name="TDBIEditCode", found_index=1)

        try:
            value_centro = int(unidade_code) + 1000
        except ValueError:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Unidade code não é um número válido.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        value_centro_str = str(value_centro)
        console.print(f"Valor final a ser inserido no Centro {value_centro_str}...\n")

        if edit.exists():
            edit.set_edit_text(value_centro_str)
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo tipo de despesas - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo tipo de despesas - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print(f"Conectado com sucesso, inserindo o valor do rateio...\n")
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            edit.set_edit_text("100")
            edit.click()
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(3)

        console.print(
            f"Selecionando a opção 'Aplicar Rateio aos Itens Selecionados'...\n"
        )
        try:
            checkbox = panel_centro.child_window(
                title="Aplicar Rateio aos Itens Selecionados",
                class_name="TDBICheckBox",
            )
            checkbox.click()
            console.print(
                "A opção 'Aplicar Rateio aos Itens Selecionados' selecionado com sucesso... \n"
            )
        except:
            try:
                aplicar_rateio = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\entrada_notas\\aplicar_rateio_itens.png",
                    confidence=0.5,
                )
                if aplicar_rateio:
                    console.print(
                        f"Campo aplicar rateio itens encontrado, clicando...\n"
                    )
                    center_x, center_y = pyautogui.center(aplicar_rateio)
                    try:
                        pyautogui.click(center_x, center_y)
                    except:
                        pyautogui.click(aplicar_rateio)
            except:
                try:
                    app = Application().connect(title="Busca Centro de Custo")
                    main_window = app["Busca Centro de Custo"]
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Centro de custo não localizado na tela de rateio, por favor, verificar",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )
                except Exception as e:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Campo aplicar rateio - Não foi encontrado, erro: {e}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )

        console.print(f"Tentando clicar em Incluir Registro...\n")
        await worker_sleep(2)
        try:
            console.print(
                f"Não foi possivel clicar em Incluir Registro, tentando via hotkeys..\n"
            )
            pyautogui.press("tab")
            pyautogui.press("tab")
            await worker_sleep(2)
            pyautogui.press("enter")
            await worker_sleep(4)
        except Exception as e:
            try:
                incluir_registro_rateio = pyautogui.locateOnScreen(
                    ASSETS_PATH
                    + "\\entrada_notas\\importar_registro_rateio_despesas.png",
                    confidence=0.5,
                )
                if incluir_registro_rateio:
                    console.print(
                        f"Campo selecionar todos encontrado, interagindo...\n"
                    )
                    pyautogui.click(incluir_registro_rateio)
            except:
                console.print(
                    f"Clicando em Incluir registro para vincular ao centro de custo '...\n"
                )
                edit = panel_centro.child_window(
                    class_name="TDBITBitBtn", found_index=3
                )

                if edit.exists():
                    edit.click()
                else:
                    console.print(f"Campo Incluir registro nao foi encontrado...\n")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Campo Incluir registro nao foi encontrado",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )


        await worker_sleep(3)

        console.print(f"Verificando se o item foi rateado com sucesso...\n")
        panel_centro = main_window.child_window(class_name="TPanel", found_index=0)
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            valor_total_rateado = edit.window_text()
            if valor_total_rateado != "0,00":
                console.print(f"Rateio inserido com sucesso., clicando em OK..\n")
                send_keys("%o")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Rateio de despesa interagido com sucesso",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o tipo de despesa, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def select_nop_document_type(nop: str) -> RpaRetornoProcessoDTO:
    """
    Função que seleciona o tipo o NOP Nota na janela de Nota Fiscal de Entrada.

    Args:
        nop (str): Qual opção nop a ser selecionada.

    Returns:
        RpaRetornoProcessoDTO: Retorna um objeto com informações sobre o status do processo.
    """
    try:
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        main_window.set_focus()

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_nop_nota = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=0
        )
        combo_box_nop_nota.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )
        await worker_sleep(2)
        set_combobox("||List", nop)
        console.print(f"NOP Nota '{nop}', selecionado com sucesso...\n")

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"NOP Nota {nop} selecionado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel selecionar o NOP Nota, erro: {e} ",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def carregamento_import_xml() -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmAguarde", timeout=20)
        max_attempts = 60
        i = 0

        while i < max_attempts:
            try:
                main_window = app["TMessageForm"]
                window_title = main_window.window_text()
                if "Confirm" in window_title or "Information" in window_title:
                    console.print(f"Janela 'TMessageForm' encontrada!")
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno=f"Janela de information encontrada",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
            except:
                console.print(f"Janela 'TMessageForm' não encontrada!")

            try:
                app = Application().connect(class_name="TFrmAguarde")
            except Exception as e:
                console.print(
                    f"Nota importada sem Warnings ou Informations, seguindo com andamento do fluxo"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Nota importada sem Warnings ou Informations, seguindo com andamento do fluxo",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

            await worker_sleep(2)
            i += 1

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Tentando seguir com o fluxo",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

    except Exception as e:
        console.print(
            f"Não foi possivel conectar a tela de aguarde para carregamento da nota: {e}"
        )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Não foi possivel conectar a tela de aguarde para carregamento da nota, mas tentando seguir com o fluxo",
            status=RpaHistoricoStatusEnum.Sucesso,
        )


async def check_nota_importada(xml_nota: str) -> RpaRetornoProcessoDTO:
    # lazy import para evitar erro de importação circular
    from worker_automate_hub.api.client import get_status_nf_emsys

    try:
        max_attempts = 60
        i = 0

        while i < max_attempts:
            information_pop_up = await is_window_open("Information")
            if information_pop_up["IsOpened"] == True:
                break
            else:
                console.print(f"Aguardando confirmação de nota incluida...\n")
                await worker_sleep(5)
                i += 1

        information_pop_up = await is_window_open("Information")
        if information_pop_up["IsOpened"] == True:
            app = Application().connect(class_name="TFrmNotaFiscalEntrada")
            main_window = app["Information"]

            main_window.set_focus()

            console.print(f"Obtendo texto do Information...\n")
            console.print(
                f"Tirando print da janela do Information para realização do OCR...\n"
            )

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = (
                f"C:\\Users\\{username}\\Downloads\\information_popup_{xml_nota}.png"
            )
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(f"Texto Full capturado {captured_text}...\n")
            os.remove(path_to_png)
            if "nota fiscal inc" in captured_text.lower():
                console.print(f"Tentando clicar no Botão OK...\n")
                btn_ok = main_window.child_window(class_name="TButton")

                if btn_ok.exists():
                    btn_ok.click()
                    status_nf_emsys = await get_status_nf_emsys(int(xml_nota))
                    if status_nf_emsys.get("status") == "Lançada":
                        return RpaRetornoProcessoDTO(
                            sucesso=True,
                            retorno=f"Nota incluida com sucesso",
                            status=RpaHistoricoStatusEnum.Sucesso,
                        )
                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Erro ao lançar nota",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=f"Pop_up Information não mapeado para andamento do robô, mensagem {captured_text}",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        else:
            console.print(f"Aba Information não encontrada")
            try:
                nota_incluida = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\entrada_notas\\nota_fiscal_incluida.png",
                    confidence=0.7,
                )
                if nota_incluida:
                    status_nf_emsys = await get_status_nf_emsys(int(xml_nota))
                    if status_nf_emsys.get("status") == "Lançada":
                        return RpaRetornoProcessoDTO(
                            sucesso=True,
                            retorno=f"Nota incluida com sucesso",
                            status=RpaHistoricoStatusEnum.Sucesso,
                        )
                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Erro ao lançar nota",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
                else:
                     try:
                        error_work = await error_after_xml_imported()
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=error_work.retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=error_work.tags
                            )
                     except: 
                        return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro ao identificar pop-error",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            except Exception as e:
                console.print(f"Error: {e}")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
    except Exception as e:
        console.print(
            f"Erro ao conectar à janela Information para obter retorno de status de inclusão da nota: {e}\n"
        )
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def kill_all_emsys():
    try:
        await kill_process("EMSysFiscal")
        await kill_process("EMSys")
        await kill_contabil_processes()
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"EMSys encerrado com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao fechar o emsys, erro{e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

async def kill_contabil_processes():
    try:
        subprocess.run(["taskkill","/F", "/IM","contabil1.exe","/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["taskkill","/F", "/IM","RezendeWSManager.exe","/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["taskkill","/F", "/IM","RezendeWSServer.exe","/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["taskkill","/F", "/IM","RezendeWSClient.exe","/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await verifica_processos_emsys_abertos()
    except Exception as error:
        console.print(f"Error: {error}")

async def verifica_processos_emsys_abertos():
    try:
        for processo in psutil.process_iter(attrs=['pid', 'name']):
            if 'emsys' in processo.info['name'].lower() or 'rezende' in processo.info['name'].lower():
                console.print(f"processo encontrado : {processo.info['name']}")
                subprocess.run(["taskkill","/F", "/IM",processo.info['name'],"/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as error:
        console.print(f"Error: {error}")

async def errors_generate_after_import(xml_nota: str) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmExibeLogErroImportacaoNfe")
        main_window = app["TFrmExibeLogErroImportacaoNfe"]
        console.print("Tela com itens com erro existe, salvando os itens...\n")

        btn_save = main_window.child_window(title="Salvar", class_name="TBitBtn")

        if btn_save.exists():
            max_attempts = 3
            i = 0
            while i < max_attempts:
                console.print("Clicando no botão de salvar...\n")
                try:
                    btn_save.click()
                except:
                    console.print("Não foi possivel clicar no Botão OK... \n")

                await worker_sleep(3)

                console.print(
                    "Verificando a existencia da tela para informar o caminho do arquivo...\n"
                )

                try:
                    app = Application().connect(title="Salvar")
                    main_window = app["Salvar"]
                    console.print("Tela para informar o caminho do arquivo existe")
                    break
                except Exception as e:
                    console.print(
                        f"Tela para informar o caminho do arquivo não encontrada. Tentativa {i + 1}/{max_attempts}."
                    )

                i += 1

            if i == max_attempts:
                raise Exception(
                    "Número máximo de tentativas atingido. Tela para informar o caminho do arquivo existe."
                )

            await worker_sleep(4)
            console.print(
                "Interagindo com a tela para informar o caminho do arquivo...\n"
            )
            app = Application().connect(title="Salvar")
            main_window = app["Salvar"]
            console.print(
                "Tela para informar o caminho do arquivo existe, inserindo o diretorio...\n"
            )
            await worker_sleep(2)
            main_window.type_keys("%n")
            username = getpass.getuser()
            path_to_txt = f"C:\\Users\\{username}\\Downloads\\erro_itens{xml_nota}.txt"
            pyautogui.write(path_to_txt)
            await worker_sleep(1)
            main_window.type_keys("%l")
            console.print(f"Arquivo salvo com sucesso... \n")

            conteudo = ""
            await worker_sleep(3)
            with open(path_to_txt, "r", encoding="latin1", errors="replace") as arquivo:
                conteudo = arquivo.read()
                console.print(
                    f"Arquivo salvo com sucesso, itens com erro {conteudo}...\n"
                )

            os.remove(path_to_txt)
            console.print(
                f"Removendo o arquivo e enviando os itens para o backoffice... \n"
            )
            console.print(
                f"Itens nao localizados para o fornecedor salvo e retornando como falha no backoffice para correção...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Itens nao localizados para o fornecedor, Mensagem: {conteudo}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )
        else:
            console.print(f"Botao Salvar - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao processar - Tela de Erros gerados na importação do NF-e - Botao Salvar - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar - Tela de Erros gerados na importação do NF-e, {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def ultimo_dia_util_do_mes(data_atual):
    ano = data_atual.year
    mes = data_atual.month

    ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
    ultimo_dia = datetime(ano, mes, ultimo_dia_mes)

    if ultimo_dia.weekday() == 5:
        ultimo_dia -= timedelta(days=1)
    elif ultimo_dia.weekday() == 6:
        ultimo_dia -= timedelta(days=2)

    return ultimo_dia


async def e_ultimo_dia_util():
    hoje = datetime.today()
    ultimo_dia_util = await ultimo_dia_util_do_mes(hoje)

    return hoje.date() == ultimo_dia_util.date()


async def ocr_warnings(numero_nota: str) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(title="Warning")
        main_window = app["Warning"]
        main_window.set_focus()

        console.print(f"Obtendo texto do Warning...\n")
        console.print(f"Tirando print da janela do warning para realização do OCR...\n")

        window_rect = main_window.rectangle()
        screenshot = pyautogui.screenshot(
            region=(
                window_rect.left,
                window_rect.top,
                window_rect.width(),
                window_rect.height(),
            )
        )
        username = getpass.getuser()
        path_to_png = (
            f"C:\\Users\\{username}\\Downloads\\warning_popup_{numero_nota}.png"
        )
        screenshot.save(path_to_png)
        console.print(f"Print salvo em {path_to_png}...\n")

        console.print(
            f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
        )
        image = Image.open(path_to_png)
        image = image.convert("L")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image.save(path_to_png)
        console.print(f"Imagem preparada com sucesso...\n")
        console.print(f"Realizando OCR...\n")
        captured_text = pytesseract.image_to_string(Image.open(path_to_png))
        os.remove(path_to_png)
        console.print(f"Texto Full capturado {captured_text}...\n")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=captured_text,
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao realizar a extração do texto vinculado ao warning, erro - {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def ocr_title(numero_nota: str, windows_title: str) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(title=windows_title)
        main_window = app[windows_title]
        main_window.set_focus()

        console.print(f"Obtendo texto da Informação...\n")
        console.print(
            f"Tirando print da janela do Informação para realização do OCR...\n"
        )

        window_rect = main_window.rectangle()
        screenshot = pyautogui.screenshot(
            region=(
                window_rect.left,
                window_rect.top,
                window_rect.width(),
                window_rect.height(),
            )
        )
        username = getpass.getuser()
        path_to_png = (
            f"C:\\Users\\{username}\\Downloads\\informacao_popup_{numero_nota}.png"
        )
        screenshot.save(path_to_png)
        console.print(f"Print salvo em {path_to_png}...\n")

        console.print(
            f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
        )
        image = Image.open(path_to_png)
        image = image.convert("L")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image.save(path_to_png)
        console.print(f"Imagem preparada com sucesso...\n")
        console.print(f"Realizando OCR...\n")
        captured_text = pytesseract.image_to_string(Image.open(path_to_png))
        console.print(f"Texto Full capturado {captured_text}...\n")
        os.remove(path_to_png)
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=captured_text,
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao realizar a extração do texto vinculado ao warning, erro - {e}",
            status=RpaHistoricoStatusEnum.Falha,
        )


async def ocr_by_class(
    numero_nota: str, windows_class: str, app_class: str
) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name=windows_class)
        main_window = app[app_class]
        main_window.set_focus()

        console.print(f"Obtendo texto da Janela...\n")
        console.print(f"Tirando print da janela do warning para realização do OCR...\n")

        window_rect = main_window.rectangle()
        screenshot = pyautogui.screenshot(
            region=(
                window_rect.left,
                window_rect.top,
                window_rect.width(),
                window_rect.height(),
            )
        )
        username = getpass.getuser()
        path_to_png = (
            f"C:\\Users\\{username}\\Downloads\\ocr_bt_class_popup_{numero_nota}.png"
        )
        screenshot.save(path_to_png)
        console.print(f"Print salvo em {path_to_png}...\n")

        console.print(
            f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
        )
        image = Image.open(path_to_png)
        image = image.convert("L")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image.save(path_to_png)
        console.print(f"Imagem preparada com sucesso...\n")
        console.print(f"Realizando OCR...\n")
        captured_text = pytesseract.image_to_string(Image.open(path_to_png))
        os.remove(path_to_png)
        console.print(f"Texto Full capturado {captured_text}...\n")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=captured_text,
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao realizar a extração do texto vinculado ao warning, erro - {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def nf_busca_nf_saida(num_nota_fiscal: str) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmNotaFiscalSaida", timeout=60)
        main_window = app["TFrmNotaFiscalSaida"]

        main_window.set_focus()
        await worker_sleep(3)

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Saida', navegando entre eles...\n"
        )
        panel_TPageControl = main_window.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        text_numero_nota = panel_TTabSheet.child_window(
            class_name="TDBIEditString", found_index=8
        )
        text_numero_nota.set_edit_text(num_nota_fiscal)
        console.print("Inserindo no numero da nota para buscar...\n")
        await worker_sleep(2)

        try:
            pesquisar_icon = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\emsys\\icon_pesquisa_nota_saida.png", confidence=0.8
            )
            pyautogui.click(pesquisar_icon)
            await worker_sleep(5)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Processo Executado com Sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel clicar na Lupa para buscar a nota fiscal na tela de nota fiscal de saída, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel realizar a atividade na tela de Nota fiscal de Saida, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def nf_devolucao_liquidar_cupom(
    num_nota_fiscal: str, data_atual: str
) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmTituloReceber", timeout=60)
        main_window = app["TFrmTituloReceber"]
        main_window.set_focus()
        console.print("Inserindo o numero da nota fiscal para buscar...\n")
        panel_TTab_Sheet = main_window.child_window(
            class_name="TTabSheet", found_index=0
        )
        n_titulo = panel_TTab_Sheet.child_window(
            class_name="TDBIEditString", found_index=8
        )
        n_titulo.set_edit_text(num_nota_fiscal)
        await worker_sleep(2)
        console.print("Numero da nota fiscal inserido com sucesso...\n")

        try:
            pesquisar_icon = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\emsys\\icon_pesquisa_nota_saida.png", confidence=0.8
            )
            pyautogui.click(pesquisar_icon)
            await worker_sleep(5)
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel clicar na Lupa para buscar a nota fiscal, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        panel_TTab_Sheet = main_window.child_window(
            class_name="TTabSheet", found_index=0
        )
        panel_status = panel_TTab_Sheet.child_window(
            class_name="TDBIGroupBox", found_index=1
        )

        radio_aberto = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=4
        )
        radio_em_protesto = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=0
        )
        radio_negociado = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=1
        )
        radio_faturado = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=2
        )
        radio_liquidado = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=3
        )

        if radio_aberto.is_checked():
            console.print(
                "Botão 'Aberto' está selecionado, seguindo com o processo...\n"
            )
        else:
            status_selecionado = None
            if radio_em_protesto.is_checked():
                console.print("O botão 'Em Protesto' está selecionado.")
                status_selecionado = "Em Protesto"
            elif radio_negociado.is_checked():
                console.print("O botão 'Negociado' está selecionado.")
                status_selecionado = "Negociado"
            elif radio_faturado.is_checked():
                console.print("O botão 'Faturado' está selecionado.")
                status_selecionado = "Faturado"
            elif radio_liquidado.is_checked():
                console.print("O botão 'Liquidado' está selecionado.")
                status_selecionado = "Liquidado"
            else:
                console.print("Nenhum botão de rádio está selecionado.")
                status_selecionado = "Nenhum status está selecionado."

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Cupom/titulo com status {status_selecionado} por favor, verificar",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        console.print("Acessando a opção de Caixa")
        panel_TPage = main_window.child_window(class_name="TcxTreeView")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("^({HOME})")
        await worker_sleep(1)
        send_keys("{DOWN " + ("2") + "}")
        await worker_sleep(2)

        main_window.set_focus()

        page_control = main_window.child_window(
            class_name="TPageControl", found_index=0
        )
        # Navegar até a aba TabSheetLiquidacao
        tab_sheet_liquidacao = page_control.child_window(title="TabSheetLiquidacao")
        panel_liquidacao = tab_sheet_liquidacao.child_window(
            class_name="TPanel", found_index=0
        )
        db_edit_date = panel_liquidacao.child_window(
            class_name="TDBIEditDate", found_index=0
        )
        console.print("Inserindo a data atual")
        db_edit_date.set_edit_text(data_atual)
        await worker_sleep(1)

        # Clicar na Calculador
        tab_sheet_caixa = tab_sheet_liquidacao.child_window(title="TabSheetCaixa")
        calculador_button = tab_sheet_caixa.child_window(
            class_name="TBitBtn", found_index=0
        )
        console.print("Clicando sobre Calculadora")
        calculador_button.click_input()
        await worker_sleep(1)

        console.print("Inserindo 13 em Especie")
        db_edit_code = tab_sheet_caixa.child_window(
            class_name="TDBIEditCode", found_index=0
        )
        db_edit_code.set_edit_text("13")
        await worker_sleep(1)
        pyautogui.press("tab")

        # Clicar no botão Liquidar dentro de TabSheetLiquidacao
        liquidar_button = panel_liquidacao.child_window(
            class_name="TBitBtn", found_index=2
        )
        console.print("Clicando em Liquidar")
        await worker_sleep(1)
        liquidar_button.click_input()

        await worker_sleep(7)

        confirm_pop_up = await is_window_open_by_class("TMessageForm", "TMessageForm")
        if confirm_pop_up["IsOpened"] == True:
            capture_text_ocr = await ocr_by_class(
                num_nota_fiscal, "TMessageForm", "TMessageForm"
            )
            if capture_text_ocr.sucesso == True:
                msg_result = capture_text_ocr.retorno
                if "deseja realmente" in msg_result.lower():
                    app_confirm = Application().connect(class_name="TMessageForm")
                    main_window_confirm = app_confirm["TMessageForm"]

                    btn_yes = main_window_confirm["&Yes"]
                    try:
                        btn_yes.click()
                        await worker_sleep(3)
                        console.print(
                            "O botão Yes foi clicado com sucesso.", style="green"
                        )
                        # main_window.close()
                    except:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Não foi possivel clicar em Yes durante para a confirmação da liquidação do titulo",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
                elif "bloqueado" in msg_result.lower():
                    app_confirm = Application().connect(class_name="TMessageForm")
                    main_window_confirm = app_confirm["TMessageForm"]

                    btn_yes = main_window_confirm["&No"]
                    try:
                        btn_yes.click()
                        await worker_sleep(3)
                        console.print(
                            "O botão Yes foi clicado com sucesso.", style="green"
                        )
                    except:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Não foi possivel clicar em Yes durante para a confirmação da liquidação do titulo",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"POP não mapeado: {msg_result}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )


        confirm_pop_up = await is_window_open_by_class("TMessageForm", "TMessageForm")
        if confirm_pop_up["IsOpened"] == True:
            capture_text_ocr = await ocr_by_class(
                num_nota_fiscal, "TMessageForm", "TMessageForm"
            )
            if capture_text_ocr.sucesso == True:
                msg_result = capture_text_ocr.retorno
                if "deseja realmente" in msg_result.lower():
                    app_confirm = Application().connect(class_name="TMessageForm")
                    main_window_confirm = app_confirm["TMessageForm"]

                    btn_yes = main_window_confirm["&Yes"]
                    try:
                        btn_yes.click()
                        await worker_sleep(3)
                        console.print(
                            "O botão Yes foi clicado com sucesso.", style="green"
                        )
                        # main_window.close()
                    except:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Não foi possivel clicar em Yes durante para a confirmação da liquidação do titulo",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
                elif "bloqueado" in msg_result.lower():
                    app_confirm = Application().connect(class_name="TMessageForm")
                    main_window_confirm = app_confirm["TMessageForm"]

                    btn_yes = main_window_confirm["&No"]
                    try:
                        btn_yes.click()
                        await worker_sleep(3)
                        console.print(
                            "O botão Yes foi clicado com sucesso.", style="green"
                        )
                    except:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Não foi possivel clicar em Yes durante para a confirmação da liquidação do titulo",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"POP não mapeado: {msg_result}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"POP de confirmação de liquidar titulo não encontrado",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        console.print("Aguardando a confirmação de Liquidação realizado com sucesso")


        try:
            try:
                msg_pop_up = await ocr_title(num_nota_fiscal, "Informação")
                console.print(f"retorno:{msg_pop_up.sucesso}")
                console.print(f"retorno:{msg_pop_up}")
            except Exception as e:
                app = Application().connect(class_name="TMessageForm", timeout=60)
                main_window = app["TMessageForm"]
                main_window.set_focus()
                msg_pop_up = await ocr_by_class(
                    num_nota_fiscal, "TMessageForm", "TMessageForm"
                )

            if msg_pop_up.sucesso == True:
                msg_result = msg_pop_up.retorno
                if "sucesso" in msg_result.lower():
                    try:
                        app = Application().connect(
                            class_name="TFrmTituloReceber", timeout=60
                        )
                        main_window = app["Informação"]
                        main_window.set_focus()
                        btn_ok = main_window.child_window(class_name="Button")
                        btn_ok.click()
                    except Exception as e:
                        pyautogui.press("enter")
                    await worker_sleep(1)
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Não foi possivel obter a confirmação de titulo liquidado com sucesso, pop_up nao mepeado: {msg_result}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel obter a confirmação de titulo liquidado com sucesso, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )


        await worker_sleep(2)
        app = Application().connect(class_name="TFrmTituloReceber", timeout=60)
        main_window = app["TFrmTituloReceber"]
        main_window.set_focus()
        console.print("Confirmando se o titulo alterou para Liquidado")
        panel_TPage = main_window.child_window(class_name="TcxTreeView")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        await worker_sleep(2)
        pyautogui.press("home")
        await worker_sleep(1)
        pyautogui.press("home")
        await worker_sleep(2)

        panel_TTab_Sheet = main_window.child_window(
            class_name="TTabSheet", found_index=0
        )
        panel_status = panel_TTab_Sheet.child_window(
            class_name="TDBIGroupBox", found_index=1
        )
        radio_liquidado = panel_status.child_window(
            class_name="TDBIRadioButton", found_index=3
        )

        if radio_liquidado.is_checked():
            console.print(
                "Botão 'Liquidado' está selecionado, seguindo com o processo...\n"
            )
            app = Application().connect(class_name="TFrmTituloReceber", timeout=60)
            main_window = app["TFrmTituloReceber"]
            main_window.set_focus()
            main_window.close()
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Titulo Liquidade com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Status diferente de liquidado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel concluir as atividades para realizar a liquidação do titulo, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def gerenciador_nf_header(
    periodo: str, cod_cliente: str
) -> RpaRetornoProcessoDTO:
    try:
        console.print(f"\n'Conectando ao Gerenciador de NF", style="bold green")
        app = Application().connect(class_name="TFrmGerenciadorNFe2", timeout=15)
        main_window = app["TFrmGerenciadorNFe2"]
        main_window.set_focus()

        console.print("Conectando as Janelas para iteração...\n")
        panel_TGroup_Box = main_window.child_window(
            class_name="TGroupBox", found_index=0
        )
        console.print("Janela principal conectada...\n")

        periodo_vigente_inicio = main_window.child_window(
            class_name="TDBIEditDate", found_index=0
        )
        console.print("Periodo vigente inicio conectada...\n")
        periodo_vigente_fim = main_window.child_window(
            class_name="TDBIEditDate", found_index=1
        )
        console.print("Periodo vigente fim conectada...\n")
        situacao_select = main_window.child_window(
            class_name="TDBIComboBoxValues", found_index=2
        )
        console.print("Situacao conectada com sucesso...\n")
        field_cod_cliente = main_window.child_window(
            class_name="TDBIEditCode", found_index=4
        )
        console.print("Campo cliente conectada com sucesso...\n")
        btn_pesquisar = main_window.child_window(title="Pesquisar")
        console.print("Botao pesquisar conectada com sucesso...\n")

        console.print("Inserindo o período vigente para buscar...\n")
        periodo_vigente_inicio.set_edit_text(periodo)
        await worker_sleep(1)
        periodo_vigente_fim.set_edit_text(periodo)
        await worker_sleep(2)

        console.print("Verificando a situação...\n")
        situacao_text = situacao_select.window_text()
        if "transmitida" in situacao_text.lower():
            console.print("Situação corretamente selecionada...\n")
        else:
            situacao_select.click()
            # set_combobox("||List", "Todas")
            set_combobox("||List", "Não Transmitida")

        console.print("Inserindo o codigo do cliente...\n")
        field_cod_cliente.click()
        await worker_sleep(1)
        field_cod_cliente.set_edit_text(cod_cliente)
        await worker_sleep(1)
        field_cod_cliente.click()
        pyautogui.press("tab")
        await worker_sleep(2)

        console.print("Cicando em Pesquisar...\n")
        btn_pesquisar.click()
        await worker_sleep(5)

        i = 0
        max_attempts = 25

        while i < max_attempts:
            i += 1
            console.print("Verificando se a nota foi encontrada...\n")
            try:
                main_window.set_focus()
                no_data_full_path = "assets\\entrada_notas\\no_data_display.png"
                img_no_data = pyautogui.locateCenterOnScreen(
                    no_data_full_path, confidence=0.6
                )
                if img_no_data:
                    console.print(
                        "'No data display' ainda aparente. Tentando novamente..."
                    )
                    await worker_sleep(10)
            except pyautogui.ImageNotFoundException:
                console.print("'No data display' não encontrado na tela!")
                break

            except Exception as e:
                console.print(f"Ocorreu um erro: {e}")

        if i == max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Tempo esgotado, No data display ainda presente na busca pela nota em Gerenciador NF-e, nota não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        try:
            console.print("Clicar Selecionar todos itens...\n")
            selecionar_todos_itens = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\emsys\\selecinar_todos_itens_quadro_azul.png",
                confidence=0.8,
            )
            pyautogui.click(selecionar_todos_itens)
            await worker_sleep(5)
            return RpaRetornoProcessoDTO(
                sucesso=True, retorno=f"Sucesso", status=RpaHistoricoStatusEnum.Sucesso
            )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel clicar em selecionar todos os itens na tela de Gerenciador de NF-e, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel clicar na Lupa para buscar a nota fiscal na tela de nota fiscal de saída, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def cadastro_pre_venda_header(
    nop: str, cod_cliente: str, cod_pagamento: str, secundary_nop: str = ""
) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmPreVenda", timeout=60)
        main_window = app["TFrmPreVenda"]
        main_window.set_focus()

        console.print("Navegando nos elementos...\n")
        panel_TPage = main_window.child_window(class_name="TPage", found_index=0)
        panel_TGroup_Box = panel_TPage.child_window(
            class_name="TGroupBox", found_index=0
        )

        console.print("Selecionando a condição de pagamento...\n")
        condicao_select = panel_TGroup_Box.child_window(
            class_name="TDBIComboBox", found_index=2
        )
        condicao_select.click()
        await worker_sleep(1)
        if "vista" in cod_pagamento.lower():
            set_combobox("||List", cod_pagamento)
            await worker_sleep(1)
            pyautogui.press("down")
        else:
            set_combobox("||List", cod_pagamento)
        await worker_sleep(1)

        console.print("Inserindo codigo do cliente...\n")
        field_cod_cliente = panel_TGroup_Box.child_window(
            class_name="TDBIEditNumber", found_index=1
        )
        field_cod_cliente.click()
        pyautogui.press("del")
        pyautogui.press("backspace")
        field_cod_cliente.set_edit_text(cod_cliente)
        pyautogui.press("tab")
        await worker_sleep(5)

        pre_vendas_existentes = await is_window_open("Information")
        if pre_vendas_existentes["IsOpened"] == True:
            app = Application().connect(title="Information", class_name="TMessageForm")
            main_window = app["Information"]
            main_window.set_focus()
            await worker_sleep(1)

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\pre_venda_existente{cod_cliente}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.5)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)

            if 'em aberto' in captured_text or 'Exist' in captured_text or 'para este cliente' in captured_text:
                app = Application().connect(title="Information")
                main_window = app["Information"]
                btn_ok = main_window.child_window(class_name="TButton", found_index=0)
                btn_ok.click()
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop-up não mapeado para seguimento do processo, erro: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        
        try:
            app = Application().connect(class_name="TFrmPreVenda", timeout=10)
            main_window = app["Confirm"]
            main_window.set_focus()

            btn_ok = main_window.child_window(class_name="TButton", found_index=0)
            btn_ok.click()
        except Exception as e:
            console.print("Não possui janela de Pre venda existe para este cliente")

        console.print("Obtendo cidade do cliente")
        field_cidade_cliente = panel_TGroup_Box.child_window(
            class_name="TDBIEditDescription", found_index=0
        )
        cidade_cliente = field_cidade_cliente.window_text()

        console.print("Inserindo NOP...\n")
        # nop_select_box = panel_TGroup_Box.child_window(
        #     class_name="TDBIComboBox", found_index=1
        # )
        # nop_select_box.click()
        await worker_sleep(1)

        # if "5667" in nop:
        app = Application().connect(class_name="TFrmPreVenda", timeout=60)
        main_window = app["TFrmPreVenda"]
        main_window.set_focus()
        panel_TPage = main_window.child_window(class_name="TPage", found_index=0)
        panel_TGroup_Box = panel_TPage.child_window(class_name="TGroupBox", found_index=0)
        nop_select_box = panel_TGroup_Box.child_window(class_name="TDBIComboBox", found_index=1)
        try:
            nop_select_box.select(nop)
            console.print(f"Selecionou NOP: {nop}")
        except:
            nop_select_box.select(secundary_nop)
            console.print(f"Selecionou NOP: {secundary_nop}")

        await worker_sleep(1)
        pyautogui.hotkey('enter')
        await worker_sleep(1)
        pyautogui.hotkey("tab")

        nop_select_box = panel_TGroup_Box.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        value_nop_selected = nop_select_box.window_text()

        if nop == value_nop_selected:
            console.print(f"NOP {nop} corretamente selecionada...\n")
        elif secundary_nop == value_nop_selected:
            console.print(f"NOP {secundary_nop} corretamente selecionada...\n")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel selecionar a nop corretamente",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        
        await worker_sleep(4)
        confirm_selecionar_nf_entrada = await is_window_open("Confirm")
        if confirm_selecionar_nf_entrada["IsOpened"] == True:
            app = Application().connect(title="Confirm")
            main_window = app["Confirm"]
            main_window.set_focus()
            await worker_sleep(1)

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\confirmar_nf_{cod_cliente}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(f"Texto Full capturado {captured_text}...\n")
            os.remove(path_to_png)

            if 'nota de entrada' in captured_text.lower():
                app = Application().connect(title="Confirm")
                main_window = app["Confirm"]
                btn_no = main_window["&No"]
                btn_no.click()
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop-up não mapeado para seguimento do processo, mensagem {captured_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=cidade_cliente,
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel clicar na Lupa para buscar a nota fiscal na tela de pre venda, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def post_partner(
    url_retorno: str, idetificador: str, num_nota: str, valor_nota: str
):
    try:
        import json

        url = url_retorno
        dados = {
            "status": "S",
            "numero_nota": num_nota,
            "observacao": "Nota lançada com sucesso!",
            "valor_nota": valor_nota,
            "identificador": idetificador,
        }

        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=json.dumps(dados), headers=headers
            ) as response:
                if response.status == 200:
                    console.print(f"Dados enviado com sucesso")
    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do webhook: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.info(err_msg)


async def pessoas_ativa_cliente_fornecedor(
    cod_cliente: str, ativar_cliente: bool, ativar_forcedor: bool
) -> RpaRetornoProcessoDTO:
    try:
        app = Application().connect(class_name="TFrmCadastroPessoaNew", timeout=60)
        main_window = app["TFrmCadastroPessoaNew"]
        main_window.set_focus()

        panel_Capa = main_window.child_window(class_name="TGroupBox", found_index=1)
        cod_pessoa = panel_Capa.child_window(class_name="TDBIEditNumber", found_index=1)
        cod_pessoa.click()
        for _ in range(3):
            pyautogui.press("del")
            pyautogui.press("backspace")

        cod_pessoa.set_edit_text(cod_cliente)
        cod_pessoa.click()
        pyautogui.press("enter")
        await worker_sleep(3)

        main_window.set_focus()
        panel_Capa = main_window.child_window(class_name="TGroupBox", found_index=0)
        grp_classificacao = panel_Capa.child_window(
            class_name="TDBIGroupBox", found_index=0
        )
        forncedor_atualizado = False
        cliente_atualizado = False

        if ativar_forcedor:
            checkbox_fornecedor = grp_classificacao.child_window(
                title="Fornecedor", class_name="TDBICheckBox"
            )
            if not checkbox_fornecedor.is_checked():
                forncedor_atualizado = True
                checkbox_fornecedor.click()
                console.print("Ativo como fornecedor... \n")

        if ativar_cliente:
            checkbox_cliente = grp_classificacao.child_window(
                title="Cliente", class_name="TDBICheckBox"
            )
            if not checkbox_cliente.is_checked():
                cliente_atualizado = True
                checkbox_cliente.click()
                console.print("Ativo como Cliente...\n")

        if cliente_atualizado == True or forncedor_atualizado == True:
            await worker_sleep(2)
            inserir_registro = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\notas_saida\\salvar_nf_saida.png", confidence=0.8
            )
            pyautogui.click(inserir_registro)
            await worker_sleep(3)

            console.print("Verificando a existência de Confirmação...\n")
            confirm_pop_up = await is_window_open_by_class(
                "TMessageForm", "TMessageForm"
            )
            if confirm_pop_up["IsOpened"] == True:
                app_confirm = Application().connect(class_name="TMessageForm")
                main_window_confirm = app_confirm["TMessageForm"]

                btn_no = main_window_confirm["&No"]
                try:
                    btn_no.click()
                    await worker_sleep(3)
                    console.print("O botão No foi clicado com sucesso.", style="green")
                    pyautogui.press("enter")
                    await worker_sleep(3)
                    pyautogui.press("enter")
                    await worker_sleep(2)
                    main_window.close()
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno=f"Sucesso",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
                except:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Não foi possivel clicar em No durante a alteração no tipo de cadastro",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            else:
                pyautogui.press("enter")
                main_window.set_focus()
                await worker_sleep(2)
                main_window.close()
                return RpaRetornoProcessoDTO(
                    sucesso=True, retorno=f"Sucesso", status=RpaHistoricoStatusEnum.Sucesso
                )
        else:
            main_window.set_focus()
            pyautogui.press("enter")
            await worker_sleep(2)
            main_window.close()
            return RpaRetornoProcessoDTO(
                sucesso=True, retorno=f"Sucesso", status=RpaHistoricoStatusEnum.Sucesso
            )
    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Não foi possivel clicar na Lupa para buscar a nota fiscal na tela de nota fiscal de saída, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def save_pdf_emsys(file_path):
    try:
        await worker_sleep(10)
        app = Application(backend="win32").connect(title="Print Preview")
        window_print_preview = app["Print Preview"]
        window_print_preview.set_focus()
        window_print_preview.maximize()

        pyautogui.click(14, 39)

        await worker_sleep(5)

        app = Application(backend="win32").connect(
            title="Print", class_name="TppPrintDialog"
        )
        window_print = app["Print"]
        # OK para salvar pdf
        btn_ok = window_print.child_window(title="OK", class_name="TButton")
        btn_ok.set_focus()
        btn_ok.click()

        await worker_sleep(5)

        app = Application(backend="win32").connect(
            title="Salvar Saída de Impressão como"
        )
        window_saida_impressao = app["Salvar Saída de Impressão como"]
        # OK para salvar pdf
        file_box = window_saida_impressao.child_window(
            class_name="ComboBox", found_index=0
        )
        btn_ok = window_saida_impressao.child_window(found_index=0, class_name="Button")
        file_box.set_focus()
        file_box.type_keys(f"{file_path}", with_spaces=True)
        await worker_sleep(2)
        btn_ok.click()

        try:
            window_print_preview.close()
        except Exception as e:
            console.print(f"Erro ao fechar print preview, erro: {e}")

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao salvar pdf, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )


async def create_temp_folder():
    nome_usuario = os.environ.get("USERNAME") or os.environ.get("USER")
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    nome_pasta = os.path.join(documents_path, f"{nome_usuario}_arquivos")

    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
        console.print(f"Pasta '{nome_pasta}' criada com sucesso.")
    else:
        console.print(f"Pasta '{nome_pasta}' já existe.")

    return os.path.abspath(nome_pasta)

async def delete_folder(folder_name):
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    folder_path = os.path.join(documents_path, folder_name)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            console.print(f"Pasta '{folder_name}' e todos os seus conteúdos foram deletados com sucesso.")
        except Exception as e:
            console.print(f"[red]Erro ao deletar a pasta '{folder_name}': {e}")
    else:
        console.print(f"[yellow]A pasta '{folder_name}' não foi encontrada no diretório '{documents_path}'.")


async def get_text_display_window(dados_texto):
    linhas = dados_texto.strip().split("\n")

    for linha in linhas[1:]:
        match = re.search(r"Rejeicao:(.*)", linha)
        if match:
            return match.group(1).strip()
    return ""

async def wait_nf_ready():
    current_try = 0
    max_tries = 60
    while current_try < max_tries:
        window_closed = await wait_window_close("Aguarde...")
        if not window_closed:
            desktop = Desktop(backend="uia")
            try:
                window = desktop.window(title_re="Aguarde...")
                if window.exists():
                    await worker_sleep(30)
                    current_try += 1
                    continue
            except Exception as e:
                console.print("Janela Aguarde Fechada")
            
            console.print("Verificando se a nota foi transmitida com sucesso")
            app = Application().connect(class_name="TFrmProcessamentoNFe2", timeout=15)
            main_window = app["TFrmProcessamentoNFe2"]
            # main_window.set_focus()
            try:
                app = Application().connect(class_name="TFrmMensagemNFe", timeout=15)
                message_window = app["TFrmMensagemNFe"]
                if message_window.exists():
                    #Clica check box "Não mostrar novamente"
                    pyautogui.click(731, 472)
                    #Clica em fechar
                    message_window.child_window(title="Fechar", class_name="TBitBtn").click()
                    await worker_sleep(3)
            except Exception as e:
                console.print(f"Janela de mensagem não encontrada, seguindo o processo... ERRO: {e}")

            tpanel_footer = main_window.child_window(class_name="TGroupBox", found_index=0)

            rect = tpanel_footer.rectangle()
            center_x = (rect.left + rect.right) // 2
            center_y = (rect.top + rect.bottom) // 2

            pyautogui.moveTo(center_x, center_y)
            pyautogui.click(center_x, center_y, clicks=2, interval=1)
            # pyautogui.click((center_x, center_y))

            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
            await worker_sleep(1)
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')

            win32clipboard.OpenClipboard()
            pop_up_status = win32clipboard.GetClipboardData().strip()
            win32clipboard.CloseClipboard()
            console.print(f"Status copiado: {pop_up_status}")

            linhas = pop_up_status.splitlines()
            cabecalho = linhas[0].split('\t')
            dados = linhas[1].split('\t')

            # if "autorizado o uso da nf-e" in pop_up_status.lower():
            if len(dados) < len(cabecalho):
                get_error_msg = await get_text_display_window(pop_up_status)
                if get_error_msg == "" or get_error_msg is None or get_error_msg ==".":
                    get_error_msg = "Nota sem mensagem de situação"
                console.print(f"Mensagem Rejeição: {get_error_msg}")
                return  {"sucesso": False, "retorno": f"{get_error_msg}"}    
            # elif "rejeicao" in pop_up_status.lower():
            elif len(dados) >= len(cabecalho):
                if "autorizado o uso da nf-e" in pop_up_status.lower():
                    return  {"sucesso": True, "retorno": f"Nota Lançada"}
                else: #if not "autorizado o uso da nf-e" in pop_up_status.lower() or "rejeicao" in pop_up_status.lower():
                    get_error_msg = await get_text_display_window(pop_up_status)
                    if (get_error_msg == "" or get_error_msg is None) and (len(dados) < len(cabecalho)):
                        get_error_msg = "Nota sem mensagem de situação"
                    return  {"sucesso": False, "retorno": f"{get_error_msg}"}
            
        else:
            current_try +=1
            await worker_sleep(15)
            continue

    return {"sucesso": False, "retorno": f"Número máximo de tentativas excedido ao tentar transmitir a nota"}


async def find_nop_divergence():
    #Varifica Divergencia de NOP na capa e no item
    try:
        await worker_sleep(2)
        app = Application().connect(class_name="TMessageForm", title="Confirm", timeout=60)
        main_window_confirm = app["TMessageForm"]
        main_window_confirm.set_focus()
        btn_yes = main_window_confirm.child_window(class_name="TButton", title="&Yes")
        btn_yes.click()
        pyautogui.click(916, 557)
    except:
        console.print("Sem tela de divergencia de NOP")


async def find_warning_nop_divergence():
    try:
        await worker_sleep(2)
        console.print('Possui warning de NOP dos itens diferente da capa da nota')
        app_warning = Application().connect(title="Warning", class_name="TMessageForm", timeout=10)
        main_window_warning = app_warning["Warning"]
        main_window_warning.child_window(class_name="TButton", title="&Yes").click()
    except:
        console.print(f'Não possui warning de NOP dos itens diferente da capa da nota')

