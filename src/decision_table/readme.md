# 割引ロジック (discount_logic.py) の複数条件テスト入門ガイド

以下では、会員種別 (gold / silver / normal)、クーポンの有無 (True / False)、購入金額 (purchase_amount) などの複数条件と結果（割引率）を扱う `discount_logic.py` を題材に、ディシジョンテーブルを使ったテスト方法を初学者向けにわかりやすくまとめます。

---

## 1. ディレクトリ構成例
my_discount_project/  
    ├── discount_logic.py   
    └── tests/  
        └── test_discount_logic.py  

- **`discount_logic.py`**  
  割引ロジックを実装するスクリプトです。  

- **`tests/test_discount_logic.py`**  
  Pytestで実行するテストコードを置くファイル。ディシジョンテーブルの考え方を活かしてテストを書きます。

---

## 2. discount_logic.py

複数条件で割引率を決定するロジックを、以下のように定義します。

###
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

# ディシジョンテーブル (Decision Table) の概要とテストコード作成ガイド

ディシジョンテーブル (Decision Table) とは、**複数の条件 (会員種別 / クーポンの有無 / 購入金額など) と、それによって変化する結果 (割引率) を表形式で整理し、漏れなくテストケースを洗い出す**ための手法です。

## 3.1 条件と結果の表 (例)

| 会員種別 | クーポン | 購入金額 >= 5000 | 割引率 (期待) |
|----------|---------|------------------|---------------|
| gold     | True    | Yes              | 20%OFF        |
| gold     | True    | No               | 15%OFF        |
| gold     | False   | -                | 10%OFF        |
| silver   | True    | -                | 10%OFF        |
| silver   | False   | -                | 5%OFF         |
| normal   | -       | Yes              | 5%OFF         |
| normal   | -       | No               | 0%OFF         |

上表のとおり、**会員種別 × クーポン × 金額 >= 5000** の組み合わせをすべて洗い出し、期待する割引率が何パーセントかを可視化します。

---

## 4. 初学者が実際にテストコードを書くステップ

1. **ロジックの仕様確認**  
   - 「ゴールド会員でクーポンあり＋購入5000円以上 → 20%OFF」など、表で定義された期待結果を把握します。

2. **ディシジョンテーブル (上の表) を参照**  
   - 必要な組み合わせをすべて網羅しているかを確認。  
   - 同じロジックでも、追加条件 (例: 会員期限切れ など) があれば列を増やします。

3. **テストコード (test_discount_logic.py) を作成**  
   - Pytest の `@pytest.mark.parametrize` を使えば、テーブルをそのままコード化しやすいです。

4. **テスト実行**  
   - `pytest` コマンドを用いてテストし、期待どおりの割引率が返るかを確かめます。

5. **失敗した場合の原因を解析し、修正**  
   - ロジックに誤りがあるのか？ それともディシジョンテーブルに漏れがあるのか？  
   - テストケースを再度検証しながら反映します。

---

## 5. テストコード例: `test_discount_logic.py`

ディシジョンテーブルを元にパラメータ化テストするサンプルです。

###
```python
import pytest
from discount_logic import get_discount_rate

@pytest.mark.parametrize(
    "member_type, has_coupon, purchase_amount, expected_rate",
    [
        # gold + coupon + >=5000 -> 20
        ("gold", True,  5000, 20),
        ("gold", True,  9999, 20),

        # gold + coupon + <5000 -> 15
        ("gold", True,  4999, 15),

        # gold + no coupon -> 10
        ("gold", False, 4000, 10),

        # silver + coupon -> 10
        ("silver", True, 3000, 10),

        # silver + no coupon -> 5
        ("silver", False, 3000, 5),

        # normal + >=5000 -> 5
        ("normal", False, 5000, 5),

        # normal + <5000 -> 0
        ("normal", False, 4999, 0),
    ],
)

def test_get_discount_rate(member_type, has_coupon, purchase_amount, expected_rate):
    result = get_discount_rate(member_type, purchase_amount, has_coupon)
    assert result == expected_rate
``` 

## 5.1 ポイント
- **全パターンを網羅**: gold / silver / normal、クーポンの有無、5000円以上/未満など  
- **テスト読みやすさ**: パラメータは `(member_type, has_coupon, purchase_amount, expected_rate)` のタプルにまとめ、**1行1パターン** で明快に  
- **期待結果** (`expected_rate`) が正しいか `assert` で確認

## 6. テスト実行

### 6.1 ファイル配置
- `discount_logic.py` をプロジェクト直下に配置  
- `tests/test_discount_logic.py` に上記のテストコードを貼り付け

### 6.2 Pytest 実行

``` python
cd my_discount_project pytest
```

## 6.3 結果の確認
- すべての組み合わせが `PASSED` になれば、ディシジョンテーブル通りにロジックが動いていることを確認  
- もし失敗があれば、どの条件が間違っているかを特定し、**ロジック or テストケース** の修正を検討

## 7. まとめ
- **ディシジョンテーブル** は、複数条件が絡むロジックを表形式で網羅的にテストする強力な手法です。  
- **初心者はまずテーブルを作成し、Pytest のパラメータ化でテーブルをそのままコードに落とし込むのがわかりやすい**  
- 今後は条件が増えたら列を追加し、テストコードにもパラメータを追加していく流れでメンテナンス可能  
