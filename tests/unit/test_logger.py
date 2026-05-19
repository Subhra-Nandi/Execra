import logging
import pytest
from core.logger import setup, get_logger

@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before and after each test."""
    root = logging.getLogger()
    handlers = root.handlers[:]
    for handler in handlers:
        root.removeHandler(handler)
    yield
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    for handler in handlers:
        root.addHandler(handler)

def test_setup_creates_handler():
    """Test that setup() attaches a StreamHandler to the root logger."""
    root = logging.getLogger()
    assert len(root.handlers) == 0
    
    setup("INFO")
    
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0], logging.StreamHandler)

def test_setup_sets_correct_level():
    """Test that setup() sets the correct log level."""
    setup("DEBUG")
    root = logging.getLogger()
    assert root.level == logging.DEBUG

def test_setup_avoids_duplicate_handlers():
    """Test that calling setup() multiple times does not duplicate handlers."""
    setup("INFO")
    setup("INFO")
    setup("INFO")
    
    root = logging.getLogger()
    assert len(root.handlers) == 1

def test_setup_configures_uvicorn_loggers():
    """Test that setup() also configures uvicorn loggers to match the level."""
    setup("WARNING")
    
    assert logging.getLogger("uvicorn.access").level == logging.WARNING
    assert logging.getLogger("uvicorn.error").level == logging.WARNING

def test_get_logger_returns_named_logger():
    """Test that get_logger() returns a logger with the correct name."""
    logger = get_logger("my_test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "my_test_module"
