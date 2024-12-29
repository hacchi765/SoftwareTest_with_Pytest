# tests/test_calculator.py
import pytest
from src.white_black_box.calculator import add, subtract, divide

def test_add():
    # 同値分割の例: 正数、負数、0
    assert add(2, 3) == 6
    assert add(-1, -2) == -3
    assert add(0, 10) == 10

def test_subtract():
    # 境界値分析: 0をまたぐケースなど
    assert subtract(0, 0) == 0
    assert subtract(5, 10) == -5
    assert subtract(10, 5) == 5

def test_divide():
    # 正常系
    assert divide(10, 2) == 5.0
    # 異常系: 0割
    with pytest.raises(ValueError):
        divide(10, 0)
