import asyncio
import getpass
from datetime import datetime

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
import os
from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import login_emsys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name, get_status_cte_emsys
from worker_automate_hub.api.ahead_service import save_xml_to_downloads
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    delete_xml,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

ASSETS_BASE_PATH = "assets/cte_xml/"
emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


async def click_importar_xml():
    await worker_sleep(5)
    try:
        pyautogui.click(1190, 248)
    except Exception as e:
        # console.print(f"Erro ao conectar a janela {title}")
        raise Exception(f"Erro ao conectar a janela: {e}")


async def importar_xml_conhecimento():

    try:
        await worker_sleep(5)
        app = Application(backend="win32").connect(
            title="Importar XML Conhecimento", found_index=0
        )
        main_window = app["Importar XML Conhecimento"]

        # Clicar em aquisicao de servico de transporte D/E
        aquisicao_servico = main_window.child_window(
            class_name="TDBIComboBox", found_index=1
        )
        aquisicao_servico.select("1353 - AQUISICAO DE SERVICO DE TRANSPORTE D/E")

        await worker_sleep(2)

        # Clicar em rodoviário
        rodoviario = main_window.child_window(class_name="TDBIComboBox", found_index=0)
        rodoviario.select("RODOVIARIO")

        await worker_sleep(2)

        # Clicar em OK
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            try:
                botao = main_window.child_window(class_name="TBitBtn", found_index=1)
                botao.wait("enabled", timeout=5)
                botao.click()

                await worker_sleep(1)

                janela_filha = botao.top_level_parent()
                if not janela_filha.exists(timeout=2):
                    print("Janela filha fechada com sucesso.")
                    break

            except Exception as e:
                print(f"Erro na tentativa {tentativa + 1}: {e}")
        else:
            print("A janela não foi fechada após várias tentativas.")

    except Exception as e:
        # console.print(f"Erro ao conectar a janela {window_title}")
        raise Exception(f"Erro ao conectar a janela: {e}")


async def selecionar_xml(cte):
    await worker_sleep(5)
    nota = cte["chaveCte"]
    nota_cte = f"{nota}.xml"
    username = getpass.getuser()
    path_to_xml = f"C:\\Users\\{username}\\Downloads\\{nota_cte}"
    app = Application(backend="win32").connect(title="Abrir", found_index=0)
    main_window = app["Abrir"]

    await worker_sleep(2)

    #  Selecionar nota baixada
    send_keys(path_to_xml)

    await worker_sleep(3)

    # Tenta clicar no botão abrir apos digitar caminho do XML
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            botao = main_window.child_window(class_name="Button", found_index=0)
            botao.wait("enabled", timeout=5)
            botao.click()

            await worker_sleep(1)

            janela_filha = botao.top_level_parent()
            if not janela_filha.exists(timeout=2):
                print("Janela filha fechada com sucesso.")
                break

        except Exception as e:
            print(f"Erro na tentativa {tentativa + 1}: {e}")
    else:
        print("A janela não foi fechada após várias tentativas.")


def calcular_vencimento_333(data_emissao):

    data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y")

    if 23 <= data_emissao.day or data_emissao.day <= 8:
        faturamento = datetime(data_emissao.year, data_emissao.month, 9)
        if data_emissao.day >= 23:
            faturamento = faturamento + timedelta(days=31)
            faturamento = faturamento.replace(day=9)
    else:
        faturamento = datetime(data_emissao.year, data_emissao.month, 23)
    if faturamento.weekday() == 5:
        faturamento -= timedelta(days=1)
    elif faturamento.weekday() == 6:
        faturamento -= timedelta(days=2)

    vencimento = faturamento + timedelta(days=15)

    if vencimento.weekday() == 5:
        vencimento -= timedelta(days=1)
    elif vencimento.weekday() == 6:
        vencimento -= timedelta(days=2)

    # Ajuste para vencimentos com data anterior ao dia atual
    hoje = datetime.now()
    if vencimento.date() < hoje.date():
        vencimento = hoje + timedelta(days=1)

    return vencimento.strftime("%d/%m/%Y")


