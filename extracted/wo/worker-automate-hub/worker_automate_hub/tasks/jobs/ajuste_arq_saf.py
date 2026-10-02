import os
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, Set, Tuple

import pandas as pd
from rich.console import Console

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_sap_dto import RpaProcessoSapDTO

console = Console()


class ProcessarArquivosSafx:

    def __init__(
        self,
        task: RpaProcessoSapDTO,
        caminho_excel: Path = Path("C:/DADOS_SAFX.xlsx"),
        pasta_base: Path = Path("C:/"),
    ):
        self.task = task
        self.caminho_excel = caminho_excel
        self.pasta_base = pasta_base

        console.print("[INIT] ProcessarArquivosSafx inicializado.")
        console.print(f"[INIT] Caminho Excel: {self.caminho_excel}")
        console.print(f"[INIT] Pasta Base: {self.pasta_base}")

    def retorno_sucesso(self, msg: str) -> RpaRetornoProcessoDTO:
        console.print(f"[SUCESSO] {msg}")
        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno=msg,
            status=RpaHistoricoStatusEnum.Sucesso,
        )

    def retorno_erro(self, msg: str) -> RpaRetornoProcessoDTO:
        console.print(f"[ERRO] {msg}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    # ==========================================================
    # LEITURA DE EXCEL (MAPEAMENTOS DE ARLA E BOMBAS)
    # ==========================================================
    def obter_tanques_arla(self) -> Set[Tuple[str, str]]:
        if not self.caminho_excel.exists():
            raise FileNotFoundError(
                f"Arquivo Excel não encontrado: {self.caminho_excel}"
            )

        excel_file = pd.ExcelFile(self.caminho_excel)
        sheet_names = excel_file.sheet_names

        nome_aba = next(
            (
                name
                for name in sheet_names
                if "arla" in name.lower() and "tanque" in name.lower()
            ),
            "Tanques de Arla" if "Tanques de Arla" in sheet_names else sheet_names[0],
        )

        df = pd.read_excel(self.caminho_excel, sheet_name=nome_aba)
        col_empresa = [c for c in df.columns if "empresa" in str(c).lower()][0]
        col_tanque = [c for c in df.columns if "tanque" in str(c).lower()][0]

        tanques_arla = set()
        for _, row in df.iterrows():
            empresa = str(row[col_empresa]).strip().lstrip("0")
            tanque = str(row[col_tanque]).strip().lstrip("0")
            if (
                empresa
                and tanque
                and empresa.lower() != "nan"
                and tanque.lower() != "nan"
            ):
                tanques_arla.add((empresa, tanque))

        return tanques_arla

    def obter_bicos_arla(self) -> Set[Tuple[str, str]]:
        if not self.caminho_excel.exists():
            raise FileNotFoundError(
                f"Arquivo Excel não encontrado: {self.caminho_excel}"
            )

        excel_file = pd.ExcelFile(self.caminho_excel)
        sheet_names = excel_file.sheet_names

        nome_aba = next(
            (
                name
                for name in sheet_names
                if "arla" in name.lower() and "bico" in name.lower()
            ),
            "Bicos de Arla" if "Bicos de Arla" in sheet_names else sheet_names[0],
        )

        df = pd.read_excel(self.caminho_excel, sheet_name=nome_aba)
        col_empresa = [c for c in df.columns if "empresa" in str(c).lower()][0]
        col_bico = [c for c in df.columns if "bico" in str(c).lower()][0]

        bicos_arla = set()
        for _, row in df.iterrows():
            empresa = str(row[col_empresa]).strip().lstrip("0")
            bico = str(row[col_bico]).strip().lstrip("0")
            if empresa and bico and empresa.lower() != "nan" and bico.lower() != "nan":
                bicos_arla.add((empresa, bico))

        return bicos_arla

    def obter_mapa_bicos_bombas(self) -> Dict[Tuple[str, str], str]:
        if not self.caminho_excel.exists():
            raise FileNotFoundError(
                f"Arquivo Excel não encontrado: {self.caminho_excel}"
            )

        excel_file = pd.ExcelFile(self.caminho_excel)
        sheet_names = excel_file.sheet_names

        nome_aba = next(
            (
                name
                for name in sheet_names
                if "bomba" in name.lower() and "bico" in name.lower()
            ),
            "Bicos x Bombas" if "Bicos x Bombas" in sheet_names else sheet_names[0],
        )

        df = pd.read_excel(self.caminho_excel, sheet_name=nome_aba)
        col_empresa = [c for c in df.columns if "empresa" in str(c).lower()][0]
        col_bico = [c for c in df.columns if "bico" in str(c).lower()][0]
        col_bomba = [c for c in df.columns if "bomba" in str(c).lower()][0]

        mapa_bombas = {}
        for _, row in df.iterrows():
            empresa = str(row[col_empresa]).strip().lstrip("0")
            bico = str(row[col_bico]).strip().lstrip("0")
            bomba = str(row[col_bomba]).strip()

            if empresa and bico and bomba and empresa.lower() != "nan":
                mapa_bombas[(empresa, bico)] = bomba

        return mapa_bombas

    # ==========================================================
    # REGRAS SAFX123
    # ==========================================================
    def processar_safx123(
        self, caminho_safx: Path, tanques_arla: Set[Tuple[str, str]]
    ) -> int:
        with open(caminho_safx, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()

        linhas_filtradas = []
        removidas = 0

        for linha in linhas:
            colunas = re.split(r"\t+|\s{2,}", linha.strip())

            if len(colunas) >= 4:
                empresa = colunas[1].strip().lstrip("0")
                tanque = colunas[3].strip().lstrip("0")

                if (empresa, tanque) in tanques_arla:
                    removidas += 1
                    continue

            linhas_filtradas.append(linha)

        with open(caminho_safx, "w", encoding="utf-8", newline="") as f:
            f.writelines(linhas_filtradas)

        return removidas

    # ==========================================================
    # REGRAS SAFX2060
    # ==========================================================
    def processar_safx2060(self, caminho_safx: Path) -> int:
        with open(caminho_safx, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()

        linhas_filtradas = []
        removidas = 0

        for linha in linhas:
            colunas = re.split(r"\t+|\s{2,}", linha.strip())

            if len(colunas) >= 6:
                cod_produto = colunas[5].strip()
                if cod_produto == "2000099":
                    removidas += 1
                    continue

            linhas_filtradas.append(linha)

        with open(caminho_safx, "w", encoding="utf-8", newline="") as f:
            f.writelines(linhas_filtradas)

        return removidas

    # ==========================================================
    # REGRAS SAFX124
    # ==========================================================
    def processar_safx124(
        self,
        caminho_safx: Path,
        bicos_arla: Set[Tuple[str, str]],
        mapa_bombas: Dict[Tuple[str, str], str],
    ) -> Tuple[int, int]:
        with open(caminho_safx, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()

        linhas_filtradas = []
        removidas = 0
        bombas_alteradas = 0

        for linha in linhas:
            # Mantém os delimitadores para remontar a linha na mesma formatação
            partes = re.split(r"(\t+|\s{2,})", linha.rstrip("\r\n"))

            # Extrai apenas os valores das colunas para validação
            colunas_valores = [p for i, p in enumerate(partes) if i % 2 == 0]

            if len(colunas_valores) >= 10:
                empresa = colunas_valores[1].strip().lstrip("0")
                bico = colunas_valores[4].strip().lstrip("0")

                # Regra 2: Remover Bicos ARLA
                if (empresa, bico) in bicos_arla:
                    removidas += 1
                    continue

                # Regra 1: Substituir Coluna 10 (índice 9 nos valores) por '@'
                # Na lista com delimitadores (partes), cada coluna N tem índice (N-1)*2
                partes[18] = "@"

                # Regra 3: Substituir Coluna 4 (índice 3 nos valores) pelo número da Bomba
                if (empresa, bico) in mapa_bombas:
                    bomba_val = mapa_bombas[(empresa, bico)].zfill(10)
                    partes[6] = bomba_val
                    bombas_alteradas += 1

            linhas_filtradas.append("".join(partes) + "\n")

        with open(caminho_safx, "w", encoding="utf-8", newline="") as f:
            f.writelines(linhas_filtradas)

        return removidas, bombas_alteradas

    # ==========================================================
    # FLUXO PRINCIPAL
    # ==========================================================
    async def iniciar(self) -> RpaRetornoProcessoDTO:
        step = "INIT"

        try:
            step = "BUSCAR_ARQUIVOS"
            todos_arquivos = [
                f
                for f in self.pasta_base.glob("*SAFX*")
                if f.is_file() and not f.name.startswith("~$")
            ]

            arquivos_123 = [f for f in todos_arquivos if "SAFX123" in f.name]
            arquivos_124 = [f for f in todos_arquivos if "SAFX124" in f.name]
            arquivos_2060 = [f for f in todos_arquivos if "SAFX2060" in f.name]

            if not arquivos_123 and not arquivos_124 and not arquivos_2060:
                msg = f"Nenhum arquivo SAFX123, SAFX124 ou SAFX2060 foi encontrado na pasta {self.pasta_base}."
                console.print(f"[AVISO] {msg}")
                return self.retorno_sucesso(msg)

            detalhes = []
            total_removido = 0

            # 1) PROCESSA SAFX123
            if arquivos_123:
                step = "CARREGAR_EXCEL_SAFX123"
                tanques_arla = self.obter_tanques_arla()

                step = "PROCESSAR_SAFX123"
                for arq in arquivos_123:
                    console.print(f"[SAFX123] Processando arquivo: {arq.name}")
                    rem = self.processar_safx123(arq, tanques_arla)
                    total_removido += rem
                    detalhes.append(f"'{arq.name}': {rem} linhas ARLA removidas")

            # 2) PROCESSA SAFX124
            if arquivos_124:
                step = "CARREGAR_EXCEL_SAFX124"
                bicos_arla = self.obter_bicos_arla()
                mapa_bombas = self.obter_mapa_bicos_bombas()

                step = "PROCESSAR_SAFX124"
                for arq in arquivos_124:
                    console.print(f"[SAFX124] Processando arquivo: {arq.name}")
                    rem, bombas = self.processar_safx124(arq, bicos_arla, mapa_bombas)
                    total_removido += rem
                    detalhes.append(
                        f"'{arq.name}': {rem} bicos ARLA removidos, {bombas} bombas atualizadas e col 10 com @"
                    )

            # 3) PROCESSA SAFX2060
            if arquivos_2060:
                step = "PROCESSAR_SAFX2060"
                for arq in arquivos_2060:
                    console.print(f"[SAFX2060] Processando arquivo: {arq.name}")
                    rem = self.processar_safx2060(arq)
                    total_removido += rem
                    detalhes.append(
                        f"'{arq.name}': {rem} linhas prod 2000099 removidas"
                    )

            msg_sucesso = (
                f"Ajuste nos arquivos SAFX concluído com sucesso! "
                f"Total de registros removidos: {total_removido}. "
                f"Detalhes: {'; '.join(detalhes)}."
            )

            return self.retorno_sucesso(msg_sucesso)

        except Exception as e:
            tb = traceback.format_exc()
            msg = (
                f"Falha na rotina de ajuste de arquivos SAFX. "
                f"Etapa: {step}. Erro: {type(e).__name__}: {e}\n{tb}"
            )
            return self.retorno_erro(msg)


# ==========================================================
# FUNÇÃO DE ENTRADA DO WORKER
# ==========================================================
async def ajuste_arq_saf(task: RpaProcessoSapDTO) -> RpaRetornoProcessoDTO:
    console.print("[MAIN] Iniciando ajuste_arq_saf (SAFX123, SAFX124 e SAFX2060).")

    try:
        processor = ProcessarArquivosSafx(task=task)
        return await processor.iniciar()

    except Exception as ex:
        tb = traceback.format_exc()
        msg = f"Erro geral ao executar ajuste_arq_saf: {type(ex).__name__}: {ex}\n{tb}"
        console.print("[MAIN][ERRO] Exceção em ajuste_arq_saf.")
        console.print(tb)

        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )

    finally:
        console.print("[MAIN] Fim do processo.")
