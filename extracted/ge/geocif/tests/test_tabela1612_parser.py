"""Unit tests for geocif.data_prep.convert_tabela1612 (SIDRA Tabela 1612 parser).

Covers: 3 stacked variable blocks, paired year/product headers, MU/BR level
filtering, state-code prefix filtering, missing-data markers, kg/ha -> t/ha
conversion, and the production/area fallback when Rendimento is absent.
"""

import textwrap

import numpy as np
import pandas as pd
import pytest

from geocif.data_prep.convert_tabela1612 import build_wide, parse_sidra_blocks


@pytest.fixture()
def sidra_csv(tmp_path):
    text = textwrap.dedent('''\
        "Tabela 1612 - Área plantada, área colhida, ..."
        "Variável - Área colhida (Hectares)"
        "Nível","Cód.","Brasil e Município","Ano x Produto das lavouras temporárias"
        "Nível","Cód.","Brasil e Município","1990",,"1991",
        "Nível","Cód.","Brasil e Município","Total","Soja (em grão)","Total","Soja (em grão)"
        "BR","1","Brasil","999","500","999","600"
        "MU","5100201","Água Boa (MT)","100","50","110","60"
        "MU","5100250","Alta Floresta (MT)","70","-","80","20"
        "MU","4106902","Curitiba (PR)","10","5","10","5"
        "Variável - Quantidade produzida (Toneladas)"
        "Nível","Cód.","Brasil e Município","Ano x Produto das lavouras temporárias"
        "Nível","Cód.","Brasil e Município","1990",,"1991",
        "Nível","Cód.","Brasil e Município","Total","Soja (em grão)","Total","Soja (em grão)"
        "MU","5100201","Água Boa (MT)","300","150","330","192"
        "MU","5100250","Alta Floresta (MT)","210","-","240","50"
        "Variável - Rendimento médio da produção (Quilogramas por Hectare)"
        "Nível","Cód.","Brasil e Município","Ano x Produto das lavouras temporárias"
        "Nível","Cód.","Brasil e Município","1990",,"1991",
        "Nível","Cód.","Brasil e Município","Total","Soja (em grão)","Total","Soja (em grão)"
        "MU","5100201","Água Boa (MT)","3000","3000","3000","3200"
        "MU","5100250","Alta Floresta (MT)","3000","...","3000","-"
        "1 - Os municípios sem informação não aparecem nas listas;"
        ''')
    path = tmp_path / "tabela1612.csv"
    path.write_text(text, encoding="utf-8-sig")
    return path


@pytest.fixture()
def lookup():
    return pd.DataFrame({
        "CD_MUN": ["5100201", "5100250"],
        "NM_MUN": ["Água Boa", "Alta Floresta"],
        "ADM2_NAME": ["mato grosso agua boa", "mato grosso alta floresta"],
        "admin_2": ["mato_grosso_agua_boa", "mato_grosso_alta_floresta"],
    })


def test_parses_three_blocks_mt_only(sidra_csv):
    blocks = parse_sidra_blocks(sidra_csv, "Soja (em grão)", code_prefix="51")
    assert set(blocks) == {"area", "production", "yield_kg_ha"}
    area = blocks["area"]
    # 2 MT municipalities x 2 years; Curitiba (41...) and the BR row excluded
    assert len(area) == 4
    assert set(area["code"]) == {"5100201", "5100250"}
    assert set(area["year"]) == {1990, 1991}
    agua_1990 = area[(area.code == "5100201") & (area.year == 1990)]["value"].item()
    assert agua_1990 == 50.0


def test_missing_markers_become_nan(sidra_csv):
    blocks = parse_sidra_blocks(sidra_csv, "Soja (em grão)", code_prefix="51")
    alta = blocks["area"].query("code == '5100250'").set_index("year")["value"]
    assert np.isnan(alta[1990])          # "-"
    assert alta[1991] == 20.0


def test_build_wide_units_and_fallback(sidra_csv, lookup):
    blocks = parse_sidra_blocks(sidra_csv, "Soja (em grão)", code_prefix="51")
    wide = build_wide(blocks, lookup, "Brazil", "Mato Grosso", "Soybean")

    agua_1991 = wide[(wide.admin_2 == "mato_grosso_agua_boa")
                     & (wide.harvest_year == 1991)].iloc[0]
    assert agua_1991["yield"] == pytest.approx(3.2)        # kg/ha -> t/ha
    assert agua_1991["area"] == 60.0
    assert agua_1991["production"] == 192.0
    assert agua_1991["product"] == "Soybean"
    assert agua_1991["season_name"] == "Main"
    assert agua_1991["qc_flag"] == 0
    assert agua_1991["num_ID"] == 5100201

    # Alta Floresta 1991: Rendimento is "-" -> fallback production/area = 50/20
    alta_1991 = wide[(wide.admin_2 == "mato_grosso_alta_floresta")
                     & (wide.harvest_year == 1991)].iloc[0]
    assert alta_1991["yield"] == pytest.approx(2.5)

    # Alta Floresta 1990: everything missing -> row dropped entirely
    assert wide[(wide.admin_2 == "mato_grosso_alta_floresta")
                & (wide.harvest_year == 1990)].empty


def test_trailing_year_without_pad_cell(tmp_path, lookup):
    """SIDRA's years row ends ON the last year (no trailing empty cell) while
    the products row still has that year's full Total/Soja pair — the final
    year's Soja column must not be dropped (regression: 2024 vanished)."""
    text = textwrap.dedent('''\
        "Tabela 1612 - ..."
        "Variável - Rendimento médio da produção (Quilogramas por Hectare)"
        "Nível","Cód.","Brasil e Município","Ano x Produto das lavouras temporárias"
        "Nível","Cód.","Brasil e Município","2023",,"2024"
        "Nível","Cód.","Brasil e Município","Total","Soja (em grão)","Total","Soja (em grão)"
        "MU","5100201","Água Boa (MT)","3000","3100","3000","3300"
        ''')
    path = tmp_path / "t.csv"
    path.write_text(text, encoding="utf-8-sig")
    blocks = parse_sidra_blocks(path, "Soja (em grão)", code_prefix="51")
    vals = blocks["yield_kg_ha"].set_index("year")["value"]
    assert vals[2023] == 3100.0
    assert vals[2024] == 3300.0


def test_unmatched_codes_dropped(sidra_csv, lookup):
    blocks = parse_sidra_blocks(sidra_csv, "Soja (em grão)", code_prefix="51")
    lookup_missing = lookup[lookup.CD_MUN != "5100250"]
    wide = build_wide(blocks, lookup_missing, "Brazil", "Mato Grosso", "Soybean")
    assert set(wide["admin_2"]) == {"mato_grosso_agua_boa"}
