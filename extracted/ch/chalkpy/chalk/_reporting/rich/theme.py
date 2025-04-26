from rich.style import Style
from rich.theme import Theme

from chalk._reporting.rich.color import PASTELY_CYAN, SERENDIPITOUS_PURPLE

CHALK_THEME = Theme(
    {
        "progress.elapsed": Style(color=SERENDIPITOUS_PURPLE),
        "progress.download": Style(color=PASTELY_CYAN),
        "bar.pulse": Style(color=SERENDIPITOUS_PURPLE),
        "progress.percentage": Style(color=PASTELY_CYAN),
    }
)
