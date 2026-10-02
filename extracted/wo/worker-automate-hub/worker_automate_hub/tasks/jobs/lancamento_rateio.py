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
from datetime import datetime

ASSETS_BASE_PATH = "assets/cte_xml/"
emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

data_hoje = datetime.now().strftime("%d%m%Y")
print(data_hoje)

async def janela_nota_fiscal(nota_entrada):
    # Declaração das variáveis
    data_emissao = nota_entrada["dataEmissao"]
    nota_fiscal = nota_entrada["numeroNota"]
    cnpj_fornecedor = nota_entrada["cnpjFornecedor"]
    try:
        await worker_sleep(5)
        app = Application(backend="win32").connect(
            title="Nota Fiscal de Entrada", found_index=0
        )
        main_window = app["Nota Fiscal de Entrada"]

        input_tipo_documento = main_window.child_window(class_name="TDBIComboBox", found_index=1)
    

        # Focar e clicar no ComboBox
        input_tipo_documento.set_focus()
        input_tipo_documento.click_input()
        
        await worker_sleep(1)

        # Selecionar Nota Fiscal de Entrada
        input_tipo_documento.select("NOTA FISCAL DE ENTRADA - SERVIÇO")
        
        await worker_sleep(3)
        
        # Enviar ENTER para confirmar
        send_keys("{ENTER}")
            
        await worker_sleep(2)
        
        # Inserir Entrada data_hoje
        input_entrada = main_window.child_window(class_name="TDBIEditDate", found_index=1)
        type_text_into_field(data_hoje, input_entrada, True, "10")
        
        # Inserir Data de Emissão
        input_emissao = main_window.child_window(class_name="TDBIEditDate", found_index=2)
        type_text_into_field(data_emissao, input_emissao, True, "10")
        
        # Inserir Nota Fiscal
        input_nota_fiscal = main_window.child_window(class_name="TDBIEditString", found_index=8)
        type_text_into_field(nota_fiscal, input_nota_fiscal, True, "50")
        
        # Inserir Serie
        input_serie = main_window.child_window(class_name="TDBIEditString", found_index=2)
        type_text_into_field("S", input_serie, True, "10")
        
        # Inserir CNPJ
        input_cnpj = main_window.child_window(class_name="TDBIEditString", found_index=4)
        type_text_into_field(cnpj_fornecedor, input_cnpj, True, "14")
    
        # Clicar na lupa
        pyautogui.click(x=980, y=504)
        
        # Inserir NOP Nota
        select_nop_nota = main_window.child_window(class_name="TDBIComboBox", found_index=0)
        
        # Focar e clicar no ComboBox
        select_nop_nota.set_focus()
        select_nop_nota.click_input()
        
        await worker_sleep(1)

        # Selecionar Opção
        select_nop_nota.select("1933 - AQUISIÇÃO DE SERVIÇOS - 1933")
        
        # Enviar ENTER para confirmar
        send_keys("{ENTER}")
        
        await worker_sleep(1)
        
        # Inserir Mod Frete
        select_mod_frete = main_window.child_window(class_name="TDBIComboBoxValues", found_index=1)
        
        # Focar e clicar no ComboBox
        select_mod_frete.set_focus()
        select_mod_frete.click_input()
        
        await worker_sleep(1)

        # Selecionar Opção
        select_mod_frete.select("9=Sem Ocorrência de Transporte.")
        
        # Enviar ENTER para confirmar
        send_keys("{ENTER}")   
         
        await worker_sleep(1)
        
        # Clicar no Itens da Nota
        pyautogui.click(x=628, y=328)
        
        await worker_sleep(3)
        
        # Clicar no sinal de +
        sinal_mais = main_window.child_window(class_name="TDBIBitBtn", found_index=3)
        
        # Focar e clicar no ComboBox
        sinal_mais.set_focus()
        sinal_mais.click_input()
    
        await worker_sleep(5)
            

    except Exception as e:
        # console.print(f"Erro ao conectar a janela {window_title}")
        raise Exception(f"Erro ao conectar a janela: {e}")

