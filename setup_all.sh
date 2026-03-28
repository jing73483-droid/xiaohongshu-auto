#!/bin/bash

echo "========================================"
echo "小红书自动化系统 - 一键安装脚本"
echo "========================================"
echo ""

# 检查Python版本
echo "📋 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 未安装，请先安装Python 3.9+"
    exit 1
fi

# 检查网络连接
echo ""
echo "📡 检查网络连接..."
curl -I https://github.com -m 5 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  警告：网络连接可能有问题"
fi

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install requests beautifulsoup4 pillow lxml > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "⚠️  Python依赖安装可能有问题，但继续执行"
fi

# 检查xiaohongshu-mcp目录
echo ""
echo "🔍 检查xiaohongshu-mcp..."
if [ ! -d "xiaohongshu-mcp" ]; then
    echo "❌ xiaohongshu-mcp目录不存在"
    echo "正在克隆项目..."
    git clone https://github.com/xpzouying/xiaohongshu-mcp.git
fi

cd xiaohongshu-mcp

# 下载预编译文件
echo ""
echo "⬇️  下载MCP工具..."

if [ ! -f "xiaohongshu-mcp-darwin-arm64" ]; then
    echo "下载MCP服务器..."
    curl -L -o xiaohongshu-mcp-darwin-arm64 \
        https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-arm64
    chmod +x xiaohongshu-mcp-darwin-arm64
    echo "✅ MCP服务器下载完成"
else
    echo "✅ MCP服务器已存在"
fi

if [ ! -f "xiaohongshu-login-darwin-arm64" ]; then
    echo "下载登录工具..."
    curl -L -o xiaohongshu-login-darwin-arm64 \
        https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-login-darwin-arm64
    chmod +x xiaohongshu-login-darwin-arm64
    echo "✅ 登录工具下载完成"
else
    echo "✅ 登录工具已存在"
fi

cd ..

# 创建必要目录
echo ""
echo "📁 创建目录结构..."
mkdir -p articles_pdf
mkdir -p logs
echo "✅ 目录创建完成"

# 验证安装
echo ""
echo "🔍 验证安装..."
echo ""

if [ -f "xiaohongshu-mcp/xiaohongshu-mcp-darwin-arm64" ]; then
    echo "✅ MCP服务器: 已安装"
else
    echo "❌ MCP服务器: 未找到"
fi

if [ -f "xiaohongshu-mcp/xiaohongshu-login-darwin-arm64" ]; then
    echo "✅ 登录工具: 已安装"
else
    echo "❌ 登录工具: 未找到"
fi

if [ -f "woshipm_ai_articles_detailed_v2.json" ]; then
    echo "✅ 文章数据: 已存在"
else
    echo "⚠️  文章数据: 未找到（需要运行爬虫）"
fi

# 完成
echo ""
echo "========================================"
echo "🎉 安装完成！"
echo "========================================"
echo ""
echo "📋 下一步操作："
echo ""
echo "1. 登录小红书："
echo "   cd xiaohongshu-mcp"
echo "   ./xiaohongshu-login-darwin-arm64"
echo ""
echo "2. 启动MCP服务器："
echo "   cd xiaohongshu-mcp"
echo "   ./xiaohongshu-mcp-darwin-arm64 -port :18060 &"
echo ""
echo "3. 发布文章："
echo "   cd /Users/huangjing/Documents/CC"
echo "   python3 auto_publish_rest.py"
echo ""
echo "📖 查看完整文档: cat README.md"
echo ""
