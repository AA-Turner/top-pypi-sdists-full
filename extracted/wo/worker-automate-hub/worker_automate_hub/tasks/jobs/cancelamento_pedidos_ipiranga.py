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
import asyncio
from datetime import date, datetime
import re
from playwright.async_api import async_playwright
from worker_automate_hub.api.client import get_config_by_name, get_mfa_code, get_codigo_raizen_by_cnpj
from worker_automate_hub.utils.util import capture_and_send_screenshot, ensure_browsers_installed, kill_all_emsys, worker_sleep

console = Console()

def log_step(step, msg):
    console.print(f"[bold cyan][STEP {step}][/bold cyan] {msg}")

def log_ok(msg):
    console.print(f"[bold green][OK][/bold green] {msg}")

def log_error(msg):
    console.print(f"[bold red][ERRO][/bold red] {msg}")

async def cancelamento_pedidos_ipiranga(task: RpaRetornoProcessoDTO):

    browser = None

    try:
        log_step(1, "Inicializando robô")

        await ensure_browsers_installed()
        await kill_all_emsys()

        config_entrada = task.configEntrada

        login_config = await get_config_by_name("ConsultaPreco")
        login_config = login_config.conConfiguracao

        cnpj_empresa = str(config_entrada.get("cnpjEmpresa", "")).strip()
        numero_pedido = str(config_entrada.get("numeroPedido", "")).strip()

        if not cnpj_empresa:
            raise ValueError("cnpjEmpresa não informado.")

        if not numero_pedido:
            raise ValueError("numeroPedido não informado.")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-infobars",
                    "--window-size=1920,1080",
                ],
            )

            page = await browser.new_page()
            await page.set_viewport_size({"width": 1850, "height": 900})

            # ========================
            # LOGIN
            # ========================
            log_step(2, "Acessando site Ipiranga")

            await page.goto(login_config.get("url_ipiranga"), wait_until="load", timeout=90000)

            await page.wait_for_selector('[title="Login"]', timeout=90000)

            log_step(3, "Realizando login")

            await page.locator('[title="Login"]').fill(login_config.get("login_ipiranga"))
            await page.locator('[type="password"]').fill(login_config.get("pass_ipiranga"))
            await page.locator('[type="submit"]').click()

            try:
                await page.wait_for_selector(
                    "//ul[contains(@style, '#ffd000')]/li[contains(text(), 'Usuário ou senha incorretos.')]",
                    timeout=10000,
                )

                log_error("Login inválido")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Login failed.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            except:
                log_ok("Login realizado com sucesso")

            # ========================
            # COOKIES / POPUPS
            # ========================
            log_step(4, "Tratando popups")

            try:
                await page.locator("#onetrust-accept-btn-container").click()
                log_ok("Cookies aceitos")
            except:
                pass

            for selector in [".newclose", "img.fechar"]:
                try:
                    await page.locator(selector).click()
                except:
                    pass

            # ========================
            # SELEÇÃO DE POSTO
            # ========================
            log_step(5, f"Selecionando posto {cnpj_empresa}")

            await page.wait_for_selector(".usuario_img", timeout=90000)
            await page.locator(".usuario_img").first.click()

            input_cnpj = page.locator('[type="text"]').first

            await input_cnpj.click()
            await worker_sleep(1)

            await input_cnpj.type(cnpj_empresa, delay=100)

            posto = page.locator("li.posto_lista_item").filter(has_text=cnpj_empresa)

            await posto.first.wait_for(state="visible", timeout=30000)

            await posto.first.locator("button:has-text('Trocar')").click()

            log_ok("Posto selecionado")

            await page.wait_for_timeout(3000)

            # ========================
            # IR PARA PEDIDOS
            # ========================
            log_step(6, "Acessando tela de pedidos")

            await page.goto(
                "https://www.redeipiranga.com.br/wps/myportal/redeipiranga/pedidos/combustivel/meuspedidos/",
                wait_until="load",
                timeout=90000,
            )

            frame = page.frame_locator(
                '//*[@id="ns_Z7_LA04H4G0P0LT906ENDVD0I3GS2__content-frame"]'
            )

            # ========================
            # CONSULTAR PEDIDO
            # ========================
            log_step(7, f"Consultando pedido {numero_pedido}")

            await frame.locator("#numeroPedido").fill(numero_pedido)
            await frame.locator("#btnConsultar").click()

            await page.wait_for_timeout(5000)

            # Valida se pedido não foi encontrado
            pedido_nao_encontrado = frame.locator(
                "text=Não foi encontrado pedido com o filtro preenchido!"
            )

            if await pedido_nao_encontrado.count() > 0:
                msg = await pedido_nao_encontrado.first.text_content()
                msg = msg.strip()

                log_error(f"Pedido não encontrado: {numero_pedido}")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pedido {numero_pedido} não encontrado. Mensagem do portal: {msg}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            # ========================
            # CANCELAR
            # ========================
            log_step(8, "Cancelando pedido")

            cancel_btn = frame.locator("#btn-abrir-cancelar-modal")

            await cancel_btn.wait_for(state="visible", timeout=30000)
            await cancel_btn.scroll_into_view_if_needed()
            await cancel_btn.click()

            await page.wait_for_timeout(3000)

            await frame.locator("#justificativaCancelamento").select_option(
                "Erro no registro do pedido"
            )

            await frame.locator("#btn-cancelar-modal").click()

            await page.wait_for_timeout(5000)

            cancelation_message = (
                await frame.locator(".alert-success p").text_content()
            ).strip()

            if "sucesso" in cancelation_message.lower():
                log_ok(f"Pedido cancelado com sucesso: {cancelation_message}")

                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Pedido cancelado com sucesso.",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )


            log_error("Cancelamento não confirmado")

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=cancelation_message,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

    except Exception as e:
        log_error(f"Erro no fluxo: {e}")

        try:
            await capture_and_send_screenshot(
                task.historico_id,
                "Erro cancelamento Ipiranga",
            )
        except:
            pass

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=str(e),
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    finally:
        if browser:
            await browser.close()