#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章转PDF工具
将爬取的JSON文章数据转换为PDF文件
"""

import json
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re


class ArticleToPDFConverter:
    """文章转PDF转换器"""

    def __init__(self, output_dir="articles_pdf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 注册中文字体（使用系统字体）
        self.setup_fonts()

        # 设置样式
        self.styles = self.setup_styles()

    def setup_fonts(self):
        """设置中文字体"""
        try:
            # macOS 系统字体
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',  # macOS 苹方字体
                '/System/Library/Fonts/STHeiti Light.ttc',  # 华文黑体
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux
                'C:\\Windows\\Fonts\\msyh.ttc',  # Windows 微软雅黑
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('Chinese', font_path))
                    print(f"✓ 成功加载字体: {font_path}")
                    return

            print("⚠️  未找到系统中文字体，将使用默认字体（可能无法正确显示中文）")
        except Exception as e:
            print(f"⚠️  字体加载失败: {e}")

    def setup_styles(self):
        """设置文档样式"""
        styles = getSampleStyleSheet()

        # 标题样式
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontName='Chinese',
            fontSize=18,
            textColor='#333333',
            spaceAfter=12,
            alignment=TA_LEFT,
            leading=24
        ))

        # 元信息样式
        styles.add(ParagraphStyle(
            name='MetaInfo',
            parent=styles['Normal'],
            fontName='Chinese',
            fontSize=10,
            textColor='#666666',
            spaceAfter=6,
            leading=14
        ))

        # 正文样式
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName='Chinese',
            fontSize=11,
            textColor='#333333',
            spaceAfter=8,
            leading=18,
            firstLineIndent=0
        ))

        # 标签样式
        styles.add(ParagraphStyle(
            name='Tags',
            parent=styles['Normal'],
            fontName='Chinese',
            fontSize=9,
            textColor='#0066cc',
            spaceAfter=6,
            leading=14
        ))

        return styles

    def clean_text(self, text):
        """清理文本内容"""
        if not text:
            return ""

        # 移除多余的空白和换行
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # 转义XML特殊字符
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        return text.strip()

    def create_pdf(self, article, filename):
        """创建单个文章的PDF"""
        pdf_path = self.output_dir / filename

        # 创建PDF文档
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []

        # 标题
        title = self.clean_text(article.get('title', '无标题'))
        # 移除网站后缀
        title = re.sub(r'\s*[–-]\s*人人都是产品经理\s*$', '', title)
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))

        # 元信息
        author = article.get('author', '未知作者')
        publish_date = article.get('publish_date', '未知日期')
        meta_text = f"<b>作者：</b>{self.clean_text(author)} | <b>发布日期：</b>{publish_date}"
        story.append(Paragraph(meta_text, self.styles['MetaInfo']))

        # URL
        url = article.get('url', '')
        if url:
            url_text = f"<b>原文链接：</b>{url}"
            story.append(Paragraph(url_text, self.styles['MetaInfo']))

        # 标签
        tags = article.get('tags', [])
        if tags:
            tags_text = f"<b>标签：</b>{' | '.join(tags)}"
            story.append(Paragraph(tags_text, self.styles['Tags']))

        story.append(Spacer(1, 0.3 * inch))

        # 正文内容
        content = article.get('content', '无内容')

        # 分段处理内容
        paragraphs = content.split('\n')
        for para in paragraphs:
            para = self.clean_text(para)
            if para:
                # 限制段落长度，避免过长
                if len(para) > 2000:
                    # 将长段落分割
                    chunks = [para[i:i+2000] for i in range(0, len(para), 2000)]
                    for chunk in chunks:
                        story.append(Paragraph(chunk, self.styles['CustomBody']))
                else:
                    story.append(Paragraph(para, self.styles['CustomBody']))

        # 生成PDF
        try:
            doc.build(story)
            return True
        except Exception as e:
            print(f"✗ 生成PDF失败 {filename}: {e}")
            return False

    def convert_all(self, json_file):
        """转换所有文章"""
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        print(f"\n开始转换 {len(articles)} 篇文章为PDF...\n")

        success_count = 0
        failed_count = 0

        for idx, article in enumerate(articles, 1):
            title = article.get('title', f'article_{idx}')
            # 清理文件名
            safe_title = re.sub(r'[^\w\s-]', '', title)[:50]
            safe_title = re.sub(r'[-\s]+', '_', safe_title)

            filename = f"{idx:02d}_{safe_title}.pdf"

            print(f"[{idx}/{len(articles)}] 正在转换: {title[:40]}...")

            if self.create_pdf(article, filename):
                print(f"    ✓ 成功: {filename}")
                success_count += 1
            else:
                print(f"    ✗ 失败: {filename}")
                failed_count += 1

        print(f"\n" + "="*60)
        print(f"转换完成！")
        print(f"成功: {success_count} 篇")
        print(f"失败: {failed_count} 篇")
        print(f"PDF文件保存在: {self.output_dir.absolute()}")
        print("="*60 + "\n")


def main():
    """主函数"""
    print("="*60)
    print("文章转PDF工具")
    print("="*60)

    # 查找JSON文件
    json_files = [
        'woshipm_ai_articles_detailed_v2.json',
        'woshipm_ai_articles_list_v2.json',
        'test_articles_v2.json'
    ]

    json_file = None
    for f in json_files:
        if os.path.exists(f):
            json_file = f
            break

    if not json_file:
        print("✗ 未找到JSON文件，请确保以下文件之一存在：")
        for f in json_files:
            print(f"  - {f}")
        return

    print(f"✓ 找到数据文件: {json_file}\n")

    # 创建转换器并执行转换
    converter = ArticleToPDFConverter(output_dir="articles_pdf")
    converter.convert_all(json_file)


if __name__ == "__main__":
    main()
