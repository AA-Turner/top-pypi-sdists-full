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
from pywinauto.timings import TimeoutError as PywTimeout, wait_until
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


ASSETS_PATH = "assets"

async def rateio_despesa_centro_custo(centro_custo : str) -> RpaRetornoProcessoDTO:
    console.print(
        f"Conectando a tela de Rateio da Despesa para encerramento do processo...\n"
    )
    console.print(f"Código filial {centro_custo }...\n")
    try:

        console.print(f"Tentando clicar em Selecionar todos...\n")
        try:
            selecionar_todos = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\SelecionarTodos.png", confidence=0.5
            )
            if selecionar_todos:
                console.print(f"Campo selecionar todos encontrado, interagindo...\n")
                pyautogui.click(selecionar_todos)

        except Exception as e:
            console.print(f"Error ao interagir com o campo de selecionar todos : {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Error ao interagir com o campo de selecionar todos : {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(5)

        try:
            app = Application().connect(class_name="TFrmDadosRateioDespesa")
            main_window = app["TFrmDadosRateioDespesa"]
            console.print(f"Conectado com pela classe do emsys...\n")
        except:
            app = Application().connect(title="Rateio da Despesa")
            main_window = app["Rateio da Despesa"]
            console.print(f"Conectado pelo title...\n")

        main_window.set_focus()

        console.print(
            f"Conectado com sucesso, acessando o atributo filho 'Centro'...\n"
        )
        panel_centro = main_window.child_window(class_name="TPanel", found_index=1)

        console.print(
            f"Conectado com sucesso, inserindo o valor do tipo de despesa...\n"
        )

        edit = panel_centro.child_window(class_name="TDBIEditCode", found_index=1)

        try:
            value_centro = int(centro_custo)
        except ValueError:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Unidade code não é um número válido.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        value_centro_str = str(value_centro)
        console.print(f"Valor final a ser inserido no Centro {value_centro_str}...\n")

        if edit.exists():
            edit.set_edit_text(value_centro_str)
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo tipo de despesas - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo tipo de despesas - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print(f"Conectado com sucesso, inserindo o valor do rateio...\n")
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            edit.set_edit_text("100")
            edit.click()
            edit.type_keys("{TAB}")
        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(3)

        console.print(
            f"Selecionando a opção 'Aplicar Rateio aos Itens Selecionados'...\n"
        )
        try:
            checkbox = panel_centro.child_window(
                title="Aplicar Rateio aos Itens Selecionados",
                class_name="TDBICheckBox",
            )
            checkbox.click()
            console.print(
                "A opção 'Aplicar Rateio aos Itens Selecionados' selecionado com sucesso... \n"
            )
        except:
            try:
                aplicar_rateio = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\entrada_notas\\aplicar_rateio_itens.png",
                    confidence=0.5,
                )
                if aplicar_rateio:
                    console.print(
                        f"Campo aplicar rateio itens encontrado, clicando...\n"
                    )
                    center_x, center_y = pyautogui.center(aplicar_rateio)
                    try:
                        pyautogui.click(center_x, center_y)
                    except:
                        pyautogui.click(aplicar_rateio)
            except:
                try:
                    app = Application().connect(title="Busca Centro de Custo")
                    main_window = app["Busca Centro de Custo"]
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Centro de custo não localizado na tela de rateio, por favor, verificar",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )
                except Exception as e:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Campo aplicar rateio - Não foi encontrado, erro: {e}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )

        console.print(f"Tentando clicar em Incluir Registro...\n")
        await worker_sleep(2)
        try:
            console.print(
                f"Não foi possivel clicar em Incluir Registro, tentando via hotkeys..\n"
            )
            pyautogui.press("tab")
            pyautogui.press("tab")
            await worker_sleep(2)
            pyautogui.press("enter")
            await worker_sleep(4)
        except Exception as e:
            try:
                incluir_registro_rateio = pyautogui.locateOnScreen(
                    ASSETS_PATH
                    + "\\entrada_notas\\importar_registro_rateio_despesas.png",
                    confidence=0.5,
                )
                if incluir_registro_rateio:
                    console.print(
                        f"Campo selecionar todos encontrado, interagindo...\n"
                    )
                    pyautogui.click(incluir_registro_rateio)
            except:
                console.print(
                    f"Clicando em Incluir registro para vincular ao centro de custo '...\n"
                )
                edit = panel_centro.child_window(
                    class_name="TDBITBitBtn", found_index=3
                )

                if edit.exists():
                    edit.click()
                else:
                    console.print(f"Campo Incluir registro nao foi encontrado...\n")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno="Campo Incluir registro nao foi encontrado",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )


        await worker_sleep(3)

        console.print(f"Verificando se o item foi rateado com sucesso...\n")
        panel_centro = main_window.child_window(class_name="TPanel", found_index=0)
        edit = panel_centro.child_window(class_name="TDBIEditNumber", found_index=0)

        if edit.exists():
            valor_total_rateado = edit.window_text()
            if valor_total_rateado != "0,00":
                console.print(f"Rateio inserido com sucesso., clicando em OK..\n")
                send_keys("%o")
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Rateio de despesa interagido com sucesso",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )

        else:
            console.print(f"Campo valor do rateio - Não foi encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Campo valor do rateio - Não foi encontrado",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao processar tela de Informações para importação da Nota Fiscal Eletrônica para inserir o tipo de despesa, erro: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

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

        # >>> AJUSTE IMPORTANTE <<<
        fornecedor_cnpj = nota.get("fornecedorCnpj")

        if not fornecedor_cnpj:
            raise ValueError("fornecedorCnpj não informado na entrada do processo")

        try:
            console.print(
                f"Buscando NF | Numero: {numero_nota} | Serie: {serie_nota} | "
                f"Filial: {filial_nota} | Fornecedor CNPJ: {fornecedor_cnpj}"
            )

            dados_nf = await get_dados_nf_emsys(
            numero_nota=numero_nota,
            serie_nota=serie_nota,
            filial_nota=filial_nota,
            fornecedor_cnpj=fornecedor_cnpj
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
            observacao = f"Erro ao lançar nota, erro: {e}"
            console.print("Erro inesperado ao buscar nota:", str(e))
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=observacao,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )



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
        
        # =============================
        # Natureza de Operação (CFOP)
        # =============================

        # Mapeamento CFOP -> (lista, código exibido no combobox)
        cfop_map = {
            "1556": (['5101', '5102', '5103', '5104'], "1.556"),
            "1407": (['5401', '5403', '5404', '5405'], "1.407"),
            "2407": (['6403'], "2.407")
        }

        cfop_str = str(cfop).strip()

        alvo_key = None
        alvo_codigo = None

        for key, (lista, codigo_combo) in cfop_map.items():
            if cfop_str in lista:
                alvo_key = key
                alvo_codigo = str(codigo_combo)
                break

        # Se não mapeou, retorna erro (mesma mensagem sua)
        if not alvo_key:
            console.print(
                "Erro mapeado, CFOP diferente de início com 540 ou 510, necessário ação manual ou ajuste no robô...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro mapeado, CFOP diferente de início com 540 ou 510, necessário ação manual ou ajuste no robô.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        # Critérios de validação do texto selecionado
        must1 = f"{alvo_key}-COMPRA DE MERCADORIAS SEM ESTOQUE"
        must2 = str(alvo_codigo)

        selecionou = False
        opcao_alvo = None

        # 1) localizar opção certa
        for opc in combo_box_natureza_operacao.item_texts():
            if (must1 in opc) and (must2 in opc):
                opcao_alvo = opc
                break

        if not opcao_alvo:
            console.print(
                f"Não encontrei no combobox uma opção contendo: '{must1}' e '{must2}'.\n",
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Natureza de operação não encontrada no combobox para CFOP {cfop_str}.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        # 2) selecionar
        combo_box_natureza_operacao.select(opcao_alvo)
        await worker_sleep(2)
        send_keys("{ENTER}")
        await worker_sleep(2)

        # 3) validar se realmente ficou selecionado (SEM falso positivo)
        #    - NÃO usar " ".join(texts()) porque alguns combos retornam a lista inteira
        #    - usa window_text() e, se vier vazio, texts()[0]
        ultimo_texto = ""
        selecionou = False

        for _ in range(15):  # mais tentativas por causa de delay do EMSys
            atual = ""

            # 1) texto visível do combo
            try:
                atual = (combo_box_natureza_operacao.window_text() or "").strip()
            except Exception:
                atual = ""

            # 2) fallback: primeiro texts() costuma ser o selecionado
            if not atual:
                try:
                    textos = combo_box_natureza_operacao.texts() or []
                    if textos:
                        atual = (textos[0] or "").strip()
                except Exception:
                    atual = ""

            ultimo_texto = atual

            if atual and (must1.lower() in atual.lower()) and (must2.lower() in atual.lower()):
                selecionou = True
                break

            time.sleep(0.2)

        # 4) (opcional) validação por índice, se suportado
        if not selecionou:
            try:
                idx_sel = combo_box_natureza_operacao.selected_index()
                itens = combo_box_natureza_operacao.item_texts()
                idx_alvo = itens.index(opcao_alvo) if opcao_alvo in itens else None

                if idx_alvo is not None and idx_sel == idx_alvo:
                    selecionou = True
            except Exception:
                pass

        if not selecionou:
            console.print(
                f"Falha ao validar seleção da Natureza Operação.\n"
                f"Esperado conter: '{must1}' e '{must2}'\n"
                f"Texto visível no combo: '{ultimo_texto}'\n",
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Falha ao validar seleção da Natureza de Operação no EMSys (texto visível não confere).",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        console.print(
            f"Natureza de operação selecionada e validada: {ultimo_texto}",
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
        imagem = "assets\\entrada_notas\\itens_nota.png"
        # imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\entrada_notas\itens_nota.png"
        pyautogui.click(623, 311)
        await worker_sleep(1)
        send_keys("{DOWN " + ("1") + "}")
        # Tenta localizar a imagem na tela
        # while True:
        #     try:
        #         local = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)  # 0.8 = 80% de precisão
        #         if local:
        #             pyautogui.click(local)   # Clica no centro da imagem
        #             print("Imagem encontrada e clicada!")
        #             break
        #         else:
        #             print("Imagem não encontrada, tentando novamente...")
        #             time.sleep(1)
        #     except Exception as e:
        #         console.print(f"Erro ao localizar imagem de itens da nota: {e}")

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
                lista_icms_060 = ["5401", "5403", "5404", "5405", "6403"]

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
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"CFOP não encontrado na lista",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )

                # Seleciona no combobox
                if opcao_desejada:
                    try:
                        tipo_icms.select(opcao_desejada)
                        await worker_sleep(2)
                        send_keys("{ENTER}")
                        await worker_sleep(2)
                    except Exception as e:
                        print(f"Erro ao selecionar opção: {e}")
                    # Localize o combobox pelo class_name
                    combo = main_window.child_window(class_name="TDBIComboBox", found_index=4)
                    
                    # Seleciona diretamente o texto
                    combo.select("IPI 0%")
                    await worker_sleep(2)
                    send_keys("{ENTER}")
                    await worker_sleep(2)
                            
                    # Clicar em alterar
                    main_window.child_window(class_name="TDBIBitBtn", found_index=3).click()

                    await worker_sleep(5)

                    # Tentar clicar em Sim janela tributacao diferente do item
                    try:                       
                        app_conf = Application().connect(class_name="TMessageForm")
                        main_window_conf = app_conf["TMessageForm"]
                        clicar_ok = main_window_conf.child_window(class_name="TButton", found_index=1).click_input() 
                    except:
                        pass


        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao trabalhar nas alterações dos itens: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

       
        await worker_sleep(10)
        
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        # Clicar em pagamentos
        # imagem = r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\worker_automate_hub\assets\entrada_notas\pagamentos.png"
        imagem = "assets\\entrada_notas\\pagamentos.png"
        pyautogui.click(623, 311)
        await worker_sleep(1)
        send_keys("{DOWN " + ("3") + "}")
        # # Tenta localizar a imagem na tela
        # while True:
        #     local = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)  # 0.8 = 80% de precisão
        #     if local:
        #         pyautogui.click(local)   # Clica no centro da imagem
        #         print("Imagem encontrada e clicada!")
        #         break
        #     else:
        #         print("Imagem não encontrada, tentando novamente...")
        #         time.sleep(1)

        await worker_sleep(3)

        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TPageControl")

        panel_TabPagamento = panel_TTabSheet.child_window(title="Pagamento")

        # Combo alvo (ajuste found_index se precisar)
        tipo_cobranca = panel_TTabSheet.child_window(class_name="TDBIComboBox", found_index=0)

        # Ordem de preferência
        opcoes = [
            "BANCO DO BRASIL BOLETO FIDC",
            "BANCO DO BRASIL BOLETO",
            "BOLETO",
        ]

        # 1) Tenta .select() direto (não digita nada)
        selecionado = None
        for alvo in opcoes:
            try:
                tipo_cobranca.select(alvo)
                if tipo_cobranca.window_text().strip().lower() == alvo.lower():
                    selecionado = alvo
                    break
            except Exception:
                pass

        # 2) Abre a LISTA e seleciona o item exato (sem digitar)
        if not selecionado:
            tipo_cobranca.set_focus()
            tipo_cobranca.click_input()
            send_keys('%{DOWN}')  # ALT+DOWN para abrir o dropdown
            # tenta achar a janela da lista (Delphi/Win32)
            lista = None
            app = tipo_cobranca.app
            for crit in (dict(title="||List"), dict(class_name="ComboLBox"), dict(class_name_re=".*(List|Combo).*")):
                try:
                    cand = app.window(**crit)
                    if cand.exists(timeout=0.5):
                        lista = cand
                        break
                except Exception:
                    pass

            if lista:
                # tenta selecionar por índice (texto exato)
                try:
                    itens = [t.strip() for t in lista.texts() if str(t).strip()]
                except Exception:
                    itens = []

                idx_alvo = -1
                alvo_escolhido = None
                for alvo in opcoes:
                    for i, t in enumerate(itens):
                        if t.lower() == alvo.lower():
                            idx_alvo = i
                            alvo_escolhido = alvo
                            break
                    if idx_alvo >= 0:
                        break

                if idx_alvo >= 0:
                    try:
                        lista.select(idx_alvo)
                    except Exception:
                        # fallback por teclas sem digitar texto do item
                        send_keys('{HOME}')
                        for _ in range(idx_alvo):
                            send_keys('{DOWN}')
                    send_keys('{ENTER}')
                    try:
                        wait_until(2, 0.2, lambda: tipo_cobranca.window_text().strip() != "")
                    except PywTimeout:
                        pass
                    if tipo_cobranca.window_text().strip().lower() == alvo_escolhido.lower():
                        selecionado = alvo_escolhido
                else:
                    # fallback só com setas (sem digitar): vai ao topo e desce checando
                    send_keys('{HOME}')
                    vistos = set()
                    for _ in range(60):
                        atual = tipo_cobranca.window_text().strip()
                        if atual.lower() in (o.lower() for o in opcoes):
                            send_keys('{ENTER}')
                            selecionado = atual
                            break
                        if atual.lower() in vistos:
                            # deu a volta
                            send_keys('{ESC}')
                            break
                        vistos.add(atual.lower())
                        send_keys('{DOWN}')

        # (opcional) validação dura
        if not selecionado or selecionado.lower() not in (o.lower() for o in opcoes):
            raise RuntimeError(f"Não consegui selecionar uma opção válida. Ficou: '{tipo_cobranca.window_text().strip()}'")

        print("Selecionado:", selecionado)
        dt_vencimento_nota = nota.get("dataVencimento")  # vem como '2025-09-26'
        data_atual = datetime.now().date()

        # Converte para date (formato yyyy-mm-dd → ISO)
        data_vencimento = datetime.strptime(dt_vencimento_nota, "%Y-%m-%d").date()
        parcela_apagada = False
        dt_alterada = False
        # Se o vencimento for hoje ou já passou, joga para próximo dia útil
        if data_vencimento <= data_atual:
            data_vencimento = data_atual + timedelta(days=1)
            dt_alterada = True

            # Ajusta para cair só em dias úteis
            while data_vencimento.weekday() >= 5:  # 5 = sábado, 6 = domingo
                data_vencimento += timedelta(days=1)
        
            try:
                apagar_parcela =  main_window.child_window(class_name="TDBIBitBtn", found_index=0).click_input()

                app_conf = Application().connect(class_name="TMessageForm")
                main_window_conf = app_conf["TMessageForm"]
                clicar_ok = main_window_conf.child_window(class_name="TButton", found_index=1).click_input() 
                parcela_apagada = True
            except:
                pass


        # Converter para string (formato brasileiro dd/mm/yyyy)
        data_vencimento_str = data_vencimento.strftime("%d/%m/%Y")
        print("Novo vencimento:", data_vencimento_str)

        # Inserir no campo
        data_venc = panel_TTabSheet.child_window(
            class_name="TDBIEditDate", found_index=0
        )

        data_venc.set_edit_text(data_vencimento_str)
        if not parcela_apagada and not dt_alterada:
            pass
        else:
            # Pegar valor 
            valor_ctrl = panel_TTabSheet.child_window(
                class_name="TDBIEditNumber",
                found_index=7
            )

            valor = valor_ctrl.window_text()
            console.print(valor)

            # Inserir valor 
            campo_destino = panel_TTabSheet.child_window(
                class_name="TDBIEditNumber",
                found_index=3
            )

            campo_destino.set_focus()
            campo_destino.select()                  # seleciona tudo
            campo_destino.type_keys("^a{BACKSPACE}") # limpa o campo
            campo_destino.type_keys(valor, with_spaces=True)

            # Clicar no + para incluir
            inserir_parcela = panel_TTabSheet.child_window(
                class_name="TDBIBitBtn",
                found_index=1
            ).click_input()
        
        await worker_sleep(2)
               
                         
        console.print(f"Incluindo registro...\n")
        try:
            inserir_registro = pyautogui.locateOnScreen("assets\\entrada_notas\\IncluirRegistro.png", confidence=0.8)
            # inserir_registro = pyautogui.locateOnScreen(r"C:\Users\automatehub\Documents\GitHub\worker-automate-hub\assets\entrada_notas\IncluirRegistro.png", confidence=0.8)
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

        await worker_sleep(5)

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

        
        despesa_rateio_work = await rateio_despesa_centro_custo(centro_custo)
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
