# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, date
import json
import os
import sys
from ftplib import FTP
from rich.console import Console

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

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

console = Console()
log = console.log

ano_atual = date.today().year
EMPRESA = "1"  # se quiser devolver no payload

# Extensões válidas (pra cortar lixo na pasta)
# tudo em minúsculo porque vamos comparar com nome.lower()
EXTENSOES_PERMITIDAS = (".ret", ".txt")


# =====================================================================
# TESTE RÁPIDO: APENAS CONECTA E LISTA PASTA REMOTA (SEM VARREDURA)
# =====================================================================
def testar_conexao_ftp(
    host: str = "186.250.186.41",
    porta: int = 21,
    usuario: str = "simrede",
    senha: str = "",
    pasta_teste: str = "/",
):
    """
    Teste simples de FTP SEM TLS, apenas para validar conexão e listagem.
    """
    ftp = None
    try:
        log("[cyan]TESTE: Conectando ao FTP simples...[/cyan]")
        ftp = FTP()
        ftp.connect(host, porta, timeout=20)
        log("[green]Conectado ao host, enviando credenciais...[/green]")
        ftp.login(usuario, senha)
        log("[green]Login FTP realizado com sucesso.[/green]")

        log(f"[cyan]Mudando para diretório de teste: {pasta_teste}[/cyan]")
        ftp.cwd(pasta_teste)

        log("[cyan]Listando diretório...[/cyan]")
        arquivos = ftp.nlst()
        if not arquivos:
            log("[yellow]Nenhum arquivo/pasta listado (pasta vazia ou sem permissão).[/yellow]")
        else:
            log("[bold green]Entradas encontradas:[/bold green]")
            for nome in arquivos:
                log(f" • {nome}")

        log("[bold green]✅ TESTE FTP SIMPLES CONCLUÍDO COM SUCESSO.[/bold green]")

    except Exception as e:
        log(f"[red]❌ ERRO NO TESTE FTP[/red]: {e}")
    finally:
        if ftp:
            try:
                ftp.quit()
            except Exception:
                pass
        log("[cyan]Conexão FTP de teste encerrada.[/cyan]")