async def janela_inclusao_itens(nota_entrada):
    # Declaracao de variáveis
    codigo_empresa = nota_entrada["codigoEmpresa"]
    valor_nota = nota_entrada["valorNota"]
    conta_contabil = nota_entrada["contaContabil"]
    quantidade = nota_entrada["quantidade"]
    
    app = Application(backend="win32").connect(
        class_name="TFrmIncluiItemNFE", found_index=0
    )
    main_window = app["TFrmIncluiItemNFE"]

    # Inserir input_Almoxarifado
    input_almoxarifado = main_window.child_window(class_name="TDBIEditCode", found_index=2)
      
     # Focar e clicar no ComboBox
    input_almoxarifado.set_focus()
    
    
    if codigo_empresa != '1':
        codigo_empresa = f"{codigo_empresa}50"
    else:
        codigo_empresa = f"{codigo_empresa}60"
    
    type_text_into_field(codigo_empresa, input_almoxarifado, True, "10")
    
    send_keys("{ENTER}")
    
    await worker_sleep(3)
    
    # Inserir Item 
    input_item = main_window.child_window(class_name="TDBIEditNumber", found_index=40)
    type_text_into_field("2483", input_item, True, "10")
    send_keys("{TAB}")
    
    await worker_sleep(5)
    try:
        # Mudar para janela pesquisa itens
        app = Application(backend="win32").connect(
            class_name="TFrmPesquisaItem", found_index=0
        )
        main_window = app["TFrmPesquisaItem"]

        # Clicar Primeira LInha
        pyautogui.click(x=561, y=397)
        
        # Clicar em confirmar
        clicar_confirmar = main_window.child_window(class_name="TDBIBitBtn", found_index=2)
        clicar_confirmar.click_input()
    except:
        pass
    
    await worker_sleep(5)
    
    # Volta para janela de inclusão de itens
    app = Application(backend="win32").connect(
        class_name="TFrmIncluiItemNFE", found_index=0
    )
    main_window = app["TFrmIncluiItemNFE"]
    
    # Inserir quantidade
    input_quantidade = main_window.child_window(class_name="TDBIEditNumber", found_index=39)
    type_text_into_field(quantidade, input_quantidade, True, "10")
    
    # Inserir Valor Unitário
    input_valor_unitario = main_window.child_window(class_name="TDBIEditNumber", found_index=9)
      
     # Focar e clicar no ComboBox
    input_valor_unitario.set_focus()
    
    
    type_text_into_field(valor_nota, input_valor_unitario, True, "10")
    
    await worker_sleep(5)
    
    # Clicar em Tipo de Despesa
    pyautogui.click(x=793, y=485)
    
    await worker_sleep(2)
    
     # Inserir Tipo [Conta COntábil]
    input_tipo = main_window.child_window(class_name="TDBIEditCode", found_index=1)
      
     # Focar e clicar no ComboBox
    input_tipo.set_focus()
    
    
    type_text_into_field(conta_contabil, input_tipo, True, "10")
    
    # Clicar em Incluir 
    incluir = main_window.child_window(class_name="TDBIBitBtn", found_index=1)
    incluir.click_input()
    
    await worker_sleep(5)
    
    # Clicar em cancelar
    cancelar = main_window.child_window(class_name="TDBIBitBtn", found_index=2)
    cancelar.click_input()

async def janela_pagamento(nota_entrada):
    # Declarar variáveis
    data_vencimento = datetime.now() + timedelta(days=1)
    data_vencimento_formatada = data_vencimento.strftime('%d%m%Y')
    valor_nota = nota_entrada["valorNota"]
    # Clicar em pagamento
    pyautogui.click(x=623, y=360)
    
    await worker_sleep(2)
    
    app = Application(backend="win32").connect(
        class_name="TFrmNotaFiscalEntrada", found_index=0
    )
    main_window = app["TFrmNotaFiscalEntrada"]
    
    # Selecionar tipo de cobrança
    select_tipo_cobranca = main_window.child_window(class_name="TDBIComboBox", found_index=0)
    select_tipo_cobranca.select("BANCO DO BRASIL BOLETO")
    
    await worker_sleep(1)
    
    # Inserir data vencimento
    input_data_vencimento = main_window.child_window(class_name="TDBIEditDate", found_index=0)
    type_text_into_field(data_vencimento_formatada, input_data_vencimento, True, "10")
    
    await worker_sleep(1)
    
    # Inserir valor da nota
    input_valor_nota = main_window.child_window(class_name="TDBIEditNumber", found_index=3)
    type_text_into_field(valor_nota, input_valor_nota, True, "10")
    
    await worker_sleep(1)
    
    # Clicar no botão +
    clicar_mais = main_window.child_window(class_name="TDBIBitBtn", found_index=1)
    clicar_mais.click_input()
    
    await worker_sleep(2)
    
    # Clicar no + para salvar
    pyautogui.click(x=594, y=281)
    
    await worker_sleep(3)
    
    # Clicar em selecionar todos
    pyautogui.click(x=746, y=478)


