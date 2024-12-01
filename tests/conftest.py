import pytest
from main import Calculator

@pytest.fixture()
def calculator():
    c = Calculator()
    return c