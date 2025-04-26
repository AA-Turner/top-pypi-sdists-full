import asyncio
import warnings
from datetime import datetime

import pyautogui
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.decorators.timeit import timeit
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
    kill_process,
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


@timeit
async def descartes(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # Inicializa variaveis
        nota_fiscal = [None]
        log_msg = None
        valor_nota = None
        # Get config from BOF
        console.print("Obtendo configuração...\n")
        config = await get_config_by_name(name="Descartes_Emsys")
        # Popula Variaveis
        itens = task.configEntrada.get("itens", [])
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()

        # Print da resolução
        console.print(f"Largura: {screen_width}, Altura: {screen_height}")

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
            console.print("Pesquisando por: Cadastro Pré Venda")
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

        # Preenche data de validade
        console.print("Preenchendo a data de validade...", style="bold green")
        
        pre_venda = app["TFrmPreVenda"]
        app = Application().connect(class_name="TFrmPreVenda")
        validade_field = pre_venda.child_window(class_name="TDBIEditDate", found_index=0)
        validade_field.set_text(f'{datetime.now().strftime("%d/%m/%Y")}')
        # screenshot_path = take_screenshot()
        # target_pos = (
        #     961,
        #     321,
        # )  # find_target_position(screenshot_path, "Validade", 10, 0, 15)
        # if target_pos == None:
        #     return RpaRetornoProcessoDTO(
        #         sucesso=False,
        #         retorno="Não foi possivel encontrar o campo de validade",
        #         status=RpaHistoricoStatusEnum.Falha,
        #     )

        # pyautogui.click(target_pos)
        # pyautogui.write(f'{datetime.now().strftime("%d/%m/%Y")}', interval=0.1)
        # pyautogui.press("tab")
        console.print(
            f"\nValidade Digitada: '{datetime.now().strftime("%d/%m/%Y")}'\n",
            style="bold green",
        )
        await worker_sleep(1)

        # Condição da Pré-Venda
        console.print("Selecionando a Condição da Pré-Venda\n")
        condicao_field = pre_venda.child_window(class_name="TDBIComboBox", found_index=2)
        condicao_field.select("A VISTA")

        # condicao_field = find_target_position(screenshot_path, "Condição", 10, 0, 15)
        # if condicao_field == None:
        #     condicao_field = (1054, 330)

        # pyautogui.click(condicao_field)
        # await worker_sleep(1)
        # pyautogui.write("A")
        # await worker_sleep(1)
        # pyautogui.press("down")
        # pyautogui.press("enter")
        # await worker_sleep(1)

        # Preenche o campo do cliente com o número da filial
        console.print("Preenchendo o campo do cliente com o número da filial...\n")
        cliente_field_position = await find_element_center(
            ASSETS_BASE_PATH + "field_cliente.png", (795, 354, 128, 50), 10
        )
        if cliente_field_position == None:
            cliente_field_position = (884, 384)

        pyautogui.click(cliente_field_position)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(task.configEntrada["filialEmpresaOrigem"])
        pyautogui.hotkey("tab")
        await worker_sleep(10)

        try:
            # Verificando a existência da janela Busca representante e clicando em Cancelar
            console.print(
                "Verificando a existência da janela Busca representante e clicando em Cancelar...\n"
            )
            app = Application().connect(class_name="TFrmBuscaGeralDialog")
            app = app["TFrmBuscaGeralDialog"]
            btn_cancelar = app.child_window(title="&Cancelar", class_name="TBitBtn")
            if btn_cancelar.exists():
                app.set_focus()
                btn_cancelar.click_input()
                console.print(f" botão Cancelar clicado com sucesso")
            else:
                console.print(f"Botão Cancelar Não encontrado")

        except:
            console.log(
                f"Nenhuma tela de Busca representante foi encontrada.",
                style="bold green",
            )

        await worker_sleep(2)

        # Verifica se precisa selecionar endereço
        console.print("Verificando se precisa selecionar endereço...\n")
        screenshot_path = take_screenshot()
        window_seleciona_endereco_position = take_target_position(
            screenshot_path, "Endereço"
        )
        if window_seleciona_endereco_position is not None:
            log_msg = f"Aviso para selecionar Endereço | Número da nota: {nota_fiscal} | Valor: {valor_nota}"
            await api_simplifica(
                task.configEntrada["urlRetorno"],
                "ERRO",
                log_msg,
                task.configEntrada["uuidSimplifica"],
                nota_fiscal,
                valor_nota,
            )
            return RpaRetornoProcessoDTO(
                sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
            )
        else:
            log_msg = f"Sem Aviso de Seleção de Endereço Número da nota: {nota_fiscal} | Valor: {valor_nota}"
            console.print(log_msg, style="bold green")
            logger.info(log_msg)

        await worker_sleep(5)

        # Aviso "Deseja alterar a condição de pagamento informada no cadastro do cliente?"
        console.print(
            "Verificando alerta de alteração de pagamento informada no cadastro do cliente...\n"
        )
        # screenshot_path = take_screenshot()
        # payment_condition_warning_position = take_target_position(screenshot_path, "pagamento")
        # if payment_condition_warning_position is not None:
        button_no_position = (
            1000,
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
        custo_medio_select_position = (851, 523)
        pyautogui.click(custo_medio_select_position)
        await worker_sleep(1)
        button_ok_position = (1042,583)
        pyautogui.click(button_ok_position)
        await worker_sleep(1)
        console.print(f"\nClicou OK 'Custo médio'", style="bold green")

        await worker_sleep(5)

        # Clica em ok na mensagem "Existem Pré-Vendas em aberto para este cliente."
        console.print("Clica em ok na mensagem 'Existem Pré-Vendas em aberto para este cliente.'\n")
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
        console.print("Definindo representante para '1'\n")
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
            # pyautogui.move(789, 523)
        await worker_sleep(5)

        # Seleciona modelo de capa
        console.print("Selecionando o modelo de capa...")
        # screenshot_path = take_screenshot()
        # model_descarte_position = find_target_position(
        #     screenshot_path, "Modelo", 0, 100, attempts=8
        # )

        # if model_descarte_position == None:
        #     model_descarte_position = await find_element_center(
        #         ASSETS_BASE_PATH + "field_modelo_faturamento.png",
        #         (681, 489, 546, 96),
        #         15,
        #     )
        #     if model_descarte_position is not None:
        #         lista = list(model_descarte_position)
        #         lista[0] += 100
        #         model_descarte_position = tuple(lista)

        # if model_descarte_position == None:
        model_descarte_position = (848, 527)

        if model_descarte_position is not None:
            # pyautogui.click(848, 527)
            pyautogui.click(model_descarte_position)
            pyautogui.click(1500, 800)
            pyautogui.write("B")
            pyautogui.hotkey("tab")
        else:
            log_msg = f"Campo Modelo na capa da nota não encontrado | Número da nota: {nota_fiscal} | Valor: {valor_nota}"
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

        # Abre Menu itens
        console.print("Abrindo Menu Itens...\n")
        menu_itens = await find_element_center(
            ASSETS_BASE_PATH + "menu_itens.png", (526, 286, 152, 45), 10
        )

        if menu_itens == None:
            menu_itens = (570, 317)

        if menu_itens is not None:
            pyautogui.click(menu_itens)
        else:
            log_msg = f'Campo "Itens" no menu da pré-venda não encontrado. | Número da nota: {nota_fiscal} | Valor: {valor_nota}'
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

        await worker_sleep(2)

        # Loop de itens
        console.print("Inicio do loop de itens\n")

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
                log_msg = f'Botão "Incluir" não encontrado | Número da nota: {nota_fiscal} | Valor: {valor_nota}'
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
                log_msg = f"Campo Almoxarifado não encontrado | Número da nota: {nota_fiscal} | Valor: {valor_nota}"
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
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO( descricao=RpaTagEnum.Tecnico)],
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

            # Verifica se o saldo disponivel é valido para descartar
            if int(amount_avaliable) > 0 and int(amount_avaliable) >= int(item["qtd"]):
                field_quantidade = (
                    1047,
                    606,
                )  # find_target_position(screenshot_path, "Quantidade", 20, 0, 15)
                pyautogui.doubleClick(field_quantidade)
                pyautogui.hotkey("del")
                pyautogui.write(str(item["qtd"]))
                pyautogui.hotkey("tab")
                await worker_sleep(2)
            else:
                log_msg = f"Saldo disponivel: '{amount_avaliable}' é menor que '{item['qtd']}' o valor que deveria ser descartado. Item: '{item['codigoProduto']}'"
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
                    sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                )

            # Clica em incluir para adicionar o item na nota
            console.print("Clicando em incluir para adicionar o item na nota...\n")
            button_incluir_item = (
                1007,
                745,
            )  # find_target_position(screenshot_path, "Inlcuir", 0, 0, 15)
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

        await worker_sleep(2)

        # Clica no botão "+" no canto superior esquerdo para lançar a pre-venda
        console.print(
            "Clica no botão '+' no canto superior esquerdo para lançar a pre-venda"
        )
        # Precisa manter por imagem pois não tem texto
        button_lanca_pre_venda = await find_element_center(
            ASSETS_BASE_PATH + "button_lanca_prevenda.png", (490, 204, 192, 207), 15
        )
        if button_lanca_pre_venda is not None:
            pyautogui.click(button_lanca_pre_venda.x, button_lanca_pre_venda.y)
            console.print("\nLançou Pré-Venda", style="bold green")
        else:
            log_msg = f"Botao lança pre-venda nao encontrado"
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

        await worker_sleep(15)

        # Verifica mensagem de "Pré-Venda incluida com número: xxxxx"
        console.print(
            "Verificando mensagem de 'Pré-Venda incluida com número: xxxxx'...\n"
        )
        # Clica no ok da mensagem
        try:
            app = Application().connect(title="Informação")
            dialog = app.window(title="Informação")

            btn_ok = dialog.child_window(title="OK", class_name="Button")
            if btn_ok.exists():
                try:
                    btn_ok.click()
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

        screenshot_path = take_screenshot()

        # Message 'Deseja pesquisar pré-venda?'
        console.print(
            "Verificando a existencia da mensagem: 'Deseja pesquisar pré-venda?'...\n"
        )
        message_prevenda = take_target_position(screenshot_path, "Deseja")
        if message_prevenda is not None:
            button_yes = find_target_position(screenshot_path, "Yes", attempts=5)
            if button_yes is not None:
                pyautogui.click(button_yes)
            else:
                pyautogui.click(914,560)
        else:
            log_msg = f"Mensagem 'Deseja pesquisar pré-venda?' não encontrada."
            console.print(log_msg, style="bold yellow")

        screenshot_path = take_screenshot()
        # Confirma pré-venda
        # Pode não precisar em descartes, mas em trânsferencias é obrigatório
        app = Application().connect(class_name="TFrmPreVenda")
        pre_venda = app["TFrmPreVenda"]
        confirma_pre_venda = pre_venda.child_window(title="&Confirma", class_name="TBitBtn")
        
        if confirma_pre_venda.exists():
            if confirma_pre_venda.is_enabled():
                confirma_pre_venda.click()
        else:
            log_msg = f"Botao 'Confirma' nao encontrado"
            console.print(log_msg, style="bold yellow")
        # console.print("Confirmando a Pre-Venda...\n")
        # screenshot_path = take_screenshot()
        # button_confirma_transferencia = take_target_position(
        #     screenshot_path, "confirma"
        # )
        # if button_confirma_transferencia is not None:
        #     pyautogui.click(button_confirma_transferencia)
        #     console.log("Confirmou transferencia", style="bold green")
        # else:
        #     try:
        #         confirma = pyautogui.locateOnScreen("assets\\descartes_transferencias_images\\button_confirma.png", grayscale=True, region=[1225, 289, 1388, 362])
        #         pyautogui.click(confirma)
        #     except:
        #         log_msg = f"Botao 'Confirma' não encontrado"
        #         console.print(log_msg, style="bold yellow")
                # return RpaRetornoProcessoDTO(
                # sucesso=False,
                # retorno=log_msg,
                # status=RpaHistoricoStatusEnum.Falha)

        pyautogui.moveTo(1200, 300)

        console.print("Verificando a mensagem: Confirmar transferencia...\n")
        await worker_sleep(5)
        pyautogui.moveTo(1200, 300)
        screenshot_path = take_screenshot()
        message_confirma_transferencia = take_target_position(
            screenshot_path, "confirmar"
        )
        if message_confirma_transferencia is not None:
            # clica em sim na mensagem
            screenshot_path = take_screenshot()
            button_yes = find_target_position(screenshot_path, "Yes", attempts=8)
            pyautogui.click(button_yes)
            console.log(
                "Cliclou em 'Sim' para cofirmar a pré-venda", style="bold green"
            )
            await worker_sleep(3)
            pyautogui.click(956, 559)
            pyautogui.moveTo(1200, 300)
            
            await worker_sleep(5)
            screenshot_path = take_screenshot()
            vencimento_message_primeira_parcela = take_target_position(
                screenshot_path, "vencimento"
            )
            # Pode nao aparecer na prod
            if vencimento_message_primeira_parcela is not None:
                button_yes = find_target_position(screenshot_path, "Yes", attempts=15)
                pyautogui.click(button_yes)
            await worker_sleep(5)
            screenshot_path = take_screenshot()
            # Clica no OK 'Pre-Venda incluida com sucesso'
            button_ok = find_target_position(screenshot_path, "Ok", attempts=15)
            pyautogui.click(button_ok)
            console.log(
                "Cliclou em 'OK' para pré-venda confirmada com sucesso",
                style="bold green",
            )
        else:
            log_msg = (
                f"Mensagem 'Deseja realmente confirmar esta pré-venda?' não encontrada."
            )
            console.print(log_msg, style="bold yellow")

        pyautogui.moveTo(1000, 500)
        await worker_sleep(10)

        retorno = await faturar_pre_venda(task)
        if retorno["sucesso"] == True:
            console.log(f"Faturou com sucesso!", style="bold green")
            valor_nota = retorno["valor_nota"]
        else:
            await api_simplifica(
                task.configEntrada["urlRetorno"],
                "ERRO",
                retorno["retorno"],
                task.configEntrada["uuidSimplifica"],
                nota_fiscal,
                valor_nota,
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno["retorno"],
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        await worker_sleep(10)

        # Mensagem de nota fiscal gerada com número
        log_msg = "Extraindo numero da nota fiscal"
        console.log(log_msg, style="bold green")
        logger.info(log_msg)
        nota_fiscal = await extract_nf_number()
        console.print(f"\nNumero NF: '{nota_fiscal}'", style="bold green")

        await worker_sleep(15)

        # Transmitir a nota
        console.print("Transmitindo a nota...\n", style="bold green")
        pyautogui.click(875, 596)
        logger.info("\nNota Transmitida")
        console.print("\nNota Transmitida", style="bold green")

        await worker_sleep(50)

        # aguardando nota ser transmitida
        nf_ready = await wait_nf_ready()
        if nf_ready['sucesso'] == True:
            # Clica em ok "processo finalizado"
            await worker_sleep(3)
            pyautogui.click(957, 556)
            # Clica em fechar
            await worker_sleep(3)
            pyautogui.click(1200, 667)
            log_msg = f"Nota lançada com sucesso! Número da nota: {nota_fiscal} | Valor: {valor_nota}"
            await api_simplifica(
                task.configEntrada["urlRetorno"],
                "SUCESSO",
                log_msg,
                task.configEntrada["uuidSimplifica"],
                nota_fiscal,
                valor_nota,
            )
            show_toast("Sucesso", f"Processo Descartes finalizado com sucesso")
            return RpaRetornoProcessoDTO(
                sucesso=True, retorno=log_msg, status=RpaHistoricoStatusEnum.Sucesso
            )
        else:
            log_msg = f"{nf_ready['retorno']}. Número da nota: {nota_fiscal} | Valor: {valor_nota}"
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
        log_msg = f"Erro Processo Descartes: {ex} | Número da nota: {nota_fiscal} | Valor: {valor_nota}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
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