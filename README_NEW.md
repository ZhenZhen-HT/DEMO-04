# 数据获取和展示工具 - Flask Web 应用

一个专业的 Flask 网站应用，用于获取、解析和展示不同格式的数据（CSV、JSON、ZIP、文本）。

## 项目结构（重构后）

```
DEMO-04/
├── app.py                 # Flask 应用主文件（含应用工厂）
├── config.py             # 配置管理文件
├── requirements.txt      # Python 依赖列表
├── README.md            # 原始文档
│
├── utils/               # 工具模块
│   ├── __init__.py
│   └── fetch_utils.py   # 数据获取工具函数
│
├── templates/           # HTML 模板
│   └── index.html       # 主页模板
│
├── static/              # 静态文件
│   ├── style.css        # 样式表
│   └── script.js        # JavaScript 脚本
│
└── run.bat / run.sh     # 启动脚本
```

## 新的架构特性

### 1. **应用工厂模式**
使用 `create_app()` 函数创建和配置应用，支持多环境配置切换。

```python
from app import create_app

app = create_app('production')  # 或 'development', 'testing'
```

### 2. **配置管理 (`config.py`)**
- `Config`: 基础配置
- `DevelopmentConfig`: 开发环境配置
- `ProductionConfig`: 生产环境配置
- `TestingConfig`: 测试环境配置

### 3. **工具模块分离 (`utils/fetch_utils.py`)**
所有数据处理逻辑独立分离：
- `fetch_data()` - 获取并解析数据
- `parse_csv_data()` - 解析 CSV 格式
- `parse_csv_or_text()` - 自动检测 CSV 或文本

### 4. **更好的错误处理**
- 404 错误处理器
- 500 错误处理器
- 统一的 JSON 响应格式

### 5. **代码组织**
- 路由注册与应用创建分离
- 配置与应用逻辑分离
- 便于单元测试

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用

**Windows:**
```bash
python app.py
```

**或使用启动脚本:**
```bash
run.bat          # Windows
./run.sh         # Linux/Mac
```

### 3. 访问应用
```
http://localhost:5000
```

## API 文档

### 1. 主页
- **URL**: `/`
- **方法**: `GET`
- **响应**: HTML 页面

### 2. 获取数据 API
- **URL**: `/api/fetch`
- **方法**: `POST`
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
    "size": 1024,
    "data_type": "csv",
    "content": {
      "headers": ["col1", "col2"],
      "rows": [["val1", "val2"]],
      "total_rows": 100,
      "column_count": 2
    }
  }
  ```

### 3. 默认数据 API
- **URL**: `/api/default-data`
- **方法**: `GET`
- **响应**: 同上

## 支持的数据格式

| 格式 | 检测方式 | 处理方式 |
|------|---------|---------|
| CSV | Content-Type 包含 "csv" | 解析并显示表格 |
| JSON | Content-Type 包含 "json" | 格式化显示 |
| ZIP | Content-Type 为 "application/zip" | 解压并列出文件 |
| 文本 | 其他类型 | 显示原始文本 |

## 开发指南

### 添加新路由

在 `app.py` 的 `register_routes()` 函数中添加：

```python
@app.route('/api/new-endpoint')
def new_endpoint():
    return jsonify({'data': 'value'})
```

### 添加新工具函数

在 `utils/fetch_utils.py` 中添加函数：

```python
def new_utility_function(param):
    """函数文档"""
    pass
```

然后在 `app.py` 中导入：

```python
from utils.fetch_utils import new_utility_function
```

### 改变环境配置

编辑 `config.py` 的相应配置类：

```python
class DevelopmentConfig(Config):
    DEBUG = True
    JSON_AS_ASCII = False
```

## 功能特性

✅ **多格式支持**
- ZIP 文件自动解压
- CSV 数据表格展示
- JSON 数据格式化
- 文本数据展示

✅ **用户界面**
- 现代化 Web UI
- 实时加载反馈
- 响应式设计
- 详细信息展示

✅ **错误处理**
- 网络错误提示
- 超时处理
- 数据解析异常捕获

## 故障排除

### 连接超时
修改 `utils/fetch_utils.py` 中的超时参数：
```python
response = requests.get(url, timeout=30, verify=False)  # 增加到 30 秒
```

### SSL 证书错误
应用已禁用 SSL 验证。生产环境应设置 `verify=True`。

### 中文显示问题
配置中已设置 `JSON_AS_ASCII = False`，确保中文正确显示。

## 从旧版本迁移

如果从原始版本升级：
1. 备份旧版本
2. 使用新的 `config.py` 和 `utils/` 目录
3. 更新 `app.py`
4. 安装新依赖：`pip install -r requirements.txt`

## 许可证

MIT
