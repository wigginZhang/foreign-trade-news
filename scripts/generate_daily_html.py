# 生成每日历史日报 HTML - 修复版
import json
import os
import re
from datetime import datetime, timedelta

BASE_DIR = r'D:\workspace\foreign-trade-news'
DATA_DIR = os.path.join(BASE_DIR, 'data')
DAILY_DIR = os.path.join(BASE_DIR, 'daily')

WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
SECTION_ICONS = {
    "data": "📊",
    "geo": "🌏",
    "fx": "💱",
    "logistics": "🚢",
}
IMPACT_LABELS = {
    "high": "高影响",
    "medium": "中影响",
    "low": "低影响"
}

def get_icon(section_id):
    return SECTION_ICONS.get(section_id, "📰")

def get_impact_label(impact):
    return IMPACT_LABELS.get(impact, "低影响")

def extract_sections_from_json(text):
    """从有问题的 JSON 中提取 sections 数据"""
    # 找到 sections 数组
    sections_match = re.search(r'"sections":\s*\[', text)
    if not sections_match:
        return None
    
    sections_start = sections_match.start()
    before_sections = text[:sections_start]
    
    # 找到 broadcast 字段的结束位置
    # broadcast 应该结束于 ", \n    "sections":
    sections_key_match = re.search(r',\s*\n\s*"sections":', text)
    if not sections_key_match:
        return None
    
    # 重新构建有效的 JSON，只包含 sections
    valid_json = '{"sections": [' + text[sections_match.end():]
    
    try:
        data = json.loads(valid_json)
        return data.get('sections', [])
    except:
        return None

def get_date_stats(text):
    """从 JSON 文本提取统计数据"""
    stats = {'totalNews': 0, 'sections': 0}
    
    # 提取日期
    date_match = re.search(r'"dateShort":\s*"([^"]+)"', text)
    if date_match:
        stats['dateShort'] = date_match.group(1)
    
    # 提取生成时间
    time_match = re.search(r'"generatedAt":\s*"([^"]+)"', text)
    if time_match:
        stats['generatedAt'] = time_match.group(1)
    
    return stats

