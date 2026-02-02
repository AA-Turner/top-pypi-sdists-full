#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2025/4/14 11:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

"""

[Model(id='LLM-Research/c4ai-command-r-plus-08-2024', created=1725120000, object='model', owned_by='system'),
 Model(id='mistralai/Mistral-Small-Instruct-2409', created=1725120000, object='model', owned_by='system'),
 Model(id='mistralai/Ministral-8B-Instruct-2410', created=1727712000, object='model', owned_by='system'),
 Model(id='mistralai/Mistral-Large-Instruct-2407', created=1719763200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-Coder-32B-Instruct', created=1731340800, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-Coder-14B-Instruct', created=1731340800, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-Coder-7B-Instruct', created=1731340800, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-72B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-32B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-14B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-7B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/QwQ-32B-Preview', created=1737907200, object='model', owned_by='system'),
 Model(id='LLM-Research/Llama-3.3-70B-Instruct', created=1733414400, object='model', owned_by='system'),
 Model(id='opencompass/CompassJudger-1-32B-Instruct', created=1733414400, object='model', owned_by='system'),
 Model(id='Qwen/QVQ-72B-Preview', created=1735056000, object='model', owned_by='system'),
 Model(id='LLM-Research/Meta-Llama-3.1-405B-Instruct', created=1721664000, object='model', owned_by='system'),
 Model(id='LLM-Research/Meta-Llama-3.1-8B-Instruct', created=1721664000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2-VL-7B-Instruct', created=1726675200, object='model', owned_by='system'),
 Model(id='LLM-Research/Meta-Llama-3.1-70B-Instruct', created=1721664000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-14B-Instruct-1M', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-7B-Instruct-1M', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-VL-3B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-VL-7B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-VL-72B-Instruct', created=1737907200, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Llama-70B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Llama-8B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Qwen-14B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', created=1737302400, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-V3', created=1737302400, object='model', owned_by='system'),
 Model(id='Qwen/QwQ-32B', created=1732517497, object='model', owned_by='system'),
 Model(id='XGenerationLab/XiYanSQL-QwenCoder-32B-2412', created=1732517497, object='model', owned_by='system'),
 Model(id='Qwen/Qwen2.5-VL-32B-Instruct', created=1732517497, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-V3-0324', created=1732517497, object='model', owned_by='system'),
 Model(id='Wan-AI/Wan2.1-T2V-1.3B', created=0, object='model', owned_by='system'),
 Model(id='LLM-Research/Llama-4-Scout-17B-16E-Instruct', created=1732517497, object='model', owned_by='system'),
 Model(id='LLM-Research/Llama-4-Maverick-17B-128E-Instruct', created=1732517497, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-0.6B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-1.7B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-4B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-8B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-14B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-30B-A3B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-32B', created=1745856000, object='model', owned_by='system'),
 Model(id='Qwen/Qwen3-235B-A22B', created=1745856000, object='model', owned_by='system'),
 Model(id='XGenerationLab/XiYanSQL-QwenCoder-32B-2504', created=1732517497, object='model', owned_by='system'),
 Model(id='deepseek-ai/DeepSeek-R1-0528', created=1748361600, object='model', owned_by='system')]
"""

modelscope_model_mapping = {
    "deepseek-reasoner": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-r1": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-r1-0528": "deepseek-ai/DeepSeek-R1-0528",
    "deepseek-r1-250528": "deepseek-ai/DeepSeek-R1-0528",

    "deepseek-chat": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3-0324": "deepseek-ai/DeepSeek-V3-0324",
    "deepseek-v3-250324": "deepseek-ai/DeepSeek-V3-0324",

    "majicflus_v1": "MAILAND/majicflus_v1",

}
