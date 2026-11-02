"""A real-shaped AcroForm (text, date, checkbox, radio group, dropdown) for the U13 forcing tests."""
import pikepdf
from _pdf_corpus import _add_text_page,_new_pdf,_save

def build_form() -> bytes:
    pdf, font = _new_pdf()
    page = _add_text_page(pdf, font, [(72, 740, "Application form")])
    D, N, A, S = pikepdf.Dictionary, pikepdf.Name, pikepdf.Array, pikepdf.String
    def widget(**kw):
        return pdf.make_indirect(D(Type=N.Annot, Subtype=N.Widget, F=4, P=page.obj, **kw))
    def box_ap(on):
        return pdf.make_stream(b"q 0 g 0 0 14 14 re S Q" if not on else b"q 0 g 0 0 14 14 re S 2 2 m 12 12 l 12 2 m 2 12 l S Q")
    def stream(on):
        s = box_ap(on); s.Type, s.Subtype, s.BBox = N.XObject, N.Form, [0,0,14,14]; return s
    DA = S("/F1 12 Tf 0 g")
    name = widget(FT=N.Tx, T=S("full_name"), Rect=[150,690,400,710], DA=DA)
    date = widget(FT=N.Tx, T=S("signed_date"), Rect=[150,650,300,670], DA=DA, AA=D(F=D(S=N.JavaScript, JS=S('AFDate_FormatEx("mm/dd/yyyy")'))))
    agree = widget(FT=N.Btn, T=S("agree"), Rect=[150,610,164,624], V=N.Off, AS=N.Off, AP=D(N=D(Yes=stream(True), Off=stream(False))), MK=D(CA=S("4")))
    r1 = widget(Rect=[150,570,164,584], Parent=None, AS=N.Off, AP=D(N=D(Small=stream(True), Off=stream(False))))
    r2 = widget(Rect=[200,570,214,584], AS=N.Off, AP=D(N=D(Large=stream(True), Off=stream(False))))
    radio = pdf.make_indirect(D(FT=N.Btn, T=S("size"), Ff=(1<<15), V=N.Off, Kids=A([r1, r2])))
    r1.Parent = radio; r2.Parent = radio
    combo = widget(FT=N.Ch, T=S("country"), Rect=[150,530,300,550], Ff=(1<<17), Opt=A([S("Canada"), S("Mexico"), S("USA")]), DA=DA)
    page.Annots = A([name, date, agree, r1, r2, combo])
    pdf.Root.AcroForm = D(Fields=A([name, date, agree, radio, combo]), DA=DA, NeedAppearances=True, DR=D(Font=D(F1=font)))
    return _save(pdf)
