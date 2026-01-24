import json
import logging
import os
import time

import logistro


def write_to_pipe(caplog, pipe, message, human):
    termed_message = message + "\n"
    os.write(pipe, termed_message.encode("utf-8"))
    time.sleep(0.5)
    if human:
        assert message in caplog.text
    else:
        obj = json.loads(caplog.text)
        assert obj["message"] == message
    caplog.clear()


def write_to_logger(caplog, logger, level, message, human):
    logger.log(level, message)
    level_name = logging.getLevelName(level)
    if human:
        assert level_name in caplog.text
        assert message in caplog.text
    else:
        obj = json.loads(caplog.text)
        assert obj["level"] == level_name
        assert obj["message"] == message
    caplog.clear()


def test_human_logs(caplog):
    human = logistro.getLogger("human")
    for handler in logistro.getLogger().handlers:
        handler.setFormatter(logistro.human_formatter)
    human.setLevel(logistro.DEBUG2)
    write_to_logger(caplog, human, logistro.DEBUG2, "d2-message", human=True)

    w, pipelogger = logistro.getPipeLogger("pipe1")
    pipelogger.setLevel(logistro.DEBUG2)
    try:
        write_to_pipe(caplog, w, "d2-message", human=True)
    finally:
        os.close(w)


def test_structured_logs(caplog):
    structured = logistro.getLogger("structured")
    for handler in logistro.getLogger().handlers:
        handler.setFormatter(logistro.structured_formatter)
    structured.setLevel(logistro.DEBUG2)
    write_to_logger(caplog, structured, logistro.DEBUG2, "d2-message", human=False)

    w, pipelogger = logistro.getPipeLogger("pipe2")
    pipelogger.setLevel(logistro.DEBUG2)
    try:
        write_to_pipe(caplog, w, "d2-message", human=False)
    finally:
        os.close(w)
