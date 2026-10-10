# -*- coding: utf-8 -*-

import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

import pyautogui
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.api.client import send_file

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
    worker_sleep,
    login_autosystem,
    kill_all_emsys,
)

console = Console()

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


# ============================================================
# CONFIGURAÇÕES DO AUTOSYSTEM
# ============================================================

CAMINHO_AUTOSYSTEM = Path(r"C:\AutoSystem\main.exe")

PASTA_DOWNLOADS = Path(r"C:\Users\automatehub\Downloads")

PASTA_AUTOSYSTEM = CAMINHO_AUTOSYSTEM.parent

NOME_PROCESSO_AUTOSYSTEM = "main.exe"
CLASSE_JANELA_AUTOSYSTEM = "gdkWindowToplevel"

TITULO_PRINCIPAL_REGEX = r".*(Linx Postos Gerencial|autosystem|AutoSystem).*"

TITULO_AVISO = "Aviso"
TITULO_MENSAGERIA = "Mensageria"
TITULO_QUESTAO_REGEX = r"^Quest.*"

# Janela exibida após clicar em Exportar Arquivo.
#
# O SWAPY pode exibir caracteres acentuados com codificação incorreta.
# Por isso, buscamos apenas pela parte estável "EFD ICMS/IPI".
TITULO_JANELA_EFD_REGEX = r".*EFD ICMS/IPI.*"

MAX_TENTATIVAS_JANELA = 30
INTERVALO_TENTATIVAS = 2

TIMEOUT_AVISO = 60
TIMEOUT_QUESTAO = 250
TIMEOUT_IMAGEM = 30
TIMEOUT_JANELA_EFD = 60
TIMEOUT_QUESTAO_POS_EXPORTACAO = 4.5 * 60 * 60

CONFIDENCE_PADRAO = 0.80

ASSETS_PATH = "assets\exportar_arquivo_autosystem"
# ASSETS_PATH = r"C:\Users\automatehub\Desktop\img_leo"

# ============================================================
# IMAGENS
# ============================================================

IMAGEM_BOTAO_NAO = Path(rf"{ASSETS_PATH}\btn_nao.png")

IMAGEM_NAO_EXIBIR = Path(rf"{ASSETS_PATH}\msg_nao_exibir.png")

IMAGEM_MENU_FINANCEIRO = Path(rf"{ASSETS_PATH}\menu_financeiro.png")

IMAGEM_MENU_FISCAL = Path(rf"{ASSETS_PATH}\menu_fiscal.png")

IMAGEM_MENU_INTEGRACOES_FISCAIS = Path(rf"{ASSETS_PATH}\menu_integracoes_fiscais.png")

IMAGEM_MENU_EFD_ICMS_IPI = Path(rf"{ASSETS_PATH}\menu_efd_icms_ipi.png")

IMAGEM_SELECIONAR_EXPORTAR_ARQUIVO = Path(
    rf"{ASSETS_PATH}\selecionar_exportar_arquivo.png"
)

IMAGEM_1601 = Path(rf"{ASSETS_PATH}\img_gerar_1601.png")

IMAGEM_BOTAO_EXPORTAR = Path(rf"{ASSETS_PATH}\btn_exportar.png")


# ============================================================
# RETORNOS
# ============================================================


def retorno_sucesso(
    mensagem: str,
) -> RpaRetornoProcessoDTO:
    return RpaRetornoProcessoDTO(
        sucesso=True,
        retorno=mensagem,
        status=RpaHistoricoStatusEnum.Sucesso,
    )


def retorno_falha_tecnica(
    mensagem: str,
) -> RpaRetornoProcessoDTO:
    return RpaRetornoProcessoDTO(
        sucesso=False,
        retorno=mensagem,
        status=RpaHistoricoStatusEnum.Falha,
        tags=[
            RpaTagDTO(
                descricao=RpaTagEnum.Tecnico,
            )
        ],
    )


# ============================================================
# LIMPAR ARQUIVOS TXT DA PASTA DOWNLOADS
# ============================================================


def limpar_arquivos_txt_downloads() -> Tuple[bool, str]:
    try:
        PASTA_DOWNLOADS.mkdir(parents=True, exist_ok=True)

        arquivos_txt = [
            arquivo for arquivo in PASTA_DOWNLOADS.glob("*.txt") if arquivo.is_file()
        ]

        for arquivo_txt in arquivos_txt:
            arquivo_txt.unlink()
            console.print(
                f"[DOWNLOADS] TXT antigo removido: {arquivo_txt.name}",
                style="bold yellow",
            )

        mensagem = (
            f"{len(arquivos_txt)} arquivo(s) TXT antigo(s) "
            "removido(s) da pasta Downloads."
        )

        console.print(
            f"[DOWNLOADS] {mensagem}",
            style="bold green",
        )

        return True, mensagem

    except Exception as error:
        mensagem = (
            "Erro ao limpar os arquivos TXT da pasta Downloads. "
            f"{type(error).__name__}: {error}"
        )

        logger.error(mensagem)
        console.print(mensagem, style="bold red")

        return False, mensagem


# ============================================================
# ENVIAR ARQUIVOS TXT PARA O BOF
# ============================================================


