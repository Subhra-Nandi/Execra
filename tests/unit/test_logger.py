import os
import json
import logging
import pytest
from core.logger import setup, get_logger, JSONFormatter

def test_get_logger():
    logger = get_logger("test.execra")
    assert logger.name == "test.execra"

def test_json_formatter():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test JSON formatting",
        args=(),
        exc_info=None
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)
    
    assert data["level"] == "INFO"
    assert data["name"] == "test_logger"
    assert data["message"] == "Test JSON formatting"
    assert "timestamp" in data
    assert "exception" not in data

def test_json_formatter_with_exception():
    formatter = JSONFormatter()
    try:
        raise ValueError("Something went wrong")
    except ValueError:
        import sys
        exc_info = sys.exc_info()
        
    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test.py",
        lineno=15,
        msg="An error occurred",
        args=(),
        exc_info=exc_info
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)
    
    assert data["level"] == "ERROR"
    assert "exception" in data
    assert "ValueError: Something went wrong" in data["exception"]

def test_setup_stream_handler():
    setup(log_level="DEBUG", json_format=True)
    root = logging.getLogger()
    assert root.level == logging.DEBUG
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0].formatter, JSONFormatter)

def test_setup_file_handler(tmp_path):
    log_file = tmp_path / "execra_test.log"
    setup(log_level="WARNING", log_file=str(log_file))
    
    root = logging.getLogger()
    assert root.level == logging.WARNING
    assert len(root.handlers) == 2  # Stream + File
    
    logger = get_logger("test.file")
    logger.warning("Write to file warning")
    
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Write to file warning" in content
        assert "WARNING" in content
