import json

from pydantic import Field

from creator.base.base_request import BaseRequest

default_workflow_json = {
    "3": {
        "inputs": {
            "seed": 985289875893903,
            "steps": 20,
            "cfg": 7.5,
            "sampler_name": "dpmpp_2m_sde",
            "scheduler": "karras",
            "denoise": 1,
            "model": [
                "4",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "latent_image": [
                "5",
                0
            ]
        },
        "class_type": "KSampler",
        "_meta": {
            "title": "KSampler"
        }
    },
    "4": {
        "inputs": {
            "ckpt_name": "Juggernaut-XI-Prototype.safetensors",
            "key_opt": "",
            "mode": "Auto"
        },
        "class_type": "CheckpointLoaderSimpleShared //Inspire",
        "_meta": {
            "title": "Shared Checkpoint Loader (Inspire)"
        }
    },
    "5": {
        "inputs": {
            "width": 1024,
            "height": 768,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
            "title": "Empty Latent Image"
        }
    },
    "6": {
        "inputs": {
            "text": "a photograph of a smiling green alien holding a sign which says \"Run Diffusion\", ultra realistic, street, city, sci-fi, ultra realistic, cute, friendly",
            "clip": [
                "4",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "7": {
        "inputs": {
            "text": "blurry, low quality",
            "clip": [
                "4",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "8": {
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        },
        "class_type": "VAEDecode",
        "_meta": {
            "title": "VAE Decode"
        }
    },
    "9": {
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    }
}

default_workflow_json_2 = {
    "21": {
        "inputs": {
            "width": 1920,
            "height": 1080,
            "batch_size": 2
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
            "title": "Empty Latent Image"
        }
    },
    "67": {
        "inputs": {
            "samples": [
                "132",
                0
            ],
            "vae": [
                "135",
                2
            ]
        },
        "class_type": "VAEDecode",
        "_meta": {
            "title": "VAE Decode"
        }
    },
    "99": {
        "inputs": {
            "seed": 1011799137402762
        },
        "class_type": "CR Seed",
        "_meta": {
            "title": "🌱 CR Seed"
        }
    },
    "100": {
        "inputs": {
            "text": [
                "114:0",
                0
            ],
            "seed": [
                "99",
                0
            ],
            "log_prompt": "No"
        },
        "class_type": "PromptExpansion",
        "_meta": {
            "title": "Prompt Expansion"
        }
    },
    "101": {
        "inputs": {
            "text": [
                "144",
                0
            ]
        },
        "class_type": "ShowText|pysssss",
        "_meta": {
            "title": "Show Text 🐍"
        }
    },
    "102": {
        "inputs": {
            "text": [
                "145",
                0
            ]
        },
        "class_type": "ShowText|pysssss",
        "_meta": {
            "title": "Show Text 🐍"
        }
    },
    "120": {
        "inputs": {
            "b1": 1.01,
            "b2": 1.02,
            "s1": 0.99,
            "s2": 0.9500000000000001,
            "model": [
                "135",
                0
            ]
        },
        "class_type": "FreeU_V2",
        "_meta": {
            "title": "FreeU_V2"
        }
    },
    "132": {
        "inputs": {
            "add_noise": False,
            "noise_seed": [
                "99",
                0
            ],
            "steps": 15,
            "cfg": 4,
            "sampler_name": "euler_ancestral",
            "scheduler": "karras",
            "start_at_step": 0,
            "end_at_step": 10000,
            "noise_mode": "CPU",
            "return_with_leftover_noise": False,
            "batch_seed_mode": "incremental",
            "variation_seed": 0,
            "variation_strength": 0,
            "model": [
                "134",
                0
            ],
            "positive": [
                "138:1",
                0
            ],
            "negative": [
                "138:0",
                0
            ],
            "latent_image": [
                "21",
                0
            ]
        },
        "class_type": "KSamplerAdvanced //Inspire",
        "_meta": {
            "title": "KSamplerAdvanced (inspire)"
        }
    },
    "134": {
        "inputs": {
            "ds_depth_1": 3,
            "ds_depth_2": 3,
            "ds_timestep_1": 900,
            "ds_timestep_2": 650,
            "resize_scale_1": 2,
            "resize_scale_2": 2,
            "model": [
                "120",
                0
            ]
        },
        "class_type": "Hires",
        "_meta": {
            "title": "Apply Kohya's HiresFix"
        }
    },
    "135": {
        "inputs": {
            "ckpt_name": "Juggernaut-XI-Prototype.safetensors",
            "key_opt": "",
            "mode": "Auto"
        },
        "class_type": "CheckpointLoaderSimpleShared //Inspire",
        "_meta": {
            "title": "Shared Checkpoint Loader (Inspire)"
        }
    },
    "139": {
        "inputs": {
            "prompt": "three squirrels in business suits having a meeting at a tiny table in a park"
        },
        "class_type": "CR Prompt Text",
        "_meta": {
            "title": "⚙️ CR Prompt Text"
        }
    },
    "140": {
        "inputs": {
            "prompt": "blurry, bad eyes, bad hands, deformed, low quality"
        },
        "class_type": "CR Prompt Text",
        "_meta": {
            "title": "⚙️ CR Prompt Text"
        }
    },
    "144": {
        "inputs": {
            "action": "replace",
            "tidy_tags": "yes",
            "text_a": [
                "100",
                0
            ],
            "text_b": "",
            "text_c": "",
            "result": "three squirrels in business suits having a meeting at a tiny table in a park, professional photograph, bokeh, 8k detailed, 35mm, vintage, highly detailed, found footage, cinematic still, emotional, harmonious, vignette, 4k detailed, sharp focus, high budget, epic, gorgeous, film grain, three squirrels in business suits having a meeting at a tiny table in a park, professional photograph, bokeh, 8k detailed, 35mm, vintage, highly detailed, found footage, cinematic still, emotional, harmonious, vignette, 4k detailed, sharp focus, high budget, epic, gorgeous, film grain, atmosphere, bright, rich vivid colors"
        },
        "class_type": "StringFunction|pysssss",
        "_meta": {
            "title": "String Function 🐍"
        }
    },
    "145": {
        "inputs": {
            "action": "replace",
            "tidy_tags": "yes",
            "text_a": [
                "114:1",
                0
            ],
            "text_b": "",
            "text_c": "",
            "result": "blurry, bad eyes, bad hands, deformed, low quality, blurry, cropped, bad face, saturated, contrast, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, anime, cartoon, graphic, (blur, blurry, bokeh), text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured, deformed, bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers, drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly, anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch"
        },
        "class_type": "StringFunction|pysssss",
        "_meta": {
            "title": "String Function 🐍"
        }
    },
    "148": {
        "inputs": {
            "filename_prefix": [
                "139",
                0
            ],
            "images": [
                "67",
                0
            ]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    },
    "119:0": {
        "inputs": {
            "text_positive": "",
            "text_negative": "",
            "style": "Fooocus Photograph",
            "log_prompt": True,
            "style_positive": True,
            "style_negative": True
        },
        "class_type": "SDXLPromptStyler",
        "_meta": {
            "title": "SDXL Prompt Styler"
        }
    },
    "119:1": {
        "inputs": {
            "text_positive": "",
            "text_negative": "",
            "style": "Fooocus Sharp",
            "log_prompt": True,
            "style_positive": True,
            "style_negative": True
        },
        "class_type": "SDXLPromptStyler",
        "_meta": {
            "title": "SDXL Prompt Styler"
        }
    },
    "119:2": {
        "inputs": {
            "text_positive": "",
            "text_negative": "",
            "style": "Fooocus Negative",
            "log_prompt": True,
            "style_positive": True,
            "style_negative": True
        },
        "class_type": "SDXLPromptStyler",
        "_meta": {
            "title": "SDXL Prompt Styler"
        }
    },
    "133:1": {
        "inputs": {
            "text1": [
                "140",
                0
            ],
            "text2": [
                "119:0",
                1
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "133:2": {
        "inputs": {
            "text1": [
                "119:1",
                0
            ],
            "text2": [
                "119:2",
                0
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "133:3": {
        "inputs": {
            "text1": [
                "119:1",
                1
            ],
            "text2": [
                "119:2",
                1
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "133:0": {
        "inputs": {
            "text1": [
                "139",
                0
            ],
            "text2": [
                "119:0",
                0
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "114:1": {
        "inputs": {
            "text1": [
                "133:1",
                0
            ],
            "text2": [
                "133:3",
                0
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "114:0": {
        "inputs": {
            "text1": [
                "133:0",
                0
            ],
            "text2": [
                "133:2",
                0
            ],
            "separator": ", "
        },
        "class_type": "CR Text Concatenate",
        "_meta": {
            "title": "🔤 CR Text Concatenate"
        }
    },
    "138:0": {
        "inputs": {
            "text": [
                "102",
                0
            ],
            "clip": [
                "135",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "138:1": {
        "inputs": {
            "text": [
                "101",
                0
            ],
            "clip": [
                "135",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    }
}

model_load_json = {
    "1": {
        "inputs": {
            "ckpt_name": "Juggernaut-XI-Prototype.safetensors",
            "key_opt": "",
            "mode": "Auto"
        },
        "class_type": "CheckpointLoaderSimpleShared //Inspire",
        "_meta": {
            "title": "Shared Checkpoint Loader (Inspire)"
        }
    },
    "3": {
        "inputs": {
            "text": "",
            "clip": [
                "1",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "4": {
        "inputs": {
            "root_dir": "output",
            "file": "file.txt",
            "append": "append",
            "insert": True,
            "text": [
                "10",
                2
            ]
        },
        "class_type": "SaveText|pysssss",
        "_meta": {
            "title": "Save Text"
        }
    },
    "10": {
        "inputs": {
            "latent_suffix": "6934042_cache",
            "image_suffix": "8568828_cache",
            "conditioning_suffix": "91602225_cache",
            "output_path": "/opt/rd/apps/ComfyUI/custom_nodes/was-node-suite-comfyui/cache",
            "conditioning": [
                "3",
                0
            ]
        },
        "class_type": "Cache Node",
        "_meta": {
            "title": "Cache Node"
        }
    }
}


class CmfyWorkflow(BaseRequest):
    workflow_json: str = Field(default="", examples=[json.dumps(default_workflow_json)])


class CmfyWorkflowFcus(BaseRequest):
    workflow_json: str = Field(default="", examples=[json.dumps(default_workflow_json_2)])