async def enviar_arquivos_txt_bof(
    historico_id: str,
    empresa: str,
) -> Tuple[bool, str]:
    try:
        historico_id = str(historico_id or "").strip()
        empresa = str(empresa or "").strip()

        if not historico_id:
            return False, "historico_id não informado."

        if not empresa:
            return False, "Número da empresa não informado."

        arquivos_txt = sorted(
            [arquivo for arquivo in PASTA_DOWNLOADS.glob("*.txt") if arquivo.is_file()],
            key=lambda arquivo: arquivo.stat().st_mtime,
        )

        if not arquivos_txt:
            return (
                False,
                "Nenhum arquivo TXT foi encontrado na pasta Downloads.",
            )

        enviados = []

        for indice, arquivo_txt in enumerate(arquivos_txt, start=1):
            nome_original = arquivo_txt.name
            prefixo_empresa = f"{empresa}_"

            # Evita duplicar o número da empresa caso o arquivo
            # já tenha sido renomeado anteriormente.
            if nome_original.startswith(prefixo_empresa):
                novo_nome = nome_original
            else:
                novo_nome = f"{prefixo_empresa}{nome_original}"

            novo_caminho = arquivo_txt.with_name(novo_nome)

            # Renomeia fisicamente o arquivo antes de enviar ao BOF.
            if novo_caminho != arquivo_txt:
                arquivo_txt.rename(novo_caminho)
                arquivo_txt = novo_caminho

                console.print(
                    (
                        f"[BOF] Arquivo renomeado: "
                        f"{nome_original} -> {arquivo_txt.name}"
                    ),
                    style="bold green",
                )

            console.print(
                (
                    f"[BOF] Enviando {indice}/{len(arquivos_txt)}: "
                    f"{arquivo_txt.name}"
                ),
                style="bold cyan",
            )

            file_bytes = arquivo_txt.read_bytes()

            if not file_bytes:
                console.print(
                    (
                        "[BOF] O arquivo está vazio, mas será enviado: "
                        f"{arquivo_txt.name}"
                    ),
                    style="bold yellow",
                )

            await send_file(
                historico_id,
                arquivo_txt.name,
                "txt",
                file_bytes,
                file_extension="txt",
            )

            enviados.append(arquivo_txt.name)

            arquivo_txt.unlink()

            console.print(
                ("[BOF] Arquivo enviado e removido da pasta: " f"{arquivo_txt.name}"),
                style="bold green",
            )

        mensagem = f"{len(enviados)} arquivo(s) TXT enviado(s) ao BOF: " + ", ".join(
            enviados
        )

        return True, mensagem

    except Exception as error:
        mensagem = (
            "Erro ao renomear ou enviar os arquivos TXT ao BOF. "
            f"{type(error).__name__}: {error}"
        )

        logger.error(mensagem)
        console.print(mensagem, style="bold red")

        return False, mensagem


# ============================================================
# VALIDAÇÃO DAS IMAGENS
# ============================================================


def validar_imagens_automacao() -> Tuple[bool, str]:
    imagens = {
        "Botão Não": IMAGEM_BOTAO_NAO,
        "Mensagem Não Exibir": IMAGEM_NAO_EXIBIR,
        "Menu Financeiro": IMAGEM_MENU_FINANCEIRO,
        "Menu Fiscal": IMAGEM_MENU_FISCAL,
        "Menu Integrações Fiscais": (IMAGEM_MENU_INTEGRACOES_FISCAIS),
        "Menu EFD ICMS/IPI": IMAGEM_MENU_EFD_ICMS_IPI,
        "Selecionar Exportar Arquivo": (IMAGEM_SELECIONAR_EXPORTAR_ARQUIVO),
        "Opção Gerar Registro 1601": IMAGEM_1601,
        "Botão Exportar": IMAGEM_BOTAO_EXPORTAR,
    }

    imagens_ausentes = []

    for descricao, caminho in imagens.items():
        if not caminho.is_file():
            imagens_ausentes.append(f"{descricao}: {caminho}")

    if imagens_ausentes:
        mensagem = "As seguintes imagens não foram encontradas:\n" + "\n".join(
            imagens_ausentes
        )
        return False, mensagem

    return True, "Todas as imagens foram encontradas."


# ============================================================
# LOCALIZAR JANELA PRINCIPAL
# ============================================================


async def localizar_janela_principal(
    pid_inicial: Optional[int] = None,
) -> Tuple[
    Optional[Application],
    Optional[Any],
]:
    console.print(
        "[AUTOSYSTEM] Aguardando janela principal...",
        style="bold cyan",
    )

    for tentativa in range(
        1,
        MAX_TENTATIVAS_JANELA + 1,
    ):
        if pid_inicial:
            try:
                app = Application(backend="win32").connect(
                    process=pid_inicial,
                    timeout=1,
                )

                janelas = app.windows(class_name=CLASSE_JANELA_AUTOSYSTEM)

                for janela in janelas:
                    try:
                        titulo = (janela.window_text() or "").lower()

                        titulo_compativel = (
                            "linx" in titulo
                            or "autosystem" in titulo
                            or "postos gerencial" in titulo
                        )

                        if (
                            janela.exists()
                            and janela.is_visible()
                            and titulo_compativel
                        ):
                            console.print(
                                (
                                    "[AUTOSYSTEM] Janela principal "
                                    f"encontrada pelo PID {pid_inicial}."
                                ),
                                style="bold green",
                            )

                            return app, janela

                    except Exception:
                        continue

            except Exception:
                pass

        try:
            app = Application(backend="win32").connect(
                class_name=CLASSE_JANELA_AUTOSYSTEM,
                title_re=TITULO_PRINCIPAL_REGEX,
                timeout=1,
            )

            janela = app.window(
                class_name=CLASSE_JANELA_AUTOSYSTEM,
                title_re=TITULO_PRINCIPAL_REGEX,
            )

            if janela.exists() and janela.is_visible():
                console.print(
                    "[AUTOSYSTEM] Janela principal encontrada.",
                    style="bold green",
                )

                return app, janela

        except Exception:
            pass

        console.print(
            (
                "[AUTOSYSTEM] Janela ainda não encontrada. "
                f"Tentativa {tentativa}/"
                f"{MAX_TENTATIVAS_JANELA}..."
            ),
            style="bold yellow",
        )

        await worker_sleep(INTERVALO_TENTATIVAS)

    return None, None


# ============================================================
# ABRIR AUTOSYSTEM
# ============================================================


