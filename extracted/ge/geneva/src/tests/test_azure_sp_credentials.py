# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Service-principal credentials must reach every PyArrow AzureFileSystem.

When an Azure service principal is supplied via ``storage_options`` and the
ambient Workload-Identity env vars are stripped (as some worker setup hooks do),
every geneva code path that builds a ``pyarrow.fs.AzureFileSystem`` must make the
service principal available to it. PyArrow's AzureFileSystem takes the SP through
the ``AZURE_*`` environment -- its internal ``DefaultAzureCredential`` resolves an
``EnvironmentCredential`` -- so the constructor must run with those vars set. If it
does not, AzureFileSystem falls through DefaultAzureCredential to node managed
identity and hits IMDS (169.254.169.254), which is rate-limited and stalls workers
at scale (GEN-726).

These probes replace AzureFileSystem with a fake that records the ``AZURE_*`` env
visible at construction time, the same technique test_bulk_load uses for the
already-correct bulk_load path.
"""

import os

import pytest

_SP_ENV_KEYS = (
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_SECRET",
    "AZURE_FEDERATED_TOKEN_FILE",
)

_SP_OPTIONS = {
    "account_name": "acct",
    "tenant_id": "tenant",
    "client_id": "client",
    "client_secret": "secret",
}

_EXPECTED_ENV = {
    "AZURE_TENANT_ID": "tenant",
    "AZURE_CLIENT_ID": "client",
    "AZURE_CLIENT_SECRET": "secret",
    "AZURE_FEDERATED_TOKEN_FILE": None,
}


def _install_env_capturing_azure_fs(monkeypatch) -> dict:
    """Swap in an AzureFileSystem that records its kwargs and the AZURE_* env
    it can see at construction time."""
    captured: dict = {"kwargs": {}, "env": {}}

    class FakeAzureFileSystem:
        def __init__(self, *args, **kwargs) -> None:
            if args:
                kwargs.setdefault("account_name", args[0])
            captured["kwargs"] = dict(kwargs)
            captured["env"] = {key: os.environ.get(key) for key in _SP_ENV_KEYS}

    import pyarrow.fs as fs

    monkeypatch.setattr(fs, "AzureFileSystem", FakeAzureFileSystem)
    return captured


@pytest.fixture(autouse=True)
def _strip_ambient_azure_env(monkeypatch) -> None:
    # Reproduce the customer's worker hook: no ambient Workload-Identity vars,
    # and no account name in the env so it must come from storage_options.
    for key in (
        *_SP_ENV_KEYS,
        "AZURE_AUTHORITY_HOST",
        "AZURE_USE_IDENTITY",
        "AZURE_STORAGE_ACCOUNT_NAME",
        "AZURE_STORAGE_ACCOUNT",
    ):
        monkeypatch.delenv(key, raising=False)


def test_filesystem_from_uri_azure_fs_receives_service_principal(monkeypatch) -> None:
    captured = _install_env_capturing_azure_fs(monkeypatch)
    from geneva.utils.storage import filesystem_from_uri

    filesystem_from_uri("az://container/blob", storage_options=dict(_SP_OPTIONS))

    assert captured["env"] == _EXPECTED_ENV
    assert "client_secret" not in captured["kwargs"]
    assert captured["kwargs"].get("account_name") == "acct"
