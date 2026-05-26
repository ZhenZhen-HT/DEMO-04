#!/bin/bash

# Linux/Mac 快速启动脚本

echo ""
echo "==============================================="
echo "  数据获取和展示工具 - Flask Web 应用"
echo "==============================================="
echo ""

# 检查 Python 是否已安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3，请先安装 Python 3.8+"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 检查和安装依赖..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 启动应用
echo ""
echo "✅ 所有准备完成！"
echo ""
echo "🚀 正在启动 Flask 应用..."
echo ""
echo "================================"
echo "📱 应用地址: http://localhost:5000"
echo "📱 按 Ctrl+C 停止应用"
echo "================================"
echo ""

python app.py
