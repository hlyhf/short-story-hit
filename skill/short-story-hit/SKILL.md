---
name: short-story-hit
description: 短篇/短故事爆款创作（钩子+关系双引擎），覆盖微小说(800-2000字)到5万字中篇全谱系。当用户写短篇、短故事、微小说、5万字中篇、爆款故事，或提到「下钩子」「开篇抓人」「关系张力」「反转」「爽点」「虐点」「伏笔回收」「情节连贯」时触发。不适用于50万字+长篇小说（用 novel-creation-sop）、剧本/分镜（用 drama-studio）。
version: 2.0.0
author: 灵析剧创 · 智子编辑部 (ima.copilot)
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [writing, short-story, hit, hook, relationship, longform, serial, lingxi-juchuang]
---

# 爆款短篇创作 · 钩子与关系双引擎

## 概述

本技能帮助你在有限篇幅内产出"能成为爆款"的短篇 / 短故事。它提供一套可复用的结构化流程与领域知识，而不是替你把文字写漂亮。核心是两台发动机：

- **钩子引擎**：用前三秒 / 前三句抓住注意力，让读者"必须往下读"。
- **关系引擎**：用人物关系的错位与翻转制造戏剧张力，让读者"心里一紧 / 一爽 / 一虐"。

微小说篇幅极短、容错极低——每一句话要么是钩子，要么是推进；5 万字中篇则需**长弧结构 + 人物弧光 + 伏笔系统**撑住连贯。本技能覆盖全谱系，把"凭感觉写"变成"按方法论造"。

## 长-form 模式（5 万字中篇短故事）

当用户要写 5 万字以上短故事（盐选 / 番茄中篇品类）时，切到长-form 模式：微小说公式不够用了，必须补三件套——**长弧结构、人物弧光、伏笔系统**，并用连贯性自检守住「内容不崩、情节连贯」。

- 完整蓝图（字数分配 / 三幕 / 弧光 / 伏笔回收表 / 连贯清单 / 防崩 SOP / 章级节拍器 / 钟馗示例大纲）：`references/longform-blueprint.md`
- 连贯性自检脚本（伏笔悬空扫描 + 章末钩子密度）：`scripts/continuity_check.py`
- 工作顺序：先用蓝图规划分卷大纲 + 填伏笔表 → 按章写稿（每章过章级节拍器）→ 跑 `continuity_check.py` 查悬空伏笔与塌陷章 → 过连贯清单。

## 核心心法

> 爆款 = 情绪交易。读者用几秒钟，换一次心跳。

三条铁律：

1. **开篇即冲突**：前三句必须出现冲突 / 异常 / 悬念，禁止环境铺垫、背景介绍、"从前有座山"。
2. **关系即钩子**：每一次关系揭露，都是一个新剧情钩子。亲密关系越错位，张力越狠。
3. **结尾留余震**：收尾要么情绪炸裂后骤停，要么留一个未解悬念引续集。

## 使用流程（6 步）

### Phase 1 · 锁定情绪靶心
先选**情绪类型**（爽 / 虐 / 爽虐交织 / 悬），再选**高张力关系模型**（替身 / 复仇 / 错认 / 阶层差 / 养恩血仇 / 契约）。用一句话讲完故事，问自己：目标读者会不会"心里一紧 / 一爽 / 一好奇"？不会就换选题。
- 关系模型见 `references/relationship-design.md`，情绪 × 关系速查见 `references/case-matrix.md`

> **确认门（必做）**：向用户用一句话复述——"情绪靶心 = __，关系模型 = __，是否按此继续？"——待用户确认后再进入 Phase 2。长流程在此设确认点，避免方向跑偏。

### Phase 2 · 下钩子（开篇）
从 5 种钩子公式中选一种，套"钩子生成模板"写开篇 3 句，必须过**前三句原则**。写不出开头时直接抄 `references/hook-arsenal.md` 的弹药库。
- 公式与模板：`references/hook-design.md`
- 现成模板 + 标题公式 + 收尾金句：`references/hook-arsenal.md`

