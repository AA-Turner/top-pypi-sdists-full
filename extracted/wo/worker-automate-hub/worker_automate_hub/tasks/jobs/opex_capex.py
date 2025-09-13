import difflib
import getpass
import os
import re
import warnings
import time
import uuid
from datetime import datetime, timedelta
import pyautogui
import pytesseract
import win32clipboard
from PIL import Image, ImageEnhance
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
from pywinauto_recorder.player import set_combobox
from rich.console import Console
import sys
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","..")))
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
    get_dados_nf_emsys,
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
from worker_automate_hub.utils.util import (
    cod_icms,
    delete_xml,
    error_after_xml_imported,
    get_xml,
    import_nfe,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_all_emsys,
    login_emsys,
    rateio_despesa,
    select_documento_type,
    set_variable,
    tipo_despesa,
    type_text_into_field,
    warnings_after_xml_imported,
    worker_sleep,
    zerar_icms,
    check_nota_importada,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()

async def get_ultimo_item():
    send_keys("^({END})")
    await worker_sleep(2)
    send_keys("+{F10}")
    await worker_sleep(1)
    send_keys("{DOWN 2}")
    await worker_sleep(1)
    send_keys("{ENTER}")
    await worker_sleep(2)
    app = Application().connect(title="Alteração de Item")
    main_window = app["Alteração de Item"]
    main_window.set_focus()
    edit = main_window.child_window(class_name="TDBIEditCode", found_index=0)
    index_ultimo_item = int(edit.window_text())
    try:
        btn_cancelar = main_window.child_window(title="&Cancelar")
        btn_cancelar.click()
    except Exception as error:
        btn_cancelar = main_window.child_window(title="Cancelar")
        btn_cancelar.click()
        console.print(f"Erro ao realizar get_ultimo_item: {error}")
    await worker_sleep(1)
    return index_ultimo_item    

async def opex_capex(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza entrada de notas no ERP EMSys(Linx ).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()
        data_atual = datetime.now().strftime("%d/%m/%Y")
        print(data_atual)       
        # Buscar número da nota
        numero_nota = nota.get("numeroNota")
        serie_nota = nota.get("serieNota")
        filial_nota = nota.get("descricaoFilial")
        filial_nota = filial_nota.split("-")[0].strip()
        centro_custo = nota.get("centroCusto")
        centro_custo = centro_custo.split("-")[0].strip().lstrip("0")

        try:
            dados_nf = await get_dados_nf_emsys(
                numero_nota=numero_nota,
                serie_nota=serie_nota,
                filial_nota=filial_nota
            )

            # Se a API retornou erro
            if isinstance(dados_nf, dict) and "erro" in dados_nf:
                console.print("Erro retornado pela API:", dados_nf["erro"])
                nf_chave_acesso = None

            # Se retornou lista mas está vazia
            elif isinstance(dados_nf, list) and not dados_nf:
                console.print("Nenhum dado encontrado para a nota.")
                nf_chave_acesso = None

            # Se retornou lista com dados
            else:
                nf_chave_acesso = dados_nf[0].get("chaveNfe")
                console.print("Chave da NF:", nf_chave_acesso)

        except Exception as e:
            console.print("Erro inesperado ao buscar nota:", str(e))
            nf_chave_acesso = None

        # Download XML
        console.log("Realizando o download do XML..\n")
        await save_xml_to_downloads(nf_chave_acesso)

        status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)

        empresa_codigo = dados_nf[0]["empresaCodigo"]
        cfop = dados_nf[0]["numeroDoCfop"]
        cfops_itens = [item["cfopProduto"] for item in dados_nf[0]["itens"]]


        
        if status_nf_emsys.get("status") == "Lançada":
            console.print(
                "\\Nota fiscal já lançada, processo finalizado...", style="bold green"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Nota fiscal já lançada",
                status=RpaHistoricoStatusEnum.Descartado,
            )
        else:
            console.print("\\Nota fiscal não lançada, iniciando o processo...")
        
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_29.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task, filial_origem = empresa_codigo)

        if return_login.sucesso == True:
            type_text_into_field(
                "Nota Fiscal de Entrada", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)

        # Procura campo documento
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        document_type = await select_documento_type(
            "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE"
        )
        if document_type.sucesso == True:
            console.log(document_type.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=document_type.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(4)

        # Clica em 'Importar-Nfe'
        imported_nfe = await import_nfe()
        if imported_nfe.sucesso == True:
            console.log(imported_nfe.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=imported_nfe.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(5)

        await get_xml(nf_chave_acesso)
        

        await worker_sleep(3)

        # VERIFICANDO A EXISTENCIA DE WARNINGS
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            warning_work = await warnings_after_xml_imported()
            if warning_work.sucesso == True:
                console.log(warning_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=warning_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            error_work = await error_after_xml_imported()
            return RpaRetornoProcessoDTO(
                sucesso=error_work.sucesso,
                retorno=error_work.retorno,
                status=error_work.status,
                tags=error_work.tags
            )

        app = Application().connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        # INTERAGINDO COM A NATUREZA DA OPERACAO
        console.print(f"Inserindo a informação da CFOP: {cfop} ...\n")
        combo_box_natureza_operacao = main_window.child_window(
            class_name="TDBIComboBox", found_index=0
        )
        combo_box_natureza_operacao.click()

        await worker_sleep(3)
        # Mapeamento CFOP -> (lista, código exibido no combobox)
        cfop_map = {
            "1556": (['5101', '5102', '5103', '5104'], "1.556"),
            "1407": (['5401', '5403', '5404', '5405'], "1.407"),
            "2407": (['6104', '6401', '6403', '6405'], "2.407")
        }

        cfop_str = str(cfop)
        for key, (lista, codigo_combo) in cfop_map.items():
            if cfop_str in lista:
                for opc in combo_box_natureza_operacao.item_texts():
                    if (f"{key}-COMPRA DE MERCADORIAS SEM ESTOQUE" in opc 
                        and str(codigo_combo) in opc):
                        combo_box_natureza_operacao.select(opc)
                        send_keys("{ENTER}")
                        break
                break

        else:
            console.print(
                "Erro mapeado, CFOP diferente de início com 540 ou 510, necessário ação manual ou ajuste no robô...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro mapeado, CFOP diferente de início com 540 ou 510, necessário ação manual ou ajuste no robô.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )
        
        await worker_sleep(3)

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        fornecedor = dados_nf[0]["fornecedorNome"]
        empresaCodigo = dados_nf[0]["empresaCodigo"]
        console.print(
            f"Inserindo a informação do Almoxarifado {empresaCodigo} ...\n"
        )
        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
            edit = window.child_window(
                class_name="TDBIEditCode", found_index=3, control_type="Edit"
            )
            if empresa_codigo == '1':
                valor_almoxarifado = empresaCodigo + "60"
            else:
                valor_almoxarifado = empresaCodigo + "50"
            edit.set_edit_text(valor_almoxarifado)
            edit.type_keys("{TAB}")
        except Exception as e:
            console.print(f"Erro ao iterar itens de almoxarifado: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao iterar itens de almoxarifado: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(1)
        console.print("Inserir conta contábil")
        despesa = nota.get('contaContabil')
        despesa = despesa.split("-")[0].strip()
        tipo_despesa_work = await tipo_despesa(despesa)
        if tipo_despesa_work.sucesso == True:
            console.log(tipo_despesa_work.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=tipo_despesa_work.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        await worker_sleep(5)
        
        try:
            console.print("Verificando se existe o tipo de despesa...")
            # Conectar à aplicação
            app = Application(backend="win32").connect(class_name="TFrmBuscaGeralDialog")

            # Acessar a janela buscar 
            janela = app.window(class_name="TFrmBuscaGeralDialog")
            janela.set_focus()
            # Clicar em canelar
            janela.child_window(title="&Cancelar", class_name="TBitBtn").click()
            console.print("Tipo de despesa não encontrado")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Tipo de Despesa / conta contábil não localizado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )
        except:
            pass
        # INTERAGINDO COM O CHECKBOX ZERAR ICMS
        checkbox_zerar_icms = await zerar_icms()
        if checkbox_zerar_icms.sucesso == True:
            console.log(checkbox_zerar_icms.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=checkbox_zerar_icms.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        # INTERAGINDO COM O CAMPO DE CODIGO DO ICMS
        if key =='1556':
            codigo_icms = '33'
        else:
            codigo_icms = '20'
        cod_icms_work = await cod_icms(codigo_icms)
        if cod_icms_work.sucesso == True:
            console.log(cod_icms_work.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=cod_icms_work.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        # INTERAGINDO COM O CAMPO Manter Natureza de Operação selecionada
        console.print(
            f"Selecionando a opção 'Manter Natureza de Operação selecionada'...\n"
        )
        checkbox = window.child_window(
            title="Manter Natureza de Operação selecionada",
            class_name="TDBICheckBox",
        )
        if not checkbox.get_toggle_state() == 1:
            checkbox.click()
            console.print(
                "A opção 'Manter Natureza de Operação selecionada' selecionado com sucesso... \n"
            )

        await worker_sleep(2)
        console.print("Clicando em OK... \n")

        max_attempts = 3
        i = 0
        while i < max_attempts:
            console.print("Clicando no botão de OK...\n")
            try:
                try:
                    btn_ok = main_window.child_window(title="Ok")
                    btn_ok.click()
                except:
                    btn_ok = main_window.child_window(title="&Ok")
                    btn_ok.click()
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")

            await worker_sleep(3)

            console.print(
                "Verificando a existencia da tela Informações para importação da Nota Fiscal Eletrônica...\n"
            )

            try:
                informacao_nf_eletronica = await is_window_open(
                    "Informações para importação da Nota Fiscal Eletrônica"
                )
                if not informacao_nf_eletronica["IsOpened"]:
                    console.print(
                        "Tela Informações para importação da Nota Fiscal Eletrônica fechada, seguindo com o processo"
                    )
                    break
            except Exception as e:
                console.print(
                    f"Tela Informações para importação da Nota Fiscal Eletrônica encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        if i == max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Número máximo de tentativas atingido, Não foi possivel finalizar os trabalhos na tela de Informações para importação da Nota Fiscal Eletrônica",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(10)

        try:
            console.print("Verificando itens não localizados ou NCM...\n")
            itens_by_supplier = await is_window_open_by_class("TFrmAguarde", "TMessageForm")

            if itens_by_supplier["IsOpened"] == True:
                itens_by_supplier_work = await itens_not_found_supplier(nota.get("nfe"))

                if not itens_by_supplier_work.sucesso:
                    return itens_by_supplier_work

        except Exception as error:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao verificar a existência de POP-UP de itens não localizados: {error}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(10)
                
        # Clicar em itens da nota
        imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\worker_automate_hub\assets\entrada_notas\intens_nota.png"

        # Tenta localizar a imagem na tela
        while True:
            local = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)  # 0.8 = 80% de precisão
            if local:
                pyautogui.click(local)   # Clica no centro da imagem
                print("Imagem encontrada e clicada!")
                break
            else:
                print("Imagem não encontrada, tentando novamente...")
                time.sleep(1)

        await worker_sleep(3)
        # Clicar em itens da nota
        pyautogui.click(791, 379)
        await worker_sleep(2)
        index_item_atual = 0
        index_ultimo_item = await get_ultimo_item()
        console.print(f"Index ultimo item: {index_ultimo_item}")
        
        try:
            while index_item_atual < index_ultimo_item:
                send_keys("^({HOME})")
                await worker_sleep(1)

                if index_item_atual > 0:
                    send_keys("{DOWN " + str(index_item_atual) + "}")

                await worker_sleep(2)
                send_keys("+{F10}")
                await worker_sleep(1)
                send_keys("{DOWN 2}")
                await worker_sleep(1)
                send_keys("{ENTER}")

                await worker_sleep(2)
                app = Application().connect(title="Alteração de Item")
                main_window = app["Alteração de Item"]

                main_window.set_focus()

                edit = main_window.child_window(
                    class_name="TDBIEditCode", found_index=0
                )
                index_item_atual += 1
                console.print(f"Item aual no final da execução: {index_item_atual}")
                await worker_sleep(1)
                # Listas
                lista_icms_090 = ["5101", "5102", "5103", "5104"]
                lista_icms_060 = ["5401", "5403", "5404", "5405", "6104", "6401", "6403", "6404", "6405"]

                # Conecta à janela
                app = Application().connect(class_name="TFrmAlteraItemNFE")
                main_window = app["TFrmAlteraItemNFE"]
                main_window.set_focus()


                # Localiza o combobox

                tipo_icms = main_window.child_window(class_name="TDBIComboBox", found_index=5)

                # Define o texto da opção desejada
                if cfop in lista_icms_090:
                    opcao_desejada = "090 - ICMS NACIONAL OUTRAS"
                elif cfop in lista_icms_060:
                    opcao_desejada = "060 - ICMS - SUBSTITUICAO TRIBUTARIA 060"
                else:
                    opcao_desejada = None

                # Seleciona no combobox
                if opcao_desejada:
                    try:
                        tipo_icms.select(opcao_desejada)
                        send_keys("{ENTER}")
                    except Exception as e:
                        print(f"Erro ao selecionar opção: {e}")
                            
                    # Clicar em alterar
                    main_window.child_window(class_name="TDBIBitBtn", found_index=3).click()
                await worker_sleep(5)
        except Exception as e:
            return {
                "sucesso": False,
                "retorno": f"Erro aotrabalhar nas alterações dos itens: {e}",
            }
       
        await worker_sleep(10)
        
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        # Clicar em pagamentos
        imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\worker_automate_hub\assets\entrada_notas\pagamentos.png"

        # Tenta localizar a imagem na tela
        while True:
            local = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)  # 0.8 = 80% de precisão
            if local:
                pyautogui.click(local)   # Clica no centro da imagem
                print("Imagem encontrada e clicada!")
                break
            else:
                print("Imagem não encontrada, tentando novamente...")
                time.sleep(1)

        await worker_sleep(3)

        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TPageControl")

        panel_TabPagamento = panel_TTabSheet.child_window(title="Pagamento")

        tipo_cobranca = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=0
        )
        tipo_cobranca.click()
        # Lista de opções em ordem de prioridade
        opcoes = [
            "BANCO DO BRASIL BOLETO FIDC",
            "BANCO DO BRASIL BOLETO",
            "BOLETO"
        ]

        # Vamos percorrer o combo com setas
        max_tentativas = 20  # evita loop infinito
        for _ in range(max_tentativas):
            texto_atual = tipo_cobranca.window_text().strip()
            if any(opcao.lower() == texto_atual.lower() for opcao in opcoes):
                send_keys("{ENTER}")
                break
            send_keys("{DOWN}")
                
        await worker_sleep(3)
        
        dt_vencimento_nota = nota.get("dataVencimento")  # vem como '2025-09-26'
        data_atual = datetime.now().date()

        # Converte para date (formato yyyy-mm-dd → ISO)
        data_vencimento = datetime.strptime(dt_vencimento_nota, "%Y-%m-%d").date()

        # Se o vencimento for hoje ou já passou, joga para próximo dia útil
        if data_vencimento <= data_atual:
            data_vencimento = data_atual + timedelta(days=1)

            # Ajusta para cair só em dias úteis
            while data_vencimento.weekday() >= 5:  # 5 = sábado, 6 = domingo
                data_vencimento += timedelta(days=1)

        # Converter para string (formato brasileiro dd/mm/yyyy)
        data_vencimento_str = data_vencimento.strftime("%d/%m/%Y")
        print("Novo vencimento:", data_vencimento_str)

        # Inserir no campo
        data_venc = panel_TTabSheet.child_window(
            class_name="TDBIEditDate", found_index=0
        )

        data_venc.set_edit_text(data_vencimento_str)
                    
        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(
                r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\entrada_notas\IncluirRegistro.png", confidence=0.8
            )
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(
                f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n"
            )
            await incluir_registro()

        await worker_sleep(10)
       
        console.print(
            "Verificando a existencia de POP-UP de Itens que Ultrapassam a Variação Máxima de Custo ...\n"
        )
        itens_variacao_maxima = await is_window_open_by_class(
            "TFrmTelaSelecao", "TFrmTelaSelecao"
        )
        if itens_variacao_maxima["IsOpened"] == True:
            app = Application().connect(class_name="TFrmTelaSelecao")
            main_window = app["TFrmTelaSelecao"]
            send_keys("%o")

        await worker_sleep(2)
        console.print(
            "Verificando a existencia de Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
        )
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        try:
            warning_pop_up_pagamentos = main_window.child_window(
                class_name="TMessageForm", title="Warning"
            )
        except:
            warning_pop_up_pagamentos = None

        if warning_pop_up_pagamentos.exists():
            console.print(
                "Erro: Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"A soma dos pagamentos não bate com o valor da nota.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )
        else:
            console.print(
                "Warning informando que a Soma dos pagamentos não bate com o valor da nota não existe ...\n"
            )

        max_attempts = 7
        i = 0
        aguarde_rateio_despesa = True

        while i < max_attempts:
            await worker_sleep(3)

            from pywinauto import Desktop

            for window in Desktop(backend="uia").windows():
                if "Rateio" in window.window_text():
                    aguarde_rateio_despesa = False
                    console.print(
                        "A janela 'Rateio da Despesas' foi encontrada. Continuando para andamento do processo...\n"
                    )
                    break

            if not aguarde_rateio_despesa:
                break

            i += 1

        if aguarde_rateio_despesa:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Número máximo de tentativas atingido. A tela para Rateio da Despesa não foi encontrada.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        despesa_rateio_work = await rateio_despesa(empresaCodigo)
        if despesa_rateio_work.sucesso == True:
            console.log(despesa_rateio_work.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=despesa_rateio_work.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=despesa_rateio_work.tags
            )

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(15)
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            app = Application().connect(title="Warning")
            main_window = app["Warning"]
            main_window.set_focus()

            console.print(f"Obtendo texto do Warning...\n")
            console.print(f"Tirando print da janela do warning para realização do OCR...\n")

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\warning_popup_{nota.get("nfe")}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)
            if 'movimento não permitido' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Filial: {empresaCodigo} está com o livro fechado ou encerrado, verificar com o setor fiscal",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )
            else:
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Warning não mapeado para seguimento do robo, mensagem: {captured_text}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            
        await worker_sleep(3)
        # Verifica se a nota foi lançada
        nf_imported = await check_nota_importada(dados_nf[0].get("chaveNfe"))
        if nf_imported.sucesso == True:
            await worker_sleep(3)
            console.print("\nVerifica se a nota ja foi lançada...")
            nf_chave_acesso = int(dados_nf[0].get("chaveNfe"))
            status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)
            if status_nf_emsys.get("status") == "Lançada":
                console.print("\nNota lançada com sucesso, processo finalizado...", style="bold green")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Nota Lançada com sucesso!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            else:
                console.print("Erro ao lançar nota", style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop-up nota incluida encontrada, porém nota encontrada como 'já lançada' trazendo as seguintes informações: {nf_imported.retorno} - {error_work}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )
        else:
            console.print("Erro ao lançar nota", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao lançar nota, erro: {nf_imported.retorno}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

    finally:
        # Deleta o xml
        await delete_xml(numero_nota)


