import asyncio
import warnings
from datetime import datetime, date

import pyautogui
from pywinauto.application import Application
from pywinauto.mouse import double_click
from pywinauto.keyboard import send_keys
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
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
    ocr_title,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def lancamento_pis_cofins(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza as atividades de lançamento do PIS & Cofins no ERP EMSys(Linx) Fiscal.

    """
    try:
        console.print(task)
        ASSETS_PATH = "assets"

        config = await get_config_by_name("login_emsys_fiscal")
        # Seta conffig entrada na var sped_processar para melhor entendimento
        lancamento_pis_cofins_processar = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

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
                class_name="TFrmLoginModulo", timeout=120
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
                "Livro de Apuração Pis Cofins",
                app["TFrmMenuPrincipal"]["Edit"],
                True,
                "50",
            )

            await worker_sleep(10)
            console.print(f"Verificando a presença de Confirm...")
            confirm_pop_up = await is_window_open("Confirm")
            if confirm_pop_up["IsOpened"] == True:
                app = Application().connect(class_name="TMessageForm")
                main_window = app["TMessageForm"]
                main_window.set_focus()
                main_window.child_window(title="&No").click()
            pyautogui.click(120, 173)
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Livro de Apuração PIS Cofins' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(8)
        console.print(
            "Verificando se a janela Movimento de Apuração PIS / COFINS foi aberta com sucesso...\n"
        )
        max_attempts = 15
        i = 0
        while i < max_attempts:
            movimento_apura_pis_cofins = await is_window_open_by_class(
                "TFrmMovtoApuraPisCofins", "TFrmMovtoApuraPisCofins"
            )
            if movimento_apura_pis_cofins["IsOpened"] == True:
                console.print(
                    "janela Movimento de Apuração PIS / COFINS foi aberta com sucesso...\n"
                )
                break
            else:
                await worker_sleep(1)
                i = i + 1

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela Movimento de Apuração PIS / COFINS, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        filial_cod = lancamento_pis_cofins_processar.get("empresa")
        periodo_dt = lancamento_pis_cofins_processar.get("periodo")

        await worker_sleep(1)
        # Preenchendo os campos necessarios de período e selecionando todas as empresas
        console.print(f"\Informando o período... ", style="bold green")
        app = Application().connect(class_name="TFrmMovtoApuraPisCofins", timeout=120)
        main_window = app["TFrmMovtoApuraPisCofins"]
        main_window.set_focus()

        console.print("Inserindo o período...\n")
        periodo_field = main_window.child_window(
            class_name="TDBIEditDate", found_index=0
        )
        periodo_field.set_edit_text(periodo_dt)

        # console.print("Selecionando Replicar para empresas...\n")
        # replicar_para_empresas_check = main_window.child_window(
        #     class_name="TcxCheckBox", found_index=0
        # )
        # replicar_para_empresas_check.click_input()
        # console.print(
        #     "A opção 'Aplicar Rateio aos Itens Selecionados' selecionado com sucesso... \n"
        # )
        try:
            await worker_sleep(5)
            console.print("Confirmando Pop-up - ...Pode causar lentidão no sistema...\n")
            console.print(f"Verificando a presença de Confirm...")
            confirm_pop_up = await is_window_open_by_class("TMessageForm", "TMessageForm")
            if confirm_pop_up["IsOpened"] == True:
                app = Application().connect(class_name="TMessageForm")
                main_window = app["TMessageForm"]
                main_window.set_focus()
                main_window.child_window(title="&Yes").click()
                console.print(f"Yes clicado com sucesso...")

            await worker_sleep(5)
            console.print(
                f"Verificando se foi aberto a tela de Seleção de Empresas clicado com sucesso..."
            )
            selecao_empresas_screen = await is_window_open_by_class(
                "TFrmSelecionaEmpresas", "TFrmSelecionaEmpresas"
            )
            if selecao_empresas_screen["IsOpened"] == True:
                console.print(f"Janela de Seleção de Empresas foi aberta com sucesso...")
                app = Application().connect(class_name="TFrmSelecionaEmpresas", timeout=120)
                main_window = app["TFrmSelecionaEmpresas"]
                main_window.set_focus()
                console.print(f"Clicando em seleciona todas...")
                try:
                    selecionar_todos_itens = (
                        ASSETS_PATH + "\\lancamento_pis_cofins\\btn_selecionar_todas.png"
                    )
                    # Tenta localizar a imagem na tela
                    localizacao = pyautogui.locateOnScreen(
                        selecionar_todos_itens, confidence=0.9
                    )
                    await worker_sleep(3)
                    if localizacao:
                        centro = pyautogui.center(localizacao)
                        pyautogui.moveTo(centro)
                        pyautogui.click()
                        console.print("Clique realizado com sucesso!")
                    else:
                        console.print("Imagem não encontrada na tela.")
                except Exception as e:
                    retorno = f"Não foi possivel clicar em selecionar todos os itens na Seleção de Empresas, erro: {e} "
                    pass
                try:            
                    console.print(f"Clicando em OK - para andamento do processo...")
                    app = Application().connect(class_name="TFrmSelecionaEmpresas", timeout=120)
                    main_window = app["TFrmSelecionaEmpresas"]
                    main_window.set_focus()

                    try:
                        btn_ok = main_window.child_window(title="OK")
                        btn_ok.click()
                    except:
                        btn_ok = main_window.child_window(title="&OK")
                        btn_ok.click()

                    await worker_sleep(3)
                except:
                    pass
        except:
            pass
              
        try:
            selecionar_todos_itens = (
                ASSETS_PATH + "\\lancamento_pis_cofins\\botao_incluir.png"
            )
            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateOnScreen(
                selecionar_todos_itens, confidence=0.9
            )
            await worker_sleep(3)
            if localizacao:
                centro = pyautogui.center(localizacao)
                pyautogui.moveTo(centro)
                pyautogui.click()
                console.print("Clique realizado com sucesso!")
            else:
                console.print("Imagem não encontrada na tela.")
        except Exception as e:
            pass
        
        await worker_sleep(10)
        
        try:
            app = Application().connect(title="Aviso", timeout=10)
            main_window = app["Aviso"]
            main_window.set_focus()

            # Pega o segundo Static usando child_window (não children)
            aviso = main_window.child_window(class_name="Static", found_index=1)
            texto_aviso = aviso.window_text()

            if "livro fiscal com status diferente de Confirmado/Encerrado" in texto_aviso:
                retorno = texto_aviso
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )

        except Exception as e:
            print(f"Erro ao capturar o aviso: {e}")
        
        await worker_sleep(2)

        # Verificar se já existe registro no mês apurado
        try:
            selecionar_todos_itens = ASSETS_PATH + "\\lancamento_pis_cofins\\ja_existe_periodo.png"

            localizacao = None
            for tentativa in range(10):
                localizacao = pyautogui.locateOnScreen(selecionar_todos_itens, confidence=0.9)
                if localizacao:
                    break
                await worker_sleep(2)  # espera 2 segundos antes da próxima tentativa

            if localizacao:
                app = Application().connect(title="Informação", timeout=60)
                main_window = app["Informação"]
                main_window.set_focus()
                informacao = main_window.child_window(title="OK")
                informacao.click()
                console.print("Clique realizado com sucesso!")
            else:
                console.print("Imagem não encontrada na tela após 10 tentativas.")

        except Exception as e:
            pass


        await worker_sleep(5)
        try:
            console.print("Verificando se possui tela de Informação... \n")
            information_pop_up = await is_window_open("Information")
            if information_pop_up["IsOpened"] == True:
                msg_pop_up = await ocr_title("Information_pop_up_cofins", "Informação")
                console.print(f"retorno:{msg_pop_up.sucesso}")
                console.print(f"retorno:{msg_pop_up}")
                if msg_pop_up.sucesso == True:
                    msg_retorno = msg_pop_up.retorno
                    console.print(msg_retorno)
                    retorno = f"Pop up nao mapeado para seguimento do robo {msg_pop_up.retorno}"
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=retorno,
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                    )
                else:
                    retorno = f"Não foi possivel realizar a confirmação do msg do OCR após clicar em Incluir na tela de Movimento de Apuração PIS / COFINS"
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=retorno,
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )
            else:
                console.print("Não possui tela de Informação... \n")
        except:
            pass
        # PRECISO TESTAR ADICIONAR EXCESSÃO PARA A TELA DE AVISO
        pop_up_aviso = []
        console.print(f"Verificando se possui tela de Aviso...")
        while True:
            aviso_screen_opened = await is_window_open("Aviso")
            if aviso_screen_opened["IsOpened"] == True:
                msg_pop_up = await ocr_title("aviso_pop_up_cofins", "Aviso")
                console.print(f"retorno:{msg_pop_up.sucesso}")
                if msg_pop_up.sucesso == True:
                    msg_retorno = msg_pop_up.retorno
                    console.print(msg_retorno)
                    pop_up_aviso.append(msg_retorno)

                    app = Application().connect(title="Aviso", timeout=120)
                    main_window = app["Aviso"]
                    main_window.set_focus()

                    try:
                        btn_ok = main_window.child_window(title="OK")
                        btn_ok.click()
                    except:
                        btn_ok = main_window.child_window(title="&OK")
                        btn_ok.click()

                    await worker_sleep(5)
            else:
                break

            if len(pop_up_aviso) > 0:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Livro de apuração diferente de Confirmado/Encerrado:  {pop_up_aviso}",
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
                )
            else:
                console.print(
                    "Não possui tela de Aviso ou Pop-up de informação, seguindo com o andamento do processo... \n"
                )
                try:
                    app = Application().connect(class_name="TFrmMovtoApuraPisCofins", timeout=60)
                    main_window = app["TFrmMovtoApuraPisCofins"]
                    
                    # Tenta fechar a janela até 10 vezes
                    for tentativa in range(10):
                        try:
                            if main_window.exists(timeout=2):
                                main_window.close()
                                await worker_sleep(2)
                                
                                if not main_window.exists(timeout=2):
                                    console.print("Tela de Movimento Apuração, fechada com sucesso... \n")
                                    break
                        except Exception as e:
                            console.print(f"Tentativa {tentativa + 1}: Erro ao tentar fechar a janela: {e}")
                            await worker_sleep(2)
                    else:
                        console.print("Não foi possível fechar a tela de Movimento Apuração após 10 tentativas.")

                except Exception as e:
                    console.print(f"Erro ao conectar com a janela TFrmMovtoApuraPisCofins: {e}")
                app = Application().connect(
                    class_name="TFrmMovtoApuraPisCofins", timeout=120
                )
                main_window = app["TFrmMovtoApuraPisCofins"]
                main_window.close()
                await worker_sleep(2)
                console.print("Tela de Movimento Apuração, fechada com sucesso... \n")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela Seleção de Empresas, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(10)
        # Verificar se já existe registro no mês apurado
        try:
            selecionar_todos_itens = (
                ASSETS_PATH + "\\lancamento_pis_cofins\\ja_existe_periodo.png"
            )
            # Tenta localizar a imagem na tela
            localizacao = pyautogui.locateOnScreen(
                selecionar_todos_itens, confidence=0.9
            )
            await worker_sleep(3)
            if localizacao:
                app = Application().connect(title="Informação", timeout=120)
                main_window = app["Informação"]
                main_window.set_focus()
                informacao = main_window.child_window(title="OK")
                informacao.click()
                console.print("Clique realizado com sucesso!")
            else:
                console.print("Imagem não encontrada na tela.")
        except:
            pass

        console.print(f"Abrindo a janela de Otimizador cálculo PIS/COFINS...")

        try:
            type_text_into_field(
                "Otimizador Cálculo PIS/COFINS",
                app["TFrmMenuPrincipal"]["Edit"],
                True,
                "50",
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            await worker_sleep(5)
            console.print(
                f"\nPesquisa: 'Otimizador Cálculo PIS/COFINS' realizada com sucesso",
                style="bold green",
            )
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao pesquisar pela janela de Otimizador cálculo PIS/COFINS",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print(
            f"Verificando se a janela de Otimizador Cálculo PIS/COFINS foi aberta com sucesso..."
        )
        otimizador_calculo_screen = await is_window_open_by_class(
            "TFrmOtimizadorCalcPisCofins", "TFrmOtimizadorCalcPisCofins"
        )
        if otimizador_calculo_screen["IsOpened"] == True:
            tipos = ["Livro Entrada", "Livro Saída"]
            for tipo in tipos:
                app = Application().connect(
                    class_name="TFrmOtimizadorCalcPisCofins", timeout=120
                )
                main_window = app["TFrmOtimizadorCalcPisCofins"]
                main_window.set_focus()

                console.print(f"Selecionando o tipo: {tipo}...")
                select_tipo_field = main_window.child_window(
                    class_name="TDBIComboBoxValues", found_index=0
                )
                select_tipo_field.select(tipo)
                await worker_sleep(2)

                console.print(f"Clicando em Lupa...")
                try:
                    lupa_pesquisar = pyautogui.locateOnScreen(
                        ASSETS_PATH + "\\lancamento_pis_cofins\\btn_lupa_pesquisar.png",
                        confidence=0.8,
                    )
                    pyautogui.click(lupa_pesquisar)
                    await worker_sleep(5)
                except Exception as e:
                    retorno = f"Não foi possivel clicar em selecionar todos os itens na Seleção de Empresas, erro: {e} "
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=retorno,
                        status=RpaHistoricoStatusEnum.Falha,
                        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                    )

                console.print(f"Verificando se a tela Buscar foi encontrada...")
                buscar_livro_screen = await is_window_open_by_class(
                    "TFrmBuscaGeralDialog", "TFrmBuscaGeralDialog"
                )
                if buscar_livro_screen["IsOpened"] == True:
                    console.print(
                        f"Tela de busca encontrada, selecionando o primeiro livro..."
                    )

                    pyautogui.click(734, 468)

                    await worker_sleep(3)

                    console.print(f"Clicando em ok...")
                    try:
                        btn_pesquisar = pyautogui.locateOnScreen(
                            ASSETS_PATH + "\\lancamento_pis_cofins\\btn_ok.png",
                            confidence=0.8,
                        )
                        pyautogui.click(btn_pesquisar)
                        console.print(f"Pesquisar clicado com sucesso...")
                        await worker_sleep(10)
                    except Exception as e:
                        retorno = f"Não foi possivel clicar em pesquisar na tela de Otimizador Cálculo PIS/COFINS, erro: {e} "
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                    console.print(f"Clicando no botão pesquisar")
                    try:
                        btn_pesquisar = pyautogui.locateOnScreen(
                            ASSETS_PATH + "\\lancamento_pis_cofins\\btn_pesquisar.png",
                            confidence=0.8,
                        )
                        pyautogui.click(btn_pesquisar)
                        console.print(f"Pesquisar clicado com sucesso...")
                        await worker_sleep(6)
                    except Exception as e:
                        retorno = f"Não foi possivel clicar em pesquisar na tela de Otimizador Cálculo PIS/COFINS, erro: {e} "
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                    console.print(f"Clicando em selecionar todos os itens...")
                    try:
                        btn_selecionar_todos_os_itens = pyautogui.locateOnScreen(
                            ASSETS_PATH
                            + "\\lancamento_pis_cofins\\btn_selecionar_todas.png",
                            confidence=0.8,
                        )
                        pyautogui.click(btn_selecionar_todos_os_itens)
                        console.print(
                            f"Selecionar todos os itens clicado com sucesso..."
                        )
                        await worker_sleep(5)
                    except Exception as e:
                        retorno = f"Não foi possivel clicar em selecionar todos os itens na tela de Otimizador Cálculo PIS/COFINS, erro: {e} "
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                    await worker_sleep(3)

                    print(f"Clicando em Atribuir Tributação do Item no Livro...")
                    try:
                        app = Application().connect(
                            class_name="TFrmOtimizadorCalcPisCofins", timeout=120
                        )
                        main_window = app["TFrmOtimizadorCalcPisCofins"]
                        main_window.set_focus()
                        btn_atribuir_tributacao = main_window.child_window(
                            title="Atribuir Tributação do Item no Livro"
                        )
                        btn_atribuir_tributacao.click()
                        await worker_sleep(3)
                    except Exception as e:
                        retorno = f"Não foi possivel clicar em Atribuir Tributação do Item no Livro tela de Otimizador Cálculo PIS/COFINS, erro: {e} "
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                    console.print(f"Aguardando processamento...")
                    while True:
                        aguarde_screen = await is_window_open_by_class(
                            "TFrmAguarde", "TFrmAguarde"
                        )
                        if aguarde_screen["IsOpened"] == True:
                            console.print(f"Em processamento...")
                            await worker_sleep(15)
                        else:
                            console.print(
                                f"Tela de aguarde não esta mais presente, saindo..."
                            )
                            break

                    await worker_sleep(6)
                    console.print(f"Gravando...")
                    try:
                        app = Application().connect(
                            class_name="TFrmOtimizadorCalcPisCofins", timeout=120
                        )
                        main_window = app["TFrmOtimizadorCalcPisCofins"]
                        main_window.set_focus()
                        btn_gravar = main_window.child_window(title="   Gravar")
                        btn_gravar.click()
                        await worker_sleep(5)
                        console.print(f"Verificando a presença de Confirm...")
                        confirm_pop_up = await is_window_open("Confirm")
                        if confirm_pop_up["IsOpened"] == True:
                            app = Application().connect(class_name="TMessageForm")
                            main_window = app["TMessageForm"]
                            main_window.set_focus()
                            main_window.child_window(title="&Yes").click()
                            await worker_sleep(3)
                    except Exception as e:
                        retorno = f"Não foi possivel Gravar na tela de Otimizador Cálculo PIS/COFINS, erro: {e} "
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=retorno,
                            status=RpaHistoricoStatusEnum.Falha,
                            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                        )

                    print(f"Aguardando processamento...")
                    while True:
                        aguarde_screen = await is_window_open_by_class(
                            "TFrmAguarde", "TFrmAguarde"
                        )
                        if aguarde_screen["IsOpened"] == True:
                            console.print(f"Em processamento...")
                            await worker_sleep(15)
                        else:
                            console.print(
                                f"Tela de aguarde não esta mais presente, saindo..."
                            )
                            break

                    await worker_sleep(6)
                    print(f"Verificando se possui tela de Informação...")

                    try:
                        btn_pesquisar = pyautogui.locateOnScreen(
                            ASSETS_PATH + "\\lancamento_pis_cofins\\btn_inf_ok.png",
                            confidence=0.8,
                        )
                        pyautogui.click(btn_pesquisar)
                        console.print(f"Pesquisar clicado com sucesso...")
                        await worker_sleep(6)
                    except:
                        pass

        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela de Otimizador Cálculo PIS/COFINS, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print(
            "Trabalho realizado na tela de Otimizador Cálculo PIS/COFINS, fechando a janela... \n"
        )
        app = Application().connect(
            class_name="TFrmOtimizadorCalcPisCofins", timeout=120
        )
        main_window = app["TFrmOtimizadorCalcPisCofins"]
        main_window.close()
        console.print(
            "Tela de Otimizador Cálculo PIS/COFINS, fechada com sucesso... \n"
        )

        type_text_into_field(
            "Livro de Apuração Pis Cofins", app["TFrmMenuPrincipal"]["Edit"], True, "50"
        )
        await worker_sleep(10)
        console.print(f"Verificando a presença de Confirm...")
        confirm_pop_up = await is_window_open("Confirm")
        if confirm_pop_up["IsOpened"] == True:
            app = Application().connect(class_name="TMessageForm")
            main_window = app["TMessageForm"]
            main_window.set_focus()
            main_window.child_window(title="&No").click()
        pyautogui.click(120, 173)
        pyautogui.press("enter")
        await worker_sleep(2)
        pyautogui.press("enter")
        console.print(
            f"\nPesquisa: 'Livro de Apuração PIS Cofins' realizada com sucesso",
            style="bold green",
        )

        console.print(
            "Verificando se a janela Movimento de Apuração PIS / COFINS foi aberta com sucesso...\n"
        )
        max_attempts = 15
        i = 0
        while i < max_attempts:
            movimento_apura_pis_cofins = await is_window_open_by_class(
                "TFrmMovtoApuraPisCofins", "TFrmMovtoApuraPisCofins"
            )
            if movimento_apura_pis_cofins["IsOpened"] == True:
                console.print(
                    "janela Movimento de Apuração PIS / COFINS foi aberta com sucesso...\n"
                )
                break
            else:
                await worker_sleep(1)
                i = i + 1

        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela Movimento de Apuração PIS / COFINS, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(5)

        console.print("Selecionando a primeira apuração...\n")
        try:
            app = Application().connect(
                class_name="TFrmMovtoApuraPisCofins", timeout=120
            )
            main_window = app["TFrmMovtoApuraPisCofins"]
            main_window.set_focus()

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
            for _ in range(20):
                pyautogui.press("up")
                await worker_sleep(1)

            await worker_sleep(3)
            console.print(f"Clicando Alterar Apuracao...")
            try:
                btn_alterar_apuracao = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\lancamento_pis_cofins\\btn_alterar_apuracao.png",
                    confidence=0.8,
                )
                pyautogui.click(btn_alterar_apuracao)
                await worker_sleep(3)
            except Exception as e:
                retorno = f"Não foi possivel clicar em Alterar Apuracao, erro: {e} "
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"Aguardando processamento...")
            while True:
                aguarde_screen = await is_window_open_by_class(
                    "TFrmAguarde", "TFrmAguarde"
                )
                if aguarde_screen["IsOpened"] == True:
                    console.print(f"Em processamento...")
                    await worker_sleep(15)
                else:
                    console.print(f"Tela de aguarde não esta mais presente, saindo...")
                    break
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao selecionar primeira apuração para gerar os creditos, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        await worker_sleep(3)
        console.print("Gerando Crédito...\n")
        try:
            app = Application().connect(
                class_name="TFrmMovtoApuraPisCofins", timeout=120
            )
            main_window = app["TFrmMovtoApuraPisCofins"]
            main_window.set_focus()
            await worker_sleep(5)

            console.print(f"Clicando Icon Crédito...")
            try:
                btn_credito_icon = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\lancamento_pis_cofins\\btn_icon_gerar_credito.png",
                    confidence=0.8,
                )
                pyautogui.click(btn_credito_icon)
                await worker_sleep(3)
            except Exception as e:
                retorno = f"Não foi possivel clicar no Icone Crédito, erro: {e} "
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            await worker_sleep(3)
            console.print(f"Clicando Gerar Registros Crédito...")
            try:
                btn_gerar_registro_credito = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\lancamento_pis_cofins\\btn_gerar_credito.png",
                    confidence=0.8,
                )
                pyautogui.click(btn_gerar_registro_credito)
                await worker_sleep(3)
            except Exception as e:
                retorno = f"Não foi possivel clicar no Icone Crédito, erro: {e} "
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"Aguardando processamento...")
            while True:
                aguarde_screen = await is_window_open_by_class(
                    "TFrmAguarde", "TFrmAguarde"
                )
                if aguarde_screen["IsOpened"] == True:
                    console.print(f"Em processamento...")
                    await worker_sleep(15)
                else:
                    console.print(f"Tela de aguarde não esta mais presente, saindo...")
                    break
        except Exception as e:
            retorno = f"Não foi possivel gerar registros crédito, erro: {e} "
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print("Gerando Débito...\n")
        try:
            app = Application().connect(
                class_name="TFrmMovtoApuraPisCofins", timeout=120
            )
            main_window = app["TFrmMovtoApuraPisCofins"]
            main_window.set_focus()
            await worker_sleep(5)

            console.print(f"Clicando Icon Débito...")
            try:
                btn_debito_icon = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\lancamento_pis_cofins\\btn_icon_gerar_debito.png",
                    confidence=0.8,
                )
                pyautogui.click(btn_debito_icon)
                await worker_sleep(3)
            except Exception as e:
                retorno = f"Não foi possivel clicar no Icone Débito, erro: {e} "
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"Clicando Gerar Registros Débito...")
            try:
                btn_gerar_registro_debito = pyautogui.locateOnScreen(
                    ASSETS_PATH + "\\lancamento_pis_cofins\\btn_gerar_debito.png",
                    confidence=0.8,
                )
                pyautogui.click(btn_gerar_registro_debito)
                await worker_sleep(3)
            except Exception as e:
                retorno = f"Não foi possivel clicar no Icone Crédito, erro: {e} "
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                    tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
                )

            console.print(f"Aguardando processamento...")
            while True:
                aguarde_screen = await is_window_open_by_class(
                    "TFrmAguarde", "TFrmAguarde"
                )
                if aguarde_screen["IsOpened"] == True:
                    console.print(f"Em processamento...")
                    await worker_sleep(15)
                else:
                    console.print(f"Tela de aguarde não esta mais presente, saindo...")
                    break
        except Exception as e:
            retorno = f"Não foi possivel gerar registros débito, erro: {e} "
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        console.print(
            "\nLançamento PIS/COFINS realizado com sucesso, processo finalizado...",
            style="bold green",
        )
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Processo executado com sucesso!",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as ex:
        observacao = f"Erro ao executar lançamento PIS/Cofins: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )

    
