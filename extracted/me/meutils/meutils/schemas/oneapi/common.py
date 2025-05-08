#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : oneapi_types
# @Time         : 2024/6/28 10:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.data.oneapi import NOTICE, FOOTER

BASE_URL = "https://api.chatfire.cn"
# BASE_URL = "https://api.ffire.cn"

# BASE_URL = "https://api-dev.chatfire.cn"
FREE = 0.001
MJ_RELAX = 1
MJ_FAST = 1.5

STEP = 2
MINIMAX_VIDEO = 3

MODEL_PRICE = {
    "o1:free": FREE,
    # "claude-3-7-sonnet-code:free": "claude-3-7-sonnet-code"
    "claude-3-7-sonnet-code:free": 0.0001,

    "black-forest-labs/FLUX.1-dev": 0.0001,
    "black-forest-labs/FLUX.1-pro": 0.0001,

    "gpt-search": 0.02,

    "gemini-2.0-flash-search": 0.01,
    "gemini-2.0-flash-exp-image-generation": 0.03,

    "gemini-2.5-flash-audio": 0.025,
    "gemini-2.5-pro-audio": 0.05,

    "gemini-2.5-flash-video": 0.05,
    "gemini-2.5-pro-video": 0.1,

    "images": FREE,
    # rix
    "kling_image": 0.05,
    "kling_virtual_try_on": 1,
    "kling_effects": 1,

    "kling_video": 1.2,
    "kling_extend": 1.2,
    "kling_lip_sync": 1.2,

    "minimax_files_retrieve": 0.01,

    "minimax_s2v-01": MINIMAX_VIDEO * 1.5,

    "minimax_i2v-01": MINIMAX_VIDEO,
    "minimax_i2v-01-live": MINIMAX_VIDEO,
    "minimax_i2v-01-director": MINIMAX_VIDEO,

    "minimax_t2v-01": MINIMAX_VIDEO,
    "minimax_t2v-01-director": MINIMAX_VIDEO,

    "minimax_video-01": MINIMAX_VIDEO,
    "minimax_video-01-live2d": MINIMAX_VIDEO,

    # free

    # chatfire
    "ppu-0001": 0.0001,
    "ppu-001": 0.001,
    "ppu-01": 0.01,
    "ppu-1": 0.1,
    "api-oss": 0.01,
    "chatfire-translator": 0.01,
    "chatfire-all": 0.0001,
    "chatfire-law": 0.01,

    "sora-1:1-480p-5s": 1.2,
    "dall-e-3": 0.03,

    # 智能体
    "ppt": 0.1,
    "ppt-islide": 0.1,

    # grok
    "grok-3": 0.01,
    "grok-3-image": 0.02,

    # 虚拟换衣fish
    "api-kolors-virtual-try-on": 0.1,
    "official-api-kolors-virtual-try-on": 0.8,

    # 语音克隆
    "official-api-fish-model": 0.1,
    "official-api-fish-tts": 0.01,

    # 官方api
    "official-api-cogvideox": 0.1,
    "official-api-kling-image": 0.02,
    "official-api-kling-video": 0.5,

    "official-api-vidu": 0.5,

    "official-api-hailuo-video": 0.5,
    "api-hailuo-video": 0.3,

    "api-videos-seedream-3.0": 0.5,

    "api-kling-video/v2/master/text-to-video": 5,
    "api-kling-video/v2/master/image-to-video": 5,

    # delle3
    "api-images-kling": 0.04,
    "api-images-hunyuan": 0.04,
    "api-images-cogview-3": 0.01,
    "api-images-stable-diffusion": 0.01,

    "api-images-recraftv3": 0.1,
    "api-images-seededit": 0.1,

    "seedream-3.0": 0.05,
    "chat-seedream-3.0": 0.05,

    "seededit": 0.1,
    "chat-seededit": 0.1,

    "api-tripo3d": 0.1,

    # 图片 音频 视频
    "recraftv3": 0.1,  # 官方的
    "recraft-v3": 0.1,  # d3
    "recraft-api": 0.1,
    "chat-recraftv3": 0.1,

    "flux-pro-1.1-ultra": 0.2,
    "ideogram-ai/ideogram-v2": 0.2,
    "ideogram-ai/ideogram-v2-turbo": 0.1,

    "api-asr": 0.01,
    "api-stt": 0.01,
    "api-tts": 0.01,

    "kolors": 0.02,
    "kling": 0.02,

    "api-hunyuan-video": 0.1,

    "deepseek-ai/Janus-Pro-7B": 0.01,

    # replicate
    "api-replicate-flux-1.1-pro": 0.040,
    "api-replicate-flux-1.1-pro-ultra": 0.060,
    "api-replicate-flux-dev": 0.025,
    "api-replicate-flux-pro": 0.055,
    "api-replicate-flux-schnell": 0.003,
    "api-replicate-ideogram-v2": 0.080,
    "api-replicate-ideogram-v2-turbo": 0.050,
    "api-replicate-recraft-v3": 0.040,
    "api-replicate-recraft-v3-svg": 0.080,
    "api-replicate-stable-diffusion-3": 0.035,
    "api-replicate-stable-diffusion-3.5-large": 0.065,
    "api-replicate-stable-diffusion-3.5-large-turbo": 0.040,
    "api-replicate-stable-diffusion-3.5-medium": 0.035,

    # sd
    "stable-diffusion-xl-base-1.0": 0.01,
    "stable-diffusion-2-1": 0.01,
    "stable-diffusion": 0.01,
    "stable-diffusion-3-medium": 0.02,
    "stable-diffusion-3-5-large": 0.05,
    "chat-stable-diffusion-3-5-large": 0.05,

    "flux": 0.01,
    "flux-schnell": 0.01,
    "flux-dev": 0.03,
    "flux-pro": 0.05,
    "flux-pro-max": 0.1,
    "flux.1.1-pro": 0.1,
    "black-forest-labs/flux.1.1-pro": 0.1,

    "step-1x-medium": 0.2,
    "chat-step-1x-medium": 0.2,

    "chat-flux-schnell": 0.01,
    "chat-flux-dev": 0.03,
    "chat-flux-pro": 0.05,
    "chat-flux-pro-max": 0.1,
    "chat-ideogram": 0.3,

    "chat-kolors": 0.02,
    "chat-kling": 0.02,
    "chat-video": 0.1,
    "chat-video-kling": 0.1,
    "chat-video-gen3": 0.1,
    "chat-video-vidu": 0.1,
    "chat-video-vidu-vip": 0.3,
    "chat-flux.1.1-pro": 0.1,

    # aitools
    "api-aitools": 0.007,
    "api-images-edits-remove-watermark": 0.01,  # mask
    "api-images-edits-remove-watermark-hunyuan": 0.01,

    "api-images-edits-remove-watermark-textin": 0.02,  # remove-watermark

    "api-images-edits-clarity": 0.01,
    "api-images-edits-clarity-hunyuan": 0.01,
    "api-images-edits-clarity-baidu": 0.01,  # 官方api

    "api-images-edits-expand": 0.01,
    "api-images-edits-rmbg-2.0": 0.01,

    # 文档智能
    "api-textin": 0.02,
    "api-pdf-to-markdown": 0.02,
    "api-file-to-text": 0.02,
    "api-ocr": 0.01,
    "api-ocr-pro": 0.02,

    # api
    "api-watermark-remove": 0.007,
    "api-idphotos": 0.01,
    "api-pcedit": 0.007,
    "api-faceswap": 0.01,

    "api-kling": 0.1,
    "api-kling-vip": 0.5,

    "api-kling-v1.6-std-5s": 1 * 0.8,
    "api-kling-v1.6-std-10s": 2 * 0.8,
    "api-kling-v1.6-pro-5s": 1 * 0.8 * 1.75,
    "api-kling-v1.6-pro-10s": 2 * 0.8 * 1.75,

    "api-vidu": 0.09,
    "api-vidu-vip": 0.6,

    "api-cogvideox": 0.1,
    "api-cogvideox-vip": 0.4,

    #
    "runway_video": 0.6,
    "runway_video2video": 0.6,
    "runway_act_one": 1,
    "runwayml_image_to_video": 0.8,

    "api-runwayml-gen3": 0.1,

    "api-translator": 0.0001,
    "api-voice-clone": 0.01,

    # textin
    "api-textin-image/watermark_remove": 0.03,

    # suno
    "suno_music": 0.4,
    "suno_lyrics": 0.01,
    "suno_uploads": 0.01,
    "suno_upload": 0.01,
    "suno_concat": 0.01,
    "chirp-v3-5": 0.5,
    "chat-suno": 0.5,

    # all
    "o1-plus": 0.2,
    "o1-pro": 1.2,

    "o1-mini-all": 0.2,
    "o1-preview-all": 0.6,

    "o3": 0.6 * 0.8,
    "o3-mini": 0.05,
    "o3-mini-high": 0.1,

    "o4-mini": 0.05 * 0.8,
    "o4-mini-high": 0.15 * 0.8,

    "gpt-4-all": 0.1,
    "gpt-4o-all": 0.1,
    "gpt-4o-image": 0.05,
    "sora-image": 0.1,
    "gpt-image-1": 0.1,

    "gpt-4-gizmo-*": 0.1,
    "advanced-voice": 1,

    "claude-3-5-sonnet-all": 0.2,

    # 前置联网
    "net-gpt-3.5-turbo": 0.01,
    "net-gpt": 0.01,
    "net-gpt-4": 0.1,
    "perplexity": 0.01,
    "net-claude": 0.015,
    "meta-search": 0.02,

    # 逆向
    "cogview-3": 0.01,
    "cogview-3-plus": 0.02,

    "glm-4-all": 0.01,

    "kimi-all": 0.01,
    "kimi-math": 0.01,
    "kimi-k1": 0.05,
    "kimi-search": 0.01,
    "kimi-research": 0.05,

    "spark-all": 0.01,
    "step-1-all": 0.01,
    "step-all": 0.01,
    "hunyuan-all": 0.01,

    "chat-stable-diffusion-3": 0.02,

    # 搜索
    "ai-search": 0.01,
    "ai-search:scholar": 0.01,

    "ai-search-pro": 0.1,
    "ai-search-pro:scholar": 0.1,

    "deepseek-search": 0.01,
    'deepseek-r1-search': 0.01,
    "deepseek-r1-search-pro": 0.02,
    "deepseek-r1-search-pro-thinking": 0.02,
    'deepseek-reasoner-search': 0.01,

    # MJ
    "mj-chat": 0.3,

    "mj_fast_blend": 0.1 * MJ_FAST,
    "mj_fast_custom_oom": 0,
    "mj_fast_describe": 0.05 * MJ_FAST,
    "mj_fast_high_variation": 0.1 * MJ_FAST,
    "mj_fast_imagine": 0.1 * MJ_FAST,
    "mj_fast_inpaint": 0,
    "mj_fast_low_variation": 0.1 * MJ_FAST,
    "mj_fast_modal": 0.1 * MJ_FAST,
    "mj_fast_pan": 0.1 * MJ_FAST,
    "mj_fast_pic_reader": 0,
    "mj_fast_prompt_analyzer": 0,
    "mj_fast_prompt_analyzer_extended": 0,
    "mj_fast_reroll": 0.1 * MJ_FAST,
    "mj_fast_shorten": 0.1 * MJ_FAST,
    "mj_fast_upload": 0.1 * MJ_FAST,
    "mj_fast_upscale": 0.05 * MJ_FAST,
    "mj_fast_upscale_creative": 0.1 * MJ_FAST,
    "mj_fast_upscale_subtle": 0.1 * MJ_FAST,
    "mj_fast_variation": 0.1 * MJ_FAST,
    "mj_fast_zoom": 0.1 * MJ_FAST,

    "mj_relax_imagine": 0.05 * MJ_RELAX,

    "mj_relax_blend": 0.08,
    "mj_relax_custom_oom": 0,
    "mj_relax_describe": 0.04 * MJ_RELAX,
    "mj_relax_high_variation": 0.08 * MJ_RELAX,
    "mj_relax_inpaint": 0,
    "mj_relax_low_variation": 0.08 * MJ_RELAX,
    "mj_relax_modal": 0.08 * MJ_RELAX,
    "mj_relax_pan": 0.08 * MJ_RELAX,
    "mj_relax_pic_reader": 0,
    "mj_relax_prompt_analyzer": 0,
    "mj_relax_prompt_analyzer_extended": 0,
    "mj_relax_reroll": 0.08 * MJ_RELAX,
    "mj_relax_shorten": 0.08 * MJ_RELAX,
    "mj_relax_upload": 0.01 * MJ_RELAX,
    "mj_relax_upscale": 0.04 * 1,
    "mj_relax_upscale_creative": 0.08 * 1,
    "mj_relax_upscale_subtle": 0.08 * 1,
    "mj_relax_variation": 0.08 * 1,
    "mj_relax_zoom": 0.08 * MJ_RELAX,

}

