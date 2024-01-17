from parma_mining.mining_common.exceptions import BaseError
from parma_mining.mining_common.helper import collect_errors
from parma_mining.producthunt.model import ErrorInfoModel


class MockError(BaseError):
    """Mock error class."""

    def __init__(self, message):
        self.message = message


def test_collect_errors():
    company_id = "test_company"
    error_message = "Test error occurred"
    mock_error = MockError(message=error_message)
    errors: dict[str, ErrorInfoModel] = {}

    collect_errors(company_id, errors, mock_error)

    assert company_id in errors
    assert isinstance(errors[company_id], ErrorInfoModel)
    assert errors[company_id].error_type == "MockError"
    assert errors[company_id].error_description == error_message
