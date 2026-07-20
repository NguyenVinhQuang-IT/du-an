"""
rename_tool.py - Chạy ứng dụng Đổi Tên File bằng PyWebView
Giao diện: HTML/CSS/JS (index.html, style.css, app.js)
Logic xử lý: logic.py
"""

import os
import sys
import webview

from logic import (
    lay_danh_sach_file,
    tao_ten_moi,
    doi_ten_file,
    lay_ten_day_du,
    lay_ten_khong_duoi,
    nhan_dien_ky_tu,
    ten_hien_thi,
    lay_chuoi_thuc_te,
)


class Api:
    """API class để JS gọi Python qua pywebview."""

    def __init__(self):
        self.folder = ""
        self.preview_data = []
        self.window = None

    # ---------- 1. Chọn thư mục ----------
    def chon_thu_muc(self):
        result = self.window.create_file_dialog(
            webview.FOLDER_DIALOG
        )
        if result and len(result) > 0:
            self.folder = result[0]
            return self.folder
        return None

    # ---------- 2. Lấy danh sách file ----------
    def lay_danh_sach(self):
        if not self.folder:
            return []
        return lay_danh_sach_file(self.folder)

    # ---------- 3. Xem trước ----------
    def xem_truoc(self, find, replace):
        if not self.folder:
            return []
        files = lay_danh_sach_file(self.folder)
        self.preview_data = tao_ten_moi(files, find, replace)
        return self.preview_data

    # ---------- 4. Đổi tên ----------
    def doi_ten(self):
        if not self.preview_data:
            return {"success": False, "message": "Chưa có dữ liệu xem trước", "count": 0}

        try:
            count = doi_ten_file(self.folder, self.preview_data)
            self.preview_data = []
            return {"success": True, "message": "Đổi tên thành công", "count": count}
        except Exception as e:
            return {"success": False, "message": str(e), "count": 0}

    # ---------- 5. Copy tên (có đuôi) ----------
    def copy_ten_day_du(self):
        if not self.folder:
            return None
        text, total = lay_ten_day_du(self.folder)
        self.window.evaluate_js(f"""
            navigator.clipboard.writeText(`{text.replace(chr(96), "")}`);
        """)
        return {"text": text, "count": total}

    # ---------- 6. Copy tên (không đuôi) ----------
    def copy_ten_khong_duoi(self):
        if not self.folder:
            return None
        text, total = lay_ten_khong_duoi(self.folder)
        self.window.evaluate_js(f"""
            navigator.clipboard.writeText(`{text.replace(chr(96), "")}`);
        """)
        return {"text": text, "count": total}

    # ---------- 7. Nhận diện ký tự ----------
    def nhan_dien_ky_tu_js(self):
        if not self.folder:
            return None

        files = lay_danh_sach_file(self.folder)
        if not files:
            return None

        special_chars, common_patterns = nhan_dien_ky_tu(self.folder)

        if not special_chars and not common_patterns:
            return {"has_data": False}

        # Chuyển đổi sang format JSON-friendly
        sc_list = []
        for ch, count in special_chars.most_common():
            sc_list.append({
                "char": ch,
                "display": ten_hien_thi(ch),
                "count": count
            })

        cp_list = []
        for pattern, count in common_patterns.most_common():
            cp_list.append({
                "pattern": pattern,
                "actual": lay_chuoi_thuc_te(pattern),
                "count": count
            })

        return {
            "has_data": True,
            "special_chars": sc_list,
            "common_patterns": cp_list
        }


def resource_path(relative_path):
    """
    Lấy đường dẫn tuyệt đối đến tài nguyên.
    Khi chạy từ .exe (PyInstaller), file nằm trong sys._MEIPASS.
    Khi chạy bình thường, dùng đường dẫn thư mục hiện tại.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# ===== Chạy ứng dụng =====
if __name__ == "__main__":
    api = Api()

    # Lấy đường dẫn đến file HTML (hỗ trợ cả chạy trực tiếp và từ .exe)
    html_path = resource_path("index.html")

    window = webview.create_window(
        title="Công Cụ Đổi Tên File Hàng Loạt",
        url=html_path,
        js_api=api,
        width=950,
        height=700,
        min_size=(800, 550),
    )

    api.window = window

    webview.start(debug=False)