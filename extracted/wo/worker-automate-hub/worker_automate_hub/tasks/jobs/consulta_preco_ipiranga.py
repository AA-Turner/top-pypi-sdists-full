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
import json
from playwright.async_api import async_playwright
from worker_automate_hub.api.client import get_config_by_name
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


async def consulta_preco_ipiranga(task, config_entrada=None, fuel_itens=None):
    browser = None
    context = None
    page = None

    try:
        fuel_itens_config = await get_config_by_name("ConsultaPrecoCombustiveisIds")
        fuel_itens = fuel_itens_config.conConfiguracao["CombustiveisIds"]

        if config_entrada is None:
            config_entrada = getattr(task, "configEntrada", None) or {}

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

        url_ipiranga = config.get("url_ipiranga")
        login_ipiranga = config.get("login_ipiranga")
        pass_ipiranga = config.get("pass_ipiranga")

        log_data(f"url_ipiranga: {url_ipiranga}")
        log_data(f"login_ipiranga preenchido: {'SIM' if login_ipiranga else 'NÃO'}")
        log_data(f"pass_ipiranga preenchido: {'SIM' if pass_ipiranga else 'NÃO'}")

        if not url_ipiranga:
            raise Exception("A configuração não possui 'url_ipiranga'.")
        if not login_ipiranga:
            raise Exception("A configuração não possui 'login_ipiranga'.")
        if not pass_ipiranga:
            raise Exception("A configuração não possui 'pass_ipiranga'.")

        consulta_posto = str(config_entrada.get("consultaPosto", "")).strip()

        log_data(f"consultaPosto: {consulta_posto}")
        log_data(f"fuel_itens recebidos: {fuel_itens}")

        if not consulta_posto:
            raise Exception("config_entrada não possui 'consultaPosto'.")

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

            log_step(4, f"Navegando para a URL da Ipiranga: {url_ipiranga}")
            await page.goto(url_ipiranga, wait_until="load", timeout=90000)
            await page.wait_for_load_state("load")
            log_ok("Página inicial da Ipiranga carregada")

            log_step(5, "Realizando login")
            await page.wait_for_selector('[title="Login"]', timeout=90000)

            log_info("Digitando usuário")
            await page.locator('[title="Login"]').fill(login_ipiranga)

            log_info("Digitando senha")
            await page.locator('[type="password"]').fill(pass_ipiranga)

            log_info("Clicando no botão de login")
            await page.locator('[type="submit"]').click()

            try:
                await asyncio.sleep(5)
                warn = await page.wait_for_selector(
                    "//ul[contains(@style, '#ffd000')]/li[contains(text(), 'Usuário ou senha incorretos.')]",
                    timeout=10000,
                )
                if warn:
                    log_error("Login failed. Verify username and password.")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Login failed. Verify username and password.",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )
            except Exception:
                log_ok("Login realizado com sucesso")

            try:
                log_info("Verificando aviso de troca de senha")
                await page.wait_for_selector(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]',
                    timeout=15000,
                )
                await page.locator(
                    '//*[@id="viewns_Z7_LA04H4G0POLN00QRBOJ72420P5_:form_lembrar:j_id_e"]'
                ).click()
                log_ok("Aviso de troca de senha tratado")
            except Exception:
                log_info("Sem aviso de troca de senha")

            try:
                log_info("Tratando cookies")
                await page.wait_for_selector(
                    "#onetrust-accept-btn-container", timeout=10000
                )
                await page.locator("#onetrust-accept-btn-container").click()
                log_ok("Cookies aceitos")
            except Exception:
                log_info("Cookies já aceitos ou banner não exibido")

            try:
                await page.wait_for_selector(".newclose", timeout=10000)
                await page.locator(".newclose").click()
                log_ok("Aviso genérico fechado")
            except Exception:
                log_info("Sem aviso genérico")

            try:
                await page.wait_for_selector("img.fechar", timeout=10000)
                await page.locator("img.fechar").click()
                log_ok("Propaganda/popup fechada")
            except Exception:
                log_info("Sem propaganda/popup")

            log_step(6, f"Selecionando posto {consulta_posto}")
            await page.wait_for_selector(".usuario_img", timeout=90000)
            await page.locator(".usuario_img").first.click()
            log_ok("Seletor de posto aberto")

            campo_busca = page.locator('[type="text"]').first

            await campo_busca.click()
            await asyncio.sleep(0.3)

            await campo_busca.press("Control+A")
            await campo_busca.press("Delete")
            await asyncio.sleep(0.2)

            cnpj_pesquisa = str(consulta_posto).zfill(14)

            await campo_busca.fill("")
            await campo_busca.type(cnpj_pesquisa, delay=100)

            await asyncio.sleep(2)

            item_posto = page.locator("li").filter(has_text=cnpj_pesquisa)

            await asyncio.sleep(2)

            try:
                botao_trocar = item_posto.locator('button:has-text("Trocar")')
                await botao_trocar.first.click()
            except Exception:
                log_warn(f"Código do posto: {cnpj_pesquisa} não localizado.")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Código do posto: {cnpj_pesquisa} não localizado.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            await page.wait_for_selector(".usuario_img", timeout=90000)
            await asyncio.sleep(10)

            log_step(7, "Coletando combustíveis e preços")
            await page.wait_for_selector("iframe", timeout=90000)

            iframe = page.frame_locator("iframe")
            cards_outer = iframe.locator(".owl-stage")
            cards = await cards_outer.locator(".owl-item").element_handles()
            counter = len(cards)

            log_data(f"Quantidade de cards encontrados: {counter}")

            if counter <= 0:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Nenhum resultado encontrado",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

            fuel_list = []

            for i in range(counter):
                item_element = cards[i]

                title_locator = await item_element.query_selector("h6.titulo.h6")
                if title_locator:
                    fuel_name = await title_locator.text_content()
                    fuel_name = fuel_name.strip() if fuel_name else ""
                else:
                    fuel_name = "Nome não encontrado"

                price_element = await item_element.query_selector(
                    ".card-comercial_info.ml-2 .valor span:nth-of-type(2)"
                )
                fuel_price = (
                    await price_element.text_content() if price_element else "0"
                )
                fuel_price = (
                    (fuel_price or "0")
                    .replace("R$", "")
                    .replace(",", ".")
                    .replace(" ", "")
                    .strip()
                )

                try:
                    fuel_price = float(fuel_price)
                except Exception as e:
                    log_warn(f"Falha convertendo preço para float em {fuel_name}: {e}")
                    fuel_price = 0.0

                item = {
                    "name": fuel_name,
                    "price": fuel_price,
                }
                fuel_list.append(item)
                log_data(f"Item fuel_list[{i}]: {item}")

            log_ok(f"fuel_list montado com {len(fuel_list)} itens")
            logger.print(f"fuel_list montado: {fuel_list}")

            log_step(8, "Comparando itens coletados com config_entrada")
            config_entrada = await compare_itens(
                fuel_list, config_entrada, fuel_itens, "descricaoIpiranga"
            )
            log_ok("compare_itens executado com sucesso")

            log_step(
                "8A",
                "Aplicando preços reais do site no JSON final usando o de/para por UUID",
            )

            precos_entrada = config_entrada.get("precos", [])

            mapa_precos_site = {
                str(item.get("name", ""))
                .strip()
                .upper(): float(item.get("price", 0) or 0)
                for item in fuel_list
            }
            log_data(f"mapa_precos_site: {mapa_precos_site}")

            mapa_combustiveis_config = {}
            for item_cfg in fuel_itens:
                descricao_ipiranga = str(item_cfg.get("descricaoIpiranga", ""))
                uuid_cfg = item_cfg.get("uuid")

                if descricao_ipiranga and uuid_cfg:
                    descricoes = [
                        d.strip().upper() for d in descricao_ipiranga.split(",")
                    ]

                    for desc_item in descricoes:
                        mapa_combustiveis_config[desc_item] = uuid_cfg

            log_data(f"mapa_combustiveis_config: {mapa_combustiveis_config}")

            mapa_uuid_para_preco = {}
            for nome_site, preco_site in mapa_precos_site.items():
                uuid_encontrado = mapa_combustiveis_config.get(nome_site)

                if uuid_encontrado and float(preco_site) > 0:
                    mapa_uuid_para_preco[uuid_encontrado] = float(preco_site)

                    log_data(
                        f"Preço mapeado pelo de/para | "
                        f"nome_site={nome_site} | uuid={uuid_encontrado} | preco={preco_site}"
                    )
                else:
                    log_warn(
                        f"Combustível do site sem correspondência no de/para ou com preço zerado | "
                        f"nome_site={nome_site} | preco={preco_site}"
                    )

            log_data(f"mapa_uuid_para_preco: {mapa_uuid_para_preco}")

            novos_precos = []

            precos_entrada = config_entrada.get("precos", []) or []

            mapa_entrada_por_uuid = {}
            for item_preco in precos_entrada:
                uuid_item = str(item_preco.get("uuidItem", "") or "").strip()
                if uuid_item:
                    mapa_entrada_por_uuid[uuid_item] = dict(item_preco)

            log_data(f"mapa_entrada_por_uuid: {mapa_entrada_por_uuid}")

            mapa_config_por_uuid = {}
            for item_cfg in fuel_itens:
                uuid_cfg = str(item_cfg.get("uuid", "") or "").strip()
                if uuid_cfg:
                    mapa_config_por_uuid[uuid_cfg] = item_cfg

            log_data(f"mapa_config_por_uuid: {mapa_config_por_uuid}")

            for uuid_item, preco_site in mapa_uuid_para_preco.items():
                item_entrada = mapa_entrada_por_uuid.get(uuid_item)
                item_cfg = mapa_config_por_uuid.get(uuid_item, {})

                if item_entrada:
                    item_atualizado = dict(item_entrada)
                    item_atualizado["preco"] = float(preco_site)
                    item_atualizado["abreviacaoProduto"] = item_entrada.get(
                        "abreviacaoProduto"
                    )
                    item_atualizado["codigoProduto"] = item_entrada.get("codigoProduto")

                    if not item_atualizado.get("descricaoProduto"):
                        item_atualizado["descricaoProduto"] = item_cfg.get("descricao")

                    log_data(
                        f"Item atualizado a partir da config de entrada | "
                        f"uuidItem={uuid_item} | "
                        f"descricaoProduto={item_atualizado.get('descricaoProduto')} | "
                        f"preco={item_atualizado['preco']}"
                    )
                else:
                    item_atualizado = {
                        "preco": float(preco_site),
                        "uuidItem": uuid_item,
                        "abreviacaoProduto": item_cfg.get("abreviacaoProduto"),
                        "codigoProduto": item_cfg.get("codigoProduto"),
                        "descricaoProduto": item_cfg.get("descricao"),
                    }

                    log_data(
                        f"Item criado a partir do site por não existir na config de entrada | "
                        f"uuidItem={uuid_item} | "
                        f"descricaoProduto={item_atualizado.get('descricaoProduto')} | "
                        f"preco={item_atualizado['preco']}"
                    )

                novos_precos.append(item_atualizado)

            config_entrada["precos"] = novos_precos
            log_data(f"config_entrada['precos'] final: {config_entrada['precos']}")
            # ================================
            # VALIDAÇÃO: nenhum preço encontrado
            # ================================
            if not novos_precos or len(novos_precos) == 0:
                log_error("Nenhum preço válido encontrado no site após o de/para")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Nenhum preço válido encontrado no site após o de/para",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            log_step(9, "Montando JSON no padrão esperado")

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

            log_step(10, "Processo concluído com sucesso")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Processo concluído com sucesso",
                status=RpaHistoricoStatusEnum.Sucesso,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

    except Exception as e:
        log_error(f"Erro crítico no fluxo consulta_preco_ipiranga: {e}")
        try:
            await capture_and_send_screenshot(
                task.historico_id, f"Erro consulta preço ipiranga: {e}"
            )
        except Exception as e_ss:
            log_warn(f"Não foi possível enviar screenshot: {e_ss}")

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
