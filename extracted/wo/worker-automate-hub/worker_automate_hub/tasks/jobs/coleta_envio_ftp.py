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

EMPRESA = "1"

# Diretório correto
PASTA_ORIGEM = (
    r"\\fcaswfs01.ditrento.com.br"
    r"\FS_BANCOS_PROD"
    r"\FS_NEXXERA_PRD"
    r"\Entrada"
    r"\Extratos"
    r"\Backup"
)

# Extensões válidas
EXTENSOES_PERMITIDAS = (".ret", ".txt")

# Prefixos obrigatórios
PREFIXOS_PERMITIDOS = (
    "EXT_246_22068335_",
    "EXT_246_66100960_",
    "EXT_041_0625_060300400_",
    "EXT_041_0625_060300405_",
    "EXT_041_0625_060300404_",
    "EXT_041_0625_060300406_",
    "EXT_041_0625_060300407_",
    "EXT_237_5533",
    "EXT_001_5103010_",
    "EXT_001_51039_",
    "EXT_208_4212710_",
    "EXT_208_0001_590566_",
    "EXT_208_1_832884_",
    "EXT_104_2132_",
    "EXT_341_19602",
    "EXT_422_2076631",
    "EXT_033_8700678716_",
    "EXT_033_008700490466_",
    "EXT_748_51270",
    "EXT_197_564959831",
    "EXT_655_2520625012",
    "EXT_655_11249811_",
)


# =====================================================================
# HELPERS
# =====================================================================
def arquivo_tem_prefixo_permitido(nome_arquivo: str) -> bool:
    """
    Valida se o arquivo começa com algum dos prefixos permitidos.
    Comparação feita em maiúsculo para evitar problema de case.
    """
    nome_upper = nome_arquivo.upper()
    return any(nome_upper.startswith(prefixo.upper()) for prefixo in PREFIXOS_PERMITIDOS)


def arquivo_tem_extensao_permitida(nome_arquivo: str) -> bool:
    """
    Valida extensão permitida.
    """
    nome_lower = nome_arquivo.lower()
    return any(nome_lower.endswith(ext) for ext in EXTENSOES_PERMITIDAS)


def arquivo_eh_do_dia_execucao(st, hoje: date) -> tuple[bool, str, str]:
    """
    Valida se a data de modificação OU criação é igual ao dia da execução.

    st.st_mtime = data de modificação
    st.st_ctime = no Windows normalmente representa data de criação.
                Em alguns sistemas pode representar alteração de metadados.
    """
    dt_modificacao = date.fromtimestamp(st.st_mtime)
    dt_criacao = date.fromtimestamp(st.st_ctime)

    eh_hoje = dt_modificacao == hoje or dt_criacao == hoje

    return (
        eh_hoje,
        dt_modificacao.strftime("%Y-%m-%d"),
        dt_criacao.strftime("%Y-%m-%d"),
    )


