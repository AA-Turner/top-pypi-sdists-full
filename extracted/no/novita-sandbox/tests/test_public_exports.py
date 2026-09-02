"""
Tests for public package exports.
"""


def test_top_level_exports_core_sandbox_api():
    """The package root should re-export the core SDK entrypoints."""
    import novita_sandbox
    from novita_sandbox import AsyncSandbox, AsyncTemplate, AsyncVolume, Sandbox, Template, Volume
    from novita_sandbox.core import (
        AsyncSandbox as CoreAsyncSandbox,
        AsyncTemplate as CoreAsyncTemplate,
        AsyncVolume as CoreAsyncVolume,
        Sandbox as CoreSandbox,
        Template as CoreTemplate,
        Volume as CoreVolume,
    )

    assert Sandbox is CoreSandbox
    assert AsyncSandbox is CoreAsyncSandbox
    assert Template is CoreTemplate
    assert AsyncTemplate is CoreAsyncTemplate
    assert Volume is CoreVolume
    assert AsyncVolume is CoreAsyncVolume
    assert "Sandbox" in novita_sandbox.__all__
    assert "AsyncSandbox" in novita_sandbox.__all__


def test_top_level_exports_secret_api():
    import novita_sandbox
    from novita_sandbox import AsyncSecret, Secret, SecretBinding
    from novita_sandbox.core.secret import (
        AsyncSecret as CoreSecretAsyncSecret,
        Secret as CoreSecretSecret,
        SecretBinding as CoreSecretSecretBinding,
    )

    assert Secret is CoreSecretSecret
    assert AsyncSecret is CoreSecretAsyncSecret
    assert SecretBinding is CoreSecretSecretBinding
    assert "Secret" in novita_sandbox.__all__
    assert "AsyncSecret" in novita_sandbox.__all__
    assert "SecretBinding" in novita_sandbox.__all__
    assert all(name != "Secrets" + "Client" for name in novita_sandbox.__all__)
