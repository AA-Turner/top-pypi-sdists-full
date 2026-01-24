# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import stat
import time
import re
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from ftplib import FTP
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import paramiko

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

# ✅ Retornos (para Sucesso/Falha)
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)

# =========================================================
# CAMINHOS FIXOS
# =========================================================
EQUALS_OPENSSH_KEY_FIXED = r"assets\ssh_key\redesim-07473735000262.com.br.openssh.key"


# =========================
# LOGGER / CONSOLE (fallback)
# =========================
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

try:
    from rich.console import Console
    console = Console()
except Exception:
    class _ConsoleFallback:
        def print(self, msg, style=None):
            print(msg, flush=True)
    console = _ConsoleFallback()


# =========================
# HELPERS
# =========================
def pick(cfg: Dict[str, Any], *keys: str, default: Any = "") -> Any:
    for k in keys:
        v = cfg.get(k)
        if v is None:
            continue
        if isinstance(v, str) and v.strip():
            return v.strip()
        if not isinstance(v, str):
            return v
    return default


def to_int(value: Any, default: int) -> int:
    try:
        if value is None:
            return default
        if isinstance(value, int):
            return value
        s = str(value).strip()
        return int(s) if s else default
    except Exception:
        return default


def is_sftp_file(attr: paramiko.SFTPAttributes) -> bool:
    return stat.S_ISREG(attr.st_mode)


def ftp_safe_name(name: str) -> str:
    return re.sub(r'[|<>:"/\\?*]', "_", name)


# =========================
# CONFIGS
# =========================
@dataclass
class NetunnaFtpConfig:
    host: str
    porta: int
    usuario: str
    senha: str
    pasta_destino: str


@dataclass
class EqualsSftpConfig:
    host: str
    porta: int
    usuario: str
    pasta_remota: str
    key_path: str
    passphrase: Optional[str]


# =========================
# LOAD CONFIGS
# =========================
async def load_netunna_ftp_cfg(get_config_by_name, log) -> NetunnaFtpConfig:
    log("Carregando configuração FTP: netunna_ftp")
    cfg = await get_config_by_name("netunna_ftp")
    c = getattr(cfg, "conConfiguracao", None) or {}

    host = pick(c, "host", "ip", "servidor", default="186.250.186.41")
    porta = to_int(pick(c, "porta", "port"), 21)
    usuario = pick(c, "usuario", "user", "login", default="simrede")
    senha = pick(c, "senha", "password", "pass", default="")
    pasta_destino = (
        pick(c, "pasta_destino", "remote_dir", "dir", "pasta", default="")
        or "/ADQUIRENTES"
    )

    if not host or not usuario:
        raise RuntimeError("Configuração 'netunna_ftp' incompleta (host/usuario).")
    if not senha:
        raise RuntimeError("Configuração 'netunna_ftp' incompleta (senha).")

    log(
        f"NETUNNA FTP -> host={host} | porta={porta} | usuario={usuario} | pasta_destino={pasta_destino}"
    )
    return NetunnaFtpConfig(host, porta, usuario, senha, pasta_destino)


async def load_equals_ftp_cfg(get_config_by_name, log) -> EqualsSftpConfig:
    log("Carregando configuração SFTP: equals_ftp")
    cfg = await get_config_by_name("equals_ftp")
    c = getattr(cfg, "conConfiguracao", None) or {}

    host = pick(c, "host", "ip", "servidor", default="ftp02.main.sao.equals.com.br")
    porta = to_int(pick(c, "porta", "port"), 20220)
    usuario = pick(c, "usuario", "user", "login", default="")
    pasta_remota = (
        pick(c, "pasta_remota", "remote_dir", "dir", "pasta", default="") or "/download"
    )

    key_path = EQUALS_OPENSSH_KEY_FIXED
    if not Path(key_path).exists():
        raise FileNotFoundError(f"Chave OpenSSH não encontrada: {key_path}")

    passphrase = pick(c, "passphrase", "senha_key", "key_password", default="") or None

    log(
        f"EQUALS SFTP -> host={host} | porta={porta} | usuario={usuario} | pasta_remota={pasta_remota} | key={key_path}"
    )
    return EqualsSftpConfig(host, porta, usuario, pasta_remota, key_path, passphrase)


