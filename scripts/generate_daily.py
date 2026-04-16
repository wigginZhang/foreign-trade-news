#!/usr/bin/env python3
"""
Generate static daily HTML pages from JSON data.
Handles files with problematic broadcast fields by extracting only sections.
"""
import json, os, re
from datetime import datetime, timedelta

BASE = r'D:\workspace\foreign-trade-news'
DATA = os.path.join(BASE, 'data')
DAILY = os.path.join(BASE, 'daily')
WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

CAT = {
    'tariff':    {'icon': '📦', 'label': '关税与贸易政策'},
    'data':      {'icon': '📊', 'label': '数据快递'},
    'geo':       {'icon': '🌏', 'label': '地缘动态'},
    'fx':        {'icon': '💱', 'label': '汇率风云'},
    'logistics': {'icon': '🚢', 'label': '物流纵览'},
    'all':       {'icon': '📌', 'label': '全部新闻'},
}
CAT_ORDER = ['tariff', 'data', 'geo', 'fx', 'logistics', 'all']

CSS = """
:root {
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
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font-sans); background: var(--color-bg); color: var(--color-text-primary); line-height: 1.65; -webkit-font-smoothing: antialiased; }
header { background: var(--color-bg); border-bottom: 1px solid var(--color-separator); padding: 0 var(--space-lg); height: 60px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
.header-title { font-family: var(--font-serif); font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.header-link { font-size: 14px; color: var(--color-accent); text-decoration: none; display: flex; align-items: center; gap: 6px; }
.header-link:hover { color: var(--color-accent-hover); }
.container { max-width: 800px; margin: 0 auto; padding: var(--space-xl); }
.day-header { text-align: center; margin-bottom: var(--space-xl); }
.day-title { font-family: var(--font-serif); font-size: 32px; font-weight: 700; color: var(--color-text-primary); margin-bottom: var(--space-sm); }
.day-subtitle { font-size: 15px; color: var(--color-text-secondary); margin-bottom: var(--space-md); }
.nav-buttons { display: flex; gap: var(--space-md); justify-content: center; margin-top: var(--space-lg); flex-wrap: wrap; }
.nav-btn { background: var(--color-white); border: 1px solid var(--color-separator); border-radius: var(--radius-full); padding: 8px 20px; font-size: 14px; font-weight: 500; color: var(--color-text-primary); text-decoration: none; transition: all 0.2s; display: inline-flex; align-items: center; }
.nav-btn:hover { background: var(--color-accent); color: var(--color-white); border-color: var(--color-accent); transform: translateY(-2px); }
.stats-bar { display: flex; gap: var(--space-md); margin-bottom: var(--space-xl); }
.stat { background: var(--color-white); border-radius: var(--radius-lg); padding: var(--space-lg); flex: 1; text-align: center; box-shadow: var(--shadow-card); }
.stat-value { font-size: 28px; font-weight: 700; color: var(--color-accent); letter-spacing: -0.02em; line-height: 1.1; }
.stat-label { font-size: 11px; font-weight: 600; color: var(--color-text-secondary); margin-top: var(--space-xs); text-transform: uppercase; letter-spacing: 0.05em; }
.section { background: var(--color-white); border-radius: var(--radius-lg); margin-bottom: var(--space-md); box-shadow: var(--shadow-card); overflow: hidden; }
.section-header { padding: 14px var(--space-lg); background: var(--color-bg-secondary); display: flex; justify-content: space-between; align-items: center; }
.section-title { font-family: var(--font-serif); font-size: 14px; font-weight: 600; }
.section-title .icon { margin-right: var(--space-sm); }
.section-count { font-size: 12px; font-weight: 500; color: var(--color-text-secondary); background: var(--color-separator); padding: 4px 10px; border-radius: var(--radius-sm); }
.news-item { padding: var(--space-lg); border-bottom: 1px solid var(--color-separator); }
.news-item:last-child { border-bottom: none; }
.news-title { font-family: var(--font-serif); font-size: 16px; font-weight: 600; margin-bottom: var(--space-sm); display: flex; gap: 8px; line-height: 1.4; }
.news-num { color: var(--color-accent); font-weight: 700; flex-shrink: 0; }
.news-title a { color: var(--color-text-primary); text-decoration: none; }
.news-title a:hover { color: var(--color-accent); }
.news-meta { display: flex; gap: var(--space-sm); margin-bottom: 10px; font-size: 13px; color: var(--color-text-secondary); flex-wrap: wrap; align-items: center; }
.impact-tag { padding: 3px 10px; border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }
.impact-tag.high { background: rgba(193,95,60,0.12); color: var(--color-high-impact); }
.impact-tag.medium { background: rgba(184,134,11,0.12); color: var(--color-medium-impact); }
.impact-tag.low { background: rgba(154,149,144,0.12); color: var(--color-low-impact); }
.news-source { color: var(--color-text-tertiary); }
.news-snippet { font-size: 14px; color: var(--color-text-primary); line-height: 1.65; margin-bottom: 14px; }
.key-facts { background: var(--color-bg); border-left: 3px solid var(--color-accent); border-radius: 0 var(--radius-md) var(--radius-md) 0; padding: 12px 14px; margin-bottom: 14px; }
.key-facts-title { font-size: 11px; font-weight: 600; color: var(--color-text-secondary); margin-bottom: var(--space-sm); text-transform: uppercase; letter-spacing: 0.05em; }
.key-facts ul { list-style: none; padding: 0; margin: 0; }
.key-facts li { font-size: 13px; color: var(--color-text-primary); padding: 3px 0; padding-left: 14px; position: relative; line-height: 1.5; }
.key-facts li::before { content: '→'; position: absolute; left: 0; color: var(--color-accent); }
.news-actions { text-align: right; }
.read-more { font-size: 13px; color: var(--color-accent); text-decoration: none; font-weight: 500; }
.read-more:hover { color: var(--color-accent-hover); }
.footer { text-align: center; font-size: 13px; color: var(--color-text-tertiary); padding: var(--space-xl); margin-top: var(--space-xl); border-top: 1px solid var(--color-separator); }
.footer a { color: var(--color-accent); }
.history-section { background: var(--color-white); border-radius: var(--radius-lg); margin-top: var(--space-xl); padding: 25px; box-shadow: var(--shadow-card); }
.history-section h2 { font-family: var(--font-serif); font-size: 16px; font-weight: 600; color: var(--color-text-primary); border-bottom: 1px solid var(--color-separator); padding-bottom: 12px; margin-bottom: 16px; }
.history-list { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 8px; }
.history-list li { margin: 0; }
.history-list a { display: inline-block; padding: 6px 14px; background: var(--color-bg); border-radius: var(--radius-full); font-size: 13px; font-weight: 500; color: var(--color-text-primary); text-decoration: none; transition: all 0.2s; }
.history-list a:hover { background: var(--color-accent); color: var(--color-white); transform: translateY(-1px); }
"""

