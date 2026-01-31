# -*- coding: utf-8 -*-
import asyncio
import os
import io
import sys
import traceback
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Union, List

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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from worker_automate_hub.api.datalake_service import send_file_to_datalake
from selenium.webdriver.common.keys import Keys
from worker_automate_hub.utils.credentials_manager import CredentialsManager
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.utils.util import worker_sleep

console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
console.print(f"[INIT] Downloads dir: {DOWNLOADS_PATH}")

now = datetime.now()
date_now = now.strftime("%Y%m%d%H%M%S")
mes = now.strftime("%m")
ano = now.strftime("%Y")


def limpar_downloads(download_path: str, extensoes: tuple = (".xlsx", ".pdf", ".crdownload")) -> int:
    """
    Deleta arquivos dentro de download_path (somente arquivos, não apaga pastas).
    Retorna quantos arquivos foram removidos.

    - extensoes: quais extensões remover (use None para remover tudo)
    """
    pasta = Path(download_path)
    if not pasta.exists() or not pasta.is_dir():
        raise ValueError(f"DOWNLOAD_PATH inválido: {download_path}")

    removidos = 0
    erros = []

    # monta lista de arquivos
    if extensoes is None:
        arquivos = [p for p in pasta.iterdir() if p.is_file()]
    else:
        arquivos = []
        for ext in extensoes:
            arquivos.extend([p for p in pasta.glob(f"*{ext}") if p.is_file()])

    for arq in arquivos:
        try:
            # tenta remover modo normal
            arq.unlink()
            removidos += 1
        except PermissionError:
            # arquivo ainda em uso; tenta aguardar um pouco e remover de novo
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
# CONFIG DE ENTRADA (AJUSTADA)
# ==========================
class ConfigEntradaSAP(BaseModel):
    """
    Entrada do processo via fila:
      - produtos: "2000011,2000025"
      - centros:  "2501,2502,2503,..."
    """
    produtos: str
    centros: str
    abrangencia: str = ""


