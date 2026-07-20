"""
build.py - Đóng gói ứng dụng Đổi Tên File thành file .exe
Chạy: python build.py
Kết quả: thư mục dist/ chứa file .exe
"""

import os
import sys
import subprocess
import shutil

# Fix encoding cho Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# === Cấu hình ===
APP_NAME = "DoiTenFile"
MAIN_SCRIPT = "rename_tool.py"
ICON_FILE = "icon.ico"  # Tùy chọn, nếu không có sẽ bỏ qua

# Các file cần gom vào exe
DATA_FILES = [
    "index.html",
    "style.css",
    "app.js",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def check_pyinstaller():
    """Kiểm tra và cài đặt PyInstaller nếu chưa có."""
    try:
        import PyInstaller
        print(f"✅ PyInstaller đã cài (v{PyInstaller.__version__})")
    except ImportError:
        print("📦 Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ Đã cài xong PyInstaller")


def build():
    """Chạy PyInstaller để đóng gói."""
    os.chdir(BASE_DIR)

    # Xóa build cũ
    for folder in ["build", "dist"]:
        path = os.path.join(BASE_DIR, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🗑️  Đã xóa {folder}/")

    spec_file = os.path.join(BASE_DIR, f"{APP_NAME}.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # Xây dựng lệnh PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",               # Thư mục chứa exe + dependencies (khởi động nhanh)
        "--windowed",             # Không hiện cửa sổ console
        f"--name={APP_NAME}",
    ]

    # Thêm icon nếu có
    icon_path = os.path.join(BASE_DIR, ICON_FILE)
    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
        print(f"🎨 Sử dụng icon: {ICON_FILE}")
    else:
        print(f"ℹ️  Không tìm thấy {ICON_FILE}, bỏ qua icon")

    # Thêm data files (HTML, CSS, JS)
    for f in DATA_FILES:
        file_path = os.path.join(BASE_DIR, f)
        if os.path.exists(file_path):
            # Trên Windows, dùng dấu ;  
            cmd.append(f"--add-data={file_path};.")
            print(f"📎 Gom file: {f}")
        else:
            print(f"⚠️  Không tìm thấy: {f}")

    # Thêm hidden imports cho pywebview
    hidden_imports = [
        "webview",
        "webview.platforms.edgechromium",
        "webview.platforms.mshtml",
        "webview.platforms.winforms",
        "clr_loader",
        "pythonnet",
    ]
    for hi in hidden_imports:
        cmd.append(f"--hidden-import={hi}")

    # File chính
    cmd.append(MAIN_SCRIPT)

    print("\n🔨 Đang đóng gói...\n")
    print(f"   Lệnh: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=BASE_DIR)

    if result.returncode == 0:
        exe_path = os.path.join(BASE_DIR, "dist", APP_NAME, f"{APP_NAME}.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n{'='*50}")
            print(f"✅ ĐÓNG GÓI THÀNH CÔNG!")
            print(f"{'='*50}")
            print(f"📁 Thư mục: dist/{APP_NAME}/")
            print(f"📁 File:    dist/{APP_NAME}/{APP_NAME}.exe")
            print(f"📐 Kích thước exe: {size_mb:.1f} MB")
            print(f"{'='*50}")
        else:
            print("\n⚠️  Build xong nhưng không tìm thấy file .exe")
    else:
        print(f"\n❌ Đóng gói thất bại (exit code: {result.returncode})")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ĐÓNG GÓI ỨNG DỤNG ĐỔI TÊN FILE")
    print("=" * 50)
    print()

    check_pyinstaller()
    build()
