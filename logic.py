"""
logic.py - Xử lý chức năng đổi tên file
Chứa tất cả logic xử lý, không phụ thuộc vào giao diện.
"""

import os
import re
from collections import Counter


def lay_danh_sach_file(folder):
    """Lấy danh sách file trong thư mục (chỉ file, không lấy thư mục con)."""
    if not folder or not os.path.isdir(folder):
        return []
    return sorted(
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    )


def tao_ten_moi(files, find, replace):
    """
    Tạo danh sách (tên_cũ, tên_mới) dựa trên chuỗi tìm và thay thế.
    Trả về list of tuples: [(old_name, new_name), ...]
    """
    result = []
    for f in files:
        new_name = f.replace(find, replace)
        result.append((f, new_name))
    return result


def doi_ten_file(folder, preview_data):
    """
    Thực hiện đổi tên file trên ổ đĩa.
    Trả về số file đã đổi tên thành công.
    """
    count = 0
    for old, new in preview_data:
        if old != new:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            os.rename(old_path, new_path)
            count += 1
    return count


def lay_ten_day_du(folder):
    """Lấy danh sách tên file đầy đủ (có đuôi, ví dụ: baocao.pdf)."""
    files = lay_danh_sach_file(folder)
    return "\n".join(files), len(files)


def lay_ten_khong_duoi(folder):
    """Lấy danh sách tên file không có đuôi (ví dụ: baocao)."""
    files = lay_danh_sach_file(folder)
    names = [os.path.splitext(f)[0] for f in files]
    return "\n".join(names), len(names)


