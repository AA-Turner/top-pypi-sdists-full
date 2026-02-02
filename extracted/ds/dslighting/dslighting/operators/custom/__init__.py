"""
Custom Operators - user-defined operators.

Add your own operators under this package.

Example (SimpleOperator):

```python
from dslighting.operators.custom import SimpleOperator

# Define your analysis function.
async def my_analysis(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Wrap it as an operator.
op = SimpleOperator(func=my_analysis)
```

Example (LLMOperator):

```python
from dslighting.operators.custom import LLMOperator

op = LLMOperator(
    llm_service=llm,
    system_prompt="You are a data analyst",
    user_prompt_template="Analyze: {input}"
)
```

Example (CodeExecutorOperator):

```python
from dslighting.operators.custom import CodeExecutorOperator

op = CodeExecutorOperator(
    sandbox_service=sandbox,
    code_template="print('{data}')"
)
```

Example (custom BaseOperator):

```python
from dslighting.operators.custom import BaseOperator

class MyCustomOperator(BaseOperator):
    async def run(self, data: str) -> dict:
        # Implement your operator logic here.
        return {"result": "..."}
```

Add your operators below and export them in __all__.
"""

# Built-in operator utilities.

from .base_operator import (
    BaseOperator,
    SimpleOperator,
    LLMOperator,
    CodeExecutorOperator,
    ChainedOperator,
    ConditionalOperator,
    create_llm_operator,
    create_code_operator,
)

# Built-in example operators.
from .data_profiler import DataProfilerOperator

# User-defined operators can be added here.
# from .my_custom_operator import MyCustomOperator
# from .my_custom_operator import MyCustomOperator
# from .my_llm_operator import MyLLMOperator
# from .my_data_operator import MyDataOperator

__all__ = [
    # Core operator building blocks.
    "BaseOperator",
    "SimpleOperator",
    "LLMOperator",
    "CodeExecutorOperator",
    "ChainedOperator",
    "ConditionalOperator",
    "create_llm_operator",
    "create_code_operator",

    # Built-in examples.
    "DataProfilerOperator",

    # User-defined operators.
    # "MyCustomOperator",
    # "MyLLMOperator",
    # "MyDataOperator",
]
