"""
单元测试示例
"""
import unittest
import json
from app import create_app
from utils.fetch_utils import parse_csv_data
import io


class FlaskAppTestCase(unittest.TestCase):
    """Flask 应用测试"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """测试后清理"""
        self.app_context.pop()
    
    def test_index_page(self):
        """测试主页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)
    
    def test_fetch_api_no_url(self):
        """测试 API - 无 URL"""
        response = self.client.post('/api/fetch',
                                   data=json.dumps({'url': ''}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_404_error(self):
        """测试 404 错误"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


class UtilsTestCase(unittest.TestCase):
    """工具函数测试"""
    
    def test_parse_csv_data(self):
        """测试 CSV 解析"""
        csv_content = b'name,age\nJohn,30\nJane,25'
        result = parse_csv_data(csv_content)
        
        self.assertEqual(result['headers'], ['name', 'age'])
        self.assertEqual(result['total_rows'], 2)
        self.assertEqual(result['column_count'], 2)


if __name__ == '__main__':
    unittest.main()
