# -*- coding: utf-8 -*-
import asyncio
import warnings
from datetime import datetime, date
import json
import io
import pyautogui
from pywinauto.application import Application, timings
from pywinauto import keyboard
from pywinauto import Desktop
from collections import defaultdict
from rich.console import Console
import getpass
import time
import re
import sys
import os
import shutil
import win32wnet  # pywin32

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from worker_automate_hub.api.client import (
    get_config_by_name,
    send_file,
    get_notas_produtos,
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
from pywinauto.keyboard import send_keys

from worker_automate_hub.utils.util import (
    kill_all_emsys,
    login_emsys,
    type_text_into_field,
    worker_sleep,
)

console = Console()
log = console.log

ASSETS_BASE_PATH = fr"assets\importacao_extratos"
# ASSETS_BASE_PATH = r"C:\Users\automatehub\Desktop\img_leo"
ano_atual = date.today().year

# === DESTINOS ===
DESTINO_BASE = fr"Z:\Nexera\Extrato\{ano_atual}"  # tentativa principal (Z:)
DESTINO_IP_ROOT = r"\\fcaswfs01.ditrento.com.br\compartilhadas$"  # root do share
DESTINO_BASE_IP = fr"{DESTINO_IP_ROOT}\Nexera\\{ano_atual}"       # pasta final no UNC

EMPRESA = "1"  # empresa fixa


async def importacao_extratos_748(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # ======== PARÂMETROS ========
        PASTA = r"Z:\Nexera\Extrato"
        CONTEM = ["EXT_748_"]          # padrões obrigatórios no nome do arquivo
        EXT_PERMITIDAS = [".ret", ".txt"]  # extensões permitidas (case-insensitive)
        TEXTO_ALVO = "SIM REDE DE POSTOS"  # texto a procurar no conteúdo
        BTN_IMPORTAR_IMG = fr"{ASSETS_BASE_PATH}\btn_imp_arq.png"
        BTN_CONCILIAR = fr"{ASSETS_BASE_PATH}\btn_conciliar.png"
        DLG_TIT_RE = ".*Browse.*"  # regex de título do diálogo de arquivo

        IMAGEM_SUCESSO = fr"{ASSETS_BASE_PATH}\conciliados_sucesso.png"

        EXT_STR = "/".join(EXT_PERMITIDAS).upper()

        # Credenciais para fallback de rede
        user_folder_login = await get_config_by_name("user_credentials")
        user_folder_cfg = user_folder_login.conConfiguracao or {}

        log("[cyan]Iniciando importacao_extratos[/] | empresa fixa = %s", EMPRESA)
        log(
            "Parâmetros -> pasta: %s | contem (obrigatório): %s | extensões: %s | texto alvo: %s",
            PASTA,
            CONTEM,
            EXT_STR,
            TEXTO_ALVO,
        )

        # ======== ACUMULADORES ========
        selecionados = []
        avaliados = 0
        ignorados_nome = 0
        nao_permitido = 0
        lidos = 0
        erros = 0

        if not os.path.isdir(PASTA):
            msg = f"Pasta não encontrada: {PASTA}"
            log(f"[red]{msg}[/]")
            raise SystemExit(msg)

        log("Varredura em: %s", PASTA)

        # ======== SCAN DE ARQUIVOS ========
        for entry in os.scandir(PASTA):
            if not entry.is_file():
                continue

            nome = entry.name
            caminho = entry.path
            upper_name = nome.upper()
            lower_name = nome.lower()

            # Seleciona somente arquivos que contenham os padrões em CONTEM
            if not any(p.upper() in upper_name for p in CONTEM):
                ignorados_nome += 1
                log("Ignorado (não contém padrões obrigatórios): %s", nome)
                continue

            # Considera apenas arquivos com extensões permitidas
            if not any(lower_name.endswith(ext.lower()) for ext in EXT_PERMITIDAS):
                nao_permitido += 1
                continue

            avaliados += 1

            # Procura o texto alvo dentro do arquivo (case-insensitive)
            alvo_norm = TEXTO_ALVO.casefold()
            encontrado = False

            try:
                with open(caminho, "r", encoding="latin1", errors="ignore") as f:
                    for linha in f:
                        if alvo_norm in linha.casefold():
                            encontrado = True
                            break
                lidos += 1
            except Exception as e:
                erros += 1
                log("[red]Erro lendo '%s': %s[/red]", nome, e)
                continue

            # Se encontrou o texto alvo, adiciona à lista de selecionados
            if encontrado:
                selecionados.append(
                    {
                        "arquivo": nome,
                        "caminho": caminho,
                        "tamanho_bytes": os.path.getsize(caminho),
                    }
                )
                log("[green]Selecionado[/green]: %s", caminho)

        # ======== SAÍDA NO CONSOLE ========
        log("======== RESULTADO DA VARREDURA ========")
        log(
            "Avaliados (ext permitidas): %s | Ignorados por nome: %s | Ignorados por extensão: %s | Lidos: %s | Erros leitura: %s",
            avaliados,
            ignorados_nome,
            nao_permitido,
            lidos,
            erros,
        )

        # ======== VERIFICA RESULTADO ========
        if not selecionados:
            if ignorados_nome > 0:
                msg = (
                    "Arquivos foram ignorados por nome conforme os padrões definidos: "
                    + ", ".join(CONTEM)
                )
            else:
                msg = (
                    f"Nenhum arquivo {EXT_STR} contendo '{TEXTO_ALVO}' encontrado."
                )
            log(f"[yellow]{msg}[/yellow]")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Sucesso,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        # ======== EMSys: LOGIN ========
        log("Carregando credenciais com get_config_by_name('login_emsys')...")
        config = await get_config_by_name("login_emsys")
        log(
            "[green]Credenciais carregadas[/green]. Tarefa recebida | empresa fixa = %s",
            EMPRESA,
        )

        log("Verificando instâncias abertas do EMSys (kill_all_emsys)...")
        await kill_all_emsys()
        log("Iniciando EMSys...")
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_22.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        log("[green]EMSys iniciando[/green]...")

        log("Realizando login no EMSys...")
        return_login = await login_emsys(
            config.conConfiguracao, app, task, filial_origem=EMPRESA
        )
        if not return_login.sucesso:
            logger.info(f"\nError Message: {return_login.retorno}")
            log(f"[red]Erro no login[/red]: {return_login.retorno}")
            return return_login
        log("[green]Login realizado com sucesso[/green].")

        # ======== ABRE MÓDULO CONCILIADOR ========
        log("Abrindo módulo: 'Conciliador Bancario 2.0'")
        try:
            type_text_into_field(
                "Conciliador Bancario 2.0",
                app["TFrmMenuPrincipal"]["Edit"],
                True,
                "50",
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("down", presses=2, interval=0.2)
            await worker_sleep(0.5)
            pyautogui.press("enter")
            log("[green]Módulo acionado[/green]. Aguardando carregamento...")
            await worker_sleep(3)
        except Exception as e:
            log("[red]Falha ao abrir o módulo[/red]: %s", e)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao abrir módulo Conciliador Bancario 2.0: {e}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # ==== IMPORTAÇÃO: para cada arquivo selecionado ====
        importados = []
        movidos = []
        falhas = []

        for idx, sel in enumerate(selecionados, 1):
            log(
                "[bold cyan]Iniciando importação (%s/%s)[/bold cyan]: %s",
                idx,
                len(selecionados),
                sel["arquivo"],
            )

            # Flag para controlar se chegamos na parte do conciliar com sucesso
            conciliacao_ok = False

            # 1) Clicar no botão "Importar Arquivo"
            log("Procurando botão 'Importar Arquivo' pela imagem: %s", BTN_IMPORTAR_IMG)
            for t in range(20):
                pos = pyautogui.locateCenterOnScreen(
                    BTN_IMPORTAR_IMG, confidence=0.9
                )
                if pos:
                    pyautogui.click(pos)
                    log("[green]Botão encontrado e clicado[/green].")
                    break
                await worker_sleep(0.5)
            else:
                msg = "Imagem do botão 'Importar Arquivo' não encontrada na tela."
                log(f"[red]{msg}[/red]")
                falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                continue

            await worker_sleep(2)

            # 2) Conectar na janela de importação
            try:
                log(
                    "Conectando na janela 'TFrmImportarArquivoConciliadorBancario2' ..."
                )
                app_imp = Application(backend="win32").connect(
                    class_name="TFrmImportarArquivoConciliadorBancario2", timeout=1200
                )
                main_window = app_imp["TFrmImportarArquivoConciliadorBancario2"]
                main_window.set_focus()
                main_window.child_window(
                    class_name="TWinControl", found_index=0
                ).click_input()
                log("[green]Janela de importação focada[/green].")
                await worker_sleep(3)
            except Exception:
                log(
                    "[yellow]Janela 'TFrmImportarArquivoConciliadorBancario2' não encontrada. Tentando seguir...[/yellow]"
                )

            # 3) Selecionar tipo de arquivo
            log("Selecionando tipo de arquivo: digitando 'A' e [TAB]...")
            try:
                pyautogui.click(982, 632)
                await worker_sleep(3)
                pyautogui.write("A")
                pyautogui.press("tab")
                await worker_sleep(0.3)
                log("[green]Tipo selecionado[/green].")
            except Exception as e:
                log(
                    "[yellow]Não foi possível interagir com o tipo de arquivo: %s[/yellow]",
                    e,
                )

            # 4) Capturar janela de diálogo de arquivo
            log("Aguardando diálogo de arquivo (%s)...", DLG_TIT_RE)
            dlg = None
            for _ in range(30):
                try:
                    app_dlg = Application().connect(title_re=DLG_TIT_RE)
                    dlg = app_dlg.window(title_re=DLG_TIT_RE)
                    if dlg.exists() and dlg.is_enabled():
                        break
                except Exception:
                    pass
                await worker_sleep(0.5)

            if dlg is None or not dlg.exists():
                msg = "Diálogo de arquivo (#32770) não apareceu."
                log(f"[red]{msg}[/red]")
                falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                continue

            log("[green]Diálogo de arquivo detectado[/green]. Preenchendo caminho...")
            dlg.set_focus()
            await worker_sleep(0.2)

            # Campo Nome:Edit
            try:
                nome_edit = dlg.child_window(best_match="&Nome:Edit")
            except Exception:
                try:
                    nome_edit = dlg.child_window(class_name="Edit", found_index=0)
                except Exception:
                    msg = "Campo de nome (Edit) não localizado no diálogo."
                    log(f"[red]{msg}[/red]")
                    falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                    continue

            try:
                nome_edit.click_input()
                await worker_sleep(0.2)
                send_keys("^a{BACKSPACE}")
                send_keys(sel["caminho"])
                await worker_sleep(0.2)
                send_keys("{ENTER}")
                log("Arquivo confirmado no diálogo: %s", sel["caminho"])

                await worker_sleep(2)
                pyautogui.click(1203, 509)

                await worker_sleep(10)

                # Aumenta a tolerância global
                timings.after_clickinput_wait = 1

                # 1) Aguarda a janela de mensagem (TMessageForm) após importação
                try:
                    console.print(
                        "[yellow]Aguardando a janela de mensagem (TMessageForm) da importação...[/yellow]"
                    )

                    msg_form = Desktop(backend="win32").window(class_name="TMessageForm")
                    msg_form.wait("exists visible ready", timeout=300)

                    console.print(
                        "[green]✅ Janela TMessageForm de importação apareceu.[/green]"
                    )

                    try:
                        btn_ok = msg_form.child_window(title_re="OK|Ok|ok")
                        if btn_ok.exists():
                            btn_ok.click()
                        else:
                            msg_form.type_keys("{ENTER}")
                    except Exception:
                        pass

                except Exception as e:
                    console.print(
                        f"[red]❌ Erro ao aguardar TMessageForm da importação: {e}[/red]"
                    )
                    falhas.append(
                        {
                            "arquivo": sel["arquivo"],
                            "motivo": f"Erro ao aguardar TMessageForm da importação: {e}",
                        }
                    )
                    continue

                # 2) Agora conecta na janela do Conciliador
                try:
                    console.print(
                        "[yellow]Conectando na janela do Conciliador Bancário...[/yellow]"
                    )

                    app_conc = Application(backend="win32").connect(
                        class_name="TFrmConciliadorBancario2",
                        timeout=60,
                    )

                    wnd = app_conc.window(class_name="TFrmConciliadorBancario2")
                    wnd.wait("visible enabled ready", timeout=60)

                    console.print(
                        "[green]✅ Janela do Conciliador carregada com sucesso![/green]"
                    )

                except Exception as e:
                    console.print(
                        f"[red]❌ Erro ao conectar na janela do Conciliador: {e}[/red]"
                    )
                    falhas.append(
                        {
                            "arquivo": sel["arquivo"],
                            "motivo": f"Erro ao conectar na janela do Conciliador: {e}",
                        }
                    )
                    continue

                # Agora sim, busca os campos numéricos
                campos = wnd.descendants(class_name="TDBIEditNumber")

                # 3) Valida quantidade de campos
                if len(campos) < 5:
                    console.print(
                        "[red]Não existem campos suficientes (precisa de pelo menos 5).[/red]"
                    )
                    falhas.append(
                        {
                            "arquivo": sel["arquivo"],
                            "motivo": "Campos numéricos insuficientes no Conciliador.",
                        }
                    )
                    continue
                else:
                    # ===== ESPERA CAMPOS ≠ 0,00 =====
                    TIMEOUT_CAMPOS = 30 * 60  # 30 minutos
                    inicio_espera = time.time()
                    valores_preenchidos = False

                    console.print(
                        "[cyan]Aguardando até que os campos 0 e 4 deixem de ser '0,00' ou vazios (timeout 30 min)...[/cyan]"
                    )

                    while True:
                        valor_0 = campos[0].window_text().strip()
                        valor_4 = campos[4].window_text().strip()

                        console.print(
                            f"[cyan]Leitura atual -> índice 0: '{valor_0}' | índice 4: '{valor_4}'[/cyan]"
                        )

                        cond_0 = valor_0 not in ("", "0,00", "0.00")
                        cond_4 = valor_4 not in ("", "0,00", "0.00")

                        if cond_0 and cond_4:
                            valores_preenchidos = True
                            console.print(
                                "[green]Campos preenchidos com valores diferentes de 0,00. Prosseguindo para comparação...[/green]"
                            )
                            break

                        if time.time() - inicio_espera > TIMEOUT_CAMPOS:
                            console.print(
                                "[red]Timeout de 30 minutos aguardando os campos saírem de 0,00.[/red]"
                            )
                            falhas.append(
                                {
                                    "arquivo": sel["arquivo"],
                                    "motivo": "Timeout aguardando campos numéricos saírem de 0,00.",
                                }
                            )
                            valores_preenchidos = False
                            break

                        await worker_sleep(5)

                    if not valores_preenchidos:
                        continue

                    console.print(f"[cyan]Valor índice 0 final:[/] {valor_0}")
                    console.print(f"[cyan]Valor índice 4 final:[/] {valor_4}")

                    if not (valor_0 == valor_4 and valor_0 not in ("", "0,00", "0.00")):
                        console.print(
                            "[yellow]Valores diferentes. Não será conciliado.[/yellow]"
                        )
                        falhas.append(
                            {
                                "arquivo": sel["arquivo"],
                                "motivo": f"Valores diferentes no Conciliador (0={valor_0}, 4={valor_4}).",
                            }
                        )
                        continue

                    console.print(
                        "[green]Valores iguais e válidos! Tentando clicar no botão 'Conciliar'...[/green]"
                    )
                    pos_conc = pyautogui.locateCenterOnScreen(
                        BTN_CONCILIAR, confidence=0.9
                    )
                    if not pos_conc:
                        console.print(
                            "[red]Botão 'Conciliar' não encontrado na tela.[/red]"
                        )
                        falhas.append(
                            {
                                "arquivo": sel["arquivo"],
                                "motivo": "Botão 'Conciliar' não localizado na tela.",
                            }
                        )
                        continue

                    pyautogui.click(pos_conc)
                    console.print(
                        "[green]Botão 'Conciliar' clicado com sucesso![/green]"
                    )

                    # ===== Aguardar imagem de sucesso + janela de confirmação =====
                    timeout = 1800  # 30 min
                    inicio = time.time()

                    console.print(
                        "[cyan]Aguardando imagem de sucesso aparecer e janela de confirmação da conciliação...[/cyan]"
                    )

                    pos_sucesso = None
                    janela_ok_encontrada = False

                    while time.time() - inicio < timeout:
                        # 1) Verifica imagem
                        pos_sucesso = pyautogui.locateCenterOnScreen(
                            IMAGEM_SUCESSO, confidence=0.85
                        )

                        if pos_sucesso:
                            console.print(
                                "[green]Imagem 'conciliados_sucesso' encontrada na tela.[/green]"
                            )

                            # 2) Agora aguarda a TMessageForm / Information
                            try:
                                console.print(
                                    "[yellow]Aguardando janela 'Movimentos selecionados conciliados com sucesso!'...[/yellow]"
                                )
                                msg_ok = Desktop(backend="win32").window(
                                    class_name="TMessageForm"
                                )
                                msg_ok.wait("exists visible ready", timeout=60)

                                console.print(
                                    "[green]✅ Janela de confirmação da conciliação encontrada.[/green]"
                                )

                                try:
                                    btn_ok = msg_ok.child_window(title_re="OK|Ok|ok")
                                    if btn_ok.exists():
                                        btn_ok.click()
                                    else:
                                        msg_ok.type_keys("{ENTER}")
                                except Exception:
                                    # se der algo errado no botão, pelo menos a janela existe
                                    msg_ok.type_keys("{ENTER}")

                                janela_ok_encontrada = True
                            except Exception as e:
                                console.print(
                                    f"[red]❌ Não foi possível encontrar/confirmar a janela de conciliação: {e}[/red]"
                                )
                                janela_ok_encontrada = False

                            # Sai do while (já encontrou imagem, independente da janela ter dado certo ou não)
                            break

                        await worker_sleep(1)

                    # Se a imagem nunca apareceu, falha
                    if not pos_sucesso:
                        console.print(
                            "[red]Imagem 'conciliados_sucesso.png' NÃO apareceu dentro do tempo limite.[/red]"
                        )
                        falhas.append(
                            {
                                "arquivo": sel["arquivo"],
                                "motivo": "Imagem de sucesso da conciliação não apareceu.",
                            }
                        )
                        continue

                    # Se a janela não foi confirmada, considerar falha também
                    if not janela_ok_encontrada:
                        msg = "Janela de confirmação da conciliação não foi encontrada/confirmada."
                        console.print(f"[red]{msg}[/red]")
                        falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                        continue

                    # Só aqui marca como conciliado com sucesso
                    conciliacao_ok = True

                # tenta fechar janela de erro, se existir
                try:
                    app_err = Application(backend="win32").connect(
                        title="Erro", found_index=0
                    )
                    main_err = app_err["Erro"]
                    log("[yellow]Janela 'Erro' detectada. Fechando...[/yellow]")
                    main_err.close()
                    await worker_sleep(1)
                except Exception:
                    pass

                # ============ CHECAGEM: SÓ MOVE SE CONCILIAR OK ============
                if not conciliacao_ok:
                    msg = (
                        "Conciliador não foi executado/confirmado com sucesso para o arquivo."
                    )
                    log(f"[red]{msg}[/red]")
                    falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                    continue

                # ============ MOVER ARQUIVO ============
                origem = sel["caminho"]
                arquivo = sel["arquivo"]

                try:
                    # 1) Tenta mover para o destino padrão (DESTINO_BASE - Z:)
                    os.makedirs(DESTINO_BASE, exist_ok=True)
                    destino_arquivo = os.path.join(DESTINO_BASE, arquivo)

                    # Sobrescrita segura se já existir
                    if os.path.exists(destino_arquivo):
                        try:
                            os.remove(destino_arquivo)
                        except Exception as e_rm:
                            log(
                                "[yellow]Aviso[/yellow]: não foi possível remover no destino: %s (%s)",
                                destino_arquivo,
                                e_rm,
                            )

                    shutil.move(origem, destino_arquivo)

                    # >>> registrar também quando move pelo Z: <<<
                    movidos.append(destino_arquivo)
                    importados.append(arquivo)

                    # LOG DE VALIDAÇÃO
                    exist_dest = os.path.exists(destino_arquivo)
                    try:
                        lista = os.listdir(os.path.dirname(destino_arquivo))
                    except Exception as e:
                        lista = [f"<<erro ao listar pasta: {e}>>"]

                    log(
                        "[green]Arquivo movido[/green]: %s -> %s (existe_destino=%s)",
                        origem,
                        destino_arquivo,
                        exist_dest,
                    )
                    log("Conteúdo da pasta destino após o move: %s", lista)

                except Exception as e1:
                    # 2) Fallback via UNC (compartilhadas$ -> Nexera\{ano})
                    try:
                        usuario = user_folder_cfg.get("usuario")
                        senha = user_folder_cfg.get("senha")

                        if win32wnet is None:
                            raise RuntimeError(
                                "pywin32 não disponível para mapear caminho de rede (win32wnet)."
                            )

                        log(
                            "Falha ao mover para Z:. Tentando fallback via UNC em %s ...",
                            DESTINO_IP_ROOT,
                        )

                        try:
                            win32wnet.WNetAddConnection2(
                                0,
                                None,
                                DESTINO_IP_ROOT,
                                None,
                                usuario,
                                senha,
                            )
                        except Exception as e_conn:
                            # Se der 1219 (conexão já existente), ignoramos
                            if getattr(e_conn, "winerror", None) != 1219:
                                raise

                        caminho_ip = DESTINO_BASE_IP
                        os.makedirs(caminho_ip, exist_ok=True)

                        if os.path.exists(origem):
                            destino_arquivo_ip = os.path.join(caminho_ip, arquivo)

                            if os.path.exists(destino_arquivo_ip):
                                try:
                                    os.remove(destino_arquivo_ip)
                                except Exception as e_rm_ip:
                                    log(
                                        "[yellow]Aviso[/yellow]: não foi possível remover no destino IP: %s (%s)",
                                        destino_arquivo_ip,
                                        e_rm_ip,
                                    )

                            shutil.move(origem, destino_arquivo_ip)
                            movidos.append(destino_arquivo_ip)
                            importados.append(arquivo)
                            log(
                                "[green]Arquivo movido (via IP)[/green]: %s -> %s",
                                origem,
                                destino_arquivo_ip,
                            )
                        else:
                            msg = (
                                f"Erro ao mover (via IP): origem não encontrada: {origem} | "
                                f"destino: {caminho_ip}"
                            )
                            log(f"[red]{msg}[/red]")
                            falhas.append({"arquivo": arquivo, "motivo": msg})
                            continue

                    except Exception as e2:
                        msg = f"Falha ao mover '{arquivo}' (fallback IP): {e2}"
                        log(f"[red]{msg}[/red]")
                        falhas.append({"arquivo": arquivo, "motivo": msg})
                        continue

            except Exception as e:
                msg = f"Falha geral no processamento do arquivo: {e}"
                log(f"[red]{msg}[/red]")
                falhas.append({"arquivo": sel["arquivo"], "motivo": msg})
                continue

            await worker_sleep(2)

        # ======== RESUMO FINAL ========
        log("======== RESUMO FINAL ========")
        log("Importados (OK): %s", len(importados))
        for n in importados:
            log(" • %s", n)
        if falhas:
            log("[yellow]Falhas (%s):[/yellow]", len(falhas))
            for f in falhas:
                log(" • %s -> %s", f.get("arquivo"), f.get("motivo"))

        # Se algum arquivo chegou até a conciliação/movimentação, sucesso
        if importados:
            retorno_payload = {
                "empresa": EMPRESA,
                "importados_count": len(importados),
                "importados": importados,
                "movidos_destino": movidos,
                "falhas": falhas,
            }
            retorno_str = json.dumps(retorno_payload, ensure_ascii=False, indent=2)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=retorno_str,
                status=RpaHistoricoStatusEnum.Sucesso,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        else:
            retorno_payload = {
                "empresa": EMPRESA,
                "importados_count": 0,
                "falhas": falhas,
                "mensagem": (
                    f"Nenhum arquivo foi conciliado/movido com sucesso. "
                    f"Verificar falhas detalhadas. (extensões permitidas: {EXT_STR})."
                ),
            }
            retorno_str = json.dumps(retorno_payload, ensure_ascii=False, indent=2)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno_str,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

    except Exception as ex:
        log("[red]Exceção geral[/red]: %s", ex)
        log(ex)
        log("Traceback pode ser consultado no logger caso configurado.")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Error: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )

