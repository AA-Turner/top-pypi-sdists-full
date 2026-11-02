"""PDF-PLAN U13: forms and Fill & Sign on the permissive stack (PyPDFForm, pikepdf, Pillow). Never PyMuPDF.

- ``list_form_fields_bytes``: every AcroForm field with its type, value, options, page and box (visible page,
  points, origin top-left, the frame the viewer uses).
- ``fill_form_bytes``: fills text, date, checkbox, radio and dropdown fields with PyPDFForm. An unknown field name
  or a value the field cannot take is an error in plain words, never a silent skip.
- ``flatten_form_bytes``: burns the field appearances into the page and deletes the form (no fields left).
- ``place_marks_bytes``: Fill & Sign for a PDF that has no form: text, a date, a check mark and a signature picture
  placed on the page. Each is a form XObject tagged ``/MatrxMark`` so the placement can be read back.
- ``read_form_values_bytes`` / ``list_marks_bytes``: the read-back the forcing tests (and agents) use.

Certifying with a digital certificate (pyHanko) is NOT part of this unit: the e-sign stack has one platform seal
key (``services/esign/seal.py``), not a signer identity per person, so a seal here would say "AI Matrx" not "you".
"""

from __future__ import annotations

import base64
import binascii
import io
import re
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from .redact_real import _inverse
from ._pike import inherited, is_signed, load_pikepdf, open_pdf, save_pdf
from .stamp import _num, _pdf_string, _rgb, _visible_box, _visual_to_user

FieldType = Literal["text", "date", "checkbox", "radio", "dropdown", "list", "button", "signature", "unknown"]

_FF_READONLY, _FF_REQUIRED, _FF_MULTILINE = 1, 1 << 1, 1 << 12
_FF_RADIO, _FF_PUSH, _FF_COMBO = 1 << 15, 1 << 16, 1 << 17
_DATE_NAME = re.compile(r"(date|dob|birth|signed_on)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Detect
# ---------------------------------------------------------------------------


def _attr(field: Any, key: str) -> Any:
    """A field attribute inherited through /Parent."""
    node = field
    for _ in range(32):
        if key in node:
            return node[key]
        node = node.get("/Parent")
        if node is None:
            return None
    return None


def _qualified(field: Any) -> str:
    parts: list[str] = []
    node = field
    for _ in range(32):
        if node is None:
            break
        if "/T" in node:
            parts.append(str(node["/T"]))
        node = node.get("/Parent")
    return ".".join(reversed(parts))


def _value_text(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v)
    return s[1:] if s.startswith("/") else s


def _user_to_visible(page_obj: Any, rect: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    x0, y0, w, h, rot = _visible_box(page_obj)
    vh = w if rot in (90, 270) else h
    inv = _inverse(load_pikepdf().Matrix(*_visual_to_user(x0, y0, w, h, rot)))
    pts = [inv.transform(p) for p in ((rect[0], rect[1]), (rect[2], rect[3]), (rect[0], rect[3]), (rect[2], rect[1]))]
    xs, ys = [p[0] for p in pts], [vh - p[1] for p in pts]
    return round(min(xs), 2), round(min(ys), 2), round(max(xs), 2), round(max(ys), 2)


def _classify(field: Any, name: str) -> tuple[FieldType, list[str]]:
    ft = str(_attr(field, "/FT") or "")
    ff = int(_attr(field, "/Ff") or 0)
    options: list[str] = []
    if ft == "/Tx":
        action = field.get("/AA")
        js = str(action.get("/F", {}).get("/JS", "")) if action is not None and "/F" in action else ""
        return ("date" if "AFDate" in js or _DATE_NAME.search(name) else "text"), options
    if ft == "/Btn":
        if ff & _FF_PUSH:
            return "button", options
        if ff & _FF_RADIO:
            for kid in field.get("/Kids", []):
                ap = kid.get("/AP")
                states = [str(k).lstrip("/") for k in (ap.get("/N").keys() if ap is not None and "/N" in ap else [])]
                options += [s for s in states if s != "Off"]
            return "radio", options
        return "checkbox", ["Yes"]
    if ft == "/Ch":
        pikepdf = load_pikepdf()
        for o in _attr(field, "/Opt") or []:
            options.append(str(o[1]) if isinstance(o, pikepdf.Array) else str(o))
        return ("dropdown" if ff & _FF_COMBO else "list"), options
    if ft == "/Sig":
        return "signature", options
    return "unknown", options


def list_form_fields_bytes(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    with open_pdf(pdf_bytes, password) as pdf:
        acro = pdf.Root.get("/AcroForm")
        page_of: dict[tuple[int, int], int] = {}
        for i, page in enumerate(pdf.pages):
            for a in page.obj.get("/Annots") or []:
                if a.is_indirect:
                    page_of[a.objgen] = i
        fields: list[dict[str, Any]] = []

        def walk(node: Any) -> None:
            kids = node.get("/Kids")
            terminal_kids = [k for k in (kids or []) if "/T" not in k]  # widgets of one field, not subfields
            if kids is not None and len(terminal_kids) != len(kids):
                for k in kids:
                    walk(k)
                return
            name = _qualified(node)
            ftype, options = _classify(node, name)
            widgets = terminal_kids if kids is not None else [node]
            first = widgets[0] if widgets else node
            page_index = page_of.get(first.objgen) if first.is_indirect else None
            if page_index is None and node.is_indirect:
                page_index = page_of.get(node.objgen)
            rect = first.get("/Rect")
            box = None
            if rect is not None and page_index is not None:
                r = [float(v) for v in rect]
                box = _user_to_visible(pdf.pages[page_index].obj, (min(r[0], r[2]), min(r[1], r[3]), max(r[0], r[2]), max(r[1], r[3])))
            ff = int(_attr(node, "/Ff") or 0)
            value = _value_text(_attr(node, "/V"))
            if ftype == "checkbox":
                value = None if value in (None, "Off") else value
            if ftype == "radio" and value == "Off":
                value = None
            fields.append(
                {
                    "name": name,
                    "type": ftype,
                    "value": value,
                    "options": options,
                    "page_number": None if page_index is None else page_index + 1,
                    "rect": None if box is None else {"x0": box[0], "y0": box[1], "x1": box[2], "y1": box[3]},
                    "required": bool(ff & _FF_REQUIRED),
                    "read_only": bool(ff & _FF_READONLY),
                    "multiline": bool(ff & _FF_MULTILINE) if ftype in ("text", "date") else False,
                    "max_length": int(_attr(node, "/MaxLen")) if _attr(node, "/MaxLen") is not None else None,
                }
            )

        if acro is not None:
            for f in acro.get("/Fields", []):
                walk(f)
        return {"has_form": bool(fields), "fields": fields, "signed": is_signed(pdf), "page_count": len(pdf.pages)}


# ---------------------------------------------------------------------------
# Fill / flatten
# ---------------------------------------------------------------------------


def _wrapper(pdf_bytes: bytes) -> Any:
    try:
        from PyPDFForm import PdfWrapper
    except ImportError as exc:  # pragma: no cover - the platform image installs it
        raise ImportError("Filling forms needs the `PyPDFForm` package. Install it with: pip install PyPDFForm", name="PyPDFForm") from exc
    return PdfWrapper(pdf_bytes)


def _coerce(field: dict[str, Any], value: Any) -> Any:
    ftype, options, name = field["type"], field["options"], field["name"]
    if field["read_only"]:
        raise ValueError(f"The field '{name}' is read-only.")
    if ftype in ("text", "date"):
        text = "" if value is None else str(value)
        if field["max_length"] and len(text) > field["max_length"]:
            raise ValueError(f"The field '{name}' takes at most {field['max_length']} characters.")
        return text
    if ftype == "checkbox":
        if isinstance(value, str):
            return value.strip().lower() in ("true", "yes", "on", "1", "checked", "x")
        return bool(value)
    if ftype in ("radio", "dropdown", "list"):
        if isinstance(value, bool) or value is None:
            raise ValueError(f"Choose one of: {', '.join(options)} for '{name}'.")
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit() and value not in options):
            idx = int(value)
            if not 0 <= idx < len(options):
                raise ValueError(f"'{name}' has {len(options)} choices; {idx} is out of range.")
            return idx
        if str(value) in options:
            return options.index(str(value))
        folded = [o.lower() for o in options]
        if str(value).lower() in folded:
            return folded.index(str(value).lower())
        raise ValueError(f"'{value}' is not a choice for '{name}'. Choose one of: {', '.join(options)}.")
    raise ValueError(f"The field '{name}' ({ftype}) cannot be filled.")


def flatten_pdf_forms(pdf: Any) -> int:
    """Burn every widget appearance into its page and delete the form. Returns the number of fields flattened."""
    acro = pdf.Root.get("/AcroForm")
    count = len(list_form_fields_from_open(pdf))
    if acro is not None:
        pdf.generate_appearance_streams()
    pdf.flatten_annotations("all")
    if "/AcroForm" in pdf.Root:
        del pdf.Root["/AcroForm"]
    return count


def list_form_fields_from_open(pdf: Any) -> list[Any]:
    acro = pdf.Root.get("/AcroForm")
    return list(acro.get("/Fields", [])) if acro is not None else []


def fill_form_bytes(
    pdf_bytes: bytes,
    values: dict[str, Any],
    *,
    flatten: bool = False,
    password: str = "",
) -> PdfBinaryResult:
    detected = list_form_fields_bytes(pdf_bytes, password=password)
    if not detected["has_form"]:
        raise ValueError("This PDF has no fillable form fields. Use Fill and sign to place text on it instead.")
    if not values:
        raise ValueError("Give at least one field value to fill.")
    by_name = {f["name"]: f for f in detected["fields"]}
    unknown = sorted(set(values) - set(by_name))
    if unknown:
        raise ValueError(f"These fields are not in the form: {', '.join(unknown)}. Fields are: {', '.join(sorted(by_name))}.")
    coerced = {name: _coerce(by_name[name], v) for name, v in values.items()}
    source = pdf_bytes
    if password:
        with open_pdf(pdf_bytes, password) as pdf:
            source = save_pdf(pdf)
    filled = _wrapper(source).fill(coerced, flatten=False).read()
    flattened = 0
    if flatten:
        with open_pdf(filled) as pdf:
            flattened = flatten_pdf_forms(pdf)
            filled = save_pdf(pdf)
    return PdfBinaryResult(
        content=filled,
        page_count=detected["page_count"],
        operation="flatten-form" if flatten else "fill-form",
        metadata={"filled": sorted(coerced), "flattened": flatten, "fields_flattened": flattened, "signed": detected["signed"]},
    )


def flatten_form_bytes(pdf_bytes: bytes, *, password: str = "") -> PdfBinaryResult:
    with open_pdf(pdf_bytes, password) as pdf:
        if not list_form_fields_from_open(pdf):
            raise ValueError("This PDF has no form fields to flatten.")
        signed = is_signed(pdf)
        n = flatten_pdf_forms(pdf)
        return PdfBinaryResult(content=save_pdf(pdf), page_count=len(pdf.pages), operation="flatten-form", metadata={"fields_flattened": n, "signed": signed})


def read_form_values_bytes(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    """Field values as PyPDFForm reads them back from the file (booleans for checkboxes, indexes for choices)."""
    source = pdf_bytes
    if password:
        with open_pdf(pdf_bytes, password) as pdf:
            source = save_pdf(pdf)
    return dict(_wrapper(source).data)


# ---------------------------------------------------------------------------
# Fill & Sign: marks on a page without a form
# ---------------------------------------------------------------------------


class PdfMark(BaseModel):
    """One thing placed on a page. Box is on the visible page, points, origin top-left."""

    kind: Literal["text", "date", "check", "signature"]
    page_number: int = Field(ge=1)
    x: float
    y: float
    width: float = Field(gt=0, le=2000)
    height: float = Field(gt=0, le=2000)
    text: str = Field(default="", max_length=2000)
    font_size: float = Field(default=0, ge=0, le=200)  # 0: fit the box height
    color: str = "#000000"
    #: Signature picture: a PNG as a data URL or plain base64.
    image: str | None = None

    @model_validator(mode="after")
    def _needs(self) -> "PdfMark":
        if self.kind in ("text", "date") and not self.text.strip():
            raise ValueError("Text and date marks need their text.")
        if self.kind == "signature" and not self.image:
            raise ValueError("A signature mark needs the signature picture.")
        return self


def _decode_image(data: str) -> Any:
    from PIL import Image

    raw = data.split(",", 1)[1] if data.startswith("data:") else data
    try:
        img = Image.open(io.BytesIO(base64.b64decode(raw, validate=False)))
        img.load()
    except (binascii.Error, OSError, ValueError) as exc:
        raise ValueError("The signature picture could not be read. Draw or upload it again.") from exc
    return img


def _image_xobject(pdf: Any, img: Any) -> Any:
    import zlib

    pikepdf = load_pikepdf()
    img = img.convert("RGBA")
    if img.width * img.height > 4_000_000:
        img.thumbnail((2000, 2000))
    rgb = img.convert("RGB")
    stream = pikepdf.Stream(pdf, zlib.compress(rgb.tobytes()))
    stream.Type, stream.Subtype = pikepdf.Name.XObject, pikepdf.Name.Image
    stream.Width, stream.Height, stream.BitsPerComponent = rgb.width, rgb.height, 8
    stream.ColorSpace, stream.Filter = pikepdf.Name.DeviceRGB, pikepdf.Name.FlateDecode
    alpha = img.getchannel("A")
    if alpha.getextrema()[0] < 255:
        mask = pikepdf.Stream(pdf, zlib.compress(alpha.tobytes()))
        mask.Type, mask.Subtype = pikepdf.Name.XObject, pikepdf.Name.Image
        mask.Width, mask.Height, mask.BitsPerComponent = alpha.width, alpha.height, 8
        mask.ColorSpace, mask.Filter = pikepdf.Name.DeviceGray, pikepdf.Name.FlateDecode
        stream.SMask = mask
    return stream


def _mark_form(pdf: Any, mark: PdfMark, font: Any, serial: int) -> Any:
    pikepdf = load_pikepdf()
    w, h = mark.width, mark.height
    r, g, b = _rgb(mark.color)
    res = pikepdf.Dictionary()
    if mark.kind in ("text", "date"):
        size = mark.font_size or max(6.0, min(h * 0.8, 24.0))
        text = mark.text.encode("cp1252", errors="replace")
        body = f"{_num(r)} {_num(g)} {_num(b)} rg BT /F1 {_num(size)} Tf 1 0 0 1 0 {_num(max(0.0, (h - size) / 2 + size * 0.22))} Tm ".encode() + _pdf_string(text) + b" Tj ET"
        res.Font = pikepdf.Dictionary(F1=font)
    elif mark.kind == "check":
        lw = max(1.0, min(w, h) * 0.12)
        body = (
            f"{_num(r)} {_num(g)} {_num(b)} RG {_num(lw)} w 1 J 1 j "
            f"{_num(w * 0.12)} {_num(h * 0.52)} m {_num(w * 0.4)} {_num(h * 0.15)} l {_num(w * 0.9)} {_num(h * 0.88)} l S"
        ).encode()
    else:
        img = _decode_image(mark.image or "")
        res.XObject = pikepdf.Dictionary(Sig=_image_xobject(pdf, img))
        scale = min(w / img.width, h / img.height)
        iw, ih = img.width * scale, img.height * scale
        body = f"q {_num(iw)} 0 0 {_num(ih)} {_num((w - iw) / 2)} {_num((h - ih) / 2)} cm /Sig Do Q".encode()
    form = pikepdf.Stream(pdf, body)
    form.Type, form.Subtype = pikepdf.Name.XObject, pikepdf.Name.Form
    form.BBox = [0, 0, w, h]
    form.Resources = res
    form.MatrxMark = pikepdf.Dictionary(Kind=pikepdf.Name("/" + mark.kind), Id=serial)
    return form


def place_marks_bytes(pdf_bytes: bytes, marks: list[PdfMark | dict[str, Any]], *, password: str = "") -> PdfBinaryResult:
    pikepdf = load_pikepdf()
    parsed = [m if isinstance(m, PdfMark) else PdfMark(**m) for m in marks]
    if not parsed:
        raise ValueError("Place at least one mark.")
    with open_pdf(pdf_bytes, password) as pdf:
        total = len(pdf.pages)
        signed = is_signed(pdf)
        font = pdf.make_indirect(
            pikepdf.Dictionary(Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type1, BaseFont=pikepdf.Name.Helvetica, Encoding=pikepdf.Name.WinAnsiEncoding)
        )
        by_page: dict[int, list[tuple[int, PdfMark]]] = {}
        for i, m in enumerate(parsed, start=1):
            if m.page_number > total:
                raise ValueError(f"The file has {total} pages; a mark is on page {m.page_number}.")
            by_page.setdefault(m.page_number, []).append((i, m))
        for pno, items in by_page.items():
            page = pdf.pages[pno - 1]
            x0, y0, w, h, rot = _visible_box(page.obj)
            vh = w if rot in (90, 270) else h
            res = page.obj.get("/Resources")
            if res is None:
                inh = inherited(page.obj, "/Resources")
                res = pikepdf.Dictionary({k: v for k, v in inh.items()}) if inh is not None else pikepdf.Dictionary()
                page.obj.Resources = res
            if "/XObject" not in res:
                res.XObject = pikepdf.Dictionary()
            ops = [b"q", (" ".join(_num(v) for v in _visual_to_user(x0, y0, w, h, rot)) + " cm").encode()]
            for serial, m in items:
                name = f"MxMark{serial}"
                res.XObject["/" + name] = _mark_form(pdf, m, font, serial)
                ops.append(f"q 1 0 0 1 {_num(m.x)} {_num(vh - m.y - m.height)} cm /{name} Do Q".encode())
            ops.append(b"Q")
            page.contents_add(pikepdf.Stream(pdf, b"q\n"), prepend=True)
            page.contents_add(pikepdf.Stream(pdf, b"\nQ\n" + b"\n".join(ops) + b"\n"), prepend=False)
        return PdfBinaryResult(
            content=save_pdf(pdf),
            page_count=total,
            operation="fill-sign",
            metadata={"marks": len(parsed), "kinds": sorted({m.kind for m in parsed}), "pages": sorted(by_page), "signed": signed},
        )


def list_marks_bytes(pdf_bytes: bytes, *, password: str = "") -> list[dict[str, Any]]:
    """Marks placed by ``place_marks_bytes`` (read from the tagged form XObjects)."""
    out: list[dict[str, Any]] = []
    with open_pdf(pdf_bytes, password) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            res = page.obj.get("/Resources")
            xobjs = res.get("/XObject") if res is not None else None
            for key, xo in (xobjs.items() if xobjs is not None else []):
                tag = xo.get("/MatrxMark")
                if tag is not None:
                    out.append({"page_number": i, "kind": str(tag.Kind).lstrip("/"), "id": int(tag.Id), "name": str(key).lstrip("/")})
    return out


async def list_form_fields_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
    return await run_in_cpu_executor(list_form_fields_bytes, pdf_bytes, **kwargs)


async def fill_form_bytes_async(pdf_bytes: bytes, values: dict[str, Any], **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(fill_form_bytes, pdf_bytes, values, **kwargs)


async def flatten_form_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(flatten_form_bytes, pdf_bytes, **kwargs)


async def place_marks_bytes_async(pdf_bytes: bytes, marks: list[Any], **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(place_marks_bytes, pdf_bytes, marks, **kwargs)
