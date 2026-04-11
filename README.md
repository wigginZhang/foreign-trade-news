# 外贸新闻播报网站

自动采集、展示外贸新闻的静态网站。

## 功能

- 📰 自动采集每日外贸新闻（关税政策、进出口数据、汇率、物流等）
- 📅 按日期归档，支持历史浏览
- 🔗 每条新闻附带原文链接
- 📊 分类展示：关税政策、外贸数据、地缘经贸、汇率动态、物流航运

## 文件结构

```
news-website/
├── index.html      # 网站主页面
├── server.py       # Python HTTP服务器
└── server.ps1      # PowerShell HTTP服务器

news-archive/
├── 2026-04-10.json # 新闻存档（按日期）
├── 2026-04-11.json
├── collect_news.ps1    # 新闻采集脚本
├── transform_news.ps1  # 数据转换脚本
└── data.json           # 临时数据文件
```

## 本地运行

```bash
cd news-website
python server.py
```

访问 http://localhost:8001

## 技术栈

- 前端：原生 HTML/CSS/JS
- 后端：Python HTTP Server
- 数据采集：PowerShell + Tavily API

## 定时任务

每日 09:20 自动采集新闻并推送至企业微信。

## 作者

张伟杰 (ZhangWeiJie)
