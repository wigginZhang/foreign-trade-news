# DESIGN.md — 外贸新闻播报网站

> 基于 Claude (Anthropic) Design System 风格重构的外贸新闻网站设计规范。

---

## 1. Visual Theme & Atmosphere

**设计理念：** 温暖赤陶色强调、编辑感布局、值得信赖的 AI 原生美学。

Claude 的设计语言围绕「温暖 + 可信 + 从容」展开——不用科技感的霓虹黑，而是用暖色调让用户感到被尊重。大量留白表明产品"不急不躁"，传达专业感和智慧感。

**关键词：** Warm、Editorial、Trustworthy、Intellectual、Calm

---

## 2. Color Palette & Roles

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Warm Ivory / Pampas | `#F4F3EE` | 主背景 |
| Secondary Background | Light Warm Gray | `#EDEBE6` | 卡片、次级背景 |
| Tertiary Background | Pale Stone | `#E8E6E1` | 分割区域 |
| Primary Accent | Terracotta / Crail | `#C15F3C` | 链接、强调、高亮 |
| Accent Hover | Deep Terracotta | `#A84E30` | 交互态 |
| Primary Text | Deep Warm Black | `#2C2825` | 正文、标题 |
| Secondary Text | Warm Gray | `#6B6560` | 元信息、次要文字 |
| Tertiary Text | Light Warm Gray | `#9A9590` | 占位符、说明 |
| Separator | Warm Line | `#DDDBD6` | 分割线 |
| White | Pure White | `#FFFFFF` | 按钮、输入框 |
| High Impact | Muted Red | `#C15F3C` | 高影响标签（复用主色） |
| Medium Impact | Warm Amber | `#B8860B` | 中影响标签 |
| Low Impact | Warm Gray | `#9A9590` | 低影响标签 |

---

## 3. Typography Rules

**字体：** 标题用 Editorial Serif（如 Playfair Display / Georgia），正文用 Clean Sans（如 Inter / system-ui）

### 字体栈

```css
/* 标题 */
font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;

/* 正文 */
font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
```

### 字体层级表

| Element | Size | Weight | Line Height | Letter Spacing | Color |
|---------|------|--------|-------------|----------------|-------|
| Page Title | 32px | 700 | 1.1 | -0.02em | #2C2825 |
| Section Heading | 21px | 600 | 1.2 | -0.01em | #2C2825 |
| Card Title | 17px | 600 | 1.35 | 0 | #2C2825 |
| Body Text | 15px | 400 | 1.65 | 0 | #2C2825 |
| Meta / Caption | 13px | 400 | 1.4 | 0.01em | #6B6560 |
| Tag / Badge | 12px | 600 | 1.0 | 0.02em | varies |
| Mini Text | 11px | 500 | 1.3 | 0.03em | #9A9590 |

### 字号系统

```
10 / 11 / 12 / 13 / 14 / 15 / 17 / 21 / 28 / 40 / 56
```

---

## 4. Component Stylings

### 4.1 Header（页头）

- **背景：** `#F4F3EE`（与页面背景融合）
- **底部：** `1px solid #DDDBD6` 温暖分割线
- **高度：** 60px
- **标题：** 22px / 700 / serif / `#2C2825`
- **副标题：** 13px / 400 / `#6B6560`

### 4.2 Sidebar（侧边栏）

- **宽度：** 240px
- **背景：** `#EDEBE6`
- **日期选择器卡片：** 白底 `#FFFFFF`，12px 圆角，柔和阴影
- **快捷按钮：** 胶囊形，8px 圆角，hover 时填充 Terracotta

### 4.3 News Card（新闻卡片）

- **背景：** `#FFFFFF`
- **圆角：** 12px
- **阴影：** `0 2px 8px rgba(44,40,37,0.06)`（温暖色调阴影）
- **内边距：** 20px
- **卡片间距：** 16px

### 4.4 Section Header（分类头部）

- **背景：** `#EDEBE6`
- **圆角：** 12px 12px 0 0
- **内边距：** 14px 20px
- **分类标题：** 14px / 600 / `#2C2825`
- **数量标签：** 12px / 500 / `#6B6560`，`#DDDBD6` 背景，6px 圆角

### 4.5 News Item（单条新闻）

- **上边距：** 20px
- **新闻标题：** 16px / 600 / `#2C2825` / serif
- **序号：** Terracotta `#C15F3C` / 700
- **元信息：** 13px / `#6B6560`
- **摘要：** 14px / 400 / line-height 1.65 / `#2C2825`
- **关键事实区块：** 左侧 3px Terracotta 边框，`#F4F3EE` 背景，8px 圆角
- **原文链接按钮：** 白色背景，Terracotta 边框和文字，hover 时填充 Terracotta

### 4.6 Impact Tag（影响标签）

| Level | Background | Text | Border |
|-------|-----------|------|--------|
| High | `#C15F3C` @ 12% opacity | `#C15F3C` | none |
| Medium | `#B8860B` @ 12% opacity | `#B8860B` | none |
| Low | `#9A9590` @ 12% opacity | `#9A9590` | none |

### 4.7 Stats Bar（统计栏）

- **统计卡片：** `#FFFFFF`，12px 圆角，温暖阴影
- **数字：** 28px / 700 / Terracotta `#C15F3C`
- **标签：** 11px / 600 / `#6B6560` / 大写