MODEL_RATIO = {
    # 智能体
    "gpt-4-plus": 2.5,
    "gpt-4o-plus": 2.5,
    "jina-deepsearch": 2,
    "deepresearch": 2,
    "deepsearch": 2,

    # embedding & rerank
    "rerank-multilingual-v2.0": 0.1,
    "rerank-multilingual-v3.0": 0.1,
    "BAAI/bge-reranker-v2-m3": 0.1,
    "jina-reranker-v2-base-multilingual": 0.1,
    "netease-youdao/bce-reranker-base_v1": 0.1,
    "BAAI/bge-m3": 0.1,
    "bge-m3": 0.1,

    "bge-large-zh-v1.5": 0.1,
    "BAAI/bge-large-zh-v1.5": 0.1,
    "bge-large-en-v1.5": 0.1,
    "BAAI/bge-large-en-v1.5": 0.1,

    "text-embedding-3-large": 0.5,
    "text-embedding-3-small": 0.5,
    "text-embedding-ada-002": 0.5,

    # 百川
    'baichuan4-turbo': 7.5,
    'baichuan4-air': 0.49,
    'baichuan4': 50,
    'baichuan3-turbo': 6,
    'baichuan3-turbo-128k': 12,
    'baichuan2-turbo': 4,

    "claude-3-5-haiku-20241022": 0.5,
    "anthropic/claude-3-5-haiku-20241022:beta": 0.5,

    # grok
    "grok-2": 1,
    "grok-2-1212": 1,
    "grok-2-vision-1212": 1,
    "grok-3": 2,
    "grok-3-deepsearch": 2,
    "grok-3-reasoner": 2,
    "grok-3-deepersearch": 2,

    "grok-3-beta": 1.5,
    "grok-3-fast-beta": 2.5,
    "grok-3-mini-beta": 0.15,
    "grok-3-mini-fast-beta": 0.3,

    # 定制
    "lingxi-all": 1,

    "kimi": 5,
    "kimi-128k": 5,

    # 智谱 https://www.bigmodel.cn/pricing
    'glm-4-9b-chat': 0.1,
    "glm-3-turbo": 0.1,
    "glm-4-flash": 0.1,  # "glm-z1-flash": "glm-z1-flash==THUDM/GLM-4-9B-0414"

    "glm-4-air": 0.25,  # THUDM/GLM-4-32B-0414
    "glm-4-airx": 0.05,

    "glm-4": 2.5,
    "glm-4-0520": 2.5,
    "glm-4-plus": 2.5,

    "glm-4v-flash": 0.1,
    "glm-4v": 2.5,
    "glm-4v-plus": 2,

    "glm-zero": 5,
    "glm-zero-preview": 5,

    "glm-z1-flash": 0.1,  # "glm-z1-flash": "glm-z1-flash==THUDM/GLM-Z1-9B-0414"
    "glm-z1-air": 0.25,  # "glm-z1-air": "glm-z1-air==THUDM/GLM-Z1-32B-0414"
    "glm-z1-airx": 2.5,  # "glm-z1-airx": "glm-z1-airx==THUDM/GLM-Z1-Rumination-32B-0414"

    # 月之暗面 https://platform.moonshot.cn/docs/price/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
    "kimi-latest-8k": 1,
    "kimi-latest-32k": 2.5,
    "kimi-latest-128k": 5,

    "moonshot-v1-8k": 1,
    "moonshot-v1-32k": 2.5,
    "moonshot-v1-128k": 5,

    "kimi-vl-a3b-thinking": 1,
    "moonshot-v1-8k-vision-preview": 1,
    "moonshot-v1-32k-vision-preview": 2.5,
    "moonshot-v1-128k-vision-preview": 5,

    # 阿里千问 https://dashscope.console.aliyun.com/billing
    "qwen-long": 0.25,
    "qwen-turbo": 0.05,
    "qwen-plus": 0.4 * 1,
    "qwen-max": 1.2 * 1,
    "qwen-max-longcontext": 20,
    "qwen-turbo-2024-11-01": 0.15,
    "qwen-max-latest": 1.2 * 1,
    "qwen2.5-max": 1.2 * 1,
    "qwen-max-2025-01-25": 1.2 * 1,

    "qwen-vl-max-latest": 1.5,
    "qwen-vl-plus-latest": 0.75,

    "qwen2.5-vl-7b-instruct": 0.15,
    "qwen2.5-vl-32b-instruct": 0.5,
    "qwen2.5-vl-72b-instruct": 1.5,

    "qwen2.5-coder-7b-instruct": 0.05,
    "qwen2.5-7b-instruct": 0.05,
    "qwen2.5-14b-instruct": 0.25,
    "qwen2.5-32b-instruct": 1,
    "qwen2.5-72b-instruct": 2,
    "qwen2.5-math-72b-instruct": 2,
    "qwen2.5-coder-32b-instruct": 0.5,
    # https://bailian.console.aliyun.com/?tab=doc#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2840914.html%239f8890ce29g5u
    "qwen3-0.6b": 0.1,
    "qwen3-1.7b": 0.15,
    "qwen3-4b": 0.2,
    "qwen3-8b": 0.25,
    "qwen3-14b": 0.5,
    "qwen3-32b": 1,
    "qwen3-30b-a3b": 0.75,
    "qwen3-235b-a22b": 2,

    "qwq-32b": 1,
    "qwq-plus": 0.8,
    "qwq-max": 0.8,
    "qwq-max-search": 2,
    "qwen-max-search": 2,

    "qvq-72b-preview": 2,
    "qvq-max-2025-03-25": 4,

    "qwen1.5-7b-chat": 0.05,  # 特价
    "qwen1.5-14b-chat": 0.7,
    "qwen1.5-32b-chat": 1.75,
    "qwen1.5-110b-chat": 3.5,

    "qwen2-1.5b-instruct": 0.05,  # 特价
    "qwen2-7b-instruct": 0.05,  # 特价
    "qwen2-57b-a14b-instruct": 1.26,
    "qwen2-72b-instruct": 4.13,
    "farui-plus": 10,  # 法律大模型
    'qwen2-math-72b-instruct': 4.13,

    # 讯飞 https://xinghuo.xfyun.cn/sparkapi?scr=price
    'spark-lite': 0.05,  # 特价
    'spark-pro': 15 / 5,  # 特价
    'spark-max': 15,
    'spark-ultra': 50,

    # 阶跃星辰 https://platform.stepfun.com/docs/pricing/details
    "step-1-flash": 0.5 * STEP,

    "step-1-8k": 2.5 * STEP,
    "step-1-32k": 7.5 * STEP,
    "step-1-256k": 47.5 * STEP,

    "step-2-16k": 19 * STEP,
    "step-2-mini": 0.5 * STEP,
    "step-2-16k-exp": 19 * STEP,

    "step-1v-8k": 2.5 * STEP,
    "step-1.5v-mini": 4 * STEP,
    "step-1v-32k": 7.5 * STEP,
    "step-1o-vision-32k": 7.5 * STEP,

    # 零一万物 https://platform.lingyiwanwu.com/docs#%E8%AE%A1%E8%B4%B9%E5%8D%95%E5%85%83
    "yi-spark": 0.05,  # 特价
    "yi-1.5-6b-chat": 0.05,  # 特价
    "yi-1.5-9b-chat-16k": 0.05,  # 特价
    "yi-34b-chat": 0.63,
    "yi-34b-chat-0205": 0.63,
    "yi-1.5-34b-chat-16k": 0.63,

    "yi-lightning": 0.5,
    "yi-vision-v2": 3,

    "yi-vision": 3,
    "yi-large": 10,
    "yi-large-turbo": 6,
    "yi-large-rag": 12.5,
    "yi-medium": 1.25,
    "yi-medium-200k": 6,

    # minimax https://platform.minimaxi.com/document/price?id=6433f32294878d408fc8293e
    "abab6.5-chat": 15 / 7.5,
    "abab6.5s-chat": 5,
    "abab6.5t-chat": 2.5,
    "abab6.5g-chat": 2.5,
    "abab5.5-chat": 7.5,
    "abab5.5s-chat": 2.5,

    # deepseek
    "deepseek-prover-v2-671b": 2,
    "deepseek-v3": 1,
    "deepseek-v3-0324": 1,
    "deepseek-v3-250324": 1,

    "deepseek-v3-8k": 0.5,
    "deepseek-v3-128k": 5,
    "deepseek-chat": 1,

    "deepseek-chat-8k": 0.5,
    "deepseek-chat-64k": 5,
    "deepseek-chat-164k": 5,
    "deepseek-chat:function": 4,
    "deepseek-vl2": 0.5,
    "deepseek-ai/deepseek-vl2": 0.5,

    'deepseek-r1': 2,
    'deepseek-r1-8k': 1,
    'deepseek-reasoner': 2,
    'deepseek-reasoner-8k': 1,
    "deepseek-r1-250120": 2,

    "deepseek-search": 1,
    'deepseek-r1-search': 2,
    'deepseek-reasoner-search': 2,

    'deepseek-r1-think': 2,
    'deepseek-reasoner-think': 2,

    "deepseek-r1-plus": 2,

    # deepseek-r1:1.5b,deepseek-r1-distill-qwen-1.5b,deepseek-r1:7b,deepseek-r1-distill-qwen-7b,deepseek-r1:8b,deepseek-r1-distill-llama-8b,deepseek-r1:14b,deepseek-r1-distill-qwen-14b,deepseek-r1:32b,deepseek-r1-distill-qwen-32b,deepseek-r1:70b,deepseek-r1-distill-llama-70b
    "deepseek-r1:1.5b": 0.1,
    'deepseek-r1-lite': 0.1,  # think
    "deepseek-r1-distill-qwen-1.5b": 0.1,
    "deepseek-r1:7b": 0.2,
    "deepseek-r1-distill-qwen-7b": 0.2,
    "deepseek-r1:8b": 0.3,
    "deepseek-r1-distill-llama-8b": 0.3,

    "deepseek-r1:14b": 0.5,
    "deepseek-r1-distill-qwen-14b": 0.5,

    "deepseek-r1:32b": 1,
    "deepseek-r1-distill-qwen-32b": 1,

    "deepseek-r1:70b": 1.5,
    "deepseek-r1-distill-llama-70b": 1.5,

    "hunyuan-t1": 1,
    "hunyuan-t1-search": 1,

    "deepseek-r1-metasearch": 2,
    "meta-deepresearch": 2,

    # 豆包
    "doubao-1-5-pro-32k": 0.4,
    "doubao-1-5-pro-32k-250115": 0.4,
    "doubao-1-5-pro-256k": 2.5,
    "doubao-1-5-pro-256k-250115": 2.5,
    "doubao-1-5-vision-pro-32k": 1.5,
    "doubao-1-5-vision-pro-32k-250115": 1.5,

    "doubao-lite-128k": 0.4,
    "doubao-lite-32k": 0.15,
    "doubao-lite-32k-character": 0.15,
    "doubao-lite-4k": 0.15,
    "doubao-1.5-lite-32k": 0.15,

    "doubao-pro-4k": 0.4,
    "doubao-pro-32k": 0.4,
    "doubao-pro-32k-character": 0.4,
    "doubao-pro-128k": 2.5,
    "doubao-pro-256k": 5,
    "doubao-1.5-pro-32k": 0.8 / 2,
    "doubao-1.5-pro-256k": 5 / 2,

    "doubao-1.5-vision-pro-32k": 1.5,
    "doubao-1.5-vision-pro-250328": 1.5,

    "doubao-vision-lite-32k": 0.75,
    "doubao-vision-pro-32k": 1.5,

    "doubao-1-5-pro-thinking": 2,

    "doubao-1-5-vision-thinking": 2,
    "doubao-1-5-thinking-pro-250415": 2,
    "doubao-1-5-thinking-pro-vision": 2,
    "doubao-1-5-thinking-pro-vision-250415": 2,
    "doubao-1-5-thinking-pro-m-250415": 2,

    # 商汤 https://platform.sensenova.cn/pricing
    # https://platform.sensenova.cn/doc?path=/pricingdoc/pricing.md
    "SenseChat-Turbo": 1 / 5,  # 特价
    "SenseChat": 6 / 5,  # 特价
    "SenseChat-32K": 18 / 5,  # 特价
    "SenseChat-128K": 30 / 5,  # 特价
    "SenseChat-5": 20 / 5,  # 最新版本#  特价
    "SenseChat-Vision": 50 / 5,  # 图生文#  特价
    "SenseChat-5-Cantonese": 13.5 / 5,  # 粤语大模型#  特价

    # 腾讯混元
    "hunyuan": 7.143,
    "hunyuan-lite": 4,
    "hunyuan-pro": 50,
    "hunyuan-standard": 5,
    "hunyuan-standard-256k": 60,

    # 百度文心
    "ERNIE-Speed-8K": 0.2858,
    "ERNIE-Speed-128K": 0.2858,

    "ERNIE-3.5-8K": 2,
    "ERNIE-3.5-128K": 4,

    "ERNIE-4.0-Turbo-8K": 15,
    "ERNIE-4.0-8K": 10,

    "text-ada-001": 0.2,
    "text-babbage-001": 0.25,
    "text-davinci-edit-001": 10,

    "omni-moderation-latest": 0.1,
    "text-moderation-latest": 0.1,

    "tts-1": 7.5,
    "tts-1-1106": 7.5,
    "tts-1-hd": 15,
    "tts-1-hd-1106": 15,
    "whisper-1": 15,

    "claude-3-haiku-20240307": 0.125,
    "claude-3-sonnet-20240229": 1.5,

    "claude-3-opus-20240229": 7.5,
    "anthropic/claude-3-opus:beta": 7.5,  # openrouter

    "claude-3-5-sonnet-20240620": 1.5,
    "claude-3-5-sonnet-20241022": 1.5,

    "anthropic/claude-3.5-sonnet": 1.5,
    "anthropic/claude-3.5-sonnet:beta": 4,  # 1022

    "claude-3-7-sonnet-thinking": 1.5,
    "claude-3-7-sonnet-20250219-thinking": 1.5,
    "claude-3-7-sonnet-latest": 1.5,
    "claude-3-7-sonnet-latest-thinking": 1.5,

    "claude-3-7-sonnet-20250219": 1.5,

    "deepclaude": 1.5,
    "deep-claude": 1.5,

    "deep-gemini": 1.5,
    "deep-grok": 1.5,

    "command": 0.5 * 2,
    "command-light": 0.5 * 2,
    "command-light-nightly": 0.5 * 2,
    "command-nightly": 0.5 * 2,
    "command-r": 0.25 * 2,
    "command-r-plus": 1.5 * 2,

    "command-r-08-2024": 0.075 * 2,
    "command-r-plus-08-2024": 1.25 * 2,

    "dall-e-3": 16,

    "gemini-all": 1.5,
    "gemini-1.0-pro-001": 1,
    "gemini-1.0-pro-latest": 1,
    "gemini-1.0-pro-vision-001": 1,
    "gemini-1.0-pro-vision-latest": 1,
    "gemini-exp-1206": 1,

    "gemini-1.5-flash": 0.1,
    "gemini-1.5-flash-002": 0.3,  # 重定向到openrouter
    "google/gemini-flash-1.5-8b": 0.3,  # openrouter  $0.0375 $0.15

    "gemini-1.5-flash-latest": 0.1,
    "gemini-1.5-flash-exp-0827": 0.1,
    "google/gemini-flash-1.5-exp": 0.1,  # openrouter免费
    "google/gemini-flash-1.5-8b-exp": 0.1,  # openrouter免费

    "gemini-2.0-flash": 0.0625,
    "gemini-2.0-flash-001": 0.0625,
    "gemini-2.0-flash-lite-preview-02-05": 0.0625,
    "gemini-2.0-flash-exp": 0.0625,
    "gemini-2.0-flash-thinking-exp": 1,
    "gemini-2.0-flash-thinking-exp-1219": 1,
    "gemini-2.0-flash-thinking-exp-01-21": 1,

    "gemini-2.5-flash-preview-04-17": 0.075,

    "gemini-2.0-pro": 0.625,
    "gemini-2.0-pro-exp": 0.625,
    "gemini-2.0-pro-exp-02-05": 0.625,
    "gemini-2.5-pro-exp-03-25": 0.625,
    "gemini-2.5-pro-preview-03-25": 0.625,
    "gemini-2.5-pro-preview-05-06": 0.625,

    "gemini-1.5-pro-001": 1.25,
    "gemini-1.5-pro-002": 1.25,
    "gemini-1.5-pro-latest": 1.75,
    "gemini-1.5-pro-exp-0827": 1.75,
    "google/gemini-pro-1.5-exp": 1,  # openrouter免费

    "gemini-1.5-pro": 2,
    "gemini-pro": 1,
    "gemini-pro-vision": 1,
    "gemini-ultra": 1,

    "gemini-2.5-flash-thinking": 0.15,
    "gemini-2.5-flash-preview-04-17-thinking": 0.15 * 2,
    "gemini-2.5-pro-thinking": 0.625 * 2,
    "gemini-2.5-pro-exp-03-25-thinking": 0.625 * 2,
    "gemini-2.5-pro-preview-03-25-thinking": 0.625 * 2,

    "gpt-3.5-turbo": 0.75,
    "gpt-3.5-turbo-0125": 0.25,
    "gpt-3.5-turbo-0613": 0.75,
    "gpt-3.5-turbo-1106": 0.5,
    "gpt-3.5-turbo-16k": 1.5,
    "gpt-3.5-turbo-16k-0613": 1.5,
    "gpt-3.5-turbo-instruct": 0.75,
    "gpt-4": 15,
    "gpt-4-0125-preview": 5,
    "gpt-4-0613": 15,
    "gpt-4-1106-preview": 5,
    "gpt-4-1106-vision-preview": 5,
    "gpt-4-32k": 30,
    "gpt-4-32k-0613": 30,
    "gpt-4-all": 15,
    "gpt-4-gizmo-*": 15,
    "gpt-4-turbo": 5,
    "gpt-4-turbo-2024-04-09": 5,
    "gpt-4-turbo-preview": 5,
    "gpt-4-vision-preview": 5,
    "chatgpt-4o-latest": 2.5,
    "gpt-4o-realtime-preview": 2.5,
    "gpt-4o-realtime-preview-2024-10-01": 2.5,

    "gpt-4o-mini-audio-preview": 0.15 / 2,

    "gpt-4o-audio-preview": 2.5 / 2,
    "gpt-4o-audio-preview-2024-12-17": 2.5 / 2,

    "gpt-4o": 1.25,
    "gpt-4o-all": 2.5,  # 逆向
    "gpt-4o-2024-05-13": 1.25,
    "gpt-4o-mini": 0.075,
    "gpt-4o-mini-2024-07-18": 0.075,
    "gpt-4o-2024-08-06": 1.25,
    "gpt-4o-2024-11-20": 1.25,
    "gpt-4.5-preview-2025-02-27": 37.5,

    "gpt-4.1": 1,
    "gpt-4.1-mini": 0.2,
    "gpt-4.1-nano": 0.05,
    "gpt-4.1-2025-04-14": 1,
    "gpt-4.1-mini-2025-04-14": 0.2,
    "gpt-4.1-nano-2025-04-14": 0.05,

    "o1": 7.5,
    "o1-2024-12-17": 7.5,

    "o1-mini": 0.55,
    "o1-mini-2024-09-12": 0.55,

    "o1-preview": 7.5,
    "o1-preview-2024-09-12": 7.5,
    "o3-mini": 0.55,
    "o4-mini": 0.55,
    "gpt-image-1": 2.5,

    # 硅基
    "llama-3.1-8b-instruct": 0.01,
    "meta-llama/Meta-Llama-3.1-8B-Instruct": 0.01,
    "llama-3.1-70b-instruct": 2,
    "meta-llama/Meta-Llama-3.1-70B-Instruct": 2,
    "llama-3.1-405b-instruct": 5,
    "meta-llama/Meta-Llama-3.1-405B-Instruct": 5,

    "meta-llama/Llama-3.3-70B-Instruct": 2,
    "llama-3.3-70b-instruct": 2,

    "meta-llama/Llama-4-Scout-17B-16E-Instruct": 0.1,
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": 0.2,

    # groq https://console.groq.com/docs/models
    "llama3-8b-8192": 0.01,
    "llama3-70b-8192": 0.01,
    "mixtral-8x7b-32768": 0.01,
    "llama-3.1-8b-instant": 0.01,
    "llama-3.1-70b-versatile": 3,

    # sili
    "gemma2-9b-it": 0.1,
    "gemma2-27b-it": 0.5,
    "google/gemma-3-27b-it": 0.5,

    "internlm2_5-7b-chat": 0.01,
    'internlm2_5-20b-chat': 0.5,
    "internlm3-8b-instruct": 0.25,

    "acge_text_embedding": 1,
    "dmeta-embedding-zh-q4": 1,

    # vision 视觉
    "minicpm-v": 0.35 / 2,
    "minicpm-v2.6": 0.35 / 2,
    "llama-3.2-11b-vision": 0.1,

    "internvl2-8b": 0.35 / 2,
    "internvl2-26b": 1 / 2,
    "internvl2-llama3-76b": 2,

    "qwen2-vl-7b-instruct": 0.5,
    "qwen2-vl-72b-instruct": 2,
    "Qwen/Qwen2-VL-72B-Instruct": 2,

    # 临时
    "microsoft/phi-4": 0.035,
    "microsoft/phi-4-reasoning": 0.035,
    "microsoft/phi-4-reasoning-plus": 0.035 * 2,
    "mistral-small-3.1-24b-instruct": 0.1,
    "mistral-small-24b-instruct-2501": 0.1,

    "meta-llama/Llama-3.2-11B-Vision-Instruct": 0.1,

}

