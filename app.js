// ===== Kết nối với Python API qua pywebview =====

// Chờ pywebview sẵn sàng
window.addEventListener('pywebviewready', function() {
    console.log('pywebview ready!');
});

// Hàm gọi API Python (có fallback nếu chưa sẵn sàng)
function callPython(method, ...args) {
    if (window.pywebview && window.pywebview.api) {
        return window.pywebview.api[method](...args);
    }
    showToast('⚠️ Chưa kết nối với Python backend');
    return Promise.resolve(null);
}

// ===== Toast notification =====
function showToast(message, duration = 2500) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

// ===== 1. Chọn Thư Mục =====
async function chonThuMuc() {
    const result = await callPython('chon_thu_muc');
    if (result) {
        const folderPath = document.getElementById('folderPath');
        folderPath.textContent = result;
        folderPath.classList.add('active');
        await loadFiles();
    }
}

// ===== Load danh sách file =====
async function loadFiles() {
    const files = await callPython('lay_danh_sach');
    if (files === null) return;

    const tbody = document.getElementById('fileTableBody');
    const fileCount = document.getElementById('fileCount');
    const totalCount = document.getElementById('totalCount');

    if (files.length === 0) {
        tbody.innerHTML = `
            <tr class="empty-row">
                <td colspan="3">
                    <div class="empty-state">
                        <span class="empty-icon">📭</span>
                        <p>Thư mục không có file nào.</p>
                    </div>
                </td>
            </tr>`;
        fileCount.textContent = '0 file';
        totalCount.textContent = 'Tổng số: 0 file';
        return;
    }

    tbody.innerHTML = files.map((f, i) => `
        <tr>
            <td>${i + 1}</td>
            <td>${escapeHtml(f)}</td>
            <td></td>
        </tr>
    `).join('');

    fileCount.textContent = `${files.length} file`;
    totalCount.textContent = `Tổng số: ${files.length} file`;
}

// ===== 2. Xem trước =====
async function xemTruoc() {
    const find = document.getElementById('txtFind').value;
    const replace = document.getElementById('txtReplace').value;

    if (!find) {
        showToast('⚠️ Vui lòng nhập chuỗi cần tìm');
        return;
    }

    const result = await callPython('xem_truoc', find, replace);
    if (result === null) return;

    const tbody = document.getElementById('fileTableBody');
    tbody.innerHTML = result.map((item, i) => {
        const changed = item[0] !== item[1];
        return `
            <tr>
                <td>${i + 1}</td>
                <td>${escapeHtml(item[0])}</td>
                <td class="${changed ? 'changed' : ''}">${escapeHtml(item[1])}</td>
            </tr>
        `;
    }).join('');
}

// ===== 3. Đổi tên =====
async function doiTen() {
    const result = await callPython('doi_ten');
    if (result === null) return;

    if (result.success) {
        showToast(`✅ Đổi tên thành công ${result.count} file`);
        await loadFiles();
    } else {
        showToast('⚠️ ' + result.message);
    }
}

// ===== 4. Copy tên =====
async function copyTenDayDu() {
    const result = await callPython('copy_ten_day_du');
    if (result) {
        showToast(`📋 Đã copy ${result.count} tên file (có đuôi)`);
    }
}

async function copyTenKhongDuoi() {
    const result = await callPython('copy_ten_khong_duoi');
    if (result) {
        showToast(`📄 Đã copy ${result.count} tên file (không đuôi)`);
    }
}

// ===== 5. Nhận diện ký tự =====
async function nhanDienKyTu() {
    const result = await callPython('nhan_dien_ky_tu_js');
    if (result === null) return;

    if (!result.has_data) {
        showToast('ℹ️ Không tìm thấy ký tự đặc biệt nào');
        return;
    }

    // Render Tab 1: Ký tự đơn
    const tab1 = document.getElementById('tabKyTuDon');
    if (result.special_chars.length > 0) {
        tab1.innerHTML = result.special_chars.map(item => `
            <div class="char-item" onclick="chonKyTu('${escapeJs(item.char)}')">
                <span class="char-label">${escapeHtml(item.display)}</span>
                <span class="char-count">xuất hiện ${item.count} lần</span>
            </div>
        `).join('');
    } else {
        tab1.innerHTML = '<div class="no-data">Không có ký tự đơn đặc biệt.</div>';
    }

    // Render Tab 2: Chuỗi phổ biến
    const tab2 = document.getElementById('tabChuoiPhoBien');
    if (result.common_patterns.length > 0) {
        tab2.innerHTML = result.common_patterns.map(item => `
            <div class="char-item" onclick="chonKyTu('${escapeJs(item.actual)}')">
                <span class="char-label">${escapeHtml(item.pattern)}</span>
                <span class="char-count">xuất hiện ${item.count} lần</span>
            </div>
        `).join('');
    } else {
        tab2.innerHTML = '<div class="no-data">Không tìm thấy chuỗi phổ biến.</div>';
    }

    // Hiện modal
    document.getElementById('modalOverlay').classList.add('show');
}

function chonKyTu(char) {
    document.getElementById('txtFind').value = char;
    dongModal();
    showToast(`✅ Đã điền "${char}" vào ô tìm kiếm`);
}

// ===== Modal =====
function dongModal(event) {
    if (event && event.target !== document.getElementById('modalOverlay')) return;
    document.getElementById('modalOverlay').classList.remove('show');
}

// ===== Tabs =====
function chuyenTab(btn, tabId) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// ===== Utility =====
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function escapeJs(str) {
    return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
}
