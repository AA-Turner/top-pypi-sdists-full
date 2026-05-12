import asyncio
import io
import os
import json
import requests
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from rich.console import Console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

import sys
import traceback

from worker_automate_hub.utils.credentials_manager import CredentialsManager

# Ajuste de path para rodar local ou no worker
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from worker_automate_hub.api.client import get_config_by_name, send_file
from worker_automate_hub.api.datalake_service import send_file_to_datalake

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)

from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

from worker_automate_hub.utils.util import (
    kill_all_emsys,
    worker_sleep,
)


console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
console.print(f"[INIT] Downloads dir: {DOWNLOADS_PATH}")

# Mantém referência do driver quando der falha.
# Isso evita o garbage collector fechar o navegador antes do perform_task tirar print.
DRIVERS_ABERTOS_PARA_PRINT = []


# ==========================
# HELPERS
# ==========================

def worker_sleep_sync(seconds: int):
    import time
    time.sleep(seconds)


def _get_from_config(config, key, default=None):
    """
    Helper para funcionar tanto com dict quanto com BaseModel/Pydantic.
    """
    if isinstance(config, dict):
        return config.get(key, default)
    return getattr(config, key, default)


# ==========================
# CONFIGURAÇÕES / CONSTANTES
# ==========================

class ConfigEntradaSAP(BaseModel):
    """
    Modelo de referência para a configuração de entrada SAP.
    """
    user: Optional[str] = None
    password: Optional[str] = None
    empresa: str
    unique_id: Optional[str] = "default"
    relatorio: str


# Configuração por tipo de relatório SAP
SAP_VIEWS = {
    "FAT": {
        "iframe_id": "application-BillingDocument-analyzeRevenue-iframe",
        "input_xpath": '//*[@id="WD86-input"]',
        "url_suffix": "#BillingDocument-analyzeRevenue?sap-ui-tech-hint=WDA",
        "expandir_id": "WDE4-tgl",
    },
    "DET": {
        "iframe_id": "application-BillingDocument-analyzeBillingDocItemPricing-iframe",
        "input_xpath": '//*[@id="WDAE-input"]',
        "url_suffix": "#BillingDocument-analyzeBillingDocItemPricing?sap-ui-tech-hint=WDA",
        "expandir_id": "WDF2-tgl",
    },
    "PED": {
        "iframe_id": "application-SalesOrder-analyzeIncoming-iframe",
        "input_xpath": '//*[@id="WD86-input"]',
        "url_suffix": "#SalesOrder-analyzeIncoming?sap-ui-tech-hint=WDA",
        "expandir_id": "WDE4-tgl",
    },
}


# Mapeamento de empresa para o filtro SAP
COMPANY_FILTER = {
    "DIS": "SD01",
    "CHA": "CH01",
    "QUE": "QD01",
    "NXD": "0289",
    "NXT": "5715",
}


