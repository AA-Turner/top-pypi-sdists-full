import openprompt

from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.mylogging import *

from openprompt.prompts import ManualTemplate, ManualVerbalizer
from openprompt import PromptForClassification, PromptDataLoader
from openprompt.data_utils import InputExample
from openprompt import plms
from openprompt.plms import *


plms._MODEL_CLASSES["wxjiao/alpaca-7b"]= ModelClass(**{"config": LlamaConfig, "tokenizer": LlamaTokenizer, "model": AutoModelForCausalLM,
                                                       "wrapper": LMTokenizerWrapper})
plms._MODEL_CLASSES["EleutherAI/gpt-j-6B"]= ModelClass(**{"config": GPTJConfig, "tokenizer": GPT2Tokenizer, "model": GPTJForCausalLM,
                                                          "wrapper": LMTokenizerWrapper})

def create_few_shot_model(config, experiment, offline=True):
    """
    Prepare an openprompt model based on the configuration
    :param config: a dictionary specifing the name and type of the model
    :return: an openprompt modle, a wrapper class, a tokenizer, and a template
    """
    model_name = config["model-name"]

    if offline:
        model_type = Path(config["model-path"])
    else:
        model_type = config["model-type"]
    if experiment == "vast":
        classes = [0, 1, 2]
        label_words = {0: ["Con"], 1: ["Pro"], 2 : ["Neutral"]}
    else:
        classes = [0, 1]
        label_words = {0: ["Con"], 1: ["Pro"]}
    plm, tokenizer, model_config, WrapperClass = my_load_plm(model_name, model_type)

    promptTemplate = ManualTemplate(
        text = 'On the topic {"placeholder":"text_b"} the argument {"placeholder":"text_a"} has the stance {"mask"}.',
        tokenizer = tokenizer,
    )
    promptVerbalizer = ManualVerbalizer(
        classes = classes,
        label_words = label_words,
        tokenizer = tokenizer,
    )

    promptModel = PromptForClassification(template = promptTemplate, plm=plm, verbalizer=promptVerbalizer, freeze_plm=False)
    if use_cuda:
        promptModel = promptModel.cuda()
    return promptModel, WrapperClass, tokenizer, promptTemplate

def my_load_plm(model_name, model_path, specials_to_add = None):
    model_class = get_model_class(plm_type = model_name)
    model_config = model_class.config.from_pretrained(model_path)
    # you can change huggingface model_config here
    # if 't5'  in model_name: # remove dropout according to PPT~\ref{}
    #     model_config.dropout_rate = 0.0
    if 'gpt' in model_name: # add pad token for gpt
        specials_to_add = ["<pad>"]
        # model_config.attn_pdrop = 0.0
        # model_config.resid_pdrop = 0.0
        # model_config.embd_pdrop = 0.0
    #model = model_class.model.from_pretrained(model_path, config=model_config, device_map = 'auto').half()
    model = model_class.model.from_pretrained(model_path, config=model_config, device_map = 'auto', load_in_8bit=True, torch_dtype=torch.float16, )
    tokenizer = model_class.tokenizer.from_pretrained(model_path)
    wrapper = model_class.wrapper


