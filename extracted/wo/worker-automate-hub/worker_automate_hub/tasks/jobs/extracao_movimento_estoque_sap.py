# -*- coding: utf-8 -*-

import asyncio
import os
import io
import sys
import traceback
import time
import re
import subprocess
from pathlib import Path
from datetime import datetime, date
from typing import Optional, Union, List, Tuple, Dict, Any

from pydantic import BaseModel
from rich.console import Console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

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


# ============================================================
# CONSOLE
# ============================================================

console = Console()


# ============================================================
# DOWNLOADS
# ============================================================

DOWNLOADS_PATH = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
)

console.print(
    f"[INIT] Downloads dir: {DOWNLOADS_PATH}"
)


# ============================================================
# LOCALE
# ============================================================

try:
    locale.setlocale(
        locale.LC_TIME,
        "Portuguese_Brazil",
    )
except locale.Error:
    pass


# ============================================================
# STATUS DA VALIDAÇÃO DA GRADE
# ============================================================

GRADE_OK = "GRADE_OK"

GRADE_SEM_MOVIMENTACAO = "GRADE_SEM_MOVIMENTACAO"

GRADE_ERRO = "GRADE_ERRO"


# ============================================================
# LIMPEZA DOS DOWNLOADS
# ============================================================

def limpar_downloads(
    download_path: str,
    extensoes: tuple = (
        ".xlsx",
        ".pdf",
        ".crdownload",
    ),
) -> int:
    """
    Deleta arquivos dentro de download_path.

    Retorna:
        Quantidade de arquivos removidos.
    """

    pasta = Path(
        download_path
    )

    if not pasta.exists() or not pasta.is_dir():
        raise ValueError(
            f"DOWNLOAD_PATH inválido: {download_path}"
        )

    removidos = 0

    erros = []

    if extensoes is None:

        arquivos = [
            p
            for p in pasta.iterdir()
            if p.is_file()
        ]

    else:

        arquivos = []

        for ext in extensoes:

            arquivos.extend(
                [
                    p
                    for p in pasta.glob(
                        f"*{ext}"
                    )
                    if p.is_file()
                ]
            )

    for arq in arquivos:

        try:

            arq.unlink()

            removidos += 1

        except PermissionError:

            try:

                time.sleep(
                    0.3
                )

                arq.unlink()

                removidos += 1

            except Exception as e:

                erros.append(
                    (
                        str(arq),
                        str(e),
                    )
                )

        except Exception as e:

            erros.append(
                (
                    str(arq),
                    str(e),
                )
            )

    if erros:

        console.print(
            "[LIMPEZA][WARN] "
            "Alguns arquivos não puderam ser removidos:"
        )

        for path, err in erros[:10]:

            console.print(
                f" - {path}: {err}"
            )

    console.print(
        f"[LIMPEZA] Arquivos removidos dos Downloads: {removidos}"
    )

    return removidos


# ============================================================
# CONFIG ENTRADA
# ============================================================

class ConfigEntradaSAP(BaseModel):
    """
    Entrada do processo via fila:

    produtos:
        "2000011,2000025"

    centros:
        "2501,2502,2503,..."
    """

    produtos: str

    centros: str

    abrangencia: str = ""


# ============================================================
# AUTOMAÇÃO SAP
# ============================================================

