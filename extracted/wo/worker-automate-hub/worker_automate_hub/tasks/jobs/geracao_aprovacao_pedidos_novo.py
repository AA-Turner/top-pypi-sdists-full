import asyncio
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from pywinauto import Application
from datetime import datetime
import pyautogui
from pywinauto.findwindows import ElementNotFoundError
import time
import warnings
from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import kill_all_emsys, type_text_into_field, wait_window_close, worker_sleep
from worker_automate_hub.utils.utils_nfe_entrada import EMSys
from rich.console import Console

from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    login_emsys,
    set_variable
)
from pytesseract import image_to_string
from PIL import ImageFilter, ImageEnhance
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
        print(f"Error: {error}")



async def geracao_aprovacao_pedidos_processo(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
        console.print(config)
        
        if task.uuidProcesso == "c8527e90-c65b-4d68-b4cf-25008b678957":
            empresa = "34"
            periodo = "1"
        elif task.uuidProcesso == "260380b7-a3e5-4c23-ab69-b428ee552830":
            empresa = "171"
            periodo = "1"
        else:
            console.print("Empresa não encontrada")
        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()
        
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task, filial_origem=empresa)
        main = app.top_window()
        main.set_focus()

        if return_login.sucesso == True:
            console.print("Indo para aprovação de negociação de compra...")
            type_text_into_field(
                "Aprovação de Negociação", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            await worker_sleep(3)
            pyautogui.press("enter", presses=2)
            await worker_sleep(4)
            aprovacao_window = app.top_window()
            try:
                console.print("Preenchendo campo periodo de dias...")
                aprovacao_window.Edit3.set_text(periodo)
            except Exception as erro:
                console.print(erro)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            try:
                console.print("Preenchendo o campo filial...")
                type_text_into_field(
                    empresa, aprovacao_window["Edit2"], True, "0"
                )
                await worker_sleep(5)
                send_keys("{ENTER}")
            except Exception as erro:
                console.print(erro)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            await worker_sleep(5)
            
            ##### Janela Aprovação de Negociação de Compra #####
            
            console.print("Marcando campo selecionar empresas...")
            app = Application(backend="win32").connect(
            class_name="TfrmAprovacaoNegociacao", found_index=0)
            main_window = app["TfrmAprovacaoNegociacao"]
            main_window.child_window(class_name="TCheckBox", found_index=0).click()
            
            await worker_sleep(2)
            empresa = "34"
            app = Application(backend="win32").connect(
            class_name="TfrmAprovacaoNegociacao", found_index=0)
            main_window = app["TfrmAprovacaoNegociacao"]
            console.print(f"Inserindo filial: {empresa}")
            input_fornecedor = main_window.child_window(class_name="TDBIEditCode", found_index=0)
            type_text_into_field(
                text=empresa,
                field=input_fornecedor,
                empty_before=True,
                chars_to_empty="3",
            )
            send_keys('{TAB}') 
            
            console.print("Clicando em pesquisar...") 
            pyautogui.click(x=1127, y=337)
            await worker_sleep(5)
            
            console.print("Selecionando todas as filiais...")
            pyautogui.click(x=720, y=620)
            await worker_sleep(5)

            
            ##### Janela Seleção de Empresa #####
            try:
                console.print("Clicando em ok para confirmar...")
                app = Application(backend="win32").connect(
                class_name="TFrmSelecionaEmpresas", found_index=0)
                main_window = app["TFrmSelecionaEmpresas"]
                main_window.child_window(class_name="TBitBtn", found_index=1).click_input()
                await worker_sleep(5)
            except:
                pass
            # tela de aguarde
            try:
                console.print("Aguardando janela de aguarde finalizar...")
                await wait_window_close("Aguarde...")
                await worker_sleep(5)
            except Exception as error:
                console.print("Janela de aguarde nao encontrada, tentando continuar")
                await worker_sleep(5)
            console.print("Tela de aguarde finalizada...")
            await worker_sleep(30)
            pyautogui.click(581, 425)
            await worker_sleep(20)
            # existe_pedidos = get_text_from_window(aprovacao_window, (40, 143, 105, 165), value="empresa")
            existe_pedidos = True
            if not existe_pedidos:
                console.print("Nenhum pedido encontrado...")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : Nao ha pedidos para o periodo",
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )
            
            await worker_sleep(30)
            
            ##### Janela Aprovação de Negociação de Compra #####
            
            console.print("Clicando para selecionar todos os registros...")
            pyautogui.click(x=579, y=430)
            
            console.print("Aguardando processar...")
            await worker_sleep(30)
            
            console.print("Clicando em aprovar...")
            pyautogui.click(x=1120, y=753)

            await worker_sleep(5)
            
            try:
                ##### Janela Motivo da Aprovação da Negociação de Compra #####
                
                console.print("clicando em OK em Motivo da aprovação da Negociação de Compra...")
                app = Application(backend="win32").connect(
                class_name="TFrmInputBoxText", found_index=0)
                main_window = app["TFrmInputBoxText"]
                main_window.set_focus()
                main_window.child_window(class_name="TBitBtn", found_index=1).click_input()
            except:
                pass
            await worker_sleep(20)
            
            ##### Janela Information #####
            
            console.print("Confirmando compra aprovada...")
            app = Application(backend="win32").connect(
            class_name="TMessageForm", found_index=0)
            main_window = app["TMessageForm"]
            main_window.child_window(class_name="TButton", found_index=0).click_input()
            
            await worker_sleep(10)
            
            ##### Janela Confirm #####
            console.print("Clicando em no na janela de envio de email...")
            app = Application(backend="win32").connect(
            class_name="TMessageForm", found_index=0)
            main_window = app["TMessageForm"]
            main_window.child_window(class_name="TButton", found_index=0).click_input()
            try:
                console.print("Aguardando janela de aguarde finalizar...")
                await wait_window_close("Aguarde...")
                await worker_sleep(5)
            except Exception as error:
                console.print("Janela de aguarde nao encontrada, tentando continuar")
                await worker_sleep(5)
            console.print("Tela de aguarde finalizada...")
            await worker_sleep(10)
            
            ##### Janela Seleção de Empresas #####
            max_wait_time = 1200  # 20 minutos em segundos
            start_time = time.time()

            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > max_wait_time:
                    raise TimeoutError("A janela 'TFrmSelecionaEmpresas' não apareceu após 20 minutos.")

                try:
                    app = Application(backend="win32").connect(class_name="TFrmSelecionaEmpresas", found_index=0)
                    main_window = app.window(class_name="TFrmSelecionaEmpresas")
                    main_window.wait("exists ready", timeout=5)
                    print("Janela encontrada e pronta.")
                    break
                except (ElementNotFoundError, TimeoutError):
                    print("Aguardando janela 'TFrmSelecionaEmpresas' aparecer...")
                    time.sleep(2)
            
            console.print("Marcando a primeira empresa da lista...")
            pyautogui.click(x=689, y=438)
            
            await worker_sleep(2)
            
            console.print("Clicando em OK...")
            app = Application(backend="win32").connect(
            class_name="TFrmSelecionaEmpresas", found_index=0)
            main_window = app["TFrmSelecionaEmpresas"]
            main_window.child_window(class_name="TBitBtn", found_index=1).click_input()
            
            await worker_sleep(5)
            
            ##### Janela Aprovação de Negociação #####
            console.print("Indo para janela de pré venda...")
            await worker_sleep(5)
            console.print("Fechando janela de aprovacao...")
            pyautogui.click(x=1331, y=280)
            
            await worker_sleep(5)
            
            ##### Janela Principal #####
            
            app = Application(backend="win32").connect(
            class_name="TFrmMenuPrincipal", found_index=0)
    
            type_text_into_field(
            "Gera Pré Venda com Pedido de Compra", app["TFrmMenuPrincipal"]["Edit"], True, "50")
            
            await worker_sleep(3)
            
            pyautogui.press("enter", presses=2)
            
            await worker_sleep(5)           
            
            ##### Janela Importar Pedido de compra para Pré Venda #####
            
            pre_venda_window = app.top_window()

            console.print("Clicando em gerar pre venda...")
            pyautogui.click(x=1291, y=693)
            
            await worker_sleep(20)
            
            console.print("Confirmando janela...")
            await emsys.verify_warning_and_error("Confirm", "&Yes")
            await worker_sleep(5)#20
            console.print("Selecionando segunda opção da janela Seleção do Tipo de Preço...")
            pyautogui.click(x=852, y=522)
            await worker_sleep(5)
            console.print("Confirmando opção...")
            pyautogui.press("enter")
            pre_venda_window.wait("ready", timeout=1000)
            await worker_sleep(10)
            console.print("Confirmando janela de pré venda gerada...")
            await emsys.verify_warning_and_error("Information", "OK")
            await emsys.verify_warning_and_error("Information", "&OK")
            await worker_sleep(20)
            console.print("Confirmando janela...")
            await emsys.verify_warning_and_error("Confirm", "&Yes")
            pre_venda_window.wait("ready", timeout=1000)
            await worker_sleep(30)
            try:
                pre_venda_window = app.window("Pré Venda")
                pre_venda_window.wait("ready", timeout=1000)
                await worker_sleep(5)
            except:
                pre_venda_window = app.top_window()
                await worker_sleep(30)
                
            await worker_sleep(5)
            console.print("Clicando em confirmar pre-venda...")
            pyautogui.click(x=1299, y=333)
            await worker_sleep(10)
            # 22 - 25
            max_attempts = 80
            minimum_checks = 4
            checks = 0
            for _ in range(max_attempts):
                if app.window(title="Confirm").exists():
                    checks = 0
                    await emsys.verify_warning_and_error("Confirm", "&Yes")
                    await emsys.verify_warning_and_error("Confirm", "Yes")
                    try:
                        pre_venda_window.wait("ready", timeout=1000)
                    except:
                        console.print("timeout")
                if app.window(title="Warning").exists():
                    checks = 0
                    await emsys.verify_warning_and_error("Warning", "OK")
                    await emsys.verify_warning_and_error("Warning", "&OK")
                    try:
                        pre_venda_window.wait("ready", timeout=1000)
                    except:
                        console.print("timeout")
                if app.window(title="Information").exists():
                    checks = 0
                    await emsys.verify_warning_and_error("Information", "OK")
                    try:
                        pre_venda_window.wait("ready", timeout=1000)
                    except:
                        console.print("timeout")
                if app.window(title="Error").exists():
                    checks = 0
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
                        status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                    )
                if checks >= minimum_checks:
                    break
                checks = checks + 1
                await worker_sleep(2)
            
            max_attempts = 80
            minimum_checks = 4
            checks = 0

            for _ in range(max_attempts):
                janela_confirm = app.window(title="Confirm")

                if janela_confirm.exists(timeout=1):  # espera 1s a cada tentativa
                    checks = 0

                    try:
                        janela_confirm.set_focus()
                        janela_confirm.restore()  # garante que está visível
                    except Exception as e:
                        print(f"Erro ao dar foco: {e}")
                        continue

                    # Tenta clicar até 4 vezes com intervalo de 5s
                    for _ in range(4):
                        try:
                            await emsys.verify_warning_and_error("Confirm", "&Yes")
                            break  # Sai do loop se clicar com sucesso
                        except Exception as e:
                            print(f"Tentativa de clique falhou: {e}")
                            time.sleep(5)
                    break  # Sai do loop principal após tentar clicar
                else:
                    checks += 1
                    if checks >= minimum_checks:
                        print("Janela 'Confirm' não apareceu após múltiplas tentativas.")
                        break
                time.sleep(1)


            for _ in range(max_attempts):
                if app.window(title="Information").exists():
                    checks = 0

                    # Traz a janela para frente
                    info_window = app.window(title="Information")
                    info_window.set_focus()

                    # Tenta clicar até 4 vezes com intervalo de 5s
                    for _ in range(4):
                        try:
                            await emsys.verify_warning_and_error("Information", "OK")
                            break  # Sai do loop se clicar com sucesso
                        except Exception as e:
                            print(f"Tentativa falhou: {e}")
                            time.sleep(5)
                    break  # Sai do loop principal se encontrou e tentou
                else:
                    checks += 1
                    if checks >= minimum_checks:
                        break
                time.sleep(1)
                    
            
            # await worker_sleep(10)
            # console.print("Clicando em aprovar venda...")
            # pyautogui.click(x=1310, y=352)
            # await worker_sleep(30)

            # max_attempts = 80
            # minimum_checks = 4
            # checks = 0
            # for _ in range(max_attempts):
            #     if app.window(title="Confirm").exists():
            #         checks = 0
            #         await emsys.verify_warning_and_error("Confirm", "&Yes")
            #         try:
            #             pre_venda_window.wait("ready", timeout=1000)
            #         except:
            #             console.print("timeout")
            #     if app.window(title="Warning").exists():
            #         checks = 0
            #         await emsys.verify_warning_and_error("Warning", "OK")
            #         try:
            #             pre_venda_window.wait("ready", timeout=1000)
            #         except:
            #             console.print("timeout")
            #     if app.window(title="Information").exists():
            #         checks = 0
            #         await emsys.verify_warning_and_error("Information", "OK")
            #         try:
            #             pre_venda_window.wait("ready", timeout=1000)
            #         except:
            #             console.print("timeout")
            #     if app.window(title="Error").exists():
            #         checks = 0
            #         return RpaRetornoProcessoDTO(
            #             sucesso=False,
            #             retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
            #             status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            #         )
            #     if checks >= minimum_checks:
            #         break
            #     checks = checks + 1
            #     await worker_sleep(2)
            # console.print("Aguardando EMSys sincronizar... ( 15 minutos )")
            # await worker_sleep(60*15)
            # return RpaRetornoProcessoDTO(
            #     sucesso=True,
            #     retorno="Pre venda lancada com sucesso",
            #     status=RpaHistoricoStatusEnum.Sucesso
            # )
    except Exception as erro:
        console.print(erro)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
        
if __name__ == "__main__":
    
    task = RpaProcessoEntradaDTO(
        datEntradaFila= datetime.now(),
        configEntrada= {
        "periodoInicial": "01/05/2025",
        "periodoFinal": "31/05/2025"
        },
        uuidProcesso='c8527e90-c65b-4d68-b4cf-25008b678957',
        nomProcesso='extracao_fechamento_emsys',
        uuidFila="",
        sistemas=[
            {
                "sistema": "EMSys",
                "timeout": "1.0"
            },
            {
                "sistema": "AutoSystem",
                "timeout": "1.0"
            }
        ],
        historico_id='2c4429c8-26ae-4ec6-b775-21583992e82f'
    )
    asyncio.run(geracao_aprovacao_pedidos_processo(task))