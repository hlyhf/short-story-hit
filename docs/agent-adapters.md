# 多 Agent 平台适配矩阵（Agent Adapters）

本仓库 `skill/short-story-hit/` 为通用技能本体，可被多种 Agent 框架加载。
各平台加载方式如下：

| 平台 | 加载方式 | 说明 |
|------|----------|------|
| **ima.copilot** | `ima_skill_create -d skill/short-story-hit` | 平台原生注册，注册后新对话自动生效 |
| **Claude Code** | 拷入 `~/.claude/skills/short-story-hit/` 或引用 `SKILL.md` | `scripts/install.sh` 自动复制 |
| **Cursor** | `~/.cursor/skills/short-story-hit/` 或将 `SKILL.md` 放入 rules | 同上 |
| **SkillHub** | 上传 `skill/short-story-hit/` 目录（SKILL.md + references/ + scripts/） | 按技能市场规范加载 |
| **OpenClaw / 通用 Agent** | `~/.openclaw/skills/short-story-hit/` 或引用 `SKILL.md` | 直接读取 Markdown |

## 渐进式披露（三级加载）

1. **元数据**（name + description）—— 始终在上下文中，用于触发匹配。
2. **SKILL.md 正文** —— 技能触发时加载（双引擎心法 + 6 步流程 + 决策路由）。
3. **references/ 方法文档** —— 按需加载（脚本可直接执行无需加载）。

> 建议 Agent 加载后**先读 SKILL.md**，再按「阶段 + 需求」读对应 reference，不要一次性读入全部 references，以节省上下文。

## 跨平台注意

- 文件名全英文，零绝对路径，零外部依赖（`skill/short-story-hit/scripts/*.py` 仅用 Python 标准库）。
- 产出物署名规则统一见 `COPYRIGHT.md`，不依赖特定 Agent 环境。
- 长-form 模式（5 万字中篇）由 Agent 在立项时与用户确认，并按 `longform-blueprint.md` 做分卷规划。

## 与 drama-studio 的衔接

本技能产出**短篇故事骨架**；若用户要改成剧本 / 分镜（短剧 / 漫剧），移交 `drama-studio`，附带：靶心卡 + 关系递进表 + 反转点标注。
