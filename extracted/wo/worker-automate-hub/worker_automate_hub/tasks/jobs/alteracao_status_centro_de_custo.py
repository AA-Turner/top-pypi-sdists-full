# -*- coding: utf-8 -*-

import asyncio
import json
import os
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console

from selenium import webdriver
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# AJUSTE DO PYTHON PATH
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
# IMPORTAÇÕES DO WORKER
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
from worker_automate_hub.utils.credentials_manager import CredentialsManager
from worker_automate_hub.utils.util import worker_sleep

console = Console()


# ============================================================
# EXCEÇÕES
# ============================================================


class FalhaNegocioSAP(Exception):
    """Erro funcional ocorrido durante o processamento no SAP."""

    pass


# ============================================================
# PROCESSO PRINCIPAL
# ============================================================


class AlteracaoStatus:
    """
    Fluxo:

    1. Abre o SAP.
    2. Realiza o login.
    3. Abre Administrar Centros de Custo.
    4. Pesquisa o centro recebido na configEntrada.
    5. Abre o registro encontrado.
    6. Clica em Editar.
    7. Verifica os dois switches.
    8. Altera somente os switches diferentes do solicitado.
    9. Grava somente quando houver alteração.
    """

    # ========================================================
    # CONFIGURAÇÕES
    # ========================================================

    HASH_ALTERACAO_STATUS = "Shell-home"

    CLIENT_SAP = "800"

    TIMEOUT_CURTO = 10
    TIMEOUT_PADRAO = 30
    TIMEOUT_LONGO = 80

    # ========================================================
    # LOGIN SAP
    # ========================================================

    X_CLIENT = "//input[@id='CLIENT_FIELD-inner']"

    X_LOGIN_INPUTS = "//input[contains(@class,'loginInputField')]"

    X_LOGIN_BUTTON = (
        "//*[contains(@class,'LOGIN_SUBMIT_BLOCK') "
        "or @id='LOGIN_LINK' "
        "or @id='LOGIN_SUBMIT_BLOCK']"
    )

    # ========================================================
    # SAP FIORI
    # ========================================================

    X_FECHAR_POPUP = "//button[@title='Fechar' or @aria-label='Fechar']"

    X_ADMINISTRAR_CENTRO_CUSTO = "//a[contains(@href, '#CostCenter-manage')]"

    # ========================================================
    # TELA DE PESQUISA
    # ========================================================

    X_CAMPO_CENTRO_CUSTO = (
        "//input[@id='fin.co.costcenter.manage.v2::"
        "sap.suite.ui.generic.template.ListReport.view.ListReport::"
        "C_CostCenter--listReportFilter-"
        "filterItemControl_BASIC-CostCenterForEdit-inner']"
    )

    X_BOTAO_INICIAR = (
        "//span[contains(@id, 'listReportFilter-btnGo-content') "
        "and contains(normalize-space(.), 'Iniciar')]"
    )

    # ========================================================
    # TELA DE DETALHES
    # ========================================================

    X_BOTAO_EDITAR = (
        "//button[@id='fin.co.costcenter.manage.v2::"
        "sap.suite.ui.generic.template.ObjectPage.view.Details::"
        "C_CostCenter--edit']"
    )

    X_SWITCH_CUSTOS_PRIMARIOS = (
        "//*[@id='fin.co.costcenter.manage.v2::"
        "sap.suite.ui.generic.template.ObjectPage.view.Details::"
        "C_CostCenter--IsBForPrimaryCostsPostingSwitchId-handle']"
    )

    X_SWITCH_CUSTOS_SECUNDARIOS = (
        "//*[@id='fin.co.costcenter.manage.v2::"
        "sap.suite.ui.generic.template.ObjectPage.view.Details::"
        "C_CostCenter--IsBForSecondaryCostsPostingSwitchId-handle']"
    )

    X_BOTAO_GRAVAR = (
        "//button[@id='fin.co.costcenter.manage.v2::"
        "sap.suite.ui.generic.template.ObjectPage.view.Details::"
        "C_CostCenter--activate']"
    )

    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: str,
    ):
        self.task = task

        self.config_entrada = self.normalizar_config_entrada(
            getattr(task, "configEntrada", {}) or {}
        )

        self.base_url = (
            base_url.split("#", 1)[0].strip() + "#" + self.HASH_ALTERACAO_STATUS
        )

        self.user = CredentialsManager().get_by_key("SAP_USER_DRC")

        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_DRC")

        self.centro = str(self.get_config_value("centro", "")).strip()

        self.status = str(self.get_config_value("status", "")).strip().upper()

        self.driver: Optional[webdriver.Chrome] = None

        self.alteracoes_realizadas: List[str] = []
        self.status_ja_corretos: List[str] = []

        console.print("[INIT] AlteracaoStatus inicializado.")
        console.print(f"[INIT] URL SAP: {self.base_url}")
        console.print(f"[INIT] Centro: {self.centro}")
        console.print(f"[INIT] Status solicitado: {self.status}")

        console.print("[INIT] Usuário carregado? " f"{'SIM' if self.user else 'NÃO'}")

    # ========================================================
    # CONFIGURAÇÃO DE ENTRADA
    # ========================================================

    def normalizar_config_entrada(
        self,
        config: Any,
    ) -> Dict[str, Any]:
        if config is None:
            return {}

        if isinstance(config, dict):
            return config

        if isinstance(config, str):
            texto = config.strip()

            if not texto:
                return {}

            try:
                resultado = json.loads(texto)

                if not isinstance(resultado, dict):
                    raise RuntimeError("configEntrada deve representar um objeto JSON.")

                return resultado

            except json.JSONDecodeError as e:
                raise RuntimeError(
                    "configEntrada veio como string, " f"mas não é um JSON válido: {e}"
                ) from e

        try:
            return vars(config)

        except Exception:
            return {}

    def get_config_value(
        self,
        chave: str,
        default: Any = None,
    ) -> Any:
        if isinstance(self.config_entrada, dict):
            return self.config_entrada.get(
                chave,
                default,
            )

        return getattr(
            self.config_entrada,
            chave,
            default,
        )

    # ========================================================
    # RETORNOS PADRONIZADOS
    # ========================================================

    def retorno_sucesso(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:
        console.print(f"[SUCESSO] {mensagem}")

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    def retorno_erro(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:
        console.print(f"[ERRO_TECNICO] {mensagem}")

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    def retorno_falha_negocio(
        self,
        mensagem: str,
    ) -> RpaRetornoProcessoDTO:
        console.print(f"[FALHA_NEGOCIO] {mensagem}")

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Falha,
        )

    # ========================================================
    # VALIDAÇÕES
    # ========================================================

    def validar_config(self) -> None:
        if not self.user:
            raise RuntimeError("Credencial SAP_USER_DRC não encontrada.")

        if not self.password:
            raise RuntimeError("Credencial SAP_PASSWORD_DRC não encontrada.")

        if not self.base_url:
            raise RuntimeError("base_url do SAP não configurada.")

        if not self.centro:
            raise RuntimeError("configEntrada.centro não informado.")

        if not self.status:
            raise RuntimeError("configEntrada.status não informado.")

        if self.status not in {"ON", "OFF"}:
            raise RuntimeError(
                f"Status inválido: {self.status}. "
                "Os valores permitidos são ON ou OFF."
            )

    # ========================================================
    # FLUXO PRINCIPAL
    # ========================================================

    async def iniciar(
        self,
    ) -> RpaRetornoProcessoDTO:
        step = "INIT"

        try:
            step = "VALIDAR_CONFIG"
            self.validar_config()

            step = "ABRIR_CHROME"
            self.abrir_chrome()

            step = "ACESSAR_SAP"

            console.print(f"[{step}] Acessando SAP...")

            if not self.driver:
                raise RuntimeError("ChromeDriver não inicializado.")

            self.driver.get(self.base_url)

            await worker_sleep(3)

            step = "LOGIN"

            login_ok = await self.login()

            if not login_ok:
                raise RuntimeError("Não foi possível concluir o login no SAP.")

            step = "PROCESSAR_CENTRO_CUSTO"

            mensagem_final = await self.steps_sap()

            return self.retorno_sucesso(mensagem_final)

        except FalhaNegocioSAP as e:
            return self.retorno_falha_negocio(str(e))

        except Exception as e:
            tb = traceback.format_exc()

            mensagem = (
                "Falha durante o processamento do centro de custo no SAP. "
                f"Etapa: {step}. "
                f"Erro: {type(e).__name__}: {e}\n"
                f"{tb}"
            )

            return self.retorno_erro(mensagem)

        finally:
            self.fechar_driver()

    # ========================================================
    # CHROME
    # ========================================================

    def abrir_chrome(self) -> None:
        console.print("[CHROME] Inicializando ChromeDriver...")

        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()

        options.add_argument("--lang=pt-BR")
        options.add_argument("--log-level=3")

        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")

        options.add_experimental_option(
            "excludeSwitches",
            [
                "enable-automation",
                "enable-logging",
            ],
        )

        options.add_experimental_option(
            "useAutomationExtension",
            False,
        )

        self.driver = webdriver.Chrome(
            service=service,
            options=options,
        )

        self.driver.set_page_load_timeout(self.TIMEOUT_LONGO)

        try:
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": """
                        Object.defineProperty(
                            navigator,
                            'webdriver',
                            {
                                get: () => undefined
                            }
                        );
                    """},
            )

        except Exception:
            pass

        self.driver.maximize_window()

    def fechar_driver(self) -> None:
        if not self.driver:
            return

        try:
            console.print("[CHROME] Encerrando navegador...")

            self.driver.quit()

        except Exception as e:
            console.print(
                "[CHROME][AVISO] Não foi possível " f"encerrar o navegador: {e}"
            )

        finally:
            self.driver = None

    # ========================================================
    # FUNÇÕES SELENIUM
    # ========================================================

    def aguardar_elemento(
        self,
        xpath: str,
        timeout: Optional[int] = None,
        clicavel: bool = False,
    ) -> WebElement:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

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

    def clicar_elemento(
        self,
        xpath: str,
        timeout: Optional[int] = None,
    ) -> None:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        elemento = self.aguardar_elemento(
            xpath=xpath,
            timeout=timeout,
            clicavel=True,
        )

        try:
            elemento.click()

        except Exception:
            elemento = WebDriverWait(
                self.driver,
                timeout or self.TIMEOUT_PADRAO,
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        xpath,
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                elemento,
            )

    # ========================================================
    # LOGIN
    # ========================================================

    async def alterar_client_para_800(
        self,
    ) -> None:
        try:
            campo_client = self.aguardar_elemento(
                xpath=self.X_CLIENT,
                timeout=self.TIMEOUT_CURTO,
            )

            valor_atual = str(campo_client.get_attribute("value") or "").strip()

            console.print("[LOGIN] Client atual: " f"{valor_atual or 'não informado'}")

            if valor_atual != self.CLIENT_SAP:
                campo_client.clear()
                campo_client.send_keys(self.CLIENT_SAP)

                console.print("[LOGIN] Client alterado para " f"{self.CLIENT_SAP}.")

        except TimeoutException:
            console.print(
                "[LOGIN] Campo de client não apareceu. "
                "O client já pode estar definido pela URL."
            )

    async def aguardar_inputs_login(
        self,
    ) -> List[WebElement]:
        if not self.driver:
            return []

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

            return self.driver.find_elements(
                By.XPATH,
                self.X_LOGIN_INPUTS,
            )

        except TimeoutException:
            return []

    async def aguardar_botao_login(
        self,
    ) -> Optional[WebElement]:
        try:
            return self.aguardar_elemento(
                xpath=self.X_LOGIN_BUTTON,
                timeout=self.TIMEOUT_PADRAO,
                clicavel=True,
            )

        except TimeoutException:
            return None

    async def login(self) -> bool:
        try:
            console.print("[LOGIN] Iniciando login...")

            await self.alterar_client_para_800()

            inputs = await self.aguardar_inputs_login()

            if len(inputs) < 2:
                console.print(
                    "[LOGIN][ERRO] Campos de usuário " "e senha não encontrados."
                )

                return False

            campo_usuario = inputs[0]
            campo_senha = inputs[1]

            campo_usuario.clear()
            campo_usuario.send_keys(self.user)

            console.print("[LOGIN] Usuário preenchido.")

            await worker_sleep(0.5)

            campo_senha.clear()
            campo_senha.send_keys(self.password)

            console.print("[LOGIN] Senha preenchida.")

            await worker_sleep(0.5)

            botao_login = await self.aguardar_botao_login()

            if not botao_login:
                console.print("[LOGIN][ERRO] Botão de login " "não encontrado.")

                return False

            try:
                botao_login.click()

            except Exception:
                if not self.driver:
                    return False

                self.driver.execute_script(
                    "arguments[0].click();",
                    botao_login,
                )

            console.print("[LOGIN] Botão de login clicado.")

            await worker_sleep(5)

            if await self.login_apresentou_erro():
                return False

            console.print("[LOGIN] Login concluído.")

            return True

        except Exception:
            console.print("[LOGIN][ERRO] Erro durante login.")

            console.print(traceback.format_exc())

            return False

    async def login_apresentou_erro(
        self,
    ) -> bool:
        if not self.driver:
            return True

        xpaths_erro = [
            (
                "//*[contains("
                "translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'usuário ou senha')]"
            ),
            (
                "//*[contains("
                "translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'logon failed')]"
            ),
            (
                "//*[contains("
                "translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'dados de logon')]"
            ),
            (
                "//*[contains(@class,'error') "
                "and string-length(normalize-space(.)) > 0]"
            ),
        ]

        for xpath in xpaths_erro:
            elementos = self.buscar_elementos(xpath)

            for elemento in elementos:
                try:
                    if not elemento.is_displayed():
                        continue

                    mensagem = elemento.text.strip()

                    if mensagem:
                        console.print(f"[LOGIN][ERRO_SAP] {mensagem}")

                        return True

                except StaleElementReferenceException:
                    continue

        return False

    # ========================================================
    # ABRIR ADMINISTRAR CENTROS DE CUSTO
    # ========================================================

    async def clicar_administrar_centro_custo(
        self,
    ) -> None:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        console.print(
            "[SAP] Aguardando o aplicativo " "Administrar Centros de Custo..."
        )

        link_centro_custo = self.aguardar_elemento(
            xpath=self.X_ADMINISTRAR_CENTRO_CUSTO,
            timeout=self.TIMEOUT_LONGO,
            clicavel=True,
        )

        try:
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                link_centro_custo,
            )

            await worker_sleep(1)

            link_centro_custo.click()

        except Exception:
            console.print(
                "[SAP] Clique normal falhou. " "Tentando clique via JavaScript..."
            )

            link_centro_custo = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.X_ADMINISTRAR_CENTRO_CUSTO,
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                link_centro_custo,
            )

        console.print("[SAP] Aplicativo Administrar Centros de Custo clicado.")

        WebDriverWait(
            self.driver,
            self.TIMEOUT_LONGO,
        ).until(lambda driver: ("#CostCenter-manage" in driver.current_url))

        console.print("[SAP] Aplicativo carregado com sucesso.")

        await worker_sleep(3)

    # ========================================================
    # PREENCHER CENTRO E INICIAR
    # ========================================================

    async def preencher_centro_custo_e_iniciar(
        self,
    ) -> None:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        console.print("[SAP] Aguardando o campo Centro de Custo...")

        campo_centro = self.aguardar_elemento(
            xpath=self.X_CAMPO_CENTRO_CUSTO,
            timeout=self.TIMEOUT_LONGO,
            clicavel=True,
        )

        console.print(f"[SAP] Preenchendo Centro de Custo: {self.centro}")

        campo_centro.click()
        campo_centro.send_keys(
            Keys.CONTROL,
            "a",
        )
        campo_centro.send_keys(Keys.DELETE)
        campo_centro.send_keys(self.centro)

        await worker_sleep(1)

        campo_centro = self.aguardar_elemento(
            xpath=self.X_CAMPO_CENTRO_CUSTO,
            timeout=self.TIMEOUT_PADRAO,
            clicavel=True,
        )

        valor_preenchido = str(campo_centro.get_attribute("value") or "").strip()

        if valor_preenchido != self.centro:
            raise RuntimeError(
                "O Centro de Custo não foi preenchido corretamente. "
                f"Esperado: {self.centro}. "
                f"Encontrado: {valor_preenchido or 'vazio'}."
            )

        console.print(
            "[SAP] Centro de Custo preenchido corretamente: " f"{valor_preenchido}"
        )

        self.clicar_elemento(
            xpath=self.X_BOTAO_INICIAR,
            timeout=self.TIMEOUT_LONGO,
        )

        console.print("[SAP] Botão Iniciar clicado com sucesso.")

        await worker_sleep(5)

    # ========================================================
    # AGUARDAR TELA DE DETALHES
    # ========================================================

    async def aguardar_tela_detalhes(
        self,
        timeout: int = 15,
    ) -> bool:
        """
        Considera que a tela de detalhes foi aberta quando:

        1. A URL contém /C_CostCenter(; ou
        2. O botão Editar aparece no DOM.
        """

        if not self.driver:
            return False

        try:
            WebDriverWait(
                self.driver,
                timeout,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                lambda driver: (
                    "/C_CostCenter(" in driver.current_url
                    or len(
                        driver.find_elements(
                            By.XPATH,
                            self.X_BOTAO_EDITAR,
                        )
                    )
                    > 0
                )
            )

            console.print("[SAP] Navegação para os detalhes confirmada.")

            console.print(f"[SAP] URL atual: {self.driver.current_url}")

            return True

        except TimeoutException:
            return False

    # ========================================================
    # CLICAR NO RESULTADO DO CENTRO
    # ========================================================

    async def clicar_resultado_centro_custo(self) -> None:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        console.print(
            f"[SAP] Aguardando a linha do Centro de Custo " f"{self.centro}..."
        )

        xpath_linha = (
            "//tbody[contains(@id, 'responsiveTable-tblBody')]"
            "//tr[contains(@class, 'sapMListTblRow') "
            f"and .//*[normalize-space()='{self.centro}']]"
        )

        try:
            linha = WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        xpath_linha,
                    )
                )
            )

        except TimeoutException as e:
            raise FalhaNegocioSAP(
                f"O Centro de Custo {self.centro} não foi encontrado "
                "na tabela de resultados do SAP."
            ) from e

        console.print(f"[SAP] Linha do Centro de Custo " f"{self.centro} encontrada.")

        xpaths_navegacao = [
            (f"{xpath_linha}" "//td[contains(@class, 'sapMListTblNavigatedCell')]"),
            (
                f"{xpath_linha}"
                "//td[contains(@class, 'sapMListTblNavCol') "
                "and not(@aria-hidden='true')]"
            ),
            (f"{xpath_linha}" "/td[last()]"),
            (
                f"{xpath_linha}"
                "//*[contains(@class, 'sapUiIcon') "
                "and contains(@class, 'sapMListTblNavIcon')]"
            ),
        ]

        url_antes = self.driver.current_url
        abriu_detalhes = False

        for numero_tentativa, xpath_navegacao in enumerate(
            xpaths_navegacao,
            start=1,
        ):
            try:
                console.print(
                    f"[SAP] Tentativa {numero_tentativa}: "
                    "localizando a célula de navegação..."
                )

                elementos = self.driver.find_elements(
                    By.XPATH,
                    xpath_navegacao,
                )

                elementos_visiveis = [
                    elemento for elemento in elementos if elemento.is_displayed()
                ]

                if not elementos_visiveis:
                    console.print(
                        f"[SAP] Tentativa {numero_tentativa}: "
                        "nenhum elemento visível encontrado."
                    )
                    continue

                alvo = elementos_visiveis[-1]

                diagnostico = self.driver.execute_script(
                    """
                    const elemento = arguments[0];

                    return {
                        tag: elemento.tagName,
                        id: elemento.id || '',
                        classe: elemento.className || '',
                        texto: (
                            elemento.innerText
                            || elemento.textContent
                            || ''
                        ).trim(),
                        largura: elemento.getBoundingClientRect().width,
                        altura: elemento.getBoundingClientRect().height
                    };
                    """,
                    alvo,
                )

                console.print(
                    f"[SAP] Elemento de navegação encontrado: " f"{diagnostico}"
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    alvo,
                )

                await worker_sleep(0.5)

                try:
                    ActionChains(self.driver).move_to_element(alvo).pause(
                        0.5
                    ).click().perform()

                    console.print(
                        "[SAP] Clique físico realizado " "na célula de navegação."
                    )

                except Exception as e:
                    console.print(
                        "[SAP] Clique físico falhou. "
                        f"Tentando clique por coordenadas: {e}"
                    )

                    self.driver.execute_script(
                        """
                        const elemento = arguments[0];
                        const rect = elemento.getBoundingClientRect();

                        const x = rect.left + Math.max(
                            rect.width - 10,
                            rect.width / 2
                        );

                        const y = rect.top + (rect.height / 2);

                        const alvoReal = document.elementFromPoint(x, y)
                            || elemento;

                        const opcoes = {
                            bubbles: true,
                            cancelable: true,
                            view: window,
                            clientX: x,
                            clientY: y,
                            button: 0
                        };

                        alvoReal.dispatchEvent(
                            new MouseEvent('mousedown', opcoes)
                        );

                        alvoReal.dispatchEvent(
                            new MouseEvent('mouseup', opcoes)
                        );

                        alvoReal.dispatchEvent(
                            new MouseEvent('click', opcoes)
                        );
                        """,
                        alvo,
                    )

                abriu_detalhes = await self.aguardar_tela_detalhes(timeout=15)

                if abriu_detalhes:
                    console.print(
                        "[SAP] Tela de detalhes aberta pela " "célula de navegação."
                    )
                    break

            except Exception as e:
                console.print(
                    f"[SAP] Tentativa {numero_tentativa} falhou: "
                    f"{type(e).__name__}: {e}"
                )

        if not abriu_detalhes:
            console.print("[SAP] Tentando clicar no extremo direito da linha...")

            linha = WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        xpath_linha,
                    )
                )
            )

            self.driver.execute_script(
                """
                const linha = arguments[0];
                const rect = linha.getBoundingClientRect();

                const x = rect.right - 10;
                const y = rect.top + (rect.height / 2);

                const alvo = document.elementFromPoint(x, y) || linha;

                const opcoes = {
                    bubbles: true,
                    cancelable: true,
                    view: window,
                    clientX: x,
                    clientY: y,
                    button: 0
                };

                alvo.dispatchEvent(
                    new MouseEvent('mouseover', opcoes)
                );

                alvo.dispatchEvent(
                    new MouseEvent('mousedown', opcoes)
                );

                alvo.dispatchEvent(
                    new MouseEvent('mouseup', opcoes)
                );

                alvo.dispatchEvent(
                    new MouseEvent('click', opcoes)
                );
                """,
                linha,
            )

            abriu_detalhes = await self.aguardar_tela_detalhes(timeout=20)

        if not abriu_detalhes:
            url_atual = self.driver.current_url

            console.print(f"[SAP][DIAGNÓSTICO] URL antes: {url_antes}")

            console.print(f"[SAP][DIAGNÓSTICO] URL atual: {url_atual}")

            if "/C_CostCenter(" in url_atual:
                console.print("[SAP] A URL confirma que os detalhes foram abertos.")

                abriu_detalhes = True

            else:
                raise RuntimeError(
                    f"O Centro de Custo {self.centro} foi encontrado, "
                    "mas a tela de detalhes não foi aberta."
                )

        console.print(f"[SAP] Centro de Custo {self.centro} " "aberto com sucesso.")

    # ========================================================
    # SWITCHES
    # ========================================================

    def obter_elemento_switch(
        self,
        xpath: str,
    ) -> WebElement:
        """
        Retorna exatamente o elemento localizado pelo XPath.

        Nos dois switches estamos utilizando o elemento *-handle,
        que possui o atributo data-sap-ui-swt="On" ou "Off".
        """
        return self.aguardar_elemento(
            xpath=xpath,
            timeout=self.TIMEOUT_LONGO,
            clicavel=False,
        )

    def obter_status_switch(
        self,
        xpath: str,
    ) -> str:
        """
        Obtém o estado real do switch SAPUI5.

        Prioridade:
        1. Controle pai sapMSwt.
        2. aria-checked / classes sapMSwtOn / sapMSwtOff.
        3. Atributos do próprio handle.
        4. data-sap-ui-swt somente como fallback.
        """

        elemento = self.obter_elemento_switch(xpath)

        # ====================================================
        # 1. CONTROLE PAI DO SWITCH
        # ====================================================
        try:
            controle_switch = elemento.find_element(
                By.XPATH,
                (
                    "./ancestor::*["
                    "contains(concat(' ', normalize-space(@class), ' '), "
                    "' sapMSwt ')"
                    "][1]"
                ),
            )

            aria_checked = (
                str(controle_switch.get_attribute("aria-checked") or "").strip().lower()
            )

            if aria_checked == "true":
                return "ON"

            if aria_checked == "false":
                return "OFF"

            classes = str(controle_switch.get_attribute("class") or "").lower()

            if "sapmswton" in classes:
                return "ON"

            if "sapmswtoff" in classes:
                return "OFF"

            aria_label = (
                str(controle_switch.get_attribute("aria-label") or "").strip().lower()
            )

            title = str(controle_switch.get_attribute("title") or "").strip().lower()

            texto_estado = f"{aria_label} {title}".strip()

            if texto_estado == "on" or " ligado" in f" {texto_estado}":
                return "ON"

            if texto_estado == "off" or " desligado" in f" {texto_estado}":
                return "OFF"

        except Exception:
            pass

        # ====================================================
        # 2. PRÓPRIO HANDLE
        # ====================================================
        aria_checked_handle = (
            str(elemento.get_attribute("aria-checked") or "").strip().lower()
        )

        if aria_checked_handle == "true":
            return "ON"

        if aria_checked_handle == "false":
            return "OFF"

        classes_handle = str(elemento.get_attribute("class") or "").lower()

        if "sapmswton" in classes_handle:
            return "ON"

        if "sapmswtoff" in classes_handle:
            return "OFF"

        # ====================================================
        # 3. data-sap-ui-swt SOMENTE COMO FALLBACK
        # ====================================================
        data_swt = str(elemento.get_attribute("data-sap-ui-swt") or "").strip().upper()

        if data_swt == "ON":
            return "ON"

        if data_swt == "OFF":
            return "OFF"

        # ====================================================
        # 4. ÚLTIMO FALLBACK PELO HTML
        # ====================================================
        html = str(elemento.get_attribute("outerHTML") or "").lower()

        if 'data-sap-ui-swt="on"' in html:
            return "ON"

        if 'data-sap-ui-swt="off"' in html:
            return "OFF"

        raise RuntimeError(
            "Não foi possível identificar o status atual " f"do switch. XPath: {xpath}"
        )

    async def clicar_switch(
        self,
        xpath: str,
    ) -> None:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        handle = self.obter_elemento_switch(xpath)

        id_handle = str(handle.get_attribute("id") or "").strip()

        estado_antes = str(handle.get_attribute("data-sap-ui-swt") or "").strip()

        console.print(f"[SAP][SWITCH] Handle encontrado: {id_handle}")

        console.print(
            "[SAP][SWITCH] data-sap-ui-swt antes do clique: "
            f"{estado_antes or 'não informado'}"
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            handle,
        )

        await worker_sleep(0.5)

        # ====================================================
        # TENTATIVA 1 - CLIQUE DIRETO NO HANDLE
        # ====================================================
        try:
            handle.click()

            console.print("[SAP][SWITCH] Clique direto no handle executado.")

            await worker_sleep(1)
            return

        except Exception as e:
            console.print(
                "[SAP][SWITCH] Clique direto no handle falhou: "
                f"{type(e).__name__}: {e}"
            )

        # ====================================================
        # TENTATIVA 2 - ACTION CHAINS
        # ====================================================
        try:
            handle = self.obter_elemento_switch(xpath)

            ActionChains(self.driver).move_to_element(handle).pause(
                0.3
            ).click().perform()

            console.print("[SAP][SWITCH] Clique via ActionChains executado.")

            await worker_sleep(1)
            return

        except Exception as e:
            console.print(
                "[SAP][SWITCH] ActionChains falhou: " f"{type(e).__name__}: {e}"
            )

        # ====================================================
        # TENTATIVA 3 - CLICAR NO CONTROLE PAI DO HANDLE
        # ====================================================
        try:
            handle = self.obter_elemento_switch(xpath)

            controle_switch = handle.find_element(
                By.XPATH,
                (
                    "./ancestor::*["
                    "contains(concat(' ', normalize-space(@class), ' '), "
                    "' sapMSwt ')"
                    "][1]"
                ),
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                controle_switch,
            )

            try:
                controle_switch.click()

            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    controle_switch,
                )

            console.print("[SAP][SWITCH] Clique no controle pai do switch executado.")

            await worker_sleep(1)
            return

        except Exception as e:
            console.print(
                "[SAP][SWITCH] Clique no controle pai falhou: "
                f"{type(e).__name__}: {e}"
            )

        # ====================================================
        # TENTATIVA 4 - JAVASCRIPT NO HANDLE
        # ====================================================
        try:
            handle = self.obter_elemento_switch(xpath)

            self.driver.execute_script(
                """
                const el = arguments[0];

                const rect = el.getBoundingClientRect();

                const x = rect.left + (rect.width / 2);
                const y = rect.top + (rect.height / 2);

                const target = document.elementFromPoint(x, y) || el;

                const opts = {
                    bubbles: true,
                    cancelable: true,
                    view: window,
                    clientX: x,
                    clientY: y,
                    button: 0
                };

                target.dispatchEvent(
                    new MouseEvent('mousedown', opts)
                );

                target.dispatchEvent(
                    new MouseEvent('mouseup', opts)
                );

                target.dispatchEvent(
                    new MouseEvent('click', opts)
                );
                """,
                handle,
            )

            console.print("[SAP][SWITCH] Clique JavaScript no handle executado.")

            await worker_sleep(1)
            return

        except Exception as e:
            raise RuntimeError(
                "Não foi possível clicar no switch. " f"{type(e).__name__}: {e}"
            ) from e

    async def ajustar_switch(
        self,
        nome: str,
        xpath: str,
    ) -> Tuple[bool, str]:
        status_atual = self.obter_status_switch(xpath)

        console.print(
            f"[SAP][STATUS] {nome}: "
            f"atual={status_atual} | "
            f"solicitado={self.status}"
        )

        if status_atual == self.status:
            mensagem = (
                f"{nome} já estava com status {self.status}. "
                "Nenhuma alteração foi necessária."
            )

            console.print(f"[SAP][SEM_ALTERACAO] {mensagem}")

            self.status_ja_corretos.append(mensagem)

            return False, mensagem

        console.print(
            f"[SAP][ALTERACAO] Alterando {nome} "
            f"de {status_atual} para {self.status}..."
        )

        await self.clicar_switch(xpath)

        console.print(
            f"[SAP][SWITCH] Aguardando o SAP refletir a alteração de {nome}..."
        )

        await worker_sleep(2)

        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_PADRAO,
                poll_frequency=0.5,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(lambda _: (self.obter_status_switch(xpath) == self.status))

        except TimeoutException as e:
            status_encontrado = "não identificado"

            try:
                status_encontrado = self.obter_status_switch(xpath)

            except Exception:
                pass

            raise RuntimeError(
                f"Não foi possível alterar {nome}. "
                f"Status esperado: {self.status}. "
                f"Status encontrado: {status_encontrado}."
            ) from e

        status_final = self.obter_status_switch(xpath)

        mensagem = f"{nome} alterado de {status_atual} " f"para {status_final}."

        console.print(f"[SAP][ALTERADO] {mensagem}")

        self.alteracoes_realizadas.append(mensagem)

        return True, mensagem

    # ========================================================
    # AGUARDAR GRAVAÇÃO DO SAP
    # ========================================================

    async def aguardar_gravacao_sap(self) -> None:
        """
        Aguarda a gravação ser realmente concluída no SAP.

        A validação considera:
        1. O processamento/loading do SAP.
        2. O desaparecimento dos indicadores de carregamento.
        3. O retorno do botão Editar.
        4. A persistência dos dois switches no status solicitado.
        """
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        console.print(
            "[SAP][GRAVACAO] Aguardando o SAP iniciar/concluir "
            "o processamento da gravação..."
        )

        # Validação
        xpath_busy = (
            "//*["
            "@aria-busy='true' "
            "or contains(@class, 'sapUiLocalBusyIndicator') "
            "or contains(@class, 'sapUiBusy') "
            "or contains(@class, 'sapMBusyIndicator')"
            "]"
        )

        def existe_busy_visivel(driver) -> bool:
            try:
                elementos = driver.find_elements(
                    By.XPATH,
                    xpath_busy,
                )

                for elemento in elementos:
                    try:
                        if elemento.is_displayed():
                            return True
                    except Exception:
                        continue

                return False

            except Exception:
                return False

        # Dá uma pequena margem para o SAP disparar as chamadas
        # assíncronas de gravação/atualização da tela.
        await worker_sleep(1)

        busy_detectado = existe_busy_visivel(self.driver)

        # Alguns loadings aparecem alguns instantes depois do clique.
        # Tentamos identificá-los por até 10 segundos.
        if not busy_detectado:
            try:
                WebDriverWait(
                    self.driver,
                    10,
                    poll_frequency=0.25,
                    ignored_exceptions=(StaleElementReferenceException,),
                ).until(existe_busy_visivel)

                busy_detectado = True

            except TimeoutException:
                busy_detectado = False

        if busy_detectado:
            console.print(
                "[SAP][GRAVACAO] Indicador de carregamento detectado. "
                "Aguardando desaparecer..."
            )

            try:
                WebDriverWait(
                    self.driver,
                    self.TIMEOUT_LONGO,
                    poll_frequency=0.5,
                    ignored_exceptions=(StaleElementReferenceException,),
                ).until(lambda driver: not existe_busy_visivel(driver))

            except TimeoutException as e:
                raise RuntimeError(
                    "O SAP permaneceu com indicador de carregamento "
                    "ativo após clicar em Gravar."
                ) from e

            console.print(
                "[SAP][GRAVACAO] Indicadores de carregamento " "desapareceram."
            )

        else:
            console.print(
                "[SAP][GRAVACAO][AVISO] Nenhum indicador de "
                "carregamento foi identificado. "
                "Será realizada a validação pelo estado final da tela."
            )

        # Aguarda um pequeno período sem loading para evitar pegar
        # uma transição intermediária entre requisições do SAP.
        await worker_sleep(2)

        if existe_busy_visivel(self.driver):
            console.print(
                "[SAP][GRAVACAO] Novo carregamento identificado. "
                "Aguardando finalizar..."
            )

            try:
                WebDriverWait(
                    self.driver,
                    self.TIMEOUT_LONGO,
                    poll_frequency=0.5,
                    ignored_exceptions=(StaleElementReferenceException,),
                ).until(lambda driver: not existe_busy_visivel(driver))

            except TimeoutException as e:
                raise RuntimeError(
                    "O SAP iniciou um novo carregamento e não "
                    "concluiu dentro do tempo esperado."
                ) from e

        # ====================================================
        # AGUARDAR O BOTÃO EDITAR
        # ====================================================
        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.5,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_BOTAO_EDITAR,
                    )
                )
            )

            console.print("[SAP][GRAVACAO] Botão Editar disponível novamente.")

        except TimeoutException as e:
            raise RuntimeError(
                "O SAP terminou o carregamento, mas o botão Editar "
                "não ficou disponível dentro do tempo esperado."
            ) from e

        # Mais uma checagem do loading depois que o botão Editar
        # reapareceu, pois no SAP ele pode reaparecer antes de algumas
        # seções da tela terminarem de atualizar.
        try:
            WebDriverWait(
                self.driver,
                self.TIMEOUT_LONGO,
                poll_frequency=0.5,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(lambda driver: not existe_busy_visivel(driver))

        except TimeoutException as e:
            raise RuntimeError(
                "O botão Editar reapareceu, mas o SAP ainda permaneceu "
                "carregando dados da tela."
            ) from e

        # Pequena estabilização final.
        await worker_sleep(10)

        # ====================================================
        # VALIDAR SE OS VALORES FORAM REALMENTE PERSISTIDOS
        # ====================================================
        console.print("[SAP][GRAVACAO] Validando os status após a gravação...")

        status_primario = self.obter_status_switch(self.X_SWITCH_CUSTOS_PRIMARIOS)

        status_secundario = self.obter_status_switch(self.X_SWITCH_CUSTOS_SECUNDARIOS)

        console.print(
            "[SAP][GRAVACAO] Status após gravação: "
            f"primários={status_primario} | "
            f"secundários={status_secundario} | "
            f"esperado={self.status}"
        )

        if status_primario != self.status:
            raise RuntimeError(
                "Após a gravação, o status de planejamento de "
                "custos primários não permaneceu com o valor solicitado. "
                f"Esperado: {self.status}. "
                f"Encontrado: {status_primario}."
            )

        if status_secundario != self.status:
            raise RuntimeError(
                "Após a gravação, o status de planejamento de "
                "custos secundários não permaneceu com o valor solicitado. "
                f"Esperado: {self.status}. "
                f"Encontrado: {status_secundario}."
            )

        console.print(
            "[SAP][GRAVACAO] Gravação confirmada com sucesso. "
            "Os dois status permanecem com o valor solicitado."
        )

    # ========================================================
    # ABRIR, EDITAR, AJUSTAR E GRAVAR
    # ========================================================

    async def abrir_editar_e_ajustar_status(
        self,
    ) -> bool:
        if not self.driver:
            raise RuntimeError("ChromeDriver não inicializado.")

        # ====================================================
        # ABRIR O CENTRO DE CUSTO
        # ====================================================
        await self.clicar_resultado_centro_custo()

        console.print("[SAP] Verificando se o botão Editar está disponível...")

        # ====================================================
        # BOTÃO EDITAR É OPCIONAL
        #
        # Se aparecer:
        #   -> clica e segue.
        #
        # Se NÃO aparecer:
        #   -> NÃO lança erro.
        #   -> apenas registra no log.
        #   -> segue diretamente para os switches.
        #
        # Se aparecer, mas o clique falhar:
        #   -> tenta JavaScript.
        #   -> se ainda falhar, NÃO lança erro.
        #   -> segue para os switches.
        # ====================================================
        try:
            botao_editar = WebDriverWait(
                self.driver,
                10,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_BOTAO_EDITAR,
                    )
                )
            )

            try:
                botao_editar.click()

                console.print("[SAP] Botão Editar encontrado e clicado.")

                await worker_sleep(3)

            except Exception as e_click:
                console.print(
                    "[SAP][AVISO] Botão Editar encontrado, "
                    "mas o clique normal falhou. "
                    "Tentando clique via JavaScript..."
                )

                try:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        botao_editar,
                    )

                    console.print("[SAP] Botão Editar clicado via JavaScript.")

                    await worker_sleep(3)

                except Exception as e_js:
                    console.print(
                        "[SAP][AVISO] Não foi possível clicar no botão Editar. "
                        "A tela pode já estar em modo de edição. "
                        "O erro será ignorado e o processo seguirá "
                        "diretamente para os switches. "
                        f"Erro ignorado: {type(e_js).__name__}: {e_js}"
                    )
                    pass

        except TimeoutException:
            console.print(
                "[SAP] Botão Editar não encontrado. "
                "A tela já pode estar em modo de edição. "
                "Nenhum erro será lançado. "
                "Seguindo diretamente para verificar os switches."
            )
            pass

        except Exception as e:
            console.print(
                "[SAP][AVISO] Ocorreu um problema ao verificar o botão Editar. "
                "Esse erro será ignorado e o processo seguirá "
                "diretamente para os switches. "
                f"Erro ignorado: {type(e).__name__}: {e}"
            )
            pass

        # ====================================================
        # A PARTIR DAQUI SEMPRE SEGUE PARA OS SWITCHES
        # ====================================================
        console.print("[SAP] Iniciando validação dos switches...")

        alterou_primario, _ = await self.ajustar_switch(
            nome="Planejamento de custos primários",
            xpath=self.X_SWITCH_CUSTOS_PRIMARIOS,
        )

        alterou_secundario, _ = await self.ajustar_switch(
            nome="Planejamento de custos secundários",
            xpath=self.X_SWITCH_CUSTOS_SECUNDARIOS,
        )

        houve_alteracao = alterou_primario or alterou_secundario

        # ====================================================
        # GRAVAR
        # ====================================================
        console.print("[SAP] Aguardando o botão Gravar...")

        self.clicar_elemento(
            xpath=self.X_BOTAO_GRAVAR,
            timeout=self.TIMEOUT_LONGO,
        )

        console.print("[SAP] Botão Gravar clicado.")

        # Aguarda o SAP terminar efetivamente a gravação,
        # finalizar os loadings da tela e valida a persistência
        # dos dois switches antes de retornar sucesso.
        await self.aguardar_gravacao_sap()

        console.print("[SAP] Registro gravado no SAP.")

        if not houve_alteracao:
            console.print(
                "[SAP][SEM_ALTERACAO] Os dois controles já estavam "
                f"configurados como {self.status}. "
                "Nenhuma alteração será gravada."
            )

            return False
        else:
            return True

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
                    timeout=2,
                ):
                    return

                self.clicar_elemento(
                    self.X_FECHAR_POPUP,
                    timeout=3,
                )

                console.print("[SAP] Popup inicial fechado.")

                await worker_sleep(1)

            except Exception:
                return

    # ========================================================
    # MENSAGEM FINAL
    # ========================================================

    def montar_mensagem_final(
        self,
        houve_alteracao: bool,
    ) -> str:
        if not houve_alteracao:
            return (
                f"Centro de Custo {self.centro} consultado com sucesso. "
                f"Nenhuma alteração foi realizada porque os status de "
                f"planejamento de custos primários e secundários já "
                f"estavam configurados como {self.status}, conforme "
                "solicitado."
            )

        alteracoes = " ".join(self.alteracoes_realizadas)

        campos_sem_alteracao = ""

        if self.status_ja_corretos:
            campos_sem_alteracao = (
                " Os controles que já estavam com o status solicitado "
                "não foram alterados. " + " ".join(self.status_ja_corretos)
            )

        return (
            f"Centro de Custo {self.centro} processado com sucesso. "
            f"As alterações foram gravadas no SAP. "
            f"{alteracoes}"
            f"{campos_sem_alteracao}"
        )

    # ========================================================
    # FLUXO SAP
    # ========================================================

    async def steps_sap(
        self,
    ) -> str:
        console.print("[SAP] Login realizado.")

        await self.fechar_popups_iniciais()

        await self.clicar_administrar_centro_custo()

        await self.preencher_centro_custo_e_iniciar()

        houve_alteracao = await self.abrir_editar_e_ajustar_status()

        mensagem_final = self.montar_mensagem_final(houve_alteracao)

        console.print(f"[SAP][RESULTADO] {mensagem_final}")

        return mensagem_final


# ============================================================
# PROCESSO PRINCIPAL
# ============================================================


async def alteracao_status_centro_de_custo(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    base_url_sap = (
        "https://vhsrkps4ci.sap.simrede.com.br:44300/"
        "sap/bc/ui2/flp?"
        "sap-client=800&"
        "sap-language=PT"
    )

    processo = AlteracaoStatus(
        task=task,
        base_url=base_url_sap,
    )

    return await processo.iniciar()
