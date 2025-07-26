import time
import pyautogui
from datetime import datetime
import sys
import os
import sys
import os
from pywinauto.keyboard import send_keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


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


def click_desconfirmar():
    cords = (675, 748)
    pyautogui.click(x=cords[0], y=cords[1])


def ctrl_c():
    pyautogui.press("tab", presses=12)  # verificar
    pyautogui.hotkey("ctrl", "c")
    return pyperclip.paste()


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

        await worker_sleep(4)

        try:
            app = Application(backend="win32").connect(
                class_name="TFrmLoginModulo", timeout=50
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
            console.print("Navegando para Livros Fiscais")
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            main_window = app["TFrmPrincipalFiscal"]
            main_window.set_focus()
            input_livros = main_window.child_window(class_name="TEdit", found_index=0)
            type_text_into_field(
                "Livros Fiscais", input_livros, True, "50"
            )
            await worker_sleep(5)

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

            # Clicar no input inicial 
            input_livros = main_window.child_window(class_name="TEdit", found_index=0).click_input()
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("down")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                "\nPesquisa: 'Livros Fiscais' realizada com sucesso.",
                style="bold green",
            )
            
            await worker_sleep(10) 
                               
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
            
            await worker_sleep(2)

            ##### Janela Principal ####
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            main_window = app["TFrmPrincipalFiscal"]
            main_window.set_focus()
            
            # Clicar no input inicial 
            input_livros = main_window.child_window(class_name="TEdit", found_index=0).click_input()
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("down")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                "\nPesquisa: 'Livros Fiscais' realizada com sucesso.",
                style="bold green",
            )
            
            await worker_sleep(10)
            
            ##### janela Movimento de Livro Fiscal #####
            app = Application().connect(class_name="TFrmMovtoLivroFiscal", timeout=20)
            main_window = app["TFrmMovtoLivroFiscal"]
            main_window.set_focus()
            data_input = main_window.child_window(class_name="TDBIEditDate", found_index=0)
            competencia = task.configEntrada.get("periodo")
            type_text_into_field(
                competencia, data_input, True, "50"
            )

            # Preenchendo campo competencia
            console.print("Preenchendo campo competencia...")
            pyautogui.press("tab")
            competencia = task.configEntrada.get("periodo")
            pyautogui.write(competencia)
            await worker_sleep(3)

            # Marcando caixa Entrada
            console.print("Marcando caixa entrada")
            entrada = main_window.child_window(class_name="TcxCheckBox", found_index=9).click_input()

            # Marcando caixa Saida
            console.print("Marcando caixa saida")
            saida = main_window.child_window(class_name="TcxCheckBox", found_index=8).click_input()
        
            await worker_sleep(2)

            # Clicando em incluir livro
            try:
                console.print("Clicando em incluir livro")
                cords = (695, 729)
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
            app = Application().connect(class_name="TPerguntasLivrosFiscaisForm", timeout=20)
            main_window = app["TPerguntasLivrosFiscaisForm"]
            main_window.set_focus()
            console.print("Clicando sim em janela somar os valores de IPI Frete")
            main_window.child_window(class_name="TDBIComboBoxValues", found_index=0).click_input()

            await worker_sleep(1)        
            send_keys("Sim{ENTER}")
            await worker_sleep(2)  
            
            console.print("Clicando sim em janela gerar Numero de Serie do SAT")
            main_window.child_window(class_name="TDBIComboBoxValues", found_index=4).click_input() 
        
            await worker_sleep(1)       
            send_keys("Sim{ENTER}")
            await worker_sleep(2)  

            console.print("Clicando sim em janela gerar Numero de Serie a partir da chave do documento")
            main_window.child_window(class_name="TDBIComboBoxValues", found_index=1).click_input()
            
            await worker_sleep(1)      
            send_keys("Sim{ENTER}")
            await worker_sleep(2)  

            console.print("Clicando sim em janela gerar livro com observação da nota fiscal")
            main_window.child_window(class_name="TDBIComboBoxValues", found_index=3).click_input() 
        
            await worker_sleep(1)       
            send_keys("Sim{ENTER}")
            await worker_sleep(2)  

            console.print("Clicando sim em janela somar valores de ICMS...")
            main_window.child_window(class_name="TDBIComboBoxValues", found_index=2).click_input()
            
            await worker_sleep(1)    
            send_keys("Sim{ENTER}")  

            await worker_sleep(2)

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

            # try:
            #     # Esperando janela aguarde
            #     console.print("Aguardando tela de aguarde ser finalizada")
            #     await wait_aguarde_window_closed(app)
            #     await worker_sleep(5)
            # except:
            #     pass
            
            await worker_sleep(5)

            ##### Janela Pré-visualizando Relatório #####
            console.print("Fechar Janela Pré-visualizando Relatório ")
            app = Application().connect(class_name="TFrmPreviewRelatorio", timeout=60)
            main_window = app["TFrmPreviewRelatorio"]
            main_window.set_focus()

            # Clicar em fechar
            main_window.close()

            await worker_sleep(3)

            ##### Janela Principal ####
            console.print("Navegando para Livro de Apuração ICMS... ")
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            input_principal = main_window = app["TFrmPrincipalFiscal"]
            input_principal.set_focus()
            input_livros = input_principal.child_window(class_name="TEdit", found_index=0)
            type_text_into_field(
                "Livro de Apuração ICMS", input_livros, True, "50"
            )
            await worker_sleep(5)

            try:
                ##### Janela Confirm #####
                app = Application().connect(class_name="TMessageForm", timeout=60)
                main_window = app["TMessageForm"]
                main_window.set_focus()
                main_window.child_window(class_name="TButton", found_index=0).click_input()
            except:
                pass
            console.print("Selecionar Livro de Apuração")
            input_livros = input_principal.child_window(class_name="TEdit", found_index=0).click_input()
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")

            await worker_sleep(5)

            ##### Janela Movimentação de Apuração ICMS #####
            app = Application().connect(class_name="TFrmMovtoApuraIcmsNew", timeout=60)
            main_window = app["TFrmMovtoApuraIcmsNew"]
            main_window.set_focus()

            console.print("Clicando no último livro, primeira linha")
            pyautogui.click(599,410)
            
            await worker_sleep(1)

            console.print("Clicando em Estornar Livro")   
            pyautogui.click(667,742)

            await worker_sleep(3)

            main_window.close()

            await worker_sleep(2)

            console.print("Selecionar Livro Saída aberto")
            
            # Selecionar linha livro de saída aberto
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\livro_saida_aberto.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)

            if localizacao:
                print(f"Imagem livro de saída aberto encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
            else:
                console.print("Imagem livro de saída aberto não encontrado na tela.")

            # Clicar em alterar livro
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\alterar_livro.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)  # você pode ajustar o confidence

            if localizacao:
                print(f"Imagem alterar livro encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
            else:
                console.print("Imagem alterar livro não encontrada na tela.")

            await worker_sleep(4)

            # Clicar em Livro fiscal
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\livro_fiscal.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)  # você pode ajustar o confidence

            if localizacao:
                print(f"Imagem Livro fiscal encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
            else:
                console.print("Imagem Livro fiscal não encontrada na tela.")
            
            await worker_sleep(4)
            
            # Clicar em Gerar Relatório
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\gerar_registros.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)  # você pode ajustar o confidence

            if localizacao:
                print(f"Imagem gerar relatório encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
            else:
                console.print("Imagem gerar relatório não encontrada na tela.")

            ##### Janela Gerar Registro ####
            console.print("Confirmar Registro")
            app = Application().connect(class_name="TMsgBox", timeout=60)
            main_window = app["TMsgBox"]
            main_window.set_focus()
            
            # Clicar em Sim
            main_window.child_window(class_name="TBitBtn", found_index=1).click_input()

            await worker_sleep(4)

            console.print("Clicar em confirmar")
            app = Application().connect(class_name="TPerguntasLivrosFiscaisForm", timeout=60)
            main_window = app["TPerguntasLivrosFiscaisForm"]
            main_window.set_focus()
            main_window.child_window(class_name="TButton", found_index=1).click_input()

            # Caminho da imagem que deve desaparecer
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\janela_carregada.png"

            # Tempo máximo de espera (em segundos)
            tempo_limite = 600  # 10 minutos
            intervalo = 2  # segundos entre as verificações

            inicio = time.time()

            while True:
                localizacao = pyautogui.locateOnScreen(imagem, confidence=0.9)

                if not localizacao:
                    print("Imagem desapareceu da tela.")
                    break  # A imagem sumiu, podemos seguir

                if time.time() - inicio > tempo_limite:
                    print("Tempo esgotado. A imagem não desapareceu.")
                    break

                print("Imagem ainda presente... aguardando")
                time.sleep(intervalo)

            ##### Janela Principal ####
            console.print("Navegando para Livro de Apuração ICMS... ")
            app = Application().connect(class_name="TFrmPrincipalFiscal", timeout=60)
            input_principal = main_window = app["TFrmPrincipalFiscal"]
            input_principal.set_focus()
            input_livros = input_principal.child_window(class_name="TEdit", found_index=0)
            type_text_into_field(
                "Livro de Apuração ICMS", input_livros, True, "50"
            )
            await worker_sleep(5)

            app = Application().connect(class_name="TFrmMovtoApuraIcmsNew", timeout=60)
            main_window = app["TFrmMovtoApuraIcmsNew"]
            main_window.set_focus()
            data_input = main_window.child_window(class_name="TDBIEditDate", found_index=0)
            competencia = competencia #task.configEntrada.get("periodo")
            type_text_into_field(
                competencia, data_input, True, "50"
            )
            
            # Clicar em incluir apuração
            imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\abertura_livros\btn_incluir_apuracao.png"

            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.9)  # você pode ajustar o confidence

            if localizacao:
                print(f"Imagem incluir apuração encontrado em: {localizacao}")
                pyautogui.moveTo(localizacao)
                pyautogui.click()
            else:
                console.print("Imagem incluir apuração não encontrada na tela.")

    except Exception as erro:
        console.print(f"Erro ao executar abertura de livros fiscais, erro : {erro}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na Abertura de Livro Fiscal : {erro}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
