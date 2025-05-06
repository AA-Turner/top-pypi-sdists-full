import asyncio
import io
import os
import warnings
from datetime import datetime, timedelta
import base64
import pyperclip
import pyautogui
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.models.dto.rpa_sistema_dto import RpaSistemaDTO
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.api.client import download_file_from_historico, get_config_by_name, send_file
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

ASSETS_BASE_PATH = 'assets/fidc/'
console = Console()



async def retorno_cobranca(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    '''
        Processo de retorno de cobrança e retorno de cobrança extraodinaria do FIDC
    '''
    if 'extraordinario' in task.nomProcesso:
        BASE_FILE_NAME = f'COB_001_240_3576383_{datetime.now().strftime("%y%m%d")}_N.ret'
    else:
        BASE_FILE_NAME = f'COB_001_240_3576383_{datetime.now().strftime("%y%m%d")}_00.ret'
    
    try:
        nome_usuario = os.environ.get('USERNAME') or os.environ.get('USER')
        nome_pasta = f"{nome_usuario}_arquivos"
        #Setando tempo de timeout
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)
        #Delete temp folder
        await delete_folder(nome_pasta)
        #Cria Pasta temporaria
        temp_folder = await create_temp_folder()
        console.print(f"Pasta criada com sucesso. \n {temp_folder}", style="bold green")
        try:
           downloaded_files =  await download_file_from_historico(task.historico_id)
        except Exception as ex:
            log_msg = f"Erro ao baixar o arquivo: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
            #Cria arquivo
        for file in downloaded_files:
            if file['tipo'].lower() == 'ret':
                decode = base64.b64decode(file['conteudo'])
                with open(os.path.join(temp_folder, BASE_FILE_NAME), 'wb') as f:
                    f.write(decode)
                break
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
            type_text_into_field('Retorno de Cobranca', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Retorno de Cobranca' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login
        
        await worker_sleep(5)

        #Digita Cobrança
        app = Application(backend='win32').connect(title="Processa Arquivo de Retorno de Cobrança")
        window_ret_cob = app['Processa Arquivo de Retorno de Cobrança']
        campo = window_ret_cob.child_window(class_name='TDBIEditCode')
        campo.set_focus()
        campo.type_keys('4')
        campo.type_keys('{TAB}')

        await worker_sleep(3)

        #Seleciona '0027'
        app = Application(backend='win32').connect(title="Busca Cobrança Banco")
        window_cob_banco = app['Busca Cobrança Banco']
        window_cob_banco.set_focus()
        for _ in range(3):
            window_cob_banco.type_keys('{DOWN}')
            await worker_sleep(1)
        window_cob_banco.type_keys('{ENTER}')
        
        await worker_sleep(5)

        #Digita caminho do arquivo
        app = Application(backend='win32').connect(title="Processa Arquivo de Retorno de Cobrança")
        window_ret_cob = app['Processa Arquivo de Retorno de Cobrança']
        file_path = window_ret_cob.child_window(class_name='TDBIEditString')
        file_path.set_text(f"{temp_folder}\\{BASE_FILE_NAME}")

        await worker_sleep(5)

        #Uncheck "Deduzir automaticamente taxa de cobrança"
        taxa_cobranca = window_ret_cob.child_window(class_name='TCheckBox', found_index=2)
        taxa_cobranca.click()

        await worker_sleep(5)

        #Alterar data da liquidação check
        taxa_cobranca = window_ret_cob.child_window(class_name='TCheckBox', found_index=1)
        taxa_cobranca.click()

        await worker_sleep(5)

        #Processar retorno
        console.print("Processando retorno")
        process_return = window_ret_cob.child_window(class_name='TBitBtn', found_index=4)
        process_return.set_focus()
        process_return.click()
        
        await worker_sleep(30)

        #Informar data de liquidação
        app = Application(backend='win32').connect(title="Information")
        window_info = app['Information']
        btn_ok = window_info.child_window(class_name='TButton')
        btn_ok.click()
        pyautogui.click(959, 558)

        await worker_sleep(10)

        #Confirmar Arquivo
        console.print("Confirmando Arquivo")
        app = Application(backend='win32').connect(title="Processa Arquivo de Retorno de Cobrança")
        window_ret_cob = app['Processa Arquivo de Retorno de Cobrança']
        btn_confirm = window_ret_cob.child_window(class_name='TBitBtn', found_index=2)
        btn_confirm.click()
        pyautogui.click(1146, 387)
        
        await worker_sleep(5)

        #Alterar Data de liquidação
        app = Application(backend='win32').connect(title="Retorno de Cobrança")
        window_ret_cob = app['Retorno de Cobrança']
        field_date = window_ret_cob.child_window(class_name='TDBIEditDate')
        btn_ok = window_ret_cob.child_window(title='&OK', class_name='TBitBtn')
        field_date.set_focus()
        field_date.type_keys(datetime.now().strftime("%d/%m/%Y"))
        # field_date.type_keys("11/01/2025")
        await worker_sleep(1)
        pyautogui.click(907, 566)

        await worker_sleep(5)

        #Confrima Alterar Data de liquidação
        try:
            app = Application(backend='win32').connect(title="Confirm")
            window_info = app['Confirm']
            pyautogui.click(917, 566)
        except Exception as ex:
            log_msg = f"Não houve tela de confirmação de alteração da data: {str(ex)}"
            logger.error(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            ) 
        

        await worker_sleep(5)

        #Registros confirmados
        try:
            app = Application(backend='win32').connect(title="Information")
            window_info = app['Information']
            pyautogui.click(952, 561)
        except Exception as ex:
            log_msg = f"Não houve tela para confirmar registros: {str(ex)}"
            logger.error(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(5)
        i = 0
        while i > 10:
            try:
                app = Application(backend='win32').connect(title="Warning")
                window_warning = app['Warning']
                window_warning.child_window(title='&No', class_name='TBitBtn').click()
                pyautogui.click(999,561)
            except Exception as ex:
                console.print("Sem cleintes bloqueados", style="bold green")
                break
            
        #Clica em "No" novamente por garantia
        pyautogui.click(999,561)
        await worker_sleep(5)

        #Imprimir
        try:
            app = Application(backend='win32').connect(title="Processa Arquivo de Retorno de Cobrança")
            window_ret_cob = app['Processa Arquivo de Retorno de Cobrança']
            pyautogui.click(1007, 375)
        except Exception as ex:
            log_msg = f"Não clicou em imprimir: {str(ex)}"
            logger.error(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(5)

        try:
            app = Application(backend="win32").connect(title="Print Preview")
        except Exception as ex:
            log_msg = f"Tela de prin preview não foi aberta corretamente: {str(ex)}"
            logger.error(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        
        await worker_sleep(5)

        await save_pdf_emsys(temp_folder + "\\" + BASE_FILE_NAME.replace(".ret", ".pdf"))

        await worker_sleep(5)

        try:
            with open(temp_folder + "\\" + BASE_FILE_NAME.replace(".ret", ".pdf"), 'rb') as file:
                file_bytes = io.BytesIO(file.read())
            # Enviando o arquivo para o backoffices
            await send_file(task.historico_id, BASE_FILE_NAME.replace(".ret", ""), "pdf", file_bytes, file_extension="pdf")
        except Exception as ex:
            log_msg = f"Erro ao enviar o arquivo para o backoffices: {str(ex)}"
            logger.error(log_msg)
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await delete_folder(nome_pasta)

        log_msg = f"Sucesso ao executar retorno de cobrança"
        logger.error(log_msg)
        console.print(log_msg, style="bold green")
        return RpaRetornoProcessoDTO(
            sucesso=True, retorno=log_msg, status=RpaHistoricoStatusEnum.Sucesso, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
    except Exception as ex:
        log_msg = f"Erro Processo Retorno Cobranca: {str(ex)}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
