#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人人都是产品经理 - AI文章爬虫 V2
使用 /ai 分类页面进行爬取
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
import os
import re


class WoShiPMCrawlerV2:
    def __init__(self):
        self.base_url = "https://www.woshipm.com"
        self.ai_url = f"{self.base_url}/ai"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        self.articles = []

    def fetch_page(self, url, retry=3):
        """获取页面内容"""
        # 第一次请求时先访问主页获取cookie
        if not self.session.cookies:
            try:
                print("初始化会话...")
                self.session.get(self.base_url, headers=self.headers, timeout=15)
                time.sleep(1)
            except Exception as e:
                print(f"初始化会话失败: {e}")

        for i in range(retry):
            try:
                # 更新Referer
                headers = self.headers.copy()
                headers['Referer'] = self.base_url

                response = self.session.get(url, headers=headers, timeout=15, allow_redirects=True)
                response.encoding = 'utf-8'

                if response.status_code == 200:
                    return response.text
                elif response.status_code == 403:
                    print(f"请求被拒绝 (403)，尝试 {i+1}/{retry}")
                elif response.status_code == 404:
                    print(f"页面不存在 (404): {url}")
                    return None
                else:
                    print(f"请求失败，状态码: {response.status_code}")

            except requests.exceptions.Timeout:
                print(f"请求超时 (尝试 {i+1}/{retry})")
            except Exception as e:
                print(f"请求出错 (尝试 {i+1}/{retry}): {e}")

            if i < retry - 1:
                time.sleep(3)

        return None

    def parse_article_list(self, html):
        """解析文章列表页面"""
        soup = BeautifulSoup(html, 'html.parser')
        articles = []

        # 匹配文章URL：支持完整URL和相对路径
        # 格式: https://www.woshipm.com/分类/数字ID.html 或 /分类/数字ID.html
        pattern = re.compile(r'(https://www\.woshipm\.com)?/\w+/\d+\.html')

        # 查找所有包含文章链接的<a>标签
        all_links = soup.find_all('a', href=pattern)

        for link in all_links:
            href = link.get('href', '')

            # 标准化URL
            article_url = href if href.startswith('http') else self.base_url + href

            # 提取文章ID
            article_id_match = re.search(r'/(\d+)\.html', href)
            if not article_id_match:
                continue

            article_id = article_id_match.group(1)

            # 获取标题：优先使用<a>标签的文本内容
            title = link.get_text(strip=True)

            # 如果<a>标签内没有文本，尝试从父级元素找
            if not title or len(title) < 5:
                parent = link.find_parent('div', class_='category-cardItem')
                if parent:
                    title_div = parent.find('div', class_='title')
                    if title_div:
                        title = title_div.get_text(strip=True)

            # 过滤掉无效标题和重复项
            if title and len(title) > 8:
                # 避免重复
                if not any(a['url'] == article_url for a in articles):
                    articles.append({
                        'title': title,
                        'url': article_url,
                        'article_id': article_id
                    })

        return articles

    def parse_article_detail(self, html, article_url):
        """解析文章详情页面"""
        soup = BeautifulSoup(html, 'html.parser')

        detail = {
            'url': article_url,
            'title': '',
            'author': '',
            'publish_date': '',
            'content': '',
            'tags': [],
            'category': ''
        }

        # 提取标题
        title_selectors = [
            soup.find('h1', class_=re.compile('title|heading')),
            soup.find('h1'),
            soup.find('meta', property='og:title')
        ]
        for selector in title_selectors:
            if selector:
                if selector.name == 'meta':
                    detail['title'] = selector.get('content', '')
                else:
                    detail['title'] = selector.get_text(strip=True)
                if detail['title']:
                    break

        # 提取作者
        author_selectors = [
            soup.find('a', class_=re.compile('author')),
            soup.find('span', class_=re.compile('author')),
            soup.find('meta', {'name': 'author'})
        ]
        for selector in author_selectors:
            if selector:
                if selector.name == 'meta':
                    detail['author'] = selector.get('content', '')
                else:
                    detail['author'] = selector.get_text(strip=True)
                if detail['author']:
                    break

        # 提取发布日期
        date_selectors = [
            soup.find('time'),
            soup.find('span', class_=re.compile('date|time')),
            soup.find('meta', property='article:published_time')
        ]
        for selector in date_selectors:
            if selector:
                if selector.name == 'meta':
                    detail['publish_date'] = selector.get('content', '')
                elif selector.name == 'time':
                    detail['publish_date'] = selector.get('datetime', '') or selector.get_text(strip=True)
                else:
                    detail['publish_date'] = selector.get_text(strip=True)
                if detail['publish_date']:
                    break

        # 提取正文内容
        content_selectors = [
            soup.find('article'),
            soup.find('div', class_=re.compile('content|post-content|article')),
            soup.find('div', id=re.compile('content|article'))
        ]
        for selector in content_selectors:
            if selector:
                # 移除脚本和样式
                for script in selector(['script', 'style', 'nav', 'aside', 'footer']):
                    script.decompose()
                content = selector.get_text(separator='\n', strip=True)
                if len(content) > 100:  # 确保是有效内容
                    detail['content'] = content
                    break

        # 提取标签
        tag_links = soup.find_all('a', href=re.compile(r'/tag/'))
        detail['tags'] = list(set([tag.get_text(strip=True) for tag in tag_links if tag.get_text(strip=True)]))

        # 提取分类
        category_match = re.search(r'/(\w+)/\d+\.html', article_url)
        if category_match:
            detail['category'] = category_match.group(1)

        return detail

    def crawl_list_pages(self, max_pages=5):
        """爬取文章列表（多页）"""
        print(f"开始爬取AI分类文章列表，最多 {max_pages} 页...")

        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.ai_url
            else:
                url = f"{self.ai_url}/page/{page}"

            print(f"\n正在爬取第 {page} 页: {url}")
            html = self.fetch_page(url)

            if html:
                articles = self.parse_article_list(html)
                if articles:
                    print(f"发现 {len(articles)} 篇文章")
                    self.articles.extend(articles)
                else:
                    print("未找到文章，可能已到最后一页")
                    break

                # 避免请求过快
                time.sleep(2)
            else:
                print(f"第 {page} 页获取失败")
                break

        # 去重
        seen = set()
        unique_articles = []
        for article in self.articles:
            if article['url'] not in seen:
                seen.add(article['url'])
                unique_articles.append(article)

        self.articles = unique_articles
        print(f"\n共找到 {len(self.articles)} 篇不重复的AI文章")
        return self.articles

    def crawl_article_details(self, articles=None, max_articles=None):
        """爬取文章详情"""
        if articles is None:
            articles = self.articles

        if max_articles:
            articles = articles[:max_articles]

        print(f"\n开始爬取 {len(articles)} 篇文章的详情...")
        detailed_articles = []

        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] 正在爬取: {article['title'][:50]}...")
            html = self.fetch_page(article['url'])

            if html:
                detail = self.parse_article_detail(html, article['url'])
                if detail['content']:
                    detailed_articles.append(detail)
                    print(f"  ✓ 成功获取，内容长度: {len(detail['content'])} 字符")
                else:
                    print(f"  ⚠ 内容为空，跳过")
            else:
                print(f"  ✗ 获取失败")

            # 避免请求过快
            time.sleep(2)

        return detailed_articles

    def save_to_json(self, data, filename='woshipm_ai_articles.json'):
        """保存为JSON文件"""
        filepath = os.path.join('/Users/huangjing/Documents/CC', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到: {filepath}")
        return filepath

    def save_to_csv(self, data, filename='woshipm_ai_articles.csv'):
        """保存为CSV文件"""
        if not data:
            print("没有数据可保存")
            return

        filepath = os.path.join('/Users/huangjing/Documents/CC', filename)

        # 确定字段
        fieldnames = list(data[0].keys())

        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                # 处理列表字段
                row = item.copy()
                for key, value in row.items():
                    if isinstance(value, list):
                        row[key] = ', '.join(value)
                writer.writerow(row)

        print(f"已保存到: {filepath}")
        return filepath


def main():
    """主函数"""
    print("=" * 60)
    print("人人都是产品经理 - AI文章爬虫 V2")
    print("=" * 60)

    crawler = WoShiPMCrawlerV2()

    # 1. 爬取文章列表（前3页）
    articles = crawler.crawl_list_pages(max_pages=3)

    if not articles:
        print("\n未能获取文章列表，请检查网络连接或网站是否可访问")
        return

    # 保存文章列表
    crawler.save_to_json(articles, 'woshipm_ai_articles_list_v2.json')
    crawler.save_to_csv(articles, 'woshipm_ai_articles_list_v2.csv')

    # 2. 询问是否爬取详情
    print("\n" + "=" * 60)
    print("文章列表已保存！")
    print(f"共找到 {len(articles)} 篇文章")
    print("=" * 60)

    choice = input("\n是否爬取文章详细内容？\n  输入数字 (如 5) 爬取前N篇\n  输入 'all' 爬取所有\n  其他键跳过\n> ").strip().lower()

    if choice == 'all':
        detailed = crawler.crawl_article_details()
        if detailed:
            crawler.save_to_json(detailed, 'woshipm_ai_articles_detailed_v2.json')
            crawler.save_to_csv(detailed, 'woshipm_ai_articles_detailed_v2.csv')
    elif choice.isdigit():
        num = int(choice)
        detailed = crawler.crawl_article_details(max_articles=num)
        if detailed:
            crawler.save_to_json(detailed, 'woshipm_ai_articles_detailed_v2.json')
            crawler.save_to_csv(detailed, 'woshipm_ai_articles_detailed_v2.csv')
    else:
        print("\n跳过详情爬取")

    print("\n" + "=" * 60)
    print("爬取完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
