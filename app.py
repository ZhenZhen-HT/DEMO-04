"""
Flask 应用主文件
数据获取和展示工具
"""
import os
from flask import Flask, render_template, request, jsonify
from config import config
from utils.fetch_utils import fetch_data


def create_app(config_name=None):
    """
    应用工厂函数 - 创建和配置 Flask 应用
    
    Args:
        config_name (str): 配置名称 (development, production, testing)
        
    Returns:
        Flask: 配置好的 Flask 应用实例
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # 注册路由
    register_routes(app)
    
    return app


def register_routes(app):
    """
    注册应用路由
    
    Args:
        app (Flask): Flask 应用实例
    """
    
    @app.route('/')
    def index():
        """显示首页"""
        default_url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
        return render_template('index.html', default_url=default_url)
    
    @app.route('/api/fetch', methods=['POST'])
    def api_fetch():
        """API 端点：获取和处理数据"""
        data = request.get_json()
        url = data.get('url', '').strip()
        limit = data.get('limit', 100)  # Thay đổi mặc định lên 100 dòng
        
        if not url:
            return jsonify({'success': False, 'error': '请输入 URL'}), 400
        
        result = fetch_data(url, display_limit=limit)
        return jsonify(result)
    
    @app.route('/api/default-data', methods=['GET'])
    def api_default_data():
        """API 端点：获取默认数据"""
        default_url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
        result = fetch_data(default_url)
        return jsonify(result)
    
    @app.errorhandler(404)
    def page_not_found(error):
        """处理 404 错误"""
        return jsonify({'success': False, 'error': '页面不存在'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """处理 500 错误"""
        return jsonify({'success': False, 'error': '服务器内部错误'}), 500


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
