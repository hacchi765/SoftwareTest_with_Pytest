# tests/test_discount_logic.py
import pytest
from src.decision_table.discount_logic import get_discount_rate

# ディシジョンテーブルを定義して、その通りにテスト
@pytest.mark.parametrize(
    "member_type, has_coupon, purchase_amount, expected_rate",
    [
        # gold & coupon & >=5000 -> 20%
        ("gold", True,  5000, 20),
        ("gold", True,  9999, 20),
        # gold & coupon & <5000 -> 15%
        ("gold", True,  4999, 15),
        # gold & no coupon -> 10%
        ("gold", False, 5000, 10),
        # silver & coupon -> 10%
        ("silver", True, 3000, 10),
        # silver & no coupon -> 5%
        ("silver", False, 3000, 5),
        # normal & >=5000 -> 5%
        ("normal", True, 5000, 5),
        # normal & <5000 -> 0%
        ("normal", False, 4999, 0),
    ],
)
def test_discount_rate(member_type, has_coupon, purchase_amount, expected_rate):
    result = get_discount_rate(member_type, purchase_amount, has_coupon)
    assert result == expected_rate