async def open_autosystem_processes() -> Tuple[
    Optional[Application],
    Optional[Any],
]:
    try:
        fechou = await kill_all_emsys()

        if not fechou:
            raise RuntimeError("Não foi possível fechar o AutoSystem anterior.")

        if not CAMINHO_AUTOSYSTEM.is_file():
            raise FileNotFoundError(
                ("Executável do AutoSystem não encontrado: " f"{CAMINHO_AUTOSYSTEM}")
            )

        console.print(
            ("[AUTOSYSTEM] Abrindo sistema: " f"{CAMINHO_AUTOSYSTEM}"),
            style="bold cyan",
        )

        processo = subprocess.Popen(
            [str(CAMINHO_AUTOSYSTEM)],
            cwd=str(PASTA_AUTOSYSTEM),
            shell=False,
        )

        console.print(
            ("[AUTOSYSTEM] Processo iniciado. " f"PID: {processo.pid}"),
            style="bold green",
        )

        await worker_sleep(2)

        if processo.poll() is not None:
            raise RuntimeError(
                (
                    "O AutoSystem encerrou imediatamente. "
                    f"Código: {processo.returncode}"
                )
            )

        app, main_window = await localizar_janela_principal(
            pid_inicial=processo.pid,
        )

        if app is None or main_window is None:
            raise RuntimeError("A janela principal não foi encontrada.")

        try:
            main_window.restore()
        except Exception:
            pass

        try:
            main_window.set_focus()
        except Exception:
            try:
                main_window.click_input()
            except Exception:
                pass

        console.print(
            ("[AUTOSYSTEM] AutoSystem aberto. " f"Título: {main_window.window_text()}"),
            style="bold green",
        )

        return app, main_window

    except Exception as error:
        mensagem = (
            "[AUTOSYSTEM][ERRO] Falha ao abrir o sistema. "
            f"{type(error).__name__}: {error}"
        )

        logger.error(mensagem)

        console.print(
            mensagem,
            style="bold red",
        )

        return None, None


# ============================================================
# AGUARDAR JANELA GTK
# ============================================================


async def aguardar_janela_gtk(
    title: Optional[str] = None,
    title_re: Optional[str] = None,
    timeout: int = 60,
) -> Tuple[
    Optional[Application],
    Optional[Any],
]:
    tempo_decorrido = 0
    intervalo = 1

    while tempo_decorrido < timeout:
        try:
            argumentos = {
                "class_name": CLASSE_JANELA_AUTOSYSTEM,
            }

            if title is not None:
                argumentos["title"] = title

            if title_re is not None:
                argumentos["title_re"] = title_re

            app = Application(backend="win32").connect(
                timeout=1,
                **argumentos,
            )

            janela = app.window(
                **argumentos,
            )

            if janela.exists() and janela.is_visible():
                return app, janela

        except Exception:
            pass

        await worker_sleep(intervalo)
        tempo_decorrido += intervalo

    return None, None


# ============================================================
# LOCALIZAR E CLICAR EM IMAGEM
# ============================================================


async def clicar_imagem_na_tela(
    caminho_imagem: str | Path,
    descricao: str,
    timeout: int = TIMEOUT_IMAGEM,
    confidence: float = CONFIDENCE_PADRAO,
    intervalo: float = 1,
    region: Optional[tuple[int, int, int, int]] = None,
    quantidade_cliques: int = 1,
) -> bool:
    caminho_imagem = Path(caminho_imagem)

    if not caminho_imagem.is_file():
        console.print(
            (
                f"[IMAGEM][ERRO] Imagem '{descricao}' "
                f"não encontrada: {caminho_imagem}"
            ),
            style="bold red",
        )
        return False

    console.print(
        (f"[IMAGEM] Procurando '{descricao}': " f"{caminho_imagem}"),
        style="bold cyan",
    )

    tempo_decorrido = 0.0

    while tempo_decorrido < timeout:
        try:
            posicao = pyautogui.locateCenterOnScreen(
                str(caminho_imagem),
                confidence=confidence,
                region=region,
                grayscale=False,
            )

            if posicao:
                console.print(
                    (
                        f"[IMAGEM] '{descricao}' encontrada. "
                        f"x={posicao.x}, y={posicao.y}"
                    ),
                    style="bold green",
                )

                pyautogui.moveTo(
                    posicao.x,
                    posicao.y,
                    duration=0.2,
                )

                await worker_sleep(3)

                pyautogui.click(
                    x=posicao.x,
                    y=posicao.y,
                    clicks=quantidade_cliques,
                    interval=0.15,
                )

                await worker_sleep(1)

                return True

        except pyautogui.ImageNotFoundException:
            # A imagem ainda não apareceu nesta tentativa.
            # Não encerra a função: continua procurando até o timeout.
            pass

        except Exception as error:
            console.print(
                (
                    f"[IMAGEM][ERRO] Erro inesperado ao procurar "
                    f"'{descricao}': "
                    f"{type(error).__name__}: {error}"
                ),
                style="bold red",
            )
            return False

        console.print(
            (
                f"[IMAGEM] '{descricao}' ainda não encontrada. "
                f"Tempo: {tempo_decorrido:.0f}/{timeout}s"
            ),
            style="bold yellow",
        )

        await worker_sleep(intervalo)
        tempo_decorrido += intervalo

    console.print(
        (f"[IMAGEM][ERRO] '{descricao}' não encontrada " f"em até {timeout} segundos."),
        style="bold red",
    )

    return False


# ============================================================
# VERIFICAR SE UMA IMAGEM EXISTE NA TELA
# ============================================================


async def imagem_existe_na_tela(
    caminho_imagem: str | Path,
    descricao: str,
    timeout: int = 5,
    confidence: float = CONFIDENCE_PADRAO,
    intervalo: float = 1,
    region: Optional[tuple[int, int, int, int]] = None,
) -> bool:
    caminho_imagem = Path(caminho_imagem)

    if not caminho_imagem.is_file():
        console.print(
            (
                f"[IMAGEM][ERRO] Imagem '{descricao}' "
                f"não encontrada no disco: {caminho_imagem}"
            ),
            style="bold red",
        )
        return False

    console.print(
        f"[IMAGEM] Verificando se '{descricao}' existe na tela...",
        style="bold cyan",
    )

    tempo_decorrido = 0.0

    while tempo_decorrido < timeout:
        try:
            posicao = pyautogui.locateCenterOnScreen(
                str(caminho_imagem),
                confidence=confidence,
                region=region,
                grayscale=False,
            )

            if posicao:
                console.print(
                    (
                        f"[IMAGEM] '{descricao}' encontrada. "
                        f"x={posicao.x}, y={posicao.y}"
                    ),
                    style="bold green",
                )
                return True

        except pyautogui.ImageNotFoundException:
            # A imagem não foi encontrada nesta tentativa.
            # Continua verificando até atingir o timeout.
            pass

        except Exception as error:
            console.print(
                (
                    f"[IMAGEM][ERRO] Erro inesperado ao verificar "
                    f"'{descricao}': "
                    f"{type(error).__name__}: {error}"
                ),
                style="bold red",
            )
            return False

        await worker_sleep(intervalo)
        tempo_decorrido += intervalo

    console.print(
        (
            f"[IMAGEM] '{descricao}' não apareceu. "
            "O processo seguirá sem alterar a opção."
        ),
        style="bold yellow",
    )

    return False


# ============================================================
# FECHAR AVISO
# ============================================================


async def aguardar_e_fechar_aviso_autosystem(
    timeout: int = TIMEOUT_AVISO,
) -> bool:
    console.print(
        "[AUTOSYSTEM] Aguardando janela 'Aviso'...",
        style="bold cyan",
    )

    app_aviso, janela_aviso = await aguardar_janela_gtk(
        title=TITULO_AVISO,
        timeout=timeout,
    )

    if app_aviso is None or janela_aviso is None:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] A janela 'Aviso' "
                f"não apareceu em até {timeout} segundos."
            ),
            style="bold red",
        )
        return False

    console.print(
        "[AUTOSYSTEM] Janela 'Aviso' encontrada.",
        style="bold green",
    )

    try:
        janela_aviso.restore()
    except Exception:
        pass

    try:
        janela_aviso.set_focus()
    except Exception:
        try:
            janela_aviso.click_input()
        except Exception:
            pass

    await worker_sleep(1)

    pyautogui.press("enter")

    await worker_sleep(5)

    try:
        ainda_aberta = janela_aviso.exists() and janela_aviso.is_visible()
    except Exception:
        ainda_aberta = False

    if ainda_aberta:
        console.print(
            "[AUTOSYSTEM] ENTER não fechou. Tentando ESC...",
            style="bold yellow",
        )

        pyautogui.press("esc")
        await worker_sleep(2)

        try:
            ainda_aberta = janela_aviso.exists() and janela_aviso.is_visible()
        except Exception:
            ainda_aberta = False

    if ainda_aberta:
        pyautogui.press("esc")
        await worker_sleep(2)
        console.print(
            "[AUTOSYSTEM][ERRO] A janela Aviso continuou aberta. Pressionando ESC",
            style="bold red",
        )
        try:
            ainda_aberta = janela_aviso.exists() and janela_aviso.is_visible()
        except Exception:
            ainda_aberta = False
        if ainda_aberta:
            console.print(
                "[AUTOSYSTEM][ERRO] A janela Aviso continuou aberta.",
                style="bold red",
            )
            return False

    console.print(
        "[AUTOSYSTEM] Janela Aviso fechada.",
        style="bold green",
    )

    return True


# ============================================================
# TRATAR JANELA MENSAGERIA, SE EXISTIR
# ============================================================


async def fechar_janela_mensageria_se_existir(
    timeout: int = 10,
) -> bool:
    """
    Verifica se a janela Mensageria aparece.

    Se existir:
    1. Clica na imagem msg_nao_exibir.png.
    2. Pressiona ESC.
    3. Confirma que a janela foi fechada.

    Se não existir, segue normalmente.
    """
    console.print(
        "[AUTOSYSTEM] Verificando se a janela Mensageria apareceu...",
        style="bold cyan",
    )

    app_mensageria, janela_mensageria = await aguardar_janela_gtk(
        title=TITULO_MENSAGERIA,
        timeout=timeout,
    )

    if app_mensageria is None or janela_mensageria is None:
        console.print(
            (
                "[AUTOSYSTEM] Janela Mensageria não encontrada. "
                "O processo seguirá normalmente."
            ),
            style="bold yellow",
        )
        return True

    console.print(
        (
            "[AUTOSYSTEM] Janela Mensageria encontrada. "
            "Procurando a opção Não Exibir..."
        ),
        style="bold green",
    )

    try:
        janela_mensageria.restore()
    except Exception:
        pass

    try:
        janela_mensageria.set_focus()
    except Exception:
        try:
            janela_mensageria.click_input()
        except Exception:
            pass

    await worker_sleep(1)

    try:
        retangulo = janela_mensageria.rectangle()

        regiao_mensageria = (
            retangulo.left,
            retangulo.top,
            retangulo.width(),
            retangulo.height(),
        )
    except Exception as error:
        console.print(
            (
                "[AUTOSYSTEM] Não foi possível limitar a busca "
                f"à janela Mensageria: {error}. "
                "A busca será feita na tela inteira."
            ),
            style="bold yellow",
        )
        regiao_mensageria = None

    clicou_nao_exibir = await clicar_imagem_na_tela(
        caminho_imagem=IMAGEM_NAO_EXIBIR,
        descricao="Mensagem Não Exibir",
        timeout=20,
        confidence=0.70,
        intervalo=1,
        region=regiao_mensageria,
    )

    # Segunda tentativa na tela inteira, caso o retângulo retornado
    # pela janela GTK não cubra corretamente a imagem.
    if not clicou_nao_exibir:
        console.print(
            (
                "[AUTOSYSTEM] A imagem Não Exibir não foi localizada "
                "dentro da região da janela. Tentando na tela inteira..."
            ),
            style="bold yellow",
        )

        clicou_nao_exibir = await clicar_imagem_na_tela(
            caminho_imagem=IMAGEM_NAO_EXIBIR,
            descricao="Mensagem Não Exibir - tela inteira",
            timeout=10,
            confidence=0.70,
            intervalo=1,
            region=None,
        )

    if not clicou_nao_exibir:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] A janela Mensageria existe, "
                "mas não foi possível clicar na imagem Não Exibir."
            ),
            style="bold red",
        )
        return False

    console.print(
        (
            "[AUTOSYSTEM] Opção Não Exibir clicada. "
            "Pressionando ESC para fechar a janela Mensageria..."
        ),
        style="bold cyan",
    )

    await worker_sleep(1)
    pyautogui.press("esc")
    await worker_sleep(2)

    try:
        ainda_aberta = janela_mensageria.exists() and janela_mensageria.is_visible()
    except Exception:
        ainda_aberta = False

    if ainda_aberta:
        console.print(
            (
                "[AUTOSYSTEM] A janela Mensageria continuou aberta. "
                "Pressionando ESC novamente..."
            ),
            style="bold yellow",
        )

        try:
            janela_mensageria.set_focus()
        except Exception:
            pass

        pyautogui.press("esc")
        await worker_sleep(2)

        try:
            ainda_aberta = janela_mensageria.exists() and janela_mensageria.is_visible()
        except Exception:
            ainda_aberta = False

    if ainda_aberta:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] A imagem Não Exibir foi clicada, "
                "mas a janela Mensageria não fechou após pressionar ESC."
            ),
            style="bold red",
        )
        return False

    console.print(
        (
            "[AUTOSYSTEM] Opção Não Exibir selecionada e "
            "janela Mensageria fechada com sucesso."
        ),
        style="bold green",
    )

    return True


# ============================================================
# RESPONDER NÃO NA JANELA QUESTÃO
# ============================================================


async def aguardar_e_responder_nao_questao(
    timeout: int = TIMEOUT_QUESTAO,
) -> bool:
    console.print(
        "[AUTOSYSTEM] Aguardando janela de questão...",
        style="bold cyan",
    )

    app_questao, janela_questao = await aguardar_janela_gtk(
        title_re=TITULO_QUESTAO_REGEX,
        timeout=timeout,
    )

    if app_questao is None or janela_questao is None:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] A janela de questão "
                f"não apareceu em até {timeout} segundos."
            ),
            style="bold red",
        )
        return False

    try:
        titulo = janela_questao.window_text()
    except Exception:
        titulo = ""

    console.print(
        ("[AUTOSYSTEM] Janela de questão encontrada. " f"Título: {titulo}"),
        style="bold green",
    )

    try:
        janela_questao.restore()
    except Exception:
        pass

    try:
        janela_questao.set_focus()
    except Exception:
        try:
            janela_questao.click_input()
        except Exception:
            pass

    await worker_sleep(1)

    try:
        retangulo = janela_questao.rectangle()

        regiao_questao = (
            retangulo.left,
            retangulo.top,
            retangulo.width(),
            retangulo.height(),
        )

    except Exception:
        regiao_questao = None

    clicou = await clicar_imagem_na_tela(
        caminho_imagem=IMAGEM_BOTAO_NAO,
        descricao="Botão Não",
        timeout=240,
        confidence=0.80,
        intervalo=1,
        region=regiao_questao,
    )

    if not clicou:
        return False

    await worker_sleep(3)

    try:
        ainda_aberta = janela_questao.exists() and janela_questao.is_visible()
    except Exception:
        ainda_aberta = False

    if ainda_aberta:
        pyautogui.press("esc")
        await worker_sleep(2)
        console.print(
            (
                "[AUTOSYSTEM][ERRO] O botão Não foi clicado, "
                "mas a janela continuou aberta. Pressionando ESC"
            ),
            style="bold red",
        )

        try:
            ainda_aberta = janela_questao.exists() and janela_questao.is_visible()
        except Exception:
            ainda_aberta = False
        return False

    console.print(
        "[AUTOSYSTEM] Botão Não clicado com sucesso.",
        style="bold green",
    )

    return True


# ============================================================
# SEQUÊNCIA DE MENUS
# ============================================================


async def clicar_sequencia_menus_autosystem() -> bool:
    console.print(
        "[AUTOSYSTEM] Iniciando busca via Ctrl+F...",
        style="bold cyan",
    )

    # 1. Clica no menu principal (Financeiro) para garantir foco na janela do AutoSystem
    clicou = await clicar_imagem_na_tela(
        caminho_imagem=IMAGEM_MENU_FINANCEIRO,
        descricao="Focar AutoSystem",
        timeout=30,
        confidence=0.80,
        intervalo=1,
        region=None,
    )

    if not clicou:
        console.print(
            "[AUTOSYSTEM][ERRO] Falha ao focar a janela do AutoSystem.",
            style="bold red",
        )
        return False

    # Fecha o menu suspenso aberto pelo clique para permitir o atalho Ctrl+F
    pyautogui.press("esc")
    await worker_sleep(0.5)

    # 2. Aciona o campo de busca (Ctrl + F)
    pyautogui.hotkey("ctrl", "f")
    await worker_sleep(0.8)

    # 3. Digita o texto de pesquisa
    pyautogui.typewrite("Exportar Arquivo", interval=0.08)
    await worker_sleep(0.5)

    # 4. Navega e seleciona
    pyautogui.press("down", presses=5, interval=0.15)
    await worker_sleep(0.3)
    pyautogui.press("enter")

    console.print(
        "[AUTOSYSTEM] Opção 'Exportar Arquivo' selecionada com sucesso.",
        style="bold green",
    )

    return True


# ============================================================
# AGUARDAR JANELA EFD E PREENCHER EMPRESA
# ============================================================


async def aguardar_e_preencher_empresa_efd(
    empresa: str,
    periodo_inicial: str,
    periodo_final: str,
    timeout: int = TIMEOUT_JANELA_EFD,
) -> bool:
    """
    Aguarda a janela EFD ICMS/IPI e preenche, na sequência:

    1. Empresa
    2. TAB
    3. Período inicial
    4. TAB
    5. Período final
    6. TAB
    7. Limpa o campo atual
    8. Digita B
    9. Pressiona TAB 3 vezes
    10. Digita o caminho C:\\Users\\automatehub\\Downloads
    11. Verifica se a opção do registro 1601 aparece
    12. Se aparecer, pressiona TAB 6 vezes e ESPAÇO para desmarcar
    13. Verifica se a imagem desapareceu
    14. Se ainda existir, pressiona ESPAÇO novamente e verifica de novo
    15. Somente quando a imagem não existir, clica no botão Exportar
    16. Aguarda até 4 horas a janela Questão
    17. Clica no botão Não usando a mesma imagem do início
    """

    empresa = str(empresa or "").strip()
    periodo_inicial = str(periodo_inicial or "").strip()
    periodo_final = str(periodo_final or "").strip()

    if not empresa:
        console.print(
            "[AUTOSYSTEM][ERRO] Empresa não informada.",
            style="bold red",
        )
        return False

    if not periodo_inicial:
        console.print(
            "[AUTOSYSTEM][ERRO] Período inicial não informado.",
            style="bold red",
        )
        return False

    if not periodo_final:
        console.print(
            "[AUTOSYSTEM][ERRO] Período final não informado.",
            style="bold red",
        )
        return False

    console.print(
        "[AUTOSYSTEM] Aguardando janela 'Integração EFD ICMS/IPI'...",
        style="bold cyan",
    )

    app_efd, janela_efd = await aguardar_janela_gtk(
        title_re=TITULO_JANELA_EFD_REGEX,
        timeout=timeout,
    )

    if app_efd is None or janela_efd is None:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] A janela EFD ICMS/IPI "
                f"não apareceu em até {timeout} segundos."
            ),
            style="bold red",
        )
        return False

    try:
        titulo = janela_efd.window_text() or ""
    except Exception:
        titulo = ""

    console.print(
        f"[AUTOSYSTEM] Janela EFD encontrada. Título: {titulo}",
        style="bold green",
    )

    try:
        janela_efd.restore()
    except Exception:
        pass

    try:
        janela_efd.set_focus()
    except Exception:
        try:
            janela_efd.click_input()
        except Exception:
            pass

    await worker_sleep(2)

    # ========================================================
    # EMPRESA
    # ========================================================

    console.print(
        f"[AUTOSYSTEM] Preenchendo empresa: {empresa}",
        style="bold cyan",
    )

    pyautogui.hotkey("ctrl", "a")
    await worker_sleep(0.3)

    pyautogui.press("backspace")
    await worker_sleep(0.3)

    pyautogui.write(
        empresa,
        interval=0.08,
    )

    await worker_sleep(0.5)

    # Vai para o período inicial.
    pyautogui.press("tab")
    await worker_sleep(0.5)

    # ========================================================
    # DATA INICIAL
    # ========================================================

    console.print(
        f"[AUTOSYSTEM] Preenchendo data inicial: {periodo_inicial}",
        style="bold cyan",
    )

    pyautogui.hotkey("ctrl", "a")
    await worker_sleep(0.3)

    pyautogui.press("backspace")
    await worker_sleep(0.3)

    pyautogui.write(
        periodo_inicial,
        interval=0.08,
    )

    await worker_sleep(0.5)

    # Vai para o período final.
    pyautogui.press("tab")
    await worker_sleep(0.5)

    # ========================================================
    # DATA FINAL
    # ========================================================

    console.print(
        f"[AUTOSYSTEM] Preenchendo data final: {periodo_final}",
        style="bold cyan",
    )

    pyautogui.hotkey("ctrl", "a")
    await worker_sleep(0.3)

    pyautogui.press("backspace")
    await worker_sleep(0.3)

    pyautogui.write(
        periodo_final,
        interval=0.08,
    )

    await worker_sleep(0.5)

    # Vai para o próximo campo.
    pyautogui.press("tab")
    await worker_sleep(0.5)

    pyautogui.press("tab")
    await worker_sleep(0.5)

    pyautogui.press("enter")
    await worker_sleep(0.5)

    pyautogui.press("down", presses=2)
    await worker_sleep(0.5)

    pyautogui.press("enter")
    await worker_sleep(0.5)

    # ========================================================
    # CAMINHO DE EXPORTAÇÃO
    # Após digitar B, avança 3 campos e informa a pasta.
    # ========================================================

    caminho_exportacao = r"C:\Users\automatehub\Downloads"

    console.print(
        (
            "[AUTOSYSTEM] Após digitar B, pressionando TAB 3 vezes "
            "e preenchendo o caminho de exportação: "
            f"{caminho_exportacao}"
        ),
        style="bold cyan",
    )

    pyautogui.press(
        "tab",
        presses=3,
        interval=0.3,
    )

    await worker_sleep(0.5)

    pyautogui.hotkey("ctrl", "a")
    await worker_sleep(0.3)

    pyautogui.press("backspace")
    await worker_sleep(0.3)

    pyautogui.write(
        caminho_exportacao,
        interval=0.03,
    )

    await worker_sleep(1)

    try:
        retangulo_efd = janela_efd.rectangle()

        regiao_janela_efd = (
            retangulo_efd.left,
            retangulo_efd.top,
            retangulo_efd.width(),
            retangulo_efd.height(),
        )

    except Exception as error:
        console.print(
            (
                "[AUTOSYSTEM] Não foi possível limitar a busca "
                f"à janela EFD: {error}. "
                "A busca será feita na tela inteira."
            ),
            style="bold yellow",
        )

        regiao_janela_efd = None

    # ========================================================
    # DESMARCAR OPÇÃO DO REGISTRO 1601, SE ELA EXISTIR
    # ========================================================
    await worker_sleep(3)
    existe_opcao_1601 = await imagem_existe_na_tela(
        caminho_imagem=IMAGEM_1601,
        descricao="Opção Gerar Registro 1601",
        timeout=5,
        confidence=CONFIDENCE_PADRAO,
        intervalo=1,
        region=regiao_janela_efd,
    )

    if existe_opcao_1601:
        console.print(
            (
                "[AUTOSYSTEM] Opção do registro 1601 encontrada. "
                "Pressionando TAB 6 vezes e ESPAÇO para desmarcar."
            ),
            style="bold cyan",
        )

        pyautogui.press(
            "tab",
            presses=6,
            interval=0.3,
        )

        await worker_sleep(2)

        pyautogui.press("space")

        await worker_sleep(2)

        console.print(
            (
                "[AUTOSYSTEM] Validando se a opção do registro 1601 "
                "foi desmarcada após a primeira tentativa..."
            ),
            style="bold cyan",
        )

        opcao_1601_ainda_marcada = await imagem_existe_na_tela(
            caminho_imagem=IMAGEM_1601,
            descricao="Opção Gerar Registro 1601 após primeira tentativa",
            timeout=3,
            confidence=CONFIDENCE_PADRAO,
            intervalo=1,
            region=regiao_janela_efd,
        )

        if opcao_1601_ainda_marcada:
            console.print(
                (
                    "[AUTOSYSTEM] A opção do registro 1601 ainda está "
                    "marcada. Pressionando ESPAÇO novamente."
                ),
                style="bold yellow",
            )

            pyautogui.press("space")

            await worker_sleep(2)

            console.print(
                (
                    "[AUTOSYSTEM] Validando novamente se a opção "
                    "do registro 1601 foi desmarcada..."
                ),
                style="bold cyan",
            )

            opcao_1601_ainda_marcada = await imagem_existe_na_tela(
                caminho_imagem=IMAGEM_1601,
                descricao="Opção Gerar Registro 1601 após segunda tentativa",
                timeout=3,
                confidence=CONFIDENCE_PADRAO,
                intervalo=1,
                region=regiao_janela_efd,
            )

            if opcao_1601_ainda_marcada:
                console.print(
                    (
                        "[AUTOSYSTEM][ERRO] Não foi possível desmarcar "
                        "a opção do registro 1601 após duas tentativas. "
                        "O botão Exportar não será clicado."
                    ),
                    style="bold red",
                )
                return False

        console.print(
            ("[AUTOSYSTEM] Opção do registro 1601 confirmada " "como desmarcada."),
            style="bold green",
        )
    else:
        console.print(
            (
                "[AUTOSYSTEM] Opção do registro 1601 não encontrada. "
                "Seguindo diretamente para o botão Exportar."
            ),
            style="bold yellow",
        )

    console.print(
        (
            "[AUTOSYSTEM] A imagem do registro 1601 não está visível. "
            "Procurando o botão Exportar..."
        ),
        style="bold cyan",
    )

    clicou_exportar = await clicar_imagem_na_tela(
        caminho_imagem=IMAGEM_BOTAO_EXPORTAR,
        descricao="Botão Exportar",
        timeout=TIMEOUT_IMAGEM,
        confidence=CONFIDENCE_PADRAO,
        intervalo=1,
        region=regiao_janela_efd,
    )

    if not clicou_exportar:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] Os campos foram preenchidos, "
                "mas não foi possível localizar ou clicar "
                "no botão Exportar."
            ),
            style="bold red",
        )

        return False

    await worker_sleep(3)

    console.print(
        (
            "[AUTOSYSTEM] Botão Exportar clicado. "
            "Aguardando a janela de questão final por até "
            f"{TIMEOUT_QUESTAO_POS_EXPORTACAO // 60} minutos..."
        ),
        style="bold cyan",
    )

    respondeu_nao_final = await aguardar_e_responder_nao_questao(
        timeout=TIMEOUT_QUESTAO_POS_EXPORTACAO,
    )

    if not respondeu_nao_final:
        console.print(
            (
                "[AUTOSYSTEM][ERRO] O botão Exportar foi clicado, "
                "mas a janela de questão final não apareceu dentro "
                f"de {TIMEOUT_QUESTAO_POS_EXPORTACAO // 3600} horas "
                "ou não foi possível clicar no botão Não."
            ),
            style="bold red",
        )

        return False

    console.print(
        (
            "[AUTOSYSTEM] Campos preenchidos, botão Exportar clicado "
            "e confirmação final respondida com Não. "
            f"Empresa: {empresa} | "
            f"Data inicial: {periodo_inicial} | "
            f"Data final: {periodo_final} | "
            "Campo seguinte: B | "
            "Caminho de exportação: "
            r"C:\Users\automatehub\Downloads"
        ),
        style="bold green",
    )

    return True


# ============================================================
# LOGIN E NAVEGAÇÃO
# ============================================================


async def executar_login_e_navegacao(
    main_window,
    empresa: str,
    periodo_inicial: str,
    periodo_final: str,
    historico_id: str,
) -> RpaRetornoProcessoDTO:
    try:
        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        await login_autosystem(
            main_window=main_window,
        )

        # ----------------------------------------------------
        # AVISO
        # ----------------------------------------------------

        aviso_fechado = await aguardar_e_fechar_aviso_autosystem(
            timeout=TIMEOUT_AVISO,
        )

        if not aviso_fechado:
            return retorno_falha_tecnica(
                "O login foi enviado, mas não foi possível " "fechar a janela Aviso."
            )

        # ----------------------------------------------------
        # QUESTÃO - BOTÃO NÃO
        # ----------------------------------------------------

        respondeu_nao = await aguardar_e_responder_nao_questao(
            timeout=TIMEOUT_QUESTAO,
        )

        # if not respondeu_nao:
        #    return retorno_falha_tecnica(
        #        "Não foi possível clicar no botão Não " "da janela de questão."
        #    )

        # ----------------------------------------------------
        # MENSAGERIA
        # Após o primeiro botão Não, verifica se a janela
        # Mensageria apareceu e fecha antes de continuar.
        # ----------------------------------------------------

        mensageria_fechada = await fechar_janela_mensageria_se_existir(
            timeout=10,
        )

        if not mensageria_fechada:
            return retorno_falha_tecnica(
                "O primeiro botão Não foi clicado, mas não foi "
                "possível fechar a janela Mensageria."
            )

        await worker_sleep(5)

        # ----------------------------------------------------
        # SEQUÊNCIA DOS MENUS
        # ----------------------------------------------------

        menus_clicados = await clicar_sequencia_menus_autosystem()

        if not menus_clicados:
            return retorno_falha_tecnica(
                "O login foi realizado, mas ocorreu uma falha "
                "na sequência de menus do AutoSystem."
            )

        # ----------------------------------------------------
        # JANELA EFD
        # ----------------------------------------------------

        empresa_preenchida = await aguardar_e_preencher_empresa_efd(
            empresa=empresa,
            periodo_inicial=periodo_inicial,
            periodo_final=periodo_final,
            timeout=TIMEOUT_JANELA_EFD,
        )

        if not empresa_preenchida:
            return retorno_falha_tecnica(
                "Os menus foram acessados, mas não foi possível "
                "localizar a janela EFD ICMS/IPI ou preencher "
                f"a empresa {empresa}, o período inicial "
                f"{periodo_inicial} e o período final {periodo_final}."
            )

        console.print(
            "[BOF] Enviando os arquivos TXT gerados...",
            style="bold cyan",
        )

        enviou_txt, mensagem_envio = await enviar_arquivos_txt_bof(
            historico_id=historico_id,
            empresa=empresa,
        )

        if not enviou_txt:
            return retorno_falha_tecnica(mensagem_envio)

        return retorno_sucesso(
            "Login realizado, exportação concluída e arquivos TXT "
            f"enviados ao BOF. {mensagem_envio}"
        )

    except Exception as error:
        mensagem = (
            "[AUTOSYSTEM][ERRO] Falha durante o login "
            "ou navegação. "
            f"{type(error).__name__}: {error}"
        )

        logger.error(mensagem)

        console.print(
            mensagem,
            style="bold red",
        )

        return retorno_falha_tecnica(mensagem)