# ==========================
# CLASSE PRINCIPAL
# ==========================
class ExtracaoMovimentoEstoque:
    # ==========
    # XPATHs
    # ==========
    X_MATERIAL     = "//input[@title='Nº do material']"
    X_CENTRO       = "//input[@title='Centro']"
    X_PERIODO      = "//input[@title='Período contábil']"
    X_ANO          = "//input[@title='Data de lançamento AAAA']"
    X_ATUALIZAR    = "//*[@role='button' and @title='Atualizar (Shift+F1)']"
    X_PRECO        = "(//div[@title='Expandir campos de seleção'])[2]"
    X_VISAO        = "//input[@title='Exibição análise do preço de material: seleção de visões']"
    X_SELECAO      = "//input[@value='Histórico de preços']"
    X_BAIXAR       = "//div[@title='Planilha eletrônica... (Ctrl+Shift+F7)']"
    X_EXPORTAR     = "//*[@role='button' and @title='Exportar']"
    X_EXPORTAR_PARA = "//*[@role='button' and @title='Exportar dados (Shift+F8)']"
    X_OK           = "//div[@id='UpDownDialogChoose']"

    # IFRAME
    X_APP_IFRAME   = "//iframe[contains(@name,'application-ActualCosting-analyzeMaterialPrice-iframe')]"

 
    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: str,
        directory: Optional[str] = None,
    ):
        console.print("[STEP 0.1] Inicializando ExtracaoMovimentoEstoque")

        self.task = task

        # Base URL
        hash_path = "ActualCosting-analyzeMaterialPrice?sap-ui-tech-hint=GUI"

        # Remove qualquer fragmento (#...) anterior e adiciona o novo
        self.base_url = base_url.split("#")[0] + "#" + hash_path

        # Credenciais SAP
        self.user = CredentialsManager().get_by_key("SAP_USER_BI")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_BI")

        # Valida configEntrada (AJUSTADA)
        self.config_entrada = ConfigEntradaSAP(
            **(getattr(task, "configEntrada", {}) or {})
        )

        # Parse produtos/centros
        self.produtos: List[str] = [p.strip() for p in self.config_entrada.produtos.split(",") if p.strip()]
        self.centros: List[str] = [c.strip() for c in self.config_entrada.centros.split(",") if c.strip()]

        if not self.produtos:
            raise ValueError("configEntrada.produtos está vazio.")
        if not self.centros:
            raise ValueError("configEntrada.centros está vazio.")

        # centro como intervalo (min/max) — mantém seu log/visual
        self.centro_ini = min(self.centros)
        self.centro_fim = max(self.centros)

        self.driver: Optional[webdriver.Chrome] = None

        # Pasta padrão de downloads (Windows)
        self.download_dir = Path.home() / "Downloads"
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # diretório do datalake
        self.directory = directory

        console.print(
            f"[STEP 0.2] user={'OK' if self.user else None} | "
            f"produtos={len(self.produtos)} | "
            f"centros={len(self.centros)} ({self.centro_ini}-{self.centro_fim}) | "
            f"abrangencia={self.config_entrada.abrangencia} | "
            f"downloads={self.download_dir} | "
            f"datalake_dir={self.directory}"
        )

    # ==========================================================
    # Helpers (iframe + scroll + limpar/digitar + click)
    # ==========================================================
    async def _entrar_no_iframe_app(self, timeout: int = 60) -> None:
        console.print("[STEP] Alternando para o iframe do app SAP...")

        wait = WebDriverWait(self.driver, timeout)

        self.driver.switch_to.default_content()
        wait.until(EC.presence_of_element_located((By.XPATH, self.X_APP_IFRAME)))
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.X_APP_IFRAME)))

        console.print("[STEP] OK: dentro do iframe do app SAP.")
        await worker_sleep(0.2)

    async def _sair_do_iframe(self) -> None:
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

    async def _scroll_center(self, el) -> None:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        await worker_sleep(0.15)


    async def _limpar_e_digitar(self, xpath: str, valor: str, timeout: int = 30) -> None:
        """
        Versão robusta contra:
        - StaleElementReferenceException (UI5 re-render)
        - clique interceptado/overlay
        - elemento existir mas ainda não estar pronto
        Mantém seu padrão (CTRL+A, DEL, clear, TAB, fallback JS),
        porém SEM reutilizar WebElement stale: sempre re-localiza quando necessário.
        """
        wait = WebDriverWait(self.driver, timeout)

        for tentativa in range(1, 4):  # 3 tentativas
            try:
                el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                await self._scroll_center(el)

                # ===== foco/click =====
                try:
                    el.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    # re-localiza e tenta JS click/focus
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    await self._scroll_center(el)
                    try:
                        self.driver.execute_script("arguments[0].click();", el)
                    except Exception:
                        self.driver.execute_script("arguments[0].focus();", el)

                await worker_sleep(0.10)

                # ===== limpar via CTRL+A / DEL =====
                try:
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    el.send_keys(Keys.CONTROL, "a")
                    await worker_sleep(0.05)
                    el.send_keys(Keys.DELETE)
                    await worker_sleep(0.10)
                except (StaleElementReferenceException, TimeoutException):
                    # re-localiza e segue
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                # ===== clear (se ainda tiver valor) =====
                try:
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    atual = el.get_attribute("value") or ""
                    if atual.strip():
                        try:
                            el.clear()
                        except Exception:
                            self.driver.execute_script("arguments[0].value='';", el)
                        await worker_sleep(0.10)
                except (StaleElementReferenceException, TimeoutException):
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                # ===== garantir foco de novo =====
                try:
                    el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    await self._scroll_center(el)
                    el.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    self.driver.execute_script("arguments[0].focus();", el)

                await worker_sleep(0.05)

                # ===== digitar =====
                el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                el.send_keys(str(valor))
                await worker_sleep(0.10)

                # ===== TAB (SAP UI5 normalmente confirma no blur) =====
                try:
                    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    el.send_keys(Keys.TAB)
                except Exception:
                    pass
                await worker_sleep(0.15)

                # ===== validação + fallback JS (re-localizando) =====
                try:
                    el2 = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    final = el2.get_attribute("value") or ""
                    if str(valor) not in final:
                        self.driver.execute_script(
                            """
                            const el = arguments[0];
                            const v = arguments[1];
                            el.value = v;
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            """,
                            el2,
                            str(valor),
                        )
                        await worker_sleep(0.15)
                        try:
                            el2.send_keys(Keys.TAB)
                        except Exception:
                            pass
                        await worker_sleep(0.10)
                except (StaleElementReferenceException, TimeoutException):
                    # se stale aqui, a tentativa recomeça
                    raise

                return  # sucesso

            except StaleElementReferenceException:
                console.print(f"[WARN] StaleElement em _limpar_e_digitar (tentativa {tentativa}/3) -> re-localizando...")
                # opcional: reafirma iframe (SAP UI5 às vezes recria o frame)
                try:
                    await self._entrar_no_iframe_app(timeout=20)
                except Exception:
                    pass
                await worker_sleep(0.6)

        # se chegar aqui, falhou todas as tentativas
        raise StaleElementReferenceException(f"Elemento ficou stale após 3 tentativas: {xpath}")

    async def _clicar(self, xpath: str, timeout: int = 60) -> None:
        wait = WebDriverWait(self.driver, timeout)
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        await self._scroll_center(el)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return
        except (ElementClickInterceptedException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", el)
            return

    # ==========================================================
    # Esperar download XLSX
    # ==========================================================
    async def _aguardar_xlsx_baixado(self, timeout: int = 240, quiet_window_sec: float = 1.2) -> Path:
        """
        Espera surgir um .xlsx novo no Downloads e terminar (.crdownload sumir e tamanho estabilizar).
        Retorna o Path do arquivo baixado.
        """
        pasta = Path(DOWNLOADS_PATH)
        start = time.time()

        existentes = {p.name for p in pasta.glob("*.xlsx")}
        console.print(f"[DL] Aguardando XLSX novo em: {pasta} (timeout={timeout}s)")

        candidato: Optional[Path] = None

        # 1) esperar aparecer xlsx novo (ou o mais recente modificado depois do start)
        while time.time() - start < timeout:
            if list(pasta.glob("*.crdownload")):
                await worker_sleep(0.5)
                continue

            xlsx_files = list(pasta.glob("*.xlsx"))
            novos = [p for p in xlsx_files if p.name not in existentes]
            if novos:
                candidato = max(novos, key=lambda p: p.stat().st_mtime)
                break

            if xlsx_files:
                ultimo = max(xlsx_files, key=lambda p: p.stat().st_mtime)
                if ultimo.stat().st_mtime >= start - 1:
                    candidato = ultimo
                    break

            await worker_sleep(0.5)

        if not candidato:
            raise TimeoutError(f"[DL] Nenhum .xlsx apareceu em {timeout}s em {pasta}")

        console.print(f"[DL] Candidato detectado: {candidato.name}")

        # 2) esperar estabilizar tamanho
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
    # Renomear + Upload (AJUSTADO para seu padrão de nome)
    # ==========================================================
    async def rename_file(
        self,
        produto: str,
        centro_tag: str,
        timeout: int = 240
    ) -> Path:
        """
        Nome final:
        CENTRO-PRODUTO-MES-ANO-DATE_NOW.xlsx

        Ex:
          2501-2000011-01-2026-20260129170011.xlsx
        """
        console.print("[RF] Iniciando renomeação + envio pro datalake.")
        try:
            # 1) aguarda o xlsx baixar de verdade
            baixado = await self._aguardar_xlsx_baixado(timeout=timeout)
            current_path = str(baixado)

            console.print(f"[RF] Arquivo baixado detectado: {current_path}")
            console.print(f"[RF] Existe? {os.path.exists(current_path)}")

            # 2) monta nome padrão
 
            # Renomear
            filename = f"{centro_tag}-{produto}-{mes}-{ano}-{date_now}.xlsx"
            final_path = os.path.join(DOWNLOADS_PATH, filename)

            console.print(f"[RF] Novo filename: {filename}")
            console.print(f"[RF] Movendo para: {final_path}")

            # 3) renomeia/move
            os.rename(current_path, final_path)
            console.print(f"[RF] Arquivo renomeado para {final_path}.")

            # 4) carrega bytes
            with open(final_path, "rb") as file:
                file_bytes = io.BytesIO(file.read())

            await worker_sleep(1)

            # 5) envia pro datalake
            if not self.directory:
                raise RuntimeError("self.directory (datalake) não foi definido. Passe pelo config SAP_Faturamento.")

            try:
                console.print(f"[RF] directory: {self.directory}")
                console.print(f"[RF] file: {final_path}")

                send_file_request = await send_file_to_datalake(
                    self.directory, file_bytes, filename, "xlsx"
                )
                console.print(f"[RF] Resposta send_file_to_datalake: {send_file_request}")
            except Exception as e:
                console.print(f"[RF][ERRO] Erro ao enviar o arquivo: {e}", style="bold red")
                console.print("[RF][ERRO] Traceback:")
                console.print(traceback.format_exc())
                raise

            await worker_sleep(1)

            # 6) apaga local
            if final_path and os.path.exists(final_path):
                try:
                    os.remove(final_path)
                    console.print(f"[RF] Arquivo deletado: {final_path}")
                except Exception as e:
                    raise RuntimeError(f"Erro ao deletar o arquivo: {e}")

            return Path(final_path)

        except Exception as e:
            console.print(f"[RF][ERRO] {e}")
            console.print("[RF][ERRO] Traceback:")
            console.print(traceback.format_exc())
            raise

    # ==========================================================
    # FLUXO: INICIAR SESSÃO SAP (ABRIR + LOGIN)
    # ==========================================================
    async def iniciar_sessao_sap(self) -> RpaRetornoProcessoDTO:
        step = "INIT"
        console.print("[STEP] Iniciando fluxo: INICIAR SESSÃO SAP")

        try:
            step = "VALIDATE_CONFIG"
            if not self.user or not self.password:
                msg = f"[{step}] Credenciais SAP inválidas."
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

            step = "INIT_CHROMEDRIVER"
            console.print(f"[STEP={step}] Obtendo ChromeDriver...")
            service = Service(ChromeDriverManager().install())

            step = "INIT_WEBDRIVER"
            console.print(f"[STEP={step}] Inicializando Chrome...")

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
                console.print("[ERRO] " + msg)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print("[LOGIN] Login realizado com sucesso.")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Sessão SAP iniciada com sucesso.",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        except Exception as e:
            tb = traceback.format_exc()
            msg = f"Erro no fluxo (etapa {step}): {type(e).__name__}: {e}"
            console.print("[ERRO] " + msg)
            console.print(tb)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg + "\n" + tb,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    # ==========================================================
    # LOGIN
    # ==========================================================
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
            console.print("[LOGIN] Usuário preenchido.")
            await worker_sleep(0.5)

            inputs[1].clear()
            inputs[1].send_keys(self.password)
            console.print("[LOGIN] Senha preenchida.")
            await worker_sleep(0.5)

            for i in range(10):
                btn = self.driver.find_elements(By.ID, "LOGIN_SUBMIT_BLOCK")
                console.print(f"[LOGIN] Tentativa {i+1}/10 | botão encontrado? {bool(btn)}")
                if btn:
                    btn[0].click()
                    console.print("[LOGIN] Botão de login clicado.")
                    break
                await worker_sleep(1)

            await worker_sleep(3)
            console.print("[LOGIN] Login finalizado.")
            return True

        except Exception:
            console.print("[LOGIN][ERRO] Exceção durante login.")
            console.print(traceback.format_exc())
            return False

    # ==========================================================
    # LOOP: PRODUTO 1 faz todos os centros -> PRODUTO 2 faz todos os centros
    # ==========================================================
    async def lista_material(self) -> List[str]:
        arquivos: List[str] = []

        centro_range_tag = f"{self.centro_ini}-{self.centro_fim}"

        total_exec = len(self.produtos) * len(self.centros)
        contador = 0
        primeira_vez = False
        for idx_prod, produto in enumerate(self.produtos, start=1):
            console.print(f"[LOOP] Produto ({idx_prod}/{len(self.produtos)}): {produto} | Centros: {centro_range_tag}")

            for idx_ctr, centro in enumerate(self.centros, start=1):
                limpar_downloads(DOWNLOADS_PATH)
                contador += 1
                console.print(f"[LOOP] ({contador}/{total_exec}) Produto: {produto} | Centro: {centro}")

                await self._entrar_no_iframe_app(timeout=60)

                console.print(f"[STEP] Material: {produto}")
                await self._limpar_e_digitar(self.X_MATERIAL, produto)

                console.print(f"[STEP] Centro: {centro}")
                await self._limpar_e_digitar(self.X_CENTRO, centro)


                if not primeira_vez:
                    mes_adapatado = mes[-1]
                    console.print(f"[STEP] Período: {mes}")
                    await self._limpar_e_digitar(self.X_PERIODO, mes_adapatado)

                    console.print(f"[STEP] Ano: {ano}")
                    await self._limpar_e_digitar(self.X_ANO, ano)

                    console.print(f"[STEP] Clicar preço")
                    await self._clicar(self.X_PRECO)
                    primeira_vez = True

                    await worker_sleep(5)

                    console.print(f"[STEP] Selecionar Visão:")
                    await self._clicar(self.X_VISAO)
                    await worker_sleep(2)

                    campo = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.X_VISAO))
                    )

                    # SAP UI5: seta + enter (Histórico de preços)
                    campo.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.2)
                    campo.send_keys(Keys.ENTER)

                await worker_sleep(2)
                
                console.print(f"[STEP] Clicar atualizar:")
                await self._clicar(self.X_ATUALIZAR)

                await worker_sleep(2)

                console.print("[STEP] Clicando em ExportaR")
                await self._clicar(self.X_EXPORTAR)

                await worker_sleep(2)

                # confirma menu/dialog de export
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()

                console.print(f"[STEP] Exportar para:")
                await self._clicar(self.X_EXPORTAR_PARA)

                console.print("[STEP] Exportar dados clicado com sucesso.")
                await worker_sleep(0.8)

                console.print("[STEP] Clicando em OK")
                await self._clicar(self.X_OK)
                console.print("[STEP] OK clicado com sucesso.")

                console.print("[STEP] Aguardando XLSX baixar + renomeando + enviando datalake...")

                # centro_tag agora é o centro atual (um arquivo por centro)
                final_path = await self.rename_file(
                    produto=produto,
                    centro_tag=centro,
                    timeout=240,
                )

                console.print(f"[STEP] Enviado e limpo local: {final_path.name}")
                arquivos.append(final_path.name)

                await self._sair_do_iframe()
                await worker_sleep(1)

        return arquivos


# ==========================================================
# FLUXO PRINCIPAL
# ==========================================================
async def extracao_movimento_estoque_sap(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando fluxo principal: extracao_movimento_estoque_sap")

    bot: Optional[ExtracaoMovimentoEstoque] = None
    try:
        console.print("[MAIN] Buscando config SAP_Faturamento...")
        cfg = await get_config_by_name("SAP_Faturamento")
        base_url = cfg.conConfiguracao.get("baseUrl")
        directory = cfg.conConfiguracao.get("directoryBucket")

        bot = ExtracaoMovimentoEstoque(task=task, base_url=base_url, directory=directory)

        ret = await bot.iniciar_sessao_sap()
        if not ret.sucesso:
            return ret

        arquivos = await bot.lista_material()

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
