# isort: skip_file
# type: ignore
# flake8: noqa
import domino_code_assist as dca
from IPython.display import display

___df_var_name___ = "df"
___learning_rate___ = 0.0001
___epochs___ = 1
___per_device_train_batch_size___ = 32
___per_device_eval_batch_size___ = 32
___weight_decay___ = 0.1
___save_total_limit___ = 2
___max_input_length___ = 1024
___max_output_length___ = 128
# ___TEMPLATE_START___ #
import datasets
import evaluate
import numpy as np
import mlflow
import os
from domino_code_assist.util import handle_errors
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments

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


model_name = "___model_name___"
learning_rate = ___learning_rate___
epochs = ___epochs___
experiment_name = "___experiment_name___"
eval_metric = "___metric_for_best_model___"
logging_steps = 5

tokenizer = AutoTokenizer.from_pretrained(model_name)


def preprocess_function(examples):
    inputs = ["summarize: " + doc for doc in examples["___input_col_name___"]]
    model_inputs = tokenizer(inputs, max_length=___max_input_length___, truncation=True)

    labels = tokenizer(text_target=examples["___output_col_name___"], max_length=___max_output_length___, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


# We batch to speed up processing by passing more than 1 row in at a time
tokenized_ds_dict = ds_dict.map(preprocess_function, batched=True)

data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model_name)
metric = evaluate.load(eval_metric)


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    if eval_metric == "rouge":
        result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)
    else:
        result = metric.compute(predictions=decoded_preds, references=decoded_labels)

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens)

    if eval_metric == "rouge":
        return {k: round(v, 4) for k, v in result.items()}
    else:
        return {k: v for k, v in result.items()}


model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

args = Seq2SeqTrainingArguments(
    output_dir="___output_dir___",
    evaluation_strategy="___evaluation_strategy___",  # batch or epoch
    learning_rate=learning_rate,
    per_device_train_batch_size=___per_device_train_batch_size___,
    per_device_eval_batch_size=___per_device_eval_batch_size___,
    num_train_epochs=epochs,
    logging_steps=logging_steps,
    weight_decay=___weight_decay___,
    save_total_limit=___save_total_limit___,
    save_strategy="___save_strategy___",
    predict_with_generate=True,
    # comment if on a non-GPU environment
    fp16=True,
    push_to_hub=False,
    report_to=["mlflow"],
    optim="adamw_torch",
)

trainer = Seq2SeqTrainer(
    model=model,
    args=args,
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