def calcular_vencimento_1353(data_emissao):
    data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y")

    if data_emissao.day <= 15:
        mes_vencimento = data_emissao.month + 1
        ano_vencimento = data_emissao.year
        if mes_vencimento > 12:
            mes_vencimento = 1
            ano_vencimento += 1
        vencimento = datetime(ano_vencimento, mes_vencimento, 1)
    else:
        mes_vencimento = data_emissao.month + 1
        ano_vencimento = data_emissao.year
        if mes_vencimento > 12:
            mes_vencimento = 1
            ano_vencimento += 1
        vencimento = datetime(ano_vencimento, mes_vencimento, 16)

    # Ajuste para vencimentos com data anterior ao dia atual
    hoje = datetime.now()
    if vencimento.date() < hoje.date():
        vencimento = hoje + timedelta(days=1)

    return vencimento.strftime("%d/%m/%Y")


async def janela_conhecimento_frete(cte):
    await worker_sleep(3)
    app = Application(backend="win32").connect(
        title="Conhecimento de Frete", found_index=0
    )
    main_window = app["Conhecimento de Frete"]
    despesa = await get_config_by_name("CTE_Despesas")
    cnpj_emitente = cte["cnpjEmitente"]
    tipo_desp = despesa.conConfiguracao["despesas"]
    valor_frete = cte["valorFrete"]
    codigo_despesa = 83  # Valor padrão
    data_emissao = cte["dataEmissao"]
    natureza = cte["natureza"]
    for item in tipo_desp:
        for chave in ["emitente", "empresas"]:
            if chave in item:
                for empresa in item[chave]:
                    if empresa["cnpj"] == cnpj_emitente:
                        codigo_despesa = item["codigoDespesa"]
                        break
                else:
                    continue  # continua no próximo grupo se não achou
                break  # sai do loop interno se achou
        else:
            continue
        break  # sai do loop externo se achou

    print(codigo_despesa)

    # Selecionar natureza da operação 9 - outros
    select_other = main_window.child_window(
        class_name="TDBIComboBoxValues", found_index=1
    )
    select_other.select("9 - Outros")

    await worker_sleep(2)

    # Preencher Tipo de despesa
    campo_tipo_despesa = main_window.child_window(
        class_name="TDBIEditCode", found_index=2
    ).click()
    await worker_sleep(2)
    type_text_into_field(
        text=codigo_despesa,
        field=campo_tipo_despesa,
        empty_before=True,
        chars_to_empty="3",
    )
    campo_tipo_despesa.type_keys("{TAB}")

    # Clicar em valores
    try:
        pyautogui.click(602, 297)
        await worker_sleep(5)

    except Exception as e:
        raise Exception(f"Erro ao clicar em Valores: {e}")

    # Preencher Base ICMS não trib
    base_icms = main_window.child_window(
        class_name="TDBIEditNumber", found_index=20
    ).click()
    base_icms.type_keys("{DEL}")
    base_icms.type_keys(valor_frete)

    # Preencher Valor frete
    base_icms = main_window.child_window(
        class_name="TDBIEditNumber", found_index=14
    ).click()
    for _ in range(10):
        base_icms.type_keys("{DEL}")
    base_icms.type_keys(valor_frete)

    # Clicar em Pagamento
    try:
        pyautogui.click(610, 313)
        await worker_sleep(5)

    except Exception as e:
        raise Exception(f"Erro ao clicar em Valores: {e}")

    # Clicar em Parcelado
    try:
        pyautogui.click(1296, 460)
        await worker_sleep(5)

    except Exception as e:
        raise Exception(f"Erro ao clicar em Valores: {e}")

    # Selecionar tipo de cobrança
    tipo_cobranca = main_window.child_window(class_name="TDBIComboBox", found_index=0)
    tipo_cobranca.select("BANCO DO BRASIL BOLETO")

    if natureza == "1353":
        vencimento = calcular_vencimento_1353(data_emissao)
    elif natureza == "333":
        vencimento = calcular_vencimento_333(data_emissao)

    try:
        # Clicar no botão - para apagar registro se existir
        main_window.child_window(class_name="TDBIBitBtn", found_index=4).click()

        await worker_sleep(2)

        # Clicar em sim para excluir registro
        pyautogui.click(953, 601)
        await worker_sleep(2)

        app = Application(backend="win32").connect(title="Informação", found_index=0)
        main_window = app["Informação"]

        # Clicar em OK
        main_window.child_window(title="OK", found_index=0).click()
        await worker_sleep(2)
    except:
        pass

    # Voltar pra janela conhecimento de frete
    app = Application(backend="win32").connect(
        title="Conhecimento de Frete", found_index=0
    )
    main_window = app["Conhecimento de Frete"]

    # Inserir data de vencimento
    data_vencimento = main_window.child_window(
        class_name="TDBIEditDate", found_index=0
    ).click()
    await worker_sleep(2)
    type_text_into_field(vencimento, data_vencimento, True, "2")

    # clicar no botao de inserir o valor
    btn_inserir_valor = main_window.child_window(
        class_name="TBitBtn", found_index=0
    ).click()

    # Clicar no botão + para salvar
    btn_salvar = main_window.child_window(
        class_name="TDBIBitBtn", found_index=5
    ).click()

    # Clicar no botão + para salvar tudo(aguarda dados de rateio)
    try:
        pyautogui.click(581, 252)
        await worker_sleep(3)

    except Exception as e:
        raise Exception(f"Erro ao clicar em Valores: {e}")


