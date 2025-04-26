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
from worker_automate_hub.api.client import get_config_by_name, send_file
from worker_automate_hub.api.datalake_service import send_file_to_datalake
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum
)
from worker_automate_hub.models.dto.rpa_sap_dto import RpaProcessoSapDTO
from worker_automate_hub.utils.util import worker_sleep

console = Console()

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

console.print(f"Downloads dir: {DOWNLOADS_PATH}")

class ConfigEntradaSAP(BaseModel):
    user: str
    password: str
    empresa: str
    unique_id: Optional[str] = "default"

    def get(self, key, default=None):
        return getattr(self, key, default)

class NotasFaturamentoSAP:
    def __init__(self, task: RpaProcessoSapDTO, sap_url, sap_key, sap_token, base_url, directory):
        console.print("Inicializando classe NotasFaturamentoSAP.")
        self.task = task
        self.sap_url = sap_url
        self.sap_key = sap_key
        self.sap_token = sap_token
        self.user = task.configEntrada.get("user")
        self.password = task.configEntrada.get("password")
        self.base_url = base_url
        self.empresa = task.configEntrada.get("empresa")
        self.directory = directory
        self.unique_id = "default"
        self.driver = None

    async def start_sap_process(self):
        console.print("Iniciando o processo SAP.")
        sim_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=sim_service)
        self.driver.maximize_window()
        console.print("Driver inicializado e janela maximizada.")

        await self.save_process_pid()
        console.print("PID do processo salvo com sucesso.")
        self.driver.get(self.base_url)
        console.print(f"Acessando a URL base: {self.base_url}")
        await worker_sleep(3)

        if not await self.login():
            msg = f"Falha ao realizar login no SAP"
            console.print(msg)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        console.print("Login realizado com sucesso.")
        await self.download_files(self.empresa, "FAT")
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                console.print("Driver fechado e referência removida.")
            except Exception as e:
                msg = f"Erro ao fechar o driver: {e}"
                console.print(msg)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

    async def save_process_pid(self):
        try:
            console.print("Salvando o PID do processo do Chrome.")
            pid = str(self.driver.service.process.pid)
            file_path = f"c:\\tmp\\chrome_pid_{self.unique_id}.txt"
            with open(file_path, "w") as f:
                f.write(pid)
            console.print(f"PID salvo em: {file_path}")
        except Exception as e:
            msg = f"Erro ao salvar PID: {e}"
            console.print(msg)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

    async def login(self):
        try:
            console.print("Iniciando login no SAP.")
            for _ in range(30):
                inputs = self.driver.find_elements(By.CLASS_NAME, "loginInputField")
                if len(inputs) >= 2:
                    console.print("Campos de entrada de login encontrados.")
                    break
                await worker_sleep(1)

            inputs = self.driver.find_elements(By.CLASS_NAME, "loginInputField")
            inputs[0].send_keys(self.user)
            console.print("Usuário inserido no campo de login.")
            await worker_sleep(2)
            inputs[1].send_keys(self.password)
            console.print("Senha inserida no campo de login.")
            await worker_sleep(1)

            for _ in range(10):
                login_btn = self.driver.find_elements(By.ID, "LOGIN_SUBMIT_BLOCK")
                if login_btn:
                    login_btn[0].click()
                    console.print("Botão de login clicado.")
                    break
                await worker_sleep(1)

            await worker_sleep(3)
            console.print("Login realizado com sucesso.")
            return True
        except Exception as e:
            console.print(f"Erro ao realizar login: {e}")
            return False

    async def download_files(self, company: str, file_type: str):
        console.print(f"Iniciando download de arquivos para empresa {company} e tipo {file_type}.")
        doc_url = self.get_document_url(file_type)
        console.print(f"Acessando a URL do documento: {doc_url}")
        self.driver.get(doc_url)
        await worker_sleep(15)

        if len(self.driver.find_elements(By.ID, "searchFieldInShell-input-inner")) < 1:
            for _ in range(10):
                sf = self.driver.find_elements(By.ID, "sf")
                if sf:
                    sf[0].click()
                    console.print("Elemento 'sf' clicado.")
                    break
                await worker_sleep(1)

        for _ in range(10):
            if len(self.driver.find_elements(By.ID, "searchFieldInShell-input-inner")) > 0:
                console.print("Campo de busca encontrado.")
                break
            await worker_sleep(1)

        self.driver.find_element(By.ID, "searchFieldInShell-input-inner").click()
        console.print("Campo de busca clicado.")
        await worker_sleep(5)

        actions = ActionChains(self.driver)
        console.print("Executando ações para navegar pelos campos.")
        for _ in range(34):
            actions.send_keys(Keys.TAB)
            actions.perform()
            await worker_sleep(0.5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        await worker_sleep(5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        await worker_sleep(5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        await worker_sleep(15)
        console.print("Ações concluídas.")
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                console.print("Driver fechado e referência removida.")
            except Exception as e:
                msg = f"Erro ao fechar o driver: {e}"
                console.print(msg)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=msg,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
        await self.rename_file(company, file_type)

    def get_document_url(self, file_type: str) -> str:
        console.print(f"Obtendo URL do documento para o tipo {file_type}.")
        mapping = {
            "FAT": "#BillingDocument-analyzeRevenue?sap-ui-tech-hint=WDA",
            "DET": "#BillingDocument-analyzeBillingDocItemPricing?sap-ui-tech-hint=WDA",
            "PED": "#SalesOrder-analyzeIncoming?sap-ui-tech-hint=WDA",
        }
        suffix = mapping.get(file_type.upper(), "")
        return f"{self.base_url}{suffix}"

    async def rename_file(self, company: str, file_type: str):
        console.print("Arquivos baixados com sucesso")
        console.print("Iniciando renomeação e movimentação do arquivo.")
        try:
            current_path = os.path.join(DOWNLOADS_PATH, "export.xlsx")
            date_now = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{company}_{file_type}_{date_now}.xlsx"
            final_path = os.path.join(DOWNLOADS_PATH, filename)
            
            console.print(f"filename: {filename}")
            
            os.rename(current_path, final_path)
            console.print(f"Arquivo renomeado para {final_path}.")
            
            with open(final_path, 'rb') as file:
                file_bytes = io.BytesIO(file.read())
            
            await worker_sleep(5)

            await self.send_message_to_webhook(f"Arquivo gerado via RPA: {filename}")

            await worker_sleep(2)

            try:
                console.print(f"directory: {self.directory}")
                console.print(f"file: {final_path}")
                send_file_request = await send_file_to_datalake(self.directory, file_bytes, filename, "xlsx")
                console.print(send_file_request)
            except Exception as e:
                console.print(f"Erro ao enviar o arquivo: {e}", style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao enviar o arquivo: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            
            await worker_sleep(2)

            if final_path and os.path.exists(final_path):
                try:
                    os.remove(final_path)
                    console.print(f"Arquivo deletado: {final_path}")
                except Exception as e:
                    msg = f"Erro ao deletar o arquivo: {e}"
                    console.print(msg)
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=msg,
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                    )

        except FileNotFoundError as fne:
            msg = f"Não foi possível renomear o arquivo, error: {fne}"
            console.print(msg)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        except Exception as e:
            msg = f"Erro ao renomear/mover arquivo: {e}"
            console.print(msg)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

    async def send_message_to_webhook(self, message: str):
        console.print("Enviando mensagem ao webhook.")
        await worker_sleep(2)
        try:
            payload = {"text": "📢 " + message}
            webhook_url = f"{self.sap_url}/key={self.sap_key}&token={self.sap_token}"
            requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            console.print("Mensagem enviada ao webhook com sucesso.")
            await worker_sleep(2)
        except Exception as e:
            msg = f"Erro ao enviar mensagem ao webhook: {e}"
            console.print(msg)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

async def notas_faturamento_sap(task: RpaProcessoSapDTO) -> RpaRetornoProcessoDTO:
    console.print("Iniciando processo de notas de faturamento SAP.")
    try:
        config = await get_config_by_name("SAP_Faturamento")
        console.print(f"config: {config}")
        sap_url = config.conConfiguracao.get("sapUrl")
        sap_key = config.conConfiguracao.get("sapKey")
        sap_token = config.conConfiguracao.get("sapToken")
        base_url = config.conConfiguracao.get("baseUrl")
        directory = config.conConfiguracao.get("directoryBucket")
        console.print(sap_url, sap_key, sap_token, base_url, directory)
        notas_sap = NotasFaturamentoSAP(task, sap_url, sap_key, sap_token, base_url, directory)
        await notas_sap.start_sap_process()
        console.print("Processo de automação SAP finalizado com sucesso.")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo de automação SAP finalizado com sucesso.",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as ex:
        console.print(f"Erro na automação SAP: {ex}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na automação SAP: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
