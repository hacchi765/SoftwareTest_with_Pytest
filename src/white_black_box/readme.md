# ホワイトボックス/ブラックボックステスト

初学者が「calculator.py」を題材にホワイトボックス/ブラックボックステストを学ぶための整理です。  
途中で、テストコードを書くステップを簡単に説明しているので、実践しながら流れを掴んでみてください。

---

## 1. なぜ `calculator.py` で学ぶのか？

- **四則演算（足し算、引き算、掛け算、割り算）** を中心にシンプルな機能が多い  
- **0割エラー** や **負数・小数** など、テスト対象としてわかりやすいテーマが豊富  
- **「実装が単純」だがテストポイントは多い** → 初学者がテスト設計の基本を理解しやすい

---

## 2. ホワイトボックステストとブラックボックステストの違い

- **ブラックボックステスト**  
  - コード内部の実装・構造を意識せず、**入力と出力** だけを基にテストする  
  - 同値分割や境界値分析など、**仕様やユーザーの期待** を中心にテストケースを作る  
- **ホワイトボックステスト**  
  - コードの内部ロジック（`if` 文や例外処理）を把握し、**すべての分岐をテストで通す**  
  - C0/C1/C2 などのカバレッジを意識して漏れを防ぐ

---

## 3. `calculator.py` のサンプル

下記のように基本的な四則演算を用意します。割り算は 0 割エラーを起こす可能性があるため、明示的に例外を投げます。

``` python
# calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

---

## 4. 実際にテストコードを書くステップ（初学者向け）

src/tests/test_calculator.pyにテストコードを書いていきましょう！  
その際は以下の点を意識してみましょう！  

1. **仕様/要件の整理**  
   - 「引数は整数？ 小数？ 負数は許可？ 文字列は？」  
   - 「0 で割ったときはエラーを出すか？」  
   - このあたりを明確にしてからテストケースを決めると混乱しにくい

2. **黒箱（ブラックボックス）テストケースを考える**  
   - 入力値の種類（正数・負数・0・小数 など）を分ける  
   - 期待する出力を明確に書き出す

3. **白箱（ホワイトボックス）テストケースを補う**  
   - `if b == 0` という分岐に必ず到達させる  
   - ほかに分岐や例外があれば、それぞれのルートをチェック

4. **Pytest のファイルを作成してテストを書く**  
   - `test_calculator.py` のような名前にする  
   - 実際に `add(a, b)` や `divide(a, b)` を呼び出し、`assert` で期待結果をチェック

5. **Pytest 実行**  
   - `pytest test_calculator.py`  
   - 必要に応じて `pytest --cov` などでカバレッジ測定

6. **失敗テストを確認→原因を修正**  
   - コード側の不具合か？ テストケースが誤っているか？  
   - 問題を発見・修正する中でテストの重要性を体感

---

## 5. ブラックボックステストの例

仕様に沿って「入力→期待する出力」を決め、実装の分岐は考えずに検証します。

```　python
# test_calculator_blackbox.py

import pytest
from calculator import add, subtract, multiply, divide

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),        # 正数×正数
        (-1, 5, 4),       # 負数＋正数
        (0, 10, 10),      # 0＋正数
        (1.5, 2.5, 4.0),  # 小数
    ]
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (5, 2, 3),
        (-1, -2, 1),
        (3.5, 1.5, 2.0),
    ]
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),
        (-1, -2, 2),
        (0, 5, 0),
        (2.5, 2, 5.0),
    ]
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


def test_divide_normal():
    # 0 以外の割り算
    assert divide(10, 2) == 5.0
    assert divide(-6, 3) == -2.0

def test_divide_zero():
    # 0 割時はエラーが出るか
    with pytest.raises(ValueError):
        divide(10, 0)
```

---

## 6. ホワイトボックステストの例 

`if b == 0:` の分岐を含めて、コード内部の行や分岐をきちんと網羅する考え方。

``` python
# test_calculator_whitebox.py

import pytest
from calculator import add, subtract, multiply, divide

def test_add_paths():
    # 分岐はないが、多様なパターンを通すことでC0を超えた網羅を狙う
    assert add(3, 4) == 7
    assert add(-1, 5) == 4
    assert add(0, 0) == 0

def test_subtract_paths():
    # subtractも分岐なし、複数パターン
    assert subtract(5, 3) == 2
    assert subtract(-2, -3) == 1

def test_multiply_paths():
    # multiplyも分岐なし
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6

def test_divide_paths():
    # divideは b == 0 の分岐あり → 0割ルートと通常ルートを網羅
    assert divide(8, 4) == 2.0
    with pytest.raises(ValueError):
        divide(1, 0)
```

---

## 7. まとめ

- **ブラックボックステスト**  
  - 「入力と出力」のみ重視  
  - 仕様通りに動くかをユーザー視点でチェック  
  - **同値分割**, **境界値分析** などを活用  
- **ホワイトボックステスト**  
  - コードの分岐・例外ルートをすべて通るように設計  
  - カバレッジ (C0, C1, etc.) を指標に漏れを減らす  
  - 実装の細部を意識

初心者はまず **ブラックボックス的な視点** で「正常系・異常系をしっかりカバー」し、次に **ホワイトボックス的な視点** で「分岐やカバレッジの漏れがないか」を確認するのがおすすめです。これで `calculator.py` を使ったテスト学習がより効率的になります。  
