import difflib
import getpass
import os
import re
import warnings
import time
import uuid
import asyncio
from datetime import datetime, timedelta
import pyautogui
import pytesseract
import win32clipboard
from PIL import Image, ImageEnhance
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
from pywinauto_recorder.player import set_combobox
from rich.console import Console
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.api.client import (
    get_config_by_name,
    get_status_nf_emsys,
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

# limite permitido (<= 5.89 pode seguir)
VALOR_UNITARIO_MAX = Decimal("5.89")

def _to_decimal(valor: Any, default: Decimal = Decimal("0")) -> Decimal:
    """
    Converte valores como '5,89', '5.89', 5.89, None para Decimal com segurança.
    """
    if valor is None:
        return default
    if isinstance(valor, (int, float, Decimal)):
        return Decimal(str(valor))
    s = str(valor).strip().replace(",", ".")
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return default

async def entrada_de_notas_22(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Executa o processo de entrada de notas.
    Regra de negócio: se QUALQUER item tiver valorUnitario > 5,89, retornar erro imediatamente.
    """
    
    cfg: Dict[str, Any] = getattr(task, "configEntrada", {}) or {}
    itens: List[Dict[str, Any]] = cfg.get("itens", []) or []

    # --- Validação de valorUnitario ---
    acima_limite = []
    for idx, item in enumerate(itens, start=1):
        valor_unit = _to_decimal(item.get("valorUnitario"))
        if valor_unit > VALOR_UNITARIO_MAX:
            acima_limite.append({
                "idx": idx,
                "codigoProduto": item.get("codigoProduto"),
                "descricaoProduto": item.get("descricaoProduto"),
                "valorUnitario": str(valor_unit)
            })

    if acima_limite:
        # Monta mensagem amigável com os itens fora da regra
        detalhes = "; ".join(
            f"item {x['idx']} (cód. {x.get('codigoProduto') or 's/ código'}): "
            f"valorUnitario={x['valorUnitario']} (> {VALOR_UNITARIO_MAX})"
            for x in acima_limite
        )
        observacao = (
            "Erro Processo Entrada de Notas: Foi identificado ao menos um item com "
            f"valorUnitario acima do permitido ({VALOR_UNITARIO_MAX}). Detalhes: {detalhes}"
        )
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
        )
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        # Seta config entrada na var nota 
        nota = task.configEntrada
        # conversão no formato certo: dd/mm/yyyy
        data_vencimento = datetime.strptime(nota['dataVencimento'], "%d/%m/%Y").date()
        hoje = datetime.today().date()

        if data_vencimento <= hoje:
            data_vencimento = hoje + timedelta(days=1)
            while data_vencimento.weekday() >= 5:  # 5 = sábado, 6 = domingo
                data_vencimento += timedelta(days=1)
        
        data_vencimento = data_vencimento.strftime("%d/%m/%Y")
        print("Data ajustada:", data_vencimento)
        valor_nota = nota['valorNota']
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        # Download XML
        console.log("Realizando o download do XML..\n")
        await save_xml_to_downloads(nota["nfe"])

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_10.exe")
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

        await get_xml(nota.get("nfe"))
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


        from pywinauto import Desktop
        from pywinauto.keyboard import send_keys
        from pywinauto.timings import wait_until_passes

        # === INTERAGINDO COM A NATUREZA DA OPERACAO (somente navegação) ===
        cfop = str(int(nota.get("cfop")))
        console.print(f"Inserindo a informação da CFOP: {cfop} ...\n")

        combo_box = main_window.child_window(class_name="TDBIComboBox", found_index=0)

        # Definir alvo conforme regra
        if cfop == "5656":
            alvo_texto = "1652-COMPRA DE MERCADORIAS - 1.652 S/ESTOQUE"
        elif cfop.startswith("6"):
            alvo_texto = "2556-COMPRA DE MERCADORIAS SEM ESTOQUE- 2.556"
        elif cfop.startswith("5"):
            alvo_texto = "1556-COMPRA DE MERCADORIAS SEM ESTOQUE- 1.556"
        else:
            console.print("Erro mapeado, CFOP não corresponde. Necessário ajuste manual.\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro mapeado, CFOP {cfop} não corresponde às regras.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        # 1) Clica no combo e abre a lista
        combo_box.click_input()
        await worker_sleep(0.3)
        send_keys("%{DOWN}")  # Alt+Down abre a lista (pode testar só {DOWN} se não funcionar)

        # 2) Aguardar lista suspensa
        try:
            listbox = wait_until_passes(
                timeout=5,
                retry_interval=0.2,
                func=lambda: Desktop(backend="win32").window(class_name="ComboLBox")
            )
        except Exception:
            listbox = None
            console.print("⚠️ Lista suspensa não localizada, tentando mesmo assim...\n")

        # 3) Percorrer até encontrar alvo
        encontrou = False
        for _ in range(200):  # limite p/ evitar loop infinito
            texto_sel = None
            if listbox:
                try:
                    sel = listbox.get_selection()
                    if sel:
                        texto_sel = sel[0].window_text().strip()
                except Exception:
                    pass

            if not texto_sel:
                try:
                    texto_sel = combo_box.window_text().strip()
                except Exception:
                    texto_sel = ""

            if texto_sel and alvo_texto in texto_sel:
                encontrou = True
                break

            send_keys("{DOWN}")
            await worker_sleep(0.05)

        # 4) Confirmar ou falhar
        if encontrou:
            send_keys("{ENTER}")
            console.print(f"✅ Selecionado: {alvo_texto}\n")
        else:
            console.print(f"❌ Não encontrei '{alvo_texto}' na lista.\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não encontrei '{alvo_texto}' no combo.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        
        await worker_sleep(3)

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        fornecedor = nota.get("nomeFornecedor")
        filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
        console.print(
            f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n"
        )
        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
            edit = window.child_window(
                class_name="TDBIEditCode", found_index=3, control_type="Edit"
            )
            if filialEmpresaOrigem != "1":
                valor_almoxarifado = filialEmpresaOrigem + "50"
            else:
                valor_almoxarifado = filialEmpresaOrigem + "60"
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
        despesa = '298'

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
        cod_icms_work = await cod_icms("20")
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

        await worker_sleep(5)
        try:
            ##### Janela Information #####
            app = Application(backend="win32").connect(title_re="Information")

            # Seleciona a janela pelo título
            dlg = app.window(title_re="Information")

            # Clica no botão "Não"
            dlg['&No'].click_input()

            console.print("Clique em NÃO realizado com sucesso!")
        except:
            pass

      
        await worker_sleep(2)
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        pyautogui.click(621, 359)

        await worker_sleep(5)

        try:
            # Verificar se já existe parcela
            console.print("Verificar se já existe parcela")
            main_window.child_window(class_name="TDBIBitBtn", found_index=0).click_input()
            console.print("Parcelas encontradas, removendo para inserir data atual")

            await worker_sleep(3)

            # conecta no dialog "Confirm"
            app = Application(backend="win32").connect(title="Confirm")
            dlg = app.window(title="Confirm", class_name="TMessageForm")

            # clica no botão Yes
            dlg.child_window(title="&Yes", class_name="TButton").click_input()
            print("Clique em 'Yes' na janela de confirmação.")
        except:
            console.print("Parcela não encontrada")

        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()

        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TPageControl")

        panel_TabPagamento = panel_TTabSheet.child_window(title="Pagamento")

        input_dt_vencimento = panel_TPage = main_window.child_window(class_name="TDBIEditDate", found_index=0).click()
        send_keys(data_vencimento)

        input_valor =  panel_TPage = main_window.child_window(class_name="TDBIEditNumber", found_index=3).click()
        send_keys('{RIGHT}')
        send_keys('^a{BACKSPACE}')    
        await worker_sleep(1)
        send_keys(valor_nota)

        # === INTERAGINDO COM O TIPO DE COBRANCA ===
        tipo_cobranca = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=0
        )

        # Opções de fallback
        alvos = ["BANCO DO BRASIL BOLETO", "BOLETO"]

        # 1) Clica no combo e abre a lista
        tipo_cobranca.click_input()
        await worker_sleep(0.3)
        send_keys("%{DOWN}")  # abre o dropdown (pode ser só {DOWN} dependendo da janela)
        await worker_sleep(0.3)

        # 2) Aguarda lista suspensa
        try:
            listbox = wait_until_passes(
                timeout=5,
                retry_interval=0.2,
                func=lambda: Desktop(backend="win32").window(class_name="ComboLBox")
            )
        except Exception:
            listbox = None
            console.print("⚠️ Lista suspensa não localizada, tentando mesmo assim...\n")

        # 3) Percorrer tentando encontrar o primeiro alvo válido
        encontrou = False
        alvo_escolhido = None

        for alvo_texto in alvos:  # tenta em ordem BANCO... depois BOLETO
            for _ in range(200):
                texto_sel = None
                if listbox:
                    try:
                        sel = listbox.get_selection()
                        if sel:
                            texto_sel = sel[0].window_text().strip()
                    except Exception:
                        pass

                if not texto_sel:
                    try:
                        texto_sel = tipo_cobranca.window_text().strip()
                    except Exception:
                        texto_sel = ""

                if texto_sel and alvo_texto in texto_sel:
                    encontrou = True
                    alvo_escolhido = alvo_texto
                    break

                send_keys("{DOWN}")
                await worker_sleep(0.05)

            if encontrou:
                break

        # 4) Confirmar ou falhar
        if encontrou:
            send_keys("{ENTER}")
            console.print(f"Selecionado: {alvo_escolhido}\n")
        else:
            console.print("Não encontrei nenhuma das opções na lista.\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não encontrei opção de cobrança válida.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

        await worker_sleep(2)
        
        # Clicar  em incluir registro
        pyautogui.click(1289, 530)
        
        await worker_sleep(3)

        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(
                "assets\\entrada_notas\\IncluirRegistro.png", confidence=0.8
            )
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(
                f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n"
            )
            
        await worker_sleep(5)
        
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

        await worker_sleep(5)
        
        console.print(
            "Verificando a existencia de Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
        )
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]
       
        # --- Verificação do pop-up "TMessageForm" ---
        warning_existe = False
        try:
            # tenta conectar na janela do aviso
            app = Application().connect(class_name="TMessageForm", timeout=3)
            dlg = app.window(class_name="TMessageForm")

            # confirma se a janela realmente existe/está visível
            if dlg.exists(timeout=1):
                warning_existe = True
               
        except (ElementNotFoundError, Exception):
            warning_existe = False

        if warning_existe:
            console.print(
                "Erro: Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="A soma dos pagamentos não bate com o valor da nota.",
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

        despesa_rateio_work = await rateio_despesa(filialEmpresaOrigem)
        if despesa_rateio_work.sucesso == True:
            console.log(despesa_rateio_work.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=despesa_rateio_work.retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=despesa_rateio_work.tags
            )

        await worker_sleep(5)
        
        try:
            # Localiza a janela Warning (pode ser Warning, Aviso, etc)
            warning_win = Desktop(backend="win32").window(title_re=".*[Ww]arning.*")

            if warning_win.exists(timeout=3):
                console.print("⚠️ Janela Warning encontrada. Clicando em YES...\n")

                # Busca pelo botão Yes (tem variações: &Yes, YesButton)
                btn_yes = warning_win.child_window(
                    title_re=".*Yes.*", class_name="TButton"
                )

                btn_yes.click_input()
                await worker_sleep(0.5)

            else:
                console.print("Nenhuma janela Warning apareceu.\n")

        except Exception as e:
            console.print(f"Erro ao clicar em YES: {e}\n")
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
                retorno=f"Filial: {filialEmpresaOrigem} está com o livro fechado ou encerrado, verificar com o setor fiscal",
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
        nf_imported = await check_nota_importada(nota.get("nfe"))
        if nf_imported.sucesso == True:
            await worker_sleep(3)
            console.print("\nVerifica se a nota ja foi lançada...")
            nf_chave_acesso = int(nota.get("nfe"))
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
        await delete_xml(nota.get("nfe"))

