# IMPORT SELENIUM
import os
import sys
import time
import json
import asyncio
import shutil
from typing import List
from datetime import datetime
from rich.console import Console


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from os import name

# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(ROOT_PATH)

from worker_automate_hub.api.datalake_service import send_file_to_datalake
from worker_automate_hub.api.client import get_config_by_name
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
)
USERNAME = os.environ.get("USERNAME")
console = Console()

HISTORICO_ID = "e8ca47cf-c49b-437c-9028-50bcfa5fe021"

# Diretório/bucket no datalake onde os arquivos serão enviados
DATALAKE_DIRECTORY = "nielsen_arquivos/raw"

# Funcões Selenium


def aguardar_elemento_ser_clicavel_xpath(
    driver: WebDriver, xpath: str, tempo: int
) -> bool:
    aguardar = WebDriverWait(driver, tempo)
    return aguardar.until(EC.element_to_be_clickable((By.XPATH, xpath)))


def inserir_texto_por_letra_xpath(driver: WebDriver, xpath: str, texto: str):
    for letter in texto:
        driver.find_element(By.XPATH, xpath).send_keys(letter)
        time.sleep(0.1)


def inserir_texto_por_xpath(driver: WebDriver, xpath: str, texto: str):
    driver.find_element(By.XPATH, xpath).send_keys(texto)


def clicar_elemento_por_xpath(driver: WebDriver, xpath: str) -> None:
    driver.find_element(By.XPATH, xpath).click()


def busca_lista_elementos_por_xpath(driver: WebDriver, xpath: str) -> List[WebElement]:
    return driver.find_elements(By.XPATH, xpath)


def limpar_pasta_downloads(caminho: str, remover_pastas: bool = False):
    """
    Limpa a pasta de downloads utilizada pelo robô.

    Args:
        caminho (str): Caminho da pasta a ser limpa.
        remover_pastas (bool): Se True, remove também subpastas.
    """
    if not os.path.exists(caminho):
        console.print(f"Pasta não existe: {caminho}", style="yellow")
        return

    try:
        itens = os.listdir(caminho)

        if not itens:
            console.print("Pasta já estava vazia.", style="green")
            return

        for item in itens:
            item_path = os.path.join(caminho, item)

            try:
                # Remover arquivos
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    console.print(f"Arquivo removido: {item_path}", style="green")

                # Remover pastas (opcional)
                elif remover_pastas and os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                    console.print(f"Pasta removida: {item_path}", style="green")

            except Exception as e:
                console.print(
                    f"Não foi possível remover {item_path}: {e}",
                    style="bold red",
                )

        console.print("Limpeza concluída!", style="bold green")

    except Exception as e:
        console.print(f"Erro ao limpar pasta: {e}", style="bold red")


