"""`import probe` must stay light (plan (a), round-2 finding 5).

The Lightning and Hugging Face integrations bring torch or transformers; a
researcher who never uses them must not pay seconds of import time or fail on
a missing optional extra. They load only when their own module is imported.
Run in a fresh interpreter: this suite's process may already hold them.
"""

from __future__ import annotations

import json
import subprocess
import sys


def test_import_probe_loads_no_trainer_framework():
    probe_code = (
        "import sys, json, probe, probe.integrations, probe.sdk.client; "
        "print(json.dumps(sorted(m for m in ('lightning', 'pytorch_lightning', "
        "'transformers', 'torch') if m in sys.modules)))"
    )
    out = subprocess.run(
        [sys.executable, "-c", probe_code], capture_output=True, text=True, check=True
    )
    assert json.loads(out.stdout.strip().splitlines()[-1]) == []


def test_the_lightning_logger_without_lightning_names_the_extra():
    """The bare ImportError named `lightning_fabric`, a package nobody asked for."""
    blocked = ("lightning", "pytorch_lightning", "lightning_fabric")
    code = (
        "import sys\n"
        f"sys.modules.update(dict.fromkeys({blocked!r}))\n"
        "try:\n"
        "    import probe.integrations.lightning\n"
        "except ImportError as exc:\n"
        "    print(exc)\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert "pip install 'probe-research[lightning]'" in out.stdout


def test_the_hf_callback_without_transformers_names_the_extra():
    """The ImportError says which extra to install and keeps the missing
    module's `name`, which test_import_every_module reads to tell an absent
    optional extra from a broken import."""
    code = (
        "import sys\n"
        "sys.modules['transformers'] = None\n"
        "try:\n"
        "    import probe.integrations.huggingface\n"
        "except ImportError as exc:\n"
        "    print(exc.name)\n"
        "    print(exc)\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    name, message = out.stdout.splitlines()[:2]
    assert name.split(".")[0] == "transformers"  # what the import walk reads
    assert "pip install 'probe-research[huggingface]'" in message
