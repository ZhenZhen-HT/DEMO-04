document.addEventListener('DOMContentLoaded', () => {
    const urlForm = document.getElementById('urlForm');
    const urlInput = document.getElementById('urlInput');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const resultSection = document.getElementById('resultSection');

    urlForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        fetchData(urlInput.value);
    });
});

async function fetchData(url) {
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const resultSection = document.getElementById('resultSection');
    
    // Reset UI
    loading.style.display = 'block';
    errorMessage.style.display = 'none';
    resultSection.style.display = 'none';

    try {
        const response = await fetch('/api/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, limit: 100 }) // Thay đổi số lượng dòng muốn hiển thị ở đây
        });

        const result = await response.json();

        if (result.success) {
            displayResult(result);
        } else {
            showError(result.error || '获取数据失败');
        }
    } catch (error) {
        showError('网络连接错误');
    } finally {
        loading.style.display = 'none';
    }
}

function displayResult(data) {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';

    document.getElementById('statusCode').textContent = data.status_code;
    document.getElementById('contentType').textContent = data.content_type;
    document.getElementById('dataSize').textContent = (data.size / 1024).toFixed(2) + ' KB';
    document.getElementById('dataType').textContent = data.data_type.toUpperCase();

    // Ẩn tất cả các khu vực nội dung trước
    document.getElementById('csvContent').style.display = 'none';
    document.getElementById('jsonContent').style.display = 'none';
    document.getElementById('textContent').style.display = 'none';

    if (data.data_type === 'csv') {
        renderCSV(data.content);
    } else if (data.data_type === 'json') {
        renderJSON(data.content);
    } else {
        renderText(data.content);
    }
}

function renderCSV(csvData) {
    const container = document.getElementById('csvContent');
    container.style.display = 'block';
    
    document.getElementById('csvColumns').textContent = csvData.column_count;
    document.getElementById('csvRows').textContent = csvData.total_rows;

    const head = document.getElementById('csvHead');
    const body = document.getElementById('csvBody');
    
    head.innerHTML = `<tr>${csvData.headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
    body.innerHTML = csvData.rows.map(row => 
        `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`
    ).join('');

    // Hiển thị thông báo về các dòng còn lại (Yêu cầu của bạn)
    if (csvData.remaining_rows > 0) {
        const remainingMsg = document.createElement('tr');
        remainingMsg.innerHTML = `<td colspan="${csvData.column_count}" style="text-align:center; color:#666; background:#f9f9f9; padding:10px;">
            ... (还有 ${csvData.remaining_rows} 筆数据未显示)
        </td>`;
        body.appendChild(remainingMsg);
    }
}

function renderJSON(json) {
    const container = document.getElementById('jsonContent');
    container.style.display = 'block';
    document.getElementById('jsonDisplay').textContent = JSON.stringify(json, null, 2);
}

function renderText(text) {
    const container = document.getElementById('textContent');
    container.style.display = 'block';
    document.getElementById('textDisplay').textContent = typeof text === 'string' ? text : JSON.stringify(text);
}

function showError(msg) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = msg;
    errorDiv.style.display = 'block';
}

async function loadDefaultData() {
    const response = await fetch('/api/default-data');
    const result = await response.json();
    if (result.success) {
        document.getElementById('urlInput').value = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file";
        displayResult(result);
    }
}