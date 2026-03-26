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
import re
import json
from playwright.async_api import async_playwright
from worker_automate_hub.api.client import get_config_by_name, get_mfa_code
from worker_automate_hub.api.datalake_service import send_file_to_datalake
from worker_automate_hub.utils.util import (
    capture_and_send_screenshot,
    ensure_browsers_installed,
    kill_all_emsys,
    compare_itens,
)

logger = Console()
DATALAKE_DIRECTORY = "precos/raw"


def log_step(step, mensagem):
    logger.print(f"[bold cyan][STEP {step}][/bold cyan] {mensagem}")


def log_ok(mensagem):
    logger.print(f"[bold green][OK][/bold green] {mensagem}")


def log_info(mensagem):
    logger.print(f"[bold blue][INFO][/bold blue] {mensagem}")


def log_warn(mensagem):
    logger.print(f"[bold yellow][ALERTA][/bold yellow] {mensagem}")


def log_error(mensagem):
    logger.print(f"[bold red][ERRO][/bold red] {mensagem}")


def log_data(mensagem):
    logger.print(f"[bold magenta][DADOS][/bold magenta] {mensagem}")


async def esta_na_tela_selecao_empresa(page) -> bool:
    try:
        log_info("Validando se a tela de seleção de empresa está visível")
        await page.wait_for_selector(
            '//*[@id="api"]/div/form/div[2]/app-select/div/div',
            state="visible",
            timeout=10000
        )
        log_ok("Tela de seleção de empresa identificada")
        return True
    except Exception:
        log_warn("Tela de seleção de empresa ainda não apareceu")
        return False


async def ainda_esta_na_tela_mfa(page) -> bool:
    try:
        log_info("Validando se ainda está na tela de MFA")
        campo_codigo = page.locator('//*[@id="readOnlyEmail_ver_input"]')
        botao_verificar = page.locator('//*[@id="readOnlyEmail_ver_but_verify"]')
        retorno = await campo_codigo.is_visible(timeout=2000) and await botao_verificar.is_visible(timeout=2000)

        if retorno:
            log_warn("Tela de MFA ainda está visível")
        else:
            log_info("Tela de MFA não está mais visível")

        return retorno
    except Exception as e:
        log_warn(f"Não foi possível validar a tela de MFA: {e}")
        return False


async def validar_e_inserir_mfa(task, page, tentativas=3):
    for tentativa in range(1, tentativas + 1):
        log_step("5A", f"Validação MFA - tentativa {tentativa}/{tentativas}")

        code = await get_mfa_code("mfa-raizen")
        log_data("Retorno bruto do MFA")

        if not code:
            log_warn("get_mfa_code retornou vazio")
            await asyncio.sleep(5)
            continue

        if code.get("status_code") != 200 or not code.get("code"):
            log_warn(f"Falha ao obter MFA: {code}")
            await asyncio.sleep(5)
            continue

        codigo = str(code["code"]).strip()
        log_ok(f"Código MFA obtido na tentativa {tentativa}")

        campo_codigo = page.locator('//*[@id="readOnlyEmail_ver_input"]')
        log_info("Aguardando campo do código MFA ficar visível")
        await campo_codigo.wait_for(state="visible", timeout=10000)

        log_info("Limpando campo do código MFA")
        await campo_codigo.click()
        await campo_codigo.fill("")

        log_info("Digitando código MFA")
        await campo_codigo.type(codigo)

        log_info("Clicando no botão de verificar MFA")
        await page.locator('//*[@id="readOnlyEmail_ver_but_verify"]').click()

        try:
            log_info("Aguardando estabilização da tela após validar MFA")
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            log_warn(f"Timeout ou falha ao aguardar networkidle após MFA: {e}")

        await asyncio.sleep(8)

        if await esta_na_tela_selecao_empresa(page):
            log_ok("MFA validado com sucesso. Tela de empresa carregada.")
            return True

        if await ainda_esta_na_tela_mfa(page):
            log_warn("Ainda está na tela de MFA. Tentando novamente.")
            try:
                await capture_and_send_screenshot(task.historico_id, f"MFA tentativa {tentativa} falhou")
                log_info(f"Screenshot enviada: MFA tentativa {tentativa} falhou")
            except Exception as e:
                log_warn(f"Não foi possível enviar screenshot da falha MFA: {e}")
            await asyncio.sleep(5)
            continue

        log_warn("Tela após MFA não reconhecida. Tentando novamente.")
        try:
            await capture_and_send_screenshot(task.historico_id, f"Tela não reconhecida após MFA tentativa {tentativa}")
            log_info(f"Screenshot enviada: Tela não reconhecida após MFA tentativa {tentativa}")
        except Exception as e:
            log_warn(f"Não foi possível enviar screenshot da tela não reconhecida: {e}")
        await asyncio.sleep(5)

    await capture_and_send_screenshot(task.historico_id, "Falha ao validar MFA após 3 tentativas")
    log_error("Não foi possível validar o código MFA após 3 tentativas.")
    raise Exception("Não foi possível validar o código MFA após 3 tentativas.")


