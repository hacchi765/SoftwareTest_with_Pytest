# ホワイトボックス/ブラックボックステスト

## 概要
初学者が「calculator.py」を題材にホワイトボックス/ブラックボックステストを学ぶためのドキュメントです。

## テスト対象のコード
```python
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

## ホワイトボックステストとブラックボックステストの違い

### ブラックボックステスト
- コード内部の実装・構造を意識せず、入力と出力だけを基にテストする
- 同値分割や境界値分析など、仕様やユーザーの期待を中心にテストケースを作る

### ホワイトボックステスト
- コードの内部ロジック（if文や例外処理）を把握し、すべての分岐をテストで通す
- C0/C1/C2 などのカバレッジを意識して漏れを防ぐ

## テストケースの設計

### ブラックボックステストの例
```python
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

### ホワイトボックステストの例
```python
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

## テストの実行方法
1. `calculator.py` をプロジェクト直下に配置
2. `tests/test_calculator.py` にテストコードを作成
3. 以下のコマンドでテストを実行
```bash
cd my_calculator_project
pytest
```

## まとめ
- ブラックボックステストは入力と出力のみを重視し、仕様通りに動くかをユーザー視点でチェック
- ホワイトボックステストはコードの分岐・例外ルートをすべて通るように設計し、カバレッジを指標に漏れを減らす
- 初心者はまずブラックボックス的な視点で正常系・異常系をカバーし、次にホワイトボックス的な視点で分岐やカバレッジの漏れを確認するのがオススメ
