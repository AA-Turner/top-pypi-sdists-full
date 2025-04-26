import asyncio
import getpass
import warnings
import os
import io
import uuid
from datetime import datetime, date
import calendar

import pyautogui
import pyperclip
import pytesseract
from pywinauto.application import Application
from pywinauto.mouse import double_click
from pywinauto.keyboard import send_keys
import win32clipboard
from PIL import Image, ImageEnhance
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
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
from worker_automate_hub.utils.util import (
    is_window_open,
    is_window_open_by_class,
    login_emsys_fiscal,
    set_variable,
    type_text_into_field,
    worker_sleep,
    kill_all_emsys,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def sped_fiscal(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza as atividades de Sped no ERP EMSys(Linx) Fiscal.

    """
    try:
        # Get config from BOF
        console.print(task)
        try:
            get_config_gerar_inventario = await get_config_by_name(
                "SPED_gerar_inventario"
            )
            console.print(get_config_gerar_inventario)
            con_config = get_config_gerar_inventario.conConfiguracao
            if con_config is not None:
                gerar_inventario = con_config.get("gerar")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Não foi possivel recuperar o valor da configuração Gerar Inventario, não sendo possivel seguir com o processo.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel recuperar o valor da configuração Gerar Inventario, erro: {e}.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        config = await get_config_by_name("login_emsys_fiscal")
        # Seta config entrada na var sped_processar para melhor entendimento
        sped_processar = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        historico_id = task.historico_id
        if historico_id:
            console.print("Historico ID recuperado com sucesso...\n")
        else:
            console.print(
                "Não foi possivel recuperar o histórico do ID, não sendo possivel enviar o arquivo SPED como retorno...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel recuperar o histórico do ID, não sendo possivel enviar o arquivo SPED como retorno",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_all_emsys()

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSysFiscal.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        await worker_sleep(4)

        try:
            app = Application(backend="win32").connect(
                class_name="TFrmLoginModulo", timeout=50
            )
        except:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir o EMSys Fiscal, tela de login não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        return_login = await login_emsys_fiscal(config.conConfiguracao, app, task)
        if return_login.sucesso == True:
            type_text_into_field(
                "Sped Fiscal", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )

            await worker_sleep(10)
            console.print(f"Verificando a presença de Confirm...")
            confirm_pop_up = await is_window_open("Confirm")
            if confirm_pop_up["IsOpened"] == True:  
                app = Application().connect(class_name="TMessageForm")
                main_window = app["TMessageForm"]
                main_window.set_focus()
                main_window.child_window(title="&No").click()
            pyautogui.click(120,173)
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Sped Fiscal' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)
        console.print(
            "Verificando se a janela para gerar Sped foi aberta com sucesso...\n"
        )
        max_attempts = 15
        i = 0
        while i < max_attempts:
            gerar_sped = await is_window_open_by_class(
                "TFrmGerarSpeed", "TFrmGerarSpeed"
            )
            if gerar_sped["IsOpened"] == True:
                console.print("janela para gerar Sped foi aberta com sucesso...\n")
                break
            else:
                await worker_sleep(1)
                i = i + 1

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela para gerar o Sped Fiscal, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        filial_cod = sped_processar.get("empresa")
        periodo_dt = sped_processar.get("periodo")

        # DIRETORIO TEMPORARIO ANTES DE SER MOVIDO PARA O GOOGLE DRIVE
        username = getpass.getuser()
        short_uuid = str(uuid.uuid4()).replace("-", "")[:6]
        temp_path_to_txt = (
            f"C:\\Users\\{username}\\Downloads\\{short_uuid}_{filial_cod}.txt"
        )
        console.print(f"Diretório temporario: {temp_path_to_txt}...\n")

        console.print("Navegando pela Janela de Gerar Sped Fiscal...\n")
        try:
            app = Application().connect(class_name="TFrmGerarSpeed")
            main_window = app["TFrmGerarSpeed"]

            main_window.set_focus()
            console.print(
                "Preenchendo as informações necessarias para gerar o sped fiscal... \n"
            )
            panel_TPage = main_window.child_window(class_name="TcxPageControl")
            panel_TTabSheet = panel_TPage.child_window(class_name="TcxTabSheet")
            panel_TTabSheet.wait("visible")

            console.print("Inserindo o diretório temporario para geração do sped...\n")
            filename = panel_TTabSheet.child_window(class_name="TFilenameEdit")
            filename.set_edit_text(temp_path_to_txt)
            await worker_sleep(2)

            console.print("Inserindo o período para geração do sped...\n")
            periodo = main_window.child_window(class_name="TDBIEditDate", found_index=0)
            periodo.set_edit_text(periodo_dt)
            await worker_sleep(1)
            periodo.type_keys("{TAB}")
            await worker_sleep(2)

            console.print("Selecionando a opção Gerar E115...\n")
            checkbox_gerar_e115 = main_window.child_window(
                class_name="TDBICheckBox", found_index=8
            )
            if not checkbox_gerar_e115.is_checked():
                checkbox_gerar_e115.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print(
                "Selecionando a opção Gerar valores zerados para notas de cfop 5929 e 6929...\n"
            )
            checkbox_gerar_cfop = main_window.child_window(
                class_name="TCheckBox", found_index=8
            )
            if not checkbox_gerar_cfop.is_checked():
                checkbox_gerar_cfop.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print("Selecionando a opção Gerar valores zerados para IPI...\n")
            checkbox_valores_ipi = main_window.child_window(
                class_name="TCheckBox", found_index=6
            )
            if not checkbox_valores_ipi.is_checked():
                checkbox_valores_ipi.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print("Gerar valores zerados para Base ST e Icms ST...\n")
            checkbox_gerar_base_ct_icms_st = main_window.child_window(
                class_name="TCheckBox", found_index=7
            )
            if not checkbox_gerar_base_ct_icms_st.is_checked():
                checkbox_gerar_base_ct_icms_st.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print("Nao gerar registro C176...\n")
            checkbox_n_regrar_registro_c176 = main_window.child_window(
                class_name="TCheckBox", found_index=1
            )
            if not checkbox_n_regrar_registro_c176.is_checked():
                checkbox_n_regrar_registro_c176.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print("Nao gerar registro C1601...\n")
            checkbox_n_regrar_registro_c1601 = main_window.child_window(
                class_name="TDBICheckBox", found_index=2
            )
            if checkbox_n_regrar_registro_c1601.is_checked():
                checkbox_n_regrar_registro_c1601.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(2)

            console.print(
                "Todos os campos selecionados com sucesso, seguindo para geração do Sped Fiscal...\n"
            )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao interagir com a tela de gerar sped fiscal, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        ano_atual = datetime.now().year
        if str(periodo_dt) == f"02/{ano_atual}":
            console.print("Filtrando período pelo Inventario...\n")
            ano_passado = ano_atual - 1
            data_busca = f"31/12/{ano_passado}"

            periodo_filtro_inicio = main_window.child_window(
                class_name="TEditDate", found_index=1
            )
            periodo_filtro_inicio.type_keys(data_busca)
            await worker_sleep(2)
            periodo_filtro_fim = main_window.child_window(
                class_name="TEditDate", found_index=0
            )
            periodo_filtro_fim.type_keys(data_busca)
            await worker_sleep(2)
            periodo_btn_buscar = main_window.child_window(
                class_name="TBitBtn", found_index=0
            )
            periodo_btn_buscar.click()
            await worker_sleep(2)
            #As vezes o click de cima não funciona
            pyautogui.click(915, 664)
            await worker_sleep(2)
            periodo_btn_buscar = main_window.child_window(
                class_name="TcxGrid", found_index=0
            )
            rect = periodo_btn_buscar.rectangle()
            center_x = (rect.left + rect.right) // 2
            center_y = (rect.top + rect.bottom) // 2
            double_click(coords=(center_x, center_y))    
        elif gerar_inventario:
            mes_atual = datetime.now().month
            if mes_atual == 1:
                mes_anterior = 12
                ano_anterior = ano_atual - 1
            else:
                mes_anterior = mes_atual - 1
                ano_anterior = ano_atual

            ultimo_dia = calendar.monthrange(ano_anterior, mes_anterior)[1]
            data_ultimo_dia = date(ano_anterior, mes_anterior, ultimo_dia)
            data_formatada = data_ultimo_dia.strftime("%d/%m/%Y")

            periodo_filtro_inicio = main_window.child_window(
                class_name="TEditDate", found_index=1
            )
            periodo_filtro_inicio.set_edit_text(data_formatada)
            await worker_sleep(2)
            periodo_filtro_fim = main_window.child_window(
                class_name="TEditDate", found_index=0
            )
            periodo_filtro_fim.set_edit_text(data_formatada)
            await worker_sleep(4)
            periodo_btn_buscar = main_window.child_window(
                class_name="TBitBtn", found_index=0
            )
            periodo_btn_buscar.click()
            await worker_sleep(2)
            #As vezes o click de cima não funciona
            pyautogui.click(915, 664)
            await worker_sleep(2)
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText("")
                win32clipboard.CloseClipboard()
            except:
                pyperclip.copy("")

            grid_inventario = main_window.child_window(
                class_name="TcxGrid", found_index=0
            )
            rect = grid_inventario.rectangle()
            center_x = (rect.left + rect.right) // 2
            center_y = (rect.top + rect.bottom) // 2
            pyautogui.moveTo(x=center_x, y=center_y)
            await worker_sleep(2)
            pyautogui.click()
            await worker_sleep(2)
            send_keys("^({HOME})")
            await worker_sleep(3)

            while True:
                last_line_inventario_emsys_fiscal = "x"
                await worker_sleep(1)
                with pyautogui.hold("ctrl"):
                    pyautogui.press("c")

                await worker_sleep(1)

                with pyautogui.hold("ctrl"):
                    pyautogui.press("c")

                win32clipboard.OpenClipboard()
                line_inventario_emsys_fiscal = win32clipboard.GetClipboardData().strip()
                win32clipboard.CloseClipboard()
                console.print(
                    f"Linha atual copiada do Emsys Fiscal: {line_inventario_emsys_fiscal}\nUltima Linha copiada: {last_line_inventario_emsys_fiscal}"
                )

                if len(line_inventario_emsys_fiscal) <= 4:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro: Nenhum registro encontrado com a data informada {periodo_btn_buscar}.",
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )

                if "no final do" in line_inventario_emsys_fiscal.lower():
                    selecionar_registro_full_path = (
                        "assets\\emsys\\button_selecionar_registro_fiscal.png"
                    )
                    try:
                        button_location = pyautogui.locateCenterOnScreen(
                            selecionar_registro_full_path, confidence=0.6
                        )
                        if button_location:
                            pyautogui.click(button_location)
                            console.print(
                                "Botão 'Selecionar Registro' clicado com sucesso!"
                            )
                            break
                    except Exception as e:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Erro: Não foi clicar na opção Selecionar Registro no Inventario, erro: {e}.",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                if bool(line_inventario_emsys_fiscal):
                    if (
                        last_line_inventario_emsys_fiscal
                        == line_inventario_emsys_fiscal
                    ):
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Erro: Não foi encontrado a opção do período de busca {periodo_filtro_inicio} nas opções do inventário.",
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                        )
                    else:
                        last_line_inventario_emsys_fiscal = line_inventario_emsys_fiscal
                        pyautogui.press("down")

        else:
            console.print(
                "Mês não é igual a Fevereiro e SPED Inventario é falso, seguindo com a geração do SPED...\n"
            )

        await worker_sleep(3)
        pesquisar_full_path = "assets\\emsys\\button_gerar_sped_fiscal.png"
        try:
            button_location = pyautogui.locateCenterOnScreen(
                pesquisar_full_path, confidence=0.6
            )
            if button_location:
                pyautogui.click(button_location)
                console.print("Botão 'Gerar Sped' clicado com sucesso!")
        except pyautogui.ImageNotFoundException:
            window_rect = main_window.rectangle()
            console.print(f"Area que sera utulizada para o recorte {window_rect}...\n")
            try:
                button_location = pyautogui.locateCenterOnScreen(
                    pesquisar_full_path,
                    region=(
                        window_rect.left,
                        window_rect.top,
                        window_rect.width(),
                        window_rect.height(),
                    ),
                )
                if button_location:
                    button_location = (
                        button_location.x + window_rect.left,
                        button_location.y + window_rect.top,
                    )
                    console.print(
                        f"Botão encontrado nas coordenadas: {button_location}"
                    )
                    pyautogui.click(button_location)
            except pyautogui.ImageNotFoundException:
                console.print(
                    "Erro - Botão de gerar o sped na tela de Gerar Sped Fiscal"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro - Botão de gerar o sped na tela de Gerar Sped Fiscal",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        except Exception as e:
            console.print(
                f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de gerar sped na tela Gerar Sped Fiscal,Error: {e}...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de gerar sped na tela Gerar Sped Fiscal,Error: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(12)
        try:
            app = Application().connect(class_name="TMsgBox")
            if "Registro de Entrada" in str(app.windows()):
                console.print(
                    f"Verificando sem possui o pop-up de Registro de Entrada... \n"
                )
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro: Livro Fiscal de Registro de Entrada não foi gerado ou não está confirmado para a empresa.",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            elif "Registro de Inventario" in str(app.windows()):
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro: POP-Up Registro de Inventario não foi gerado ou não esta confirmado para a empresa",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            elif "Apuração de ICMS" in str(app.windows()):
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro: POP-Up Apuração de ICMS, Livro de Apuração de ICMS não foi gerado no período na empresa",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
            else:
                console.print(f"POP UP: {str(app.windows())}. Continuando...\n")
        except Exception as e:
            console.print(f"Erro ao verificar janelas: {e}. Continuando...\n")

        await worker_sleep(5)
        warning_pop_up = await is_window_open("Aviso")
        if warning_pop_up["IsOpened"] == True:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro: POP-Up aviso impedindo seguir para gerar o Sped Fiscal",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(5)
        max_attempts = 100
        i = 0

        while i < max_attempts:
            try:
                app = Application().connect(class_name="TMsgBox")
                if "Informação" in str(app.windows()):
                    main_window = app["Informação"]
                    console.print(f"Tela de Informação encontrada, saindo...\n")
                    break
                elif "Aviso" in str(app.windows()):
                    main_window = app["Aviso"]
                    console.print(f"Tela de Aviso encontrada, saindo...\n")
                    break
            except Exception as e:
                console.print(f"Erro ao verificar janelas: {e}. Continuando...\n")

            warning_pop_up = await is_window_open("Aviso")
            if warning_pop_up["IsOpened"]:
                console.print(
                    f"Tela de Aviso encontrada (via função is_window_open), saindo...\n"
                )
                break
            else:
                console.print(f"Tela de Aviso não encontrada, continuando...\n")

            i += 1
            await worker_sleep(130)

        if i == max_attempts:
            console.print("Número máximo de tentativas atingido. Encerrando...")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Tempo esgotado e numero de tentativas atingido, não foi possivel obter o retorno de conclusão do SPED",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # Verificando se possui pop-up de Aviso
        await worker_sleep(6)
        warning_pop_up = await is_window_open("Aviso")
        if warning_pop_up["IsOpened"] == True:
            app = Application().connect(title="Aviso")
            main_window = app["Aviso"]
            main_window.set_focus()

            console.print(f"Obtendo texto do Aviso...\n")
            console.print(
                f"Tirando print da janela do warning para realização do OCR...\n"
            )

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
            path_to_png = f"C:\\Users\\{username}\\Downloads\\aviso_popup_{short_uuid}_{filial_cod}.png"
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
            console.print(f"Texto Full capturado {captured_text}...\n")
            os.remove(path_to_png)
            if "movimento não permitido" in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Filial: {filial_cod} está com o livro fechado ou encerrado, verificar com o setor fiscal",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            elif "não foi possiv" in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Filial: {filial_cod} Não foi possível gerar o SPED, devido a mensagem: {captured_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            elif "informe o tipo de" in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Mensagem do Aviso, Informe o tipo cobraça ",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Aviso não mapeado para seguimento do robo, mensagem: {captured_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )
        else:
            console.print(f"POP-up aviso não encontrado...\n")

        # Verifica se a info 'Arquivo do SPED gerado com sucesso' está na tela
        await worker_sleep(6)
        try:
            max_attempts = 10
            i = 0

            while i < max_attempts:
                information_pop_up_class = await is_window_open_by_class(
                    "TMsgBox", "TMsgBox"
                )
                if information_pop_up_class["IsOpened"] == True:
                    break
                else:
                    console.print(f"Aguardando confirmação de sped finalizado...\n")
                    await worker_sleep(5)
                    i += 1

            if i >= max_attempts:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Não foi possivel obter o retorno de conclusão do SPED",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print("\nArquivo do SPED gerado com sucesso...", style="bold green")
            console.log("Realizando o envio para o Backoffice...\n")
            with open(temp_path_to_txt, "rb") as file:
                file_bytes = io.BytesIO(file.read())

            await worker_sleep(6)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desArquivo = f"ArquivoSped_{filial_cod}_{timestamp}.txt"
            try:
                await send_file(
                    historico_id, desArquivo, "txt", file_bytes, file_extension="txt"
                )
                result = (
                    "Arquivo do SPED gerado com sucesso e arquivo salvo no Backoffice !"
                )
                os.remove(temp_path_to_txt)
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=result,
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            except Exception as e:
                result = f"Arquivo do SPED gerado com sucesso, porém gerou erro ao realizar o envio para o backoffice {e} - Arquivo ainda salvo na dispositivo utilizado no diretório {temp_path_to_txt} !"
                console.print(result, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=result,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

        except Exception as e:
            console.print(f"Erro ao conectar à janela Informação: {e}\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro em obter o retorno, Arquivo do SPED gerado com sucesso, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

    except Exception as ex:
        observacao = f"Erro ao gerar o Arquivo do SPED: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )