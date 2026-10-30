# -*- coding: utf-8 -*-
import asyncio
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional
import pyautogui
from pywinauto.application import Application
from rich.console import Console
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
# Mantém o mecanismo de segurança padrão do PyAutoGUI.
pyautogui.FAILSAFE = True

CAMINHO_AUTOSYSTEM = Path(r"C:\AutoSystem\main.exe")
# ASSETS_PATH = Path(r"C:\Users\automatehub\Desktop\img_leo")
ASSETS_PATH = Path("assets/lancamento_produtos_as")
IMAGEM_BOTAO_NAO = ASSETS_PATH / "btn_nao.png"
IMAGEM_NAO_EXIBIR = ASSETS_PATH / "msg_nao_exibir.png"
CLASSE_JANELA = "gdkWindowToplevel"
TIMEOUT_JANELA_PRINCIPAL = 90
TIMEOUT_AVISO = 60
TIMEOUT_QUESTAO = 250
TIMEOUT_LANCAMENTO_PRODUTOS = 90
IMAGEM_PRODUTO = ASSETS_PATH / "btn_produto.png"
IMAGEM_BOTAO_NOVO = ASSETS_PATH / "btn_novo.png"
IMAGENS_OPERACOES = {
    "E": ("Entrada", ASSETS_PATH / "operacao_entrada.png"),
    "C": ("Consumo", ASSETS_PATH / "operacao_consumo.png"),
    "P": ("Perda", ASSETS_PATH / "operacao_perda.png"),
    "S": ("Sobra", ASSETS_PATH / "operacao_sobra.png"),
    "I": ("Inventário", ASSETS_PATH / "operacao_inventario.png"),
    "A": ("Aferição", ASSETS_PATH / "operacao_afericao.png"),
    "B": ("Brinde", ASSETS_PATH / "operacao_brinde.png"),
    "DC": ("Devolução do Cliente", ASSETS_PATH / "operacao_devolucao_cliente.png"),
}


def retorno_sucesso(mensagem: str) -> RpaRetornoProcessoDTO:
    return RpaRetornoProcessoDTO(
        sucesso=True, retorno=mensagem, status=RpaHistoricoStatusEnum.Sucesso
    )


def retorno_falha_tecnica(mensagem: str) -> RpaRetornoProcessoDTO:
    console.print(f"[ERRO] {mensagem}", style="bold red")
    return RpaRetornoProcessoDTO(
        sucesso=False,
        retorno=mensagem,
        status=RpaHistoricoStatusEnum.Falha,
        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
    )


async def encontrar_janela(
    titulo: Optional[str] = None, titulo_regex: Optional[str] = None, timeout: int = 30
):
    argumentos = {"class_name": CLASSE_JANELA}
    if titulo is not None:
        argumentos["title"] = titulo
    if titulo_regex is not None:
        argumentos["title_re"] = titulo_regex
    for _ in range(timeout):
        try:
            app = Application(backend="win32").connect(timeout=1, **argumentos)
            janela = app.window(**argumentos)
            if janela.exists() and janela.is_visible():
                return janela
        except Exception:
            pass
        await worker_sleep(1)
    return None


def focar(janela):
    try:
        janela.restore()
    except Exception:
        pass
    try:
        janela.set_focus()
    except Exception:
        janela.click_input()


def janela_esta_aberta(janela) -> bool:
    try:
        return janela.exists() and janela.is_visible()
    except Exception:
        return False


async def abrir_autosystem():
    console.print("[AUTOSYSTEM] Encerrando processos anteriores...")
    if not await kill_all_emsys():
        raise RuntimeError("Não foi possível encerrar o AutoSystem anterior.")
    if not CAMINHO_AUTOSYSTEM.is_file():
        raise FileNotFoundError(f"Executável não encontrado: {CAMINHO_AUTOSYSTEM}")
    console.print(f"[AUTOSYSTEM] Abrindo: {CAMINHO_AUTOSYSTEM}")
    processo = subprocess.Popen(
        [str(CAMINHO_AUTOSYSTEM)], cwd=str(CAMINHO_AUTOSYSTEM.parent), shell=False
    )
    await worker_sleep(2)
    if processo.poll() is not None:
        raise RuntimeError(
            f"AutoSystem encerrou na inicialização: {processo.returncode}"
        )
    # Primeiro procura a janela pelo PID; caso o aplicativo abra outro processo,
    # procura pelo título da janela GTK, como no fluxo original.
    for tentativa in range(TIMEOUT_JANELA_PRINCIPAL):
        try:
            app = Application(backend="win32").connect(process=processo.pid, timeout=1)
            janelas = app.windows(class_name=CLASSE_JANELA)
            for janela in janelas:
                titulo = (janela.window_text() or "").lower()
                if janela.is_visible() and any(
                    x in titulo for x in ("linx", "autosystem", "postos gerencial")
                ):
                    focar(janela)
                    console.print(
                        f"[AUTOSYSTEM] Janela encontrada: {janela.window_text()}"
                    )
                    return janela
        except Exception:
            pass
        try:
            app = Application(backend="win32").connect(
                class_name=CLASSE_JANELA,
                title_re=r"(?i).*(linx postos gerencial|autosystem|postos gerencial).*",
                timeout=1,
            )
            janela = app.window(
                class_name=CLASSE_JANELA,
                title_re=r"(?i).*(linx postos gerencial|autosystem|postos gerencial).*",
            )
            if janela.exists() and janela.is_visible():
                focar(janela)
                console.print(f"[AUTOSYSTEM] Janela encontrada: {janela.window_text()}")
                return janela
        except Exception:
            pass
        if tentativa % 10 == 0:
            console.print(f"[AUTOSYSTEM] Aguardando janela principal: {tentativa + 1}s")
        await worker_sleep(1)
    raise RuntimeError("A janela principal do AutoSystem não apareceu.")


async def clicar_imagem(
    imagem: Path,
    descricao: str,
    timeout: int = 25,
    confidence: float = 0.80,
    region=None,
) -> bool:
    if not imagem.is_file():
        raise FileNotFoundError(f"Imagem de {descricao} não encontrada: {imagem}")
    for _ in range(timeout):
        try:
            posicao = pyautogui.locateCenterOnScreen(
                str(imagem), confidence=confidence, region=region
            )
            if posicao:
                pyautogui.click(posicao.x, posicao.y)
                console.print(f"[IMAGEM] Clicado: {descricao}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        await worker_sleep(1)
    return False


def regiao(janela):
    try:
        ret = janela.rectangle()
        return (ret.left, ret.top, ret.width(), ret.height())
    except Exception:
        return None


async def fechar_aviso():
    console.print("[AUTOSYSTEM] Procurando janela Aviso...")
    janela = await encontrar_janela(titulo="Aviso", timeout=TIMEOUT_AVISO)
    if janela is None:
        raise RuntimeError("Janela 'Aviso' não apareceu após o login.")
    focar(janela)
    pyautogui.press("enter")
    await worker_sleep(3)
    if janela_esta_aberta(janela):
        pyautogui.press("esc")
        await worker_sleep(2)
    if janela_esta_aberta(janela):
        raise RuntimeError("Janela 'Aviso' permaneceu aberta.")
    console.print("[AUTOSYSTEM] Aviso fechado.", style="bold green")


async def responder_questao():
    console.print("[AUTOSYSTEM] Aguardando janela Questão...", style="bold cyan")
    janela = await encontrar_janela(
        titulo_regex=r"(?i)^Quest.*", timeout=TIMEOUT_QUESTAO
    )
    if janela is None:
        raise RuntimeError("Janela 'Questão' não apareceu no tempo esperado.")
    console.print(
        f"[AUTOSYSTEM] Janela encontrada: {janela.window_text()}", style="bold green"
    )
    focar(janela)
    await worker_sleep(2)
    # Fecha a janela diretamente, sem utilizar imagem.
    janela.close()
    await worker_sleep(2)
    # Confirma se realmente fechou.
    if janela_esta_aberta(janela):
        raise RuntimeError(
            "Janela Questão permaneceu aberta após tentativa de fechamento."
        )
    console.print(
        "[AUTOSYSTEM] Janela Questão fechada com sucesso.", style="bold green"
    )


async def fechar_mensageria_se_existir():
    console.print("[AUTOSYSTEM] Verificando Mensageria...")
    janela = await encontrar_janela(titulo="Mensageria", timeout=10)
    if janela is None:
        console.print("[AUTOSYSTEM] Mensageria não apareceu; seguindo.")
        return
    focar(janela)
    clicou = await clicar_imagem(
        IMAGEM_NAO_EXIBIR,
        "Não Exibir",
        timeout=20,
        confidence=0.70,
        region=regiao(janela),
    )
    if not clicou:
        clicou = await clicar_imagem(
            IMAGEM_NAO_EXIBIR, "Não Exibir (tela inteira)", timeout=10, confidence=0.70
        )
    if not clicou:
        raise RuntimeError("Não foi possível clicar em 'Não Exibir' na Mensageria.")
    pyautogui.press("esc")
    await worker_sleep(2)
    if janela_esta_aberta(janela):
        focar(janela)
        pyautogui.press("esc")
        await worker_sleep(2)
    if janela_esta_aberta(janela):
        raise RuntimeError("Mensageria permaneceu aberta.")
    console.print("[AUTOSYSTEM] Mensageria fechada.", style="bold green")


async def acessar_produtos(janela=None):
    """Acessa Produtos usando somente a imagem, sem tocar no HWND antigo."""
    console.print("[PRODUTOS] Procurando botão pela imagem btn_produto.png...")
    if not IMAGEM_PRODUTO.is_file():
        raise FileNotFoundError(f"Imagem de Produtos não encontrada: {IMAGEM_PRODUTO}")
    # o AutoSystem pode recriar a janela durante o login.
    clicou = await clicar_imagem(
        IMAGEM_PRODUTO,
        "Produtos",
        timeout=40,
        confidence=0.80,
        region=None,
    )
    if not clicou:
        raise RuntimeError(
            f"Botão Produtos não localizado pela imagem: {IMAGEM_PRODUTO}"
        )
    console.print("[PRODUTOS] Botão Produtos clicado.", style="bold green")
    await worker_sleep(2)


async def preencher_lancamento_produtos(config: dict):
    """Aguarda a janela GTK de lançamento e preenche seguindo a ordem de TABs.

    A tela já deve abrir com o campo Data Inicial focado.

    Não utiliza cliques nos campos, preservando a navegação do sistema.

    """
    console.print("[PRODUTOS] Aguardando janela 'Lançamento de Produtos'...")
    # O título pode aparecer no SWAPY com caracteres acentuados incorretos.
    janela = await encontrar_janela(
        titulo_regex=r"(?i).*amento de Produtos.*",
        timeout=TIMEOUT_LANCAMENTO_PRODUTOS,
    )
    if janela is None:
        raise RuntimeError(
            "Janela 'Lançamento de Produtos' não apareceu "
            f"em {TIMEOUT_LANCAMENTO_PRODUTOS} segundos."
        )
    console.print(
        f"[PRODUTOS] Janela localizada: {janela.window_text()}", style="bold green"
    )
    # Data Inicial
    try:
        janela.set_focus()
    except Exception:
        console.print(
            "[PRODUTOS][AVISO] Não foi possível ativar a janela. "
            "Verifique se está em primeiro plano.",
            style="bold yellow",
        )
    await worker_sleep(1)

    def preencher_campo(valor, nome):
        console.print(f"[PRODUTOS] Preenchendo {nome}: {valor}")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        pyautogui.write(str(valor), interval=0.08)

    preencher_campo(config["periodoInicial"], "Data Inicial")
    pyautogui.press("tab")
    await worker_sleep(0.4)
    preencher_campo(config["periodoFinal"], "Data Final")
    console.print("[PRODUTOS] Avançando 6 TABs até Empresa...")
    pyautogui.press("tab", presses=6, interval=0.3)
    await worker_sleep(0.5)
    preencher_campo(config["empresa"], "Empresa")
    pyautogui.press("tab")
    await worker_sleep(0.5)
    preencher_campo(config["deposito"], "Depósito")
    console.print("[PRODUTOS] Avançando 3 TABs e confirmando com ENTER...")
    pyautogui.press("tab", presses=3, interval=0.3)
    await worker_sleep(0.5)
    pyautogui.press("enter")
    await worker_sleep(2)
    console.print(
        "[PRODUTOS] ENTER de confirmação enviado. "
        "Seguindo para seleção da operação.",
        style="bold green",
    )


async def selecionar_operacao_produtos(config: dict):
    """Na janela Lançamentos de Produtos, seleciona Novo e a operação."""
    console.print("[PRODUTOS] Aguardando janela 'Lançamentos de Produtos'...")
    janela = await encontrar_janela(
        titulo_regex=r"(?i).*amentos? de Produtos.*",
        timeout=TIMEOUT_LANCAMENTO_PRODUTOS,
    )
    if janela is None:
        raise RuntimeError("Janela 'Lançamentos de Produtos' não apareceu.")
    console.print("[PRODUTOS] Janela de lançamentos encontrada.", style="bold green")
    # Localização por imagem na tela inteira evita utilizar HWND desatualizado.
    if not await clicar_imagem(IMAGEM_BOTAO_NOVO, "Novo", timeout=40, region=None):
        raise RuntimeError(f"Botão Novo não encontrado: {IMAGEM_BOTAO_NOVO}")
    await worker_sleep(2)
    operacao = str(config.get("operacao", "")).strip().upper()
    if operacao not in IMAGENS_OPERACOES:
        raise ValueError(
            f"Operação '{operacao}' inválida. Válidas: {', '.join(IMAGENS_OPERACOES)}"
        )
    nome_operacao, imagem_operacao = IMAGENS_OPERACOES[operacao]
    descricao = f"Operação {nome_operacao} ({operacao})"
    console.print(f"[PRODUTOS] Selecionando: {descricao}")
    if not await clicar_imagem(imagem_operacao, descricao, timeout=40, region=None):
        raise RuntimeError(
            f"Imagem da operação não encontrada na tela: {imagem_operacao}"
        )
    await worker_sleep(1)
    pyautogui.press("tab")
    await worker_sleep(0.5)
    pyautogui.press("enter")
    await worker_sleep(2)
    console.print(
        f"[PRODUTOS] Operação {operacao}: TAB e ENTER enviados.", style="bold green"
    )


async def preencher_produto_quantidade(config: dict):
    """Aguarda a janela singular 'Lançamento de Produto' e confirma os campos."""
    console.print("[PRODUTOS] Aguardando janela 'Lançamento de Produto'...")
    janela = await encontrar_janela(
        titulo_regex=r"(?i).*amento de Produto\s*$",
        timeout=TIMEOUT_LANCAMENTO_PRODUTOS,
    )
    if janela is None:
        raise RuntimeError(
            "Janela 'Lançamento de Produto' não apareceu no tempo esperado."
        )
    console.print(
        f"[PRODUTOS] Janela localizada: {janela.window_text()}", style="bold green"
    )
    # A tela já deve estar ativa após a confirmação da operação anterior.
    await worker_sleep(1)
    console.print("[PRODUTOS] 3 TABs até Produto...")
    pyautogui.press("tab", presses=3, interval=0.3)
    await worker_sleep(0.5)
    console.print(f"[PRODUTOS] Preenchendo produto: {config['produto']}")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyautogui.write(str(config["produto"]), interval=0.08)
    pyautogui.press("tab")
    await worker_sleep(0.5)
    console.print(f"[PRODUTOS] Preenchendo quantidade: {config['quantidade']}")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyautogui.write(str(config["quantidade"]), interval=0.08)
    # Antes, 5 TABs chegavam ao botão de confirmação.
    # Agora, 4 TABs chegam à Observação; mais 1 TAB chega à confirmação.
    console.print("[PRODUTOS] 4 TABs até Observação...")
    pyautogui.press("tab", presses=4, interval=0.3)
    await worker_sleep(0.5)
    observacao = "AJUSTE RPA REF. SALDO NEGATIVO AS"
    console.print(f"[PRODUTOS] Preenchendo observação: {observacao}")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyautogui.write(observacao, interval=0.05)
    await worker_sleep(0.5)
    console.print("[PRODUTOS] 1 TAB e ENTER para confirmar...")
    pyautogui.press("tab")
    await worker_sleep(0.5)
    pyautogui.press("enter")
    await worker_sleep(2)
    console.print("[PRODUTOS] Confirmação enviada. Fechando a janela de lançamento...")
    # Reencontra a janela APÓS confirmar, evitando reutilizar um HWND inválido.
    janela_final = await encontrar_janela(
        titulo_regex=r"(?i).*amento de Produto\s*$", timeout=5
    )
    if janela_final is not None:
        try:
            janela_final.close()
        except OSError as erro:
            # Se a confirmação já destruiu o HWND, conferimos pelo título abaixo.
            console.print(
                f"[PRODUTOS] Janela mudou após o ENTER: {erro}", style="yellow"
            )
        await worker_sleep(2)
        restante = await encontrar_janela(
            titulo_regex=r"(?i).*amento de Produto\s*$", timeout=3
        )
        if restante is not None:
            raise RuntimeError(
                "A janela 'Lançamento de Produto' permaneceu aberta após fechar."
            )
    console.print(
        "[PRODUTOS] Lançamento confirmado e janela fechada.", style="bold green"
    )


async def fechar_janela_listagem_produtos():
    """Fecha a tela de listagem (plural) e mantém o AutoSystem principal aberto."""
    console.print("[PRODUTOS] Aguardando retorno à janela 'Lançamentos de Produtos'...")
    padrao = r"(?i).*amentos de Produtos\s*$"
    janela = await encontrar_janela(titulo_regex=padrao, timeout=15)
    if janela is None:
        raise RuntimeError(
            "Janela 'Lançamentos de Produtos' não encontrada para fechar."
        )
    console.print("[PRODUTOS] Fechando janela de listagem de Produtos...")
    try:
        janela.close()
    except OSError as erro:
        console.print(
            f"[PRODUTOS] Identificador da janela mudou: {erro}", style="yellow"
        )
    await worker_sleep(2)
    # Confere pelo título atual, não pelo identificador antigo.
    restante = await encontrar_janela(titulo_regex=padrao, timeout=3)
    if restante is not None:
        raise RuntimeError("A janela 'Lançamentos de Produtos' permaneceu aberta.")
    console.print(
        "[PRODUTOS] Janela de listagem fechada. AutoSystem permanece aberto.",
        style="bold green",
    )


def log_etapa(etapa: str, mensagem: str, estilo: str = "cyan"):
    """Logs operacionais: somente no terminal, nunca no retorno do AutomateHub."""
    console.print(f"[RPA][{etapa}] {mensagem}", style=estilo)


def mensagem_sucesso_controle(config: dict) -> str:
    """Resumo de negócio para o histórico do AutomateHub."""
    codigo = str(config["operacao"]).strip().upper()
    nome = IMAGENS_OPERACOES[codigo][0]
    return (
        "Lançamento de produto concluído no AutoSystem. "
        f"Empresa: {config['empresa']} | Depósito: {config['deposito']} | "
        f"Produto: {config['produto']} | Quantidade: {config['quantidade']} | "
        f"Operação: {codigo} ({nome}) | "
        f"Período: {config['periodoInicial']} a {config['periodoFinal']}."
    )


async def lancamento_produtos_as(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """Processa o lançamento; devolve ao Worker apenas status e resumo objetivo."""
    etapa = "VALIDAÇÃO"
    try:
        config = getattr(task, "configEntrada", None) or {}
        log_etapa(etapa, "Verificando parâmetros de entrada...")
        parametros = (
            "empresa",
            "periodoInicial",
            "periodoFinal",
            "deposito",
            "produto",
            "quantidade",
            "operacao",
        )
        for campo in parametros:
            if config.get(campo) is None or config.get(campo) == "":
                return retorno_falha_tecnica(f"Parâmetro obrigatório ausente: {campo}.")
        operacao = str(config["operacao"]).strip().upper()
        if operacao not in IMAGENS_OPERACOES:
            return retorno_falha_tecnica(f"Operação não suportada: {operacao}.")
        log_etapa(etapa, "Parâmetros válidos.", "green")

        etapa = "ABERTURA"
        log_etapa(etapa, "Iniciando AutoSystem...")
        janela = await abrir_autosystem()

        etapa = "LOGIN"
        log_etapa(etapa, "Autenticando...")
        await login_autosystem(main_window=janela)
        log_etapa(etapa, "Rotina de login executada.", "green")

        etapa = "MENSAGENS"
        log_etapa(etapa, "Tratando avisos e janelas iniciais...")
        await fechar_aviso()
        await responder_questao()
        await fechar_mensageria_se_existir()
        log_etapa(etapa, "Mensagens iniciais tratadas.", "green")

        etapa = "PRODUTOS"
        log_etapa(etapa, "Acessando módulo de Produtos...")
        await acessar_produtos(janela)

        etapa = "FILTROS"
        log_etapa(etapa, "Preenchendo período, empresa e depósito...")
        await preencher_lancamento_produtos(config)

        etapa = "OPERAÇÃO"
        log_etapa(
            etapa, f"Selecionando {operacao} ({IMAGENS_OPERACOES[operacao][0]})..."
        )
        await selecionar_operacao_produtos(config)

        etapa = "LANÇAMENTO"
        log_etapa(etapa, "Preenchendo produto, quantidade e observação...")
        await preencher_produto_quantidade(config)

        etapa = "FINALIZAÇÃO"
        log_etapa(etapa, "Fechando a janela de listagem...")
        await fechar_janela_listagem_produtos()

        await worker_sleep(10)
        mensagem = mensagem_sucesso_controle(config)
        log_etapa("SUCESSO", mensagem, "bold green")
        return retorno_sucesso(mensagem)

    except Exception as erro:
        # Diagnóstico técnico detalhado somente no terminal/log do Worker.
        log_etapa(
            "FALHA", f"Etapa: {etapa} | {type(erro).__name__}: {erro}", "bold red"
        )
        traceback.print_exc()
        logger.error(f"AutoSystem - etapa {etapa}: {type(erro).__name__}: {erro}")
        # Retorno mensagem
        return retorno_falha_tecnica(
            f"Falha no lançamento de produto. Etapa: {etapa}. Motivo: {erro}"
        )
