import subprocess
import sys
from pathlib import Path

# 標題
def print_header():
    print("=" * 50)
    print(" 🔐 PyArmor 一鍵混淆工具 ")
    print("=" * 50)

# 顯示成功訊息
def print_success(msg):
    print(f"[✅] {msg}")

# 顯示錯誤訊息
def print_error(msg):
    print(f"[❌] {msg}")

# 檢查 pyarmor 是否安裝
def check_pyarmor():
    try:
        subprocess.run(["pyarmor", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except Exception:
        return False

# 執行混淆指令
def obfuscate_file(filepath: Path, output_dir: Path):
    cmd = [
        "pyarmor", "gen",
        "--output", str(output_dir),
        str(filepath)
    ]
    subprocess.run(cmd, check=True)

# 主執行邏輯
def main():
    print_header()

    if not check_pyarmor():
        print_error("未安裝 PyArmor！請先執行：pip install pyarmor")
        sys.exit(1)

    target = input("請輸入要混淆的檔案或資料夾路徑：").strip()

    # 移除路徑中的引號
    if target.startswith('"') and target.endswith('"'):
        target = target[1:-1]
    elif target.startswith("'") and target.endswith("'"):
        target = target[1:-1]

    path = Path(target)

    if not path.exists():
        print_error("指定的路徑不存在。")
        return

    output_base = Path("Obfuscation")
    output_base.mkdir(exist_ok=True)

    if path.is_file() and path.suffix == ".py":
        print(f"正在混淆檔案：{path.name}")
        obfuscate_file(path, output_base / path.stem)
        print_success(f"{path.name} 混淆完成！結果儲存在 Obfuscation/{path.stem}/")

    elif path.is_dir():
        py_files = list(path.rglob("*.py"))
        if not py_files:
            print_error("資料夾中找不到任何 .py 檔案。")
            return

        for py in py_files:
            print(f"→ 混淆：{py.relative_to(path)}")
            output_dir = output_base / py.stem
            output_dir.mkdir(parents=True, exist_ok=True)
            obfuscate_file(py, output_dir)
        print_success("全部檔案混淆完成！請查看 Obfuscation/")
    else:
        print_error("請指定 .py 檔案或包含 Python 檔案的資料夾。")

if __name__ == "__main__":
    main()
