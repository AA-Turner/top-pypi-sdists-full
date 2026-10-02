import asyncio
import os
import sys
import re
import json
import traceback
import unicodedata
from datetime import datetime
from typing import Optional, List

from rich.console import Console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from worker_automate_hub.utils.credentials_manager import CredentialsManager

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

from worker_automate_hub.api.client import get_config_by_name

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)

from worker_automate_hub.models.dto.rpa_sap_dto import (
    RpaProcessoSapDTO,
)

from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

from worker_automate_hub.utils.util import (
    worker_sleep,
    kill_all_emsys,
)

console = Console()


# ============================================================
# EXCEÇÕES
# ============================================================

class FalhaNegocioSAP(Exception):
    pass


class FalhaNegocioDescartadoSAP(Exception):
    pass


# ============================================================
# CLASSE PRINCIPAL
# ============================================================

class EmissaoNotaCuponadaSAP:

    # ========================================================
    # URL / SHELL
    # ========================================================

    HASH_INICIAL = "Z_NFC-manage"

    # ========================================================
    # LOGIN
    # ========================================================

    X_CLIENT = "//input[@id='CLIENT_FIELD-inner']"
    X_LOGIN_INPUTS = "loginInputField"
    X_LOGIN_BUTTON = "LOGIN_SUBMIT_BLOCK"

    # ========================================================
    # IFRAME
    # ========================================================

    X_IFRAME_NFC = (
        "//iframe[@name='application-Z_NFC-manage-iframe']"
    )

    # ========================================================
    # BOTÕES / CAMPOS
    # ========================================================

    X_BOTAO_EXECUTAR = (
        "//*[self::button or self::a or @role='button' "
        "or contains(@class,'Button')]"
        "[normalize-space(.)='Executar' "
        "or @title='Executar' "
        "or @aria-label='Executar']"
        " | "
        "//*[normalize-space(.)='Executar']"
        "/ancestor::*"
        "[self::button or self::a or @role='button'][1]"
    )

    X_BOTAO_CRIAR_NOTA = (
        "//*["
        "self::button "
        "or self::a "
        "or @role='button' "
        "or contains(@class,'Button') "
        "or contains(@class,'urBtn')"
        "]["
        "normalize-space(.)='Criar Nota Fiscal Cuponada' "
        "or @title='Criar Nota Fiscal Cuponada' "
        "or @aria-label='Criar Nota Fiscal Cuponada' "
        "or contains(@lsdata,'Criar Nota Fiscal Cuponada')"
        "]"
    )

    X_CAMPO_BP_NF = (
        "//input[@title='Código do BP da NF:']"
    )

    X_BOTAO_AVANCAR = (
        "//*[self::button or self::a or @role='button' "
        "or contains(@class,'Button')]"
        "[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÃÂÉÊÍÓÔÕÚÇ',"
        "'abcdefghijklmnopqrstuvwxyzáàãâéêíóôõúç'),"
        "'avançar'"
        ")"
        " or "
        "contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'avancar'"
        ")]"
    )

    X_BOTAO_AVANCAR_LISTA_CUPONS = (
        "//div[@role='button' and ("
        "@title='Avançar (Entrada)' "
        "or @aria-label='Avançar (Entrada)' "
        "or @aria-label='Avançar'"
        ")]"
    )

    # ========================================================
    # CONSTRUTOR
    # ========================================================

    def __init__(
        self,
        task: RpaProcessoSapDTO,
        base_url: str,
    ):

        self.task = task

        self.config_entrada = self.normalizar_config_entrada(
            getattr(
                task,
                "configEntrada",
                {},
            )
            or {}
        )

        base_limpa = str(
            base_url or ""
        ).split("#")[0]

        self.base_url = (
            base_limpa
            + "#"
            + self.HASH_INICIAL
        )

        # ====================================================
        # CREDENCIAIS
        # ====================================================

        self.user = (
            CredentialsManager().get_by_key(
                "SAP_USER_DRC"
            )
        )

        self.password = (
            CredentialsManager().get_by_key(
                "SAP_PASSWORD_DRC"
            )
        )

        # ====================================================
        # CONFIG ENTRADA
        # ====================================================

        self.filial = self.get_config_value(
            "filial"
        )

        self.codigo_cupom = self.get_config_value(
            "codigoCupom"
        )

        self.codigo_cliente = self.get_config_value(
            "codigoCliente"
        )

        self.codigo_empresa = self.get_config_value(
            "codigoEmpresa"
        )

        self.identificador = self.get_config_value(
            "identificador"
        )

        self.valor_montante = self.get_config_value(
            "valorMontante"
        )

        self.data_lancamento = self.get_config_value(
            "dataLancamento"
        )

        self.data_compensacao = self.get_config_value(
            "dataCompensacao"
        )

        # ====================================================
        # VARIÁVEIS INTERNAS
        # ====================================================

        self.driver: Optional[
            webdriver.Chrome
        ] = None

        self.numero_nota_fiscal: Optional[
            str
        ] = None

        self.ultima_mensagem_status_sap: Optional[
            str
        ] = None

        # ====================================================
        # LOG INICIAL
        # ====================================================

        console.print(
            "[INIT] EmissaoNotaCuponadaSAP inicializado."
        )

        console.print(
            f"[INIT] URL SAP: {self.base_url}"
        )

        console.print(
            "[INIT] Usuário SAP carregado? "
            f"{'SIM' if self.user else 'NÃO'}"
        )

        console.print(
            f"[INIT] filial={self.filial}"
        )

        console.print(
            f"[INIT] codigoCupom={self.codigo_cupom}"
        )

        console.print(
            f"[INIT] codigoCliente={self.codigo_cliente}"
        )

        console.print(
            f"[INIT] codigoEmpresa={self.codigo_empresa}"
        )

        console.print(
            f"[INIT] identificador={self.identificador}"
        )

        console.print(
            f"[INIT] valorMontante={self.valor_montante}"
        )

        console.print(
            f"[INIT] dataLancamento={self.data_lancamento}"
        )

        console.print(
            f"[INIT] dataCompensacao={self.data_compensacao}"
        )

    # ========================================================
    # CONFIG ENTRADA
    # ========================================================

    def normalizar_config_entrada(
        self,
        config,
    ):

        if config is None:
            return {}

        if isinstance(
            config,
            dict,
        ):
            return config

        if isinstance(
            config,
            str,
        ):

            texto = config.strip()

            if not texto:
                return {}

            try:

                return json.loads(
                    texto
                )

            except Exception as e:

                raise RuntimeError(
                    "configEntrada veio como string, "
                    f"mas não é JSON válido: {e}"
                )

        try:

            return vars(
                config
            )

        except Exception:

            return {}

    def get_config_value(
        self,
        chave: str,
        default=None,
    ):

        if isinstance(
            self.config_entrada,
            dict,
        ):

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
    # RETORNOS
    # ========================================================

    def retorno_sucesso(
        self,
        status_retorno: str,
    ) -> RpaRetornoProcessoDTO:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[RESULTADO][SUCESSO] "
            "PROCESSO FINALIZADO COM SUCESSO"
        )

        console.print(
            "=" * 100
        )

        console.print(
            f"[RESULTADO][SUCESSO] "
            f"{status_retorno}"
        )

        console.print(
            "=" * 100 + "\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=status_retorno,
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    def retorno_falha_negocio(
        self,
        status_retorno: str,
    ) -> RpaRetornoProcessoDTO:

        mensagem = (
            "Ocorreu uma falha ao tentar criar "
            "a Nota Fiscal Cuponada, "
            f"status retornado : {status_retorno}"
        )

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[RESULTADO][FALHA_NEGOCIO] "
            "PROCESSO FINALIZADO COM FALHA DE NEGÓCIO"
        )

        console.print(
            "=" * 100
        )

        console.print(
            f"[RESULTADO][FALHA_NEGOCIO] "
            f"{mensagem}"
        )

        console.print(
            "=" * 100 + "\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[
                RpaTagDTO(
                    descricao=RpaTagEnum.Negocio
                )
            ],
        )

    def retorno_descartado(
        self,
        status_retorno: str,
    ) -> RpaRetornoProcessoDTO:

        mensagem = (
            "Ocorreu uma falha ao tentar criar "
            "a Nota Fiscal Cuponada, "
            f"status retornado : {status_retorno}"
        )

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[RESULTADO][DESCARTADO] "
            "PROCESSO FINALIZADO COMO DESCARTADO"
        )

        console.print(
            "=" * 100
        )

        console.print(
            f"[RESULTADO][DESCARTADO] "
            f"{mensagem}"
        )

        console.print(
            "=" * 100 + "\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Descartado,
            tags=[
                RpaTagDTO(
                    descricao=RpaTagEnum.Negocio
                )
            ],
        )

    def retorno_erro(
        self,
        status_retorno: str,
    ) -> RpaRetornoProcessoDTO:

        mensagem = (
            "Ocorreu uma falha técnica ao tentar criar "
            "a Nota Fiscal Cuponada, "
            f"status retornado : {status_retorno}"
        )

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[RESULTADO][ERRO_TECNICO] "
            "PROCESSO FINALIZADO COM ERRO TÉCNICO"
        )

        console.print(
            "=" * 100
        )

        console.print(
            f"[RESULTADO][ERRO_TECNICO] "
            f"{mensagem}"
        )

        console.print(
            "=" * 100 + "\n"
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=mensagem,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[
                RpaTagDTO(
                    descricao=RpaTagEnum.Tecnico
                )
            ],
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

            step = "ACESSAR_SAP_Z_NFC"

            console.print(
                "[SAP] Acessando diretamente a rotina "
                "Nota Fiscal Cuponada..."
            )

            console.print(
                f"[SAP] URL solicitada: "
                f"{self.base_url}"
            )

            self.driver.get(
                self.base_url
            )

            await worker_sleep(3)

            console.print(
                f"[SAP] URL antes do login: "
                f"{self.driver.current_url}"
            )

            step = "LOGIN"

            login_ok = await self.login()

            if not login_ok:

                return self.retorno_erro(
                    "Falha ao realizar login no SAP."
                )

            console.print(
                f"[SAP] URL após login: "
                f"{self.driver.current_url}"
            )

            console.print(
                f"[SAP] Título após login: "
                f"{self.driver.title}"
            )

            step = "AGUARDAR_Z_NFC"

            await self.garantir_rotina_nfc()

            step = "PREENCHER_PARAMETROS"

            await self.preencher_parametros()

            step = "EXECUTAR_CONSULTA"

            await self.clicar_executar_consulta()

            step = "TRATAR_LISTA_CUPONS_DUPLICADOS"

            await self.tratar_lista_cupons_duplicados()

            step = "CRIAR_NOTA_FISCAL_CUPONADA"

            await self.clicar_criar_nota_fiscal_cuponada()

            step = "VALIDAR_CUPOM_JA_POSSUI_NF"

            await self.validar_cupom_ja_possui_nota_fiscal()

            step = "PREENCHER_MODAL_NOTA"

            await self.preencher_modal_nota()

            step = "AVANCAR_MODAL"

            await self.clicar_avancar()

            step = "SELECIONAR_LOG_PROCESSAMENTO"

            numero_nota_fiscal = (
                await self.selecionar_registro_log()
            )

            console.print(
                "[SAP][LOG_PROCESSAMENTO] "
                "Nota Fiscal armazenada em variável: "
                f"{numero_nota_fiscal}"
            )

            step = "AVANCAR_LOG_PROCESSAMENTO"

            await self.clicar_avancar()

            step = "RETORNO_SUCESSO"

            mensagem_sucesso = (
                "Nota Fiscal Cuponada criada com sucesso. "
                f"Filial: {self.filial}. "
                f"Cupom: {self.codigo_cupom}. "
                f"Nota Fiscal: {self.numero_nota_fiscal}."
            )

            return self.retorno_sucesso(
                mensagem_sucesso
            )

        except FalhaNegocioDescartadoSAP as e:

            return self.retorno_descartado(
                str(e)
            )

        except FalhaNegocioSAP as e:

            return self.retorno_falha_negocio(
                str(e)
            )

        except Exception as e:

            tb = traceback.format_exc()

            msg = (
                "Falha na emissão de Nota Fiscal "
                "Cuponada no SAP. "
                f"Etapa: {step}. "
                f"Erro: {type(e).__name__}: {e}\n"
                f"{tb}"
            )

            console.print(
                msg
            )

            return self.retorno_erro(
                msg
            )

    # ========================================================
    # VALIDAR CONFIG
    # ========================================================

    def validar_config(
        self,
    ) -> None:

        if not self.user:

            raise RuntimeError(
                "Credencial SAP_USER_DRC "
                "não encontrada."
            )

        if not self.password:

            raise RuntimeError(
                "Credencial SAP_PASSWORD_DRC "
                "não encontrada."
            )

        obrigatorios = {
            "filial": self.filial,
            "codigoCupom": self.codigo_cupom,
            "codigoCliente": self.codigo_cliente,
            "codigoEmpresa": self.codigo_empresa,
            "identificador": self.identificador,
            "valorMontante": self.valor_montante,
            "dataLancamento": self.data_lancamento,
            "dataCompensacao": self.data_compensacao,
        }

        faltando = []

        for chave, valor in obrigatorios.items():

            if (
                valor is None
                or str(valor).strip() == ""
            ):

                faltando.append(
                    chave
                )

        if faltando:

            raise RuntimeError(
                "Campos obrigatórios não informados: "
                + ", ".join(faltando)
            )

        self.converter_data_sap(
            self.data_lancamento
        )

        self.converter_data_sap(
            self.data_compensacao
        )

    # ========================================================
    # CHROME
    # ========================================================

    def abrir_chrome(
        self,
    ) -> None:

        console.print(
            "[CHROME] Inicializando ChromeDriver..."
        )

        service = Service(
            ChromeDriverManager().install()
        )

        options = webdriver.ChromeOptions()

        options.add_argument(
            "--lang=pt-BR"
        )

        options.add_argument(
            "--log-level=3"
        )

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"],
        )

        options.add_experimental_option(
            "useAutomationExtension",
            False,
        )

        options.add_argument(
            "--disable-blink-features="
            "AutomationControlled"
        )

        options.add_argument(
            "--disable-infobars"
        )

        self.driver = webdriver.Chrome(
            service=service,
            options=options,
        )

        try:

            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                    Object.defineProperty(
                        navigator,
                        'webdriver',
                        {
                            get: () => undefined
                        }
                    );
                    """
                },
            )

        except Exception:

            pass

        self.driver.maximize_window()

        # ====================================================
        # DIAGNÓSTICO DO AMBIENTE
        # ====================================================

        try:

            capabilities = (
                self.driver.capabilities
                or {}
            )

            chrome_info = (
                capabilities.get(
                    "chrome",
                    {},
                )
                or {}
            )

            console.print(
                "[CHROME][AMBIENTE] "
                f"browserName="
                f"{capabilities.get('browserName')}"
            )

            console.print(
                "[CHROME][AMBIENTE] "
                f"browserVersion="
                f"{capabilities.get('browserVersion')}"
            )

            console.print(
                "[CHROME][AMBIENTE] "
                f"chromedriverVersion="
                f"{chrome_info.get('chromedriverVersion')}"
            )

            try:

                tamanho = (
                    self.driver.get_window_size()
                )

                console.print(
                    "[CHROME][AMBIENTE] "
                    f"windowWidth="
                    f"{tamanho.get('width')} | "
                    f"windowHeight="
                    f"{tamanho.get('height')}"
                )

            except Exception as e:

                console.print(
                    "[CHROME][AMBIENTE][WARN] "
                    f"Não foi possível obter tamanho "
                    f"da janela: {e}"
                )

        except Exception as e:

            console.print(
                "[CHROME][AMBIENTE][WARN] "
                f"Não foi possível coletar diagnóstico: "
                f"{e}"
            )

    # ========================================================
    # LOGIN
    # ========================================================

    async def login(
        self,
    ) -> bool:

        try:

            console.print(
                "[LOGIN] Iniciando login..."
            )

            await self.alterar_client_para_800()

            inputs = (
                await self.aguardar_inputs_login()
            )

            if len(inputs) < 2:

                console.print(
                    "[LOGIN][ERRO] "
                    "Usuário/senha não encontrados."
                )

                return False

            inputs[0].clear()

            inputs[0].send_keys(
                self.user
            )

            inputs[1].clear()

            inputs[1].send_keys(
                self.password
            )

            await worker_sleep(0.5)

            botao = (
                await self.aguardar_botao_login()
            )

            if not botao:

                return False

            botao.click()

            console.print(
                "[LOGIN][OK] "
                "Clique realizado via Selenium."
            )

            await worker_sleep(7)

            return True

        except Exception:

            console.print(
                traceback.format_exc()
            )

            return False

    async def alterar_client_para_800(
        self,
    ) -> None:

        campo = WebDriverWait(
            self.driver,
            30,
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.X_CLIENT,
                )
            )
        )

        campo.click()

        campo.send_keys(
            Keys.CONTROL,
            "a",
        )

        campo.send_keys(
            Keys.DELETE
        )

        campo.send_keys(
            "800"
        )

        await worker_sleep(0.5)

        valor = (
            campo.get_attribute("value")
            or ""
        )

        if valor.strip() != "800":

            self.driver.execute_script(
                """
                const el = arguments[0];

                el.value = '800';

                el.dispatchEvent(
                    new Event(
                        'input',
                        {
                            bubbles: true
                        }
                    )
                );

                el.dispatchEvent(
                    new Event(
                        'change',
                        {
                            bubbles: true
                        }
                    )
                );
                """,
                campo,
            )

        valor = (
            campo.get_attribute("value")
            or ""
        )

        console.print(
            f"[LOGIN] Client SAP: {valor}"
        )

        if valor.strip() != "800":

            raise RuntimeError(
                "Não conseguiu definir "
                "SAP client 800."
            )

    async def aguardar_inputs_login(
        self,
    ):

        for tentativa in range(
            1,
            31,
        ):

            inputs = (
                self.driver.find_elements(
                    By.CLASS_NAME,
                    self.X_LOGIN_INPUTS,
                )
            )

            console.print(
                f"[LOGIN] tentativa "
                f"{tentativa}/30 | "
                f"inputs={len(inputs)}"
            )

            if len(inputs) >= 2:

                return inputs

            await worker_sleep(1)

        return []

    async def aguardar_botao_login(
        self,
    ):

        for tentativa in range(
            1,
            11,
        ):

            botoes = (
                self.driver.find_elements(
                    By.ID,
                    self.X_LOGIN_BUTTON,
                )
            )

            if botoes:

                return botoes[0]

            await worker_sleep(1)

        return None

    # ========================================================
    # ACESSO Z_NFC
    # ========================================================

    async def garantir_rotina_nfc(
        self,
        timeout: int = 90,
    ) -> None:

        console.print(
            "[SAP] Aguardando carregamento "
            "da rotina Z_NFC..."
        )

        await worker_sleep(8)

        url_atual = (
            self.driver.current_url
            or ""
        )

        console.print(
            f"[SAP] URL após autenticação: "
            f"{url_atual}"
        )

        if "#Z_NFC-manage" not in url_atual:

            console.print(
                "[SAP][WARN] "
                "A URL após o login não está "
                "na Z_NFC. Reabrindo..."
            )

            self.driver.get(
                self.base_url
            )

            await worker_sleep(8)

            url_atual = (
                self.driver.current_url
                or ""
            )

            console.print(
                f"[SAP] URL após reabrir Z_NFC: "
                f"{url_atual}"
            )

        fim = (
            datetime.now().timestamp()
            + timeout
        )

        ultimo_titulo = ""

        while (
            datetime.now().timestamp()
            < fim
        ):

            try:

                ultimo_titulo = (
                    self.driver.title
                    or ""
                )

                self.driver.switch_to.default_content()

                body = (
                    self.driver.find_elements(
                        By.TAG_NAME,
                        "body",
                    )
                )

                if body:

                    texto = (
                        self.normalizar_texto(
                            body[0].text
                        )
                    )

                    if (
                        "nota fiscal" in texto
                        or "cuponada" in texto
                        or "z_nfc" in texto
                    ):

                        console.print(
                            "[SAP] Rotina Nota Fiscal "
                            "Cuponada carregada."
                        )

                        return

                texto_frames = (
                    self.normalizar_texto(
                        self.obter_texto_todos_frames()
                    )
                )

                if (
                    "nota fiscal" in texto_frames
                    or "cuponada" in texto_frames
                    or "programa de criação"
                    in texto_frames
                ):

                    console.print(
                        "[SAP] Rotina Nota Fiscal "
                        "Cuponada encontrada em iframe."
                    )

                    return

            except Exception as e:

                console.print(
                    "[SAP][WARN] "
                    f"Ainda aguardando Z_NFC: {e}"
                )

            await worker_sleep(2)

        console.print(
            "[SAP][WARN] "
            "Não foi possível confirmar "
            "o carregamento da Z_NFC."
        )

        console.print(
            f"[SAP][WARN] "
            f"URL atual: "
            f"{self.driver.current_url}"
        )

        console.print(
            f"[SAP][WARN] "
            f"Título atual: "
            f"{ultimo_titulo}"
        )

        await self.debug_tela()

    # ========================================================
    # PREENCHER PARÂMETROS
    # ========================================================

    async def preencher_parametros(
        self,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][PARAMETROS] "
            "INICIANDO PREENCHIMENTO DOS PARÂMETROS"
        )

        console.print(
            "=" * 100
        )

        data_operacao = (
            self.converter_data_sap(
                self.data_lancamento
            )
        )

        console.print(
            "[SAP][PARAMETROS] "
            f"Cupom fiscal ..........: "
            f"{self.codigo_cupom}"
        )

        console.print(
            "[SAP][PARAMETROS] "
            f"Centro .................: "
            f"{self.filial}"
        )

        console.print(
            "[SAP][PARAMETROS] "
            f"Data inicial ...........: "
            f"{data_operacao}"
        )

        console.print(
            "[SAP][PARAMETROS] "
            f"Data final .............: "
            f"{data_operacao}"
        )

        console.print(
            "[SAP][PARAMETROS] "
            "Nro. PDV ................: "
            "NÃO PREENCHER"
        )

        console.print(
            "[SAP][PARAMETROS] "
            "Id do cliente ...........: "
            "NÃO PREENCHER"
        )

        preenchido_cupom = (
            await self.preencher_por_label(
                labels=[
                    "Cupom fiscal",
                    "Cupom fiscal:",
                ],
                valor=str(
                    self.codigo_cupom
                ),
                obrigatorio=True,
            )
        )

        if not preenchido_cupom:

            raise RuntimeError(
                "Não foi possível preencher "
                "o campo Cupom fiscal."
            )

        preenchido_centro = (
            await self.preencher_por_label(
                labels=[
                    "Centro",
                    "Centro:",
                ],
                valor=str(
                    self.filial
                ),
                obrigatorio=True,
            )
        )

        if not preenchido_centro:

            raise RuntimeError(
                "Não foi possível preencher "
                "o campo Centro."
            )

        preenchido_data_inicial = (
            await self.preencher_por_label(
                labels=[
                    "Data de operação",
                    "Data de operacao",
                    "Data de operação:",
                    "Data de operacao:",
                ],
                valor=data_operacao,
                obrigatorio=True,
            )
        )

        if not preenchido_data_inicial:

            raise RuntimeError(
                "Não foi possível preencher "
                "a Data de operação inicial."
            )

        preenchido_data_final = (
            await self.preencher_por_label(
                labels=[
                    "até",
                    "ate",
                    "até:",
                    "ate:",
                ],
                valor=data_operacao,
                obrigatorio=True,
            )
        )

        if not preenchido_data_final:

            raise RuntimeError(
                "Não foi possível preencher "
                "a Data de operação final."
            )

        await worker_sleep(2)

        console.print(
            "[SAP][PARAMETROS] "
            "PREENCHIMENTO FINALIZADO"
        )

        await self.debug_campos_visiveis()

    # ========================================================
    # EXECUTAR CONSULTA
    # ========================================================

    async def clicar_executar_consulta(
        self,
        timeout: int = 60,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][EXECUTAR] "
            "INICIANDO EXECUÇÃO DA CONSULTA"
        )

        console.print(
            "=" * 100
        )

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            elemento = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_BOTAO_EXECUTAR,
                    )
                )
            )

            self.scroll_elemento(
                elemento
            )

            await worker_sleep(0.5)

            elemento.click()

            console.print(
                "[SAP][EXECUTAR][OK] "
                "Clique realizado."
            )

            await worker_sleep(6)

            self.capturar_e_tratar_mensagem_status_sap(
                origem="EXECUTAR"
            )

        except FalhaNegocioDescartadoSAP:

            raise

        except FalhaNegocioSAP:

            raise

        except Exception as e:

            raise RuntimeError(
                "Não foi possível clicar "
                "no botão 'Executar' dentro "
                "do iframe "
                "application-Z_NFC-manage-iframe."
            ) from e

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # MODAL BP
    # ========================================================

    def modal_bp_ja_aberto(
        self,
    ) -> bool:

        try:

            campos = (
                self.driver.find_elements(
                    By.XPATH,
                    self.X_CAMPO_BP_NF,
                )
            )

            for campo in campos:

                try:

                    if campo.is_displayed():

                        console.print(
                            "[SAP][CRIAR_NOTA][ESTADO] "
                            "Modal 'Código do BP da NF' "
                            "já está aberto."
                        )

                        return True

                except StaleElementReferenceException:

                    continue

                except Exception:

                    continue

        except Exception:

            pass

        return False

    # ========================================================
    # BOTÃO REAL CRIAR NOTA
    # ========================================================

    def localizar_botao_criar_nota_real(
        self,
    ):

        try:

            candidatos = (
                self.driver.find_elements(
                    By.XPATH,
                    self.X_BOTAO_CRIAR_NOTA,
                )
            )

            if not candidatos:

                candidatos = (
                    self.driver.find_elements(
                        By.XPATH,
                        "//*[contains("
                        "translate(normalize-space(.),"
                        "'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÃÂÉÊÍÓÔÕÚÇ',"
                        "'abcdefghijklmnopqrstuvwxyzáàãâéêíóôõúç'),"
                        "'criar nota fiscal cuponada'"
                        ")]",
                    )
                )

            candidatos_validos = []

            for elemento in candidatos:

                try:

                    if not elemento.is_displayed():

                        continue

                    if not elemento.is_enabled():

                        continue

                    tag = (
                        elemento.tag_name
                        or ""
                    ).strip().lower()

                    id_elemento = (
                        elemento.get_attribute("id")
                        or ""
                    ).strip()

                    role = (
                        elemento.get_attribute("role")
                        or ""
                    ).strip().lower()

                    titulo = (
                        elemento.get_attribute("title")
                        or ""
                    ).strip()

                    aria = (
                        elemento.get_attribute("aria-label")
                        or ""
                    ).strip()

                    classe = (
                        elemento.get_attribute("class")
                        or ""
                    ).strip()

                    lsdata = (
                        elemento.get_attribute("lsdata")
                        or ""
                    )

                    texto = " ".join(
                        (
                            elemento.text
                            or ""
                        ).split()
                    ).strip()

                    if id_elemento == "webguiPage0":

                        continue

                    if len(texto) > 200:

                        continue

                    alvo = (
                        "criar nota fiscal cuponada"
                    )

                    texto_normalizado = (
                        self.normalizar_texto(
                            texto
                        )
                    )

                    titulo_normalizado = (
                        self.normalizar_texto(
                            titulo
                        )
                    )

                    aria_normalizado = (
                        self.normalizar_texto(
                            aria
                        )
                    )

                    lsdata_normalizado = (
                        self.normalizar_texto(
                            lsdata
                        )
                    )

                    corresponde = (
                        texto_normalizado == alvo
                        or titulo_normalizado == alvo
                        or aria_normalizado == alvo
                        or alvo in lsdata_normalizado
                    )

                    if not corresponde:

                        continue

                    classe_lower = (
                        classe.lower()
                    )

                    clicavel = (
                        tag in (
                            "button",
                            "a",
                        )
                        or role == "button"
                        or "button"
                        in classe_lower
                        or "urbtn"
                        in classe_lower
                        or titulo_normalizado
                        == alvo
                        or aria_normalizado
                        == alvo
                        or alvo
                        in lsdata_normalizado
                    )

                    if not clicavel:

                        try:

                            pai = (
                                elemento.find_element(
                                    By.XPATH,
                                    "./ancestor::*["
                                    "@role='button' "
                                    "or self::button "
                                    "or self::a "
                                    "or contains(@class,'Button') "
                                    "or contains(@class,'urBtn')"
                                    "][1]",
                                )
                            )

                            if (
                                pai.is_displayed()
                                and pai.is_enabled()
                            ):

                                pai_id = (
                                    pai.get_attribute(
                                        "id"
                                    )
                                    or ""
                                ).strip()

                                pai_texto = " ".join(
                                    (
                                        pai.text
                                        or ""
                                    ).split()
                                ).strip()

                                if (
                                    pai_id
                                    != "webguiPage0"
                                    and len(
                                        pai_texto
                                    ) <= 200
                                ):

                                    elemento = pai

                                    clicavel = True

                        except Exception:

                            pass

                    if not clicavel:

                        continue

                    candidatos_validos.append(
                        elemento
                    )

                except StaleElementReferenceException:

                    continue

                except Exception:

                    continue

            if not candidatos_validos:

                return None

            for elemento in candidatos_validos:

                try:

                    texto = (
                        self.normalizar_texto(
                            elemento.text
                        )
                    )

                    if (
                        texto
                        == "criar nota fiscal cuponada"
                    ):

                        return elemento

                except Exception:

                    continue

            return candidatos_validos[0]

        except Exception as e:

            console.print(
                "[SAP][CRIAR_NOTA][WARN] "
                f"Erro ao localizar botão real: "
                f"{e}"
            )

            return None

    # ========================================================
    # AGUARDAR ESTADO CRIAR NOTA
    # ========================================================

    async def aguardar_estado_criar_nota(
        self,
        timeout_total: int = 180,
    ):

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][CRIAR_NOTA] "
            "AGUARDANDO TRANSIÇÃO DO SAP"
        )

        console.print(
            f"[SAP][CRIAR_NOTA] "
            f"Timeout total: "
            f"{timeout_total} segundos"
        )

        console.print(
            "=" * 100
        )

        inicio = (
            datetime.now().timestamp()
        )

        fim = (
            inicio
            + timeout_total
        )

        ultimo_texto = ""

        ultimo_segundo_log = -1

        while (
            datetime.now().timestamp()
            < fim
        ):

            try:

                self.driver.switch_to.default_content()

                WebDriverWait(
                    self.driver,
                    15,
                    poll_frequency=0.5,
                    ignored_exceptions=(
                        StaleElementReferenceException,
                        NoSuchElementException,
                    ),
                ).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (
                            By.XPATH,
                            self.X_IFRAME_NFC,
                        )
                    )
                )

                # ============================================
                # URL
                # ============================================

                try:

                    url_atual = (
                        self.driver.current_url
                        or ""
                    )

                except Exception:

                    url_atual = ""

                # ============================================
                # 1 - MODAL BP
                # ============================================

                if self.modal_bp_ja_aberto():

                    console.print(
                        "[SAP][CRIAR_NOTA][OK] "
                        "Modal do BP identificado."
                    )

                    return "MODAL_BP"

                # ============================================
                # 2 - MENSAGEM SAP
                # ============================================

                self.capturar_e_tratar_mensagem_status_sap(
                    origem="AGUARDAR_CRIAR_NOTA"
                )

                # ============================================
                # 3 - BOTÃO
                # ============================================

                botao = (
                    self.localizar_botao_criar_nota_real()
                )

                if botao is not None:

                    console.print(
                        "[SAP][CRIAR_NOTA][OK] "
                        "Botão real "
                        "'Criar Nota Fiscal Cuponada' "
                        "localizado."
                    )

                    return botao

                # ============================================
                # 4 - ESTADO VISUAL
                # ============================================

                try:

                    body = (
                        self.driver.find_element(
                            By.TAG_NAME,
                            "body",
                        )
                    )

                    texto_atual = " ".join(
                        (
                            body.text
                            or ""
                        ).split()
                    )

                    texto_normalizado = (
                        self.normalizar_texto(
                            texto_atual
                        )
                    )

                    # ----------------------------------------
                    # REGRAS DE NEGÓCIO
                    # ----------------------------------------

                    if (
                        "cupom ja possui nota fiscal criada"
                        in texto_normalizado
                        or
                        "cupom selecionado ja possui nfc criada"
                        in texto_normalizado
                        or
                        "cupom ja possui nfc criada"
                        in texto_normalizado
                    ):

                        raise FalhaNegocioDescartadoSAP(
                            "Cupom já possui Nota Fiscal criada."
                        )

                    if (
                        "dados do cupom nao encontrados"
                        in texto_normalizado
                        or
                        "cupom nao encontrado"
                        in texto_normalizado
                    ):

                        raise FalhaNegocioSAP(
                            self.extrair_mensagem_relevante(
                                texto_atual
                            )
                        )

                    # ----------------------------------------
                    # LOG SOMENTE QUANDO A TELA MUDA
                    # ----------------------------------------

                    if (
                        texto_atual
                        and texto_atual
                        != ultimo_texto
                    ):

                        ultimo_texto = (
                            texto_atual
                        )

                        console.print(
                            "[SAP][CRIAR_NOTA][ESTADO] "
                            f"URL={url_atual}"
                        )

                        console.print(
                            "[SAP][CRIAR_NOTA][ESTADO] "
                            f"Tela: "
                            f"{texto_atual[:1200]}"
                        )

                except FalhaNegocioDescartadoSAP:

                    raise

                except FalhaNegocioSAP:

                    raise

                except Exception:

                    pass

                # ============================================
                # LOG DE PROGRESSO A CADA ~15 SEGUNDOS
                # ============================================

                decorrido = int(
                    datetime.now().timestamp()
                    - inicio
                )

                if (
                    decorrido // 15
                    != ultimo_segundo_log // 15
                ):

                    ultimo_segundo_log = (
                        decorrido
                    )

                    restante = max(
                        0,
                        timeout_total
                        - decorrido,
                    )

                    console.print(
                        "[SAP][CRIAR_NOTA][AGUARDANDO] "
                        f"Decorrido={decorrido}s | "
                        f"Restante={restante}s"
                    )

            except FalhaNegocioDescartadoSAP:

                raise

            except FalhaNegocioSAP:

                raise

            except (
                TimeoutException,
                StaleElementReferenceException,
                NoSuchElementException,
            ):

                pass

            except Exception as e:

                console.print(
                    "[SAP][CRIAR_NOTA][WARN] "
                    "Erro temporário durante espera: "
                    f"{type(e).__name__}: {e}"
                )

            finally:

                try:

                    self.driver.switch_to.default_content()

                except Exception:

                    pass

            await worker_sleep(2)

        # ====================================================
        # TIMEOUT TOTAL
        # ====================================================

        try:

            console.print(
                "[SAP][CRIAR_NOTA][TIMEOUT] "
                f"URL final: "
                f"{self.driver.current_url}"
            )

        except Exception:

            pass

        raise TimeoutException(
            "O SAP não apresentou o botão real "
            "'Criar Nota Fiscal Cuponada' nem o modal "
            "'Código do BP da NF' dentro de "
            f"{timeout_total} segundos."
        )

    # ========================================================
    # LISTA DUPLICADOS
    # ========================================================

    async def tratar_lista_cupons_duplicados(
        self,
        timeout: int = 45,
    ) -> bool:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][CUPONS_DUPLICADOS] "
            "VALIDANDO LISTA DE CUPONS"
        )

        console.print(
            "=" * 100
        )

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            titulo_xpath = (
                "//*[contains("
                "translate(normalize-space(.),"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÃÂÉÊÍÓÔÕÚÇ',"
                "'abcdefghijklmnopqrstuvwxyzáàãâéêíóôõúç'),"
                "'lista de cupons conforme os parametros informados'"
                ")]"
            )

            fim_espera = (
                datetime.now().timestamp()
                + timeout
            )

            titulos_visiveis = []

            while (
                datetime.now().timestamp()
                < fim_espera
            ):

                try:

                    self.capturar_e_tratar_mensagem_status_sap(
                        origem="CUPONS_DUPLICADOS"
                    )

                except (
                    FalhaNegocioDescartadoSAP,
                    FalhaNegocioSAP,
                ):

                    raise

                except Exception:

                    pass

                if self.modal_bp_ja_aberto():

                    console.print(
                        "[SAP][CUPONS_DUPLICADOS] "
                        "Modal BP já disponível."
                    )

                    return False

                try:

                    titulos = (
                        self.driver.find_elements(
                            By.XPATH,
                            titulo_xpath,
                        )
                    )

                    titulos_visiveis = []

                    for titulo in titulos:

                        try:

                            if titulo.is_displayed():

                                titulos_visiveis.append(
                                    titulo
                                )

                        except Exception:

                            continue

                    if titulos_visiveis:

                        console.print(
                            "[SAP][CUPONS_DUPLICADOS][OK] "
                            "Lista encontrada."
                        )

                        break

                except Exception:

                    pass

                botao_real = (
                    self.localizar_botao_criar_nota_real()
                )

                if botao_real is not None:

                    console.print(
                        "[SAP][CUPONS_DUPLICADOS] "
                        "Botão Criar Nota já disponível. "
                        "Não houve duplicidade."
                    )

                    return False

                await worker_sleep(1)

            if not titulos_visiveis:

                console.print(
                    "[SAP][CUPONS_DUPLICADOS][WARN] "
                    "Nenhuma lista de duplicidade foi "
                    "identificada. O próximo passo fará "
                    "o monitoramento contínuo do SAP."
                )

                return False

            cupom_esperado = str(
                self.codigo_cupom
                or ""
            ).strip()

            cupom_esperado_sem_zeros = (
                cupom_esperado.lstrip("0")
                or "0"
            )

            linhas = (
                self.driver.find_elements(
                    By.XPATH,
                    "//tr",
                )
            )

            linhas_correspondentes = []

            for linha in linhas:

                try:

                    if not linha.is_displayed():

                        continue

                    texto_linha = (
                        linha.text
                        or ""
                    ).strip()

                    if not texto_linha:

                        continue

                    celulas = (
                        linha.find_elements(
                            By.XPATH,
                            "./td",
                        )
                    )

                    cupom_linha = ""

                    if len(celulas) >= 3:

                        cupom_linha = (
                            celulas[2].text
                            or celulas[2].get_attribute(
                                "innerText"
                            )
                            or ""
                        ).strip()

                    corresponde = False

                    if cupom_linha:

                        somente_digitos = re.sub(
                            r"\D",
                            "",
                            cupom_linha,
                        )

                        if somente_digitos:

                            corresponde = (
                                somente_digitos.lstrip(
                                    "0"
                                )
                                or "0"
                            ) == (
                                cupom_esperado_sem_zeros
                            )

                    if not corresponde:

                        numeros_linha = re.findall(
                            r"\d+",
                            texto_linha,
                        )

                        for numero in numeros_linha:

                            if (
                                numero.lstrip("0")
                                or "0"
                            ) == (
                                cupom_esperado_sem_zeros
                            ):

                                corresponde = True

                                break

                    if corresponde:

                        linhas_correspondentes.append(
                            linha
                        )

                except StaleElementReferenceException:

                    continue

                except Exception:

                    continue

            quantidade = len(
                linhas_correspondentes
            )

            console.print(
                "[SAP][CUPONS_DUPLICADOS] "
                f"Quantidade encontrada: "
                f"{quantidade}"
            )

            if quantidade == 0:

                raise RuntimeError(
                    "A lista de cupons apareceu, "
                    "mas nenhuma linha correspondente "
                    f"ao cupom {self.codigo_cupom} "
                    "foi encontrada."
                )

            linha_selecionada = (
                linhas_correspondentes[-1]
            )

            console.print(
                "[SAP][CUPONS_DUPLICADOS] "
                "Selecionando a ÚLTIMA ocorrência."
            )

            linha_selecionada.click()

            await worker_sleep(0.8)

            botao_avancar = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_BOTAO_AVANCAR_LISTA_CUPONS,
                    )
                )
            )

            botao_avancar.click()

            console.print(
                "[SAP][CUPONS_DUPLICADOS][OK] "
                "Avançar clicado."
            )

            await worker_sleep(4)

            return True

        except FalhaNegocioDescartadoSAP:

            raise

        except FalhaNegocioSAP:

            raise

        except Exception as e:

            raise RuntimeError(
                "A lista de cupons foi exibida, "
                "mas não foi possível selecionar "
                "a última linha e clicar em Avançar."
            ) from e

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # CRIAR NOTA
    # ========================================================

    async def clicar_criar_nota_fiscal_cuponada(
        self,
        timeout_total: int = 180,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][CRIAR_NOTA] "
            "INICIANDO ETAPA DE CRIAÇÃO DA NOTA"
        )

        console.print(
            "=" * 100
        )

        try:

            # =================================================
            # DIAGNÓSTICO ANTES DA ESPERA
            # =================================================

            try:

                console.print(
                    "[SAP][CRIAR_NOTA] "
                    f"URL atual: "
                    f"{self.driver.current_url}"
                )

            except Exception:

                pass

            # =================================================
            # AGUARDA QUALQUER ESTADO VÁLIDO
            # =================================================

            resultado = (
                await self.aguardar_estado_criar_nota(
                    timeout_total=timeout_total
                )
            )

            # =================================================
            # SAP JÁ ESTÁ NO MODAL
            # =================================================

            if resultado == "MODAL_BP":

                console.print(
                    "[SAP][CRIAR_NOTA][OK] "
                    "SAP já avançou para o modal do BP."
                )

                return

            elemento = resultado

            # =================================================
            # LOG DO BOTÃO
            # =================================================

            try:

                console.print(
                    "[SAP][CRIAR_NOTA] "
                    "BOTÃO REAL => "
                    f"tag='{elemento.tag_name}' | "
                    f"id='"
                    f"{elemento.get_attribute('id')}' | "
                    f"role='"
                    f"{elemento.get_attribute('role')}' | "
                    f"title='"
                    f"{elemento.get_attribute('title')}' | "
                    f"aria-label='"
                    f"{elemento.get_attribute('aria-label')}' | "
                    f"class='"
                    f"{elemento.get_attribute('class')}' | "
                    f"text='"
                    f"{' '.join((elemento.text or '').split())}'"
                )

            except Exception:

                pass

            self.scroll_elemento(
                elemento
            )

            await worker_sleep(1)

            # =================================================
            # RELOCALIZA IMEDIATAMENTE ANTES DO CLIQUE
            # =================================================

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                15,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            if self.modal_bp_ja_aberto():

                console.print(
                    "[SAP][CRIAR_NOTA][OK] "
                    "Modal BP apareceu antes do clique."
                )

                return

            elemento = (
                self.localizar_botao_criar_nota_real()
            )

            if elemento is None:

                raise RuntimeError(
                    "O botão real "
                    "'Criar Nota Fiscal Cuponada' "
                    "desapareceu antes do clique."
                )

            # =================================================
            # CLIQUE
            # =================================================

            console.print(
                "[SAP][CRIAR_NOTA] "
                "Clicando no botão real..."
            )

            elemento.click()

            console.print(
                "[SAP][CRIAR_NOTA][OK] "
                "Clique realizado."
            )

            # =================================================
            # AGUARDA RESULTADO DO CLIQUE
            # =================================================

            inicio_resposta = (
                datetime.now().timestamp()
            )

            fim_resposta = (
                inicio_resposta
                + 60
            )

            ultimo_log = -1

            while (
                datetime.now().timestamp()
                < fim_resposta
            ):

                if self.modal_bp_ja_aberto():

                    console.print(
                        "[SAP][CRIAR_NOTA][OK] "
                        "Modal do BP aberto após clique."
                    )

                    return

                try:

                    self.capturar_e_tratar_mensagem_status_sap(
                        origem="CRIAR_NOTA_POS_CLIQUE"
                    )

                except (
                    FalhaNegocioDescartadoSAP,
                    FalhaNegocioSAP,
                ):

                    raise

                except Exception:

                    pass

                try:

                    body = (
                        self.driver.find_element(
                            By.TAG_NAME,
                            "body",
                        )
                    )

                    texto = (
                        self.normalizar_texto(
                            body.text
                        )
                    )

                    if (
                        "cupom ja possui nota fiscal criada"
                        in texto
                        or
                        "cupom selecionado ja possui nfc criada"
                        in texto
                        or
                        "cupom ja possui nfc criada"
                        in texto
                    ):

                        raise FalhaNegocioDescartadoSAP(
                            "Cupom já possui "
                            "Nota Fiscal criada."
                        )

                    if (
                        "dados do cupom nao encontrados"
                        in texto
                        or
                        "cupom nao encontrado"
                        in texto
                    ):

                        raise FalhaNegocioSAP(
                            self.extrair_mensagem_relevante(
                                body.text
                            )
                        )

                except FalhaNegocioDescartadoSAP:

                    raise

                except FalhaNegocioSAP:

                    raise

                except Exception:

                    pass

                decorrido = int(
                    datetime.now().timestamp()
                    - inicio_resposta
                )

                if (
                    decorrido // 10
                    != ultimo_log // 10
                ):

                    ultimo_log = (
                        decorrido
                    )

                    console.print(
                        "[SAP][CRIAR_NOTA][POS_CLIQUE] "
                        f"Aguardando modal BP... "
                        f"{decorrido}s"
                    )

                await worker_sleep(2)

            raise RuntimeError(
                "O clique no botão "
                "'Criar Nota Fiscal Cuponada' "
                "foi realizado, porém o SAP "
                "não apresentou o modal "
                "'Código do BP da NF' dentro "
                "de 60 segundos."
            )

        except FalhaNegocioDescartadoSAP:

            raise

        except FalhaNegocioSAP:

            raise

        except Exception as e:

            try:

                await self.debug_tela()

            except Exception:

                pass

            mensagem_status = (
                self.ultima_mensagem_status_sap
            )

            complemento = (
                f" Última mensagem SAP: "
                f"{mensagem_status}"
                if mensagem_status
                else
                " Nenhuma mensagem foi encontrada "
                "na barra de status do SAP."
            )

            raise RuntimeError(
                "Não foi possível concluir a etapa "
                "'Criar Nota Fiscal Cuponada'. "
                f"Erro: "
                f"{type(e).__name__}: {e}."
                f"{complemento}"
            ) from e

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # VALIDAR CUPOM JÁ PROCESSADO
    # ========================================================

    async def validar_cupom_ja_possui_nota_fiscal(
        self,
        timeout: int = 10,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][VALIDACAO_CUPOM] "
            "VERIFICANDO SE O CUPOM JÁ POSSUI NF"
        )

        console.print(
            "=" * 100
        )

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            body = (
                self.driver.find_element(
                    By.TAG_NAME,
                    "body",
                )
            )

            texto_tela = (
                body.text
                or ""
            ).strip()

            match = re.search(
                r"Cupom\s+j[áa]\s+possui\s+"
                r"Nota\s+Fiscal\s+criada\.?",
                texto_tela,
                flags=re.IGNORECASE,
            )

            if match:

                mensagem_sap = (
                    match.group(0).strip()
                )

                if not mensagem_sap.endswith(
                    "."
                ):

                    mensagem_sap += "."

                raise FalhaNegocioDescartadoSAP(
                    mensagem_sap
                )

            console.print(
                "[SAP][VALIDACAO_CUPOM][OK] "
                "Cupom ainda não possui NF."
            )

        except FalhaNegocioDescartadoSAP:

            raise

        except Exception as e:

            console.print(
                "[SAP][VALIDACAO_CUPOM][WARN] "
                f"Leitura complementar não "
                f"concluída: {e}"
            )

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # MODAL BP
    # ========================================================

    async def preencher_modal_nota(
        self,
        timeout: int = 60,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][MODAL_BP] "
            "PREENCHENDO CÓDIGO DO BP DA NF"
        )

        console.print(
            "=" * 100
        )

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            campo_bp = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_CAMPO_BP_NF,
                    )
                )
            )

            valor_atual = (
                campo_bp.get_attribute(
                    "value"
                )
                or ""
            )

            console.print(
                "[SAP][MODAL_BP] "
                f"Valor atual: {valor_atual}"
            )

            campo_bp.click()

            campo_bp.send_keys(
                Keys.CONTROL,
                "a",
            )

            campo_bp.send_keys(
                Keys.DELETE
            )

            campo_bp.send_keys(
                str(
                    self.codigo_cliente
                )
            )

            await worker_sleep(0.5)

            valor_final = (
                campo_bp.get_attribute(
                    "value"
                )
                or ""
            )

            if (
                valor_final.strip()
                != str(
                    self.codigo_cliente
                ).strip()
            ):

                raise RuntimeError(
                    "O campo 'Código do BP da NF' "
                    "não ficou com o código "
                    "do cliente. "
                    f"Esperado="
                    f"'{self.codigo_cliente}' | "
                    f"Atual='{valor_final}'."
                )

            console.print(
                "[SAP][MODAL_BP][OK] "
                "Código do BP preenchido."
            )

        except Exception as e:

            console.print(
                "[SAP][MODAL_BP][ERRO] "
                f"{e}"
            )

            raise

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # AVANÇAR
    # ========================================================

    async def clicar_avancar(
        self,
        timeout: int = 60,
    ) -> None:

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.XPATH,
                        self.X_IFRAME_NFC,
                    )
                )
            )

            botao_avancar = WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.X_BOTAO_AVANCAR,
                    )
                )
            )

            botao_avancar.click()

            console.print(
                "[SAP][AVANCAR][OK] "
                "Clique realizado."
            )

            await worker_sleep(5)

        except Exception as e:

            raise RuntimeError(
                "Não foi possível clicar "
                "no botão 'Avançar' dentro "
                "do iframe."
            ) from e

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    # ========================================================
    # LOG PROCESSAMENTO
    # ========================================================

    async def selecionar_registro_log(
        self,
        timeout: int = 60,
    ) -> str:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[SAP][LOG_PROCESSAMENTO] "
            "VALIDANDO LOG DE PROCESSAMENTO"
        )

        console.print(
            "=" * 100
        )

        try:

            self.driver.switch_to.default_content()

            WebDriverWait(
                self.driver,
                timeout,
            ).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.NAME,
                        "application-Z_NFC-manage-iframe",
                    )
                )
            )

            fim = (
                datetime.now().timestamp()
                + timeout
            )

            ultimo_texto_log = ""

            while (
                datetime.now().timestamp()
                < fim
            ):

                linhas = (
                    self.driver.find_elements(
                        By.XPATH,
                        "//tr",
                    )
                )

                textos_linhas = []

                for linha_log in linhas:

                    try:

                        texto = (
                            linha_log.text
                            or ""
                        ).strip()

                        if texto:

                            textos_linhas.append(
                                texto
                            )

                    except Exception:

                        pass

                if textos_linhas:

                    ultimo_texto_log = (
                        " | ".join(
                            textos_linhas
                        )
                    )

                notas_criadas = []

                for linha_log in linhas:

                    try:

                        texto_linha = (
                            linha_log.text
                            or ""
                        ).strip()

                    except Exception:

                        continue

                    if not texto_linha:

                        continue

                    match = re.search(
                        r"nota\s+fiscal\s+"
                        r"(\d+)\s+criada",
                        texto_linha,
                        flags=re.IGNORECASE,
                    )

                    if match:

                        notas_criadas.append(
                            (
                                linha_log,
                                texto_linha,
                                match.group(1),
                            )
                        )

                if notas_criadas:

                    (
                        linha_nota,
                        texto_nota,
                        numero_nota,
                    ) = notas_criadas[-1]

                    self.numero_nota_fiscal = (
                        numero_nota
                    )

                    console.print(
                        "[SAP][LOG_PROCESSAMENTO][OK] "
                        f"Nota Fiscal: "
                        f"{numero_nota}"
                    )

                    console.print(
                        "[SAP][LOG_PROCESSAMENTO] "
                        f"Linha: "
                        f"{texto_nota}"
                    )

                    linha_nota.click()

                    await worker_sleep(1)

                    return numero_nota

                for texto_linha in textos_linhas:

                    mensagem_parceiro = (
                        self.extrair_parceiro_nao_encontrado(
                            texto_linha
                        )
                    )

                    if mensagem_parceiro:

                        raise FalhaNegocioSAP(
                            mensagem_parceiro
                        )

                for texto_linha in textos_linhas:

                    texto_normalizado = (
                        self.normalizar_texto(
                            texto_linha
                        )
                    )

                    if (
                        "mestre de materiais"
                        in texto_normalizado
                        or
                        "nenhum documento de nota fiscal criado"
                        in texto_normalizado
                        or
                        "classe de material"
                        in texto_normalizado
                    ):

                        raise FalhaNegocioSAP(
                            "Erro de cadastro no SAP "
                            "durante a criação da NF: "
                            f"{texto_linha}"
                        )

                await worker_sleep(1)

            raise RuntimeError(
                "O SAP não apresentou uma "
                "linha de Nota Fiscal criada "
                "dentro do tempo limite. "
                f"Último conteúdo: "
                f"{ultimo_texto_log}"
            )

        except FalhaNegocioSAP:

            raise

        except Exception as e:

            raise RuntimeError(
                "Não foi possível localizar/"
                "selecionar a Nota Fiscal criada "
                "no Log de processamento."
            ) from e

        finally:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

    def extrair_parceiro_nao_encontrado(
        self,
        texto: str,
    ) -> Optional[str]:

        if not texto:

            return None

        for linha in str(
            texto
        ).splitlines():

            linha_limpa = " ".join(
                linha.split()
            )

            if not linha_limpa:

                continue

            match = re.search(
                r"(Parceiro\s+\S+\s+"
                r"(?:não|nao)\s+encontrado)",
                linha_limpa,
                flags=re.IGNORECASE,
            )

            if match:

                return (
                    match.group(1).strip()
                )

        match = re.search(
            r"(Parceiro\s+\S+\s+"
            r"(?:não|nao)\s+encontrado)",
            str(
                texto
            ),
            flags=re.IGNORECASE,
        )

        if match:

            return " ".join(
                match.group(1).split()
            )

        return None

    # ========================================================
    # PREENCHER POR LABEL
    # ========================================================

    async def preencher_por_label(
        self,
        labels: List[str],
        valor: str,
        obrigatorio: bool = True,
    ) -> bool:

        for label in labels:

            console.print(
                f"[CAMPO] Procurando label "
                f"'{label}'..."
            )

            elemento = (
                self.localizar_input_por_label_em_frames(
                    label
                )
            )

            if elemento is None:

                continue

            try:

                self.scroll_elemento(
                    elemento
                )

                elemento.click()

                elemento.send_keys(
                    Keys.CONTROL,
                    "a",
                )

                elemento.send_keys(
                    Keys.DELETE
                )

                elemento.send_keys(
                    str(
                        valor
                    )
                )

                await worker_sleep(0.4)

                valor_atual = (
                    elemento.get_attribute(
                        "value"
                    )
                    or ""
                )

                console.print(
                    f"[CAMPO] '{label}' => "
                    f"'{valor_atual}'"
                )

                self.driver.switch_to.default_content()

                return True

            except Exception as e:

                console.print(
                    f"[CAMPO][WARN] "
                    f"Erro preenchendo "
                    f"'{label}': {e}"
                )

                try:

                    self.driver.execute_script(
                        """
                        arguments[0].focus();
                        arguments[0].value = arguments[1];

                        arguments[0].dispatchEvent(
                            new Event(
                                'input',
                                {bubbles:true}
                            )
                        );

                        arguments[0].dispatchEvent(
                            new Event(
                                'change',
                                {bubbles:true}
                            )
                        );
                        """,
                        elemento,
                        str(
                            valor
                        ),
                    )

                    self.driver.switch_to.default_content()

                    return True

                except Exception:

                    pass

            finally:

                try:

                    self.driver.switch_to.default_content()

                except Exception:

                    pass

        if obrigatorio:

            raise RuntimeError(
                "Campo não encontrado. "
                f"Labels testados: "
                f"{labels}"
            )

        return False

    def localizar_input_por_label_em_frames(
        self,
        label_procurado: str,
    ):

        self.driver.switch_to.default_content()

        resultado = (
            self._localizar_input_por_label_recursivo(
                label_procurado
            )
        )

        if resultado is None:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

        return resultado

    def _localizar_input_por_label_recursivo(
        self,
        label_procurado: str,
    ):

        label_normalizado = (
            self.normalizar_texto(
                label_procurado
            )
        )

        labels = (
            self.driver.find_elements(
                By.XPATH,
                "//label",
            )
        )

        for label in labels:

            try:

                texto_label = (
                    self.normalizar_texto(
                        label.text
                    )
                )

                if (
                    label_normalizado
                    not in texto_label
                ):

                    continue

                id_for = (
                    label.get_attribute(
                        "for"
                    )
                    or ""
                )

                if id_for:

                    candidatos = (
                        self.driver.find_elements(
                            By.ID,
                            id_for,
                        )
                    )

                    if candidatos:

                        return candidatos[0]

                candidatos = (
                    label.find_elements(
                        By.XPATH,
                        ".//following::input[1] "
                        "| .//following::textarea[1]",
                    )
                )

                if candidatos:

                    return candidatos[0]

            except Exception:

                pass

        elementos_texto = (
            self.driver.find_elements(
                By.XPATH,
                "//*[normalize-space(text())!='']",
            )
        )

        for elemento in elementos_texto:

            try:

                texto = (
                    self.normalizar_texto(
                        elemento.text
                    )
                )

                if (
                    not texto
                    or label_normalizado
                    not in texto
                ):

                    continue

                candidatos = (
                    elemento.find_elements(
                        By.XPATH,
                        "./following::input[1] "
                        "| ./following::textarea[1]",
                    )
                )

                if candidatos:

                    return candidatos[0]

            except Exception:

                pass

        inputs = (
            self.driver.find_elements(
                By.XPATH,
                "//input | //textarea",
            )
        )

        for inp in inputs:

            try:

                atributos = " ".join(
                    [
                        inp.get_attribute(
                            "placeholder"
                        )
                        or "",
                        inp.get_attribute(
                            "aria-label"
                        )
                        or "",
                        inp.get_attribute(
                            "title"
                        )
                        or "",
                        inp.get_attribute(
                            "name"
                        )
                        or "",
                        inp.get_attribute(
                            "id"
                        )
                        or "",
                    ]
                )

                atributos = (
                    self.normalizar_texto(
                        atributos
                    )
                )

                if (
                    label_normalizado
                    in atributos
                ):

                    return inp

            except Exception:

                pass

        iframes = (
            self.driver.find_elements(
                By.TAG_NAME,
                "iframe",
            )
        )

        for iframe in iframes:

            try:

                self.driver.switch_to.frame(
                    iframe
                )

                resultado = (
                    self._localizar_input_por_label_recursivo(
                        label_procurado
                    )
                )

                if resultado is not None:

                    return resultado

                self.driver.switch_to.parent_frame()

            except Exception:

                try:

                    self.driver.switch_to.parent_frame()

                except Exception:

                    self.driver.switch_to.default_content()

        return None

    # ========================================================
    # TEXTO DOS FRAMES
    # ========================================================

    def obter_texto_todos_frames(
        self,
    ) -> str:

        textos = []

        try:

            self.driver.switch_to.default_content()

            body = (
                self.driver.find_element(
                    By.TAG_NAME,
                    "body",
                )
            )

            textos.append(
                body.text
            )

        except Exception:

            pass

        try:

            self.driver.switch_to.default_content()

            textos.extend(
                self._obter_texto_frames_recursivo()
            )

        except Exception:

            pass

        try:

            self.driver.switch_to.default_content()

        except Exception:

            pass

        return "\n".join(
            [
                texto
                for texto in textos
                if texto
            ]
        )

    def _obter_texto_frames_recursivo(
        self,
    ) -> list:

        textos = []

        iframes = (
            self.driver.find_elements(
                By.TAG_NAME,
                "iframe",
            )
        )

        for iframe in iframes:

            try:

                self.driver.switch_to.frame(
                    iframe
                )

                try:

                    body = (
                        self.driver.find_element(
                            By.TAG_NAME,
                            "body",
                        )
                    )

                    textos.append(
                        body.text
                    )

                except Exception:

                    pass

                textos.extend(
                    self._obter_texto_frames_recursivo()
                )

                self.driver.switch_to.parent_frame()

            except Exception:

                try:

                    self.driver.switch_to.parent_frame()

                except Exception:

                    self.driver.switch_to.default_content()

        return textos

    # ========================================================
    # DEBUG
    # ========================================================

    async def debug_tela(
        self,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[DEBUG] TEXTO COMPLETO DA TELA"
        )

        console.print(
            "=" * 100
        )

        texto = (
            self.obter_texto_todos_frames()
        )

        console.print(
            texto[:15000]
        )

        console.print(
            "=" * 100
        )

    async def debug_campos_visiveis(
        self,
    ) -> None:

        console.print(
            "\n" + "=" * 100
        )

        console.print(
            "[DEBUG] INPUTS / CAMPOS"
        )

        console.print(
            "=" * 100
        )

        self.driver.switch_to.default_content()

        self._debug_inputs_recursivo(
            nivel=0
        )

        self.driver.switch_to.default_content()

    def _debug_inputs_recursivo(
        self,
        nivel: int,
    ) -> None:

        prefixo = (
            "  " * nivel
        )

        inputs = (
            self.driver.find_elements(
                By.XPATH,
                "//input | //textarea | //select",
            )
        )

        console.print(
            f"{prefixo}"
            f"[FRAME NIVEL {nivel}] "
            f"inputs={len(inputs)}"
        )

        for idx, inp in enumerate(
            inputs[:100],
            start=1,
        ):

            try:

                console.print(
                    f"{prefixo}"
                    f"[INPUT {idx}] "
                    f"id='"
                    f"{inp.get_attribute('id')}' | "
                    f"name='"
                    f"{inp.get_attribute('name')}' | "
                    f"type='"
                    f"{inp.get_attribute('type')}' | "
                    f"placeholder='"
                    f"{inp.get_attribute('placeholder')}' | "
                    f"aria-label='"
                    f"{inp.get_attribute('aria-label')}' | "
                    f"title='"
                    f"{inp.get_attribute('title')}' | "
                    f"value='"
                    f"{inp.get_attribute('value')}'"
                )

            except Exception:

                pass

        iframes = (
            self.driver.find_elements(
                By.TAG_NAME,
                "iframe",
            )
        )

        for indice, iframe in enumerate(
            iframes,
            start=1,
        ):

            try:

                console.print(
                    f"{prefixo}"
                    f"[IFRAME {indice}] "
                    f"name='"
                    f"{iframe.get_attribute('name')}' | "
                    f"id='"
                    f"{iframe.get_attribute('id')}' | "
                    f"src='"
                    f"{iframe.get_attribute('src')}'"
                )

                self.driver.switch_to.frame(
                    iframe
                )

                self._debug_inputs_recursivo(
                    nivel + 1
                )

                self.driver.switch_to.parent_frame()

            except Exception:

                try:

                    self.driver.switch_to.parent_frame()

                except Exception:

                    self.driver.switch_to.default_content()

    # ========================================================
    # STATUS SAP
    # ========================================================

    def obter_mensagem_status_sap(
        self,
    ) -> Optional[str]:

        try:

            elementos = (
                self.driver.find_elements(
                    By.XPATH,
                    "//span[@id='wnd[0]/sbar_msg-txt']",
                )
            )

            for elemento in elementos:

                try:

                    if not elemento.is_displayed():

                        continue

                    mensagem = (
                        elemento.text
                        or elemento.get_attribute(
                            "innerText"
                        )
                        or elemento.get_attribute(
                            "textContent"
                        )
                        or ""
                    )

                    mensagem = " ".join(
                        str(
                            mensagem
                        ).split()
                    ).strip()

                    if mensagem:

                        return mensagem

                except StaleElementReferenceException:

                    continue

                except Exception:

                    continue

        except Exception:

            pass

        return None

    def capturar_e_tratar_mensagem_status_sap(
        self,
        origem: str = "STATUS",
    ) -> Optional[str]:

        mensagem_sap = (
            self.obter_mensagem_status_sap()
        )

        if not mensagem_sap:

            return None

        mensagem_anterior = (
            self.ultima_mensagem_status_sap
        )

        self.ultima_mensagem_status_sap = (
            mensagem_sap
        )

        if (
            mensagem_sap
            != mensagem_anterior
        ):

            console.print(
                f"[SAP][{origem}][STATUS] "
                f"Mensagem SAP: "
                f"{mensagem_sap}"
            )

        mensagem_normalizada = (
            self.normalizar_texto(
                mensagem_sap
            )
        )

        mensagens_ja_processado = (
            "cupom selecionado ja possui nfc criada",
            "cupom ja possui nfc criada",
            "cupom selecionado ja possui nota fiscal criada",
            "cupom ja possui nota fiscal criada",
        )

        if any(
            termo in mensagem_normalizada
            for termo in mensagens_ja_processado
        ):

            mensagem_limpa = (
                mensagem_sap.rstrip(
                    " ."
                )
            )

            raise FalhaNegocioDescartadoSAP(
                f"{mensagem_limpa}. "
                f"Filial: {self.filial}. "
                f"Cupom: {self.codigo_cupom}. "
                f"Data: "
                f"{self.converter_data_sap(self.data_lancamento)}."
            )

        mensagens_nao_encontrado = (
            "dados do cupom nao encontrados",
            "cupom nao encontrado",
            "cupom nao foi encontrado",
        )

        if any(
            termo in mensagem_normalizada
            for termo in mensagens_nao_encontrado
        ):

            mensagem_limpa = (
                mensagem_sap.rstrip(
                    " ."
                )
            )

            raise FalhaNegocioSAP(
                f"{mensagem_limpa}. "
                f"Filial: {self.filial}. "
                f"Cupom: {self.codigo_cupom}. "
                f"Data: "
                f"{self.converter_data_sap(self.data_lancamento)}."
            )

        return mensagem_sap

    # ========================================================
    # AUXILIARES
    # ========================================================

    def converter_data_sap(
        self,
        valor,
    ) -> str:

        texto = str(
            valor
            or ""
        ).strip()

        formatos = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]

        for formato in formatos:

            try:

                dt = datetime.strptime(
                    texto,
                    formato,
                )

                return dt.strftime(
                    "%d.%m.%Y"
                )

            except ValueError:

                continue

        raise RuntimeError(
            f"Data inválida: "
            f"{valor}"
        )

    def normalizar_texto(
        self,
        texto,
    ) -> str:

        texto = str(
            texto
            or ""
        ).lower()

        texto = unicodedata.normalize(
            "NFD",
            texto,
        )

        texto = "".join(
            caractere
            for caractere in texto
            if unicodedata.category(
                caractere
            ) != "Mn"
        )

        texto = texto.replace(
            "\n",
            " ",
        )

        texto = texto.replace(
            "\r",
            " ",
        )

        texto = texto.replace(
            "\t",
            " ",
        )

        texto = re.sub(
            r"\s+",
            " ",
            texto,
        )

        return texto.strip()

    def extrair_mensagem_relevante(
        self,
        texto,
    ) -> str:

        linhas = [
            linha.strip()
            for linha in str(
                texto
                or ""
            ).splitlines()
            if linha.strip()
        ]

        palavras = [
            "erro",
            "falha",
            "sucesso",
            "criada",
            "criado",
            "processado",
            "nota fiscal",
            "cupom",
            "bp",
            "cliente",
            "inválido",
            "invalido",
            "não encontrado",
            "nao encontrado",
            "já existe",
            "ja existe",
        ]

        relevantes = []

        for linha in linhas:

            normalizada = (
                self.normalizar_texto(
                    linha
                )
            )

            if any(
                self.normalizar_texto(
                    palavra
                )
                in normalizada
                for palavra
                in palavras
            ):

                relevantes.append(
                    linha
                )

        if relevantes:

            return " | ".join(
                relevantes[:10]
            )

        if linhas:

            return " | ".join(
                linhas[-10:]
            )

        return (
            "Nenhuma mensagem SAP capturada."
        )

    def scroll_elemento(
        self,
        elemento,
    ) -> None:

        try:

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: 'instant',
                    block: 'center',
                    inline: 'center'
                });
                """,
                elemento,
            )

        except Exception:

            pass