# =====================================================================
# TESTE RÁPIDO: APENAS CONECTA E LISTA PASTA REMOTA
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
            log("[yellow]Nenhum arquivo/pasta listado, pasta vazia ou sem permissão.[/yellow]")
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
        hoje = date.today()

        log("[cyan]Iniciando coleta_envio_ftp - envio FTP simples[/cyan]")
        log(f"Varredura: {PASTA_ORIGEM}")
        log(f"Data execução: {hoje.strftime('%d/%m/%Y')}")

        if not os.path.isdir(PASTA_ORIGEM):
            msg = f"Pasta não encontrada: {PASTA_ORIGEM}"
            log(f"[red]{msg}[/red]")

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
            msg = "Configuração 'netunna_ftp' incompleta: host/usuario."
            log(f"[red]{msg}[/red]")

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
            )

        log(
            f"Config FTP -> host={host} | porta={porta} | "
            f"usuario={usuario} | pasta_destino={pasta_destino}"
        )

        # ====================================
        # FILTRAR ARQUIVOS
        # ====================================
        selecionados = []

        avaliados = 0
        ignorados_ext = 0
        ignorados_prefixo = 0
        ignorados_data = 0
        ignorados_nao_arquivo = 0

        log("Iniciando varredura dos arquivos...")
        inicio_scan = datetime.now()

        with os.scandir(PASTA_ORIGEM) as it:
            for entry in it:
                if not entry.is_file(follow_symlinks=False):
                    ignorados_nao_arquivo += 1
                    continue

                avaliados += 1

                nome = entry.name

                # 1. Valida extensão
                if not arquivo_tem_extensao_permitida(nome):
                    ignorados_ext += 1
                    continue

                # 2. Valida prefixo obrigatório
                if not arquivo_tem_prefixo_permitido(nome):
                    ignorados_prefixo += 1
                    continue

                # 3. Valida data de criação/modificação
                try:
                    st = entry.stat()
                except FileNotFoundError:
                    continue

                eh_do_dia, data_modificacao, data_criacao = arquivo_eh_do_dia_execucao(
                    st=st,
                    hoje=hoje,
                )

                if not eh_do_dia:
                    ignorados_data += 1
                    continue

                selecionados.append(
                    {
                        "arquivo": nome,
                        "caminho": entry.path,
                        "tamanho_bytes": st.st_size,
                        "data_modificacao": data_modificacao,
                        "data_criacao": data_criacao,
                    }
                )

                log(
                    "[green]Selecionado para envio[/green]: "
                    f"{nome} | modificação={data_modificacao} | criação={data_criacao}"
                )

        fim_scan = datetime.now()
        tempo_scan = (fim_scan - inicio_scan).total_seconds()

        log(
            "======== RESULTADO VARREDURA ========\n"
            f"Avaliados: {avaliados}\n"
            f"Selecionados: {len(selecionados)}\n"
            f"Ignorados não arquivo: {ignorados_nao_arquivo}\n"
            f"Ignorados por extensão: {ignorados_ext}\n"
            f"Ignorados por prefixo: {ignorados_prefixo}\n"
            f"Ignorados por data criação/modificação: {ignorados_data}\n"
            f"Tempo varredura: {tempo_scan:.2f} s"
        )

        if not selecionados:
            msg = (
                f"Nenhum arquivo válido encontrado em {hoje.strftime('%d/%m/%Y')} "
                f"na pasta {PASTA_ORIGEM}. "
                f"Filtros: extensão {EXTENSOES_PERMITIDAS}, prefixos obrigatórios EXT_ específicos, "
                f"data de criação/modificação igual ao dia da execução."
            )

            log(f"[yellow]{msg}[/yellow]")

            retorno_payload = {
                "empresa": EMPRESA,
                "data_processamento": hoje.strftime("%Y-%m-%d"),
                "pasta_origem": PASTA_ORIGEM,
                "pasta_destino_ftp": pasta_destino,
                "enviados_count": 0,
                "enviados": [],
                "falhas_envio": [],
                "ignorados": {
                    "nao_arquivo": ignorados_nao_arquivo,
                    "por_extensao": ignorados_ext,
                    "por_prefixo": ignorados_prefixo,
                    "por_data_criacao_modificacao": ignorados_data,
                },
                "tempo_varredura_segundos": tempo_scan,
                "mensagem": msg,
            }

            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=json.dumps(retorno_payload, ensure_ascii=False, indent=2),
                status=RpaHistoricoStatusEnum.Sucesso,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)],
            )

        # ====================================
        # PRINTAR LISTA DOS ARQUIVOS
        # ====================================
        log("[bold green]===== ARQUIVOS QUE SERÃO ENVIADOS =====[/bold green]")

        for arq in selecionados:
            log(
                f" • {arq['arquivo']} | "
                f"modificação={arq['data_modificacao']} | "
                f"criação={arq['data_criacao']} | "
                f"bytes={arq['tamanho_bytes']}"
            )

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

            # -------- garante que pasta destino existe --------
            def ftp_mkdir_recursive(ftp_obj: FTP, path: str):
                if not path or path in ["", "/", "\\"]:
                    return

                try:
                    ftp_obj.cwd("/")
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
                remoto = f"{pasta_destino.rstrip('/')}/{nome}"

                log(f"[bold cyan]Enviando arquivo ({idx}/{total}):[/bold cyan] {nome}")

                try:
                    with open(caminho, "rb") as f:
                        ftp.storbinary(f"STOR {nome}", f)

                    enviados.append(
                        {
                            "arquivo": nome,
                            "local": caminho,
                            "remoto": remoto,
                            "tamanho_bytes": sel["tamanho_bytes"],
                            "data_modificacao": sel["data_modificacao"],
                            "data_criacao": sel["data_criacao"],
                        }
                    )

                    log(f"[green]Arquivo enviado com sucesso:[/green] {nome}")

                except Exception as e_env:
                    falhas_envio.append(
                        {
                            "arquivo": nome,
                            "local": caminho,
                            "remoto": remoto,
                            "motivo": str(e_env),
                        }
                    )

                    log(f"[red]Falha ao enviar {nome} -> {e_env}[/red]")

        except Exception as e_conn:
            msg = f"Erro ao conectar/enviar via FTP simples: {e_conn}"
            log(f"[red]{msg}[/red]")

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
        log("======== RESUMO FINAL - FTP SIMPLES ========")
        log(f"Enviados: {len(enviados)} | Falhas: {len(falhas_envio)}")

        sucesso = len(enviados) > 0 and len(falhas_envio) == 0

        if len(enviados) > 0 and len(falhas_envio) > 0:
            status_final = RpaHistoricoStatusEnum.Falha
            sucesso_final = False
            msg_final = "Processo finalizado com envio parcial: existem falhas de envio."
            tag_final = RpaTagEnum.Tecnico

        elif len(enviados) > 0:
            status_final = RpaHistoricoStatusEnum.Sucesso
            sucesso_final = True
            msg_final = "Processo finalizado com sucesso: arquivos enviados ao FTP."

        else:
            status_final = RpaHistoricoStatusEnum.Falha
            sucesso_final = False
            msg_final = "Nenhum arquivo foi enviado ao FTP."
            tag_final = RpaTagEnum.Tecnico

        retorno_payload = {
            "empresa": EMPRESA,
            "data_processamento": hoje.strftime("%Y-%m-%d"),
            "pasta_origem": PASTA_ORIGEM,
            "pasta_destino_ftp": pasta_destino,
            "enviados_count": len(enviados),
            "falhas_count": len(falhas_envio),
            "enviados": enviados,
            "falhas_envio": falhas_envio,
            "ignorados": {
                "nao_arquivo": ignorados_nao_arquivo,
                "por_extensao": ignorados_ext,
                "por_prefixo": ignorados_prefixo,
                "por_data_criacao_modificacao": ignorados_data,
            },
            "tempo_varredura_segundos": tempo_scan,
            "mensagem": msg_final,
        }

        retorno_str = json.dumps(retorno_payload, ensure_ascii=False, indent=2)

        return RpaRetornoProcessoDTO(
            sucesso=sucesso_final,
            retorno=retorno_str,
            status=status_final,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    except Exception as ex:
        log(f"[red]Exceção geral:[/red] {ex}")
        logger.exception("Erro geral coleta_envio_ftp - FTP simples")

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=str(ex),
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

if __name__ == "__main__":
    async def main():
        retorno = await coleta_envio_ftp(None)

        print("\n========== RETORNO DO PROCESSO ==========")
        print("Sucesso:", retorno.sucesso)
        print("Status:", retorno.status)
        print("Retorno:", retorno.retorno)
        print("Tags:", retorno.tags)

    asyncio.run(main())