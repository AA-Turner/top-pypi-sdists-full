from novita_sandbox.code_interpreter import Sandbox


def test_reconnect(sandbox: Sandbox):
    sandbox_id = sandbox.sandbox_id

    sandbox2 = Sandbox.connect(sandbox_id)
    result = sandbox2.run_code("x =1; x")
    assert result.text == "1"
