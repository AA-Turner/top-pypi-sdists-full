# isort: skip_file
# type: ignore
# flake8: noqa
# fmt: off
import domino_code_assist as dca
from IPython.display import display
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor
from typing import Dict, List

___df_var_name___ = "df"
___per_device_train_batch_size___ = 8
___epochs___ = 10
___learning_rate___ = 1e-5
___weight_decay___ = 1e-4
___save_steps___ = 200
___fp16___ = True
___save_total_limit___ = 2


# ___TEMPLATE_START___ #
from typing import Any, Dict, List

import albumentations
import datasets
import mlflow.transformers
import numpy as np
from domino_code_assist.util import handle_errors
from matplotlib.pyplot import imshow
import os
from PIL import ImageDraw
from tqdm.auto import tqdm
from transformers import (
    AutoImageProcessor,
    AutoModelForObjectDetection,
    Trainer,
    TrainingArguments,
)

os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"
os.environ["HF_MLFLOW_LOG_ARTIFACTS"] = "1"

# If using non Hugging models as well consider using autolog instead
# mlflow.transformers.autolog(log_input_examples=True, log_model_signatures=True, log_models=True, log_datasets=False, silent=True)

experiment_name = "___experiment_name___"
MODEL_NAME = "___model_name___"
IMAGE_COL = "___input_col_name___"
OBJECTS_COL = "___output_col_name___"
LABEL_COL = "___label_key___"
# Bounding box coordinates, COCO format
BBOX_COL = "bbox"
logging_steps = 5

# Load the dataset and the model's image processor
ds_dict = datasets.DatasetDict({"train": dca.img_df_to_ds(___df_var_name___, LABEL_COL)})
ds_dict = datasets.load_dataset("___hf_dataset_name___", "___hf_dataset_config___")
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

if "train" not in ds_dict:
    raise Exception(
        'No split named "train" exists in the dataset. Please reconfigure the dataset to include a split named "train" or choose a different dataset.'
    )

if "test" not in ds_dict:
    ds_dict = ds_dict["train"].train_test_split(test_size=0.2, stratify_by_column=LABEL_COL)

# Draw and image and its annotations. Visual validation
image = ds_dict["train"][0][IMAGE_COL]
annotations = ds_dict["train"][0][OBJECTS_COL]
draw = ImageDraw.Draw(image)

categories = ds_dict["train"].features[OBJECTS_COL].feature[LABEL_COL].names

id2label = {index: x for index, x in enumerate(categories, start=0)}
label2id = {v: k for k, v in id2label.items()}

# Draw the boxes over the image
for box, class_idx in zip(annotations[BBOX_COL], annotations[LABEL_COL]):
    # COCO Format: xmin, ymin, width, height
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), outline="red", width=1)
    draw.text((x, y), id2label[class_idx], fill="white")


imshow(image)


# We need to apply augmentations to our images in order to train.
# We need to augment the images and format the annotations. See this guide for more details on your model and dataset:
# https://huggingface.co/docs/datasets/object_detection

transform_width = 480
transform_height = 480
transform = albumentations.Compose(
    [
        albumentations.Resize(transform_width, transform_height),
        albumentations.HorizontalFlip(p=1.0),
        albumentations.RandomBrightnessContrast(p=1.0),
    ],
    bbox_params=albumentations.BboxParams(format="coco", label_fields=[LABEL_COL]),
)


# Structure annotations to format: {'image_id': int, 'annotations': List[Dict]}
def formatted_anns(image_id: int, category: Dict, area: List[float], bbox: List[float]) -> List[Dict]:
    annotations = []
    for i in range(len(category)):
        new_ann = {
            "image_id": image_id,
            "category_id": category[i],
            "isCrowd": 0,
            "area": area[i],
            "bbox": bbox[i],
        }
        annotations.append(new_ann)

    return annotations

# transforming a batch
def transform_aug_ann(examples: Dict[str, List]):
    image_ids = examples["image_id"]
    images, bboxes, area, categories = [], [], [], []
    for image, objects in zip(examples[IMAGE_COL], examples[OBJECTS_COL]):
        image = np.array(image.convert("RGB"))[:, :, ::-1]
        out = transform(image=image, bboxes=objects[BBOX_COL], category=objects[LABEL_COL])

        area.append(objects["area"])
        images.append(out[IMAGE_COL])
        bboxes.append(out["bboxes"])
        categories.append(out[LABEL_COL])

    targets = [
        {"image_id": id_, "annotations": formatted_anns(id_, cat_, ar_, box_)}
        for id_, cat_, ar_, box_ in zip(image_ids, categories, area, bboxes)
    ]

    return image_processor(images=images, annotations=targets, return_tensors="pt")


# Use with_transform so these transformations happen on-the-fly rather than all at once
ds_dict["train"] = ds_dict["train"].with_transform(transform_aug_ann)

for split in ds_dict.keys():
    remove_idx = set()
    for i in tqdm(range(len(ds_dict[split]))):
        try:
            ds_dict["train"][i]
        except ValueError:
            remove_idx.add(i)

    keep = [i for i in range(len(ds_dict[split])) if i not in remove_idx]
    print(f"{len(remove_idx)} Samples removed from {split}")
    ds_dict[split] = ds_dict[split].select(keep)


# Create a collate function to batch images together.
# Pad images (which are now pixel_values) to the largest image in a batch,
# and create a corresponding pixel_mask to indicate which pixels are real (1) and which are padding (0).

def collate_fn(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a collate function to batch images together.

    Pad images (which are now pixel_values) to the largest image in a batch,
    and create a corresponding pixel_mask to indicate which pixels are real
    (1) and which are padding (0).
    """
    pixel_values = [item["pixel_values"] for item in batch]
    encoding = image_processor.pad_and_create_pixel_mask(pixel_values, return_tensors="pt")
    labels = [item["labels"] for item in batch]
    result = {}
    result["pixel_values"] = encoding["pixel_values"]
    result["pixel_mask"] = encoding["pixel_mask"]
    result["labels"] = labels
    return result

# Training


model = AutoModelForObjectDetection.from_pretrained(
    MODEL_NAME,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True,
)

training_args = TrainingArguments(
    output_dir="___output_dir___",
    per_device_train_batch_size=___per_device_train_batch_size___,
    num_train_epochs=___epochs___,
    fp16=___fp16___,
    save_steps=___save_steps___,
    logging_steps=logging_steps,
    learning_rate=___learning_rate___,
    weight_decay=___weight_decay___,
    save_total_limit=___save_total_limit___,
    remove_unused_columns=False,
    push_to_hub=False,
    report_to=["mlflow"],
    optim="adamw_torch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=collate_fn,
    train_dataset=ds_dict["train"],
    tokenizer=image_processor,
    eval_dataset=ds_dict["test"],
)

exp = mlflow.set_experiment(experiment_name)
with mlflow.start_run() as run:
    display(dca.automl.OpenExperiment(experiment_name))
    with handle_errors():
        print("Fine-tuning model:")
        trainer.train()
    trainer.save_model("___output_dir___/model")
