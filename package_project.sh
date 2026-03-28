#!/bin/bash

echo "========================================"
echo "小红书自动化系统 - 项目打包脚本"
echo "========================================"
echo ""

# 设置变量
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="xiaohongshu_automation"
BASE_DIR="/Users/huangjing/Documents/CC"

# 创建打包目录
PACKAGE_DIR="${BASE_DIR}/packages_${TIMESTAMP}"
mkdir -p "${PACKAGE_DIR}"

echo "📦 打包目录: ${PACKAGE_DIR}"
echo ""

# ========== 包1: 完整项目包 ==========
echo "📦 创建包1: 完整项目包..."
FULL_PACKAGE="${PACKAGE_DIR}/${PROJECT_NAME}_full_${TIMESTAMP}"
mkdir -p "${FULL_PACKAGE}"

# 复制核心文件
cp README.md "${FULL_PACKAGE}/" 2>/dev/null
cp QUICKSTART.md "${FULL_PACKAGE}/" 2>/dev/null
cp API_DOCS.md "${FULL_PACKAGE}/" 2>/dev/null
cp setup_all.sh "${FULL_PACKAGE}/" 2>/dev/null

# 复制Python脚本
cp woshipm_ai_crawler_v2.py "${FULL_PACKAGE}/" 2>/dev/null
cp auto_publish_rest.py "${FULL_PACKAGE}/" 2>/dev/null
cp create_professional_images.py "${FULL_PACKAGE}/" 2>/dev/null
cp batch_publish.py "${FULL_PACKAGE}/" 2>/dev/null

# 复制数据文件
cp woshipm_ai_articles_detailed_v2.json "${FULL_PACKAGE}/" 2>/dev/null
cp woshipm_ai_articles_detailed_v2.csv "${FULL_PACKAGE}/" 2>/dev/null

# 压缩
cd "${PACKAGE_DIR}"
zip -r "${PROJECT_NAME}_full_${TIMESTAMP}.zip" "${PROJECT_NAME}_full_${TIMESTAMP}" > /dev/null
FULL_SIZE=$(du -h "${PROJECT_NAME}_full_${TIMESTAMP}.zip" | cut -f1)
echo "✅ 完整项目包创建成功: ${FULL_SIZE}"
rm -rf "${PROJECT_NAME}_full_${TIMESTAMP}"

# ========== 包2: 仅文档包 ==========
echo ""
echo "📦 创建包2: 仅文档包..."
DOCS_PACKAGE="${PACKAGE_DIR}/${PROJECT_NAME}_docs_${TIMESTAMP}"
mkdir -p "${DOCS_PACKAGE}"

cp README.md "${DOCS_PACKAGE}/" 2>/dev/null
cp QUICKSTART.md "${DOCS_PACKAGE}/" 2>/dev/null
cp API_DOCS.md "${DOCS_PACKAGE}/" 2>/dev/null

cd "${PACKAGE_DIR}"
zip -r "${PROJECT_NAME}_docs_${TIMESTAMP}.zip" "${PROJECT_NAME}_docs_${TIMESTAMP}" > /dev/null
DOCS_SIZE=$(du -h "${PROJECT_NAME}_docs_${TIMESTAMP}.zip" | cut -f1)
echo "✅ 文档包创建成功: ${DOCS_SIZE}"
rm -rf "${PROJECT_NAME}_docs_${TIMESTAMP}"

# ========== 包3: 数据包 ==========
echo ""
echo "📦 创建包3: 数据包（文章+PDF）..."
DATA_PACKAGE="${PACKAGE_DIR}/${PROJECT_NAME}_data_${TIMESTAMP}"
mkdir -p "${DATA_PACKAGE}"

cp woshipm_ai_articles_detailed_v2.json "${DATA_PACKAGE}/" 2>/dev/null
cp woshipm_ai_articles_detailed_v2.csv "${DATA_PACKAGE}/" 2>/dev/null

# 复制PDF目录
if [ -d "articles_pdf" ]; then
    cp -r "${BASE_DIR}/articles_pdf" "${DATA_PACKAGE}/" 2>/dev/null
fi

cd "${PACKAGE_DIR}"
zip -r "${PROJECT_NAME}_data_${TIMESTAMP}.zip" "${PROJECT_NAME}_data_${TIMESTAMP}" > /dev/null
DATA_SIZE=$(du -h "${PROJECT_NAME}_data_${TIMESTAMP}.zip" | cut -f1)
echo "✅ 数据包创建成功: ${DATA_SIZE}"
rm -rf "${PROJECT_NAME}_data_${TIMESTAMP}"

# ========== 创建分享说明 ==========
echo ""
echo "📝 创建分享说明..."
cat > "${PACKAGE_DIR}/README_分享说明.txt" << 'EOF'
======================================
小红书自动化系统 - 分享包说明
======================================

本项目包含三个压缩包：

1. [项目名]_full_[时间].zip
   - 完整项目包
   - 包含所有代码、脚本、文档
   - 适合技术人员使用
   - 需要按照文档配置环境

2. [项目名]_docs_[时间].zip
   - 仅文档包
   - README.md（主文档）
   - QUICKSTART.md（快速开始）
   - API_DOCS.md（API文档）
   - 适合查阅使用方法

3. [项目名]_data_[时间].zip
   - 数据包
   - 24篇AI文章（JSON/CSV格式）
   - 24篇PDF文章
   - 适合内容查看和分析

======================================
使用方法
======================================

【技术人员】：
1. 解压 full 包
2. 阅读 README.md
3. 运行 ./setup_all.sh 安装
4. 按照文档操作

【普通用户】：
1. 解压 docs 包查看文档
2. 解压 data 包查看文章内容
3. 如需使用自动化功能，联系技术人员

======================================
系统要求
======================================

- 操作系统: macOS (已测试) 或 Linux
- Python: 3.9+
- 网络连接
- 小红书账号（实名认证）

======================================
功能特性
======================================

✅ 自动爬取AI相关文章
✅ 100%自动化发布到小红书
✅ 专业配图生成
✅ 批量发布支持
✅ REST API接口

======================================
注意事项
======================================

⚠️ 遵守小红书平台规则
⚠️ 控制发布频率（建议30秒间隔）
⚠️ 注意每日发布上限（约50篇）
⚠️ 不要多端同时登录网页版

======================================
技术支持
======================================

查看 README.md 获取详细文档
查看 QUICKSTART.md 快速上手
查看 API_DOCS.md 了解API

======================================
版本信息
======================================

版本: v1.0.0
日期: 2025-03-28
作者: Claude Code

EOF

echo "✅ 分享说明创建成功"

# 统计信息
echo ""
echo "========================================"
echo "🎉 打包完成！"
echo "========================================"
echo ""
echo "📊 打包统计："
echo "   完整项目包: ${FULL_SIZE}"
echo "   文档包: ${DOCS_SIZE}"
echo "   数据包: ${DATA_SIZE}"
echo ""
echo "📁 打包位置:"
echo "   ${PACKAGE_DIR}"
echo ""
echo "📤 分享方式:"
echo "   1. 将压缩包发送给对方"
echo "   2. 对方解压后阅读 README_分享说明.txt"
echo "   3. 技术人员运行 setup_all.sh 安装"
echo ""
echo "💡 提示:"
echo "   - full包适合技术人员"
echo "   - docs包适合查阅文档"
echo "   - data包适合查看内容"
echo ""
