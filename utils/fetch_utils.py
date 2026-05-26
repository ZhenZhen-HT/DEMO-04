"""
数据获取工具模块
"""
import requests
import json
import io
import zipfile
import csv
from io import TextIOWrapper
import warnings

# 禁用 SSL 验证警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def fetch_data(url, display_limit=100):
    """
    读取 URL 的数据并返回格式化的结果
    
    Args:
        url (str): 数据源 URL
        display_limit (int): 限制返回的数据行数
        
    Returns:
        dict: 包含成功状态、状态码、内容类型、大小、数据类型和内容的字典
    """
    try:
        # 发送 GET 请求
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        result = {
            'success': True,
            'status_code': response.status_code,
            'content_type': response.headers.get('content-type', 'N/A'),
            'size': len(response.content),
            'data_type': 'unknown',
            'content': ''
        }
        
        # 检查是否是 ZIP 文件
        if response.headers.get('content-type') == 'application/zip' or url.endswith('.zip'):
            result['data_type'] = 'zip'
            try:
                zip_content = []
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                    for file_name in zip_file.namelist():
                        file_info = {
                            'filename': file_name,
                            'size': [f.file_size for f in zip_file.filelist if f.filename == file_name][0],
                            'content': ''
                        }
                        with zip_file.open(file_name) as file:
                            content = file.read()
                            try:
                                text_content = content.decode('utf-8')
                                file_info['content'] = text_content[:1000]
                                file_info['is_text'] = True
                                file_info['full_size'] = len(text_content)
                            except UnicodeDecodeError:
                                file_info['content'] = '(二进制文件)'
                                file_info['is_text'] = False
                        zip_content.append(file_info)
                result['content'] = zip_content
            except zipfile.BadZipFile:
                result['data_type'] = 'text'
                result['content'] = parse_csv_or_text(response.content, display_limit=display_limit)
        
        # 检查是否是 CSV 数据
        elif 'csv' in response.headers.get('content-type', ''):
            result['data_type'] = 'csv'
            result['content'] = parse_csv_data(response.content, display_limit=display_limit)
        
        # 检查是否是 JSON 数据
        elif 'json' in response.headers.get('content-type', ''):
            result['data_type'] = 'json'
            try:
                data = response.json()
                result['content'] = data
            except:
                result['content'] = response.text[:1000]
        
        # 其他文本类型
        else:
            result['data_type'] = 'text'
            result['content'] = parse_csv_or_text(response.content, display_limit=display_limit)
        
        return result
    
    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': '无法连接到服务器'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': f'发生错误: {str(e)}'}


def parse_csv_data(content, display_limit=100, truncate_long_text=True):
    """
    解析 CSV 数据并返回格式化结果
    
    Args:
        content (bytes): CSV 文件内容
        display_limit (int): 显示上限
        
    Returns:
        dict: 包含表头、数据行、总行数和列数的字典
    """
    try:
        csv_file = TextIOWrapper(io.BytesIO(content), encoding='utf-8-sig')
        reader = csv.reader(csv_file)
        rows = list(reader)
        
        if rows:
            headers = rows[0]
            raw_data_rows = rows[1:min(display_limit + 1, len(rows))]
            
            # 處理長文本截斷 (移植自 fetch_data.py)
            processed_rows = []
            long_text_fields = {'description', 'link', 'title'}
            
            for row in raw_data_rows:
                processed_row = []
                for i, value in enumerate(row):
                    header_name = headers[i].lower() if i < len(headers) else ""
                    if truncate_long_text and header_name in long_text_fields and len(value) > 80:
                        processed_row.append(value[:80] + "...")
                    else:
                        processed_row.append(value)
                processed_rows.append(processed_row)
            
            return {
                'headers': headers,
                'rows': processed_rows,
                'total_rows': len(rows) - 1,
                'column_count': len(headers),
                'remaining_rows': max(0, len(rows) - 1 - display_limit)
            }
        else:
            return {'error': 'CSV 文件为空'}
    except Exception as e:
        return {'error': str(e)}


def parse_csv_or_text(content, display_limit=100):
    """
    尝试解析 CSV 或文本数据
    
    Args:
        content (bytes): 文件内容
        
    Returns:
        dict 或 str: 解析结果或文本内容
    """
    try:
        text_content = content.decode('utf-8-sig')
        try:
            csv_file = TextIOWrapper(io.BytesIO(content), encoding='utf-8-sig')
            reader = csv.reader(csv_file)
            rows = list(reader)
            
            if rows:
                return parse_csv_data(content, display_limit=display_limit)
            else:
                return text_content[:1000]
        except:
            return text_content[:1000]
    except UnicodeDecodeError:
        return '(无法解码为文本)'
