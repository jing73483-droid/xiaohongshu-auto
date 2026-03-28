# API 使用文档

xiaohongshu-mcp REST API 完整文档

---

## 基础信息

**Base URL**: `http://localhost:18060`

**默认端口**: `18060`

**请求格式**: `application/json`

**超时时间**: 120秒

---

## API 端点

### 1. 健康检查

检查MCP服务器运行状态。

**端点**: `GET /health`

**请求示例**:

```bash
curl http://localhost:18060/health
```

**响应示例**:

```json
{
  "status": "ok",
  "timestamp": "2025-03-28T14:30:00Z"
}
```

---

### 2. 发布图文

发布图文笔记到小红书。

**端点**: `POST /api/v1/publish`

**请求头**:

```
Content-Type: application/json
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 文章标题（最多20字符） |
| content | string | 是 | 文章正文（最多1000字符） |
| images | array | 否 | 图片路径数组（1-9张） |
| tags | array | 否 | 标签数组（建议3-5个） |
| is_original | boolean | 否 | 是否原创（默认false） |

**请求示例**:

```bash
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI设计趋势",
    "content": "2025年AI设计行业发展迅猛，设计师使用率达85.8%...",
    "images": [
      "/tmp/image1.jpg",
      "/tmp/image2.jpg"
    ],
    "tags": ["AI应用", "设计趋势", "行业观察"],
    "is_original": false
  }' \
  -m 120
```

**成功响应** (200 OK):

```json
{
  "success": true,
  "message": "发布成功",
  "data": {
    "title": "AI设计趋势",
    "content": "2025年AI设计行业发展迅猛...",
    "images": 2,
    "status": "发布完成"
  }
}
```

**失败响应** (400/500):

```json
{
  "success": false,
  "message": "标题超过字数限制",
  "error": "title too long"
}
```

---

### 3. 查询发布状态

查询最近的发布状态。

**端点**: `GET /api/v1/status`

**请求示例**:

```bash
curl http://localhost:18060/api/v1/status
```

**响应示例**:

```json
{
  "last_publish_time": "2025-03-28T14:35:22Z",
  "total_published": 2,
  "success_rate": "100%"
}
```

---

## Python SDK 示例

### 基础发布

```python
import requests
import json

def publish_article(title, content, images=None, tags=None):
    """发布文章到小红书"""
    url = "http://localhost:18060/api/v1/publish"

    data = {
        "title": title,
        "content": content,
        "images": images or [],
        "tags": tags or [],
        "is_original": False
    }

    response = requests.post(
        url,
        json=data,
        headers={"Content-Type": "application/json"},
        timeout=120
    )

    return response.json()

# 使用示例
result = publish_article(
    title="AI应用趋势",
    content="AI技术正在改变设计行业...",
    images=["/tmp/img1.jpg", "/tmp/img2.jpg"],
    tags=["AI应用", "行业趋势"]
)

print(result)
```

### 批量发布

```python
import json
import time

def batch_publish(articles, interval=30):
    """批量发布文章"""
    results = []

    for i, article in enumerate(articles, 1):
        print(f"发布第{i}篇: {article['title']}")

        result = publish_article(
            title=article['title'],
            content=article['content'],
            images=article.get('images', []),
            tags=article.get('tags', [])
        )

        results.append(result)

        if result.get('success'):
            print(f"✅ 成功")
        else:
            print(f"❌ 失败: {result.get('message')}")

        # 等待间隔
        if i < len(articles):
            print(f"等待{interval}秒...")
            time.sleep(interval)

    return results

# 加载文章数据
with open('woshipm_ai_articles_detailed_v2.json', 'r') as f:
    articles = json.load(f)

# 批量发布前5篇
batch_publish(articles[:5], interval=30)
```

### 错误处理

```python
def publish_with_retry(title, content, max_retries=3):
    """带重试的发布"""
    for attempt in range(max_retries):
        try:
            result = publish_article(title, content)

            if result.get('success'):
                return result
            else:
                print(f"尝试{attempt+1}失败: {result.get('message')}")

        except Exception as e:
            print(f"请求异常: {e}")

        if attempt < max_retries - 1:
            time.sleep(5)  # 等待5秒后重试

    return {"success": False, "message": "重试次数用尽"}
```

---

## Node.js SDK 示例

```javascript
const axios = require('axios');

async function publishArticle(title, content, images = [], tags = []) {
    try {
        const response = await axios.post(
            'http://localhost:18060/api/v1/publish',
            {
                title,
                content,
                images,
                tags,
                is_original: false
            },
            {
                headers: { 'Content-Type': 'application/json' },
                timeout: 120000
            }
        );

        return response.data;
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

// 使用示例
publishArticle(
    'AI应用趋势',
    'AI技术正在改变设计行业...',
    ['/tmp/img1.jpg', '/tmp/img2.jpg'],
    ['AI应用', '行业趋势']
).then(result => {
    console.log(result);
});
```

---

## cURL 示例集合

### 简单发布

```bash
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{"title":"测试标题","content":"测试内容"}' \
  -m 120
```

### 带图片发布

```bash
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI趋势",
    "content": "完整内容...",
    "images": ["/tmp/img1.jpg", "/tmp/img2.jpg"]
  }' \
  -m 120
```

### 带标签发布

```bash
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI趋势",
    "content": "完整内容...",
    "tags": ["AI", "科技", "趋势"]
  }' \
  -m 120
```

---

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查参数格式和内容 |
| 401 | 未登录或登录过期 | 重新登录小红书 |
| 413 | 内容过长 | 缩短标题或正文 |
| 429 | 请求过于频繁 | 降低发布频率 |
| 500 | 服务器内部错误 | 查看服务器日志 |
| 503 | 服务不可用 | 检查MCP服务器状态 |

---

## 限制说明

### 内容限制

- **标题**: 最多20个字符
- **正文**: 最多1000个字符
- **图片**: 1-9张
- **标签**: 建议3-5个

### 频率限制

- **发布间隔**: 建议30秒以上
- **每日上限**: 约50篇
- **登录限制**: 不能多端同时登录

### 性能指标

- **发布耗时**: 40-60秒
- **成功率**: 99%+
- **并发**: 不支持（顺序发布）

---

## 最佳实践

### 1. 内容优化

- 标题简洁有力（15-20字）
- 正文排版清晰（使用换行和标点）
- 添加相关标签（提高曝光）
- 配图高清美观（1080x1350）

### 2. 发布策略

- 选择最佳时间段发布
- 保持稳定的发布频率
- 控制每日发布数量
- 监控发布效果数据

### 3. 安全建议

- 定期更新登录状态
- 不要频繁操作
- 遵守平台规则
- 保护账号安全

---

## 调试技巧

### 查看请求日志

```bash
# 实时查看MCP服务器日志
tail -f xiaohongshu-mcp/logs/server.log
```

### 测试连接

```bash
# 测试服务器是否运行
curl -v http://localhost:18060/health

# 测试发布接口
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{"title":"测试","content":"测试内容"}' \
  -v
```

### 抓包分析

```bash
# 使用tcpdump抓包
sudo tcpdump -i lo0 -A 'tcp port 18060'
```

---

## 更新日志

### v1.0.0 (2025-03-28)

- 首次发布
- 支持图文发布
- 支持批量操作

---

**需要更多帮助？查看 [README.md](./README.md) 或提交 Issue。**
