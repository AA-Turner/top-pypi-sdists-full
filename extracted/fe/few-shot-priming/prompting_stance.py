import logging
import random
import vllm
import pandas as pd

import os
import torch


import openai
from openai import OpenAI
openai.api_key = ""


from argparse import ArgumentParser
from joblib import Memory
from sklearn.metrics import accuracy_score, f1_score
from transformers import AdamW, get_linear_schedule_with_warmup
from transformers import BertTokenizer, BertModel,  AutoTokenizer, AutoModelForCausalLM
from transformers import DebertaModel, DebertaTokenizer, GPT2Tokenizer, GPT2Model, GPT2LMHeadModel, DebertaForSequenceClassification
from transformers import OPTConfig, OPTModel, BertForSequenceClassification, AutoModelWithLMHead, LlamaTokenizer, LlamaConfig
from transformers import set_seed
from torch.nn import CrossEntropyLoss
from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.mylogging import *
from few_shot_priming.argument_sampling.topic_similarity import *
from few_shot_priming.argument_sampling.topic_similarity_sentence_transformer import *
from few_shot_priming.argument_sampling.diversify import *

from peft import PeftModel
use_cuda = torch.cuda.is_available()



def save_pre_trained_model():
    """
    Saving pretrained model to use huggingface transformers without internet
    """
    config = load_config()
    config = config["pre-trained-models"]
    path = Path(config["path"])
    bert_path = os.path.join(path,"bert-base-uncased")
    if not os.path.exists(bert_path):
        bert = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        berttokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        bert.save_pretrained(bert_path)
        berttokenizer.save_pretrained(bert_path)


    gpt_2_path = os.path.join(path, "gpt2-xl")
    if not os.path.exists(gpt_2_path):
        gpt_2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2-xl')
        gpt_2_model = GPT2Model.from_pretrained('gpt2-xl')
        gpt_2_model.save_pretrained(gpt_2_path)
        gpt_2_tokenizer.save_pretrained(gpt_2_path)

    deberta_path = os.path.join(path, "microsoft/deberta-base")
    if not os.path.exists(deberta_path):
        deberta_tokenizer = DebertaTokenizer.from_pretrained("microsoft/deberta-base")
        deberta_model = DebertaForSequenceClassification.from_pretrained("microsoft/deberta-base")
        deberta_tokenizer.save_pretrained(deberta_path)
        deberta_model.save_pretrained(deberta_path)
    alpaca_path  = os.path.join(path, "wxjiao/alpaca-7b")

    if not os.path.exists(alpaca_path) and torch.cuda.is_available():
        device = torch.device("cpu")
        alpaca_tokenizer = AutoTokenizer.from_pretrained("wxjiao/alpaca-7b")
        alpaca_model = AutoModelForCausalLM.from_pretrained("wxjiao/alpaca-7b", device_map="auto")

        alpaca_tokenizer.save_pretrained(alpaca_path)
        alpaca_model.save_pretrained(alpaca_path)
    geo_neox_path = os.path.join(path, "EleutherAI/gpt-neox-20b")
    if not os.path.exists(geo_neox_path) :

        gptneox_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
        gptneox_model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b").half().cuda()

        gptneox_tokenizer.save_pretrained(geo_neox_path)
        gptneox_model.save_pretrained(geo_neox_path)



    model, tokenizer = add_special_tokens(model, tokenizer, specials_to_add=specials_to_add)

    if 'opt' in model_name:
        tokenizer.add_bos_token=False
    return model, tokenizer, model_config, wrapper

