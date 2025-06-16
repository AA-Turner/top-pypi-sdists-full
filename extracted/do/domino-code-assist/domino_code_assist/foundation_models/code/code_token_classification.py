# isort: skip_file
# type: ignore
import domino_code_assist as dca
from IPython.display import display

___df_var_name___ = "df"
___learning_rate___ = 0.0001
___epochs___ = 1
___per_device_train_batch_size___ = 32
___per_device_eval_batch_size___ = 32
___weight_decay___ = 0.1
___save_total_limit___ = 2
# ___TEMPLATE_START___ #
import datasets
import evaluate
import mlflow
import numpy as np
import os
from domino_code_assist.util import handle_errors
from transformers import AutoModelForTokenClassification, AutoTokenizer, DataCollatorForTokenClassification, Trainer, TrainingArguments

os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"
os.environ["HF_MLFLOW_LOG_ARTIFACTS"] = "1"

# If using non Hugging models as well consider using autolog instead
# mlflow.transformers.autolog(log_input_examples=True, log_model_signatures=True, log_models=True, log_datasets=False, silent=True)

ds_dict = datasets.DatasetDict({"train": dca.df_to_ds_ner(___df_var_name___, "___output_col_name___")})
ds_dict = datasets.load_dataset("___hf_dataset_name___", "___hf_dataset_config___")

if "train" not in ds_dict:
    raise Exception(
        'No split named "train" exists in the dataset. Please reconfigure the dataset to include a split named "train" or choose a different dataset.'
    )

if "test" not in ds_dict:
    ds_dict = ds_dict["train"].train_test_split(test_size=0.2)

label_list = ds_dict["train"].features["___output_col_name___"].feature.names

model_name = "___model_name___"
learning_rate = ___learning_rate___
logging_steps = 5
epochs = ___epochs___
experiment_name = "___experiment_name___"

tokenizer = AutoTokenizer.from_pretrained(model_name)
example = ds_dict["train"][0]
tokenized_input = tokenizer(example["___input_col_name___"], is_split_into_words=True)
tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"])


def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["___input_col_name___"], truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples["___output_col_name___"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


tokenized_ds_dict = ds_dict.map(tokenize_and_align_labels, batched=True)

data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

seqeval = evaluate.load("seqeval")


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [[label_list[p] for (p, lbl) in zip(prediction, label) if lbl != -100] for prediction, label in zip(predictions, labels)]
    true_labels = [[label_list[lbl] for (p, lbl) in zip(prediction, label) if lbl != -100] for prediction, label in zip(predictions, labels)]

    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


model = AutoModelForTokenClassification.from_pretrained(
    model_name, num_labels=len(label_list), id2label={i: v for i, v in enumerate(label_list)}, label2id={v: i for i, v in enumerate(label_list)}
)

training_args = TrainingArguments(
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
    load_best_model_at_end=True,
    report_to=["mlflow"],
    optim="adamw_torch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds_dict["train"],
    eval_dataset=tokenized_ds_dict["validation"] if "validation" in tokenized_ds_dict else tokenized_ds_dict["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

exp = mlflow.set_experiment(experiment_name)
with mlflow.start_run() as run:
    display(dca.automl.OpenExperiment(experiment_name))
    with handle_errors():
        print("Fine-tuning model:")
        trainer.train()
        if "validation" in tokenized_ds_dict:  # If validation split was used in training, then use the test split for prediction
            print("Using fine-tuned model to predict values in test split:")
            accuracy_test = trainer.predict(tokenized_ds_dict["test"]).metrics["test_accuracy"]
            print("Accuracy of predictions for test dataset: {:.2f}".format(accuracy_test))
    trainer.save_model("___output_dir___/model")
