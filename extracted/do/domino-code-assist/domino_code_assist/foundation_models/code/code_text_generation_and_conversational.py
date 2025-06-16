# isort: skip_file
# type: ignore
# flake8: noqa
import domino_code_assist as dca
from IPython.display import display

___df_var_name___ = "df"
___learning_rate___ = 0.0001
___epochs___ = 1
___per_device_train_batch_size___ = 4
___per_device_eval_batch_size___ = 4
___weight_decay___ = 0.1
___save_total_limit___ = 2
___max_input_length___ = 1024
___max_output_length___ = 128
# ___TEMPLATE_START___ #
import datasets
import mlflow
import numpy as np
import os
from domino_code_assist.util import handle_errors
from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorForLanguageModeling, TrainingArguments, Trainer

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

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

prompt_template = f"___prompt_prefix___:\n{{dialogue}}\n---\nText:\n{{text}}{{eos_token}}"


def template_dataset(sample):
    sample["text"] = prompt_template.format(dialogue=sample["___input_col_name___"], text=sample["___output_col_name___"], eos_token=tokenizer.eos_token)
    return sample


train_dataset = ds_dict["train"].map(template_dataset, remove_columns=list(ds_dict["train"].features))
test_dataset = ds_dict["test"].map(template_dataset, remove_columns=list(ds_dict["test"].features))

lm_train_dataset = train_dataset.map(
    lambda sample: tokenizer(sample["text"], max_length=1024, truncation=True), batched=True, batch_size=24, remove_columns=list(train_dataset.features)
)
lm_test_dataset = test_dataset.map(
    lambda sample: tokenizer(sample["text"], max_length=1024, truncation=True), batched=True, remove_columns=list(test_dataset.features)
)


def preprocess_function(examples):
    inputs = ["___task_prefix___" + doc for doc in examples["___input_col_name___"]]
    model_inputs = tokenizer(inputs, max_length=___max_input_length___, truncation=True)

    labels = tokenizer(text_target=examples["___output_col_name___"], max_length=___max_output_length___, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


# We batch to speed up processing by passing more than 1 row in at a time
tokenized_ds_dict = ds_dict.map(preprocess_function, batched=True)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

model = AutoModelForCausalLM.from_pretrained(model_name)

# please adjust training argument parameters as needed
args = TrainingArguments(
    output_dir="___output_dir___",
    evaluation_strategy="___evaluation_strategy___",  # batch or epoch
    learning_rate=learning_rate,
    per_device_train_batch_size=___per_device_train_batch_size___,
    per_device_eval_batch_size=___per_device_eval_batch_size___,
    num_train_epochs=epochs,
    weight_decay=___weight_decay___,
    save_total_limit=___save_total_limit___,
    save_strategy="___save_strategy___",
    # comment if on a non-GPU environment
    fp16=True,
    push_to_hub=False,
    report_to=["mlflow"],
    logging_steps=5,
    optim="adamw_torch",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=lm_train_dataset,
    eval_dataset=lm_test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

exp = mlflow.set_experiment(experiment_name)
with mlflow.start_run() as run:
    display(dca.automl.OpenExperiment(experiment_name))
    with handle_errors():
        print("Fine-tuning model:")
        trainer.train()
        eval_results = trainer.evaluate()
        perplexity = np.exp(eval_results["eval_loss"])
        print(f"Perplexity: {perplexity:.2f}")
    trainer.save_model("___output_dir___/model")