### Phase 3 · 排关系（张力发动机）
选 1 个关系模型打底，填**关系递进表**（开局 → 转折 → 中局 → 高潮 → 收尾），每一层标一个"钩子动作"。人物立不住时先填 `references/character-builder.md` 的角色卡。
- 模型与递进表：`references/relationship-design.md`
- 角色速建：`references/character-builder.md`

### Phase 4 · 设反转
在中局 / 高潮安排 ≥ 1 次"认知反转"（读者以为 A，其实是 B）。铁律：**每 1/3 篇幅至少一个反转或新钩子**，否则中间塌。
- 反转类型与节奏：`references/emotion-curve.md`
- 避免烂俗、踩中趋势：`references/anti-cliche.md`

### Phase 5 · 收尾钩
二选一：
- **爆点落幕**：情绪炸裂后骤停，不给缓冲。
- **悬念断点**：留一个未解关系 / 谜团，引读者期待续集或评论区讨论（做连载见 `references/serial-hook.md`）。
- 做系列 / 连载：`references/serial-hook.md`

### Phase 6 · 自检
跑结构体检脚本（v3.2 输出逐句情绪曲线 + 逐句改写建议），或对照清单人工核查：
```bash
python3 scripts/structure_check.py 你的故事.md
# 或批量: python3 scripts/structure_check.py --dir 你的文件夹/
```
- **对标拆解（让弹药库自我进化）**：把任意爆文喂给脚本，输出方法论骨架（靶心情绪 / 钩子公式 / 关系模型 / 反转点 / 结尾类型 / 弹药库对照 / 可入库卡片），一眼看出它是「已有格子」还是「新组合」，拆完即沉淀为新案例：
```bash
python3 scripts/structure_check.py 爆文.md --benchmark
# 加标题: --title 标题   批量拆解: --dir 文件夹/ --benchmark
```
- 自检清单与红线：`references/hit-checklist.md`
- 十大死因对照：`references/death-causes.md`（病文 → 诊断 → 处方）

## 标准交付物（当用户要成品时）

按本流程交付时，产出物应包含以下五件，顺序即工作流：

1. **靶心卡**：情绪类型 + 关系模型 + 一句话爽点 / 虐点（来自 Phase 1 + 确认门）。
2. **钩子（前三句）**：过前三句原则的成稿开头（来自 Phase 2）。
3. **关系表**：5 阶段递进表，每阶段标钩子动作（来自 Phase 3 + 角色卡）。
4. **正文**：800–2000 字成稿，含 ≥1 次反转、结尾余震（来自 Phase 4–5；可用 `references/ai-expand-prompt.md` 的模板让 AI 扩写）。
5. **体检报告**：`structure_check.py` 输出（评分 + 改进建议）或 `hit-checklist.md` 勾选结果。

### 长-form 交付物（5 万字中篇）
1. **设定圣经**（一页纸：规则 / 能力 / 世界观 / 禁忌）。
2. **分卷大纲**（对齐字数桶，五幕节拍）。
3. **人物弧光卡**（主角三件套 + 四节点；配角迷你弧）。
4. **伏笔回收表**（每个主线伏笔的铺设 / 回收位置）。
5. **分章成稿**（每章过章级节拍器四问）。
6. **连贯自检报告**：`continuity_check.py` 输出 + §5 清单勾选。

## 决策路由

| 用户意图 | 动作 |
|----------|------|
| 要给选题 / 定情绪 | Phase 1 + 读 `case-matrix.md` + `relationship-design.md` |
| 卡在开篇 / 要标题 | 读 `hook-arsenal.md`，套模板 |
| 要做人物关系 | 读 `relationship-design.md` + `character-builder.md`，填表 |
| 要防烂俗 / 追趋势 | 读 `anti-cliche.md` |
| 要平台发布 | 读 `platform-adapt.md` |
| 要做连载 / 续集 | 读 `serial-hook.md` |
| 写完要质检 | 跑 `structure_check.py`（情绪曲线+逐句建议）+ 读 `hit-checklist.md` + 对照 `death-causes.md` |
| 要发布到平台 | 读 `release-kit.md`（三件套 + 平台 Checklist + 数据回收） |
| 要控信息差节奏 | 读 `information-gap.md`（三种体验 + 设计三问） |
| 要 AI 扩写 | 读 `ai-expand-prompt.md`，套 prompt |
| 要示范案例 | 读 `examples.md` |
| 写 5 万字以上中篇短故事 | 读 `longform-blueprint.md`（蓝图）+ 跑 `continuity_check.py`（连贯自检） |

