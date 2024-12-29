import streamlit as st
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd

def run_pytest_junit():
    """
    Pytest を --junitxml オプション付きで実行し、
    テスト結果を 'pytest_report.xml' に出力する。
    """
    # 既存のレポートファイルがあれば削除
    report_file = Path("pytest_report.xml")
    if report_file.exists():
        report_file.unlink()

    # Pytest 実行コマンド
    cmd = ["pytest", "--junitxml=pytest_report.xml", "-vv"]  # -vv で詳細ログ
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode

def parse_junit_xml(xml_path: str):
    """
    JUnit XML レポートをパースし、テストケースごとの情報をリスト化する。
    返却: [
      {
        "classname": str,
        "testcase": str,
        "status": str,     # PASSED / FAILED / ERROR / SKIPPED
        "time": str,
        "detail": str      # 失敗・エラー時のメッセージなど
      },
      ...
    ]
    """
    test_data = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for testsuite in root.findall("testsuite"):
        for testcase in testsuite.findall("testcase"):
            classname = testcase.get("classname", "")
            name = testcase.get("name", "")
            time = testcase.get("time", "0.0")

            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped = testcase.find("skipped")

            if failure is not None:
                status = "FAILED"
                detail = failure.text or ""
            elif error is not None:
                status = "ERROR"
                detail = error.text or ""
            elif skipped is not None:
                status = "SKIPPED"
                detail = skipped.get("message", "")
            else:
                status = "PASSED"
                detail = ""

            test_data.append({
                "classname": classname,
                "testcase": name,
                "status": status,
                "time": time,
                "detail": detail.strip()
            })

    return test_data

def show_test_results_in_table(test_data):
    """
    テスト結果を DataFrame として表示し、Status列をアイコン付き＆色文字でわかりやすく示す。
    背景色は白のままにし、テキストだけ色を変える。
    """
    st.write("## テスト結果")
    df = pd.DataFrame(test_data)

    if not df.empty:
        # カラム順と表示名を整理
        df = df[["classname", "testcase", "status", "time", "detail"]]
        df.columns = ["テストが含まれるファイル", "テストの名前", "ステータス", "実行時間(秒)", "詳細"]

        # アイコンを付けた新列を作成
        icons = []
        for status in df["ステータス"]:
            if status == "PASSED":
                icons.append("✅ 成功")
            elif status in ["FAILED", "ERROR"]:
                icons.append("❌ " + status)
            elif status == "SKIPPED":
                icons.append("⏭️ スキップ")
            else:
                icons.append(status)

        df["結果"] = icons  # 新しい列を追加して後で表示に使う
        df = df[["テストが含まれるファイル", "テストの名前", "結果", "実行時間(秒)", "詳細"]]

        # ステータス行の文字色だけ変更
        def highlight_result(val):
            if "成功" in val:
                return "color: green;"
            elif "FAILED" in val or "ERROR" in val:
                return "color: red;"
            elif "スキップ" in val:
                return "color: gray;"
            return ""

        styled = df.style.applymap(highlight_result, subset=["結果"])
        st.write(styled.to_html(), unsafe_allow_html=True)
    else:
        st.info("テストが見つかりませんでした。")

def main():
    st.title("初心者向けテスト結果表示アプリ")
    st.write("""
    このアプリでは、Python のテストフレームワーク Pytest を使ったテストを
    ワンクリックで実行し、その結果をわかりやすく表示します。  
    """)

    if st.button("テストを実行する"):
        return_code = run_pytest_junit()
        if return_code == 0:
            st.success("テストがすべて成功しました！")
        else:
            st.error("一部のテストでエラーが発生しました。")

        xml_path = Path("pytest_report.xml")
        if xml_path.exists():
            test_data = parse_junit_xml(str(xml_path))
            show_test_results_in_table(test_data)
        else:
            st.warning("テスト結果ファイルが見つかりませんでした。")

if __name__ == "__main__":
    main()
