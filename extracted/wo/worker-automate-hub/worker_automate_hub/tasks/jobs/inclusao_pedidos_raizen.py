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
import unicodedata

from playwright.async_api import async_playwright

from worker_automate_hub.api.client import (
    get_config_by_name,
    get_mfa_code,
    get_codigo_raizen_by_cnpj,
)

from worker_automate_hub.utils.util import (
    capture_and_send_screenshot,
    ensure_browsers_installed,
    kill_all_emsys,
)

logger = Console()


def log_step(step, mensagem):
    logger.print(f"[bold cyan][STEP {step}][/bold cyan] {mensagem}")


def log_ok(mensagem):
    logger.print(f"[bold green][OK][/bold green] {mensagem}")


def log_warn(mensagem):
    logger.print(f"[bold yellow][ALERTA][/bold yellow] {mensagem}")


def log_error(mensagem):
    logger.print(f"[bold red][ERRO][/bold red] {mensagem}")


def log_data(mensagem):
    logger.print(f"[bold magenta][DADOS][/bold magenta] {mensagem}")


def normalizar_texto(txt):
    txt = str(txt or "").strip().upper()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    txt = txt.replace("'", "")
    txt = " ".join(txt.split())
    return txt


def quebrar_descricoes(descricao_raw):
    """
    Transforma:
        "GASOLINA COMUM, GASOLINA TIPO C, GASOLINA C, CONS"

    Em:
        ["GASOLINA COMUM", "GASOLINA TIPO C", "GASOLINA C", "CONS"]
    """
    return [
        normalizar_texto(desc)
        for desc in str(descricao_raw or "").split(",")
        if desc.strip()
    ]


def montar_mapa_descricoes_raizen(lista_de_para):
    """
    Monta mapa:
        uuid -> lista de possíveis descrições Raízen

    Exemplo:
        {
            "b9de72dd-aa25-4af7-9610-c5e4a43cb8b5": [
                "GASOLINA COMUM",
                "GASOLINA TIPO C",
                "GASOLINA C",
                "CONS"
            ]
        }
    """
    mapa = {}

    for item in lista_de_para:
        uuid = str(item.get("uuid", "") or "").strip()

        if not uuid:
            continue

        descricoes = []

        descricao_raizen = item.get("descricaoRaizen", "")
        descricao_padrao = item.get("descricao", "")

        for desc in quebrar_descricoes(descricao_raizen):
            if desc and desc not in descricoes:
                descricoes.append(desc)

        descricao_padrao_norm = normalizar_texto(descricao_padrao)
        if descricao_padrao_norm and descricao_padrao_norm not in descricoes:
            descricoes.append(descricao_padrao_norm)

        mapa[uuid] = descricoes

    return mapa


async def localizar_linha_combustivel(page, descricoes):
    """
    Tenta localizar a linha do combustível usando todas as descrições possíveis.
    Usa match direto pelo texto da linha.
    """
    linhas = page.locator(".orders-fuels-list__row")

    for desc in descricoes:
        if not desc:
            continue

        linha = linhas.filter(has_text=desc)

        qtd = await linha.count()

        if qtd > 0:
            log_ok(f"Linha localizada com descrição: {desc}")
            return linha.first, desc

        log_warn(f"Não encontrou linha com descrição: {desc}")

    return None, None


