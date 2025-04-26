import asyncio
import warnings
from datetime import datetime, timedelta

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
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.util import (
    capture_and_send_screenshot,
    kill_all_emsys,
    kill_process, 
    login_emsys, 
    type_text_into_field, 
    worker_sleep,
    set_variable,
    )

ASSETS_BASE_PATH = 'assets/fidc/'
console = Console()



async def gerar_nosso_numero(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    '''
        Primeiro processo do Fidc, Geração do Nosso Número.
    '''
    try:
        #Setando tempo de timeout
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        #Pega Config para logar no Emsys
        config = await get_config_by_name("login_emsys")
        console.print(task)
        #Abre um novo emsys
        await kill_all_emsys()
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field('Impressao de Boletos', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Impressao de Boletos' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login
        
        await worker_sleep(10)
        #Identificando jenela principal
        app = Application().connect(title="Impressão de Boleto Título a Receber")
        main_window = app["Impressão de Boleto Título a Receber"]

        #Selecionando modelo
        model_select = main_window.child_window(class_name="TDBIComboBox", found_index=0)
        console.print("Selecionando 'BANCO DO BRASIL FIDC'...", style='bold green')
        if task.uuidProcesso == "29338b70-4ae6-4560-8aef-5d0d7095a527": #Banco do Brasil S.A
            model_select.select("BANCO DO BRASIL BOLETO")
        else: #Banco do Brasil FIDC
            model_select.select("BANCO DO BRASIL FIDC")
        await worker_sleep(2)

        #Periodo de Emissão
        emission_period = main_window.child_window(class_name="TGroupBox", found_index=2)
        emission_period_start = emission_period.child_window(class_name="TDBIEditDate", found_index=1)
        emission_period_end = emission_period.child_window(class_name="TDBIEditDate", found_index=0)

        # Data atual
        data_atual = datetime.now()
        # Data(8 dias atrás)
        start_date = data_atual - timedelta(days=8)
        # Data(1 dia atrás)
        end_date = data_atual - timedelta(days=1)
        
        emission_period_start.type_keys(start_date.strftime("%d%m%Y"))
        emission_period_end.type_keys(end_date.strftime("%d%m%Y"))

        await worker_sleep(2)

        #Seleciona chackboxes
        checkbox_pe = main_window.child_window(class_name="TDBICheckBox", found_index=3)
        checkbox_cupom_fiscal = main_window.child_window(class_name="TDBICheckBox", found_index=7)
        
        #Seleciona P.E.
        checkbox_pe.check()
        #Seleciona Cupom Fiscal
        checkbox_cupom_fiscal.check()

        # Clicando em pesquisar
        imprimir_titulos = pyautogui.locateOnScreen(ASSETS_BASE_PATH + 'gerar_nn_pesquisar.png', confidence=0.89)
        if imprimir_titulos:
            console.log("Pesquisando titulos" , style="bold green")
            pyautogui.click(imprimir_titulos)
            pyautogui.move(800,800)
        else:
            log_msg = "Botão Pesquisar não encontrado ou não habilitado!"
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

        await worker_sleep(20)
            
        # Clicando em Marcar Todos
        imprimir_titulos = pyautogui.locateOnScreen(ASSETS_BASE_PATH + 'gerar_nn_marcar_todos.png', confidence=0.89)
        if imprimir_titulos:
            console.print("Marcando todos titulos" , style="bold green")
            pyautogui.click(imprimir_titulos)
        else:
            log_msg = "Botão Marcar Todos não encontrado!"
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

        # Clicando em na coluna da tabela para ordenar os titulos com nosso número
        pyautogui.click(718,642, clicks=2, interval=1)
        
        await worker_sleep(1)

        # Indo para o ultimo titulo
        with pyautogui.hold('ctrl'):
            pyautogui.press('end')

        await worker_sleep(2)

        with pyautogui.hold('ctrl'):
            pyautogui.press('c')
        
        actual_line = pyperclip.paste()
        print(actual_line)
        try:
            if actual_line.split('\n')[1].split('\t')[2] != '':
                log_msg = "Todos os nossos numeros estao preenchidos!"
                console.print(log_msg, style="bold yellow")
                return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )
        except Exception as e:
            await capture_and_send_screenshot(task.historico_id, "Gerar_NN_Error.png")
            if "out of range" in str(e):
                log_msg = "Não foram encontrados títulos!"
                return RpaRetornoProcessoDTO(sucesso=True, retorno=log_msg, status=RpaHistoricoStatusEnum.Sucesso)
            else:
                log_msg = f"Erro desconhecido: {str(e)}"
                console.print(log_msg, style="bold red")
                return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        # Indo para o primeiro titulo
        with pyautogui.hold('ctrl'):
            pyautogui.press('home')
        
        while True:
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')

            actual_line = pyperclip.paste()

            #Se a Coluna "Nosso Numero" estiver populada desceleciona o dado
            if actual_line.split('\n')[1].split('\t')[2] != '':
                pyautogui.press('enter')
            #Se a Coluna "Nosso Numero" estiver vazia quebra o loop
            elif actual_line.split('\n')[1].split('\t')[2] == '':
                break

            pyautogui.press('down')
            console.log("Seguindo para próximo título.", style="bold yellow")
            await worker_sleep(1)
             
        #Clicando em Imprimir
        imprimir_titulos = pyautogui.locateOnScreen(ASSETS_BASE_PATH + 'gerar_nn_imprimir.png', confidence=0.89)
        if imprimir_titulos:
            console.log("Imprimindo titulos" , style="bold green")
            pyautogui.click(imprimir_titulos)
        else:
            rlog_msg = "Botão Imprimir não encontrado!"
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
        await worker_sleep(5)
        
        app = Application().connect(title="Warning")
        main_window = app["Warning"]

        console.print("Clicando em Yes, para andamento do processo...\n")
        btn_yes = main_window.child_window(title="&Yes")
        if btn_yes.exists() and btn_yes.is_enabled():
            btn_yes.click()
            await worker_sleep(7)
        else:
            log_msg = "Warning - Erro após clicar em Yes, na tela de warning...\n"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
    
        app = Application().connect(title="Seleciona Cobrança Bancária")
        main_window = app["Seleciona Cobrança Bancária"]
        code = main_window.child_window(class_name="TDBIEditCode", found_index=0)
        await worker_sleep(1)
        if task.uuidProcesso == "29338b70-4ae6-4560-8aef-5d0d7095a527": #Banco do Brasil S.A
            code.type_keys("1")
        else: #Banco do Brasil Fidc
            code.type_keys("4")
        pyautogui.hotkey("tab")

        button_ok = main_window.child_window(class_name="TBitBtn", found_index=0)
        button_ok.click()

        await worker_sleep(80)
        boleto_argenta = None
        max_trys = 5
        trys = 0
        while boleto_argenta == None and trys <= max_trys:
            try:
                app = Application().connect(title="BOLETO ARGENTA_1")
                boleto_argenta = app["BOLETO ARGENTA_1"]
                console.log("Boleto Argenta sendo fechado", style="bold green")
                boleto_argenta.close()
                break
            except:
                try:
                    app = Application().connect(title="BoletoBB-D.PostosLogista-MATRIZ")
                    boleto_argenta = app["BoletoBB-D.PostosLogista-MATRIZ"]
                    console.log("Boleto BB sendo fechado", style="bold green")
                    pyautogui.click(1147, 446)
                    break
                except:
                    console.print("Tela de boleto Argenta/BB ainda não encontrada", style="bold yellow")
            
            trys += 1
            await worker_sleep(60)
        
        #Verifica se tela Boleto Argenta foi fechada
        try:
            app = Application().connect(title="BOLETO ARGENTA_1")
            boleto_argenta = app["BOLETO ARGENTA_1"]
            console.log("Boleto Argenta sendo fechado", style="bold green")
            pyautogui.click(1147, 446)
        except:
            try:
                app = Application().connect(title="BoletoBB-D.PostosLogista-MATRIZ")
                boleto_argenta = app["BoletoBB-D.PostosLogista-MATRIZ"]
                console.log("Boleto BB sendo fechado", style="bold green")
                pyautogui.click(1147, 446)
            except:
                console.print("Tela de boleto Argenta/BB ainda não encontrada", style="bold yellow")
            
        await worker_sleep(5)
        #Confirmando tela de impressão
        #Clica em "Yes"
        # pyautogui.click(900, 561)
        #Clica em "No"
        pyautogui.click(1000, 561)

        await worker_sleep(5)

        if boleto_argenta != None:
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Nosso número gerado com sucesso!",
                status=RpaHistoricoStatusEnum.Sucesso
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao finalizar processo Gerar Nosso Número!",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
    except Exception as ex:
        log_msg = f"Erro Processo Gerar Nosso Número: {str(ex)}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
