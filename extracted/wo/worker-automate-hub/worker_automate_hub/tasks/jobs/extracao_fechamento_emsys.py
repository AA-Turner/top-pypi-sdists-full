import asyncio
import getpass
from datetime import datetime
import pyperclip
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from rich.console import Console
import re
import io
import os
import time
import json
import pandas as pd
from pathlib import Path

from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import login_emsys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
    send_file,
)
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    delete_xml,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox
from worker_automate_hub.api.datalake_service import send_file_to_datalake

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

ASSETS_BASE_PATH = "assets"
emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


async def wait_aguarde_window_closed(app, timeout=180):
    console.print("Verificando existencia de aguarde...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            janela_topo = app.top_window()
            titulo = janela_topo.window_text()
            console.print(f"Título da janela no topo: {titulo}")
        except Exception as e:
            console.print(f"Erro ao obter janela do topo: {e}", style="bold red")
            titulo = ""

        # Verifica se há alertas de aviso ou erro e clica no botão OK
        await emsys.verify_warning_and_error("Aviso", "&Ok")

        # Aguarda um pouco antes de verificar de novo
        await worker_sleep(2)

        if "Relatório Extrato Bancário" in titulo:
            console.log("Fim de aguardando...")
            return
        else:
            console.log("Aguardando...")

    console.log("Timeout esperando a janela Aguarde...")


async def extracao_fechamento_emsys(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys")
        periodo_inicial = task.configEntrada["periodoInicial"]
        periodo_final = task.configEntrada["periodoFinal"]
        historico_id = task.historico_id
        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_35.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(
            config.conConfiguracao, app, task, filial_origem=1
        )

        if return_login.sucesso == True:
            type_text_into_field(
                "Rel. Extrato Bancário", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")

        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)

        ##### Janela Extrato Bancário #####

        # Clicar na lupa
        pyautogui.click(x=1077, y=351)

        await worker_sleep(2)

        # Armazenar os Mneumonico
        linhas = []
        vistos = set()
        ultima_linha = ""
        repeticoes = 0
        limite_repeticoes = 3
        max_linhas = 1000

        console.print("Iniciando leitura dos mnemônicos..")
        # Clicar na primeira linha
        pyautogui.click(x=698, y=467)

        await worker_sleep(2)

        # Percorrer todas as linhas
        for _ in range(max_linhas):
            send_keys("^c")
            await asyncio.sleep(0.5)
            linha = pyperclip.paste().strip()

            if not linha:
                print("[Aviso] Linha vazia detectada. Pulando...")
                send_keys("{DOWN}")
                await asyncio.sleep(0.3)
                continue

            if linha == ultima_linha:
                repeticoes += 1
                if repeticoes >= limite_repeticoes:
                    print("Fim detectado: linha repetida várias vezes.")
                    break
            else:
                repeticoes = 0

            if linha not in vistos:
                print(f"[{len(linhas)+1}] {linha}")
                linhas.append(linha)
                vistos.add(linha)

            ultima_linha = linha
            send_keys("{DOWN}")
            await asyncio.sleep(0.3)

        console.print("Números mnemônicos armazenados")
        # Extrair apenas o mnemônico da linha de dados após o cabeçalho
        mnemonicos_detalhados = []
        for linha in linhas:
            if "Mnemônico" in linha:
                partes = linha.split("\r\n")
                if len(partes) > 1:
                    dados = partes[1].split("\t")
                    if len(dados) >= 4:
                        mnemonico = dados[0].strip()
                        agencia = dados[1].strip()
                        conta = dados[2].strip()
                        banco = dados[3].strip()

                        mnemonicos_detalhados.append(
                            {
                                "mnemonico": mnemonico,
                                "agencia": agencia,
                                "conta": conta,
                                "banco": banco,
                            }
                        )

        ##### Janela  Buscar Mneumônico
        pyautogui.click(x=1196, y=650)

        saldos = []
        # Extrair apenas o mnemônico da linha de dados após o cabeçalho
        mnemonicos_detalhados = []
        clicou_conciliados = False
        inserir_periodo = False
        for linha in linhas:
            caminho_excel = ""
            filename = ""
            await worker_sleep(1)
            ##### Janela Relatório Extrato Bancário #####
            app = Application(backend="win32").connect(
                class_name="TFrmRelExtratoBancario", found_index=0
            )
            main_window = app["TFrmRelExtratoBancario"]

            # Inserir Mnemonico
            console.log("Iniciando  Baixa do XLS")
            if "Mnemônico" in linha:
                partes = linha.split("\r\n")
                if len(partes) > 1:
                    dados = partes[1].split("\t")
                    if len(dados) >= 4:
                        mnemonico = dados[0].strip()
                        agencia = dados[1].strip()
                        conta = dados[2].strip()
                        banco = dados[3].strip()

                        mnemonicos_detalhados.append(
                            {
                                "mnemonico": mnemonico,
                                "agencia": agencia,
                                "conta": conta,
                                "banco": banco,
                            }
                        )
            conta_movimento = f"{banco}/ AG {agencia}/ Conta {conta}"
            input_mnemonico = main_window.child_window(
                class_name="TDBIEditCode", found_index=0
            )
            console.print(f"Inserindo Mnemônico: {mnemonico}")
            type_text_into_field(
                text=mnemonico,
                field=input_mnemonico,
                empty_before=True,
                chars_to_empty="10",
            )
            await worker_sleep(1)

            send_keys("{TAB}")

            await worker_sleep(1)
            if not inserir_periodo:
                console.print("Inserindo perído inicial")
                # Inserir período inicial
                input_data_inicial = main_window.child_window(
                    class_name="TDBIEditDate", found_index=3
                )

                type_text_into_field(
                    text=periodo_inicial,
                    field=input_data_inicial,
                    empty_before=True,
                    chars_to_empty="10",
                )
                await worker_sleep(1)

                console.print("Inserindo perído final")
                input_data_final = main_window.child_window(
                    class_name="TDBIEditDate", found_index=2
                )

                type_text_into_field(
                    text=periodo_final,
                    field=input_data_final,
                    empty_before=True,
                    chars_to_empty="10",
                )
                inserir_periodo = True
                await worker_sleep(1)
            console.print("Marcando movimentos conciliados")
            # Marcar movimentos conciliados
            if not clicou_conciliados:
                chk_mov_conciliados = main_window.child_window(
                    class_name="TDBICheckBox", found_index=2
                ).click()

                await worker_sleep(2)

                console.print("Selecionar tipo Excel")
                # Selecionar Excel
                slc_excel = main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=0
                ).select("Excel")
                clicou_conciliados = True

            await worker_sleep(3)

            # Clicar em gerar relatório
            console.print("Clicar em gerar relatório")            
            btn_gerar_relatorio = main_window.child_window(class_name="TBitBtn", found_index=0).click_input()
            
            await worker_sleep(7)
            console.print("Verificar se existem dados")

            try:
                nao_existe_dados = fr"{ASSETS_BASE_PATH}\extracao_fechamento_emsys\nao_existem_dados.png"

                for tentativa in range(3):
                    console.print(f"Tentativa {tentativa + 1}: Clicar em 'Gerar Relatório'")
                 
                    btn_gerar_relatorio = main_window.child_window(class_name="TBitBtn", found_index=0)
                    if btn_gerar_relatorio.exists(timeout=5):
                        btn_gerar_relatorio.click_input()
                        await worker_sleep(5)

                        # Verifica se apareceu a imagem de "sem dados"
                        localizacao = pyautogui.locateOnScreen(
                            nao_existe_dados, confidence=0.9
                        )
                        if localizacao:
                            console.print(f"Nenhum dado para {mnemonico}")
                            valor = "0,00"

                            try:
                                app_sem_dados = Application(backend="win32").connect(
                                    title="Information", found_index=0
                                )
                                window_sem_dados = app_sem_dados["Information"]
                                botao_ok = window_sem_dados.child_window(
                                    class_name="TButton", found_index=0
                                ).click()
                            except Exception as e:
                                console.print(
                                    f"Erro ao fechar janela 'Information': {e}",
                                    style="bold red",
                                )

                            await worker_sleep(5)
                            break  

                        # Verifica se apareceu a janela "Salvar para arquivo"
                        try:
                            app_salvar = Application(backend="win32").connect(
                                title="Salvar para arquivo", found_index=0
                            )
                            main_window_salvar = app_salvar["Salvar para arquivo"]
                            console.print("Janela 'Salvar para arquivo' encontrada.")
                            break  # Janela encontrada, pode sair do loop
                        except:
                            console.print(
                                "Janela 'Salvar para arquivo' não encontrada.",
                                style="yellow",
                            )

                    else:
                        console.print(
                            "Botão 'Gerar Relatório' não encontrado.", style="bold red"
                        )
                        break
            except:      
                await worker_sleep(5)                   
                ##### Janela Salvar para arquivo #####
                console.print(f"Dados encontrados para {mnemonico}")
                app = Application(backend="win32").connect(
                    title="Salvar para arquivo", found_index=0
                )
                main_window = app["Salvar para arquivo"]
                date_now = datetime.now().strftime("%Y%m%d%H%M%S")
                data_inicial_arquivo = periodo_inicial.replace("/", "")
                data_final_arquivo = periodo_final.replace("/", "")

                # Caminho completo para Downloads
                nome_arquivo = f"C:\\Users\\{getpass.getuser()}\\Downloads\\fechamento_{data_inicial_arquivo}_{data_final_arquivo}_{date_now}.XLS"

                console.print(f"Salvar arquivo: {nome_arquivo}")

                # Inserir nome do arquivo
                console.print(f"Inserir caminho do arquivo: {nome_arquivo}")
                input_nome = main_window.child_window(class_name="Edit", found_index=0)
                type_text_into_field(
                    nome_arquivo, input_nome, empty_before=False, chars_to_empty="0"
                )

                await worker_sleep(2)

                console.print("Salvando o arquivo")
                # Clicar em salvar
                botao_salvar = main_window.child_window(
                    class_name="Button", found_index=0
                )
                botao_salvar.click_input()

                await worker_sleep(6)

                await wait_aguarde_window_closed(app)

                arquivo_path = Path(nome_arquivo)
                # Altera a extensão para .XLS
                caminho_arquivo = arquivo_path.with_suffix(".XLS")
                # Altera a extensão final para .xls minúsculo
                caminho_ajustado = caminho_arquivo.with_suffix(".xls")
                nome_com_extensao = caminho_ajustado.name
                print(nome_com_extensao)
                # Renomeia o arquivo
                os.rename(caminho_arquivo, caminho_ajustado)

                console.print(f"Arquivo renomeado para: {caminho_ajustado}")

                await worker_sleep(1)

                console.print("Extraindo os dados do Excel")

                # Envia o arquivo para o BOF
                df = pd.read_excel(caminho_ajustado, header=None, engine="xlrd")

                # Filtra onde a coluna Q (índice 16) contém "Total Geral"
                mask = (
                    df[16].astype(str).str.contains("Total Geral", case=False, na=False)
                )
                linha_subtot = df[mask].index

                valor = None

                if not linha_subtot.empty:
                    index_subtot = linha_subtot[0]
                    index_verificacao = index_subtot - 2

                    # Regex para aceitar apenas números, vírgulas, pontos e sinal de menos
                    padrao_numerico = re.compile(r"^-?[\d\.\,]+$")

                    while index_verificacao >= 0:
                        valor_bruto = str(df.at[index_verificacao, 23]).strip()

                        # Verifica se não contém letras, apenas caracteres numéricos válidos
                        if padrao_numerico.fullmatch(valor_bruto):
                            valor = (
                                valor_bruto  # Mantém exatamente como está na planilha
                            )
                            break

                        index_verificacao -= 1

                    if valor is not None:
                        console.print(f"Valor encontrado: {valor}")
                    else:
                        console.print(
                            "Nenhum valor numérico puro encontrado nas linhas anteriores."
                        )
                else:
                    console.print("Linha contendo 'Total Geral' não encontrada.")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro ao enviar o arquivo: {e}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            console.print("Adicionando dados no json")
            await worker_sleep(2)
            # Adiciona o item à lista de saldos
            saldos.append(
                {
                    "mnemonico": mnemonico,
                    "contaMovimento": conta_movimento,
                    "valor": valor,
                }
            )

            try:
                # lê o arquivo
                with open(f"{caminho_ajustado}", "rb") as file:
                    file_bytes = io.BytesIO(file.read())

                console.print("Enviar Excel para o BOF")
                # Envia o arquivo para o BOF
                try:
                    await send_file(
                        historico_id,
                        nome_com_extensao,
                        "xls",
                        file_bytes,
                        file_extension="xls",
                    )
                    console.print("Removendo arquivo XLS da pasta downloads")
                    os.remove(f"{caminho_ajustado}")

                except Exception as e:
                    console.print(f"Erro ao enviar o arquivo: {e}", style="bold red")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro ao enviar o arquivo: {e}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            except:
                pass
        console.print("Criando estrutura do Json")
        # Cria estrutura final do JSON
        dados_json = {
            "fechamento": {
                "periodoInicial": periodo_inicial,
                "periodoFinal": periodo_final,
                "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
            "saldos": saldos,
        }

        console.print("Salvando arquivo json")
        # Salva em arquivo
        filename = (
            f"fechamento_{data_inicial_arquivo}_{data_final_arquivo}_{date_now}.json"
        )
        caminho_downloads = os.path.join(os.environ["USERPROFILE"], "Downloads")
        full_path = os.path.join(
            caminho_downloads,
            f"fechamento_{data_inicial_arquivo}_{data_final_arquivo}_{date_now}.json",
        )

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=2)

        print(f"Arquivo JSON salvo em: {full_path}")

        console.print("Enviar arquivo para o Datalake")
        # Envia o JSON para o datalake
        directory = "balancete_contabil/raw"

        with open(full_path, "rb") as file:
            file_bytes = io.BytesIO(file.read())
        try:
            send_file_request = await send_file_to_datalake(
                directory, file_bytes, filename, "json"
            )
            os.remove(full_path)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=json.dumps(dados_json),
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        except Exception as e:
            console.print(f"Erro ao enviar o arquivo: {e}", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao enviar o arquivo: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro no processo Extração de fechamento Emsys: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    finally:
        print("fim")
