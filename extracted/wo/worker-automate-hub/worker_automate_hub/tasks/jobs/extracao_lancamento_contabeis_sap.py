# -*- coding: utf-8 -*-
import asyncio
import os
import io
import traceback
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from rich.console import Console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from worker_automate_hub.api.datalake_service import send_file_to_datalake
from worker_automate_hub.utils.credentials_manager import CredentialsManager
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.utils.util import worker_sleep

import locale
from datetime import datetime

console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
console.print(f"[INIT] Downloads dir: {DOWNLOADS_PATH}")


try:
    # fallback comum no Windows
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil")
except locale.Error:
    # fallback final: não usa locale
    pass

now = datetime.now()
date_now = now.strftime("%Y%m%d%H%M%S")

# mês por extenso
mes = now.strftime("%B").lower()
mes_num = now.strftime("%m")
ano = now.strftime("%Y")


def limpar_downloads(
    download_path: str, extensoes: tuple = (".xlsx", ".pdf", ".crdownload")
) -> int:
    pasta = Path(download_path)
    if not pasta.exists() or not pasta.is_dir():
        raise ValueError(f"DOWNLOAD_PATH inválido: {download_path}")

    removidos = 0
    erros = []

    if extensoes is None:
        arquivos = [p for p in pasta.iterdir() if p.is_file()]
    else:
        arquivos = []
        for ext in extensoes:
            arquivos.extend([p for p in pasta.glob(f"*{ext}") if p.is_file()])

    for arq in arquivos:
        try:
            arq.unlink()
            removidos += 1
        except PermissionError:
            try:
                time.sleep(0.3)
                arq.unlink()
                removidos += 1
            except Exception as e:
                erros.append((str(arq), str(e)))
        except Exception as e:
            erros.append((str(arq), str(e)))

    if erros:
        print("[limpar_downloads] Alguns arquivos não puderam ser removidos:")
        for path, err in erros[:10]:
            print(f" - {path}: {err}")

    return removidos


# ==========================
# CONFIG DE ENTRADA
# ==========================
class ConfigEntradaSAP(BaseModel):
    """
    Entrada do processo via fila:
      - empresa: "2500" ou "2500,2501"
      - conta_razao: "3111101,3111102,41111001"
    Observação: para não quebrar seu payload antigo, aceitamos também "centros" como alias.
    """

    empresa: str
    conta_razao: str = Field(..., alias="centros")

    class Config:
        allow_population_by_field_name = (
            True  # permite usar "conta_razao" OU alias "centros"
        )
        extra = "ignore"


