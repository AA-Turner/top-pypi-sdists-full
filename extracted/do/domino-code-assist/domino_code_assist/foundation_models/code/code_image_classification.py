# isort: skip_file
# type: ignore
# flake8: noqa
import domino_code_assist as dca
from IPython.display import display
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor
from typing import Dict, List

___df_var_name___ = "df"
___learning_rate___ = 0.0001
___per_device_train_batch_size___ = 16
___per_device_eval_batch_size___ = 16
___epochs___ = 3
___gradient_accumulation_steps___ = 4
___warmup_ratio___ = (0.1,)


# ___TEMPLATE_START___ #
import datasets
import evaluate
import mlflow.transformers
import numpy as np
import os
from domino_code_assist.util import handle_errors
from evaluate import EvaluationModule
from transformers import AutoImageProcessor, AutoModelForImageClassification, DefaultDataCollator, Trainer, TrainingArguments
from PIL.Image import Image as PIL_Image
from torchvision.transforms import Compose, Normalize, RandomResizedCrop, ToTensor
from typing import Dict, List

os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"
os.environ["HF_MLFLOW_LOG_ARTIFACTS"] = "1"

# If using non Hugging models as well consider using autolog instead
# mlflow.transformers.autolog(log_input_examples=True, log_model_signatures=True, log_models=True, log_datasets=False, silent=True)

experiment_name = "___experiment_name___"
MODEL_NAME = "___model_name___"
IMAGE_COL = "___input_col_name___"
LABEL_COL = "___output_col_name___"
logging_steps = 5

ds_dict = datasets.DatasetDict({"train": dca.img_df_to_ds(___df_var_name___, LABEL_COL)})
ds_dict = datasets.load_dataset("___hf_dataset_name___", "___hf_dataset_config___")
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

if "train" not in ds_dict:
    raise Exception(
        'No split named "train" exists in the dataset. Please reconfigure the dataset to include a split named "train" or choose a different dataset.'
    )

if "test" not in ds_dict:
    ds_dict = ds_dict["train"].train_test_split(test_size=0.2, stratify_by_column=LABEL_COL)

assert isinstance(ds_dict["train"][0][IMAGE_COL], PIL_Image), "Data must have PIL images loaded to train"

# Crop a random part of the image, resize it, and normalize it with the image mean and standard deviation
normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
size = image_processor.size["shortest_edge"] if "shortest_edge" in image_processor.size else (image_processor.size["height"], image_processor.size["width"])
transformations = Compose([RandomResizedCrop(size), ToTensor(), normalize])


def transforms(examples: Dict[str, List]):
    """Apply the transformations and return the pixel_values"""
    examples["pixel_values"] = [transformations(img.convert("RGB")) for img in examples[IMAGE_COL]]
    del examples[IMAGE_COL]
    return examples


ds_dict = ds_dict.with_transform(transforms)


EVAL_METRIC = "___metric_for_best_model___"
metric = evaluate.load(EVAL_METRIC)


def compute_metrics(eval_pred: EvaluationModule):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)


# Mappings to/from labels and ids
labels = ds_dict["train"].features[LABEL_COL].names
id2label = dict(enumerate(labels))
label2id = {v: k for k, v in id2label.items()}

data_collator = DefaultDataCollator()

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True,
)

mlflow_run_name = "run1"

training_args = TrainingArguments(
    output_dir="___output_dir___",
    remove_unused_columns=False,
    evaluation_strategy="___evaluation_strategy___",
    save_strategy="___save_strategy___",
    learning_rate=___learning_rate___,
    per_device_train_batch_size=___per_device_train_batch_size___,
    gradient_accumulation_steps=___gradient_accumulation_steps___,
    per_device_eval_batch_size=___per_device_eval_batch_size___,
    num_train_epochs=___epochs___,
    warmup_ratio=___warmup_ratio___,
    logging_steps=logging_steps,
    load_best_model_at_end=True,
    metric_for_best_model=EVAL_METRIC,
    push_to_hub=False,
    report_to=["mlflow"],
    optim="adamw_torch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=ds_dict["train"],
    eval_dataset=ds_dict["validation"] if "validation" in ds_dict else ds_dict["test"],
    tokenizer=image_processor,
    compute_metrics=compute_metrics,
)

exp = mlflow.set_experiment(experiment_name)
with mlflow.start_run() as run:
    display(dca.automl.OpenExperiment(experiment_name))
    with handle_errors():
        print("Fine-tuning model:")
        trainer.train()
        if "validation" in ds_dict:  # If validation split was used in training, then use the test split for prediction
            print("Using fine-tuned model to predict values in test split:")
            if ds_dict["test"].unique(LABEL_COL) == [-1]:  # check if test split is unlabeled
                ds_dict["test"] = ds_dict["test"].remove_columns(LABEL_COL)
                predictions, _, _ = trainer.predict(ds_dict["test"])
                y_pred = np.argmax(predictions, axis=1)
                print("The test split of the dataset has no labels. Here are the predictions, but the accuracy cannot be verified:")
                print(y_pred)
            else:
                accuracy_test = trainer.predict(ds_dict["test"]).metrics["test_accuracy"]
                print("Accuracy of predictions for test dataset: {:.2f}".format(accuracy_test))
    trainer.save_model("___output_dir___/model")
