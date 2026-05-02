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
from datetime import datetime
from playwright.async_api import async_playwright
from worker_automate_hub.api.client import get_config_by_name, get_mfa_code, get_codigo_raizen_by_cnpj
from worker_automate_hub.utils.util import (
    capture_and_send_screenshot,
    ensure_browsers_installed,
    kill_all_emsys,
    worker_sleep,
)

console = Console()


def log_step(step, msg):
    console.print(f"[bold cyan][STEP {step}][/bold cyan] {msg}")


def log_ok(msg):
    console.print(f"[bold green][OK][/bold green] {msg}")


def log_error(msg):
    console.print(f"[bold red][ERRO][/bold red] {msg}")


async def cancelamento_pedidos_raizen(task: RpaRetornoProcessoDTO):

    browser = None

    try:
        log_step(1, "Inicializando robô Raízen")

        await ensure_browsers_installed()
        await kill_all_emsys()

        config_entrada = task.configEntrada

        login_config = await get_config_by_name("ConsultaPreco")
        login_config = login_config.conConfiguracao

        cnpj_empresa = str(config_entrada.get("cnpjEmpresa", "")).strip()
        numero_pedido = str(config_entrada.get("numeroPedido", "")).strip()
        data_pedido = str(config_entrada.get("dataPedido", "")).strip()

        if not cnpj_empresa:
            raise ValueError("cnpjEmpresa não informado.")

        if not numero_pedido:
            raise ValueError("numeroPedido não informado.")

        if not data_pedido:
            raise ValueError("dataPedido não informado.")

        data_pedido_formatada = datetime.fromisoformat(data_pedido).strftime("%d/%m/%Y")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                slow_mo=100,
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
            log_step(2, "Acessando site Raízen")

            await page.goto(
                login_config.get("url_raizen"),
                wait_until="networkidle",
                timeout=90000,
            )

            log_step(3, "Realizando login")

            await page.locator("#signInName").fill(login_config.get("login_raizen"))
            await page.locator("#password").fill(login_config.get("pass_raizen"))
            await page.locator("#next").click()

            # ========================
            # MFA
            # ========================
            log_step(4, "Enviando código MFA")

            await page.locator("#readOnlyEmail_ver_but_send").click(timeout=60000)

            await asyncio.sleep(60)

            code = await get_mfa_code("mfa-raizen")

            if code.get("status_code") != 200:
                log_error("Falha ao buscar código MFA")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Falha ao buscar código MFA Raízen.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            log_ok("Código MFA recuperado")

            await page.locator("#readOnlyEmail_ver_input").fill(str(code.get("code")))
            await page.locator("#readOnlyEmail_ver_but_verify").click()

            await page.wait_for_timeout(5000)

            # ========================
            # SELEÇÃO DA EMPRESA
            # ========================
            log_step(5, f"Selecionando empresa CNPJ {cnpj_empresa}")

            relacao_cod_raizen = await get_codigo_raizen_by_cnpj(cnpj_empresa)

            if not relacao_cod_raizen:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"CNPJ {cnpj_empresa} não encontrado na configuração RelacaoCodigosRaizen.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            cod_cnpj = relacao_cod_raizen.lstrip("0")

            await page.wait_for_selector(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div',
                state="visible",
                timeout=90000,
            )

            await page.locator(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div'
            ).click()

            empresa = page.locator(f'text="{cod_cnpj} - SIM REDE DE POSTOS LTDA"')

            await empresa.wait_for(state="visible", timeout=60000)
            await empresa.scroll_into_view_if_needed()
            await empresa.click()

            await page.locator('//*[@id="undefined"]').click()
            await page.wait_for_load_state("load")

            log_ok("Empresa selecionada")

            # ========================
            # SELEÇÃO COMBUSTÍVEIS CLAROS
            # ========================
            log_step(6, "Selecionando Combustíveis Claros")

            try:
                await page.locator('//span[contains(text(), "Combustíveis Claros")]').click(
                    timeout=10000
                )
                await page.locator('//*[@id="undefined"]/div').click(timeout=10000)
                log_ok("Combustíveis Claros selecionado")
            except:
                log_ok("Tela de Combustíveis Claros não exigiu seleção")

            await page.wait_for_timeout(5000)

            # ========================
            # ACESSAR HISTÓRICO DE PEDIDOS
            # ========================
            log_step(7, "Acessando histórico de pedidos")

            await page.locator('//*[@id="pages-orders-orders-main"]').hover()
            await page.locator('//*[@id="spa-appv2-new-orders-history"]/span').click()

            await page.wait_for_timeout(5000)

            # ========================
            # CONSULTAR PEDIDO
            # ========================
            log_step(8, f"Consultando pedido {numero_pedido}")

            await page.locator( 
                '//*[@id="main-scroll"]/div/app-base-google-analytics/app-orders-history/div/div/app-orders-history-orders/div[1]/div/div/div/div[2]/form/div[1]/div[1]/input'
            ).type(numero_pedido)

            await page.locator(
                '//*[@id="main-scroll"]/div/app-base-google-analytics/app-orders-history/div/div/app-orders-history-orders/div[1]/div/div/div/div[2]/form/div[2]/div[1]/div[1]/input'
            ).type(data_pedido_formatada)

            await page.locator(
                '//*[@id="main-scroll"]/div/app-base-google-analytics/app-orders-history/div/div/app-orders-history-orders/div[1]/div/div/div/div[2]/form/div[2]/div[2]/div/input'
            ).type(data_pedido_formatada)

            await page.locator('//*[@id="btn-search"]').click()

            await page.wait_for_timeout(5000)

            # ========================
            # VALIDAR SE PEDIDO EXISTE
            # ========================
            botao_alterar = page.locator('//*[@id="btn-edit-order-0"]/i')

            if await botao_alterar.count() == 0:
                log_error("Botão de alterar pedido não encontrado")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pedido {numero_pedido} não encontrado ou não disponível para cancelamento.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            # ========================
            # CANCELAR PEDIDO
            # ========================
            log_step(9, "Abrindo pedido para cancelamento")

            await botao_alterar.first.click()

            await page.wait_for_timeout(10000)

            log_step(10, "Clicando em eliminar pedido")

            await page.locator('//*[@id="orders-fuels-button-delete"]').click(timeout=60000)

            await page.wait_for_timeout(3000)

            log_step(11, "Confirmando eliminação")

            await page.get_by_role("button", name="Eliminar").click(timeout=60000)

            await page.wait_for_timeout(5000)

            # ========================
            # CONFIRMAÇÃO
            # ========================
            log_step(12, "Capturando mensagem de confirmação")

            msg_locator = page.locator(".msgDuplicatedConfirm")

            await msg_locator.wait_for(state="visible", timeout=30000)

            msg = await msg_locator.text_content()
            msg = msg.strip() if msg else "Pedido eliminado com sucesso."

            log_ok(f"Retorno do portal: {msg}")

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Sucesso,
            )

    except Exception as e:
        log_error(f"Erro no fluxo: {e}")

        try:
            await capture_and_send_screenshot(
                task.historico_id,
                "Erro cancelamento Raizen",
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