async def inclusao_pedidos_raizen(task: RpaProcessoEntradaDTO):
    browser = None

    try:
        log_step(1, "Inicializando robô Raízen")

        await ensure_browsers_installed()
        await kill_all_emsys()

        config_entrada = task.configEntrada or {}

        # ========================
        # CONFIG LOGIN
        # ========================
        log_step(2, "Buscando configuração ConsultaPreco")

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

            # ========================
            # ACESSO
            # ========================
            log_step(3, f"Navegando para {config.get('url_raizen')}")

            await page.goto(config.get("url_raizen"), wait_until="networkidle")
            await page.wait_for_load_state("load")

            # ========================
            # LOGIN
            # ========================
            log_step(4, "Realizando login")

            await page.locator("#signInName").type(config.get("login_raizen"))
            await page.locator("#password").type(config.get("pass_raizen"))
            await page.locator("#next").click()

            # ========================
            # MFA
            # ========================
            log_step(5, "Enviando código MFA")

            await page.locator("#readOnlyEmail_ver_but_send").click()
            await page.wait_for_load_state("load")

            log_step("5A", "Aguardando MFA por 90 segundos")
            await asyncio.sleep(90)

            code = await get_mfa_code("mfa-raizen")

            if code and code.get("status_code") == 200 and code.get("code"):
                await page.locator('//*[@id="readOnlyEmail_ver_input"]').type(
                    str(code["code"])
                )
                await page.locator('//*[@id="readOnlyEmail_ver_but_verify"]').click()
                log_ok("MFA preenchido")
            else:
                await capture_and_send_screenshot(task.historico_id, "Erro MFA")
                raise Exception("Failed to retrieve MFA code")

            # ========================
            # SELECIONAR EMPRESA
            # ========================
            log_step(6, "Selecionando empresa")

            cnpj_empresa = str(config_entrada.get("cnpjEmpresa", "")).strip()

            if not cnpj_empresa:
                await capture_and_send_screenshot(
                    task.historico_id,
                    "CNPJ não informado",
                )
                raise Exception("CNPJ da empresa não informado na config_entrada")

            codigo_raizen = await get_codigo_raizen_by_cnpj(cnpj_empresa)

            if not codigo_raizen:
                await capture_and_send_screenshot(
                    task.historico_id,
                    f"Código Raízen não encontrado para o CNPJ {cnpj_empresa}",
                )
                raise Exception(
                    f"Não foi encontrado código Raízen para o CNPJ {cnpj_empresa}"
                )

            await page.wait_for_load_state("load")

            await page.wait_for_selector(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div',
                state="visible",
            )

            await page.locator(
                '//*[@id="api"]/div/form/div[2]/app-select/div/div'
            ).click()

            cod_cnpj = str(codigo_raizen).strip().lstrip("0")

            log_data(
                f"CNPJ: {cnpj_empresa} | "
                f"codigoRaizen retornado: {codigo_raizen} | "
                f"usado na seleção: {cod_cnpj}"
            )

            element = page.locator(f'text="{cod_cnpj} - SIM REDE DE POSTOS LTDA"')
            await element.scroll_into_view_if_needed()
            await element.click()

            await page.locator('//*[@id="undefined"]').click()
            await page.wait_for_load_state("load")

            log_ok("Empresa selecionada")

            # ========================
            # COMBUSTÍVEIS CLAROS
            # ========================
            log_step(7, "Selecionando Combustíveis Claros")

            try:
                await asyncio.sleep(5)

                await page.locator(
                    "label.cso-radio-option:has-text('Combustíveis Claros')"
                ).click()

                await page.locator("button span:has-text('Acessar')").click()

                log_ok("Combustíveis Claros selecionado")
            except Exception:
                logger.print("Radio button already selected or not available")
                await asyncio.sleep(10)

            await asyncio.sleep(15)

            try:
                await page.locator(".messages__popup__button_ok").click()
            except Exception:
                pass

            # ========================
            # IR PARA PÁGINA DE PEDIDOS
            # ========================
            log_step(8, "Navegando para tela de pedidos")

            await page.goto(
                "https://portal.csonline.com.br/#/ordersfuels",
                wait_until="load",
            )

            await asyncio.sleep(5)

            # ========================
            # SELECIONAR LITROS
            # ========================
            log_step(9, "Selecionando litros")

            litro_radio = page.locator("#orders-fuels-input-radio-L")
            await litro_radio.wait_for(state="visible")

            if not await litro_radio.is_checked():
                await litro_radio.click()
                await page.wait_for_timeout(10000)
                await page.locator('//*[@id="undefined"]').click()

            # ========================
            # DATA
            # ========================
            try:
                log_step(10, "Selecionando data")

                data_retirada = config_entrada["dataRetirada"]
                data_retirada_formatada = datetime.fromisoformat(
                    data_retirada.replace("Z", "+00:00")
                ).strftime("%d/%m/%Y")

                input_elem = page.locator("#orders-fuels-div-calendar-datepicker")

                await input_elem.evaluate(
                    """
                    (el, value) => {
                        el.removeAttribute('readonly');
                        el.value = value;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    """,
                    data_retirada_formatada,
                )

                log_ok(f"Data selecionada: {data_retirada_formatada}")

            except Exception:
                await capture_and_send_screenshot(
                    task.historico_id,
                    "Erro ao realizar pedido!",
                )
                raise Exception("Erro ao selecionar data")

            # ========================
            # BASE E PLACA
            # ========================
            placa_veiculo = str(config_entrada.get("placaVeiculo", "") or "").strip()

            if "cif" not in placa_veiculo.lower():
                # Base
                try:
                    log_step(11, "Selecionando base")

                    rel_base_raizen = await get_config_by_name("relacaoBaseRaizen")
                    rel_base_raizen = rel_base_raizen.conConfiguracao

                    base_nome = rel_base_raizen[config_entrada["baseNome"]]

                    await page.locator(
                        '//*[@id="orders-fuels-div-dropdown-withdrawal-place"]'
                    ).click()

                    await page.locator(f'//*[contains(text(), "{base_nome}")]').click()

                    log_ok(f"Base selecionada: {base_nome}")

                except Exception:
                    await capture_and_send_screenshot(
                        task.historico_id,
                        "Erro ao selecionar base",
                    )
                    raise Exception("Erro ao selecionar base")

                # Placa
                try:
                    log_step(12, "Selecionando placa do veículo")

                    await page.locator(
                        '//*[@id="orders-fuels-div-dropdown-plate-place-button"]'
                    ).click()

                    await page.locator(
                        '//*[@id="orders-fuels-div-dropdown-plate-place-button"]'
                    ).fill(placa_veiculo.upper())

                    await page.locator(
                        f'//*[contains(text(), "{placa_veiculo}")]'
                    ).click()

                    log_ok(f"Placa selecionada: {placa_veiculo}")

                except Exception:
                    await capture_and_send_screenshot(
                        task.historico_id,
                        "Erro ao selecionar placa do veiculo",
                    )
                    raise Exception("Erro ao selecionar placa do veiculo")

            # ========================
            # PREENCHER COMBUSTÍVEIS
            # ========================
            try:
                log_step(13, "Preenchendo combustíveis")

                nome_config_combustiveis = "ConsultaPrecoCombustiveisIds"

                log_data(f"Buscando de/para: {nome_config_combustiveis}")

                combustiveis_ids_config = await get_config_by_name(
                    nome_config_combustiveis
                )

                lista_de_para = combustiveis_ids_config.conConfiguracao[
                    "CombustiveisIds"
                ]

                mapa_nomes_raizen = montar_mapa_descricoes_raizen(lista_de_para)

                log_data("Mapa de descrições Raízen montado:")

                for uuid, descricoes in mapa_nomes_raizen.items():
                    log_data(f"{uuid} => {descricoes}")

                for combustivel in config_entrada["combustiveis"]:
                    combustivel_uuid = str(combustivel.get("uuidItem", "") or "").strip()
                    quantidade = str(combustivel.get("quantidade", "") or "").strip()
                    descricao_entrada = combustivel.get("descricaoProduto", "")

                    if not combustivel_uuid:
                        log_warn(f"Combustível sem uuidItem ignorado: {combustivel}")
                        continue

                    if not quantidade:
                        log_warn(
                            f"Combustível sem quantidade ignorado | uuidItem={combustivel_uuid}"
                        )
                        continue

                    descricoes_raizen = mapa_nomes_raizen.get(combustivel_uuid, [])

                    # Também adiciona descricaoProduto da entrada como fallback
                    for desc_entrada in quebrar_descricoes(descricao_entrada):
                        if desc_entrada and desc_entrada not in descricoes_raizen:
                            descricoes_raizen.append(desc_entrada)

                    if not descricoes_raizen:
                        logger.print(
                            f"Produto com UUID {combustivel_uuid} não encontrado no mapa."
                        )
                        continue

                    log_data(
                        f"Buscando produto | uuid={combustivel_uuid} | "
                        f"quantidade={quantidade} | "
                        f"descricoes={descricoes_raizen}"
                    )

                    linha_produto, descricao_usada = await localizar_linha_combustivel(
                        page,
                        descricoes_raizen,
                    )

                    if not linha_produto:
                        logger.print(
                            f"Input para o produto não encontrado na tela | "
                            f"uuid={combustivel_uuid} | "
                            f"descricoes testadas={descricoes_raizen}"
                        )
                        continue

                    locator_input = linha_produto.locator(
                        "input.orders-fuels-list__quantity__value"
                    )

                    if await locator_input.count() > 0:
                        await locator_input.fill(quantidade)
                        await locator_input.blur()

                        log_ok(
                            f"Quantidade preenchida | "
                            f"produto={descricao_usada} | "
                            f"uuid={combustivel_uuid} | "
                            f"quantidade={quantidade}"
                        )
                    else:
                        logger.print(
                            f"Input para o produto '{descricao_usada}' não encontrado na linha."
                        )
                        continue

                    # Prazo faturamento
                    try:
                        dias_faturamento = int(config_entrada.get("diasFaturamento", 1))

                        if dias_faturamento != 1:
                            dropdown = linha_produto.locator(
                                "#orders-fuels-list-button-payment-term-obj"
                            )

                            await dropdown.click()

                            target_text = f" {dias_faturamento} Dias "

                            option = (
                                page.locator("button.dropdown-item")
                                .filter(has_text=target_text)
                                .first
                            )

                            await option.scroll_into_view_if_needed()
                            await option.click(force=True)

                            log_ok(
                                f"Prazo selecionado | "
                                f"produto={descricao_usada} | "
                                f"{dias_faturamento} Dias"
                            )

                    except Exception:
                        await capture_and_send_screenshot(task.historico_id, "Erro")
                        raise Exception(
                            f"Opção de {str(config_entrada.get('diasFaturamento'))} Dia(s) não encontrada"
                        )

            except Exception as e:
                await capture_and_send_screenshot(
                    task.historico_id,
                    "Erro preenchendo combustiveis",
                )
                raise Exception(f"Erro ao preencher combustiveis: {str(e)}")

            # ========================
            # SALVAR PEDIDO
            # ========================
            log_step(14, "Salvando pedido")

            await page.locator('//*[@id="orders-fuels-button-save"]').click()

            await asyncio.sleep(10)

            try:
                log_step(15, "Confirmando pedido")
                await page.get_by_text("Continuar mesmo assim").click()
            except Exception:
                pass

            await page.wait_for_load_state("load")

            # ========================
            # PEGAR NÚMERO DO PEDIDO
            # ========================
            await asyncio.sleep(10)

            log_step(16, "Capturando número do pedido")

            numero_elem = page.locator(
                '//span[contains(@class, "status__order-number__value")]'
            )

            numero_pedido = (await numero_elem.inner_text()).strip()

            if not numero_pedido:
                await capture_and_send_screenshot(
                    task.historico_id,
                    "Número do pedido não encontrado!",
                )
                raise Exception("Número do pedido não encontrado!")

            data_retirada = datetime.fromisoformat(
                config_entrada["dataRetirada"].replace("Z", "+00:00")
            )

            bof = {
                "numero_pedido": numero_pedido,
                "cnpj": config_entrada["cnpjEmpresa"],
                "data": data_retirada.strftime("%d/%m/%Y"),
            }

            await capture_and_send_screenshot(
                task.historico_id,
                "Sucesso ao realizar pedido!",
            )

            log_ok(f"Pedido criado com sucesso: {bof}")

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=str(bof),
                status=RpaHistoricoStatusEnum.Sucesso,
            )

    except Exception as e:
        try:
            await capture_and_send_screenshot(task.historico_id, "Erro")
        except Exception:
            pass

        log_error(f"An error occurred: {e}")

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
        try:
            if browser:
                await browser.close()
        except Exception:
            pass