import asyncio
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
from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import login_emsys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name, get_status_cte_emsys
from worker_automate_hub.utils.util import (
    kill_process,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


async def set_tipo_pagamento_combobox(app: Application, window_title: str):
    try:
        app = Application(backend="uia").connect(process=app.process)
        main_window = app.top_window()
        main_window = main_window.child_window(
            title="Conhecimento de Frete", found_index=0
        )
        janelaPagamento = main_window.child_window(title="tsPagamento", found_index=0)
        janelaPagamento.ComboBox.select("BANCO DO BRASIL BOLETO")

    except Exception as e:
        console.print(f"Erro ao conectar a janela {window_title}")
        raise Exception(f"Erro ao conectar a janela: {e}")


def calcular_vencimento(data_emissao_str):
    data_emissao = datetime.strptime(data_emissao_str, "%d/%m/%Y")

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
    return vencimento.strftime("%d/%m/%Y")


async def entrada_cte_333(task: RpaProcessoEntradaDTO):
    try:
        config = await get_config_by_name("login_emsys")
        console.print(task)

        cte = task.configEntrada

        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        await kill_process("EMSys")

        # Verifica se o CTE ja foi lançado
        console.print("\nVerifica se o CTE ja foi lançado...")
        nf_chave_acesso = int(cte.get("chaveCte"))
        status_nf_emsys = await get_status_cte_emsys(nf_chave_acesso)
        if status_nf_emsys.get("status") == "Lançada":
            console.print(
                "\\CTE ja lançado, processo finalizado...", style="bold green"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="CTE já lançado",
                status=RpaHistoricoStatusEnum.Descartado,
            )
        else:
            console.print("\\CTE não lançado, iniciando o processo...")

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        console.print("\nEMSys iniciando...", style="bold green")
        await worker_sleep(5)

        return_login = await login_emsys(config.conConfiguracao, app, task)
        if return_login.sucesso:
            type_text_into_field(
                "Conhecimento de Frete", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")
            await worker_sleep(5)

            console.print(
                "\nPesquisa: 'Conhecimento de Frete' realizada com sucesso",
                style="bold green",
            )
            await worker_sleep(6)

            console.print("conhecimento frete window")
            type_text_into_field(
                task.configEntrada.get("numeroCte"),
                app["TFrmConhecimentoNotaNew"]["Edit26"],
                False,
                "0",
            )
            await worker_sleep(4)

            type_text_into_field(
                task.configEntrada.get("serieCte"),
                app["TFrmConhecimentoNotaNew"]["Edit24"],
                False,
                "0",
            )
            await worker_sleep(5)

            send_keys(
                "{TAB 2}{ENTER}"
                + task.configEntrada.get("nomeEmitente").replace(" ", "{SPACE}")
                + "{ENTER}"
            )
            await emsys.verify_warning_and_error("Pesquisa", "&Cancelar")
            await worker_sleep(5)
            try:
                app["TFrmConhecimentoNotaNew"]["Edit21"].set_focus()
                app["TFrmConhecimentoNotaNew"]["Edit21"].set_focus()
            except Exception as error:
                console.print(
                    "Não foi possivel focar no campo dataEmissao, clicando na coordenada (903, 417)"
                )
                pyautogui.click(x=903, y=417)
            send_keys(task.configEntrada.get("dataEmissao").replace("/", ""))

            await worker_sleep(4)

            if app["TFrmConhecimentoNotaNew"]["Edit9"].window_text() == "":
                type_text_into_field(
                    task.configEntrada.get("cnpjEmitente"),
                    app["TFrmConhecimentoNotaNew"]["Edit9"],
                    False,
                    "0",
                )
                await worker_sleep(2)

            data_entrada = datetime.now().strftime("%d/%m/%Y")
            try:
                app["TFrmConhecimentoNotaNew"]["Edit20"].set_focus()
                app["TFrmConhecimentoNotaNew"]["Edit20"].set_focus()
            except Exception as error:
                console.print(
                    "Não foi possivel focar no campo dataEntrada, clicando na coordenada (1096, 419)"
                )
                pyautogui.click(x=1096, y=419)
            app["TFrmConhecimentoNotaNew"]["Edit20"].type_keys(
                data_entrada.replace("/", "")
            )
            await worker_sleep(2)

            app["TFrmConhecimentoNotaNew"]["ComboBox4"].select(1)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox3"].select(1)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox5"].select(2)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox2"].select("9 - Outros")

            await emsys.verify_warning_and_error("Pesquisa", "&Cancelar")
            type_text_into_field(
                task.configEntrada.get("chaveCte"),
                app["TFrmConhecimentoNotaNew"]["Edit10"],
                False,
                "0",
            )

            nomeEmitente = task.configEntrada.get("nomeEmitente").upper()
            listaEmitentes01 = ("Reiter", "COL")
            listaEmitentes02 = (
                "Elton",
                "Gotardo",
                "Leandro Xavier",
                "TVF",
                "Pizzolatto",
                "Arco",
                "Dalçoquio",
                "Borges",
                "Delgado",
            )
            tipo_despesa = "83"

            is_reiter_or_col = False

            for emitente in listaEmitentes01:
                emitente = emitente.upper()
                if emitente in nomeEmitente:
                    tipo_despesa = "358"
                    is_reiter_or_col = True
                    break

            for emitente in listaEmitentes02:
                emitente = emitente.upper()
                if emitente in nomeEmitente:
                    tipo_despesa = "359"
                    break

            type_text_into_field(
                tipo_despesa, app["TFrmConhecimentoNotaNew"]["Edit4"], False, "3"
            )
            await worker_sleep(2)

            send_keys("{TAB 3}{DOWN}{ENTER}")
            await worker_sleep(5)
            valorFrete = task.configEntrada.get("valorFrete").replace(".", ",")
            type_text_into_field(
                valorFrete,
                app["TFrmConhecimentoNotaNew"]["Edit21"],
                False,
                "0",
            )
            await worker_sleep(2)

            type_text_into_field(
                valorFrete,
                app["TFrmConhecimentoNotaNew"]["Edit15"],
                False,
                "0",
            )
            await worker_sleep(2)

            send_keys("{TAB 11}{DOWN}{ENTER}")
            await worker_sleep(5)

            pyautogui.click(x=1293, y=537)
            await worker_sleep(2)

            await set_tipo_pagamento_combobox(app, "CONHECIMENTO DE FRETE - CTE")
            await worker_sleep(2)

            dataVencimento = calcular_vencimento(task.configEntrada.get("dataEmissao"))

            send_keys("{TAB}" + dataVencimento)
            await worker_sleep(2)

            pyautogui.click(x=1081, y=404)
            await worker_sleep(2)

            pyautogui.click(x=1261, y=402)
            await worker_sleep(2)

            if is_reiter_or_col:
                await worker_sleep(10)
                console.print("Aguardando informações de rateio", style="bold yellow")
            else:
                type_text_into_field(
                    "100", app["TFrmConhecimentoNotaNew"]["Edit5"], False, "0"
                )
                await worker_sleep(4)

                codigo_empresa = int(task.configEntrada.get("codigoEmpresa")) + 1000
                codigo_empresa = str(codigo_empresa)
                type_text_into_field(
                    codigo_empresa, app["TFrmConhecimentoNotaNew"]["Edit4"], False, "0"
                )
                await worker_sleep(2)

                pyautogui.click(x=1257, y=617)
                await worker_sleep(2)

                await emsys.verify_warning_and_error("Informação", "&Ok")

            await worker_sleep(5)
            pyautogui.click(x=584, y=323)
            await worker_sleep(20)

            try:
                # Verifica se o CTE ja foi lançado
                console.print("\nVerifica se o CTE ja foi lançado...")
                nf_chave_acesso = int(cte.get("chaveCte"))
                status_nf_emsys = await get_status_cte_emsys(nf_chave_acesso)
                if status_nf_emsys.get("status") == "Lançada":
                    await worker_sleep(2)
                    return RpaRetornoProcessoDTO(
                        sucesso=True,
                        retorno="CTE incluso com sucesso!",
                        status=RpaHistoricoStatusEnum.Sucesso,
                    )
                else:
                    status_retorno = status_nf_emsys.get("status")
                    await worker_sleep(2)
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Ocorreu uma falha ao tentar lançar o CTE, status retornado : {status_retorno}",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            except Exception as error:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao incluir CTE, erro: {error}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao efetuar login no EMsys, erro {return_login.retorno}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as error:
        console.print(f"Erro ao executar a função error: {error}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao incluir CTE, erro: {error}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