COMPLETION_RATIO = {
    # 智能体
    "gpt-4-plus": 5,
    "gpt-4o-plus": 5,
    "jina-deepsearch": 4,
    "deepresearch": 4,
    "deepsearch": 4,

    # kimi
    "kimi-latest-8k": 5,
    "kimi-latest-32k": 4,
    "kimi-latest-128k": 3,

    "moonshot-v1-8k": 5,
    "moonshot-v1-32k": 4,
    "moonshot-v1-128k": 3,

    "kimi-vl-a3b-thinking": 5,
    "moonshot-v1-8k-vision-preview": 5,
    "moonshot-v1-32k-vision-preview": 4,
    "moonshot-v1-128k-vision-preview": 3,

    "grok-2": 5,
    "grok-2-1212": 5,
    "grok-2-vision-1212": 5,

    "grok-3": 5,
    "grok-3-deepsearch": 5,
    "grok-3-reasoner": 5,
    "grok-3-deepersearch": 5,

    "grok-3-beta": 5,
    "grok-3-fast-beta": 5,
    "grok-3-mini-beta": 5 / 3,
    "grok-3-mini-fast-beta": 4 / 0.6,

    "claude-3-5-haiku-20241022": 5,
    "anthropic/claude-3-5-haiku-20241022:beta": 5,

    "gpt-4-all": 4,
    "gpt-4-gizmo-*": 4,
    "gpt-4o-all": 4,
    "gpt-4.5-preview-2025-02-27": 2,

    "o1-mini": 4,
    "o1-preview": 4,
    "o1-mini-2024-09-12": 4,
    "o1-preview-2024-09-12": 4,
    "o3-mini": 4,
    "o4-mini": 4,

    "gpt-4o-realtime-preview": 4,
    "gpt-4o-realtime-preview-2024-10-01": 4,
    "gpt-4o-2024-11-20": 4,

    "gpt-4o-mini-audio-preview": 4,

    "gpt-4o-audio-preview": 4,
    "gpt-4o-audio-preview-2024-12-17": 4,

    "gpt-4.1": 4,
    "gpt-4.1-mini": 4,
    "gpt-4.1-nano": 4,
    "gpt-4.1-2025-04-14": 4,
    "gpt-4.1-mini-2025-04-14": 4,
    "gpt-4.1-nano-2025-04-14": 4,

    "gpt-image-1": 8,

    # claude
    "claude-3-opus-20240229": 5,
    "anthropic/claude-3-opus:beta": 5,  # openrouter

    "anthropic/claude-3.5-sonnet": 5,
    "anthropic/claude-3.5-sonnet:beta": 5,

    "claude-3-7-sonnet-think": 5,
    "claude-3-7-sonnet-latest": 5,
    "claude-3-7-sonnet-20250219": 5,
    "claude-3-7-sonnet-latest-thinking": 5,

    "llama-3.1-70b-instruct": 2,
    "meta-llama/Meta-Llama-3.1-70B-Instruct": 2,

    "llama-3.1-405b-instruct": 6,
    "meta-llama/Meta-Llama-3.1-405B-Instruct": 6,

    "meta-llama/Llama-4-Scout-17B-16E-Instruct": 3,
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": 3,

    "llama-3.3-70b-instruct": 4,

    "command": 4,
    "command-light": 4,
    "command-light-nightly": 4,
    "command-nightly": 4,
    "command-r": 4,
    "command-r-plus": 4,

    "command-r-08-2024": 4,
    "command-r-plus-08-2024": 4,

    "ERNIE-Speed-8K": 3,
    "ERNIE-Speed-128K": 3,

    "ERNIE-3.5-8K": 3,
    "ERNIE-3.5-128K": 3,

    "ERNIE-4.0-Turbo-8K": 3,
    "ERNIE-4.0-8K": 3,

    "gemini-all": 5,
    "gemini-1.5-pro-001": 4,
    "gemini-1.5-pro-002": 4,
    "gemini-1.5-flash": 4,
    "gemini-1.5-flash-002": 4,

    "gemini-exp-1206": 5,

    "gemini-2.0-flash": 4,
    "gemini-2.0-flash-001": 4,

    "gemini-2.0-flash-exp": 5,

    "gemini-2.0-flash-thinking-exp": 5,
    "gemini-2.0-flash-thinking-exp-1219": 5,
    "gemini-2.0-flash-thinking-exp-01-21": 5,

    "gemini-2.0-flash-lite-preview-02-05": 4,
    "gemini-2.5-flash-preview-04-17": 4,

    "gemini-2.0-pro": 5,
    "gemini-2.0-pro-exp": 5,
    "gemini-2.0-pro-exp-02-05": 5,
    "gemini-2.5-pro-exp-03-25": 8,
    "gemini-2.5-pro-preview-03-25": 8,
    "gemini-2.5-pro-preview-05-06": 8,

    "gemma2-9b-it": 4,
    "gemma2-27b-it": 4,
    "google/gemma-3-27b-it": 4,
    # thinking
    "gemini-2.5-flash-thinking": 8,
    "gemini-2.5-flash-preview-04-17-thinking": 8,
    "gemini-2.5-pro-thinking": 8,
    "gemini-2.5-pro-exp-03-25-thinking": 8,
    "gemini-2.5-pro-preview-03-25-thinking": 8,

    "hunyuan-a52b-instruct": 5,
    "qwen2.5-coder-32b-instruct": 3,

    "qwen-turbo-2024-11-01": 3,
    "qwen/qwq-32b-preview": 3,
    "Qwen/QwQ-32B-Preview": 3,
    "qwq-32b": 3,

    "qwq-32b-preview": 3,
    "qvq-72b-preview": 3,

    "qwen-long": 4,
    "qwen-max": 4,
    "qwen-vl-max-latest": 3,
    "qwen-vl-plus-latest": 3,

    "qwen2.5-vl-7b-instruct": 4,
    "qwen2.5-vl-32b-instruct": 4,
    "qwen2.5-vl-72b-instruct": 4,

    "qwen2-vl-7b-instruct": 5,
    "qwen2-vl-72b-instruct": 5,
    "qwen-max-latest": 4,
    "qwen2.5-max": 4,
    "qwen-max-2025-01-25": 4,

    "qwen-plus": 2.5,

    "qwq-plus": 2.5,
    "qwq-max": 2.5,
    "qwq-max-search": 4,
    "qwen-max-search": 4,
    "qvq-max-2025-03-25": 4,

    "qwen2.5-7b-instruct": 4,
    "qwen2.5-14b-instruct": 4,
    "qwen2.5-32b-instruct": 4,
    "qwen2.5-72b-instruct": 4,
    "qwen2.5-math-72b-instruct": 4,

    "qwen3-0.6b": 4,
    "qwen3-1.7b": 4,
    "qwen3-4b": 4,

    "qwen3-8b": 4,
    "qwen3-14b": 4,
    "qwen3-32b": 4,
    "qwen3-30b-a3b": 4,
    "qwen3-235b-a22b": 3,

    "deepseek-vl2": 4,
    "deepseek-ai/deepseek-vl2": 4,

    # 豆包
    "doubao-lite-128k": 3,
    "doubao-lite-32k": 3,
    "doubao-lite-32k-character": 3,
    "doubao-lite-4k": 3,
    "doubao-1.5-lite-32k": 2,

    "doubao-pro-4k": 3,
    "doubao-pro-32k": 3,
    "doubao-pro-32k-241215": 3,
    "doubao-pro-32k-character": 3,
    "doubao-pro-128k": 3,
    "doubao-pro-256k": 3,
    "doubao-1.5-pro-32k": 3,
    "doubao-1.5-pro-256k": 3,

    "doubao-1.5-vision-pro-32k": 3,
    "doubao-1.5-vision-pro-250328": 3,

    "doubao-1-5-vision-pro-32k": 3,
    "doubao-1-5-vision-pro-32k-250115": 3,

    "doubao-vision-lite-32k": 3,
    "doubao-vision-pro-32k": 3,

    "doubao-1-5-pro-32k": 1.25,
    "doubao-1-5-pro-32k-250115": 1.25,
    "doubao-1-5-pro-256k": 1.8,
    "doubao-1-5-pro-256k-250115": 1.8,

    "doubao-1-5-vision-thinking": 4,
    "doubao-1-5-pro-thinking": 4,
    "doubao-1-5-thinking-pro": 4,
    "doubao-1-5-thinking-pro-250415": 4,
    "doubao-1-5-thinking-pro-vision": 4,
    "doubao-1-5-thinking-pro-vision-250415": 4,
    "doubao-1-5-thinking-pro-m-250415": 4,

    "deepseek-prover-v2-671b": 4,
    "deepseek-r1:1.5b": 4,
    "deepseek-r1-distill-qwen-1.5b": 4,
    "deepseek-r1:7b": 4,
    "deepseek-r1-distill-qwen-7b": 4,
    "deepseek-r1:8b": 4,
    "deepseek-r1-distill-llama-8b": 4,
    "deepseek-r1:14b": 4,
    "deepseek-r1-distill-qwen-14b": 4,
    "deepseek-r1:32b": 4,
    "deepseek-r1-distill-qwen-32b": 4,
    "deepseek-r1:70b": 4,
    "deepseek-r1-distill-llama-70b": 4,

    "hunyuan-t1": 4,
    "hunyuan-t1-search": 4,

    "deepseek-r1-metasearch": 4,
    "meta-deepresearch": 4,

    "deepseek-v3": 4,
    "deepseek-v3-0324": 4,
    "deepseek-v3-250324": 4,
    "deepseek-chat": 4,

    'deepseek-r1': 4,
    'deepseek-reasoner': 4,
    "deepseek-reasoner-164k": 8,
    "deepseek-r1-250120": 4,

    "deepseek-chat:function": 4,

    "deepseek-chat-8k": 5,
    "deepseek-chat-64k": 5,
    "deepseek-chat-164k": 5,

    "deepseek-v3-128k": 5,

    "deepseek-llm-67b-chat": 4,
    'deepseek-r1-think': 4,
    'deepseek-reasoner-think': 4,
    "deepseek-search": 5,
    'deepseek-r1-search': 5,
    'deepseek-reasoner-search': 5,

    "deepseek-r1-plus": 4,
    "deepclaude": 4,
    "deep-claude": 4,
    "deep-gemini": 4,
    "deep-grok": 4,

    "glm-zero": 5,
    "glm-zero-preview": 5,
    "glm-4v-flash": 5,

    "step-1-flash": 5,
    "step-1-8k": 5,
    "step-1-32k": 5,
    "step-1-256k": 5,
    "step-2-16k": 5,
    "step-2-mini": 5,
    "step-2-16k-exp": 5,
    "step-1v-8k": 5,
    "step-1v-32k": 5,
    "step-1.5v-mini": 5,
    "step-1o-vision-32k": 5,

    "meta-llama/Llama-3.2-11B-Vision-Instruct": 4,

    "mistral-small-3.1-24b-instruct": 0.1,
    "mistral-small-24b-instruct-2501": 3

}