def h(text):
    if not text: return ''
    return (str(text)
        .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        .replace('"', '&quot;').replace("'", '&#39;'))

def esc(text):
    """Escape text for HTML."""
    return h(text)

def load_json(path):
    """Load JSON, handling broadcast field encoding issues."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()
    
    # Fix common JSON issues from encoding problems
    # Replace literal \n sequences (not escaped) inside strings with \n
    # This is a heuristic: find patterns like "text\nmore" and escape them
    
    # Try standard JSON parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    
    # Try to fix unescaped newlines in string values
    # Pattern: find "field": "...\n..." where \n is literal backslash-n
    # We do this by finding the sections array and parsing just that
    try:
        # Extract just the sections portion
        m = re.search(r'"sections":\s*\[', raw)
        if m:
            start = m.start()
            rest = raw[start + len('"sections": '):]
            
            # Find the closing bracket
            depth = 0
            end = 0
            for i, c in enumerate(rest):
                if c == '[': depth += 1
                elif c == ']': 
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            
            sections_text = rest[:end]
            
            # Now parse just the sections
            sections_json = '[' + sections_text + ']'
            
            # Replace literal \n with escaped \\n within string values
            # This regex finds string values and fixes unescaped newlines
            def fix_string_newlines(m):
                s = m.group(0)
                # s is like "field": "value"
                # Fix literal \n inside the value
                s = re.sub(r'(?<!\\)\\n', '\\\\n', s)
                s = re.sub(r'(?<!\\)\\r', '\\\\r', s)
                return s
            
            # We need to be more careful. The issue is \n (backslash + n) inside strings
            # Let's try a simpler fix: just escape all \n in the sections text
            fixed = sections_text.replace('\\n', '\\\\n').replace('\\r', '\\\\r')
            sections_json = '[' + fixed + ']'
            
            sections = json.loads(sections_json)
            
            # Also extract dateShort and generatedAt
            date_match = re.search(r'"dateShort":\s*"([^"]+)"', raw)
            time_match = re.search(r'"generatedAt":\s*"([^"]+)"', raw)
            stats_match = re.search(r'"totalNews":\s*(\d+)', raw)
            sections_count_match = re.search(r'"sections":\s*(\d+)', raw)
            
            return {
                'dateShort': date_match.group(1) if date_match else 'unknown',
                'generatedAt': time_match.group(1) if time_match else 'unknown',
                'sections': sections,
                'stats': {
                    'totalNews': int(stats_match.group(1)) if stats_match else sum(len(s.get('news',[])) for s in sections),
                    'sections': int(sections_count_match.group(1)) if sections_count_match else len(sections)
                }
            }
    except Exception as e:
        print(f'  [WARN] Fallback parse failed: {e}')
    
    raise ValueError(f'Cannot parse {path}')

def get_sections(data):
    if 'sections' in data and data['sections']:
        return data['sections']
    if 'news' in data and data['news']:
        return [{'id': 'all', 'title': '全部新闻', 'news': data['news']}]
    return []

def friendly_date(ds):
    d = datetime.strptime(ds, '%Y-%m-%d')
    return f'{d.month}月{d.day}日', WEEKDAYS[d.weekday()]

def render_news_item(item, num):
    impact = item.get('impact', 'medium')
    impact_labels = {'high': '高影响', 'medium': '中影响', 'low': '低影响'}
    key_facts = item.get('keyFacts') or []
    kf_html = ''
    if key_facts:
        kf_html = f'<div class="key-facts"><div class="key-facts-title">关键事实</div><ul>{"".join(f"<li>{esc(e)}</li>" for e in key_facts)}</ul></div>'
    url = item.get('url', '')
    link_html = f'<a href="{esc(url)}" target="_blank" class="read-more">阅读原文 →</a>' if url else ''
    return f'''<div class="news-item">
        <div class="news-title"><span class="news-num">{num}.</span><a href="{esc(url)}" target="_blank">{esc(item.get("title",""))}</a></div>
        <div class="news-meta"><span class="impact-tag {impact}">{impact_labels.get(impact,"中影响")}</span><span class="news-source">{esc(item.get("source",""))}</span></div>
        <div class="news-snippet">{esc(item.get("snippet",""))}</div>
        {kf_html}
        <div class="news-actions">{link_html}</div>
    </div>'''

def generate_daily_html(ds, data, all_dates):
    month_day, weekday = friendly_date(ds)
    sections = get_sections(data)
    all_news = [n for s in sections for n in s.get('news', [])]
    high_count = sum(1 for n in all_news if n.get('impact') == 'high')

    sections_sorted = sorted(sections, key=lambda s: (CAT_ORDER.index(s['id']) if s['id'] in CAT_ORDER else 99, 0))
    sections_html = ''
    for sec in sections_sorted:
        cat = CAT.get(sec['id'], {'icon': '📌', 'label': sec.get('title', sec['id'])})
        news = sec.get('news', [])
        news_html = ''.join(render_news_item(n, i+1) for i, n in enumerate(news))
        sections_html += f'<div class="section"><div class="section-header"><div class="section-title"><span class="icon">{cat["icon"]}</span>{cat["label"]}</div><div class="section-count">{len(news)} 条</div></div><div>{news_html}</div></div>'

    # Navigation
    nav_html = '<div class="nav-buttons">'
    prev_ds = next((d for i, d in enumerate(all_dates) if d == ds and i > 0), None)
    next_ds = next((d for i, d in enumerate(all_dates) if d == ds and i < len(all_dates) - 1), None)
    
    if prev_ds:
        pm, pd = friendly_date(prev_ds)
        nav_html += f'<a href="{prev_ds}.html" class="nav-btn">← {pm}{pd}</a>'
    nav_html += '<a href="../index.html" class="nav-btn">📅 返回目录</a>'
    if next_ds and ds != '2026-04-16':
        nm, nd = friendly_date(next_ds)
        nav_html += f'<a href="{next_ds}.html" class="nav-btn">{nm}{nd} →</a>'
    nav_html += '</div>'

    # History list (all dates up to this one)
    past = [d for d in all_dates if d <= ds]
    history_items = ''.join(f'<li><a href="https://wigginzhang.github.io/foreign-trade-news/daily/{d}.html" target="_blank">{d}</a></li>' for d in reversed(past))

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{month_day} {weekday} 外贸新闻播报</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>{CSS}</style>
</head>
<body>
    <header>
        <div class="header-title">🐾 外贸新闻播报</div>
        <a href="../index.html" class="header-link">← 返回首页</a>
    </header>
    <div class="container">
        <div class="day-header">
            <h1 class="day-title">{month_day} {weekday}</h1>
            <p class="day-subtitle">{ds} · {data.get("generatedAt","")} 生成 · {len(all_news)} 条新闻 · {len(sections)} 个分类</p>
            {nav_html}
        </div>
        <div class="stats-bar">
            <div class="stat"><div class="stat-value">{len(all_news)}</div><div class="stat-label">新闻总数</div></div>
            <div class="stat"><div class="stat-value">{len(sections)}</div><div class="stat-label">内容分类</div></div>
            <div class="stat"><div class="stat-value">{high_count}</div><div class="stat-label">高影响</div></div>
        </div>
        {sections_html}
        <div class="history-section">
            <h2>📅 历史日报目录</h2>
            <ul class="history-list">
                {history_items}
            </ul>
        </div>
    </div>
    <div class="footer">
        外贸新闻播报 · <a href="https://github.com/wigginZhang/foreign-trade-news">GitHub</a>
    </div>
</body>
</html>'''

def main():
    os.makedirs(DAILY, exist_ok=True)

    files = sorted([f for f in os.listdir(DATA) if f.endswith('.json')])
    dates = [f.replace('.json', '') for f in files]

    print(f'Found {len(files)} data files: {dates}')

    generated = []
    for fname in files:
        ds = fname.replace('.json', '')
        out = os.path.join(DAILY, f'{ds}.html')
        print(f'Generating {ds}...', end=' ')
        try:
            data = load_json(os.path.join(DATA, fname))
            html = generate_daily_html(ds, data, dates)
            with open(out, 'w', encoding='utf-8') as f:
                f.write(html)
            sections = get_sections(data)
            total = sum(len(s.get('news', [])) for s in sections)
            print(f'OK ({total} news, {len(sections)} sections)')
            generated.append(ds)
        except Exception as e:
            print(f'FAIL: {e}')

    print(f'\nGenerated {len(generated)}/{len(files)} daily HTML pages')
    if generated:
        print(f'Dates: {", ".join(generated)}')

if __name__ == '__main__':
    main()
