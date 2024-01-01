import logging

import pytest

from parma_mining.producthunt import __version__

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("arg", [True, False])
def test_dummy(arg: bool):
    logger.debug("Testing parma_mining.producthunt")
    assert arg or not arg
    assert len(__version__) > 0
