# ディシジョンテーブルを使った割引ロジックのテスト

## 概要
本ドキュメントでは、会員種別 (gold / silver / normal)、クーポンの有無 (True / False)、購入金額 (purchase_amount) などの複数条件と結果（割引率）を扱う `discount_logic.py` を題材に、ディシジョンテーブルを使ったテスト方法を解説します。

## テスト対象のコード
```python
def get_discount_rate(member_type: str, purchase_amount: int, has_coupon: bool) -> int:
    """
    複数の条件で割引率が決まるロジックの例:
      - member_type: 'gold', 'silver', 'normal'
      - purchase_amount: 購入金額 (int)
      - has_coupon: True / False (クーポン所持)
    """
    if member_type == 'gold':
        if has_coupon:
            if purchase_amount >= 5000:
                return 20  # 20%OFF
            else:
                return 15  # 15%OFF
        else:
            return 10     # 10%OFF
    elif member_type == 'silver':
        if has_coupon:
            return 10     # 10%OFF
        else:
            return 5      # 5%OFF
    else:
        # normal
        if purchase_amount >= 5000:
            return 5      # 5%OFF
        else:
            return 0      # 割引なし
```

## テストの考え方
ディシジョンテーブル (Decision Table) とは、複数の条件とそれによって変化する結果を表形式で整理し、漏れなくテストケースを洗い出すための手法です。

## テストケースの設計
以下の表に基づいてテストケースを設計します。

| 会員種別 | クーポン | 購入金額 >= 5000 | 割引率 (期待) |
|----------|---------|------------------|---------------|
| gold     | True    | Yes              | 20%OFF        |
| gold     | True    | No               | 15%OFF        |
| gold     | False   | -                | 10%OFF        |
| silver   | True    | -                | 10%OFF        |
| silver   | False   | -                | 5%OFF         |
| normal   | -       | Yes              | 5%OFF         |
| normal   | -       | No               | 0%OFF         |

## テストコードの実装
```python
import pytest
from discount_logic import get_discount_rate

@pytest.mark.parametrize(
    "member_type, has_coupon, purchase_amount, expected_rate",
    [
        ("gold", True, 5000, 20),
        ("gold", True, 4999, 15),
        ("gold", False, 4000, 10),
        ("silver", True, 3000, 10),
        ("silver", False, 3000, 5),
        ("normal", False, 5000, 5),
        ("normal", False, 4999, 0),
    ]
)
def test_get_discount_rate(member_type, has_coupon, purchase_amount, expected_rate):
    result = get_discount_rate(member_type, purchase_amount, has_coupon)
    assert result == expected_rate
```

## テストの実行方法
1. `discount_logic.py` をプロジェクト直下に配置
2. `tests/test_discount_logic.py` にテストコードを作成
3. 以下のコマンドでテストを実行
```bash
cd my_discount_project
pytest
```

## まとめ
- ディシジョンテーブルは複数条件が絡むロジックを表形式で網羅的にテストする強力な手法です
- Pytestのパラメーター化を活用することで効率的にテストケースを実装できます
- 条件が増えた場合もテーブルとテストコードを拡張することでメンテナンス可能です
