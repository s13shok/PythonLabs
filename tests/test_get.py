import pytest
from main import Calculator

def test_plus(calculator):
    assert(calculator.plus(5, 7) == 5+7)

def test_plus_exception(calculator):
    with pytest.raises(Exception):
        calculator('','')