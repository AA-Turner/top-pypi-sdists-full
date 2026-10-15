"""#2490: AzureBlobStorageClient の認証経路の契約テスト (3.0.16)。

固定する契約:
  1. connection_string があれば `BlobServiceClient.from_connection_string` (従来どおり。
     azure-identity は import しない)
  2. connection_string が無く storage_account_name があれば
     `BlobServiceClient(account_url, credential=DefaultAzureCredential())`
     (account_url = https://<name>.blob.<endpoint_suffix>)
  3. どちらも無ければ構築時に StorageConfigError
  4. 空文字 / 空白だけの connection_string は「無し」(設定ファイルで空にした形)
  5. str(config) / repr(config) に接続文字列が出ない
  6. 資格情報なし経路で azure-identity が無ければ extra 案内つきの StorageConfigError
  7. close() が credential も閉じる
  8. 後方互換: 位置引数 AzureBlobConfig("container", "conn") と from_dict の従来の形

Azure には繋がない: BlobServiceClient と DefaultAzureCredential を monkeypatch で
記録用の偽物に差し替える (DefaultAzureCredential は生成時に token を取らないので、
本物を使っても失敗しないが、どの経路に入ったかを見るために差し替える)。

実行: python -m pytest tests/storage/test_azure_credential.py -v
"""

from __future__ import annotations

import builtins
import sys

import pytest
from agenticstar_platform.storage import AzureBlobConfig, StorageConfigError
from agenticstar_platform.storage import azure as azure_module

CONN = "DefaultEndpointsProtocol=https;AccountName=acct;AccountKey=c2VjcmV0;EndpointSuffix=core.windows.net"


class _FakeBlobServiceClient:
    """経路と引数を記録するだけの BlobServiceClient"""

    instances: list = []

    def __init__(self, account_url=None, credential=None, **options):
        self.account_url = account_url
        self.credential = credential
        self.options = options
        self.via = "account_url"
        self.closed = False
        _FakeBlobServiceClient.instances.append(self)

    @classmethod
    def from_connection_string(cls, conn_str, **options):
        inst = cls(**options)
        inst.conn_str = conn_str
        inst.via = "connection_string"
        return inst

    def close(self):
        self.closed = True


class _FakeDefaultAzureCredential:
    instances: list = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.closed = False
        _FakeDefaultAzureCredential.instances.append(self)

    def close(self):
        self.closed = True


@pytest.fixture
def fakes(monkeypatch: pytest.MonkeyPatch):
    _FakeBlobServiceClient.instances = []
    _FakeDefaultAzureCredential.instances = []
    monkeypatch.setattr(azure_module, "BlobServiceClient", _FakeBlobServiceClient)
    monkeypatch.setattr(azure_module, "AZURE_BLOB_AVAILABLE", True)
    # 資格情報なし経路は azure.identity を遅延 import するので module 側を差し替える
    import azure.identity

    monkeypatch.setattr(azure.identity, "DefaultAzureCredential", _FakeDefaultAzureCredential)
    return _FakeBlobServiceClient, _FakeDefaultAzureCredential


class TestConnectionStringPath:
    """契約 1 / 5 / 8: 接続文字列の従来経路"""

    def test_connection_string_uses_from_connection_string(self, fakes) -> None:
        blob_cls, cred_cls = fakes
        config = AzureBlobConfig(bucket_name="c", connection_string=CONN)
        client = azure_module.AzureBlobStorageClient(config)

        assert config.uses_connection_string is True
        assert blob_cls.instances[-1].via == "connection_string"
        assert blob_cls.instances[-1].conn_str == CONN
        assert cred_cls.instances == []  # DefaultAzureCredential は作らない
        assert client._credential is None
        assert blob_cls.instances[-1].options == {
            "max_block_size": config.max_block_size,
            "max_single_put_size": config.max_single_put_size,
            "connection_timeout": config.connection_timeout,
            "read_timeout": config.read_timeout,
        }

    def test_connection_string_wins_when_both_given(self, fakes) -> None:
        blob_cls, cred_cls = fakes
        config = AzureBlobConfig(
            bucket_name="c", connection_string=CONN, storage_account_name="acct"
        )
        azure_module.AzureBlobStorageClient(config)
        assert blob_cls.instances[-1].via == "connection_string"
        assert cred_cls.instances == []

    def test_positional_construction_still_means_connection_string(self, fakes) -> None:
        blob_cls, _ = fakes
        config = AzureBlobConfig("c", CONN)
        assert config.connection_string == CONN
        azure_module.AzureBlobStorageClient(config)
        assert blob_cls.instances[-1].via == "connection_string"

    def test_from_dict_without_storage_account_name_key(self, fakes) -> None:
        """3.0.15 までの辞書 (storage_account_name キー無し) がそのまま通る"""
        config = AzureBlobConfig.from_dict({"bucket_name": "c", "connection_string": CONN})
        assert config.uses_connection_string is True
        assert config.storage_account_name is None
        assert config.endpoint_suffix == "core.windows.net"

    def test_secret_never_in_str_or_repr(self, fakes) -> None:
        config = AzureBlobConfig(bucket_name="c", connection_string=CONN)
        assert "AccountKey" not in str(config)
        assert "AccountKey" not in repr(config)
        assert "connection_string=***" in str(config)


