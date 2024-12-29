# src/discount_logic.py

def get_discount_rate(member_type: str, purchase_amount: int, has_coupon: bool) -> int:
    """
    複数の条件で割引率が決まるロジック：
    - member_type: 'gold', 'silver', 'normal'
    - purchase_amount: 購入金額
    - has_coupon: True/False
    """
    # 単純な例: 
    # gold & couponあり & purchase_amount>=5000 -> 20%
    # gold & couponあり & purchase_amount<5000  -> 15%
    # gold & couponなし -> 10% ...
    # （詳細はテスト側でディシジョンテーブル化して確認）
    
    if member_type == 'gold':
        if has_coupon:
            if purchase_amount >= 5000:
                return 20
            else:
                return 15
        else:
            return 10
    elif member_type == 'silver':
        if has_coupon:
            return 10
        else:
            return 5
    else:  # normal
        if purchase_amount >= 5000:
            return 5
        else:
            return 0