class ExtracaoDados:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.caminho_downloads = rf"C:\Users\{USERNAME}\Downloads"
        self.handles = []

    async def limpar_downloads(self):
        limpar_pasta_downloads(self.caminho_downloads, remover_pastas=False)

    async def abrir_site(self):
        await asyncio.sleep(2)
        try:
            console.print(
                "Iniciando navegador e acessando site da Nielsen...", style="cyan"
            )
            self.driver.get("https://web.na-mft.nielseniq.com/cfcc/bclient/index.jsp#/")
        except Exception as e:
            console.print(f"Erro ao abrir o site: {e}", style="bold red")
            raise

    # Lê credenciais via API usando RpaConfiguracao.conConfiguracao (JSON)
    async def load_config(self):
        try:
            config = await get_config_by_name("nielsen_credenciais")

            if config is None:
                raise Exception(
                    "get_config_by_name retornou None para 'nielsen_credenciais'."
                )

            # conConfiguracao é onde fica o conteúdo da configuração
            raw_valor = getattr(config, "conConfiguracao", None)
            if raw_valor is None:
                raise Exception(
                    "Objeto RpaConfiguracao não possui conteúdo em 'conConfiguracao'. "
                    f"Atributos disponíveis: {dir(config)}"
                )

            # Se for string JSON, fazer parse
            if isinstance(raw_valor, str):
                try:
                    valor_json = json.loads(raw_valor)
                except Exception as e_json:
                    raise Exception(
                        f"Falha ao fazer json.loads em conConfiguracao: {e_json}. "
                        f"valor bruto: {raw_valor}"
                    )
            # Se já vier como dict
            elif isinstance(raw_valor, dict):
                valor_json = raw_valor
            else:
                raise Exception(
                    f"Tipo inesperado em conConfiguracao: {type(raw_valor)}. "
                    "Esperado str (JSON) ou dict."
                )

            username = valor_json.get("usuario")
            password = valor_json.get("senha")

            if not username or not password:
                raise Exception(
                    "Usuário ou senha não encontrados no JSON da configuração. "
                    f"JSON: {valor_json}"
                )

            return username, password

        except Exception as e:
            console.print(
                f"Erro ao obter credenciais via get_config_by_name: {e}",
                style="bold red",
            )
            raise
    
    async def clicar_diretorio_principal(self, nome_diretorio: str):
        """
        Clica no diretório principal pelo nome, tentando vários seletores
        para não quebrar com mudanças pequenas de HTML.
        """

        # Possíveis XPaths para localizar o item
        xpaths_possiveis = [
            # 1) span com classe 'file' e texto exato
            f"//span[contains(@class, 'file') and normalize-space(text())='{nome_diretorio}']",

            # 2) elemento com title igual ao nome (span, a, td, etc.)
            f"//*[@title='{nome_diretorio}' and (self::span or self::a or self::td)]",

            # 3) tr que tenha aria-label contendo o nome
            f"//tr[contains(@aria-label, '{nome_diretorio}')]",

            # 4) Qualquer elemento com texto visível igual ao nome
            f"//*[normalize-space(text())='{nome_diretorio}']",
        ]

        elemento_encontrado = False
        ultimo_erro = None

        for xpath in xpaths_possiveis:
            try:
                print(f"Tentando localizar diretório com XPath: {xpath}")
                aguardar_elemento_ser_clicavel_xpath(self.driver, xpath, 20)
                clicar_elemento_por_xpath(self.driver, xpath)
                print(f"Diretório '{nome_diretorio}' clicado com sucesso usando XPath: {xpath}.")
                elemento_encontrado = True
                break
            except Exception as e:
                print(f"Não encontrado/clicável com esse XPath. Erro: {e}")
                ultimo_erro = e

        if not elemento_encontrado:
            raise RuntimeError(
                f"Não foi possível clicar no diretório '{nome_diretorio}' "
                f"com nenhum dos seletores. Último erro: {ultimo_erro}"
            )
    
    async def clicar_ultima_pasta(self, timeout: int = 20):

        wait = WebDriverWait(self.driver, timeout)

        # 1) Esperar o tbody da tabela ficar presente
        try:
            tbody = wait.until(
                EC.presence_of_element_located(
                    # tabela de listagem de arquivos/pastas
                    (By.CSS_SELECTOR, "table.cursor-pointer tbody, table.w-full.cursor-pointer.table-auto tbody")
                )
            )
        except TimeoutException:
            raise RuntimeError("Tabela de transfers não encontrada na página.")

        # 2) Pegar todas as linhas clicáveis
        # No HTML do TIBCO cada linha tem tabindex="0" e aria-label com o nome
        rows = tbody.find_elements(By.CSS_SELECTOR, "tr[tabindex='0'][aria-label]")

        # Filtra apenas as visíveis (caso tenha linha escondida)
        rows = [r for r in rows if r.is_displayed()]

        if not rows:
            raise RuntimeError("Nenhuma linha clicável encontrada na tabela.")

        # 3) Última linha da lista (mais recente)
        last_row = rows[-1]
        print("Última linha encontrada com aria-label:",
            last_row.get_attribute("aria-label"))

        # 4) Dentro da linha, tentamos clicar no elemento mais específico
        target = None
        try:
            # span com classe 'file' (texto do nome)
            target = last_row.find_element(By.CSS_SELECTOR, "span.file")
        except Exception:
            # fallback: qualquer span da primeira coluna de nome
            try:
                target = last_row.find_element(By.CSS_SELECTOR, "td span")
            except Exception:
                # fallback final: a própria <tr>
                target = last_row

        # 5) Garantir que o elemento está visível na tela
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", target
        )

        # 6) Esperar ficar clicável e clicar
        try:
            wait.until(EC.element_to_be_clickable(target))
        except TimeoutException:
            # se não ficar "clicável" oficialmente, ainda tentamos via JS
            print("⚠️ Elemento não ficou clicável pelo EC, tentando mesmo assim...")

        try:
            target.click()
        except Exception:
            # fallback robusto: clique via JavaScript
            self.driver.execute_script("arguments[0].click();", target)

        print("Última pasta/arquivo clicado com sucesso!")



    async def login_e_baixar(self):
        # limpa downloads antes de começar
        await self.limpar_downloads()

        # pega credenciais via API (async)
        username, password = await self.load_config()

        console.print("Realizando login na NielsenIQ...", style="cyan")

        # Inserir usuário
        xpath = "//input[@id='userid']"
        aguardar_elemento_ser_clicavel_xpath(self.driver, xpath, 30)
        inserir_texto_por_letra_xpath(self.driver, xpath, username)

        # Inserir senha
        xpath = "//input[@id='password']"
        inserir_texto_por_letra_xpath(self.driver, xpath, password)

        # Clicar em OK
        xpath = "//input[@id='button']"
        clicar_elemento_por_xpath(self.driver, xpath)

        time.sleep(2)

        # Clicar no diretório principal LA_BR_REDE_SIM_DO_SUL
        await self.clicar_diretorio_principal("LA_BR_REDE_SIM_DO_SUL")


        await asyncio.sleep(5)

        # ====== CLICAR NA PASTA COM O ÚLTIMO MÊS ======
        await self.clicar_ultima_pasta()
      
        await asyncio.sleep(5)

        # ====== BAIXAR OS ARQUIVOS DENTRO DA PASTA ======
                                
       # Localiza as linhas de arquivo na tabela atual (TIBCO MFT)
        xpath_linhas_arquivos = (
            "//table[contains(@class,'cursor-pointer') and "
            "contains(@class,'table-auto')]/tbody/tr[@tabindex='0']"
        )

        # Aguarda até 20 segundos pelo menos 1 linha da tabela aparecer
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath_linhas_arquivos))
        )

        linhas_arquivos = busca_lista_elementos_por_xpath(
            self.driver, xpath_linhas_arquivos
        )

        qtd_arquivos = len(linhas_arquivos)
        console.print(
            f"Total de linhas (arquivos visíveis): {qtd_arquivos}", style="cyan"
        )

        # Arquivos já existentes na pasta de download (baseline)
        conhecidos = set(os.listdir(self.caminho_downloads))

        for r in range(1, qtd_arquivos + 1):
            # Linha r
            xpath_linha = f"{xpath_linhas_arquivos}[{r}]"

            # Coluna Name: span com classe 'file' (link do arquivo)
            xpath_baixar = rf"{xpath_linha}//span[contains(@class, 'file')]"
            clicar_elemento_por_xpath(self.driver, xpath_baixar)
            
            await asyncio.sleep(1)

            # Esperar o download completar (sem .crdownload/.tmp)
            timeout_segundos = 180
            inicio = time.time()
            novos_arquivos = set()

            while time.time() - inicio < timeout_segundos:
                arquivos_atual = [
                    f
                    for f in os.listdir(self.caminho_downloads)
                    if not f.endswith(".crdownload") and not f.endswith(".tmp")
                ]
                novos = set(arquivos_atual) - conhecidos
                if novos:
                    novos_arquivos = novos
                    conhecidos.update(novos)
                    break
                await asyncio.sleep(1)

            if not novos_arquivos:
                console.print(
                    "Nenhum arquivo novo foi baixado dentro do tempo limite.",
                    style="bold red",
                )
                continue

            for arquivo_baixado in sorted(novos_arquivos):
                caminho_arquivo = os.path.join(self.caminho_downloads, arquivo_baixado)
                console.print(f"Arquivo baixado: {caminho_arquivo}", style="bold green")

                try:
                    with open(caminho_arquivo, "rb") as file:
                        file_bytes = file.read()

                    nome_arquivo = arquivo_baixado
                    ext = "doc"  # tipo lógico esperado pelo datalake

                    await send_file_to_datalake(
                        directory=DATALAKE_DIRECTORY,
                        file=file_bytes,
                        filename=nome_arquivo,
                        file_extension=ext,
                    )

                    os.remove(caminho_arquivo)
                    console.print(
                        f"Arquivo {nome_arquivo} enviado ao datalake e removido da pasta de download.",
                        style="bold green",
                    )

                except Exception as e:
                    result = (
                        f"Arquivo baixado com sucesso, porém erro ao enviar para o datalake: {e} "
                        f"- Arquivo mantido em {caminho_arquivo}"
                    )
                    console.print(result, style="bold red")


