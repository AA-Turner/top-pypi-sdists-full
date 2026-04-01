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
        log_data(f"Retorno bruto do MFA: {code}")

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


async def consulta_preco_raizen(task, config_entrada=None, fuel_itens=None):
    browser = None
    context = None
    page = None

    fuel_itens_config = await get_config_by_name("ConsultaPrecoCombustiveisIds")
    fuel_itens = fuel_itens_config.conConfiguracao["CombustiveisIds"]

    if config_entrada is None:
        config_entrada = getattr(task, "configEntrada", None) or {}

    if fuel_itens is None:
        fuel_itens = config_entrada.get("precos", [])

    try:
        log_step(1, "Iniciando preparação do ambiente")
        await ensure_browsers_installed()
        log_ok("Browsers do Playwright validados/instalados")

        await kill_all_emsys()
        log_ok("Processos EMSys encerrados")

        log_step(2, "Buscando configuração ConsultaPreco")
        config = await get_config_by_name("ConsultaPreco")
        log_data(f"Tipo retornado por get_config_by_name: {type(config)}")

        config = config.conConfiguracao
        log_ok("Objeto conConfiguracao carregado")

        if not config:
            raise Exception("Configuração ConsultaPreco não carregada.")

        url_raizen = config.get("url_raizen")
        login_raizen = config.get("login_raizen")
        pass_raizen = config.get("pass_raizen")

        log_data(f"url_raizen: {url_raizen}")
        log_data(f"login_raizen preenchido: {'SIM' if login_raizen else 'NÃO'}")
        log_data(f"pass_raizen preenchido: {'SIM' if pass_raizen else 'NÃO'}")

        if not url_raizen:
            raise Exception("A configuração não possui 'url_raizen'.")
        if not login_raizen:
            raise Exception("A configuração não possui 'login_raizen'.")
        if not pass_raizen:
            raise Exception("A configuração não possui 'pass_raizen'.")

        consulta_posto = config_entrada.get("consultaPosto")
        base_nome = config_entrada.get("baseNome")

        log_data(f"consultaPosto: {consulta_posto}")
        log_data(f"baseNome: {base_nome}")
        log_data(f"Quantidade de fuel_itens recebidos: {len(fuel_itens) if fuel_itens else 0}")
        log_data(f"fuel_itens recebidos: {fuel_itens}")

        if not consulta_posto:
            raise Exception("config_entrada não possui 'consultaPosto'.")
        if not base_nome:
            raise Exception("config_entrada não possui 'baseNome'.")

        log_step(3, "Inicializando Playwright e navegador")
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                slow_mo=100,
                args=[
                    "--ignore-certificate-errors",
                    "--ignore-ssl-errors",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-infobars",
                    "--window-size=1920,1080",
                ],
            )
            log_ok("Chromium iniciado com sucesso")

            context = await browser.new_context(ignore_https_errors=True)
            log_ok("Contexto do navegador criado")

            page = await context.new_page()
            log_ok("Nova página criada")

            await page.set_viewport_size({"width": 1850, "height": 900})
            log_ok("Viewport configurado para 1850x900")

            log_step(4, f"Navegando para a URL da Raizen: {url_raizen}")
            await page.goto(url_raizen, wait_until="networkidle")
            await page.wait_for_load_state("load")
            log_ok("Página inicial da Raizen carregada")

            log_step(5, "Realizando login")
            log_info("Digitando usuário")
            await page.locator("#signInName").type(login_raizen)

            log_info("Digitando senha")
            await page.locator("#password").type(pass_raizen)

            log_info("Clicando no botão avançar/login")
            await page.locator("#next").click()
            log_ok("Ação de login executada")

            log_step(6, "Solicitando envio do código de verificação")
            await page.locator("#readOnlyEmail_ver_but_send").click()
            await page.wait_for_load_state("load")
            log_ok("Solicitação de envio do código executada")

            log_info("Aguardando chegada do código MFA por 90 segundos")
            await asyncio.sleep(90)

            await validar_e_inserir_mfa(task, page, tentativas=3)

            log_step(7, f"Selecionando empresa do posto {consulta_posto}")
            await page.wait_for_selector(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div',
                state="visible",
                timeout=15000
            )
            log_ok("Combo de seleção de empresa visível")

            await page.locator('//*[@id="api"]/div/form/div[2]/app-select/div/div').click()
            log_info("Combo de empresa aberto")

            try:
                log_info(f"Tentando selecionar empresa pelo texto: {consulta_posto} - SIM REDE DE POSTOS LTDA")
                element = page.locator(f'text="{consulta_posto} - SIM REDE DE POSTOS LTDA"')
                await element.scroll_into_view_if_needed()
                await element.click()
                log_ok("Empresa selecionada com sucesso")
            except Exception:
                log_warn(f"Código do posto: {consulta_posto} não localizado.")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Código do posto: {consulta_posto} não localizado.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )

            log_step(8, "Avançando após seleção da empresa")
            try:
                await page.locator('//*[@id="api"]/div/form/div[3]/app-button-primary/button/div').click()
                log_ok("Botão continuar clicado com sucesso")
            except Exception as e:
                log_warn(f"Falha ao clicar no botão continuar principal: {e}. Tentando rádio alternativo.")
                await page.locator('//*[@id="divisionType"]/div/div/cso-input-radio-option[1]/label/span').click()
                log_ok("Rádio alternativo clicado com sucesso")

            await page.wait_for_load_state("load")
            log_ok("Tela carregada após avanço")

            try:
                log_step(9, "Selecionando tipo de combustível e acessando")
                await asyncio.sleep(5)
                await page.locator("label.cso-radio-option:has-text('Combustíveis Claros')").click()
                log_ok("Opção 'Combustíveis Claros' selecionada")

                await page.locator("button span:has-text('Acessar')").click()
                log_ok("Botão 'Acessar' clicado")
            except Exception as e:
                log_warn(f"Radio button já selecionado ou indisponível: {e}")

            log_info("Aguardando estabilização da tela por 15 segundos")
            await asyncio.sleep(15)

            try:
                log_info("Tentando fechar popup de mensagens")
                await page.locator(".messages__popup__button_ok").click()
                log_ok("Popup fechado com sucesso")
            except Exception as e:
                log_warn(f"Popup não apareceu ou não foi possível fechar: {e}")

            log_step(10, "Executando fluxo adicional de continuidade")
            try:
                logger.log("Clicking continue")
                await page.locator('//*[@id="api"]/div/form/div[3]/app-button-primary/button/div').click()
                log_ok("Continue adicional clicado com sucesso")
            except Exception as e1:
                log_warn(f"Falha no continue adicional principal: {e1}")
                try:
                    await page.locator('//*[@id="divisionType"]/div/div/cso-input-radio-option[1]/label/span').click()
                    log_ok("Rádio alternativo do fluxo adicional clicado com sucesso")
                except Exception as e2:
                    log_warn(f"Também não foi possível clicar no rádio alternativo do fluxo adicional: {e2}")

            try:
                log_info("Tentando clicar em elemento intermediário para evitar timeout")
                await page.locator('//*[@id="undefined"]/div/span').click()
                log_ok("Elemento intermediário clicado com sucesso")
                await asyncio.sleep(20)
            except Exception as e:
                log_warn(f"Elemento intermediário não apareceu ou não pôde ser clicado: {e}")

            try:
                logger.log("Clicking pop up")
                log_info("Tentando fechar popup 'OK' adicional")
                await page.locator('a.messages__popup__button_ok', has_text="OK").click()
                log_ok("Popup adicional fechado")
                await asyncio.sleep(2)
            except Exception as e:
                logger.log("No pop up")
                log_warn(f"Popup adicional não apareceu: {e}")

            log_step(11, "Acessando menu de preços")
            await page.locator('//*[@id="pages-pricing-pricing-main"]').hover()
            log_ok("Hover no menu de preços realizado")

            await page.locator('//*[@id="navbarSupportedContent"]/ul/li[5]/div').click()
            log_ok("Menu de preços clicado")

            await asyncio.sleep(20)
            log_info("Aguardados 20 segundos para carregamento da tela de preços")

            log_step(12, f"Selecionando cliente para filtro | Posto: {consulta_posto}")
            await page.locator(
                '//*[@id="customer-filter-multiselect"]/section/div/div/div/app-multi-select-option-selected/div'
            ).click()
            log_ok("Combo de cliente aberto")

            await page.keyboard.type(str(consulta_posto))
            log_ok(f"Texto do cliente digitado: {consulta_posto}")

            await page.locator(
                '//*[@id="customer-filter-multiselect"]/section/div/div/div/app-multi-select-list/ul/li[1]'
            ).click()
            log_ok("Primeira opção do filtro de cliente selecionada")

            await page.locator('//*[@id="customer-filter-multiselect"]/div').click()
            log_ok("Combo de cliente fechado")

            log_step(13, f"Selecionando base para filtro | Base: {base_nome}")
            await page.locator(
                '//*[@id="plant-filter-multiselect"]/section/div/div/div/app-multi-select-option-selected/div/label'
            ).click()
            log_ok("Combo de base aberto")

            await page.keyboard.type(str(base_nome))
            log_ok(f"Texto da base digitado: {base_nome}")

            await page.locator(
                '//*[@id="plant-filter-multiselect"]/section/div/div/div/app-multi-select-list/ul/li[1]'
            ).click()
            log_ok("Primeira opção do filtro de base selecionada")

            await page.locator('//*[@id="plant-filter-multiselect"]/div').click()
            log_ok("Combo de base fechado")

            log_step(14, "Aplicando filtro")
            await page.locator('//*[@id="button-filter-apply"]/button/div').click()
            log_ok("Botão aplicar filtro clicado")

            await asyncio.sleep(10)
            log_info("Aguardados 10 segundos após aplicar filtro")

            try:
                log_step(15, "Validando se houve retorno vazio")

                mensagens = page.locator("div.message-text")
                qtd_mensagem = await mensagens.count()
                log_data(f"Quantidade total de elementos 'div.message-text' encontrados no DOM: {qtd_mensagem}")

                for i in range(qtd_mensagem):
                    msg = mensagens.nth(i)
                    texto = ((await msg.text_content()) or "").strip()
                    visivel = await msg.is_visible()

                    log_data(f"Mensagem índice {i} | visível={visivel} | texto='{texto}'")

                    if visivel and texto == "Não foram encontrados resultados":
                        log_warn("Nenhum resultado encontrado")
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Nenhum resultado encontrado",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                        )

            except Exception as e:
                log_warn(f"Não foi possível validar mensagem de ausência de resultados: {e}")

            log_step(16, "Coletando produtos")
            products = await page.locator("div#products").all_text_contents()
            log_data(f"Quantidade de produtos encontrados: {len(products)}")
            log_data(f"Produtos encontrados: {products}")

            log_step(17, "Coletando preços")
            products_prices = await page.locator(".product-price.ng-star-inserted").all_text_contents()
            raw_prices = await page.locator("div#product-price >> div >> div").all_text_contents()

            log_data(f"Quantidade de products_prices encontrados: {len(products_prices)}")
            log_data(f"Quantidade de raw_prices encontrados: {len(raw_prices)}")
            log_data(f"products_prices: {products_prices}")
            log_data(f"raw_prices: {raw_prices}")

            clean_prices = []
            for idx, price in enumerate(raw_prices, start=1):
                match = re.search(r"[\d,]+", price.replace(u" R$\xa0", ""))
                if match:
                    valor_convertido = float(match.group().replace(",", "."))
                    clean_prices.append(valor_convertido)
                    log_data(f"Preço tratado {idx}: bruto='{price}' | convertido={valor_convertido}")
                else:
                    log_warn(f"Preço bruto sem match regex: '{price}'")

            fuel_list = []
            total_iteracoes = min(len(products), len(products_prices), len(clean_prices))
            log_data(f"Total de iterações para montar fuel_list: {total_iteracoes}")

            for i in range(total_iteracoes):
                price = products_prices[i].strip()
                price = price.replace(u"R$\xa0", "")
                price = price.replace(",", ".")

                item = {
                    "name": products[i].strip(),
                    "price": float(price),
                }

                fuel_list.append(item)
                log_data(f"Item fuel_list[{i}]: {item}")

            log_ok(f"fuel_list montado com {len(fuel_list)} itens")
            logger.print(f"fuel_list montado: {fuel_list}")

            log_step(18, "Comparando itens coletados com config_entrada")
            config_entrada = await compare_itens(
                fuel_list,
                config_entrada,
                fuel_itens,
                "descricaoRaizen"
            )
            log_ok("compare_itens executado com sucesso")

            log_step("18A", "Garantindo preenchimento explícito dos preços no JSON final")

            precos_entrada = config_entrada.get("precos", [])

            mapa_precos_site = {
                str(item.get("name", "")).strip().upper(): item.get("price", 0)
                for item in fuel_list
            }
            log_data(f"mapa_precos_site: {mapa_precos_site}")

            mapa_combustiveis_config = {}
            for item_cfg in fuel_itens:
                descricao_raizen = str(item_cfg.get("descricaoRaizen", "")).strip().upper()
                uuid_cfg = item_cfg.get("uuid")
                if descricao_raizen:
                    mapa_combustiveis_config[descricao_raizen] = uuid_cfg

            log_data(f"mapa_combustiveis_config: {mapa_combustiveis_config}")

            mapa_uuid_para_preco = {}
            for nome_site, preco_site in mapa_precos_site.items():
                uuid_encontrado = mapa_combustiveis_config.get(nome_site)
                if uuid_encontrado:
                    mapa_uuid_para_preco[uuid_encontrado] = preco_site

            log_data(f"mapa_uuid_para_preco: {mapa_uuid_para_preco}")

            novos_precos = []
            for item_preco in precos_entrada:
                uuid_item = item_preco.get("uuidItem")
                preco_encontrado = mapa_uuid_para_preco.get(uuid_item)

                if preco_encontrado is not None and float(preco_encontrado) > 0:
                    item_atualizado = dict(item_preco)
                    item_atualizado["preco"] = float(preco_encontrado)
                    novos_precos.append(item_atualizado)

                    log_data(
                        f"Item incluído no JSON | uuidItem={uuid_item} | "
                        f"descricaoProduto={item_atualizado.get('descricaoProduto')} | "
                        f"preco={item_atualizado['preco']}"
                    )
                else:
                    log_warn(
                        f"Item ignorado no JSON por não ter preço encontrado | "
                        f"uuidItem={uuid_item} | descricaoProduto={item_preco.get('descricaoProduto')}"
                    )

            config_entrada["precos"] = novos_precos
            log_data(f"config_entrada['precos'] final: {config_entrada['precos']}")

            log_step(19, "Montando JSON no padrão esperado")

            return_json = {
                "coleta": {
                    "metodo": "RPA",
                    "detalhe": "ALAN",
                    "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "identificador": config_entrada.get("identificador"),
                    "cnpjEmpresa": config_entrada.get("cnpjEmpresa"),
                    "nomeEmpresa": config_entrada.get("nomeEmpresa"),
                    "codigoEmpresa": config_entrada.get("codigoEmpresa"),
                    "consultaPosto": config_entrada.get("consultaPosto"),
                    "consultaBase": config_entrada.get("consultaBase"),
                },
                "base": {
                    "uuid": config_entrada.get("baseUuid"),
                    "nome": config_entrada.get("baseNome"),
                    "bandeira": config_entrada.get("baseBandeira"),
                    "codigoSistema": config_entrada.get("baseCodigoSistema", 0),
                },
                "precos": config_entrada.get("precos", []),
            }

            json_str = json.dumps(return_json, ensure_ascii=False, indent=4)
            json_bytes = json_str.encode("utf-8")

            nome_arquivo_json = (
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            log_data("JSON que será enviado ao datalake:")
            logger.print(json_str)

            print("\n================ JSON ENVIADO AO DATALAKE ================\n")
            print(json_str)
            print("\n==========================================================\n")

            log_data(
                f"Metadados do envio | "
                f"directory={DATALAKE_DIRECTORY} | "
                f"filename={nome_arquivo_json} | "
                f"bytes={len(json_bytes)}"
            )

            try:
                await send_file_to_datalake(
                    directory=DATALAKE_DIRECTORY,
                    file=json_bytes,
                    filename=nome_arquivo_json,
                    file_extension="json",
                )
                log_ok(
                    f"JSON enviado ao datalake com sucesso | "
                    f"directory={DATALAKE_DIRECTORY} | "
                    f"filename={nome_arquivo_json}"
                )
            except Exception as e:
                log_error(
                    f"Erro ao enviar JSON ao datalake | "
                    f"directory={DATALAKE_DIRECTORY} | "
                    f"filename={nome_arquivo_json} | "
                    f"error={e}"
                )
                raise Exception(f"Erro ao enviar JSON ao datalake: {e}")

            log_step(20, "Processo concluído com sucesso")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Processo concluído com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

    except Exception as e:
        log_error(f"Erro crítico no fluxo consulta_preco_raizen_service: {e}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao performar o processo: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
        )

    finally:
        log_step("FINAL", "Iniciando encerramento de recursos")

        try:
            if page:
                await page.close()
                log_ok("Página fechada com sucesso")
        except Exception:
            pass

        try:
            if context:
                await context.close()
                log_ok("Contexto fechado com sucesso")
        except Exception:
            pass

        try:
            if browser:
                await browser.close()
                log_ok("Browser fechado com sucesso")
        except Exception:
            pass