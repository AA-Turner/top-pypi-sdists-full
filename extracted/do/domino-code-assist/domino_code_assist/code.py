import ipyvuetify as v
import reacton
import traitlets
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


class CodeWidget(v.VuetifyTemplate):
    template_file = (__file__, "code.vue")

    highlighted_chunks = traitlets.List().tag(sync=True)
    error = traitlets.List(allow_none=True).tag(sync=True)
    no_controls = traitlets.Bool().tag(sync=True)
    assistant_mode = traitlets.Bool().tag(sync=True)

    event = traitlets.Any().tag(sync=True)


@reacton.component
def Code(code_chunks, on_event, error=None, no_controls=False, assistant_mode=False):
    def to_code_chunks(plain_chunks):
        formatter = HtmlFormatter()
        lexer = PythonLexer()
        return [highlight(chunk, lexer, formatter) for chunk in plain_chunks]

    return CodeWidget.element(
        highlighted_chunks=to_code_chunks(code_chunks), on_event=on_event, error=error, no_controls=no_controls, assistant_mode=assistant_mode
    )
