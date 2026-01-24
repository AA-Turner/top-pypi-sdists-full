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
from playwright.async_api import async_playwright
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.util import capture_and_send_screenshot, ensure_browsers_installed, kill_all_emsys

logger = Console()


async def inclusao_pedidos_vibra(task: RpaProcessoEntradaDTO):
    try:
        await ensure_browsers_installed()
        await kill_all_emsys()
        config_entrada = task.configEntrada
        #Collect configs
        config = await get_config_by_name("ConsultaPreco")
        config = config.conConfiguracao
        async with async_playwright() as p:
            logger.print("Starting Browser")
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-infobars",
                    "--window-size=1920,1080"
                ]
            )
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1850, "height": 900})
            await page.goto(config.get('url_vibra'), wait_until="load")
            #Login
            await page.wait_for_load_state('load')
            try:
                await page.locator('//*[@id="usuario"]').type(config.get('login_vibra'))
                await page.locator('//*[@id="senha"]').type(config.get('pass_vibra'))
                await page.locator('//*[@id="btn-acessar"]').click()
                await asyncio.sleep(20)
            except Exception as e:
                raise Exception("An error occurred: Erro ao efetuar login")
            await page.wait_for_load_state('load')
            await page.wait_for_selector("#img-menu-open", timeout=50000)
            selector = '.btn.btn-informativo'
            counter = 0
            count = await page.locator(selector).count()
            while counter < count:
                count = await page.locator(selector).count()
                if count == 0:
                    break
                for i in range(count):
                    try:
                        button = page.locator(selector).nth(i)
                        await button.scroll_into_view_if_needed(timeout=1000)
                        await button.click(force=True, timeout=1000)
                        await asyncio.sleep(1)
                    except Exception as e:
                        continue
                counter += 1
                await asyncio.sleep(1)
                
            try:
                try:
                    await page.locator('//*[@id="img-menu-open"]').click()
                except:
                    await page.locator('//*[@id="btnMenu"]').click()
                await asyncio.sleep(1)
                await page.locator('//*[@id="menu"]/div/div[2]/ul/li[4]').hover()
                await asyncio.sleep(1)
                await page.locator('//*[@id="menu"]/div/div[2]/ul/li[4]/ul/li[5]/a').click()
            except Exception as e:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("An error occurred: Erro ao abrir menu")
            await asyncio.sleep(20)
            logger.print("Selecting company")
            #Getting cod SAP
            try:
                cod_sap_relation = await get_config_by_name('vibraCodSapRelation')
                cod_sap_relation = cod_sap_relation.conConfiguracao
                cnpj = config_entrada.get('cnpjEmpresa')
                #Selecting company by CodSAP
                await page.wait_for_selector("select[name='filtroCodigoLogin']", state="visible", timeout=60000)
                await page.select_option("select[name='filtroCodigoLogin']", cod_sap_relation[cnpj], timeout=60000)
            except:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("An error occurred: Erro ao selecionar empresa")
            await page.locator('//*[@id="conteudo"]/div/form[1]/div/table[2]/tbody/tr/td/input').click()
            await page.wait_for_selector('//*[@id="conteudo"]/div/form[2]/div/table[2]/tbody/tr[2]/td[1]/input[1]')
            texto = await page.locator('tr td.result_bold').nth(0).inner_text()
            await page.locator('//*[@id="conteudo"]/div/form[2]/div/table[2]/tbody/tr[2]/td[1]/input[1]').click()
            await asyncio.sleep(1)
            logger.print("Confirming")
            await page.locator('//*[@id="conteudo"]/div/form[2]/div/table[1]/tbody/tr/td/input[1]').click()
            texto_atual = await page.locator('span.info-cliente.hidden-xs').inner_text()
            if texto not in texto_atual:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("An error occurred: Não foi possivel selecionar a empresa para realizer pedido de combustivel.")
            logger.print("Clicking Pedidos")
            await page.locator('//*[@id="menuAcessoRevendedorPedidos"]').click()
            await asyncio.sleep(10)
            #Cleaning cart
            try:
                await page.goto("https://cn.vibraenergia.com.br/central-de-pedidos/#/meu-carrinho")
                await asyncio.sleep(6)
                #Cleaning cart
                await page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-meu-carrinho/div/div[1]/app-carrinho/div/div[2]/div/button[2]/span[1]/mat-icon').click()
                await asyncio.sleep(6)
            except:
                await page.goto('https://cn.vibraenergia.com.br/central-de-pedidos/#/vitrine')
            await page.wait_for_load_state('load')
            logger.print("Selecting Base")
            base_ralation = await get_config_by_name("relacaoBaseVibra")
            base_ralation = base_ralation.conConfiguracao
            base = base_ralation[config_entrada['baseNome']]
            try:
                logger.print(f"{base}")
                try:
                    await page.wait_for_selector('input[formcontrolname="base"]', state="visible", timeout=6000)
                except:
                    try:
                        await page.wait_for_selector('//*[@id="mat-select-6"]', state="visible", timeout=6000)
                    except:
                        raise Exception("An error occurred: Erro ao selecionar base")
                try:
                    await page.locator('input[formcontrolname="base"]').click()
                except:
                    try:
                        await page.locator('//*[@id="mat-select-6"]').click()
                    except:
                        raise Exception("An error occurred: Erro ao selecionar base")
                await page.wait_for_load_state('load')
                await asyncio.sleep(3)
                try:
                    await page.locator('.md-icons.adicionar-bases-icon').click()
                except:
                    pass
                await page.wait_for_load_state('load')
                await asyncio.sleep(3)
                base_selection = page.locator('.mat-option-text', has_text=base)
                await base_selection.scroll_into_view_if_needed()
                await asyncio.sleep(3)
                await base_selection.click()

                await page.wait_for_load_state('load')
                await asyncio.sleep(4)
            except:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("An error occurred: Erro ao selecionar base")
            #If CIF
            if "cif" in config_entrada['placaVeiculo'].lower():
                await page.locator('//mat-select[@formcontrolname="modalidade"]').click()
                await page.wait_for_selector('.mat-option')
                cif_option = page.locator('.mat-option')
                cif_option_span =  cif_option.locator('.mat-option-text', has_text="CIF")
                await cif_option_span.scroll_into_view_if_needed()
                await cif_option_span.click()
            logger.print("Getting configuration")
            xpaths = await get_config_by_name('vibraXpathCombustiveis')
            xpaths = xpaths.conConfiguracao
            #fill fuels
            try:
                for fuel in config_entrada['combustiveis']:
                    if fuel['uuidItem'] in xpaths:
                        try:
                            logger.print('Collecting Carrossel')
                            carrossel = page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]')
                            xpath = xpaths[fuel['uuidItem']]
                            fuel_card = carrossel.locator(xpath)
                            await fuel_card.scroll_into_view_if_needed()
                            try:
                                warning_msg = await fuel_card.locator('.warning', has_text="restrição").inner_text()
                                if 'restrição' in warning_msg:
                                    await capture_and_send_screenshot(task.historico_id, "Erro")
                                    return RpaRetornoProcessoDTO(
                                        sucesso=False,
                                        retorno=f"{warning_msg} | {fuel['descricaoProduto']}",
                                        status=RpaHistoricoStatusEnum.Falha,
                                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico), RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                                    )
                            except:
                                pass
                            card = fuel_card.filter(has=page.locator('button:not([disabled])', has_text="Adicionar"))
                            await card.scroll_into_view_if_needed()
                            await card.locator('button:not([disabled])', has_text="Adicionar").click()
                        except:
                            try:
                                logger.print('Collecting Carrossel 2')
                                carrossel = page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]')
                                await carrossel.locator('mat-icon:has-text("chevron_right")').click()
                                carrossel = page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]')
                                fuel_card = carrossel.locator(xpath)
                                card = fuel_card.filter(has=page.locator('button:not([disabled])', has_text="Adicionar")).first
                                await card.scroll_into_view_if_needed()
                                await card.locator(
                                    "button:not([disabled])", has_text="Adicionar"
                                ).click()
                            except:
                                try:
                                    logger.print("Collecting Carrossel 2")
                                    carrossel = page.locator(
                                        '//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]'
                                    )
                                    await carrossel.locator(
                                        'mat-icon:has-text("chevron_right")'
                                    ).click()
                                    carrossel = page.locator(
                                        '//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]'
                                    )
                                    fuel_card = carrossel.locator(xpath)
                                    card = fuel_card.filter(
                                        has=page.locator(
                                            "button:not([disabled])",
                                            has_text="Adicionar",
                                        )
                                    ).first
                                    await card.scroll_into_view_if_needed()
                                    await card.locator(
                                        "button:not([disabled])", has_text="Adicionar"
                                    ).click()
                                except:
                                    logger.print('Collecting Carrossel 3')
                                    carrossel = page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]')
                                    await carrossel.locator('mat-icon:has-text("chevron_left")').click()
                                    carrossel = page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-vitrine/div/div[3]/div[4]/div[2]/app-carrosel-produtos/div/div[1]')
                                    fuel_card = carrossel.locator(xpath)
                                    card = fuel_card.filter(has=page.locator('button:not([disabled])', has_text="Adicionar")).first
                                    await card.scroll_into_view_if_needed()
                                    await card.locator('button:not([disabled])', has_text="Adicionar").click()
            except:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("An error occurred: Nao foi possivel selecionar combustivel")
            #Go to Cart
            await asyncio.sleep(5)
            await page.locator('//*[@id="user"]/app-root/div[1]/div[1]/cn-header/header/div/div[4]/div/i').click()
            await asyncio.sleep(5)
            #Fill Date
            await page.wait_for_load_state("load")
            await page.get_by_role("button", name="Open calendar").click()
            #Get Calendar
            await asyncio.sleep(1)
            await page.wait_for_selector(".cdk-overlay-pane mat-calendar")
            date = config_entrada['dataRetirada']
            date = datetime.fromisoformat(date)
            date_day = str(date.day)
            today = datetime.now()
            if date.month > today.month:
                #change month
                await page.get_by_label("Next month").click()
                await asyncio.sleep(1)
            await page.locator(f".mat-calendar-body-cell-content:text-is('{date_day}')").click()
            await page.keyboard.press("Escape")
            await asyncio.sleep(5)
            #Collect Cards in cart
            items = page.locator("app-accordion-item-carrinho")
            count = await items.count()
            consulta_preco = await get_config_by_name('ConsultaPrecoCombustiveisIds')
            consulta_preco = consulta_preco.conConfiguracao["CombustiveisIds"]
            logger.print(f"Found {count} items in cart")
            await asyncio.sleep(5)
            for i in range(count):
                logger.print(f"Collecting name of  item {i}")
                item = items.nth(i)
                nome = (await item.locator(".produto-nome").inner_text()).strip()
                logger.print(f"Collecting {nome}")
                # Find config by fuel name
                config_item = next((c for c in consulta_preco if c['descricaoVibra'].lower() == nome.lower()), None)
                if not config_item:
                    continue
                # Find fuel by UUID
                fuel = next((f for f in config_entrada['combustiveis'] if f['uuidItem'] == config_item['uuid']), None)
                if not fuel:
                    continue
                await item.locator("input[formcontrolname='quantidade']").fill("")
                await item.locator("input[formcontrolname='quantidade']").fill(str(fuel['quantidade']))
                await item.locator("input[formcontrolname='quantidade']").press("Escape")
                prazo_select_trigger = item.locator("mat-select[formcontrolname='prazo']")
                await prazo_select_trigger.scroll_into_view_if_needed()
                await prazo_select_trigger.click()
                await asyncio.sleep(5)
                await page.wait_for_selector("mat-option", timeout=5000)
                try:
                    if config_entrada['diasFaturamento'] == 1:
                        option = page.locator("mat-option .mat-option-text", has_text="1 Dia").first
                    else:
                        option = page.locator("mat-option .mat-option-text", has_text=f"{str(config_entrada['diasFaturamento'])} Dias").first
                except:
                    await capture_and_send_screenshot(task.historico_id, "Erro")
                    raise Exception(f"Opção de {str(config_entrada['diasFaturamento'])} Dia(s) não encontrada")
                await option.scroll_into_view_if_needed()
                # await option.click()
                await option.evaluate("(el) => el.click()")
                await asyncio.sleep(10)
            #Confirm order
            try:
                msg = page.locator("text=Volume solicitado acima")
                msg.scroll_into_view_if_needed()
                if await msg.is_visible():
                    texto = await msg.inner_text()
                    await capture_and_send_screenshot(task.historico_id, "Erro")
                    raise Exception(texto)
            except Exception as e:
                raise Exception(e)
            try:
                await page.wait_for_selector('//*[@id="user"]/app-root/div[2]/div/div/app-meu-carrinho/div/div[1]/app-carrinho/div/div[2]/button')
                await page.locator('//*[@id="user"]/app-root/div[2]/div/div/app-meu-carrinho/div/div[1]/app-carrinho/div/div[2]/button').click()
                await asyncio.sleep(5)
            except:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("Falha ao confirmar pedido")
            #Close Satisfaction Survey
            try:    
                logger.print("Closing satisfaction survey")
                await page.locator('//*[@id="mat-dialog-2"]/lib-cn-pesquisa-satisfacao/div/i', timeout=1000).click()
            except:
                logger.print("No satisfaction survey found")
                pass
            await asyncio.sleep(10)
            #Collect order details
            logger.print("Collecting order details")
            numero_pedido = None
            for _ in range(5):
                try:
                    success_message = page.locator("div.sucesso span").first
                    success_message = await success_message.inner_text()
                    if "sucesso" in success_message:
                        success_message = success_message.strip()
                        logger.print(success_message)
                        numero_pedido = re.search(r"\d+", success_message).group()
                        break
                    else:
                        await capture_and_send_screenshot(task.historico_id, "Erro")
                        raise Exception(f"Site nao retornou sucesso ao realizar pedido: {str(success_message)}")
                except Exception as e:
                    logger.print(f"An error occurred: {e}")
                    await asyncio.sleep(7)
                    continue
            if not numero_pedido:
                await capture_and_send_screenshot(task.historico_id, "Erro")
                raise Exception("Erro ao coletar numero do pedido")
            bof = {
                'numero_pedido' : numero_pedido,
                'cnpj': config_entrada["cnpjEmpresa"],
                'data': date.strftime('%d/%m/%Y')
            }
            await capture_and_send_screenshot(task.historico_id, "Sucesso ao realizar pedido!")
            await browser.close()
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=str(bof),
                status=RpaHistoricoStatusEnum.Sucesso)
    except Exception as e:
        logger.print(f"An error occurred: {e}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"An error occurred: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico), RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )
    finally:
        await browser.close()