class ExtracaoMovimentoEstoque:

    # ========================================================
    # XPATHS
    # ========================================================

    X_MATERIAL = (
        "//input[@title='Nº do material']"
    )

    X_CENTRO = (
        "//input[@title='Centro']"
    )

    X_PERIODO = (
        "//input[@title='Período contábil']"
    )

    X_ANO = (
        "//input[@title='Data de lançamento AAAA']"
    )

    X_ATUALIZAR = (
        "//*[@role='button' and @title=' (Shift+F1)']"
    )

    X_PRECO = (
        "(//div[@title='Expandir campos de seleção'])[2]"
    )

    X_VISAO = (
        "//input[@title="
        "'Exibição análise do preço de material: seleção de visões']"
    )

    X_SELECAO = (
        "//input[@value='Histórico de preços']"
    )

    X_BAIXAR = (
        "//div[@title='Planilha eletrônica... (Ctrl+Shift+F7)']"
    )

    X_EXPORTAR = (
        "//*[@role='button' and @title='Exportar']"
    )

    X_EXPORTAR_PARA = (
        "//*[@role='button' and @title='Exportar dados (Shift+F8)']"
    )

    X_OK = (
        "//div[@id='UpDownDialogChoose']"
    )

    # ========================================================
    # IFRAME
    # ========================================================

    X_APP_IFRAME = (
        "//iframe[contains("
        "@name,"
        "'application-ActualCosting-analyzeMaterialPrice-iframe'"
        ")]"
    )

    # ========================================================
    # GRADE SAP
    #
    # Estrutura observada no SAP WebGUI:
    #
    #   <table id="C132-mrss-cont-none-content">
    #       <tbody irowsfragmentlength="55">
    #           <tr id="C132-mrss-cont-none-Row-0" role="row">
    #               <td id="grid#C132#1,6">...</td>
    #
    # O prefixo Cxxx é dinâmico. Por isso a automação NÃO deve
    # depender de C130, C132 ou de uma coluna fixa.
    #
    # ========================================================

    X_TABELA_GRADE = (
        "//table["
        "contains(@id,'-mrss-cont-none-content') "
        "and .//tbody"
        "]"
    )

    X_LINHAS_GRADE = (
        ".//tbody/tr["
        "@role='row' "
        "and contains(@id,'-Row-')"
        "]"
    )

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: str,
        directory: Optional[str] = None,
    ):

        console.print(
            "============================================================"
        )

        console.print(
            "[STEP 0.1] Inicializando ExtracaoMovimentoEstoque"
        )

        console.print(
            "============================================================"
        )

        self.task = task

        hash_path = (
            "ActualCosting-analyzeMaterialPrice"
            "?sap-ui-tech-hint=GUI"
        )

        self.base_url = (
            base_url.split("#")[0]
            + "#"
            + hash_path
        )

        self.user = (
            CredentialsManager()
            .get_by_key(
                "SAP_USER_BI"
            )
        )

        self.password = (
            CredentialsManager()
            .get_by_key(
                "SAP_PASSWORD_BI"
            )
        )

        self.config_entrada = ConfigEntradaSAP(
            **(
                getattr(
                    task,
                    "configEntrada",
                    {},
                )
                or {}
            )
        )

        self.produtos: List[str] = [
            p.strip()
            for p
            in self.config_entrada.produtos.split(",")
            if p.strip()
        ]

        self.centros: List[str] = [
            c.strip()
            for c
            in self.config_entrada.centros.split(",")
            if c.strip()
        ]

        if not self.produtos:

            raise ValueError(
                "configEntrada.produtos está vazio."
            )

        if not self.centros:

            raise ValueError(
                "configEntrada.centros está vazio."
            )

        self.centro_ini = min(
            self.centros
        )

        self.centro_fim = max(
            self.centros
        )

        self.driver: Optional[
            webdriver.Chrome
        ] = None

        self.download_dir = (
            Path.home()
            / "Downloads"
        )

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.directory = directory

        # ====================================================
        # DATA/HORA
        # ====================================================

        self.data_python_now: Optional[
            datetime
        ] = None

        self.data_python_date: Optional[
            date
        ] = None

        self.data_vm_sistema: Optional[
            date
        ] = None

        self.date_now: str = ""

        self.mes: str = ""

        self.ano: str = ""

        self.mes_periodo: str = ""

        self._validar_data_python_vs_data_vm_ou_erro()

        console.print(
            f"[STEP 0.2] "
            f"user={'OK' if self.user else None} | "
            f"produtos={len(self.produtos)} | "
            f"centros={len(self.centros)} "
            f"({self.centro_ini}-{self.centro_fim}) | "
            f"abrangencia={self.config_entrada.abrangencia} | "
            f"downloads={self.download_dir} | "
            f"datalake_dir={self.directory}"
        )

    # ========================================================
    # DATA DA VM
    # ========================================================

    def _obter_data_vm_sistema(
        self,
    ) -> date:
        """
        Obtém a data diretamente do Windows da VM.
        """

        try:

            comando = [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-Date -Format 'yyyy-MM-dd'",
            ]

            result = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=10,
                shell=False,
            )

            if result.returncode != 0:

                raise RuntimeError(
                    f"PowerShell retornou código "
                    f"{result.returncode}. "
                    f"stderr={result.stderr}"
                )

            texto_data = (
                result.stdout
                or ""
            ).strip()

            if not texto_data:

                raise RuntimeError(
                    "PowerShell não retornou a data da VM."
                )

            return datetime.strptime(
                texto_data,
                "%Y-%m-%d",
            ).date()

        except Exception as e:

            raise RuntimeError(
                "Não foi possível obter a data da VM "
                f"via sistema operacional: {e}"
            )

    # ========================================================
    # ATUALIZA DATA
    # ========================================================

    def _atualizar_data_vm(
        self,
    ) -> None:

        self.data_python_now = (
            datetime.now()
        )

        self.data_python_date = (
            self.data_python_now.date()
        )

        self.date_now = (
            self.data_python_now.strftime(
                "%Y%m%d%H%M%S"
            )
        )

        self.mes = (
            self.data_python_now.strftime(
                "%m"
            )
        )

        self.ano = (
            self.data_python_now.strftime(
                "%Y"
            )
        )

        self.mes_periodo = str(
            int(self.mes)
        )

        console.print(
            f"[DATA PYTHON] "
            f"datetime.now(): "
            f"{self.data_python_now.strftime('%d/%m/%Y %H:%M:%S')} | "
            f"Data usada na comparação="
            f"{self.data_python_date.strftime('%d/%m/%Y')} | "
            f"Mês SAP={self.mes_periodo} | "
            f"Ano={self.ano}",
            style="bold cyan",
        )

    # ========================================================
    # VALIDA DATA PYTHON X VM
    # ========================================================

    def _validar_data_python_vs_data_vm_ou_erro(
        self,
    ) -> None:

        self._atualizar_data_vm()

        self.data_vm_sistema = (
            self._obter_data_vm_sistema()
        )

        console.print(
            f"[VALIDA DATA VM] "
            f"data_python="
            f"{self.data_python_date.strftime('%d/%m/%Y')} | "
            f"data_vm_sistema="
            f"{self.data_vm_sistema.strftime('%d/%m/%Y')}",
            style="bold yellow",
        )

        if (
            self.data_python_date
            != self.data_vm_sistema
        ):

            raise RuntimeError(
                "[VALIDA DATA VM][ERRO] "
                "Datas diferentes entre o datetime "
                "e a data da VM. "
                f"Python="
                f"{self.data_python_date.strftime('%d/%m/%Y')} | "
                f"VM="
                f"{self.data_vm_sistema.strftime('%d/%m/%Y')}"
            )

    # ========================================================
    # ENTRA IFRAME
    # ========================================================

    async def _entrar_no_iframe_app(
        self,
        timeout: int = 60,
    ) -> None:

        console.print(
            "[STEP] Alternando para o iframe do app SAP..."
        )

        wait = WebDriverWait(
            self.driver,
            timeout,
        )

        self.driver.switch_to.default_content()

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.X_APP_IFRAME,
                )
            )
        )

        wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.XPATH,
                    self.X_APP_IFRAME,
                )
            )
        )

        console.print(
            "[STEP] OK: dentro do iframe do app SAP."
        )

        await worker_sleep(
            0.2
        )

    # ========================================================
    # SAI IFRAME
    # ========================================================

    async def _sair_do_iframe(
        self,
    ) -> None:

        try:

            self.driver.switch_to.default_content()

        except Exception:

            pass

    # ========================================================
    # SCROLL
    # ========================================================

    async def _scroll_center(
        self,
        el,
    ) -> None:

        try:

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                el,
            )

        except Exception:

            pass

        await worker_sleep(
            0.15
        )

    # ========================================================
    # LIMPA E DIGITA
    # ========================================================

    async def _limpar_e_digitar(
        self,
        xpath: str,
        valor: str,
        timeout: int = 30,
    ) -> None:

        wait = WebDriverWait(
            self.driver,
            timeout,
        )

        for tentativa in range(
            1,
            4,
        ):

            try:

                el = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            xpath,
                        )
                    )
                )

                await self._scroll_center(
                    el
                )

                try:

                    el.click()

                except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
                ):

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    await self._scroll_center(
                        el
                    )

                    try:

                        self.driver.execute_script(
                            "arguments[0].click();",
                            el,
                        )

                    except Exception:

                        self.driver.execute_script(
                            "arguments[0].focus();",
                            el,
                        )

                await worker_sleep(
                    0.10
                )

                try:

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    el.send_keys(
                        Keys.CONTROL,
                        "a",
                    )

                    await worker_sleep(
                        0.05
                    )

                    el.send_keys(
                        Keys.DELETE
                    )

                    await worker_sleep(
                        0.10
                    )

                except (
                    StaleElementReferenceException,
                    TimeoutException,
                ):

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                try:

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    atual = (
                        el.get_attribute(
                            "value"
                        )
                        or ""
                    )

                    if atual.strip():

                        try:

                            el.clear()

                        except Exception:

                            self.driver.execute_script(
                                "arguments[0].value='';",
                                el,
                            )

                        await worker_sleep(
                            0.10
                        )

                except (
                    StaleElementReferenceException,
                    TimeoutException,
                ):

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                try:

                    el = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    await self._scroll_center(
                        el
                    )

                    el.click()

                except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
                ):

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].focus();",
                        el,
                    )

                await worker_sleep(
                    0.05
                )

                el = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            xpath,
                        )
                    )
                )

                el.send_keys(
                    str(valor)
                )

                await worker_sleep(
                    0.10
                )

                try:

                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    el.send_keys(
                        Keys.TAB
                    )

                except Exception:

                    pass

                await worker_sleep(
                    0.15
                )

                try:

                    el2 = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                xpath,
                            )
                        )
                    )

                    final = (
                        el2.get_attribute(
                            "value"
                        )
                        or ""
                    )

                    if str(valor) not in final:

                        self.driver.execute_script(
                            """
                            const el = arguments[0];
                            const v = arguments[1];

                            el.value = v;

                            el.dispatchEvent(
                                new Event(
                                    'input',
                                    {bubbles: true}
                                )
                            );

                            el.dispatchEvent(
                                new Event(
                                    'change',
                                    {bubbles: true}
                                )
                            );
                            """,
                            el2,
                            str(valor),
                        )

                        await worker_sleep(
                            0.15
                        )

                        try:

                            el2.send_keys(
                                Keys.TAB
                            )

                        except Exception:

                            pass

                        await worker_sleep(
                            0.10
                        )

                except (
                    StaleElementReferenceException,
                    TimeoutException,
                ):

                    raise

                return

            except StaleElementReferenceException:

                console.print(
                    f"[WARN] StaleElement em _limpar_e_digitar "
                    f"(tentativa {tentativa}/3) "
                    f"-> re-localizando..."
                )

                try:

                    await self._entrar_no_iframe_app(
                        timeout=20
                    )

                except Exception:

                    pass

                await worker_sleep(
                    0.6
                )

        raise StaleElementReferenceException(
            f"Elemento ficou stale após 3 tentativas: {xpath}"
        )

    # ========================================================
    # CLICAR
    # ========================================================

    async def _clicar(
        self,
        xpath: str,
        timeout: int = 60,
    ) -> None:

        wait = WebDriverWait(
            self.driver,
            timeout,
        )

        el = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    xpath,
                )
            )
        )

        await self._scroll_center(
            el
        )

        try:

            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        xpath,
                    )
                )
            ).click()

            return

        except (
            ElementClickInterceptedException,
            TimeoutException,
        ):

            self.driver.execute_script(
                "arguments[0].click();",
                el,
            )

            return

    # ========================================================
    # CONFIRMAR CAMPO SAP
    # ========================================================

    async def _confirmar_campo_sap(
        self,
        xpath: str,
        timeout: int = 20,
    ) -> None:
        """
        Confirma um campo do SAP com ENTER + TAB.

        O SAP WebGUI pode recriar o elemento no DOM depois do ENTER,
        causando StaleElementReferenceException. Por isso o elemento
        é sempre relocalizado e a confirmação é repetida até 3 vezes.
        """

        for tentativa in range(
            1,
            4,
        ):

            try:

                campo = WebDriverWait(
                    self.driver,
                    timeout,
                ).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            xpath,
                        )
                    )
                )

                campo.send_keys(
                    Keys.ENTER
                )

                # asyncio.sleep aqui evita poluir o console com os logs
                # internos do worker_sleep durante tentativas curtas.
                await asyncio.sleep(
                    0.2
                )

                # O ENTER pode provocar refresh parcial do SAP.
                # Relocaliza obrigatoriamente o elemento antes do TAB.
                campo = WebDriverWait(
                    self.driver,
                    timeout,
                ).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            xpath,
                        )
                    )
                )

                campo.send_keys(
                    Keys.TAB
                )

                await asyncio.sleep(
                    0.2
                )

                console.print(
                    f"[CONFIRMA CAMPO][OK] "
                    f"Campo confirmado na tentativa "
                    f"{tentativa}/3.",
                    style="bold green",
                )

                return

            except StaleElementReferenceException:

                console.print(
                    f"[CONFIRMA CAMPO][WARN] "
                    f"Elemento ficou stale na tentativa "
                    f"{tentativa}/3. "
                    f"Relocalizando...",
                    style="bold yellow",
                )

                await asyncio.sleep(
                    0.3
                )

                continue

            except TimeoutException as e:

                console.print(
                    f"[CONFIRMA CAMPO][WARN] "
                    f"Timeout na tentativa "
                    f"{tentativa}/3: {e}",
                    style="bold yellow",
                )

                await asyncio.sleep(
                    0.3
                )

                continue

            except Exception as e:

                console.print(
                    f"[CONFIRMA CAMPO][WARN] "
                    f"Erro na tentativa "
                    f"{tentativa}/3: "
                    f"{type(e).__name__}: {e}",
                    style="bold yellow",
                )

                await asyncio.sleep(
                    0.3
                )

                continue

        console.print(
            "[CONFIRMA CAMPO][WARN] "
            "Não foi possível confirmar o campo após 3 tentativas. "
            "O fluxo continuará e a validação posterior verificará "
            "se o valor foi aplicado corretamente.",
            style="bold yellow",
        )

    # ========================================================
    # DOWNLOAD XLSX
    # ========================================================

    async def _aguardar_xlsx_baixado(
        self,
        timeout: int = 240,
        quiet_window_sec: float = 1.2,
        inicio_download: Optional[float] = None,
        tolerancia_inicio_sec: float = 15.0,
    ) -> Path:
        """
        Aguarda o XLSX exportado pelo SAP aparecer no diretório real
        configurado para o Chrome.

        IMPORTANTE:
        O SAP pode exibir no rodapé um caminho lógico como Z:\\EXPORT_....xlsx,
        enquanto o Chrome efetivamente salva o arquivo em
        C:\\Users\\<usuario>\\Downloads.

        A referência de tempo é capturada ANTES do clique em OK.
        Isso evita a race condition em que o arquivo baixa muito rápido e,
        quando esta função começa, ele já existe na pasta e seria tratado
        como arquivo antigo.
        """

        pasta = Path(
            DOWNLOADS_PATH
        )

        inicio_espera = time.time()

        referencia_download = (
            inicio_download
            if inicio_download is not None
            else inicio_espera
        )

        limite_mtime = (
            referencia_download
            - tolerancia_inicio_sec
        )

        console.print(
            f"[DL] Aguardando XLSX em: "
            f"{pasta} "
            f"(timeout={timeout}s)"
        )

        console.print(
            f"[DL] Referência do download: "
            f"{datetime.fromtimestamp(referencia_download).strftime('%d/%m/%Y %H:%M:%S')} | "
            f"tolerância={tolerancia_inicio_sec:.1f}s",
            style="bold cyan",
        )

        candidato: Optional[
            Path
        ] = None

        # ====================================================
        # LOCALIZA ARQUIVO GERADO NESTA EXPORTAÇÃO
        # ====================================================

        while (
            time.time()
            - inicio_espera
            < timeout
        ):

            try:

                crdownloads = list(
                    pasta.glob(
                        "*.crdownload"
                    )
                )

                xlsx_files = []

                for arquivo in pasta.glob(
                    "*.xlsx"
                ):

                    try:

                        if (
                            arquivo.is_file()
                            and arquivo.stat().st_mtime
                            >= limite_mtime
                        ):

                            xlsx_files.append(
                                arquivo
                            )

                    except FileNotFoundError:
                        continue

                if xlsx_files:

                    candidato = max(
                        xlsx_files,
                        key=lambda p:
                        p.stat().st_mtime,
                    )

                    # Se ainda existir .crdownload, o Chrome pode estar
                    # concluindo a gravação. Mantemos o candidato, mas
                    # esperamos a finalização antes da estabilização.
                    if crdownloads:

                        await asyncio.sleep(
                            0.25
                        )

                        continue

                    break

            except Exception as e:

                console.print(
                    f"[DL][WARN] "
                    f"Erro ao procurar XLSX: "
                    f"{type(e).__name__}: {e}",
                    style="bold yellow",
                )

            await asyncio.sleep(
                0.25
            )

        if not candidato:

            raise TimeoutError(
                f"[DL] Nenhum .xlsx recente apareceu "
                f"em {timeout}s em {pasta}. "
                f"Referência="
                f"{datetime.fromtimestamp(referencia_download).strftime('%d/%m/%Y %H:%M:%S')}"
            )

        console.print(
            f"[DL] Candidato detectado: "
            f"{candidato.name}",
            style="bold green",
        )

        console.print(
            f"[DL] Caminho real detectado: "
            f"{candidato}",
            style="bold green",
        )

        # ====================================================
        # AGUARDA O TAMANHO DO ARQUIVO ESTABILIZAR
        # ====================================================

        last_size = -1

        stable_since: Optional[
            float
        ] = None

        while (
            time.time()
            - inicio_espera
            < timeout
        ):

            try:

                if list(
                    pasta.glob(
                        "*.crdownload"
                    )
                ):

                    stable_since = None

                    await asyncio.sleep(
                        0.25
                    )

                    continue

                size = (
                    candidato
                    .stat()
                    .st_size
                )

            except FileNotFoundError:

                # O Chrome pode trocar/renomear o arquivo no instante
                # da finalização. Reprocura apenas arquivos recentes.
                candidatos_recentes = []

                for arquivo in pasta.glob(
                    "*.xlsx"
                ):

                    try:

                        if (
                            arquivo.is_file()
                            and arquivo.stat().st_mtime
                            >= limite_mtime
                        ):

                            candidatos_recentes.append(
                                arquivo
                            )

                    except FileNotFoundError:
                        continue

                if not candidatos_recentes:

                    await asyncio.sleep(
                        0.25
                    )

                    continue

                candidato = max(
                    candidatos_recentes,
                    key=lambda p:
                    p.stat().st_mtime,
                )

                last_size = -1
                stable_since = None

                await asyncio.sleep(
                    0.25
                )

                continue

            if size != last_size:

                last_size = size

                stable_since = (
                    time.time()
                )

            else:

                if (
                    stable_since is not None
                    and (
                        time.time()
                        - stable_since
                    )
                    >= quiet_window_sec
                ):

                    console.print(
                        f"[DL][OK] Arquivo estabilizado | "
                        f"arquivo={candidato.name} | "
                        f"tamanho={size} bytes",
                        style="bold green",
                    )

                    return candidato

            await asyncio.sleep(
                0.25
            )

        raise TimeoutError(
            f"[DL] Arquivo encontrado, mas não estabilizou "
            f"dentro de {timeout}s: {candidato}"
        )

    # ========================================================
    # RENOMEAR + DATALAKE
    # ========================================================

    async def rename_file(
        self,
        produto: str,
        centro_tag: str,
        timeout: int = 240,
        inicio_download: Optional[float] = None,
    ) -> Path:

        console.print(
            "[RF] Iniciando renomeação + envio pro datalake."
        )

        try:

            self._validar_data_python_vs_data_vm_ou_erro()

            baixado = (
                await self._aguardar_xlsx_baixado(
                    timeout=timeout,
                    inicio_download=inicio_download,
                    tolerancia_inicio_sec=15.0,
                )
            )

            current_path = str(
                baixado
            )

            console.print(
                f"[RF] Arquivo baixado detectado: "
                f"{current_path}"
            )

            console.print(
                f"[RF] Existe? "
                f"{os.path.exists(current_path)}"
            )

            filename = (
                f"{centro_tag}-"
                f"{produto}-"
                f"{self.mes}-"
                f"{self.ano}-"
                f"{self.date_now}.xlsx"
            )

            final_path = os.path.join(
                DOWNLOADS_PATH,
                filename,
            )

            console.print(
                f"[RF] Novo filename: {filename}"
            )

            console.print(
                f"[RF] Movendo para: {final_path}"
            )

            os.rename(
                current_path,
                final_path,
            )

            console.print(
                f"[RF] Arquivo renomeado para "
                f"{final_path}."
            )

            with open(
                final_path,
                "rb",
            ) as file:

                file_bytes = io.BytesIO(
                    file.read()
                )

            await worker_sleep(
                1
            )

            if not self.directory:

                raise RuntimeError(
                    "self.directory não foi definido. "
                    "Passe pelo config SAP_Faturamento."
                )

            try:

                console.print(
                    f"[RF] directory: "
                    f"{self.directory}"
                )

                console.print(
                    f"[RF] file: "
                    f"{final_path}"
                )

                send_file_request = (
                    await send_file_to_datalake(
                        "qd_comercial/raw",
                        file_bytes,
                        filename,
                        "xlsx",
                    )
                )

                console.print(
                    f"[RF] Resposta "
                    f"send_file_to_datalake: "
                    f"{send_file_request}"
                )

            except Exception as e:

                console.print(
                    f"[RF][ERRO] "
                    f"Erro ao enviar o arquivo: {e}",
                    style="bold red",
                )

                console.print(
                    "[RF][ERRO] Traceback:"
                )

                console.print(
                    traceback.format_exc()
                )

                raise

            await worker_sleep(
                1
            )

            if (
                final_path
                and os.path.exists(
                    final_path
                )
            ):

                try:

                    os.remove(
                        final_path
                    )

                    console.print(
                        f"[RF] Arquivo deletado: "
                        f"{final_path}"
                    )

                except Exception as e:

                    raise RuntimeError(
                        f"Erro ao deletar o arquivo: {e}"
                    )

            return Path(
                final_path
            )

        except Exception as e:

            console.print(
                f"[RF][ERRO] {e}"
            )

            console.print(
                "[RF][ERRO] Traceback:"
            )

            console.print(
                traceback.format_exc()
            )

            raise

    # ========================================================
    # INICIAR SESSÃO
    # ========================================================

    async def iniciar_sessao_sap(
        self,
    ) -> RpaRetornoProcessoDTO:

        step = "INIT"

        console.print(
            "[STEP] Iniciando fluxo: "
            "INICIAR SESSÃO SAP"
        )

        try:

            step = "VALIDATE_CONFIG"

            self._validar_data_python_vs_data_vm_ou_erro()

            if (
                not self.user
                or not self.password
            ):

                msg = (
                    f"[{step}] "
                    f"Credenciais SAP inválidas."
                )

                console.print(
                    "[ERRO] " + msg
                )

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[
                        RpaTagDTO(
                            descricao=RpaTagEnum.Tecnico
                        )
                    ],
                )

            if not self.base_url:

                msg = (
                    f"[{step}] "
                    f"base_url não configurada."
                )

                console.print(
                    "[ERRO] " + msg
                )

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[
                        RpaTagDTO(
                            descricao=RpaTagEnum.Tecnico
                        )
                    ],
                )

            step = (
                "INIT_CHROMEDRIVER"
            )

            console.print(
                f"[STEP={step}] "
                f"Obtendo ChromeDriver..."
            )

            service = Service(
                ChromeDriverManager()
                .install()
            )

            step = (
                "INIT_WEBDRIVER"
            )

            console.print(
                f"[STEP={step}] "
                f"Inicializando Chrome..."
            )

            options = webdriver.ChromeOptions()

            prefs = {

                "download.default_directory":
                    str(
                        self.download_dir
                    ),

                "download.prompt_for_download":
                    False,

                "download.directory_upgrade":
                    True,

                "safebrowsing.enabled":
                    True,
            }

            options.add_experimental_option(
                "prefs",
                prefs,
            )

            self.driver = webdriver.Chrome(
                service=service,
                options=options,
            )

            self.driver.maximize_window()

            step = (
                "GET_BASE_URL"
            )

            console.print(
                f"[STEP={step}] "
                f"Acessando: {self.base_url}"
            )

            self.driver.get(
                self.base_url
            )

            await worker_sleep(
                2
            )

            step = "LOGIN"

            console.print(
                f"[STEP={step}] "
                f"Executando login..."
            )

            ok = (
                await self._login()
            )

            if not ok:

                msg = (
                    f"[{step}] "
                    f"Falha ao realizar login."
                )

                console.print(
                    "[ERRO] " + msg
                )

                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[
                        RpaTagDTO(
                            descricao=RpaTagEnum.Tecnico
                        )
                    ],
                )

            console.print(
                "[LOGIN] Login realizado com sucesso."
            )

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=(
                    "Sessão SAP iniciada com sucesso."
                ),
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        except Exception as e:

            tb = traceback.format_exc()

            msg = (
                f"Erro no fluxo "
                f"(etapa {step}): "
                f"{type(e).__name__}: "
                f"{e}"
            )

            console.print(
                "[ERRO] " + msg
            )

            console.print(
                tb
            )

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=(
                    msg
                    + "\n"
                    + tb
                ),
                status=RpaHistoricoStatusEnum.Falha,
                tags=[
                    RpaTagDTO(
                        descricao=RpaTagEnum.Tecnico
                    )
                ],
            )

    # ========================================================
    # LOGIN
    # ========================================================

    async def _login(
        self,
    ) -> bool:

        try:

            console.print(
                "[LOGIN] Aguardando campos de login..."
            )

            inputs = []

            for i in range(
                30
            ):

                inputs = self.driver.find_elements(
                    By.CLASS_NAME,
                    "loginInputField",
                )

                console.print(
                    f"[LOGIN] Tentativa "
                    f"{i + 1}/30 | "
                    f"campos: {len(inputs)}"
                )

                if len(inputs) >= 2:

                    break

                await worker_sleep(
                    1
                )

            if len(inputs) < 2:

                console.print(
                    "[LOGIN][ERRO] "
                    "Campos de login não encontrados."
                )

                return False

            inputs[0].clear()

            inputs[0].send_keys(
                self.user
            )

            console.print(
                "[LOGIN] Usuário preenchido."
            )

            await worker_sleep(
                0.5
            )

            inputs[1].clear()

            inputs[1].send_keys(
                self.password
            )

            console.print(
                "[LOGIN] Senha preenchida."
            )

            await worker_sleep(
                0.5
            )

            for i in range(
                10
            ):

                btn = self.driver.find_elements(
                    By.ID,
                    "LOGIN_SUBMIT_BLOCK",
                )

                console.print(
                    f"[LOGIN] Tentativa "
                    f"{i + 1}/10 | "
                    f"botão encontrado? "
                    f"{bool(btn)}"
                )

                if btn:

                    btn[0].click()

                    console.print(
                        "[LOGIN] Botão de login clicado."
                    )

                    break

                await worker_sleep(
                    1
                )

            await worker_sleep(
                3
            )

            console.print(
                "[LOGIN] Login finalizado."
            )

            return True

        except Exception:

            console.print(
                "[LOGIN][ERRO] "
                "Exceção durante login."
            )

            console.print(
                traceback.format_exc()
            )

            return False

    # ========================================================
    # LER VALOR DE CAMPO
    # ========================================================

    async def _ler_valor_campo(
        self,
        xpath: str,
        timeout: int = 20,
    ) -> str:

        campo = WebDriverWait(
            self.driver,
            timeout,
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    xpath,
                )
            )
        )

        valor = (
            campo.get_attribute(
                "value"
            )
            or campo.text
            or campo.get_attribute(
                "innerText"
            )
            or campo.get_attribute(
                "textContent"
            )
            or ""
        )

        return str(
            valor
        ).strip()

    # ========================================================
    # CONVERTE NÚMERO SAP
    # ========================================================

    def _converter_numero_sap(
        self,
        valor: str,
    ) -> Optional[float]:
        """
        Converte valores SAP.

        Exemplos:

            0        -> 0.0
            0,00     -> 0.0
            3,320    -> 3.32
            1.234,56 -> 1234.56
        """

        if valor is None:

            return None

        texto = str(
            valor
        ).strip()

        if texto == "":

            return None

        texto = texto.replace(
            " ",
            "",
        )

        # formato brasileiro/SAP
        if "," in texto:

            texto = (
                texto
                .replace(
                    ".",
                    "",
                )
                .replace(
                    ",",
                    ".",
                )
            )

        try:

            return float(
                texto
            )

        except (
            ValueError,
            TypeError,
        ):

            return None

    # ========================================================
    # NOVO:
    # LÊ A GRADE LINHA POR LINHA
    # ========================================================

    async def _obter_linhas_grade(
        self,
        timeout: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Lê as linhas visíveis da grade SAP sem depender de C130/C132
        nem de número fixo de coluna.

        A regra principal do processo usa somente a quantidade de linhas.
        Esta função fica disponível para diagnóstico/log da grade.
        """

        fim = time.time() + timeout

        while time.time() < fim:

            try:

                tabelas = self.driver.find_elements(
                    By.XPATH,
                    self.X_TABELA_GRADE,
                )

                for tabela in tabelas:

                    try:

                        linhas_html = tabela.find_elements(
                            By.XPATH,
                            self.X_LINHAS_GRADE,
                        )

                        linhas: List[Dict[str, Any]] = []

                        for posicao, linha_html in enumerate(
                            linhas_html,
                            start=1,
                        ):

                            try:

                                id_linha = (
                                    linha_html.get_attribute("id")
                                    or ""
                                ).strip()

                                textos_linha: List[str] = []

                                celulas = linha_html.find_elements(
                                    By.XPATH,
                                    ".//td",
                                )

                                for celula in celulas:

                                    try:

                                        texto = (
                                            celula.text
                                            or celula.get_attribute(
                                                "innerText"
                                            )
                                            or celula.get_attribute(
                                                "textContent"
                                            )
                                            or ""
                                        ).strip()

                                        if texto:
                                            textos_linha.append(texto)

                                    except StaleElementReferenceException:
                                        continue

                                data_linha = ""

                                for texto in textos_linha:

                                    match_data = re.search(
                                        r"\b\d{2}\.\d{2}\.\d{4}\b",
                                        texto,
                                    )

                                    if match_data:
                                        data_linha = match_data.group(0)
                                        break

                                linhas.append(
                                    {
                                        "linha": posicao,
                                        "id_linha": id_linha,
                                        "data": data_linha,
                                        "estoque_texto": "",
                                        "estoque": None,
                                        "textos": textos_linha,
                                    }
                                )

                            except StaleElementReferenceException:
                                continue

                        if linhas:

                            console.print(
                                "============================================================",
                                style="bold cyan",
                            )

                            console.print(
                                f"[VALIDA GRADE] "
                                f"Total de linhas visíveis encontradas: "
                                f"{len(linhas)}",
                                style="bold cyan",
                            )

                            console.print(
                                "============================================================",
                                style="bold cyan",
                            )

                            return linhas

                    except StaleElementReferenceException:
                        continue

            except StaleElementReferenceException:
                pass

            except Exception as e:

                console.print(
                    f"[VALIDA GRADE][WARN] "
                    f"Erro lendo linhas da grade: {e}",
                    style="bold yellow",
                )

            await worker_sleep(0.5)

        return []

    # ========================================================
    # CONTA AS LINHAS DA GRADE SEM LER O CONTEÚDO
    # ========================================================

    async def _obter_quantidade_linhas_grade(
        self,
        timeout: int = 10,
    ) -> int:
        """
        Obtém a quantidade de linhas da grade SAP sem depender de:

            - C130 / C132 / qualquer Cxxx fixo
            - coluna 6 / coluna 9 / qualquer coluna fixa
            - ID de célula específico

        Estratégia:
            1. Localiza tabelas cujo ID termina no padrão
               *-mrss-cont-none-content.
            2. Prioriza tabelas que realmente contenham células grid#C...
            3. Lê tbody[irowsfragmentlength], quando disponível.
            4. Usa a quantidade de <tr role="row"> como fallback.

        Regra do processo:
            1 linha  = sem movimentação
            >1 linha = houve movimentação
        """

        fim = time.time() + timeout
        tentativa = 0

        while time.time() < fim:

            tentativa += 1

            try:

                tabelas = self.driver.find_elements(
                    By.XPATH,
                    self.X_TABELA_GRADE,
                )

                if not tabelas:

                    console.print(
                        f"[AGUARDA GRADE] "
                        f"Tentativa {tentativa}: "
                        f"tabela da grade ainda não encontrada.",
                        style="bold yellow",
                    )

                    await worker_sleep(0.5)
                    continue

                candidatos = []

                for tabela in tabelas:

                    try:

                        id_tabela = (
                            tabela.get_attribute("id")
                            or ""
                        ).strip()

                        tbodys = tabela.find_elements(
                            By.XPATH,
                            ".//tbody",
                        )

                        if not tbodys:
                            continue

                        tbody = tbodys[0]

                        # Confirma que é uma grade de dados do SAP.
                        celulas_grid = tabela.find_elements(
                            By.XPATH,
                            ".//td[starts-with(@id,'grid#C')]",
                        )

                        linhas_html = tbody.find_elements(
                            By.XPATH,
                            "./tr[@role='row' and contains(@id,'-Row-')]",
                        )

                        qtd_atributo_texto = (
                            tbody.get_attribute(
                                "irowsfragmentlength"
                            )
                            or ""
                        ).strip()

                        qtd_atributo = (
                            int(qtd_atributo_texto)
                            if qtd_atributo_texto.isdigit()
                            else 0
                        )

                        qtd_tr = len(
                            {
                                (
                                    linha.get_attribute("id")
                                    or f"linha-sem-id-{idx}"
                                )
                                for idx, linha in enumerate(linhas_html)
                            }
                        )

                        # Não considera tabelas vazias/estruturais que não
                        # representam a grade de dados.
                        if not celulas_grid and qtd_atributo <= 0 and qtd_tr <= 0:
                            continue

                        quantidade = max(
                            qtd_atributo,
                            qtd_tr,
                        )

                        candidatos.append(
                            {
                                "id": id_tabela,
                                "quantidade": quantidade,
                                "qtd_atributo": qtd_atributo,
                                "qtd_tr": qtd_tr,
                                "tem_celulas_grid": bool(celulas_grid),
                            }
                        )

                    except StaleElementReferenceException:
                        continue

                if candidatos:

                    # Prioriza a tabela que contém células grid#C...
                    # e, entre elas, a de maior quantidade de linhas.
                    candidatos.sort(
                        key=lambda item: (
                            item["tem_celulas_grid"],
                            item["quantidade"],
                        ),
                        reverse=True,
                    )

                    escolhido = candidatos[0]

                    console.print(
                        f"[AGUARDA GRADE][DEBUG] "
                        f"Tabela={escolhido['id']} | "
                        f"irowsfragmentlength="
                        f"{escolhido['qtd_atributo']} | "
                        f"tr_visiveis={escolhido['qtd_tr']} | "
                        f"celulas_grid="
                        f"{escolhido['tem_celulas_grid']}",
                        style="bold cyan",
                    )

                    if escolhido["quantidade"] > 0:

                        console.print(
                            f"[AGUARDA GRADE][OK] "
                            f"Quantidade detectada: "
                            f"{escolhido['quantidade']}",
                            style="bold green",
                        )

                        return escolhido["quantidade"]

                console.print(
                    f"[AGUARDA GRADE] "
                    f"Tentativa {tentativa}: "
                    f"estrutura encontrada, mas nenhuma "
                    f"linha válida foi identificada ainda.",
                    style="bold yellow",
                )

            except StaleElementReferenceException:

                console.print(
                    "[AGUARDA GRADE][WARN] "
                    "DOM da grade foi atualizado durante a leitura. "
                    "Tentando novamente...",
                    style="bold yellow",
                )

            except Exception as e:

                console.print(
                    f"[AGUARDA GRADE][WARN] "
                    f"Erro ao contar as linhas da grade: "
                    f"{type(e).__name__}: {e}",
                    style="bold yellow",
                )

            await worker_sleep(0.5)

        return 0

    # ========================================================
    # AGUARDA A QUANTIDADE DE LINHAS ESTABILIZAR
    # ========================================================

    async def _aguardar_grade_estavel(
        self,
        timeout: int = 30,
        leituras_estaveis_necessarias: int = 2,
        intervalo_segundos: float = 1.0,
    ) -> int:
        """
        Aguarda a quantidade de linhas da grade parar de mudar.

        Não lê data, estoque ou demais células durante a estabilização.
        Isso evita o problema anterior, em que uma grade grande demorava
        tanto para ser percorrida que o timeout de 30 segundos expirava
        antes da terceira leitura.

        Se o timeout for atingido, mas já existir uma leitura válida,
        utiliza a última quantidade encontrada em vez de descartar a grade.
        """

        inicio = time.time()
        quantidade_anterior: Optional[int] = None
        quantidade_estavel = 0
        ultima_quantidade = 0
        numero_leitura = 0

        console.print(
            "[AGUARDA GRADE] "
            "Aguardando a quantidade de linhas estabilizar...",
            style="bold cyan",
        )

        while time.time() - inicio < timeout:

            numero_leitura += 1

            tempo_restante = max(
                1,
                int(timeout - (time.time() - inicio)),
            )

            quantidade_atual = (
                await self._obter_quantidade_linhas_grade(
                    timeout=min(5, tempo_restante)
                )
            )

            if quantidade_atual <= 0:

                quantidade_anterior = None
                quantidade_estavel = 0

                console.print(
                    f"[AGUARDA GRADE] "
                    f"Leitura {numero_leitura}: "
                    "grade ainda não disponível.",
                    style="bold yellow",
                )

                await worker_sleep(
                    intervalo_segundos
                )

                continue

            ultima_quantidade = quantidade_atual

            if quantidade_atual == quantidade_anterior:
                quantidade_estavel += 1
            else:
                quantidade_anterior = quantidade_atual
                quantidade_estavel = 1

            console.print(
                f"[AGUARDA GRADE] "
                f"Leitura {numero_leitura}: "
                f"linhas={quantidade_atual} | "
                f"estabilidade={quantidade_estavel}/"
                f"{leituras_estaveis_necessarias}",
                style="bold cyan",
            )

            if (
                quantidade_estavel
                >= leituras_estaveis_necessarias
            ):

                console.print(
                    "============================================================",
                    style="bold green",
                )

                console.print(
                    "[AGUARDA GRADE][OK] "
                    "Quantidade de linhas estabilizada. "
                    f"Linhas={quantidade_atual} | "
                    f"Leituras consecutivas iguais="
                    f"{quantidade_estavel}",
                    style="bold green",
                )

                console.print(
                    "============================================================",
                    style="bold green",
                )

                return quantidade_atual

            await worker_sleep(
                intervalo_segundos
            )

        # Se já houve uma leitura válida, não transforma em erro apenas
        # porque o timeout terminou antes de completar as leituras estáveis.
        if ultima_quantidade > 0:

            console.print(
                "============================================================",
                style="bold yellow",
            )

            console.print(
                "[AGUARDA GRADE][WARN] "
                f"Timeout de {timeout}s atingido, mas a grade possui "
                f"{ultima_quantidade} linha(s). "
                "Utilizando a última quantidade válida.",
                style="bold yellow",
            )

            console.print(
                "============================================================",
                style="bold yellow",
            )

            return ultima_quantidade

        console.print(
            "============================================================",
            style="bold red",
        )

        console.print(
            "[AGUARDA GRADE][ERRO] "
            "Nenhuma linha foi encontrada na grade.",
            style="bold red",
        )

        console.print(
            "============================================================",
            style="bold red",
        )

        return 0

    # ========================================================
    # VALIDA GRADE PELA QUANTIDADE DE LINHAS
    #
    # REGRA DEFINITIVA:
    #
    # 1 LINHA:
    #   = SEM MOVIMENTAÇÃO / SUCESSO
    #
    # MAIS DE 1 LINHA:
    #   = EXISTE MOVIMENTAÇÃO / EXPORTA
    #
    # NÃO HÁ VALIDAÇÃO DE DATA OU ESTOQUE NAS LINHAS DA GRADE.
    # ========================================================

    async def _validar_grade_por_quantidade_linhas(
        self,
        timeout: int = 30,
    ) -> str:

        total_linhas = (
            await self._aguardar_grade_estavel(
                timeout=timeout,
                leituras_estaveis_necessarias=2,
                intervalo_segundos=1.0,
            )
        )

        if total_linhas <= 0:

            console.print(
                "[VALIDA GRADE][ERRO] "
                "Nenhuma linha válida foi encontrada na grade.",
                style="bold red",
            )

            return GRADE_ERRO

        console.print(
            "============================================================",
            style="bold cyan",
        )

        console.print(
            f"[VALIDA GRADE] "
            f"Quantidade de linhas da grade: {total_linhas}",
            style="bold cyan",
        )

        # ====================================================
        # UMA LINHA = SEM MOVIMENTAÇÃO
        # ====================================================

        if total_linhas == 1:

            console.print(
                "[VALIDA GRADE][SEM MOVIMENTAÇÃO] "
                "A grade possui somente 1 linha.",
                style="bold green",
            )

            console.print(
                "[VALIDA GRADE][SEM MOVIMENTAÇÃO] "
                "Item considerado SUCESSO - sem movimentação.",
                style="bold green",
            )

            console.print(
                "============================================================",
                style="bold green",
            )

            return GRADE_SEM_MOVIMENTACAO

        # ====================================================
        # MAIS DE UMA LINHA = TEVE MOVIMENTAÇÃO
        # ====================================================

        console.print(
            "[VALIDA GRADE][COM MOVIMENTAÇÃO] "
            f"A grade possui {total_linhas} linhas.",
            style="bold green",
        )

        console.print(
            "[VALIDA GRADE][COM MOVIMENTAÇÃO] "
            "Item possui movimentação e seguirá para exportação.",
            style="bold green",
        )

        console.print(
            "============================================================",
            style="bold green",
        )

        return GRADE_OK

    # ========================================================
    # PREENCHE PERÍODO / ANO / ATUALIZA / VALIDA GRADE
    # ========================================================

    async def _preencher_periodo_ano_atualizar_e_validar_grade(
        self,
        max_tentativas: int = 3,
    ) -> str:

        for tentativa in range(
            1,
            max_tentativas + 1,
        ):

            console.print(
                "============================================================"
            )

            console.print(
                f"[VALIDA MES/ANO GRADE] "
                f"Tentativa "
                f"{tentativa}/"
                f"{max_tentativas}",
                style="bold cyan",
            )

            console.print(
                "============================================================"
            )

            try:

                self._validar_data_python_vs_data_vm_ou_erro()

                mes_periodo = (
                    self.mes_periodo
                )

                ano_atual = (
                    self.ano
                )

                await self._entrar_no_iframe_app(
                    timeout=30
                )

                console.print(
                    f"[STEP] "
                    f"Preenchendo Período atual da VM: "
                    f"{mes_periodo}"
                )

                await self._limpar_e_digitar(
                    self.X_PERIODO,
                    mes_periodo,
                )

                await self._confirmar_campo_sap(
                    self.X_PERIODO
                )

                console.print(
                    f"[STEP] "
                    f"Preenchendo Ano atual da VM: "
                    f"{ano_atual}"
                )

                await self._limpar_e_digitar(
                    self.X_ANO,
                    ano_atual,
                )

                await self._confirmar_campo_sap(
                    self.X_ANO
                )

                await worker_sleep(
                    1
                )

                valor_periodo = (
                    await self._ler_valor_campo(
                        self.X_PERIODO
                    )
                )

                valor_ano = (
                    await self._ler_valor_campo(
                        self.X_ANO
                    )
                )

                console.print(
                    f"[CHECK CAMPOS] "
                    f"Período tela='{valor_periodo}' | "
                    f"Ano tela='{valor_ano}'",
                    style="bold yellow",
                )

                periodo_ok = (
                    str(valor_periodo).strip()
                    == str(mes_periodo).strip()
                )

                ano_ok = (
                    str(valor_ano).strip()
                    == str(ano_atual).strip()
                )

                if not periodo_ok:

                    console.print(
                        f"[VALIDA CAMPOS][WARN] "
                        f"Período no campo diferente. "
                        f"Esperado={mes_periodo} | "
                        f"Tela={valor_periodo}",
                        style="bold red",
                    )

                if not ano_ok:

                    console.print(
                        f"[VALIDA CAMPOS][WARN] "
                        f"Ano no campo diferente. "
                        f"Esperado={ano_atual} | "
                        f"Tela={valor_ano}",
                        style="bold red",
                    )

                # Não atualiza o SAP com filtro divergente.
                # Volta para o início da tentativa e preenche novamente.
                if (
                    not periodo_ok
                    or not ano_ok
                ):

                    console.print(
                        "[VALIDA CAMPOS][WARN] "
                        "Período/Ano não foram confirmados na tela. "
                        "A atualização não será executada nesta tentativa.",
                        style="bold yellow",
                    )

                    await worker_sleep(
                        1
                    )

                    continue

                console.print(
                    "[VALIDA CAMPOS][OK] "
                    f"Período={mes_periodo} | Ano={ano_atual}",
                    style="bold green",
                )

                console.print(
                    "[STEP] Clicar atualizar:"
                )

                await self._clicar(
                    self.X_ATUALIZAR
                )

                # Espera mínima apenas para o SAP iniciar o refresh.
                # A confirmação real de carregamento é feita por
                # _aguardar_grade_estavel().
                await worker_sleep(
                    2
                )

                resultado_grade = (
                    await self._validar_grade_por_quantidade_linhas(
                        timeout=30
                    )
                )

                # ============================================
                # GRADE OK
                # ============================================

                if (
                    resultado_grade
                    == GRADE_OK
                ):

                    return GRADE_OK

                # ============================================
                # SEM MOVIMENTAÇÃO
                #
                # NÃO PRECISA TENTAR 3 VEZES
                # ============================================

                if (
                    resultado_grade
                    == GRADE_SEM_MOVIMENTACAO
                ):

                    return (
                        GRADE_SEM_MOVIMENTACAO
                    )

                # ============================================
                # GRADE INVÁLIDA / NÃO ESTABILIZOU
                #
                # TENTA NOVAMENTE
                # ============================================

                console.print(
                    "[VALIDA GRADE][WARN] "
                    "Não foi possível confirmar a quantidade "
                    "de linhas da grade. "
                    "Tentando atualizar novamente.",
                    style="bold red",
                )

                await worker_sleep(
                    2
                )

            except StaleElementReferenceException:

                console.print(
                    f"[VALIDA MES/ANO GRADE][WARN] "
                    f"StaleElement na tentativa "
                    f"{tentativa}/"
                    f"{max_tentativas}. "
                    f"Tentando novamente...",
                    style="bold yellow",
                )

                try:

                    await self._entrar_no_iframe_app(
                        timeout=20
                    )

                except Exception:

                    pass

                await worker_sleep(
                    2
                )

            except Exception as e:

                console.print(
                    f"[VALIDA MES/ANO GRADE][WARN] "
                    f"Erro na tentativa "
                    f"{tentativa}/"
                    f"{max_tentativas}: "
                    f"{e}",
                    style="bold red",
                )

                console.print(
                    traceback.format_exc()
                )

                if (
                    "[VALIDA DATA VM][ERRO]"
                    in str(e)
                ):

                    raise

                await worker_sleep(
                    2
                )

        console.print(
            "[VALIDA GRADE][ERRO] "
            "Não foi possível validar a quantidade de linhas "
            f"da grade após {max_tentativas} tentativas.",
            style="bold red",
        )

        return GRADE_ERRO

    # ========================================================
    # LISTA MATERIAL
    # ========================================================

    async def lista_material(
        self,
    ) -> Tuple[
        List[str],
        List[str],
        List[str],
    ]:

        arquivos: List[
            str
        ] = []

        falhas: List[
            str
        ] = []

        sem_movimentacao: List[
            str
        ] = []

        centro_range_tag = (
            f"{self.centro_ini}-"
            f"{self.centro_fim}"
        )

        total_exec = (
            len(self.produtos)
            * len(self.centros)
        )

        contador = 0

        primeira_vez = False

        self._validar_data_python_vs_data_vm_ou_erro()

        console.print(
            f"[CONFIG] "
            f"Mês atual da VM calculado para SAP: "
            f"{self.mes_periodo}"
        )

        console.print(
            f"[CONFIG] "
            f"Ano atual da VM calculado para SAP: "
            f"{self.ano}"
        )

        for idx_prod, produto in enumerate(
            self.produtos,
            start=1,
        ):

            console.print(
                "============================================================"
            )

            console.print(
                f"[LOOP] Produto "
                f"({idx_prod}/"
                f"{len(self.produtos)}): "
                f"{produto} | "
                f"Centros: "
                f"{centro_range_tag}"
            )

            console.print(
                "============================================================"
            )

            for idx_ctr, centro in enumerate(
                self.centros,
                start=1,
            ):

                self._validar_data_python_vs_data_vm_ou_erro()

                # ============================================
                # LIMPA DOWNLOADS ANTES DE CADA ITEM
                # ============================================

                limpar_downloads(
                    DOWNLOADS_PATH
                )

                contador += 1

                console.print(
                    "============================================================"
                )

                console.print(
                    f"[LOOP] "
                    f"({contador}/"
                    f"{total_exec}) "
                    f"Produto: "
                    f"{produto} | "
                    f"Centro: "
                    f"{centro}"
                )

                console.print(
                    "============================================================"
                )

                try:

                    await self._entrar_no_iframe_app(
                        timeout=60
                    )

                    # ========================================
                    # MATERIAL
                    # ========================================

                    console.print(
                        f"[STEP] Material: {produto}"
                    )

                    await self._limpar_e_digitar(
                        self.X_MATERIAL,
                        produto,
                    )

                    # ========================================
                    # CENTRO
                    # ========================================

                    console.print(
                        f"[STEP] Centro: {centro}"
                    )

                    await self._limpar_e_digitar(
                        self.X_CENTRO,
                        centro,
                    )

                    # ========================================
                    # PRIMEIRA VEZ
                    # ========================================

                    if not primeira_vez:

                        console.print(
                            "[STEP] Clicar preço"
                        )

                        await self._clicar(
                            self.X_PRECO
                        )

                        primeira_vez = True

                        await worker_sleep(
                            5
                        )

                        console.print(
                            "[STEP] Selecionar Visão:"
                        )

                        await self._clicar(
                            self.X_VISAO
                        )

                        await worker_sleep(
                            2
                        )

                        campo = WebDriverWait(
                            self.driver,
                            20,
                        ).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    self.X_VISAO,
                                )
                            )
                        )

                        campo.send_keys(
                            Keys.ARROW_DOWN
                        )

                        time.sleep(
                            0.2
                        )

                        campo.send_keys(
                            Keys.ENTER
                        )

                    await worker_sleep(
                        2
                    )

                    # ========================================
                    # VALIDA GRADE
                    # ========================================

                    resultado_grade = (
                        await self
                        ._preencher_periodo_ano_atualizar_e_validar_grade(
                            max_tentativas=3,
                        )
                    )

                    # ========================================
                    # SEM MOVIMENTAÇÃO
                    #
                    # REGRA: GRADE COM APENAS 1 LINHA
                    # ========================================

                    if (
                        resultado_grade
                        == GRADE_SEM_MOVIMENTACAO
                    ):

                        msg_sem_mov = (
                            f"Produto={produto} | "
                            f"Centro={centro} | "
                            f"Sucesso: sem movimentação de estoque "
                            f"(grade com apenas uma linha)"
                        )

                        console.print(
                            "============================================================",
                            style="bold green",
                        )

                        console.print(
                            f"[ITEM][SUCESSO SEM MOVIMENTAÇÃO] "
                            f"{msg_sem_mov}",
                            style="bold green",
                        )

                        console.print(
                            "[ITEM][SUCESSO SEM MOVIMENTAÇÃO] "
                            "Nenhum arquivo será exportado "
                            "para este produto/centro.",
                            style="bold green",
                        )

                        console.print(
                            "============================================================",
                            style="bold green",
                        )

                        sem_movimentacao.append(
                            msg_sem_mov
                        )

                        await self._sair_do_iframe()

                        await worker_sleep(
                            1
                        )

                        continue

                    # ========================================
                    # FALHA NA VALIDAÇÃO DA GRADE
                    # ========================================

                    if (
                        resultado_grade
                        != GRADE_OK
                    ):

                        msg_falha = (
                            f"Produto={produto} | "
                            f"Centro={centro} | "
                            f"Erro: não foi possível validar "
                            f"a quantidade de linhas da grade "
                            f"antes da exportação."
                        )

                        console.print(
                            f"[VALIDA GRADE][FALHA ITEM] "
                            f"{msg_falha}",
                            style="bold red",
                        )

                        falhas.append(
                            msg_falha
                        )

                        await self._sair_do_iframe()

                        await worker_sleep(
                            1
                        )

                        continue

                    # ========================================
                    # GRADE OK
                    # EXPORTAÇÃO
                    # ========================================

                    console.print(
                        "[STEP] Clicando em Exportar"
                    )

                    await self._clicar(
                        self.X_EXPORTAR
                    )

                    await worker_sleep(
                        2
                    )

                    ActionChains(
                        self.driver
                    ).send_keys(
                        Keys.ENTER
                    ).perform()

                    console.print(
                        "[STEP] Exportar para:"
                    )

                    await self._clicar(
                        self.X_EXPORTAR_PARA
                    )

                    console.print(
                        "[STEP] Exportar dados "
                        "clicado com sucesso."
                    )

                    await worker_sleep(
                        0.8
                    )

                    console.print(
                        "[STEP] Clicando em OK"
                    )

                    # Captura o instante ANTES do clique que dispara/conclui
                    # a exportação. Assim, mesmo que o XLSX seja criado muito
                    # rápido, ele ainda será reconhecido como arquivo desta
                    # execução quando _aguardar_xlsx_baixado() iniciar.
                    inicio_download = (
                        time.time()
                    )

                    console.print(
                        f"[DL] Início da janela de download registrado: "
                        f"{datetime.fromtimestamp(inicio_download).strftime('%d/%m/%Y %H:%M:%S')}",
                        style="bold cyan",
                    )

                    await self._clicar(
                        self.X_OK
                    )

                    console.print(
                        "[STEP] OK clicado com sucesso."
                    )

                    console.print(
                        "[STEP] Aguardando XLSX baixar + "
                        "renomeando + enviando datalake..."
                    )

                    final_path = (
                        await self.rename_file(
                            produto=produto,
                            centro_tag=centro,
                            timeout=240,
                            inicio_download=inicio_download,
                        )
                    )

                    console.print(
                        f"[STEP] Enviado e limpo local: "
                        f"{final_path.name}"
                    )

                    arquivos.append(
                        final_path.name
                    )

                    await self._sair_do_iframe()

                    await worker_sleep(
                        1
                    )

                except Exception as e:

                    msg_falha = (
                        f"Produto={produto} | "
                        f"Centro={centro} | "
                        f"Erro durante processamento do item: "
                        f"{type(e).__name__}: {e}"
                    )

                    console.print(
                        f"[ITEM][ERRO] "
                        f"{msg_falha}",
                        style="bold red",
                    )

                    console.print(
                        traceback.format_exc()
                    )

                    if (
                        "[VALIDA DATA VM][ERRO]"
                        in str(e)
                    ):

                        raise

                    falhas.append(
                        msg_falha
                    )

                    try:

                        await self._sair_do_iframe()

                    except Exception:

                        pass

                    await worker_sleep(
                        1
                    )

                    continue

        return (
            arquivos,
            falhas,
            sem_movimentacao,
        )


# ============================================================
# FLUXO PRINCIPAL
# ============================================================

async def extracao_movimento_estoque_sap(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:

    console.print(
        "============================================================"
    )

    console.print(
        "[MAIN] Iniciando fluxo principal: "
        "extracao_movimento_estoque_sap"
    )

    console.print(
        "============================================================"
    )

    bot: Optional[
        ExtracaoMovimentoEstoque
    ] = None

    try:

        console.print(
            "[MAIN] Buscando config SAP_Faturamento..."
        )

        cfg = await get_config_by_name(
            "SAP_Faturamento"
        )

        base_url = (
            cfg.conConfiguracao
            .get(
                "baseUrl"
            )
        )

        directory = (
            cfg.conConfiguracao
            .get(
                "directoryBucket"
            )
        )

        bot = ExtracaoMovimentoEstoque(
            task=task,
            base_url=base_url,
            directory=directory,
        )

        ret = (
            await bot.iniciar_sessao_sap()
        )

        if not ret.sucesso:

            return ret

        (
            arquivos,
            falhas,
            sem_movimentacao,
        ) = (
            await bot.lista_material()
        )

        # ====================================================
        # TEM FALHA REAL
        # ====================================================

        if falhas:

            retorno = (
                f"Processo finalizado com falhas "
                f"em {len(falhas)} item(ns). "
                f"Arquivos exportados/enviados "
                f"com sucesso: {len(arquivos)}. "
                f"Itens sem movimentação de estoque: "
                f"{len(sem_movimentacao)}"
            )

            if arquivos:

                retorno += (
                    " | Arquivos: "
                    + ", ".join(
                        arquivos
                    )
                )

            if sem_movimentacao:

                retorno += (
                    " | Sem movimentação: "
                    + " ; ".join(
                        sem_movimentacao
                    )
                )

            retorno += (
                " | Falhas: "
                + " ; ".join(
                    falhas
                )
            )

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[
                    RpaTagDTO(
                        descricao=RpaTagEnum.Tecnico
                    )
                ],
            )

        # ====================================================
        # SUCESSO
        # ====================================================

        retorno_sucesso = (
            f"Processo finalizado com sucesso. "
            f"Arquivos exportados/enviados: "
            f"{len(arquivos)}. "
            f"Itens sem movimentação de estoque: "
            f"{len(sem_movimentacao)}"
        )

        if arquivos:

            retorno_sucesso += (
                " | Arquivos: "
                + ", ".join(
                    arquivos
                )
            )

        if sem_movimentacao:

            retorno_sucesso += (
                " | Sem movimentação de estoque: "
                + " ; ".join(
                    sem_movimentacao
                )
            )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=retorno_sucesso,
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:

        console.print(
            "[MAIN][ERRO] "
            "Exceção no fluxo principal."
        )

        console.print(
            traceback.format_exc()
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=(
                f"Erro na automação SAP: {ex}"
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
                    "[MAIN] Encerrando navegador."
                )

                try:

                    bot.driver.quit()

                except Exception:

                    pass

                bot.driver = None

            await worker_sleep(
                0.5
            )

            console.print(
                "[MAIN] Fim do processo."
            )

        except Exception:

            pass
