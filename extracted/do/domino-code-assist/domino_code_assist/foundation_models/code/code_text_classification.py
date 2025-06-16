# isort: skip_file
# type: ignore
import domino_code_assist as dca
from IPython.display import display

___epochs___ = 1
___df_var_name___ = "df"
___learning_rate___ = 0.0001
___per_device_train_batch_size___ = 32
___per_device_eval_batch_size___ = 32
___weight_decay___ = 0.1
___save_total_limit___ = 2
# ___TEMPLATE_START___ #
import datasets
import mlflow
import numpy as np
import os
from domino_code_assist.util import handle_errors
from sklearn.metrics import accuracy_score
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments

os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"
os.environ["HF_MLFLOW_LOG_ARTIFACTS"] = "1"

# If using non Hugging models as well consider using autolog instead
# mlflow.transformers.autolog(log_input_examples=True, log_model_signatures=True, log_models=True, log_datasets=False, silent=True)

label_col = "___output_col_name___"
text_col = "___input_col_name___"

ds_dict = datasets.DatasetDict({"train": dca.df_to_ds(___df_var_name___, text_col, label_col)})
ds_dict = datasets.load_dataset("___hf_dataset_name___", "___hf_dataset_config___")

if "train" not in ds_dict:
    raise Exception(
        'No split named "train" exists in the dataset. Please reconfigure the dataset to include a split named "train" or choose a different dataset.'
    )

if "test" not in ds_dict:
    ds_dict = ds_dict["train"].train_test_split(test_size=0.2, stratify_by_column=label_col)

df_labels = ds_dict["train"].to_pandas()[label_col].unique().tolist()

model_name = "___model_name___"

learning_rate = ___learning_rate___
logging_steps = 5
epochs = ___epochs___
experiment_name = "___experiment_name___"

for split in ["train", "test", "validation"]:
    if split in ds_dict:
        print("Samples in {:<10s}      : {:d}".format(split, ds_dict[split].shape[0]))


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"accuracy": accuracy_score(predictions, labels)}


model = BertForSequenceClassification.from_pretrained(model_name, num_labels=len(df_labels))

tokenizer = BertTokenizer.from_pretrained(model_name)


def prep_dataset(ds, label_col, text_col):
    def to_int(e):
        e[label_col] = [df_labels.index(x) for x in e[label_col]]
        return e

    if "int" not in ds.features[label_col].dtype:
        ds = ds.map(to_int, batched=True)

    ds = ds.map(lambda e: tokenizer(e[text_col], truncation=True, padding="max_length", max_length=315), batched=True)
    ds.set_format(type="torch", columns=["input_ids", "token_type_ids", "attention_mask", label_col])
    return ds


for split in ["train", "test", "validation"]:
    if split in ds_dict:
        ds_dict[split] = prep_dataset(ds_dict[split], label_col, text_col)

args = TrainingArguments(
    output_dir="___output_dir___",
    evaluation_strategy="___evaluation_strategy___",
    learning_rate=learning_rate,
    per_device_train_batch_size=___per_device_train_batch_size___,
    per_device_eval_batch_size=___per_device_eval_batch_size___,
    num_train_epochs=epochs,
    logging_steps=logging_steps,
    weight_decay=___weight_decay___,
    metric_for_best_model="___metric_for_best_model___",
    save_total_limit=___save_total_limit___,
    save_strategy="___save_strategy___",
    load_best_model_at_end=False,
    report_to=["mlflow"],
    optim="adamw_torch",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=ds_dict["train"],
    eval_dataset=ds_dict["validation"] if "validation" in ds_dict else ds_dict["test"],
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
            if ds_dict["test"].unique(label_col) == [-1]:  # check if test split is unlabeled
                ds_dict["test"] = ds_dict["test"].remove_columns(label_col)
                predictions, _, _ = trainer.predict(ds_dict["test"])
                y_pred = np.argmax(predictions, axis=1)
                print("The test split of the dataset has no labels. Here are the predictions, but the accuracy cannot be verified:")
                print(y_pred)
            else:
                accuracy_test = trainer.predict(ds_dict["test"]).metrics["test_accuracy"]
                print("Accuracy of predictions for test dataset: {:.2f}".format(accuracy_test))
    trainer.save_model("___output_dir___/model")
