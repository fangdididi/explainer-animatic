[English](README.md) | **简体中文**

# 讲解短片动态分镜（Explainer Animatic）

> 一个 AI 智能体技能：按时长规划一支讲解短片，并在视频做出来之前就能看到它——一句“观众收获”、一份字数预算、一份为耳朵写的口播稿、一张每句旁白都有画面的分镜表、一次时间核对，以及一个带字幕和草稿配音、可直接播放的 HTML 动态分镜。

让 AI 做“一支 60 秒的 X 讲解视频”，常见结果是：稿子 60 秒根本念不完，想把原文全塞进去，镜头列表只是把旁白原句再贴到屏幕上。往往等视频做完了才发现问题。

**Explainer Animatic** 给智能体一套小型动画工作室的工作顺序：先定下观众看完能做到什么，把时长换算成字数预算，选一条叙事主线，写短句口播，给每一句配上画面、动作和到下一拍的衔接，再用脚本核对时间，生成一个可以播放、拖动、分享的单个 HTML 文件。在这里修正顺序和节奏，只需要几分钟；然后再用你喜欢的任何工具做正式视频。

适用于产品和功能讲解、概念小课、更新日志和合并请求、技巧清单、内部通知，支持中文和英文。

## 功能

- **先写观众收获。**“看完之后，<谁> 能 <做到/说出> <什么>。”之后的每一次删改都以它为准。
- **按时长算字数。** 中文约 4.2 字/秒，英文约 2.3 词/秒，并为停顿留出余量。超了就删，绝不加速。
- **四条叙事主线。** 卡点 → 原理 → 证据 → 收益 → 下一步；误区 → 反转 → 证据 → 规则；改之前 → 改了什么 → 改之后 → 注意事项；清单倒数。每条都给出时长占比。
- **为耳朵写稿的规则。** 一行一个意思、句子短、数字按播音的念法写、只有一个行动号召。
- **有意图的分镜表。** 每一拍包含旁白、补充而不是重复旁白的屏幕文字、五类画面之一（文字、图解、数字、比喻、界面）、一个动作动词、一种衔接方式（硬切、在某个词上切、元素带入下一拍、停顿），以及关键结论前可选的静止。
- **时间核对。** `animatic.py check` 估算每一拍的口播时长和阅读时长，输出带时间码的表格，并标出超时、停留过长或一闪而过的拍、缺失的画面、过长的句子、照抄旁白的屏幕文字。
- **可播放的动态分镜。** `animatic.py build` 生成一个独立的 HTML 文件：按时长播放的各拍、按动作动词的简单入场、字幕、可点击的分拍条、键盘控制、直达某一拍的链接，以及使用浏览器自带语音的可选草稿配音。任何一拍都可以放入内联 SVG 做草图。
- **新鲜眼睛评审。** 正式制作前做复述测试、静音测试和盲听测试。
- **制作表。** `animatic.py sheet` 输出带时间码的 Markdown 镜头表，交给剪辑师、动效设计师、HTML 转视频渲染器或生成式视频工具。
- **零依赖。** 一个 Python 3.8+ 脚本，只用标准库。不需要账号，不需要 API Key。
- **双语。** 分镜文件、时长计算和播放器界面支持中文或英文（`"lang": "zh-CN"`）。

## 安装

把仓库克隆到智能体的技能目录，文件夹名应为 `explainer-animatic`。

**Claude Code**

```bash
# 个人（所有项目）
git clone https://github.com/fangdididi/explainer-animatic ~/.claude/skills/explainer-animatic
# 或者只用于某个项目
git clone https://github.com/fangdididi/explainer-animatic .claude/skills/explainer-animatic
```

**OpenAI Codex CLI**

```bash
git clone https://github.com/fangdididi/explainer-animatic ~/.codex/skills/explainer-animatic
```

**Cursor**

```bash
git clone https://github.com/fangdididi/explainer-animatic .cursor/skills/explainer-animatic
```

**Gemini CLI、OpenCode、Windsurf 及其他智能体**

如果智能体有技能目录（例如 `.agents/skills/`），克隆到那里即可。如果没有技能系统，在 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 或规则文件里加一行：

```text
当我要讲解视频、短视频脚本或分镜时，按照 ./explainer-animatic/SKILL.zh-CN.md 的方法进行，并把分镜保存在 beats.json 中。
```

要求：辅助脚本需要 Python 3.8 或更新版本，观看动态分镜需要任意现代浏览器。方法本身不依赖它们也能使用。

## 使用

直接用自然语言提出需求：

- “把这篇产品介绍做成 60 秒的讲解视频分镜。”
- “我们把报表导出改成了后台任务，做一个 45 秒的视频给客服团队看。”
- “这是我的文章，我需要一份 30 秒竖屏视频的口播稿和分镜。”
- "Make a 60-second explainer that convinces new hires to start saving early."

智能体会写出观众收获，提出主线和字数预算，起草口播稿，填写 `beats.json`，并运行辅助脚本：

```bash
python3 scripts/animatic.py new beats.json --lang zh-CN --seconds 45   # 新建模板
python3 scripts/animatic.py check beats.json                           # 时间核对 + 检查，有错误时退出码为 1
python3 scripts/animatic.py build beats.json -o animatic.html          # 生成可播放的动态分镜
python3 scripts/animatic.py sheet beats.json -o production-sheet.md    # 生成制作用镜头表
```

在浏览器中打开 `animatic.html`。空格播放/暂停，左右方向键切换拍，Home 回到开头，`animatic.html#b05` 直接打开第 `b05` 拍。勾选 **草稿配音** 可以听到每句旁白被朗读出来。

## 示例

`examples/async-export.zh-CN.json`（中文，45 秒，“报表导出改成后台任务”）的核对结果：

```text
这次改动：报表导出改成后台任务  (zh-CN, pace 4.2 chars/s)
id    start   part           vo screen    dur  picture
b01   0:00.0  before       5.2s   1.5s   5.6s  浏览器窗口，按钮按下后一个转圈图标，右上角计时器从 0 跳到 55
b02   0:05.6  before       6.0s   1.3s   6.8s  请求与服务器之间一根线越拉越长，到 60 秒处断开变红
b03   0:12.4  change       5.7s   1.5s   6.1s  请求线一来一回只用一瞬间；一个“任务卡片”落进后台队列
...
b07   0:34.6  next         4.5s   1.5s   6.4s  文档目录，第二节高亮
total 0:41.0  |  7 beats  |  150 spoken chars  |  target 45
OK
```

第 b03 拍用内联 SVG 画了“页面 → 服务器 → 后台队列”的简图，其余各拍用画面说明卡占位。`examples/early-start.json` 是英文的 60 秒理财讲解，演示“卡点 → 原理 → 证据 → 收益 → 下一步”主线：初稿里 8.9 秒的证据拍被核对标出后，拆成了两拍并用元素带入衔接。两个示例都附带生成好的 `.html` 动态分镜和 `.sheet.md` 制作表。

## 文件结构

```text
explainer-animatic/
├── SKILL.md                    # 技能说明（英文）
├── SKILL.zh-CN.md              # 技能说明（中文）
├── README.md
├── README.zh-CN.md
├── LICENSE
├── scripts/
│   └── animatic.py             # new / check / build / sheet
└── examples/
    ├── early-start.json        # 英文，60 秒，理财讲解
    ├── early-start.html        # 生成的动态分镜
    ├── early-start.sheet.md    # 制作表
    ├── async-export.zh-CN.json # 中文，45 秒，合并请求讲解
    ├── async-export.zh-CN.html
    └── async-export.zh-CN.sheet.md
```

## 许可证

MIT © fangdididi
