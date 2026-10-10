#!/usr/bin/env bash
# short-story-hit 一键安装脚本（Linux / macOS）
# 将 skill/short-story-hit 安装到常见 Agent 平台的 skills 目录。
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SRC="$SCRIPT_DIR/skill/short-story-hit"

echo "== short-story-hit 安装 =="
echo "技能源目录: $SKILL_SRC"
echo ""

# 1) ima.copilot（优先，平台原生注册）
if command -v ima_skill_create >/dev/null 2>&1; then
  echo "[ima] 检测到 ima_skill_create，正在注册技能..."
  ima_skill_create -d "$SKILL_SRC"
  echo ""
fi

# 2) Claude Code
if [ -d "$HOME/.claude/skills" ]; then
  cp -r "$SKILL_SRC" "$HOME/.claude/skills/short-story-hit"
  echo "[Claude Code] 已安装到 ~/.claude/skills/short-story-hit"
fi

# 3) Cursor（用户级 skills 目录，若存在）
if [ -d "$HOME/.cursor/skills" ]; then
  cp -r "$SKILL_SRC" "$HOME/.cursor/skills/short-story-hit"
  echo "[Cursor] 已安装到 ~/.cursor/skills/short-story-hit"
fi

# 4) OpenClaw / 通用 Agent（按 SKILL.md 引用）
if [ -d "$HOME/.openclaw/skills" ]; then
  cp -r "$SKILL_SRC" "$HOME/.openclaw/skills/short-story-hit"
  echo "[OpenClaw] 已安装到 ~/.openclaw/skills/short-story-hit"
fi

echo ""
echo "完成。未检测到的平台目录已跳过。"
echo "提示：SkillHub 用户可手动上传 skill/short-story-hit/ 目录（SKILL.md + references/ + scripts/）。"
