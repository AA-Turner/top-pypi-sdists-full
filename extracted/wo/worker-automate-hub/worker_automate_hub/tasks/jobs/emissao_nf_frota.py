# -*- coding: utf-8 -*-
import asyncio
import warnings
import re
import glob
import getpass
import os
import pyautogui
import pyscreeze
import pyperclip

from pywinauto import Application, Desktop  # Desktop para diálogos
from pywinauto.timings import wait_until_passes  # wait robusto
from rich.console import Console
from pywinauto.findwindows import ElementNotFoundError

from worker_automate_hub.api.client import get_config_by_name, send_file
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.util import (
    kill_all_emsys,
    type_text_into_field,
    worker_sleep as worker_sleep_hub,  # não usamos aqui; mantido por compat
    login_emsys,
)

from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional


# =========================
# CONSOLE / PYAutoGUI
# =========================
console = Console()
pyautogui.PAUSE = 0.06
pyautogui.FAILSAFE = True

# ==========================================================
# AJUSTE CRÍTICO: não estourar ImageNotFoundException
# ==========================================================
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False

# ==========================================================
# AJUSTES
# ==========================================================
CODIGO_CONSUMIDOR_FINAL_FIXO = "140552"

AMBIENTE = "PROD"

if AMBIENTE == "PROD":
    NO_DATA = r"assets\emissao_nf_frota\no_data.png"
    BTN_FECHAR = r"assets\emissao_nf_frota\fechar_btn.png"
else:
    NO_DATA = r"C:\Users\automatehub\Desktop\img_leo\no_data.png"
    BTN_FECHAR = r"c:\Users\automatehub\Desktop\img_leo\fechar_btn.png"

USUARIO_MAQUINA = getpass.getuser()
DOWNLOADS_DIR = rf"C:\Users\{USUARIO_MAQUINA}\Downloads"

# =========================
# COORDENADAS DA TELA
# =========================
GRID_FIRST_ROW_Y = 574
GRID_CLICK_X = 1063

OPEN_CLICK_X = 1060
OPEN_CLICK_Y_OFFSET = 8

ROW_HEIGHT = 18
MAX_LINHAS = 300
MAX_REPETICOES_SEM_MUDAR = 2

TENTATIVAS_CTRL_C = 3
ESPERA_APOS_CTRL_C = 0.08

ESPERA_APOS_ABRIR = 0.35


# =========================
# TRACE / PASSOS
# =========================
_STEP_COUNTER = 0


def step(msg: str, *, level: str = "cyan") -> None:
    global _STEP_COUNTER
    _STEP_COUNTER += 1
    ts = datetime.now().strftime("%H:%M:%S")
    console.print(f"[{level}]{ts} | PASSO {_STEP_COUNTER:03d} | {msg}[/{level}]")


# =========================
# HELPERS (ASYNC SLEEP)
# =========================
async def worker_sleep(s: float):
    await asyncio.sleep(s)


# =========================
# HELPERS (NORMALIZAÇÃO)
# =========================
def _normalize_valor_ptbr(s: str) -> str:
    if not s:
        return ""
    s = str(s).strip().replace("R$", "").replace(" ", "")
    s = re.sub(r"[^0-9\.,]", "", s)
    if not s:
        return ""

    if "." in s and "," not in s:
        s = s.replace(".", ",")

    if "," in s and "." in s:
        s = s.replace(".", "")

    m = re.search(r"\d+(?:,\d{2})", s)
    if not m:
        return ""

    inteiro, dec = m.group(0).split(",", 1)
    inteiro = re.sub(r"\D", "", inteiro)
    dec = (re.sub(r"\D", "", dec) + "00")[:2]
    return f"{inteiro},{dec}" if inteiro else ""


def _extrair_total_da_linha_texto(linha: str) -> str:
    if not linha:
        return ""

    s = str(linha).replace("\r", " ").replace("\n", " ").strip()

    ptbr_milhar = re.findall(r"\d{1,3}(?:\.\d{3})+,\d{2}", s)
    ptbr_simples = re.findall(r"\d+,\d{2}", s)
    en_simples = re.findall(r"\d+\.\d{2}", s)

    candidatos = ptbr_milhar or ptbr_simples or en_simples
    if not candidatos:
        return ""

    candidatos.sort(key=len, reverse=True)
    return _normalize_valor_ptbr(candidatos[0])


def _normalizar_valor_para_nome(valor: str) -> str:
    return re.sub(r"[^\d]", "", str(valor))


# ==========================================================
# ADAPTADORES (configEntrada)
# ==========================================================
def _data_iso_para_br(data_iso: Any) -> str:
    if not data_iso:
        return ""
    s = str(data_iso).strip()

    if re.match(r"^\d{2}/\d{2}/\d{4}$", s):
        return s

    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        yyyy, mm, dd = m.groups()
        return f"{dd}/{mm}/{yyyy}"

    try:
        dt = datetime.fromisoformat(s)
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return s