def nhan_dien_ky_tu(folder):
    """
    Quét tên file trong thư mục, tìm ký tự đặc biệt và chuỗi phổ biến.
    Trả về (special_chars: Counter, common_patterns: Counter)
    """
    files = lay_danh_sach_file(folder)

    special_chars = Counter()
    common_patterns = Counter()

    for f in files:
        name, ext = os.path.splitext(f)

        # --- Ký tự đặc biệt đơn lẻ ---
        for ch in name:
            if not ch.isalnum() and ch not in ('.',):
                special_chars[ch] += 1

        # --- Dấu cách ---
        # Nhiều dấu cách liên tiếp
        multi_spaces = re.findall(r' {2,}', name)
        for sp in multi_spaces:
            label = f'{"⎵" * len(sp)} ({len(sp)} dấu cách)'
            common_patterns[label] += 1
        # Dấu cách ở đầu tên
        if name != name.lstrip(' '):
            leading = len(name) - len(name.lstrip(' '))
            common_patterns[f'⎵×{leading} ở đầu tên ({leading} dấu cách đầu)'] += 1
        # Dấu cách ở cuối tên
        if name != name.rstrip(' '):
            trailing = len(name) - len(name.rstrip(' '))
            common_patterns[f'⎵×{trailing} ở cuối tên ({trailing} dấu cách cuối)'] += 1

        # --- Dấu gạch ---
        if '_' in name:
            common_patterns['_ (gạch dưới)'] += name.count('_')
        if '-' in name:
            common_patterns['- (gạch ngang)'] += name.count('-')
        # Nhiều gạch ngang liên tiếp
        multi_dash = re.findall(r'-{2,}', name)
        for md in multi_dash:
            common_patterns[f'{md} ({len(md)} gạch ngang liên tiếp)'] += 1
        # Nhiều gạch dưới liên tiếp
        multi_under = re.findall(r'_{2,}', name)
        for mu in multi_under:
            common_patterns[f'{mu} ({len(mu)} gạch dưới liên tiếp)'] += 1

        # --- Dấu chấm (không phải phần mở rộng) ---
        dots_in_name = name.count('.')
        if dots_in_name > 0:
            common_patterns['. (dấu chấm trong tên)'] += dots_in_name

        # --- Chuỗi số dài (ví dụ: timestamp, mã số) ---
        numbers = re.findall(r'\d{4,}', name)
        for num in numbers:
            common_patterns[f'{num} (chuỗi số)'] += 1

        # --- Dấu ngoặc tròn và nội dung ---
        brackets = re.findall(r'\([^)]*\)', name)
        for b in brackets:
            common_patterns[b] += 1

        # --- Dấu ngoặc vuông và nội dung ---
        brackets2 = re.findall(r'\[[^\]]*\]', name)
        for b in brackets2:
            common_patterns[b] += 1

        # --- Dấu ngoặc nhọn và nội dung ---
        brackets3 = re.findall(r'\{[^}]*\}', name)
        for b in brackets3:
            common_patterns[b] += 1

        # --- Ký tự đặc biệt phổ biến khác ---
        if '~' in name:
            common_patterns['~ (dấu ngã)'] += name.count('~')
        if '@' in name:
            common_patterns['@ (dấu at)'] += name.count('@')
        if '#' in name:
            common_patterns['# (dấu thăng)'] += name.count('#')
        if '$' in name:
            common_patterns['$ (dấu đô la)'] += name.count('$')
        if '%' in name:
            common_patterns['% (dấu phần trăm)'] += name.count('%')
        if '^' in name:
            common_patterns['^ (dấu mũ)'] += name.count('^')
        if '&' in name:
            common_patterns['& (dấu và)'] += name.count('&')
        if '+' in name:
            common_patterns['+ (dấu cộng)'] += name.count('+')
        if '=' in name:
            common_patterns['= (dấu bằng)'] += name.count('=')
        if '!' in name:
            common_patterns['! (dấu chấm than)'] += name.count('!')
        if ';' in name:
            common_patterns['; (dấu chấm phẩy)'] += name.count(';')
        if ',' in name:
            common_patterns[', (dấu phẩy)'] += name.count(',')
        if "'" in name:
            common_patterns["' (dấu nháy đơn)"] += name.count("'")
        if '"' in name:
            common_patterns['" (dấu nháy kép)'] += name.count('"')
        if '`' in name:
            common_patterns['` (dấu backtick)'] += name.count('`')

        # --- Ký tự Unicode đặc biệt / không phải ASCII ---
        for ch in name:
            if ord(ch) > 127 and not ch.isalnum():
                common_patterns[f'{ch} (Unicode U+{ord(ch):04X})'] += 1

        # --- Tab trong tên file ---
        if '\t' in name:
            common_patterns['→ (ký tự tab)'] += name.count('\t')

    # --- Tìm prefix chung (tiền tố giống nhau ở nhiều file) ---
    if len(files) >= 2:
        names = [os.path.splitext(f)[0] for f in files]
        prefix = _tim_prefix_chung(names)
        if prefix and len(prefix) >= 2:
            count = sum(1 for n in names if n.startswith(prefix))
            if count >= 2:
                common_patterns[f'{prefix} (tiền tố chung {count} file)'] = count

    # --- Tìm suffix chung (hậu tố giống nhau ở nhiều file) ---
    if len(files) >= 2:
        names = [os.path.splitext(f)[0] for f in files]
        suffix = _tim_suffix_chung(names)
        if suffix and len(suffix) >= 2:
            count = sum(1 for n in names if n.endswith(suffix))
            if count >= 2:
                common_patterns[f'{suffix} (hậu tố chung {count} file)'] = count

    # --- Tìm chuỗi lặp lại ở nhiều file (substring chung >= 3 ký tự) ---
    if len(files) >= 3:
        names = [os.path.splitext(f)[0] for f in files]
        repeated = _tim_chuoi_lap(names)
        for sub, cnt in repeated:
            key = f'{sub} (lặp lại {cnt} file)'
            if key not in common_patterns:
                common_patterns[key] = cnt

    return special_chars, common_patterns


def _tim_prefix_chung(names):
    """Tìm tiền tố chung dài nhất của danh sách tên."""
    if not names:
        return ''
    prefix = names[0]
    for name in names[1:]:
        while not name.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ''
    return prefix.rstrip()


def _tim_suffix_chung(names):
    """Tìm hậu tố chung dài nhất của danh sách tên."""
    if not names:
        return ''
    suffix = names[0]
    for name in names[1:]:
        while not name.endswith(suffix):
            suffix = suffix[1:]
            if not suffix:
                return ''
    return suffix.lstrip()


def _tim_chuoi_lap(names, min_len=3, min_count=3):
    """
    Tìm các chuỗi con (substring) xuất hiện trong >= min_count tên file.
    Trả về list of (substring, count), sắp xếp theo count giảm dần.
    Chỉ trả về tối đa 5 kết quả để tránh quá nhiều.
    """
    # Giới hạn số file để tránh lag
    if len(names) > 50:
        names = names[:50]

    # Thu thập substring cho mỗi tên (giới hạn độ dài để tránh chậm)
    max_sub_len = 15
    seen_per_name = {}
    for name in names:
        seen = set()
        name_len = len(name)
        for length in range(min_len, min(name_len + 1, max_sub_len + 1)):
            for start in range(name_len - length + 1):
                sub = name[start:start + length]
                if not sub.isdigit() and not sub.isspace():
                    seen.add(sub)
        seen_per_name[name] = seen

    # Đếm mỗi substring xuất hiện ở bao nhiêu file (dùng Counter nhanh hơn)
    substr_counts = Counter()
    for seen in seen_per_name.values():
        for sub in seen:
            substr_counts[sub] += 1

    # Chỉ lấy những substring đủ điều kiện
    results = [(sub, cnt) for sub, cnt in substr_counts.items() if cnt >= min_count]

    # Lọc: ưu tiên substring dài, loại bỏ ngắn nếu đã có dài hơn chứa nó
    results.sort(key=lambda x: (-len(x[0]), -x[1]))
    filtered = []
    for sub, cnt in results:
        if not any(sub in existing for existing, _ in filtered):
            filtered.append((sub, cnt))
        if len(filtered) >= 5:
            break

    filtered.sort(key=lambda x: -x[1])
    return filtered[:5]


