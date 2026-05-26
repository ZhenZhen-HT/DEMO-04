import requests
import json
import io
import zipfile
import csv
from io import TextIOWrapper
import warnings

# 禁用 SSL 验证警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def fetch_and_display_data(url):
    """
    读取 URL 的数据并显示内容
    """
    try:
        print("\n" + "=" * 120)
        print("📡 开始下载数据")
        print("=" * 120)
        print(f"URL: {url}\n")
        
        # 发送 GET 请求
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()  # 如果有错误则抛出异常
        
        print(f"✓ 下载成功")
        print(f"  HTTP 状态码: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"  下载大小: {len(response.content):,} 字节\n")
        
        # 检查是否是 ZIP 文件
        if response.headers.get('content-type') == 'application/zip' or url.endswith('.zip'):
            print("🗂️  检测到 ZIP 文件，正在解压...")
            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                    # 列出 ZIP 中的文件
                    print(f"ZIP 文件中包含的文件:")
                    for file_info in zip_file.filelist:
                        print(f"  - {file_info.filename} ({file_info.file_size:,} 字节)")
                    
                    # 读取每个文件的内容
                    for file_name in zip_file.namelist():
                        print(f"\n--- 文件内容: {file_name} ---")
                        with zip_file.open(file_name) as file:
                            content = file.read()
                            # 尝试解码为文本
                            try:
                                text_content = content.decode('utf-8')
                                print(text_content[:1000])  # 显示前 1000 个字符
                                if len(text_content) > 1000:
                                    print(f"\n... (还有 {len(text_content) - 1000:,} 个字符)")
                            except UnicodeDecodeError:
                                # 如果是二进制文件
                                print(f"(二进制文件，大小: {len(content):,} 字节)")
            except zipfile.BadZipFile:
                print("⚠️  不是有效的 ZIP 文件，尝试以文本形式显示...")
                display_csv_or_text(response.content)
        
        # 检查是否是 CSV 数据
        elif 'csv' in response.headers.get('content-type', ''):
            print("📄 检测到 CSV 数据\n")
            display_csv_or_text(response.content)
        
        # 检查是否是 JSON 数据
        elif 'json' in response.headers.get('content-type', ''):
            print("📋 检测到 JSON 数据:")
            data = response.json()
            print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
        
        # 其他文本类型
        else:
            display_csv_or_text(response.content)
    
    except requests.exceptions.Timeout:
        print("❌ 错误: 请求超时")
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
    except requests.exceptions.RequestException as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"❌ 发生未预期的错误: {e}")
    
    print("=" * 120 + "\n")

def display_csv_or_text(content):
    """
    显示 CSV 或文本数据
    """
    try:
        # 尝试以 UTF-8 BOM 解码 CSV
        text_content = content.decode('utf-8-sig')
        
        # 尝试解析为 CSV
        try:
            csv_file = TextIOWrapper(io.BytesIO(content), encoding='utf-8-sig')
            reader = csv.reader(csv_file)
            rows = list(reader)
            
            if rows:
                display_csv_table(rows)
            else:
                print("❌ CSV 文件为空")
        except:
            # 如果不是 CSV，直接显示文本
            print("📄 显示响应内容 (前 1500 个字符):\n")
            print(text_content[:1500])
            if len(text_content) > 1500:
                print(f"\n... (还有 {len(text_content) - 1500:,} 个字符)")
    except UnicodeDecodeError:
        print("❌ 无法解码为文本，显示前 500 字节的原始数据:")
        print(content[:500])

def display_csv_table(rows):
    """
    以易读的格式显示 CSV 数据（根据字段类型自动调整显示方式）
    """
    if not rows:
        return
    
    headers = rows[0]
    print(f"✓ CSV 文件信息")
    print(f"  列数: {len(headers)}")
    print(f"  数据行数: {len(rows) - 1}\n")
    
    # 显示表头列表
    print(f"表头列表:")
    for i, header in enumerate(headers, 1):
        print(f"  [{i:2d}] {header}")
    
    print(f"\n前 5 行数据详情:")
    print("=" * 120)
    
    # 识别长文本字段
    long_text_fields = {'description', 'link', 'title'}
    
    # 显示前 5 行数据
    max_rows_to_show = min(5, len(rows) - 1)
    for row_idx, row in enumerate(rows[1:max_rows_to_show+1], 1):
        print(f"\n【记录 {row_idx}】")
        print("-" * 120)
        
        for header, value in zip(headers, row):
            # 为长文本字段特殊处理
            if header.lower() in long_text_fields:
                # 长文本字段显示截断版本
                display_value = value[:80] + "..." if len(value) > 80 else value
                print(f"  {header:12s}: {display_value}")
            else:
                # 短文本字段正常显示
                print(f"  {header:12s}: {value}")
        print()
    
    if len(rows) > 6:
        remaining = len(rows) - 6
        print(f"\n... (还有 {remaining} 行数据未显示)")
    
    print("\n" + "=" * 120)

if __name__ == "__main__":
    url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
    fetch_and_display_data(url)
