import asyncio
import getpass
import warnings
import os
import re
import io
import json
from pathlib import Path
import uuid
import pandas as pd
import pyautogui
import pytesseract
from datetime import datetime, timedelta
from pywinauto.application import Application
from pypdf import PdfReader
from PIL import Image, ImageEnhance
from pywinauto.keyboard import send_keys
from pywinauto.mouse import double_click
import win32clipboard
from pywinauto_recorder.player import set_combobox
from rich.console import Console
from worker_automate_hub.api.datalake_service import send_file_to_datalake
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
    send_file,
)
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys
from worker_automate_hub.utils.util import (
    e_ultimo_dia_util,
    delete_xml,
    find_nop_divergence,
    find_warning_nop_divergence,
    ocr_warnings,
    ocr_by_class,
    nf_busca_nf_saida,
    pessoas_ativa_cliente_fornecedor,
    nf_devolucao_liquidar_cupom,
    gerenciador_nf_header,
    cadastro_pre_venda_header,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    kill_all_emsys,
    login_emsys,
    ocr_title,
    select_documento_type,
    set_variable,
    type_text_into_field,
    worker_sleep,
    post_partner,
    get_text_display_window,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()
emsys = EMSys()


async def open_contabil_processes():
    try:
        console.print("Abrindo EMSys Contabil...")
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil1.lnk")
        await worker_sleep(3)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil2.lnk")
        await worker_sleep(30)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil3.lnk")
        await worker_sleep(20)
        pyautogui.hotkey("win", "d")
        await worker_sleep(4)
        os.startfile("C:\\Users\\automatehub\\Desktop\\Contabil\\contabil4.lnk")
        await worker_sleep(2)
    except Exception as error:
        console.print(f"Error: {error}")


async def extracao_fechamento_contabil(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        # DEFINIR CONSTANTE DEFAULT PARA O ASSETS
        ASSETS_PATH = "assets"
        # Get config from BOF
        config = await get_config_by_name("login_emsys")

        console.print(task)

        # Seta config entrada na var nota para melhor entendimento
        periodo_inicial = task.configEntrada["periodoInicial"]
        periodo_final = task.configEntrada["periodoFinal"]

        # Definindo Variaveis com Escopo global
        data_hoje = datetime.today().strftime("%d/%m/%Y")
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # VERIFICANDO ENTRADA
        historico_id = task.historico_id
        if historico_id:
            console.print("Historico ID recuperado com sucesso...\n")
        else:
            console.print(
                "Não foi possivel recuperar o histórico do ID, não sendo possivel enviar os arquivo gerados como retorno...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel recuperar o histórico do ID, não sendo possivel enviar os arquivo gerados como retorno",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        try:
            multiplicador_timeout = int(float(task.sistemas[0].timeout))
            set_variable("timeout_multiplicador", multiplicador_timeout)
            await kill_all_emsys()
            await open_contabil_processes()
            config = await get_config_by_name("login_emsys_contabil")

            app = None
            max_attempts = 30
            console.print("Tentando encontrar janela de login...")
            for attempt in range(max_attempts):
                try:
                    app = Application(backend="win32").connect(
                        title="Selecione o Usuário para autenticação"
                    )
                    console.print("Janela encontrada!")
                    break
                except:
                    console.print("Janela ainda nao encontrada...")
                    await worker_sleep(2)
            if not app:
                console.print("Nao foi possivel encontrar a janela de login...")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro durante tentativa localizacao de janelas...",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            await emsys.verify_warning_and_error("Erro", "&Ok")
            await worker_sleep(10)
            pyautogui.click(x=1021, y=127)
            console.print("Logando...")
            await emsys.verify_warning_and_error("Erro", "&Ok")
            pyautogui.write(config.conConfiguracao.get("user"))
            pyautogui.press("enter")

            await worker_sleep(4)
            pyautogui.write(config.conConfiguracao.get("pass"))
            pyautogui.press("enter")
            await worker_sleep(10)

            main_window = None
            for attempt in range(max_attempts):
                main_window = Application().connect(title="EMSys [Contabil]")
                main_window = main_window.top_window()
                if main_window.exists():
                    console.print("Janela encontrada!")
                    break
                console.print("Janela ainda nao encontrada...")
                await worker_sleep(1)

            if not main_window:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro durante tentativa localizacao de janelas....",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            # Adicionando foco
            try:
                main_window.set_focus()
                console.print(f"Ativando janela: {main_window}")
            except Exception as error:
                console.print(f"Erro ao setar foco na janela: {main_window}")

            await worker_sleep(5)

            # Clicar em BAL
            console.print("Clicanco em BAL")
            pyautogui.click(x=450, y=94)

            await worker_sleep(5)

            ##### Janela Balancete #####

            console.log("Buscando janela Balancete")
            app = Application(backend="win32").connect(title="Balancete", found_index=0)
            main_window = app["Balancete"]

            # Inserir período inicial
            console.print("Inserindo Data Inicial")
            periodo_inicial_temp = periodo_inicial.replace("/", "")
            input_data_inicial = main_window.child_window(
                class_name="TRzEditDate", found_index=1
            ).click()

            await worker_sleep(1)

            type_text_into_field(
                text=periodo_inicial_temp,
                field=input_data_inicial,
                empty_before=False,
                chars_to_empty="0",
            )

            # Inserir período final
            console.print("Inserindo Data Final")
            periodo_final_temp = periodo_final.replace("/", "")
            input_data_final = main_window.child_window(
                class_name="TRzEditDate", found_index=0
            ).click()

            await worker_sleep(1)

            type_text_into_field(
                text=periodo_final_temp,
                field=input_data_final,
                empty_before=False,
                chars_to_empty="0",
            )
            console.print("Selecionar complemento")
            # Seleciona complemento
            select_complemento = main_window.child_window(
                class_name="TRzComboBox", found_index=0
            )
            select_complemento.select("Complemento")

            console.print("Marcar filiais")
            # Selecionar filiais
            chk_selecionar_filiais = main_window.child_window(
                title="Selecionar Filiais", class_name="TRzCheckBox"
            )
            chk_selecionar_filiais.click_input()

            await worker_sleep(1)

            console.print("Clicar em gerar relatório")
            # Clica no botão "Gerar Relatório"
            main_window.child_window(
                title="Gerar Relatório", class_name="TBitBtn"
            ).click()

            ###### Janela seleção de Empresas #####

            console.print("Clicar em selecionar todas as empresas")
            # Selecionar todas empresas
            pyautogui.click(x=673, y=613)

            await worker_sleep(2)

            # Clicar em ok
            app = Application(backend="win32").connect(
                class_name="TFrmSelecaoEmpresasRel", found_index=0
            )
            main_window = app["TFrmSelecaoEmpresasRel"]
            botao_ok = main_window.child_window(class_name="TBitBtn", found_index=1)
            botao_ok.click_input()
            await worker_sleep(1)

            ##### Janela de pré visualização do relatório
            while True:
                console.print("Aguardando janela de pré visualização")
                try:
                    app = Application(backend="win32").connect(
                        class_name="TFrmPreviewRelatorio", found_index=0
                    )
                    main_window = app["TFrmPreviewRelatorio"]
                    console.print("Janela encontrada!")
                    break
                except Exception:
                    await worker_sleep(10)

            await worker_sleep(5)

            console.print("Clicar no botão salvar")
            # Clicar  em Salvar
            pyautogui.click(x=50, y=35)

            await worker_sleep(3)

            ##### Janela Configuração para salvar arquivo #####
            app = Application(backend="win32").connect(
                class_name="TFrmRelatorioFormato"
            )

            # Pegando a janela principal
            main_window = app["TFrmRelatorioFormato"]

            console.print("Selecionar item Excel")
            # Selecionando o item "Excel"
            select_pdf = main_window.child_window(class_name="TComboBox")
            select_pdf.select("Excel")

            await worker_sleep(1)

            # Clicar no botão ok
            botao_ok = main_window.child_window(class_name="TBitBtn", found_index=1)
            botao_ok.click_input()

            await worker_sleep(5)

            ##### Janela Salvar para arquivo #####

            app = Application(backend="win32").connect(
                title="Salvar para arquivo", found_index=0
            )
            main_window = app["Salvar para arquivo"]
            date_now = datetime.now().strftime("%Y%m%d%H%M%S")
            data_inicial_arquivo = periodo_inicial.replace("/", "")
            data_final_arquivo = periodo_final.replace("/", "")

            # Caminho completo para Downloads
            nome_arquivo = f"C:\\Users\\{getpass.getuser()}\\Downloads\\balancete_{data_inicial_arquivo}_{data_final_arquivo}_{date_now}.XLS"

            console.print(f"Salvar arquivo: {nome_arquivo}")

            # Inserir nome do arquivo
            input_nome = main_window.child_window(class_name="Edit", found_index=0)
            type_text_into_field(
                nome_arquivo, input_nome, empty_before=False, chars_to_empty="0"
            )

            await worker_sleep(2)

            # Clicar em salvar
            botao_salvar = main_window.child_window(class_name="Button", found_index=0)
            botao_salvar.click_input()

            await worker_sleep(2)

            ##### Janela Print #####

            app = Application(backend="win32").connect(title="Print")
            main_window = app.window(title="Print")

            # localizar o ComboBox da impressora
            printer_combo = main_window.child_window(
                title_re="Microsoft.*", class_name="TComboBox"
            ).wrapper_object()

            # Selecionar o Microsoft Print to PDF
            printer_combo.select("Microsoft Print to PDF")

            await worker_sleep(3)

            # Seleciona diretamente o ComboBox correto
            select_xls = main_window.descendants(class_name="TComboBox")[2]  # índice 2
            select_xls.select("Excel File")

            # Clica no botão 'OK'
            main_window.child_window(title="OK", class_name="TButton").click()

            await worker_sleep(5)

            username = getpass.getuser()

            await worker_sleep(3)

            console.print("Criar arquivo JSON")

            arquivo_path = Path(nome_arquivo)
            # Altera a extensão para .XLS maiúsculo (caso o EMSys exporte assim)
            caminho_arquivo = arquivo_path.with_suffix(".XLS")
            # Altera a extensão final para .xls minúsculo
            caminho_ajustado = caminho_arquivo.with_suffix(".xls")
            nome_com_extensao = caminho_ajustado.name
            print(nome_com_extensao)
            # Renomeia o arquivo
            os.rename(caminho_arquivo, caminho_ajustado)

            console.print(f"Arquivo renomeado para: {caminho_ajustado}")
            # Caminho do arquivo
            arquivo = caminho_ajustado

            # Lê o Excel (linhas e colunas corretas)
            df = pd.read_excel(arquivo, skiprows=10, usecols=[1, 2, 10], header=None)

            # Renomeia as colunas
            df.columns = ["contaContabil", "contaMovimento", "valor"]

            # Filtra apenas as linhas com 'contaContabil' numérico
            df = df[pd.to_numeric(df["contaContabil"], errors="coerce").notnull()]

            # Converte 'contaContabil' para inteiro como string (ex: 123 -> "123")
            df["contaContabil"] = df["contaContabil"].astype(int).astype(str)

            # Converte a coluna 'valor' para float, ignorando erros
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)

            # Formata o valor como moeda brasileira
            df["valor"] = df["valor"].apply(
                lambda x: f"{x:,.2f}".replace(".", "X")
                .replace(",", ".")
                .replace("X", ",")
            )

            # Cria o JSON no formato final
            dados_json = {
                "balancete": {
                    "periodoInicial": periodo_inicial,
                    "periodoFinal": periodo_final,
                    "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                },
                "saldos": df.to_dict(orient="records"),
            }

            # Salva o JSON

            # Caminho completo do arquivo
            nome_sem_extensao = caminho_ajustado.stem
            full_path = f"C:\\Users\\{username}\\Downloads\\{nome_sem_extensao}.json"
            filename = os.path.basename(full_path)
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(dados_json, f, ensure_ascii=False, indent=2)

            # Exibe o JSON formatado
            console.print(json.dumps(dados_json, ensure_ascii=False, indent=2))

            await worker_sleep(3)
            sended_to_datalake = False
            console.print("Enviar arquivo para o Datalake")
            # Envia o JSON para o datalake
            directory = "balancete_contabil/raw"

            with open(full_path, "rb") as file:
                file_bytes = io.BytesIO(file.read())
            try:
                console.print("Enviando Json para data lake")
                await send_file_to_datalake(directory, file_bytes, filename, "json")
                sended_to_datalake = True
            except Exception as e:
                console.print(f"Erro ao enviar o arquivo: {e}", style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao enviar o arquivo: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            sended_to_bof = False
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
                console.print("Removendo arquivo JSON da pasta downloads")
                os.remove(full_path)
                sended_to_bof = True
            except Exception as e:
                result = f"Arquivo Balancete contábil gerado com sucesso, porém gerou erro ao realizar o envio para o backoffice {e} - Arquivo ainda salvo na dispositivo utilizado no diretório {caminho_arquivo} !"
                console.print(result, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=result,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            if sended_to_datalake and sended_to_bof:
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=json.dumps(dados_json),
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        except Exception as erro:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro durante o processo integração contabil, erro : {erro}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as ex:
        retorno = f"Erro Processo Fechamento Balancete: {str(ex)}"
        logger.error(retorno)
        console.print(retorno, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=retorno,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
