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
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.util import (
    capture_and_send_screenshot,
    ensure_browsers_installed,
    kill_all_emsys,
)

logger = Console()


async def inclusao_pedidos_ipiranga(task: RpaRetornoProcessoDTO):
    try:
        await ensure_browsers_installed()
        config_entrada = task.configEntrada
        await kill_all_emsys()
        # Collect configs
        config_entrada = task.configEntrada
        config = await get_config_by_name("ConsultaPreco")
        config = config.conConfiguracao
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

            # Going to Main page
            logger.print(f"Navigating to {config.get('url_ipiranga')}")
            await page.goto(config.get("url_ipiranga"), wait_until="load")
            # Wait page load
            await page.wait_for_load_state("load")
            # Wait for login
            await page.wait_for_selector('[title="Login"]', timeout=90000)

            # Login
            logger.print(f"Logging")
            login = (
                config.get("login_ipiranga2")
                if config_entrada.get("cnpjEmpresa") == "07473735017661"
                else config.get("login_ipiranga")
            )
            password = (
                config.get("pass_ipiranga2")
                if config_entrada.get("cnpjEmpresa") == "07473735017661"
                else config.get("pass_ipiranga")
            )
            await page.locator('[title="Login"]').type(login)
            await page.locator('[type="password"]').type(password)
            await page.locator('[type="submit"]').click()
            try:
                await asyncio.sleep(5)
                warn = await page.wait_for_selector(
                    "//ul[contains(@style, '#ffd000')]/li[contains(text(), 'Usuário ou senha incorretos.')]",
                    timeout=10000,
                )
                if warn:
                    logger.print("Login failed. Verify username and password.")
                    await capture_and_send_screenshot(task.historico_id, "Erro")
                    raise Exception("Falha ao Logar no site.")
            except:
                logger.print("Login successful")

            # Warn to change password
            try:
                await page.wait_for_selector(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]',
                    timeout=5000,
                )
                await page.locator(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]'
                ).click()
            except:
                logger.print("No warning message.")

            # Wait and accept cookies
            logger.print("Identifiying cookies message")
            await page.wait_for_selector("#onetrust-accept-btn-container")
            try:
                await page.locator("#onetrust-accept-btn-container").click()
            except:
                logger.print("Cookies already accepted.")
            # Wait and close warning message
            try:
                await page.wait_for_selector(".newclose", timeout=10000)
                await page.locator(".newclose").click()
            except:
                logger.print("No warning message.")

            try:
                await page.wait_for_selector("img.fechar", timeout=10000)
                await page.locator("img.fechar").click()
            except:
                logger.print("No Ads message.")
            cnpj_atual = await page.locator(".usuario_cnpj.mb-0").first.text_content()
            if not config_entrada.get("cnpjEmpresa") in cnpj_atual:
                # Select Gas Station
                await page.wait_for_selector(".usuario_img", timeout=90000)
                await page.locator(".usuario_img").first.click()
                # Fill the station
                logger.print("Selecting gas station")
                change_station = page.locator(
                    '//*[@id="trocaMuitosPostosModal"]/div[2]/div/div'
                )
                await change_station.locator('[type="text"]').first.type(
                    config_entrada.get("cnpjEmpresa")
                )
                # cnpj = config_entrada.get("cnpjEmpresa")
                # await page.locator(f'li[data-cdpessptoecli="{cnpj}"]').click()
                await asyncio.sleep(3)
                await change_station.get_by_text("Trocar", exact=True).locator(
                    "visible=true"
                ).click()

            await asyncio.sleep(5)
            logger.print("Going to order page")
            await page.goto(
                "https://www.redeipiranga.com.br/wps/myportal/redeipiranga/pedidos/combustivel/registrarpedido/",
                wait_until="load",
            )
            await asyncio.sleep(5)
            # Get Iframe to collect locators
            iframe = page.frame_locator(
                '//*[@id="ns_Z7_LA04H4G0P0FDB061C74LHG2G17__content-frame"]'
            )
            await asyncio.sleep(20)
            bases = await get_config_by_name("ipirangaBasesValue")
            bases = bases.conConfiguracao
            # Change Base
            try:
                base = bases[config_entrada["baseNome"]]
                # await page.locator('//*[@id="frmPedido"]/section[1]/div[3]/div[1]/select').select_option(value=base)
                await iframe.locator("select[name='codigoDependencia']").select_option(
                    value=base
                )
                await asyncio.sleep(2)

            except:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("Base não encontrada")
            # Fill Fuels
            logger.print("Filling Fuels")
            await asyncio.sleep(2)

            combusutiveis_ids = await get_config_by_name("ConsultaPrecoCombustiveisIds")
            combusutiveis_ids = combusutiveis_ids.conConfiguracao["CombustiveisIds"]

            xpath_ids = await get_config_by_name("ipirangaXpathCombustiveis")
            xpath_ids = xpath_ids.conConfiguracao

            for combustivel in config_entrada["combustiveis"]:
                for id in combusutiveis_ids:
                    if id["uuid"] == combustivel["uuidItem"]:

                        # trata múltiplas descrições
                        descricoes = [
                            d.strip() for d in id["descricaoIpiranga"].split(",")
                        ]

                        fuel = None
                        for desc in descricoes:
                            locator = iframe.locator(
                                f'.combustivel_box.clTrProdutos:has-text("{desc}")'
                            )

                            if await locator.count() > 0:
                                fuel = locator
                                break

                        if not fuel:
                            raise Exception(
                                f"Nenhuma descrição encontrada para {descricoes}"
                            )

                        try:
                            indisponivel = await fuel.locator(
                                ".texto-indisponivel", timeout=5000
                            ).text_content()
                            if indisponivel:
                                await capture_and_send_screenshot(
                                    task.historico_id, "Erro"
                                )
                                raise Exception(f"{indisponivel}")
                        except:
                            pass

                        await fuel.locator('input[name="quantidade"]').fill(
                            str(combustivel["quantidade"])
                        )
                        await fuel.locator('input[name="quantidade"]').press("Tab")

            # Next
            logger.print("Going to next page")
            await iframe.locator(
                'a[href="javascript:avancar()"]:has-text("Avançar")'
            ).click()

            await asyncio.sleep(5)
            # Finish Order
            logger.print("Finishing order")
            await page.wait_for_selector(
                "iframe#ns_Z7_LA04H4G0P0FDB061C74LHG2G17__content-frame"
            )
            iframe_final = page.frame_locator(
                "iframe#ns_Z7_LA04H4G0P0FDB061C74LHG2G17__content-frame"
            )
            btn_finish = iframe_final.locator('button:has-text("Finalizar pedido")')
            await btn_finish.scroll_into_view_if_needed()
            await btn_finish.click(force=True)

            await asyncio.sleep(30)
            finish_iframe = page.frame_locator(
                '//*[@id="ns_Z7_LA04H4G0P0FDB061C74LHG2G17__content-frame"]'
            )
            element = finish_iframe.locator(".titulo.titulo-area")
            await element.scroll_into_view_if_needed()
            text = await element.text_content()
            text = " ".join(text.split())
            numero_pedido = re.findall(r"\d+", text)
            date = config_entrada["dataRetirada"]
            date = datetime.fromisoformat(date)
            if "sucesso" in text:
                bof = {
                    "numero_pedido": numero_pedido[0],
                    "cnpj": config_entrada["cnpjEmpresa"],
                    "data": date.strftime("%d/%m/%Y"),
                }
                await capture_and_send_screenshot(
                    task.historico_id, "Sucesso ao realizar pedido!"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=str(bof),
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            else:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception(f"Erro ao realizar pedido: {text}")
    except Exception as e:
        logger.print(f"An error occurred: {e}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"An error occurred: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[
                RpaTagDTO(descricao=RpaTagEnum.Tecnico),
                RpaTagDTO(descricao=RpaTagEnum.Negocio),
            ],
        )
    finally:
        await browser.close()
