import logging
from datetime import datetime, date
import os
import torch
import time



def setup_logging(logger_name, path, level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    print(f"current working directory is {os.getcwd()}")
    print(f"path of log file {path}")
    fh = logging.FileHandler(path)
    fh.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    now=datetime.now()
    logger.info(now.strftime("%Y-%m-%d-%H:%M")+"\n")
    return logger

def log_message(logger, message, level=logging.WARNING):
    #logger = logging.getLogger(logger_name)
    now=datetime.now()
    if level == logging.INFO:
        logger.info(now.strftime("%H:%M")+"\t" + message)
    else:
        logger.warning(now.strftime("%H:%M")+"\t" + message)

def format_metrics(metrics):
    formatted_str = ""
    for metric in metrics:
        formatted_str = formatted_str + f"{metric}: {metrics[metric]:2.2f}\t"
    return formatted_str

def format_params (params):
    formatted_str = ""
    for param_key in params:
        formatted_str = formatted_str + f"{param_key}: {params[param_key]}\t"
    return formatted_str

def log_metrics(logger, metrics, level = logging.WARNING):

    message = format_metrics(metrics)
    log_message(logger, message, level)

def log_params(logger, params, level = logging.WARNING):

    params_message = format_params (params)
    log_message(logger, params_message, level= logging.WARNING)

def log_memory_usage(logger, state):
    total_free_gpu_memory, total_gpu_memory = torch.cuda.mem_get_info()
    log_message(logger, state, level=logging.INFO)
    log_message(logger, f"Total free GPU memory: {round(total_free_gpu_memory * 1e-9, 3)} GB", level=logging.INFO)
    log_message(logger,f"Total GPU memory: {round(total_gpu_memory * 1e-9, 3)} GB", level=logging.INFO)

def measure_time():
    return time.time()

def log_time(logger, start_time, message):
    elapsed_time = time.time() - start_time
    log_message(logger, f"meesage took {elapsed_time}")