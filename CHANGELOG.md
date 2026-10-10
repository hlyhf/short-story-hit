# Changelog

## v2.1.0 (2026-10-10)
- GitHub 标准布局梳理：技能包收进 `skill/short-story-hit/`，Python 工具内置 `skill/short-story-hit/scripts/` 保证自包含。
- 品牌统一：版权人由「狮心善道 · 智子编辑部」统一为「灵析剧创 · 智子编辑部」，与 drama-studio / script-studio 体系一致（`LICENSE` / `COPYRIGHT.md` / `SKILL.md` / `README×2` / `longform-blueprint.md` 同步）。
- 补齐仓库文件：`CONTRIBUTING.md`、`examples/sample-story.md`（双引擎示范）、`docs/agent-adapters.md` 与 `docs/en/agent-adapters.md`（中英双语适配矩阵）、`README.en.md`、`.gitattributes`、更完整 `.gitignore`、`scripts/install.sh` + `install.bat`。
- 修正 `references/*.md` 因目录加深导致的内部链接（`cases/`、`hit-checklist.md`、`../scripts/...`）。
- `README.md` / `README.en.md` 结构图按真实文件树重写（16 篇方法文档 + 8 篇 `cases/` 范文 + 2 个脚本）。

## v2.0.0 (2026-10-08)
- 初始发布（原名 `short-story-hit-longform`）。
- 双引擎方法论：钩子引擎（5 公式 + 模板 + 前三句原则）+ 关系引擎（三定律 + 6 模型 + 递进表）。
- 6 步创作流程：锁靶心 → 下钩子 → 排关系 → 设反转 → 收尾钩 → 自检。
- 16 篇方法文档 + `cases/` 8 篇纯净范文库（覆盖 8 个情绪×关系格子）。
- 长-form 模式：5 万字中篇蓝图（`longform-blueprint.md`）+ 连贯性自检脚本 `continuity_check.py`。
- 结构体检脚本 `structure_check.py` v3.2：ASCII 情绪曲线 + 逐句改写建议 + 关系推荐 + 批量检查 + 10 分评分 + `--benchmark` 对标拆解。
- 与 `drama-studio`（剧创总控）的短篇 → 剧本 / 分镜移交协议。