# ==========================
# CLASSE PRINCIPAL
# ==========================
class ExtracaoLancamentoContabeis:
    # ==========================================================
    # XPATHs (SEM IFRAME)
    # ==========================================================
    X_EMPRESA = "(//input[@aria-roledescription='Entrada de valores múltiplos'])[1]"
    X_CONTA_RAZAO = "(//input[@aria-roledescription='Entrada de valores múltiplos'])[2]"
    X_PERIODO = "//input[@aria-roledescription='Entrada de data dinâmica']"
    X_BTN_INICIAR = "//bdi[text()='Iniciar']"
    X_EXPORTAR = (
        "//span[contains(@id,'btnExcelExport-internalSplitBtn-textButton-img')]"
    )

    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: str,
        directory: Optional[str] = None,
    ):
        console.print("[STEP 0.1] Inicializando ExtracaoLancamentoContabeis")

        self.task = task

        # Base URL + hash completo
        hash_path = "GLAccount-displayLineItemMAView&/?sap-iapp-state=TASWGDY6EHSZXQ7NAW52YGE5RG6IFUHLYI1TEYUA8"
        self.base_url = base_url.split("#", 1)[0] + "#" + hash_path

        # Credenciais SAP
        self.user = CredentialsManager().get_by_key("SAP_USER_BI")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_BI")

        # Valida configEntrada
        self.config_entrada = ConfigEntradaSAP(
            **(getattr(task, "configEntrada", {}) or {})
        )

        # Parse empresa e contas razão (lote com ENTER)
        self.empresas: List[str] = [
            p.strip() for p in self.config_entrada.empresa.split(",") if p.strip()
        ]
        self.contas_razao: List[str] = [
            c.strip() for c in self.config_entrada.conta_razao.split(",") if c.strip()
        ]

        if not self.empresas:
            raise ValueError("configEntrada.empresa está vazio.")
        if not self.contas_razao:
            raise ValueError("configEntrada.conta_razao/centros está vazio.")

        self.conta_ini = min(self.contas_razao)
        self.conta_fim = max(self.contas_razao)

        self.driver: Optional[webdriver.Chrome] = None

        self.download_dir = Path.home() / "Downloads"
        self.download_dir.mkdir(parents=True, exist_ok=True)

        self.directory = directory

        console.print(
            f"[STEP 0.2] user={'OK' if self.user else None} | "
            f"empresas={len(self.empresas)} | "
            f"contas_razao={len(self.contas_razao)} ({self.conta_ini}-{self.conta_fim}) | "
            f"downloads={self.download_dir} | "
            f"datalake_dir={self.directory}"
        )

    # ==========================================================
    # Helpers: scroll + limpar/digitar + click
    # ==========================================================
    async def _scroll_center(self, el) -> None:
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
        except Exception:
            pass
        await worker_sleep(0.15)

    async def _clicar(self, xpath: str, timeout: int = 60) -> None:
        wait = WebDriverWait(self.driver, timeout)
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        await self._scroll_center(el)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except (ElementClickInterceptedException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", el)

    async def _limpar_e_digitar(
        self, xpath: str, valor: str, timeout: int = 30
    ) -> None:
        wait = WebDriverWait(self.driver, timeout)

        for tentativa in range(1, 4):
            try:
                el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                await self._scroll_center(el)
                try:
                    el.click()
                except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
                ):
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    await self._scroll_center(el)
                    self.driver.execute_script("arguments[0].click();", el)

                await worker_sleep(0.10)

                el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                el.send_keys(Keys.CONTROL, "a")
                await worker_sleep(0.05)
                el.send_keys(Keys.DELETE)
                await worker_sleep(0.10)

                el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                el.send_keys(str(valor))
                await worker_sleep(0.10)
                try:
                    el.send_keys(Keys.TAB)
                except Exception:
                    pass
                await worker_sleep(0.15)

                return

            except StaleElementReferenceException:
                console.print(
                    f"[WARN] StaleElement em _limpar_e_digitar (tentativa {tentativa}/3)"
                )
                await worker_sleep(0.6)

        raise StaleElementReferenceException(
            f"Elemento ficou stale após 3 tentativas: {xpath}"
        )

    async def _digitar_em_lote_com_enter(
        self,
        xpath: str,
        valores: List[str],
        timeout: int = 30,
        pausa_entre: float = 1.0,
        limpar_antes: bool = True,
    ) -> None:
        """
        Campo SAP UI5 de valores múltiplos que só “assume” cada item com ENTER:
        digita -> ENTER -> espera -> repete.
        """
        wait = WebDriverWait(self.driver, timeout)
        valores = [str(v).strip() for v in valores if str(v).strip()]
        if not valores:
            raise ValueError("Lista de valores vazia em _digitar_em_lote_com_enter.")

        for tentativa in range(1, 4):
            try:
                el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                await self._scroll_center(el)
                try:
                    el.click()
                except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
                ):
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    await self._scroll_center(el)
                    self.driver.execute_script("arguments[0].click();", el)

                await worker_sleep(0.2)

                if limpar_antes:
                    try:
                        el = wait.until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        el.send_keys(Keys.CONTROL, "a")
                        await worker_sleep(0.05)
                        el.send_keys(Keys.DELETE)
                        await worker_sleep(0.2)
                    except Exception:
                        pass

                for v in valores:
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    el.send_keys(v + Keys.ENTER)
                    await worker_sleep(pausa_entre)

                return

            except StaleElementReferenceException:
                console.print(
                    f"[WARN] StaleElement em _digitar_em_lote_com_enter (tentativa {tentativa}/3)"
                )
                await worker_sleep(0.6)

        raise StaleElementReferenceException(
            f"Falha ao digitar em lote após 3 tentativas: {xpath}"
        )

    # ==========================================================
    # Esperar download XLSX
    # ==========================================================
    async def _aguardar_xlsx_baixado(
        self,
        timeout: int = 240,
        quiet_window_sec: float = 1.2,
        expected_name: Optional[str] = None,
        grace_sec: int = 300,  # aceita arquivo já existente se foi modificado nos últimos X segundos
    ) -> Path:
        pasta = Path(DOWNLOADS_PATH)
        start = time.time()

        console.print(f"[DL] Aguardando XLSX em: {pasta} (timeout={timeout}s)")

        # Caso você saiba o nome exato (melhor cenário)
        if expected_name:
            candidato = pasta / expected_name
            while time.time() - start < timeout:
                if list(pasta.glob("*.crdownload")):
                    await worker_sleep(0.5)
                    continue

                if candidato.exists():
                    break

                await worker_sleep(0.5)

            if not candidato.exists():
                raise TimeoutError(
                    f"[DL] Arquivo esperado não apareceu: {expected_name} em {timeout}s"
                )

            console.print(f"[DL] Candidato detectado (por nome): {candidato.name}")
            # espera estabilizar
            last_size = -1
            stable_since = None

            while time.time() - start < timeout:
                if list(pasta.glob("*.crdownload")):
                    stable_since = None
                    await worker_sleep(0.5)
                    continue

                size = candidato.stat().st_size
                if size != last_size:
                    last_size = size
                    stable_since = time.time()
                else:
                    if (
                        stable_since
                        and (time.time() - stable_since) >= quiet_window_sec
                    ):
                        return candidato

                await worker_sleep(0.4)

            return candidato  # fallback (em geral já estabilizou)

        # Caso genérico: pega o mais recente que seja "novo" OU "recente dentro de grace_sec"
        existentes = {p.name for p in pasta.glob("*.xlsx")}
        candidato: Optional[Path] = None

        while time.time() - start < timeout:
            if list(pasta.glob("*.crdownload")):
                await worker_sleep(0.5)
                continue

            xlsx_files = list(pasta.glob("*.xlsx"))
            if not xlsx_files:
                await worker_sleep(0.5)
                continue

            # 1) Se surgiu algum arquivo com nome novo, prioriza ele
            novos = [p for p in xlsx_files if p.name not in existentes]
            if novos:
                candidato = max(novos, key=lambda p: p.stat().st_mtime)
                break

            # 2) Se não surgiu nome novo, mas o mais recente foi modificado "há pouco", aceita
            ultimo = max(xlsx_files, key=lambda p: p.stat().st_mtime)
            if ultimo.stat().st_mtime >= (start - grace_sec):
                candidato = ultimo
                break

            await worker_sleep(0.5)

        if not candidato:
            raise TimeoutError(
                f"[DL] Nenhum .xlsx apareceu/atualizou em {timeout}s em {pasta}"
            )

        console.print(f"[DL] Candidato detectado: {candidato.name}")

        # Espera estabilizar tamanho
        last_size = -1
        stable_since = None

        while time.time() - start < timeout:
            if list(pasta.glob("*.crdownload")):
                stable_since = None
                await worker_sleep(0.5)
                continue

            try:
                size = candidato.stat().st_size
            except FileNotFoundError:
                xlsx_files = list(pasta.glob("*.xlsx"))
                if not xlsx_files:
                    await worker_sleep(0.5)
                    continue
                candidato = max(xlsx_files, key=lambda p: p.stat().st_mtime)
                last_size = -1
                stable_since = None
                await worker_sleep(0.4)
                continue

            if size != last_size:
                last_size = size
                stable_since = time.time()
            else:
                if stable_since and (time.time() - stable_since) >= quiet_window_sec:
                    break

            await worker_sleep(0.4)

        return candidato

    # ==========================================================
    # Renomear + Upload
    # ==========================================================
    async def rename_file(
        self, empresa: str, conta_tag: str, timeout: int = 240
    ) -> Path:
        """
        Nome final:
          CR41111001-MES-ANO-DATE_NOW.xlsx
        Ex:
          3111101-41111001-2500-02-2026-20260205173000.xlsx
        """
        console.print("[RF] Iniciando renomeação + envio pro datalake.")
        baixado = await self._aguardar_xlsx_baixado(expected_name="Itens.xlsx")
        current_path = str(baixado)

        filename = f"CR41111001-{ano}-{mes_num}-{date_now}.xlsx"
        final_path = os.path.join(DOWNLOADS_PATH, filename)

        console.print(f"[RF] Movendo para: {final_path}")
        os.rename(current_path, final_path)

        with open(final_path, "rb") as f:
            file_bytes = io.BytesIO(f.read())

        await worker_sleep(1)

        if not self.directory:
            raise RuntimeError(
                "self.directory (datalake) não foi definido. Passe pelo config SAP_Faturamento."
            )

        console.print(f"[RF] Enviando datalake: {filename}")
        await send_file_to_datalake("qd_comercial/raw", file_bytes, filename, "xlsx")

        await worker_sleep(1)

        if os.path.exists(final_path):
            os.remove(final_path)

        return Path(final_path)

    # ==========================================================
    # FLUXO: INICIAR SESSÃO SAP
    # ==========================================================
    async def iniciar_sessao_sap(self) -> RpaRetornoProcessoDTO:
        step = "INIT"
        console.print("[STEP] Iniciando fluxo: INICIAR SESSÃO SAP")

        try:
            step = "VALIDATE_CONFIG"
            if not self.user or not self.password:
                msg = f"[{step}] Credenciais SAP inválidas."
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            if not self.base_url:
                msg = f"[{step}] base_url não configurada."
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            step = "INIT_CHROMEDRIVER"
            service = Service(ChromeDriverManager().install())

            step = "INIT_WEBDRIVER"
            options = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory": str(self.download_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            }
            options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()

            step = "GET_BASE_URL"
            console.print(f"[STEP={step}] Acessando: {self.base_url}")
            self.driver.get(self.base_url)
            await worker_sleep(2)

            step = "LOGIN"
            console.print(f"[STEP={step}] Executando login...")
            ok = await self._login()
            if not ok:
                msg = f"[{step}] Falha ao realizar login."
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Sessão SAP iniciada com sucesso.",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        except Exception as e:
            tb = traceback.format_exc()
            msg = f"Erro no fluxo (etapa {step}): {type(e).__name__}: {e}"
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg + "\n" + tb,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    async def _login(self) -> bool:
        try:
            console.print("[LOGIN] Aguardando campos de login...")

            inputs = []
            for i in range(30):
                inputs = self.driver.find_elements(By.CLASS_NAME, "loginInputField")
                console.print(f"[LOGIN] Tentativa {i+1}/30 | campos: {len(inputs)}")
                if len(inputs) >= 2:
                    break
                await worker_sleep(1)

            if len(inputs) < 2:
                console.print("[LOGIN][ERRO] Campos de login não encontrados.")
                return False

            inputs[0].clear()
            inputs[0].send_keys(self.user)
            await worker_sleep(0.3)

            inputs[1].clear()
            inputs[1].send_keys(self.password)
            await worker_sleep(0.3)

            for i in range(10):
                btn = self.driver.find_elements(By.ID, "LOGIN_SUBMIT_BLOCK")
                if btn:
                    btn[0].click()
                    break
                await worker_sleep(1)

            await worker_sleep(3)
            return True

        except Exception:
            console.print("[LOGIN][ERRO] Exceção durante login.")
            console.print(traceback.format_exc())
            return False

    # ==========================================================
    # EXECUÇÃO: Conta Razão em lote (digita+ENTER+pausa)
    # ==========================================================
    async def lancamento_contabeis(self) -> List[str]:
        arquivos: List[str] = []

        conta_tag = f"{self.conta_ini}-{self.conta_fim}"

        for idx_emp, empresa in enumerate(self.empresas, start=1):
            console.print(f"[RUN] Empresa ({idx_emp}/{len(self.empresas)}): {empresa}")
            console.print(f"[RUN] Contas razão (qtd): {len(self.contas_razao)}")

            limpar_downloads(DOWNLOADS_PATH)

            # Empresa (normal)
            console.print("[STEP] Preenchendo Empresa...")
            await self._limpar_e_digitar(self.X_EMPRESA, empresa)

            # Conta Razão (lote com ENTER, 1s entre cada)
            console.print("[STEP] Preenchendo Conta Razão em lote (digita+ENTER)...")
            await self._digitar_em_lote_com_enter(
                self.X_CONTA_RAZAO,
                self.contas_razao,
                pausa_entre=1.0,
                limpar_antes=True,
            )

            # Período (se exigir outro formato no seu SAP, ajuste aqui)
            console.print("[STEP] Preenchendo Período...")
            await self._limpar_e_digitar(self.X_PERIODO, mes)

            await worker_sleep(2)

            # Clicar Iniciar
            console.print("[STEP] Clicar Iniciar...")
            await self._clicar(self.X_BTN_INICIAR)
            await worker_sleep(5)

            # Exportar
            console.print("[STEP] Exportar...")
            await self._clicar(self.X_EXPORTAR)
            await worker_sleep(2)

            console.print(
                "[STEP] Aguardando XLSX baixar + renomeando + enviando datalake..."
            )
            final_path = await self.rename_file(
                empresa=empresa,
                conta_tag=conta_tag,
                timeout=240,
            )

            console.print(f"[OK] Enviado e limpo local: {final_path.name}")
            arquivos.append(final_path.name)

            await worker_sleep(1)

        return arquivos


