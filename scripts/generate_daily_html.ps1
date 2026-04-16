# 生成每日历史日报 HTML
# 使用方式: .\generate_daily_html.ps1

param(
    [string]$Date = ""  # 可选，指定日期如 "2026-04-16"，留空则生成所有
)

$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$DataDir = Join-Path $BaseDir "data"
$DailyDir = Join-Path $BaseDir "daily"

# 确保 daily 目录存在
if (-not (Test-Path $DailyDir)) {
    New-Item -ItemType Directory -Path $DailyDir | Out-Null
}

# 获取所有 JSON 文件
if ($Date) {
    $jsonFiles = @((Join-Path $DataDir "$Date.json"))
} else {
    $jsonFiles = Get-ChildItem $DataDir -Filter "*.json" | Sort-Object Name -Descending
}

# 星期映射
$Weekdays = @('周日', '周一', '周二', '周三', '周四', '周五', '周六')

# 分类图标映射
$SectionIcons = @{
    "data" = "📊"
    "geo" = "🌏"
    "fx" = "💱"
    "logistics" = "🚢"
    "default" = "📰"
}

function Get-IconForSection($id) {
    return $SectionIcons[$id] ?? $SectionIcons["default"]
}

function New-DailyHtml {
    param($DateStr, $Data)
    
    $date = Get-Date $DateStr
    $weekday = $Weekdays[$date.DayOfWeek.Value__]
    $monthDay = "$($date.ToString('M月d日'))"
    
    $stats = $Data.stats
    $sections = $Data.sections
    
    # 构建新闻 HTML
    $newsItemsHtml = ""
    foreach ($section in $sections) {
        $icon = Get-IconForSection $section.id
        $newsItemsHtml += @"
        <div class="section">
            <div class="section-header">
                <div class="section-title">
                    <span class="icon">$icon</span>$($section.title)
                </div>
                <div class="section-count">$($section.news.Count) 条</div>
            </div>
            <div class="section-content">
"$@
        
        foreach ($news in $section.news) {
            $impactClass = switch ($news.impact) {
                "high" { "high" }
                "medium" { "medium" }
                default { "low" }
            }
            $impactText = switch ($news.impact) {
                "high" { "高影响" }
                "medium" { "中影响" }
                default { "低影响" }
            }
            
            $keyFactsHtml = ""
            if ($news.keyFacts -and $news.keyFacts.Count -gt 0) {
                $keyFactsList = ($news.keyFacts | ForEach-Object { "<li>$_</li>" }) -join ""
                $keyFactsHtml = @"
                <div class="key-facts">
                    <div class="key-facts-title">关键事实</div>
                    <ul>$keyFactsList</ul>
                </div>
"@
            }
            
            $newsItemsHtml += @"
                <div class="news-item">
                    <div class="news-title">
                        <span class="news-num">$($section.news.IndexOf($news) + 1).</span>
                        <a href="$($news.url)" target="_blank">$($news.title)</a>
                    </div>
                    <div class="news-meta">
                        <span class="impact-tag $($impactClass)">$impactText</span>
                        <span class="news-source">$($news.source)</span>
                    </div>
                    <div class="news-snippet">$($news.snippet)</div>
                    $keyFactsHtml
                    <div class="news-actions">
                        <a href="$($news.url)" target="_blank" class="read-more">阅读原文 →</a>
                    </div>
                </div>
"@
        }
        
        $newsItemsHtml += @"
            </div>
        </div>
"@
    }
    
    # 判断是否是最新一天
    $isLatest = $DateStr -eq "2026-04-16"
    $prevDate = $date.AddDays(-1).ToString("yyyy-MM-dd")
    $nextDate = $date.AddDays(1).ToString("yyyy-MM-dd")
    
    # 检查前后日期是否存在
    $hasPrev = Test-Path (Join-Path $DataDir "$prevDate.json")
    $hasNext = $isLatest -or (Test-Path (Join-Path $DataDir "$nextDate.json"))
    
    $navHtml = ""
    if ($hasPrev -or $hasNext) {
        $navHtml = '<div class="nav-buttons">'
        if ($hasPrev) {
            $prevMonthDay = (Get-Date $prevDate).ToString("M月d日")
            $navHtml += "<a href=`"$prevDate.html`" class=`"nav-btn`">← $prevMonthDay</a>"
        }
        $navHtml += '<a href="../history.html" class="nav-btn">📅 历史目录</a>'
        if ($hasNext -and -not $isLatest) {
            $nextMonthDay = (Get-Date $nextDate).ToString("M月d日")
            $navHtml += "<a href=`"$nextDate.html`" class=`"nav-btn`">$nextMonthDay →</a>"
        }
        $navHtml += '</div>'
    }
    
$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$monthDay $weekday 外贸新闻播报</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-bg: #F4F3EE;
            --color-bg-secondary: #EDEBE6;
            --color-bg-tertiary: #E8E6E1;
            --color-accent: #C15F3C;
            --color-accent-hover: #A84E30;
            --color-text-primary: #2C2825;
            --color-text-secondary: #6B6560;
            --color-text-tertiary: #9A9590;
            --color-separator: #DDDBD6;
            --color-white: #FFFFFF;
            --color-high-impact: #C15F3C;
            --color-medium-impact: #B8860B;
            --color-low-impact: #9A9590;
            --font-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
            --font-sans: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 20px;
            --space-xl: 32px;
            --space-2xl: 48px;
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-full: 100px;
            --shadow-card: 0 2px 8px rgba(44,40,37,0.06);
            --shadow-elevated: 0 4px 16px rgba(44,40,37,0.10);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: var(--font-sans);
            background: var(--color-bg);
            color: var(--color-text-primary);
            line-height: 1.65;
            -webkit-font-smoothing: antialiased;
        }
        header {
            background: var(--color-bg);
            border-bottom: 1px solid var(--color-separator);
            padding: 0 var(--space-lg);
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-title {
            font-family: var(--font-serif);
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .header-link {
            font-size: 14px;
            color: var(--color-accent);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .header-link:hover { color: var(--color-accent-hover); }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: var(--space-xl);
        }
        .day-header {
            text-align: center;
            margin-bottom: var(--space-xl);
        }
        .day-title {
            font-family: var(--font-serif);
            font-size: 32px;
            font-weight: 700;
            color: var(--color-text-primary);
            margin-bottom: var(--space-sm);
        }
        .day-subtitle {
            font-size: 15px;
            color: var(--color-text-secondary);
        }
        .nav-buttons {
            display: flex;
            gap: var(--space-md);
            justify-content: center;
            margin-top: var(--space-lg);
            flex-wrap: wrap;
        }
        .nav-btn {
            background: var(--color-white);
            border: 1px solid var(--color-separator);
            border-radius: var(--radius-full);
            padding: 8px 20px;
            font-size: 14px;
            font-weight: 500;
            color: var(--color-text-primary);
            text-decoration: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
        }
        .nav-btn:hover {
            background: var(--color-accent);
            color: var(--color-white);
            border-color: var(--color-accent);
            transform: translateY(-2px);
        }
        .stats-bar {
            display: flex;
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
        }
        .stat {
            background: var(--color-white);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            flex: 1;
            text-align: center;
            box-shadow: var(--shadow-card);
        }
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--color-accent);
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        .stat-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--color-text-secondary);
            margin-top: var(--space-xs);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .section {
            background: var(--color-white);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-md);
            box-shadow: var(--shadow-card);
            overflow: hidden;
        }
        .section-header {
            padding: 14px var(--space-lg);
            background: var(--color-bg-secondary);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .section-title {
            font-family: var(--font-serif);
            font-size: 14px;
            font-weight: 600;
            color: var(--color-text-primary);
        }
        .section-title .icon { margin-right: var(--space-sm); }
        .section-count {
            font-size: 12px;
            font-weight: 500;
            color: var(--color-text-secondary);
            background: var(--color-separator);
            padding: 4px 10px;
            border-radius: var(--radius-sm);
        }
        .news-item {
            padding: var(--space-lg);
            border-bottom: 1px solid var(--color-separator);
        }
        .news-item:last-child { border-bottom: none; }
        .news-title {
            font-family: var(--font-serif);
            font-size: 16px;
            font-weight: 600;
            margin-bottom: var(--space-sm);
            display: flex;
            gap: 8px;
            line-height: 1.4;
        }
        .news-num {
            color: var(--color-accent);
            font-weight: 700;
            flex-shrink: 0;
        }
        .news-title a {
            color: var(--color-text-primary);
            text-decoration: none;
        }
        .news-title a:hover { color: var(--color-accent); }
        .news-meta {
            display: flex;
            gap: var(--space-sm);
            margin-bottom: 10px;
            font-size: 13px;
            color: var(--color-text-secondary);
            flex-wrap: wrap;
            align-items: center;
        }
        .impact-tag {
            padding: 3px 10px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            font-weight: 600;
        }
        .impact-tag.high { background: rgba(193,95,60,0.12); color: var(--color-high-impact); }
        .impact-tag.medium { background: rgba(184,134,11,0.12); color: var(--color-medium-impact); }
        .impact-tag.low { background: rgba(154,149,144,0.12); color: var(--color-low-impact); }
        .news-source { color: var(--color-text-tertiary); }
        .news-snippet {
            font-size: 14px;
            color: var(--color-text-primary);
            line-height: 1.65;
            margin-bottom: 14px;
        }
        .key-facts {
            background: var(--color-bg);
            border-left: 3px solid var(--color-accent);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            padding: 12px 14px;
            margin-bottom: 14px;
        }
        .key-facts-title {
            font-size: 11px;
            font-weight: 600;
            color: var(--color-text-secondary);
            margin-bottom: var(--space-sm);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .key-facts ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .key-facts li {
            font-size: 13px;
            color: var(--color-text-primary);
            padding: 3px 0;
            padding-left: 14px;
            position: relative;
            line-height: 1.5;
        }
        .key-facts li::before {
            content: '→';
            position: absolute;
            left: 0;
            color: var(--color-accent);
        }
        .news-actions {
            text-align: right;
        }
        .read-more {
            font-size: 13px;
            color: var(--color-accent);
            text-decoration: none;
            font-weight: 500;
        }
        .read-more:hover { color: var(--color-accent-hover); }
        .footer {
            text-align: center;
            font-size: 13px;
            color: var(--color-text-tertiary);
            padding: var(--space-xl);
            margin-top: var(--space-xl);
            border-top: 1px solid var(--color-separator);
        }
        .footer a { color: var(--color-accent); }
    </style>
</head>
<body>
    <header>
        <div class="header-title">🐾 外贸新闻播报</div>
        <a href="../index.html" class="header-link">← 返回首页</a>
    </header>
    
    <div class="container">
        <div class="day-header">
            <h1 class="day-title">$monthDay $weekday</h1>
            <p class="day-subtitle">外贸新闻日报 · $($stats.totalNews) 条新闻 · $($stats.sections) 个分类</p>
            $navHtml
        </div>
        
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">$($stats.totalNews)</div>
                <div class="stat-label">新闻总数</div>
            </div>
            <div class="stat">
                <div class="stat-value">$($stats.sections)</div>
                <div class="stat-label">内容分类</div>
            </div>
        </div>
        
        $newsItemsHtml
    </div>
    
    <div class="footer">
        外贸新闻播报 · 
        <a href="../history.html">历史日报目录</a> · 
        <a href="https://github.com/wigginZhang/foreign-trade-news">GitHub</a>
    </div>
</body>
</html>
"@

    return $html
}

# 处理每个 JSON 文件
foreach ($file in $jsonFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "文件不存在: $file" -ForegroundColor Yellow
        continue
    }
    
    $dateStr = ($file.Name -replace '\.json$', '')
    $outputFile = Join-Path $DailyDir "$dateStr.html"
    
    Write-Host "生成: $outputFile" -ForegroundColor Cyan
    
    try {
        $content = Get-Content $file -Raw -Encoding UTF8
        $data = $content | ConvertFrom-Json
        
        $html = New-DailyHtml -DateStr $dateStr -Data $data
        
        $html | Out-File -FilePath $outputFile -Encoding UTF8
        Write-Host "  ✓ 完成" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ 失败: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "所有历史日报 HTML 生成完成！" -ForegroundColor Green
Write-Host "输出目录: $DailyDir"