def ten_hien_thi(ch):
    """Chuyển ký tự đặc biệt sang tên hiển thị dễ đọc."""
    hien_thi = {
        ' ': '⎵ (dấu cách)',
        '\t': '→ (tab)',
        '\n': '↵ (xuống dòng)',
        '_': '_ (gạch dưới)',
        '-': '- (gạch ngang)',
        '.': '. (dấu chấm)',
        '~': '~ (dấu ngã)',
        '@': '@ (dấu at)',
        '#': '# (dấu thăng)',
        '$': '$ (dấu đô la)',
        '%': '% (dấu phần trăm)',
        '^': '^ (dấu mũ)',
        '&': '& (dấu và)',
        '*': '* (dấu sao)',
        '+': '+ (dấu cộng)',
        '=': '= (dấu bằng)',
        '!': '! (dấu chấm than)',
        '?': '? (dấu hỏi)',
        '/': '/ (dấu gạch chéo)',
        '\\': '\\ (dấu gạch chéo ngược)',
        '|': '| (dấu gạch đứng)',
        ':': ': (dấu hai chấm)',
        ';': '; (dấu chấm phẩy)',
        ',': ', (dấu phẩy)',
        "'": "' (dấu nháy đơn)",
        '"': '" (dấu nháy kép)',
        '`': '` (dấu backtick)',
        '(': '( (mở ngoặc tròn)',
        ')': ') (đóng ngoặc tròn)',
        '[': '[ (mở ngoặc vuông)',
        ']': '] (đóng ngoặc vuông)',
        '{': '{ (mở ngoặc nhọn)',
        '}': '} (đóng ngoặc nhọn)',
        '<': '< (dấu nhỏ hơn)',
        '>': '> (dấu lớn hơn)',
        '©': '© (bản quyền)',
        '®': '® (đã đăng ký)',
        '™': '™ (thương hiệu)',
        '°': '° (dấu độ)',
        '…': '… (dấu ba chấm)',
        '–': '– (gạch ngang dài)',
        '—': '— (gạch ngang rất dài)',
        '•': '• (dấu chấm tròn)',
        '×': '× (dấu nhân)',
        '÷': '÷ (dấu chia)',
        '±': '± (dấu cộng trừ)',
        '≠': '≠ (dấu khác)',
        '≤': '≤ (nhỏ hơn hoặc bằng)',
        '≥': '≥ (lớn hơn hoặc bằng)',
        '∞': '∞ (vô cực)',
        '√': '√ (căn bậc hai)',
        '←': '← (mũi tên trái)',
        '→': '→ (mũi tên phải)',
        '↑': '↑ (mũi tên lên)',
        '↓': '↓ (mũi tên xuống)',
        '«': '« (ngoặc kép Pháp mở)',
        '»': '» (ngoặc kép Pháp đóng)',
        '\u200b': '⊘ (zero-width space)',
        '\u200c': '⊘ (zero-width non-joiner)',
        '\u200d': '⊘ (zero-width joiner)',
        '\u00a0': '⎵ (non-breaking space)',
        '\ufeff': '⊘ (BOM / zero-width no-break)',
    }
    if ch in hien_thi:
        return hien_thi[ch]
    # Ký tự Unicode không phổ biến
    if ord(ch) > 127:
        return f'{ch} (U+{ord(ch):04X})'
    return ch


def lay_chuoi_thuc_te(pattern):
    """Lấy chuỗi thực tế từ pattern (bỏ phần mô tả trong ngoặc)."""
    # Xử lý trường hợp pattern kết thúc bằng dấu ngoặc mô tả
    # Ví dụ: "_ (gạch dưới)" -> "_"
    # Nhưng không ảnh hưởng đến "(1)" hay "[abc]"
    if ' (' in pattern:
        parts = pattern.rsplit(' (', 1)
        if parts[1].endswith(')'):
            return parts[0]
    return pattern