class NotasFaturamentoSAP:
    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        sap_url: str,
        sap_key: str,
        sap_token: str,
        base_url: str,
        directory: str,
        relatorio_override: Optional[str] = None,
    ):
        console.print("[STEP 0.1] Inicializando classe NotasFaturamentoSAP.")

        self.task = task
        self.sap_url = sap_url
        self.sap_key = sap_key
        self.sap_token = sap_token
        self.base_url = base_url
        self.directory = directory

        config = task.configEntrada

        self.user = CredentialsManager().get_by_key("SAP_USER_BI")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_BI")

        # Se quiser usar direto da configEntrada, descomente:
        # self.user = _get_from_config(config, "user")
        # self.password = _get_from_config(config, "password")

        self.empresa = _get_from_config(config, "empresa")

        self.relatorio = (
            (relatorio_override or "").upper()
            or _get_from_config(config, "relatorio", "").upper()
            or getattr(task, "relatorio", "").upper()
        )

        self.unique_id = _get_from_config(config, "unique_id", "default")
        self.driver = None

        console.print(
            f"[STEP 0.2] user={self.user} empresa={self.empresa} "
            f"relatorio={self.relatorio}"
        )

    # ============================================================
    # HELPERS DE TELA SAP
    # ============================================================

    def wait_sap_loading_sumir(self, timeout=120):
        """
        Aguarda overlays/loadings do SAP sumirem antes de clicar.
        Evita ElementClickInterceptedException por causa do ur-loading-box.
        """
        console.print("[WAIT] Aguardando loading/overlay do SAP sumir...")

        loading_selectors = [
            "#ur-loading-box",
            ".urLoadA",
            ".lsLoadABlockLayer",
            ".lsBusyIndicator",
            ".sapUiBusy",
            ".sapUiLocalBusyIndicator",
            "div[id*='loading']",
            "div[class*='Load']",
            "div[class*='Busy']",
        ]

        end_time = datetime.now().timestamp() + timeout

        while datetime.now().timestamp() < end_time:
            try:
                loading_visivel = False

                for selector in loading_selectors:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    for el in elementos:
                        try:
                            if el.is_displayed():
                                loading_visivel = True
                                break
                        except StaleElementReferenceException:
                            continue

                    if loading_visivel:
                        break

                if not loading_visivel:
                    console.print("[WAIT] Loading/overlay não está mais visível.")
                    return True

            except Exception:
                pass

            worker_sleep_sync(1)

        console.print("[WAIT][ALERTA] Timeout aguardando loading sumir.")
        return False

    def safe_click(self, element, descricao="elemento", timeout=120):
        """
        Clique seguro:
        - aguarda loading sumir
        - faz scroll até o elemento
        - tenta clique normal
        - se interceptar, aguarda novamente
        - fallback com JavaScript
        """
        console.print(f"[CLICK] Preparando clique em: {descricao}")

        self.wait_sap_loading_sumir(timeout=timeout)

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element,
            )
            worker_sleep_sync(1)
        except Exception:
            pass

        try:
            element.click()
            console.print(f"[CLICK] Clique normal realizado em: {descricao}")
            return True

        except ElementClickInterceptedException as e:
            console.print(
                f"[CLICK][ALERTA] Clique interceptado em {descricao}. "
                "Aguardando loading novamente..."
            )
            console.print(f"[CLICK][ALERTA] {str(e)}")

            self.wait_sap_loading_sumir(timeout=timeout)
            worker_sleep_sync(2)

            try:
                element.click()
                console.print(
                    f"[CLICK] Clique normal realizado após nova espera em: {descricao}"
                )
                return True

            except Exception:
                console.print(f"[CLICK] Usando fallback JavaScript em: {descricao}")
                self.driver.execute_script("arguments[0].click();", element)
                return True

        except Exception as e:
            console.print(f"[CLICK][ALERTA] Clique normal falhou em {descricao}: {e}")
            console.print(f"[CLICK] Usando fallback JavaScript em: {descricao}")
            self.driver.execute_script("arguments[0].click();", element)
            return True

    # ============================================================
    # FLUXO PRINCIPAL
    # ============================================================

    async def start_sap_process(self) -> RpaRetornoProcessoDTO:
        """
        Fluxo principal do SAP com logs de etapa:
        - VALIDATE_CONFIG
        - KILL_ALL_EMSYS
        - INIT_CHROMEDRIVER
        - INIT_WEBDRIVER
        - SAVE_PID
        - GET_BASE_URL
        - LOGIN
        - DOWNLOAD_FILES
        """
        step = "INIT"
        console.print("[STEP] Iniciando o processo SAP.")

        try:
            # 0) Validar config básica
            step = "VALIDATE_CONFIG"

            if not self.user or not self.password:
                msg = (
                    f"[{step}] Credenciais SAP inválidas: "
                    f"user={self.user} password={'***' if self.password else None}"
                )
                console.print("[ERRO] " + msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            if not self.base_url:
                msg = f"[{step}] base_url não configurada."
                console.print("[ERRO] " + msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            if self.relatorio not in SAP_VIEWS:
                msg = f"[{step}] Tipo de relatório não mapeado: {self.relatorio}"
                console.print("[ERRO] " + msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            if self.empresa not in COMPANY_FILTER:
                msg = f"[{step}] Empresa não mapeada: {self.empresa}"
                console.print("[ERRO] " + msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            # 1) Matar instâncias antigas
            step = "KILL_ALL_EMSYS"
            console.print(f"[STEP={step}] Matando instâncias EMsys/Chrome antigas...")
            await kill_all_emsys()
            console.print(f"[STEP={step}] kill_all_emsys concluído.")

            # 2) Instalar/obter ChromeDriver
            step = "INIT_CHROMEDRIVER"
            console.print(f"[STEP={step}] Instalando/obtendo ChromeDriver...")
            sim_service = Service(ChromeDriverManager().install())
            console.print(f"[STEP={step}] ChromeDriverManager instalado com sucesso.")

            # 3) Inicializar webdriver
            step = "INIT_WEBDRIVER"
            console.print(f"[STEP={step}] Inicializando webdriver.Chrome...")
            self.driver = webdriver.Chrome(service=sim_service)
            self.driver.maximize_window()
            console.print(f"[STEP={step}] Driver inicializado e janela maximizada.")

            # 4) Salvar PID
            step = "SAVE_PID"
            console.print(f"[STEP={step}] Salvando PID do Chrome...")
            ret_pid = await self.save_process_pid()

            if isinstance(ret_pid, RpaRetornoProcessoDTO) and not ret_pid.sucesso:
                console.print(f"[STEP={step}] Falha ao salvar PID, retornando erro.")
                return ret_pid

            console.print(f"[STEP={step}] PID salvo com sucesso.")

            # 5) Acessar URL base
            step = "GET_BASE_URL"
            console.print(f"[STEP={step}] Acessando URL base do SAP...")
            console.print(f"[STEP={step}] base_url: {self.base_url}")

            self.driver.get(self.base_url)

            console.print(f"[STEP={step}] driver.get(base_url) concluído.")
            await worker_sleep(3)

            # 6) Login
            step = "LOGIN"
            console.print(f"[STEP={step}] Realizando login no SAP...")

            login_ok = await self.login()

            if not login_ok:
                msg = f"Falha ao realizar login no SAP na etapa {step}"
                console.print(f"[STEP={step}] {msg}")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"[STEP={step}] Login realizado com sucesso.")

            # 7) Download / Export
            step = "DOWNLOAD_FILES"
            console.print(f"[STEP={step}] Iniciando download de arquivos...")

            ret_download = await self.download_files(self.empresa, self.relatorio)

            if isinstance(ret_download, RpaRetornoProcessoDTO):
                if not ret_download.sucesso:
                    return ret_download

                # Caso específico: sem dados para exportar.
                if ret_download.retorno:
                    return ret_download

            console.print(f"[STEP={step}] Download de arquivos concluído.")

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Processo SAP executado com sucesso.",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        except Exception as e:
            tb = traceback.format_exc()
            msg = (
                f"Erro em start_sap_process na etapa '{step}': "
                f"{type(e).__name__}: {e}"
            )

            console.print("[ERRO] " + msg)
            console.print("[ERRO] Traceback completo:")
            console.print(tb)

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg + "\n" + tb,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    async def save_process_pid(self):
        try:
            console.print("[STEP PID] Salvando o PID do processo do Chrome.")

            pid = str(self.driver.service.process.pid)
            file_path = f"c:\\tmp\\chrome_pid_{self.unique_id}.txt"

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w") as f:
                f.write(pid)

            console.print(f"[STEP PID] PID salvo em: {file_path}")

        except Exception as e:
            msg = f"Erro ao salvar PID: {e}"
            console.print(f"[ERRO PID] {msg}")
            console.print("[ERRO PID] Traceback:")
            console.print(traceback.format_exc())

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    async def login(self) -> bool:
        try:
            console.print("[LOGIN] Iniciando login no SAP.")

            for i in range(30):
                inputs = self.driver.find_elements(By.CLASS_NAME, "loginInputField")

                console.print(
                    f"[LOGIN] Tentativa {i + 1}/30 - qtd campos encontrados: {len(inputs)}"
                )

                if len(inputs) >= 2:
                    console.print("[LOGIN] Campos de entrada de login encontrados.")
                    break

                await worker_sleep(1)

            inputs = self.driver.find_elements(By.CLASS_NAME, "loginInputField")

            if len(inputs) < 2:
                console.print("[LOGIN][ERRO] Não encontrou campos de login.")
                return False

            inputs[0].send_keys(self.user)
            console.print("[LOGIN] Usuário inserido no campo de login.")

            await worker_sleep(2)

            inputs[1].send_keys(self.password)
            console.print("[LOGIN] Senha inserida no campo de login.")

            await worker_sleep(1)

            for i in range(10):
                login_btn = self.driver.find_elements(By.ID, "LOGIN_SUBMIT_BLOCK")

                console.print(
                    f"[LOGIN] Tentativa {i + 1}/10 - btn login encontrado? {bool(login_btn)}"
                )

                if login_btn:
                    login_btn[0].click()
                    console.print("[LOGIN] Botão de login clicado.")
                    break

                await worker_sleep(1)

            await worker_sleep(3)

            console.print("[LOGIN] Login finalizado sem exceção.")
            return True

        except Exception as e:
            console.print("[LOGIN][ERRO] Exceção ao realizar login.")
            console.print(f"[LOGIN][ERRO] Tipo: {type(e).__name__}")
            console.print(f"[LOGIN][ERRO] str(e): {str(e)}")
            console.print("[LOGIN][ERRO] Traceback:")
            console.print(traceback.format_exc())
            return False

    async def download_files(self, company: str, file_type: str):
        console.print(
            f"[DW] Iniciando download de arquivos para empresa {company} e tipo {file_type}."
        )
        console.print(f"[DW] self.relatorio={self.relatorio}")

        view_conf = SAP_VIEWS.get(file_type)

        if not view_conf:
            msg = f"[DW][ERRO] Tipo de arquivo não mapeado: {file_type}"
            console.print(msg)

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        doc_url = self.get_document_url(file_type)

        console.print(f"[DW] Acessando a URL do documento: {doc_url}")

        self.driver.get(doc_url)

        console.print("[DW] URL do documento carregada.")
        await worker_sleep(50)

        try:
            console.print("[DW] Localizando iframe e campo de filtro...")

            iframe = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, view_conf["iframe_id"]))
            )

            self.driver.switch_to.frame(iframe)

            console.print("[DW] Iframe principal do SAP acessado com sucesso.")

            self.wait_sap_loading_sumir(timeout=120)

            campo = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, view_conf["input_xpath"]))
            )

            console.print("[DW] Input de filtro localizado dentro do iframe.")

            if not campo:
                msg = "[DW][ERRO] Campo de filtro não localizado. Abortando exportação."
                console.print(msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"[DW] Preenchendo empresa para company={company}")

            filtro_empresa = COMPANY_FILTER.get(company)

            if not filtro_empresa:
                msg = f"[DW][ERRO] Empresa não mapeada: {company}"
                console.print(msg)

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            self.wait_sap_loading_sumir(timeout=120)
            self.safe_click(campo, "campo filtro empresa SAP")

            campo.clear()
            await worker_sleep(1)

            campo.send_keys(filtro_empresa)

            console.print(f"[DW] Empresa preenchida no filtro: {filtro_empresa}")

            self.wait_sap_loading_sumir(timeout=120)
            await worker_sleep(2)

            console.print("[DW] Clicando em 'Início' após filtros...")

            botao_inicio = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and contains(., 'nício')]")
                )
            )

            self.safe_click(botao_inicio, "botão Início")

            console.print("[DW] Botão 'Início' clicado.")

            await worker_sleep(8)

            self.wait_sap_loading_sumir(timeout=120)

            toggle = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, view_conf["expandir_id"]))
            )

            estado = toggle.get_attribute("aria-expanded")

            console.print(f"[DW] Estado do toggle expandir: {estado}")

            if estado == "false":
                self.safe_click(toggle, "toggle expandir")

            await worker_sleep(12)

            self.wait_sap_loading_sumir(timeout=120)

            console.print("[DW] Localizando botão de exportar...")

            try:
                botao_exportar = WebDriverWait(self.driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@title='Exportar']"))
                )

                self.safe_click(botao_exportar, "botão Exportar")

                console.print("[DW] Botão de exportar clicado.")

            except Exception:
                console.print("[DW] Não há dados para serem exportados.")

                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Não há dados para serem exportados.",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

            await worker_sleep(5)

            self.wait_sap_loading_sumir(timeout=120)

            opcao_exportar = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Exportar']"))
            )

            self.safe_click(opcao_exportar, "opção Exportar")

            console.print("[DW] Opção 'Exportar' clicada com sucesso.")

            await worker_sleep(5)

            console.print("[DW] Pressionando ENTER para confirmar exportação...")

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()

            await worker_sleep(30)

            console.print("[DW] Chamando rename_file...")

            ret_rename = await self.rename_file(company, file_type)

            if isinstance(ret_rename, RpaRetornoProcessoDTO):
                return ret_rename

            console.print("[DW] rename_file concluído.")

        except Exception as e:
            console.print("[DW][ERRO] Exceção em download_files.")
            console.print(f"[DW][ERRO] Tipo: {type(e).__name__}")
            console.print(f"[DW][ERRO] str(e): {str(e)}")
            console.print("[DW][ERRO] Traceback:")
            console.print(traceback.format_exc())
            raise

    def get_document_url(self, file_type: str) -> str:
        console.print(f"[URL] Obtendo URL do documento para o tipo {file_type}.")

        view_conf = SAP_VIEWS.get(file_type)
        suffix = view_conf["url_suffix"] if view_conf else ""

        url_final = f"{self.base_url}{suffix}"

        console.print(f"[URL] URL final: {url_final}")

        return url_final

    async def rename_file(self, company: str, file_type: str):
        console.print("[RF] Iniciando renomeação e movimentação do arquivo.")

        try:
            current_path = os.path.join(DOWNLOADS_PATH, "export.xlsx")

            console.print(f"[RF] current_path esperado: {current_path}")
            console.print(f"[RF] Arquivo existe? {os.path.exists(current_path)}")

            if not os.path.exists(current_path):
                msg = f"Arquivo export.xlsx não encontrado em: {current_path}"
                console.print(f"[RF][ERRO] {msg}")

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            date_now = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{company}_{file_type}_{date_now}.xlsx"
            final_path = os.path.join(DOWNLOADS_PATH, filename)

            console.print(f"[RF] Novo filename: {filename}")

            os.rename(current_path, final_path)

            console.print(f"[RF] Arquivo renomeado para {final_path}.")

            with open(final_path, "rb") as file:
                file_bytes = io.BytesIO(file.read())

            await worker_sleep(5)

            try:
                console.print(f"[RF] directory: {self.directory}")
                console.print(f"[RF] file: {final_path}")

                send_file_request = await send_file_to_datalake(
                    self.directory,
                    file_bytes,
                    filename,
                    "xlsx",
                )

                console.print(
                    f"[RF] Resposta send_file_to_datalake: {send_file_request}"
                )

            except Exception as e:
                console.print(
                    f"[RF][ERRO] Erro ao enviar o arquivo: {e}",
                    style="bold red",
                )
                console.print("[RF][ERRO] Traceback:")
                console.print(traceback.format_exc())

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao enviar o arquivo: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            await worker_sleep(2)

            if final_path and os.path.exists(final_path):
                try:
                    os.remove(final_path)
                    console.print(f"[RF] Arquivo deletado: {final_path}")

                except Exception as e:
                    msg = f"Erro ao deletar o arquivo: {e}"

                    console.print(f"[RF][ERRO] {msg}")
                    console.print("[RF][ERRO] Traceback:")
                    console.print(traceback.format_exc())

                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=msg,
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )

            return None

        except FileNotFoundError as fne:
            msg = f"Não foi possível renomear o arquivo, error: {fne}"

            console.print(f"[RF][ERRO] {msg}")
            console.print("[RF][ERRO] Traceback:")
            console.print(traceback.format_exc())

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        except Exception as e:
            msg = f"Erro ao renomear/mover arquivo: {e}"

            console.print(f"[RF][ERRO] {msg}")
            console.print("[RF][ERRO] Traceback:")
            console.print(traceback.format_exc())

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    async def send_message_to_webhook(self, message: str):
        console.print("[WEBHOOK] Enviando mensagem ao webhook.")

        await worker_sleep(2)

        try:
            payload = {"text": "📢 " + message}
            webhook_url = f"{self.sap_url}/key={self.sap_key}&token={self.sap_token}"

            requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            console.print("[WEBHOOK] Mensagem enviada ao webhook com sucesso.")

            await worker_sleep(2)

        except Exception as e:
            msg = f"Erro ao enviar mensagem ao webhook: {e}"

            console.print(f"[WEBHOOK][ERRO] {msg}")
            console.print("[WEBHOOK][ERRO] Traceback:")
            console.print(traceback.format_exc())

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )


