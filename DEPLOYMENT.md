# 部署指南

本指南说明如何将 Flask 应用部署到生产环境。

## 生产环境部署

### 1. 使用 Gunicorn（推荐）

#### 安装 Gunicorn
```bash
pip install gunicorn
```

#### 运行应用
```bash
# 基础用法
gunicorn wsgi:app

# 指定工作进程和绑定地址
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# 使用端口 8000
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

参数说明：
- `-w`: 工作进程数（通常为 CPU 核心数 × 2 + 1）
- `-b`: 绑定地址和端口

### 2. 使用 uWSGI

#### 安装 uWSGI
```bash
pip install uwsgi
```

#### 运行应用
```bash
uwsgi --http :5000 --wsgi-file wsgi.py --callable app
```

### 3. 使用 Nginx 反向代理

#### Nginx 配置示例

创建 `/etc/nginx/sites-available/flask-app`：

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/DEMO-04/static;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. 环境变量配置

创建 `.env` 文件（生产环境）：

```bash
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

加载环境变量：
```bash
export $(cat .env | xargs)
```

## Docker 部署

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY . .

# 安装 Gunicorn
RUN pip install gunicorn

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t flask-data-fetcher .

# 运行容器
docker run -p 5000:5000 flask-data-fetcher

# 指定环境变量
docker run -p 5000:5000 -e FLASK_ENV=production flask-data-fetcher
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    volumes:
      - ./static:/app/static
      - ./templates:/app/templates
```

运行：
```bash
docker-compose up -d
```

## 性能优化

### 1. 缓存配置

在 `app.py` 中添加：
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/fetch', methods=['POST'])
@cache.cached(timeout=300, query_string=True)
def api_fetch():
    # ...
```

### 2. 连接池

在 `utils/fetch_utils.py` 中：
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 3. 日志配置

```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 监控和维护

### 1. 应用状态检查

添加健康检查端点：
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

### 2. 日志管理

```bash
# 查看最新日志
tail -f logs/app.log

# 日志轮转（使用 logrotate）
```

### 3. 自动重启（使用 Supervisor）

创建 `/etc/supervisor/conf.d/flask-app.conf`：

```ini
[program:flask-app]
command=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
directory=/path/to/DEMO-04
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/flask-app.log
```

## 安全建议

1. **关闭调试模式**
   ```python
   FLASK_DEBUG = False
   ```

2. **使用 HTTPS**
   - 配置 SSL 证书
   - 更新 Nginx 配置

3. **CORS 配置**
   ```python
   from flask_cors import CORS
   CORS(app, resources={r"/api/*": {"origins": "yourdomain.com"}})
   ```

4. **速率限制**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/fetch', methods=['POST'])
   @limiter.limit("10/minute")
   def api_fetch():
       # ...
   ```

5. **输入验证**
   - 验证 URL 格式
   - 限制请求大小

## 常见问题

### 端口被占用
```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### 权限问题
```bash
sudo chown -R www-data:www-data /path/to/DEMO-04
sudo chmod -R 755 /path/to/DEMO-04
```

### SSL 证书配置
```bash
# 使用 Let's Encrypt (Certbot)
sudo certbot certonly --webroot -w /var/www/html -d yourdomain.com
```

## 测试部署

运行测试：
```bash
python -m pytest test_app.py -v
```

性能测试：
```bash
ab -n 1000 -c 10 http://localhost:5000/
```

## 监控工具

推荐使用：
- **PM2**: Node.js 进程管理器（也支持 Python）
- **Supervisor**: 进程监控工具
- **New Relic**: 应用性能监控
- **Sentry**: 错误追踪

## 备份和恢复

```bash
# 定期备份应用目录
tar -czf backup-$(date +%Y%m%d).tar.gz /path/to/DEMO-04/

# 恢复
tar -xzf backup-20240101.tar.gz
```