async def janela_information():
    await worker_sleep(3)
    app = Application(backend="win32").connect(title="Information", found_index=0)
    main_window = app["Information"]

    # Clicar em OK
    main_window.child_window(title="OK", found_index=0).click()


async def desmarcar_flag():
    app = Application(backend="win32").connect(
        title="Conhecimento de Frete", found_index=0
    )
    main_window = app["Conhecimento de Frete"]

    # Clicar em Informar nota no conhecimento
    main_window.child_window(class_name="TCheckBox", found_index=0).click()

    # Clicar no botão + para salvar tudo(aguarda dados de rateio)
    try:
        pyautogui.click(581, 252)
        await worker_sleep(5)

    except Exception as e:
        raise Exception(f"Erro ao clicar em Valores: {e}")

    await worker_sleep(3)
    try:
        app = Application(backend="win32").connect(title="Informação", found_index=0)
        main_window = app["Informação"]

        # Clicar em OK
        main_window.child_window(title="OK", found_index=0).click()
    except:
        pass


async def importar_cte_xml(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys")
        cte = task.configEntrada

        # Verifica se a nota já foi lançada
        status_nf_emsys = await get_status_cte_emsys(cte["chaveCte"])
        status = status_nf_emsys["status"]
        print(f"Status da nota:  {status}")
        if status == "Lançada":
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota: {cte['chaveCte']} já foi lançada",
                status=RpaHistoricoStatusEnum.Descartado,
            )

        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_35.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field(
                "Conhecimento de Frete", app["TFrmMenuPrincipal"]["Edit"], True, "50"
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

        # Download XML
        console.log("Realizando o download do XML..\n")
        await save_xml_to_downloads(cte["chaveCte"])
        await worker_sleep(5)
        await click_importar_xml()
        await importar_xml_conhecimento()
        await selecionar_xml(cte)
        await janela_conhecimento_frete(cte)
        await worker_sleep(8)
        try:
            await janela_information()
        except:
            pass
        await desmarcar_flag()

        # Verifica se a nota foi lançada e atualizado no banco
        status_nf_emsys = await get_status_cte_emsys(cte["chaveCte"])
        status = status_nf_emsys["status"]
        print(f"Status da nota:  {status}")
        if status != "Lançada":
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nota: {cte['chaveCte']} não foi lançada com sucesso",
                status=RpaHistoricoStatusEnum.Falha,
            )
        else:
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Suceso no processo CTE com XML",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro no processo CTE com XML: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    finally:
        await delete_xml(cte.get("chaveCte"))
