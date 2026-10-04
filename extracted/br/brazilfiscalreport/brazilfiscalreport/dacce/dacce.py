# Copyright (C) 2021-2022 Edson Bernardino <edsones at yahoo.com.br>
# Copyright (C) 2024 Engenere - Antônio S. Pereira Neto <neto@engenere.one>

import warnings
import xml.etree.ElementTree as ET
from io import BytesIO

from barcode.codex import Code128
from barcode.writer import SVGWriter

from ..utils import (
    chunks,
    format_cpf_cnpj,
    get_date_utc,
    get_tag_text,
)
from ..xfpdf import xFPDF

URL = ".//{http://www.portalfiscal.inf.br/nfe}"

# cStat of an event registered by the SEFAZ: 135 (registered and linked to the
# NF-e) and 136 (registered, but not linked to the NF-e)
REGISTERED_STATUS = ("135", "136")


def _join(separator, *parts):
    """Join the non-empty parts, so missing data leaves no stray separator."""
    return separator.join(str(part).strip() for part in parts if part)


class DaCCe(xFPDF):
    """
    Document generation:
    DACCe - Documento Auxiliar da Carta de Correção Eletrônica
    """

    def __init__(self, xml=None, emitente=None, image=None):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(auto=False, margin=10.0)
        self.set_title("DACCe")

        root = ET.fromstring(xml)
        det_event = root.find(f"{URL}detEvento")
        inf_event = root.find(f"{URL}infEvento")
        ret_event = root.find(f"{URL}retEvento")
        inf_ret_event = None
        if ret_event is not None:
            inf_ret_event = ret_event.find(f"{URL}infEvento")

        c_stat = get_tag_text(node=inf_ret_event, url=URL, tag="cStat")
        n_prot = get_tag_text(node=inf_ret_event, url=URL, tag="nProt")
        registered = c_stat in REGISTERED_STATUS and bool(n_prot)

        self.add_page(orientation="P", format="A4")

        # Watermark (drawn first, so the text stays on top of it): homologation
        # events and events the SEFAZ did not register have no fiscal value
        tp_amb = get_tag_text(node=inf_ret_event, url=URL, tag="tpAmb") or get_tag_text(
            node=inf_event, url=URL, tag="tpAmb"
        )
        if tp_amb == "2" or not registered:
            self._draw_watermark("SEM VALOR FISCAL")

        self._draw_issuer(emitente or {}, inf_event, image)

        # Evento
        self.set_font("Helvetica", "B", 10)
        self.set_xy(x=90, y=12)
        self.cell(w=110, h=5, text="Representação Gráfica de CC-e", align="C")
        self.set_font("Helvetica", "I", 9)
        self.set_xy(x=90, y=17)
        self.cell(w=110, h=4, text="(Carta de Correção Eletrônica)", align="C")

        self.set_font("Helvetica", "", 8)
        event_id = (inf_event.attrib.get("Id") or "").removeprefix("ID")
        self.text(x=92, y=26, text=f"ID do Evento: {event_id}")

        n_seq = get_tag_text(node=inf_event, url=URL, tag="nSeqEvento")
        self.text(x=92, y=30.5, text=f"Sequência do Evento: {n_seq or ''}")

        dt, hr = get_date_utc(
            get_tag_text(node=inf_event, url=URL, tag="dhEvento") or ""
        )
        self.text(x=92, y=35, text=f"Criado em: {dt} {hr}")

        if registered:
            dt, hr = get_date_utc(
                get_tag_text(node=inf_ret_event, url=URL, tag="dhRegEvento") or ""
            )
            text = f"Protocolo: {n_prot} - Registrado na SEFAZ em: {dt} {hr}"
        else:
            text = "Evento não registrado na SEFAZ"
            if c_stat:
                text += f" (status {c_stat})"
        self.text(x=92, y=39.5, text=text)

        # Destinatário
        self.rect(x=10, y=47, w=190, h=50, style="")
        self.line(10, 83, 200, 83)

        self.set_xy(x=11, y=48)
        text = (
            "De acordo com as determinações legais vigentes, vimos por "
            "meio desta comunicar-lhe que a Nota Fiscal, "
            "abaixo referenciada, contém irregularidades que estão "
            "destacadas e suas respectivas correções, solicitamos que "
            "sejam aplicadas essas correções ao executar seus "
            "lançamentos fiscais."
        )

        self.set_font("Helvetica", "", 8)
        self.multi_cell(w=185, h=4, text=text, border=0, align="L", fill=False)

        key = get_tag_text(node=inf_event, url=URL, tag="chNFe")

        # Generate a Code128 Barcode as SVG:
        svg_img_bytes = BytesIO()
        Code128(key, writer=SVGWriter()).write(
            svg_img_bytes, options={"write_text": False}
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self.image(svg_img_bytes, x=127, y=60, w=73, h=8)

        self.set_font("Helvetica", "", 7)
        self.text(x=130, y=78, text=" ".join(chunks(key, 4)))

        self.set_font("Helvetica", "B", 9)

        cnpj_dest = get_tag_text(node=inf_ret_event, url=URL, tag="CNPJDest")
        cpf_dest = get_tag_text(node=inf_ret_event, url=URL, tag="CPFDest")
        if cnpj_dest or cpf_dest:
            label = "CNPJ" if cnpj_dest else "CPF"
            doc_dest = format_cpf_cnpj(cnpj_dest or cpf_dest)
            self.text(x=12, y=71, text=f"{label} Destinatário:  {doc_dest}")

        text = (
            f"Nota Fiscal: {int(key[25:34]):011,}".replace(",", ".")
            + f" - Série: {key[22:25]}"
        )

        self.text(x=12, y=76, text=text)

        self._fit_multi_cell(
            x=11,
            y=84,
            w=185,
            h=12.5,
            text=get_tag_text(node=det_event, url=URL, tag="xCondUso") or "",
            style="I",
            size=7,
            line_height=3,
            min_size=5,
        )

        # Correções
        self.set_font("Helvetica", "B", 9)
        self.text(x=11, y=103, text="CORREÇÕES A SEREM CONSIDERADAS")

        self.rect(x=10, y=104, w=190, h=170, style="")

        text = get_tag_text(node=det_event, url=URL, tag="xCorrecao") or ""
        # Some issuers send the line breaks as a literal backslash + n
        text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
        # The footer starts at y=265: shrink the text instead of running over it
        self._fit_multi_cell(
            x=11,
            y=106,
            w=185,
            h=158,
            text=text,
            style="B",
            size=9,
            line_height=4,
            min_size=6,
        )

        self.set_xy(x=11, y=265)
        text = (
            "Este documento é uma representação gráfica da CC-e e "
            "foi impresso apenas para sua informação e não possui validade "
            "fiscal.\nA CC-e deve ser recebida e mantida em arquivo "
            "eletrônico XML e pode ser consultada através dos portais "
            "das SEFAZ."
        )

        self.set_font("Helvetica", "I", 8)
        self.multi_cell(w=185, h=4, text=text, border=0, align="C", fill=False)

    def _draw_issuer(self, emitente, inf_event, image):
        """
        Draw the issuer box. The CC-e XML only carries the issuer CNPJ/CPF (the
        event author); name, address and IE come from the ``emitente`` dict.
        """
        self.rect(x=10, y=10, w=190, h=33, style="")
        self.line(90, 10, 90, 43)

        cnpj = get_tag_text(node=inf_event, url=URL, tag="CNPJ")
        cpf = get_tag_text(node=inf_event, url=URL, tag="CPF")
        doc = ""
        if cnpj or cpf:
            doc = f"{'CNPJ' if cnpj else 'CPF'}: {format_cpf_cnpj(cnpj or cpf)}"
        ie = emitente.get("ie")

        name = _join("", emitente.get("nome"))
        address = "\n".join(
            line
            for line in (
                _join("", emitente.get("end")),
                _join(" - ", emitente.get("bairro"), emitente.get("cep")),
                _join(
                    " ",
                    _join(" - ", emitente.get("cidade"), emitente.get("uf")),
                    emitente.get("fone"),
                ),
                _join("  ", doc, f"IE: {ie}" if ie else ""),
            )
            if line
        )

        # Box interior, with 1 mm of padding: x 11-89, y 11-42
        if image:
            self.image(image, 12, 12, 12)
            name_x, name_w = 25, 64
        else:
            name_x, name_w = 11, 78

        self.set_font("Helvetica", "B", 10)
        name_h = 4 * len(self._lines(name, name_w, 4))
        self.set_font("Helvetica", "", 8)
        address_lines = len(self._lines(address, 78, 4))

        if image:
            # Name centered beside the logo, address below both
            name_y = max(11, 18 - name_h / 2)
            address_y = max(25, name_y + name_h + 1)
        else:
            # Name and address centered together in the box
            block_h = name_h + 1 + 4 * address_lines
            name_y = max(11, 10 + (33 - block_h) / 2)
            address_y = name_y + name_h + 1
        # Tighten the address lines when they do not fit in the box
        address_lh = 4
        if address_lines:
            address_lh = min(4, (42 - address_y) / address_lines)

        self.set_xy(x=name_x, y=name_y)
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(w=name_w, h=4, text=name, border=0, align="C", fill=False)
        self.set_xy(x=11, y=address_y)
        self.set_font("Helvetica", "", 8)
        self.multi_cell(
            w=78, h=address_lh, text=address, border=0, align="C", fill=False
        )

    def _lines(self, text, w, h):
        """Lines ``multi_cell`` would print with the current font."""
        if not text:
            return []
        return self.multi_cell(w=w, h=h, text=text, dry_run=True, output="LINES")

    def _fit_multi_cell(self, x, y, w, h, text, style, size, line_height, min_size):
        """
        Write ``text`` in a box of height ``h``, shrinking the font (down to
        ``min_size``) until it fits. Text that still does not fit is cut, and
        the last line ends with an ellipsis.
        """
        for font_size in range(size, min_size - 1, -1):
            lh = line_height * font_size / size
            self.set_font("Helvetica", style, font_size)
            lines = self._lines(text, w, lh)
            if len(lines) * lh <= h:
                break
        else:
            lines = lines[: int(h // lh)]
            last = lines[-1]
            while last and self.get_string_width(last + "…") > w - 2 * self.c_margin:
                last = last[:-1]
            lines[-1] = last + "…"
            text = "\n".join(lines)

        self.set_xy(x=x, y=y)
        self.multi_cell(w=w, h=lh, text=text, border=0, align="L", fill=False)

    def _draw_watermark(self, watermark_text):
        """Draw a diagonal watermark, as the DANFE does."""
        font_size = 50
        self.set_font("Helvetica", "B", font_size)
        width = self.get_string_width(watermark_text)
        height = font_size * 0.25
        x_center = (self.w - width) / 2
        y_center = (self.h + height) / 2
        self.set_text_color(r=220, g=150, b=150)
        with self.rotation(55, x_center + (width / 2), y_center - (height / 2)):
            self.text(x_center, y_center, watermark_text)
        self.set_text_color(r=0, g=0, b=0)
