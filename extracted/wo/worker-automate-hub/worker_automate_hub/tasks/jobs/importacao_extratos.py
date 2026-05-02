# -*- coding: utf-8 -*-
import asyncio
import warnings
from datetime import datetime, date
import json
import io
import pyautogui
from pywinauto.application import Application
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

ASSETS_BASE_PATH = rf"assets\importacao_extratos"
# ASSETS_BASE_PATH = r"C:\Users\automatehub\Desktop\img_leo"
ano_atual = date.today().year

# === DESTINOS ===
DESTINO_BASE = rf"Z:\Nexera\Extrato\{ano_atual}"  # tentativa principal (Z:)
DESTINO_IP_ROOT = r"\\fcaswfs01.ditrento.com.br\compartilhadas$"  # root do share
DESTINO_BASE_IP = rf"{DESTINO_IP_ROOT}\Nexera\Extrato\{ano_atual}"  # pasta final UNC

EMPRESA = "1"  # empresa fixa


def _try_get_dialog_text(win) -> str:
    """
    Tenta capturar uma mensagem textual do diálogo (Erro/Informação) sem quebrar o fluxo.
    """
    try:
        st = win.child_window(class_name="Static", found_index=0)
        txt = st.window_text()
        return (txt or "").strip()
    except Exception:
        return ""


def _formatar_falhas_clean(falhas: list[dict]) -> str:
    partes = []
    for f in falhas or []:
        arquivo = (f.get("arquivo") or "").strip() or "arquivo_desconhecido"
        motivo = (f.get("motivo") or "").strip() or "falha não especificada"
        partes.append(f"arquivo {arquivo}, {motivo}.")
    return " ".join(partes).strip()


