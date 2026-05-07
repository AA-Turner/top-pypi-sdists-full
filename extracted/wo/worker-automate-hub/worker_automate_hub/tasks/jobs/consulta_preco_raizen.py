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
    worker_sleep,
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


def normalizar_texto(txt):
    return str(txt or "").strip().upper()


async def esta_na_tela_selecao_empresa(page) -> bool:
    try:
        log_info("Validando se a tela de seleção de empresa está visível")
        await page.wait_for_selector(
            '//*[@id="api"]/div/form/div[2]/app-select/div/div',
            state="visible",
            timeout=10000,
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
        await campo_codigo.wait_for(state="visible", timeout=10000)

        await campo_codigo.click()
        await campo_codigo.fill("")
        await campo_codigo.type(codigo)

        await page.locator('//*[@id="readOnlyEmail_ver_but_verify"]').click()

        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            log_warn(f"Timeout ao aguardar networkidle após MFA: {e}")

        await asyncio.sleep(8)

        if await esta_na_tela_selecao_empresa(page):
            log_ok("MFA validado com sucesso. Tela de empresa carregada.")
            return True

        if await ainda_esta_na_tela_mfa(page):
            log_warn("Ainda está na tela de MFA. Tentando novamente.")
            try:
                await capture_and_send_screenshot(
                    task.historico_id,
                    f"MFA tentativa {tentativa} falhou",
                )
            except Exception as e:
                log_warn(f"Não foi possível enviar screenshot da falha MFA: {e}")

            await asyncio.sleep(5)
            continue

        log_warn("Tela após MFA não reconhecida. Tentando novamente.")
        try:
            await capture_and_send_screenshot(
                task.historico_id,
                f"Tela não reconhecida após MFA tentativa {tentativa}",
            )
        except Exception as e:
            log_warn(f"Não foi possível enviar screenshot da tela não reconhecida: {e}")

        await asyncio.sleep(5)

    await capture_and_send_screenshot(
        task.historico_id,
        "Falha ao validar MFA após 3 tentativas",
    )

    raise Exception("Não foi possível validar o código MFA após 3 tentativas.")


async def consulta_preco_raizen(task, config_entrada=None, fuel_itens=None):
    browser = None
    context = None
    page = None

    try:
        log_step(1, "Iniciando preparação do ambiente")
        await ensure_browsers_installed()
        await kill_all_emsys()

        if config_entrada is None:
            config_entrada = getattr(task, "configEntrada", None) or {}

        log_step(2, "Buscando configuração ConsultaPreco")
        config = await get_config_by_name("ConsultaPreco")
        config = config.conConfiguracao

        if not config:
            raise Exception("Configuração ConsultaPreco não carregada.")

        url_raizen = config.get("url_raizen")
        login_raizen = config.get("login_raizen")
        pass_raizen = config.get("pass_raizen")

        if not url_raizen:
            raise Exception("A configuração não possui 'url_raizen'.")
        if not login_raizen:
            raise Exception("A configuração não possui 'login_raizen'.")
        if not pass_raizen:
            raise Exception("A configuração não possui 'pass_raizen'.")

        log_step(2.1, "Buscando configuração ConsultaPrecoCombustiveisIds")
        fuel_itens_config = await get_config_by_name("ConsultaPrecoCombustiveisIds")
        fuel_itens = fuel_itens_config.conConfiguracao["CombustiveisIds"]

        consulta_posto = config_entrada.get("consultaPosto")
        base_nome = config_entrada.get("baseNome")
        codigo_base = config_entrada.get("consultaBase")

        if not consulta_posto:
            raise Exception("config_entrada não possui 'consultaPosto'.")
        if not base_nome:
            raise Exception("config_entrada não possui 'baseNome'.")
        if not codigo_base:
            raise Exception("config_entrada não possui 'consultaBase'.")

        precos_entrada_original = [
            dict(item) for item in (config_entrada.get("precos", []) or [])
        ]

        if not precos_entrada_original:
            raise Exception("config_entrada não possui itens em 'precos'.")

        log_data(f"consultaPosto: {consulta_posto}")
        log_data(f"baseNome: {base_nome}")
        log_data(f"consultaBase: {codigo_base}")
        log_data(f"Quantidade de preços da entrada: {len(precos_entrada_original)}")

        async with async_playwright() as p:
            log_step(3, "Inicializando navegador")
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

            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()
            await page.set_viewport_size({"width": 1850, "height": 900})

            log_step(4, f"Navegando para a URL da Raizen: {url_raizen}")
            await page.goto(url_raizen, wait_until="networkidle")
            await page.wait_for_load_state("load")

            log_step(5, "Realizando login")
            await page.locator("#signInName").type(login_raizen)
            await page.locator("#password").type(pass_raizen)
            await page.locator("#next").click()

            log_step(6, "Solicitando código MFA")
            await page.locator("#readOnlyEmail_ver_but_send").click()
            await page.wait_for_load_state("load")

            log_info("Aguardando chegada do código MFA por 90 segundos")
            await asyncio.sleep(90)

            await validar_e_inserir_mfa(task, page, tentativas=3)

            log_step(7, f"Selecionando empresa do posto {consulta_posto}")
            await page.wait_for_selector(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div',
                state="visible",
                timeout=15000,
            )

            await page.locator(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div'
            ).click()

            try:
                element = page.locator(
                    f'text="{consulta_posto} - SIM REDE DE POSTOS LTDA"'
                )
                await element.scroll_into_view_if_needed()
                await element.click()
                log_ok("Empresa selecionada com sucesso")
            except Exception:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Código do posto: {consulta_posto} não localizado.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            log_step(8, "Avançando após seleção da empresa")
            try:
                await page.locator(
                    '//*[@id="api"]/div/form/div[3]/app-button-primary/button/div'
                ).click()
            except Exception:
                await page.locator(
                    '//*[@id="divisionType"]/div/div/cso-input-radio-option[1]/label/span'
                ).click()

            await page.wait_for_load_state("load")

            log_step(9, "Selecionando Combustíveis Claros")
            try:
                await asyncio.sleep(5)
                await page.locator(
                    "label.cso-radio-option:has-text('Combustíveis Claros')"
                ).click()
                await page.locator("button span:has-text('Acessar')").click()
            except Exception as e:
                log_warn(f"Radio button já selecionado ou indisponível: {e}")

            await asyncio.sleep(15)

            try:
                await page.locator(".messages__popup__button_ok").click()
            except Exception:
                pass

            log_step(10, "Executando fluxo adicional")
            try:
                await page.locator(
                    '//*[@id="api"]/div/form/div[3]/app-button-primary/button/div'
                ).click()
            except Exception:
                try:
                    await page.locator(
                        '//*[@id="divisionType"]/div/div/cso-input-radio-option[1]/label/span'
                    ).click()
                except Exception:
                    pass

            try:
                await page.locator('//*[@id="undefined"]/div/span').click()
                await asyncio.sleep(20)
            except Exception:
                pass

            try:
                await page.locator(
                    "a.messages__popup__button_ok",
                    has_text="OK",
                ).click()
                await asyncio.sleep(2)
            except Exception:
                pass

            log_step(11, "Acessando menu de preços")
            await page.locator('//*[@id="pages-pricing-pricing-main"]').hover()
            await page.locator('//*[@id="navbarSupportedContent"]/ul/li[5]/div').click()

            await asyncio.sleep(20)

            log_step(12, f"Selecionando cliente para filtro | Posto: {consulta_posto}")
            await page.locator(
                '//*[@id="customer-filter-multiselect"]/section/div/div/div/app-multi-select-option-selected/div'
            ).click()

            await page.keyboard.type(str(consulta_posto))

            await page.locator(
                '//*[@id="customer-filter-multiselect"]/section/div/div/div/app-multi-select-list/ul/li[1]'
            ).click()

            await page.locator('//*[@id="customer-filter-multiselect"]/div').click()

            log_step(13, f"Selecionando base para filtro | Base: {codigo_base}")
            await page.locator(
                '//*[@id="plant-filter-multiselect"]/section/div/div/div/app-multi-select-option-selected/div/label'
            ).click()

            base = page.get_by_role("listitem").filter(has_text=f"[{codigo_base}]")

            try:
                await base.scroll_into_view_if_needed()
                await base.click()
                log_ok(f"Base selecionada: {codigo_base}")
            except Exception:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Base '{codigo_base}' não encontrada no site para seleção.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            try:
                await page.locator("//a[@id='pages-pricing-pricing-main']").click()
            except Exception:
                pass

            await worker_sleep(1)

            log_step(14, "Aplicando filtro")
            await page.locator('//*[@id="button-filter-apply"]/button/div').click()

            await asyncio.sleep(10)

            log_step(15, "Validando retorno vazio")
            try:
                mensagens = page.locator("div.message-text")
                qtd_mensagem = await mensagens.count()

                for i in range(qtd_mensagem):
                    msg = mensagens.nth(i)
                    texto = ((await msg.text_content()) or "").strip()
                    visivel = await msg.is_visible()

                    if visivel and texto == "Não foram encontrados resultados":
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Nenhum resultado encontrado",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                        )
            except Exception as e:
                log_warn(f"Não foi possível validar mensagem de ausência: {e}")

            log_step(16, "Coletando produtos")
            products = await page.locator("div#products").all_text_contents()
            log_data(f"Produtos encontrados: {products}")

            log_step(17, "Coletando preços")
            products_prices = await page.locator(
                ".product-price.ng-star-inserted"
            ).all_text_contents()

            log_data(f"Preços encontrados: {products_prices}")

            fuel_list = []
            total_iteracoes = min(len(products), len(products_prices))

            for i in range(total_iteracoes):
                nome_produto = products[i].strip()
                preco_txt = products_prices[i].strip()

                preco_txt = preco_txt.replace("R$\xa0", "")
                preco_txt = preco_txt.replace("R$", "")
                preco_txt = preco_txt.replace(".", "")
                preco_txt = preco_txt.replace(",", ".")
                preco_txt = preco_txt.strip()

                match = re.search(r"\d+(\.\d+)?", preco_txt)

                if not match:
                    log_warn(f"Preço inválido para produto '{nome_produto}': {preco_txt}")
                    continue

                item = {
                    "name": nome_produto,
                    "price": float(match.group()),
                }

                fuel_list.append(item)
                log_data(f"Item coletado do site: {item}")

            if not fuel_list:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Nenhum produto/preço foi coletado no site.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            log_step(18, "Executando compare_itens apenas para compatibilidade/log")
            try:
                config_entrada_compare = await compare_itens(
                    fuel_list,
                    dict(config_entrada),
                    fuel_itens,
                    "descricaoRaizen",
                )
                log_ok("compare_itens executado com sucesso")
                log_data(f"Resultado compare_itens: {config_entrada_compare}")
            except Exception as e:
                log_warn(f"compare_itens falhou, seguindo com mapeamento próprio: {e}")

            log_step(
                "18A",
                "Atualizando somente o campo preco nos itens originais da entrada",
            )

            mapa_precos_site = {
                normalizar_texto(item.get("name")): float(item.get("price", 0) or 0)
                for item in fuel_list
            }

            log_data(f"mapa_precos_site: {mapa_precos_site}")

            mapa_uuid_para_preco = {}

            for item_cfg in fuel_itens:
                uuid_cfg = str(item_cfg.get("uuid", "") or "").strip()
                descricao_raw = item_cfg.get("descricaoRaizen")

                if not uuid_cfg or not descricao_raw:
                    continue

                descricoes = [
                    normalizar_texto(d)
                    for d in str(descricao_raw).split(",")
                    if d.strip()
                ]

                preco_encontrado = None

                for nome_site, preco_site in mapa_precos_site.items():
                    nome_site_norm = normalizar_texto(nome_site)

                    for desc in descricoes:
                        # MATCH FLEXÍVEL
                        if desc in nome_site_norm or nome_site_norm in desc:
                            if float(preco_site) > 0:
                                preco_encontrado = float(preco_site)

                                log_data(
                                    f"Match FLEX | site='{nome_site_norm}' | desc='{desc}' | uuid={uuid_cfg} | preco={preco_encontrado}"
                                )
                                break

                    if preco_encontrado:
                        break

                if preco_encontrado is not None:
                    mapa_uuid_para_preco[uuid_cfg] = preco_encontrado
                else:
                    log_warn(
                        f"Nenhum match encontrado | uuid={uuid_cfg} | descricoes={descricoes}"
                    )

            log_data(f"mapa_uuid_para_preco: {mapa_uuid_para_preco}")

            novos_precos = []

            for item_original in precos_entrada_original:
                uuid_item = str(item_original.get("uuidItem", "") or "").strip()

                if not uuid_item:
                    log_warn(f"Item da entrada sem uuidItem ignorado: {item_original}")
                    continue

                preco_site = mapa_uuid_para_preco.get(uuid_item)

                if preco_site is None or float(preco_site) <= 0:
                    log_warn(
                        f"Preço não encontrado para uuidItem={uuid_item}. "
                        f"Item não será enviado."
                    )
                    continue

                item_atualizado = dict(item_original)

                # ÚNICO CAMPO ALTERADO
                item_atualizado["preco"] = float(preco_site)

                novos_precos.append(item_atualizado)

                log_data(
                    f"Item da entrada mantido | "
                    f"uuidItem={uuid_item} | "
                    f"codigoProduto={item_atualizado.get('codigoProduto')} | "
                    f"descricaoProduto={item_atualizado.get('descricaoProduto')} | "
                    f"abreviacaoProduto={item_atualizado.get('abreviacaoProduto')} | "
                    f"preco={item_atualizado.get('preco')}"
                )

            config_entrada["precos"] = novos_precos

            if not novos_precos:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Nenhum preço válido encontrado no site para os itens da entrada.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

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
                    "abreviacao": config_entrada.get("baseAbreviacao"),
                    "cnpj": config_entrada.get("baseCnpj"),
                },
                "precos": config_entrada.get("precos", []),
            }

            json_str = json.dumps(return_json, ensure_ascii=False, indent=4)
            json_bytes = json_str.encode("utf-8")
            nome_arquivo_json = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            log_data("JSON que será enviado ao datalake:")
            logger.print(json_str)

            await send_file_to_datalake(
                directory=DATALAKE_DIRECTORY,
                file=json_bytes,
                filename=nome_arquivo_json,
                file_extension="json",
            )

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
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )

    finally:
        log_step("FINAL", "Iniciando encerramento de recursos")

        try:
            if page:
                await page.close()
        except Exception:
            pass

        try:
            if context:
                await context.close()
        except Exception:
            pass

        try:
            if browser:
                await browser.close()
        except Exception:
            pass