# ============================================================
# PROCESSO PRINCIPAL
# ============================================================


async def exportacao_arquivo_efd_icms_as(
    task: RpaProcessoEntradaDTO,
) -> RpaRetornoProcessoDTO:
    try:
        console.print(
            "[PROCESSO] Iniciando processo no AutoSystem...",
            style="bold cyan",
        )

        console.print(task)

        config_entrada = (
            getattr(
                task,
                "configEntrada",
                {},
            )
            or {}
        )

        empresa = config_entrada.get("empresa")

        periodo_inicial = config_entrada.get("periodoInicial")

        periodo_final = config_entrada.get("periodoFinal")

        if not empresa:
            return retorno_falha_tecnica(
                ("Campo 'empresa' não informado " "em configEntrada.")
            )

        if not periodo_inicial:
            return retorno_falha_tecnica(
                ("Campo 'periodoInicial' não informado " "em configEntrada.")
            )

        if not periodo_final:
            return retorno_falha_tecnica(
                ("Campo 'periodoFinal' não informado " "em configEntrada.")
            )

        limpou_downloads, mensagem_limpeza = limpar_arquivos_txt_downloads()

        if not limpou_downloads:
            return retorno_falha_tecnica(mensagem_limpeza)

        imagens_validas, mensagem_imagens = validar_imagens_automacao()

        if not imagens_validas:
            return retorno_falha_tecnica(mensagem_imagens)

        console.print(
            "[PROCESSO] Todas as imagens foram encontradas.",
            style="bold green",
        )

        console.print(
            f"[PROCESSO] Empresa: {empresa}",
            style="bold cyan",
        )

        console.print(
            ("[PROCESSO] Período: " f"{periodo_inicial} até {periodo_final}"),
            style="bold cyan",
        )

        app, main_window = await open_autosystem_processes()

        if app is None or main_window is None:
            return retorno_falha_tecnica(
                ("Não foi possível abrir ou conectar " "no AutoSystem.")
            )

        resultado_login = await executar_login_e_navegacao(
            main_window=main_window,
            empresa=str(empresa),
            periodo_inicial=str(periodo_inicial),
            periodo_final=str(periodo_final),
            historico_id=str(task.historico_id),
        )

        return resultado_login

    except Exception as error:
        retorno = (
            "[PROCESSO][ERRO] Falha no processo AutoSystem. "
            f"{type(error).__name__}: {error}"
        )

        logger.error(retorno)

        console.print(
            retorno,
            style="bold red",
        )

        return retorno_falha_tecnica(retorno)