async def importacao_extratos(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # ======== PARÂMETROS ========
        PASTA = r"Z:\Nexera\Extrato"
        IGNORAR_SE_CONTEM = [
            "EXT_237_",
            "EXT_748_",
        ]  # padrões no nome do arquivo a ignorar
        EXT_PERMITIDAS = [".ret", ".txt"]  # extensões permitidas (case-insensitive)
        TEXTO_ALVO = "SIM REDE DE POSTOS"  # texto a procurar no conteúdo
        BTN_IMPORTAR_IMG = rf"{ASSETS_BASE_PATH}\btn_imp_arq.png"
        DLG_TIT_RE = ".*Browse.*"  # regex de título do diálogo de arquivo

        EXT_STR = "/".join(EXT_PERMITIDAS).upper()

        # Credenciais para fallback UNC
        user_folder_login = await get_config_by_name("user_credentials")
        user_folder_cfg = user_folder_login.conConfiguracao or {}

        log("[cyan]Iniciando importacao_extratos[/] | empresa fixa = %s", EMPRESA)
        log(
            "Parâmetros -> pasta: %s | ignorar se contém: %s | extensões: %s | texto alvo: %s",
            PASTA,
            IGNORAR_SE_CONTEM,
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

            # 1) Ignora se o nome contiver qualquer padrão da lista IGNORAR_SE_CONTEM
            padrao_batido = next(
                (p for p in IGNORAR_SE_CONTEM if p.upper() in upper_name), None
            )
            if padrao_batido is not None:
                ignorados_nome += 1
                log("Ignorado por nome: %s (contém '%s')", nome, padrao_batido)
                continue

            # 2) Considera apenas arquivos com extensões permitidas
            if not any(lower_name.endswith(ext.lower()) for ext in EXT_PERMITIDAS):
                nao_permitido += 1
                continue

            avaliados += 1

            # 3) Procura o texto alvo dentro do arquivo (case-insensitive)
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

            # 4) Se encontrou o texto alvo, adiciona à lista de selecionados
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
        log("Arquivos avaliados (extensões permitidas) : %s", avaliados)
        log("Arquivos ignorados por nome              : %s", ignorados_nome)
        log("Arquivos ignorados por extensão          : %s", nao_permitido)
        log("Arquivos lidos com sucesso               : %s", lidos)
        log("Arquivos com erro de leitura             : %s", erros)
        log("==============================================")

        # ======== VERIFICA RESULTADO ========
        if not selecionados:
            if ignorados_nome > 0:
                msg = (
                    "Arquivos foram ignorados por nome conforme os padrões definidos: "
                    + ", ".join(IGNORAR_SE_CONTEM)
                )
            else:
                msg = f"Nenhum arquivo {EXT_STR} contendo '{TEXTO_ALVO}' encontrado."
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
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3_10.exe")
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

            # 1) Clicar no botão "Importar Arquivo"
            log("Procurando botão 'Importar Arquivo' pela imagem: %s", BTN_IMPORTAR_IMG)
            for _ in range(20):
                pos = pyautogui.locateCenterOnScreen(BTN_IMPORTAR_IMG, confidence=0.9)
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
                    class_name="TFrmImportarArquivoConciliadorBancario2", timeout=30
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
            TEMPO_MAX = 120  # segundos
            inicio = time.time()

            while time.time() - inicio < TEMPO_MAX:
                try:
                    app_dlg = Application().connect(title_re=DLG_TIT_RE)
                    dlg = app_dlg.window(title_re=DLG_TIT_RE)

                    if dlg.exists() and dlg.is_enabled():
                        log("[green]Diálogo de arquivo encontrado![/green]")
                        break

                except Exception:
                    pass

                await worker_sleep(1)

            if dlg is None or not dlg.exists():
                msg = (
                    f"Diálogo de arquivo (#32770) não apareceu dentro de {TEMPO_MAX}s."
                )
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

                # Clique do botão de importação/confirmar dentro do EMSys
                pyautogui.click(1203, 509)
                await worker_sleep(22)

                # Se aparecer "Erro" => falha e NÃO move
                viu_erro = False
                erro_msg_import = ""

                # Informação
                try:
                    app_info = Application(backend="win32").connect(
                        title="Informação", found_index=0
                    )
                    main_info = app_info["Informação"]
                    info_txt = _try_get_dialog_text(main_info)
                    try:
                        main_info.child_window(title="OK", found_index=0).click()
                    except Exception:
                        pass
                    log(
                        "[green]Confirmação de 'Informação' recebida e confirmada[/green]."
                    )
                    if info_txt:
                        log("Mensagem (Informação): %s", info_txt)
                    await worker_sleep(2)
                except Exception:
                    log(
                        "[yellow]Janela 'Informação' não apareceu (pode ser normal).[/yellow]"
                    )

                # Erro
                try:
                    app_err = Application(backend="win32").connect(
                        title="Error", found_index=0
                    )
                    main_err = app_err["Error"]
                    err_txt = _try_get_dialog_text(main_err)
                    viu_erro = True
                    log("[yellow]Janela 'Erro' detectada.[/yellow]")

                    try:
                        btn_ok = main_err.child_window(title="OK", found_index=0)
                        if btn_ok.exists():
                            btn_ok.click()
                        else:
                            main_err.close()
                    except Exception:
                        try:
                            main_err.close()
                        except Exception:
                            pass

                    await worker_sleep(1)
                    erro_msg_import = (
                        err_txt or "Importação retornou janela 'Erro' no EMSys."
                    )
                except Exception:
                    pass

                if viu_erro:
                    motivo = erro_msg_import or "Falha na importação (janela 'Erro')."

                    # >>> PRINT / LOG EXPLÍCITO DO ARQUIVO COM ERRO <<<
                    print(f"[ERRO IMPORTAÇÃO] Arquivo: {sel['arquivo']}")
                    log("[red][ERRO IMPORTAÇÃO][/red] Arquivo: %s", sel["arquivo"])
                    log("[red]Motivo:[/red] %s", motivo)

                    falhas.append({"arquivo": sel["arquivo"], "motivo": motivo})

                    # fecha janela e segue fluxo normal
                    app_imp = Application(backend="win32").connect(
                        class_name="TFrmImportarArquivoConciliadorBancario2", timeout=30
                    )
                    main_window = app_imp["TFrmImportarArquivoConciliadorBancario2"]
                    main_window.close()

                    app_info = Application(backend="win32").connect(
                        title="Information", found_index=0
                    )
                    await worker_sleep(5)
                    main_info = app_info["Information"]
                    info_txt = _try_get_dialog_text(main_info)
                    main_info.child_window(title="OK", found_index=0).click()

                    continue

                # Se não viu erro, considera OK
                log(
                    "[green]Importação marcada como OK[/green]. Prosseguindo para mover arquivo..."
                )

                # ============ MOVER ARQUIVO (SÓ SE OK) ============
                origem = sel["caminho"]
                arquivo = sel["arquivo"]

                try:
                    os.makedirs(DESTINO_BASE, exist_ok=True)
                    destino_arquivo = os.path.join(DESTINO_BASE, arquivo)

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
                    movidos.append(destino_arquivo)
                    importados.append(arquivo)
                    log(
                        "[green]Arquivo movido[/green]: %s -> %s",
                        origem,
                        destino_arquivo,
                    )

                except Exception:
                    # Fallback UNC
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
                                0, None, DESTINO_IP_ROOT, None, usuario, senha
                            )
                        except Exception as e_conn:
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
                            msg = f"Erro ao mover (via IP): origem não encontrada: {origem} | destino: {caminho_ip}"
                            log(f"[red]{msg}[/red]")
                            falhas.append({"arquivo": arquivo, "motivo": msg})
                            continue

                    except Exception as e2:
                        msg = f"Falha ao mover '{arquivo}' (fallback IP): {e2}"
                        log(f"[red]{msg}[/red]")
                        falhas.append({"arquivo": arquivo, "motivo": msg})
                        continue

            except Exception as e:
                msg = f"Falha ao preencher caminho do arquivo: {e}"
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

        # ======== RETORNO FINAL (REGRA DEFINITIVA) ========
        # REGRA: se falhas > 0 => sucesso = False (independente de importados)
        sucesso_final = len(falhas) == 0

        # Se teve falhas: retorna e sucesso False
        if falhas:
            retorno_clean = _formatar_falhas_clean(falhas)
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno_clean,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        # Se NÃO teve falhas: mantém retorno detalhado
        retorno_payload = {
            "empresa": EMPRESA,
            "importados_count": len(importados),
            "importados": importados,
            "movidos_destino": movidos,
            "falhas": falhas,
        }
        retorno_str = json.dumps(retorno_payload, ensure_ascii=False, indent=2)

        # Sem falhas, mas se por algum motivo ninguém importou: falha
        if len(importados) == 0:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=retorno_str,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        return RpaRetornoProcessoDTO(
            sucesso=sucesso_final,
            retorno=retorno_str,
            status=RpaHistoricoStatusEnum.Sucesso,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )

    except Exception as ex:
        log("[red]Exceção geral[/red]: %s", ex)
        log(ex)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Error: {ex}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
