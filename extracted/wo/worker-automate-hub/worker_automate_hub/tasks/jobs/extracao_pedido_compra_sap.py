import asyncio
import os
import io
import sys
import traceback
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from worker_automate_hub.api.datalake_service import send_file_to_datalake
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)

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

console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
console.print(f"[INIT] Downloads dir: {DOWNLOADS_PATH}")


# ==========================
# CONFIG DE ENTRADA (NOVA)
# ==========================
class ConfigEntradaSAP(BaseModel):
    """
    Configuração de entrada do processo
    (EXATAMENTE a configEntrada do main)
    """

    materialInicial: str
    materialFinal: str
    centroInicial: str
    centroFinal: str
    abrangencia: str


# ==========================
# CLASSE PRINCIPAL
# ==========================
class ExtracaoPedidosCompra:
    # ==========
    # XPATHs
    # ==========
    X_MATERIAL_INI = "(//input[@title='Nº do material'])[1]"
    X_MATERIAL_FIM = "(//input[@title='Nº do material'])[2]"
    X_CENTRO_INI = "(//input[@title='Centro'])[1]"
    X_CENTRO_FIM = "(//input[@title='Centro'])[2]"
    X_ABRANGENCIA = "//input[@title='Parâmetros de abrangência das listas de compra']"
    X_EXECUTAR = "//div[@title='Executar (F8)']"
    X_BAIXAR = "//div[@title='Planilha eletrônica... (Ctrl+Shift+F7)']"
    X_EXPORTAR = "//div[@title='Exportar dados (Shift+F8)']"
    X_OK = "//div[@id='UpDownDialogChoose']"

    # IFRAME
    X_APP_IFRAME = (
        "//iframe[contains(@name,'application-PurchaseOrder-displayByMaterial')]"
    )

    def __init__(
        self,
        task: RpaProcessoEntradaDTO,
        base_url: str,
        directory: Optional[str] = None,  # ✅ usado para enviar pro datalake
    ):
        console.print("[STEP 0.1] Inicializando ExtracaoPedidosCompra")

        self.task = task

        hash_path = "PurchaseOrder-displayByMaterial?sap-ui-tech-hint=GUI"

        # Remove qualquer fragment anterior e adiciona o novo
        self.base_url = base_url.split("#")[0] + "#" + hash_path

        # Credenciais SAP
        self.user = CredentialsManager().get_by_key("SAP_USER_BI")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_BI")

        # Valida configEntrada
        self.config_entrada = ConfigEntradaSAP(
            **(getattr(task, "configEntrada", {}) or {})
        )

        self.driver: Optional[webdriver.Chrome] = None

        # Pasta padrão de downloads (Windows)
        self.download_dir = Path.home() / "Downloads"
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # diretório do datalake
        self.directory = directory

        console.print(
            f"[STEP 0.2] user={'OK' if self.user else None} | "
            f"material={self.config_entrada.materialInicial}-{self.config_entrada.materialFinal} | "
            f"centro={self.config_entrada.centroInicial}-{self.config_entrada.centroFinal} | "
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
        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.X_APP_IFRAME))
        )

        console.print("[STEP] OK: dentro do iframe do app SAP.")
        await worker_sleep(0.2)

    async def _sair_do_iframe(self) -> None:
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

    async def _scroll_center(self, el) -> None:
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
        except Exception:
            pass
        await worker_sleep(0.15)

    async def _limpar_e_digitar(
        self, xpath: str, valor: str, timeout: int = 30
    ) -> None:
        wait = WebDriverWait(self.driver, timeout)

        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        await self._scroll_center(el)

        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].focus();", el)
        await worker_sleep(0.1)

        try:
            el.send_keys(Keys.CONTROL, "a")
            await worker_sleep(0.05)
            el.send_keys(Keys.DELETE)
            await worker_sleep(0.10)
        except Exception:
            pass

        try:
            atual = el.get_attribute("value") or ""
            if atual.strip():
                el.clear()
                await worker_sleep(0.10)
        except Exception:
            pass

        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].focus();", el)
        await worker_sleep(0.05)

        el.send_keys(str(valor))
        await worker_sleep(0.10)

        try:
            el.send_keys(Keys.TAB)
        except Exception:
            pass
        await worker_sleep(0.15)

        try:
            final = el.get_attribute("value") or ""
            if str(valor) not in final:
                self.driver.execute_script(
                    """
                    const el = arguments[0];
                    const v = arguments[1];
                    el.value = v;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    """,
                    el,
                    str(valor),
                )
                await worker_sleep(0.15)
                try:
                    el.send_keys(Keys.TAB)
                except Exception:
                    pass
                await worker_sleep(0.10)
        except Exception:
            pass

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
    # Eesperar download XLSX
    # ==========================================================
    async def _aguardar_xlsx_baixado(
        self, timeout: int = 240, quiet_window_sec: float = 1.2
    ) -> Path:
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
                # se foi modificado depois que começamos a esperar
                if ultimo.stat().st_mtime >= start - 1:
                    candidato = ultimo
                    break

            await worker_sleep(0.5)

        if not candidato:
            raise TimeoutError(f"[DL] Nenhum .xlsx apareceu em {timeout}s em {pasta}")

        console.print(f"[DL] Candidato detectado: {candidato.name}")

        # 2) esperar estabilizar tamanho (garantir finalização)
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
                # pode ter trocado de nome no final, pega o mais recente
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

    async def rename_file(
        self, company: str, file_type: str, timeout: int = 240
    ) -> Path:
        console.print(
            "[RF] Iniciando renomeação + envio pro datalake (mantendo sua função)."
        )
        try:
            # 1) aguarda o xlsx baixar de verdade (sem depender de export.xlsx)
            baixado = await self._aguardar_xlsx_baixado(timeout=timeout)
            current_path = str(baixado)

            console.print(f"[RF] Arquivo baixado detectado: {current_path}")
            console.print(f"[RF] Existe? {os.path.exists(current_path)}")

            # 2) monta nome padrão
            date_now = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{company}_{file_type}_{date_now}.xlsx"
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

            # 5) envia pro datalake (mantido)
            if not self.directory:
                raise RuntimeError(
                    "self.directory (datalake) não foi definido. Passe pelo config SAP_Faturamento."
                )

            try:
                console.print(f"[RF] directory: {self.directory}")
                console.print(f"[RF] file: {final_path}")

                send_file_request = await send_file_to_datalake(
                    "qd_comercial/raw", file_bytes, filename, "xlsx"
                )
                console.print(
                    f"[RF] Resposta send_file_to_datalake: {send_file_request}"
                )
            except Exception as e:
                console.print(
                    f"[RF][ERRO] Erro ao enviar o arquivo: {e}", style="bold red"
                )
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
            # Mantém comportamento de erro “visível”
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
                console.print(
                    f"[LOGIN] Tentativa {i+1}/10 | botão encontrado? {bool(btn)}"
                )
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
    # PASSO: ENTRAR NO IFRAME + PREENCHER CAMPOS + EXECUTAR + EXPORTAR + BAIXAR + RENOMEAR+ENVIAR
    # ==========================================================
    async def lista_material(self) -> str:
        console.print("[STEP] Preenchendo filtros")

        await self._entrar_no_iframe_app(timeout=60)

        console.print(f"[STEP] Material inicial: {self.config_entrada.materialInicial}")
        await self._limpar_e_digitar(
            self.X_MATERIAL_INI, self.config_entrada.materialInicial
        )

        console.print(f"[STEP] Material final: {self.config_entrada.materialFinal}")
        await self._limpar_e_digitar(
            self.X_MATERIAL_FIM, self.config_entrada.materialFinal
        )

        console.print(f"[STEP] Centro inicial: {self.config_entrada.centroInicial}")
        await self._limpar_e_digitar(
            self.X_CENTRO_INI, self.config_entrada.centroInicial
        )

        console.print(f"[STEP] Centro final: {self.config_entrada.centroFinal}")
        await self._limpar_e_digitar(self.X_CENTRO_FIM, self.config_entrada.centroFinal)

        console.print(f"[STEP] Abrangência: {self.config_entrada.abrangencia}")
        await self._limpar_e_digitar(
            self.X_ABRANGENCIA, self.config_entrada.abrangencia
        )

        console.print("[STEP] Clicando em Executar (F8)")
        await self._clicar(self.X_EXECUTAR)
        console.print("[STEP] Executar (F8) clicado com sucesso.")
        await worker_sleep(1.5)

        console.print("[STEP] Clicando em Planilha eletrônica... (Ctrl+Shift+F7)")
        await self._clicar(self.X_BAIXAR)
        console.print("[STEP] Planilha eletrônica... clicado com sucesso.")
        await worker_sleep(0.8)

        console.print("[STEP] Clicando em Exportar dados (Shift+F8)")
        await self._clicar(self.X_EXPORTAR)
        console.print("[STEP] Exportar dados clicado com sucesso.")
        await worker_sleep(0.8)

        console.print("[STEP] Clicando em OK")
        await self._clicar(self.X_OK)
        console.print("[STEP] OK clicado com sucesso.")

        # Função rename+upload, mas agora ela aguarda o XLSX baixar
        console.print(
            "[STEP] Aguardando XLSX baixar + renomeando + enviando datalake..."
        )
        final_path = await self.rename_file(
            company="PEDIDOS_DE_COMPRAS",
            file_type="VS_FORNECEDOR",
            timeout=240,
        )

        console.print(f"[STEP] Enviado e limpo local: {final_path.name}")
        return final_path.name


# ==========================================================
# FLUXO PRINCIPAL
# ==========================================================
async def extracao_pedidos_compras_sap(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando fluxo principal: extracao_pedidos_compras_sap")

    bot: Optional[ExtracaoPedidosCompra] = None
    try:
        console.print("[MAIN] Buscando config SAP_Faturamento...")
        cfg = await get_config_by_name("SAP_Faturamento")
        base_url = cfg.conConfiguracao.get("baseUrl")

        directory = cfg.conConfiguracao.get("directoryBucket")
        bot = ExtracaoPedidosCompra(task=task, base_url=base_url, directory=directory)

        ret = await bot.iniciar_sessao_sap()
        if not ret.sucesso:
            return ret

        arquivo_nome = await bot.lista_material()

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Login OK, exportação OK, envio datalake OK: {arquivo_nome}",
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
