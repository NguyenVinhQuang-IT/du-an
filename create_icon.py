"""
create_icon.py - Chuyển đổi ảnh PNG thành file icon.ico cho ứng dụng
Tạo icon với nhiều kích thước (16, 24, 32, 48, 64, 128, 256 px)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn ảnh gốc
SOURCE_IMAGE = os.path.join(
    os.path.expanduser("~"),
    ".gemini", "antigravity-ide", "brain",
    "64686c1f-bd2d-4b73-b97e-dda2edaaffd1",
    "app_icon_1784338165243.png"
)

OUTPUT_ICO = os.path.join(BASE_DIR, "icon.ico")

# Các kích thước icon cần tạo
SIZES = [16, 24, 32, 48, 64, 128, 256]


def create_ico():
    if not os.path.exists(SOURCE_IMAGE):
        print(f"❌ Không tìm thấy ảnh: {SOURCE_IMAGE}")
        sys.exit(1)

    print(f"🎨 Đang mở ảnh: {os.path.basename(SOURCE_IMAGE)}")
    img = Image.open(SOURCE_IMAGE)

    # Chuyển sang RGBA nếu chưa
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Tạo danh sách ảnh ở các kích thước
    icon_images = []
    for size in SIZES:
        resized = img.resize((size, size), Image.LANCZOS)
        icon_images.append(resized)
        print(f"   ✅ {size}x{size} px")

    # Lưu file .ico
    icon_images[0].save(
        OUTPUT_ICO,
        format='ICO',
        sizes=[(s, s) for s in SIZES],
        append_images=icon_images[1:]
    )

    size_kb = os.path.getsize(OUTPUT_ICO) / 1024
    print(f"\n✅ Đã tạo: {OUTPUT_ICO}")
    print(f"📐 Kích thước: {size_kb:.1f} KB")
    print(f"📏 Bao gồm {len(SIZES)} kích thước: {SIZES}")


if __name__ == "__main__":
    create_ico()
