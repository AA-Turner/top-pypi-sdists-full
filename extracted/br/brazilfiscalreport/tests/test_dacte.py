import re

import pytest

from brazilfiscalreport.dacte import (
    Dacte,
    DacteConfig,
    Margins,
    ReceiptPosition,
)
from tests.conftest import assert_pdf_equal, get_pdf_output_path


@pytest.fixture
def load_dacte(load_xml):
    def _load_dacte(filename, config=None):
        xml_content = load_xml(f"dacte/{filename}")
        return Dacte(xml=xml_content, config=config)

    return _load_dacte


@pytest.fixture(scope="module")
def default_dacte_config(logo_path):
    config = DacteConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
        logo=logo_path,
        receipt_pos=ReceiptPosition.TOP,
    )
    return config


def test_dacte_default(tmp_path, load_dacte):
    dacte = load_dacte("dacte_test_1.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_default")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_without_compl(tmp_path, load_dacte):
    dacte = load_dacte("dacte_test_without_compl.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_without_compl")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_overload(tmp_path, load_dacte):
    dacte_config = DacteConfig(margins=Margins(top=10, right=10, bottom=10, left=10))
    dacte = load_dacte("dacte_test_overload.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_overload")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_multi_pages(tmp_path, load_dacte):
    dacte = load_dacte("dacte_test_multi_pages.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_multi_pages")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_logo(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_test_1.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_logo")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_aquaviario(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_aquaviario_test.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_aquaviario")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_aereo(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_aereo_test.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_aereo")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_ferroviario(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_ferroviario_test.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_ferroviario")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_dutoviario(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_dutoviario_test.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_dutoviario")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_default_multimodal(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_multimodal_test.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_default_multimodal")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_tomador_outros(tmp_path, load_dacte, logo_path):
    dacte_config = DacteConfig(
        logo=logo_path,
    )
    dacte = load_dacte("dacte_tomador_outros.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_tomador_outros")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_watermark_cancelled_production(tmp_path, load_dacte):
    """Test watermark for cancelled DACTE in production environment"""
    dacte_config = DacteConfig(watermark_cancelled=True)
    dacte = load_dacte("dacte_test_1.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_watermark_cancelled_production")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_watermark_cancelled_homologation(tmp_path, load_dacte):
    """Test watermark for cancelled DACTE in homologation environment"""
    dacte_config = DacteConfig(watermark_cancelled=True)
    dacte = load_dacte("dacte_test_homolog.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_watermark_cancelled_homologation")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_watermark_homologation_only(tmp_path, load_dacte):
    """Test watermark for DACTE in homologation environment without cancellation"""
    dacte_config = DacteConfig(watermark_cancelled=False)
    dacte = load_dacte("dacte_test_homolog.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_watermark_homologation_only")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_reforma_tributaria(tmp_path, load_dacte):
    """Test DACTE with PIS/COFINS and IBS/CBS display (reforma tributária)."""
    dacte_config = DacteConfig(display_ibs_cbs=True)
    dacte = load_dacte("dacte_reforma_tributaria.xml", config=dacte_config)
    pdf_path = get_pdf_output_path("dacte", "dacte_reforma_tributaria")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_cnpj_alfanumerico(tmp_path, load_dacte):
    dacte = load_dacte("dacte_cnpj_alfanumerico.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_cnpj_alfanumerico")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_icms_st(tmp_path, load_dacte):
    """CT-e com ICMS retido por substituição tributária (CST 60)."""
    dacte = load_dacte("dacte_icms_st.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_icms_st")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_icms_st_le_vicmsstret(load_dacte):
    """A coluna ICMS ST vem de vICMSSTRet, não do vICMS.

    vICMSSTRet (grupo ICMS60) é o único campo de ST do leiaute do CT-e. Antes
    o campo repetia o vICMS, ou seja, imprimia o ICMS próprio como se fosse ST.
    """
    dacte = load_dacte("dacte_icms_st.xml")
    assert dacte.v_icms_st == "20,00"


def test_dacte_icms_st_zero_quando_nao_declarado(load_dacte):
    """Sem ST no XML (CST 00), a coluna é zero — não o ICMS próprio.

    Era o caso mais grave: um CT-e sem substituição tributária nenhuma exibia
    o vICMS na coluna ICMS ST, sugerindo uma ST que não existe.
    """
    dacte = load_dacte("dacte_test_1.xml")
    assert dacte.v_icms == "26,54"
    assert dacte.v_icms_st == "0,00"


# ---------------------------------------------------------------------------
# Reforma tributária (IBS/CBS) no DACTE
#
# A NT 2026.004 v1.00 trata só do leiaute XML (vTPrestLiq, regra do vTotDFe,
# ICMS previsto em pagamento antecipado) e não altera a impressão. O MOC do
# DACTE (Anexo II, v4.00) não tem campo de IBS/CBS. Os testes abaixo garantem
# que o DACTE gera corretamente com o XML novo, que o bloco opcional
# (display_ibs_cbs) é coerente com o XML e que nada é inventado.
# Fixtures validadas contra o XSD PL_CTe_400_NT2026.004 RTC_1.00 (SVRS).
# ---------------------------------------------------------------------------


def test_dacte_sem_reforma(tmp_path, load_dacte):
    """CT-e sem nada da reforma: o PDF não pode mudar."""
    dacte = load_dacte("dacte_sem_reforma.xml")
    pdf_path = get_pdf_output_path("dacte", "dacte_sem_reforma")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_rtc_aliquota_nominal_sem_gred(load_dacte):
    dacte = load_dacte("dacte_rtc_2027.xml")
    assert dacte.p_ibs_uf == "0,05"
    assert dacte.v_ibs_uf == "0,50"
    assert dacte.p_ibs_mun == "0,05"
    assert dacte.v_ibs_mun == "0,50"
    assert dacte.p_cbs == "8,80"
    assert dacte.v_cbs == "88,00"


def test_dacte_rtc_aliquota_efetiva_com_gred(load_dacte):
    """Com gRed, o % impresso é pAliqEfet (o que gerou o valor), não o nominal.

    Transporte aéreo regional (cClassTrib 200050): redução de 40%.
    """
    dacte = load_dacte("dacte_rtc_2027_gred.xml")
    assert dacte.p_ibs_uf == "0,03"
    assert dacte.v_ibs_uf == "3,60"
    assert dacte.p_ibs_mun == "0,03"
    assert dacte.v_ibs_mun == "3,60"
    assert dacte.p_cbs == "5,28"
    assert dacte.v_cbs == "633,60"


@pytest.mark.parametrize(
    "fixture", ["dacte_rtc_sem_ibscbs.xml", "dacte_sem_reforma.xml"]
)
def test_dacte_ibscbs_ausente_fica_em_branco(load_dacte, fixture):
    """Sem o grupo IBSCBS no XML não se imprime 0,00 inventado."""
    dacte = load_dacte(fixture, config=DacteConfig(display_ibs_cbs=True))
    for attr in (
        "p_ibs_uf",
        "v_ibs_uf",
        "p_ibs_mun",
        "v_ibs_mun",
        "p_cbs",
        "v_cbs",
    ):
        assert getattr(dacte, attr) == "", attr


def test_dacte_base_icms_nao_vem_do_ibscbs(load_dacte):
    """ICMS sem vBC (CST 40) com IBSCBS: a base do ICMS não é a base do IBS."""
    dacte = load_dacte("dacte_rtc_2027_gred.xml")
    assert dacte.cst == "40"
    assert dacte.vbc == "0,00"


def test_dacte_rtc_valor_total_e_vtprest(load_dacte):
    """Valor total é o vTPrest (IBS/CBS já dentro, sem somar de novo)."""
    dacte = load_dacte("dacte_rtc_2027.xml")
    assert dacte.v_tpprest == "1.089,00"
    assert dacte.v_rec == "1.089,00"


def _sem_tags(xml, *tags):
    for tag in tags:
        xml = re.sub(rf"\s*<{tag}>.*?</{tag}>", "", xml, flags=re.S)
    return xml


def test_dacte_rtc_campos_novos_nao_alteram_impressao(load_xml, tmp_path):
    """vTPrestLiq e vTotDFe são só leiaute: o PDF é igual sem eles."""
    xml = load_xml("dacte/dacte_rtc_sem_ibscbs.xml")
    com = Dacte(xml=xml)
    sem = Dacte(xml=_sem_tags(xml, "vTPrestLiq", "vTotDFe"))
    assert_pdf_equal(com, sem, tmp_path)


def test_dacte_rtc_sem_flag_nao_imprime_bloco_ibscbs(load_xml, tmp_path):
    """Sem display_ibs_cbs, o IBSCBS do XML não muda o PDF (compatibilidade)."""
    xml = load_xml("dacte/dacte_rtc_2027.xml")
    com = Dacte(xml=xml)
    sem = Dacte(xml=_sem_tags(xml, "IBSCBS", "vTPrestLiq", "vTotDFe"))
    assert_pdf_equal(com, sem, tmp_path)


def test_dacte_rtc_2027_pdf(tmp_path, load_dacte):
    dacte = load_dacte("dacte_rtc_2027.xml", config=DacteConfig(display_ibs_cbs=True))
    pdf_path = get_pdf_output_path("dacte", "dacte_rtc_2027")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_rtc_2027_gred_pdf(tmp_path, load_dacte):
    dacte = load_dacte(
        "dacte_rtc_2027_gred.xml", config=DacteConfig(display_ibs_cbs=True)
    )
    pdf_path = get_pdf_output_path("dacte", "dacte_rtc_2027_gred")
    assert_pdf_equal(dacte, pdf_path, tmp_path)


def test_dacte_rtc_sem_ibscbs_pdf(tmp_path, load_dacte):
    """Flag ligada e XML sem IBSCBS: bloco com valores em branco."""
    dacte = load_dacte(
        "dacte_rtc_sem_ibscbs.xml", config=DacteConfig(display_ibs_cbs=True)
    )
    pdf_path = get_pdf_output_path("dacte", "dacte_rtc_sem_ibscbs")
    assert_pdf_equal(dacte, pdf_path, tmp_path)
