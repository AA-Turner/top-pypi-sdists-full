from typing import Callable, Dict, Optional

import solara.lab

save_notebook: Optional[Callable[[Callable[[bool], None]], None]] = None
markdown_cells: Optional[Dict] = None
notebook_browser_path = solara.lab.Reactive("")