async def consulta_preco_ipiranga(self, config, config_entrada, fuel_itens):
    browser = None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True, slow_mo=100)
            page = await browser.new_page()

            # Going to Main page
            logger.info(f"Navigating to {config.get('url_ipiranga')}")
            await page.goto(config.get('url_ipiranga'), wait_until="load", timeout=90000)

            # Wait page load
            await page.wait_for_selector('[title="Login"]', timeout=90000)

            # Login
            logger.info("Logging")
            await page.locator('[title="Login"]').type(config.get('login_ipiranga'))
            await page.locator('[type="password"]').type(config.get('pass_ipiranga'))
            await page.locator('[type="submit"]').click()

            try:
                await asyncio.sleep(5)
                warn = await page.wait_for_selector(
                    "//ul[contains(@style, '#ffd000')]/li[contains(text(), 'Usuário ou senha incorretos.')]",
                    timeout=10000
                )
                if warn:
                    logger.info("Login failed. Verify username and password.")
                    return config_entrada, {
                        'error': 'Login failed. Verify username and password.',
                        'status_code': 401
                    }
            except Exception:
                logger.info("Login successful")

            try:
                # Warn to change password
                await page.wait_for_selector(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]',
                    timeout=90000
                )
                await page.locator(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]'
                ).click()
            except Exception:
                logger.info("No warning message.")

            # Wait and accept cookies
            logger.info("Identifying cookies message")
            try:
                await page.wait_for_selector('#onetrust-accept-btn-container', timeout=10000)
                await page.locator('#onetrust-accept-btn-container').click()
            except Exception:
                logger.info("Cookies already accepted or not displayed.")

            # Wait and close warning message
            try:
                await page.wait_for_selector('.newclose', timeout=10000)
                await page.locator('.newclose').click()
            except Exception:
                logger.info("No warning message.")

            try:
                await page.wait_for_selector("img.fechar", timeout=10000)
                await page.locator("img.fechar").click()
            except Exception:
                logger.info("No Ads message.")

            # Select Gas Station
            await page.wait_for_selector('.usuario_img', timeout=90000)
            await page.locator('.usuario_img').first.click()

            # Fill the station
            logger.info("Selecting gas station")
            await page.locator('[type="text"]').first.type(config_entrada.get('consultaPosto'))

            await page.locator('li[data-cdpessptoecli="07473735006401"]').click()
            await page.wait_for_selector('.usuario_img', timeout=90000)

            await asyncio.sleep(10)

            # Collect data
            logger.info("Collecting fuel data")
            await page.wait_for_selector('iframe')
            iframe = page.frame_locator("iframe")
            cards_outer = iframe.locator('.owl-stage')
            cards = await cards_outer.locator('.owl-item').element_handles()
            counter = len(cards)

            if counter <= 0:
                logger.info("No data found.")
                return config_entrada, {'error': 'No data found.', 'status_code': 500}

            fuel_list = []

            for i in range(counter):
                item_element = cards[i]

                # Get fuel name
                title_locator = await item_element.query_selector('h6.titulo.h6')
                if title_locator:
                    fuel_name = await title_locator.text_content()
                    fuel_name = (fuel_name or "").strip()
                else:
                    fuel_name = "Nome não encontrado"

                # Get fuel price
                price_element = await item_element.query_selector(
                    '.card-comercial_info.ml-2 .valor span:nth-of-type(2)'
                )
                fuel_price = await price_element.text_content() if price_element else "Preço não encontrado"
                fuel_price = (fuel_price or "").replace('R$', '').replace(',', '.').replace(' ', '').strip()

                try:
                    fuel_price = float(fuel_price)
                except Exception as e:
                    logger.info(f"Exception in converting price to float: {e}")
                    fuel_price = 0.0

                fuel_item = {
                    'name': fuel_name,
                    'price': fuel_price
                }
                fuel_list.append(fuel_item)

            logger.info(f"Fuel list collected successfully: {fuel_list}")

            # Compare items and update config_entrada with prices found on the site
            logger.info("Comparing items")
            config_entrada = await compare_itens(
                fuel_list,
                config_entrada,
                fuel_itens,
                'descricaoIpiranga'
            )

            logger.info("compare_itens executed successfully")

            # Build JSON payload for datalake
            logger.info("Building JSON payload for datalake")
            payload_json = {
                "fonte": "ipiranga",
                "dataConsulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "consultaPosto": config_entrada.get("consultaPosto"),
                "codigoEmpresa": config_entrada.get("codigoEmpresa"),
                "nomeEmpresa": config_entrada.get("nomeEmpresa"),
                "baseNome": config_entrada.get("baseNome"),
                "consultaBase": config_entrada.get("consultaBase"),
                "baseUuid": config_entrada.get("baseUuid"),
                "baseBandeira": config_entrada.get("baseBandeira"),
                "cnpjEmpresa": config_entrada.get("cnpjEmpresa"),
                "identificador": config_entrada.get("identificador"),
                "uuidHistorico": config_entrada.get("uuidHistorico"),
                "processo": config_entrada.get("processo"),
                "fuel_list_site": fuel_list,
                "precos_atualizados": config_entrada.get("precos", []),
            }

            json_bytes = json.dumps(
                payload_json,
                ensure_ascii=False,
                indent=4
            ).encode("utf-8")

            nome_arquivo_json = (
                f"preco_ipiranga_{config_entrada.get('consultaPosto')}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            try:
                await send_file_to_datalake(
                    directory=DATALAKE_DIRECTORY,
                    file=json_bytes,
                    filename=nome_arquivo_json,
                    file_extension="json",
                )
                logger.info(
                    f"JSON sent to datalake successfully | "
                    f"directory={DATALAKE_DIRECTORY} | filename={nome_arquivo_json}"
                )
            except Exception as e:
                logger.error(
                    f"Error sending JSON to datalake | "
                    f"directory={DATALAKE_DIRECTORY} | filename={nome_arquivo_json} | error={e}"
                )
                raise Exception(f"Erro ao enviar JSON ao datalake: {e}")

            logger.info("Closing browser")
            await browser.close()
            browser = None

            return config_entrada, {"status_code": 200, "error": "No errors"}

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return config_entrada, {"status_code": 500, "error": f"An error occurred: {e}"}

        finally:
            if browser:
                try:
                    await browser.close()
                except Exception:
                    pass