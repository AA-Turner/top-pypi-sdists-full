"""Test the logging module."""

import logging

from pyorbital.logger import get_logger, logging_off, logging_on


def test_logging_on_and_off(caplog):
    """Test that switching logging on and off works."""
    logger = get_logger("pyorbital.spam")
    logging_on()
    with caplog.at_level(logging.WARNING):
        logger.debug("I'd like to leave the army please, sir.")
        logger.warning("Stop that! It's SPAM.")
    assert "Stop that! It's SPAM" in caplog.text
    assert "I'd like to leave the army please, sir." not in caplog.text
    logging_off()
    with caplog.at_level(logging.DEBUG):
        logger.warning("You've got a nice army base here, Colonel.")
    assert "You've got a nice army base here, Colonel." not in caplog.text
