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
from worker_automate_hub.api.client import get_config_by_name, get_mfa_code
from worker_automate_hub.utils.util import capture_and_send_screenshot, ensure_browsers_installed, kill_all_emsys

logger = Console()

async def inclusao_pedidos_raizen(task: RpaRetornoProcessoDTO):
    try:
        await ensure_browsers_installed()
        await kill_all_emsys()
        config_entrada = task.configEntrada
        #Collect configs
        config = await get_config_by_name("ConsultaPreco")
        config = config.conConfiguracao
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-infobars",
                    "--window-size=1920,1080"])
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1850, "height": 900})
            #Going to Main page
            logger.print(f"Navigating to {config.get('url_raizen')}")
            await page.goto(config.get('url_raizen'), wait_until="networkidle")
            await page.wait_for_load_state('load')
            #Login
            logger.print(f"Logging")
            await page.locator("#signInName").type(config.get('login_raizen'))
            await page.locator("#password").type(config.get('pass_raizen'))
            await page.locator("#next").click()

            logger.print("Waiting for verification code")
            logger.print("Sending verification code")
            await page.locator("#readOnlyEmail_ver_but_send").click()
            await page.wait_for_load_state('load')
            await asyncio.sleep(90)
        
            #chamar endpoint com código retornado
            code = await get_mfa_code('mfa-raizen')
            if code['status_code'] == 200:
                await page.locator('//*[@id="readOnlyEmail_ver_input"]').type(str(code['code']))
                await page.locator('//*[@id="readOnlyEmail_ver_but_verify"]').click()
            else:
                await capture_and_send_screenshot(task.historico_id, "Erro MFA")
                raise Exception("Failed to retrieve MFA code")
                
            # Select Company
            logger.print("Selecting company")
            relacao_cod_raizen = await get_config_by_name("RelacaoCodigosRaizen")
            relacao_cod_raizen = relacao_cod_raizen.conConfiguracao
            await page.wait_for_load_state('load')
            await page.wait_for_selector('//*[@id="api"]/div/form/div[2]/app-select/div/div', state="visible")
            await page.locator('//*[@id="api"]/div/form/div[2]/app-select/div/div').click()
            cod_cnpj = str(relacao_cod_raizen[config_entrada['cnpjEmpresa']]).lstrip('0')
            element = page.locator(f'text="{cod_cnpj} - SIM REDE DE POSTOS LTDA"')              
            await element.scroll_into_view_if_needed()
            await element.click()
            await page.locator('//*[@id="undefined"]').click()
            await page.wait_for_load_state('load')
            try:
                await asyncio.sleep(5)
                await page.locator("label.cso-radio-option:has-text('Combustíveis Claros')").click()
                await page.locator("button span:has-text('Acessar')").click()
            except:
                logger.print("Radio button already selected or not available")
                await asyncio.sleep(10)
                
            await asyncio.sleep(15)
            try:
                await page.locator(".messages__popup__button_ok").click()
            except:
                pass
            # try:
            #     change_password = page.locator('//*[@id="main-scroll"]/div[2]/app-change-password/form/h1')
            # except:
            #     pass
            # if change_password:
            #     await capture_and_send_screenshot(task.historico_id, "Troca de senha obrigatória!")
            #     raise Exception("Troca de senha obrigatória!")
            logger.print("Navegating to orders page")
            await page.goto('https://portal.csonline.com.br/#/ordersfuels', wait_until="load")
            await asyncio.sleep(5)
            #Select Liters
            logger.print("Selecting Liters")
            litro_radio = page.locator("#orders-fuels-input-radio-L")
            await litro_radio.wait_for(state='visible')
            if not await litro_radio.is_checked():
                await litro_radio.click()
                await page.wait_for_timeout(10000)
                await page.locator('//*[@id="undefined"]').click()
            # Date
            try:
                logger.print("Selecting date")
                date = config_entrada['dataRetirada']
                date = datetime.fromisoformat(date)
                date = date.strftime("%d/%m/%Y")
                input_elem = page.locator("#orders-fuels-div-calendar-datepicker")
                await input_elem.evaluate("(el, value) => { el.removeAttribute('readonly'); el.value = value; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }", date)
            except:
                await capture_and_send_screenshot(task.historico_id, "Erro ao realizar pedido!")
                raise Exception("Erro ao selecionar data")
            
            if not 'cif' in config_entrada.get("placaVeiculo").lower():
                # Base
                try:
                    logger.print("Selecting base")
                    rel_base_raizen = await get_config_by_name("relacaoBaseRaizen")
                    rel_base_raizen = rel_base_raizen.conConfiguracao
                    base_nome = rel_base_raizen[config_entrada['baseNome']]
                    await page.locator('//*[@id="orders-fuels-div-dropdown-withdrawal-place"]').click()
                    await page.locator(f'//*[contains(text(), "{base_nome}")]').click()
                except:
                    await capture_and_send_screenshot(task.historico_id, "Erro ao selecionar base")
                    raise Exception("Erro ao selecionar base")
            # Veichle Sign
                try:
                    logger.print("Selecting vehicle sign")
                    await page.locator('//*[@id="orders-fuels-div-dropdown-plate-place-button"]').click()
                    await page.locator('//*[@id="orders-fuels-div-dropdown-plate-place-button"]').fill(config_entrada["placaVeiculo"].upper())
                    await page.locator(f'//*[contains(text(), "{config_entrada["placaVeiculo"]}")]').click()
                except:
                    await capture_and_send_screenshot(task.historico_id, "Erro ao selecionar placa do veiculo")
                    raise Exception("Erro ao selecionar placa do veiculo")
            
            #Fill Fuels
            try:
                logger.print("Filling Fuels")
                combusutiveis_ids_config = await get_config_by_name('ConsultaPrecoCombustiveisIds')
                lista_de_para = combusutiveis_ids_config.conConfiguracao['CombustiveisIds']

                mapa_nomes_raizen = {
                    item['uuid']: item['descricaoRaizen'].replace("'", "").strip() 
                    for item in lista_de_para
                }

                for combustivel in config_entrada['combustiveis']:
                    combustivel_uuid = combustivel['uuidItem']
                    quantidade = str(combustivel['quantidade'])
                    
                    # Busca o nome do produto baseado no UUID
                    nome_produto = mapa_nomes_raizen.get(combustivel_uuid)

                    if not nome_produto:
                        logger.print(f"Produto com UUID {combustivel_uuid} não encontrado no mapa.")
                        continue

                    locator_input = page.locator('.orders-fuels-list__row') \
                                        .filter(has_text=nome_produto) \
                                        .locator('input.orders-fuels-list__quantity__value')

                    if await locator_input.count() > 0:
                        await locator_input.fill(quantidade)
                        await locator_input.blur() 
                    else:
                        logger.print(f"Input para o produto '{nome_produto}' não encontrado na tela.")
            except Exception as e:
                await capture_and_send_screenshot(task.historico_id, "Erro preenchendo combustiveis")
                raise Exception(f"Erro ao preencher combustiveis: {str(e)}")
            # Save order
            logger.print("Saving order")
            await page.locator('//*[@id="orders-fuels-button-save"]').click()
            await asyncio.sleep(10)
            try:
                logger.print("Confirming order")
                await page.get_by_text("Continuar mesmo assim").click()
            except:
                pass
            await page.wait_for_load_state('load')
            
            #Get order number
            await asyncio.sleep(10)
            numero_elem = page.locator('//span[contains(@class, "status__order-number__value")]')
            numero_pedido = ( await numero_elem.inner_text()).strip()
            if not numero_pedido:
                await capture_and_send_screenshot(task.historico_id,"Número do pedido não encontrado!")
                raise Exception("Número do pedido não encontrado!")
            date = config_entrada["dataRetirada"]
            date = datetime.fromisoformat(date)
            bof = {
                    "numero_pedido": numero_pedido,
                    "cnpj": config_entrada["cnpjEmpresa"],
                    "data": date.strftime("%d/%m/%Y"),
                }
            await capture_and_send_screenshot(task.historico_id, "Sucesso ao realizar pedido!")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=str(bof),
                status=RpaHistoricoStatusEnum.Sucesso,
            )
    except Exception as e:
        await capture_and_send_screenshot(task.historico_id, "Erro")
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