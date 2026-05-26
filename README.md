# 数据获取和展示工具 - Flask Web 应用

这是一个 Flask Web 应用，用于从远程 URL 获取和展示各种格式的数据（支持 ZIP、CSV、JSON 和文本格式）。

## 功能特性

✅ **多格式支持**
- ZIP 文件自动解压显示
- CSV 数据表格化展示
- JSON 数据格式化显示
- 文本数据内容展示

✅ **用户友好的界面**
- 现代化的 Web UI
- 实时数据加载反馈
- 响应式设计（支持移动设备）
- 详细的数据信息展示

✅ **错误处理**
- 网络错误提示
- 超时处理
- 数据解析异常捕获

## 项目结构

```
DEMO-04/
├── app.py                 # Flask 主应用程序
├── fetch_data.py          # 原始命令行脚本（已改写为 app.py）
├── requirements.txt       # Python 依赖列表
├── README.md             # 本文件
├── templates/
│   └── index.html        # 主页 HTML 模板
└── static/
    ├── style.css         # 样式表
    └── script.js         # 前端 JavaScript
```

## 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

## 使用说明

### 方法 1: 通过 Web 界面
1. 打开浏览器访问 `http://localhost:5000`
2. 在输入框中输入数据 URL
3. 点击"📥 获取数据"按钮
4. 应用会自动识别数据格式并展示结果

### 方法 2: 使用默认 URL
1. 点击"使用默认 URL"按钮
2. 系统会加载新竹市政府开放的数据

### 方法 3: 使用 API
发送 POST 请求到 `/api/fetch`：

```bash
curl -X POST http://localhost:5000/api/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-data-url.com/data.csv"}'
```

## API 端点

### 获取数据
- **URL**: `/api/fetch`
- **方法**: POST
- **请求体**:
```json
{
  "url": "https://example.com/data.csv"
}
```
- **响应**:
```json
{
  "success": true,
  "status_code": 200,
  "content_type": "text/csv",
  "size": 12345,
  "data_type": "csv",
  "content": {
    "headers": ["列1", "列2", "列3"],
    "rows": [[...], [...], ...],
    "total_rows": 100,
    "column_count": 3
  }
}
```

### 加载默认数据
- **URL**: `/api/default-data`
- **方法**: GET
- **响应**: 同上述格式

## 支持的数据格式

### CSV 格式
- 自动识别 UTF-8 和 UTF-8 BOM 编码
- 显示列数和数据行数
- 表格化展示前 5 行数据

### JSON 格式
- 自动解析和格式化显示
- 支持嵌套 JSON 结构

### ZIP 格式
- 自动解压并列出所有文件
- 显示文件大小
- 显示文本文件内容（前 1000 字符）

### 文本格式
- 尝试识别是否为 CSV 格式
- 显示前 1000-1500 个字符

## 数据信息展示

对于每个获取的数据源，应用会显示：
- ✓ HTTP 状态码
- ✓ Content-Type
- ✓ 数据大小（自动转换为 B/KB/MB 等）
- ✓ 识别的数据类型

## 错误处理

应用会处理以下错误情况：
- 网络连接失败
- 请求超时（默认 10 秒）
- SSL 验证失败（已禁用警告）
- 数据解析异常

## 配置选项

在 `app.py` 中可以修改的配置：
- `debug=True`: 调试模式（生产环境应设置为 False）
- `host='0.0.0.0'`: 监听地址（0.0.0.0 允许外部访问）
- `port=5000`: 服务器端口

## 技术栈

- **后端**: Flask 2.3.3
- **前端**: HTML5, CSS3, Vanilla JavaScript
- **依赖包**: requests (HTTP 请求), Werkzeug (WSGI 工具)

## 常见问题

### Q: 如何修改服务器端口？
A: 在 `app.py` 最后一行修改 `port=5000` 为其他值。

### Q: 如何在生产环境使用？
A: 
1. 设置 `debug=False`
2. 使用生产级 WSGI 服务器（如 Gunicorn）
3. 配置 SSL 证书
4. 设置适当的错误日志记录

### Q: 如何处理大文件？
A: 当前实现将整个文件加载到内存。对于大文件，可以修改为流式处理。

### Q: 如何添加身份验证？
A: 可以使用 Flask-Login 或 Flask-JWT-Extended 等扩展。

## 许可证

MIT License

## 作者

数据获取工具开发团队

---

**更新时间**: 2024 年
**Flask 版本**: 2.3.3+
**Python 版本**: 3.8+