def format_prompt(dataset, tokenizer, labels_text_map, token_limit, few_shot_size, logger, model_name=None, input=pd.DataFrame({})):
    label_str = ""
    for i, label in enumerate(labels_text_map):
        if i == 0:
            label_str = labels_text_map[label]
        elif i == len(labels_text_map) - 1:
            label_str = label_str + " or " +  labels_text_map[label]
        else:
            label_str = label_str + ", " + labels_text_map[label]
    examples = ""
    log_message(logger, f"model {model_name}")
    if len(input):

        prompt_head = f"Classify the stance of the following argument on the given topic into: {label_str}\n as illustrated by the following examples:"
        if "alpaca" in model_name:
            alpaca_head = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. \n\n### Instruction:"
            prompt = alpaca_head + prompt_head
        elif "Mistral" in model_name:
            mistral_head = "<s>[INST]"
            prompt = mistral_head + prompt_head
        else:
            prompt = prompt_head

        sentence = input["text"]
        topic = input["topic"]
        if "alpaca" in model_name:
            input = f"""\n\n### Input:\n Topic: {topic} \nArgument: {sentence} \n Response:"""
        else:
            input = f"\nOn the topic '{topic}' the argument '{sentence}' has the stance"
        prompt = prompt + input
        input_tokens = tokenizer.encode(prompt)
        input_size = len(input_tokens)
        token_limit = token_limit - input_size - 4 # 4 is added extra for the label to predicted
    if few_shot_size:
        token_limit = token_limit // (few_shot_size)

    for i, train_record in dataset.iterrows():
        sentence = train_record["text"]

        id = train_record["id"]
        topic = train_record["topic"]
        stance = train_record["stance"]
        label = labels_text_map[stance]
        ### Attempt to calculate the needed subtokens
        if "alpaca" in model_name:
            template = f"""Topic: {topic} \n Argument: {sentence} \n Response: {label}\n"""
        else:
            template = f"On the topic '{topic}' the argument '{sentence}' has the stance {label}.\n"

        tokens = tokenizer.encode(template)
        if len(tokens) > token_limit:
            sentence_tokens = tokenizer.encode(sentence)
            tokens_to_remove_from_sentence = len(tokens) + 1 - token_limit
            if tokens_to_remove_from_sentence < len(sentence_tokens):
                sentence = tokenizer.decode(sentence_tokens[:-tokens_to_remove_from_sentence], skip_special_tokens=True)
            else:
                continue
        if "alpaca" in model_name:
            template = f"""Topic: {topic} \nArgument: {sentence} \n Response: {label}\n"""
            log_message(logger, f"template {template}")
        else:
            template = f"On the topic '{topic}' the argument '{sentence}' has the stance {label}.\n"
        log_message(logger, f"{id}:{token_limit}\tOn the topic '{topic}' the argument '{sentence}' has the stance {label}\t", level=logging.INFO)
        #assert (len(tokenizer.encode(template))<= token_limit)

        examples = examples + template
    if len(input):
        return prompt_head + examples + input
    else:
        return examples

def create_model(model_name, model_input_limit, is_vllm, adapter_path=None):
    if torch.cuda.is_available() and is_vllm:
        model = vllm.LLM(model=model_name, max_model_len=model_input_limit, seed=42, trust_remote_code=True)
    else:
        if adapter_path:
            model = AutoModelForCausalLM.from_pretrained(model_name, device_map = 'auto', torch_dtype=torch.float16)
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name, device_map = 'auto')
    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)
        model = model.merge_and_unload()
    return model

