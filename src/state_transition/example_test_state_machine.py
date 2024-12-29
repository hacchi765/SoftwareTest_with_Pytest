# tests/test_state_machine.py
from PytestPractice.src.state_transition.state_machine import UserSession

def test_state_machine():
    session = UserSession()

    # 初期状態: LOGGED_OUT
    assert session.state == "LOGGED_OUT"

    # LOGGED_OUT -> login -> LOGGED_IN
    assert session.login("user", "pass") is True
    assert session.state == "LOGGED_IN"

    # LOGGED_IN -> logout -> LOGGED_OUT
    assert session.logout() is True
    assert session.state == "LOGGED_OUT"

    # LOGGED_OUTでlogoutしてもFalse（状態変わらず）
    assert session.logout() is False
    assert session.state == "LOGGED_OUT"