async def notas_faturamento_sap(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Importante:
    - Em sucesso: fecha o navegador.
    - Em falha: mantém o navegador aberto para o perform_task tirar print.
    """
    console.print("[MAIN] Iniciando processo de notas de faturamento SAP.")

    notas_sap = None

    try:
        console.print("[MAIN] Buscando configuração 'SAP_Faturamento'...")

        config = await get_config_by_name("SAP_Faturamento")

        console.print(f"[MAIN] config recebido: {config}")

        sap_url = config.conConfiguracao.get("sapUrl")
        sap_key = config.conConfiguracao.get("sapKey")
        sap_token = config.conConfiguracao.get("sapToken")
        base_url = config.conConfiguracao.get("baseUrl")
        directory = config.conConfiguracao.get("directoryBucket")

        console.print(
            f"[MAIN] sap_url={sap_url} base_url={base_url} directory={directory}"
        )

        # PEGAR RELATORIO DE FORMA SEGURA
        relatorio = None
        config_entrada = task.configEntrada

        if isinstance(config_entrada, dict):
            relatorio = config_entrada.get("relatorio")
        else:
            relatorio = getattr(config_entrada, "relatorio", None)

        if not relatorio:
            relatorio = "FAT"

        console.print(f"[MAIN] Relatório usado: {relatorio}")

        notas_sap = NotasFaturamentoSAP(
            task=task,
            sap_url=sap_url,
            sap_key=sap_key,
            sap_token=sap_token,
            base_url=base_url,
            directory=directory,
            relatorio_override=relatorio,
        )

        console.print("[MAIN] Chamando start_sap_process...")

        resultado = await notas_sap.start_sap_process()

        console.print(
            f"[MAIN] Resultado do start_sap_process: sucesso={resultado.sucesso}"
        )

        if resultado.sucesso:
            console.print("[MAIN] Processo finalizou com sucesso. Fechando navegador.")

            if notas_sap.driver:
                try:
                    notas_sap.driver.quit()
                    console.print("[MAIN] Navegador fechado com sucesso.")
                except Exception as e:
                    console.print(f"[MAIN][ALERTA] Erro ao fechar navegador: {e}")

        else:
            console.print(
                "[MAIN][FALHA] Processo retornou falha. "
                "Mantendo navegador aberto para o perform_task capturar screenshot."
            )

            if notas_sap.driver:
                DRIVERS_ABERTOS_PARA_PRINT.append(notas_sap.driver)

        return resultado

    except Exception as ex:
        console.print("[MAIN][ERRO] Exceção em notas_faturamento_sap.")
        console.print(f"[MAIN][ERRO] Tipo: {type(ex).__name__}")
        console.print(f"[MAIN][ERRO] str(ex): {str(ex)}")
        console.print("[MAIN][ERRO] Traceback completo:")
        console.print(traceback.format_exc())

        if notas_sap and notas_sap.driver:
            console.print(
                "[MAIN][ERRO] Mantendo navegador aberto para o perform_task capturar screenshot."
            )
            DRIVERS_ABERTOS_PARA_PRINT.append(notas_sap.driver)

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na automação SAP: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )