import asyncio
import io
import os
import json
import shutil
from datetime import datetime
import requests
from pydantic import BaseModel
from typing import Optional
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import traceback

from worker_automate_hub.utils.credentials_manager import CredentialsManager  # para logs de exceção detalhados

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
from worker_automate_hub.models.dto.rpa_sap_dto import RpaProcessoSapDTO
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    worker_sleep,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
console.print(f"[INIT] Downloads dir: {DOWNLOADS_PATH}")

# ==========================
# CONFIGURAÇÕES / CONSTANTES
# ==========================


class ConfigEntradaSAP(BaseModel):
    """
    Modelo de referência para a configuração de entrada SAP.
    Agora empresa/relatorio são opcionais e têm default.
    """
    user: str
    password: str
    empresa: Optional[str] = "DIS"
    unique_id: Optional[str] = "default"
    relatorio: Optional[str] = "FAT"


def _get_from_config(config, key, default=None):
    """
    Helper para funcionar tanto com dict quanto com BaseModel (Pydantic ou similar).
    """
    if isinstance(config, dict):
        return config.get(key, default)
    return getattr(config, key, default)


# (Mantidos para possível uso futuro)
SAP_VIEWS = {}
COMPANY_FILTER = {}

def clear_downloads_folder():
    """
    Remove todos os ARQUIVOS da pasta Downloads do usuário.
    Não remove pastas internas.
    """
    try:
        console.print("[CLEAN] Limpando pasta Downloads...")

        for item in os.listdir(DOWNLOADS_PATH):
            full_path = os.path.join(DOWNLOADS_PATH, item)

            # apenas arquivos (evita excluir pastas do usuário)
            if os.path.isfile(full_path):
                try:
                    os.remove(full_path)
                    console.print(f"[CLEAN] Arquivo removido: {item}")
                except Exception as e:
                    console.print(f"[CLEAN][WARN] Não foi possível remover {item}: {e}")

        console.print("[CLEAN] Downloads limpo com sucesso!")

    except Exception as e:
        console.print(f"[CLEAN][ERRO] Falha ao limpar Downloads: {e}")
        console.print(traceback.format_exc())



class ListaDevolucoesSAP:
    def __init__(
        self,
        task: RpaProcessoSapDTO,
        sap_url: str,
        sap_key: str,
        sap_token: str,
        base_url: str,
        directory: str,
        relatorio_override: Optional[str] = None,
    ):
        console.print("[STEP 0.1] Inicializando classe ListaClientesSAP.")
        self.task = task
        self.sap_url = sap_url
        self.sap_key = sap_key
        self.sap_token = sap_token
        self.base_url = base_url
        self.directory = directory

        config = task.configEntrada  # pode ser dict ou BaseModel

        self.user = CredentialsManager().get_by_key("SAP_USER_BI")
        self.password = CredentialsManager().get_by_key("SAP_PASSWORD_BI")
        # self.user = _get_from_config(config, "user")
        # self.password = _get_from_config(config, "password")

        # empresa padrão DIS se não vier na config (não usamos no fluxo atual, mas deixei)
        self.empresa = _get_from_config(config, "empresa", "DIS") or "DIS"

        # relatorio default FAT (não usamos no fluxo atual, mas deixei)
        self.relatorio = (
            (relatorio_override or "").upper()
            or _get_from_config(config, "relatorio", "").upper()
            or getattr(task, "relatorio", "").upper()
            or "FAT"
        )

        self.unique_id = "default"
        self.driver = None

        console.print(
            f"[STEP 0.2] user={self.user} empresa={self.empresa} "
            f"relatorio={self.relatorio}"
        )

    async def start_sap_process(self) -> RpaRetornoProcessoDTO:
        """
        Fluxo principal do SAP com logs de etapa:
        - KILL_ALL_EMSYS
        - INIT_CHROMEDRIVER
        - INIT_WEBDRIVER
        - VALIDATE_CONFIG
        - SAVE_PID
        - GET_BASE_URL
        - LOGIN
        - CLICK_EXIBIR_LISTA_CLIENTES
        - EXPORTAR_LISTA_CLIENTES
        """
        step = "INIT"
        console.print("[STEP] Iniciando o processo SAP.")

        try:
            # 0) Validar config básica
            step = "VALIDATE_CONFIG"
            if not self.user or not self.password:
                msg = f"[{step}] Credenciais SAP inválidas: user={self.user} password={'***' if self.password else None}"
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

            # 1) Matar instâncias antigas
            step = "KILL_ALL_EMSYS"
            console.print(f"[STEP={step}] Matando instâncias EMsys/Chrome antigas...")
            await kill_all_emsys()
            console.print(f"[STEP={step}] kill_all_emsys concluído.")

            clear_downloads_folder()
            console.print("[CLEAN] Downloads limpo antes da exportação.")

            # 2) Instalar ChromeDriver
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
                msg = f"Falha ao realizar login no SAP (etapa {step})"
                console.print(f"[STEP={step}] {msg}")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            console.print(f"[STEP={step}] Login realizado com sucesso.")

            # 7) Clicar na tela inicial: "Exibir lista de clientes"
            step = "EXIBIR PARTIDAS INDIVIDUAIS NO RAZÃO"
            try:
                console.print(f"[STEP={step}] Procurando botão 'Exibir partidas individuais no razão' na home...")
                await worker_sleep(5)  # tempo para a tela inicial carregar

                
                # Tenta com aproximação que ignora soft-hyphen
                botao_exibir = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//span[contains(translate(normalize-space(.), '­', ''), 'Exibir partidas individuais')]",
                        )
                    )
                )
        

                botao_exibir.click()
                console.print(f"[STEP={step}] Botão 'Exibir lista de clientes' clicado com sucesso!")
                await worker_sleep(5)

            except Exception as e:
                console.print(f"[STEP={step}][ERRO] Não foi possível clicar em 'Exibir lista de clientes': {e}")
                console.print("[STEP={step}] Abortando processo.")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao clicar em 'Exibir lista de clientes': {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            # 8) Fluxo simples de exportação (Início + Exportar)
            step = "EXPORTAR_PARTIDAS_INDIVIDUAIS_NO_RAZÃO"
            console.print(f"[STEP={step}] Iniciando fluxo de exportação da lista de clientes...")
            await self.exportar_devolucoes()
            console.print(f"[STEP={step}] Exportação concluída com sucesso.")

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
                    f"[LOGIN] Tentativa {i+1}/30 - qtd campos encontrados: {len(inputs)}"
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
                    f"[LOGIN] Tentativa {i+1}/10 - btn login encontrado? {bool(login_btn)}"
                )
                if login_btn:
                    login_btn[0].click()
                    console.print("[LOGIN] Botão de login clicado.")
                    break
                await worker_sleep(1)

            await worker_sleep(3)
            console.print("[LOGIN] Login finalizado (sem exceção).")
            return True
        except Exception as e:
            console.print("[LOGIN][ERRO] Exceção ao realizar login.")
            console.print(f"[LOGIN][ERRO] Tipo: {type(e).__name__}")
            console.print(f"[LOGIN][ERRO] str(e): {str(e)}")
            console.print("[LOGIN][ERRO] Traceback:")
            console.print(traceback.format_exc())
            return False

    async def wait_for_xlsx_download(self, timeout_seconds=600):
        """
        Espera até 10 minutos por algum arquivo .xlsx aparecer nos Downloads.
        """
        console.print("[DW] Aguardando arquivo XLSX aparecer na pasta Downloads...")
        start = datetime.now()

        while (datetime.now() - start).total_seconds() < timeout_seconds:
            for file in os.listdir(DOWNLOADS_PATH):
                if file.lower().endswith(".xlsx"):
                    full_path = os.path.join(DOWNLOADS_PATH, file)
                    console.print(f"[DW] Arquivo encontrado: {full_path}")
                    return full_path

            await worker_sleep(2)

        raise TimeoutError("Nenhum arquivo XLSX encontrado após 10 minutos.")

    async def exportar_devolucoes(self):
        console.print("[EXP] Iniciando passos de 'Início' e 'Exportar'...")
        try:
            # Clicar em "Início"
            console.print("[EXP] Procurando botão 'Início'...")
            botao_inicio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//bdi[contains(normalize-space(.), 'Iniciar')]")
                )
            )
            botao_inicio.click()
            console.print("[EXP] Botão 'Iniciar' clicado.")
            await worker_sleep(5)

            # Clicar em "Exportar" (botão)
            console.print("[EXP] Localizando botão de Exportar...")
            botao_exportar = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Abrir menu']"))
            )
            botao_exportar.click()
            console.print("[EXP] Botão 'Exportar' clicado.")

            await worker_sleep(3)

            # Clicar na opção "Exportar" do menu
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            console.print("[EXP] Opção 'Exportar' clicada.")

            try:
                # Clicar em "Exportar" para baixar
                console.print("[EXP] Clicarndo no botao 'Exportar para baixar...")
                botao_exportar = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//bdi[text()='Exportar']"))
                )
                botao_exportar.click()
                console.print("[EXP] Botão 'Exportar' clicado.")
            except:
                pass
   
            # AQUI — aguarda até 10 MIN pelo arquivo
            arquivo_baixado = await self.wait_for_xlsx_download()
            console.print(f"[EXP] Download concluído! Arquivo: {arquivo_baixado}")

            console.print("[EXP] Chamando rename_file...")
            await self.rename_file()
            console.print("[EXP] rename_file concluído.")

        except Exception as e:
            console.print("[EXP][ERRO] Exceção em exportar_devolucoes.")
            console.print(f"[EXP][ERRO] Tipo: {type(e).__name__}")
            console.print(f"[EXP][ERRO] str(e): {str(e)}")
            console.print("[EXP][ERRO] Traceback:")
            console.print(traceback.format_exc())
            raise

    async def rename_file(self):
        console.print("[RF] Iniciando renomeação e movimentação do arquivo.")
        try:
            # === 1) Localizar qualquer XLSX nos downloads ===
            xlsx_files = [
                os.path.join(DOWNLOADS_PATH, f)
                for f in os.listdir(DOWNLOADS_PATH)
                if f.lower().endswith(".xlsx")
            ]

            if not xlsx_files:
                msg = "[RF][ERRO] Nenhum arquivo XLSX encontrado na pasta Downloads."
                console.print(msg)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            # pega o arquivo mais recente
            current_path = max(xlsx_files, key=os.path.getmtime)

            console.print(f"[RF] Arquivo encontrado: {current_path}")

            # === 2) Criar nome SIM_DEV + timestamp ===
            date_now = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"SIM_DEV_{date_now}.xlsx"
            final_path = os.path.join(DOWNLOADS_PATH, filename)

            console.print(f"[RF] Novo filename: {filename}")

            # === 3) Renomear ===
            os.rename(current_path, final_path)
            console.print(f"[RF] Arquivo renomeado para {final_path}.")

            # === 4) Ler conteúdo para envio ===
            with open(final_path, "rb") as file:
                file_bytes = io.BytesIO(file.read())

            await worker_sleep(2)

            # === 5) Enviar para o datalake ===
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
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao enviar o arquivo: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            await worker_sleep(1)

            # === 6) Deletar arquivo final após envio ===
            if os.path.exists(final_path):
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

        except Exception as e:
            msg = f"Erro ao manipular arquivo XLSX: {e}"
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


