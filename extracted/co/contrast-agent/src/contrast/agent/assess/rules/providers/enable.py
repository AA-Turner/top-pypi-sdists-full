# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from contrast.agent.assess.rules.providers.hardcoded_key import HardcodedKey
from contrast.agent.assess.rules.providers.hardcoded_password import HardcodedPassword
from contrast.utils.patch_utils import get_loaded_modules

PROVIDERS_THREAD_NAME = "ContrastProviders"


def run_providers_in_thread():
    threading.Thread(
        target=_run_providers,
        name=PROVIDERS_THREAD_NAME,
        daemon=True,
    ).start()


def _run_providers():
    """
    Providers are non-dataflow rules that analyze the contents of a module.
    """
    providers = [p for p in [HardcodedKey(), HardcodedPassword()] if not p.disabled]
    if not providers:
        return

    loaded_modules = get_loaded_modules().values()
    for provider in providers:
        for module in loaded_modules:
            provider.analyze(module)
