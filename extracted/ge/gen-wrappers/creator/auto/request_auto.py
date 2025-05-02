from typing import List, Dict, Any

from pydantic import Field

from creator.base.base_request import BaseRequest


class AutoTxt2Img(BaseRequest):
    prompt: str = Field("", examples=["A beautiful sunset over a mountain lake."])
    negative_prompt: str = ""
    styles: List[str] = Field(default_factory=list, examples=[[]])
    seed: int = -1
    subseed: int = -1
    subseed_strength: float = 0
    seed_resize_from_h: int = -1
    seed_resize_from_w: int = -1
    sampler_name: str = "DPM++ 2M"
    scheduler: str = ""
    batch_size: int = 1
    n_iter: int = 1
    steps: int = 30
    cfg_scale: float = 7.5
    width: int = 1024
    height: int = 768
    restore_faces: bool = False
    tiling: bool = False
    do_not_save_samples: bool = True
    do_not_save_grid: bool = True
    eta: float = 0
    denoising_strength: float = 0
    s_min_uncond: float = 0
    s_churn: float = 0
    s_tmax: float = 0
    s_tmin: float = 0
    s_noise: float = 0
    override_settings: Dict[str, Any] = Field(default_factory=dict, examples=[{}])
    override_settings_restore_afterwards: bool = True
    refiner_checkpoint: str = ""
    refiner_switch_at: float = 0
    disable_extra_networks: bool = False
    firstpass_image: str = ""
    comments: Dict[str, Any] = {}
    enable_hr: bool = False
    firstphase_width: int = 0
    firstphase_height: int = 0
    hr_scale: int = 2
    hr_upscaler: str = ""
    hr_second_pass_steps: int = 0
    hr_resize_x: int = 0
    hr_resize_y: int = 0
    hr_checkpoint_name: str = ""
    hr_sampler_name: str = ""
    hr_scheduler: str = ""
    hr_prompt: str = ""
    hr_negative_prompt: str = ""
    force_task_id: str = ""
    script_name: str = ""
    script_args: List[str] = []
    alwayson_scripts: Dict[str, Any] = {}
    infotext: str = ""
    checkpoint: str = "Juggernaut-XI-Prototype.safetensors"
    vae: str = ""
    callback_url: str = ""
    user_name: str = ""
    password: str = ""


class AutoImg2Img(BaseRequest):
    prompt: str = Field("", examples=["A beautiful sunset over a mountain lake."])
    negative_prompt: str = ""
    styles: List[str] = Field(default_factory=list, examples=[[]])
    seed: int = -1
    subseed: int = -1
    subseed_strength: float = 0.0
    seed_resize_from_h: int = -1
    seed_resize_from_w: int = -1
    sampler_name: str = "DPM++ 2M"
    scheduler: str = ""
    batch_size: int = 1
    n_iter: int = 1
    steps: int = 30
    cfg_scale: float = 7.5
    width: int = 1024
    height: int = 768
    restore_faces: bool = False
    tiling: bool = False
    do_not_save_samples: bool = True
    do_not_save_grid: bool = True
    eta: float = 0.0
    denoising_strength: float = 0.75
    s_min_uncond: float = 0.0
    s_churn: float = 0.0
    s_tmax: float = 0.0
    s_tmin: float = 0.0
    s_noise: float = 0.0
    override_settings: Dict[str, Any] = Field(default_factory=dict, examples=[{}])
    override_settings_restore_afterwards: bool = True
    refiner_checkpoint: str = ""
    refiner_switch_at: float = 0
    disable_extra_networks: bool = False
    firstpass_image: str = ""
    comments: Dict[str, Any] = Field(default_factory=dict, examples=[{}])
    init_images: List[str] = Field(default_factory=list, examples=[[]])
    resize_mode: int = 0
    image_cfg_scale: float = 0.0
    mask: str = ""
    mask_blur_x: int = 4
    mask_blur_y: int = 4
    mask_blur: int = 0
    mask_round: bool = True
    inpainting_fill: int = 0
    inpaint_full_res: bool = True
    inpaint_full_res_padding: int = 0
    inpainting_mask_invert: int = 0
    initial_noise_multiplier: float = 0.0
    latent_mask: str = ""
    force_task_id: str = ""
    include_init_images: bool = False
    script_name: str = ""
    script_args: List[Any] = Field(default_factory=list, examples=[[]])
    alwayson_scripts: Dict[str, Any] = Field(default_factory=dict, examples=[{}])
    infotext: str = ""
    checkpoint: str = "Juggernaut-XI-Prototype.safetensors"
    vae: str = ""
    callback_url: str = ""
    user_name: str = ""
    password: str = ""
