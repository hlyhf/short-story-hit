# 贡献指南（Contributing）

感谢为本项目贡献内容。请遵循以下约定：

## 分支与提交
- 分支命名：`feature/<主题>`、`fix/<问题>`、`docs/<文档>`
- 提交信息：`<类型>: <简述>`，类型 ∈ feat / fix / docs / chore / release
- 版本管理：语义化版本 `主.次.修订`，每次变更同步更新 `CHANGELOG.md`

## 内容规范
1. **双引擎优先**：新增方法必须同时服务于「钩子引擎」或「关系引擎」，避免堆砌无结构经验。
2. **格式铁律**：文档内引用故事用 `正文` 与 `（OS）` 区分；禁止成段未转化的纯心理描写；脚本执行零外部依赖。
3. **字数分层**：微小说 800–2000 字；5 万字中篇按 `longform-blueprint.md` 字数桶分配；用 `scripts/continuity_check.py` 守伏笔回收。
4. **验收**：自检清单见 `skill/short-story-hit/references/hit-checklist.md`；结构体检见 `structure_check.py`。
5. **署名**：凡引用本技能生成的内容，须按 `COPYRIGHT.md` 落「版权：© 灵析剧创 · 智子编辑部 · 版权所有」。
6. **版权**：仓库内容 `© 灵析剧创 · 智子编辑部 · 版权所有`；提交即视为同意 MIT 许可（框架与方法论部分）。

## 提交前自检
```bash
python3 skill/short-story-hit/scripts/structure_check.py examples/sample-story.md   # 跑通结构体检
python3 skill/short-story-hit/scripts/continuity_check.py examples/sample-story.md  # 长-form 连贯自检（如含伏笔标记）
grep -rniE "[A-Z]:\\\\|/Users/|/home/[^/]+" . || echo "无本机绝对路径"              # 可移植性检测
```

## 文件名约定
- `references/` 内方法文档统一用英文小写 + 连字符命名（如 `hook-design.md`）。
- 案例范文统一置于 `references/cases/`，命名 `case_<字母>_<主题>.md`。
