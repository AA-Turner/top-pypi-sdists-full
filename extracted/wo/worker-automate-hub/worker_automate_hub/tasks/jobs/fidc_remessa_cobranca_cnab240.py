import asyncio
import io
import os
import re
import shutil
import warnings
from datetime import datetime, timedelta


import pyperclip
import pyautogui
from pywinauto.application import Application
from rich.console import Console
from dateutil.relativedelta import relativedelta

from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from googleapiclient.discovery import build
from worker_automate_hub.utils.logger import logger
from pywinauto_recorder import set_combobox
from worker_automate_hub.api.client import get_config_by_name, get_valor_remessa_cobranca, send_file, sync_get_config_by_name
from worker_automate_hub.utils.util import (
    create_temp_folder,
    delete_folder,
    kill_all_emsys,
    login_emsys,
    save_pdf_emsys, 
    type_text_into_field,
    worker_sleep,
    set_variable,
    )

pyautogui.PAUSE = 0.5
ASSETS_BASE_PATH = 'assets/fidc/'
PDF_SUFFIX = "_PDF.pdf"
console = Console()



async def remessa_cobranca_cnab240(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    '''
       Processo FIDC - Remessa de Cobrança CNAB240
    '''
    try:
        #Setando tempo de timeout
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)
        
        #Pegando nome do usuario
        nome_usuario = os.environ.get('USERNAME') or os.environ.get('USER')
        nome_pasta = f"{nome_usuario}_arquivos"

        #Delete temp folder
        await delete_folder(nome_pasta)
        #Cria Pasta temporaria
        temp_folder = await create_temp_folder()
        temp_folder = temp_folder +'\\'
        #Pega Config para logar no Emsys
        config = await get_config_by_name("login_emsys")
        folders_paths = await get_config_by_name("Folders_Fidc")

        #Abre um novo emsys
        await kill_all_emsys()
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field('Remessa de Cobranca', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Retorno de Cobranca' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login
        
        await worker_sleep(10)
        
        # Identificando jenela principal
        app = Application().connect(title="Gera Arquivo Cobranca", backend="uia")
        main_window_arquivo_cobranca = app["Gera Arquivo Cobranca"]
        main_window_arquivo_cobranca.set_focus()

        # Digitando Cobrança
        cobranca = main_window_arquivo_cobranca.child_window(class_name="TDBIEditCode", found_index=2)
        console.print("Selecionando Cobrança", style='bold green')
        cobranca.type_keys("4")
        pyautogui.hotkey("tab") 
        await worker_sleep(5)
        pyautogui.press("down", presses=3, interval=0.5)
        await worker_sleep(2)
        pyautogui.hotkey("enter")

        await worker_sleep(10)
        
        # Identificando jenela principal
        app = Application().connect(title="Gera Arquivo Cobranca", backend="uia")
        main_window_arquivo_cobranca = app["Gera Arquivo Cobranca"]

        # Selecionando caminho do arquivo
        field_arquivo = main_window_arquivo_cobranca.child_window(class_name="TDBIEditString", found_index=0)
        text_field_arquivo = field_arquivo.window_text()
        new_text_field_arquivo = str(re.search(r'REM(.*)\.txt', text_field_arquivo).group(1))
        new_text_field_arquivo = 'R00102#####.001'.replace('#####', str(new_text_field_arquivo).zfill(5))
        field_arquivo.set_focus()
        
        field_arquivo.double_click_input()
        field_arquivo.set_edit_text("")
        # field_arquivo.type_keys(folders_paths.conConfiguracao['remessa_cobranca_path'] + new_text_field_arquivo, with_spaces=True)
        field_arquivo.type_keys(temp_folder + new_text_field_arquivo, with_spaces=True)

        await worker_sleep(2)   
        #Seleciona Banco
        pyautogui.click(810, 397)
        pyautogui.press("down", presses=2)

        pyautogui.hotkey("enter")
        
        # Data atual
        data_atual = datetime.now()

        # Data(8 dias atrás)
        start_date = data_atual - timedelta(days=8)
        # Data(1 dia atrás)
        end_date = data_atual - timedelta(days=1)


        #Data de emissão
        pyautogui.click(700, 482)
        pyautogui.write(start_date.strftime("%d%m%Y"))
        pyautogui.click(780, 485)
        pyautogui.write(end_date.strftime("%d%m%Y"))

        #Data Vencimento
        pyautogui.click(900, 485)
        pyautogui.write(datetime.now().strftime("%d%m%Y"))
        # pyautogui.write(start_date)
        pyautogui.click(1000, 485)
        pyautogui.write((datetime.now() + relativedelta(months=6)).strftime("%d%m%Y"))
        # pyautogui.write(end_date)

        filtro = main_window_arquivo_cobranca.child_window(class_name="TGroupBox", found_index=2)
        faturados_negociados = filtro.child_window(title="Faturados/Negociados", class_name="TRadioButton")
        faturados_negociados.click()
        somente_nosso_numero = main_window_arquivo_cobranca.child_window(title="Somente Títulos com Nosso Número",class_name="TCheckBox", found_index=0)
        somente_nosso_numero.click()

        # Clica Pesquisar Titulos
        pyautogui.click(1160, 548)

        await worker_sleep(10)

        #Clicando em sim para titulos
        pyautogui.click(920, 560)

        await worker_sleep(20)

        #Selecionando todas empresas na tela  Seleção de Empresa
        pyautogui.click(720, 620)

        #clcica em OK
        pyautogui.click(1100, 660)

        await worker_sleep(120)

        try:
            app = Application().connect(title="Informação", backend="uia")
            main_window_arquivo_cobranca = app["Informação"]
            if main_window_arquivo_cobranca.exists():
                return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno="Nenhum titulo encontrado para a remessa de cobrança!",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
        except Exception as ex:
            ...
        # Seleciona todos titulos
        pyautogui.click(1275, 600)
        # pyautogui.click(636, 591)
        
        await worker_sleep(10)

        # Pegando Total do Emsys
        app = Application().connect(title="Gera Arquivo Cobranca", backend="uia")
        main_window_arquivo_cobranca = app["Gera Arquivo Cobranca"]
        main_window_arquivo_cobranca.set_focus()
        field_total_emsys = main_window_arquivo_cobranca.child_window(class_name="TDBIEditNumber", found_index=3).window_text()
        #Pegando total do banco
        # total_db = await get_valor_remessa_cobranca(data_atual.strftime("%Y-%m-%d"))
        total_db = await get_valor_remessa_cobranca("2025-01-29")
        console.print("Total DB: " + str(total_db))
        console.print("Total EMSYS: " + str(field_total_emsys))
        field_total_emsys = 0
        total_db = 0
        if total_db == field_total_emsys:
            #Clica gerar cobrança
            await worker_sleep(5)
            pyautogui.click(1135, 789)
        else:
            log_msg = "Valores divergem! \nValor no EmSys: " + str(field_total_emsys) + " \nValor dos titulos: " + str(total_db)
            return RpaRetornoProcessoDTO(sucesso=False, 
                                         retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, 
                                         tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)])    

        await worker_sleep(10)

        # Confirma geração com sucesso
        max_try = 10
        current_try = 0
        while current_try <= max_try:
            try:
                app = Application().connect(title="Information", class_name="TMessageForm")
                window_cobranca = app["Information"]
                if window_cobranca.exists():
                    #Click OK
                    window_cobranca.set_focus()
                    await worker_sleep(1)
                    pyautogui.click(958, 560)
                    break
            except Exception as ex:
                log_msg = f"Erro ao encontrar janela de confirmação de cobrança: {str(ex)}"
                console.print(log_msg, style="bold red")
                
            current_try += 1
            await worker_sleep(20)
            
        if current_try >= max_try:
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])    

        # # Substituindo arquivo original e fazedno upload (feito logo apos gerar para  garaintir que o arquivo não se perca)
        # origem = folders_paths.conConfiguracao['remessa_cobranca_path'] + new_text_field_arquivo
        origem = temp_folder + new_text_field_arquivo
        
        # Abrindo o arquivo original para leitura
        file = open(origem, 'r')
        file_text = file.read()
        file.close()
        # Realizando as substituições
        file_text = file_text.replace(
        '074737350001813576383             0316820000000058114 SIM REDE DE POSTOS LTDA',
        '45931917000148003576383001417019  0316820000000058114 ARGENTA FUNDO DE INVEST').replace(
        '20074737350001813576383             0316820000000058114 SIM REDE DE POSTOS LTDA',
        '2045931917000148003576383001417019  0316820000000058114 ARGENTA FUNDO DE INVEST')
        # Sobrescrevendo o arquivo original com o conteúdo alterado
        file = open(origem, 'w')
        file.write(file_text)
        file.close()

        console.print(f"Substituições realizadas com sucesso no arquivo original: {origem}")
        try:
            with open(origem, 'rb') as file:
                file_bytes = io.BytesIO(file.read())
            # Enviando o arquivo 001 para BOF
            await send_file(task.historico_id, new_text_field_arquivo, "001", file_bytes, file_extension="001")
        except Exception as e:
            log_msg=(f"Erro ao enviar o arquivo 001: {e}")
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])


        # Clica em 'Yes' imprimir listagem
        await worker_sleep(10)
        try:
            app = Application().connect(title="Confirm", class_name="TMessageForm")
            window_listagem_alfabetica = app["Confirm"]
            if window_listagem_alfabetica.exists():
                window_listagem_alfabetica.set_focus()
                yes_btn = window_listagem_alfabetica.child_window(title="&Yes", class_name="TButton")
                yes_btn.click()
        except Exception as ex:
            log_msg = f"Erro ao encontrar janela de impressão de listagem: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        
        #Clica em "Yes" ordem alfabética
        await worker_sleep(10)
        try:
            app = Application().connect(title="Confirm", class_name="TMessageForm")
            window_listagem_alfabetica = app["Confirm"]
            if window_listagem_alfabetica.exists():
                window_listagem_alfabetica.set_focus()
                yes_btn = window_listagem_alfabetica.child_window(title="&Yes", class_name="TButton")    
                yes_btn.click()  
        except Exception as ex:
            log_msg = f"Erro ao encontrar janela de impressão de listagem em ordem alfabética: {str(ex)}"
            console.print(log_msg, style="bold red")            
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])

        await worker_sleep(10)
        
        # await save_pdf_emsys(folders_paths.conConfiguracao['remessa_cobranca_path'] + new_text_field_arquivo +" (PDF)")
        await save_pdf_emsys(temp_folder + new_text_field_arquivo + PDF_SUFFIX)
        
        await worker_sleep(5) 

        #Clica para não imprimir os boletos
        try:
            app = Application().connect(title="Confirm", class_name="TMessageForm")
            window_listagem_alfabetica = app["Confirm"]
            if window_listagem_alfabetica.exists():
                window_listagem_alfabetica.set_focus()
                pyautogui.click(998, 562)
        except Exception as ex:
            log_msg = f"Erro ao encontrar janela 'deseja imprimir os boletos?': {str(ex)}"
            console.print(log_msg, style="bold red")            
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
                
        try:
            # Enviando arquivo PDF para BOF
            with open(temp_folder + new_text_field_arquivo + PDF_SUFFIX, 'rb') as file:
                file_bytes_pdf = io.BytesIO(file.read())
            await send_file(task.historico_id, new_text_field_arquivo, "pdf", file_bytes_pdf, file_extension="pdf")
        except Exception as e:
            log_msg=(f"Erro ao enviar o arquivo PDF: {e}")
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        
        try:
            #Mover para pasta correta
            shutil.move(origem, folders_paths.conConfiguracao["remessa_cobranca_path_prod"])
        except Exception as e:
            log_msg=(f"Erro ao mover o arquivo para pasta de remessa: {e}")
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
    
        #Delete temp folder
        await delete_folder(nome_pasta)
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo Remessa de Cobranca CNAB240 concluido com sucesso",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:
        log_msg = f"Erro Processo Remessa de Cobranca CNAB240: {str(ex)}"
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
        sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])