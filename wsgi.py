"""
WSGI 入口点 - 用于生产环境部署
适配 Gunicorn 或其他 WSGI 服务器

Usage:
    gunicorn wsgi:app
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
import os
from app import create_app

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run()