# ============================================================
# ENTRY POINT
# ============================================================

async def emissao_nota_cuponada_sap(
    task: RpaProcessoSapDTO,
) -> RpaRetornoProcessoDTO:

    console.print(
        "\n" + "=" * 100
    )

    console.print(
        "[MAIN] INICIANDO ROBÔ - "
        "EMISSÃO DE NOTA FISCAL CUPONADA SAP"
    )

    console.print(
        "=" * 100
    )

    bot: Optional[
        EmissaoNotaCuponadaSAP
    ] = None

    try:

        await kill_all_emsys()

        config = (
            await get_config_by_name(
                "SAP_Faturamento"
            )
        )

        base_url = (
            config.conConfiguracao.get(
                "baseUrl"
            )
        )

        if not base_url:

            raise RuntimeError(
                "baseUrl não encontrada "
                "em SAP_Faturamento."
            )

        bot = EmissaoNotaCuponadaSAP(
            task=task,
            base_url=base_url,
        )

        return await bot.iniciar()

    except Exception as ex:

        tb = traceback.format_exc()

        msg = (
            "Erro geral na automação SAP "
            "de emissão de Nota Fiscal Cuponada: "
            f"{type(ex).__name__}: {ex}\n"
            f"{tb}"
        )

        console.print(
            "[MAIN][ERRO]"
        )

        console.print(
            tb
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=(
                "Ocorreu uma falha técnica "
                "ao tentar criar "
                "a Nota Fiscal Cuponada, "
                f"status retornado : {msg}"
            ),
            status=RpaHistoricoStatusEnum.Falha,
            tags=[
                RpaTagDTO(
                    descricao=RpaTagEnum.Tecnico
                )
            ],
        )

    finally:

        try:

            if (
                bot
                and bot.driver
            ):

                console.print(
                    "[MAIN] Fechando navegador."
                )

                bot.driver.quit()

                bot.driver = None

        except Exception:

            pass

        console.print(
            "=" * 100
        )

        console.print(
            "[MAIN] FIM DO ROBÔ - "
            "EMISSÃO DE NOTA FISCAL CUPONADA SAP"
        )

        console.print(
            "=" * 100 + "\n"
        )