async def extracao_dados_nielsen(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Função principal para ser chamada pelo worker.
    """
    console.print("Iniciando processo de extração Nielsen...", style="bold cyan")
    driver = None
    await kill_all_emsys()
    try:
        service = Service(ChromeDriverManager().install())

        # === CONFIG PARA REMOVER POPUPS ===
        chrome_options = Options()
        chrome_prefs = {
            "profile.default_content_setting_values.notifications": 2,  # bloqueia notificações
            "profile.default_content_setting_values.automatic_downloads": 1,  # permite múltiplos downloads
            "download.prompt_for_download": False,  # não perguntar onde salvar
            "download.directory_upgrade": True,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        chrome_options.add_argument("--disable-popup-blocking")  # evita popups gerais
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        console.print("Driver Chrome inicializado e maximizado.", style="green")

        extracao = ExtracaoDados(driver)
        await extracao.abrir_site()
        await extracao.login_e_baixar()

        # Fecha o driver com segurança
        if driver:
            try:
                driver.quit()
                driver = None
                console.print("Driver fechado com sucesso.", style="green")
            except Exception as e:
                console.print(f"Erro ao fechar o driver: {e}", style="yellow")

        console.print(
            "Processo de extração Nielsen finalizado com sucesso.",
            style="bold green",
        )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo de extração Nielsen finalizado com sucesso.",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:
        console.print(f"Erro na automação Nielsen: {ex}", style="bold red")
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro na automação Nielsen: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

