

import asyncio
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from pywinauto import Application
import pyautogui
import warnings
from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import type_text_into_field, wait_window_close, worker_sleep
from worker_automate_hub.utils.utils_nfe_entrada import EMSys
from rich.console import Console

from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    login_emsys,
    kill_process,
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


async def geracao_aprovacao_pedidos_34(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    filial_origem = "34"
    periodo = "1"
    retorno = await geracao_aprovacao_pedidos_processo(task=task, filial_origem=filial_origem, periodo=periodo)
    return retorno

async def geracao_aprovacao_pedidos_171(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    filial_origem = "171"
    periodo = "1"
    retorno = await geracao_aprovacao_pedidos_processo(task=task, filial_origem=filial_origem, periodo=periodo)
    return retorno

async def geracao_aprovacao_pedidos_processo(task: RpaProcessoEntradaDTO, filial_origem: str, periodo: str) -> RpaRetornoProcessoDTO:
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
        console.print(config)
        
        filialEmpresaOrigem = filial_origem
        periodo = periodo
        # Abre um novo emsys
        await kill_process("EMSys")
        
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task, filial_origem=filialEmpresaOrigem)
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
                    filialEmpresaOrigem, aprovacao_window["Edit2"], True, "0"
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
            console.print("Marcando campo selecionar empresas...")
            pyautogui.click(x=942, y=311)
            await worker_sleep(5)
            console.print("Clicando em pesquisar...") 
            pyautogui.click(x=1107, y=333)
            await worker_sleep(5)
            console.print("Selecionando todas as filiais...")
            pyautogui.click(x=720, y=615)
            await worker_sleep(5)
            console.print("Clicando em ok para confirmar...")
            pyautogui.click(x=1090, y=657)
            await worker_sleep(5)

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
            await worker_sleep(15)
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
            console.print("Clicando para selecionar todos os registros...")
            pyautogui.click(x=577, y=422)
            console.print("Aguardando processar...")
            await worker_sleep(30)
            pyautogui.click(x=1120, y=751)
            console.print("Clicando em aprovar...")
            await worker_sleep(30)
            console.print("clicando em OK em Motivo da aprovação da Negociação de Compra...")
            await emsys.verify_warning_and_error("Motivo da Aprovação da Negociação de Compra", "&Ok")
            await worker_sleep(10)
            console.print("Confirmando compra aprovada...")
            await emsys.verify_warning_and_error("Information", "OK")
            await emsys.verify_warning_and_error("Warning", "OK")
            await worker_sleep(10)
            console.print("Clicando em yes na janela de envio de email...")
            await emsys.verify_warning_and_error("Confirm", "&No")
            try:
                console.print("Aguardando janela de aguarde finalizar...")
                await wait_window_close("Aguarde...")
                await worker_sleep(5)
            except Exception as error:
                console.print("Janela de aguarde nao encontrada, tentando continuar")
                await worker_sleep(5)
            console.print("Tela de aguarde finalizada...")
            await worker_sleep(10)
            console.print("Marcando a primeira empresa da lista...")
            pyautogui.press("space")
            await worker_sleep(5)
            console.print("Clicando em OK...")
            await emsys.verify_warning_and_error("Seleção de Empresas", "&OK")
            await worker_sleep(5)
            console.print("Indo para janela de pré venda...")
            await worker_sleep(5)
            console.print("Fechando janela de aprovacao...")
            pyautogui.click(x=1329, y=277)
            await worker_sleep(5)
            type_text_into_field(
                "Gera Pré Venda com Pedido de Compra", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            await worker_sleep(3)
            pyautogui.press("enter", presses=2)
            await worker_sleep(5)
            pre_venda_window = app.top_window()
            console.print("Clicando em gerar pre venda...")
            pyautogui.click(x=1274, y=695)
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
            
            await worker_sleep(10)
            console.print("Clicando em aprovar venda...")
            pyautogui.click(x=1310, y=352)
            await worker_sleep(30)

            max_attempts = 80
            minimum_checks = 4
            checks = 0
            for _ in range(max_attempts):
                if app.window(title="Confirm").exists():
                    checks = 0
                    await emsys.verify_warning_and_error("Confirm", "&Yes")
                    try:
                        pre_venda_window.wait("ready", timeout=1000)
                    except:
                        console.print("timeout")
                if app.window(title="Warning").exists():
                    checks = 0
                    await emsys.verify_warning_and_error("Warning", "OK")
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
            console.print("Aguardando EMSys sincronizar... ( 15 minutos )")
            await worker_sleep(60*15)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Pre venda lancada com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso
            )
    except Exception as erro:
        console.print(erro)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro durante o processo geracao_aprovacao_pedidos, erro : {erro}",
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

