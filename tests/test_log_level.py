import logging
import os
from importlib import reload
from unittest.mock import patch

import pytest

from parma_mining.producthunt.api import main


@pytest.mark.parametrize(
    "env_setting, expected_log_level",
    [
        ("prod", logging.INFO),
        ("staging", logging.DEBUG),
        ("local", logging.DEBUG),
        ("other", logging.INFO),
        ("", logging.INFO),
    ],
)
@patch("logging.basicConfig")
def test_logging_level(mock_basic_config, env_setting, expected_log_level):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": env_setting}):
        reload(main)
        mock_basic_config.assert_called_with(level=expected_log_level)
