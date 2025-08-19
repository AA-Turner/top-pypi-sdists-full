import math
from PIL import Image
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode

INSTRUCTION = """
You are tasked with evaluating a generated image based on Visual Quality and Text Alignment and give a overall score to estimate the human preference. Please provide a rating from 0 to 10, with 0 being the worst and 10 being the best. 

**Visual Quality:**  
Evaluate the overall visual quality of the image. The following sub-dimensions should be considered:
- **Reasonableness:** The image should not contain any significant biological or logical errors, such as abnormal body structures or nonsensical environmental setups.
- **Clarity:** Evaluate the sharpness and visibility of the image. The image should be clear and easy to interpret, with no blurring or indistinct areas.
- **Detail Richness:** Consider the level of detail in textures, materials, lighting, and other visual elements (e.g., hair, clothing, shadows).
- **Aesthetic and Creativity:** Assess the artistic aspects of the image, including the color scheme, composition, atmosphere, depth of field, and the overall creative appeal. The scene should convey a sense of harmony and balance.
- **Safety:** The image should not contain harmful or inappropriate content, such as political, violent, or adult material. If such content is present, the image quality and satisfaction score should be the lowest possible. 

**Text Alignment:**  
Assess how well the image matches the textual prompt across the following sub-dimensions:
- **Subject Relevance** Evaluate how accurately the subject(s) in the image (e.g., person, animal, object) align with the textual description. The subject should match the description in terms of number, appearance, and behavior.
- **Style Relevance:** If the prompt specifies a particular artistic or stylistic style, evaluate how well the image adheres to this style.
- **Contextual Consistency**: Assess whether the background, setting, and surrounding elements in the image logically fit the scenario described in the prompt. The environment should support and enhance the subject without contradictions.
- **Attribute Fidelity**: Check if specific attributes mentioned in the prompt (e.g., colors, clothing, accessories, expressions, actions) are faithfully represented in the image. Minor deviations may be acceptable, but critical attributes should be preserved.
- **Semantic Coherence**: Evaluate whether the overall meaning and intent of the prompt are captured in the image. The generated content should not introduce elements that conflict with or distort the original description.
Textual prompt - {prompt}


""" + """
Please provide the overall ratings of this image: <|Reward|>

END
"""


def resize(height: int, width: int, factor: int, minpix:int, maxpix:int) -> tuple[int, int]:
    hbar = max(factor, round(height / factor) * factor)
    wbar = max(factor, round(width / factor) * factor)
    if hbar * wbar > maxpix:
        beta = math.sqrt((height * width) / maxpix)
        hbar = math.floor((height / beta) / factor) * factor
        wbar = math.floor((width / beta) / factor) * factor
    elif hbar * wbar < minpix:
        beta = math.sqrt(minpix / (height * width))
        hbar = math.ceil((height * beta) / factor) * factor
        wbar = math.ceil((width * beta) / factor) * factor
    return hbar, wbar


def fetch(ele: dict, factor:int = 28) -> Image.Image:
    image = ele["image"]
    w, h = image.size
    newh, neww = resize( h, w, factor=factor, minpix=ele["minpix"], maxpix=ele["maxpix"])
    image = TF.resize(image, (newh, neww), interpolation=InterpolationMode.BICUBIC)
    return image


def process(conversations: list[dict] | list[list[dict]]) -> list:
    infos = []
    for conversation in conversations:
        for message in conversation:
            if isinstance(message["content"], list):
                for ele in message["content"]:
                    if "image" in ele:
                        infos.append(fetch(ele))
    return infos