import os
from pathlib import Path

docs_path = "file://" + str(Path(Path(os.path.realpath(__file__)).parent, "html", "index.html").absolute())
try:
    import webbrowser

    webbrowser.open(docs_path)
except ImportError:
    print(docs_path)
