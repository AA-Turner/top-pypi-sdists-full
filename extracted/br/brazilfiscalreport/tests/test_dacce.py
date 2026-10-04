import re

import pytest

from brazilfiscalreport.dacce import DaCCe
from tests.conftest import assert_pdf_equal, get_pdf_output_path


def test_dacce(tmp_path, load_xml, logo_path):
    emitente = {
        "nome": "EMPRESA LTDA",
        "end": "AV. TEST, 100",
        "bairro": "TEST",
        "cep": "88888-888",
        "cidade": "SÃO PAULO",
        "uf": "SP",
        "fone": "(11) 1234-5678",
    }
    xm_content = load_xml("dacce/xml_cce_1.xml")

    pdf_cce = DaCCe(xml=xm_content, emitente=emitente, image=logo_path)
    pdf_path = get_pdf_output_path("dacce", "cce")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_without_emitente(tmp_path, load_xml):
    xm_content = load_xml("dacce/xml_cce_1.xml")

    pdf_cce = DaCCe(xml=xm_content)
    pdf_path = get_pdf_output_path("dacce", "cce_no_emitente")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_cpf_recipient_and_issuer_ids(tmp_path, load_xml, logo_path):
    # Production event for an individual (CPFDest), with the official xCondUso
    # text: no watermark, "CPF Destinatário", issuer CNPJ (from the XML) and IE.
    emitente = {
        "nome": "EMPRESA LTDA",
        "end": "AV. TEST, 100",
        "bairro": "TEST",
        "cidade": "SÃO PAULO",
        "uf": "SP",
        "fone": "(11) 1234-5678",
        "ie": "123456789012",
    }
    xm_content = load_xml("dacce/xml_cce_cpf.xml")

    pdf_cce = DaCCe(xml=xm_content, emitente=emitente, image=logo_path)
    pdf_path = get_pdf_output_path("dacce", "cce_cpf")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


@pytest.mark.parametrize(
    "fixture",
    ["dacce/xml_cce_newlines_real.xml", "dacce/xml_cce_newlines_literal.xml"],
)
def test_dacce_correction_newlines(tmp_path, load_xml, fixture):
    # Real line breaks and a literal backslash + n (as some issuers send it)
    # must render the same: one line per line of the correction text.
    xm_content = load_xml(fixture)

    pdf_cce = DaCCe(xml=xm_content)
    pdf_path = get_pdf_output_path("dacce", "cce_newlines")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_issuer_cpf_rejected_event(tmp_path, load_xml):
    # Issuer identified by CPF, and an event the SEFAZ rejected (no nProt):
    # "CPF:" label for the issuer, no protocol and the "SEM VALOR FISCAL" mark
    # even in production.
    xm_content = (
        load_xml("dacce/xml_cce_cpf.xml")
        .replace("<CNPJ>01234567890123</CNPJ>", "<CPF>12345678909</CPF>")
        .replace("<cStat>135</cStat>", "<cStat>573</cStat>")
        .replace("<nProt>999999999999999</nProt>", "")
    )

    pdf_cce = DaCCe(xml=xm_content, emitente={"nome": "JOSE DA SILVA"})
    pdf_path = get_pdf_output_path("dacce", "cce_rejected")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_without_ret_evento(tmp_path, load_xml):
    # Event XML that was never sent (no retEvento): renders without the
    # recipient and protocol, marked as having no fiscal value.
    xm_content = re.sub(
        r"<retEvento.*</retEvento>",
        "",
        load_xml("dacce/xml_cce_cpf.xml"),
        flags=re.DOTALL,
    )

    pdf_cce = DaCCe(xml=xm_content)
    pdf_path = get_pdf_output_path("dacce", "cce_without_ret_evento")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_long_texts(tmp_path, load_xml, logo_path):
    # Long issuer data and a correction with more lines than the box holds:
    # the header stays inside its box and the text shrinks above the footer.
    emitente = {
        "nome": "EMPRESA DE COMERCIO E DISTRIBUICAO DE PRODUTOS ALIMENTICIOS LTDA",
        "end": "AVENIDA DOS ESTADOS UNIDOS DA AMERICA DO NORTE, 12345 - GALPAO 7",
        "bairro": "DISTRITO INDUSTRIAL",
        "cep": "88888-888",
        "cidade": "SÃO JOSÉ DOS CAMPOS",
        "uf": "SP",
        "fone": "(12) 3456-7890",
        "ie": "123456789012",
    }
    correction = "\\n".join(f"Item {i:02}: corrigido" for i in range(1, 46))
    xm_content = load_xml("dacce/xml_cce_cpf.xml").replace(
        "Correção: Dados fictícios adicionados.", correction
    )

    pdf_cce = DaCCe(xml=xm_content, emitente=emitente, image=logo_path)
    pdf_path = get_pdf_output_path("dacce", "cce_long_texts")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)


def test_dacce_emitente_partial_and_numeric(load_xml):
    # A config.yaml loads unquoted numbers as int and may leave keys out
    emitente = {"nome": "EMPRESA LTDA", "cep": 88888888, "fone": 1112345678, "ie": 1}

    DaCCe(xml=load_xml("dacce/xml_cce_1.xml"), emitente=emitente).output()
