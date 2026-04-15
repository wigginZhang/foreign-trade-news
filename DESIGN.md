# DESIGN.md — 外贸新闻播报网站

> 基于 Apple Design System 风格重构的外贸新闻网站设计规范。

---

## 1. Visual Theme & Atmosphere

**设计理念：** 极致留白、清晰层次、高端质感。

Apple 的设计语言围绕「让内容呼吸」展开——大量留白使新闻内容成为焦点，SF Pro 字体确保可读性，柔和的灰色调营造专业、沉稳的外贸新闻阅读氛围。

**关键词：** Premium、Clean、Editorial、Minimal

---

## 2. Color Palette & Roles

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary Text | Deep Black | `#1D1D1F` | 正文、标题 |
| Secondary Text | Medium Gray | `#86868B` | 元信息、日期 |
| Tertiary Text | Light Gray | `#A1A1A6` | 占位符、次要说明 |
| Accent / Links | Apple Blue | `#0071E3` | 链接、高亮、按钮 |
| Accent Hover | Deep Blue | `#0077ED` | 交互态 |
| Background | Pure White | `#FFFFFF` | 主背景 |
| Secondary Background | Light Gray | `#F5F5F7` | 卡片、侧边栏背景 |
| Separator | Ultra Light | `#E5E5EA` | 分割线 |
| High Impact Tag | Soft Red | `#FF3B30` | 高影响新闻标签 |
| Medium Impact Tag | Orange | `#FF9500` | 中影响新闻标签 |

---

## 3. Typography Rules

**字体：** SF Pro Display（标题）、SF Pro Text（正文）、系统默认 fallback

### 字体栈（跨平台兼容）

```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', sans-serif;
```

### 字体层级表

| Element | Size | Weight | Line Height | Letter Spacing | Color |
|---------|------|--------|-------------|----------------|-------|
| Page Title | 32px | 700 | 1.1 | -0.02em | #1D1D1F |
| Section Heading | 21px | 700 | 1.2 | -0.01em | #1D1D1F |
| Card Title | 17px | 600 | 1.35 | 0 | #1D1D1F |
| Body Text | 15px | 400 | 1.6 | 0 | #1D1D1F |
| Meta / Caption | 13px | 400 | 1.4 | 0.01em | #86868B |
| Tag / Badge | 12px | 600 | 1.0 | 0.02em | varies |
| Mini Text | 11px | 500 | 1.3 | 0.03em | #A1A1A6 |

### 字号系统（Apple 8px 基准）

```
10 / 11 / 12 / 13 / 14 / 15 / 17 / 21 / 28 / 40 / 56
```

---

## 4. Component Stylings

### 4.1 Header（页头）

- **背景：** 纯白 `#FFFFFF`，底部 `1px solid #E5E5EA` 分割线
- **高度：** 56px（紧凑，留出更多内容空间）
- **标题：** 24px / 700 / -0.02em，黑色
- **副标题：** 13px / 400 / 灰色
- **图标：** emoji 表情符号，如 🐾

### 4.2 Sidebar（侧边栏）

- **宽度：** 240px
- **背景：** `#F5F5F7`
- **圆角：** 无（贴边）
- **日期选择器卡片：** 白底，16px 圆角，轻微阴影 `0 2px 8px rgba(0,0,0,0.06)`
- **快捷按钮：** 12px 圆角胶囊按钮，hover 时变为蓝色背景

### 4.3 News Card（新闻卡片）

- **背景：** `#FFFFFF`
- **圆角：** 16px
- **阴影：** `0 2px 12px rgba(0,0,0,0.08)`（Apple 风格柔和阴影）
- **内边距：** 24px
- **卡片间距：** 16px
- **分割线：** 无（用留白代替）

### 4.4 Section Header（分类头部）

- **背景：** `#F5F5F7`
- **圆角：** 16px 16px 0 0（仅顶部圆角）
- **内边距：** 16px 24px
- **分类图标：** 16px emoji
- **分类标题：** 15px / 700
- **数量标签：** 12px / 500，灰色背景 `#E5E5EA`，8px 圆角

### 4.5 News Item（单条新闻）

- **上边距：** 24px
- **第一个元素不加上边距**（与 section header 紧凑衔接）
- **新闻标题：** 17px / 600 / #1D1D1F
- **序号：** Apple Blue #0071E3 / 700
- **元信息行：** 13px / #86868B，包含来源、影响标签
- **摘要：** 15px / 400 / #1D1D1F，行高 1.7
- **关键事实区块：** 左侧 3px 蓝色边框，背景 `#F5F5F7`，12px 圆角
- **原文链接按钮：** 白色背景，Apple Blue 边框和文字，12px 圆角，hover 时填充蓝色

### 4.6 Impact Tag（影响标签）

| Level | Background | Text | Border |
|-------|-----------|------|--------|
| High | `#FF3B30` @ 12% opacity | `#FF3B30` | none |
| Medium | `#FF9500` @ 12% opacity | `#FF9500` | none |
| Low | `#86868B` @ 12% opacity | `#86868B` | none |

### 4.7 Stats Bar（统计栏）

- **统计卡片：** `#FFFFFF`，16px 圆角，轻阴影
- **数字：** 32px / 700 / Apple Blue #0071E3
- **标签：** 11px / 500 / #86868B / 大写
- **间距：** 16px，flex 布局均匀分布

### 4.8 Buttons（按钮）

**Primary Button:**
- Background: `#0071E3`
- Text: `#FFFFFF` / 14px / 600
- Border-radius: 12px
- Padding: 12px 24px
- Hover: `#0077ED`
- Active: `#005BB5`

**Secondary Button:**
- Background: `#FFFFFF`
- Text: `#0071E3`
- Border: `1.5px solid #0071E3`
- Border-radius: 12px
- Hover: Background `#F5F5F7`

