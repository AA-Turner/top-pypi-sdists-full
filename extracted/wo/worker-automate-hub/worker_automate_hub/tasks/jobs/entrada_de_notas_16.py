import asyncio
import getpass
import os
import warnings
import uuid
import time
import win32clipboard
import difflib

import pyautogui
from pywinauto.keyboard import send_keys
from PIL import Image, ImageEnhance
import pytesseract
from pywinauto.application import Application
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
    sync_get_config_by_name,
)
from worker_automate_hub.config.settings import load_env_config
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
    check_nota_importada,
    error_after_xml_imported,
    error_before_persist_record,
    import_nfe,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_process,
    login_emsys,
    set_variable,
    type_text_into_field,
    verify_nf_incuded,
    warnings_after_xml_imported,
    worker_sleep,
    select_documento_type
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()

emsys = EMSys()


async def entrada_de_notas_16(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        console.print(config)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Abre um novo emsys
        await kill_process("EMSys")

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field(
                "Nota Fiscal de Entrada", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(10)

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

        await worker_sleep(10)

        # Download XML
        await save_xml_to_downloads(nota["nfe"])

        # Permanece 'XML'
        # Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await worker_sleep(3)

        # Click Downloads
        await emsys.get_xml(nota["nfe"])
        await worker_sleep(15)

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

        # Deleta o xml
        await emsys.delete_xml(nota.get("nfe"))
        await worker_sleep(5)

        app = Application().connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        # INTERAGINDO COM A DATA DE ENTRADA
        await worker_sleep(2)
        try:
            recebimento_fisico = nota.get("recebimentoFisico", None)
            if recebimento_fisico:
                recebimento_fisico = nota["recebimentoFisico"].split(" ")
                pyautogui.write(recebimento_fisico[0])
                await worker_sleep(2)
        except:
            console.print(
                f"A chave recebimentoFisico não está presente na config de entrada...\n"
            )

        if nota.get("cfop"):
            console.print(
                f"Inserindo a informação da CFOP, caso se aplique {nota.get("cfop")} ...\n"
            )
            if nota.get("cfop") not in ["5910", "6910"]:
                combo_box_natureza_operacao = main_window.child_window(
                    class_name="TDBIComboBox", found_index=0
                )
                combo_box_natureza_operacao.click()
                await worker_sleep(4)
                set_combobox("||List", "1403 - COMPRA DE MERCADORIAS- 1.403")
                await worker_sleep(3)
            elif nota.get("cfop") == "6910":
                combo_box_natureza_operacao = main_window.child_window(
                    class_name="TDBIComboBox", found_index=0
                )
                combo_box_natureza_operacao.click()
                await worker_sleep(4)
                set_combobox(
                    "||List", "2910-ENTRADA DE BONIFICACAO - COM ESTOQUE - 2910"
                )
                await worker_sleep(4)
            else:
                combo_box_natureza_operacao = main_window.child_window(
                    class_name="TDBIComboBox", found_index=0
                )
                combo_box_natureza_operacao.click()
                await worker_sleep(4)
                set_combobox(
                    "||List", "1910-ENTRADA DE BONIFICACAO - COM ESTOQUE - 1910"
                )
                await worker_sleep(3)

        await worker_sleep(3)
        try:
            console.print(f"Trabalhando com itens com multiplas referencias.\n")
            itens_nao_semelhantes = []
            # TRABALHANDO COM ITENS QUE POSSUEM MULTIPLAS REFERÊNCIAS
            while True:
                await worker_sleep(3)
                console.print(
                    f"Verificando a existencia de fornecedor com múltiplas referencias...\n"
                )
                itens_by_supplier = await is_window_open_by_class(
                    "TFrmSelecionaItensFornecedor", "TFrmSelecionaItensFornecedor"
                )
                if itens_by_supplier["IsOpened"] == True:
                    new_app = Application(backend="uia").connect(
                        class_name="TFrmSelecionaItensFornecedor"
                    )
                    window = new_app["TFrmSelecionaItensFornecedor"]
                    window.set_focus()
                    await worker_sleep(2)

                    console.print(f"Obtendo item com multiplas referências...\n")
                    console.print(f"Tirando print da janela para realização do OCR...\n")

                    text_captured = False
                    count_while = 0
                    max_attempts = 3
                    item_da_nota = ''

                    while count_while < max_attempts:
                        window_rect = window.rectangle()
                        console.print(f"Area que sera utulizada para o screenshot {window_rect}...\n")
                        screenshot = window.capture_as_image()

                        username = getpass.getuser()
                        short_uuid = str(uuid.uuid4()).replace('-', '')[:6]
                        path_to_png = f"C:\\Users\\{username}\\Downloads\\{short_uuid}.png"
                        screenshot.save(path_to_png)
                        while not os.path.exists(path_to_png) or os.path.getsize(path_to_png) == 0:
                            time.sleep(0.1)
                        console.print(f"Print salvo em {path_to_png}...\n")

                        await worker_sleep(2)
                        console.print("Preparando a imagem para maior resolução e assertividade no OCR...\n")
                        image = Image.open(path_to_png)
                        image = image.convert("L")
                        enhancer = ImageEnhance.Contrast(image)
                        image = enhancer.enhance(2.0)
                        image.save(path_to_png)
                        console.print("Imagem preparada com sucesso...\n")

                        console.print(f"Imagem antes do OCR: {image}\n")
                        console.print(f"Dimensões da imagem: {image.size}\n")

                        console.print("Realizando OCR...\n")
                        captured_text = pytesseract.image_to_string(image)
                        console.print(f"Texto Full capturado {captured_text}, tentando obter o item da nota...\n")

                        match = re.search(r"Item da Nota:\s*(.*)\s*", captured_text)
                        if os.path.exists(path_to_png):
                            os.remove(path_to_png)
                            console.print(f"Imagem apagada com sucesso do diretorio {path_to_png}... \n")
                        else:
                            console.print(f"Imagem não encontrada para realização do OCR... \n")

                        console.print(f"Texto extraido do RegEx: {match}... \n")
                        if match:
                            item_da_nota = match.group(1).strip()
                            console.print(f"Item da Nota capturado: {item_da_nota}... \n")
                            text_captured = True
                            break
                        else:
                            if match:
                                item_da_nota = match.group(1).strip()
                                console.print(f"Item da Nota capturado: {item_da_nota}... \n")
                                text_captured = True
                                break
                            else:
                                match = re.search(r"Item da (Nota|Nata|N0ta)\s*(.*)\s*", captured_text)
                                if match:
                                    item_da_nota = match.group(1).strip()
                                    console.print(f"Item da Nota capturado: {item_da_nota}... \n")
                                    text_captured = True
                                    break
                                else:
                                    console.print(f"Tentativa {count_while + 1} de {max_attempts} falhou. Tentando novamente...\n")
                                    count_while += 1

                    if not text_captured:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno="Quantidade de tentativa atingida (3), não foi possivel capturar o item da nota com multiplas referencias para andamento no processo",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                        )

                    console.print(
                        f"Interagindo com os multiplos itens e detectando qual ira ser selecionado para andamento no processo... \n"
                    )
                    copied_codes_list = []
                    count = 0
                    last_copied = None

                    while True:
                        if count == 0:
                            send_keys("^({HOME})")
                        else:
                            send_keys("{DOWN 1}")

                        send_keys("^c")
                        win32clipboard.OpenClipboard()
                        window_message = win32clipboard.GetClipboardData().strip()
                        win32clipboard.CloseClipboard()

                        console.print(f"Linha copiada: {window_message}... \n")

                        if last_copied is not None and window_message == last_copied:
                            break

                        copied_codes_list.append(
                            {"linha": count, "conteudo": window_message}
                        )

                        last_copied = window_message
                        count = +1

                    console.print(f"Valores copiados {copied_codes_list}... \n")

                    extracted_items = {}

                    for entry in copied_codes_list:
                        content = entry["conteudo"]
                        lines = content.split("\r\n")
                        for line in lines:
                            items = line.split("\t")
                            if len(items) >= 3:
                                cod_item = items[0].strip()
                                descricao = items[1].strip()
                                cod_barra = items[2].strip()

                                extracted_items[cod_item] = {
                                    "Descrição": descricao,
                                    "Código de Barra": cod_barra,
                                    "Linha": entry["linha"],
                                }

                    best_match = None
                    highest_ratio = 0.0

                    for cod_item, info in extracted_items.items():
                        descricao = info["Descrição"]
                        similarity_ratio = difflib.SequenceMatcher(
                            None, item_da_nota, descricao
                        ).ratio()

                        if similarity_ratio > highest_ratio:
                            highest_ratio = similarity_ratio
                            best_match = {
                                "Cod Item": cod_item,
                                "Descrição": descricao,
                                "Código de Barra": info["Código de Barra"],
                                "Linha": info["Linha"],
                                "Similaridade": similarity_ratio,
                            }

                    if best_match and highest_ratio > 0.7:
                        console.print(
                            f"Melhor semelhança encontrada {best_match}, selecionando... \n"
                        )
                        send_keys("^({HOME})")
                        send_keys("{DOWN " + str(best_match["Linha"]) + "}")
                        send_keys("%o")
                        await worker_sleep(2)
                    else:
                        itens_nao_semelhantes.append(
                            {"item": item_da_nota, "match": best_match}
                        )
                        send_keys("%o")
                else:
                    console.print(
                        "Não possui a tela de fornecedor com múltiplas referencias, seguindo com o processo...\n"
                    )
                    break

            if len(itens_nao_semelhantes) > 0:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Não foi possivel encontrar o item mais proximo ao item da nota com multiplas referencias {itens_nao_semelhantes}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
        except Exception as error:
            console.print("Erro durante a trativa de multiplas referencias, erro : {error}")
        
        await worker_sleep(3)
        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        filial_empresa_origem = nota.get("filialEmpresaOrigem")
        valor_almoxarifado = filial_empresa_origem + "50"
        pyautogui.press("tab")
        pyautogui.write(valor_almoxarifado)
        await worker_sleep(2)
        pyautogui.press("tab")

        await worker_sleep(3)
        # INTERAGINDO COM CHECKBOX Utilizar unidade de agrupamento dos itens
        fornecedor = nota.get("nomeFornecedor")
        console.print(f"Fornecedor: {fornecedor} ...\n")
        console.print(
            f"Sim, nota emitida para: {fornecedor}, marcando o agrupar por unidade de medida...\n"
        )

        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
        except Exception as e:
            console.print(f"Erro ao iterar itens de almoxarifado: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao iterar itens de almoxarifado: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        checkbox = window.child_window(
            title="Utilizar unidade de agrupamento dos itens",
            class_name="TCheckBox",
            control_type="CheckBox",
        )
        if not checkbox.get_toggle_state() == 1:
            checkbox.click()
            console.print("Realizado o agrupamento por unidade de medida... \n")

        console.print(
            f"Valor do checkbox: {checkbox.get_toggle_state()}", style="bold purple"
        )

        await worker_sleep(3)

        # INTERAGINDO COM CHECKBOX SOMENTE SE CFOP == 5910
        if nota.get("cfop") == "5910":
            checkbox_manter_natureza_op = window.child_window(
                title="Manter Natureza de Operação selecionada",
                class_name="TDBICheckBox",
                control_type="CheckBox",
            )
            if not checkbox_manter_natureza_op.get_toggle_state() == 1:
                checkbox_manter_natureza_op.click()

        await worker_sleep(10)
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
                if informacao_nf_eletronica["IsOpened"] == False:
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
                retorno=f"Número máximo de tentativas atingido, Não foi possivel finalizar os trabalhos na tela de Informações para importação da Nota Fiscal Eletrônica",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(15)

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

        await worker_sleep(3)

        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()

        await emsys.verify_warning_and_error("Information", "&No")

        await worker_sleep(10)
        await emsys.percorrer_grid()
        await emsys.select_tipo_cobranca()
        await emsys.inserir_vencimento_e_valor(
            nota.get("nomeFornecedor"),
            nota.get("dataEmissao"),
            nota.get("dataVencimento"),
            nota.get("valorNota"),
        )
        await worker_sleep(5)
        try:
            retorno = await emsys.incluir_registro(chave_nfe=nota.get("nfe"))
            if retorno.sucesso == True:
                return RpaRetornoProcessoDTO(
                    sucesso=error_work.sucesso,
                    retorno=error_work.retorno,
                    status=error_work.status,
                )
        except:
            console.print("A Nota fiscal ainda não foi incluída, continuando o processo...")

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

        await worker_sleep(5)
        
        await emsys.verify_warning_and_error("Warning", "OK")
        await emsys.verify_warning_and_error("Aviso", "OK")

        try:
            erro_pop_up = await is_window_open("Information")
            if erro_pop_up["IsOpened"] == True:
                error_work = await error_before_persist_record()
                return RpaRetornoProcessoDTO(
                    sucesso=error_work.sucesso,
                    retorno=error_work.retorno,
                    status=error_work.status,
                )
        except:
            console.print("Erros não foram encontrados durante a alteração do item")

        await worker_sleep(5)
        resultado = await emsys.verify_max_variation()

        if not resultado:
            pass
        else:
            if resultado.sucesso == False:
                return resultado

        await worker_sleep(5)
        
        try:
            retorno = await emsys.incluir_registro(chave_nfe=nota.get("nfe"))
            if retorno.sucesso == True:
                return RpaRetornoProcessoDTO(
                    sucesso=error_work.sucesso,
                    retorno=error_work.retorno,
                    status=error_work.status,
                )
        except:
            console.print("A Nota fiscal ainda não foi incluída, continuando o processo...")

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

        await worker_sleep(5)

        await emsys.verify_warning_and_error("Warning", "OK")
        await emsys.verify_warning_and_error("Aviso", "OK")

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(6)
        retorno = False
        try:
            app = Application().connect(class_name="TFrmNotaFiscalEntrada")
            main_window = app["Information"]

            main_window.set_focus()

            console.print(f"Tentando clicar no Botão OK...\n")
            btn_ok = main_window.child_window(class_name="TButton")

            if btn_ok.exists():
                btn_ok.click()
                retorno = True
            else:
                console.print(f" botão OK Não enontrado")
                retorno = await verify_nf_incuded()

        except Exception as e:
            try:
                alterar_nop_result = await emsys.alterar_nop(nota.get("cfop"), nota.get("nfe"))
                if alterar_nop_result:
                    await worker_sleep(5)
                    resultado = await emsys.verify_max_variation()
                    return alterar_nop_result
            except ValueError as ve:
                observacao = f"Erro Processo Entrada de Notas: {str(ve)}"
                logger.error(observacao)
                console.print(observacao, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )
            except Exception as error:
                observacao = f"Erro Processo Entrada de Notas: {str(error)}"
                logger.error(observacao)
                console.print(observacao, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

        try:
            
            await emsys.verify_warning_and_error("Warning", "OK")
            await emsys.verify_warning_and_error("Aviso", "OK")

            await worker_sleep(2)
            
            max_attempts = 60
            i = 0

            while i < max_attempts and retorno is not True:
                information_pop_up = await is_window_open("Information")
                if information_pop_up["IsOpened"] == True:
                    break
                else:
                    console.print(f"Aguardando confirmação de nota incluida...\n")
                    await worker_sleep(5)
                    i += 1

            information_pop_up = await is_window_open("Information")
            
            if not retorno:
                if information_pop_up["IsOpened"] == True:
                    app = Application().connect(class_name="TFrmNotaFiscalEntrada")
                    main_window = app["Information"]

                    main_window.set_focus()

                    console.print(f"Obtendo texto do Information...\n")
                    console.print(f"Tirando print da janela do Information para realização do OCR...\n")

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
                    path_to_png = f"C:\\Users\\{username}\\Downloads\\information_popup_{nota.get("nfe")}.png"
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
                    if 'nota fiscal inc' in captured_text.lower():
                        console.print(f"Tentando clicar no Botão OK...\n")
                        btn_ok = main_window.child_window(class_name="TButton")

                        if btn_ok.exists():
                            btn_ok.click()
                            retorno = True
                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Pop_up Informantion não mapeado para andamento do robô, mensagem {captured_text}",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                        )
                else:
                    console.print(f"Aba Information não encontrada")
                    retorno = await verify_nf_incuded()

        except Exception as e:
            console.print(f"Erro ao conectar à janela Information: {e}\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        console.print("\nVerifica se a nota ja foi lançada...")
        nf_chave_acesso = int(nota.get("nfe"))
        status_nf_emsys = await get_status_nf_emsys(nf_chave_acesso)
        nf_imported = await check_nota_importada(nota.get("nfe"))
        if nf_imported.sucesso == True:
            await worker_sleep(12)
            console.print("\nVerifica se a nota ja foi lançada...")
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