## 与 drama-studio 的交接（短篇 → 剧本 / 分镜）

本技能产出**短篇故事骨架**。若用户要把它改成剧本 / 分镜（如做漫剧、短剧），移交 `drama-studio` 技能，并附带：
- **靶心卡**（情绪 + 关系模型）
- **关系递进表**（5 阶段）
- **反转点标注**

这三件正好是 drama-studio 的"题材定位 + 人物关系 + 情节钩子"输入，衔接最顺。移交话术参考 `references/ai-expand-prompt.md` 第四节。

## 资源目录

### references/
- `hook-design.md` — 钩子公式（5 种）+ 生成模板 + 前三句原则 + 正反案例
- `relationship-design.md` — 关系三定律 + 6 大高张力模型 + 关系递进表
- `emotion-curve.md` — 情绪曲线与反转节奏（防中间塌）
- `platform-adapt.md` — 短视频 / 公众号 / 番茄等平台适配
- `hit-checklist.md` — 爆款自检清单与红线
- `examples.md` — **案例库（深度版）**：4 篇完整成稿带逐段拆解 + 从烂到爆对照 + 8 题材速通骨架 + 机检档案
- `hook-arsenal.md` — **弹药库**：50 条开头钩子 + 标题公式 + 20 条收尾金句
- `case-matrix.md` — **案例矩阵**：4 情绪 × 6 关系速查
- `character-builder.md` — **角色速建卡**：主角 / 反派 / 工具人三分钟建模
- `ai-expand-prompt.md` — **AI 扩写提示词模板**：骨架 → 1500 字成品
- `serial-hook.md` — **系列化与续集钩子**：连载 IP 化
- `anti-cliche.md` — **反套路与创新**：避烂俗、踩趋势
- `information-gap.md` — **信息差管理**：三种体验 + 设计三问 + 释放节奏
- `death-causes.md` — **十大死因**：病文 + 诊断 + 处方，写完逐条对照
- `release-kit.md` — **发布三件套**：封面标题 + 黄金前 3 句 + 末句金句一致性 + 四平台 Checklist + 数据回收闭环
- `longform-blueprint.md` — **5万字长-form蓝图**：品类定位+字数分配+长弧结构+人物弧光+伏笔回收表+连贯自检+防崩SOP+章级节拍器，附钟馗民俗诡异宇宙5万字示例大纲
- `cases/` — **纯净范文库**：8 篇完整故事（覆盖 8 个情绪×关系格子）的机检干净版（无拆解注释），可直接模仿 / 搬运

### scripts/
- `structure_check.py` — 结构体检 v3.2：ASCII 情绪曲线 + 塌陷区检测 + 逐句改写建议 + 关系推荐 + 批量检查 + 10 分评分；新增 `--benchmark` 对标拆解模式
- `continuity_check.py` — 连贯性自检 v1.0：扫描 `【伏笔:Vxx 铺设/回收】` 标记揪出悬空/残缺伏笔（防烂尾）+ 章级钩子密度检测（防中段塌陷），长-form 模式配套

---

**使用建议**：本技能是"方法论 + 工具"，不是代写。微小说用 6 步流程搭骨架；5 万字中篇先读 `longform-blueprint.md` 做分卷规划与伏笔表，写作中每章过章级节拍器，收尾跑 `continuity_check.py` 守连贯。需要变成剧本 / 分镜时，移交 `drama-studio`。