def run_experiment_prompting(config, experiment, model, logger, debug, offline, validate, few_shot_size
                             ,openai, guided, is_vllm, sampling_strategy=None, similarity=None, drop_duplicate_perspectives=False, path_similar_examples=None, topic_count=None, path_predictions=None):

    model_name = config["model-name"]
    if experiment == "ibmsc" or experiment == "perspectrum":
        labels_text_map = {0: "Con", 1: "Pro" }
    else:
        labels_text_map = {0: "Con", 1: "Pro" ,  2: "Neutral" }
    if sampling_strategy:
        splits = load_splits(experiment, oversample=False, validate=validate, drop_duplicate_perspectives=drop_duplicate_perspectives, topic_count= topic_count, debug=debug)
    else:
        splits = load_splits(experiment, oversample=True, validate=validate, drop_duplicate_perspectives=drop_duplicate_perspectives, topic_count= topic_count, debug=debug)
    if topic_count:
        log_message(logger, f"loading {topic_count} topics got {len(splits['training'])}")

    if validate:
        experiment_type = "validation"
    else:
        experiment_type = "test"
    test_dataset = splits[experiment_type]

    #test_dataset = test_dataset.sample(16)
    model_input_limit = config[f"{model_name}-input-limit"]
    if not openai:
        #save_pre_trained_model()
        if offline:
            model_name = config[f"{model_name}-path"]
        else:
            model_name = config["model-name"]
        log_message(logger, f"{model_name} loaded", logging.INFO)

        tokenizer = AutoTokenizer.from_pretrained(model_name)

        if torch.cuda.is_available() and is_vllm:
            choices_regex = "(" + "|".join(labels_text_map.values()) + ")"
            sampling_params = vllm.SamplingParams(
                    temperature=0.0,
                    max_tokens=4, # max number of output tokens
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name, device_map = 'auto')
        #model_is_on_cuda = next(model.parameters()).is_cuda
        #log_message(logger,f"model is on cuda {model_is_on_cuda}", logging.INFO)
        #if use_cuda and not model_is_on_cuda:
        #    model= model.cuda()
    else:
        client = OpenAI(api_key=get_openai_key())
        tokenizer = AutoTokenizer.from_pretrained("gpt2")



    #token_limit = token_limit - template_size

    predictions = []

    labels = []
    log_message(logger, f"** few shot-size {few_shot_size}", logging.INFO)
    if sampling_strategy=="similar":
        log_message(logger, f"** smapling strategy {sampling_strategy}", logging.INFO)
        df_all_similar_examples = load_similar_examples(experiment, experiment_type,path_similar_examples=path_similar_examples, topic_count=topic_count, few_shot_size=few_shot_size)
    #i = 0

    for i, record in test_dataset.iterrows():


        if not sampling_strategy:
            if few_shot_size > len(splits["training"]):
                training_dataset = splits["training"].sample(few_shot_size, replace=True)
            else:
                training_dataset = splits["training"].sample(few_shot_size)
        elif sampling_strategy == "similar":
            training_dataset = get_similar_examples(record["id"], df_examples=df_all_similar_examples)
        else:
            training_dataset = sample_diverse_examples(experiment, experiment_type, few_shot_size, logger, topic_count, drop_duplicate_perspectives )

        training_dataset.sort_values("topic", inplace=True)

        prompt_to_predict = format_prompt(training_dataset, tokenizer, labels_text_map, model_input_limit, few_shot_size, logger, model_name=model_name, input=record)

        log_message(logger, prompt_to_predict + f" with the id {record['id']}", level=logging.INFO)
        label = record["stance"]
        labels.append(label)
        log_message(logger, f"label {label}", level=logging.INFO)
        if openai:

            completion = prompt_openai(client, "gpt-3.5-turbo-0125", prompt_to_predict)
            log_message(logger, completion, logging.INFO)

        else:
            seq = tokenizer.encode(prompt_to_predict, return_tensors="pt")
            if use_cuda:
                seq = seq.cuda()
            assert(len(seq)<model_input_limit)

            start_time = measure_time()
            if torch.cuda.is_available() and is_vllm:
                regex_output = model.generate(prompt_to_predict, sampling_params=sampling_params, use_tqdm=False)
                log_message(logger, "***OUTPUT***"+regex_output[0].outputs[0].text, level=logging.INFO)
                resulted_string_truncated = regex_output[0].outputs[0].text.lower()
            else:
                generated = model.generate(seq, max_new_tokens=4, )
                log_time(logger, start_time, f"inference {model_name} for {experiment}{few_shot_size}")
                resulted_string = tokenizer.decode(generated.tolist()[0])
                resulted_string_truncated = resulted_string[-15:].lower()
        if "pro" in resulted_string_truncated :
            predictions.append(1)
        elif "con" in resulted_string_truncated:
            predictions.append(0)
        else:
            if experiment == "vast":
                predictions.append(2)
            else:
                predictions.append(random.randint(0,1))
        #i = i + 1
    test_dataset["prediction"] = predictions
    if path_predictions:
        test_dataset.to_csv(path_predictions, sep="\t", encoding="utf-8",index=False)
    log_message(logger, f"predictions {predictions}", level=logging.WARNING)
    log_message(logger, f"labels {labels}", level=logging.WARNING)
    accuracy = accuracy_score(labels, predictions)
    metrics = {}
    if experiment == "vast":
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1, 2])
        neutral_f1 = f1s[2]
        metrics[f"{experiment_type}/neutral-f1"] = neutral_f1
    else:
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1])
    con_f1 = f1s[0]
    pro_f1 = f1s[1]

    macro_f1 = f1_score(labels, predictions, average="macro")

    metrics[f"{experiment_type}/pro-f1"] = pro_f1
    metrics[f"{experiment_type}/con-f1"] = con_f1
    if experiment == "vast":
        metrics[f"{experiment_type}/neutral-f1"] = neutral_f1

    metrics[f"{experiment_type}/macro-f1"] = macro_f1
    metrics[f"{experiment_type}/accuracy"] = accuracy

    log_metrics(logger, metrics, level=logging.WARNING)
    return metrics

def prompt_openai(client, model, prompt):
    response = client.chat.completions.create(model=model,
                                        messages=[{"role":"system", "content":prompt}],
                                        max_tokens= 1, temperature=0)
    resulted_string_truncated = response.choices[0].message.content
    return resulted_string_truncated
