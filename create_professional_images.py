#!/usr/bin/env python3
"""
生成专业小红书配图
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_professional_cover(title, subtitle, output_path, size=(1080, 1350)):
    """创建专业封面图"""
    # 创建图片
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)

    # 渐变背景
    for i in range(size[1]):
        progress = i / size[1]
        r = int(255 - progress * 50)
        g = int(240 - progress * 40)
        b = int(245 - progress * 30)
        draw.rectangle([(0, i), (size[0], i+1)], fill=(r, g, b))

    # 加载字体（使用系统字体）
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 80)
        subtitle_font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 50)
        tag_font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tag_font = ImageFont.load_default()

    # 绘制标题（多行）
    wrapped_title = textwrap.wrap(title, width=12)
    y_offset = 300
    for line in wrapped_title[:3]:  # 最多3行
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        draw.text((x, y_offset), line, fill='#1a1a1a', font=title_font)
        y_offset += 120

    # 绘制副标题
    if subtitle:
        wrapped_sub = textwrap.wrap(subtitle, width=20)
        for line in wrapped_sub[:2]:
            bbox = draw.textbbox((0, 0), line, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            draw.text((x, y_offset), line, fill='#666666', font=subtitle_font)
            y_offset += 80

    # 绘制装饰线
    draw.rectangle([(100, size[1]-300), (size[0]-100, size[1]-296)], fill='#4a90e2')

    # 绘制标签
    tags = ['#AI资讯', '#科技前沿', '#OpenAI']
    tag_y = size[1] - 220
    tag_x_start = 150
    for tag in tags:
        draw.text((tag_x_start, tag_y), tag, fill='#4a90e2', font=tag_font)
        tag_x_start += 280

    # 保存
    img.save(output_path, quality=95)
    print(f"✅ 封面图已生成: {output_path}")
    return output_path


def create_content_image(content_lines, output_path, size=(1080, 1350)):
    """创建内容图"""
    img = Image.new('RGB', size, color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    try:
        content_font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 45)
    except:
        content_font = ImageFont.load_default()

    # 绘制标题区域
    draw.rectangle([(0, 0), (size[0], 200)], fill='#4a90e2')

    try:
        header_font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 60)
    except:
        header_font = ImageFont.load_default()

    header_text = "核心要点"
    bbox = draw.textbbox((0, 0), header_text, font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((size[0] - text_width) // 2, 70), header_text, fill='white', font=header_font)

    # 绘制内容
    y_offset = 280
    for i, line in enumerate(content_lines[:8], 1):  # 最多8行
        # 编号
        draw.ellipse([(80, y_offset-10), (130, y_offset+40)], fill='#4a90e2')
        num_bbox = draw.textbbox((0, 0), str(i), font=content_font)
        num_width = num_bbox[2] - num_bbox[0]
        draw.text((105 - num_width//2, y_offset), str(i), fill='white', font=content_font)

        # 内容文字
        wrapped = textwrap.wrap(line, width=18)
        for wrapped_line in wrapped[:2]:
            draw.text((180, y_offset), wrapped_line, fill='#1a1a1a', font=content_font)
            y_offset += 70

        y_offset += 50

    # 保存
    img.save(output_path, quality=95)
    print(f"✅ 内容图已生成: {output_path}")
    return output_path


if __name__ == '__main__':
    # 生成封面图
    create_professional_cover(
        title="OpenAI Sora登顶美区榜首",
        subtitle="AI短视频社交新时代",
        output_path="/tmp/xhs_cover.jpg"
    )

    # 生成内容图
    content_lines = [
        "上线10天登顶App Store",
        "支持文字和图片生成视频",
        "1080p高清分辨率",
        "单个视频最长20秒",
        "类似Instagram的社区",
        "探索板块可浏览他人作品",
        "或成AI短视频领域TikTok",
        "引领短视频创作新潮流"
    ]
    create_content_image(content_lines, "/tmp/xhs_content.jpg")

    print("\n✅ 所有图片生成完成！")
