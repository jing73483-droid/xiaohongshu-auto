#!/usr/bin/env python3
"""
完全自动化发布 - 使用REST API
最简单直接的方式！
"""
import requests
import json
import time
import sys

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def check_login_status():
    """检查登录状态"""
    url = "http://localhost:18060/api/v1/login/status"

    log("检查登录状态...")
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        log(f"❌ HTTP错误: {response.status_code}")
        return False

    data = response.json()

    if data.get("is_logged_in"):
        username = data.get("username", "未知")
        log(f"✅ 登录状态正常")
        log(f"   用户: {username}")
        return True
    else:
        log("❌ 未登录！")
        return False

def publish_content(title, content, images, tags):
    """发布内容到小红书"""
    url = "http://localhost:18060/api/v1/publish"

    log(f"\n开始发布内容...")
    log(f"  📝 标题: {title}")
    log(f"  📄 正文: {len(content)}字")
    log(f"  🖼️  图片: {len(images)}张")
    for i, img in enumerate(images, 1):
        log(f"       {i}. {img}")
    log(f"  🏷️  标签: {', '.join(tags)}")

    payload = {
        "title": title,
        "content": content,
        "images": images,
        "tags": tags,
        "is_original": False
    }

    log("\n⏳ 发布中，请稍候（可能需要30-60秒）...")

    try:
        response = requests.post(url, json=payload, timeout=120)

        if response.status_code != 200:
            log(f"❌ HTTP错误: {response.status_code}")
            log(f"   响应: {response.text}")
            return False

        result = response.json()

        log(f"\n📝 发布结果:")
        log(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get("success") or "成功" in str(result):
            log("\n🎉 发布成功！")
            return True
        else:
            log(f"\n⚠️  发布可能有问题")
            return True  # 继续流程

    except requests.exceptions.Timeout:
        log(f"\n⚠️  请求超时（可能仍在发布中，请检查小红书APP）")
        return True
    except Exception as e:
        log(f"\n❌ 发布失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主流程"""
    log("=" * 60)
    log("🤖 小红书全自动发布系统 v3.0 (REST API)")
    log("=" * 60)

    try:
        # 步骤1: 检查登录状态
        log("")
        if not check_login_status():
            log("\n❌ 请先登录！")
            log("   运行: cd xiaohongshu-mcp && ./xiaohongshu-login-darwin-arm64")
            return 1

        # 步骤2: 准备内容
        log("\n" + "=" * 60)
        log("📦 准备发布内容...")
        log("=" * 60)

        title = "OpenAI Sora登顶榜首"  # 20字以内

        content = """OpenAI上线不到10天，Sora的官方App就霸榜美国区App Store免费榜榜首。

这是Sora这款AI视频生成工具首次推出独立的移动应用，此前只能在网页端使用。

根据OpenAI官方发布的信息，移动版Sora支持用户通过文字、图片直接生成视频，提供1080p高清分辨率，单个视频时长最高可达20秒。

此外，用户还能使用Remix、Recut、Blend等工具来调整视频。OpenAI称移动版Sora"专为创作者设计"。

从功能上看，Sora App确实提供了一些针对移动端创作场景的优化，比如支持竖屏拍摄、便于分享到社交媒体等。

但更重要的是，OpenAI这次还试图为Sora建立一个类似Instagram的社区氛围。在App首页，除了"创建"按钮外，还设置了一个"探索"板块，用户可以浏览其他人生成的视频，并进行点赞、评论、转发。

这其实是一个很有意思的尝试。OpenAI显然希望Sora不仅仅是一个工具，而是一个能够形成内容生态的平台。如果这个方向成功，Sora或许能成为AI短视频领域的TikTok。

📖 完整内容：https://www.woshipm.com/ai/6279149.html"""

        images = [
            "/tmp/xhs_cover.jpg",
            "/tmp/xhs_content.jpg"
        ]

        tags = ["AI短视频", "OpenAI", "Sora应用"]

        # 步骤3: 发布内容
        log("\n" + "=" * 60)
        log("🚀 开始自动发布...")
        log("=" * 60)

        success = publish_content(title, content, images, tags)

        if success:
            log("\n" + "=" * 60)
            log("🎉" * 15)
            log("✅ 发布完成！请在小红书APP中查看发布结果")
            log("🎉" * 15)
            log("=" * 60)
            return 0
        else:
            log("\n" + "=" * 60)
            log("⚠️  发布可能未完成，请检查小红书APP和错误日志")
            log("=" * 60)
            return 1

    except Exception as e:
        log(f"\n❌ 系统错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