### 4.8 Buttons（按钮）

**Primary Button:**
- Background: `#C15F3C`（Terracotta）
- Text: `#FFFFFF`
- Border-radius: 8px
- Padding: 10px 20px
- Hover: `#A84E30`

**Secondary Button:**
- Background: `#FFFFFF`
- Text: `#C15F3C`
- Border: `1.5px solid #C15F3C`
- Border-radius: 8px
- Hover: Background `#C15F3C`，Text `#FFFFFF`

**Capsule Button:**
- Background: `#EDEBE6`
- Text: `#2C2825`
- Border-radius: 100px
- Padding: 8px 14px
- Hover: Background `#C15F3C`，Text `#FFFFFF`

---

## 5. Layout Principles

### 5.1 页面结构

```
┌─────────────────────────────────────────┐
│           Header (60px, warm ivory)       │
├──────────────┬──────────────────────────┤
│             │                           │
│  Sidebar    │      Main Content         │
│  (240px)    │      (flex: 1)            │
│  warm gray  │                           │
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
| `--space-lg` | 20px | 区块间间距 |
| `--space-xl` | 32px | 大区块间距 |
| `--space-2xl` | 48px | 页面级留白 |

### 5.3 最大内容宽度

- 主内容区最大宽度：**680px**（阅读最佳宽度）
- 侧边栏固定宽度：**240px**
- 页面最大宽度：**1080px**

### 5.4 留白哲学

Claude 的核心理念：「留白意味着产品不急躁、不拼命推销。」

- 卡片内边距：**20px**
- 卡片外间距：**16px**
- 新闻标题与摘要间距：**10px**
- 摘要与标签/链接间距：**14px**
- 行高：**1.65**（比 Apple 的 1.6 更高，强调可读性）

---

## 6. Depth & Elevation

### 6.1 阴影系统

| Level | Shadow | Usage |
|-------|--------|-------|
| Subtle | `0 1px 3px rgba(44,40,37,0.05)` | 侧边栏卡片 |
| Card | `0 2px 8px rgba(44,40,37,0.06)` | 新闻卡片 |
| Elevated | `0 4px 16px rgba(44,40,37,0.10)` | 弹窗、浮层 |

### 6.2 圆角系统

| Element | Radius |
|---------|--------|
| 按钮 | 8px |
| 卡片 | 12px |
| 标签/Badge | 6px |
| 胶囊按钮 | 100px |
| 输入框 | 8px |

### 6.3 分割线

- 颜色：`#DDDBD6`（温暖灰）
- 宽度：1px

---

## 7. Do's and Don'ts

### ✅ 应该做

- 温暖的 Ivory 背景（不用纯白）
- Terracotta 赤陶色作为唯一强调色
- Editorial Serif 字体作为标题
- 较高行高（1.65）确保阅读舒适
- 大量留白，传达从容感
- 温暖色调的阴影

### ❌ 不应该做

- 不要用纯白背景（用 Ivory `#F4F3EE`）
- 不要用霓虹或科技蓝作为主色
- 不要用太粗的边框或分割线
- 不要内容拥挤（留白优先）
- 不要用太多颜色（保持单强调色）
- 不要用纯黑文字（用 `#2C2825` 暖黑）

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
- 统计栏变为 3 列变为 1 列
- 卡片圆角从 12px 减为 8px
- 内容区内边距从 20px 减为 16px

### 8.3 触控目标

- 最小触控区域：**44px × 44px**
- 按钮最小高度：**40px**

---

## 9. Agent Prompt Guide

### 快速参考

```
Color:
- Background: #F4F3EE (warm ivory)
- Secondary BG: #EDEBE6
- Accent: #C15F3C (terracotta)
- Primary Text: #2C2825 (warm black)
- Secondary Text: #6B6560

Typography:
- Title: Playfair Display / serif, 32px / 700
- Section: serif, 21px / 600
- Body: sans-serif, 15px / 400 / line-height 1.65
- Meta: 13px / #6B6560

Spacing:
- Card padding: 20px
- Card gap: 16px
- Border radius: 8px (buttons) / 12px (cards)

Shadow:
- Card: 0 2px 8px rgba(44,40,37,0.06)
```

### UI 生成 prompt 模板

```
请为外贸新闻网站生成 Claude (Anthropic) 风格的 UI 组件，遵循以下规范：

1. 颜色：背景 #F4F3EE（暖象牙），强调色 #C15F3C（赤陶），主文字 #2C2825（暖黑）
2. 字体：标题用 serif（Playfair Display），正文用 sans-serif（Inter）
3. 间距：16px 基础单位，行高 1.65（强调可读性）
4. 圆角：按钮 8px，卡片 12px
5. 阴影：0 2px 8px rgba(44,40,37,0.06)（温暖色调）
6. 氛围：温暖、编辑感、从容不急
7. 层级：标题 > 正文 > 元信息，层次分明

生成内容：[具体需求]
```

---

## 10. 文件结构

```
foreign-trade-news/
├── index.html          # 主页面（已按此规范优化）
├── DESIGN.md           # 本设计规范文档
├── preview.html        # 设计预览页面
├── server.py           # Python 服务器
└── data/
    └── YYYY-MM-DD.json  # 每日新闻数据
```

---

_本设计规范由小O1号创建，基于 Claude (Anthropic) Design System — 2026-04-15_
