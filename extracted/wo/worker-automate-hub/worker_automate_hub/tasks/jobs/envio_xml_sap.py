import asyncio
import os
import sys
import re
import json
import base64
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional

from rich.console import Console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pyperclip
except Exception:
    pyperclip = None

from worker_automate_hub.utils.credentials_manager import CredentialsManager

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_sap_dto import RpaProcessoSapDTO
from worker_automate_hub.utils.util import worker_sleep, kill_all_emsys

from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

console = Console()


class FalhaNegocioSAP(Exception):
    """Erro funcional retornado pelo SAP durante o processamento do XML."""

    pass


class EnvioXmlSAP:
    HASH_ENVIO_XML = "SupplierInvoice-createAdvanced?sap-ui-tech-hint=GUI"

    # Login
    X_CLIENT = "//input[@id='CLIENT_FIELD-inner']"
    X_LOGIN_INPUTS = "loginInputField"
    X_LOGIN_BUTTON = "LOGIN_SUBMIT_BLOCK"

    # Tela inicial SupplierInvoice
    X_IFRAME_SUPPLIER = (
        "//iframe[@name='application-SupplierInvoice-createAdvanced-iframe']"
    )
    X_FECHAR_POPUP = "//button[@title='Fechar']"

    # Busca Shell SAP
    X_BUSCA_SHELL = "//input[@id='searchFieldInShell-input-inner']"
    X_BOTAO_BUSCA = "//span[@id='searchFieldInShell-button-img']"

    # Resultado EDOC UPLOAD
    X_RESULTADO_EDOC_UPLOAD = (
        "//a[contains(@aria-label, 'eDocument Brasil') "
        "and contains(@aria-label, 'carregar documento')]"
    )

    # Iframe EDOC
    X_IFRAME_EDOC = (
        "//iframe[contains(@name,'application-SupplierInvoice-createAdvanced') "
        "or contains(@name,'EDOC') "
        "or contains(@name,'Z_CAT_EDO') "
        "or contains(@src,'Z_CAT_EDO') "
        "or contains(@src,'EDOC_BR_UPLOAD')]"
    )

    # Botão ajuda empresa
    X_BOTAO_HELP_EMPRESA = "//span[contains(@id,'ls-inputfieldhelpbutton')]"

    # Botão OK da seleção de empresa
    X_BOTAO_OK_EMPRESA = (
        "//div[@role='button' and contains(@class,'lsButton') "
        "and (contains(., 'OK') or contains(@lsdata, 'OK'))]"
    )

    # Botão Executar EDOC
    X_BOTAO_EXECUTAR_EDOC = "//div[@title=' (F8)']"

    def __init__(self, task: RpaProcessoSapDTO, base_url: str):
        self.task = task

        self.config_entrada = self.normalizar_config_entrada(
            getattr(task, "configEntrada", {}) or {}
        )

        self.base_url = base_url.split("#")[0] + "#" + self.HASH_ENVIO_XML

        self.user = CredentialsManager().get_by_key("SAP_USER_DRC")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_DRC")

        self.id_email = self.get_config_value("idEmail")

        # Mantém o nome original apenas para diagnóstico.
        self.nome_arquivo_original = self.get_config_value("nomeArquivo")

        # Nome efetivamente usado no arquivo, upload e logs.
        # É atualizado definitivamente em criar_xml_da_config().
        self.nome_arquivo_config = self.sanitizar_nome_arquivo(
            self.nome_arquivo_original
        )

        self.driver: Optional[webdriver.Chrome] = None

        self.pasta_xml = Path.home() / "Documents" / "envio_xml_sap"
        self.pasta_xml.mkdir(parents=True, exist_ok=True)

        console.print("[INIT] EnvioXmlSAP inicializado.")
        console.print(f"[INIT] URL SAP: {self.base_url}")
        console.print(f"[INIT] Usuário carregado? {'SIM' if self.user else 'NÃO'}")
        console.print(f"[INIT] Pasta XML: {self.pasta_xml}")
        console.print(
            f"[INIT] nomeArquivo recebido: {repr(self.nome_arquivo_original)}"
        )
        console.print(
            f"[INIT] nomeArquivo normalizado: {self.nome_arquivo_config}"
        )
        console.print(f"[INIT] idEmail: {self.id_email}")

    # ==========================================================
    # CONFIG ENTRADA
    # ==========================================================
    def normalizar_config_entrada(self, config):
        if config is None:
            return {}

        if isinstance(config, dict):
            return config

        if isinstance(config, str):
            texto = config.strip()

            if not texto:
                return {}

            try:
                return json.loads(texto)
            except Exception as e:
                raise RuntimeError(
                    f"configEntrada veio como string, mas não é JSON válido: {e}"
                )

        try:
            return vars(config)
        except Exception:
            return {}

    def get_config_value(self, chave: str, default=None):
        if isinstance(self.config_entrada, dict):
            return self.config_entrada.get(chave, default)

        return getattr(self.config_entrada, chave, default)

    # ==========================================================
    # RETORNOS PADRONIZADOS
    # ==========================================================
    def retorno_sucesso(self, msg: str) -> RpaRetornoProcessoDTO:
        console.print(f"[SUCESSO] {msg}")

        status_final = (
            RpaHistoricoStatusEnum.Descartado
            if "importado anteriormente no SAP" in msg or "Registro já existente" in msg
            else RpaHistoricoStatusEnum.Sucesso
        )

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=msg,
            status=status_final,
        )

    def retorno_erro(self, msg: str) -> RpaRetornoProcessoDTO:
        console.print(f"[ERRO] {msg}")

        status_final = (
            RpaHistoricoStatusEnum.Descartado
            if "importado anteriormente no SAP" in msg or "Registro já existente" in msg
            else RpaHistoricoStatusEnum.Falha
        )

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=msg,
            status=status_final,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    def retorno_falha_negocio(self, msg: str) -> RpaRetornoProcessoDTO:
        console.print(f"[FALHA_NEGOCIO] {msg}")

        status_final = (
            RpaHistoricoStatusEnum.Descartado
            if "importado anteriormente no SAP" in msg or "Registro já existente" in msg
            else RpaHistoricoStatusEnum.Falha
        )

        # Não marca como erro técnico. A mensagem funcional do SAP é
        # devolvida diretamente no retorno do processo.
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=msg,
            status=status_final,
        )

    # ==========================================================
    # FLUXO PRINCIPAL
    # ==========================================================
    async def iniciar(self) -> RpaRetornoProcessoDTO:
        step = "INIT"

        try:
            step = "VALIDAR_CONFIG"
            self.validar_config()

            step = "CRIAR_XML"
            caminho_xml = self.criar_xml_da_config()
            console.print(f"[XML] Arquivo XML preparado: {caminho_xml}")

            step = "ABRIR_CHROME"
            self.abrir_chrome()

            step = "ACESSAR_SAP"
            console.print(f"[{step}] Acessando SAP...")
            self.driver.get(self.base_url)
            await worker_sleep(3)

            step = "LOGIN"
            login_ok = await self.login()

            if not login_ok:
                return self.retorno_erro("Falha ao realizar login no SAP.")

            step = "STEPS_SAP"
            mensagem_final = await self.steps_sap(caminho_xml)

            return self.retorno_sucesso(mensagem_final)

        except FalhaNegocioSAP as e:
            return self.retorno_falha_negocio(str(e))

        except Exception as e:
            tb = traceback.format_exc()
            msg = (
                f"Falha no envio/importação do XML no SAP. "
                f"Etapa: {step}. "
                f"Erro: {type(e).__name__}: {e}\n{tb}"
            )

            console.print(f"[ERRO] {msg}")

            return self.retorno_erro(msg)

    def validar_config(self) -> None:
        if not self.user or not self.password:
            raise RuntimeError(
                "Credenciais SAP_USER_DRC ou SAP_PASSWORD_DRC não encontradas."
            )

        if not self.base_url:
            raise RuntimeError("base_url não configurada.")

        xml_base64 = self.get_config_value("xml")
        nome_arquivo = self.get_config_value("nomeArquivo")

        if not xml_base64:
            raise RuntimeError("configEntrada.xml não informado.")

        if not nome_arquivo:
            raise RuntimeError("configEntrada.nomeArquivo não informado.")

    def abrir_chrome(self) -> None:
        console.print("[CHROME] Inicializando ChromeDriver...")

        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument("--lang=pt-BR")
        options.add_argument("--log-level=3")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")

        self.driver = webdriver.Chrome(service=service, options=options)

        try:
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """},
            )
        except Exception:
            pass

        self.driver.maximize_window()

    # ==========================================================
    # XML BASE64
    # ==========================================================
    def criar_xml_da_config(self) -> Path:
        xml_base64 = self.get_config_value("xml")
        nome_arquivo_original = self.get_config_value("nomeArquivo")

        # Sanitiza novamente a partir da configuração para garantir que
        # caracteres ocultos, TABs e espaços extras nunca cheguem ao Windows.
        nome_arquivo = self.sanitizar_nome_arquivo(nome_arquivo_original)

        if not nome_arquivo.lower().endswith(".xml"):
            nome_arquivo += ".xml"

        # criação do arquivo, upload e mensagens retornadas/logadas.
        self.nome_arquivo_original = nome_arquivo_original
        self.nome_arquivo_config = nome_arquivo

        caminho_xml = self.pasta_xml / self.nome_arquivo_config

        console.print(
            f"[XML] Nome recebido da configuração: {repr(nome_arquivo_original)}"
        )
        console.print(
            f"[XML] Nome final utilizado: {self.nome_arquivo_config}"
        )
        console.print(f"[XML] Caminho final: {caminho_xml}")

        xml_bytes = self.converter_base64_para_bytes(xml_base64)

        with open(caminho_xml, "wb") as f:
            f.write(xml_bytes)

        if not caminho_xml.exists():
            raise RuntimeError(f"XML não foi criado: {caminho_xml}")

        if caminho_xml.stat().st_size == 0:
            raise RuntimeError(f"XML criado vazio: {caminho_xml}")

        console.print(f"[XML] Arquivo salvo com sucesso: {caminho_xml}")
        console.print(
            f"[XML] Tamanho do arquivo: {caminho_xml.stat().st_size} bytes"
        )

        return caminho_xml

    def converter_base64_para_bytes(self, valor: str) -> bytes:
        valor = str(valor).strip()

        if valor.startswith("<"):
            return valor.encode("utf-8")

        if "," in valor and "base64" in valor[:100].lower():
            valor = valor.split(",", 1)[1].strip()

        valor = valor.replace("\n", "").replace("\r", "").replace(" ", "")

        try:
            return base64.b64decode(valor)
        except Exception as e:
            raise RuntimeError(f"Não conseguiu converter XML base64: {e}")

    def sanitizar_nome_arquivo(self, nome: str) -> str:
        nome_original = str(nome or "")
        nome = nome_original.strip()

        # Remove caracteres de controle reais:
        # TAB (\t), CR (\r), LF (\n), NUL etc.
        nome = re.sub(r"[\x00-\x1f\x7f]", "", nome)

        # Substitui caracteres inválidos em nomes de arquivo no Windows.
        nome = re.sub(r'[\\/:*?"<>|]', "_", nome)

        # Remove espaços antes/depois de "_".
        # Ex.: "Pelotas JK   _140920260.xml"
        # vira "Pelotas JK_140920260.xml".
        nome = re.sub(r"[ ]*_+[ ]*", "_", nome)

        # Garante que não existam underscores duplicados.
        nome = re.sub(r"_+", "_", nome)

        # Normaliza qualquer sequência restante de espaços.
        nome = re.sub(r"[ ]+", " ", nome).strip()

        # O Windows não aceita nome terminando em espaço ou ponto.
        nome = nome.rstrip(" .")

        if not nome:
            nome = f"xml_sap_{datetime.now().strftime('%Y%m%d%H%M%S')}.xml"

        return nome

    # ==========================================================
    # LOGIN
    # ==========================================================
    async def login(self) -> bool:
        try:
            console.print("[LOGIN] Iniciando login...")

            await self.alterar_client_para_800()

            inputs = await self.aguardar_inputs_login()

            if len(inputs) < 2:
                console.print("[LOGIN][ERRO] Campos de usuário/senha não encontrados.")
                return False

            inputs[0].clear()
            inputs[0].send_keys(self.user)
            console.print("[LOGIN] Usuário preenchido.")

            await worker_sleep(0.5)

            inputs[1].clear()
            inputs[1].send_keys(self.password)
            console.print("[LOGIN] Senha preenchida.")

            await worker_sleep(0.5)

            botao_login = await self.aguardar_botao_login()

            if not botao_login:
                console.print("[LOGIN][ERRO] Botão de login não encontrado.")
                return False

            botao_login.click()
            console.print("[LOGIN] Botão de login clicado.")

            await worker_sleep(5)

            console.print("[LOGIN] Login finalizado.")
            return True

        except Exception:
            console.print("[LOGIN][ERRO] Erro durante login.")
            console.print(traceback.format_exc())
            return False

    async def alterar_client_para_800(self) -> None:
        console.print("[LOGIN] Alterando client SAP para 800...")

        campo = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.X_CLIENT))
        )

        campo.click()
        campo.send_keys(Keys.CONTROL, "a")
        campo.send_keys(Keys.DELETE)
        campo.send_keys("800")

        await worker_sleep(0.5)

        valor = campo.get_attribute("value") or ""

        if valor.strip() != "800":
            console.print(f"[LOGIN][WARN] Client atual='{valor}'. Forçando via JS...")

            self.driver.execute_script(
                """
                const el = arguments[0];
                el.value = '800';
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                campo,
            )

            await worker_sleep(0.5)

        valor = campo.get_attribute("value") or ""
        console.print(f"[LOGIN] Client final: {valor}")

        if valor.strip() != "800":
            raise RuntimeError("Não conseguiu alterar o client SAP para 800.")

    async def aguardar_inputs_login(self):
        for tentativa in range(1, 31):
            inputs = self.driver.find_elements(By.CLASS_NAME, self.X_LOGIN_INPUTS)

            console.print(
                f"[LOGIN] Tentativa {tentativa}/30 | campos encontrados: {len(inputs)}"
            )

            if len(inputs) >= 2:
                return inputs

            await worker_sleep(1)

        return []

    async def aguardar_botao_login(self):
        for tentativa in range(1, 11):
            botoes = self.driver.find_elements(By.ID, self.X_LOGIN_BUTTON)

            console.print(
                f"[LOGIN] Tentativa {tentativa}/10 | botão encontrado? {bool(botoes)}"
            )

            if botoes:
                return botoes[0]

            await worker_sleep(1)

        return None

    # ==========================================================
    # STEPS SAP
    # ==========================================================
    async def steps_sap(self, caminho_xml: Path) -> str:
        console.print("[SAP] Aguardando tela carregar após login...")
        await worker_sleep(8)

        await self.fechar_popup_empresa()
        await self.sair_iframe()

        abriu_edoc = await self.pesquisar_e_abrir_edoc_upload()

        if not abriu_edoc:
            raise RuntimeError("Não foi possível pesquisar e abrir EDOC UPLOAD.")

        clicou_help = await self.clicar_botao_help_empresa()

        if not clicou_help:
            raise RuntimeError("Não foi possível clicar no botão de ajuda Empresa.")

        clicou_ok = await self.clicar_botao_ok_empresa()

        if not clicou_ok:
            raise RuntimeError(
                "Não foi possível clicar no botão OK da seleção de empresa."
            )

        selecionou = await self.selecionar_xml_no_dialogo_windows(caminho_xml)

        if not selecionou:
            raise RuntimeError(
                "Não foi possível selecionar o XML no diálogo do Windows."
            )

        executou = await self.clicar_botao_executar_edoc()

        if not executou:
            raise RuntimeError(
                "Não foi possível clicar no botão Executar após subir o XML."
            )

        mensagem_sap = await self.validar_resultado_importacao_xml(timeout=360)

        console.print(f"[SAP] Resultado final: {mensagem_sap}")

        return mensagem_sap

    # ==========================================================
    # IFRAMES
    # ==========================================================
    async def entrar_iframe_supplier(self, timeout: int = 60) -> None:
        console.print("[IFRAME] Entrando no iframe SupplierInvoice...")

        self.driver.switch_to.default_content()

        WebDriverWait(self.driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, self.X_IFRAME_SUPPLIER)
            )
        )

        console.print("[IFRAME] Dentro do iframe SupplierInvoice.")

    async def entrar_iframe_edoc(self, timeout: int = 60) -> None:
        console.print("[IFRAME] Entrando no iframe EDOC...")

        self.driver.switch_to.default_content()

        wait = WebDriverWait(self.driver, timeout)

        wait.until(EC.presence_of_element_located((By.XPATH, self.X_IFRAME_EDOC)))

        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.X_IFRAME_EDOC))
        )

        console.print("[IFRAME] Dentro do iframe EDOC.")

    async def sair_iframe(self) -> None:
        try:
            self.driver.switch_to.default_content()
            console.print("[IFRAME] Fora do iframe.")
        except Exception:
            pass

    # ==========================================================
    # POPUP EMPRESA INICIAL
    # ==========================================================
    async def fechar_popup_empresa(self, timeout: int = 40) -> bool:
        try:
            console.print("[SAP] Fechando popup 'Entrar empresa'...")

            await self.entrar_iframe_supplier(timeout=timeout)

            botao_fechar = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, self.X_FECHAR_POPUP))
            )

            try:
                botao_fechar.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", botao_fechar)

            console.print("[SAP] Popup 'Entrar empresa' fechado.")
            await worker_sleep(2)

            return True

        except Exception as e:
            console.print(f"[SAP][WARN] Popup não apareceu ou não foi fechado: {e}")
            return False

        finally:
            await self.sair_iframe()

    # ==========================================================
    # PESQUISAR E ABRIR EDOC UPLOAD
    # ==========================================================
    async def pesquisar_e_abrir_edoc_upload(self, timeout: int = 60) -> bool:
        console.print("[SAP] Pesquisando EDOC UPLOAD no Shell...")

        self.driver.switch_to.default_content()
        wait = WebDriverWait(self.driver, timeout)

        try:
            await self.preencher_busca_shell(wait, "EDOC UPLOAD")
            await self.clicar_botao_busca_shell(wait)
            await self.clicar_resultado_edoc_upload(wait)

            console.print("[SAP] EDOC UPLOAD aberto com sucesso.")
            await worker_sleep(8)

            return True

        except Exception as e:
            console.print(f"[SAP][ERRO] Falha ao pesquisar/abrir EDOC UPLOAD: {e}")
            console.print(traceback.format_exc())
            await self.debug_inputs_shell()
            return False

    async def preencher_busca_shell(self, wait: WebDriverWait, texto: str) -> None:
        for tentativa in range(1, 6):
            try:
                console.print(f"[SAP] Preenchendo busca tentativa {tentativa}/5...")

                campo = wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.X_BUSCA_SHELL))
                )

                campo.click()
                await worker_sleep(0.2)

                campo.send_keys(Keys.CONTROL, "a")
                campo.send_keys(Keys.DELETE)
                campo.send_keys(texto)

                await worker_sleep(0.8)

                campo = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.X_BUSCA_SHELL))
                )

                valor = campo.get_attribute("value") or ""
                console.print(f"[SAP] Valor no campo busca: '{valor}'")

                if valor.strip() == texto:
                    return

                console.print("[SAP][WARN] Valor não ficou correto. Forçando via JS...")

                self.driver.execute_script(
                    """
                    const el = arguments[0];
                    const value = arguments[1];

                    el.focus();
                    el.value = value;

                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    el.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                    """,
                    campo,
                    texto,
                )

                await worker_sleep(0.8)

                campo = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.X_BUSCA_SHELL))
                )

                valor = campo.get_attribute("value") or ""
                console.print(f"[SAP] Valor após JS: '{valor}'")

                if valor.strip() == texto:
                    return

            except StaleElementReferenceException:
                console.print("[SAP][WARN] Campo ficou stale. Relocalizando...")
                await worker_sleep(1)

            except Exception as e:
                console.print(f"[SAP][WARN] Erro ao preencher busca: {e}")
                await worker_sleep(1)

        raise RuntimeError("Campo de busca não ficou preenchido com EDOC UPLOAD.")

    async def clicar_botao_busca_shell(self, wait: WebDriverWait) -> None:
        for tentativa in range(1, 6):
            try:
                console.print(f"[SAP] Clicando na lupa tentativa {tentativa}/5...")

                botao = wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.X_BOTAO_BUSCA))
                )

                try:
                    botao.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", botao)

                console.print("[SAP] Botão de pesquisa clicado.")
                await worker_sleep(3)
                return

            except StaleElementReferenceException:
                console.print("[SAP][WARN] Botão ficou stale. Relocalizando...")
                await worker_sleep(1)

            except Exception as e:
                console.print(f"[SAP][WARN] Erro ao clicar na lupa: {e}")
                await worker_sleep(1)

        raise RuntimeError("Não conseguiu clicar no botão de pesquisa.")

    async def clicar_resultado_edoc_upload(self, wait: WebDriverWait) -> None:
        console.print("[SAP] Aguardando resultado EDOC UPLOAD aparecer...")

        for tentativa in range(1, 6):
            try:
                console.print(
                    f"[SAP] Clicando no resultado EDOC UPLOAD tentativa {tentativa}/5..."
                )

                resultado = wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.X_RESULTADO_EDOC_UPLOAD))
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    resultado,
                )

                await worker_sleep(0.5)

                try:
                    resultado.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", resultado)

                console.print("[SAP] Resultado EDOC UPLOAD clicado com sucesso.")
                await worker_sleep(5)
                return

            except StaleElementReferenceException:
                console.print("[SAP][WARN] Resultado ficou stale. Relocalizando...")
                await worker_sleep(1)

            except Exception as e:
                console.print(f"[SAP][WARN] Erro ao clicar no resultado: {e}")
                await worker_sleep(1)

        raise RuntimeError("Não conseguiu clicar no resultado EDOC UPLOAD.")

    # ==========================================================
    # HELP EMPRESA, OK E EXECUTAR
    # ==========================================================
    async def clicar_botao_help_empresa(self, timeout: int = 60) -> bool:
        try:
            console.print("[EDOC] Aguardando tela EDOC carregar...")
            await worker_sleep(5)

            await self.entrar_iframe_edoc(timeout=timeout)

            wait = WebDriverWait(self.driver, timeout)

            for tentativa in range(1, 6):
                try:
                    console.print(
                        f"[EDOC] Tentativa {tentativa}/5 para clicar no botão help..."
                    )

                    botao = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, self.X_BOTAO_HELP_EMPRESA)
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        botao,
                    )

                    await worker_sleep(0.5)

                    try:
                        botao.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", botao)

                    console.print("[EDOC] Botão de ajuda Empresa clicado com sucesso.")
                    await worker_sleep(3)

                    return True

                except StaleElementReferenceException:
                    console.print("[EDOC][WARN] Botão ficou stale. Relocalizando...")
                    await worker_sleep(1)

                except Exception as e:
                    console.print(f"[EDOC][WARN] Erro ao clicar no botão help: {e}")
                    await worker_sleep(1)

            await self.debug_inputs_frame()
            return False

        except Exception as e:
            console.print(
                f"[EDOC][ERRO] Não conseguiu acessar/clicar no botão help Empresa: {e}"
            )
            console.print(traceback.format_exc())
            return False

        finally:
            await self.sair_iframe()

    async def clicar_botao_ok_empresa(self, timeout: int = 60) -> bool:
        try:
            console.print("[EDOC] Aguardando botão OK da seleção de empresa...")

            await worker_sleep(2)

            await self.entrar_iframe_edoc(timeout=timeout)

            wait = WebDriverWait(self.driver, timeout)

            for tentativa in range(1, 6):
                try:
                    console.print(
                        f"[EDOC] Tentativa {tentativa}/5 para clicar no OK..."
                    )

                    botao_ok = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, self.X_BOTAO_OK_EMPRESA)
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        botao_ok,
                    )

                    await worker_sleep(0.5)

                    try:
                        botao_ok_clicavel = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, self.X_BOTAO_OK_EMPRESA)
                            )
                        )
                        botao_ok_clicavel.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", botao_ok)

                    console.print("[EDOC] Botão OK clicado com sucesso.")
                    await worker_sleep(3)

                    return True

                except StaleElementReferenceException:
                    console.print("[EDOC][WARN] Botão OK ficou stale. Relocalizando...")
                    await worker_sleep(1)

                except Exception as e:
                    console.print(f"[EDOC][WARN] Erro ao clicar no OK: {e}")
                    await worker_sleep(1)

            await self.debug_inputs_frame()
            return False

        except Exception as e:
            console.print(f"[EDOC][ERRO] Erro ao clicar no botão OK: {e}")
            console.print(traceback.format_exc())
            return False

        finally:
            await self.sair_iframe()

    async def clicar_botao_executar_edoc(self, timeout: int = 60) -> bool:
        try:
            console.print("[EDOC] Aguardando botão Executar após upload do XML...")

            await worker_sleep(4)

            await self.entrar_iframe_edoc(timeout=timeout)

            wait = WebDriverWait(self.driver, timeout)

            for tentativa in range(1, 6):
                try:
                    console.print(
                        f"[EDOC] Tentativa {tentativa}/5 para clicar em Executar..."
                    )

                    botao_executar = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, self.X_BOTAO_EXECUTAR_EDOC)
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        botao_executar,
                    )

                    await worker_sleep(0.5)

                    try:
                        botao_executar_clicavel = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, self.X_BOTAO_EXECUTAR_EDOC)
                            )
                        )
                        botao_executar_clicavel.click()
                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].click();",
                            botao_executar,
                        )

                    console.print("[EDOC] Botão Executar clicado com sucesso.")
                    await worker_sleep(5)

                    return True

                except StaleElementReferenceException:
                    console.print(
                        "[EDOC][WARN] Botão Executar ficou stale. Relocalizando..."
                    )
                    await worker_sleep(1)

                except Exception as e:
                    console.print(f"[EDOC][WARN] Erro ao clicar em Executar: {e}")
                    await worker_sleep(1)

            await self.debug_inputs_frame()
            return False

        except Exception as e:
            console.print(f"[EDOC][ERRO] Erro ao clicar no botão Executar: {e}")
            console.print(traceback.format_exc())
            return False

        finally:
            await self.sair_iframe()

    # ==========================================================
    # VALIDAR RESULTADO SAP
    # ==========================================================
    async def validar_resultado_importacao_xml(self, timeout: int = 60) -> str:
        """
        Depois de clicar em Executar, aguarda a resposta do SAP.

        Regras:
        - Se encontrar uma mensagem conhecida de sucesso, retorna sucesso.
        - Se encontrar uma mensagem funcional do SAP, retorna falha de negócio.
        - Somente falhas da automação, Selenium, iframe etc. são erros técnicos.
        """

        console.print("[SAP] Validando resultado da importação do XML...")

        mensagens_sucesso = [
            "edocument criado sem erros",
            "document criado sem erros",
            "criado sem erros",
            "already received",
            "importado com sucesso",
            "importada com sucesso",
            "documento importado",
            "document imported",
            "xml importado",
            "carregado com sucesso",
            "upload realizado com sucesso",
            "processado com sucesso",
            "successfully",
            "edocument created",
        ]

        # Mensagens típicas de rejeição/regra funcional do SAP.
        mensagens_falha_negocio = [
            "não encontrado",
            "nao encontrado",
            "não cadastr",
            "nao cadastr",
            "inexistente",
            "inválido",
            "invalido",
            "invalid",
            "rejeitado",
            "rejected",
            "não autorizado",
            "nao autorizado",
            "já existe",
            "ja existe",
            "duplicado",
            "divergência",
            "divergencia",
            "inconsistência",
            "inconsistencia",
            "obrigatório",
            "obrigatorio",
            "não informado",
            "nao informado",
            "sem cadastro",
            "bloqueado",
            "erro ao importar",
            "falha ao importar",
            "não foi possível processar",
            "nao foi possivel processar",
        ]

        # Textos de diálogos transitórios do SAP que não representam
        # sucesso nem falha funcional do processamento do XML.
        mensagens_intermediarias = [
            "a aplicação pretende carregar um arquivo para o sistema da sap",
            "a aplicacao pretende carregar um arquivo para o sistema da sap",
            "upload de arquivo",
        ]

        fim = datetime.now().timestamp() + timeout
        ultimo_texto = ""
        ultima_mensagem_relevante = ""
        repeticoes_mesma_mensagem = 0

        while datetime.now().timestamp() < fim:
            try:
                self.driver.switch_to.default_content()

                texto_tela = self.obter_texto_todos_frames()
                texto_normalizado = self.normalizar_texto_sap(texto_tela)

                if texto_normalizado:
                    ultimo_texto = texto_tela

                console.print(
                    f"[SAP][VALIDACAO] Texto capturado: {texto_normalizado[:700]}"
                )

                if any(
                    mensagem in texto_normalizado
                    for mensagem in mensagens_intermediarias
                ):
                    console.print(
                        "[SAP][VALIDACAO] Diálogo intermediário de upload "
                        "detectado. Aguardando o resultado definitivo..."
                    )
                    await worker_sleep(2)
                    continue

                # Sucesso deve ser validado primeiro porque
                # "criado sem erros" contém a palavra "erro".
                for msg_sucesso in mensagens_sucesso:
                    if msg_sucesso in texto_normalizado:
                        mensagem_relevante = self.extrair_mensagem_relevante_sap(
                            texto_tela
                        )

                        if "already received" in texto_normalizado:
                            return (
                                "XML já recebido/importado anteriormente no SAP. "
                                f"Arquivo: {self.nome_arquivo_config or 'não informado'}. "
                                f"Mensagem SAP: {mensagem_relevante}"
                            )

                        if (
                            "edocument criado sem erros" in texto_normalizado
                            or "document criado sem erros" in texto_normalizado
                            or "criado sem erros" in texto_normalizado
                        ):
                            return (
                                "eDocument criado sem erros no SAP. "
                                f"Arquivo: {self.nome_arquivo_config or 'não informado'}. "
                                f"Mensagem SAP: {mensagem_relevante}"
                            )

                        return (
                            "XML importado/processado com sucesso no SAP. "
                            f"Arquivo: {self.nome_arquivo_config or 'não informado'}. "
                            f"Mensagem SAP: {mensagem_relevante}"
                        )

                mensagem_relevante = self.extrair_mensagem_relevante_sap(texto_tela)
                mensagem_relevante_normalizada = self.normalizar_texto_sap(
                    mensagem_relevante
                )

                if (
                    mensagem_relevante
                    and mensagem_relevante != "Nenhuma mensagem SAP capturada."
                ):
                    if mensagem_relevante == ultima_mensagem_relevante:
                        repeticoes_mesma_mensagem += 1
                    else:
                        ultima_mensagem_relevante = mensagem_relevante
                        repeticoes_mesma_mensagem = 1

                encontrou_falha_negocio = any(
                    termo in texto_normalizado for termo in mensagens_falha_negocio
                )

                # Aguarda a mesma mensagem aparecer duas vezes para evitar
                # capturar texto transitório da tela.
                if encontrou_falha_negocio and repeticoes_mesma_mensagem >= 2:
                    raise FalhaNegocioSAP(
                        "Falha de negócio retornada pelo SAP. "
                        f"Arquivo: {self.nome_arquivo_config or 'não informado'}. "
                        f"Mensagem SAP: {mensagem_relevante}"
                    )

            except FalhaNegocioSAP:
                raise

            except Exception as e:
                # Erro de leitura temporário da tela não encerra a validação.
                console.print(f"[SAP][WARN] Erro ao validar resultado SAP: {e}")

            await worker_sleep(2)

        mensagem_final = self.extrair_mensagem_relevante_sap(ultimo_texto)
        mensagem_final_normalizada = self.normalizar_texto_sap(mensagem_final)

        encontrou_falha_negocio = any(
            termo in mensagem_final_normalizada for termo in mensagens_falha_negocio
        )

        if encontrou_falha_negocio:
            raise FalhaNegocioSAP(
                "Falha de negócio retornada pelo SAP. "
                f"Arquivo: {self.nome_arquivo_config or 'não informado'}. "
                f"Mensagem SAP: {mensagem_final}"
            )

        if any(
            mensagem in mensagem_final_normalizada
            for mensagem in mensagens_intermediarias
        ):
            raise RuntimeError(
                "O SAP permaneceu no diálogo intermediário de upload e não "
                "apresentou uma mensagem definitiva dentro do tempo limite. "
                f"Último texto capturado: {mensagem_final}"
            )

        raise RuntimeError(
            "O SAP não apresentou uma mensagem conclusiva de sucesso ou "
            "falha dentro do tempo limite. "
            f"Último texto capturado: {mensagem_final}"
        )

    def normalizar_texto_sap(self, texto: str) -> str:
        texto = str(texto or "").lower()
        texto = texto.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        texto = texto.replace("interromper", "")
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    def extrair_mensagem_relevante_sap(self, texto: str) -> str:
        texto = str(texto or "").strip()
        texto = texto.replace("\r", "\n")

        linhas = [linha.strip() for linha in texto.split("\n") if linha.strip()]

        palavras_chave = [
            "edocument criado sem erros",
            "document criado sem erros",
            "criado sem erros",
            "sem erros",
            "sem erro",
            "already received",
            "received",
            "sucesso",
            "success",
            "importado",
            "importada",
            "imported",
            "processado",
            "processed",
            "erro",
            "error",
            "falha",
            "failed",
            "rejeitado",
            "rejected",
            "inválido",
            "invalido",
            "invalid",
            "não encontrado",
            "nao encontrado",
            "não cadastrado",
            "nao cadastrado",
            "inexistente",
            "não autorizado",
            "nao autorizado",
            "obrigatório",
            "obrigatorio",
            "bloqueado",
            "duplicado",
            "já existe",
            "ja existe",
        ]

        linhas_relevantes = []

        for linha in linhas:
            linha_lower = linha.lower()

            if any(palavra in linha_lower for palavra in palavras_chave):
                linhas_relevantes.append(linha)

        if linhas_relevantes:
            return " | ".join(linhas_relevantes[:5])

        if linhas:
            return " | ".join(linhas[-5:])

        return "Nenhuma mensagem SAP capturada."

    def obter_texto_todos_frames(self) -> str:
        textos = []

        try:
            self.driver.switch_to.default_content()
            textos.append(self.driver.find_element(By.TAG_NAME, "body").text)
        except Exception:
            pass

        try:
            self.driver.switch_to.default_content()
            textos.extend(self._obter_texto_frames_recursivo())
        except Exception:
            pass

        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

        return "\n".join([t for t in textos if t])

    def _obter_texto_frames_recursivo(self) -> list:
        textos = []

        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)

                try:
                    textos.append(self.driver.find_element(By.TAG_NAME, "body").text)
                except Exception:
                    pass

                textos.extend(self._obter_texto_frames_recursivo())

                self.driver.switch_to.parent_frame()

            except Exception:
                try:
                    self.driver.switch_to.parent_frame()
                except Exception:
                    self.driver.switch_to.default_content()

        return textos

    # ==========================================================
    # JANELA WINDOWS ABRIR
    # ==========================================================
    async def selecionar_xml_no_dialogo_windows(self, caminho_xml: Path) -> bool:
        try:
            if pyautogui is None:
                raise RuntimeError(
                    "pyautogui não instalado. Execute: pip install pyautogui pyperclip"
                )

            caminho_xml = Path(caminho_xml).resolve()

            if not caminho_xml.exists():
                raise RuntimeError(f"Arquivo XML não existe: {caminho_xml}")

            console.print("[UPLOAD] Aguardando janela 'Abrir' do Windows...")
            await worker_sleep(2)

            console.print(f"[UPLOAD] Selecionando arquivo: {caminho_xml}")

            self.copiar_para_clipboard(str(caminho_xml))

            await worker_sleep(0.5)

            try:
                pyautogui.hotkey("alt", "n")
                await worker_sleep(0.3)
            except Exception:
                pass

            pyautogui.hotkey("ctrl", "v")
            await worker_sleep(0.5)

            pyautogui.press("enter")

            console.print("[UPLOAD] Caminho do XML enviado para o diálogo Windows.")
            await worker_sleep(5)

            return True

        except Exception as e:
            console.print(f"[UPLOAD][ERRO] Falha ao selecionar XML: {e}")
            console.print(traceback.format_exc())
            return False

    def copiar_para_clipboard(self, texto: str) -> None:
        if pyperclip:
            pyperclip.copy(texto)
            return

        import subprocess

        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Set-Clipboard -Value $args[0]",
                texto,
            ],
            check=True,
        )

    # ==========================================================
    # DEBUG
    # ==========================================================
    async def debug_inputs_shell(self) -> None:
        try:
            self.driver.switch_to.default_content()

            inputs = self.driver.find_elements(By.XPATH, "//input")
            console.print(f"[DEBUG] Total de inputs fora do iframe: {len(inputs)}")

            for idx, inp in enumerate(inputs[:30], start=1):
                try:
                    console.print(
                        f"[DEBUG][INPUT {idx}] "
                        f"id='{inp.get_attribute('id')}' | "
                        f"placeholder='{inp.get_attribute('placeholder')}' | "
                        f"value='{inp.get_attribute('value')}'"
                    )
                except Exception:
                    pass

        except Exception:
            pass

    async def debug_inputs_frame(self) -> None:
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input")
            spans = self.driver.find_elements(By.XPATH, "//span")
            divs = self.driver.find_elements(By.XPATH, "//div[@role='button']")

            console.print(f"[DEBUG_FRAME] Total inputs no iframe: {len(inputs)}")
            console.print(f"[DEBUG_FRAME] Total spans no iframe: {len(spans)}")
            console.print(f"[DEBUG_FRAME] Total div buttons no iframe: {len(divs)}")

            for idx, div in enumerate(divs[:50], start=1):
                try:
                    console.print(
                        f"[DEBUG_FRAME][BUTTON {idx}] "
                        f"id='{div.get_attribute('id')}' | "
                        f"title='{div.get_attribute('title')}' | "
                        f"aria-label='{div.get_attribute('aria-label')}' | "
                        f"class='{div.get_attribute('class')}' | "
                        f"lsdata='{div.get_attribute('lsdata')}' | "
                        f"text='{div.text}'"
                    )
                except Exception:
                    pass

        except Exception:
            pass


async def envio_xml_sap(task: RpaProcessoSapDTO) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando envio_xml_sap.")

    bot: Optional[EnvioXmlSAP] = None

    try:
        await kill_all_emsys()
        config = await get_config_by_name("SAP_Faturamento")
        base_url = config.conConfiguracao.get("baseUrl")

        bot = EnvioXmlSAP(task=task, base_url=base_url)

        return await bot.iniciar()

    except Exception as ex:
        tb = traceback.format_exc()
        msg = (
            f"Erro geral na automação SAP de envio/importação XML: "
            f"{type(ex).__name__}: {ex}\n{tb}"
        )

        console.print("[MAIN][ERRO] Exceção em envio_xml_sap.")
        console.print(tb)

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    finally:
        try:
            if bot and bot.driver:
                console.print("[MAIN] Fechando navegador.")
                bot.driver.quit()
                bot.driver = None
        except Exception:
            pass

        console.print("[MAIN] Fim do processo.")