REDIRECT_MODEL = {
    # https://docs.siliconflow.cn/docs/4-api%E8%B0%83%E7%94%A8
    "gpt-3.5-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    # "gpt-4o-mini": "THUDM/glm-4-9b-chat",  # 永久免费

    "chatfire-translator": "Qwen/Qwen2.5-7B-Instruct",  # 永久免费
    "internlm2_5-7b-chat": "internlm/internlm2_5-7b-chat",  # 永久免费

    "glm-3-turbo": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-air": "THUDM/glm-4-9b-chat",  # 永久免费
    "glm-4-flash": "THUDM/glm-4-9b-chat",  # 永久免费
    'glm-4-9b-chat': 'THUDM/glm-4-9b-chat',  # 永久免费
    'chatglm3-6b': 'THUDM/chatglm3-6b',  # 永久免费

    # "deepseek-chat": "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-chat": "deepseek-ai/DeepSeek-V2.5",
    "deepseek-vl2": "deepseek-ai/deepseek-vl2",

    "deepseek-coder": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    'deepseek-coder-v2-instruct': 'deepseek-ai/DeepSeek-Coder-V2-Instruct',
    'deepseek-v2-chat': 'deepseek-ai/DeepSeek-V2-Chat',
    "deepseek-v2.5-chat": "deepseek-ai/DeepSeek-V2.5",
    'deepseek-llm-67b-chat': 'deepseek-ai/deepseek-llm-67b-chat',

    "yi-spark": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费
    "yi-medium": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费
    "yi-large-turbo": "01-ai/Yi-1.5-9B-Chat-16K",  # 永久免费

    'yi-1.5-6b-chat': '01-ai/Yi-1.5-6B-Chat',  # 永久免费
    'yi-1.5-9b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-34b-chat-0205': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-9B-Chat-16K',  # 永久免费
    # 'yi-1.5-34b-chat-16k': '01-ai/Yi-1.5-34B-Chat-16K',

    "yi-lightning": "yi-lightning",
    "yi-large": "yi-lightning",
    "yi-large-rag": "yi-lightning",
    "yi-large-fc": "yi-lightning",
    "yi-medium-200k": "yi-lightning",

    # Vision
    "llama-3.2-11b-vision": "meta-llama/Llama-Vision-Free",

    # InternVL2
    "internvl2-8b": "Pro/OpenGVLab/InternVL2-8B",
    "internvl2-26b": "OpenGVLab/InternVL2-26B",
    "internvl2-llama3-76b": "OpenGVLab/InternVL2-Llama3-76B",

    # 千问
    "minicpm-v": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "minicpm-v2.6": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "qwen2-vl-7b-instruct": "Pro/Qwen/Qwen2-VL-7B-Instruct",
    "qwen2-vl-72b-instruct": "Qwen/Qwen2-VL-72B-Instruct",

    "qwen2.5-7b-instruct": "Qwen/Qwen2.5-7B-Instruct",
    "qwen2.5-14b-instruct": "Qwen/Qwen2.5-14B-Instruct",
    "qwen2.5-32b-instruct": "Qwen/Qwen2.5-32B-Instruct",
    "qwen2.5-72b-instruct": "Qwen/Qwen2.5-72B-Instruct",
    "qwen2.5-math-72b-instruct": "Qwen/Qwen2.5-Math-72B-Instruct",
    "qwen2.5-coder-7b-instruct": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "qwen2.5-coder-32b-instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",

    "qwen-turbo": "Qwen/Qwen2.5-7B-Instruct",  # 兜底
    'qwen2-1.5b-instruct': 'Qwen/Qwen2-1.5B-Instruct',
    'qwen2-7b-instruct': 'Qwen/Qwen2-7B-Instruct',
    'qwen2-72b-instruct': 'Qwen/Qwen2-72B-Instruct',
    'qwen2-math-72b-instruct': 'Qwen/Qwen2-Math-72B-Instruct',

    'qwen2-57b-a14b-instruct': 'Qwen/Qwen2-57B-A14B-Instruct',
    'qwen1.5-7b-chat': 'Qwen/Qwen1.5-7B-Chat',
    'qwen1.5-14b-chat': 'Qwen/Qwen1.5-14B-Chat',
    'qwen1.5-32b-chat': 'Qwen/Qwen1.5-32B-Chat',
    'qwen1.5-110b-chat': 'Qwen/Qwen1.5-110B-Chat',

    'internlm2_5-20b-chat': 'internlm/internlm2_5-20b-chat',

    # 千问兜底
    "qwen-max": 'Qwen/Qwen2.5-72B-Instruct',
    "qwen-plus": 'Qwen/Qwen2.5-72B-Instruct',

    # 国外开源
    "gemma2-9b-it": "google/gemma-2-9b-it",  # 永久免费
    "gemma2-27b-it": "google/gemma-2-27b-it",
    "gemini": "google/gemma-2-9b-it",  # todo
    "gemini-1.5": "google/gemma-2-27b-it",

    "meta-llama-3-8b-instruct": "meta-llama/Meta-Llama-3-8B-Instruct",  # 永久免费
    "mistral-7b-instruct": "mistralai/Mistral-7B-Instruct-v0.2",  # 永久免费

    "mixtral-8x7b-instruct-v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",

    "meta-llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3-70b-instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "llama-3.1-8b-instruct": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "llama-3.1-70b-instruct": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "llama-3.1-405b-instruct": "meta-llama/Meta-Llama-3.1-405B-Instruct",

    "llama-3.1-nemotron-70b-instruct": "nvidia/Llama-3.1-Nemotron-70B-Instruct",

    "meta-llama/Llama-3.3-70B-Instruct": "llama-3.3-70b-instruct",

    # https://xinghuo.xfyun.cn/sparkapi
    # spark-lite,spark-pro,spark-max,spark-ultra
    # 'spark-lite': "general",  # 实名免费
    'spark-lite': "generalv3.5",  # 实名免费
    'spark-pro': "generalv3.5",
    'spark-pro-128k': "generalv3.5",
    'spark-max': "generalv3.5",
    'spark-ultra': "generalv3.5",

    # 硅基
    "hunyuan-a52b-instruct": "Tencent/Hunyuan-A52B-Instruct",

    "stable-diffusion": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3-medium": "stabilityai/stable-diffusion-3-medium",

    "stable-diffusion-turbo": "stabilityai/sd-turbo",
    "stable-diffusion-xl-turbo": "stabilityai/sdxl-turbo",
    "dreamshaper-8-lcm": "ByteDance/SDXL-Lightning",

    "stable-diffusion-v1-5-img2img": "ByteDance/SDXL-Lightning",
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",
    "stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",
    "stable-diffusion-xl-lightning": "ByteDance/SDXL-Lightning",
    "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium",

    "photomaker": "TencentARC/PhotoMaker",

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",

    # groq
    # "llama3-8b": "llama3-8b-8192",
    # "mixtral-8x7b": "mixtral-8x7b-32768",
    # "gemma-7b": "gemma-7b-it",
    # "gemma2-9b": "gemma2-9b-it"

    "todo": "gpt-4-vision-preview",

    # https://chat.tune.app/api/models
    "claude-3-haiku-20240307": "anthropic/claude-3-haiku",
    "claude-3-5-sonnet-20240620": "anthropic/claude-3.5-sonnet",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "mistral-large": "mistral/mistral-large",
    "o1-mini": "openai/o1-mini",

    "o1-preview": "openai/o1-preview",
    # "qwen-2-vl-72b": "qwen/qwen-2-vl-72b",
    # "qwen-2.5-72b": "qwen/qwen-2.5-72b",
    "tune-blob": "kaushikaakash04/tune-blob",
    "tune-mythomax-l2-13b": "rohan/tune-mythomax-l2-13b",
    "tune-wizardlm-2-8x22b": "rohan/tune-wizardlm-2-8x22b",

    "microsoft/phi-4": 5,
    "microsoft/phi-4-reasoning": 5,
    "microsoft/phi-4-reasoning-plus": 5,

}

GROUP_RATIO = {
    "chatfire": 1,

    "default": 1,

    "特价": 0.5,  # 包含逆向等模型

    "vip3": 3,
    "vip8": 8,

    "国产": 0.5,

    "2B": 4,

    # 定制分组：不公开
    "35": 1,

    "images": 0.5

}

# https://oss.ffire.cc/images/qw.jpeg?x-oss-process=image/format,jpg/resize,w_512
if __name__ == '__main__':
    # print(','.join(RE`DD`IRECT_MODEL.keys()))

    from meutils.apis.oneapi import option, channel

    option()
    # #
    arun(channel.edit_channel(MODEL_PRICE))

    print(bjson({k: v * 6 for k, v in MODEL_RATIO.items() if k.startswith('claude')}))
    print([k for k in MODEL_RATIO if k.startswith('gpt-4.1')] | xjoin(","))
    print([k for k in MODEL_RATIO if k.startswith('qwen3')] | xjoin(","))

    print([k for k in MODEL_RATIO if k.startswith(('deepseek', 'doubao', 'moon'))] | xjoin(","))