def _valor_any_para_ptbr(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    try:
        return f"{float(v):.2f}".replace(".", ",")
    except Exception:
        return str(v)


def _split_codigos_pgto(codigos: Any) -> List[str]:
    if codigos is None:
        return []
    if isinstance(codigos, list):
        out = []
        for c in codigos:
            s = str(c).strip()
            if s:
                out.append(s)
        return out

    s = str(codigos).strip()
    if not s:
        return []
    partes = [p.strip() for p in s.split(",")]
    return [p for p in partes if p]


def adaptar_item_entrada_para_nota(item: Dict[str, Any]) -> Dict[str, Any]:
    item = item or {}
    lista_pgto = _split_codigos_pgto(item.get("codigoFormaPagamento"))

    return {
        "filialEmpresaOrigem": str(item.get("filialEmpresaOrigem") or "").strip(),
        "data": _data_iso_para_br(item.get("data")),
        "codigoTransacao": (item.get("codigoTransacao") or None),
        "valor": _valor_any_para_ptbr(item.get("valor")),
        "codigoFormaPagamento": str(item.get("codigoFormaPagamento") or "").strip(),
        "codigoFormaPagamentoLista": lista_pgto,
        "codigoClienteCorreto": str(item.get("codigoClienteCorreto") or "").strip(),
    }


def extrair_notas_de_config_entrada(config_entrada: Any) -> List[Dict[str, Any]]:
    step("Extrair notas do configEntrada")
    if not config_entrada:
        step("configEntrada vazio: nenhuma nota extraída", level="yellow")
        return []

    if isinstance(config_entrada, list):
        notas: List[Dict[str, Any]] = []
        for it in config_entrada:
            if isinstance(it, dict):
                notas.append(adaptar_item_entrada_para_nota(it))
        step(f"configEntrada (list) -> {len(notas)} nota(s)")
        return notas

    if isinstance(config_entrada, dict):
        step("configEntrada (dict) -> 1 nota")
        return [adaptar_item_entrada_para_nota(config_entrada)]

    try:
        import json

        obj = json.loads(str(config_entrada))
        return extrair_notas_de_config_entrada(obj)
    except Exception:
        step(
            "configEntrada em formato desconhecido: não consegui parsear",
            level="yellow",
        )
        return []


def expandir_notas_por_pagamento(notas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for n in notas or []:
        lista = n.get("codigoFormaPagamentoLista") or []
        if not isinstance(lista, list):
            lista = _split_codigos_pgto(lista)

        if not lista:
            lista = _split_codigos_pgto(n.get("codigoFormaPagamento"))

        if not lista:
            n2 = dict(n)
            n2["codigoFormaPagamento"] = ""
            n2["codigoFormaPagamentoLista"] = []
            out.append(n2)
            continue

        for cod in lista:
            n2 = dict(n)
            n2["codigoFormaPagamento"] = cod
            out.append(n2)

    step(f"Expandir notas por pagamento -> {len(out)} tentativa(s)")
    return out


# ==========================================================
# FILIAL ORIGEM
# ==========================================================
def resolver_filial_origem(
    filial_origem_param: Optional[str],
    notas: List[Dict[str, Any]],
    config_entrada_raw: Any,
) -> str:
    if filial_origem_param and str(filial_origem_param).strip():
        return str(filial_origem_param).strip()

    filiais = [str(n.get("filialEmpresaOrigem") or "").strip() for n in (notas or [])]
    filiais = [f for f in filiais if f]

    if filiais:
        unicas = sorted(set(filiais))
        if len(unicas) == 1:
            return unicas[0]
        raise ValueError(f"configEntrada trouxe múltiplas filiais diferentes: {unicas}")

    if isinstance(config_entrada_raw, dict):
        f = str(config_entrada_raw.get("filialEmpresaOrigem") or "").strip()
        if f:
            return f

    if isinstance(config_entrada_raw, list):
        filiais2 = []
        for it in config_entrada_raw:
            if isinstance(it, dict):
                f = str(it.get("filialEmpresaOrigem") or "").strip()
                if f:
                    filiais2.append(f)
        unicas2 = sorted(set(filiais2))
        if len(unicas2) == 1:
            return unicas2[0]
        if len(unicas2) > 1:
            raise ValueError(
                f"configEntrada trouxe múltiplas filiais diferentes: {unicas2}"
            )

    return ""


# =========================
# AÇÕES NA TELA "GERA NOTA"
# =========================
def preencher_codigo_cliente(janela_gera_nota, codigo_cliente: str) -> None:
    step(f"Preencher código do cliente na tela Gera Nota: {codigo_cliente}")
    campo_codigo = janela_gera_nota.child_window(class_name="TDBIEditCode")
    campo_codigo.wait("ready", timeout=10)
    campo_codigo.set_focus()
    campo_codigo.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_codigo.type_keys(str(codigo_cliente), with_spaces=True)
    campo_codigo.type_keys("{TAB}", with_spaces=True)


def clicar_gera_nota_fiscal(app: Application) -> bool:
    step("Clicar em 'Gera Nota Fiscal' (menu/botão/fallback)")
    try:
        main = app.top_window()
        main.set_focus()

        try:
            step(
                "Tentativa 1: menu_select Gera Nota Fiscal de Cupom -> Gera Nota Fiscal"
            )
            main.menu_select("Gera Nota Fiscal de Cupom->Gera Nota Fiscal")
            step("Clique via menu_select OK", level="green")
            return True
        except Exception:
            step(
                "menu_select não disponível/ falhou; seguindo para botão",
                level="yellow",
            )

        try:
            j = app["TFrmGeraNotaCupomFiscal"]
            j.wait("ready", timeout=10)
            j.set_focus()

            for cls in ("TBitBtn", "TDBIBitBtn"):
                try:
                    step(f"Tentativa 2: botão por title_re em class={cls}")
                    b = j.child_window(class_name=cls, title_re=".*Gera Nota Fiscal.*")
                    b.wait("enabled", timeout=2)
                    b.click_input()
                    step("Clique via botão title_re OK", level="green")
                    return True
                except Exception:
                    pass

            try:
                step("Tentativa 3: botão por found_index=3")
                b = j.child_window(class_name="TBitBtn", found_index=3)
                b.wait("enabled", timeout=2)
                b.click_input()
                step("Clique via found_index OK", level="green")
                return True
            except Exception:
                step("found_index=3 falhou", level="yellow")

        except Exception:
            step(
                "Janela TFrmGeraNotaCupomFiscal não acessível por pywinauto",
                level="yellow",
            )

        step("Fallback final: pressionar ENTER", level="yellow")
        pyautogui.press("enter")
        return True

    except Exception as e:
        step(f"Falha ao clicar em 'Gera Nota Fiscal': {e}", level="red")
        return False


def clicar_ok_janela_seleciona_cupom(app: Application) -> bool:
    step("Clicar OK na janela TFrmSelecionaCupomFiscal")
    try:
        janela = app["TFrmSelecionaCupomFiscal"]
        janela.wait("ready", timeout=10)
        janela.set_focus()

        try:
            btn_ok = janela.child_window(class_name="TDBIBitBtn", title="OK")
            btn_ok.wait("enabled", timeout=20)
            btn_ok.click_input()
            step("OK clicado na TFrmSelecionaCupomFiscal", level="green")
            return True
        except Exception:
            step("Não encontrei botão OK por TDBIBitBtn/title=OK", level="yellow")
            return False

    except Exception as e:
        step(f"Falha ao acessar janela TFrmSelecionaCupomFiscal: {e}", level="red")
        return False


# =========================
# CLIPBOARD GRID
# =========================
async def _copiar_linha_selecionada_via_clipboard() -> Tuple[str, str]:
    texto = ""
    for tentativa in range(1, TENTATIVAS_CTRL_C + 1):
        step(f"Grid Ctrl+C tentativa {tentativa}/{TENTATIVAS_CTRL_C}", level="dim")
        pyperclip.copy("")
        pyautogui.hotkey("ctrl", "c")
        await worker_sleep(ESPERA_APOS_CTRL_C)

        texto = pyperclip.paste() or ""
        texto = texto.replace("\r", " ").replace("\n", " ").strip()
        if texto:
            break

    valor = _extrair_total_da_linha_texto(texto)
    return valor, texto


async def varrer_grid_por_down() -> List[Tuple[str, str]]:
    step("Iniciar varredura do grid (DOWN + Ctrl+C)")
    itens: List[Tuple[str, str]] = []

    pyautogui.click(GRID_CLICK_X, GRID_FIRST_ROW_Y)
    await worker_sleep(0.15)

    ultimo_raw: Optional[str] = None
    repet_sem_mudar = 0
    raws_vistos: set = set()

    for i in range(1, MAX_LINHAS + 1):
        valor, raw = await _copiar_linha_selecionada_via_clipboard()
        raw_curto = raw[:140] + ("..." if len(raw) > 140 else "")

        if not raw and ultimo_raw is not None:
            repet_sem_mudar += 1
            console.print(
                f"[dim]Linha {i:03d} -> raw vazio (rep {repet_sem_mudar}/{MAX_REPETICOES_SEM_MUDAR})[/dim]"
            )
            if repet_sem_mudar >= MAX_REPETICOES_SEM_MUDAR:
                step("Fim do grid detectado (clipboard vazio repetido)", level="yellow")
                break
            pyautogui.press("down")
            await worker_sleep(0.06)
            continue

        console.print(
            f"[dim]Linha {i:03d} -> valor='{valor}' | raw='{raw_curto}'[/dim]"
        )

        if ultimo_raw is not None and raw == ultimo_raw:
            repet_sem_mudar += 1
            console.print(
                f"[yellow]Linha repetida detectada (rep {repet_sem_mudar}/{MAX_REPETICOES_SEM_MUDAR}).[/yellow]"
            )
            if repet_sem_mudar >= MAX_REPETICOES_SEM_MUDAR:
                step("Fim do grid detectado (Ctrl+C não muda mais)", level="yellow")
                break

            pyautogui.press("down")
            await worker_sleep(0.06)
            continue

        repet_sem_mudar = 0
        ultimo_raw = raw

        if raw not in raws_vistos:
            raws_vistos.add(raw)
            itens.append((valor, raw))

        pyautogui.press("down")
        await worker_sleep(0.06)

    step(
        f"Varredura do grid concluída: {len(itens)} linha(s) únicas coletadas",
        level="green",
    )
    return itens


def _y_da_linha(index_1_based: int) -> int:
    return int(
        GRID_FIRST_ROW_Y + (index_1_based - 1) * ROW_HEIGHT + OPEN_CLICK_Y_OFFSET
    )


async def ir_para_linha_e_abrir(index_1_based: int, double_click: bool = True):
    step(f"Ir para linha {index_1_based} e abrir (double_click={double_click})")
    pyautogui.click(GRID_CLICK_X, GRID_FIRST_ROW_Y)
    await worker_sleep(3)

    for _ in range(index_1_based - 1):
        pyautogui.press("down")
        await worker_sleep(0.03)

    if double_click:
        x = OPEN_CLICK_X
        y = _y_da_linha(index_1_based)

        pyautogui.moveTo(x, y)
        await worker_sleep(0.12)

        pyautogui.click(clicks=2, interval=0.12)
        await worker_sleep(ESPERA_APOS_ABRIR)
        step("Linha aberta via double click", level="green")


async def buscar_valor_unico_e_abrir(
    valor_alvo: str, double_click: bool = True
) -> Tuple[bool, str]:
    alvo = _normalize_valor_ptbr(valor_alvo)
    if not alvo:
        return False, f"Valor alvo inválido: '{valor_alvo}'"

    step(f"Procurar Total Cupom único no grid: alvo={alvo}")
    itens = await varrer_grid_por_down()
    valores = [v for (v, _raw) in itens]
    linhas_match = [i + 1 for i, v in enumerate(valores) if v == alvo]

    if len(linhas_match) == 0:
        step("Nenhum cupom encontrado para o valor alvo", level="yellow")
        return False, f"NAO_ENCONTRADO: nenhum cupom com Total Cupom={alvo}"

    if len(linhas_match) > 1:
        step(
            f"Valor duplicado: apareceu em {len(linhas_match)} linhas {linhas_match}",
            level="yellow",
        )
        return (
            False,
            f"VALOR_DUPLICADO: Total Cupom={alvo} aparece em {len(linhas_match)} linhas {linhas_match}",
        )

    linha = linhas_match[0]
    step(f"Único encontrado na linha {linha}. Abrindo...", level="green")
    await ir_para_linha_e_abrir(linha, double_click=double_click)

    return True, f"OK: Total Cupom={alvo} (linha {linha})"


async def _voltar_para_tela_gera_nota(app: Application) -> None:
    step("Normalizar UI e voltar para a tela TFrmGeraNotaCupomFiscal", level="dim")
    for _ in range(3):
        try:
            top = app.top_window()
            top.set_focus()
            pyautogui.press("esc")
            await worker_sleep(0.2)
        except Exception:
            pass


# ==========================================================
# PESQUISAR COM FILTROS
# ==========================================================
async def pesquisar_nfe_com_filtros(
    app: Application,
    nota: Dict[str, Any],
    double_click: bool = True,
) -> Tuple[bool, str, bool]:
    step("Abrir janela TFrmSelecionaCupomFiscal e preencher filtros")
    janela = app["TFrmSelecionaCupomFiscal"]
    janela.set_focus()

    data_nota = str(nota.get("data") or "").strip()
    codigo_pgto = str(nota.get("codigoFormaPagamento") or "").strip()
    valor_nota = str(nota.get("valor") or "").strip()

    step(
        f"Filtros: data={data_nota} | valor={_normalize_valor_ptbr(valor_nota)} | pgto={codigo_pgto}",
        level="dim",
    )

    campo_data_inicial = janela.child_window(class_name="TDBIEditDate", found_index=1)
    campo_data_inicial.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_data_inicial.type_keys(f"{data_nota}{{TAB}}", with_spaces=True)

    campo_data_final = janela.child_window(class_name="TDBIEditDate", found_index=0)
    campo_data_final.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_data_final.type_keys(f"{data_nota}{{TAB}}", with_spaces=True)

    campo_valor_inicial = janela.child_window(
        class_name="TDBIEditNumber", found_index=2
    )
    campo_valor_inicial.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_valor_inicial.type_keys(f"{valor_nota}{{TAB}}", with_spaces=True)

    campo_valor_final = janela.child_window(class_name="TDBIEditNumber", found_index=1)
    campo_valor_final.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_valor_final.type_keys(f"{valor_nota}{{TAB}}", with_spaces=True)

    campo_pagamento = janela.child_window(class_name="TDBIEditCode", found_index=1)
    campo_pagamento.type_keys("^a{BACKSPACE}", with_spaces=True)
    campo_pagamento.type_keys(f"{codigo_pgto}{{TAB}}", with_spaces=True)

    step("Clicar no botão Pesquisar (found_index=3)", level="dim")
    janela.child_window(class_name="TDBIBitBtn", found_index=3).click_input()

    step("Aguardar resultado da pesquisa (sleep 30s)", level="dim")
    await worker_sleep(30)

    step("Verificar se apareceu imagem NO_DATA", level="dim")
    try:
        pos_no_data = pyautogui.locateCenterOnScreen(NO_DATA, confidence=0.85)
    except Exception as e:
        pos_no_data = None
        step(f"Erro ao localizar imagem NO_DATA (tratado): {e}", level="yellow")

    if pos_no_data:
        step("NO_DATA encontrado (sem registros)", level="yellow")
        try:
            janela.close()
        except Exception:
            pass
        return False, "NO_DATA encontrado", True

    step(
        "NO_DATA não encontrado: há registros (vou localizar por Total Cupom)",
        level="green",
    )

    valor_alvo = str(nota.get("valor") or "").strip()
    ok, msg = await buscar_valor_unico_e_abrir(valor_alvo, double_click=double_click)
    if not ok:
        step(f"Falha ao abrir por valor único: {msg}", level="yellow")
        return False, msg, False

    await worker_sleep(3)

    step("Confirmar seleção na janela (OK)", level="dim")
    clicou_ok = clicar_ok_janela_seleciona_cupom(app)
    if not clicou_ok:
        step("Fallback: pressionar ENTER para confirmar", level="yellow")
        try:
            pyautogui.press("enter")
        except Exception:
            pass

    return True, msg, False


# ==========================================================
# FUNÇÕES: (GERAR/EXPORTAR/ENVIAR)
# ==========================================================
def _arquivo_mais_recente(pasta: str, extensao: str) -> str:
    step(
        f"Localizar arquivo mais recente: pasta={pasta} extensao={extensao}",
        level="dim",
    )
    ext = extensao.lower().strip()
    if not ext.startswith("."):
        ext = "." + ext

    padrao = os.path.join(pasta, f"*{ext}")
    candidatos = [p for p in glob.glob(padrao) if os.path.isfile(p)]
    if not candidatos:
        raise FileNotFoundError(f"Nenhum arquivo '{ext}' encontrado em: {pasta}")

    candidatos.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    step(f"Arquivo mais recente encontrado: {candidatos[0]}", level="green")
    return candidatos[0]


def _click_yes_messageform() -> None:
    app_msg = Application().connect(class_name="TMessageForm")
    win = app_msg["TMessageForm"]
    btn = win.child_window(title="&Yes", class_name="TButton")
    btn.click_input()


def _click_no_messageform() -> None:
    app_msg = Application().connect(class_name="TMessageForm")
    win = app_msg["TMessageForm"]
    btn = win.child_window(title="&No", class_name="TButton")
    btn.click_input()


def _click_ok_messageform() -> None:
    app_msg = Application().connect(class_name="TMessageForm")
    win = app_msg["TMessageForm"]
    win.child_window(title="OK", found_index=0).click()


# ==========================================================
# Browse Folder robusto (Desktop + wait)
# ==========================================================
async def _selecionar_downloads_dialog_browse_folder_por_teclado() -> None:
    step("Aguardar diálogo de pasta (Browse/Procurar/Selecionar)", level="dim")
    title_re = r"(Procurar Pasta|Browse For Folder|Selecionar Pasta|Select Folder|Selecionar Diretório|Select Directory)"

    await worker_sleep(3)

    def _get_dlg():
        dlg = Desktop(backend="win32").window(title_re=title_re)
        dlg.wait("exists enabled visible ready", timeout=15)
        return dlg

    try:
        dlg = wait_until_passes(15, 0.5, _get_dlg)
    except Exception as e:
        raise RuntimeError(
            f"Não consegui encontrar o diálogo de seleção de pasta. Detalhe: {e}"
        )

    dlg.set_focus()
    await worker_sleep(0.3)

    CLICK_X = 981
    CLICK_Y = 454
    pyautogui.click(CLICK_X, CLICK_Y)
    await worker_sleep(0.25)

    pyautogui.press("home")
    await worker_sleep(0.25)

    for _ in range(2):
        pyautogui.press("d")
        await worker_sleep(0.15)

    pyautogui.press("enter")
    await worker_sleep(0.25)

    step("Downloads selecionado e confirmado (Browse Folder)", level="green")


async def _selecionar_downloads_dialog_select_directory_por_edit(
    downloads_dir: str,
) -> None:
    step("Aguardar diálogo 'Select Directory' ficar disponível (robusto)", level="dim")

    title_re = r"(Select Directory|Selecionar Diretório|Selecionar diretorio|Procurar Pasta|Select Folder|Selecionar Pasta)"

    def _get_dlg():
        dlg = Desktop(backend="win32").window(title_re=title_re)
        dlg.wait("exists enabled visible ready", timeout=20)
        return dlg

    try:
        dlg = wait_until_passes(25, 0.4, _get_dlg)
    except Exception as e:
        raise TimeoutError(
            f"Diálogo 'Select Directory' não apareceu a tempo. Detalhe: {e}"
        )

    dlg.set_focus()
    await worker_sleep(0.25)

    edit = None
    try:
        edit = dlg.child_window(class_name="Edit")
        edit.wait("ready", timeout=5)
    except Exception:
        try:
            edits = dlg.descendants(class_name="Edit")
            if edits:
                edit = edits[0]
        except Exception:
            edit = None

    if not edit:
        raise ElementNotFoundError(
            "Não encontrei campo Edit no diálogo 'Select Directory'."
        )

    last_err = None
    for tentativa in range(1, 4):
        try:
            step(
                f"Preencher caminho no diálogo (tentativa {tentativa}/3): {downloads_dir}",
                level="dim",
            )
            edit.set_focus()
            await worker_sleep(0.15)

            edit.type_keys("^a{BACKSPACE}", with_spaces=True)
            await worker_sleep(0.10)

            try:
                import pyperclip

                pyperclip.copy(downloads_dir)
                pyautogui.hotkey("ctrl", "v")
            except Exception:
                edit.type_keys(downloads_dir, with_spaces=True)

            await worker_sleep(0.25)

            pyautogui.press("tab")
            await worker_sleep(0.15)
            pyautogui.press("enter")
            await worker_sleep(0.6)

            step(
                "Caminho Downloads informado e confirmado (TAB + ENTER)", level="green"
            )
            return

        except Exception as e:
            last_err = e
            await worker_sleep(0.6)

    raise TimeoutError(
        f"Não consegui preencher/confirmar o caminho no Select Directory. Último erro: {last_err}"
    )


async def executar_fluxo_geracao_exportacao_envio(
    app: Application,
    nota: Dict[str, Any],
    uuid_relacao: str,
    downloads_dir: str,
) -> None:
    step(
        "Iniciar fluxo: Gera NF -> Transmitir -> Exportar XML -> Gerar PDF -> Enviar -> Cleanup",
        level="cyan",
    )

    ok_gera = clicar_gera_nota_fiscal(app)
    if not ok_gera:
        step(
            "Não consegui clicar em 'Gera Nota Fiscal' (fallback Enter acionado)",
            level="yellow",
        )

    step("Aguardar janelas de confirmação (sleep 4s)", level="dim")
    await worker_sleep(8)

    step("Confirmar TMessageForm (&Yes) - 1", level="dim")
    _click_yes_messageform()

    step("Aguardar (sleep 4s)", level="dim")
    await worker_sleep(8)

    step("Confirmar TMessageForm (&Yes) - 2", level="dim")
    _click_yes_messageform()

    step("Aguardar (sleep 4s)", level="dim")
    await worker_sleep(8)

    step("Clicar em Transmitir (TFrmGerenciadorNFe2 found_index=5)", level="dim")
    app_nfe = Application().connect(class_name="TFrmGerenciadorNFe2")
    win_nfe = app_nfe["TFrmGerenciadorNFe2"]
    win_nfe.child_window(class_name="TBitBtn", found_index=5).click_input()

    step("Aguardar (sleep 5s)", level="dim")
    await worker_sleep(10)

    step("Clicar OK Information (TMessageForm)", level="dim")
    _click_ok_messageform()

    step("Aguardar (sleep 5s)", level="dim")
    await worker_sleep(5)

    step("Tentar localizar BTN_FECHAR (imagem)", level="dim")
    try:
        btn_fechar = pyautogui.locateCenterOnScreen(BTN_FECHAR, confidence=0.85)
    except Exception as e:
        btn_fechar = None
        step(f"Erro ao localizar imagem BTN_FECHAR (tratado): {e}", level="yellow")

    if btn_fechar:
        step("BTN_FECHAR encontrado, clicando", level="dim")
        pyautogui.click(btn_fechar)
        pyautogui.sleep(0.5)
    else:
        step("BTN_FECHAR não encontrado, seguindo fluxo", level="cyan")

    step("Aguardar (sleep 5s)", level="dim")
    await worker_sleep(5)

    step("Clicar em Exportar NF-e (TFrmGerenciadorNFe2 found_index=1)", level="dim")
    app_nfe = Application().connect(class_name="TFrmGerenciadorNFe2")
    win_nfe = app_nfe["TFrmGerenciadorNFe2"]
    win_nfe.child_window(class_name="TBitBtn", found_index=1).click_input()

    step("Selecionar pasta Downloads no dialog 'Procurar Pasta' (XML)", level="dim")
    await _selecionar_downloads_dialog_browse_folder_por_teclado()
    await worker_sleep(3)

    step("Confirmar TMessageForm (&No) após exportar XML", level="dim")
    _click_no_messageform()

    step("Aguardar (sleep 3s)", level="dim")
    await worker_sleep(3)

    step("Clicar OK Information (TMessageForm) após exportar XML", level="dim")
    _click_ok_messageform()

    await worker_sleep(3)

    step("Clicar em Imprimir DANFE (TFrmGerenciadorNFe2 found_index=0)", level="dim")
    app_nfe = Application().connect(class_name="TFrmGerenciadorNFe2")
    win_nfe = app_nfe["TFrmGerenciadorNFe2"]
    win_nfe.child_window(class_name="TBitBtn", found_index=0).click_input()

    await worker_sleep(3)

    step("Selecionar saída PDF (TFrmConfiguraTemplateDANF2)", level="dim")
    app_danfe = Application().connect(class_name="TFrmConfiguraTemplateDANF2")
    win_danfe = app_danfe["TFrmConfiguraTemplateDANF2"]
    win_danfe.child_window(title="&PDF", class_name="TRadioButton").click_input()

    await worker_sleep(3)

    step("Clicar em Gerar (DANFE PDF)", level="dim")
    win_danfe.child_window(title="Gerar", class_name="TBitBtn").click_input()

    await worker_sleep(10)

    step("Selecionar diretório Downloads no dialog 'Select Directory'", level="dim")
    await _selecionar_downloads_dialog_select_directory_por_edit(downloads_dir)

    await worker_sleep(5)

    step("Clicar OK (TMessageForm) após gerar PDF", level="dim")
    _click_ok_messageform()

    await worker_sleep(3)

    step("Fechar janela TFrmConfiguraTemplateDANF2", level="dim")
    app_danfe = Application().connect(class_name="TFrmConfiguraTemplateDANF2")
    app_danfe["TFrmConfiguraTemplateDANF2"].close()

    await worker_sleep(3)

    step("Fechar janela TFrmGerenciadorNFe2", level="dim")
    app_nfe = Application().connect(class_name="TFrmGerenciadorNFe2")
    app_nfe["TFrmGerenciadorNFe2"].close()

    await worker_sleep(3)

    step("Localizar PDF e XML mais recentes no Downloads", level="dim")
    caminho_pdf = _arquivo_mais_recente(downloads_dir, "pdf")
    caminho_xml = _arquivo_mais_recente(downloads_dir, "xml")

    step("Montar nome padrão dos arquivos (filial_cliente_pgto_valor)", level="dim")
    filial = str(nota.get("filialEmpresaOrigem"))
    codigo_cliente = str(nota.get("codigoClienteCorreto"))
    codigo_pgto = str(nota.get("codigoFormaPagamento"))
    valor_limpo = _normalizar_valor_para_nome(nota.get("valor"))

    nome_base = f"{filial}_{codigo_cliente}_{codigo_pgto}_{valor_limpo}"
    nome_pdf = f"{nome_base}.pdf"
    nome_xml = f"{nome_base}.xml"
    step(f"Nome base: {nome_base}", level="dim")

    step("Ler bytes do PDF/XML (bytes puros)", level="dim")
    with open(caminho_pdf, "rb") as f:
        pdf_bytes = f.read()
    with open(caminho_xml, "rb") as f:
        xml_bytes = f.read()

    step("Enviar PDF via send_file()", level="dim")
    await send_file(uuid_relacao, nome_pdf, "pdf", pdf_bytes, file_extension="pdf")

    step("Enviar XML via send_file()", level="dim")
    await send_file(uuid_relacao, nome_xml, "xml", xml_bytes, file_extension="xml")

    step("Remover arquivos locais do Downloads (cleanup)", level="dim")
    os.remove(caminho_pdf)
    os.remove(caminho_xml)

    step(f"ENVIADO OK: {nome_pdf} + {nome_xml}", level="green")


# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def emissao_nf_frota(
    task: RpaProcessoEntradaDTO,
    filial_origem: Optional[str] = None,
    notas: Optional[List[Dict[str, Any]]] = None,
    codigo_consumidor_final: str = CODIGO_CONSUMIDOR_FINAL_FIXO,
    historico_id: str = "",
) -> RpaRetornoProcessoDTO:
    step("Início emissao_nf_frota()")
    try:
        step("Carregar config 'login_emsys'")
        config = await get_config_by_name("login_emsys")

        step("Resolver uuidRelacao (uuidProcesso)")
        uuid_relacao = str(task.historico_id or "").strip()
        if not uuid_relacao:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="uuidProcesso está vazio. Não posso enviar arquivo sem uuidRelacao.",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        step(f"uuid_relacao resolvido: {uuid_relacao}", level="green")

        step("kill_all_emsys()")
        await kill_all_emsys()

        step("Configurar warnings para pywinauto 32-bit", level="dim")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        step("Abrir EMSys")
        app = Application(backend="win32").start(r"C:\Rezende\EMSys3\EMSys3_10.exe")

        step("Carregar notas (task.configEntrada -> lista)")
        if not notas:
            notas = extrair_notas_de_config_entrada(task.configEntrada)

        if not notas:
            step("Nenhuma nota válida em configEntrada. Retornando falha.", level="red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"configEntrada não trouxe notas válidas. configEntrada={task.configEntrada}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        step("Resolver filial_origem a partir do configEntrada")
        try:
            filial_origem_resolvida = resolver_filial_origem(
                filial_origem_param=filial_origem,
                notas=notas,
                config_entrada_raw=task.configEntrada,
            )
        except Exception as e_filial:
            step(f"Filial inválida no configEntrada: {e_filial}", level="red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Filial inválida no configEntrada: {e_filial}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        filial_origem_resolvida = (filial_origem_resolvida or "").strip()
        if not filial_origem_resolvida:
            step(
                "Não foi possível resolver filial_origem no configEntrada.", level="red"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possível resolver 'filialEmpresaOrigem' no configEntrada. configEntrada={task.configEntrada}",
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        step(f"Filial origem resolvida: {filial_origem_resolvida}", level="green")

        step("Login no EMSys")
        return_login = await login_emsys(
            config.conConfiguracao, app, task, filial_origem=filial_origem_resolvida
        )

        main = app.top_window()
        main.set_focus()

        if not return_login.sucesso:
            step("Falha no login. Retornando.", level="red")
            return return_login

        step("Ir para 'gera nota fiscal de cupom' via busca no menu")
        type_text_into_field(
            "gera nota fiscal de cupom", app["TFrmMenuPrincipal"]["Edit"], True, "50"
        )

        step("Confirmar acesso ao menu (ENTER x2) e aguardar abertura", level="dim")
        await worker_sleep(3)
        pyautogui.press("enter", presses=2)
        await worker_sleep(4)

        resultados_sucesso: List[Dict[str, Any]] = []
        resultados_erro: List[Dict[str, Any]] = []

        tentativas = expandir_notas_por_pagamento(notas)

        for idx, nota in enumerate(tentativas, start=1):
            step(
                f"Início processamento da tentativa {idx}/{len(tentativas)}",
                level="dim",
            )

            try:
                codigo_cliente_correto = str(
                    nota.get("codigoClienteCorreto") or ""
                ).strip()
                if not codigo_cliente_correto:
                    step(
                        "codigoClienteCorreto vazio. Pulando tentativa.", level="yellow"
                    )
                    resultados_erro.append(
                        {
                            "tentativa": idx,
                            "status": "SKIP",
                            "motivo": "codigoClienteCorreto vazio",
                            "data": nota.get("data"),
                            "valor": _normalize_valor_ptbr(nota.get("valor")),
                            "formaPgto": nota.get("codigoFormaPagamento"),
                            "filial": nota.get("filialEmpresaOrigem"),
                        }
                    )
                    await _voltar_para_tela_gera_nota(app)
                    continue

                step(
                    f"Resumo nota: filial={nota.get('filialEmpresaOrigem')} | "
                    f"data={nota.get('data')} | valor={_normalize_valor_ptbr(nota.get('valor'))} | "
                    f"pgto={nota.get('codigoFormaPagamento')} | cliente={codigo_cliente_correto}",
                    level="dim",
                )

                # 1) tenta com cliente correto
                step("Focar janela TFrmGeraNotaCupomFiscal", level="dim")
                janela_gera = app["TFrmGeraNotaCupomFiscal"]
                janela_gera.set_focus()

                preencher_codigo_cliente(janela_gera, codigo_cliente_correto)

                step(
                    "Clicar 'Buscar Itens/Cupons' (TBitBtn found_index=2)", level="dim"
                )
                janela_gera.child_window(
                    class_name="TBitBtn", found_index=2
                ).click_input()
                await worker_sleep(1)

                step("Pesquisar com filtros (cliente correto)", level="dim")
                app["TFrmSelecionaCupomFiscal"].set_focus()
                encontrou, motivo, no_data = await pesquisar_nfe_com_filtros(
                    app, nota, double_click=True
                )

                if encontrou:
                    step(
                        "Cupom encontrado. Executar fluxo completo (envio incluído).",
                        level="green",
                    )

                    await executar_fluxo_geracao_exportacao_envio(
                        app=app,
                        nota=nota,
                        uuid_relacao=uuid_relacao,
                        downloads_dir=DOWNLOADS_DIR,
                    )

                    resultados_sucesso.append(
                        {
                            "tentativa": idx,
                            "status": "SUCESSO",
                            "cliente_usado": codigo_cliente_correto,
                            "fallback_consumidor_final": False,
                            "data": nota.get("data"),
                            "valor": _normalize_valor_ptbr(nota.get("valor")),
                            "formaPgto": nota.get("codigoFormaPagamento"),
                            "filial": nota.get("filialEmpresaOrigem"),
                            "motivo": motivo,
                        }
                    )
                    step(f"Final: SUCESSO na tentativa {idx}. Parando.", level="green")
                    break

                # se não encontrou com cliente correto, registra ocorrência (só vai aparecer no retorno se falhar geral)
                resultados_erro.append(
                    {
                        "tentativa": idx,
                        "status": "NAO_ENCONTRADO_CLIENTE",
                        "cliente_usado": codigo_cliente_correto,
                        "data": nota.get("data"),
                        "valor": _normalize_valor_ptbr(nota.get("valor")),
                        "formaPgto": nota.get("codigoFormaPagamento"),
                        "filial": nota.get("filialEmpresaOrigem"),
                        "motivo": motivo,
                        "no_data": bool(no_data),
                    }
                )

                # 2) tenta consumidor final
                step(
                    f"Não encontrou com cliente {codigo_cliente_correto}. Tentar consumidor final {codigo_consumidor_final}",
                    level="yellow",
                )

                await _voltar_para_tela_gera_nota(app)

                janela_gera = app["TFrmGeraNotaCupomFiscal"]
                janela_gera.set_focus()

                step("Preencher cliente consumidor final", level="dim")
                preencher_codigo_cliente(janela_gera, codigo_consumidor_final)

                step(
                    "Clicar 'Buscar Itens/Cupons' (TBitBtn found_index=2)", level="dim"
                )
                janela_gera.child_window(
                    class_name="TBitBtn", found_index=2
                ).click_input()

                step("Aguardar retorno da busca (sleep 15s)", level="dim")
                await worker_sleep(15)

                step("Pesquisar com filtros (consumidor final)", level="dim")
                app["TFrmSelecionaCupomFiscal"].set_focus()
                encontrou2, motivo2, no_data2 = await pesquisar_nfe_com_filtros(
                    app, nota, double_click=True
                )

                if encontrou2:
                    step(
                        "Encontrou com consumidor final. Trocar para cliente correto e emitir.",
                        level="green",
                    )

                    await _voltar_para_tela_gera_nota(app)

                    janela_gera = app["TFrmGeraNotaCupomFiscal"]
                    janela_gera.set_focus()

                    step("Repreencher cliente correto antes do fluxo", level="dim")
                    preencher_codigo_cliente(janela_gera, codigo_cliente_correto)
                    await worker_sleep(2)

                    await executar_fluxo_geracao_exportacao_envio(
                        app=app,
                        nota=nota,
                        uuid_relacao=uuid_relacao,
                        downloads_dir=DOWNLOADS_DIR,
                    )

                    resultados_sucesso.append(
                        {
                            "tentativa": idx,
                            "status": "SUCESSO",
                            "cliente_usado": codigo_consumidor_final,
                            "fallback_consumidor_final": True,
                            "data": nota.get("data"),
                            "valor": _normalize_valor_ptbr(nota.get("valor")),
                            "formaPgto": nota.get("codigoFormaPagamento"),
                            "filial": nota.get("filialEmpresaOrigem"),
                            "motivo": motivo2,
                        }
                    )
                    step(
                        f"Final: SUCESSO (consumidor final) na tentativa {idx}. Parando.",
                        level="green",
                    )
                    break

                # se não encontrou com consumidor final, registra ocorrência (só vai aparecer no retorno se falhar geral)
                resultados_erro.append(
                    {
                        "tentativa": idx,
                        "status": "NAO_ENCONTRADO_CONSUMIDOR_FINAL",
                        "cliente_usado": codigo_consumidor_final,
                        "data": nota.get("data"),
                        "valor": _normalize_valor_ptbr(nota.get("valor")),
                        "formaPgto": nota.get("codigoFormaPagamento"),
                        "filial": nota.get("filialEmpresaOrigem"),
                        "motivo": motivo2,
                        "no_data": bool(no_data2),
                    }
                )

                step(
                    "Não encontrou com cliente correto nem consumidor final. Indo para próxima tentativa.",
                    level="yellow",
                )
                await _voltar_para_tela_gera_nota(app)
                continue

            except Exception as e:
                # logs de erro
                step(f"ERRO na tentativa {idx}: {e}", level="red")
                resultados_erro.append(
                    {
                        "tentativa": idx,
                        "status": "ERRO",
                        "data": nota.get("data"),
                        "valor": _normalize_valor_ptbr(nota.get("valor")),
                        "formaPgto": nota.get("codigoFormaPagamento"),
                        "filial": nota.get("filialEmpresaOrigem"),
                        "erro": str(e),
                    }
                )
                await _voltar_para_tela_gera_nota(app)
                continue

        # RETORNO FINAL
        if resultados_sucesso:
            step("Processo concluído com sucesso (1 nota emitida).", level="green")
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=f"Emitida 1 nota (parou no primeiro sucesso). Tentativas={len(tentativas)}. Sucesso: {resultados_sucesso}",
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        step("Processo concluído sem emitir nota (falha).", level="red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Nenhuma nota foi emitida. Tentativas={len(tentativas)}. Erros/ocorrências: {resultados_erro}",
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
        )

    except Exception as erro:
        step(f"Erro geral emissao_nf_frota: {erro}", level="red")
        console.print(erro, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=str(erro),
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
