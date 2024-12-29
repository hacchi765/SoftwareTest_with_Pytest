# src/state_machine.py

class UserSession:
    """
    シンプルな状態遷移の例:
    - "LOGGED_OUT" -> "LOGGED_IN" -> "LOGGED_OUT"
    """
    def __init__(self):
        self.state = "LOGGED_OUT"

    def login(self, username, password):
        if self.state == "LOGGED_OUT":
            # 本来は認証処理など
            self.state = "LOGGED_IN"
            return True
        return False

    def logout(self):
        if self.state == "LOGGED_IN":
            self.state = "LOGGED_OUT"
            return True
        return False
