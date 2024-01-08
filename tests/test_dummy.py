import logging

import pytest
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200
from parma_mining.producthunt import __version__
from parma_mining.producthunt.api.dependencies.auth import authenticate
from parma_mining.producthunt.api.dependencies.mock_auth import mock_authenticate
from parma_mining.producthunt.api.main import app


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.mark.parametrize("arg", [True, False])
def test_dummy(arg: bool):
    assert arg or not arg
    assert len(__version__) > 0


def test_root(client):
    response = client.get("/")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-producthunt"}


def test_dummy_auth(client):
    response = client.get("/dummy-auth")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-producthunt"}
