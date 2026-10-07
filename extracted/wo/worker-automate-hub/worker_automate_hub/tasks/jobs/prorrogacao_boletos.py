# -*- coding: utf-8 -*-
import os
import sys
import io
import re
import time
import asyncio
import traceback
import openpyxl
import requests

from datetime import datetime
from typing import List, Optional

from rich.console import Console

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# ============================================================
# PYTHON PATH
# ============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
        )
    )
)


# ============================================================
# WORKER
# ============================================================

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)

from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

from worker_automate_hub.utils.credentials_manager import (
    CredentialsManager,
)

from worker_automate_hub.utils.util import worker_sleep

from worker_automate_hub.api.client import (
    send_file,
    baixa_boleto_antigo_emsys,
)

console = Console()


# ============================================================
# EXCEÇÕES
# ============================================================


class FalhaNegocio(Exception):
    pass


# ============================================================
# PROCESSO
# ============================================================


class ProrrogacaoBoletos:

    CLIENT_SAP = "800"

    TIMEOUT_CURTO = 10
    TIMEOUT_PADRAO = 30
    TIMEOUT_LONGO = 60
    TIMEOUT_DOWNLOAD = 180

    EDGE_DRIVER_PATH = r"C:\WebDriver\msedgedriver.exe"

    # ========================================================
    # URLS
    # ========================================================

    URL_SAP_INICIAL = (
        "https://vhsrkps4ci.sap.simrede.com.br:44300/"
        "sap/bc/ui2/flp?"
        "sap-client=800&"
        "sap-language=PT"
    )

    URL_CUSTOMER_LINE_ITEMS = (
        "https://vhsrkps4ci.sap.simrede.com.br:44300/"
        "sap/bc/ui2/flp?"
        "appState=lean&"
        "sap-client=800&"
        "sap-language=PT"
        "#Customer-manageLineItems"
    )

    URL_GERENCIADOR_FATURAS = (
        "https://vhsrkps4ci.sap.simrede.com.br:44300/"
        "sap/bc/ui2/flp?"
        "appState=lean&"
        "sap-client=800&"
        "sap-language=PT"
        "#ZSO_BOLETO-manage"
    )

    URL_AGRUPAMENTO_MANUAL = (
        "https://vhsrkps4ci.sap.simrede.com.br:44300/"
        "sap/bc/ui2/flp?"
        "appState=lean&"
        "sap-client=800&"
        "sap-language=PT"
        "#ZZ1_AGRP_MANUAL-display"
    )

    # ========================================================
    # LOGIN
    # ========================================================

    X_CLIENT = "//input[@id='CLIENT_FIELD-inner']"

    X_LOGIN_INPUTS = "//input[contains(@class,'loginInputField')]"

    X_LOGIN_BUTTON = (
        "//*["
        "contains(@class,'LOGIN_SUBMIT_BLOCK') "
        "or @id='LOGIN_LINK' "
        "or @id='LOGIN_SUBMIT_BLOCK'"
        "]"
    )

    # ========================================================
    # POPUP
    # ========================================================

    X_FECHAR_POPUP = "//button[" "@title='Fechar' " "or @aria-label='Fechar'" "]"

    # ========================================================
    # CUSTOMER LINE ITEMS
    # ========================================================

    X_STATUS = "//span[" "contains(@id,'SelectClearingStatus-labelText')" "]"

    X_STATUS_SETA = "//span[" "contains(@id,'SelectClearingStatus-arrow')" "]"

    X_STATUS_PARTIDAS_ABERTO = (
        "//*["
        "(@role='option' or self::li or self::div) "
        "and normalize-space(.)='Partidas em aberto'"
        "]"
    )

    X_CLIENTE = "//input[contains(@id,'Customer-inner')]"

    X_BOTAO_INICIAR = "//button[" "contains(@id,'SmartFilterBar-btnGo')" "]"

    X_DADOS_NAO_DISPONIVEIS = (
        "//span["
        "contains(@id,'TableItems-noDataMsg') "
        "and normalize-space(.)='Dados não disponíveis'"
        "]"
    )

    X_PROCESSAR_PARTIDAS_INDIVIDUAIS = "//button[" "contains(@id,'ChangeButton')" "]"

    X_PROCESSAR_ATRIBUICAO = (
        "//input[" "contains(@id,'InputChangeDocumentsAssignment-inner')" "]"
    )

    # ========================================================
    # GERENCIADOR
    # ========================================================

    X_GERENCIADOR_REFERENCIA = (
        "//input["
        "contains(@id,'listReportFilter') "
        "and contains(@id,'Referencia-inner')"
        "]"
    )

    X_GERENCIADOR_INICIAR = "//button[" "contains(@id,'listReportFilter-btnGo')" "]"

    X_GERENCIADOR_BAIXA = (
        "//button["
        "contains(@id,'action::cds_zui_fi_boleto') "
        "and contains(@id,'::baixa')"
        "]"
    )

    X_GERENCIADOR_PDF = "//button[" "contains(@id,'ShowPDFBtnButton')" "]"

    # ========================================================
    # AGRUPAMENTO
    # ========================================================

    X_AGRUPAMENTO_REFERENCIA = (
        "//input["
        "contains(@id,'listReportFilter') "
        "and contains(@id,'Referencia-inner')"
        "]"
    )

    X_AGRUPAMENTO_INICIAR = "//button[" "contains(@id,'listReportFilter-btnGo')" "]"

    X_AGRUPAMENTO_MANUAL_BOTAO = (
        "//button["
        "contains(@id,'AgrpManual') "
        "and contains(@id,'btnAgrpManualButton')"
        "]"
    )

    # ========================================================
    # CONSTRUTOR
    # ========================================================

    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: Optional[str] = None,
    ):
        self.task = task

        self.base_url = base_url.strip() if base_url else self.URL_CUSTOMER_LINE_ITEMS

        self.historico_id = str(
            getattr(
                task,
                "historico_id",
                "",
            )
            or ""
        ).strip()

        config_entrada = (
            getattr(
                task,
                "configEntrada",
                None,
            )
            or getattr(
                task,
                "config_entrada",
                None,
            )
            or {}
        )

        self.codigo_cliente = str(config_entrada.get("codigo") or "").strip()

        self.valor = config_entrada.get("valor")

        self.chave = str(config_entrada.get("chave") or "").strip()

        self.condicao_pagamento = str(config_entrada.get("condicaoPag") or "").strip()

        # ORIGINAL
        self.referencia = ""

        # NOVOS DADOS APÓS AGRUPAMENTO
        self.nova_chave_ref3 = ""
        self.nova_referencia = ""

        # CREDENCIAIS
        self.user = CredentialsManager().get_by_key("SAP_USER_DRC")

        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_DRC")

        # DOWNLOAD
        self.pasta_download = os.path.abspath(
            os.path.join(
                os.getcwd(),
                "downloads_prorrogacao_boletos",
            )
        )

        os.makedirs(
            self.pasta_download,
            exist_ok=True,
        )

        self.driver: Optional[webdriver.Edge] = None

        console.print("[INIT] ProrrogacaoBoletos inicializado.")

        console.print("[INIT] Navegador: Microsoft Edge")

        console.print(f"[INIT] Cliente: {self.codigo_cliente}")

        console.print(f"[INIT] Valor: {self.valor}")

        console.print("[INIT] Chave original: " f"{self.chave}")

        console.print("[INIT] Condição pagamento: " f"{self.condicao_pagamento}")

    # ========================================================
    # RETORNOS
    # ========================================================

    def retorno_sucesso(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:

        console.print(f"[SUCESSO] {mensagem}")

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=mensagem,
            status=(RpaHistoricoStatusEnum.Sucesso),
        )

    def retorno_erro(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:

        console.print(f"[ERRO_TECNICO] {mensagem}")

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=(RpaHistoricoStatusEnum.Falha),
            tags=[RpaTagDTO(descricao=(RpaTagEnum.Tecnico))],
        )

    def retorno_falha_negocio(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:

        console.print(f"[FALHA_NEGOCIO] {mensagem}")

        tag_negocio = getattr(
            RpaTagEnum,
            "Negocio",
            None,
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=(RpaHistoricoStatusEnum.Falha),
            tags=(
                [RpaTagDTO(descricao=tag_negocio)] if tag_negocio is not None else []
            ),
        )

    # ========================================================
    # CONFIG
    # ========================================================

    def validar_config(
        self,
    ) -> None:

        if not self.user:
            raise RuntimeError("SAP_USER_DRC não encontrado.")

        if not self.password:
            raise RuntimeError("SAP_PASSWORD_DRC não encontrado.")

        if not self.historico_id:
            raise RuntimeError("historico_id não informado.")

        if not self.codigo_cliente:
            raise RuntimeError("Código do cliente não informado.")

        if self.valor is None or str(self.valor).strip() == "":
            raise RuntimeError("Valor não informado.")

        if not self.chave:
            raise RuntimeError("Chave não informada.")

        if not self.condicao_pagamento:
            raise RuntimeError("Condição de pagamento não informada.")

    # ========================================================
    # DOWNLOAD
    # ========================================================

    def limpar_pasta_download(
        self,
    ) -> None:

        os.makedirs(
            self.pasta_download,
            exist_ok=True,
        )

        for nome in os.listdir(self.pasta_download):

            caminho = os.path.join(
                self.pasta_download,
                nome,
            )

            if not os.path.isfile(caminho):
                continue

            try:
                os.remove(caminho)

            except Exception as e:
                raise RuntimeError(
                    "Não foi possível limpar "
                    "a pasta de download. "
                    f"Arquivo: {caminho}. "
                    f"Erro: {type(e).__name__}: {e}"
                ) from e

    # ========================================================
    # EDGE
    # ========================================================

    def abrir_edge(self) -> None:
        console.print("[EDGE] Inicializando Microsoft Edge...")

        options = webdriver.EdgeOptions()

        options.add_argument("--lang=pt-BR")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")

        prefs = {
            "download.default_directory": self.pasta_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True,
            "download.open_pdf_in_system_reader": False,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.popups": 1,
        }

        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging"],
        )

        # Baixa/atualiza a versão correta do msedgedriver.exe automaticamente
        caminho_driver = EdgeChromiumDriverManager().install()

        service = Service(executable_path=caminho_driver)

        self.driver = webdriver.Edge(
            service=service,
            options=options,
        )

        self.driver.set_page_load_timeout(self.TIMEOUT_LONGO)

        try:
            self.driver.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {
                    "behavior": "allow",
                    "downloadPath": self.pasta_download,
                },
            )
            console.print("[EDGE] Download automático habilitado.")
        except Exception as e:
            console.print(
                "[EDGE][AVISO] " f"Não foi possível configurar download via CDP: {e}"
            )

        self.driver.maximize_window()

        console.print("[EDGE] Microsoft Edge inicializado.")

    def fechar_driver(
        self,
    ) -> None:

        if not self.driver:
            return

        try:
            console.print("[EDGE] Encerrando navegador...")

            self.driver.quit()

        except Exception:
            pass

        finally:
            self.driver = None

    # ========================================================
    # SELENIUM
    # ========================================================

    def aguardar_elemento(
        self,
        xpath: str,
        timeout: Optional[int] = None,
        clicavel: bool = False,
    ) -> WebElement:

        if not self.driver:
            raise RuntimeError("EdgeDriver não inicializado.")

        tempo = timeout or self.TIMEOUT_PADRAO

        if clicavel:
            condicao = EC.element_to_be_clickable(
                (
                    By.XPATH,
                    xpath,
                )
            )

        else:
            condicao = EC.visibility_of_element_located(
                (
                    By.XPATH,
                    xpath,
                )
            )

        return WebDriverWait(
            self.driver,
            tempo,
            poll_frequency=0.5,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(condicao)

    def buscar_elementos(
        self,
        xpath: str,
    ) -> List[WebElement]:

        if not self.driver:
            return []

        try:
            return self.driver.find_elements(
                By.XPATH,
                xpath,
            )

        except Exception:
            return []

    def elemento_existe(
        self,
        xpath: str,
        timeout: int = 3,
    ) -> bool:

        try:
            self.aguardar_elemento(
                xpath=xpath,
                timeout=timeout,
            )

            return True

        except Exception:
            return False

    # ========================================================
    # OVERLAY
    # ========================================================

    def desbloquear_overlay_sap(
        self,
    ) -> None:

        if not self.driver:
            return

        try:
            quantidade = self.driver.execute_script("""
                    const elementos =
                        Array.from(
                            document.querySelectorAll(
                                '.help4-wrapper, ' +
                                '[class*="help4-wrapper"], ' +
                                '[id$="-wrapper"][class*="help4"]'
                            )
                        );

                    let total = 0;

                    for (
                        const elemento
                        of elementos
                    ) {
                        const estilo =
                            window.getComputedStyle(
                                elemento
                            );

                        const rect =
                            elemento
                            .getBoundingClientRect();

                        const visivel =
                            estilo.display !== 'none' &&
                            estilo.visibility !== 'hidden' &&
                            estilo.opacity !== '0' &&
                            rect.width > 0 &&
                            rect.height > 0;

                        if (!visivel) {
                            continue;
                        }

                        elemento.style.pointerEvents =
                            'none';

                        total++;
                    }

                    return total;
                    """)

            if quantidade:
                console.print(
                    "[SAP][OVERLAY] " f"{quantidade} overlay(s) " "desbloqueado(s)."
                )

        except Exception as e:
            console.print("[SAP][OVERLAY][AVISO] " f"{type(e).__name__}: {e}")

    # ========================================================
    # INPUT SAP
    # ========================================================

    def preencher_input_sap(
        self,
        elemento: WebElement,
        valor: str,
        descricao: str,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        try:
            ActionChains(self.driver).move_to_element(elemento).perform()

        except Exception:
            pass

        try:
            elemento.click()

        except ElementClickInterceptedException:
            self.desbloquear_overlay_sap()

            try:
                elemento.click()

            except Exception:
                # Fallback técnico para elementos UI5 que recebem foco,
                # mas continuam interceptados pelo DOM.
                self.driver.execute_script(
                    "arguments[0].focus();",
                    elemento,
                )

        except Exception:
            try:
                ActionChains(self.driver).move_to_element(elemento).click().perform()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].focus();",
                    elemento,
                )

        elemento.send_keys(
            Keys.CONTROL,
            "a",
        )

        elemento.send_keys(Keys.DELETE)

        elemento.send_keys(str(valor))

        console.print("[SAP][INPUT] " f"{descricao}: {valor}")

    async def alterar_client_para_800(
        self,
    ) -> None:

        try:
            campo = self.aguardar_elemento(
                self.X_CLIENT,
                self.TIMEOUT_CURTO,
            )

            valor = str(campo.get_attribute("value") or "").strip()

            if valor != self.CLIENT_SAP:
                campo.clear()

                campo.send_keys(self.CLIENT_SAP)

        except TimeoutException:
            pass

    async def login(
        self,
    ) -> bool:

        try:
            console.print("[LOGIN] Iniciando...")

            await self.alterar_client_para_800()

            if not self.driver:
                return False

            try:
                WebDriverWait(
                    self.driver,
                    self.TIMEOUT_PADRAO,
                ).until(
                    lambda driver: len(
                        driver.find_elements(
                            By.XPATH,
                            self.X_LOGIN_INPUTS,
                        )
                    )
                    >= 2
                )

            except TimeoutException:

                if "#Customer-manageLineItems" in str(self.driver.current_url or ""):
                    return True

                return False

            inputs = self.driver.find_elements(
                By.XPATH,
                self.X_LOGIN_INPUTS,
            )

            inputs[0].clear()
            inputs[0].send_keys(self.user)

            inputs[1].clear()
            inputs[1].send_keys(self.password)

            botao = self.aguardar_elemento(
                self.X_LOGIN_BUTTON,
                self.TIMEOUT_PADRAO,
                True,
            )

            try:
                botao.click()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    botao,
                )

            await worker_sleep(5)

            console.print("[LOGIN] Login concluído.")

            return True

        except Exception:
            console.print(traceback.format_exc())

            return False

    # ========================================================
    # POPUPS
    # ========================================================

    async def fechar_popups_iniciais(
        self,
    ) -> None:

        for _ in range(3):

            try:
                if not self.elemento_existe(
                    self.X_FECHAR_POPUP,
                    2,
                ):
                    return

                botao = self.aguardar_elemento(
                    self.X_FECHAR_POPUP,
                    3,
                    True,
                )

                botao.click()

                await worker_sleep(1)

            except Exception:
                return

    # ========================================================
    # CUSTOMER
    # ========================================================

    async def acessar_customer_line_items(
        self,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        if "#Customer-manageLineItems" not in str(self.driver.current_url or ""):
            self.driver.get(self.URL_CUSTOMER_LINE_ITEMS)

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            lambda driver: "#Customer-manageLineItems" in str(driver.current_url or "")
        )

        await worker_sleep(5)

        await self.fechar_popups_iniciais()

    # ========================================================
    # CLIENTE
    # ========================================================

    async def preencher_cliente(
        self,
    ) -> None:

        console.print("[SAP][CLIENTE] " f"Preenchendo: {self.codigo_cliente}")

        campo = self.aguardar_elemento(
            self.X_CLIENTE,
            self.TIMEOUT_LONGO,
            True,
        )

        campo.click()

        campo.send_keys(
            Keys.CONTROL,
            "a",
        )

        campo.send_keys(Keys.DELETE)

        campo.send_keys(self.codigo_cliente)

        await worker_sleep(2)

        xpath_sugestao = (
            "//*["
            "(@role='row' "
            "or self::tr "
            "or self::li) "
            "and contains("
            "normalize-space(.),"
            f"'{self.codigo_cliente}'"
            ")"
            "]"
        )

        try:
            sugestao = WebDriverWait(
                self.driver,
                self.TIMEOUT_CURTO,
                poll_frequency=0.5,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        xpath_sugestao,
                    )
                )
            )

            sugestao.click()

        except Exception:
            campo.send_keys(Keys.ENTER)

        await worker_sleep(2)

    # ========================================================
    # STATUS
    # ========================================================

    async def selecionar_status_partidas_em_aberto(
        self,
    ) -> None:

        elemento = self.aguardar_elemento(
            self.X_STATUS,
            self.TIMEOUT_LONGO,
        )

        texto = str(elemento.text or "").strip()

        if texto.casefold() == "partidas em aberto":
            return

        seta = self.aguardar_elemento(
            self.X_STATUS_SETA,
            self.TIMEOUT_LONGO,
            True,
        )

        try:
            seta.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                seta,
            )

        opcao = WebDriverWait(
            self.driver,
            self.TIMEOUT_PADRAO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_STATUS_PARTIDAS_ABERTO,
                )
            )
        )

        try:
            opcao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                opcao,
            )

        await worker_sleep(2)

    # ========================================================
    # INICIAR CUSTOMER
    # ========================================================

    async def clicar_botao_iniciar(
        self,
    ) -> None:

        botao = self.aguardar_elemento(
            self.X_BOTAO_INICIAR,
            self.TIMEOUT_LONGO,
            True,
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        await worker_sleep(10)

    # ========================================================
    # SEM DADOS
    # ========================================================

    def dados_nao_disponiveis(
        self,
        timeout: int = 3,
    ) -> bool:

        try:
            elemento = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.X_DADOS_NAO_DISPONIVEIS,
                    )
                )
            )

            return (
                str(elemento.text or "").strip().casefold() == "dados não disponíveis"
            )

        except Exception:
            return False

    # ========================================================
    # CHAVE ORIGINAL + REFERÊNCIA
    # ========================================================

    @staticmethod
    def normalizar_texto_tabela(
        valor,
    ) -> str:
        return str(valor or "").replace("\u00a0", " ").strip()

    @staticmethod
    def normalizar_identificador_coluna(
        valor,
    ) -> str:
        import unicodedata

        texto = unicodedata.normalize(
            "NFD",
            str(valor or "").casefold(),
        )

        return "".join(
            caractere for caractere in texto if unicodedata.category(caractere) != "Mn"
        )

    def obter_linhas_customer_visiveis(
        self,
    ) -> List[WebElement]:
        if not self.driver:
            return []

        seletores = [
            "tr[id*='TableItems-rows-row']",
            "tr[role='row'].sapUiTableTr",
            "tr[role='row'][data-sap-ui-rowindex]",
        ]

        linhas = []
        ids_vistos = set()

        for seletor in seletores:
            try:
                encontrados = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    seletor,
                )
            except Exception:
                continue

            for linha in encontrados:
                try:
                    if not linha.is_displayed():
                        continue

                    identificador = str(linha.get_attribute("id") or id(linha))

                    if identificador in ids_vistos:
                        continue

                    ids_vistos.add(identificador)
                    linhas.append(linha)

                except StaleElementReferenceException:
                    continue

        return linhas

    def obter_celulas_linha(
        self,
        linha: WebElement,
    ) -> List[WebElement]:
        try:
            celulas = linha.find_elements(
                By.XPATH,
                "./td[@role='gridcell'] | ./td",
            )

            return [celula for celula in celulas if celula.is_displayed()]

        except StaleElementReferenceException:
            return []

    async def rolar_tabela_customer(
        self,
    ) -> bool:
        if not self.driver:
            return False

        # Tenta primeiro rolar usando a última linha visível.
        try:
            linhas = self.obter_linhas_customer_visiveis()

            if linhas:
                ultima_linha = linhas[-1]

                try:
                    ActionChains(self.driver).move_to_element(
                        ultima_linha
                    ).scroll_by_amount(
                        0,
                        650,
                    ).perform()

                    await worker_sleep(1)
                    return True

                except Exception:
                    pass
        except Exception:
            pass

        # Tenta PAGE_DOWN no grid/tabela.
        seletores_foco = [
            "tr[id*='TableItems-rows-row']",
            "table[id*='TableItems']",
            ".sapUiTable",
            ".sapMListTbl",
        ]

        for seletor in seletores_foco:
            try:
                elementos = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    seletor,
                )
            except Exception:
                continue

            for elemento in elementos:
                try:
                    if not elemento.is_displayed():
                        continue

                    ActionChains(self.driver).move_to_element(
                        elemento
                    ).click().send_keys(Keys.PAGE_DOWN).perform()

                    await worker_sleep(1)
                    return True

                except Exception:
                    continue

        # Tenta containers de scroll do SAP.
        seletores_scroll = [
            ".sapUiTableVSb",
            ".sapUiTableCtrlScr",
            ".sapUiTableCCnt",
            ".sapUiTableCnt",
            ".sapMPageScroll",
            ".sapMScrollContScroll",
            ".sapMList",
        ]

        for seletor in seletores_scroll:
            try:
                elementos = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    seletor,
                )
            except Exception:
                continue

            for elemento in elementos:
                try:
                    if not elemento.is_displayed():
                        continue

                    ActionChains(self.driver).move_to_element(
                        elemento
                    ).scroll_by_amount(
                        0,
                        650,
                    ).perform()

                    await worker_sleep(1)
                    return True

                except Exception:
                    continue

        # Último fallback: scroll da janela/viewport.
        try:
            antes = self.driver.execute_script(
                "return window.pageYOffset || document.documentElement.scrollTop || 0;"
            )

            self.driver.execute_script("window.scrollBy(0, 700);")

            await worker_sleep(1)

            depois = self.driver.execute_script(
                "return window.pageYOffset || document.documentElement.scrollTop || 0;"
            )

            return depois != antes

        except Exception:
            return False

    async def localizar_chave_e_referencia(
        self,
    ) -> str:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        chave_esperada = str(self.chave).replace("\u00a0", "").replace(" ", "").strip()

        console.print("[SAP][CHAVE] " f"Procurando Chave ref.3: {chave_esperada}")

        inicio = time.time()
        assinatura_anterior = None
        tentativas_sem_mudanca = 0
        varredura = 0

        while time.time() - inicio <= self.TIMEOUT_LONGO:
            varredura += 1

            linhas = self.obter_linhas_customer_visiveis()

            console.print(
                "[SAP][CHAVE] "
                f"Varredura {varredura}. "
                f"Linhas visíveis: {len(linhas)}"
            )

            assinatura_atual = []

            for linha in linhas:
                try:
                    celulas = self.obter_celulas_linha(linha)

                    if not celulas:
                        continue

                    textos = [
                        self.normalizar_texto_tabela(celula.text) for celula in celulas
                    ]

                    texto_linha = "|".join(textos)
                    assinatura_atual.append(texto_linha)

                    encontrou_chave = False

                    for texto in textos:
                        candidato = texto.replace("\u00a0", "").replace(" ", "").strip()

                        if candidato == chave_esperada:
                            encontrou_chave = True
                            break

                    if not encontrou_chave:
                        continue

                    console.print("[SAP][CHAVE] " "Chave encontrada na linha.")

                    console.print("[SAP][CHAVE] " f"Linha: {' | '.join(textos)}")

                    referencia = ""

                    for celula, texto in zip(
                        celulas,
                        textos,
                    ):
                        identificador = self.normalizar_identificador_coluna(
                            (
                                str(celula.get_attribute("data-sap-ui-colid") or "")
                                + " "
                                + str(celula.get_attribute("data-sap-ui-column") or "")
                                + " "
                                + str(celula.get_attribute("headers") or "")
                                + " "
                                + str(celula.get_attribute("id") or "")
                            )
                        )

                        if (
                            "documentreferenceid" in identificador
                            or "referencia" in identificador
                            or (
                                "reference" in identificador
                                and "reference3" not in identificador
                                and "ref3" not in identificador
                            )
                        ):
                            candidato = texto.replace(" ", "").strip()

                            if candidato:
                                referencia = candidato
                                break

                    # Fallback: referência gerada possui 14 dígitos.
                    if not referencia:
                        for texto in textos:
                            candidato = (
                                texto.replace("\u00a0", "").replace(" ", "").strip()
                            )

                            if (
                                candidato.isdigit()
                                and len(candidato) == 14
                                and candidato != chave_esperada
                            ):
                                referencia = candidato
                                break

                    if not referencia:
                        raise RuntimeError(
                            "A Chave ref.3 foi localizada, "
                            "mas a Referência da mesma linha "
                            "não foi identificada. "
                            f"Chave: {chave_esperada}."
                        )

                    self.referencia = referencia

                    console.print(
                        "[SAP][CHAVE] " "Chave ref.3 encontrada: " f"{chave_esperada}"
                    )

                    console.print(
                        "[SAP][CHAVE] " "Referência original: " f"{self.referencia}"
                    )

                    return self.referencia

                except StaleElementReferenceException:
                    continue

            assinatura = tuple(assinatura_atual)

            if assinatura and assinatura == assinatura_anterior:
                tentativas_sem_mudanca += 1
            else:
                tentativas_sem_mudanca = 0

            assinatura_anterior = assinatura

            # Não encerra imediatamente. Alguns grids SAP precisam
            # de mais de uma rolagem antes de virtualizar novas linhas.
            if tentativas_sem_mudanca >= 4:
                console.print(
                    "[SAP][CHAVE][AVISO] " "Tabela não mudou após várias rolagens."
                )
                break

            moveu = await self.rolar_tabela_customer()

            if not moveu:
                tentativas_sem_mudanca += 1

                if tentativas_sem_mudanca >= 4:
                    console.print(
                        "[SAP][CHAVE][AVISO] "
                        "Não foi possível continuar rolando a tabela."
                    )
                    break

            await worker_sleep(0.5)

        raise FalhaNegocio(
            "Chave ref.3 não localizada. "
            f"Cliente: {self.codigo_cliente}. "
            f"Chave: {self.chave}."
        )

    async def acessar_gerenciador_faturas(
        self,
    ) -> None:

        try:
            self.driver.switch_to.default_content()

        except Exception:
            pass

        self.driver.get(self.URL_GERENCIADOR_FATURAS)

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(lambda driver: "#ZSO_BOLETO-manage" in str(driver.current_url or ""))

        await worker_sleep(5)

        self.desbloquear_overlay_sap()

    async def preencher_referencia_gerenciador_faturas(
        self,
    ) -> None:

        campo = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.X_GERENCIADOR_REFERENCIA,
                )
            )
        )

        self.preencher_input_sap(
            campo,
            self.referencia,
            "Referência",
        )

        await worker_sleep(1)

    async def clicar_iniciar_gerenciador_faturas(
        self,
    ) -> None:

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_GERENCIADOR_INICIAR,
                )
            )
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        await worker_sleep(3)

    async def selecionar_linha_referencia_gerenciador(
        self,
    ) -> None:

        xpath = (
            "//td["
            "contains(@id,'ZC_FI_BOLETO') "
            "and contains(@id,'ListReportTable') "
            "and normalize-space(.)="
            f"'{self.referencia}'"
            "]"
        )

        celula = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    xpath,
                )
            )
        )

        id_celula = str(celula.get_attribute("id") or "")

        prefixo = id_celula.rsplit(
            "_cell",
            1,
        )[0]

        checkbox = None

        for by, seletor in [
            (
                By.ID,
                f"{prefixo}-selectMulti",
            ),
            (
                By.ID,
                f"{prefixo}-selectMulti-CbBg",
            ),
        ]:
            try:
                checkbox = WebDriverWait(
                    self.driver,
                    5,
                ).until(
                    EC.presence_of_element_located(
                        (
                            by,
                            seletor,
                        )
                    )
                )

                break

            except TimeoutException:
                continue

        if checkbox is None:
            raise RuntimeError("Checkbox da referência " "não encontrado.")

        try:
            checkbox.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                checkbox,
            )

        await worker_sleep(1)

    # ========================================================
    # BAIXA
    # ========================================================

    def verificar_janela_pos_baixa(
        self,
        timeout: int = 10,
    ) -> str:

        xpath_erro = (
            "//*[contains(" "normalize-space(.)," "'Recurso não encontrado'" ")]"
        )

        xpath_dialogo = (
            "//*[@role='dialog' "
            "or contains(@class,'sapMDialog') "
            "or contains(@class,'sapMMessageBox')]"
        )

        inicio = datetime.now()

        while (datetime.now() - inicio).total_seconds() < timeout:

            try:
                for elemento in self.driver.find_elements(
                    By.XPATH,
                    xpath_erro,
                ):
                    if elemento.is_displayed():
                        return "erro"

                for dialogo in self.driver.find_elements(
                    By.XPATH,
                    xpath_dialogo,
                ):
                    if dialogo.is_displayed():
                        return "confirmacao"

            except Exception:
                pass

            time.sleep(0.5)

        return "nenhuma"

    async def clicar_baixa_gerenciador_faturas(
        self,
    ) -> None:

        console.print("[SAP][GERENCIADOR] " "Clicando em Baixa...")

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_GERENCIADOR_BAIXA,
                )
            )
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        resultado = self.verificar_janela_pos_baixa(10)

        if resultado == "erro":
            raise FalhaNegocio("Recurso não encontrado.")

        if resultado == "confirmacao":
            console.print("[SAP][GERENCIADOR] " "Confirmação encontrada.")

            return

        # ====================================================
        # AGRUPAMENTO
        # ====================================================

        await self.acessar_agrupamento_manual()

        await self.preencher_referencia_agrupamento_manual()

        await self.clicar_iniciar_agrupamento_manual()

        await self.selecionar_linha_agrupamento_manual()

        await self.clicar_agrupamento_manual()

        await self.selecionar_banco_bb001()

        await self.selecionar_condicao_pagamento()

        await self.marcar_envio_boleto_faturamento()

        await self.confirmar_agrupamento_manual()

        await self.fechar_mensagem_apos_agrupamento()

        # ====================================================
        # VOLTA ADMINISTRAR ITENS
        # ====================================================

        await self.voltar_administrar_itens_cliente()

        await self.pesquisar_cliente_novamente()

        # Localiza:
        # DATA HOJE + VALOR

        await self.selecionar_linha_data_valor()

        # ====================================================
        # PROCESSAR PARTIDA
        # ====================================================

        await self.clicar_processar_partidas_individuais()

        await self.preencher_atribuicao_renegociado_e_confirmar()

        # ====================================================
        # VOLTA GERENCIADOR
        # ====================================================

        await self.voltar_gerenciador_faturas_apos_renegociacao()

        await self.preencher_nova_referencia_gerenciador()

        await self.clicar_iniciar_nova_referencia()

        await self.selecionar_linha_nova_referencia()

        caminho_pdf = await self.baixar_pdf_diretamente_da_nova_aba()

        console.print("[BACKOFFICE][PDF] " f"Arquivo enviado: {caminho_pdf}")

    # ========================================================
    # AGRUPAMENTO
    # ========================================================

    async def acessar_agrupamento_manual(
        self,
    ) -> None:

        try:
            self.driver.switch_to.default_content()

        except Exception:
            pass

        self.driver.get(self.URL_AGRUPAMENTO_MANUAL)

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            lambda driver: "#ZZ1_AGRP_MANUAL-display" in str(driver.current_url or "")
        )

        await worker_sleep(5)

    async def preencher_referencia_agrupamento_manual(
        self,
    ) -> None:

        campo = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.X_AGRUPAMENTO_REFERENCIA,
                )
            )
        )

        self.preencher_input_sap(
            campo,
            self.referencia,
            "Referência Agrupamento",
        )

        await worker_sleep(1)

    async def clicar_iniciar_agrupamento_manual(
        self,
    ) -> None:

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_AGRUPAMENTO_INICIAR,
                )
            )
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        await worker_sleep(5)

    async def selecionar_linha_agrupamento_manual(
        self,
    ) -> None:

        xpath = (
            "//*["
            "contains(@id,'AgrpManual') "
            "and contains(@id,'ListReportTable') "
            "and contains(@id,'-selectMulti-CbBg')"
            "]"
        )

        checkbox = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    xpath,
                )
            )
        )

        checkbox.click()

        await worker_sleep(1)

    async def clicar_agrupamento_manual(
        self,
    ) -> None:

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_AGRUPAMENTO_MANUAL_BOTAO,
                )
            )
        )

        botao.click()

        await worker_sleep(2)

    # ========================================================
    # DIALOG AGRUPAMENTO
    # ========================================================

    def obter_dialogo_agrupamento_manual(
        self,
    ) -> WebElement:

        return WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div["
                    "@role='dialog' "
                    "and contains("
                    "@id,"
                    "'dlgAgrupamentoManual'"
                    ")"
                    "]",
                )
            )
        )

    def localizar_input_dialogo_por_label(
        self,
        texto_label: str,
    ) -> WebElement:

        dialogo = self.obter_dialogo_agrupamento_manual()

        label = dialogo.find_element(
            By.XPATH,
            ".//*["
            "self::label "
            "or contains(@class,'sapMLabel')"
            "]"
            "[contains("
            "normalize-space(.),"
            f"'{texto_label}'"
            ")]",
        )

        label_id = str(label.get_attribute("id") or "")

        if label_id:
            try:
                return dialogo.find_element(
                    By.XPATH,
                    ".//input[" "contains(" "@aria-labelledby," f"'{label_id}'" ")" "]",
                )

            except Exception:
                pass

        return label.find_element(
            By.XPATH,
            "./following::input[1]",
        )

    async def abrir_ajuda_valores_do_input(
        self,
        input_elemento: WebElement,
        nome_campo: str,
    ) -> None:

        input_id = str(input_elemento.get_attribute("id") or "")

        ajuda = None

        if input_id.endswith("-inner"):
            base_id = input_id[: -len("-inner")]

            try:
                ajuda = WebDriverWait(
                    self.driver,
                    self.TIMEOUT_PADRAO,
                ).until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            f"{base_id}-vhi",
                        )
                    )
                )

            except TimeoutException:
                ajuda = None

        if ajuda is None:
            container = input_elemento.find_element(
                By.XPATH,
                "./ancestor::*" "[contains(" "@class," "'sapMInputBase'" ")][1]",
            )

            ajuda = container.find_element(
                By.XPATH,
                ".//*["
                "@role='button' "
                "and ("
                "contains(@id,'-vhi') "
                "or "
                "@aria-label="
                "'Visualizar entradas possíveis'"
                ")"
                "]",
            )

        ajuda.click()

        await worker_sleep(2)

    def obter_dialogo_selecao_valor(
        self,
        titulo: str,
    ) -> WebElement:

        def localizar(
            driver,
        ):
            for dlg in driver.find_elements(
                By.XPATH,
                "//*[@role='dialog' " "or contains(@class,'sapMDialog')]",
            ):
                try:
                    if not dlg.is_displayed():
                        continue

                    dlg_id = str(dlg.get_attribute("id") or "")

                    if "dlgAgrupamentoManual" in dlg_id:
                        continue

                    texto = str(dlg.text or "")

                    if titulo.casefold() in texto.casefold():
                        return dlg

                except Exception:
                    continue

            return False

        return WebDriverWait(
            self.driver,
            self.TIMEOUT_PADRAO,
        ).until(localizar)

    async def pesquisar_e_selecionar_valor(
        self,
        titulo_dialogo: str,
        codigo: str,
        descricao_log: str,
    ) -> None:

        dialogo = self.obter_dialogo_selecao_valor(titulo_dialogo)

        campo = dialogo.find_element(
            By.XPATH,
            ".//input[" "@placeholder='Procurar' " "or contains(@class,'sapMSFI')" "]",
        )

        campo.click()

        campo.send_keys(
            Keys.CONTROL,
            "a",
        )

        campo.send_keys(Keys.DELETE)

        campo.send_keys(codigo)

        botao = dialogo.find_element(
            By.XPATH,
            ".//button["
            "normalize-space(.)='Iniciar' "
            "or .//*["
            "normalize-space(.)='Iniciar'"
            "]"
            "]",
        )

        botao.click()

        await worker_sleep(2)

        linha = dialogo.find_element(
            By.XPATH,
            ".//tr["
            "@role='row' "
            "and .//*["
            "normalize-space(.)="
            f"'{codigo}'"
            "]"
            "]",
        )

        celula = linha.find_element(
            By.XPATH,
            ".//*[" "normalize-space(.)=" f"'{codigo}'" "]",
        )

        ActionChains(self.driver).move_to_element(celula).pause(0.3).double_click(
            celula
        ).perform()

        console.print("[SAP][AGRUPAMENTO] " f"{descricao_log}: {codigo}")

        await worker_sleep(1)

    async def selecionar_banco_bb001(
        self,
    ) -> None:

        campo = self.localizar_input_dialogo_por_label("Banco")

        await self.abrir_ajuda_valores_do_input(
            campo,
            "Banco",
        )

        await self.pesquisar_e_selecionar_valor(
            "Selecionar: Banco",
            "BB001",
            "Banco",
        )

    async def selecionar_condicao_pagamento(
        self,
    ) -> None:

        campo = self.localizar_input_dialogo_por_label("Condições pgto.")

        await self.abrir_ajuda_valores_do_input(
            campo,
            "Condições pgto.",
        )

        await self.pesquisar_e_selecionar_valor(
            "Selecionar: Condições pgto.",
            self.condicao_pagamento,
            "Condições pgto.",
        )

    async def marcar_envio_boleto_faturamento(
        self,
    ) -> None:

        dialogo = self.obter_dialogo_agrupamento_manual()

        label = dialogo.find_element(
            By.XPATH,
            ".//*["
            "self::label "
            "or contains(@class,'sapMLabel')"
            "]"
            "[contains("
            "normalize-space(.),"
            "'Envio do boleto/faturamento'"
            ")]",
        )

        checkbox = label.find_element(
            By.XPATH,
            "./following::*[" "@role='checkbox' " "or contains(@class,'sapMCb')" "][1]",
        )

        aria = str(checkbox.get_attribute("aria-checked") or "").lower()

        classes = str(checkbox.get_attribute("class") or "")

        if aria != "true" and "sapMCbMarkChecked" not in classes:
            checkbox.click()

        await worker_sleep(1)

    async def confirmar_agrupamento_manual(
        self,
    ) -> None:

        dialogo = self.obter_dialogo_agrupamento_manual()

        botao = dialogo.find_element(
            By.XPATH,
            ".//button["
            "normalize-space(.)="
            "'Agrupamento manual' "
            "or .//*["
            "normalize-space(.)="
            "'Agrupamento manual'"
            "]"
            "]",
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

    # ========================================================
    # MENSAGENS
    # ========================================================

    async def fechar_mensagem_apos_agrupamento(
        self,
    ) -> None:

        xpath_dialogo = (
            "//div["
            "@role='dialog' "
            "and ("
            "contains(@id,'messageDialog') "
            "or .//*["
            "normalize-space(.)='Mensagens'"
            "]"
            ")"
            "]"
        )

        dialogo = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    xpath_dialogo,
                )
            )
        )

        console.print("[SAP][AGRUPAMENTO][MENSAGEM]")

        console.print(str(dialogo.text or ""))

        botao = dialogo.find_element(
            By.XPATH,
            ".//button["
            "contains(@id,'Close') "
            "or normalize-space(.)='Fechar' "
            "or .//*["
            "normalize-space(.)='Fechar'"
            "]"
            "]",
        )

        botao.click()

        WebDriverWait(
            self.driver,
            self.TIMEOUT_PADRAO,
        ).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    xpath_dialogo,
                )
            )
        )

    # ========================================================
    # VOLTA CUSTOMER
    # ========================================================

    async def voltar_administrar_itens_cliente(
        self,
    ) -> None:

        try:
            self.driver.switch_to.default_content()

        except Exception:
            pass

        self.driver.get(self.URL_CUSTOMER_LINE_ITEMS)

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            lambda driver: "#Customer-manageLineItems" in str(driver.current_url or "")
        )

        await worker_sleep(5)

        await self.fechar_popups_iniciais()

        self.desbloquear_overlay_sap()

    async def pesquisar_cliente_novamente(
        self,
    ) -> None:

        await self.preencher_cliente()

        await self.selecionar_status_partidas_em_aberto()

        await self.clicar_botao_iniciar()

        if self.dados_nao_disponiveis(5):
            raise FalhaNegocio("Dados não disponíveis " "na segunda consulta.")

    # ========================================================
    # NORMALIZAR VALOR
    # ========================================================

    @staticmethod
    def normalizar_valor_para_comparacao(
        valor,
    ) -> str:

        if valor is None:
            return ""

        texto = (
            str(valor)
            .strip()
            .replace("R$", "")
            .replace("BRL", "")
            .replace("\u00a0", "")
            .replace(" ", "")
        )

        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")

        try:
            return f"{float(texto):.2f}"

        except Exception:
            return texto

    # ========================================================
    # DATA + VALOR + NOVA CHAVE + NOVA REFERÊNCIA
    # ========================================================

    async def selecionar_linha_data_valor(
        self,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        data_ponto = datetime.now().strftime("%d.%m.%Y")

        data_barra = datetime.now().strftime("%d/%m/%Y")

        valor_esperado = self.normalizar_valor_para_comparacao(self.valor)

        console.print("[SAP][NOVA_LINHA] " f"Data esperada: {data_ponto}")

        console.print("[SAP][NOVA_LINHA] " f"Valor esperado: {valor_esperado}")

        inicio = time.time()
        assinaturas_vistas = set()
        tentativas_sem_mudanca = 0

        while time.time() - inicio <= self.TIMEOUT_LONGO:
            linhas = self.obter_linhas_customer_visiveis()

            assinatura_atual = []

            for linha in linhas:
                try:
                    celulas = self.obter_celulas_linha(linha)

                    if not celulas:
                        continue

                    textos = [
                        self.normalizar_texto_tabela(celula.text) for celula in celulas
                    ]

                    texto_linha = " | ".join(texto for texto in textos if texto)

                    assinatura_atual.append(texto_linha)

                    possui_data = any(
                        data_ponto in texto or data_barra in texto for texto in textos
                    )

                    if not possui_data:
                        continue

                    possui_valor = any(
                        self.normalizar_valor_para_comparacao(texto) == valor_esperado
                        for texto in textos
                    )

                    if not possui_valor:
                        continue

                    nova_chave = ""
                    nova_referencia = ""

                    for celula, texto in zip(
                        celulas,
                        textos,
                    ):
                        identificador = self.normalizar_identificador_coluna(
                            (
                                str(celula.get_attribute("data-sap-ui-colid") or "")
                                + " "
                                + str(celula.get_attribute("id") or "")
                            )
                        )

                        if (
                            "reference3" in identificador or "ref3" in identificador
                        ) and texto:
                            nova_chave = texto.replace(" ", "").strip()

                        eh_referencia = (
                            (
                                "documentreferenceid" in identificador
                                or "referencia" in identificador
                                or "reference" in identificador
                            )
                            and "reference3" not in identificador
                            and "ref3" not in identificador
                            and "chaveref" not in identificador
                        )

                        if eh_referencia and texto:
                            nova_referencia = texto.replace(" ", "").strip()

                    # Fallback por formato dos dados exibidos.
                    if not nova_chave:
                        for texto in textos:
                            candidato = texto.replace(" ", "").strip()

                            if candidato.isdigit() and 18 <= len(candidato) <= 25:
                                nova_chave = candidato
                                break

                    if not nova_referencia:
                        for texto in textos:
                            candidato = texto.replace(" ", "").strip()

                            if (
                                candidato.isdigit()
                                and len(candidato) == 14
                                and candidato != nova_chave
                            ):
                                nova_referencia = candidato
                                break

                    id_linha = str(linha.get_attribute("id") or "").strip()

                    console.print("[SAP][NOVA_LINHA] " "Linha encontrada:")

                    console.print(texto_linha)

                    if not id_linha:
                        raise RuntimeError("ID da nova linha " "não identificado.")

                    if not nova_chave:
                        raise RuntimeError("Nova Chave ref.3 " "não identificada.")

                    if not nova_referencia:
                        raise RuntimeError("Nova Referência " "não identificada.")

                    self.nova_chave_ref3 = nova_chave

                    self.nova_referencia = nova_referencia

                    console.print(
                        "[SAP][NOVA_LINHA] "
                        "Nova Chave ref.3: "
                        f"{self.nova_chave_ref3}"
                    )

                    console.print(
                        "[SAP][NOVA_LINHA] "
                        "Nova Referência: "
                        f"{self.nova_referencia}"
                    )

                    await self.selecionar_linha_por_id(id_linha)

                    return

                except StaleElementReferenceException:
                    continue

            assinatura = tuple(assinatura_atual)

            if assinatura in assinaturas_vistas:
                tentativas_sem_mudanca += 1
            else:
                assinaturas_vistas.add(assinatura)
                tentativas_sem_mudanca = 0

            if tentativas_sem_mudanca >= 2:
                break

            if not await self.rolar_tabela_customer():
                break

        raise FalhaNegocio(
            "Não foi localizada linha "
            "com data de hoje e valor informado. "
            f"Data: {data_ponto}. "
            f"Valor: {self.valor}."
        )

    async def selecionar_linha_por_id(
        self,
        id_linha: str,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        if not id_linha:
            raise RuntimeError("ID da linha não informado.")

        console.print("[SAP][NOVA_LINHA] " f"ID da linha encontrada: {id_linha}")

        match = re.search(
            r"-rows-row(\d+)$",
            id_linha,
        )

        if not match:
            raise RuntimeError(
                "Não foi possível identificar "
                "o índice visual da linha SAP. "
                f"ID recebido: {id_linha}"
            )

        indice_linha = match.group(1)

        console.print("[SAP][NOVA_LINHA] " f"Índice visual SAP: {indice_linha}")

        prefixo = re.sub(
            r"-rows-row\d+$",
            "",
            id_linha,
        )

        id_selecao = f"{prefixo}-rowsel{indice_linha}"

        console.print("[SAP][NOVA_LINHA] " "ID da célula de seleção: " f"{id_selecao}")

        # ====================================================
        # LOCALIZA CELULA ROWSEL
        # ====================================================

        try:
            celula_selecao = WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.5,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        id_selecao,
                    )
                )
            )

        except TimeoutException as e:
            raise RuntimeError(
                "Célula de seleção da linha "
                "não encontrada. "
                f"ID esperado: {id_selecao}"
            ) from e

        # ====================================================
        # ESTADO ANTES
        # ====================================================

        aria_selected = (
            str(celula_selecao.get_attribute("aria-selected") or "").strip().lower()
        )

        console.print("[SAP][NOVA_LINHA] " "aria-selected antes: " f"{aria_selected}")

        if aria_selected == "true":
            console.print("[SAP][NOVA_LINHA] " "Linha já estava selecionada.")

            return

        # ====================================================
        # SCROLL
        # ====================================================

        try:
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block:'center',
                    inline:'center'
                });
                """,
                celula_selecao,
            )

        except Exception:
            pass

        await worker_sleep(0.5)

        # ====================================================
        # PRIMEIRA TENTATIVA
        # ====================================================

        try:
            celula_selecao.click()

        except ElementClickInterceptedException:

            console.print("[SAP][NOVA_LINHA][AVISO] " "Clique interceptado.")

            self.desbloquear_overlay_sap()

            celula_selecao = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        id_selecao,
                    )
                )
            )

            try:
                celula_selecao.click()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    celula_selecao,
                )

        except StaleElementReferenceException:

            celula_selecao = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        id_selecao,
                    )
                )
            )

            try:
                celula_selecao.click()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    celula_selecao,
                )

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                celula_selecao,
            )

        await worker_sleep(1)

        # ====================================================
        # VERIFICA SE SELECIONOU
        # ====================================================

        def linha_esta_selecionada(
            driver,
        ):
            try:
                elemento = driver.find_element(
                    By.ID,
                    id_selecao,
                )

                aria = (
                    str(elemento.get_attribute("aria-selected") or "").strip().lower()
                )

                classes = str(elemento.get_attribute("class") or "")

                return aria == "true" or "sapUiTableRowSelectionCellSelected" in classes

            except Exception:
                return False

        try:
            WebDriverWait(
                self.driver,
                5,
                poll_frequency=0.25,
            ).until(linha_esta_selecionada)

        except TimeoutException:

            console.print(
                "[SAP][NOVA_LINHA][AVISO] "
                "Primeira tentativa não confirmou "
                "a seleção."
            )

            # ================================================
            # SEGUNDA TENTATIVA COM ACTIONCHAINS
            # ================================================

            celula_selecao = self.driver.find_element(
                By.ID,
                id_selecao,
            )

            ActionChains(self.driver).move_to_element(celula_selecao).pause(0.2).click(
                celula_selecao
            ).perform()

            await worker_sleep(1)

        # ====================================================
        # VALIDAÇÃO FINAL
        # ====================================================

        celula_selecao = self.driver.find_element(
            By.ID,
            id_selecao,
        )

        aria_selected = (
            str(celula_selecao.get_attribute("aria-selected") or "").strip().lower()
        )

        classes = str(celula_selecao.get_attribute("class") or "")

        selecionada = (
            aria_selected == "true" or "sapUiTableRowSelectionCellSelected" in classes
        )

        console.print("[SAP][NOVA_LINHA] " "aria-selected depois: " f"{aria_selected}")

        if not selecionada:
            raise RuntimeError(
                "A linha correta foi localizada, "
                "mas não foi possível selecioná-la. "
                f"ID linha: {id_linha}. "
                f"ID seleção: {id_selecao}. "
                "Nova Referência: "
                f"{self.nova_referencia}. "
                "Nova Chave ref.3: "
                f"{self.nova_chave_ref3}."
            )

        console.print("[SAP][NOVA_LINHA] " "Linha selecionada com sucesso.")

        console.print(
            "[SAP][NOVA_LINHA] " "Nova Referência: " f"{self.nova_referencia}"
        )

        console.print(
            "[SAP][NOVA_LINHA] " "Nova Chave ref.3: " f"{self.nova_chave_ref3}"
        )

    # ========================================================
    # PROCESSAR PARTIDAS INDIVIDUAIS
    # ========================================================

    async def clicar_processar_partidas_individuais(
        self,
    ) -> None:

        console.print(
            "[SAP][PARTIDAS] " "Aguardando botão " "'Processar partidas individuais'..."
        )

        self.desbloquear_overlay_sap()

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
            poll_frequency=0.5,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_PROCESSAR_PARTIDAS_INDIVIDUAIS,
                )
            )
        )

        try:
            botao.click()

        except ElementClickInterceptedException:
            self.desbloquear_overlay_sap()

            try:
                botao.click()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    botao,
                )

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        console.print("[SAP][PARTIDAS] " "Processar partidas individuais clicado.")

        await worker_sleep(2)

    # ========================================================
    # RENEGOCIADO + OK
    # ========================================================

    async def preencher_atribuicao_renegociado_e_confirmar(
        self,
    ) -> None:

        xpath_dialogo = (
            "//div["
            "@role='dialog' "
            "and ("
            ".//*[contains("
            "normalize-space(.),"
            "'Processar 1 partida indiv.'"
            ")] "
            "or contains("
            "@id,"
            "'ChangeDocuments'"
            ")"
            ")"
            "]"
        )

        dialogo = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    xpath_dialogo,
                )
            )
        )

        campo = WebDriverWait(
            dialogo,
            self.TIMEOUT_PADRAO,
        ).until(
            lambda dlg: dlg.find_element(
                By.XPATH,
                ".//input["
                "contains("
                "@id,"
                "'InputChangeDocumentsAssignment-inner'"
                ")"
                "]",
            )
        )

        self.preencher_input_sap(
            campo,
            "RENEGOCIADO",
            "Atribuição",
        )

        await worker_sleep(1)

        campo = self.driver.find_element(
            By.XPATH,
            self.X_PROCESSAR_ATRIBUICAO,
        )

        valor = str(campo.get_attribute("value") or "").strip()

        if valor != "RENEGOCIADO":
            raise RuntimeError("Atribuição incorreta. " f"Encontrado: {valor}")

        console.print("[SAP][PARTIDAS] " "Atribuição = RENEGOCIADO.")

        botao_ok = dialogo.find_element(
            By.XPATH,
            ".//button["
            "contains("
            "@id,"
            "'ButtonChangeDocuments'"
            ") "
            "or normalize-space(.)='OK'"
            "]",
        )

        try:
            botao_ok.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao_ok,
            )

        console.print("[SAP][PARTIDAS] OK clicado.")

        WebDriverWait(
            self.driver,
            self.TIMEOUT_PADRAO,
        ).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    xpath_dialogo,
                )
            )
        )

        await worker_sleep(1)

    # ========================================================
    # VOLTA GERENCIADOR
    # ========================================================

    async def voltar_gerenciador_faturas_apos_renegociacao(
        self,
    ) -> None:

        try:
            self.driver.switch_to.default_content()

        except Exception:
            pass

        self.driver.get(self.URL_GERENCIADOR_FATURAS)

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(lambda driver: "#ZSO_BOLETO-manage" in str(driver.current_url or ""))

        await worker_sleep(5)

        self.desbloquear_overlay_sap()

        console.print(
            "[SAP][GERENCIADOR] "
            "Nova Referência disponível: "
            f"{self.nova_referencia}"
        )

    # ========================================================
    # NOVA REFERÊNCIA GERENCIADOR
    # ========================================================

    async def preencher_nova_referencia_gerenciador(
        self,
    ) -> None:

        if not self.nova_referencia:
            raise RuntimeError("Nova Referência não armazenada.")

        campo = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.X_GERENCIADOR_REFERENCIA,
                )
            )
        )

        self.preencher_input_sap(
            campo,
            self.nova_referencia,
            "Nova Referência",
        )

        await worker_sleep(1)

    async def clicar_iniciar_nova_referencia(
        self,
    ) -> None:

        botao = WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.X_GERENCIADOR_INICIAR,
                )
            )
        )

        try:
            botao.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        await worker_sleep(3)

    async def selecionar_linha_nova_referencia(
        self,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        if not self.nova_referencia:
            raise RuntimeError("Nova Referência não disponível.")

        console.print(
            "[SAP][GERENCIADOR] "
            "Procurando linha da nova Referência: "
            f"{self.nova_referencia}"
        )

        # Localiza somente a linha visível que contém a nova referência.
        xpath_linha = (
            "//tr["
            "contains(@id,'ListReportTable') "
            "and .//*[normalize-space(.)="
            f"'{self.nova_referencia}'"
            "]"
            "]"
        )

        def localizar_linha_visivel(driver):
            for elemento in driver.find_elements(
                By.XPATH,
                xpath_linha,
            ):
                try:
                    if elemento.is_displayed():
                        return elemento
                except StaleElementReferenceException:
                    continue
            return False

        try:
            linha = WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(localizar_linha_visivel)
        except TimeoutException as e:
            raise RuntimeError(
                "Linha visível da nova Referência não encontrada. "
                f"Referência: {self.nova_referencia}."
            ) from e

        id_linha = str(linha.get_attribute("id") or "").strip()

        texto_linha = str(linha.text or "").strip()

        console.print("[SAP][GERENCIADOR] " f"ID da linha: {id_linha}")

        console.print("[SAP][GERENCIADOR] " f"Linha localizada: {texto_linha}")

        # DOM real do SAP:
        # ...ColumnListItem-__clone599-selectMulti
        xpath_checkbox = ".//*[@role='checkbox' " "and contains(@id,'-selectMulti')]"

        def localizar_checkbox_visivel(row):
            for elemento in row.find_elements(
                By.XPATH,
                xpath_checkbox,
            ):
                try:
                    if elemento.is_displayed():
                        return elemento
                except StaleElementReferenceException:
                    continue
            return False

        try:
            checkbox = WebDriverWait(
                linha,
                self.TIMEOUT_PADRAO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(localizar_checkbox_visivel)
        except TimeoutException as e:
            raise RuntimeError(
                "A linha da nova Referência foi localizada, "
                "mas o checkbox selectMulti não foi encontrado. "
                f"Referência: {self.nova_referencia}."
            ) from e

        id_checkbox = str(checkbox.get_attribute("id") or "").strip()

        if not id_checkbox:
            raise RuntimeError("Checkbox da nova Referência sem ID.")

        aria_antes = str(checkbox.get_attribute("aria-checked") or "").strip().lower()

        console.print("[SAP][GERENCIADOR] " f"Checkbox: {id_checkbox}")

        console.print("[SAP][GERENCIADOR] " f"aria-checked antes: {aria_antes}")

        if aria_antes != "true":
            # Primeiro tenta o fundo visual interno do checkbox.
            id_checkbox_bg = f"{id_checkbox}-CbBg"

            try:
                alvo_clique = WebDriverWait(
                    self.driver,
                    3,
                    poll_frequency=0.2,
                ).until(
                    EC.presence_of_element_located(
                        (
                            By.ID,
                            id_checkbox_bg,
                        )
                    )
                )
                console.print("[SAP][GERENCIADOR] " "Usando CbBg interno para seleção.")
            except TimeoutException:
                alvo_clique = checkbox
                console.print(
                    "[SAP][GERENCIADOR] " "CbBg não encontrado; usando selectMulti."
                )

            try:
                ActionChains(self.driver).move_to_element(alvo_clique).pause(
                    0.2
                ).click().perform()

            except ElementClickInterceptedException:
                self.desbloquear_overlay_sap()
                ActionChains(self.driver).move_to_element(alvo_clique).click().perform()

            except StaleElementReferenceException:
                checkbox = self.driver.find_element(
                    By.ID,
                    id_checkbox,
                )
                ActionChains(self.driver).move_to_element(checkbox).click().perform()

            except Exception:
                # Fallback técnico para controles UI5.
                checkbox = self.driver.find_element(
                    By.ID,
                    id_checkbox,
                )
                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox,
                )

        def checkbox_marcado(driver):
            try:
                elemento = driver.find_element(
                    By.ID,
                    id_checkbox,
                )
                return (
                    str(elemento.get_attribute("aria-checked") or "").strip().lower()
                    == "true"
                )
            except Exception:
                return False

        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_CURTO,
                poll_frequency=0.25,
            ).until(checkbox_marcado)
        except TimeoutException as e:
            raise RuntimeError(
                "A linha foi encontrada, mas o checkbox não foi "
                "marcado pelo SAP. "
                f"Referência: {self.nova_referencia}. "
                f"Checkbox: {id_checkbox}."
            ) from e

        checkbox = self.driver.find_element(
            By.ID,
            id_checkbox,
        )

        aria_depois = str(checkbox.get_attribute("aria-checked") or "").strip().lower()

        console.print("[SAP][GERENCIADOR] " f"aria-checked depois: {aria_depois}")

        console.print(
            "[SAP][GERENCIADOR] " "Linha da nova Referência selecionada com sucesso."
        )

        # Só continua quando o PDF realmente ficar habilitado.
        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_GERENCIADOR_PDF,
                    )
                )
            )
        except TimeoutException as e:
            raise RuntimeError(
                "A linha foi selecionada, mas o botão PDF "
                "não ficou habilitado. "
                f"Referência: {self.nova_referencia}."
            ) from e

        console.print("[SAP][GERENCIADOR] " "Botão PDF habilitado.")

    # ========================================================
    # PDF
    # ========================================================

    async def clicar_pdf_gerenciador(
        self,
    ) -> None:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        console.print("[SAP][PDF] " "Aguardando botão PDF...")

        try:
            botao = WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_GERENCIADOR_PDF,
                    )
                )
            )
        except TimeoutException as e:
            raise RuntimeError(
                "Botão PDF não ficou habilitado após a seleção "
                "da nova Referência. "
                f"Referência: {self.nova_referencia}."
            ) from e

        try:
            botao.click()
        except ElementClickInterceptedException:
            self.desbloquear_overlay_sap()
            try:
                botao.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    botao,
                )
        except StaleElementReferenceException:
            botao = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_GERENCIADOR_PDF,
                    )
                )
            )
            botao.click()
        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao,
            )

        console.print("[SAP][PDF] Botão PDF clicado.")

    async def enviar_pdf_backoffice(
        self,
        caminho_pdf: str,
    ) -> str:

        if not caminho_pdf:
            raise RuntimeError("Caminho do PDF não informado para envio ao backoffice.")

        if not os.path.isfile(caminho_pdf):
            raise RuntimeError(
                "PDF não encontrado para envio ao backoffice. "
                f"Arquivo: {caminho_pdf}"
            )

        nome_arquivo = os.path.basename(caminho_pdf)

        console.print("[BACKOFFICE][PDF] " f"Preparando envio: {nome_arquivo}")

        with open(
            caminho_pdf,
            "rb",
        ) as arquivo:
            file_bytes = io.BytesIO(arquivo.read())

        try:
            await send_file(
                self.historico_id,
                nome_arquivo,
                "pdf",
                file_bytes,
                file_extension="pdf",
            )

            console.print("[BACKOFFICE][PDF] " "Arquivo enviado com sucesso.")

        except Exception as e:
            raise RuntimeError(
                "Boleto PDF gerado com sucesso, porém ocorreu erro "
                "ao enviar o arquivo para o backoffice. "
                f"Erro: {type(e).__name__}: {e}. "
                "O arquivo permanece salvo no dispositivo em: "
                f"{caminho_pdf}"
            ) from e

        try:
            os.remove(caminho_pdf)

            console.print("[BACKOFFICE][PDF] " "Arquivo local removido após o envio.")

        except Exception as e:
            console.print(
                "[BACKOFFICE][PDF][AVISO] "
                "Arquivo enviado, mas não foi possível remover "
                f"o arquivo local: {type(e).__name__}: {e}"
            )

        return nome_arquivo

    async def baixar_pdf_diretamente_da_nova_aba(
        self,
    ) -> str:

        if not self.driver:
            raise RuntimeError("Driver não inicializado.")

        console.print("[SAP][PDF] " "Iniciando geração, download e envio do boleto...")

        handle_sap = self.driver.current_window_handle

        # ====================================================
        # 1 - CLICA EM PDF NO GERENCIADOR
        # ====================================================

        await self.clicar_pdf_gerenciador()

        # ====================================================
        # 2 - AGUARDA A JANELA VISUALIZAR
        # ====================================================

        console.print("[SAP][PDF] " "Aguardando janela Visualizar...")

        xpath_popup_pdf = "//div[" "@role='dialog' " "and contains(@id,'pdfviewer')" "]"

        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        xpath_popup_pdf,
                    )
                )
            )

        except TimeoutException as e:
            raise RuntimeError(
                "Após clicar em PDF, a janela Visualizar "
                "não foi apresentada pelo SAP."
            ) from e

        console.print("[SAP][PDF] " "Janela Visualizar aberta.")

        # ====================================================
        # 3 - AGUARDA O BOTÃO BAIXAR DO VISUALIZADOR
        # ====================================================

        xpath_baixar_visualizador = "//button[contains(@id,'popupDownloadButton')]"

        console.print("[SAP][PDF] " "Aguardando botão Baixar do visualizador...")

        try:
            botao_baixar = WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        xpath_baixar_visualizador,
                    )
                )
            )

        except TimeoutException as e:
            raise RuntimeError(
                "A janela Visualizar abriu, mas o botão Baixar " "não ficou disponível."
            ) from e

        console.print(
            "[SAP][PDF] "
            "Botão Baixar localizado: "
            f"{botao_baixar.get_attribute('id')}"
        )

        # Cookies e user-agent são capturados ainda na sessão SAP.
        cookies_sap = self.driver.get_cookies()

        try:
            user_agent = self.driver.execute_script("return navigator.userAgent;")
        except Exception:
            user_agent = "Mozilla/5.0"

        handles_antes = set(self.driver.window_handles)

        # ====================================================
        # 4 - CLICA EM BAIXAR
        # ====================================================

        try:
            botao_baixar.click()

        except ElementClickInterceptedException:
            self.desbloquear_overlay_sap()

            try:
                botao_baixar.click()
            except Exception:
                ActionChains(self.driver).move_to_element(
                    botao_baixar
                ).click().perform()

        except StaleElementReferenceException:
            botao_baixar = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                poll_frequency=0.25,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        xpath_baixar_visualizador,
                    )
                )
            )
            botao_baixar.click()

        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                botao_baixar,
            )

        console.print("[SAP][PDF] " "Botão Baixar clicado.")

        # ====================================================
        # 5 - AGUARDA A NOVA ABA DO BOLETO
        # ====================================================

        console.print("[SAP][PDF] " "Aguardando abertura da nova aba do boleto...")

        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.25,
            ).until(lambda driver: len(set(driver.window_handles) - handles_antes) > 0)

        except TimeoutException as e:
            raise RuntimeError(
                "O botão Baixar foi clicado, mas nenhuma nova aba "
                "do boleto foi aberta."
            ) from e

        novos_handles = list(set(self.driver.window_handles) - handles_antes)

        if not novos_handles:
            raise RuntimeError("Não foi possível identificar a nova aba do boleto.")

        handle_pdf = novos_handles[-1]
        caminho_pdf = ""

        try:
            # ================================================
            # 6 - CAPTURA URL ODATA DO PDF
            # ================================================

            self.driver.switch_to.window(handle_pdf)

            try:
                WebDriverWait(
                    self.driver,
                    self.TIMEOUT_LONGO,
                    poll_frequency=0.25,
                ).until(
                    lambda driver: str(driver.current_url or "").strip()
                    not in ("", "about:blank")
                )
            except TimeoutException:
                pass

            await worker_sleep(1)

            url_pdf = str(self.driver.current_url or "").strip()

            console.print("[SAP][PDF] " f"URL do boleto capturada: {url_pdf}")

            if not url_pdf:
                raise RuntimeError("URL do boleto vazia.")

            if "/sap/opu/odata/" not in url_pdf:
                console.print(
                    "[SAP][PDF][AVISO] "
                    "A URL aberta não possui /sap/opu/odata/. "
                    "O download direto será tentado mesmo assim."
                )

            # ================================================
            # 7 - REAPROVEITA A SESSÃO AUTENTICADA
            # ================================================

            sessao = requests.Session()

            for cookie in cookies_sap:
                nome = cookie.get("name")
                valor = cookie.get("value")

                if not nome:
                    continue

                kwargs_cookie = {
                    "name": nome,
                    "value": valor,
                    "path": cookie.get("path", "/"),
                }

                dominio = cookie.get("domain")

                if dominio:
                    kwargs_cookie["domain"] = dominio

                try:
                    sessao.cookies.set(**kwargs_cookie)
                except Exception:
                    sessao.cookies.set(
                        nome,
                        valor,
                    )

            headers = {
                "User-Agent": user_agent,
                "Accept": ("application/pdf," "application/octet-stream,*/*"),
                "Referer": self.URL_GERENCIADOR_FATURAS,
            }

            # ================================================
            # 8 - DOWNLOAD DO PDF COM REQUESTS
            # ================================================

            console.print("[SAP][PDF] " "Baixando conteúdo diretamente com requests...")

            try:
                resposta = sessao.get(
                    url_pdf,
                    headers=headers,
                    timeout=120,
                    allow_redirects=True,
                    verify=False,
                )
            except Exception as e:
                raise RuntimeError(
                    "Falha no download direto do boleto. " f"{type(e).__name__}: {e}"
                ) from e

            content_type = str(
                resposta.headers.get(
                    "Content-Type",
                    "",
                )
            ).lower()

            console.print("[SAP][PDF] " f"HTTP: {resposta.status_code}")

            console.print("[SAP][PDF] " f"Content-Type: {content_type}")

            if resposta.status_code != 200:
                try:
                    texto_erro = resposta.text[:500]
                except Exception:
                    texto_erro = ""

                raise RuntimeError(
                    "SAP retornou erro no download do boleto. "
                    f"HTTP {resposta.status_code}. "
                    f"Resposta: {texto_erro}"
                )

            conteudo = resposta.content

            if not conteudo:
                raise RuntimeError("SAP retornou conteúdo vazio para o boleto.")

            if not (conteudo.startswith(b"%PDF") or "application/pdf" in content_type):
                inicio_resposta = conteudo[:500].decode(
                    "utf-8",
                    errors="replace",
                )

                raise RuntimeError(
                    "Resposta do SAP não é um PDF válido. "
                    f"Content-Type: {content_type}. "
                    f"Início da resposta: {inicio_resposta}"
                )

            # ================================================
            # 9 - SALVA O PDF
            # ================================================

            nome_pdf = f"boleto_{self.codigo_cliente}_" f"{self.nova_referencia}.pdf"

            caminho_pdf = os.path.join(
                self.pasta_download,
                nome_pdf,
            )

            with open(
                caminho_pdf,
                "wb",
            ) as arquivo:
                arquivo.write(conteudo)

            if not os.path.isfile(caminho_pdf):
                raise RuntimeError("PDF não foi criado no disco.")

            tamanho = os.path.getsize(caminho_pdf)

            if tamanho <= 0:
                raise RuntimeError("PDF salvo com tamanho zero.")

            console.print("[SAP][PDF] " "Boleto salvo com sucesso.")

            console.print("[SAP][PDF] " f"Arquivo: {caminho_pdf}")

            console.print("[SAP][PDF] " f"Tamanho: {tamanho} bytes")

            # ================================================
            # 10 - ENVIA PARA O BACKOFFICE
            # ================================================

            nome_enviado = await self.enviar_pdf_backoffice(caminho_pdf)

            return nome_enviado

        finally:
            # Fecha somente a aba do boleto, se ainda estiver aberta.
            try:
                if handle_pdf in self.driver.window_handles:
                    self.driver.switch_to.window(handle_pdf)
                    self.driver.close()
            except Exception:
                pass

            # Sempre retorna para a aba do Gerenciador do SAP.
            try:
                if handle_sap in self.driver.window_handles:
                    self.driver.switch_to.window(handle_sap)
            except Exception:
                pass

    async def steps_sap(
        self,
    ) -> str:

        console.print("[SAP][FLUXO] Iniciando...")

        # 1
        await self.preencher_cliente()

        # 2
        await self.selecionar_status_partidas_em_aberto()

        # 3
        await self.clicar_botao_iniciar()

        # 4
        if self.dados_nao_disponiveis():
            return "Dados não disponíveis."

        # 5
        await self.localizar_chave_e_referencia()

        # 6
        await self.acessar_gerenciador_faturas()

        # 7
        await self.preencher_referencia_gerenciador_faturas()

        # 8
        await self.clicar_iniciar_gerenciador_faturas()

        # 9
        await self.selecionar_linha_referencia_gerenciador()

        # 10+
        await self.clicar_baixa_gerenciador_faturas()

        return (
            "Fluxo realizado com sucesso até PDF. "
            f"Cliente: {self.codigo_cliente}. "
            f"Valor: {self.valor}. "
            f"Chave original: {self.chave}. "
            f"Referência original: {self.referencia}. "
            f"Nova Chave ref.3: {self.nova_chave_ref3}. "
            f"Nova Referência: {self.nova_referencia}."
        )

    # ========================================================
    # INICIAR
    # ========================================================

    async def iniciar(
        self,
    ) -> RpaRetornoProcessoDTO:

        etapa = "INIT"

        try:
            etapa = "VALIDAR_CONFIG"

            self.validar_config()

            etapa = "LIMPAR_DOWNLOAD"

            self.limpar_pasta_download()

            etapa = "ABRIR_EDGE"

            self.abrir_edge()

            etapa = "ACESSAR_SAP"

            self.driver.get(self.base_url)

            await worker_sleep(3)

            etapa = "LOGIN"

            if not await self.login():
                raise RuntimeError("Login SAP não concluído.")

            etapa = "CUSTOMER_LINE_ITEMS"

            await self.acessar_customer_line_items()

            etapa = "STEPS_SAP"

            mensagem = await self.steps_sap()

            return self.retorno_sucesso(mensagem)

        except FalhaNegocio as e:
            return self.retorno_falha_negocio(str(e))

        except Exception as e:
            mensagem = (
                "Falha durante o processamento no SAP. "
                f"Etapa: {etapa}. "
                f"Erro: "
                f"{type(e).__name__}: {e}\n"
                f"{traceback.format_exc()}"
            )

            return self.retorno_erro(mensagem)

        finally:
            self.fechar_driver()


# ============================================================
# WORKER
# ============================================================


async def prorrogacao_boletos(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:

    processo = ProrrogacaoBoletos(
        task=task,
        base_url=(ProrrogacaoBoletos.URL_CUSTOMER_LINE_ITEMS),
    )

    return await processo.iniciar()