class TestDefaultAzureCredentialPath:
    """契約 2 / 7: storage_account_name + DefaultAzureCredential"""

    def test_account_name_builds_account_url_and_credential(self, fakes) -> None:
        blob_cls, cred_cls = fakes
        config = AzureBlobConfig(bucket_name="c", storage_account_name="agtstrdemo")
        client = azure_module.AzureBlobStorageClient(config)

        assert config.uses_connection_string is False
        assert config.account_url == "https://agtstrdemo.blob.core.windows.net"
        inst = blob_cls.instances[-1]
        assert inst.via == "account_url"
        assert inst.account_url == "https://agtstrdemo.blob.core.windows.net"
        assert len(cred_cls.instances) == 1
        assert inst.credential is cred_cls.instances[0]
        assert client._credential is cred_cls.instances[0]
        assert inst.options["connection_timeout"] == config.connection_timeout

    def test_endpoint_suffix_is_honoured(self, fakes) -> None:
        blob_cls, _ = fakes
        config = AzureBlobConfig.from_dict({
            "bucket_name": "c",
            "storage_account_name": "acct",
            "endpoint_suffix": "core.chinacloudapi.cn",
        })
        azure_module.AzureBlobStorageClient(config)
        assert blob_cls.instances[-1].account_url == "https://acct.blob.core.chinacloudapi.cn"

    def test_str_names_the_account_not_a_secret(self, fakes) -> None:
        config = AzureBlobConfig(bucket_name="c", storage_account_name="acct")
        assert "storage_account_name='acct'" in str(config)
        assert "***" not in str(config)

    @pytest.mark.asyncio
    async def test_close_closes_credential_too(self, fakes) -> None:
        blob_cls, cred_cls = fakes
        client = azure_module.AzureBlobStorageClient(
            AzureBlobConfig(bucket_name="c", storage_account_name="acct")
        )
        await client.close()
        assert blob_cls.instances[-1].closed is True
        assert cred_cls.instances[-1].closed is True
        assert client._credential is None
        assert client._blob_service_client is None

    def test_missing_azure_identity_gives_extra_hint(
        self, fakes, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """契約 6: 資格情報なし経路でだけ azure-identity を要求し、extra を案内する"""
        monkeypatch.delitem(sys.modules, "azure.identity", raising=False)
        real_import = builtins.__import__

        def _block_identity(name, *args, **kwargs):
            if name == "azure.identity" or name.startswith("azure.identity."):
                raise ImportError(f"No module named '{name}'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", _block_identity)

        with pytest.raises(StorageConfigError) as excinfo:
            azure_module.AzureBlobStorageClient(
                AzureBlobConfig(bucket_name="c", storage_account_name="acct")
            )
        assert "azure-identity" in str(excinfo.value)
        assert "pip install 'agenticstar-platform[storage-azure]'" in str(excinfo.value)

        # 接続文字列の経路は azure-identity が無くても構築できる
        azure_module.AzureBlobStorageClient(
            AzureBlobConfig(bucket_name="c", connection_string=CONN)
        )


class TestNeitherOrBlank:
    """契約 3 / 4: 認証手段が無い形と、空文字の正規化"""

    @pytest.mark.parametrize("blank", ["", "   ", None])
    def test_blank_connection_string_means_none(self, blank) -> None:
        config = AzureBlobConfig(bucket_name="c", connection_string=blank)
        assert config.connection_string is None
        assert config.uses_connection_string is False

    @pytest.mark.parametrize("blank", ["", "   ", None])
    def test_blank_storage_account_name_means_none(self, blank) -> None:
        config = AzureBlobConfig(
            bucket_name="c", connection_string=CONN, storage_account_name=blank
        )
        assert config.storage_account_name is None
        assert config.account_url is None

    def test_blank_connection_string_from_dict_falls_back_to_account_name(self, fakes) -> None:
        """設定ファイルで connection_string = "" にした形 (Helm の値が空のとき)"""
        blob_cls, cred_cls = fakes
        config = AzureBlobConfig.from_dict({
            "bucket_name": "c",
            "connection_string": "",
            "storage_account_name": "acct",
        })
        azure_module.AzureBlobStorageClient(config)
        assert blob_cls.instances[-1].via == "account_url"
        assert len(cred_cls.instances) == 1

    def test_neither_raises_config_error(self, fakes) -> None:
        blob_cls, cred_cls = fakes
        with pytest.raises(StorageConfigError) as excinfo:
            azure_module.AzureBlobStorageClient(
                AzureBlobConfig(bucket_name="c", connection_string="")
            )
        assert "connection_string" in str(excinfo.value)
        assert "storage_account_name" in str(excinfo.value)
        assert blob_cls.instances == []
        assert cred_cls.instances == []

    def test_from_dict_neither_raises_at_client_not_at_config(self, fakes) -> None:
        config = AzureBlobConfig.from_dict({"bucket_name": "c"})
        assert config.connection_string is None
        with pytest.raises(StorageConfigError):
            azure_module.AzureBlobStorageClient(config)

    def test_missing_bucket_still_rejected(self, fakes) -> None:
        with pytest.raises(StorageConfigError) as excinfo:
            azure_module.AzureBlobStorageClient(
                AzureBlobConfig(bucket_name="", storage_account_name="acct")
            )
        assert "bucket_name" in str(excinfo.value)