# ==========================================================
# FLUXO PRINCIPAL
# ==========================================================
async def extracao_lancamento_contabeis_sap(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando fluxo principal: extracao_lancamento_contabeis_sap")

    bot: Optional[ExtracaoLancamentoContabeis] = None
    try:
        console.print("[MAIN] Buscando config SAP_Faturamento...")
        cfg = await get_config_by_name("SAP_Faturamento")
        base_url = cfg.conConfiguracao.get("baseUrl")
        directory = cfg.conConfiguracao.get("directoryBucket")

        bot = ExtracaoLancamentoContabeis(
            task=task, base_url=base_url, directory=directory
        )

        ret = await bot.iniciar_sessao_sap()
        if not ret.sucesso:
            return ret

        arquivos = await bot.lancamento_contabeis()

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Login OK, exportação OK, envio datalake OK: {len(arquivos)} arquivos -> {', '.join(arquivos)}",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:
        console.print("[MAIN][ERRO] Exceção no fluxo principal.")
        console.print(traceback.format_exc())
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na automação SAP: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    finally:
        try:
            if bot and bot.driver:
                console.print("[MAIN] Encerrando navegador.")
                try:
                    bot.driver.quit()
                except Exception:
                    pass
                bot.driver = None

            await worker_sleep(0.5)
            console.print("[MAIN] Fim do processo.")
        except Exception:
            pass
