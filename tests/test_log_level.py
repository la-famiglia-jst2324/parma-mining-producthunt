import logging
import os
from importlib import reload
from unittest.mock import patch


@patch("logging.basicConfig")
def test_logging_level_prod(mock_basic_config):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": "prod"}):
        import parma_mining.producthunt.api.main

        reload(parma_mining.producthunt.api.main)
        mock_basic_config.assert_called_with(level=logging.INFO)


@patch("logging.basicConfig")
def test_logging_level_staging(mock_basic_config):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": "staging"}):
        import parma_mining.producthunt.api.main

        reload(parma_mining.producthunt.api.main)
        mock_basic_config.assert_called_with(level=logging.DEBUG)


@patch("logging.basicConfig")
def test_logging_level_local(mock_basic_config):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": "local"}):
        import parma_mining.producthunt.api.main

        reload(parma_mining.producthunt.api.main)
        mock_basic_config.assert_called_with(level=logging.DEBUG)


@patch("logging.basicConfig")
def test_logging_level_other(mock_basic_config):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": "other"}):
        import parma_mining.producthunt.api.main

        reload(parma_mining.producthunt.api.main)
        mock_basic_config.assert_called_with(level=logging.INFO)


@patch("logging.basicConfig")
def test_logging_level_empty(mock_basic_config):
    with patch.dict(os.environ, {"DEPLOYMENT_ENV": ""}):
        import parma_mining.producthunt.api.main

        reload(parma_mining.producthunt.api.main)
        mock_basic_config.assert_called_with(level=logging.INFO)
