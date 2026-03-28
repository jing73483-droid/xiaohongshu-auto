# 快速开始指南

10分钟快速上手小红书自动化发布系统。

---

## 步骤1：环境准备（2分钟）

### 检查系统要求

```bash
# 检查Python版本（需要3.9+）
python3 --version

# 检查网络连接
curl -I https://www.xiaohongshu.com
```

---

## 步骤2：一键安装（3分钟）

```bash
cd /Users/huangjing/Documents/CC
chmod +x setup_all.sh
./setup_all.sh
```

安装脚本会自动完成：
- ✅ 下载xiaohongshu-mcp工具
- ✅ 安装Python依赖包
- ✅ 配置目录结构
- ✅ 验证安装

---

## 步骤3：登录小红书（2分钟）

```bash
cd xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

**操作步骤**：
1. 等待浏览器自动弹出
2. 使用小红书APP扫描二维码
3. 确认登录
4. 看到"登录成功"提示后关闭浏览器

---

## 步骤4：启动服务（1分钟）

```bash
cd xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64 -port :18060 &
```

**验证服务**：

```bash
# 检查服务是否运行
lsof -i:18060

# 测试API
curl http://localhost:18060/health
```

---

## 步骤5：发布第一篇文章（2分钟）

### 方式A：使用自动发布脚本（推荐）

```bash
cd /Users/huangjing/Documents/CC
python3 auto_publish_rest.py
```

### 方式B：使用REST API

```bash
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI应用趋势洞察",
    "content": "2025年AI技术发展迅猛...",
    "images": ["/tmp/xhs_cover.jpg"],
    "tags": ["AI应用", "行业观察"],
    "is_original": false
  }' \
  -m 120
```

---

## 完成！🎉

现在您已经：
- ✅ 安装并配置了所有工具
- ✅ 登录了小红书账号
- ✅ 启动了MCP服务器
- ✅ 成功发布了第一篇文章

---

## 下一步

### 批量发布更多文章

```bash
python3 batch_publish.py --start 1 --end 5 --interval 30
```

### 自定义发布内容

编辑 `woshipm_ai_articles_detailed_v2.json` 文件，修改文章内容。

### 查看详细文档

- 完整功能：查看 [README.md](./README.md)
- API文档：查看 [API_DOCS.md](./API_DOCS.md)

---

## 常见问题速查

### 服务器无法启动？

```bash
# 停止旧进程
lsof -ti:18060 | xargs kill

# 重新启动
cd xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64 -port :18060 &
```

### 登录过期？

```bash
cd xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

### 发布失败？

1. 检查内容长度（标题≤20字，正文≤1000字）
2. 检查登录状态
3. 检查网络连接
4. 查看错误日志

---

**开始您的小红书自动化之旅吧！** 🚀
