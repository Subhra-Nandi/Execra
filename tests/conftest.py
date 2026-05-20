import numpy as np
import pytest
from core.config import Settings

@pytest.fixture
def mock_settings():
    """
    Returns a fresh Settings instance for testing.
    """
    return Settings(
        LLM_BACKEND="test-model",
        OPENAI_API_KEY="test-openai-key",
        GEMINI_API_KEY="test-gemini-key",
        API_PORT=9999
    )

@pytest.fixture
def api_base_url():
    """
    Returns the base URL for the API in tests.
    """
    return "http://localhost:8000"

@pytest.fixture
def sample_frame() -> np.ndarray:
    """Return a small dummy screen frame for tests."""
    return np.zeros((10, 10, 3), dtype=np.uint8)

@pytest.fixture(autouse=True, scope="module")
def cleanup_module_patches():
    """Automatically stops all active mocks after each module finishes execution."""
    yield
    from unittest.mock import patch
    patch.stopall()