**Capsule Button（快捷日期）:**
- Background: `#F5F5F7`
- Text: `#1D1D1F` / 13px
- Border-radius: 100px（胶囊形）
- Padding: 8px 16px
- Hover: Background `#E5E5EA`

---

## 5. Layout Principles

### 5.1 页面结构

```
┌─────────────────────────────────────────┐
│              Header (56px)               │
├──────────────┬──────────────────────────┤
│             │                           │
│  Sidebar    │      Main Content         │
│  (240px)    │      (flex: 1)            │
│             │                           │
│  - Date     │  - Stats Bar              │
│    Picker   │  - News Sections          │
│  - Quick    │    - Section Header       │
│    Dates    │    - News Cards           │
│             │                           │
└──────────────┴──────────────────────────┘
```

### 5.2 间距系统（8px 基准）

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | 紧凑元素间距 |
| `--space-sm` | 8px | 组件内部间距 |
| `--space-md` | 16px | 卡片内边距、间距 |
| `--space-lg` | 24px | 区块间间距 |
| `--space-xl` | 32px | 大区块间距 |
| `--space-2xl` | 48px | 页面级留白 |

### 5.3 最大内容宽度

- 主内容区最大宽度：**680px**（阅读最佳宽度）
- 侧边栏固定宽度：**240px**
- 页面最大宽度：**1080px**

### 5.4 留白哲学

Apple 的核心理念：「内容周围留白不是浪费空间，是让内容被看见。」

- 卡片内边距：**24px**
- 卡片外间距：**16px**
- 新闻标题与摘要间距：**12px**
- 摘要与标签/链接间距：**16px**

---

## 6. Depth & Elevation

### 6.1 阴影系统

| Level | Shadow | Usage |
|-------|--------|-------|
| Subtle | `0 2px 8px rgba(0,0,0,0.06)` | 侧边栏卡片 |
| Card | `0 2px 12px rgba(0,0,0,0.08)` | 新闻卡片 |
| Elevated | `0 4px 20px rgba(0,0,0,0.12)` | 弹窗、浮层 |

### 6.2 圆角系统

| Element | Radius |
|---------|--------|
| 按钮 | 12px |
| 卡片 | 16px |
| 标签/Badge | 8px |
| 胶囊按钮 | 100px |
| 输入框 | 10px |

### 6.3 分割线

- 颜色：`#E5E5EA`
- 宽度：1px
- Apple 偏好「用留白代替分割线」，分割线仅用于需要明确分组的场景

---

## 7. Do's and Don'ts

### ✅ 应该做

- 大量的留白和呼吸空间
- 使用 SF Pro 字体（或系统默认）
- 文字层次分明（标题 > 正文 > 元信息）
- 圆角统一（12px 按钮，16px 卡片）
- 柔和阴影（不刺眼）
- 强调色统一使用 Apple Blue #0071E3

### ❌ 不应该做

- 不要使用过多的颜色（保持主色 + 灰阶）
- 不要用太深的阴影（Apple 不使用浓重阴影）
- 不要内容挤在一起（留白优先）
- 不要用太多字体粗细（600/700 标题，400 正文）
- 不要用太小的字号（正文不小于 14px）
- 不要用纯黑 `#000000` 作为正文色（用 `#1D1D1F`）

---

## 8. Responsive Behavior

### 8.1 断点

| Breakpoint | Layout Change |
|------------|--------------|
| < 640px | 侧边栏折叠为顶部横条，堆叠布局 |
| 640-1024px | 保持侧边栏，收窄内容区 |
| > 1024px | 完整布局 |

### 8.2 移动端适配

- 侧边栏宽度改为 100%，显示在顶部
- 日期选择器变为横向滚动
- 统计栏变为横向两列或三列
- 卡片圆角从 16px 减为 12px
- 内容区内边距从 24px 减为 16px

### 8.3 触控目标

- 最小触控区域：**44px × 44px**（Apple HIG 标准）
- 按钮最小高度：**44px**
- 链接点击区域足够大**

---

## 9. Agent Prompt Guide

### 快速参考

```
Color:
- Primary Text: #1D1D1F
- Secondary Text: #86868B  
- Accent/Link: #0071E3
- Background: #FFFFFF
- Secondary BG: #F5F5F7

Typography:
- Title: 32px / 700
- Section: 21px / 700
- Body: 15px / 400 / line-height 1.6
- Meta: 13px / 400 / #86868B

Spacing:
- Card padding: 24px
- Card gap: 16px
- Border radius: 12px (buttons) / 16px (cards)

Shadow:
- Card: 0 2px 12px rgba(0,0,0,0.08)
```

### UI 生成 prompt 模板

```
请为外贸新闻网站生成 Apple 风格的 UI 组件，遵循以下规范：

1. 颜色：主文字 #1D1D1F，次文字 #86868B，强调色 #0071E3，背景 #FFFFFF/#F5F5F7
2. 字体：-apple-system, SF Pro, 系统默认无衬线
3. 间距：16px 基础单位，卡片内边距 24px，卡片间距 16px
4. 圆角：按钮 12px，卡片 16px
5. 阴影：0 2px 12px rgba(0,0,0,0.08)
6. 留白：大量留白，内容不拥挤
7. 层级：标题 > 正文 > 元信息，层次分明

生成内容：[具体需求]
```

---

## 10. 文件结构

```
foreign-trade-news/
├── index.html          # 主页面（已按此规范优化）
├── DESIGN.md           # 本设计规范文档
├── server.py           # Python 服务器
└── data/
    └── YYYY-MM-DD.json  # 每日新闻数据
```

---

_本设计规范由小O1号创建，基于 Apple Design System — 2026-04-15_
