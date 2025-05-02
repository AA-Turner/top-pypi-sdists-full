from dataclasses import dataclass, field
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from creator.base.base_request import BaseRequest


@dataclass
class FcusAdvancedParams:
    adm_scaler_positive: float = 1.5
    adm_scaler_negative: float = 0.8
    adm_scaler_end: float = 0.3
    refiner_swap_method: str = "joint"
    adaptive_cfg: int = 7
    sampler_name: str = "dpmpp_2m_sde_gpu"
    scheduler_name: str = "karras"
    overwrite_step: int = -1
    overwrite_switch: int = -1
    overwrite_width: int = -1
    overwrite_height: int = -1
    overwrite_vary_strength: int = -1
    overwrite_upscale_strength: int = -1
    mixing_image_prompt_and_vary_upscale: bool = False
    mixing_image_prompt_and_inpaint: bool = False
    debugging_cn_preprocessor: bool = False
    skipping_cn_preprocessor: bool = False
    controlnet_softness: float = 0.25
    canny_low_threshold: int = 64
    canny_high_threshold: int = 128
    inpaint_engine: str = "v1"
    freeu_enabled: bool = False
    freeu_b1: float = 1.01
    freeu_b2: float = 1.02
    freeu_s1: float = 0.99
    freeu_s2: float = 0.95


@dataclass
class Lora:
    model_name: str = ""
    weight: float = 1.0


class FcusTxt2Img(BaseRequest):
    prompt: str = ""
    negative_prompt: str = ""
    style_selections: List[str] = Field(default_factory=list, examples=[["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"]])
    performance_selection: str = "Speed"
    aspect_ratios_selection: str = "1152*896"
    image_number: int = 2
    image_seed: int = -1
    sharpness: float = 0.0
    guidance_scale: float = 7.5
    base_model_name: str = "Juggernaut-XI-Prototype.safetensors"
    refiner_model_name: str = "None"
    refiner_switch: float = 0.1
    loras: List[Lora] = Field(default_factory=list, examples=[[Lora()]])
    advanced_params: Optional[FcusAdvancedParams] = Field(default=None, examples=[FcusAdvancedParams()])
    require_base64: bool = True
    async_process: bool = True


class FcusUpscaleOrVary(BaseRequest):
    input_image: str = ""
    uov_method: str = ""
    prompt: str = ""
    negative_prompt: str = ""
    style_selections: List[str] = Field(default_factory=list,
                                        examples=[["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"]])
    performance_selection: str = ""
    aspect_ratios_selection: str = ""
    image_number: int = 1
    image_seed: int = -1
    sharpness: float = 0.0
    guidance_scale: float = 7.5
    base_model_name: str = "RunDiffusion-XL-Photo.safetensors"
    refiner_model_name: str = "None"
    refiner_switch: float = 0.1
    loras: List[Lora] = Field(default_factory=list, examples=[[Lora()]])
    advanced_params: Optional[FcusAdvancedParams] = Field(default=None, examples=[FcusAdvancedParams()])
    require_base64: bool = False
    async_process: bool = True


class FcusInpaintOrOutpaint(BaseRequest):
    request_params: str = ""
    input_image: str = ""
    input_mask: str = ""
    outpaint_selections: List[str] = Field(default_factory=list, examples=[])
    prompt: str = ""
    negative_prompt: str = ""
    style_selections: List[str] = Field(default_factory=list,
                                        examples=[["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"]])
    performance_selection: str = ""
    aspect_ratios_selection: str = ""
    image_number: int = 1
    image_seed: int = -1
    sharpness: float = 0.0
    guidance_scale: float = 7.5
    base_model_name: str = "RunDiffusion-XL-Photo.safetensors"
    refiner_model_name: str = "None"
    refiner_switch: float = 0.1
    loras: List[Lora] = Field(default_factory=list, examples=[[Lora()]])
    advanced_params: Optional[FcusAdvancedParams] = Field(default=None, examples=[FcusAdvancedParams()])
    require_base64: bool = False
    async_process: bool = True
