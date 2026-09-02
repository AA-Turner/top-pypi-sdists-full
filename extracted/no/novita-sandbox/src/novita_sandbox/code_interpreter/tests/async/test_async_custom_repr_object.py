from novita_sandbox.code_interpreter import AsyncSandbox

code = """
from IPython.display import display

display({'text/latex': r'\text{CustomReprObject}'}, raw=True)
"""


async def test_bash(async_sandbox: AsyncSandbox):
    execution = await async_sandbox.run_code(code)
    assert execution.results[0].formats() == ["latex"]
