# short-story-hit · 爆款短篇创作技能

> **🌐 Language / 语言**: [中文](README.md) ｜ [English](README.en.md)

> 短篇 / 短故事爆款创作方法论（**钩子 + 关系双引擎**）。把"凭感觉写"变成"按方法论造"。
> 版本：v2.0.0 ｜ 许可：MIT ｜ 多 Agent 通用（ima.copilot / Claude Code / Cursor / SkillHub / OpenClaw …）

---

## 一、特性

- **双引擎**：钩子引擎（5 公式 + 模板 + 前三句原则）+ 关系引擎（三定律 + 6 模型 + 递进表）
- **6 步流程**：锁靶心 → 下钩子 → 排关系 → 设反转 → 收尾钩 → 自检
- **弹药库**：50 条开头钩子 + 标题公式 + 20 条收尾金句
- **案例矩阵**：4 情绪 × 6 关系 速查表
- **角色速建卡 / AI 扩写提示词 / 系列化续集钩子 / 反套路创新**
- **长-form 模式**：5 万字中篇蓝图（长弧结构 + 人物弧光 + 伏笔系统）+ 连贯性自检脚本
- **结构体检脚本**：逐句钩子分析 + 情绪分段 + 关系推荐 + 批量检查 + 10 分评分 + `--benchmark` 对标拆解
- **与 `drama-studio` 的剧本 / 分镜移交协议**（短篇 → 短剧 / 漫剧）

## 二、仓库结构（GitHub 标准）

```
short-story-hit/
├── skill/short-story-hit/        # 技能本体（可上传/注册）
│   ├── SKILL.md                  # 主入口：双引擎心法 + 6步流程 + 决策路由
│   ├── scripts/                  # 自包含工具（纯标准库，零依赖）
│   │   ├── structure_check.py    # 结构体检 v3.2（情绪曲线+逐句建议+评分+benchmark）
│   │   └── continuity_check.py   # 连贯性自检 v1.0（长-form 配套：悬空伏笔+章钩密度）
│   └── references/               # 方法文档（全英文文件名，含 cases/ 纯净范文库）
│       ├── hook-design.md        # 钩子公式 + 模板 + 前三句原则
│       ├── relationship-design.md# 关系三定律 + 6 模型 + 递进表
│       ├── emotion-curve.md      # 情绪曲线与反转节奏
│       ├── platform-adapt.md     # 平台适配
│       ├── hit-checklist.md      # 自检清单与红线
│       ├── examples.md           # 示范案例（逐段拆解 + 从烂到爆对照）
│       ├── hook-arsenal.md       # 弹药库：50钩子+标题+金句
│       ├── case-matrix.md        # 案例矩阵 4×6
│       ├── character-builder.md  # 角色速建卡
│       ├── ai-expand-prompt.md   # AI 扩写提示词
│       ├── serial-hook.md        # 系列化续集钩子
│       ├── anti-cliche.md        # 反套路与创新
│       ├── information-gap.md    # 信息差管理
│       ├── death-causes.md       # 十大死因（病文→诊断→处方）
│       ├── release-kit.md        # 发布三件套 + 平台 Checklist
│       ├── longform-blueprint.md # 5万字长-form 蓝图
│       └── cases/                # 纯净范文库（8 篇，无拆解注释）
├── docs/agent-adapters.md        # 多 Agent 平台适配矩阵（中文）
├── docs/en/agent-adapters.md     # 多 Agent 平台适配矩阵（English）
├── examples/sample-story.md      # 原创格式示范（双引擎演示，非成品）
├── scripts/                      # 安装器（非 skill 内容）
│   ├── install.sh                # Linux/macOS 安装
│   └── install.bat               # Windows 安装
├── LICENSE                       # MIT
├── COPYRIGHT.md                  # 整合版权说明
├── CONTRIBUTING.md               # 贡献指南
├── CHANGELOG.md
├── README.md / README.en.md
```

> 脚本内置在 `skill/short-story-hit/scripts/` 下，保证技能包自包含、零外部路径依赖。

## 三、安装

```bash
# ima.copilot（推荐，平台原生注册）
ima_skill_create -d skill/short-story-hit

# 或跨平台一键安装（Claude Code / Cursor / OpenClaw）
bash scripts/install.sh        # Linux/macOS
scripts\install.bat            # Windows
```

SkillHub 用户：直接上传 `skill/short-story-hit/` 目录（SKILL.md + references/ + scripts/），平台按技能市场规范加载。

## 四、快速使用

按 SKILL.md 的 6 步流程走。写完用脚本质检：

```bash
# 单篇
python3 skill/short-story-hit/scripts/structure_check.py 你的故事.md
# 批量
python3 skill/short-story-hit/scripts/structure_check.py --dir 你的文件夹/
```

长-form（5 万字中篇）写完跑连贯性自检：

```bash
python3 skill/short-story-hit/scripts/continuity_check.py 你的故事.md
```

## 五、版权

- 仓库许可：MIT（见 `LICENSE`），版权归「灵析剧创 · 智子编辑部」（ima.copilot）。
- 产出物署名规则见 `COPYRIGHT.md`。
