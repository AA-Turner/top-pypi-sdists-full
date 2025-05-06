import asyncio
from datetime import datetime
import warnings

import pyautogui
import pyperclip
from pywinauto.application import Application
from rich.console import Console

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
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.toast import show_toast
from worker_automate_hub.utils.util import (
    api_simplifica,
    extract_nf_number,
    faturar_pre_venda,
    find_element_center,
    find_target_position,
    kill_all_emsys,
    login_emsys,
    set_variable,
    take_screenshot,
    take_target_position,
    type_text_into_field,
    wait_nf_ready,
    wait_window_close,
    worker_sleep,
)

console = Console()

ASSETS_BASE_PATH = "assets/descartes_transferencias_images/"
ALMOXARIFADO_DEFAULT = "50"


async def transferencias(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # Inicializa variaveis
        # pre_venda_message = None
        itens_zero_qtd = []
        nota_fiscal = [None]
        log_msg = None
        valor_nota = None

        # Get config from BOF
        config = await get_config_by_name("Transferencias_Emsys")
        itens = task.configEntrada.get("itens")
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()

        # Print da resolução
        console.print(f"Largura: {screen_width}, Altura: {screen_height}")

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()
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
                "Cadastro Pré Venda", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Cadastro Pre Venda' realizada com sucesso",
                style="bold green",
            )
            await worker_sleep(3)
            try:
                app = Application().connect(class_name="TFrmSelecionaTipoPreVenda")
                select_prevenda_type = app["Selecione o Tipo de Pré-Venda"]

                if select_prevenda_type.exists():
                    tipo = select_prevenda_type.child_window(class_name="TComboBox", found_index=0)
                    tipo.select("Orçamento")
                    confirm = select_prevenda_type.child_window(class_name="TDBIBitBtn", found_index=1)
                    confirm.click()
            except:
                console.print("Sem tela de selecionar modelo de pre venda", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(7)

        # Deveríamos habilitar?
        # Preenche data de validade
        # screenshot_path = take_screenshot()
        # target_pos = find_target_position(screenshot_path, "Validade", 10, 0, 15)
        # if target_pos == None:
        #     return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de validade"}

        # Condição da Pré-Venda
        console.print("Selecionando a Condição da Pré-Venda\n")
        app = Application().connect(class_name="TFrmPreVenda")
        pre_venda = app["TFrmPreVenda"]
        condicao_field = pre_venda.child_window(class_name="TDBIComboBox", found_index=2)
        condicao_field.select("TRANSFERENCIA")
        

        # Preenche o campo do cliente com o número da filial
        cliente_field_position = await find_element_center(
            ASSETS_BASE_PATH + "field_cliente.png", (795, 354, 128, 50), 10
        )
        if cliente_field_position == None:
            cliente_field_position = (884, 384)

        pyautogui.click(cliente_field_position)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(task.configEntrada.get("filialEmpresaDestino"))
        pyautogui.hotkey("tab")
        await worker_sleep(10)

        # Clica em cancelar na Janela "Busca Representante"
        # screenshot_path = take_screenshot()
        # window_busca_representante_position = take_target_position(screenshot_path, "Representante")
        # if window_busca_representante_position is not None:
        #     button_cancelar_position = find_target_position(screenshot_path, "Cancelar", attempts=15)
        #     pyautogui.click(button_cancelar_position)
        pyautogui.click(1150, 650)

        await worker_sleep(8)

        # Aviso "Deseja alterar a condição de pagamento informada no cadastro do cliente?"
        # screenshot_path = take_screenshot()
        # payment_condition_warning_position = take_target_position(screenshot_path, "pagamento")
        # if payment_condition_warning_position is not None:
        button_no_position = (
            999,
            568,
        )  # find_target_position(screenshot_path, "No", attempts=15)
        pyautogui.click(button_no_position)
        console.print(
            f"\nClicou 'No' Mensagem 'Deseja alterar a condição de pagamento informada no cadastro do cliente?'",
            style="bold green",
        )
        await worker_sleep(10)
        # else:
        #     log_msg = f"\nError Message: Aviso de condição de pagamento não encontrado"
        #     logger.info(log_msg)
        #     console.print(log_msg, style="bold red")

        # Seleciona 'Custo Médio' (Seleção do tipo de preço)
        console.print("Seleciona 'Custo Médio' (Seleção do tipo de preço)...\n")
        # screenshot_path = take_screenshot()
        # custo_medio_select_position = find_target_position(screenshot_path, "Médio", attempts=15)
        # if custo_medio_select_position == None:
        custo_medio_select_position = (851, 523)
        # if custo_medio_select_position is not None:
        pyautogui.click(custo_medio_select_position)
        button_ok_position = (
            1042,
            583,
        )  # find_target_position(screenshot_path, "OK", attempts=15)
        pyautogui.click(button_ok_position)
        await worker_sleep(1)
        console.print(f"\nClicou OK 'Custo médio'", style="bold green")
        await worker_sleep(10)

        # Clica em ok na mensagem "Existem Pré-Vendas em aberto para este cliente."
        screenshot_path = take_screenshot()
        existing_pre_venda_position = find_target_position(
            screenshot_path, "Existem", attempts=15
        )

        if existing_pre_venda_position == None:
            existing_pre_venda_position = await find_element_center(
                ASSETS_BASE_PATH + "existing_pre_venda.png", (831, 437, 247, 156), 15
            )

        if existing_pre_venda_position is not None:
            button_ok_position = (962, 562)
            pyautogui.click(button_ok_position)
            console.print(f"\nClicou OK 'Pre Venda Existente'", style="bold green")
            await worker_sleep(5)
        else:
            log_msg = f"\nError Message: Menssagem de prevenda existente não encontrada"
            logger.info(log_msg)
            console.print(log_msg, style="bold yellow")

        # Define representante para "1"
        screenshot_path = take_screenshot()
        field_representante_position = find_target_position(
            screenshot_path, "Representante", 0, 50, attempts=15
        )

        if field_representante_position == None:
            field_representante_position = await find_element_center(
                ASSETS_BASE_PATH + "field_representante.png", (679, 416, 214, 72), 15
            )
            if field_representante_position is not None:
                lista = list(field_representante_position)
                lista[0] += 50
                lista[1] += 1
                field_representante_position = tuple(lista)

        if field_representante_position is not None:
            pyautogui.doubleClick(field_representante_position)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("del")
            pyautogui.write("1")
            pyautogui.hotkey("tab")
        else:
            pyautogui.doubleClick(800, 457)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("del")
            pyautogui.write("1")
            pyautogui.hotkey("tab")

        await worker_sleep(5)

        # Abre Menu itens
        menu_itens = await find_element_center(
            ASSETS_BASE_PATH + "menu_itens.png", (526, 286, 152, 45), 10
        )

        if menu_itens == None:
            menu_itens = (570, 317)

        if menu_itens is not None:
            pyautogui.click(menu_itens)
        else:
            log_msg = f'Campo "Itens" no menu da pré-venda não encontrado'
            await api_simplifica(
                task.configEntrada.get("urlRetorno"),
                "ERRO",
                log_msg,
                task.configEntrada.get("uuidSimplifica"),
                nota_fiscal,
                valor_nota,
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=log_msg,
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(2)

        for item in itens:
            screenshot_path = take_screenshot()
            # Clica no botão inclui para abrir a tela de item
            console.print("Clicando em Incluir...\n")
            button_incluir = (
                905,
                573,
            )  # find_target_position(screenshot_path, "Incluir", 0, 0, attempts=15)
            if button_incluir is not None:
                pyautogui.click(button_incluir)
                console.print("\nClicou em 'Incluir'", style="bold green")
            else:
                log_msg = f'Botão "Incluir" não encontrado'
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    log_msg,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            await worker_sleep(3)

            # Digita Almoxarifado
            console.print("Preenchendo o campo de almoxarifado...\n")
            screenshot_path = take_screenshot()
            field_almoxarifado = (
                839,
                313,
            )  # find_target_position(screenshot_path, "Almoxarifado",0, 129, 15)
            if field_almoxarifado is not None:
                pyautogui.doubleClick(field_almoxarifado)
                pyautogui.hotkey("del")
                pyautogui.write(
                    task.configEntrada["filialEmpresaOrigem"] + ALMOXARIFADO_DEFAULT
                )
                pyautogui.hotkey("tab")
                await worker_sleep(2)
                console.print(
                    f"\nDigitou almoxarifado {task.configEntrada["filialEmpresaOrigem"] + ALMOXARIFADO_DEFAULT}",
                    style="bold green",
                )
            else:
                log_msg = f"Campo Almoxarifado não encontrado"
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    log_msg,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

            # Segue para o campo do item
            console.print("Preenchendo o campo do item...\n")
            field_item = (
                841,
                339,
            )  # find_target_position(screenshot_path, "Item", 0, 130, 15)
            pyautogui.doubleClick(field_item)
            pyautogui.hotkey("del")
            pyautogui.write(item["codigoProduto"])
            pyautogui.hotkey("tab")
            await worker_sleep(2)
            console.print(f"\nDigitou item {item['codigoProduto']}", style="bold green")

            # Checa tela de pesquisa de item
            console.print("Verificando a existencia da tela de pesquisa de item...\n")
            screenshot_path = take_screenshot()
            window_pesquisa_item = await find_element_center(
                ASSETS_BASE_PATH + "window_pesquisa_item.png", (488, 226, 352, 175), 10
            )
            console.print(
                f"Produto {item['codigoProduto']} encontrado", style="bold green"
            )
            logger.info(f"Produto {item['codigoProduto']} encontrado")

            if window_pesquisa_item is not None:
                observacao = (
                    f"Item {item['codigoProduto']} não encontrado, verificar cadastro"
                )
                console.print(f"{observacao}", style="bold green")
                logger.info(f"{observacao}")
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    observacao,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )

            # Checa se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)
            console.print(
                "Verificando se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)...\n"
            )
            warning_price = await find_element_center(
                ASSETS_BASE_PATH + "warning_item_price.png", (824, 426, 255, 191), 10
            )
            if warning_price is not None:
                observacao = f"Item {item['codigoProduto']} não possui preço, verificar erro de estoque ou de bloqueio."
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    observacao,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )

            screenshot_path = take_screenshot()

            await worker_sleep(2)

            # Seleciona o Saldo Disponivel e verifica se ah possibilidade do descarte
            console.print(
                "Selecionando o Saldo Disponivel e verificando se há possibilidade do descarte...\n"
            )
            try:
                app = Application().connect(title="Inclui Item Pré Venda")
                item_pre_venda = app["Inclui Item Pré Venda"]
                saldo_disponivel: str = item_pre_venda.child_window(
                    class_name="TDBIEditNumber", found_index=9
                ).window_text()
            except Exception as error:
                console.print(f"Erro ao selecionar o Saldo Disponivel: {error}")
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    error,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=error,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

            try:
                # Remove parênteses, se houver
                saldo_disponivel = saldo_disponivel.strip("()")

                # Caso tenha vírgula e ponto, tratamos como separador de milhar e decimal
                if "." in saldo_disponivel and "," in saldo_disponivel:
                    saldo_disponivel = saldo_disponivel.replace(".", "").replace(
                        ",", "."
                    )
                else:
                    # Caso contrário, apenas troca a vírgula por ponto para converter o decimal
                    saldo_disponivel = saldo_disponivel.replace(",", ".")

                amount_avaliable = float(saldo_disponivel)

                console.print(
                    f"Saldo Disponivel: '{amount_avaliable}'", style="bold green"
                )
            except Exception as error:
                console.print(f"Erro ao converter o Saldo Disponível: {error}")
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    error,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=error,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
            field_quantidade = (1047,606)
            # Verifica se o saldo disponivel é valido para descartar
            if int(amount_avaliable) > 0 and int(amount_avaliable) >= int(item["qtd"]):
                pyautogui.doubleClick(field_quantidade)
                pyautogui.hotkey("del")
                pyautogui.write(str(item["qtd"]))
                pyautogui.hotkey("tab")
                await worker_sleep(2)
            else:
                if int(amount_avaliable) == 0:
                    itens_zero_qtd.append(f"DIVERGENCIA DE ESTOQUE - Item: {item["codigoProduto"]} Quantidade que deveria ser transferida: {item['qtd']} | Quantidade disponível: {amount_avaliable}")
                    #Clica cancelar
                    pyautogui.click((1194, 745))
                    await worker_sleep(5)
                    continue
                else:
                    itens_zero_qtd.append(f"DIVERGENCIA DE ESTOQUE - Item: {item["codigoProduto"]} Quantidade que deveria ser transferida: {item['qtd']} | Quantidade disponível: {amount_avaliable}")
                    pyautogui.doubleClick(field_quantidade)
                    pyautogui.hotkey("del")
                    pyautogui.write(str(amount_avaliable))
                    pyautogui.hotkey("tab")
                    await worker_sleep(2)
                # console.print(log_msg, style="bold red")
                #Clica cancelar
                # pyautogui.click((1194, 745))
                # await worker_sleep(5)
                # continue
                # return RpaRetornoProcessoDTO(
                #     sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                # )

            # Clica em incluir para adicionar o item na nota
            console.print("Clicando em incluir para adicionar o item na nota...\n")
            button_incluir_item = (1007,745)  # find_target_position(screenshot_path, "Inlcuir", 0, 0, 15)
            if button_incluir_item is not None:
                pyautogui.click(button_incluir_item)
                await worker_sleep(2)
            else:
                log_msg = f"Botao 'Incluir' item não encontrado"
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    log_msg,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                console.print(log_msg, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=log_msg,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

            try:
                # Verificar tela de Valor de custo maior que preço de venda do item
                console.print("Verificando tela de Valor de custo...\n")
                custo_window = Application().connect(title="Warning")
                custo_window = custo_window["Warning"]

                text_custo = custo_window.window_text()
                if "Warning" in text_custo:
                    log_msg = f"O valor de custo do Item: {item['codigoProduto']} é maior que o valor de venda."
                    await api_simplifica(
                        task.configEntrada["urlRetorno"],
                        "ERRO",
                        log_msg,
                        task.configEntrada["uuidSimplifica"],
                        nota_fiscal,
                        valor_nota,
                    )
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=log_msg,
                        status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                    )
            except:
                console.log(
                    "Nenhuma tela de warning foi encontrada", style="bold green"
                )

            try:
                # Verificando janela Confirm - Item já incluido nesta pré-venda, Deseja continuar?
                console.print(
                    "Verificando janela Confirm - Item já incluido nesta pré-venda, Deseja continuar?...\n"
                )
                custo_window = Application().connect(title="Confirm")
                custo_window = custo_window["Confirm"]

                text_custo = custo_window.window_text()
                if "Confirm" in text_custo:
                    btn_window = custo_window["&Yes"]
                    if btn_window.exists():
                        btn_window.click()
                        console.print(f" botão Yes clicado com sucesso")
                    else:
                        console.print(f"Botão Yes Não encontrado")

            except:
                console.log(
                    "Nenhuma tela de Confirm - Item já incluido nesta pré-venda foi encontrada",
                    style="bold green",
                )

            # Clica em cancelar para fechar a tela e abrir novamente caso houver mais itens
            console.print(
                "Clicando em cancelar para fechar a tela e abrir novamente caso houver mais itens...\n"
            )
            button_cancela_item = (
                1194,
                745,
            )  # find_target_position(screenshot_path, "Cancela", 0, 0, 15)
            if button_cancela_item is not None:
                pyautogui.click(button_cancela_item)
                await worker_sleep(2)
            else:
                log_msg = f"Botao cancelar para fechar a tela do item nao encontrado"
                await api_simplifica(
                    task.configEntrada["urlRetorno"],
                    "ERRO",
                    log_msg,
                    task.configEntrada["uuidSimplifica"],
                    nota_fiscal,
                    valor_nota,
                )
                console.print(log_msg, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

        await worker_sleep(5)

        # Volta para Capa
        pyautogui.click(578, 302)

        # Clica no botão "+" no canto superior esquerdo para lançar a pre-venda
        screenshot_path = take_screenshot()
        button_lanca_pre_venda = await find_element_center(
            ASSETS_BASE_PATH + "button_lanca_prevenda.png", (490, 204, 192, 207), 15
        )
        if button_lanca_pre_venda is not None:
            pyautogui.click(button_lanca_pre_venda.x, button_lanca_pre_venda.y)
            console.print("\nLançou Pré-Venda", style="bold green")
        else:
            log_msg = f"Botao lança pre-venda nao encontrado"
            await api_simplifica(
                task.configEntrada.get("urlRetorno"),
                "ERRO",
                log_msg,
                task.configEntrada.get("uuidSimplifica"),
                nota_fiscal,
                valor_nota,
            )
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=log_msg,
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(8)

         # Verifica mensagem de "Pré-Venda incluida com número: xxxxx"
        console.print(
            "Verificando mensagem de 'Pré-Venda incluida com número: xxxxx'...\n"
        )
        # Clica no ok da mensagem
        try:
            app = Application().connect(title="Informação")
            dialog = app.window(title="Informação")

            btn_yes = dialog.child_window(title="OK", class_name="Button")
            if btn_yes.exists():
                try:
                    btn_yes.click()
                    await worker_sleep(3)
                    console.print(
                        "O botão OK de pré-venda incluída foi clicado com sucesso.",
                        style="green",
                    )
                except Exception as e:
                    console.print(
                        f"Falha ao clicar no botão OK de pré-venda incluída: {e}",
                        style="red",
                    )
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Falha ao clicar no botão OK de pré-venda incluída: {e}",
                        status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                    )
            else:

                console.print(
                    "O Botão OK de pré-venda incluída não foi encontrado.", style="red"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="O Botão OK de pré-venda incluída não foi encontrado.",
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

        except Exception as e:
            console.print(
                f"O Botão OK de pré-venda incluída não foi encontrado: {e}", style="red"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"O Botão OK de pré-venda incluída não foi encontrado: {e}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(5)

        # Message 'Deseja pesquisar pré-venda?'
        console.print(
            "Verificando a existencia da mensagem: 'Deseja pesquisar pré-venda?'...\n"
        )
        try:
            app = Application().connect(title="Confirm")
            dialog_prevenda = app.window(title="Confirm")

            btn_yes = dialog_prevenda.child_window(title="&Yes", class_name="TButton")
            if btn_yes.exists():
                try:
                    btn_yes.click()
                    await worker_sleep(3)
                    console.print(
                        "O botão YES de pesquisa pré-venda incluída foi clicado com sucesso.",
                        style="green",
                    )
                except Exception as e:
                    console.print(
                        f"Falha ao clicar no botão YES de pesquisa pré-venda incluída: {e}",
                        style="red",
                    )
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Falha ao clicar no botão YES de pesquisa pré-venda incluída: {e}",
                        status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                    )
            else:

                console.print(
                    "O Botão OK de pré-venda incluída não foi encontrado.", style="red"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="O Botão YES de pesquisa pré-venda incluída não foi encontrado.",
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

        except Exception as e:
            console.print(
                f"O Botão YES de pesquisa pré-venda incluída não foi encontrado: {e}", style="red"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"O Botão YES de pesquisa pré-venda incluída não foi encontrado: {e}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )


        await worker_sleep(5)
        
        # Confirma pré-venda
        # Pode não precisar em descartes, mas em trânsferencias é obrigatório
        try:
            app = Application().connect(class_name="TFrmPreVenda")
            pre_venda = app["TFrmPreVenda"]
            confirma_pre_venda = pre_venda.child_window(title="&Confirma", class_name="TBitBtn")
            
            if confirma_pre_venda.exists():
                if confirma_pre_venda.is_enabled():
                    confirma_pre_venda.click()
            else:
                log_msg = f"Botao 'Confirma' nao encontrado"
                console.print(log_msg, style="bold yellow")
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao clicar no botão 'Confirma': {e}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        # pyautogui.moveTo(1200, 300)
        await worker_sleep(5)

        console.print("Verificando a mensagem: Confirmar transferencia...\n")
        try:
            app = Application().connect(class_name="TMessageForm")
            cofirma_pre_venda = app["TMessageForm"]
            confirma_pre_venda_yes = cofirma_pre_venda.child_window(title="&Yes", class_name="TButton")
            if confirma_pre_venda_yes.exists():
                if confirma_pre_venda_yes.is_enabled():
                    confirma_pre_venda_yes.click()
            else:
                log_msg = f"Confirmação pré-venda da transferência nao encontrada"
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=log_msg,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao confirmar pre venda: {e}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
        await worker_sleep(5)
        try:
            app = Application().connect(class_name="TMessageForm")
            confirmada_pre_venda = app["TMessageForm"]
            confirmada_pre_venda_ok = confirmada_pre_venda.child_window(title="OK", class_name="TButton")
            if confirmada_pre_venda_ok.exists():
                if confirmada_pre_venda_ok.is_enabled():  
                    confirmada_pre_venda_ok.click()
            else:
                log_msg = f"Tela de pré-venda confirmada nao encontrada"
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=log_msg,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )    
        except Exception as e:
            log_msg = f"Tela de pré-venda confirmada nao encontrada"
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=log_msg,
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )   
        await worker_sleep(10)

        # Faturando Pre-venda
        retorno = await faturar_pre_venda(task)
        if retorno.get("sucesso") == True:
            console.log(f"Faturou com sucesso!", style="bold green")
            valor_nota = retorno.get("valor_nota")
        else:
            await api_simplifica(
                task.configEntrada.get("urlRetorno"),
                "ERRO",
                retorno["retorno"] + f"Número da nota: {nota_fiscal} | Valor: {valor_nota}",
                task.configEntrada.get("uuidSimplifica"),
                None,
                None,
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno.get("retorno"),
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        # Extraindo nota fiscal
        await worker_sleep(5)
        console.log("Extraindo numero da nota fiscal", style="bold green")
        nota_fiscal = await extract_nf_number()
        console.print(f"\nNumero NF: '{nota_fiscal}'", style="bold green")

        await worker_sleep(7)

        # Transmitir a nota
        console.print("Transmitindo a nota...\n", style="bold green")
        pyautogui.click(875, 596)
        logger.info("\nNota Transmitida")
        console.print("\nNota Transmitida", style="bold green")

        await worker_sleep(60)

        # aguardando nota ser transmitida
        nf_ready = await wait_nf_ready()
        if nf_ready['sucesso'] == True:
            # Clica em ok "processo finalizado"
            await worker_sleep(3)
            pyautogui.click(957, 556)
            # Clica em fechar
            await worker_sleep(3)
            pyautogui.click(1200, 667)
            log_msg = f"Nota lançada com sucesso! Número da nota: {nota_fiscal} | Valor: {valor_nota}" + (f" | Itens com quantidade zerada: {itens_zero_qtd}" if itens_zero_qtd else "")
            await api_simplifica(
                task.configEntrada.get("urlRetorno"),
                "SUCESSO",
                log_msg,
                task.configEntrada.get("uuidSimplifica"),
                nota_fiscal,
                valor_nota,
            )
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=log_msg,
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        else:
            log_msg = f"Erro Processo Transferências: Número da nota: {nota_fiscal} | Valor: {valor_nota}" + (f" | Itens com quantidade zerada: {itens_zero_qtd}" if itens_zero_qtd else "")
        
            console.print(log_msg)
            logger.error(log_msg)
            await api_simplifica(
            task.configEntrada["urlRetorno"],
            "ERRO",
            log_msg,
            task.configEntrada["uuidSimplifica"],
            nota_fiscal,
            valor_nota,
            )
            show_toast("Falha", log_msg)
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )

    except Exception as ex:
        log_msg = f"Erro Processo Transferências: {ex} | Número da nota: {nota_fiscal} | Valor: {valor_nota}" + (f" | Itens com quantidade zerada: {itens_zero_qtd}" if itens_zero_qtd else "")
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        await api_simplifica(
            task.configEntrada.get("urlRetorno"),
            "ERRO",
            log_msg,
            task.configEntrada.get("uuidSimplifica"),
            nota_fiscal,
            valor_nota,
        )
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