def generate_daily_html(date_str, data, stats):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = WEEKDAYS[date.weekday()]
    month_day = date.strftime("%m月%d日").lstrip('0')
    
    sections = data if isinstance(data, list) else []
    total_news = sum(len(s.get('news', [])) for s in sections)
    
    # 更新统计
    stats['totalNews'] = stats.get('totalNews', total_news)
    stats['sections'] = stats.get('sections', len(sections))
    
    # 构建新闻 HTML
    news_items_html = ""
    for section in sections:
        icon = get_icon(section.get('id', ''))
        news = section.get('news', [])
        
        news_items_html += f'''
        <div class="section">
            <div class="section-header">
                <div class="section-title">
                    <span class="icon">{icon}</span>{section.get('title', '')}
                </div>
                <div class="section-count">{len(news)} 条</div>
            </div>
            <div class="section-content">
'''
        
        for i, news in enumerate(news):
            impact = news.get('impact', 'low')
            impact_class = impact
            impact_text = get_impact_label(impact)
            
            key_facts = news.get('keyFacts', [])
            key_facts_html = ""
            if key_facts:
                facts_list = ''.join(f'<li>{f}</li>' for f in key_facts)
                key_facts_html = f'''
                <div class="key-facts">
                    <div class="key-facts-title">关键事实</div>
                    <ul>{facts_list}</ul>
                </div>
'''
            
            news_url = news.get('url', '#')
            news_title = news.get('title', '')
            news_source = news.get('source', '')
            news_snippet = news.get('snippet', '')
            
            news_items_html += f'''
                <div class="news-item">
                    <div class="news-title">
                        <span class="news-num">{i + 1}.</span>
                        <a href="{news_url}" target="_blank">{news_title}</a>
                    </div>
                    <div class="news-meta">
                        <span class="impact-tag {impact_class}">{impact_text}</span>
                        <span class="news-source">{news_source}</span>
                    </div>
                    <div class="news-snippet">{news_snippet}</div>
                    {key_facts_html}
                    <div class="news-actions">
                        <a href="{news_url}" target="_blank" class="read-more">阅读原文 →</a>
                    </div>
                </div>
'''
        
        news_items_html += '''
            </div>
        </div>
'''
    
    # 导航按钮
    prev_date = (date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    
    has_prev = os.path.exists(os.path.join(DATA_DIR, f"{prev_date}.json"))
    has_next = os.path.exists(os.path.join(DATA_DIR, f"{next_date}.json"))
    
    nav_html = ""
    if has_prev or has_next:
        nav_html = '<div class="nav-buttons">'
        if has_prev:
            prev_md = datetime.strptime(prev_date, "%Y-%m-%d").strftime("%m月%d日").lstrip('0')
            nav_html += f'<a href="{prev_date}.html" class="nav-btn">← {prev_md}</a>'
        nav_html += '<a href="../history.html" class="nav-btn">📅 历史目录</a>'
        if has_next and date_str != "2026-04-16":
            next_md = datetime.strptime(next_date, "%Y-%m-%d").strftime("%m月%d日").lstrip('0')
            nav_html += f'<a href="{next_date}.html" class="nav-btn">{next_md} →</a>'
        nav_html += '</div>'
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{month_day} {weekday} 外贸新闻播报</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-bg: #F4F3EE; --color-bg-secondary: #EDEBE6; --color-bg-tertiary: #E8E6E1;
            --color-accent: #C15F3C; --color-accent-hover: #A84E30;
            --color-text-primary: #2C2825; --color-text-secondary: #6B6560; --color-text-tertiary: #9A9590;
            --color-separator: #DDDBD6; --color-white: #FFFFFF;
            --color-high-impact: #C15F3C; --color-medium-impact: #B8860B; --color-low-impact: #9A9590;
            --font-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
            --font-sans: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
            --space-xs: 4px; --space-sm: 8px; --space-md: 16px; --space-lg: 20px; --space-xl: 32px;
            --radius-sm: 6px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 100px;
            --shadow-card: 0 2px 8px rgba(44,40,37,0.06); --shadow-elevated: 0 4px 16px rgba(44,40,37,0.10);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: var(--font-sans); background: var(--color-bg); color: var(--color-text-primary); line-height: 1.65; -webkit-font-smoothing: antialiased; }}
        header {{ background: var(--color-bg); border-bottom: 1px solid var(--color-separator); padding: 0 var(--space-lg); height: 60px; display: flex; align-items: center; justify-content: space-between; }}
        .header-title {{ font-family: var(--font-serif); font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }}
        .header-link {{ font-size: 14px; color: var(--color-accent); text-decoration: none; display: flex; align-items: center; gap: 6px; }}
        .header-link:hover {{ color: var(--color-accent-hover); }}
        .container {{ max-width: 800px; margin: 0 auto; padding: var(--space-xl); }}
        .day-header {{ text-align: center; margin-bottom: var(--space-xl); }}
        .day-title {{ font-family: var(--font-serif); font-size: 32px; font-weight: 700; color: var(--color-text-primary); margin-bottom: var(--space-sm); }}
        .day-subtitle {{ font-size: 15px; color: var(--color-text-secondary); }}
        .nav-buttons {{ display: flex; gap: var(--space-md); justify-content: center; margin-top: var(--space-lg); flex-wrap: wrap; }}
        .nav-btn {{ background: var(--color-white); border: 1px solid var(--color-separator); border-radius: var(--radius-full); padding: 8px 20px; font-size: 14px; font-weight: 500; color: var(--color-text-primary); text-decoration: none; transition: all 0.2s; display: inline-flex; align-items: center; }}
        .nav-btn:hover {{ background: var(--color-accent); color: var(--color-white); border-color: var(--color-accent); transform: translateY(-2px); }}
        .stats-bar {{ display: flex; gap: var(--space-md); margin-bottom: var(--space-xl); }}
        .stat {{ background: var(--color-white); border-radius: var(--radius-lg); padding: var(--space-lg); flex: 1; text-align: center; box-shadow: var(--shadow-card); }}
        .stat-value {{ font-size: 28px; font-weight: 700; color: var(--color-accent); letter-spacing: -0.02em; line-height: 1.1; }}
        .stat-label {{ font-size: 11px; font-weight: 600; color: var(--color-text-secondary); margin-top: var(--space-xs); text-transform: uppercase; letter-spacing: 0.05em; }}
        .section {{ background: var(--color-white); border-radius: var(--radius-lg); margin-bottom: var(--space-md); box-shadow: var(--shadow-card); overflow: hidden; }}
        .section-header {{ padding: 14px var(--space-lg); background: var(--color-bg-secondary); display: flex; justify-content: space-between; align-items: center; }}
        .section-title {{ font-family: var(--font-serif); font-size: 14px; font-weight: 600; }}
        .section-title .icon {{ margin-right: var(--space-sm); }}
        .section-count {{ font-size: 12px; font-weight: 500; color: var(--color-text-secondary); background: var(--color-separator); padding: 4px 10px; border-radius: var(--radius-sm); }}
        .news-item {{ padding: var(--space-lg); border-bottom: 1px solid var(--color-separator); }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-title {{ font-family: var(--font-serif); font-size: 16px; font-weight: 600; margin-bottom: var(--space-sm); display: flex; gap: 8px; line-height: 1.4; }}
        .news-num {{ color: var(--color-accent); font-weight: 700; flex-shrink: 0; }}
        .news-title a {{ color: var(--color-text-primary); text-decoration: none; }}
        .news-title a:hover {{ color: var(--color-accent); }}
        .news-meta {{ display: flex; gap: var(--space-sm); margin-bottom: 10px; font-size: 13px; color: var(--color-text-secondary); flex-wrap: wrap; align-items: center; }}
        .impact-tag {{ padding: 3px 10px; border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }}
        .impact-tag.high {{ background: rgba(193,95,60,0.12); color: var(--color-high-impact); }}
        .impact-tag.medium {{ background: rgba(184,134,11,0.12); color: var(--color-medium-impact); }}
        .impact-tag.low {{ background: rgba(154,149,144,0.12); color: var(--color-low-impact); }}
        .news-source {{ color: var(--color-text-tertiary); }}
        .news-snippet {{ font-size: 14px; color: var(--color-text-primary); line-height: 1.65; margin-bottom: 14px; }}
        .key-facts {{ background: var(--color-bg); border-left: 3px solid var(--color-accent); border-radius: 0 var(--radius-md) var(--radius-md) 0; padding: 12px 14px; margin-bottom: 14px; }}
        .key-facts-title {{ font-size: 11px; font-weight: 600; color: var(--color-text-secondary); margin-bottom: var(--space-sm); text-transform: uppercase; letter-spacing: 0.05em; }}
        .key-facts ul {{ list-style: none; padding: 0; margin: 0; }}
        .key-facts li {{ font-size: 13px; color: var(--color-text-primary); padding: 3px 0; padding-left: 14px; position: relative; line-height: 1.5; }}
        .key-facts li::before {{ content: '→'; position: absolute; left: 0; color: var(--color-accent); }}
        .news-actions {{ text-align: right; }}
        .read-more {{ font-size: 13px; color: var(--color-accent); text-decoration: none; font-weight: 500; }}
        .read-more:hover {{ color: var(--color-accent-hover); }}
        .footer {{ text-align: center; font-size: 13px; color: var(--color-text-tertiary); padding: var(--space-xl); margin-top: var(--space-xl); border-top: 1px solid var(--color-separator); }}
        .footer a {{ color: var(--color-accent); }}
    </style>
</head>
<body>
    <header>
        <div class="header-title">🐾 外贸新闻播报</div>
        <a href="../index.html" class="header-link">← 返回首页</a>
    </header>
    
    <div class="container">
        <div class="day-header">
            <h1 class="day-title">{month_day} {weekday}</h1>
            <p class="day-subtitle">外贸新闻日报 · {stats.get('totalNews', 0)} 条新闻 · {stats.get('sections', 0)} 个分类</p>
            {nav_html}
        </div>
        
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">{stats.get('totalNews', 0)}</div>
                <div class="stat-label">新闻总数</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats.get('sections', 0)}</div>
                <div class="stat-label">内容分类</div>
            </div>
        </div>
        
        {news_items_html}
    </div>
    
    <div class="footer">
        外贸新闻播报 · <a href="../history.html">历史日报目录</a> · <a href="https://github.com/wigginZhang/foreign-trade-news">GitHub</a>
    </div>
</body>
</html>'''

def main():
    os.makedirs(DAILY_DIR, exist_ok=True)
    
    json_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')], reverse=True)
    
    print(f"Found {len(json_files)} data files")
    print(f"Output dir: {DAILY_DIR}")
    print()
    
    for filename in json_files:
        date_str = filename.replace('.json', '')
        output_file = os.path.join(DAILY_DIR, f"{date_str}.html")
        
        print(f"生成: {output_file}")
        
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        
        # 提取 sections 数据
        sections = extract_sections_from_json(text)
        stats = get_date_stats(text)
        
        if sections is None:
            print(f"  [FAIL] 无法解析 JSON 数据")
            continue
        
        html = generate_daily_html(date_str, sections, stats)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  [OK] 完成 ({len(sections)} 个分类)")
    
    print()
    print("所有历史日报 HTML 生成完成！")

if __name__ == '__main__':
    main()