# =====================================================================
# FUNÇÃO OFICIAL: COLETA E ENVIA ARQUIVOS POR FTP SIMPLES
# =====================================================================
async def coleta_envio_ftp(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    try:
        # ====================================
        # PARÂMETROS DE ORIGEM
        # ====================================
        DESTINO_IP_ROOT = r"\\fcaswfs01.ditrento.com.br\compartilhadas$"
        PASTA_ANO_ATUAL = fr"{DESTINO_IP_ROOT}\Nexera\Extrato\{ano_atual}"

        hoje = date.today()
        hoje_ordinal = hoje.toordinal()

        log("[cyan]Iniciando coleta_envio_ftp (envio FTP simples)[/]")
        log(
            f"Varredura: {PASTA_ANO_ATUAL} | Data = {hoje.strftime('%d/%m/%Y')}"
        )

        if not os.path.isdir(PASTA_ANO_ATUAL):
            msg = f"Pasta não encontrada: {PASTA_ANO_ATUAL}"
            log(f"[red]{msg}[/]")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        # ====================================
        # CARREGAR CONFIG FTP
        # ====================================
        log("Carregando configuração FTP: get_config_by_name('netunna_ftp')")
        cfg_ftp = await get_config_by_name("netunna_ftp")
        ftp_cfg = cfg_ftp.conConfiguracao or {}

        host = (
            ftp_cfg.get("host")
            or ftp_cfg.get("ip")
            or ftp_cfg.get("servidor")
            or "186.250.186.41"
        )

        porta_cfg = ftp_cfg.get("porta")
        try:
            porta = int(porta_cfg) if porta_cfg else 21
        except Exception:
            porta = 21

        usuario = (
            ftp_cfg.get("usuario")
            or ftp_cfg.get("user")
            or ftp_cfg.get("login")
            or "simrede"
        )
        senha = ftp_cfg.get("senha") or ftp_cfg.get("password") or ""

        # PRD ou QAS
        pasta_destino = "/EXTRATOS_PRD"
        # pasta_destino = "/EXTRATOS_QAS"

        if not host or not usuario:
            msg = "Configuração 'netunna_ftp' incompleta (host/usuario)."
            log(f"[red]{msg}[/]")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        log(
            f"Config FTP -> host={host} | porta={porta} | usuario={usuario} | pasta_destino={pasta_destino}"
        )

        # ====================================
        # FILTRAR ARQUIVOS (somente data de hoje) - POR MTIME
        # ====================================
        selecionados = []
        avaliados = 0
        ignorados_data = 0
        ignorados_ext = 0

        log("Iniciando varredura dos arquivos (por mtime, com extensão filtrada)...")
        inicio_scan = datetime.now()

        with os.scandir(PASTA_ANO_ATUAL) as it:
            for entry in it:
                if not entry.is_file(follow_symlinks=False):
                    continue

                nome = entry.name
                nome_lower = nome.lower()

                # Filtro de extensão
                if EXTENSOES_PERMITIDAS is not None:
                    if not any(nome_lower.endswith(ext) for ext in EXTENSOES_PERMITIDAS):
                        ignorados_ext += 1
                        continue

                try:
                    st = entry.stat()
                except FileNotFoundError:
                    # arquivo pode ter sumido no meio do caminho
                    continue

                dt_mod = date.fromtimestamp(st.st_mtime)

                # compara usando ordinal (barato)
                if dt_mod.toordinal() != hoje_ordinal:
                    ignorados_data += 1
                    continue

                avaliados += 1
                selecionados.append(
                    {
                        "arquivo": nome,
                        "caminho": entry.path,
                        "tamanho_bytes": st.st_size,
                        "data_modificacao": dt_mod.strftime("%Y-%m-%d"),
                    }
                )

                log("[green]Selecionado para envio[/green]: %s", nome)

        fim_scan = datetime.now()
        tempo_scan = (fim_scan - inicio_scan).total_seconds()
        log(
            "======== RESULTADO VARREDURA ========\n"
            "Selecionados hoje: %s\n"
            "Ignorados por data (mtime): %s\n"
            "Ignorados por extensão: %s\n"
            "Tempo varredura: %.2f s",
            len(selecionados),
            ignorados_data,
            ignorados_ext,
            tempo_scan,
        )

        if not selecionados:
            msg = (
                f"Nenhum arquivo modificado em {hoje.strftime('%d/%m/%Y')} "
                f"encontrado em {PASTA_ANO_ATUAL}"
            )
            log(f"[yellow]{msg}[/]")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Sucesso,  # negócio: nada pra enviar
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        # ===== PRINTAR LISTA COMPLETA DOS ARQUIVOS QUE SERÃO ENVIADOS =====
        log("[bold green]===== ARQUIVOS QUE SERÃO ENVIADOS =====[/bold green]")
        for arq in selecionados:
            log(f" • {arq['arquivo']}")
        log("[bold green]========================================[/bold green]")

        # ====================================
        # CONECTAR AO FTP SIMPLES
        # ====================================
        enviados = []
        falhas_envio = []
        ftp = None

        log("[cyan]Conectando ao FTP simples...[/cyan]")

        try:
            ftp = FTP()
            ftp.connect(host, porta, timeout=20)
            ftp.login(usuario, senha)
            log("[green]Conexão FTP estabelecida e autenticada.[/green]")

            # -------- garante que pasta destino existe (recursivo) --------
            def ftp_mkdir_recursive(ftp_obj: FTP, path: str):
                if not path or path in ["", "/", "\\"]:
                    return
                try:
                    ftp_obj.cwd("/")  # garante raiz
                except Exception:
                    pass

                partes = [p for p in path.replace("\\", "/").split("/") if p]
                for p in partes:
                    try:
                        ftp_obj.cwd(p)
                    except Exception:
                        ftp_obj.mkd(p)
                        ftp_obj.cwd(p)

            if pasta_destino not in ["", "/", "\\"]:
                ftp_mkdir_recursive(ftp, pasta_destino)

            # ====================================
            # ENVIO DOS ARQUIVOS
            # ====================================
            total = len(selecionados)
            for idx, sel in enumerate(selecionados, 1):
                nome = sel["arquivo"]
                caminho = sel["caminho"]

                log("[bold cyan]Enviando arquivo (%s/%s):[/] %s", idx, total, nome)

                try:
                    with open(caminho, "rb") as f:
                        ftp.storbinary(f"STOR {nome}", f)

                    enviados.append(
                        {
                            "arquivo": nome,
                            "local": caminho,
                            "remoto": f"{pasta_destino.rstrip('/')}/{nome}",
                            "tamanho_bytes": sel["tamanho_bytes"],
                        }
                    )

                    log("[green]Arquivo enviado com sucesso[/green]: %s", nome)

                except Exception as e_env:
                    falhas_envio.append(
                        {
                            "arquivo": nome,
                            "local": caminho,
                            "remoto": f"{pasta_destino.rstrip('/')}/{nome}",
                            "motivo": str(e_env),
                        }
                    )
                    log("[red]Falha ao enviar %s -> %s[/red]", nome, str(e_env))

        except Exception as e_conn:
            msg = f"Erro ao conectar/enviar via FTP simples: {e_conn}"
            log(f"[red]{msg}[/]")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )
        finally:
            if ftp:
                try:
                    ftp.quit()
                except Exception:
                    pass
            log("[cyan]Conexão FTP encerrada.[/cyan]")

        # ====================================
        # RESUMO FINAL
        # ====================================
        log("======== RESUMO FINAL (FTP simples) ========")
        log("Enviados: %s | Falhas: %s", len(enviados), len(falhas_envio))

        retorno_payload = {
            "empresa": EMPRESA,
            "data_processamento": hoje.strftime("%Y-%m-%d"),
            "pasta_origem": PASTA_ANO_ATUAL,
            "pasta_destino_ftp": pasta_destino,
            "enviados_count": len(enviados),
            "enviados": enviados,
            "falhas_envio": falhas_envio,
            "ignorados": {
                "por_data_mtime": ignorados_data,
                "por_extensao": ignorados_ext,
            },
            "tempo_varredura_segundos": tempo_scan,
        }

        retorno_str = json.dumps(retorno_payload, ensure_ascii=False, indent=2)

        sucesso = len(enviados) > 0

        return RpaRetornoProcessoDTO(
            sucesso=sucesso,
            retorno=retorno_str,
            status=RpaHistoricoStatusEnum.Sucesso
            if sucesso
            else RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    except Exception as ex:
        log("[red]Exceção geral[/red]: %s", ex)
        logger.exception("Erro geral coleta_envio_ftp (FTP simples)")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=str(ex),
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