async def lista_devolucoes_sap(task: RpaProcessoSapDTO) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando processo de lista de clientes SAP.")
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

        # PEGAR RELATORIO DE FORMA SEGURA (default FAT – não interfere no fluxo atual)
        relatorio = None
        config_entrada = task.configEntrada

        if isinstance(config_entrada, dict):
            relatorio = config_entrada.get("relatorio")
        else:
            relatorio = getattr(config_entrada, "relatorio", None)

        if not relatorio:
            relatorio = "FAT"

        console.print(f"[MAIN] Relatório usado: {relatorio}")

        notas_sap = ListaDevolucoesSAP(
            task,
            sap_url,
            sap_key,
            sap_token,
            base_url,
            directory,
            relatorio_override=relatorio,
        )

        console.print("[MAIN] Chamando start_sap_process...")
        resultado = await notas_sap.start_sap_process()
        console.print(f"[MAIN] Resultado do start_sap_process: sucesso={resultado.sucesso}")

        return resultado

    except Exception as ex:
        console.print("[MAIN][ERRO] Exceção em lista_clientes_sap.")
        console.print(f"[MAIN][ERRO] Tipo: {type(ex).__name__}")
        console.print(f"[MAIN][ERRO] str(ex): {str(ex)}")
        console.print("[MAIN][ERRO] Traceback completo:")
        console.print(traceback.format_exc())
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na automação SAP: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    finally:
        if notas_sap and notas_sap.driver:
            console.print("[MAIN] Fechando driver no final do processo.")
            notas_sap.driver.quit()
        console.print("[MAIN] Fim do processo (finally).")