# =========================
# CONEXÕES
# =========================
def sftp_connect(
    cfg: EqualsSftpConfig, log
) -> Tuple[paramiko.SFTPClient, paramiko.Transport]:
    key_file = cfg.key_path

    if not Path(key_file).exists():
        raise FileNotFoundError(f"Arquivo de chave não encontrado: {key_file}")

    # 1) tenta auto-detect (melhor caminho)
    last_ex = None
    try:
        pkey = paramiko.PKey.from_private_key_file(key_file, password=cfg.passphrase)
        t = paramiko.Transport((cfg.host, cfg.porta))
        t.connect(username=cfg.usuario, pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(t)
        return sftp, t
    except Exception as e:
        last_ex = e

    # 2) fallback explícito por tipo (caso auto-detect falhe)
    for cls_name in ("Ed25519Key", "ECDSAKey", "RSAKey"):
        cls = getattr(paramiko, cls_name, None)
        if not cls:
            continue
        try:
            pkey = cls.from_private_key_file(key_file, password=cfg.passphrase)
            t = paramiko.Transport((cfg.host, cfg.porta))
            t.connect(username=cfg.usuario, pkey=pkey)
            sftp = paramiko.SFTPClient.from_transport(t)
            return sftp, t
        except Exception as e:
            last_ex = e

    raise RuntimeError(
        "Falha ao carregar chave OpenSSH.\n"
        f"Arquivo: {key_file}\n"
        f"Detalhe: {repr(last_ex)}\n"
        "Possíveis causas:\n"
        " - A chave está com passphrase e o campo 'passphrase' não está correto no equals_ftp (Maestro)\n"
        " - A chave exportada não é Private Key (OpenSSH) e sim Public Key\n"
        " - Permissão de leitura no arquivo da chave\n"
    )


def ftp_connect(cfg: NetunnaFtpConfig) -> FTP:
    ftp = FTP()
    ftp.connect(cfg.host, cfg.porta, timeout=60)
    ftp.login(cfg.usuario, cfg.senha)
    ftp.set_pasv(True)
    return ftp


def ftp_cwd_safe(ftp: FTP, path: str) -> None:
    try:
        ftp.cwd(path)
        return
    except Exception:
        parts = [p for p in path.replace("\\", "/").split("/") if p]
        if path.startswith("/"):
            ftp.cwd("/")
        for p in parts:
            try:
                ftp.cwd(p)
            except Exception:
                ftp.mkd(p)
                ftp.cwd(p)


def ftp_noop_safe(ftp: FTP) -> None:
    try:
        ftp.voidcmd("NOOP")
    except Exception:
        pass


# =========================
# CORE STREAM
# =========================
def sftp_to_ftp_stream(
    sftp: paramiko.SFTPClient,
    remote_dir: str,
    remote_name: str,
    ftp: FTP,
    dest_name: str,
    blocksize: int = 1024 * 1024,
) -> None:
    remote_path = f"{remote_dir.rstrip('/')}/{remote_name}"
    with sftp.open(remote_path, "rb") as f:
        ftp.storbinary(f"STOR {dest_name}", f, blocksize=blocksize)


def sftp_to_ftp_batch(
    sftp: paramiko.SFTPClient,
    remote_dir: str,
    files: List[paramiko.SFTPAttributes],
    ftp: FTP,
    ftp_cfg: NetunnaFtpConfig,
    log,
    blocksize: int = 1024 * 1024,
    retry_per_file: int = 2,
    noop_every: int = 1,
) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Mantém o comportamento original (retry, noop, fallback 550, reconecta),
    e AGORA retorna (enviados, erros) para o retorno final do processo.
    """
    ftp_cwd_safe(ftp, ftp_cfg.pasta_destino)

    total = len(files)
    erros: List[Tuple[str, str]] = []
    enviados = 0

    for idx, attr in enumerate(files, 1):
        original = attr.filename
        dest = original
        last_err = None
        ok = False

        for attempt in range(1, retry_per_file + 2):
            try:
                log(
                    f"[{idx}/{total}] Transferindo: {dest} (tentativa {attempt}/{retry_per_file + 1})"
                )
                sftp_to_ftp_stream(
                    sftp=sftp,
                    remote_dir=remote_dir,
                    remote_name=original,
                    ftp=ftp,
                    dest_name=dest,
                    blocksize=blocksize,
                )
                enviados += 1
                ok = True

                if noop_every > 0 and (idx % noop_every == 0):
                    ftp_noop_safe(ftp)

                if dest != original:
                    log(f"[{idx}/{total}] Nome alternativo usado: {original} -> {dest}")
                break

            except Exception as e:
                last_err = e
                msg = str(e)

                # Se 550 e era o nome original, tenta fallback uma vez
                if "550" in msg and dest == original:
                    alt = ftp_safe_name(original)
                    if alt != original:
                        log(
                            f"[{idx}/{total}] FTP recusou nome original (550). Tentando nome alternativo: {alt}"
                        )
                        dest = alt
                        continue

                # tenta NOOP
                ftp_noop_safe(ftp)

                # tenta reconectar FTP
                try:
                    try:
                        ftp.quit()
                    except Exception:
                        pass
                    ftp = ftp_connect(ftp_cfg)
                    ftp_cwd_safe(ftp, ftp_cfg.pasta_destino)
                except Exception:
                    time.sleep(2)

        if not ok:
            erros.append((original, str(last_err)))
            log(f"[{idx}/{total}] ERRO ao transferir: {original} -> {last_err}")

    log(
        f"Transferência concluída: {enviados} sucesso, {len(erros)} erro(s), total {total}"
    )
    if erros:
        log("Arquivos com erro:")
        for n, m in erros:
            log(f" - {n} | {m}")

    return enviados, erros


# =========================
# PROCESSO
# =========================
async def sftp_equals_netunna(task):
    def log(msg: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

    log("Iniciando processo")

    sftp = None
    transport = None
    ftp = None

    try:
        equals_cfg = await load_equals_ftp_cfg(get_config_by_name, log)
        netunna_cfg = await load_netunna_ftp_cfg(get_config_by_name, log)

        log("Conectando no SFTP (Equals)")
        sftp, transport = sftp_connect(equals_cfg, log)

        # lista D-1
        sftp.chdir(equals_cfg.pasta_remota)
        ref = (datetime.now() - timedelta(days=1)).date()

        items = sftp.listdir_attr(".")
        files = [
            f
            for f in items
            if is_sftp_file(f) and datetime.fromtimestamp(f.st_mtime).date() == ref
        ]

        log(f"Arquivos D-1 encontrados: {len(files)}")

        if not files:
            msg = "Nenhum arquivo D-1 encontrado"
            log(msg)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno=msg,
                status=RpaHistoricoStatusEnum.Sucesso,
            )

        log("Conectando no FTP (Netunna)")
        ftp = ftp_connect(netunna_cfg)

        log(f"Iniciando stream SFTP -> FTP para destino: {netunna_cfg.pasta_destino}")
        enviados, erros = sftp_to_ftp_batch(
            sftp=sftp,
            remote_dir=equals_cfg.pasta_remota,
            files=files,
            ftp=ftp,
            ftp_cfg=netunna_cfg,
            log=log,
            blocksize=1024 * 1024,
            retry_per_file=2,
            noop_every=1,
        )

        # Retorno final do processo
        if erros:
            observacao = f"[FALHA PARCIAL] {enviados} enviado(s) com sucesso, {len(erros)} erro(s)."
            logger.error(observacao)
            console.print(observacao, style="bold red")
            # (Opcional) acrescenta uma lista curta no retorno
            detalhes = "\n".join([f"- {n}: {m}" for n, m in erros[:10]])
            if len(erros) > 10:
                detalhes += f"\n... e mais {len(erros) - 10} erro(s)."
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"{observacao}\n{detalhes}".strip(),
                status=RpaHistoricoStatusEnum.Falha,
                tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        log("Processo finalizado com sucesso")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Arquivos movidos com sucesso!",
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    except Exception as ex:
        observacao = f"[ERRO GERAL] Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )

    finally:
        try:
            if ftp:
                ftp.quit()
        except Exception:
            pass
        try:
            if sftp:
                sftp.close()
        except Exception:
            pass
        try:
            if transport:
                transport.close()
        except Exception:
            pass
