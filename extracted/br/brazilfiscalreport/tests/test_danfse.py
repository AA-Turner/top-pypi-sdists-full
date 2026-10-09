import pytest

from brazilfiscalreport.danfse import (
    Danfse,
    DanfseConfig,
    Margins,
)
from tests.conftest import assert_pdf_equal, get_pdf_output_path


@pytest.fixture
def load_danfse(load_xml):
    def _load_danfse(filename, config=None):
        xml_content = load_xml(f"danfse/{filename}")
        return Danfse(xml=xml_content, config=config)

    return _load_danfse


def test_danfse_default(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
    )
    danfse = load_danfse("nfse_test_prod.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_default_prod")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_default_hom(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
    )
    danfse = load_danfse("nfse_test_hom.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_default_hom")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_intermediary(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
    )
    danfse = load_danfse("nfse_test_interm.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_intermediary")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_minimal(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
    )
    danfse = load_danfse("nfse_test_minimal.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_minimal")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_rtc(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
        display_canhoto=True,
    )
    danfse = load_danfse("nfse_test_rtc.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_rtc")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_replaced(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
        watermark_replaced=True,
    )
    danfse = load_danfse("nfse_test_rtc.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_replaced")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_cancelled(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2), watermark_cancelled=True
    )
    danfse = load_danfse("nfse_test_prod.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_cancelled_prod")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_cancelled_hom(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2), watermark_cancelled=True
    )
    danfse = load_danfse("nfse_test_hom.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_cancelled_hom")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_cnpj_alfanumerico(tmp_path, load_danfse):
    config = DanfseConfig(
        margins=Margins(top=2, right=2, bottom=2, left=2),
    )
    danfse = load_danfse("nfse_test_cnpj_alfanumerico.xml", config=config)
    pdf_path = get_pdf_output_path("danfse", "danfse_cnpj_alfanumerico")
    assert_pdf_equal(danfse, pdf_path, tmp_path)


def test_danfse_rtc_valid_xsd(tmp_path, load_danfse):
    """IBS/CBS block read from a NFS-e that is valid against the official XSD.

    The fixture `nfse_rtc_valid.xml` carries a real `infNFSe/IBSCBS` group and
    was validated against `Schemas/1.01/NFSe_v1.01.xsd` from the package
    `nfse-esquemas_xsd-v1-01-20260209.zip` (gov.br/nfse, documentacao-tecnica,
    documentacao-atual). The XSD is not vendored. The only deviation is the
    pattern of `TSSerieDPS` (`^0{0,4}\\d{1,5}$`), whose literal anchors make
    every value fail in strict XSD engines; validate with that pattern written
    without `^` and `$`. The `ds:Signature` is a structural placeholder.
    """
    config = DanfseConfig(margins=Margins(top=2, right=2, bottom=2, left=2))
    danfse = load_danfse("nfse_rtc_valid.xml", config=config)

    assert danfse.data["ibscbs"] == {
        "cst_cclasstrib": "000 / 000001",
        "ind_op": "010101 / 3550308 / São Paulo / SP",
        "exclusions": "R$ 460,00",
        "bc_after": "R$ 9.040,00",
        "red_aliq": "10,00% / 10,00% / 10,00%",
        "aliq_ibs": "5,00% / 2,00%",
        "aliq_efet_mun": "1,80%",
        "v_ibs_mun": "R$ 162,72",
        "aliq_efet_uf": "4,50%",
        "v_ibs_uf": "R$ 406,80",
        "v_ibs_tot": "R$ 569,52",
        "aliq_cbs": "8,80%",
        "aliq_efet_cbs": "7,92%",
        "v_cbs": "R$ 715,97",
    }
    assert danfse.data["total_value"]["total_ibscbs"] == "R$ 1.285,49"
    assert danfse.data["total_value"]["net_value_ibscbs"] == "R$ 10.201,49"

    pdf_path = get_pdf_output_path("danfse", "danfse_rtc_valid")
    assert_pdf_equal(danfse, pdf_path, tmp_path)