def run_experiment_prompt_fine_tuning(config=None, experiment="ibmsc", params=None, offline=False, validate=True,
                                      splits=None, logger = None, debug=False, save=False, sampling_strategy=None, similarity=None):
    """
    Run a validation experiment or a test experiment
    :param validate: a boolean flag specifying whether to run a validation or  test experiment
    :return:
    """
    #if offline:
    #    save_pre_trained_model()




    log_memory_usage(logger, "begining")
    batch_size = params["batch-size"]
    lr = params["learning-rate"]
    epochs_num = params["epochs"]
    if not splits:
        splits = load_splits(experiment, oversample=False, validate=validate, debug=debug)
        #splits["validation"] = splits["validation"].sample(16) # REEEEEEMEBEr
        prompt_dataset = convert_to_prompt_splits(splits, config)
    else:
        prompt_dataset = convert_to_prompt_splits(splits, config, sample=False)

    log_memory_usage(logger, "loaded-split")
    promptModel, WrapperClass, tokenizer, promptTemplate = create_few_shot_model(config, experiment=experiment, offline=offline)
    log_memory_usage(logger, "created model and tokenizer")
    train_data_loader = PromptDataLoader(dataset = prompt_dataset["training"], tokenizer=tokenizer, template=promptTemplate,
                                         tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
    log_memory_usage(logger, "created training data loadert")
    if validate:
        experiment_type = "validate"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["validation"], tokenizer = tokenizer, template = promptTemplate,
                                            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
        log_memory_usage(logger, "created validation data loadert")
    else:
        experiment_type = "test"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["test"], tokenizer = tokenizer, template = promptTemplate,
                                            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
        log_memory_usage(logger, "created test data loadert")

    loss_func = CrossEntropyLoss()
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in promptModel.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in promptModel.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.01}
    ]
    path_model_fine_tuned = config["model-path-fine-tuned"]

    optimizer = AdamW(optimizer_grouped_parameters, lr=float(lr))
    #optimizer = SGD(promptModel.parameters(), lr=float(lr))

    log_memory_usage(logger, "created optimizer")
    metrics = {}
    best_accuracy =  0
    best_f1 = 0
    best_epoch = 0
    best_metrics = None
    for epoch in range(epochs_num):
        tot_loss = 0
        for step, inputs in enumerate(train_data_loader):
            if use_cuda:
                inputs = inputs.cuda()
            promptModel.train()

            logits = promptModel(inputs)
            log_memory_usage(logger, "inference on inputs")
            labels = inputs["label"]
            loss = loss_func(logits, labels)
            log_memory_usage(logger, "loss = loss_func(logits, labels)")
            loss.backward()
            log_memory_usage(logger, "loss.backward()")
            tot_loss += loss.item()
            optimizer.step()
            optimizer.zero_grad()
            if step % 100 == 1:
                log_message(logger, "Epoch {}, average loss: {}".format(epoch, tot_loss/(step+1)), level=logging.INFO)
            metrics["train/loss"] = tot_loss/(step+1)
            wandb.log(metrics)
        promptModel.eval()
        test_loss = 0
        all_test_labels = []
        all_test_preds = []
        for step, test_inputs in enumerate(test_data_loader):
            if use_cuda:
                test_inputs = test_inputs.cuda()
            test_logits = promptModel(test_inputs)
            test_labels = test_inputs["label"]
            all_test_labels.extend(test_labels.cpu().tolist())
            all_test_preds.extend(torch.argmax(test_logits, dim = -1).cpu().tolist())
            loss = loss_func(test_logits, test_labels)
            test_loss += loss.item()
            metrics[f"{experiment_type}/loss"] = test_loss/(step+1)
            wandb.log(metrics)
        accuracy = accuracy_score(all_test_labels, all_test_preds)
        metrics[f"{experiment_type}/accuracy"] = accuracy
        if experiment == "vast":
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1, 2])
            neutral_f1 = f1s[2]
            metrics[f"{experiment_type}/neutral-f1"] = neutral_f1
        else:
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1])

        con_f1 = f1s[0]
        pro_f1 = f1s[1]

        macro_f1 = f1_score(all_test_labels, all_test_preds, average="macro")
        metrics[f"{experiment_type}/pro-f1"] = pro_f1
        metrics[f"{experiment_type}/con-f1"] = con_f1

        metrics[f"{experiment_type}/macro-f1"] = macro_f1
        if macro_f1 > best_f1:
            best_metrics = metrics
            best_f1 = macro_f1
            best_epoch = epoch
            torch.save({"model_state_dict":promptModel.state_dict()}, path_model_fine_tuned)
        metrics[f"{experiment_type}/epoch"] = best_epoch
    log_message(logger, f"best epoch is {best_epoch}", level=logging.WARNING)
    log_metrics(logger, best_metrics, level=logging.WARNING)
    metrics["score"] = best_metrics[f"{experiment_type}/accuracy"]
    wandb.log(metrics)
    return metrics["score"]

def convert_to_prompt_splits(dataset, config, sample=True):
    """
    Conver the pandas dataframes to splits as specified by the openprompt api
    :param dataset: a dictionary containing the trianing, validation, and test dataframes
    :return: a dictionary containing lists of input examples as specified by the openprompt api
    """
    prompt_splits = {}
    prompt_splits["test"] = []
    prompt_splits["training"] = []
    prompt_splits["validation"] = []
    for key in dataset.keys():
        if key == "training" and sample:
            dataset["training"] = dataset["training"].sample(config["few-shot-size"])
        for i,record in dataset[key].iterrows():
            prompt_splits[key].append(InputExample(guid= i , text_a = record["text"], text_b = record["topic"], label = record["stance"]))

    return prompt_splits