async def janela_rateio_despesa(nota_entrada):
    await worker_sleep(5)
    # Declarar variável
    app = Application(backend="win32").connect(
        class_name="TFrmDadosRateioDespesa", found_index=0
    )
    main_window = app["TFrmDadosRateioDespesa"]   

    for rateio in nota_entrada["rateios"]:
        centro_custo = rateio["centroCusto"]
        valor = rateio["valor"]
        print(f"Centro de Custo: {centro_custo} | Valor: {valor}") 
        
        # Inserir centro de custo
        input_centro_custo = main_window.child_window(class_name="TDBIEditCode", found_index=0)
        type_text_into_field(centro_custo, input_centro_custo, True, "10")
        send_keys("{TAB}")
        
        await worker_sleep(1)
       
        # Inserir valor
        input_valor = main_window.child_window(class_name="TDBIEditNumber", found_index=5)
        type_text_into_field(valor, input_valor, False, "10")
        
        await worker_sleep(1)
        
        # Clicar em incluir rateio
        clicar_incluir_rateio = main_window.child_window(class_name="TDBIBitBtn", found_index=3)
        clicar_incluir_rateio.click()
        
        await worker_sleep(2)

async def lancamento_rateio(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        config = await get_config_by_name("login_emsys")
        nota_entrada = task.configEntrada

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

        await janela_nota_fiscal(nota_entrada)
        
        await janela_inclusao_itens(nota_entrada)
        
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=f"Suceso no processo Lançamento de Rateio",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as e:
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro no processo CTE com XML: {e}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
    
        

if __name__ == "__main__":
    task = RpaProcessoEntradaDTO(
        datEntradaFila=datetime.now(),
        configEntrada={
            "rateios": [
                {"valor": "3040,10", "centroCusto": "1133"},
                {"valor": "999,50", "centroCusto": "1155"},
                {"valor": "1516,53", "centroCusto": "1210"},
                {"valor": "4162,28", "centroCusto": "1154"},
                {"valor": "4145,93", "centroCusto": "1146"},
                {"valor": "3553,20", "centroCusto": "1136"},
                {"valor": "205,58", "centroCusto": "1071"},
                {"valor": "2270,66", "centroCusto": "1156"},
                {"valor": "2346,79", "centroCusto": "1088"},
                {"valor": "13720,75", "centroCusto": "1223"},
                {"valor": "6747,75", "centroCusto": "1035"},
                {"valor": "2886,55", "centroCusto": "1129"},
                {"valor": "3011,67", "centroCusto": "1130"},
                {"valor": "2103,99", "centroCusto": "1054"},
                {"valor": "2544,05", "centroCusto": "1077"},
                {"valor": "3308,69", "centroCusto": "1091"},
                {"valor": "3104,85", "centroCusto": "1093"},
                {"valor": "1507,34", "centroCusto": "1092"},
                {"valor": "4143,30", "centroCusto": "1103"},
                {"valor": "4774,93", "centroCusto": "1060"},
                {"valor": "1743,58", "centroCusto": "9999"},
                {"valor": "3783,73", "centroCusto": "1053"},
                {"valor": "3141,57", "centroCusto": "1041"},
                {"valor": "2586,06", "centroCusto": "1099"},
                {"valor": "2286,40", "centroCusto": "1166"},
                {"valor": "2848,49", "centroCusto": "1119"},
                {"valor": "3428,97", "centroCusto": "1078"},
                {"valor": "1672,26", "centroCusto": "1139"},
                {"valor": "1872,63", "centroCusto": "1124"},
                {"valor": "2060,27", "centroCusto": "1039"},
                {"valor": "5148,94", "centroCusto": "1062"},
                {"valor": "3182,39", "centroCusto": "1211"}
            ],
            "valorNota": "10849,75",
            "identificador": "aquiSeuIdentificador",
            "numeroNota": "127",
            "urlRetorno": "https://suaempresa.com.br/retorno-nota",
            "codigoEmpresa": "1",
            "nomeEmpresa": "MATRIZ",
            "contaContabil": "13",
            "cnpjFornecedor": "31492377000139",
            "dataEmissao": "23/05/2025",
            "quantidade": "1"
        },  # vírgula aqui é essencial
        uuidProcesso='b47f25e8-0b41-429d-904b-7db7a03219cc',
        nomProcesso='lancamento_rateio',
        uuidFila="",
        sistemas=[
            {"sistema": "EMSys", "timeout": "1.0"},
            {"sistema": "AutoSystem", "timeout": "1.0"}
        ],
        historico_id='01'
    )

    asyncio.run(lancamento_rateio(task))
