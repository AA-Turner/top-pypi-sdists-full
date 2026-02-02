
import dslighting
dslighting.explore()  # 查看所有组件



# 只看 AIDE workflow 的 prompts
aide_prompts = dslighting.list_prompts(category="aide")

# 只看 LLM operators
llm_ops = dslighting.list_operators(category="llm")

from dslighting.prompts import get_prompt_info
from dslighting.operators import get_operator_info

# 了解某个 prompt 的用途
info = get_prompt_info("create_improve_prompt")

# 了解某个 operator 的用法
info = get_operator_info("PlanOperator")

print(info)